import base64
from collections import defaultdict
import json
import typing
import httpx
import uuid

from .utils.timeout_iterator import TimeoutIterator
from .types.output_format import OutputFormat
from .types.web_socket_tts_request import WebSocketTtsRequest
from .types.web_socket_tts_output import WebSocketTtsOutput
from .types.tts_request_voice_specifier import TtsRequestVoiceSpecifier
from .types.web_socket_response import (
    WebSocketResponse,
    WebSocketResponse_Chunk,
    WebSocketResponse_Error,
    WebSocketResponse_Done,
    WebSocketResponse_Timestamp,
)
from ..core.pydantic_utilities import parse_obj_as

try:
    from websockets.sync.client import connect

    IS_WEBSOCKET_SYNC_AVAILABLE = True
except ImportError:
    IS_WEBSOCKET_SYNC_AVAILABLE = False

from .client import TtsClient, AsyncTtsClient


class TtsConnectOptions(typing.TypedDict, total=False):
    cartesia_version: typing.Optional[str]

    api_key: typing.Optional[str]


class _TTSContext:
    """Manage a single context over a WebSocket.

    This class can be used to stream inputs, as they become available, to a specific `context_id`. See README for usage.

    See :class:`_AsyncTTSContext` for asynchronous use cases.

    Each TTSContext will close automatically when a done message is received for that context. It also closes if there is an error.
    """

    def __init__(self, context_id: str, websocket: typing.Any):
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
        model_id: str,
        transcript: typing.Iterator[str],
        output_format: OutputFormat,
        voice: TtsRequestVoiceSpecifier,
        context_id: typing.Optional[str] = None,
        duration: typing.Optional[int] = None,
        language: typing.Optional[str] = None,
        add_timestamps: bool = False,
    ) -> typing.Generator[bytes, None, None]:
        """Send audio generation requests to the WebSocket and yield responses.

        Args:
            model_id: The ID of the model to use for generating audio.
            transcript: Iterator over text chunks with <1s latency.
            output_format: A dictionary containing the details of the output format.
            voice_id: The ID of the voice to use for generating audio.
            voice_embedding: The embedding of the voice to use for generating audio.
            context_id: The context ID to use for the request. If not specified, a random context ID will be generated.
            duration: The duration of the audio in seconds.
            language: The language code for the audio request. This can only be used with `model_id = sonic-multilingual`
            add_timestamps: Whether to return word-level timestamps.
            _experimental_voice_controls: Experimental voice controls for controlling speed and emotion.
                Note: This is an experimental feature and may change rapidly in future releases.

        Yields:
            Dictionary containing the following key(s):
            - audio: The audio as bytes.
            - context_id: The context ID for the request.

        Raises:
            ValueError: If provided context_id doesn't match the current context.
            RuntimeError: If there's an error generating audio.
        """
        if context_id is not None and context_id != self._context_id:
            raise ValueError("Context ID does not match the context ID of the current context.")

        self._websocket.connect()

        # Create the initial request body
        request_body = WebSocketTtsRequest(
            model_id=model_id,
            transcript=transcript,
            output_format=output_format,
            voice=voice,
            duration=duration,
            language=language,
            context_id=self._context_id,
            add_timestamps=add_timestamps,
        ).dict()

        try:
            # Create an iterator with a timeout to get text chunks
            text_iterator = TimeoutIterator(transcript, timeout=0.001)  # 1ms timeout for nearly non-blocking receive
            next_chunk = next(text_iterator, None)

            while True:
                # Send the next text chunk to the WebSocket if available
                if next_chunk is not None and next_chunk != text_iterator.get_sentinel():
                    request_body["transcript"] = next_chunk
                    request_body["continue"] = True
                    self._websocket._send(request_body)
                    next_chunk = next(text_iterator, None)

                try:
                    # Receive responses from the WebSocket with a small timeout
                    response_obj = typing.cast(
                        WebSocketResponse,
                        parse_obj_as(
                            type_=WebSocketResponse,  # type: ignore
                            object_=json.loads(self._websocket.recv(timeout=0.001)),
                        ),
                    )
                    if hasattr(response_obj, "context_id") and response_obj.context_id != self._context_id:
                        pass
                    if isinstance(response_obj, WebSocketResponse_Error):
                        raise RuntimeError(f"Error generating audio:\n{response_obj.error}")
                    if isinstance(response_obj, WebSocketResponse_Done):
                        break
                    if isinstance(response_obj, WebSocketResponse_Chunk) and response_obj.data:
                        yield self._websocket._convert_response(response_obj=response_obj, include_context_id=True)
                except TimeoutError:
                    pass

                # Continuously receive from WebSocket until the next text chunk is available
                while next_chunk == text_iterator.get_sentinel():
                    try:
                        response_obj = typing.cast(
                            WebSocketResponse,
                            parse_obj_as(
                                type_=WebSocketResponse,  # type: ignore
                                object_=json.loads(self._websocket.recv(timeout=0.001)),
                            ),
                        )
                        if hasattr(response_obj, "context_id") and response_obj.context_id != self._context_id:
                            continue
                        if isinstance(response_obj, WebSocketResponse_Error):
                            raise RuntimeError(f"Error generating audio:\n{response_obj.error}")
                        if isinstance(response_obj, WebSocketResponse_Done):
                            break
                        if isinstance(response_obj, WebSocketResponse_Chunk) and response_obj.data:
                            yield self._websocket._convert_response(response_obj=response_obj, include_context_id=True)
                    except TimeoutError:
                        pass
                    next_chunk = next(text_iterator, None)

                # Send final message if all input text chunks are exhausted
                if next_chunk is None:
                    request_body["transcript"] = ""
                    request_body["continue"] = False
                    self._websocket._send(request_body)
                    break

            # Receive remaining messages from the WebSocket until "done" is received
            while True:
                response_obj = typing.cast(
                    WebSocketResponse,
                    parse_obj_as(
                        type_=WebSocketResponse,  # type: ignore
                        object_=json.loads(self._websocket.recv(timeout=0.001)),
                    ),
                )
                if hasattr(response_obj, "context_id") and response_obj.context_id != self._context_id:
                    continue
                if isinstance(response_obj, WebSocketResponse_Error):
                    raise RuntimeError(f"Error generating audio:\n{response_obj.error}")
                if isinstance(response_obj, WebSocketResponse_Done):
                    break
                yield self._websocket._convert_response(response_obj=response_obj, include_context_id=True)

        except Exception as e:
            self._websocket.close()
            raise RuntimeError(f"Failed to generate audio. {e}")

    def _close(self):
        """Closes the context. Automatically called when a done message is received for this context."""
        self._websocket._remove_context(self._context_id)

    def is_closed(self):
        """Check if the context is closed or not. Returns True if closed."""
        return self._context_id not in self._websocket._contexts


