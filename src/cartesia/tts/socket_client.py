import asyncio
import base64
import json
import typing
import uuid
from collections import defaultdict

import httpx
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK

from ..core.pydantic_utilities import parse_obj_as
from .types.cancel_context_request import CancelContextRequest
from .types.generation_request import GenerationRequest
from .types.web_socket_request import WebSocketRequest
from .types.web_socket_response import (
    WebSocketResponse,
    WebSocketResponse_Chunk,
    WebSocketResponse_Done,
    WebSocketResponse_Error,
    WebSocketResponse_PhonemeTimestamps,
    WebSocketResponse_Timestamps,
)
from .types.web_socket_tts_output import WebSocketTtsOutput

try:
    from websockets.client import WebSocketClientProtocol
    from websockets.client import connect as async_ws_connect

    IS_WEBSOCKET_ASYNC_AVAILABLE = True
except ImportError:
    IS_WEBSOCKET_ASYNC_AVAILABLE = False
try:
    from websockets.sync.client import connect

    IS_WEBSOCKET_SYNC_AVAILABLE = True
except ImportError:
    IS_WEBSOCKET_SYNC_AVAILABLE = False

from .client import AsyncTtsClient, TtsClient


class TtsConnectOptions(typing.TypedDict, total=False):
    cartesia_version: typing.Optional[str]
    api_key: typing.Optional[str]


def _construct_ws_uri(base_url: str, route: str, options: TtsConnectOptions) -> str:
    """
    Builds the WebSocket URI with query parameters.
    """
    query_params = httpx.QueryParams()

    api_key = options.get("api_key")
    cartesia_version = options.get("cartesia_version")

    if api_key:
        query_params = query_params.add("api_key", api_key)
    if cartesia_version:
        query_params = query_params.add("cartesia_version", cartesia_version)

    return f"{base_url}/{route}?{query_params}"


