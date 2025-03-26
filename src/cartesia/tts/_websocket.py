import base64
import json
import typing
import uuid
from collections import defaultdict
from typing import Any, Dict, Generator, Optional, Set, Union

try:
    from websockets.sync.client import connect

    IS_WEBSOCKET_SYNC_AVAILABLE = True
except ImportError:
    IS_WEBSOCKET_SYNC_AVAILABLE = False

from iterators import TimeoutIterator  # type: ignore

from cartesia.tts.requests import TtsRequestVoiceSpecifierParams
from cartesia.tts.requests.output_format import OutputFormatParams
from cartesia.tts.types import (
    WebSocketResponse,
    WebSocketResponse_Chunk,
    WebSocketResponse_Done,
    WebSocketResponse_Error,
    WebSocketResponse_FlushDone,
    WebSocketResponse_PhonemeTimestamps,
    WebSocketResponse_Timestamps,
    WebSocketTtsOutput,
    WordTimestamps,
    PhonemeTimestamps,
)

from ..core.pydantic_utilities import parse_obj_as
from .types.generation_request import GenerationRequest


class _TTSContext:
    """Manage a single context over a WebSocket.

    This class can be used to stream inputs, as they become available, to a specific `context_id`. See README for usage.

    See :class:`_AsyncTTSContext` for asynchronous use cases.

    Each TTSContext will close automatically when a done message is received for that context. It also closes if there is an error.
    """

    def __init__(self, context_id: str, websocket: "TtsWebsocket"):
        self._context_id = context_id
        self._websocket = websocket
        self._error = None

    def __del__(self):
        self._close()

    @property
    def context_id(self) -> str:
        return self._context_id

    def send(
        self,
        *,
        model_id: str,
        transcript: typing.Generator[str, None, None],
        output_format: OutputFormatParams,
        voice: TtsRequestVoiceSpecifierParams,
        context_id: Optional[str] = None,
        duration: Optional[int] = None,
        language: Optional[str] = None,
        stream: bool = True,
        add_timestamps: bool = False,
        add_phoneme_timestamps: bool = False,
        use_original_timestamps: bool = False,
    ) -> Generator[bytes, None, None]:
        """Send audio generation requests to the WebSocket and yield responses.

        Args:
            request: The request to generate audio.

        Yields:
            Dictionary containing the following key(s):
            - audio: The audio as bytes.
            - context_id: The context ID for the request.

        Raises:
            ValueError: If provided context_id doesn't match the current context.
            RuntimeError: If there's an error generating audio.
        """
        self._websocket.connect()
        assert self._websocket.websocket is not None, "WebSocket is not connected"

        request_body = {
            "model_id": model_id,
            "transcript": transcript,
            "output_format": output_format,
            "voice": voice,
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

        if (
            "context_id" in request_body
            and request_body["context_id"] is not None
            and request_body["context_id"] != self._context_id
        ):
            raise ValueError(
                "Context ID does not match the context ID of the current context."
            )

        try:
            text_iterator = TimeoutIterator(request_body["transcript"], timeout=0.001)
            next_chunk = next(text_iterator, None)

            while True:
                # Send the next text chunk to the WebSocket if available
                if (
                    next_chunk is not None
                    and next_chunk != text_iterator.get_sentinel()
                ):
                    request_body["transcript"] = next_chunk
                    request_body["continue"] = True
                    self._websocket.websocket.send(json.dumps(request_body))
                    next_chunk = next(text_iterator, None)

                try:
                    # Receive responses from the WebSocket with a small timeout
                    response_obj = typing.cast(
                        WebSocketResponse,
                        parse_obj_as(
                            type_=WebSocketResponse,  # type: ignore
                            object_=json.loads(
                                self._websocket.websocket.recv(timeout=0.001)
                            ),
                        ),
                    )
                    if response_obj.context_id != self._context_id:
                        pass
                    if isinstance(response_obj, WebSocketResponse_Error):
                        raise RuntimeError(
                            f"Error generating audio:\n{response_obj.error}"
                        )
                    if isinstance(response_obj, WebSocketResponse_Done):
                        break
                    if (
                        isinstance(response_obj, WebSocketResponse_Chunk)
                        or isinstance(response_obj, WebSocketResponse_Timestamps)
                        or isinstance(response_obj, WebSocketResponse_PhonemeTimestamps)
                    ):
                        yield self._websocket._convert_response(
                            response_obj, include_context_id=True
                        )
                except TimeoutError:
                    pass

                # Continuously receive from WebSocket until the next text chunk is available
                while next_chunk == text_iterator.get_sentinel():
                    try:
                        response_obj = typing.cast(
                            WebSocketResponse,
                            parse_obj_as(
                                type_=WebSocketResponse,  # type: ignore
                                object_=json.loads(
                                    self._websocket.websocket.recv(timeout=0.001)
                                ),
                            ),
                        )
                        if response_obj.context_id != self._context_id:
                            continue
                        if isinstance(response_obj, WebSocketResponse_Error):
                            raise RuntimeError(
                                f"Error generating audio:\n{response_obj.error}"
                            )
                        if isinstance(response_obj, WebSocketResponse_Done):
                            break
                        if (
                            isinstance(response_obj, WebSocketResponse_Chunk)
                            or isinstance(response_obj, WebSocketResponse_Timestamps)
                            or isinstance(
                                response_obj, WebSocketResponse_PhonemeTimestamps
                            )
                        ):
                            yield self._websocket._convert_response(
                                response_obj, include_context_id=True
                            )
                    except TimeoutError:
                        pass
                    next_chunk = next(text_iterator, None)

                # Send final message if all input text chunks are exhausted
                if next_chunk is None:
                    request_body["transcript"] = ""
                    request_body["continue"] = False
                    self._websocket.websocket.send(json.dumps(request_body))
                    break

            # Receive remaining messages from the WebSocket until "done" is received
            while True:
                response_obj = typing.cast(
                    WebSocketResponse,
                    parse_obj_as(
                        type_=WebSocketResponse,  # type: ignore
                        object_=json.loads(self._websocket.websocket.recv()),
                    ),
                )
                if response_obj.context_id != self._context_id:
                    continue
                if isinstance(response_obj, WebSocketResponse_Error):
                    raise RuntimeError(f"Error generating audio:\n{response_obj.error}")
                if isinstance(response_obj, WebSocketResponse_Done):
                    break
                yield self._websocket._convert_response(
                    response_obj, include_context_id=True
                )

        except Exception as e:
            self._websocket.close()
            raise RuntimeError(f"Failed to generate audio. {e}")

    def _close(self):
        """Closes the context. Automatically called when a done message is received for this context."""
        self._websocket._remove_context(self._context_id)

    def is_closed(self):
        """Check if the context is closed or not. Returns True if closed."""
        return self._context_id not in self._websocket._contexts


class TtsWebsocket:
    """This class contains methods to generate audio using WebSocket. Ideal for low-latency audio generation.

    Usage:
        >>> ws = client.tts.websocket()
        >>> generation_request = GenerationRequest(
        ...     model_id="sonic-2",
        ...     transcript="Hello world!",
        ...     voice_embedding=embedding
        ...     output_format={"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100}
        ...     context_id=context_id,
        ...     stream=True
        ... )
        >>> for audio_chunk in ws.send(generation_request):
        ...     audio = audio_chunk["audio"]
    """

    def __init__(
        self,
        ws_url: str,
        api_key: str,
        cartesia_version: str,
    ):
        self.ws_url = ws_url
        self.api_key = api_key
        self.cartesia_version = cartesia_version
        self.websocket = None
        self._contexts: Set[str] = set()

    def __del__(self):
        try:
            self.close()
        except Exception as e:
            raise RuntimeError("Failed to close WebSocket: ", e)

    def connect(self):
        """This method connects to the WebSocket if it is not already connected.

        Raises:
            RuntimeError: If the connection to the WebSocket fails.
        """
        if not IS_WEBSOCKET_SYNC_AVAILABLE:
            raise ImportError(
                "The synchronous WebSocket client is not available. Please ensure that you have 'websockets>=12.0' or compatible version installed."
            )
        if self.websocket is None or self._is_websocket_closed():
            route = "tts/websocket"
            try:
                self.websocket = connect(
                    f"{self.ws_url}/{route}?api_key={self.api_key}&cartesia_version={self.cartesia_version}"
                )
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
                    raise RuntimeError(f"Failed to connect to WebSocket. {e}")

    def _is_websocket_closed(self):
        return self.websocket.socket.fileno() == -1

    def close(self):
        """This method closes the WebSocket connection. *Highly* recommended to call this method when done using the WebSocket."""
        if self.websocket and not self._is_websocket_closed():
            self.websocket.close()

        if self._contexts:
            self._contexts.clear()

    def _convert_response(
        self,
        response: typing.Union[
            WebSocketResponse_Chunk,
            WebSocketResponse_Timestamps,
            WebSocketResponse_PhonemeTimestamps,
            WebSocketResponse_FlushDone,
        ],
        include_context_id: bool,
        include_flush_id: bool = False,
    ) -> WebSocketTtsOutput:
        out = {}
        if isinstance(response, WebSocketResponse_Chunk):
            out["audio"] = base64.b64decode(response.data)
        elif isinstance(response, WebSocketResponse_Timestamps):
            out["word_timestamps"] = response.word_timestamps  # type: ignore
        elif isinstance(response, WebSocketResponse_PhonemeTimestamps):
            out["phoneme_timestamps"] = response.phoneme_timestamps  # type: ignore
        elif include_flush_id and isinstance(response, WebSocketResponse_FlushDone):
            out["flush_done"] = response.flush_done  # type: ignore
            out["flush_id"] = response.flush_id  # type: ignore

        if include_context_id and response.context_id:
            out["context_id"] = response.context_id  # type: ignore

        return WebSocketTtsOutput(**out)  # type: ignore

    def send(
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
        """Send a request to the WebSocket to generate audio.

        Args:
            request: The request to generate audio.
            stream: Whether to stream the audio or not.

        Returns:
            If `stream` is True, the method returns a generator that yields chunks. Each chunk is a dictionary.
            If `stream` is False, the method returns a dictionary.
            Both the generator and the dictionary contain the following key(s):
            - audio: The audio as bytes.
            - context_id: The context ID for the request.
        """
        self.connect()

        if context_id is None:
            context_id = str(uuid.uuid4())

        request_body = {
            "model_id": model_id,
            "transcript": transcript,
            "output_format": output_format,
            "voice": voice,
            "context_id": context_id,
            "duration": duration,
            "language": language,
            "stream": stream,
            "add_timestamps": add_timestamps,
            "add_phoneme_timestamps": add_phoneme_timestamps,
            "use_original_timestamps": use_original_timestamps,
        }
        generator = self._websocket_generator(request_body)

        if stream:
            return generator

        chunks: typing.List[str] = []
        words: typing.List[str] = []
        start: typing.List[float] = []
        end: typing.List[float] = []
        phonemes: typing.List[str] = []
        phoneme_start: typing.List[float] = []
        phoneme_end: typing.List[float] = []
        for chunk in generator:
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

    def _websocket_generator(self, request_body: Dict[str, Any]):
        assert self.websocket is not None, "WebSocket is not connected"
        self.websocket.send(json.dumps(request_body))

        try:
            while True:
                response_obj = typing.cast(
                    WebSocketResponse,
                    parse_obj_as(
                        type_=WebSocketResponse,  # type: ignore
                        object_=json.loads(self.websocket.recv()),
                    ),
                )
                if isinstance(response_obj, WebSocketResponse_Error):
                    raise RuntimeError(f"Error generating audio:\n{response_obj.error}")
                if isinstance(response_obj, WebSocketResponse_Done):
                    break
                yield self._convert_response(response_obj, include_context_id=True)
        except Exception as e:
            # Close the websocket connection if an error occurs.
            self.close()
            raise RuntimeError(f"Failed to generate audio. {e}") from e

    def _remove_context(self, context_id: str):
        if context_id in self._contexts:
            self._contexts.remove(context_id)

    def context(self, context_id: Optional[str] = None):
        if context_id in self._contexts:
            raise ValueError(f"Context for context ID {context_id} already exists.")
        if context_id is None:
            context_id = str(uuid.uuid4())
        if context_id not in self._contexts:
            self._contexts.add(context_id)
        return _TTSContext(context_id, self)
