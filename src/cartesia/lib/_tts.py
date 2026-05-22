# FIXME: Delete this code and use Stainless to generate a WebSocket method for v4.
#
# See [v3.1.0-b3](https://github.com/cartesia-ai/cartesia-python/releases/tag/v3.1.0-b3)
# for how we can simplify our interfaces
# and use generated code without modification to avoid a maintenance headache.

from __future__ import annotations

import json
import uuid
import queue
import asyncio
import logging
from types import TracebackType
from typing import TYPE_CHECKING, Any, Union, Mapping, Iterator, Optional, cast
from typing_extensions import AsyncIterator

import httpx
from pydantic import BaseModel

from .._types import Omit, Query, Headers, omit
from .._utils import maybe_transform, async_maybe_transform
from .._models import construct_type_unchecked
from .._exceptions import CartesiaError
from .._base_client import _merge_mappings
from ..types.model_speed import ModelSpeed
from ..types.supported_language import SupportedLanguage
from ..types.websocket_response import WebsocketResponse
from ..types.voice_specifier_param import VoiceSpecifierParam
from ..types.websocket_client_event import CancelContextRequest, WebsocketClientEvent
from ..types.generation_config_param import GenerationConfigParam
from ..types.raw_output_format_param import RawOutputFormatParam
from ..types.generation_request_param import GenerationRequestParam
from ..types.websocket_client_event_param import WebsocketClientEventParam
from ..types.websocket_connection_options import WebsocketConnectionOptions

if TYPE_CHECKING:
    from websockets.sync.client import ClientConnection as WebsocketConnection
    from websockets.asyncio.client import ClientConnection as AsyncWebsocketConnection

    from .._client import Cartesia, AsyncCartesia


class AsyncTTSResourceConnection:
    """Represents a live WebSocket connection to the TTS API"""

    _connection: AsyncWebsocketConnection

    def __init__(
        self, connection: AsyncWebsocketConnection, manager: Optional[AsyncTTSResourceConnectionManager] = None
    ) -> None:
        self._connection = connection
        self._manager = manager
        self._context_queues: dict[str, asyncio.Queue[WebsocketResponse]] = {}
        self._processing_task: Optional[asyncio.Task[None]] = None
        self._closing = False
        self._logger = logging.getLogger(__name__)

    async def __aiter__(self) -> AsyncIterator[WebsocketResponse]:
        """
        An infinite-iterator that will continue to yield events until
        the connection is closed.
        """
        from websockets.exceptions import ConnectionClosedOK

        try:
            while True:
                yield await self.recv()
        except ConnectionClosedOK:
            return

    async def recv(self) -> WebsocketResponse:
        """
        Receive the next message from the connection and parses it into a `WebsocketResponse` object.

        Canceling this method is safe. There's no risk of losing data.
        """
        return self.parse_event(await self.recv_bytes())

    async def recv_bytes(self, timeout: Optional[float] = None) -> bytes:
        """Receive the next message from the connection as raw bytes.

        Canceling this method is safe. There's no risk of losing data.

        If you want to parse the message into a `WebsocketResponse` object like `.recv()` does,
        then you can call `.parse_event(data)`.
        """
        if timeout is not None:
            import asyncio as _asyncio

            message = await _asyncio.wait_for(self._connection.recv(decode=False), timeout=timeout)
        else:
            message = await self._connection.recv(decode=False)
        self._logger.debug(f"Received websocket message: %s", message)
        return message

    async def send(self, event: Union[WebsocketClientEvent, WebsocketClientEventParam]) -> None:
        await self._ensure_connected()
        data = (
            event.to_json(use_api_names=True, exclude_defaults=True, exclude_unset=True)
            if isinstance(event, BaseModel)
            else json.dumps(await async_maybe_transform(event, WebsocketClientEventParam))
        )
        await self._connection.send(data)

    async def close(self, *, code: int = 1000, reason: str = "") -> None:
        import asyncio as _asyncio

        self._closing = True
        try:
            if self._processing_task is not None:
                self._processing_task.cancel()
                try:
                    await self._processing_task
                except _asyncio.CancelledError:
                    pass
                self._processing_task = None
            await self._connection.close(code=code, reason=reason)
        finally:
            self._closing = False

    def _dispatch_listener(self) -> None:
        import asyncio as _asyncio

        if self._processing_task is None or self._processing_task.done():
            self._processing_task = _asyncio.create_task(self._process_responses())

    async def _process_responses(self) -> None:
        from websockets.exceptions import ConnectionClosed

        try:
            while True:
                raw = await self._connection.recv(decode=False)
                self._logger.debug("Received websocket message: %s", raw)
                event = self.parse_event(raw)
                event_ctx = event.context_id if hasattr(event, "context_id") else None
                if event_ctx is not None and event_ctx in self._context_queues:
                    await self._context_queues[event_ctx].put(event)
                else:
                    self._logger.debug("Received event for unregistered context %s", event_ctx)
        except ConnectionClosed:
            if not self._closing:
                self._logger.warning("WebSocket connection closed unexpectedly")

    async def _ensure_connected(self) -> None:
        import asyncio as _asyncio

        from websockets.protocol import State

        if self._manager is not None and self._connection.state in (State.CLOSED, State.CLOSING):
            self._logger.debug("Connection is not open (state=%s), reconnecting...", self._connection.state)
            if self._processing_task is not None:
                self._processing_task.cancel()
                try:
                    await self._processing_task
                except _asyncio.CancelledError:
                    pass
                self._processing_task = None
            new_conn = await self._manager.__aenter__()
            self._connection = new_conn._connection
            self._context_queues.clear()

    def parse_event(self, data: Union[str, bytes]) -> WebsocketResponse:
        """
        Converts a raw `str` or `bytes` message into a `WebsocketResponse` object.

        This is helpful if you're using `.recv_bytes()`.
        """
        return cast(
            WebsocketResponse, construct_type_unchecked(value=json.loads(data), type_=cast(Any, WebsocketResponse))
        )

    def context(
        self,
        context_id: Optional[str] = None,
        *,
        timeout: Optional[float] = None,
        model_id: Optional[str] = None,
        voice: Optional[VoiceSpecifierParam] = None,
        output_format: Union[RawOutputFormatParam, Mapping[str, Any], None] = None,
        language: Optional[SupportedLanguage] = None,
        add_timestamps: Optional[bool] = None,
        add_phoneme_timestamps: Optional[bool] = None,
        generation_config: Optional[GenerationConfigParam] = None,
        max_buffer_delay_ms: Optional[int] = None,
        pronunciation_dict_id: Optional[str] = None,
        use_normalized_timestamps: Optional[bool] = None,
    ) -> AsyncWebSocketContext:
        """Create a context helper for managing conversational flows.

        Args:
            context_id: Unique identifier for this context. If not provided,
                a UUID will be auto-generated.
            model_id: Default model_id for push().
            voice: Default voice for push().
            output_format: Default output_format for push().
            language: Default language for push().
            add_timestamps: Default add_timestamps for push().
            add_phoneme_timestamps: Default add_phoneme_timestamps for push().
            generation_config: Default generation_config for push().
            max_buffer_delay_ms: Default generation_config for push().
            pronunciation_dict_id: Default generation_config for push().
            use_normalized_timestamps: Default generation_config for push().

        Returns:
            AsyncWebSocketContext helper for simplified sending and receiving
        """
        if context_id is not None and context_id in self._context_queues:
            raise ValueError(f"Context for context ID {context_id} already exists.")
        if context_id is None:
            context_id = str(uuid.uuid4())
        import asyncio

        self._context_queues[context_id] = asyncio.Queue()
        return AsyncWebSocketContext(
            self,
            context_id,
            timeout=timeout,
            model_id=model_id,
            voice=voice,
            output_format=output_format,
            language=language,
            add_timestamps=add_timestamps,
            add_phoneme_timestamps=add_phoneme_timestamps,
            generation_config=generation_config,
            max_buffer_delay_ms=max_buffer_delay_ms,
            pronunciation_dict_id=pronunciation_dict_id,
            use_normalized_timestamps=use_normalized_timestamps,
        )


