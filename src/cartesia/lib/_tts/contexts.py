from __future__ import annotations

import uuid
import queue
import asyncio
import logging
import threading
from types import TracebackType
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Union,
    Literal,
    Mapping,
    Callable,
    Iterator,
    Optional,
    cast,
    overload,
)
from typing_extensions import AsyncIterator, override

from ...types import (
    ReconnectingEvent,
    SupportedLanguage,
    WebsocketResponse,
    VoiceSpecifierParam,
    WebsocketClientEvent,
    GenerationConfigParam,
    ReconnectingOverrides,
    GenerationRequestParam,
    WebsocketClientEventParam,
    WebSocketConnectionOptions,
)
from ..._types import Omit, Query, Headers, omit
from ..._exceptions import CartesiaError, WebSocketQueueFullError
from ..tts.contexts import (
    TTSWSContext,
    AsyncTTSWSContext,
    TTSContextsWSConnection,
    TTSContextsWSErrorHandler,
    AsyncTTSContextsWSConnection,
    TTSContextsWSConnectionManager,
    AsyncTTSContextsWSConnectionManager,
)
from ..._event_handler import EventHandlerRegistry
from ...types.websocket_response import Error as WebSocketResponseError, FlushDone as FlushDone
from ...types.websocket_client_event import (
    CancelContextRequest,
)
from ...types.generation_request_param import OutputFormat

if TYPE_CHECKING:
    from ..._client import Cartesia, AsyncCartesia
    from ...resources.tts import (
        TTSResourceConnection,
        AsyncTTSResourceConnection,
        TTSResourceConnectionManager,
        AsyncTTSResourceConnectionManager,
    )


class _Sentinel:
    """Events placed on a context queue that are not :class:`WebsocketResponse`."""

    def __init__(self, kind: Literal["disconnect"]) -> None:
        self.kind: Literal["disconnect"] = kind


def _is_terminal(response: WebsocketResponse) -> bool:
    """Return True if this response should end the per-context iteration."""
    if response.type == "done":
        return True
    if response.type == "error":
        # Error.done is required (bool). True means the context is terminated.
        return getattr(response, "done", True) is not False
    return False


def _build_generation_request(
    *,
    context_id: str,
    model_id: str,
    transcript: str,
    voice: VoiceSpecifierParam,
    output_format: OutputFormat,
    continue_: bool,
    language: Optional[SupportedLanguage],
    add_timestamps: Optional[bool] | Omit,
    add_phoneme_timestamps: Optional[bool] | Omit,
    flush: Optional[bool] | Omit,
    generation_config: Optional[GenerationConfigParam],
    extra: Mapping[str, Any],
) -> GenerationRequestParam:
    # Internal dict so we can accept arbitrary `extra` keys; cast to the strict
    # TypedDict at return.
    request_params: GenerationRequestParam = {
        "model_id": model_id,
        "transcript": transcript,
        "voice": voice,
        "output_format": output_format,
        "context_id": context_id,
        "continue": continue_,
    }
    if language is not None:
        request_params["language"] = language
    if not isinstance(add_timestamps, Omit):
        request_params["add_timestamps"] = add_timestamps
    if not isinstance(add_phoneme_timestamps, Omit):
        request_params["add_phoneme_timestamps"] = add_phoneme_timestamps
    if not isinstance(flush, Omit):
        request_params["flush"] = flush
    if generation_config is not None:
        request_params["generation_config"] = generation_config
    request_params.update(cast(GenerationRequestParam, extra))
    return request_params


# ---------------------------------------------------------------------------
# Sync
# ---------------------------------------------------------------------------


