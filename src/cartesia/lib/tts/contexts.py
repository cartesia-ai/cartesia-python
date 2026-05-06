from __future__ import annotations

from types import TracebackType
from typing import (
    Any,
    Union,
    Mapping,
    Callable,
    Iterator,
    Optional,
    Sequence,
    overload,
)
from typing_extensions import Protocol, AsyncIterator, runtime_checkable

from ...types import (
    SupportedLanguage,
    WebsocketResponse,
    VoiceSpecifierParam,
    GenerationConfigParam,
    GenerationRequestParam as GenerationRequestParam,
)
from ..._exceptions import CartesiaError as CartesiaError, WebSocketQueueFullError as WebSocketQueueFullError
from ...types.websocket_response import Error as WebSocketResponseError, FlushDone as FlushDone
from ...types.generation_request_param import OutputFormat

TTSContextsWSErrorHandler = Callable[[WebSocketResponseError], Any]
"""Type of an error event handler.

For :class:`AsyncTTSContextsWSConnection`, the handler may also be ``async def``
— its returned coroutine is scheduled as a fire-and-forget task.
"""


# ---------------------------------------------------------------------------
# Sync
# ---------------------------------------------------------------------------


@runtime_checkable
class TTSWSContext(Protocol):
    """
    Contexts are short-lived and designed to generate audio for a single transcript.

    The transcript can be broken up into chunks and streamed over time using continuations,
    which is useful if you're still in the middle of generating your transcript.

    See [the API docs](https://docs.cartesia.ai/use-the-api/tts-websocket/contexts) for details.
    """

    @property
    def context_id(self) -> str:
        """A unique identifier for this context within the WebSocket connection."""
        ...

    @property
    def is_closed(self) -> bool:
        """
        If true, :meth:`push` and :meth:`flush` will raise :class:`CartesiaError`.

        Once a context is closed, a new one must be created to generate more audio.
        """
        ...

    def push(
        self,
        transcript: str,
        *,
        generation_config: Optional[GenerationConfigParam] = None,
        continue_: Optional[bool] = True,
        extra_args: Optional[Mapping[str, Any]] = None,
    ) -> None:
        """Call this multiple times to stream transcript chunks, then call :meth:`end` to finish.

        Args:
            transcript (str): Transcript chunk to add to the context.
            generation_config (GenerationConfigParam, optional): Speed, volume, and emotion controls.
            continue_ (bool): If set to false, signal that the transcript is complete.
                You do not need to call :meth:`end` if you send a request with ``continue_=False``.
                Defaults to True.
            extra_args (Mapping[str, Any], optional): Additional properties to add to :class:`GenerationRequestParam`.
                This can be useful if you'd like to override properties or leverage new API capabilities without updating this SDK.

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
        ...

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
        ...

    def flush(self) -> None:
        """Flushes the context. You should ignore this method unless you need flushes.

        Useful if you need to know when transcript chunks finished generating. You will
        receive a :class:`FlushDone` event once the transcript pushed to this context so far
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
        ...

    def cancel(self) -> None:
        """Cancel this context to stop generating speech.

        Raises:
            :class:`WebSocketQueueFullError`: If sending the request fails due to too many requests being queued.

        See Also:
            :meth:`end`: Signal that no more transcript chunks will be sent (graceful completion).
            :attr:`is_closed`: Will be ``True`` after :meth:`cancel` returns.
        """
        ...

    def receive(self) -> Iterator[WebsocketResponse]:
        """Iterate over messages for this context.

        Yields:
            WebsocketResponse: Audio chunks (and timestamps if requested) are streamed in multiple messages as they are generated.
                :class:`WebSocketResponseError` with ``error_code="client_timeout"`` is sent if the context's timeout was reached and no messages were seen.

        See Also:
            :meth:`push`: Stream transcript chunks.
            :meth:`end`: Signal that no more transcript chunks will be sent.
        """
        ...