def _decode_and_build_output(
    response_obj: typing.Union[
        WebSocketResponse_Chunk,
        WebSocketResponse_Timestamps,
        WebSocketResponse_PhonemeTimestamps,
    ],
    include_context_id: bool = True,
) -> WebSocketTtsOutput:
    """
    Converts a parsed WebSocketResponse object into a WebSocketTtsOutput
    with the binary audio data decoded, or timestamps, etc.
    """
    out: typing.Dict[str, typing.Any] = {}

    if isinstance(response_obj, WebSocketResponse_Chunk) and response_obj.data:
        out["audio"] = base64.b64decode(response_obj.data)
    elif isinstance(response_obj, WebSocketResponse_Timestamps):
        out["word_timestamps"] = response_obj.word_timestamps
    elif isinstance(response_obj, WebSocketResponse_PhonemeTimestamps):
        out["phoneme_timestamps"] = response_obj.phoneme_timestamps

    if include_context_id:
        out["context_id"] = response_obj.context_id

    return WebSocketTtsOutput(**out)


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

    @property
    def context_id(self) -> str:
        return self._context_id

    def send(
        self,
        request: WebSocketRequest,
    ) -> typing.Generator[bytes, None, None]:
        """
        Handle both GenerationRequest and CancelContextRequest via a single WebSocketRequest object.
        Yields audio chunks (as bytes) when generating speech.
        """

        if isinstance(request, CancelContextRequest):
            if request.context_id != self._context_id:
                raise ValueError(
                    f"Context ID {request.context_id} does not match current context {self._context_id}."
                )
            self._websocket.connect()
            self._websocket._send(request.dict(by_alias=True))

            try:
                while True:
                    response_str = self._websocket.recv(timeout=0.5)
                    if not response_str:
                        break
                    response_obj = json.loads(response_str)

                    if response_obj.get("type") == "Done":
                        break
                    if response_obj.get("type") == "Error":
                        raise RuntimeError(f"Error cancelling context: {response_obj}")

            except TimeoutError:
                pass
            finally:
                self._websocket.close()

            return

        if isinstance(request, GenerationRequest):
            if request.context_id != self._context_id:
                raise ValueError(
                    f"Context ID {request.context_id} does not match current context {self._context_id}."
                )

            self._websocket.connect()

            request_body = request.dict(by_alias=True)
            text_iterator = iter([request.transcript])
            next_chunk = next(text_iterator, None)

            try:
                while True:
                    if next_chunk:
                        request_body["transcript"] = next_chunk
                        request_body["continue"] = request.continue_ or False
                        self._websocket._send(request_body)
                        next_chunk = next(text_iterator, None)

                    try:
                        response_str = self._websocket.recv(timeout=0.001)
                        if response_str:
                            response_obj = typing.cast(
                                WebSocketResponse,
                                parse_obj_as(
                                    type_=WebSocketResponse,  # type: ignore
                                    object_=json.loads(
                                        self._websocket.recv(timeout=0.001)
                                    ),
                                ),
                            )
                            if isinstance(response_obj, WebSocketResponse_Error):
                                raise RuntimeError(
                                    f"Error generating audio:\n{response_obj.error}"
                                )
                            if isinstance(response_obj, WebSocketResponse_Done):
                                break
                            if (
                                isinstance(response_obj, WebSocketResponse_Chunk)
                                and response_obj.data
                            ):
                                yield self._websocket._convert_response(
                                    response_obj=response_obj, include_context_id=True
                                )
                    except TimeoutError:
                        pass

                    if next_chunk is None:
                        request_body["transcript"] = ""
                        request_body["continue"] = False
                        self._websocket._send(request_body)
                        break

                while True:
                    response_str = self._websocket.recv(timeout=0.001)
                    if not response_str:
                        break
                    response_obj = typing.cast(
                        WebSocketResponse,
                        parse_obj_as(
                            type_=WebSocketResponse,  # type: ignore
                            object_=json.loads(self._websocket.recv(timeout=0.001)),
                        ),
                    )
                    if isinstance(response_obj, WebSocketResponse_Error):
                        raise RuntimeError(
                            f"Error generating audio:\n{response_obj.error}"
                        )
                    if isinstance(response_obj, WebSocketResponse_Done):
                        break
                    if (
                        isinstance(response_obj, WebSocketResponse_Chunk)
                        and response_obj.data
                    ):
                        yield self._websocket._convert_response(
                            response_obj=response_obj, include_context_id=True
                        )

            except Exception as e:
                self._websocket.close()
                raise RuntimeError(f"Failed to generate audio. {e}")

            self._websocket.close()

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

    def _send(self, data: typing.Any) -> None:
        """
        Send data as JSON over the WebSocket.
        """
        if isinstance(data, dict):
            data = json.dumps(data)
        self.websocket.send(data)

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
                self.websocket = connect(
                    _construct_ws_uri(self.ws_url, "tts/websocket", self.options)
                )
            except Exception as e:
                raise RuntimeError(f"Failed to connect to WebSocket. {e}")

    def _is_websocket_closed(self):
        """
        Check if the WebSocket connection is closed.
        """
        return self.websocket.socket.fileno() == -1

    def close(self):
        """This method closes the WebSocket connection. *Highly* recommended to call this method when done using the WebSocket."""
        if self.websocket and not self._is_websocket_closed():
            self.websocket.close()

        if self._contexts:
            self._contexts.clear()

    def _convert_response(
        self,
        response_obj: typing.Union[
            WebSocketResponse_Chunk,
            WebSocketResponse_Timestamps,
            WebSocketResponse_PhonemeTimestamps,
        ],
        include_context_id: bool,
    ) -> WebSocketTtsOutput:
        """
        Converts a parsed WebSocketResponse object into a WebSocketTtsOutput
        with the binary audio data decoded, or timestamps, etc.
        """
        return _decode_and_build_output(response_obj, include_context_id)

    def send(
        self,
        request: WebSocketRequest,
        stream: bool = True,
    ):
        """
        Send either a GenerationRequest or a CancelContextRequest to the TTS WebSocket.

        If `stream` is True, returns a generator of audio chunks (dict).
        Otherwise, returns a single dict with all audio concatenated.

        For a CancelContextRequest, there is typically no audio returned.
        """

        self.connect()

        if isinstance(request, CancelContextRequest):
            try:
                self._websocket_generator(request.dict(by_alias=True))
            except TimeoutError:
                pass
            finally:
                self.close()

            return {"status": "cancelled", "context_id": request.context_id}

        if isinstance(request, GenerationRequest):
            if not request.context_id:
                request.context_id = str(uuid.uuid4())

            request_body = request.dict(by_alias=True)

            generator = self._websocket_generator(request_body)

            if stream:
                return generator

    def _websocket_generator(self, request_body: typing.Dict[str, typing.Any]):
        """
        Send a request to the TTS WebSocket and yield responses as they arrive.
        """
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
                if isinstance(
                    response_obj,
                    (
                        WebSocketResponse_Chunk,
                        WebSocketResponse_Timestamps,
                        WebSocketResponse_PhonemeTimestamps,
                    ),
                ):
                    yield self._convert_response(
                        response_obj=response_obj, include_context_id=True
                    ).dict()
        except Exception as e:
            self.close()
            raise RuntimeError(f"Failed to generate audio. Exception {e}")

    def _accumulate_chunks(
        self,
        request: GenerationRequest,
        generator: typing.Generator[dict, None, None],
    ) -> dict:
        """
        Accumulate audio chunks and timestamps into a single dict.
        """
        chunks = []
        word_timestamps = defaultdict(list)
        context_id = request.context_id

        try:
            for chunk in generator:
                if "audio" in chunk:
                    chunks.append(chunk["audio"])
                if request.add_timestamps and "word_timestamps" in chunk:
                    for k, v in chunk["word_timestamps"].items():
                        word_timestamps[k].extend(v)
        except Exception as e:
            self.close()
            raise RuntimeError(f"Failed to generate audio. Exception: {e}")

        audio_bytes = b"".join(chunks)
        out_dict: typing.Dict[str, typing.Any] = {
            "audio": audio_bytes,
            "context_id": context_id,
        }
        if request.add_timestamps:
            out_dict["word_timestamps"] = word_timestamps

        return out_dict

    def _remove_context(self, context_id: str):
        """
        Remove a context from the active set.
        """
        if context_id in self._contexts:
            self._contexts.remove(context_id)

    def context(self, context_id: typing.Optional[str] = None) -> _TTSContext:
        """
        Create or retrieve a synchronous TTS context object with the given context_id.
        """
        if context_id in self._contexts:
            raise ValueError(f"Context for context ID {context_id} already exists.")
        if context_id is None:
            context_id = str(uuid.uuid4())
        if context_id not in self._contexts:
            self._contexts.add(context_id)
        return _TTSContext(context_id, self)