class AsyncTTSResourceConnectionManager:
    """
    Context manager over a `AsyncTTSResourceConnection` that is returned by `tts.websocket_connect()`

    This context manager ensures that the connection will be closed when it exits.

    ---

    Note that if your application doesn't work well with the context manager approach then you
    can call the `.enter()` method directly to initiate a connection.

    **Warning**: You must remember to close the connection with `.close()`.

    ```py
    connection = await client.tts.websocket_connect(...).enter()
    # ...
    await connection.close()
    ```
    """

    def __init__(
        self,
        *,
        client: AsyncCartesia,
        extra_query: Query,
        extra_headers: Headers,
        websocket_connection_options: WebsocketConnectionOptions,
    ) -> None:
        self.__client = client
        self.__connection: Optional[AsyncTTSResourceConnection] = None
        self.__extra_query = extra_query
        self.__extra_headers = extra_headers
        self.__websocket_connection_options = websocket_connection_options
        self.__lock = asyncio.Lock()
        self._logger = logging.getLogger(__name__)

    async def __aenter__(self) -> AsyncTTSResourceConnection:
        """
        👋 If your application doesn't work well with the context manager approach then you
        can call this method directly to initiate a connection.

        **Warning**: You must remember to close the connection with `.close()`.

        ```py
        connection = await client.tts.websocket_connect(...).enter()
        # ...
        await connection.close()
        ```
        """
        async with self.__lock:
            if self.__connection is not None:
                return self.__connection

            try:
                from websockets.asyncio.client import connect
            except ImportError as exc:
                raise CartesiaError("You need to install `cartesia[websockets]` to use this method") from exc

            url = self._prepare_url().copy_with(
                params={
                    **self.__client.base_url.params,
                    **self.__extra_query,
                },
            )
            self._logger.debug("Connecting to %s", url)
            if self.__websocket_connection_options:
                self._logger.debug("Connection options: %s", self.__websocket_connection_options)

            self.__connection = AsyncTTSResourceConnection(
                await connect(
                    str(url),
                    user_agent_header=self.__client.user_agent,
                    additional_headers=_merge_mappings(
                        {
                            **self.__client.auth_headers,
                            "Cartesia-Version": self.__client.default_headers.get("cartesia-version", "2025-11-04"),
                        },
                        self.__extra_headers,
                    ),
                    **self.__websocket_connection_options,
                ),
                manager=self,
            )

            return self.__connection

    enter = __aenter__

    def _prepare_url(self) -> httpx.URL:
        if self.__client.websocket_base_url is not None:
            base_url = httpx.URL(self.__client.websocket_base_url)
        else:
            base_url = self.__client._base_url.copy_with(scheme="wss")

        merge_raw_path = base_url.raw_path.rstrip(b"/") + b"/tts/websocket"
        return base_url.copy_with(raw_path=merge_raw_path)

    async def __aexit__(
        self, exc_type: Optional[type[BaseException]], exc: Optional[BaseException], exc_tb: Optional[TracebackType]
    ) -> None:
        if self.__connection is not None:
            await self.__connection.close()