@runtime_checkable
class TTSContextsWSConnection(Protocol):
    """Used to create instances of :class:`TTSWSContext` on a single WebSocket connection."""

    def close(self) -> None:
        """Close the WebSocket and cleanup all resources."""
        ...

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
    ) -> TTSWSContext:
        """Create a context. Contexts are short-lived and designed to generate audio for a single transcript.

        See [the API docs](https://docs.cartesia.ai/use-the-api/tts-websocket/contexts) for details.

        Args:
            model_id: Model used to generate audio for this context.
            voice: Voice for this context.
            output_format: Output audio format for this context.
            context_id: Unique identifier for this context. If not provided,
                a UUID will be auto-generated. Must be unique per WebSocket connection
                if provided.
            timeout: Client-side receive timeout in seconds. If set, :meth:`TTSWSContext.receive`
                will yield a synthetic ``client_timeout`` :class:`WebSocketResponseError` and return when no
                events arrive within the timeout.
            language: Language for this context.
            add_timestamps: Include word-level timestamps.
            add_phoneme_timestamps: Include phoneme-level timestamps.

        Returns:
            :class:`TTSWSContext` for generating audio on the context.

        Raises:
            :class:`CartesiaError`: If an :class:`TTSWSContext` with the same ``context_id`` already exists.
        """
        ...

    def get_context(self, context_id: str) -> TTSWSContext | None:
        """
        Gets the context created by :meth:`context`.
        Contexts are automatically cleaned up when :meth:`TTSWSContext.receive` returns.

        Args:
            context_id: :attr:`TTSWSContext.context_id`

        Returns:
            :class:`TTSWSContext` or ``None`` if it was cleaned up.
        """
        ...

    def list_contexts(self) -> Sequence[TTSWSContext]:
        """
        Lists all contexts created by :meth:`context` that have not been cleaned up.
        Contexts are automatically cleaned up when :meth:`TTSWSContext.receive` returns.

        Returns:
            A sequence of :class:`TTSWSContext`.
        """
        ...

    @overload
    def on_error(self, handler: TTSContextsWSErrorHandler) -> TTSContextsWSConnection: ...
    @overload
    def on_error(self) -> Callable[[TTSContextsWSErrorHandler], TTSContextsWSErrorHandler]: ...
    def on_error(
        self, handler: Optional[TTSContextsWSErrorHandler] = None
    ) -> Union[TTSContextsWSConnection, Callable[[TTSContextsWSErrorHandler], TTSContextsWSErrorHandler]]:
        """Register a handler for :class:`WebSocketResponseError` events that don't have a ``context_id``.

        Errors with a ``context_id`` are delivered through :meth:`TTSWSContext.receive` instead.

        No checks are made to see if the handler has already been added.
        Multiple calls with the same handler register it multiple times.

        Can be used as a method (returns ``self`` for chaining)::

            connection.on_error(my_handler)

        Or as a decorator::

            @connection.on_error()
            def my_handler(event): ...
        """
        ...

    def off_error(self, handler: TTSContextsWSErrorHandler) -> TTSContextsWSConnection:
        """Remove a previously registered error handler."""
        ...

    @overload
    def once_error(self, handler: TTSContextsWSErrorHandler) -> TTSContextsWSConnection: ...
    @overload
    def once_error(self) -> Callable[[TTSContextsWSErrorHandler], TTSContextsWSErrorHandler]: ...
    def once_error(
        self, handler: Optional[TTSContextsWSErrorHandler] = None
    ) -> Union[TTSContextsWSConnection, Callable[[TTSContextsWSErrorHandler], TTSContextsWSErrorHandler]]:
        """Register a one-time error handler. Automatically removed after first invocation.

        Supports both method and decorator forms; see :meth:`on_error`.
        """
        ...

    def dispatch_events(self) -> None:
        """Block the calling thread until :meth:`close` is called.

        A background thread continuously reads from the underlying WebSocket
        and dispatches non-context error events to handlers registered via
        :meth:`on_error`. This method merely parks the calling thread.
        """
        ...


