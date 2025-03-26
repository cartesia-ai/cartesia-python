import asyncio
import json
import typing
import uuid
from collections import defaultdict
from types import TracebackType
from typing import Any, AsyncGenerator, Callable, Dict, List, Optional, Union

import aiohttp

from cartesia.tts.requests import TtsRequestVoiceSpecifierParams
from cartesia.tts.requests.output_format import OutputFormatParams
from cartesia.tts.types import (
    WebSocketResponse,
    WebSocketResponse_Done,
    WebSocketResponse_Error,
    WebSocketResponse_FlushDone,
    WebSocketTtsOutput,
    WordTimestamps,
    PhonemeTimestamps,
)

from ..core.pydantic_utilities import parse_obj_as
from ._websocket import TtsWebsocket
from .types.generation_request import GenerationRequest
from .utils.constants import (
    DEFAULT_MODEL_ID,
    DEFAULT_OUTPUT_FORMAT,
    DEFAULT_VOICE_EMBEDDING,
)
from .utils.tts import get_output_format


class _AsyncTTSContext:
    """Manage a single context over an AsyncWebSocket.

    This class separates sending requests and receiving responses into two separate methods.
    This can be used for sending multiple requests without awaiting the response.
    Then you can listen to the responses in the order they were sent. See README for usage.

    Each AsyncTTSContext will close automatically when a done message is received for that context.
    This happens when the no_more_inputs method is called (equivalent to sending a request with `continue_ = False`),
    or if no requests have been sent for 5 seconds on the same context. It also closes if there is an error.

    """

    def __init__(
        self, context_id: str, websocket: "AsyncTtsWebsocket", timeout: float = 30
    ):
        self._context_id = context_id
        self._websocket = websocket
        self.timeout = timeout
        self._error = None

    @property
    def context_id(self) -> str:
        return self._context_id

    async def send(
        self,
        *,
        model_id: str,
        transcript: str,
        output_format: OutputFormatParams,
        voice: TtsRequestVoiceSpecifierParams,
        context_id: Optional[str] = None,
        duration: Optional[int] = None,
        language: Optional[str] = None,
        stream: bool = True,
        add_timestamps: bool = False,
        add_phoneme_timestamps: bool = False,
        use_original_timestamps: bool = False,
        continue_: bool = False,
        flush: bool = False,
    ) -> None:
        """Send audio generation requests to the WebSocket. The response can be received using the `receive` method.

        Args:
            request: The request to generate audio.

        Returns:
            None.
        """
        await self._websocket.connect()
        assert self._websocket.websocket is not None, "WebSocket is not connected"

        request_body = {
            "model_id": model_id,
            "transcript": transcript,
            "output_format": (
                output_format
                if isinstance(output_format, dict)
                else output_format.dict()
            ),
            "voice": (voice if isinstance(voice, dict) else voice.dict()),
            "context_id": self._context_id,
        }
        if context_id is not None:
            request_body["context_id"] = context_id
        if duration is not None:
            request_body["duration"] = duration
        if language is not None:
            request_body["language"] = language
        if stream:
            request_body["stream"] = stream
        if add_timestamps:
            request_body["add_timestamps"] = add_timestamps
        if add_phoneme_timestamps:
            request_body["add_phoneme_timestamps"] = add_phoneme_timestamps
        if use_original_timestamps:
            request_body["use_original_timestamps"] = use_original_timestamps
        if continue_:
            request_body["continue"] = continue_
        if flush:
            request_body["flush"] = flush

        if (
            "context_id" in request_body
            and request_body["context_id"] is not None
            and request_body["context_id"] != self._context_id
        ):
            raise ValueError(
                "Context ID does not match the context ID of the current context."
            )
        request_body["context_id"] = self._context_id

        if (
            "continue" in request_body
            and request_body["continue"]
            and request_body["transcript"] == ""
            and ("flush" in request_body and not request_body["flush"])
        ):
            raise ValueError("Transcript cannot be empty when continue_ is True.")

        await self._websocket.websocket.send_json(request_body)

        # Start listening for responses on the WebSocket
        self._websocket._dispatch_listener()

    async def no_more_inputs(self) -> None:
        """Send a request to the WebSocket to indicate that no more requests will be sent."""
        await self.send(
            model_id=DEFAULT_MODEL_ID,
            transcript="",
            output_format=get_output_format(DEFAULT_OUTPUT_FORMAT),
            voice={
                "mode": "embedding",
                "embedding": DEFAULT_VOICE_EMBEDDING,
            },
            context_id=self._context_id,
            continue_=False,
        )

    async def flush(self) -> Callable[[], AsyncGenerator[Dict[str, Any], None]]:
        """Trigger a manual flush for the current context's generation. This method returns a generator that yields the audio prior to the flush."""
        await self.send(
            model_id=DEFAULT_MODEL_ID,
            transcript="",
            output_format=get_output_format(DEFAULT_OUTPUT_FORMAT),
            voice={
                "mode": "embedding",
                "embedding": DEFAULT_VOICE_EMBEDDING,
            },
            context_id=self._context_id,
            continue_=True,
            flush=True,
        )

        # Save the old flush ID
        flush_id = len(self._websocket._context_queues[self._context_id]) - 1

        # Create a new Async Queue to store the responses for the new flush ID
        self._websocket._context_queues[self._context_id].append(asyncio.Queue())

        # Return the generator for the old flush ID
        async def generator():
            try:
                while True:
                    response = await self._websocket._get_message(
                        self._context_id, timeout=self.timeout, flush_id=flush_id
                    )
                    response_obj = typing.cast(
                        WebSocketResponse,
                        parse_obj_as(
                            type_=WebSocketResponse, object_=response  # type: ignore
                        ),
                    )
                    if isinstance(response_obj, WebSocketResponse_Error):
                        raise RuntimeError(
                            f"Error generating audio:\n{response_obj.error}"
                        )
                    if isinstance(response_obj, WebSocketResponse_Done) or isinstance(
                        response_obj, WebSocketResponse_FlushDone
                    ):
                        break
                    yield self._websocket._convert_response(
                        response_obj, include_context_id=True
                    )
            except Exception as e:
                if isinstance(e, asyncio.TimeoutError):
                    raise RuntimeError("Timeout while waiting for audio chunk")
                raise RuntimeError(f"Failed to generate audio:\n{e}")

        return generator

    async def receive(self) -> AsyncGenerator[WebSocketTtsOutput, None]:
        """Receive the audio chunks from the WebSocket. This method is a generator that yields audio chunks.

        Returns:
            An async generator that yields audio chunks. Each chunk is a dictionary containing the audio as bytes.
        """
        try:
            while True:
                response = await self._websocket._get_message(
                    self._context_id, timeout=self.timeout
                )
                response_obj = typing.cast(
                    WebSocketResponse,
                    parse_obj_as(
                        type_=WebSocketResponse,  # type: ignore
                        object_=response,
                    ),
                )

                if isinstance(response_obj, WebSocketResponse_Error):
                    raise RuntimeError(f"Error generating audio:\n{response_obj.error}")
                if isinstance(response_obj, WebSocketResponse_Done):
                    break
                yield self._websocket._convert_response(
                    response_obj, include_context_id=True
                )
        except Exception as e:
            if isinstance(e, asyncio.TimeoutError):
                raise RuntimeError("Timeout while waiting for audio chunk")
            raise RuntimeError(f"Failed to generate audio:\n{e}")
        finally:
            self._close()

    async def cancel(self):
        """Cancel the context. This will stop the generation of audio for this context."""
        await self._websocket.websocket.send_json({"context_id": self._context_id, "cancel": True})
        self._close()

    def _close(self) -> None:
        """Closes the context. Automatically called when a done message is received for this context."""
        self._websocket._remove_context(self._context_id)

    def is_closed(self):
        """Check if the context is closed or not. Returns True if closed."""
        return self._context_id not in self._websocket._context_queues

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type: Union[type, None],
        exc: Union[BaseException, None],
        exc_tb: Union[TracebackType, None],
    ):
        self._close()

    def __del__(self):
        self._close()


