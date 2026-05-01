from __future__ import annotations

import uuid
import queue
import asyncio
import logging
import threading
from types import TracebackType
from typing import TYPE_CHECKING, Any, Dict, List, Union, Mapping, Callable, Iterator, Optional, cast, overload
from typing_extensions import AsyncIterator

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
from ..._exceptions import CartesiaError, WebSocketQueueFullError as WebSocketQueueFullError
from ..._event_handler import EventHandlerRegistry
from ...types.websocket_response import Error as WebSocketResponseError
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

log: logging.Logger = logging.getLogger(__name__)


_ErrorHandler = Callable[[WebSocketResponseError], Any]
"""Type of an error event handler.

For :class:`AsyncTTSContextsConnection`, the handler may also be ``async def``
— its returned coroutine is scheduled as a fire-and-forget task.
"""


class _Sentinel:
    """Marker placed on a context queue when the context is closing."""


_DISCONNECT_SENTINEL = _Sentinel()


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


class TTSContext:
    """
    Contexts are short-lived and designed to generate audio for a single transcript.

    The transcript can broken up into chunks and streamed over time using continuations,
    which is useful if you're still in the middle of generating your transcript.

    See [the API docs](https://docs.cartesia.ai/use-the-api/tts-websocket/contexts) for details.
    """

    def __init__(
        self,
        *,
        contexts: TTSContextsConnection,
        timeout: float | None = None,
        context_id: str,
        model_id: str,
        voice: VoiceSpecifierParam,
        output_format: OutputFormat,
        language: SupportedLanguage | None = None,
        add_timestamps: bool | None = None,
        add_phoneme_timestamps: bool | None = None,
    ) -> None:
        self._contexts = contexts
        self._context_id = context_id
        self._queue: queue.Queue[Any] = queue.Queue()
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
    def context_id(self) -> str:
        """A unique identifier for this context within the WebSocket connection."""
        return self._context_id

    @property
    def is_closed(self) -> bool:
        """
        If true, :meth:`push` and :meth:`flush` will raise :class:`CartesiaError`.

        Once a context is closed, a new one must be created to generated more audio.
        """
        return self._closed

    def push(
        self,
        transcript: str,
        *,
        continue_: Optional[bool] = True,
        generation_config: Optional[GenerationConfigParam] = None,
        **kwargs: Any,
    ) -> None:
        """Call this multiple times to stream transcript chunks, then call :meth:`end` to finish.

        Args:
            transcript (str): Transcript chunk to add to the context.
            continue_ (bool): If set to false, signal that the transcript is complete.
                You do not need to call :meth:`end` if you send a request with ``continue_=False``.
                Defaults to True.
            generation_config (GenerationConfigParam, optional): Speed, volume, and emotion controls.

        Raises:
            :class:`WebSocketQueueFullError`: If sending the request fails due to too many requests being queued.

            :class:`CartesiaError`: If the request cannot be sent.

        .. note::
            The server may still send a :class:`WebSocketResponseError` message even if this method
            did not raise an exception.

        See Also:
            :meth:`end`: Signal that no more transcript chunks will be sent.
            :meth:`flush`: Request a flush so buffered transcript is generated immediately.
            :meth:`cancel`: Abort generation in progress.
            :meth:`receive`: Consume audio chunks and other events for this context.
        """
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
            extra=kwargs,
        )
        self._contexts._send(request)

    def end(self) -> None:
        """Signal that no more transcript chunks will be sent.

        You must call this method if you are relying on Cartesia to manage buffering
        (default behavior). See
        [the API docs](https://docs.cartesia.ai/use-the-api/tts-websocket/buffering) for details.

        Raises:
            :class:`WebSocketQueueFullError`: If sending the request fails due to too many requests being queued.

        See Also:
            :meth:`push`: Stream transcript chunks before calling :meth:`end`.
            :meth:`cancel`: Abort generation immediately instead of letting it finish gracefully.
        """
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
            self._contexts._send(request)
        except WebSocketQueueFullError:
            raise
        except CartesiaError:
            pass

    def flush(self) -> None:
        """Flushes the context. You should ignore this method unless you need flushes.

        Useful if you need to know when transcript chunks finished generating. You will
        receive a ``flush_done`` event once the transcript pushed to this context so far
        by :meth:`push` is done generating. See
        [the API docs](https://docs.cartesia.ai/use-the-api/tts-websocket/context-flushing-and-flush-i-ds)
        for details.

        Raises:
            :class:`WebSocketQueueFullError`: If sending the request fails due to too many requests being queued.

            :class:`CartesiaError`: If the request cannot be sent.

        .. note::
            The server may still send a :class:`WebSocketResponseError` message even if this method
            did not raise an exception.

        See Also:
            :meth:`push`: Stream transcript chunks.
            :meth:`end`: Signal that no more transcript chunks will be sent.
        """
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
        self._contexts._send(request)

    def cancel(self) -> None:
        """Cancel this context to stop generating speech.

        Raises:
            :class:`WebSocketQueueFullError`: If sending the request fails due to too many requests being queued.

        See Also:
            :meth:`end`: Signal that no more transcript chunks will be sent (graceful completion).
            :attr:`is_closed`: Will be ``True`` after :meth:`cancel` returns.
        """
        if self._closed:
            return
        try:
            self._contexts._send(CancelContextRequest(cancel=True, context_id=self._context_id))
        except WebSocketQueueFullError:
            raise
        except CartesiaError:
            pass
        self._mark_closed()

    def receive(self) -> Iterator[WebsocketResponse]:
        """Iterate over messages for this context.

        Yields:
            Iterator[WebsocketResponse]: Audio chunks (and timestamps if requested) are streamed in multiple messages as they are generated.
                :class:`WebSocketResponseError` with ``error_code="client_timeout"`` is sent if the context's timeout was reached and no messages were seen.

        See Also:
            :meth:`push`: Stream transcript chunks.
            :meth:`end`: Signal that no more transcript chunks will be sent.
        """

        if self._closed:
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
                    return
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
        self._queue.put_nowait(_DISCONNECT_SENTINEL)
        self._contexts._unregister_context(self._context_id, self)