class _AsyncTTSContext:
    def __init__(
        self,
        context_id: str,
        websocket_connection: "AsyncTtsWebsocketConnection",
    ):
        self._context_id = context_id
        self._connection = websocket_connection

    @property
    def context_id(self) -> str:
        return self._context_id

    async def send(
        self,
        request: WebSocketRequest,
    ) -> typing.AsyncGenerator[bytes, None]:
        """
        Send either a GenerationRequest or a CancelContextRequest to the TTS WebSocket.
        """
        if request.context_id != self._context_id:
            raise ValueError(
                f"Context ID {request.context_id} does not match "
                f"current context {self._context_id}."
            )

        if isinstance(request, CancelContextRequest):
            await self._connection._ensure_connected()
            await self._connection._send(request.dict(by_alias=True))

            try:
                while True:
                    response_str = await self._connection._recv_with_optional_timeout()
                    if not response_str:
                        break

                    response_obj = json.loads(response_str)
                    if response_obj.get("type") == "Done":
                        break
                    if response_obj.get("type") == "Error":
                        raise RuntimeError(f"Error cancelling context: {response_obj}")
            except TimeoutError:
                pass
            finally:
                await self._close()

            return

        if isinstance(request, GenerationRequest):
            await self._connection._ensure_connected()

            request_body = request.dict(by_alias=True)
            await self._connection._send(request_body)

            try:
                while True:
                    response_str = await self._connection._recv_with_optional_timeout()
                    if not response_str:
                        continue

                    response_obj = typing.cast(
                        WebSocketResponse,
                        parse_obj_as(
                            type_=WebSocketResponse,  # type: ignore
                            object_=json.loads(response_str),
                        ),
                    )

                    if isinstance(response_obj, WebSocketResponse_Error):
                        raise RuntimeError(
                            f"Error generating audio:\n{response_obj.error}"
                        )
                    if isinstance(response_obj, WebSocketResponse_Done):
                        break

                    if isinstance(
                        response_obj,
                        (
                            WebSocketResponse_Chunk,
                            WebSocketResponse_Timestamps,
                            WebSocketResponse_PhonemeTimestamps,
                        ),
                    ):
                        output = self._connection._convert_response(
                            response_obj, include_context_id=True
                        )
                        if output.audio:
                            yield output.audio

            except Exception as e:
                raise RuntimeError(f"Failed to generate audio. {e}")
            finally:
                await self._close()

    async def _close(self):
        """Remove this context from the active set.
        If no more contexts remain, close the socket."""
        self._connection._remove_context(self._context_id)
        if not self._connection._contexts:
            await self._connection.close()

    def is_closed(self) -> bool:
        return self._context_id not in self._connection._contexts