class _TTSWSContext(TTSWSContext):
    def __init__(
        self,
        *,
        ws: _TTSContextsWSConnection,
        timeout: float | None = None,
        context_id: str,
        model_id: str,
        voice: VoiceSpecifierParam,
        output_format: OutputFormat,
        language: SupportedLanguage | None = None,
        add_timestamps: bool | None = None,
        add_phoneme_timestamps: bool | None = None,
    ) -> None:
        self._ws = ws
        self._context_id = context_id
        self._queue: queue.Queue[WebsocketResponse | _Sentinel] = queue.Queue()
        self._closed = False
        self._timeout = timeout
        self._model_id = model_id
        self._voice = voice
        self._output_format = output_format
        self._language = language
        self._add_timestamps: bool | Omit = add_timestamps if add_timestamps is not None else omit
        self._add_phoneme_timestamps: bool | Omit = (
            add_phoneme_timestamps if add_phoneme_timestamps is not None else omit
        )

    @property
    @override
    def context_id(self) -> str:
        return self._context_id

    @property
    @override
    def is_closed(self) -> bool:
        return self._closed

    @override
    def push(
        self,
        transcript: str,
        *,
        generation_config: Optional[GenerationConfigParam] = None,
        continue_: Optional[bool] = True,
        extra_args: Optional[Mapping[str, Any]] = None,
    ) -> None:
        if self.is_closed:
            raise CartesiaError(f"Cannot push to closed context ({self._context_id}).")

        request = _build_generation_request(
            context_id=self._context_id,
            model_id=self._model_id,
            transcript=transcript,
            voice=self._voice,
            output_format=self._output_format,
            continue_=True if continue_ is None else continue_,
            language=self._language,
            add_timestamps=self._add_timestamps,
            add_phoneme_timestamps=self._add_phoneme_timestamps,
            flush=omit,
            generation_config=generation_config,
            extra={} if extra_args is None else extra_args,
        )
        self._ws._send(request)

    @override
    def end(self) -> None:
        if self.is_closed:
            return
        request = _build_generation_request(
            context_id=self._context_id,
            model_id=self._model_id,
            transcript="",
            voice=self._voice,
            output_format=self._output_format,
            continue_=False,
            language=self._language,
            add_timestamps=self._add_timestamps,
            add_phoneme_timestamps=self._add_phoneme_timestamps,
            flush=omit,
            generation_config=None,
            extra={},
        )

        try:
            self._ws._send(request)
        except WebSocketQueueFullError:
            raise
        except CartesiaError:
            pass

    @override
    def flush(self) -> None:
        if self.is_closed:
            raise CartesiaError(f"Cannot flush closed context ({self._context_id}).")
        request = _build_generation_request(
            context_id=self._context_id,
            model_id=self._model_id,
            transcript="",
            voice=self._voice,
            output_format=self._output_format,
            continue_=True,
            language=self._language,
            add_timestamps=self._add_timestamps,
            add_phoneme_timestamps=self._add_phoneme_timestamps,
            flush=True,
            generation_config=None,
            extra={},
        )
        self._ws._send(request)

    @override
    def cancel(self) -> None:
        if self.is_closed:
            return
        try:
            self._ws._send(CancelContextRequest(cancel=True, context_id=self._context_id))
        except WebSocketQueueFullError:
            raise
        except CartesiaError:
            pass
        self._mark_closed()

    @override
    def receive(self) -> Iterator[WebsocketResponse]:
        if self.is_closed:
            # Already drained; subsequent receive() calls return immediately
            # rather than blocking on an empty queue.
            return
        try:
            while True:
                try:
                    if self._timeout is not None:
                        item = self._queue.get(timeout=self._timeout)
                    else:
                        item = self._queue.get()
                except queue.Empty:
                    yield WebSocketResponseError(
                        type="error",
                        done=True,
                        context_id=self._context_id,
                        error_code="client_timeout",
                        title="Timeout",
                        message=(f"Client-side timeout of {self._timeout}s reached with no events from the server."),
                    )
                    return
                if isinstance(item, _Sentinel):
                    if item.kind == "disconnect":
                        return
                else:
                    yield item
                    if _is_terminal(item):
                        return
        finally:
            self._mark_closed()

    def _mark_closed(self) -> None:
        if self._closed:
            return
        self._closed = True
        # Wake any pending receive() loop. The queue is unbounded so put_nowait can't raise.
        self._queue.put_nowait(_Sentinel("disconnect"))
        self._ws._unregister_context(self._context_id, self)