class TTSResourceConnection:
    """Represents a live WebSocket connection to the TTS API"""

    _connection: WebsocketConnection

    def __init__(self, connection: WebsocketConnection, manager: Optional[TTSResourceConnectionManager] = None) -> None:
        self._connection = connection
        self._manager = manager
        self._context_queues: dict[str, queue.Queue[WebsocketResponse]] = {}
        self._logger = logging.getLogger(__name__)

    def __iter__(self) -> Iterator[WebsocketResponse]:
        """
        An infinite-iterator that will continue to yield events until
        the connection is closed.
        """
        from websockets.exceptions import ConnectionClosedOK

        try:
            while True:
                yield self.recv()
        except ConnectionClosedOK:
            return

    def recv(self) -> WebsocketResponse:
        """
        Receive the next message from the connection and parses it into a `WebsocketResponse` object.

        Canceling this method is safe. There's no risk of losing data.
        """
        return self.parse_event(self.recv_bytes())

    def recv_bytes(self, timeout: Optional[float] = None) -> bytes:
        """Receive the next message from the connection as raw bytes.

        Canceling this method is safe. There's no risk of losing data.

        If you want to parse the message into a `WebsocketResponse` object like `.recv()` does,
        then you can call `.parse_event(data)`.
        """
        message = self._connection.recv(decode=False, timeout=timeout)
        self._logger.debug(f"Received websocket message: %s", message)
        return message

    def send(self, event: Union[WebsocketClientEvent, WebsocketClientEventParam]) -> None:
        self._ensure_connected()
        data = (
            event.to_json(use_api_names=True, exclude_defaults=True, exclude_unset=True)
            if isinstance(event, BaseModel)
            else json.dumps(maybe_transform(event, WebsocketClientEventParam))
        )
        self._connection.send(data)

    def close(self, *, code: int = 1000, reason: str = "") -> None:
        self._connection.close(code=code, reason=reason)

    def _ensure_connected(self) -> None:
        from websockets.protocol import State

        if self._manager is not None and self._connection.state in (State.CLOSED, State.CLOSING):
            self._logger.debug("Connection is not open (state=%s), reconnecting...", self._connection.state)
            new_conn = self._manager.__enter__()
            self._connection = new_conn._connection
            self._context_queues.clear()

    def parse_event(self, data: Union[str, bytes]) -> WebsocketResponse:
        """
        Converts a raw `str` or `bytes` message into a `WebsocketResponse` object.

        This is helpful if you're using `.recv_bytes()`.
        """
        return cast(
            WebsocketResponse, construct_type_unchecked(value=json.loads(data), type_=cast(Any, WebsocketResponse))
        )

    def context(
        self,
        context_id: Optional[str] = None,
        *,
        timeout: Optional[float] = None,
        model_id: Optional[str] = None,
        voice: Optional[VoiceSpecifierParam] = None,
        output_format: Union[RawOutputFormatParam, Mapping[str, Any], None] = None,
        language: Optional[SupportedLanguage] = None,
        add_timestamps: Optional[bool] = None,
        add_phoneme_timestamps: Optional[bool] = None,
        generation_config: Optional[GenerationConfigParam] = None,
        max_buffer_delay_ms: Optional[int] = None,
        pronunciation_dict_id: Optional[str] = None,
        use_normalized_timestamps: Optional[bool] = None,
    ) -> WebSocketContext:
        """Create a context helper for managing conversational flows.

        Args:
            context_id: Unique identifier for this context. If not provided,
                a UUID will be auto-generated.
            model_id: Default model_id for push().
            voice: Default voice for push().
            output_format: Default output_format for push().
            language: Default language for push().
            add_timestamps: Default add_timestamps for push().
            add_phoneme_timestamps: Default add_phoneme_timestamps for push().
            generation_config: Default generation_config for push().
            max_buffer_delay_ms: Default generation_config for push().
            pronunciation_dict_id: Default generation_config for push().
            use_normalized_timestamps: Default generation_config for push().

        Returns:
            WebSocketContext helper for simplified sending and receiving
        """
        if context_id is not None and context_id in self._context_queues:
            raise ValueError(f"Context for context ID {context_id} already exists.")
        if context_id is None:
            context_id = str(uuid.uuid4())
        self._context_queues[context_id] = queue.Queue()
        return WebSocketContext(
            self,
            context_id,
            timeout=timeout,
            model_id=model_id,
            voice=voice,
            output_format=output_format,
            language=language,
            add_timestamps=add_timestamps,
            add_phoneme_timestamps=add_phoneme_timestamps,
            generation_config=generation_config,
            max_buffer_delay_ms=max_buffer_delay_ms,
            pronunciation_dict_id=pronunciation_dict_id,
            use_normalized_timestamps=use_normalized_timestamps,
        )