class AsyncTtsWebsocketConnection:
    """
    Asynchronous WebSocket TTS connection. Parallels TtsWebsocketConnection but uses `websockets` in async mode.
    """

    def __init__(
        self,
        *,
        ws_url: str,
        tts_connect_options: TtsConnectOptions,
    ):
        self.ws_url = ws_url
        self.options = tts_connect_options
        self.websocket: typing.Optional[WebSocketClientProtocol] = None
        self._contexts: typing.Set[str] = set()

    async def _ensure_connected(self):
        """
        Ensure the WebSocket connection is established.
        """
        if not IS_WEBSOCKET_ASYNC_AVAILABLE:
            raise ImportError(
                "The asynchronous WebSocket client is not available. "
                "Please ensure that you have 'websockets>=10.0' installed."
            )

        if self.websocket is None or self.websocket.closed:
            try:
                uri = _construct_ws_uri(self.ws_url, "tts/websocket", self.options)
                self.websocket = await async_ws_connect(uri)
            except Exception as e:
                raise RuntimeError(f"Failed to connect to WebSocket. {e}") from e

    async def close(self):
        """
        Close the WebSocket connection completely. Recommended to call this when done.
        """
        if self.websocket and not self.websocket.closed:
            await self.websocket.close()
        self.websocket = None
        self._contexts.clear()

    async def close_context(self, context_id: str):
        """
        Remove a context from the active set. If no contexts remain, optionally close the connection.
        """
        self._remove_context(context_id)

    async def _send(self, data: typing.Any) -> None:
        """
        Send data as JSON over the WebSocket.
        """
        await self._ensure_connected()
        if not self.websocket:
            raise RuntimeError("WebSocket is not connected after _ensure_connected().")

        if isinstance(data, dict):
            data = json.dumps(data)
        await self.websocket.send(data)

    async def _recv_with_optional_timeout(
        self, timeout: float = 0.5
    ) -> typing.Optional[str]:
        """
        Attempt to receive data from the websocket with a short timeout.
        If no data arrives, returns None.
        """
        if not self.websocket or self.websocket.closed:
            return None

        try:
            msg: typing.Union[str, bytes] = await asyncio.wait_for(
                self.websocket.recv(), timeout=timeout
            )
            if isinstance(msg, bytes):
                msg = msg.decode("utf-8")
            return msg

        except asyncio.TimeoutError:
            return None
        except (ConnectionClosedOK, ConnectionClosedError):
            return None

    def _convert_response(
        self,
        response_obj: typing.Union[
            WebSocketResponse_Chunk,
            WebSocketResponse_Timestamps,
            WebSocketResponse_PhonemeTimestamps,
        ],
        include_context_id: bool,
    ) -> WebSocketTtsOutput:
        """
        Converts a parsed WebSocketResponse object into a WebSocketTtsOutput
        with the binary audio data decoded, or timestamps, etc.
        """
        return _decode_and_build_output(response_obj, include_context_id)

    def _remove_context(self, context_id: str):
        """
        Remove a context from the active set.
        """
        if context_id in self._contexts:
            self._contexts.remove(context_id)

    def context(self, context_id: typing.Optional[str] = None) -> _AsyncTTSContext:
        """
        Create or retrieve an asynchronous TTS context object with the given context_id.
        """
        if context_id is None:
            context_id = str(uuid.uuid4())
        if context_id in self._contexts:
            raise ValueError(f"Context for context ID {context_id} already exists.")
        self._contexts.add(context_id)
        return _AsyncTTSContext(context_id, self)

    async def send(
        self,
        request: WebSocketRequest,
        stream: bool = True,
    ) -> typing.Union[
        typing.AsyncGenerator[typing.Dict[str, typing.Any], None],
        typing.Dict[str, typing.Any],
    ]:
        """
        Send either a GenerationRequest or a CancelContextRequest to the TTS WebSocket.

        If `stream` is True, returns an async generator of audio chunks (dict).
        Otherwise, returns a single dict with all audio concatenated.

        For a CancelContextRequest, there is typically no audio returned.
        """
        await self._ensure_connected()

        if isinstance(request, CancelContextRequest):
            try:
                self._async_websocket_generator(request.dict(by_alias=True))
            except TimeoutError:
                pass
            finally:
                self.close()

            return {"status": "cancelled", "context_id": request.context_id}

        if isinstance(request, GenerationRequest):
            if not request.context_id:
                request.context_id = str(uuid.uuid4())

            request_body = request.dict(by_alias=True)

            generator = self._async_websocket_generator(request_body)

            if stream:
                return generator

            return await self._accumulate_chunks(request, generator)

        raise ValueError("Unknown request type for TTS WebSocket.")

    async def _async_websocket_generator(
        self, request_body: dict
    ) -> typing.AsyncGenerator[dict, None]:
        """
        Send a request to the TTS WebSocket and yield responses as they arrive.
        """
        await self._send(request_body)

        try:
            while True:
                response_str = await self._recv_with_optional_timeout()
                if not response_str:
                    continue

                response_obj = typing.cast(
                    WebSocketResponse,
                    parse_obj_as(
                        type_=WebSocketResponse,  # type: ignore
                        object_=json.loads(response_str),
                    ),
                )

                if isinstance(response_obj, WebSocketResponse_Error):
                    raise RuntimeError(f"Error generating audio:\n{response_obj.error}")
                if isinstance(response_obj, WebSocketResponse_Done):
                    break

                if isinstance(
                    response_obj,
                    (
                        WebSocketResponse_Chunk,
                        WebSocketResponse_Timestamps,
                        WebSocketResponse_PhonemeTimestamps,
                    ),
                ):
                    yield self._convert_response(
                        response_obj, include_context_id=True
                    ).dict()
        except Exception as e:
            await self.close()
            raise RuntimeError(f"Failed to generate audio. Exception: {e}")

    async def _accumulate_chunks(
        self,
        request: GenerationRequest,
        generator: typing.AsyncGenerator[dict, None],
    ) -> dict:
        """
        Accumulate audio chunks and timestamps into a single dict.
        """
        chunks = []
        word_timestamps = defaultdict(list)
        context_id = request.context_id

        try:
            async for chunk in generator:
                if "audio" in chunk:
                    chunks.append(chunk["audio"])
                if request.add_timestamps and "word_timestamps" in chunk:
                    for k, v in chunk["word_timestamps"].items():
                        word_timestamps[k].extend(v)
        except Exception as e:
            await self.close()
            raise RuntimeError(f"Failed to generate audio. Exception: {e}")

        audio_bytes = b"".join(chunks)
        out_dict: typing.Dict[str, typing.Any] = {
            "audio": audio_bytes,
            "context_id": context_id,
        }
        if request.add_timestamps:
            out_dict["word_timestamps"] = dict(word_timestamps)

        return out_dict