class _TTSContextsWSConnection(TTSContextsWSConnection):
    def __init__(self, manager: _TTSContextsWSConnectionManager) -> None:
        self._manager = manager
        self._inner_manager: TTSResourceConnectionManager | None = None
        self._inner_connection: TTSResourceConnection | None = None
        self._contexts: Dict[str, _TTSWSContext] = {}
        self._event_handler_registry = EventHandlerRegistry(use_lock=True)
        self._reader_thread: threading.Thread | None = None
        self._connect_lock = threading.Lock()
        self._closed_event = threading.Event()
        self._permanently_closed = False
        self._logger = logging.getLogger(__name__)

    @override
    def close(self) -> None:
        connection: TTSResourceConnection | None
        inner_manager: TTSResourceConnectionManager | None
        thread: threading.Thread | None
        with self._connect_lock:
            if self._permanently_closed:
                return
            self._permanently_closed = True
            connection = self._inner_connection
            inner_manager = self._inner_manager
            thread = self._reader_thread
            self._inner_connection = None
            self._inner_manager = None
            self._reader_thread = None
        if connection is not None:
            try:
                connection.close()
            except Exception:
                self._logger.warning("Error closing inner connection", exc_info=True)
        if thread is not None and thread is not threading.current_thread() and thread.is_alive():
            thread.join(timeout=5.0)
        if inner_manager is not None:
            try:
                inner_manager.__exit__(None, None, None)
            except Exception:
                self._logger.warning("Error exiting inner manager", exc_info=True)
        for ctx in list(self._contexts.values()):
            ctx._mark_closed()
        self._contexts.clear()
        self._closed_event.set()

    @override
    def context(
        self,
        *,
        model_id: str,
        voice: VoiceSpecifierParam,
        output_format: OutputFormat,
        context_id: Optional[str] = None,
        timeout: float | None = None,
        language: SupportedLanguage | None = None,
        add_timestamps: bool | None = None,
        add_phoneme_timestamps: bool | None = None,
    ) -> _TTSWSContext:
        self._ensure_connected()
        if context_id is None:
            context_id = str(uuid.uuid4())
        if context_id in self._contexts:
            raise CartesiaError(f"Duplicate context ID: {context_id}")
        ctx = _TTSWSContext(
            ws=self,
            context_id=context_id,
            timeout=timeout,
            model_id=model_id,
            voice=voice,
            output_format=output_format,
            language=language,
            add_timestamps=add_timestamps,
            add_phoneme_timestamps=add_phoneme_timestamps,
        )
        self._contexts[context_id] = ctx
        return ctx

    @override
    def get_context(self, context_id: str) -> _TTSWSContext | None:
        return self._contexts.get(context_id)

    @override
    def list_contexts(self) -> List[_TTSWSContext]:
        return list(self._contexts.values())

    @overload
    def on_error(self, handler: TTSContextsWSErrorHandler) -> _TTSContextsWSConnection: ...
    @overload
    def on_error(self) -> Callable[[TTSContextsWSErrorHandler], TTSContextsWSErrorHandler]: ...
    @override
    def on_error(
        self, handler: Optional[TTSContextsWSErrorHandler] = None
    ) -> Union[_TTSContextsWSConnection, Callable[[TTSContextsWSErrorHandler], TTSContextsWSErrorHandler]]:
        if handler is not None:
            self._event_handler_registry.add("error", handler)
            return self

        def decorator(fn: TTSContextsWSErrorHandler) -> TTSContextsWSErrorHandler:
            self._event_handler_registry.add("error", fn)
            return fn

        return decorator

    @override
    def off_error(self, handler: TTSContextsWSErrorHandler) -> _TTSContextsWSConnection:
        self._event_handler_registry.remove("error", handler)
        return self

    @overload
    def once_error(self, handler: TTSContextsWSErrorHandler) -> _TTSContextsWSConnection: ...
    @overload
    def once_error(self) -> Callable[[TTSContextsWSErrorHandler], TTSContextsWSErrorHandler]: ...
    @override
    def once_error(
        self, handler: Optional[TTSContextsWSErrorHandler] = None
    ) -> Union[_TTSContextsWSConnection, Callable[[TTSContextsWSErrorHandler], TTSContextsWSErrorHandler]]:
        if handler is not None:
            self._event_handler_registry.add("error", handler, once=True)
            return self

        def decorator(fn: TTSContextsWSErrorHandler) -> TTSContextsWSErrorHandler:
            self._event_handler_registry.add("error", fn, once=True)
            return fn

        return decorator

    @override
    def dispatch_events(self) -> None:
        self._closed_event.wait()

    # -- internals -----------------------------------------------------------

    def _send(self, event: WebsocketClientEvent | WebsocketClientEventParam) -> None:
        connection = self._inner_connection
        if connection is None:
            raise CartesiaError("TTSContextsWSConnection is not connected.")
        connection.send(event)

    def _unregister_context(self, context_id: str, ctx: TTSWSContext) -> None:
        if self._contexts.get(context_id) is ctx:
            self._contexts.pop(context_id, None)

    def _ensure_connected(self) -> None:
        from ...resources.tts import TTSResourceConnectionManager

        with self._connect_lock:
            if self._permanently_closed:
                raise CartesiaError("TTSContextsWSConnection is closed.")
            connection = self._inner_connection
            thread = self._reader_thread
            if connection is not None and thread is not None and thread.is_alive():
                return
            # Discard any stale state before building a new connection.
            self._teardown_inner_locked()
            inner_manager = TTSResourceConnectionManager(
                client=self._manager._client,
                extra_query=self._manager._extra_query,
                extra_headers=self._manager._extra_headers,
                websocket_connection_options=self._manager._websocket_connection_options,
                on_reconnecting=self._wrap_on_reconnecting(),
                max_retries=self._manager._max_retries,
                initial_delay=self._manager._initial_delay,
                max_delay=self._manager._max_delay,
                max_queue_size=self._manager._max_queue_size,
            )
            new_connection = inner_manager.enter()
            self._inner_manager = inner_manager
            self._inner_connection = new_connection
            self._reader_thread = threading.Thread(
                target=self._reader_loop,
                args=(new_connection,),
                name=f"cartesia-tts-ws-reader-{id(self):x}",
                daemon=True,
            )
            self._reader_thread.start()

    def _teardown_inner_locked(self) -> None:
        """Caller must hold ``_connect_lock``."""
        connection = self._inner_connection
        inner_manager = self._inner_manager
        thread = self._reader_thread
        self._inner_connection = None
        self._inner_manager = None
        self._reader_thread = None
        if connection is not None:
            try:
                connection.close()
            except Exception:
                self._logger.warning("Error closing inner connection during teardown", exc_info=True)
        if thread is not None and thread is not threading.current_thread() and thread.is_alive():
            thread.join(timeout=5.0)
        if inner_manager is not None:
            try:
                inner_manager.__exit__(None, None, None)
            except Exception:
                self._logger.warning("Error exiting inner manager during teardown", exc_info=True)

    def _wrap_on_reconnecting(
        self,
    ) -> Optional[Callable[[ReconnectingEvent], ReconnectingOverrides | None]]:
        user_callback = self._manager._on_reconnecting
        if user_callback is None:
            return None

        def wrapped(event: ReconnectingEvent) -> ReconnectingOverrides | None:
            if event.attempt == 1:
                # Server-side context_ids do not survive across a ws reconnect.
                # NOTE: this runs from the bg reader thread inside the inner
                # connection's _reconnect(), without holding _connect_lock.
                # Concurrent context() calls hold the lock
                # during inner_manager.__enter__() but only mutate _contexts
                # afterwards. CPython's GIL keeps individual dict ops atomic;
                # the worst case is a freshly-registered context surviving the
                # clear, against a freshly-reconnected ws that doesn't know it.
                self._clear_contexts_for_disconnect()
            return user_callback(event)

        return wrapped

    def _clear_contexts_for_disconnect(self) -> None:
        for ctx in list(self._contexts.values()):
            ctx._mark_closed()
        self._contexts.clear()

    def _reader_loop(self, connection: TTSResourceConnection) -> None:
        try:
            for response in connection:
                self._route_event(response)
        except Exception:
            self._logger.warning("WebSocket reader exited with exception", exc_info=True)
        finally:
            self._handle_terminal_disconnect(connection)

    def _route_event(self, response: WebsocketResponse) -> None:
        ctx_id = getattr(response, "context_id", None)
        if ctx_id:
            ctx = self._contexts.get(ctx_id)
            if ctx is not None:
                # Per-context queue is unbounded; put_nowait can't raise.
                ctx._queue.put_nowait(response)
        elif response.type == "error":
            # No context to consume the event. Surface "error" events to handlers;
            # silently drop everything else (it's already been logged on the wire).
            self._dispatch_error(response)

    def _dispatch_error(self, response: WebsocketResponse) -> None:
        for handler in self._event_handler_registry.get_handlers("error"):
            try:
                handler(response)
            except Exception:
                self._logger.exception("Error in 'error' handler")

    def _handle_terminal_disconnect(self, connection: TTSResourceConnection) -> None:
        inner_manager_to_close: TTSResourceConnectionManager | None = None
        with self._connect_lock:
            if self._inner_connection is not connection:
                # close() or another path already swapped this out.
                return
            self._inner_connection = None
            inner_manager_to_close = self._inner_manager
            self._inner_manager = None
            self._reader_thread = None
            self._clear_contexts_for_disconnect()
        if inner_manager_to_close is not None:
            try:
                inner_manager_to_close.__exit__(None, None, None)
            except Exception:
                self._logger.warning("Error exiting inner manager after disconnect", exc_info=True)