class TTSResourceConnectionManager:
    """
    Context manager over a `TTSResourceConnection` that is returned by `tts.websocket_connect()`

    This context manager ensures that the connection will be closed when it exits.

    ---

    Note that if your application doesn't work well with the context manager approach then you
    can call the `.enter()` method directly to initiate a connection.

    **Warning**: You must remember to close the connection with `.close()`.

    ```py
    connection = client.tts.websocket_connect(...).enter()
    # ...
    connection.close()
    ```
    """

    def __init__(
        self,
        *,
        client: Cartesia,
        extra_query: Query,
        extra_headers: Headers,
        websocket_connection_options: WebsocketConnectionOptions,
    ) -> None:
        self.__client = client
        self.__connection: Optional[TTSResourceConnection] = None
        self.__extra_query = extra_query
        self.__extra_headers = extra_headers
        self.__websocket_connection_options = websocket_connection_options
        self._logger = logging.getLogger(__name__)

    def __enter__(self) -> TTSResourceConnection:
        """
        👋 If your application doesn't work well with the context manager approach then you
        can call this method directly to initiate a connection.

        **Warning**: You must remember to close the connection with `.close()`.

        ```py
        connection = client.tts.websocket_connect(...).enter()
        # ...
        connection.close()
        ```
        """
        if self.__connection is not None:
            return self.__connection

        try:
            from websockets.sync.client import connect
        except ImportError as exc:
            raise CartesiaError("You need to install `cartesia[websockets]` to use this method") from exc

        url = self._prepare_url().copy_with(
            params={
                **self.__client.base_url.params,
                **self.__extra_query,
            },
        )
        self._logger.debug("Connecting to %s", url)
        if self.__websocket_connection_options:
            self._logger.debug("Connection options: %s", self.__websocket_connection_options)

        self.__connection = TTSResourceConnection(
            connect(
                str(url),
                user_agent_header=self.__client.user_agent,
                additional_headers=_merge_mappings(
                    {
                        **self.__client.auth_headers,
                        "Cartesia-Version": self.__client.default_headers.get("cartesia-version", "2025-11-04"),
                    },
                    self.__extra_headers,
                ),
                **self.__websocket_connection_options,
            ),
            manager=self,
        )

        return self.__connection

    enter = __enter__

    def _prepare_url(self) -> httpx.URL:
        if self.__client.websocket_base_url is not None:
            base_url = httpx.URL(self.__client.websocket_base_url)
        else:
            base_url = self.__client._base_url.copy_with(scheme="wss")

        merge_raw_path = base_url.raw_path.rstrip(b"/") + b"/tts/websocket"
        return base_url.copy_with(raw_path=merge_raw_path)

    def __exit__(
        self, exc_type: Optional[type[BaseException]], exc: Optional[BaseException], exc_tb: Optional[TracebackType]
    ) -> None:
        if self.__connection is not None:
            self.__connection.close()