class TtsWebsocketConnection:
    def __init__(
        self,
        *,
        ws_url,
        tts_connect_options,
    ):
        self.ws_url = ws_url
        self.options = tts_connect_options
        self.websocket = None
        self._contexts = set()

    def __del__(self):
        try:
            self.close()
        except Exception as e:
            raise RuntimeError("Failed to close WebSocket: ", e)
    
    def _send(self, data: typing.Any) -> None:
        if isinstance(data, dict):
            data = json.dumps(data)
        self.websocket.send(data)

    def _construct_ws_uri(self):
        query_params = httpx.QueryParams()

        query_params = query_params.add("api_key", self.options.get("api_key"))
        query_params = query_params.add("cartesia_version", self.options.get("cartesia_version"))
        route = "tts/websocket"
        return f"{self.ws_url}/{route}?{query_params}"

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
            try:
                self.websocket = connect(self._construct_ws_uri())
            except Exception as e:
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
        self, response_obj: typing.Union[WebSocketResponse_Chunk, WebSocketResponse_Timestamp], include_context_id: bool
    ) -> WebSocketTtsOutput:
        out: dict[str, typing.Any] = {}
        if isinstance(response_obj, WebSocketResponse_Chunk):
            out["audio"] = base64.b64decode(response_obj.data)
        elif isinstance(response_obj, WebSocketResponse_Timestamp):
            out["word_timestamps"] = response_obj.word_timestamps

        if include_context_id:
            out["context_id"] = response_obj.context_id

        return WebSocketTtsOutput(**out)

    def send(
        self,
        model_id: str,
        transcript: str,
        output_format: OutputFormat,
        voice: TtsRequestVoiceSpecifier,
        context_id: typing.Optional[str] = None,
        duration: typing.Optional[int] = None,
        language: typing.Optional[str] = None,
        stream: bool = True,
        add_timestamps: bool = False,
    ) -> WebSocketTtsOutput:
        """Send a request to the WebSocket to generate audio.

        Args:
            model_id: The ID of the model to use for generating audio.
            transcript: The text to convert to speech.
            output_format: A dictionary containing the details of the output format.
            voice_id: The ID of the voice to use for generating audio.
            voice_embedding: The embedding of the voice to use for generating audio.
            context_id: The context ID to use for the request. If not specified, a random context ID will be generated.
            duration: The duration of the audio in seconds.
            language: The language code for the audio request. This can only be used with `model_id = sonic-multilingual`
            stream: Whether to stream the audio or not.
            add_timestamps: Whether to return word-level timestamps.
            _experimental_voice_controls: Experimental voice controls for controlling speed and emotion.
                Note: This is an experimental feature and may change rapidly in future releases.

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

        request_body = WebSocketTtsRequest(
            model_id=model_id,
            transcript=transcript,
            output_format=output_format,
            voice=voice,
            context_id=context_id,
            duration=duration,
            language=language,
            add_timestamps=add_timestamps,
        ).dict()

        generator = self._websocket_generator(request_body)

        if stream:
            return generator

        chunks = []
        word_timestamps = defaultdict(list)
        for chunk in generator:
            if "audio" in chunk:
                chunks.append(chunk["audio"])
            if add_timestamps and "word_timestamps" in chunk:
                for k, v in chunk["word_timestamps"].items():
                    word_timestamps[k].extend(v)
        out: dict[str, typing.Any] = {"audio": b"".join(chunks), "context_id": context_id}
        if add_timestamps:
            out["word_timestamps"] = word_timestamps
        return WebSocketTtsOutput(**out)

    def _websocket_generator(self, request_body: typing.Dict[str, typing.Any]):
        self._send(request_body)

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
                yield self._convert_response(response_obj=response_obj, include_context_id=True)
        except Exception as e:
            # Close the websocket connection if an error occurs.
            self.close()
            raise RuntimeError(f"Failed to generate audio. {response_obj}. Exception {e}")

    def _remove_context(self, context_id: str):
        if context_id in self._contexts:
            self._contexts.remove(context_id)

    def context(self, context_id: typing.Optional[str] = None) -> _TTSContext:
        if context_id in self._contexts:
            raise ValueError(f"Context for context ID {context_id} already exists.")
        if context_id is None:
            context_id = str(uuid.uuid4())
        if context_id not in self._contexts:
            self._contexts.add(context_id)
        return _TTSContext(context_id, self)


class TtsClientWithWebsocket(TtsClient):
    def __init__(self, *, client_wrapper):
        super().__init__(client_wrapper=client_wrapper)

    def _ws_url(self):
        base_url = self._client_wrapper.get_base_url()
        if base_url.startswith("ws://") or base_url.startswith("wss://"):
            return base_url
        else:
            prefix = "ws" if "localhost" in base_url else "wss"
            base_url_without_protocol = base_url.split("://")[-1]
            return f"{prefix}://{base_url_without_protocol}"

    def websocket(self) -> TtsWebsocketConnection:
        client_headers = self._client_wrapper.get_headers()
        tts_connect_options = TtsConnectOptions(
            cartesia_version=client_headers["Cartesia-Version"], api_key=client_headers["X-API-Key"]
        )
        return TtsWebsocketConnection(
            ws_url=self._ws_url(),
            tts_connect_options=tts_connect_options,
        )


class AsyncTtsClientWithWebsocket(AsyncTtsClient):
    def __init__(self, *, client_wrapper):
        super().__init__(client_wrapper=client_wrapper)

    def websocket(self) -> None:
        raise NotImplementedError(
            "The websocket at `.tts` is only available on the `Cartesia`, not this asynchronous client (`AsyncCartesia`)."
        )
