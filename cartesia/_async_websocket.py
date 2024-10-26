import asyncio
import uuid
from collections import defaultdict
from types import TracebackType
from typing import Any, AsyncGenerator, Callable, Dict, List, Optional, Union

import aiohttp

from cartesia._constants import DEFAULT_MODEL_ID, DEFAULT_VOICE_EMBEDDING
from cartesia._types import OutputFormat, VoiceControls
from cartesia._websocket import _WebSocket
from cartesia.tts import TTS
from cartesia.utils.tts import _construct_tts_request


class _AsyncTTSContext:
    """Manage a single context over an AsyncWebSocket.

    This class separates sending requests and receiving responses into two separate methods.
    This can be used for sending multiple requests without awaiting the response.
    Then you can listen to the responses in the order they were sent. See README for usage.

    Each AsyncTTSContext will close automatically when a done message is received for that context.
    This happens when the no_more_inputs method is called (equivalent to sending a request with `continue_ = False`),
    or if no requests have been sent for 5 seconds on the same context. It also closes if there is an error.

    """

    def __init__(self, context_id: str, websocket: "_AsyncWebSocket", timeout: float):
        self._context_id = context_id
        self._websocket = websocket
        self.timeout = timeout
        self._error = None

    @property
    def context_id(self) -> str:
        return self._context_id

    async def send(
        self,
        model_id: str,
        transcript: str,
        output_format: OutputFormat,
        voice_id: Optional[str] = None,
        voice_embedding: Optional[List[float]] = None,
        context_id: Optional[str] = None,
        continue_: bool = False,
        duration: Optional[int] = None,
        language: Optional[str] = None,
        add_timestamps: bool = False,
        _experimental_voice_controls: Optional[VoiceControls] = None,
    ) -> None:
        """Send audio generation requests to the WebSocket. The response can be received using the `receive` method.

        Args:
            model_id: The ID of the model to use for generating audio.
            transcript: The text to convert to speech.
            output_format: A dictionary containing the details of the output format.
            voice_id: The ID of the voice to use for generating audio.
            voice_embedding: The embedding of the voice to use for generating audio.
            context_id: The context ID to use for the request. If not specified, a random context ID will be generated.
            continue_: Whether to continue the audio generation from the previous transcript or not.
            duration: The duration of the audio in seconds.
            language: The language code for the audio request. This can only be used with `model_id = sonic-multilingual`.
            add_timestamps: Whether to return word-level timestamps.
            _experimental_voice_controls: Experimental voice controls for controlling speed and emotion.
                Note: This is an experimental feature and may change rapidly in future releases.

        Returns:
            None.
        """
        if context_id is not None and context_id != self._context_id:
            raise ValueError("Context ID does not match the context ID of the current context.")
        if continue_ and transcript == "":
            raise ValueError("Transcript cannot be empty when continue_ is True.")

        await self._websocket.connect()

        request_body = _construct_tts_request(
            model_id=model_id,
            transcript=transcript,
            output_format=output_format,
            voice_id=voice_id,
            voice_embedding=voice_embedding,
            duration=duration,
            language=language,
            context_id=self._context_id,
            add_timestamps=add_timestamps,
            continue_=continue_,
            _experimental_voice_controls=_experimental_voice_controls,
        )

        await self._websocket.websocket.send_json(request_body)

        # Start listening for responses on the WebSocket
        self._websocket._dispatch_listener()

    async def no_more_inputs(self) -> None:
        """Send a request to the WebSocket to indicate that no more requests will be sent."""
        await self.send(
            model_id=DEFAULT_MODEL_ID,
            transcript="",
            output_format=TTS.get_output_format("raw_pcm_f32le_44100"),
            voice_embedding=DEFAULT_VOICE_EMBEDDING,  # Default voice embedding since it's a required input for now.
            context_id=self._context_id,
            continue_=False,
        )

    async def receive(self) -> AsyncGenerator[Dict[str, Any], None]:
        """Receive the audio chunks from the WebSocket. This method is a generator that yields audio chunks.

        Returns:
            An async generator that yields audio chunks. Each chunk is a dictionary containing the audio as bytes.
        """
        try:
            while True:
                response = await self._websocket._get_message(
                    self._context_id, timeout=self.timeout
                )
                if "error" in response:
                    raise RuntimeError(f"Error generating audio:\n{response['error']}")
                if response["done"]:
                    break
                yield self._websocket._convert_response(response, include_context_id=True)
        except Exception as e:
            if isinstance(e, asyncio.TimeoutError):
                raise RuntimeError("Timeout while waiting for audio chunk")
            raise RuntimeError(f"Failed to generate audio:\n{e}")
        finally:
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