# WebSocket context helpers for managing conversational flows.
class WebSocketContext:
    """Context helper for managing WebSocket conversations with automatic context_id handling."""

    def __init__(
        self,
        connection: "TTSResourceConnection",
        context_id: str,
        *,
        timeout: Optional[float] = None,
        model_id: Optional[str] = None,
        voice: Optional[VoiceSpecifierParam] = None,
        output_format: Union[RawOutputFormatParam, Mapping[str, Any], None] = None,
        language: Optional[SupportedLanguage] = None,
        add_timestamps: Optional[bool] = None,
        add_phoneme_timestamps: Optional[bool] = None,
        generation_config: Optional[GenerationConfigParam] = None,
        max_buffer_delay_ms: Optional[int] = None,
        pronunciation_dict_id: Optional[str] = None,
        use_normalized_timestamps: Optional[bool] = None,
    ):
        self._connection = connection
        self._context_id = context_id
        self._completed = False
        self._timeout = timeout
        self._model_id = model_id
        self._voice = voice
        self._output_format = output_format
        self._language = language
        self._add_timestamps = add_timestamps
        self._add_phoneme_timestamps = add_phoneme_timestamps
        self._generation_config = generation_config
        self._max_buffer_delay_ms = max_buffer_delay_ms
        self._pronunciation_dict_id = pronunciation_dict_id
        self._use_normalized_timestamps = use_normalized_timestamps

    def send(
        self,
        *,
        transcript: str,
        voice: VoiceSpecifierParam,
        model_id: Optional[str] = None,
        output_format: Union[RawOutputFormatParam, Mapping[str, Any], None] = None,
        continue_: bool = True,
        language: Union[SupportedLanguage, None, Omit] = omit,
        speed: Optional[ModelSpeed] = None,
        add_timestamps: Union[bool, None, Omit] = omit,
        add_phoneme_timestamps: Union[bool, None, Omit] = omit,
        flush: Union[bool, None, Omit] = omit,
        generation_config: Union[GenerationConfigParam, None, Omit] = omit,
        **kwargs: Any,
    ) -> None:
        """Send a generation request with automatic context_id management."""
        if self._completed:
            raise ValueError("Cannot send to completed context. Call no_more_inputs() only once per context.")

        # Default output format
        if output_format is not None:
            pass
        elif self._output_format is not None:
            output_format = self._output_format
        else:
            output_format = {
                "container": "raw",
                "encoding": "pcm_f32le",
                "sample_rate": 44100,
            }

        # Default model_id
        if model_id is not None:
            pass
        elif self._model_id is not None:
            model_id = self._model_id
        else:
            model_id = "sonic-latest"

        # Build request parameters, excluding omitted values
        request_params: GenerationRequestParam = {
            "context_id": self._context_id,
            "model_id": model_id,
            "transcript": transcript,
            "voice": voice,
            "output_format": cast(RawOutputFormatParam, output_format),
            "continue": continue_,
        }

        # Optional parameters with context value
        if language is None:
            pass
        elif not isinstance(language, Omit):
            request_params["language"] = language
        elif self._language is not None:
            request_params["language"] = self._language

        if add_timestamps is None:
            pass
        elif not isinstance(add_timestamps, Omit):
            request_params["add_timestamps"] = add_timestamps
        elif self._add_timestamps is not None:
            request_params["add_timestamps"] = self._add_timestamps

        if add_phoneme_timestamps is None:
            pass
        elif not isinstance(add_phoneme_timestamps, Omit):
            request_params["add_phoneme_timestamps"] = add_phoneme_timestamps
        elif self._add_phoneme_timestamps is not None:
            request_params["add_phoneme_timestamps"] = self._add_phoneme_timestamps

        if generation_config is None:
            pass
        elif not isinstance(generation_config, Omit):
            request_params["generation_config"] = generation_config
        elif self._generation_config is not None:
            request_params["generation_config"] = self._generation_config

        # Parameters from context only
        if self._max_buffer_delay_ms is not None:
            request_params["max_buffer_delay_ms"] = self._max_buffer_delay_ms
        if self._pronunciation_dict_id is not None:
            request_params["pronunciation_dict_id"] = self._pronunciation_dict_id
        if self._use_normalized_timestamps is not None:
            request_params["use_normalized_timestamps"] = self._use_normalized_timestamps

        # Other optional parameters
        if not isinstance(flush, Omit):
            request_params["flush"] = flush
        if speed is not None:
            request_params["speed"] = speed

        # Add any additional kwargs
        request_params.update(cast(GenerationRequestParam, kwargs))

        self._connection.send(request_params)

    def push(
        self,
        transcript: str,
        *,
        continue_: bool = True,
        voice: Union[VoiceSpecifierParam, Omit] = omit,
        **kwargs: Any,
    ) -> None:
        """Send a generation request with continue_=True using context defaults."""

        if not isinstance(voice, Omit):
            pass
        elif self._voice is not None:
            voice = self._voice
        else:
            raise ValueError("Context was initialized without required parameters (voice).")

        self.send(
            transcript=transcript,
            continue_=continue_,
            voice=voice,
            **kwargs,
        )

    def no_more_inputs(self) -> None:
        """Signal that no more inputs will be sent for this context."""
        if self._completed:
            return  # Already completed, ignore

        voice: VoiceSpecifierParam = self._voice or cast(
            VoiceSpecifierParam, {"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"}
        )

        self.send(
            transcript="",
            voice=voice,
            continue_=False,
        )
        self._completed = True

    def cancel(self) -> None:
        """Cancel this context, stopping any in-progress generation."""
        self._connection.send(CancelContextRequest(cancel=True, context_id=self._context_id))
        self._connection._context_queues.pop(self._context_id, None)

    def receive(self) -> Iterator[WebsocketResponse]:
        """Receive responses filtered to this context only.

        When multiple contexts share a connection, the context that reads from
        the websocket acts as a router: non-matching events are placed onto the
        correct context's queue so they are never lost.
        """
        from websockets.exceptions import ConnectionClosedOK

        my_queue = self._connection._context_queues.get(self._context_id)
        done = False

        try:
            while True:
                # 1. Drain our own queue first (events routed here by another context).
                if my_queue is not None:
                    try:
                        event = my_queue.get_nowait()
                        yield event
                        if event.type in ("done", "error"):
                            done = True
                            return
                        continue
                    except queue.Empty:
                        pass

                # 2. Read the next event from the connection.
                try:
                    raw = self._connection.recv_bytes(timeout=self._timeout)
                    event = self._connection.parse_event(raw)
                except ConnectionClosedOK:
                    done = True
                    return
                except TimeoutError:
                    done = True
                    raise

                # 3. Route the event.
                event_ctx = event.context_id if hasattr(event, "context_id") else None

                if event_ctx == self._context_id:
                    yield event
                    if event.type in ("done", "error"):
                        done = True
                        return
                elif event_ctx is not None and event_ctx in self._connection._context_queues:
                    self._connection._context_queues[event_ctx].put(event)
                elif not hasattr(event, "context_id") and event.type in ("done", "error"):
                    # Global events without context_id
                    yield event
                    if event.type in ("done", "error"):
                        done = True
                        return
                else:
                    # Unregistered context — yield for backwards compat
                    yield event
                    if event.type == "done":
                        done = True
                        return
        finally:
            # Only unregister the queue if the context completed.  If the
            # consumer exited early (break / cancel), keep the queue so
            # future events for this context_id are absorbed rather than
            # leaking into other contexts via the fallback path.
            if done:
                self._connection._context_queues.pop(self._context_id, None)