class _TTSContextsWSConnectionManager(TTSContextsWSConnectionManager):
    def __init__(
        self,
        *,
        client: Cartesia,
        extra_query: Query,
        extra_headers: Headers,
        websocket_connection_options: WebSocketConnectionOptions,
        on_reconnecting: Callable[[ReconnectingEvent], ReconnectingOverrides | None] | None = None,
        max_retries: int = 5,
        initial_delay: float = 0.5,
        max_delay: float = 8.0,
        max_queue_size: int = 1_048_576,
    ) -> None:
        self._client = client
        self._extra_query = extra_query
        self._extra_headers = extra_headers
        self._websocket_connection_options = websocket_connection_options
        self._on_reconnecting = on_reconnecting
        self._max_retries = max_retries
        self._initial_delay = initial_delay
        self._max_delay = max_delay
        self._max_queue_size = max_queue_size
        self._event_handler_registry = EventHandlerRegistry(use_lock=True)
        self._connection: TTSContextsWSConnection | None = None

    @overload
    def on_error(self, handler: TTSContextsWSErrorHandler) -> _TTSContextsWSConnectionManager: ...
    @overload
    def on_error(self) -> Callable[[TTSContextsWSErrorHandler], TTSContextsWSErrorHandler]: ...
    @override
    def on_error(
        self, handler: Optional[TTSContextsWSErrorHandler] = None
    ) -> Union[_TTSContextsWSConnectionManager, Callable[[TTSContextsWSErrorHandler], TTSContextsWSErrorHandler]]:
        if handler is not None:
            self._event_handler_registry.add("error", handler)
            return self

        def decorator(fn: TTSContextsWSErrorHandler) -> TTSContextsWSErrorHandler:
            self._event_handler_registry.add("error", fn)
            return fn

        return decorator

    @override
    def off_error(self, handler: TTSContextsWSErrorHandler) -> _TTSContextsWSConnectionManager:
        self._event_handler_registry.remove("error", handler)
        return self

    @overload
    def once_error(self, handler: TTSContextsWSErrorHandler) -> _TTSContextsWSConnectionManager: ...
    @overload
    def once_error(self) -> Callable[[TTSContextsWSErrorHandler], TTSContextsWSErrorHandler]: ...
    @override
    def once_error(
        self, handler: Optional[TTSContextsWSErrorHandler] = None
    ) -> Union[_TTSContextsWSConnectionManager, Callable[[TTSContextsWSErrorHandler], TTSContextsWSErrorHandler]]:
        if handler is not None:
            self._event_handler_registry.add("error", handler, once=True)
            return self

        def decorator(fn: TTSContextsWSErrorHandler) -> TTSContextsWSErrorHandler:
            self._event_handler_registry.add("error", fn, once=True)
            return fn

        return decorator

    @override
    def enter(self) -> _TTSContextsWSConnection:
        connection = _TTSContextsWSConnection(self)
        self._event_handler_registry.merge_into(connection._event_handler_registry)
        connection._ensure_connected()
        self._connection = connection
        return connection

    @override
    def __enter__(self) -> _TTSContextsWSConnection:
        return self.enter()

    @override
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if self._connection is not None:
            self._connection.close()