class _AsyncWebSocket(_WebSocket):
    """This class contains methods to generate audio using WebSocket asynchronously."""

    def __init__(
        self,
        ws_url: str,
        api_key: str,
        cartesia_version: str,
        timeout: float,
        get_session: Callable[[], Optional[aiohttp.ClientSession]],
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
        self._context_queues: Dict[str, asyncio.Queue] = {}
        self._processing_task: asyncio.Task = None

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
                # Ignore the error if the task is already cancelled
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
        model_id: str,
        transcript: str,
        output_format: OutputFormat,
        voice_id: Optional[str] = None,
        voice_embedding: Optional[List[float]] = None,
        context_id: Optional[str] = None,
        duration: Optional[int] = None,
        language: Optional[str] = None,
        stream: bool = True,
        add_timestamps: bool = False,
        _experimental_voice_controls: Optional[VoiceControls] = None,
    ) -> Union[bytes, AsyncGenerator[bytes, None]]:
        """See :meth:`_WebSocket.send` for details."""
        if context_id is None:
            context_id = str(uuid.uuid4())

        ctx = self.context(context_id)

        await ctx.send(
            model_id=model_id,
            transcript=transcript,
            output_format=output_format,
            voice_id=voice_id,
            voice_embedding=voice_embedding,
            context_id=context_id,
            duration=duration,
            language=language,
            continue_=False,
            add_timestamps=add_timestamps,
            _experimental_voice_controls=_experimental_voice_controls,
        )

        generator = ctx.receive()

        if stream:
            return generator

        chunks = []
        word_timestamps = defaultdict(list)
        async for chunk in generator:
            if "audio" in chunk:
                chunks.append(chunk["audio"])
            if add_timestamps and "word_timestamps" in chunk:
                for k, v in chunk["word_timestamps"].items():
                    word_timestamps[k].extend(v)
        out = {"audio": b"".join(chunks), "context_id": context_id}
        if add_timestamps:
            out["word_timestamps"] = word_timestamps
        return out

    async def _process_responses(self):
        try:
            while True:
                response = await self.websocket.receive_json()
                if response["context_id"]:
                    context_id = response["context_id"]
                if context_id in self._context_queues:
                    await self._context_queues[context_id].put(response)
        except Exception as e:
            self._error = e
            raise e

    async def _get_message(self, context_id: str, timeout: float) -> Dict[str, Any]:
        if context_id not in self._context_queues:
            raise ValueError(f"Context ID {context_id} not found.")
        return await asyncio.wait_for(self._context_queues[context_id].get(), timeout=timeout)

    def _remove_context(self, context_id: str):
        if context_id in self._context_queues:
            del self._context_queues[context_id]

    def _dispatch_listener(self):
        if self._processing_task is None or self._processing_task.done():
            self._processing_task = asyncio.create_task(self._process_responses())

    def context(self, context_id: Optional[str] = None) -> _AsyncTTSContext:
        if context_id in self._context_queues:
            raise ValueError(f"AsyncContext for context ID {context_id} already exists.")
        if context_id is None:
            context_id = str(uuid.uuid4())
        if context_id not in self._context_queues:
            self._context_queues[context_id] = asyncio.Queue()
        return _AsyncTTSContext(context_id, self, self.timeout)