class AsyncTtsWebsocket(TtsWebsocket):
    """This class contains methods to generate audio using WebSocket asynchronously."""

    def __init__(
        self,
        ws_url: str,
        api_key: str,
        cartesia_version: str,
        get_session: Callable[[], Optional[aiohttp.ClientSession]],
        timeout: float = 30,
    ):
        """
        Args:
            ws_url: The WebSocket URL for the Cartesia API.
            api_key: The API key to use for authorization.
            cartesia_version: The version of the Cartesia API to use.
            timeout: The timeout for responses on the WebSocket in seconds.
            get_session: A function that returns an aiohttp.ClientSession object.
        """
        super().__init__(ws_url, api_key, cartesia_version)
        self.timeout = timeout
        self._get_session = get_session
        self.websocket = None
        self._context_queues: Dict[str, List[asyncio.Queue]] = {}
        self._processing_task: Optional[asyncio.Task] = None

    def __del__(self):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop is None:
            asyncio.run(self.close())
        elif loop.is_running():
            loop.create_task(self.close())

    async def connect(self):
        if self.websocket is None or self._is_websocket_closed():
            route = "tts/websocket"
            session = await self._get_session()
            url = f"{self.ws_url}/{route}?api_key={self.api_key}&cartesia_version={self.cartesia_version}"
            try:
                self.websocket = await session.ws_connect(url)
            except Exception as e:
                # Extract status code if available
                status_code = None
                error_message = str(e)
                
                if hasattr(e, 'status') and e.status is not None:
                    status_code = e.status
                
                    # Create a meaningful error message based on status code
                    if status_code == 402:
                        error_message = "Payment required. Your API key may have insufficient credits or permissions."
                    elif status_code == 401:
                        error_message = "Unauthorized. Please check your API key."
                    elif status_code == 403:
                        error_message = "Forbidden. You don't have permission to access this resource."
                    elif status_code == 404:
                        error_message = "Not found. The requested resource doesn't exist."
                    
                    raise RuntimeError(f"Failed to connect to WebSocket.\nStatus: {status_code}. Error message: {error_message}")
                else:
                    raise RuntimeError(f"Failed to connect to WebSocket at {url}. {e}")

    def _is_websocket_closed(self):
        return self.websocket.closed

    async def close(self):
        """This method closes the websocket connection. *Highly* recommended to call this method when done."""
        if self.websocket is not None and not self._is_websocket_closed():
            await self.websocket.close()
        if self._processing_task:
            self._processing_task.cancel()
            try:
                self._processing_task = None
            except asyncio.CancelledError:
                pass
            except TypeError as e:
                # Ignore the error if the task is already canceled.
                # For some reason we are getting None responses
                # TODO: This needs to be fixed - we need to think about why we are getting None responses.
                if "Received message 256:None" not in str(e):
                    raise e

        for context_id in list(self._context_queues.keys()):
            self._remove_context(context_id)

        self._context_queues.clear()
        self._processing_task = None
        self.websocket = None

    async def send(
        self,
        *,
        model_id: str,
        transcript: str,
        output_format: OutputFormatParams,
        voice: TtsRequestVoiceSpecifierParams,
        context_id: Optional[str] = None,
        duration: Optional[int] = None,
        language: Optional[str] = None,
        stream: bool = True,
        add_timestamps: bool = False,
        add_phoneme_timestamps: bool = False,
        use_original_timestamps: bool = False,
    ):
        """See :meth:`_WebSocket.send` for details."""
        if context_id is None:
            context_id = str(uuid.uuid4())

        ctx = self.context(context_id)

        await ctx.send(
            model_id=model_id,
            transcript=transcript,
            output_format=output_format,
            voice=voice,
            context_id=context_id,
            duration=duration,
            language=language,
            continue_=False,
            add_timestamps=add_timestamps,
            add_phoneme_timestamps=add_phoneme_timestamps,
            use_original_timestamps=use_original_timestamps,
        )

        generator = ctx.receive()

        if stream:
            return generator

        chunks: typing.List[str] = []
        words: typing.List[str] = []
        start: typing.List[float] = []
        end: typing.List[float] = []
        phonemes: typing.List[str] = []
        phoneme_start: typing.List[float] = []
        phoneme_end: typing.List[float] = []
        async for chunk in generator:
            if chunk.audio is not None:
                chunks.append(chunk.audio)
            if add_timestamps and chunk.word_timestamps is not None:
                if chunk.word_timestamps is not None:
                    words.extend(chunk.word_timestamps.words)
                    start.extend(chunk.word_timestamps.start)
                    end.extend(chunk.word_timestamps.end)
            if add_phoneme_timestamps and chunk.phoneme_timestamps is not None:
                if chunk.phoneme_timestamps is not None:
                    phonemes.extend(chunk.phoneme_timestamps.phonemes)
                    phoneme_start.extend(chunk.phoneme_timestamps.start)
                    phoneme_end.extend(chunk.phoneme_timestamps.end)

        return WebSocketTtsOutput(
            audio=b"".join(chunks),  # type: ignore
            context_id=context_id,
            word_timestamps=(
                WordTimestamps(
                    words=words,
                    start=start,
                    end=end,
                )
                if add_timestamps
                else None
            ),
            phoneme_timestamps=(
                PhonemeTimestamps(
                    phonemes=phonemes,
                    start=phoneme_start,
                    end=phoneme_end,
                )
                if add_phoneme_timestamps
                else None
            ),
        )

    async def _process_responses(self):
        try:
            while True:
                response = await self.websocket.receive_json()
                if response["context_id"]:
                    context_id = response["context_id"]
                flush_id = response.get("flush_id", -1)
                if context_id in self._context_queues:
                    await self._context_queues[context_id][flush_id].put(response)
        except Exception as e:
            self._error = e
            raise e

    async def _get_message(
        self, context_id: str, timeout: float, flush_id: int = -1
    ) -> Dict[str, Any]:
        if context_id not in self._context_queues:
            raise ValueError(f"Context ID {context_id} not found.")
        if len(self._context_queues[context_id]) <= flush_id:
            raise ValueError(
                f"Flush ID {flush_id} not found for context ID {context_id}."
            )
        return await asyncio.wait_for(
            self._context_queues[context_id][flush_id].get(), timeout=timeout
        )

    def _remove_context(self, context_id: str):
        if context_id in self._context_queues:
            del self._context_queues[context_id]

    def _dispatch_listener(self):
        if self._processing_task is None or self._processing_task.done():
            self._processing_task = asyncio.create_task(self._process_responses())

    def context(self, context_id: Optional[str] = None):
        if context_id in self._context_queues:
            raise ValueError(
                f"AsyncContext for context ID {context_id} already exists."
            )
        if context_id is None:
            context_id = str(uuid.uuid4())
        if context_id not in self._context_queues:
            self._context_queues[context_id] = [asyncio.Queue()]
        return _AsyncTTSContext(context_id, self, self.timeout)