# ---------------------------------------------------------------------------
# Async
# ---------------------------------------------------------------------------


class _AsyncTTSWSContext(AsyncTTSWSContext):
    def __init__(
        self,
        *,
        ws: _AsyncTTSContextsWSConnection,
        timeout: float | None = None,
        context_id: str,
        model_id: str,
        voice: VoiceSpecifierParam,
        output_format: OutputFormat,
        language: SupportedLanguage | None = None,
        add_timestamps: bool | None = None,
        add_phoneme_timestamps: bool | None = None,
    ) -> None:
        self._ws = ws
        self._context_id = context_id
        self._queue: asyncio.Queue[WebsocketResponse | _Sentinel] = asyncio.Queue()
        self._closed = False
        self._timeout = timeout
        self._model_id = model_id
        self._voice = voice
        self._output_format = output_format
        self._language = language
        self._add_timestamps: bool | Omit = add_timestamps if add_timestamps is not None else omit
        self._add_phoneme_timestamps: bool | Omit = (
            add_phoneme_timestamps if add_phoneme_timestamps is not None else omit
        )

    @property
    @override
    def context_id(self) -> str:
        return self._context_id

    @property
    @override
    def is_closed(self) -> bool:
        return self._closed

    @override
    async def push(
        self,
        transcript: str,
        *,
        generation_config: Optional[GenerationConfigParam] = None,
        continue_: Optional[bool] = True,
        extra_args: Optional[Mapping[str, Any]] = None,
    ) -> None:
        if self.is_closed:
            raise CartesiaError(f"Cannot push to closed context ({self._context_id}).")

        request = _build_generation_request(
            context_id=self._context_id,
            model_id=self._model_id,
            transcript=transcript,
            voice=self._voice,
            output_format=self._output_format,
            continue_=True if continue_ is None else continue_,
            language=self._language,
            add_timestamps=self._add_timestamps,
            add_phoneme_timestamps=self._add_phoneme_timestamps,
            flush=omit,
            generation_config=generation_config,
            extra={} if extra_args is None else extra_args,
        )
        await self._ws._send(request)

    @override
    async def end(self) -> None:
        if self.is_closed:
            return
        request = _build_generation_request(
            context_id=self._context_id,
            model_id=self._model_id,
            transcript="",
            voice=self._voice,
            output_format=self._output_format,
            continue_=False,
            language=self._language,
            add_timestamps=self._add_timestamps,
            add_phoneme_timestamps=self._add_phoneme_timestamps,
            flush=omit,
            generation_config=None,
            extra={},
        )

        try:
            await self._ws._send(request)
        except WebSocketQueueFullError:
            raise
        except CartesiaError:
            pass

    @override
    async def flush(self) -> None:
        if self.is_closed:
            raise CartesiaError(f"Cannot flush closed context ({self._context_id}).")
        request = _build_generation_request(
            context_id=self._context_id,
            model_id=self._model_id,
            transcript="",
            voice=self._voice,
            output_format=self._output_format,
            continue_=True,
            language=self._language,
            add_timestamps=self._add_timestamps,
            add_phoneme_timestamps=self._add_phoneme_timestamps,
            flush=True,
            generation_config=None,
            extra={},
        )
        await self._ws._send(request)

    @override
    async def cancel(self) -> None:
        if self.is_closed:
            return
        try:
            await self._ws._send(CancelContextRequest(cancel=True, context_id=self._context_id))
        except WebSocketQueueFullError:
            raise
        except CartesiaError:
            pass
        self._mark_closed()

    @override
    async def receive(self) -> AsyncIterator[WebsocketResponse]:
        if self.is_closed:
            # Already drained; subsequent receive() calls return immediately
            # rather than blocking on an empty queue.
            return
        try:
            while True:
                try:
                    if self._timeout is not None:
                        item = await asyncio.wait_for(self._queue.get(), timeout=self._timeout)
                    else:
                        item = await self._queue.get()
                except asyncio.TimeoutError:
                    yield WebSocketResponseError(
                        type="error",
                        done=True,
                        context_id=self._context_id,
                        error_code="client_timeout",
                        title="Timeout",
                        message=(f"Client-side timeout of {self._timeout}s reached with no events from the server."),
                    )
                    return
                if isinstance(item, _Sentinel):
                    if item.kind == "disconnect":
                        return
                else:
                    yield item
                    if _is_terminal(item):
                        return
        finally:
            self._mark_closed()

    def _mark_closed(self) -> None:
        if self._closed:
            return
        self._closed = True
        # Wake any pending receive() loop. The queue is unbounded so put_nowait can't raise.
        self._queue.put_nowait(_Sentinel("disconnect"))
        self._ws._unregister_context(self._context_id, self)


