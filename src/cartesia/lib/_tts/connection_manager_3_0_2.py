"""
TTSResource.websocket_connect() and AsyncTTSResource.websocket_connect() implementation.

.. deprecated::
    Use contexts.py instead.
"""

from __future__ import annotations

import json
import uuid
import queue
import logging
from types import TracebackType
from typing import TYPE_CHECKING, Any, Dict, Iterator, Optional, cast
from typing_extensions import AsyncIterator

import httpx
from pydantic import BaseModel

from ...types import (
    ModelSpeed,
    SupportedLanguage,
)
from ..._types import Omit, Query, Headers, omit
from ..._utils import maybe_transform, async_maybe_transform
from ..._models import construct_type_unchecked
from ..._exceptions import CartesiaError
from ..._base_client import _merge_mappings
from ...types.model_speed import ModelSpeed
from ...types.supported_language import SupportedLanguage
from ...types.websocket_response import WebsocketResponse
from ...types.voice_specifier_param import VoiceSpecifierParam
from ...types.websocket_client_event import GenerationRequest, CancelContextRequest, WebsocketClientEvent
from ...types.generation_config_param import GenerationConfigParam
from ...types.websocket_client_event_param import WebsocketClientEventParam
from ...types.websocket_connection_options import WebsocketConnectionOptions

if TYPE_CHECKING:
    import asyncio

    from websockets.sync.client import ClientConnection as WebsocketConnection
    from websockets.asyncio.client import ClientConnection as AsyncWebsocketConnection

    from ..._client import Cartesia, AsyncCartesia


log: logging.Logger = logging.getLogger(__name__)


class AsyncTTSResourceConnection_3_0_2:
    """
    Represents a live WebSocket connection to the TTS API

    .. deprecated::
        Created by :class:`AsyncTTSResourceConnectionManager_3_0_2`.
    """

    _connection: AsyncWebsocketConnection

    def __init__(
        self, connection: AsyncWebsocketConnection, manager: AsyncTTSResourceConnectionManager_3_0_2 | None = None
    ) -> None:
        self._connection = connection
        self._manager = manager
        self._context_queues: dict[str, asyncio.Queue[WebsocketResponse]] = {}
        self._processing_task: asyncio.Task[None] | None = None
        self._closing = False

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

    async def recv_bytes(self, timeout: float | None = None) -> bytes:
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
        log.debug(f"Received websocket message: %s", message)
        return message

    # Dict[str, Any] is added for backward compatibility since WebsocketClientEventParam used to not require context_id
    # Not providing a context_id will result in an error event
    async def send(self, event: WebsocketClientEvent | WebsocketClientEventParam | Dict[str, Any]) -> None:
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
                log.debug("Received websocket message: %s", raw)
                event = self.parse_event(raw)
                event_ctx = event.context_id if hasattr(event, "context_id") else None
                if event_ctx is not None and event_ctx in self._context_queues:
                    await self._context_queues[event_ctx].put(event)
                else:
                    log.debug("Received event for unregistered context %s", event_ctx)
        except ConnectionClosed:
            if not self._closing:
                log.warning("WebSocket connection closed unexpectedly")

    async def _ensure_connected(self) -> None:
        import asyncio as _asyncio

        from websockets.protocol import State

        if self._manager is not None and self._connection.state in (State.CLOSED, State.CLOSING):
            log.debug("Connection is not open (state=%s), reconnecting...", self._connection.state)
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

    def parse_event(self, data: str | bytes) -> WebsocketResponse:
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
        timeout: float | None = None,
        model_id: str | None = None,
        voice: VoiceSpecifierParam | None = None,
        output_format: Dict[str, Any] | None = None,
        language: SupportedLanguage | None = None,
        add_timestamps: bool | None = None,
        add_phoneme_timestamps: bool | None = None,
        generation_config: GenerationConfigParam | None = None,
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

        Returns:
            AsyncWebSocketContext helper for simplified sending and receiving.
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
        )