class AsyncWebSocketContext:
    """Async context helper for managing WebSocket conversations with automatic context_id handling."""

    def __init__(
        self,
        connection: "AsyncTTSResourceConnection",
        context_id: str,
        *,
        timeout: Optional[float] = None,
        model_id: Optional[str] = None,
        voice: Optional[VoiceSpecifierParam] = None,
        output_format: Union[RawOutputFormatParam, Mapping[str, Any], None] = None,
        language: Optional[SupportedLanguage] = None,
        add_timestamps: Optional[bool] = None,
        add_phoneme_timestamps: Optional[bool] = None,
        generation_config: Optional[GenerationConfigParam] = None,
        max_buffer_delay_ms: Optional[int] = None,
        pronunciation_dict_id: Optional[str] = None,
        use_normalized_timestamps: Optional[bool] = None,
    ):
        self._connection = connection
        self._context_id = context_id
        self._completed = False
        self._timeout = timeout
        self._model_id = model_id
        self._voice = voice
        self._output_format = output_format
        self._language = language
        self._add_timestamps = add_timestamps
        self._add_phoneme_timestamps = add_phoneme_timestamps
        self._generation_config = generation_config
        self._max_buffer_delay_ms = max_buffer_delay_ms
        self._pronunciation_dict_id = pronunciation_dict_id
        self._use_normalized_timestamps = use_normalized_timestamps

    async def send(
        self,
        *,
        transcript: str,
        voice: VoiceSpecifierParam,
        model_id: Optional[str] = None,
        output_format: Union[RawOutputFormatParam, Mapping[str, Any], None] = None,
        continue_: bool = True,
        language: Union[SupportedLanguage, None, Omit] = omit,
        speed: Optional[ModelSpeed] = None,
        add_timestamps: Union[bool, None, Omit] = omit,
        add_phoneme_timestamps: Union[bool, None, Omit] = omit,
        flush: Union[bool, None, Omit] = omit,
        generation_config: Union[GenerationConfigParam, None, Omit] = omit,
        **kwargs: Any,
    ) -> None:
        """Send a generation request with automatic context_id management."""
        if self._completed:
            raise ValueError("Cannot send to completed context. Call no_more_inputs() only once per context.")

        # Default output format
        if output_format is not None:
            pass
        elif self._output_format is not None:
            output_format = self._output_format
        else:
            output_format = {
                "container": "raw",
                "encoding": "pcm_f32le",
                "sample_rate": 44100,
            }

        # Default model_id
        if model_id is not None:
            pass
        elif self._model_id is not None:
            model_id = self._model_id
        else:
            model_id = "sonic-latest"

        # Build request parameters, excluding omitted values
        request_params: GenerationRequestParam = {
            "context_id": self._context_id,
            "model_id": model_id,
            "transcript": transcript,
            "voice": voice,
            "output_format": cast(RawOutputFormatParam, output_format),
            "continue": continue_,
        }

        # Optional parameters with context value
        if language is None:
            pass
        elif not isinstance(language, Omit):
            request_params["language"] = language
        elif self._language is not None:
            request_params["language"] = self._language

        if add_timestamps is None:
            pass
        elif not isinstance(add_timestamps, Omit):
            request_params["add_timestamps"] = add_timestamps
        elif self._add_timestamps is not None:
            request_params["add_timestamps"] = self._add_timestamps

        if add_phoneme_timestamps is None:
            pass
        elif not isinstance(add_phoneme_timestamps, Omit):
            request_params["add_phoneme_timestamps"] = add_phoneme_timestamps
        elif self._add_phoneme_timestamps is not None:
            request_params["add_phoneme_timestamps"] = self._add_phoneme_timestamps

        if generation_config is None:
            pass
        elif not isinstance(generation_config, Omit):
            request_params["generation_config"] = generation_config
        elif self._generation_config is not None:
            request_params["generation_config"] = self._generation_config

        # Parameters from context only
        if self._max_buffer_delay_ms is not None:
            request_params["max_buffer_delay_ms"] = self._max_buffer_delay_ms
        if self._pronunciation_dict_id is not None:
            request_params["pronunciation_dict_id"] = self._pronunciation_dict_id
        if self._use_normalized_timestamps is not None:
            request_params["use_normalized_timestamps"] = self._use_normalized_timestamps

        # Other optional parameters
        if not isinstance(flush, Omit):
            request_params["flush"] = flush
        if speed is not None:
            request_params["speed"] = speed

        # Add any additional kwargs
        request_params.update(cast(GenerationRequestParam, kwargs))

        await self._connection.send(request_params)
        self._connection._dispatch_listener()

    async def push(
        self,
        transcript: str,
        *,
        continue_: bool = True,
        voice: Union[VoiceSpecifierParam, Omit] = omit,
        **kwargs: Any,
    ) -> None:
        """Send a generation request with continue_=True using context defaults."""

        if not isinstance(voice, Omit):
            pass
        elif self._voice is not None:
            voice = self._voice
        else:
            raise ValueError("Context was initialized without required parameters (voice).")

        await self.send(
            transcript=transcript,
            continue_=continue_,
            voice=voice,
            **kwargs,
        )

    async def no_more_inputs(self) -> None:
        """Signal that no more inputs will be sent for this context."""
        if self._completed:
            return  # Already completed, ignore

        voice: VoiceSpecifierParam = self._voice or cast(
            VoiceSpecifierParam, {"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"}
        )

        await self.send(
            transcript="",
            voice=voice,
            continue_=False,
        )
        self._completed = True

    async def cancel(self) -> None:
        """Cancel this context, stopping any in-progress generation."""
        await self._connection.send(CancelContextRequest(cancel=True, context_id=self._context_id))
        self._connection._context_queues.pop(self._context_id, None)

    async def receive(self) -> AsyncIterator[WebsocketResponse]:
        """Receive responses filtered to this context only.

        A background task on the connection continuously reads from the wire
        and routes events into per-context queues.  This method simply drains
        the queue for this context.
        """
        import asyncio as _asyncio

        my_queue = self._connection._context_queues.get(self._context_id)
        if my_queue is None:
            return

        done = False

        try:
            while True:
                try:
                    if self._timeout is not None:
                        event = await _asyncio.wait_for(my_queue.get(), timeout=self._timeout)
                    else:
                        event = await my_queue.get()
                except TimeoutError:
                    done = True
                    raise

                yield event
                if event.type in ("done", "error"):
                    done = True
                    return
        finally:
            if done:
                self._connection._context_queues.pop(self._context_id, None)