class TTSContextsConnection:
    """Used to create instances of :class:`TTSContext` on a single WebSocket connection."""

    def __init__(self, manager: TTSContextsConnectionManager) -> None:
        self._manager = manager
        self._inner_manager: TTSResourceConnectionManager | None = None
        self._inner_connection: TTSResourceConnection | None = None
        self._contexts: Dict[str, TTSContext] = {}
        self._event_handler_registry = EventHandlerRegistry(use_lock=True)
        self._reader_thread: threading.Thread | None = None
        self._connect_lock = threading.Lock()
        self._closed_event = threading.Event()
        self._permanently_closed = False

    def close(self) -> None:
        """Close the WebSocket and cleanup all resources."""
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
                log.warning("Error closing inner connection", exc_info=True)
        if thread is not None and thread is not threading.current_thread() and thread.is_alive():
            thread.join(timeout=5.0)
        if inner_manager is not None:
            try:
                inner_manager.__exit__(None, None, None)
            except Exception:
                log.warning("Error exiting inner manager", exc_info=True)
        for ctx in list(self._contexts.values()):
            ctx._mark_closed()
        self._contexts.clear()
        self._closed_event.set()

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
    ) -> TTSContext:
        """Create a context. TTSContexts are short-lived and designed to generate audio for a single transcript.

        See [the API docs](https://docs.cartesia.ai/use-the-api/tts-websocket/contexts) for details.

        Args:
            model_id: Model used to generate audio for this context.
            voice: Voice for this context.
            output_format: Output audio format for this context.
            context_id: Unique identifier for this context. If not provided,
                a UUID will be auto-generated. Must be unique per WebSocket connection
                if provided.
            timeout: Client-side receive timeout in seconds. If set, :meth:`TTSContext.receive`
                will yield a synthetic ``client_timeout`` :class:`WebSocketResponseError` and return when no
                events arrive within the timeout.
            language: Language for this context.
            add_timestamps: Include word-level timestamps.
            add_phoneme_timestamps: Include phoneme-level timestamps.

        Returns:
            :class:`TTSContext` for generating audio on the context.

        Raises:
            :class:`CartesiaError`: If a :class:`TTSContext` with the same ``context_id`` already exists.
        """
        self._ensure_connected()
        if context_id is None:
            context_id = str(uuid.uuid4())
        if context_id in self._contexts:
            raise CartesiaError(f"Duplicate context ID: {context_id}")
        ctx = TTSContext(
            contexts=self,
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

    def get_context(self, context_id: str) -> TTSContext | None:
        """
        Gets the context created by :meth:`context`.
        Contexts are automatically cleaned up when :meth:`TTSContext.receive` returns.

        Args:
            context_id: :attr:`TTSContext.context_id`

        Returns:
            :class:`TTSContext` or ``None`` if it was cleaned up.
        """
        return self._contexts.get(context_id)

    def list_contexts(self) -> List[TTSContext]:
        """
        Lists all contexts created by :meth:`context` that have not been cleaned up.
        Contexts are automatically cleaned up when :meth:`TTSContext.receive` returns.

        Returns:
            A list of :class:`TTSContext`.
        """
        return list(self._contexts.values())

    @overload
    def on_error(self, handler: _ErrorHandler) -> TTSContextsConnection: ...
    @overload
    def on_error(self) -> Callable[[_ErrorHandler], _ErrorHandler]: ...
    def on_error(
        self, handler: Optional[_ErrorHandler] = None
    ) -> Union[TTSContextsConnection, Callable[[_ErrorHandler], _ErrorHandler]]:
        """Register a handler for ``error`` events that don't have a ``context_id``.

        Errors with a ``context_id`` are delivered through :meth:`AsyncTTSContext.receive` instead.

        No checks are made to see if the handler has already been added.
        Multiple calls with the same handler register it multiple times.

        Can be used as a method (returns ``self`` for chaining)::

            connection.on_error(my_handler)

        Or as a decorator::

            @connection.on_error()
            def my_handler(event): ...
        """
        if handler is not None:
            self._event_handler_registry.add("error", handler)
            return self

        def decorator(fn: _ErrorHandler) -> _ErrorHandler:
            self._event_handler_registry.add("error", fn)
            return fn

        return decorator

    def off_error(self, handler: _ErrorHandler) -> TTSContextsConnection:
        """Remove a previously registered error handler."""
        self._event_handler_registry.remove("error", handler)
        return self

    @overload
    def once_error(self, handler: _ErrorHandler) -> TTSContextsConnection: ...
    @overload
    def once_error(self) -> Callable[[_ErrorHandler], _ErrorHandler]: ...
    def once_error(
        self, handler: Optional[_ErrorHandler] = None
    ) -> Union[TTSContextsConnection, Callable[[_ErrorHandler], _ErrorHandler]]:
        """Register a one-time error handler. Automatically removed after first invocation.

        Supports both method and decorator forms; see :meth:`on_error`.
        """
        if handler is not None:
            self._event_handler_registry.add("error", handler, once=True)
            return self

        def decorator(fn: _ErrorHandler) -> _ErrorHandler:
            self._event_handler_registry.add("error", fn, once=True)
            return fn

        return decorator

    def dispatch_events(self) -> None:
        """Block the calling thread until :meth:`close` is called.

        A background thread continuously reads from the underlying WebSocket
        and dispatches non-context error events to handlers registered via
        :meth:`on`. This method merely parks the calling thread.
        """
        self._closed_event.wait()

    # -- internals -----------------------------------------------------------

    def _send(self, event: WebsocketClientEvent | WebsocketClientEventParam) -> None:
        connection = self._inner_connection
        if connection is None:
            raise CartesiaError("TTSContextsConnection is not connected.")
        connection.send(event)

    def _unregister_context(self, context_id: str, ctx: TTSContext) -> None:
        if self._contexts.get(context_id) is ctx:
            self._contexts.pop(context_id, None)

    def _ensure_connected(self) -> None:
        from ...resources.tts import TTSResourceConnectionManager

        with self._connect_lock:
            if self._permanently_closed:
                raise CartesiaError("TTSContextsConnection is closed.")
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
                log.warning("Error closing inner connection during teardown", exc_info=True)
        if thread is not None and thread is not threading.current_thread() and thread.is_alive():
            thread.join(timeout=5.0)
        if inner_manager is not None:
            try:
                inner_manager.__exit__(None, None, None)
            except Exception:
                log.warning("Error exiting inner manager during teardown", exc_info=True)

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
                # Concurrent context() calls on the main thread hold the lock
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
            log.warning("WebSocket reader exited with exception", exc_info=True)
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
            self._dispatch_error(response)

    def _dispatch_error(self, response: WebsocketResponse) -> None:
        for handler in self._event_handler_registry.get_handlers("error"):
            try:
                handler(response)
            except Exception:
                log.exception("Error in 'error' handler")

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
                log.warning("Error exiting inner manager after disconnect", exc_info=True)


class TTSContextsConnectionManager:
    """
    Context manager over a :class:`TTSContextsConnection` that is returned by `tts.create_context_manager()`

    This context manager ensures that the connection will be closed when it exits.

    ---

    Note that if your application doesn't work well with the context manager approach then you
    can call :meth:`enter` directly to initiate a connection.

    **Warning**: You must remember to close the connection with :meth:`TTSContextsConnection.close` if you use :meth:`enter`.

    ```py
    # using .__enter__()
    with client.tts.create_context_manager(...) as connection:
        # ...

    # using .enter()
    connection = client.tts.create_context_manager(...).enter()
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
        self._contexts: TTSContextsConnection | None = None

    @overload
    def on_error(self, handler: _ErrorHandler) -> TTSContextsConnectionManager: ...
    @overload
    def on_error(self) -> Callable[[_ErrorHandler], _ErrorHandler]: ...
    def on_error(
        self, handler: Optional[_ErrorHandler] = None
    ) -> Union[TTSContextsConnectionManager, Callable[[_ErrorHandler], _ErrorHandler]]:
        """Register an error handler before the connection is established.

        The handler is transferred to the connection on enter.
        See :meth:`TTSContextsConnection.on_error`.
        """
        if handler is not None:
            self._event_handler_registry.add("error", handler)
            return self

        def decorator(fn: _ErrorHandler) -> _ErrorHandler:
            self._event_handler_registry.add("error", fn)
            return fn

        return decorator

    def off_error(self, handler: _ErrorHandler) -> TTSContextsConnectionManager:
        """Remove a previously registered error handler."""
        self._event_handler_registry.remove("error", handler)
        return self

    @overload
    def once_error(self, handler: _ErrorHandler) -> TTSContextsConnectionManager: ...
    @overload
    def once_error(self) -> Callable[[_ErrorHandler], _ErrorHandler]: ...
    def once_error(
        self, handler: Optional[_ErrorHandler] = None
    ) -> Union[TTSContextsConnectionManager, Callable[[_ErrorHandler], _ErrorHandler]]:
        """Register a one-time error handler before the connection is established."""
        if handler is not None:
            self._event_handler_registry.add("error", handler, once=True)
            return self

        def decorator(fn: _ErrorHandler) -> _ErrorHandler:
            self._event_handler_registry.add("error", fn, once=True)
            return fn

        return decorator

    def __enter__(self) -> TTSContextsConnection:
        """
        If your application doesn't work well with the context manager approach then you
        can call this method directly to initiate a connection.

        **Warning**: You must remember to close the connection with :meth:`TTSContextsConnection.close`.

        ```py
        contexts = client.tts.create_context_manager(...).enter()
        # ...
        contexts.close()
        ```
        """
        contexts = TTSContextsConnection(self)
        self._event_handler_registry.merge_into(contexts._event_handler_registry)
        contexts._ensure_connected()
        self._contexts = contexts
        return contexts

    enter = __enter__

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if self._contexts is not None:
            self._contexts.close()


# ---------------------------------------------------------------------------
# Async
# ---------------------------------------------------------------------------


class AsyncTTSContext:
    """
    Contexts are short-lived and designed to generate audio for a single transcript.

    The transcript can broken up into chunks and streamed over time using continuations,
    which is useful if you're still in the middle of generating your transcript.

    See [the API docs](https://docs.cartesia.ai/use-the-api/tts-websocket/contexts) for details.
    """

    def __init__(
        self,
        *,
        contexts: AsyncTTSContextsConnection,
        timeout: float | None = None,
        context_id: str,
        model_id: str,
        voice: VoiceSpecifierParam,
        output_format: OutputFormat,
        language: SupportedLanguage | None = None,
        add_timestamps: bool | None = None,
        add_phoneme_timestamps: bool | None = None,
    ) -> None:
        self._contexts = contexts
        self._context_id = context_id
        self._queue: asyncio.Queue[Any] = asyncio.Queue()
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
    def context_id(self) -> str:
        """A unique identifier for this context within the WebSocket connection."""
        return self._context_id

    @property
    def is_closed(self) -> bool:
        """
        If true, :meth:`push` and :meth:`flush` will raise :class:`CartesiaError`.

        Once a context is closed, a new one must be created to generated more audio.
        """
        return self._closed

    async def push(
        self,
        transcript: str,
        *,
        continue_: Optional[bool] = True,
        generation_config: Optional[GenerationConfigParam] = None,
        **kwargs: Any,
    ) -> None:
        """Call this multiple times to stream transcript chunks, then call :meth:`end` to finish.

        Args:
            transcript (str): Transcript chunk to add to the context.
            continue_ (bool): If set to false, signal that the transcript is complete.
                You do not need to call :meth:`end` if you send a request with ``continue_=False``.
                Defaults to True.
            generation_config (GenerationConfigParam, optional): Speed, volume, and emotion controls.

        Raises:
            :class:`WebSocketQueueFullError`: If sending the request fails due to too many requests being queued.

            :class:`CartesiaError`: If the request cannot be sent.

        .. note::
            The server may still send a :class:`WebSocketResponseError` message even if this method
            did not raise an exception.

        See Also:
            :meth:`end`: Signal that no more transcript chunks will be sent.
            :meth:`flush`: Request a flush so buffered transcript is generated immediately.
            :meth:`cancel`: Abort generation in progress.
            :meth:`receive`: Consume audio chunks and other events for this context.
        """
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
            extra=kwargs,
        )
        await self._contexts._send(request)

    async def end(self) -> None:
        """Signal that no more transcript chunks will be sent.

        You must call this method if you are relying on Cartesia to manage buffering
        (default behavior). See
        [the API docs](https://docs.cartesia.ai/use-the-api/tts-websocket/buffering) for details.

        Raises:
            :class:`WebSocketQueueFullError`: If sending the request fails due to too many requests being queued.

        See Also:
            :meth:`push`: Stream transcript chunks before calling :meth:`end`.
            :meth:`cancel`: Abort generation immediately instead of letting it finish gracefully.
        """
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
            await self._contexts._send(request)
        except WebSocketQueueFullError:
            raise
        except CartesiaError:
            pass

    async def flush(self) -> None:
        """Flushes the context. You should ignore this method unless you need flushes.

        Useful if you need to know when transcript chunks finished generating. You will
        receive a ``flush_done`` event once the transcript pushed to this context so far
        by :meth:`push` is done generating. See
        [the API docs](https://docs.cartesia.ai/use-the-api/tts-websocket/context-flushing-and-flush-i-ds)
        for details.

        Raises:
            :class:`WebSocketQueueFullError`: If sending the request fails due to too many requests being queued.

            :class:`CartesiaError`: If the request cannot be sent.

        .. note::
            The server may still send a :class:`WebSocketResponseError` message even if this method
            did not raise an exception.

        See Also:
            :meth:`push`: Stream transcript chunks.
            :meth:`end`: Signal that no more transcript chunks will be sent.
        """
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
        await self._contexts._send(request)

    async def cancel(self) -> None:
        """Cancel this context to stop generating speech.

        Raises:
            :class:`WebSocketQueueFullError`: If sending the request fails due to too many requests being queued.

        See Also:
            :meth:`end`: Signal that no more transcript chunks will be sent (graceful completion).
            :attr:`is_closed`: Will be ``True`` after :meth:`cancel` returns.
        """
        if self._closed:
            return
        try:
            await self._contexts._send(CancelContextRequest(cancel=True, context_id=self._context_id))
        except WebSocketQueueFullError:
            raise
        except CartesiaError:
            pass
        self._mark_closed()

    async def receive(self) -> AsyncIterator[WebsocketResponse]:
        """Iterate over messages for this context.

        Yields:
            AsyncIterator[WebsocketResponse]: Audio chunks (and timestamps if requested) are streamed in multiple messages as they are generated.
                :class:`WebSocketResponseError` with ``error_code="client_timeout"`` is sent if the context's timeout was reached and no messages were seen.

        See Also:
            :meth:`push`: Stream transcript chunks.
            :meth:`end`: Signal that no more transcript chunks will be sent.
        """

        if self._closed:
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
                    return
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
        self._queue.put_nowait(_DISCONNECT_SENTINEL)
        self._contexts._unregister_context(self._context_id, self)


class AsyncTTSContextsConnection:
    """Used to create instances of :class:`AsyncTTSContext` on a single WebSocket connection."""

    def __init__(self, manager: AsyncTTSContextsConnectionManager) -> None:
        self._manager = manager
        self._inner_manager: AsyncTTSResourceConnectionManager | None = None
        self._inner_connection: AsyncTTSResourceConnection | None = None
        self._contexts: Dict[str, AsyncTTSContext] = {}
        self._event_handler_registry = EventHandlerRegistry(use_lock=False)
        self._reader_task: asyncio.Task[None] | None = None
        self._connect_lock = asyncio.Lock()
        self._closed_event = asyncio.Event()
        self._permanently_closed = False

    async def close(self) -> None:
        """Close the WebSocket and cleanup all resources."""
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
                log.warning("Error closing inner connection", exc_info=True)
        if task is not None and not task.done():
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
                log.warning("Error exiting inner manager", exc_info=True)
        for ctx in list(self._contexts.values()):
            ctx._mark_closed()
        self._contexts.clear()
        self._closed_event.set()

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
    ) -> AsyncTTSContext:
        """Create a context. AsyncTTSContexts are short-lived and designed to generate audio for a single transcript.

        See [the API docs](https://docs.cartesia.ai/use-the-api/tts-websocket/contexts) for details.

        Args:
            model_id: Model used to generate audio for this context.
            voice: Voice for this context.
            output_format: Output audio format for this context.
            context_id: Unique identifier for this context. If not provided,
                a UUID will be auto-generated. Must be unique per WebSocket connection
                if provided.
            timeout: Client-side receive timeout in seconds. If set, :meth:`AsyncTTSContext.receive`
                will yield a synthetic ``client_timeout`` :class:`WebSocketResponseError` and return when no
                events arrive within the timeout.
            language: Language for this context.
            add_timestamps: Include word-level timestamps.
            add_phoneme_timestamps: Include phoneme-level timestamps.

        Returns:
            AsyncTTSContext for generating audio on the context.

        Raises:
            :class:`CartesiaError`: If an AsyncTTSContext with the same context_id already exists.
        """
        await self._ensure_connected()
        if context_id is None:
            context_id = str(uuid.uuid4())
        if context_id in self._contexts:
            raise CartesiaError(f"Duplicate context ID: {context_id}")
        ctx = AsyncTTSContext(
            contexts=self,
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

    def get_context(self, context_id: str) -> AsyncTTSContext | None:
        """
        Gets the context created by :meth:`context`.
        Contexts are automatically cleaned up when :meth:`AsyncTTSContext.receive` returns.

        Args:
            context_id: :attr:`AsyncTTSContext.context_id`

        Returns:
            :class:`AsyncTTSContext` or ``None`` if it was cleaned up.
        """
        return self._contexts.get(context_id)

    def list_contexts(self) -> List[AsyncTTSContext]:
        """
        Lists all contexts created by :meth:`context` that have not been cleaned up.
        Contexts are automatically cleaned up when :meth:`AsyncTTSContext.receive` returns.

        Returns:
            A list of :class:`AsyncTTSContext`.
        """
        return list(self._contexts.values())

    @overload
    def on_error(self, handler: _ErrorHandler) -> AsyncTTSContextsConnection: ...
    @overload
    def on_error(self) -> Callable[[_ErrorHandler], _ErrorHandler]: ...
    def on_error(
        self, handler: Optional[_ErrorHandler] = None
    ) -> Union[AsyncTTSContextsConnection, Callable[[_ErrorHandler], _ErrorHandler]]:
        """Register a handler for ``error`` events that don't have a ``context_id``.

        Errors with a ``context_id`` are delivered through :meth:`AsyncTTSContext.receive` instead.

        The handler may be ``async def`` — its returned coroutine is scheduled
        as a fire-and-forget task.

        No checks are made to see if the handler has already been added.
        Multiple calls with the same handler register it multiple times.

        Can be used as a method (returns ``self`` for chaining)::

            connection.on_error(my_handler)

        Or as a decorator::

            @connection.on_error()
            async def my_handler(event): ...
        """
        if handler is not None:
            self._event_handler_registry.add("error", handler)
            return self

        def decorator(fn: _ErrorHandler) -> _ErrorHandler:
            self._event_handler_registry.add("error", fn)
            return fn

        return decorator

    def off_error(self, handler: _ErrorHandler) -> AsyncTTSContextsConnection:
        """Remove a previously registered error handler."""
        self._event_handler_registry.remove("error", handler)
        return self

    @overload
    def once_error(self, handler: _ErrorHandler) -> AsyncTTSContextsConnection: ...
    @overload
    def once_error(self) -> Callable[[_ErrorHandler], _ErrorHandler]: ...
    def once_error(
        self, handler: Optional[_ErrorHandler] = None
    ) -> Union[AsyncTTSContextsConnection, Callable[[_ErrorHandler], _ErrorHandler]]:
        """Register a one-time error handler. Automatically removed after first invocation.

        Supports both method and decorator forms; see :meth:`on_error`.
        """
        if handler is not None:
            self._event_handler_registry.add("error", handler, once=True)
            return self

        def decorator(fn: _ErrorHandler) -> _ErrorHandler:
            self._event_handler_registry.add("error", fn, once=True)
            return fn

        return decorator

    async def dispatch_events(self) -> None:
        """Block until :meth:`close` is called.

        A background task continuously reads from the underlying WebSocket
        and dispatches non-context error events to handlers registered via
        :meth:`on`. This coroutine merely awaits the close event.
        """
        await self._closed_event.wait()

    # -- internals -----------------------------------------------------------

    async def _send(self, event: WebsocketClientEvent | WebsocketClientEventParam) -> None:
        connection = self._inner_connection
        if connection is None:
            raise CartesiaError("AsyncTTSContextsConnection is not connected.")
        await connection.send(event)

    def _unregister_context(self, context_id: str, ctx: AsyncTTSContext) -> None:
        if self._contexts.get(context_id) is ctx:
            self._contexts.pop(context_id, None)

    async def _ensure_connected(self) -> None:
        from ...resources.tts import AsyncTTSResourceConnectionManager

        async with self._connect_lock:
            if self._permanently_closed:
                raise CartesiaError("AsyncTTSContextsConnection is closed.")
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
                log.warning("Error closing inner connection during teardown", exc_info=True)
        if task is not None and not task.done():
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
                log.warning("Error exiting inner manager during teardown", exc_info=True)

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
            log.warning("WebSocket reader exited with exception", exc_info=True)
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
                log.exception("Error in 'error' handler")
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
                log.warning("Error exiting inner manager after disconnect", exc_info=True)


class AsyncTTSContextsConnectionManager:
    """
    Context manager over a :class:`AsyncTTSContextsConnection` that is returned by `tts.create_context_manager()`

    This context manager ensures that the connection will be closed when it exits.

    ---

    Note that if your application doesn't work well with the context manager approach then you
    can call :meth:`enter` directly to initiate a connection.

    **Warning**: You must remember to close the connection with :meth:`AsyncTTSContextsConnection.close` if you use :meth:`enter`.

    ```py
    # using .__aenter__()
    async with client.tts.create_context_manager(...) as connection:
        # ...

    # using .enter()
    connection = await client.tts.create_context_manager(...).enter()
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
        self._contexts: AsyncTTSContextsConnection | None = None

    @overload
    def on_error(self, handler: _ErrorHandler) -> AsyncTTSContextsConnectionManager: ...
    @overload
    def on_error(self) -> Callable[[_ErrorHandler], _ErrorHandler]: ...
    def on_error(
        self, handler: Optional[_ErrorHandler] = None
    ) -> Union[AsyncTTSContextsConnectionManager, Callable[[_ErrorHandler], _ErrorHandler]]:
        """Register an error handler before the connection is established.

        The handler is transferred to the connection on enter.
        See :meth:`AsyncTTSContextsConnection.on_error`.
        """
        if handler is not None:
            self._event_handler_registry.add("error", handler)
            return self

        def decorator(fn: _ErrorHandler) -> _ErrorHandler:
            self._event_handler_registry.add("error", fn)
            return fn

        return decorator

    def off_error(self, handler: _ErrorHandler) -> AsyncTTSContextsConnectionManager:
        """Remove a previously registered error handler."""
        self._event_handler_registry.remove("error", handler)
        return self

    @overload
    def once_error(self, handler: _ErrorHandler) -> AsyncTTSContextsConnectionManager: ...
    @overload
    def once_error(self) -> Callable[[_ErrorHandler], _ErrorHandler]: ...
    def once_error(
        self, handler: Optional[_ErrorHandler] = None
    ) -> Union[AsyncTTSContextsConnectionManager, Callable[[_ErrorHandler], _ErrorHandler]]:
        """Register a one-time error handler before the connection is established."""
        if handler is not None:
            self._event_handler_registry.add("error", handler, once=True)
            return self

        def decorator(fn: _ErrorHandler) -> _ErrorHandler:
            self._event_handler_registry.add("error", fn, once=True)
            return fn

        return decorator

    async def __aenter__(self) -> AsyncTTSContextsConnection:
        """
        If your application doesn't work well with the context manager approach then you
        can call this method directly to initiate a connection.

        **Warning**: You must remember to close the connection with :meth:`AsyncTTSContextsConnection.close`.

        ```py
        contexts = await client.tts.create_context_manager(...).enter()
        # ...
        await contexts.close()
        ```
        """
        contexts = AsyncTTSContextsConnection(self)
        self._event_handler_registry.merge_into(contexts._event_handler_registry)
        await contexts._ensure_connected()
        self._contexts = contexts
        return contexts

    enter = __aenter__

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if self._contexts is not None:
            await self._contexts.close()