class _AsyncTTSContextsWSConnection(AsyncTTSContextsWSConnection):
    def __init__(self, manager: _AsyncTTSContextsWSConnectionManager) -> None:
        self._manager = manager
        self._inner_manager: AsyncTTSResourceConnectionManager | None = None
        self._inner_connection: AsyncTTSResourceConnection | None = None
        self._contexts: Dict[str, _AsyncTTSWSContext] = {}
        self._event_handler_registry = EventHandlerRegistry(use_lock=False)
        self._reader_task: asyncio.Task[None] | None = None
        self._connect_lock = asyncio.Lock()
        self._closed_event = asyncio.Event()
        self._permanently_closed = False
        self._logger = logging.getLogger(__name__)

    @override
    async def close(self) -> None:
        connection: AsyncTTSResourceConnection | None
        inner_manager: AsyncTTSResourceConnectionManager | None
        task: asyncio.Task[None] | None
        async with self._connect_lock:
            if self._permanently_closed:
                return
            self._permanently_closed = True
            connection = self._inner_connection
            inner_manager = self._inner_manager
            task = self._reader_task
            self._inner_connection = None
            self._inner_manager = None
            self._reader_task = None
        if connection is not None:
            try:
                await connection.close()
            except Exception:
                self._logger.warning("Error closing inner connection", exc_info=True)
        if task is not None and not task.done() and task is not asyncio.current_task():
            try:
                await asyncio.wait_for(task, timeout=5.0)
            except asyncio.TimeoutError:
                task.cancel()
                try:
                    await task
                except (asyncio.CancelledError, Exception):
                    pass
            except (asyncio.CancelledError, Exception):
                pass
        if inner_manager is not None:
            try:
                await inner_manager.__aexit__(None, None, None)
            except Exception:
                self._logger.warning("Error exiting inner manager", exc_info=True)
        for ctx in list(self._contexts.values()):
            ctx._mark_closed()
        self._contexts.clear()
        self._closed_event.set()

    @override
    async def context(
        self,
        *,
        model_id: str,
        voice: VoiceSpecifierParam,
        output_format: OutputFormat,
        context_id: Optional[str] = None,
        timeout: float | None = None,
        language: SupportedLanguage | None = None,
        add_timestamps: bool | None = None,
        add_phoneme_timestamps: bool | None = None,
    ) -> _AsyncTTSWSContext:
        await self._ensure_connected()
        if context_id is None:
            context_id = str(uuid.uuid4())
        if context_id in self._contexts:
            raise CartesiaError(f"Duplicate context ID: {context_id}")
        ctx = _AsyncTTSWSContext(
            ws=self,
            context_id=context_id,
            timeout=timeout,
            model_id=model_id,
            voice=voice,
            output_format=output_format,
            language=language,
            add_timestamps=add_timestamps,
            add_phoneme_timestamps=add_phoneme_timestamps,
        )
        self._contexts[context_id] = ctx
        return ctx

    @override
    def get_context(self, context_id: str) -> _AsyncTTSWSContext | None:
        return self._contexts.get(context_id)

    @override
    def list_contexts(self) -> List[_AsyncTTSWSContext]:
        return list(self._contexts.values())

    @overload
    def on_error(self, handler: TTSContextsWSErrorHandler) -> _AsyncTTSContextsWSConnection: ...
    @overload
    def on_error(self) -> Callable[[TTSContextsWSErrorHandler], TTSContextsWSErrorHandler]: ...
    @override
    def on_error(
        self, handler: Optional[TTSContextsWSErrorHandler] = None
    ) -> Union[_AsyncTTSContextsWSConnection, Callable[[TTSContextsWSErrorHandler], TTSContextsWSErrorHandler]]:
        if handler is not None:
            self._event_handler_registry.add("error", handler)
            return self

        def decorator(fn: TTSContextsWSErrorHandler) -> TTSContextsWSErrorHandler:
            self._event_handler_registry.add("error", fn)
            return fn

        return decorator

    @override
    def off_error(self, handler: TTSContextsWSErrorHandler) -> _AsyncTTSContextsWSConnection:
        self._event_handler_registry.remove("error", handler)
        return self

    @overload
    def once_error(self, handler: TTSContextsWSErrorHandler) -> _AsyncTTSContextsWSConnection: ...
    @overload
    def once_error(self) -> Callable[[TTSContextsWSErrorHandler], TTSContextsWSErrorHandler]: ...
    @override
    def once_error(
        self, handler: Optional[TTSContextsWSErrorHandler] = None
    ) -> Union[_AsyncTTSContextsWSConnection, Callable[[TTSContextsWSErrorHandler], TTSContextsWSErrorHandler]]:
        if handler is not None:
            self._event_handler_registry.add("error", handler, once=True)
            return self

        def decorator(fn: TTSContextsWSErrorHandler) -> TTSContextsWSErrorHandler:
            self._event_handler_registry.add("error", fn, once=True)
            return fn

        return decorator

    @override
    async def dispatch_events(self) -> None:
        await self._closed_event.wait()

    # -- internals -----------------------------------------------------------

    async def _send(self, event: WebsocketClientEvent | WebsocketClientEventParam) -> None:
        connection = self._inner_connection
        if connection is None:
            raise CartesiaError("AsyncTTSContextsWSConnection is not connected.")
        await connection.send(event)

    def _unregister_context(self, context_id: str, ctx: AsyncTTSWSContext) -> None:
        if self._contexts.get(context_id) is ctx:
            self._contexts.pop(context_id, None)

    async def _ensure_connected(self) -> None:
        from ...resources.tts import AsyncTTSResourceConnectionManager

        async with self._connect_lock:
            if self._permanently_closed:
                raise CartesiaError("AsyncTTSContextsWSConnection is closed.")
            connection = self._inner_connection
            task = self._reader_task
            if connection is not None and task is not None and not task.done():
                return
            await self._teardown_inner_locked()
            inner_manager = AsyncTTSResourceConnectionManager(
                client=self._manager._client,
                extra_query=self._manager._extra_query,
                extra_headers=self._manager._extra_headers,
                websocket_connection_options=self._manager._websocket_connection_options,
                on_reconnecting=self._wrap_on_reconnecting(),
                max_retries=self._manager._max_retries,
                initial_delay=self._manager._initial_delay,
                max_delay=self._manager._max_delay,
                max_queue_size=self._manager._max_queue_size,
            )
            new_connection = await inner_manager.enter()
            self._inner_manager = inner_manager
            self._inner_connection = new_connection
            self._reader_task = asyncio.create_task(
                self._reader_loop(new_connection),
                name=f"cartesia-tts-ws-reader-{id(self):x}",
            )

    async def _teardown_inner_locked(self) -> None:
        """Caller must hold ``_connect_lock``."""
        connection = self._inner_connection
        inner_manager = self._inner_manager
        task = self._reader_task
        self._inner_connection = None
        self._inner_manager = None
        self._reader_task = None
        if connection is not None:
            try:
                await connection.close()
            except Exception:
                self._logger.warning("Error closing inner connection during teardown", exc_info=True)
        if task is not None and not task.done() and task is not asyncio.current_task():
            try:
                await asyncio.wait_for(task, timeout=5.0)
            except asyncio.TimeoutError:
                task.cancel()
                try:
                    await task
                except (asyncio.CancelledError, Exception):
                    pass
            except (asyncio.CancelledError, Exception):
                pass
        if inner_manager is not None:
            try:
                await inner_manager.__aexit__(None, None, None)
            except Exception:
                self._logger.warning("Error exiting inner manager during teardown", exc_info=True)

    def _wrap_on_reconnecting(
        self,
    ) -> Optional[Callable[[ReconnectingEvent], ReconnectingOverrides | None]]:
        user_callback = self._manager._on_reconnecting
        if user_callback is None:
            return None

        def wrapped(event: ReconnectingEvent) -> ReconnectingOverrides | None:
            if event.attempt == 1:
                # Server-side context_ids do not survive across a ws reconnect.
                # NOTE: this runs from the bg reader task inside the inner
                # connection's _reconnect(), without holding _connect_lock.
                # Concurrent context() calls on the same loop hold the lock
                # during inner_manager.__aenter__() but only mutate _contexts
                # afterwards. Since asyncio runs single-threaded, dict mutation
                # is safe; the worst case is a freshly-registered context
                # surviving the clear, against a freshly-reconnected ws that
                # doesn't know it.
                self._clear_contexts_for_disconnect()
            return user_callback(event)

        return wrapped

    def _clear_contexts_for_disconnect(self) -> None:
        for ctx in list(self._contexts.values()):
            ctx._mark_closed()
        self._contexts.clear()

    async def _reader_loop(self, connection: AsyncTTSResourceConnection) -> None:
        try:
            async for response in connection:
                self._route_event(response)
        except asyncio.CancelledError:
            raise
        except Exception:
            self._logger.warning("WebSocket reader exited with exception", exc_info=True)
        finally:
            await self._handle_terminal_disconnect(connection)

    def _route_event(self, response: WebsocketResponse) -> None:
        ctx_id = getattr(response, "context_id", None)
        if ctx_id:
            ctx = self._contexts.get(ctx_id)
            if ctx is not None:
                # Per-context queue is unbounded; put_nowait can't raise.
                ctx._queue.put_nowait(response)
        elif response.type == "error":
            # No context to consume the event. Surface "error" events to handlers;
            # silently drop everything else (it's already been logged on the wire).
            self._dispatch_error(response)

    def _dispatch_error(self, response: WebsocketResponse) -> None:
        for handler in self._event_handler_registry.get_handlers("error"):
            try:
                result = handler(response)
            except Exception:
                self._logger.exception("Error in 'error' handler")
                continue
            if asyncio.iscoroutine(result):
                # Fire-and-forget; the handler is responsible for its own lifetime.
                asyncio.create_task(result)

    async def _handle_terminal_disconnect(self, connection: AsyncTTSResourceConnection) -> None:
        inner_manager_to_close: AsyncTTSResourceConnectionManager | None = None
        async with self._connect_lock:
            if self._inner_connection is not connection:
                return
            self._inner_connection = None
            inner_manager_to_close = self._inner_manager
            self._inner_manager = None
            self._reader_task = None
            self._clear_contexts_for_disconnect()
        if inner_manager_to_close is not None:
            try:
                await inner_manager_to_close.__aexit__(None, None, None)
            except Exception:
                self._logger.warning("Error exiting inner manager after disconnect", exc_info=True)