@runtime_checkable
class TTSContextsWSConnectionManager(Protocol):
    """
    Context manager over an :class:`TTSContextsWSConnection` that is returned by `cartesia.tts.contexts_ws()`

    This context manager ensures that the connection will be closed when it exits.

    ---

    Note that if your application doesn't work well with the context manager approach then you
    can call :meth:`enter` directly to initiate a connection.

    **Warning**: You must remember to close the connection with :meth:`TTSContextsWSConnection.close` if you use :meth:`enter`.

    ```py
    # using .__enter__()
    with client.tts.contexts_ws(...) as connection:
        # ...

    # using .enter()
    connection = client.tts.contexts_ws(...).enter()
    # ...
    connection.close()
    ```
    """

    @overload
    def on_error(self, handler: TTSContextsWSErrorHandler) -> TTSContextsWSConnectionManager: ...
    @overload
    def on_error(self) -> Callable[[TTSContextsWSErrorHandler], TTSContextsWSErrorHandler]: ...
    def on_error(
        self, handler: Optional[TTSContextsWSErrorHandler] = None
    ) -> Union[TTSContextsWSConnectionManager, Callable[[TTSContextsWSErrorHandler], TTSContextsWSErrorHandler]]:
        """Register an error handler before the connection is established.

        The handler is transferred to the connection on enter.
        See :meth:`TTSContextsWSConnection.on_error`.
        """
        ...

    def off_error(self, handler: TTSContextsWSErrorHandler) -> TTSContextsWSConnectionManager:
        """Remove a previously registered error handler."""
        ...

    @overload
    def once_error(self, handler: TTSContextsWSErrorHandler) -> TTSContextsWSConnectionManager: ...
    @overload
    def once_error(self) -> Callable[[TTSContextsWSErrorHandler], TTSContextsWSErrorHandler]: ...
    def once_error(
        self, handler: Optional[TTSContextsWSErrorHandler] = None
    ) -> Union[TTSContextsWSConnectionManager, Callable[[TTSContextsWSErrorHandler], TTSContextsWSErrorHandler]]:
        """Register a one-time error handler before the connection is established."""
        ...

    def enter(self) -> TTSContextsWSConnection:
        """
        If your application doesn't work well with the context manager approach then you
        can call this method directly to initiate a connection.

        **Warning**: You must remember to close the connection with :meth:`TTSContextsWSConnection.close`.

        ```py
        connection = client.tts.contexts_ws(...).enter()
        # ...
        connection.close()
        ```
        """
        ...

    def __enter__(self) -> TTSContextsWSConnection: ...

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None: ...


# ---------------------------------------------------------------------------
# Async
# ---------------------------------------------------------------------------


@runtime_checkable
class AsyncTTSWSContext(Protocol):
    """
    Contexts are short-lived and designed to generate audio for a single transcript.

    The transcript can be broken up into chunks and streamed over time using continuations,
    which is useful if you're still in the middle of generating your transcript.

    See [the API docs](https://docs.cartesia.ai/use-the-api/tts-websocket/contexts) for details.
    """

    @property
    def context_id(self) -> str:
        """A unique identifier for this context within the WebSocket connection."""
        ...

    @property
    def is_closed(self) -> bool:
        """
        If true, :meth:`push` and :meth:`flush` will raise :class:`CartesiaError`.

        Once a context is closed, a new one must be created to generate more audio.
        """
        ...

    async def push(
        self,
        transcript: str,
        *,
        generation_config: Optional[GenerationConfigParam] = None,
        continue_: Optional[bool] = True,
        extra_args: Optional[Mapping[str, Any]] = None,
    ) -> None:
        """Call this multiple times to stream transcript chunks, then call :meth:`end` to finish.

        Args:
            transcript (str): Transcript chunk to add to the context.
            generation_config (GenerationConfigParam, optional): Speed, volume, and emotion controls.
            continue_ (bool): If set to false, signal that the transcript is complete.
                You do not need to call :meth:`end` if you send a request with ``continue_=False``.
                Defaults to True.
            extra_args (Mapping[str, Any], optional): Additional properties to add to :class:`GenerationRequestParam`.
                This can be useful if you'd like to override properties or leverage new API capabilities without updating this SDK.

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
        ...

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
        ...

    async def flush(self) -> None:
        """Flushes the context. You should ignore this method unless you need flushes.

        Useful if you need to know when transcript chunks finished generating. You will
        receive a :class:`FlushDone` event once the transcript pushed to this context so far
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
        ...

    async def cancel(self) -> None:
        """Cancel this context to stop generating speech.

        Raises:
            :class:`WebSocketQueueFullError`: If sending the request fails due to too many requests being queued.

        See Also:
            :meth:`end`: Signal that no more transcript chunks will be sent (graceful completion).
            :attr:`is_closed`: Will be ``True`` after :meth:`cancel` returns.
        """
        ...

    def receive(self) -> AsyncIterator[WebsocketResponse]:
        """Iterate over messages for this context.

        Yields:
            WebsocketResponse: Audio chunks (and timestamps if requested) are streamed in multiple messages as they are generated.
                :class:`WebSocketResponseError` with ``error_code="client_timeout"`` is sent if the context's timeout was reached and no messages were seen.

        See Also:
            :meth:`push`: Stream transcript chunks.
            :meth:`end`: Signal that no more transcript chunks will be sent.
        """
        ...