class BackcompatWebSocketTtsOutput(BaseModel):
    """Output object for backward compatibility with v2 WebSocket response."""

    audio: Optional[bytes] = None
    word_timestamps: Optional[Any] = None
    phoneme_timestamps: Optional[Any] = None
    context_id: Optional[str] = None
    flush_done: Optional[bool] = None
    flush_id: Optional[str] = None


class BackcompatTTSResourceConnection:
    """Wrapper for TTSResourceConnection to provide v2-compatible API."""

    def __init__(self, manager: TTSResourceConnectionManager):
        self._manager = manager
        self._connection: Optional[TTSResourceConnection] = None

    def connect(self) -> None:
        if self._connection is None:
            self._connection = self._manager.enter()

    def close(self) -> None:
        if self._connection:
            self._manager.__exit__(None, None, None)
            self._connection = None

    def context(self, context_id: Optional[str] = None) -> WebSocketContext:
        """Create a context helper (v2 compatible)."""
        if not self._connection:
            self.connect()
        assert self._connection is not None
        return self._connection.context(context_id)

    def send(
        self,
        *,
        model_id: str,
        transcript: str,
        output_format: Union[RawOutputFormatParam, Mapping[str, Any]],
        voice: Union[VoiceSpecifierParam, Mapping[str, Any]],
        context_id: Optional[str] = None,
        stream: bool = True,
        **kwargs: Any,
    ) -> Union[Iterator[BackcompatWebSocketTtsOutput], BackcompatWebSocketTtsOutput]:
        """Send a request and return responses (v2 compatible).

        If stream is True, returns an iterator of BackcompatWebSocketTtsOutput chunks.
        If stream is False, returns a single BackcompatWebSocketTtsOutput with all
        audio concatenated and timestamps aggregated (matching v2 behaviour).
        """
        if not self._connection:
            self.connect()
        assert self._connection is not None
        self._connection._ensure_connected()

        ctx = self._connection.context(context_id)

        # Send the request
        ctx.send(
            model_id=model_id,
            transcript=transcript,
            voice=cast(VoiceSpecifierParam, voice),
            output_format=output_format,
            continue_=False,
            **kwargs,
        )

        # Generate output stream
        def generator() -> Iterator[BackcompatWebSocketTtsOutput]:
            for event in ctx.receive():
                if event.type == "error":
                    raise RuntimeError(f"Error generating audio:\n{getattr(event, 'error', 'Unknown error')}")

                out = BackcompatWebSocketTtsOutput(context_id=event.context_id)

                if event.type == "chunk":
                    out.audio = event.audio
                elif event.type == "timestamps":
                    out.word_timestamps = getattr(event, "word_timestamps", None)
                elif event.type == "phoneme_timestamps":
                    out.phoneme_timestamps = getattr(event, "phoneme_timestamps", None)
                elif event.type == "flush_done":
                    out.flush_done = getattr(event, "flush_done", None)
                    out.flush_id = getattr(event, "flush_id", None)

                yield out

        if stream:
            return generator()

        audio_parts: list[bytes] = []
        words: list[str] = []
        word_starts: list[float] = []
        word_ends: list[float] = []
        phonemes: list[str] = []
        phoneme_starts: list[float] = []
        phoneme_ends: list[float] = []
        for chunk in generator():
            if chunk.audio is not None:
                audio_parts.append(chunk.audio)
            if chunk.word_timestamps is not None:
                wt = chunk.word_timestamps
                words.extend(wt.words)
                word_starts.extend(wt.start)
                word_ends.extend(wt.end)
            if chunk.phoneme_timestamps is not None:
                pt = chunk.phoneme_timestamps
                phonemes.extend(pt.phonemes)
                phoneme_starts.extend(pt.start)
                phoneme_ends.extend(pt.end)
        return BackcompatWebSocketTtsOutput(
            audio=b"".join(audio_parts) if audio_parts else None,
            context_id=ctx._context_id,
            word_timestamps={"words": words, "start": word_starts, "end": word_ends} if words else None,
            phoneme_timestamps={"phonemes": phonemes, "start": phoneme_starts, "end": phoneme_ends}
            if phonemes
            else None,
        )