class _AsyncTTSContextsWSConnectionManager(AsyncTTSContextsWSConnectionManager):
    def __init__(
        self,
        *,
        client: AsyncCartesia,
        extra_query: Query,
        extra_headers: Headers,
        websocket_connection_options: WebSocketConnectionOptions,
        on_reconnecting: Callable[[ReconnectingEvent], ReconnectingOverrides | None] | None = None,
        max_retries: int = 5,
        initial_delay: float = 0.5,
        max_delay: float = 8.0,
        max_queue_size: int = 1_048_576,
    ) -> None:
        self._client = client
        self._extra_query = extra_query
        self._extra_headers = extra_headers
        self._websocket_connection_options = websocket_connection_options
        self._on_reconnecting = on_reconnecting
        self._max_retries = max_retries
        self._initial_delay = initial_delay
        self._max_delay = max_delay
        self._max_queue_size = max_queue_size
        self._event_handler_registry = EventHandlerRegistry(use_lock=False)
        self._connection: AsyncTTSContextsWSConnection | None = None

    @overload
    def on_error(self, handler: TTSContextsWSErrorHandler) -> _AsyncTTSContextsWSConnectionManager: ...
    @overload
    def on_error(self) -> Callable[[TTSContextsWSErrorHandler], TTSContextsWSErrorHandler]: ...
    @override
    def on_error(
        self, handler: Optional[TTSContextsWSErrorHandler] = None
    ) -> Union[_AsyncTTSContextsWSConnectionManager, Callable[[TTSContextsWSErrorHandler], TTSContextsWSErrorHandler]]:
        if handler is not None:
            self._event_handler_registry.add("error", handler)
            return self

        def decorator(fn: TTSContextsWSErrorHandler) -> TTSContextsWSErrorHandler:
            self._event_handler_registry.add("error", fn)
            return fn

        return decorator

    @override
    def off_error(self, handler: TTSContextsWSErrorHandler) -> _AsyncTTSContextsWSConnectionManager:
        """Remove a previously registered error handler."""
        self._event_handler_registry.remove("error", handler)
        return self

    @overload
    def once_error(self, handler: TTSContextsWSErrorHandler) -> _AsyncTTSContextsWSConnectionManager: ...
    @overload
    def once_error(self) -> Callable[[TTSContextsWSErrorHandler], TTSContextsWSErrorHandler]: ...
    @override
    def once_error(
        self, handler: Optional[TTSContextsWSErrorHandler] = None
    ) -> Union[_AsyncTTSContextsWSConnectionManager, Callable[[TTSContextsWSErrorHandler], TTSContextsWSErrorHandler]]:
        if handler is not None:
            self._event_handler_registry.add("error", handler, once=True)
            return self

        def decorator(fn: TTSContextsWSErrorHandler) -> TTSContextsWSErrorHandler:
            self._event_handler_registry.add("error", fn, once=True)
            return fn

        return decorator

    @override
    async def enter(self) -> _AsyncTTSContextsWSConnection:
        connection = _AsyncTTSContextsWSConnection(self)
        self._event_handler_registry.merge_into(connection._event_handler_registry)
        await connection._ensure_connected()
        self._connection = connection
        return connection

    @override
    async def __aenter__(self) -> _AsyncTTSContextsWSConnection:
        return await self.enter()

    @override
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if self._connection is not None:
            await self._connection.close()