@runtime_checkable
class AsyncTTSContextsWSConnection(Protocol):
    """Used to create instances of :class:`AsyncTTSWSContext` on a single WebSocket connection."""

    async def close(self) -> None:
        """Close the WebSocket and cleanup all resources."""
        ...

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
    ) -> AsyncTTSWSContext:
        """Create a context. Contexts are short-lived and designed to generate audio for a single transcript.

        See [the API docs](https://docs.cartesia.ai/use-the-api/tts-websocket/contexts) for details.

        Args:
            model_id: Model used to generate audio for this context.
            voice: Voice for this context.
            output_format: Output audio format for this context.
            context_id: Unique identifier for this context. If not provided,
                a UUID will be auto-generated. Must be unique per WebSocket connection
                if provided.
            timeout: Client-side receive timeout in seconds. If set, :meth:`AsyncTTSWSContext.receive`
                will yield a synthetic ``client_timeout`` :class:`WebSocketResponseError` and return when no
                events arrive within the timeout.
            language: Language for this context.
            add_timestamps: Include word-level timestamps.
            add_phoneme_timestamps: Include phoneme-level timestamps.

        Returns:
            AsyncTTSWSContext for generating audio on the context.

        Raises:
            :class:`CartesiaError`: If an AsyncTTSWSContext with the same context_id already exists.
        """
        ...

    def get_context(self, context_id: str) -> AsyncTTSWSContext | None:
        """
        Gets the context created by :meth:`context`.
        Contexts are automatically cleaned up when :meth:`AsyncTTSWSContext.receive` returns.

        Args:
            context_id: :attr:`AsyncTTSWSContext.context_id`

        Returns:
            :class:`AsyncTTSWSContext` or ``None`` if it was cleaned up.
        """
        ...

    def list_contexts(self) -> Sequence[AsyncTTSWSContext]:
        """
        Lists all contexts created by :meth:`context` that have not been cleaned up.
        Contexts are automatically cleaned up when :meth:`AsyncTTSWSContext.receive` returns.

        Returns:
            A sequence of :class:`AsyncTTSWSContext`.
        """
        ...

    @overload
    def on_error(self, handler: TTSContextsWSErrorHandler) -> AsyncTTSContextsWSConnection: ...
    @overload
    def on_error(self) -> Callable[[TTSContextsWSErrorHandler], TTSContextsWSErrorHandler]: ...
    def on_error(
        self, handler: Optional[TTSContextsWSErrorHandler] = None
    ) -> Union[AsyncTTSContextsWSConnection, Callable[[TTSContextsWSErrorHandler], TTSContextsWSErrorHandler]]:
        """Register a handler for :class:`WebSocketResponseError` events that don't have a ``context_id``.

        Errors with a ``context_id`` are delivered through :meth:`AsyncTTSWSContext.receive` instead.

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
        ...

    def off_error(self, handler: TTSContextsWSErrorHandler) -> AsyncTTSContextsWSConnection:
        """Remove a previously registered error handler."""
        ...

    @overload
    def once_error(self, handler: TTSContextsWSErrorHandler) -> AsyncTTSContextsWSConnection: ...
    @overload
    def once_error(self) -> Callable[[TTSContextsWSErrorHandler], TTSContextsWSErrorHandler]: ...
    def once_error(
        self, handler: Optional[TTSContextsWSErrorHandler] = None
    ) -> Union[AsyncTTSContextsWSConnection, Callable[[TTSContextsWSErrorHandler], TTSContextsWSErrorHandler]]:
        """Register a one-time error handler. Automatically removed after first invocation.

        Supports both method and decorator forms; see :meth:`on_error`.
        """
        ...

    async def dispatch_events(self) -> None:
        """Block until :meth:`close` is called.

        A background task continuously reads from the underlying WebSocket
        and dispatches non-context error events to handlers registered via
        :meth:`on_error`. This coroutine merely awaits the close event.
        """
        ...


@runtime_checkable
class AsyncTTSContextsWSConnectionManager(Protocol):
    """
    Context manager over an :class:`AsyncTTSContextsWSConnection` that is returned by `cartesia.tts.contexts_ws()`

    This context manager ensures that the connection will be closed when it exits.

    ---

    Note that if your application doesn't work well with the context manager approach then you
    can call :meth:`enter` directly to initiate a connection.

    **Warning**: You must remember to close the connection with :meth:`AsyncTTSContextsWSConnection.close` if you use :meth:`enter`.

    ```py
    # using .__aenter__()
    async with client.tts.contexts_ws(...) as connection:
        # ...

    # using .enter()
    connection = await client.tts.contexts_ws(...).enter()
    # ...
    await connection.close()
    ```
    """

    @overload
    def on_error(self, handler: TTSContextsWSErrorHandler) -> AsyncTTSContextsWSConnectionManager: ...
    @overload
    def on_error(self) -> Callable[[TTSContextsWSErrorHandler], TTSContextsWSErrorHandler]: ...
    def on_error(
        self, handler: Optional[TTSContextsWSErrorHandler] = None
    ) -> Union[AsyncTTSContextsWSConnectionManager, Callable[[TTSContextsWSErrorHandler], TTSContextsWSErrorHandler]]:
        """Register an error handler before the connection is established.

        The handler is transferred to the connection on enter.
        See :meth:`AsyncTTSContextsWSConnection.on_error`.
        """
        ...

    def off_error(self, handler: TTSContextsWSErrorHandler) -> AsyncTTSContextsWSConnectionManager:
        """Remove a previously registered error handler."""
        ...

    @overload
    def once_error(self, handler: TTSContextsWSErrorHandler) -> AsyncTTSContextsWSConnectionManager: ...
    @overload
    def once_error(self) -> Callable[[TTSContextsWSErrorHandler], TTSContextsWSErrorHandler]: ...
    def once_error(
        self, handler: Optional[TTSContextsWSErrorHandler] = None
    ) -> Union[AsyncTTSContextsWSConnectionManager, Callable[[TTSContextsWSErrorHandler], TTSContextsWSErrorHandler]]:
        """Register a one-time error handler before the connection is established."""
        ...

    async def enter(self) -> AsyncTTSContextsWSConnection:
        """
        If your application doesn't work well with the context manager approach then you
        can call this method directly to initiate a connection.

        **Warning**: You must remember to close the connection with :meth:`AsyncTTSContextsWSConnection.close`.

        ```py
        connection = await client.tts.contexts_ws(...).enter()
        # ...
        await connection.close()
        ```
        """
        ...

    async def __aenter__(self) -> AsyncTTSContextsWSConnection: ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None: ...