class AsyncTTSResourceConnectionManager_3_0_2:
    """
    Context manager over a `AsyncTTSResourceConnection` that is returned by `cartesia.tts.websocket_connect()`

    This context manager ensures that the connection will be closed when it exits.

    .. deprecated::
        Created by ``cartesia.tts.websocket_connect()``. Use ``cartesia.tts.contexts_ws()`` instead.

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
        self.__connection: AsyncTTSResourceConnection_3_0_2 | None = None
        self.__extra_query = extra_query
        self.__extra_headers = extra_headers
        self.__websocket_connection_options = websocket_connection_options

    async def __aenter__(self) -> AsyncTTSResourceConnection_3_0_2:
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
        log.debug("Connecting to %s", url)
        if self.__websocket_connection_options:
            log.debug("Connection options: %s", self.__websocket_connection_options)

        self.__connection = AsyncTTSResourceConnection_3_0_2(
            await connect(
                str(url),
                user_agent_header=self.__client.user_agent,
                additional_headers=_merge_mappings(
                    {
                        **self.__client.auth_headers,
                        "Cartesia-Version": self.__client.default_headers.get("cartesia-version", "2026-03-01"),
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
        self, exc_type: type[BaseException] | None, exc: BaseException | None, exc_tb: TracebackType | None
    ) -> None:
        if self.__connection is not None:
            await self.__connection.close()


class TTSResourceConnection_3_0_2:
    """
    Represents a live WebSocket connection to the TTS API

    .. deprecated::
        Created by :class:`TTSResourceConnectionManager_3_0_2`.
    """

    _connection: WebsocketConnection

    def __init__(
        self, connection: WebsocketConnection, manager: TTSResourceConnectionManager_3_0_2 | None = None
    ) -> None:
        self._connection = connection
        self._manager = manager
        self._context_queues: dict[str, queue.Queue[WebsocketResponse]] = {}

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

    def recv_bytes(self, timeout: float | None = None) -> bytes:
        """Receive the next message from the connection as raw bytes.

        Canceling this method is safe. There's no risk of losing data.

        If you want to parse the message into a `WebsocketResponse` object like `.recv()` does,
        then you can call `.parse_event(data)`.
        """
        message = self._connection.recv(decode=False, timeout=timeout)
        log.debug(f"Received websocket message: %s", message)
        return message

    # Dict[str, Any] is added for backward compatibility since WebsocketClientEventParam used to not require context_id
    # Not providing a context_id will result in an error event
    def send(self, event: WebsocketClientEvent | WebsocketClientEventParam | Dict[str, Any]) -> None:
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
            log.debug("Connection is not open (state=%s), reconnecting...", self._connection.state)
            new_conn = self._manager.__enter__()
            self._connection = new_conn._connection
            self._context_queues.clear()

    def parse_event(self, data: str | bytes) -> WebsocketResponse:
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
        timeout: float | None = None,
        model_id: str | None = None,
        voice: VoiceSpecifierParam | None = None,
        output_format: Dict[str, Any] | None = None,
        language: SupportedLanguage | None = None,
        add_timestamps: bool | None = None,
        add_phoneme_timestamps: bool | None = None,
        generation_config: GenerationConfigParam | None = None,
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
        )


class TTSResourceConnectionManager_3_0_2:
    """
    Context manager over a `TTSResourceConnection` that is returned by `cartesia.tts.websocket_connect()`

    This context manager ensures that the connection will be closed when it exits.

    .. deprecated::
        Created by ``cartesia.tts.websocket_connect()``. Use ``cartesia.tts.contexts_ws()`` instead.

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
        self.__connection: TTSResourceConnection_3_0_2 | None = None
        self.__extra_query = extra_query
        self.__extra_headers = extra_headers
        self.__websocket_connection_options = websocket_connection_options

    def __enter__(self) -> TTSResourceConnection_3_0_2:
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
        log.debug("Connecting to %s", url)
        if self.__websocket_connection_options:
            log.debug("Connection options: %s", self.__websocket_connection_options)

        self.__connection = TTSResourceConnection_3_0_2(
            connect(
                str(url),
                user_agent_header=self.__client.user_agent,
                additional_headers=_merge_mappings(
                    {
                        **self.__client.auth_headers,
                        "Cartesia-Version": self.__client.default_headers.get("cartesia-version", "2026-03-01"),
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
        self, exc_type: type[BaseException] | None, exc: BaseException | None, exc_tb: TracebackType | None
    ) -> None:
        if self.__connection is not None:
            self.__connection.close()


class WebSocketContext:
    """
    Context helper for managing WebSocket conversations with automatic context_id handling.

    .. deprecated ::
        Created by :meth:`TTSResourceConnection_3_0_2.connect`.
    """

    def __init__(
        self,
        connection: "TTSResourceConnection_3_0_2",
        context_id: str,
        *,
        timeout: float | None = None,
        model_id: str | None = None,
        voice: VoiceSpecifierParam | None = None,
        output_format: Dict[str, Any] | None = None,
        language: SupportedLanguage | None = None,
        add_timestamps: bool | None = None,
        add_phoneme_timestamps: bool | None = None,
        generation_config: GenerationConfigParam | None = None,
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

    def send(
        self,
        *,
        model_id: str,
        transcript: str,
        voice: VoiceSpecifierParam,
        output_format: Optional[Dict[str, Any]] = None,
        continue_: bool = True,
        duration: Optional[float] | Omit = omit,
        language: Optional[SupportedLanguage] | Omit = omit,
        speed: Optional[ModelSpeed] | Omit = omit,
        add_timestamps: Optional[bool] | Omit = omit,
        add_phoneme_timestamps: Optional[bool] | Omit = omit,
        flush: Optional[bool] | Omit = omit,
        generation_config: Optional[GenerationConfigParam] | Omit = omit,
        **kwargs: Any,
    ) -> None:
        """Send a generation request with automatic context_id management."""
        if self._completed:
            raise ValueError("Cannot send to completed context. Call no_more_inputs() only once per context.")

        # Default output format
        if output_format is None:
            output_format = {
                "container": "raw",
                "encoding": "pcm_f32le",
                "sample_rate": 44100,
            }

        # Build request parameters, excluding omitted values
        request_params: dict[str, Any] = {
            "model_id": model_id,
            "transcript": transcript,
            "voice": voice,
            "output_format": output_format,
            "context_id": self._context_id,
            "continue": continue_,
        }

        # Add optional parameters only if they're not omitted
        if not isinstance(duration, Omit):
            request_params["duration"] = duration
        if not isinstance(language, Omit):
            request_params["language"] = language
        if not isinstance(speed, Omit):
            request_params["speed"] = speed
        if not isinstance(add_timestamps, Omit):
            request_params["add_timestamps"] = add_timestamps
        if not isinstance(add_phoneme_timestamps, Omit):
            request_params["add_phoneme_timestamps"] = add_phoneme_timestamps
        if not isinstance(flush, Omit):
            request_params["flush"] = flush
        if not isinstance(generation_config, Omit):
            request_params["generation_config"] = generation_config

        # Add any additional kwargs
        request_params.update(kwargs)

        request = GenerationRequest(**request_params)
        self._connection.send(request)

    def push(
        self,
        transcript: str,
        *,
        flush: Optional[bool] | Omit = omit,
        **kwargs: Any,
    ) -> None:
        """Send a generation request with continue_=True using context defaults."""
        if self._model_id is None or self._voice is None:
            raise ValueError(
                "Context was initialized without required parameters (model_id, voice). Cannot use push()."
            )

        language: SupportedLanguage | Omit = (
            cast(SupportedLanguage, self._language) if self._language is not None else omit
        )
        add_timestamps: bool | Omit = self._add_timestamps if self._add_timestamps is not None else omit
        add_phoneme_timestamps: bool | Omit = (
            self._add_phoneme_timestamps if self._add_phoneme_timestamps is not None else omit
        )

        # Use passed generation_config if provided in kwargs, otherwise use context default
        generation_config: GenerationConfigParam | None = kwargs.pop("generation_config", self._generation_config)

        self.send(
            model_id=self._model_id,
            transcript=transcript,
            voice=self._voice,
            output_format=self._output_format,
            continue_=True,
            language=language,
            add_timestamps=add_timestamps,
            add_phoneme_timestamps=add_phoneme_timestamps,
            flush=flush,
            generation_config=generation_config,
            **kwargs,
        )

    def no_more_inputs(self) -> None:
        """Signal that no more inputs will be sent for this context."""
        if self._completed:
            return  # Already completed, ignore

        model_id: str = self._model_id or "sonic-3"
        voice: VoiceSpecifierParam = self._voice or cast(
            VoiceSpecifierParam, {"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"}
        )
        output_format = self._output_format or {
            "container": "raw",
            "encoding": "pcm_f32le",
            "sample_rate": 44100,
        }
        language: SupportedLanguage | Omit = (
            cast(SupportedLanguage, self._language) if self._language is not None else omit
        )

        self.send(
            model_id=model_id,
            transcript="",
            voice=voice,
            output_format=output_format,
            continue_=False,
            language=language,
            generation_config=self._generation_config,
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
    """
    Async context helper for managing WebSocket conversations with automatic context_id handling.

    .. deprecated ::
        Created by :meth:`AsyncTTSResourceConnection_3_0_2.connect`.
    """

    def __init__(
        self,
        connection: "AsyncTTSResourceConnection_3_0_2",
        context_id: str,
        *,
        timeout: float | None = None,
        model_id: str | None = None,
        voice: VoiceSpecifierParam | None = None,
        output_format: Dict[str, Any] | None = None,
        language: SupportedLanguage | None = None,
        add_timestamps: bool | None = None,
        add_phoneme_timestamps: bool | None = None,
        generation_config: GenerationConfigParam | None = None,
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

    async def send(
        self,
        *,
        model_id: str,
        transcript: str,
        voice: VoiceSpecifierParam,
        output_format: Optional[Dict[str, Any]] = None,
        continue_: bool = True,
        duration: Optional[float] | Omit = omit,
        language: Optional[SupportedLanguage] | Omit = omit,
        speed: Optional[ModelSpeed] | Omit = omit,
        add_timestamps: Optional[bool] | Omit = omit,
        add_phoneme_timestamps: Optional[bool] | Omit = omit,
        flush: Optional[bool] | Omit = omit,
        generation_config: Optional[GenerationConfigParam] | Omit = omit,
        **kwargs: Any,
    ) -> None:
        """Send a generation request with automatic context_id management."""
        if self._completed:
            raise ValueError("Cannot send to completed context. Call no_more_inputs() only once per context.")

        # Default output format
        if output_format is None:
            output_format = {
                "container": "raw",
                "encoding": "pcm_f32le",
                "sample_rate": 44100,
            }

        # Build request parameters, excluding omitted values
        request_params: dict[str, Any] = {
            "model_id": model_id,
            "transcript": transcript,
            "voice": voice,
            "output_format": output_format,
            "context_id": self._context_id,
            "continue": continue_,
        }

        # Add optional parameters only if they're not omitted
        if not isinstance(duration, Omit):
            request_params["duration"] = duration
        if not isinstance(language, Omit):
            request_params["language"] = language
        if not isinstance(speed, Omit):
            request_params["speed"] = speed
        if not isinstance(add_timestamps, Omit):
            request_params["add_timestamps"] = add_timestamps
        if not isinstance(add_phoneme_timestamps, Omit):
            request_params["add_phoneme_timestamps"] = add_phoneme_timestamps
        if not isinstance(flush, Omit):
            request_params["flush"] = flush
        if not isinstance(generation_config, Omit):
            request_params["generation_config"] = generation_config

        # Add any additional kwargs
        request_params.update(kwargs)

        request = GenerationRequest(**request_params)
        await self._connection.send(request)
        self._connection._dispatch_listener()

    async def push(
        self,
        transcript: str,
        *,
        flush: Optional[bool] | Omit = omit,
        **kwargs: Any,
    ) -> None:
        """Send a generation request with continue_=True using context defaults."""
        if self._model_id is None or self._voice is None:
            raise ValueError(
                "Context was initialized without required parameters (model_id, voice). Cannot use push()."
            )

        language: SupportedLanguage | Omit = (
            cast(SupportedLanguage, self._language) if self._language is not None else omit
        )
        add_timestamps: bool | Omit = self._add_timestamps if self._add_timestamps is not None else omit
        add_phoneme_timestamps: bool | Omit = (
            self._add_phoneme_timestamps if self._add_phoneme_timestamps is not None else omit
        )

        # Use passed generation_config if provided in kwargs, otherwise use context default
        generation_config: GenerationConfigParam | None = kwargs.pop("generation_config", self._generation_config)

        await self.send(
            model_id=self._model_id,
            transcript=transcript,
            voice=self._voice,
            output_format=self._output_format,
            continue_=True,
            language=language,
            add_timestamps=add_timestamps,
            add_phoneme_timestamps=add_phoneme_timestamps,
            flush=flush,
            generation_config=generation_config,
            **kwargs,
        )

    async def no_more_inputs(self) -> None:
        """Signal that no more inputs will be sent for this context."""
        if self._completed:
            return  # Already completed, ignore

        model_id: str = self._model_id or "sonic-3"
        voice: VoiceSpecifierParam = self._voice or cast(
            VoiceSpecifierParam, {"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"}
        )
        output_format = self._output_format or {
            "container": "raw",
            "encoding": "pcm_f32le",
            "sample_rate": 44100,
        }
        language: SupportedLanguage | Omit = (
            cast(SupportedLanguage, self._language) if self._language is not None else omit
        )

        await self.send(
            model_id=model_id,
            transcript="",
            voice=voice,
            output_format=output_format,
            continue_=False,
            language=language,
            generation_config=self._generation_config,
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