class AsyncBackcompatTTSResourceConnection:
    """Wrapper for AsyncTTSResourceConnection to provide v2-compatible API."""

    def __init__(self, manager: AsyncTTSResourceConnectionManager):
        self._manager = manager
        self._connection: Optional[AsyncTTSResourceConnection] = None

    async def connect(self) -> None:
        if self._connection is None:
            self._connection = await self._manager.enter()

    async def close(self) -> None:
        if self._connection:
            await self._manager.__aexit__(None, None, None)
            self._connection = None

    def context(self, context_id: Optional[str] = None) -> AsyncWebSocketContext:
        """Create a context helper (v2 compatible)."""
        if not self._connection:
            raise RuntimeError("Must call connect() before creating context")
        return self._connection.context(context_id)

    async def send(
        self,
        *,
        model_id: str,
        transcript: str,
        output_format: Union[RawOutputFormatParam, Mapping[str, Any]],
        voice: Union[VoiceSpecifierParam, Mapping[str, Any]],
        context_id: Optional[str] = None,
        stream: bool = True,
        **kwargs: Any,
    ) -> Union[AsyncIterator[BackcompatWebSocketTtsOutput], BackcompatWebSocketTtsOutput]:
        """Send a request and return responses (v2 compatible).

        If stream is True, returns an async iterator of BackcompatWebSocketTtsOutput chunks.
        If stream is False, returns a single BackcompatWebSocketTtsOutput with all
        audio concatenated and timestamps aggregated (matching v2 behaviour).
        """
        if not self._connection:
            await self.connect()
        assert self._connection is not None
        await self._connection._ensure_connected()

        ctx = self._connection.context(context_id)

        # Send the request
        await ctx.send(
            model_id=model_id,
            transcript=transcript,
            voice=cast(VoiceSpecifierParam, voice),
            output_format=output_format,
            continue_=False,
            **kwargs,
        )

        # Generate output stream
        async def generator() -> AsyncIterator[BackcompatWebSocketTtsOutput]:
            async for event in ctx.receive():
                if event.type == "error":
                    raise RuntimeError(f"Error generating audio:\n{getattr(event, 'error', 'Unknown error')}")

                out = BackcompatWebSocketTtsOutput(context_id=event.context_id)

                if event.type == "chunk":
                    out.audio = event.audio
                elif event.type == "timestamps":
                    out.word_timestamps = getattr(event, "word_timestamps", None)
                elif event.type == "phoneme_timestamps":
                    out.phoneme_timestamps = getattr(event, "phoneme_timestamps", None)
                elif event.type == "flush_done":
                    out.flush_done = getattr(event, "flush_done", None)
                    out.flush_id = getattr(event, "flush_id", None)

                yield out

        if stream:
            return generator()

        audio_parts: list[bytes] = []
        words: list[str] = []
        word_starts: list[float] = []
        word_ends: list[float] = []
        phonemes: list[str] = []
        phoneme_starts: list[float] = []
        phoneme_ends: list[float] = []
        async for chunk in generator():
            if chunk.audio is not None:
                audio_parts.append(chunk.audio)
            if chunk.word_timestamps is not None:
                wt = chunk.word_timestamps
                words.extend(wt.words)
                word_starts.extend(wt.start)
                word_ends.extend(wt.end)
            if chunk.phoneme_timestamps is not None:
                pt = chunk.phoneme_timestamps
                phonemes.extend(pt.phonemes)
                phoneme_starts.extend(pt.start)
                phoneme_ends.extend(pt.end)
        return BackcompatWebSocketTtsOutput(
            audio=b"".join(audio_parts) if audio_parts else None,
            context_id=ctx._context_id,
            word_timestamps={"words": words, "start": word_starts, "end": word_ends} if words else None,
            phoneme_timestamps={"phonemes": phonemes, "start": phoneme_starts, "end": phoneme_ends}
            if phonemes
            else None,
        )