class TtsClientWithWebsocket(TtsClient):
    """
    Extension of TtsClient that supports a synchronous WebSocket TTS connection.
    """

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
            cartesia_version=client_headers["Cartesia-Version"],
            api_key=client_headers["X-API-Key"],
        )
        return TtsWebsocketConnection(
            ws_url=self._ws_url(),
            tts_connect_options=tts_connect_options,
        )


class AsyncTtsClientWithWebsocket(AsyncTtsClient):
    """
    Extension of AsyncTtsClient that supports an asynchronous WebSocket TTS connection.
    """

    def __init__(self, *, client_wrapper):
        super().__init__(client_wrapper=client_wrapper)

    def _ws_url(self) -> str:
        base_url = self._client_wrapper.get_base_url()
        if base_url.startswith("ws://") or base_url.startswith("wss://"):
            return base_url
        else:
            prefix = "ws" if "localhost" in base_url else "wss"
            base_url_without_protocol = base_url.split("://")[-1]
            return f"{prefix}://{base_url_without_protocol}"

    def websocket(self) -> AsyncTtsWebsocketConnection:
        client_headers = self._client_wrapper.get_headers()
        tts_connect_options = TtsConnectOptions(
            cartesia_version=client_headers.get("Cartesia-Version"),
            api_key=client_headers.get("X-API-Key"),
        )
        return AsyncTtsWebsocketConnection(
            ws_url=self._ws_url(),
            tts_connect_options=tts_connect_options,
        )
