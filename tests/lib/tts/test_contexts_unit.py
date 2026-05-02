"""Unit tests for the TTS contexts wrapper.

These tests use mocks; no live API calls are made. They verify the per-context
helper behavior, the connection-level routing, and lifecycle event emission.
"""

from __future__ import annotations

import threading
from typing import Any, Dict, List, Tuple, Optional, cast
from unittest.mock import MagicMock

import pytest

from cartesia.types import ReconnectingEvent
from cartesia._types import omit
from cartesia._exceptions import CartesiaError
from cartesia.lib._tts.contexts import (
    _Sentinel,
    _is_terminal,
    _TTSWSContext,
    _AsyncTTSWSContext,
    _TTSContextsWSConnection,
    _build_generation_request,
    _AsyncTTSContextsWSConnection,
    _TTSContextsWSConnectionManager,
)
from cartesia.types.websocket_response import Done, Chunk, Error, FlushDone

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


DEFAULT_OUTPUT_FORMAT: Any = {"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100}
DEFAULT_VOICE: Any = {"mode": "id", "id": "test-voice"}


def _chunk(context_id: str, seq: int = 0) -> Chunk:
    return Chunk(
        type="chunk",
        context_id=context_id,
        data=f"audio_{seq}",
        done=False,
        status_code=200,
        step_time=0.0,
    )


def _done(context_id: str) -> Done:
    return Done(type="done", context_id=context_id, done=True, status_code=200)


def _error(context_id: Optional[str] = None, *, done: bool = True) -> Error:
    return Error(
        type="error",
        done=done,
        context_id=context_id,
        error_code="test_error",
        message="test message",
    )


def _flush_done(context_id: str, flush_id: int = 1) -> FlushDone:
    return FlushDone(
        type="flush_done",
        context_id=context_id,
        done=False,
        flush_done=True,
        flush_id=flush_id,
        status_code=200,
    )


class FakeContexts:
    """Stub for TTSContextsWSConnection used in TTSWSContext unit tests."""

    def __init__(self) -> None:
        self.sent: List[Any] = []
        self.unregistered: List[Tuple[str, Any]] = []
        self.send_should_raise: Optional[BaseException] = None

    def _send(self, event: Any) -> None:
        if self.send_should_raise is not None:
            raise self.send_should_raise
        self.sent.append(event)

    def _unregister_context(self, context_id: str, ctx: Any) -> None:
        self.unregistered.append((context_id, ctx))


class FakeAsyncContexts:
    """Stub for AsyncTTSContextsWSConnection used in AsyncTTSWSContext unit tests."""

    def __init__(self) -> None:
        self.sent: List[Any] = []
        self.unregistered: List[Tuple[str, Any]] = []
        self.send_should_raise: Optional[BaseException] = None

    async def _send(self, event: Any) -> None:
        if self.send_should_raise is not None:
            raise self.send_should_raise
        self.sent.append(event)

    def _unregister_context(self, context_id: str, ctx: Any) -> None:
        self.unregistered.append((context_id, ctx))


class FakeManager:
    """Minimal stub for TTSContextsWSConnectionManager / AsyncTTSContextsWSConnectionManager."""

    def __init__(self, on_reconnecting: Any = None) -> None:
        self._client: Any = MagicMock()
        self._extra_query: Dict[str, Any] = {}
        self._extra_headers: Dict[str, Any] = {}
        self._websocket_connection_options: Dict[str, Any] = {}
        self._on_reconnecting: Any = on_reconnecting
        self._max_retries: int = 5
        self._initial_delay: float = 0.5
        self._max_delay: float = 8.0
        self._max_queue_size: int = 1_048_576


def _make_sync_ctx(
    *,
    contexts: Optional[FakeContexts] = None,
    context_id: str = "ctx-id",
    timeout: Optional[float] = None,
    model_id: str = "sonic-3",
    voice: Any = None,
    output_format: Any = None,
    language: Optional[str] = None,
    add_timestamps: Optional[bool] = None,
    add_phoneme_timestamps: Optional[bool] = None,
) -> Tuple[_TTSWSContext, FakeContexts]:
    fc = contexts or FakeContexts()
    ctx = _TTSWSContext(
        ws=cast(Any, fc),
        context_id=context_id,
        timeout=timeout,
        model_id=model_id,
        voice=voice or DEFAULT_VOICE,
        output_format=output_format or DEFAULT_OUTPUT_FORMAT,
        language=cast(Any, language),
        add_timestamps=add_timestamps,
        add_phoneme_timestamps=add_phoneme_timestamps,
    )
    return ctx, fc


def _make_async_ctx(
    *,
    contexts: Optional[FakeAsyncContexts] = None,
    context_id: str = "ctx-id",
    timeout: Optional[float] = None,
    model_id: str = "sonic-3",
    voice: Any = None,
    output_format: Any = None,
    language: Optional[str] = None,
    add_timestamps: Optional[bool] = None,
    add_phoneme_timestamps: Optional[bool] = None,
) -> Tuple[_AsyncTTSWSContext, FakeAsyncContexts]:
    fc = contexts or FakeAsyncContexts()
    ctx = _AsyncTTSWSContext(
        ws=cast(Any, fc),
        context_id=context_id,
        timeout=timeout,
        model_id=model_id,
        voice=voice or DEFAULT_VOICE,
        output_format=output_format or DEFAULT_OUTPUT_FORMAT,
        language=cast(Any, language),
        add_timestamps=add_timestamps,
        add_phoneme_timestamps=add_phoneme_timestamps,
    )
    return ctx, fc


def _make_sync_connection(on_reconnecting: Any = None) -> _TTSContextsWSConnection:
    """Build a _TTSContextsWSConnection with a mocked inner connection."""
    conn = _TTSContextsWSConnection(cast(Any, FakeManager(on_reconnecting=on_reconnecting)))
    inner: Any = MagicMock()
    inner.send = MagicMock()
    conn._inner_connection = inner
    # Skip real connection setup.
    conn._ensure_connected = lambda: None  # type: ignore[method-assign]
    return conn


def _make_async_connection(on_reconnecting: Any = None) -> _AsyncTTSContextsWSConnection:
    conn = _AsyncTTSContextsWSConnection(cast(Any, FakeManager(on_reconnecting=on_reconnecting)))
    inner: Any = MagicMock()

    async def _async_send(_event: Any) -> None:
        return None

    inner.send = _async_send
    conn._inner_connection = inner

    async def _noop() -> None:
        return None

    conn._ensure_connected = _noop  # type: ignore[method-assign]
    return conn


# ---------------------------------------------------------------------------
# _is_terminal
# ---------------------------------------------------------------------------


class TestIsTerminal:
    def test_done_is_terminal(self) -> None:
        assert _is_terminal(_done("c")) is True

    def test_error_with_done_true_is_terminal(self) -> None:
        assert _is_terminal(_error("c", done=True)) is True

    def test_error_with_done_false_is_not_terminal(self) -> None:
        assert _is_terminal(_error("c", done=False)) is False

    def test_chunk_is_not_terminal(self) -> None:
        assert _is_terminal(_chunk("c")) is False

    def test_flush_done_is_not_terminal(self) -> None:
        assert _is_terminal(_flush_done("c")) is False


# ---------------------------------------------------------------------------
# _build_generation_request
# ---------------------------------------------------------------------------


class TestBuildGenerationRequest:
    def test_minimal_required_fields(self) -> None:
        req = cast(
            Dict[str, Any],
            _build_generation_request(
                context_id="c",
                model_id="m",
                transcript="hi",
                voice=DEFAULT_VOICE,
                output_format=DEFAULT_OUTPUT_FORMAT,
                continue_=True,
                language=None,
                add_timestamps=omit,
                add_phoneme_timestamps=omit,
                flush=omit,
                generation_config=None,
                extra={},
            ),
        )
        assert req["model_id"] == "m"
        assert req["transcript"] == "hi"
        assert req["context_id"] == "c"
        assert req["continue"] is True
        assert "language" not in req
        assert "add_timestamps" not in req
        assert "add_phoneme_timestamps" not in req
        assert "flush" not in req
        assert "generation_config" not in req

    def test_optional_fields_included_when_set(self) -> None:
        req = cast(
            Dict[str, Any],
            _build_generation_request(
                context_id="c",
                model_id="m",
                transcript="hi",
                voice=DEFAULT_VOICE,
                output_format=DEFAULT_OUTPUT_FORMAT,
                continue_=True,
                language=cast(Any, "en"),
                add_timestamps=True,
                add_phoneme_timestamps=False,
                flush=True,
                generation_config=cast(Any, {"speed": 1.5}),
                extra={},
            ),
        )
        assert req["language"] == "en"
        assert req["add_timestamps"] is True
        assert req["add_phoneme_timestamps"] is False
        assert req["flush"] is True
        assert req["generation_config"] == {"speed": 1.5}

    def test_extra_kwargs_merged(self) -> None:
        req = _build_generation_request(
            context_id="c",
            model_id="m",
            transcript="hi",
            voice=DEFAULT_VOICE,
            output_format=DEFAULT_OUTPUT_FORMAT,
            continue_=True,
            language=None,
            add_timestamps=omit,
            add_phoneme_timestamps=omit,
            flush=omit,
            generation_config=None,
            extra={"duration": 5.0},
        )
        assert cast(Dict[str, Any], req)["duration"] == 5.0

    def test_continue_false(self) -> None:
        req = cast(
            Dict[str, Any],
            _build_generation_request(
                context_id="c",
                model_id="m",
                transcript="hi",
                voice=DEFAULT_VOICE,
                output_format=DEFAULT_OUTPUT_FORMAT,
                continue_=False,
                language=None,
                add_timestamps=omit,
                add_phoneme_timestamps=omit,
                flush=omit,
                generation_config=None,
                extra={},
            ),
        )
        assert req["continue"] is False


# ---------------------------------------------------------------------------
# TTSWSContext (sync)
# ---------------------------------------------------------------------------


class TestTTSWSContextSync:
    def test_context_id_property(self) -> None:
        ctx, _ = _make_sync_ctx(context_id="abc-123")
        assert ctx.context_id == "abc-123"

    def test_is_closed_initially_false(self) -> None:
        ctx, _ = _make_sync_ctx()
        assert ctx.is_closed is False

    def test_mark_closed_sets_is_closed(self) -> None:
        ctx, _ = _make_sync_ctx()
        ctx._mark_closed()
        assert ctx.is_closed is True

    def test_mark_closed_unregisters_from_contexts(self) -> None:
        ctx, fc = _make_sync_ctx()
        ctx._mark_closed()
        assert ("ctx-id", ctx) in fc.unregistered

    def test_mark_closed_idempotent(self) -> None:
        ctx, fc = _make_sync_ctx()
        ctx._mark_closed()
        ctx._mark_closed()
        assert len(fc.unregistered) == 1

    # ---- push ----

    def test_push_sends_request_with_continue_true(self) -> None:
        ctx, fc = _make_sync_ctx()
        ctx.push("hello")
        assert len(fc.sent) == 1
        sent = cast(Dict[str, Any], fc.sent[0])
        assert sent["transcript"] == "hello"
        assert sent["continue"] is True
        assert sent["context_id"] == "ctx-id"
        assert sent["model_id"] == "sonic-3"

    def test_push_with_continue_false(self) -> None:
        ctx, fc = _make_sync_ctx()
        ctx.push("hello", continue_=False)
        assert cast(Dict[str, Any], fc.sent[0])["continue"] is False

    def test_push_with_continue_none_defaults_to_true(self) -> None:
        ctx, fc = _make_sync_ctx()
        ctx.push("hello", continue_=None)
        assert cast(Dict[str, Any], fc.sent[0])["continue"] is True

    def test_push_with_generation_config(self) -> None:
        ctx, fc = _make_sync_ctx()
        ctx.push("hi", generation_config=cast(Any, {"speed": 1.5}))
        assert cast(Dict[str, Any], fc.sent[0])["generation_config"] == {"speed": 1.5}

    def test_push_with_extra_kwargs(self) -> None:
        ctx, fc = _make_sync_ctx()
        ctx.push("hi", extra_args={"duration": 5.0})
        assert cast(Dict[str, Any], fc.sent[0])["duration"] == 5.0

    def test_push_inherits_constructor_defaults(self) -> None:
        ctx, fc = _make_sync_ctx(language="en", add_timestamps=True)
        ctx.push("hi")
        sent = cast(Dict[str, Any], fc.sent[0])
        assert sent["language"] == "en"
        assert sent["add_timestamps"] is True

    def test_push_after_close_raises(self) -> None:
        ctx, _ = _make_sync_ctx()
        ctx._mark_closed()
        with pytest.raises(CartesiaError, match="closed context"):
            ctx.push("hi")

    # ---- end ----

    def test_end_sends_continue_false_with_empty_transcript(self) -> None:
        ctx, fc = _make_sync_ctx()
        ctx.end()
        assert len(fc.sent) == 1
        sent = cast(Dict[str, Any], fc.sent[0])
        assert sent["continue"] is False
        assert sent["transcript"] == ""

    def test_end_does_not_mark_closed(self) -> None:
        # TS-compat: end() does not flip is_closed (the server's terminal event does)
        ctx, _ = _make_sync_ctx()
        ctx.end()
        assert ctx.is_closed is False

    def test_end_after_close_no_op(self) -> None:
        ctx, fc = _make_sync_ctx()
        ctx._mark_closed()
        ctx.end()
        assert fc.sent == []

    def test_push_after_end_still_works(self) -> None:
        # TS-compat: end() doesn't close the context
        ctx, fc = _make_sync_ctx()
        ctx.end()
        ctx.push("more")
        assert len(fc.sent) == 2

    # ---- flush ----

    def test_flush_sends_correct_request(self) -> None:
        ctx, fc = _make_sync_ctx()
        ctx.flush()
        sent = cast(Dict[str, Any], fc.sent[0])
        assert sent["transcript"] == ""
        assert sent["continue"] is True
        assert sent["flush"] is True

    def test_flush_after_close_raises(self) -> None:
        ctx, _ = _make_sync_ctx()
        ctx._mark_closed()
        with pytest.raises(CartesiaError, match="closed context"):
            ctx.flush()

    def test_flush_after_end_works(self) -> None:
        # TS-compat: flush() works after end() since end() doesn't close
        ctx, fc = _make_sync_ctx()
        ctx.end()
        ctx.flush()
        assert len(fc.sent) == 2

    # ---- cancel ----

    def test_cancel_sends_cancel_request(self) -> None:
        ctx, fc = _make_sync_ctx()
        ctx.cancel()
        assert len(fc.sent) == 1
        sent: Any = fc.sent[0]
        assert sent.context_id == "ctx-id"
        assert sent.cancel is True

    def test_cancel_marks_closed(self) -> None:
        ctx, _ = _make_sync_ctx()
        ctx.cancel()
        assert ctx.is_closed is True

    def test_cancel_idempotent(self) -> None:
        ctx, fc = _make_sync_ctx()
        ctx.cancel()
        ctx.cancel()
        assert len(fc.sent) == 1

    def test_cancel_swallows_cartesia_error_and_marks_closed(self) -> None:
        # cancel() is best-effort: a CartesiaError from send is swallowed and
        # the local context is still marked closed.
        ctx, fc = _make_sync_ctx()
        fc.send_should_raise = CartesiaError("network down")
        ctx.cancel()  # should not raise
        assert ctx.is_closed is True

    # ---- receive ----

    def test_receive_yields_queued_chunks(self) -> None:
        ctx, _ = _make_sync_ctx()
        ctx._queue.put_nowait(_chunk("ctx-id", 0))
        ctx._queue.put_nowait(_chunk("ctx-id", 1))
        ctx._queue.put_nowait(_done("ctx-id"))
        events = list(ctx.receive())
        assert len(events) == 3
        assert events[0].type == "chunk"
        assert events[2].type == "done"

    def test_receive_terminates_on_done(self) -> None:
        ctx, _ = _make_sync_ctx()
        ctx._queue.put_nowait(_done("ctx-id"))
        ctx._queue.put_nowait(_chunk("ctx-id"))  # should NOT be yielded
        events = list(ctx.receive())
        assert len(events) == 1
        assert events[0].type == "done"

    def test_receive_terminates_on_terminal_error(self) -> None:
        ctx, _ = _make_sync_ctx()
        ctx._queue.put_nowait(_error("ctx-id", done=True))
        events = list(ctx.receive())
        assert len(events) == 1
        assert events[0].type == "error"

    def test_receive_continues_on_non_terminal_error(self) -> None:
        ctx, _ = _make_sync_ctx()
        ctx._queue.put_nowait(_error("ctx-id", done=False))
        ctx._queue.put_nowait(_chunk("ctx-id"))
        ctx._queue.put_nowait(_done("ctx-id"))
        events = list(ctx.receive())
        assert len(events) == 3

    def test_receive_terminates_on_sentinel(self) -> None:
        ctx, _ = _make_sync_ctx()
        ctx._queue.put_nowait(_chunk("ctx-id"))
        ctx._queue.put_nowait(_Sentinel("disconnect"))
        ctx._queue.put_nowait(_chunk("ctx-id"))  # should NOT be yielded
        events = list(ctx.receive())
        assert len(events) == 1

    def test_receive_marks_closed_on_finish(self) -> None:
        ctx, _ = _make_sync_ctx()
        ctx._queue.put_nowait(_done("ctx-id"))
        list(ctx.receive())
        assert ctx.is_closed is True

    def test_receive_marks_closed_on_break(self) -> None:
        from typing import Generator

        ctx, _ = _make_sync_ctx()
        ctx._queue.put_nowait(_chunk("ctx-id"))
        gen = cast(Generator[Any, None, None], ctx.receive())
        next(gen)
        gen.close()
        assert ctx.is_closed is True

    def test_receive_after_close_returns_immediately(self) -> None:
        ctx, _ = _make_sync_ctx()
        ctx._mark_closed()
        events = list(ctx.receive())
        assert events == []

    def test_receive_called_twice_does_not_block(self) -> None:
        ctx, _ = _make_sync_ctx()
        ctx._queue.put_nowait(_done("ctx-id"))
        first = list(ctx.receive())
        assert len(first) == 1
        # Second call must return immediately rather than block on empty queue.
        second = list(ctx.receive())
        assert second == []

    def test_receive_timeout_yields_synthetic_error(self) -> None:
        ctx, _ = _make_sync_ctx(timeout=0.05)
        events = list(ctx.receive())
        assert len(events) == 1
        ev = events[0]
        assert ev.type == "error"
        assert isinstance(ev, Error)
        assert ev.error_code == "client_timeout"
        assert ev.context_id == "ctx-id"
        assert ev.done is True

    def test_receive_timeout_marks_closed(self) -> None:
        ctx, _ = _make_sync_ctx(timeout=0.05)
        list(ctx.receive())
        assert ctx.is_closed is True


# ---------------------------------------------------------------------------
# AsyncTTSWSContext
# ---------------------------------------------------------------------------


class TestAsyncTTSWSContext:
    @pytest.mark.asyncio
    async def test_push_sends_request(self) -> None:
        ctx, fc = _make_async_ctx()
        await ctx.push("hello")
        assert cast(Dict[str, Any], fc.sent[0])["transcript"] == "hello"

    @pytest.mark.asyncio
    async def test_push_after_close_raises(self) -> None:
        ctx, _ = _make_async_ctx()
        ctx._mark_closed()
        with pytest.raises(CartesiaError):
            await ctx.push("hi")

    @pytest.mark.asyncio
    async def test_end_does_not_mark_closed(self) -> None:
        ctx, _ = _make_async_ctx()
        await ctx.end()
        assert ctx.is_closed is False

    @pytest.mark.asyncio
    async def test_flush_after_close_raises(self) -> None:
        ctx, _ = _make_async_ctx()
        ctx._mark_closed()
        with pytest.raises(CartesiaError):
            await ctx.flush()

    @pytest.mark.asyncio
    async def test_flush_after_end_works(self) -> None:
        ctx, fc = _make_async_ctx()
        await ctx.end()
        await ctx.flush()
        assert len(fc.sent) == 2

    @pytest.mark.asyncio
    async def test_cancel_marks_closed(self) -> None:
        ctx, _ = _make_async_ctx()
        await ctx.cancel()
        assert ctx.is_closed is True

    @pytest.mark.asyncio
    async def test_cancel_swallows_cartesia_error_and_marks_closed(self) -> None:
        # cancel() is best-effort: a CartesiaError from send is swallowed and
        # the local context is still marked closed.
        ctx, fc = _make_async_ctx()
        fc.send_should_raise = CartesiaError("boom")
        await ctx.cancel()  # should not raise
        assert ctx.is_closed is True

    @pytest.mark.asyncio
    async def test_receive_yields_then_terminates_on_done(self) -> None:
        ctx, _ = _make_async_ctx()
        ctx._queue.put_nowait(_chunk("ctx-id", 0))
        ctx._queue.put_nowait(_done("ctx-id"))
        events: List[Any] = []
        async for ev in ctx.receive():
            events.append(ev)
        assert len(events) == 2

    @pytest.mark.asyncio
    async def test_receive_after_close_returns_immediately(self) -> None:
        ctx, _ = _make_async_ctx()
        ctx._mark_closed()
        events: List[Any] = [ev async for ev in ctx.receive()]
        assert events == []

    @pytest.mark.asyncio
    async def test_receive_double_call_does_not_block(self) -> None:
        ctx, _ = _make_async_ctx()
        ctx._queue.put_nowait(_done("ctx-id"))
        first: List[Any] = [ev async for ev in ctx.receive()]
        assert len(first) == 1
        second: List[Any] = [ev async for ev in ctx.receive()]
        assert second == []

    @pytest.mark.asyncio
    async def test_receive_timeout_yields_synthetic_error(self) -> None:
        ctx, _ = _make_async_ctx(timeout=0.05)
        events: List[Any] = []
        async for ev in ctx.receive():
            events.append(ev)
        assert len(events) == 1
        ev = events[0]
        assert isinstance(ev, Error)
        assert ev.error_code == "client_timeout"


# ---------------------------------------------------------------------------
# TTSContextsWSConnection registry
# ---------------------------------------------------------------------------


class TestTTSContextsWSConnectionRegistry:
    def test_context_creates_with_uuid(self) -> None:
        conn = _make_sync_connection()
        ctx = conn.context(
            model_id="m",
            voice=DEFAULT_VOICE,
            output_format=DEFAULT_OUTPUT_FORMAT,
        )
        assert len(ctx.context_id) == 36
        assert ctx in conn.list_contexts()

    def test_context_uses_provided_id(self) -> None:
        conn = _make_sync_connection()
        ctx = conn.context(
            model_id="m",
            voice=DEFAULT_VOICE,
            output_format=DEFAULT_OUTPUT_FORMAT,
            context_id="my-id",
        )
        assert ctx.context_id == "my-id"

    def test_duplicate_context_id_raises(self) -> None:
        conn = _make_sync_connection()
        conn.context(
            model_id="m",
            voice=DEFAULT_VOICE,
            output_format=DEFAULT_OUTPUT_FORMAT,
            context_id="dup",
        )
        with pytest.raises(CartesiaError, match="Duplicate context ID"):
            conn.context(
                model_id="m",
                voice=DEFAULT_VOICE,
                output_format=DEFAULT_OUTPUT_FORMAT,
                context_id="dup",
            )

    def test_get_context_returns_registered(self) -> None:
        conn = _make_sync_connection()
        ctx = conn.context(
            model_id="m",
            voice=DEFAULT_VOICE,
            output_format=DEFAULT_OUTPUT_FORMAT,
            context_id="abc",
        )
        assert conn.get_context("abc") is ctx

    def test_get_context_returns_none_for_unknown(self) -> None:
        conn = _make_sync_connection()
        assert conn.get_context("missing") is None

    def test_unregister_after_mark_closed(self) -> None:
        conn = _make_sync_connection()
        ctx = conn.context(
            model_id="m",
            voice=DEFAULT_VOICE,
            output_format=DEFAULT_OUTPUT_FORMAT,
            context_id="abc",
        )
        ctx._mark_closed()
        assert conn.get_context("abc") is None


# ---------------------------------------------------------------------------
# TTSContextsWSConnection routing
# ---------------------------------------------------------------------------


class TestTTSContextsWSConnectionRouting:
    def test_route_event_routes_to_context_queue(self) -> None:
        conn = _make_sync_connection()
        ctx = conn.context(
            model_id="m",
            voice=DEFAULT_VOICE,
            output_format=DEFAULT_OUTPUT_FORMAT,
            context_id="abc",
        )
        ev = _chunk("abc")
        conn._route_event(ev)
        assert ctx._queue.get_nowait() is ev

    def test_route_event_drops_unknown_context_chunk(self) -> None:
        conn = _make_sync_connection()
        # Should not raise.
        conn._route_event(_chunk("unknown-ctx"))

    def test_route_event_dispatches_unknown_context_error(self) -> None:
        conn = _make_sync_connection()
        received: List[Error] = []

        def handler(e: Error) -> None:
            received.append(e)

        conn.on_error(handler)
        err = _error(context_id=None)
        conn._route_event(err)
        assert received == [err]

    def test_off_error_removes_handler(self) -> None:
        conn = _make_sync_connection()
        received: List[Error] = []

        def handler(e: Error) -> None:
            received.append(e)

        conn.on_error(handler).off_error(handler)
        conn._route_event(_error(context_id=None))
        assert received == []

    def test_once_error_fires_then_removes(self) -> None:
        conn = _make_sync_connection()
        received: List[Error] = []

        def handler(e: Error) -> None:
            received.append(e)

        conn.once_error(handler)
        conn._route_event(_error(context_id=None))
        conn._route_event(_error(context_id=None))
        assert len(received) == 1

    def test_on_error_decorator_form(self) -> None:
        conn = _make_sync_connection()
        received: List[Error] = []

        @conn.on_error()
        def handler(e: Error) -> None:
            received.append(e)

        # Decorator must return the original function so the name still binds to it.
        assert callable(handler)
        err = _error(context_id=None)
        conn._route_event(err)
        assert received == [err]
        # And the function reference can still be passed back to off_error.
        conn.off_error(handler)
        conn._route_event(_error(context_id=None))
        assert len(received) == 1

    def test_once_error_decorator_form(self) -> None:
        conn = _make_sync_connection()
        received: List[Error] = []

        @conn.once_error()
        def handler(e: Error) -> None:
            received.append(e)

        conn._route_event(_error(context_id=None))
        conn._route_event(_error(context_id=None))
        assert len(received) == 1
        # Decorator returns the original function, not the connection.
        assert callable(handler)


# ---------------------------------------------------------------------------
# TTSContextsWSConnection lifecycle events
# ---------------------------------------------------------------------------


class TestTTSContextsWSConnectionLifecycleEvents:
    def test_reconnecting_user_callback_invoked(self) -> None:
        """The user-supplied on_reconnecting callback is forwarded as-is."""
        received_user: List[ReconnectingEvent] = []

        def user_cb(event: ReconnectingEvent) -> None:
            received_user.append(event)
            return None

        conn = _make_sync_connection(on_reconnecting=user_cb)
        wrapped = conn._wrap_on_reconnecting()
        assert wrapped is not None
        evt = ReconnectingEvent(
            attempt=1,
            max_attempts=5,
            delay=0.5,
            close_code=1006,
            extra_query={},
            extra_headers={},
        )
        wrapped(evt)
        assert received_user == [evt]

    def test_reconnecting_clears_contexts_on_first_attempt(self) -> None:
        """On reconnect attempt 1, all contexts are marked closed (server context_ids don't survive)."""

        def user_cb(_e: ReconnectingEvent) -> None:
            return None

        conn = _make_sync_connection(on_reconnecting=user_cb)
        ctx = conn.context(
            model_id="m",
            voice=DEFAULT_VOICE,
            output_format=DEFAULT_OUTPUT_FORMAT,
        )
        wrapped = conn._wrap_on_reconnecting()
        assert wrapped is not None
        wrapped(
            ReconnectingEvent(
                attempt=1,
                max_attempts=5,
                delay=0.5,
                close_code=1006,
                extra_query={},
                extra_headers={},
            )
        )
        assert conn.list_contexts() == []
        assert ctx.is_closed is True

    def test_dispatch_events_blocks_until_close(self) -> None:
        conn = _make_sync_connection()
        finished = threading.Event()

        def waiter() -> None:
            conn.dispatch_events()
            finished.set()

        t = threading.Thread(target=waiter, daemon=True)
        t.start()
        # Should still be blocked.
        assert not finished.wait(0.05)
        conn.close()
        assert finished.wait(2.0)


# ---------------------------------------------------------------------------
# AsyncTTSContextsWSConnection (subset)
# ---------------------------------------------------------------------------


class TestAsyncTTSContextsWSConnection:
    @pytest.mark.asyncio
    async def test_context_creates_and_registers(self) -> None:
        conn = _make_async_connection()
        ctx = await conn.context(
            model_id="m",
            voice=DEFAULT_VOICE,
            output_format=DEFAULT_OUTPUT_FORMAT,
            context_id="abc",
        )
        assert ctx.context_id == "abc"
        assert conn.get_context("abc") is ctx

    @pytest.mark.asyncio
    async def test_route_event_to_context_queue(self) -> None:
        conn = _make_async_connection()
        ctx = await conn.context(
            model_id="m",
            voice=DEFAULT_VOICE,
            output_format=DEFAULT_OUTPUT_FORMAT,
            context_id="abc",
        )
        ev = _chunk("abc")
        conn._route_event(ev)
        assert ctx._queue.get_nowait() is ev

    @pytest.mark.asyncio
    async def test_handle_terminal_disconnect_clears_contexts(self) -> None:
        """Terminal disconnect should mark all contexts closed."""
        conn = _make_async_connection()
        ctx = await conn.context(
            model_id="m",
            voice=DEFAULT_VOICE,
            output_format=DEFAULT_OUTPUT_FORMAT,
            context_id="abc",
        )
        connection = conn._inner_connection
        await conn._handle_terminal_disconnect(cast(Any, connection))
        assert ctx.is_closed is True
        assert conn.list_contexts() == []


# ---------------------------------------------------------------------------
# Manager-level handler propagation
# ---------------------------------------------------------------------------


class TestManagerHandlerPropagation:
    def _new_mgr(self) -> _TTSContextsWSConnectionManager:
        return _TTSContextsWSConnectionManager(
            client=cast(Any, MagicMock()),
            extra_query={},
            extra_headers={},
            websocket_connection_options={},
        )

    def test_on_error_registers_handler(self) -> None:
        mgr = self._new_mgr()

        def handler(_e: Error) -> None:
            return None

        mgr.on_error(handler)
        assert mgr._event_handler_registry.has_handlers("error")

    def test_off_error_removes_handler(self) -> None:
        mgr = self._new_mgr()

        def handler(_e: Error) -> None:
            return None

        mgr.on_error(handler)
        mgr.off_error(handler)
        assert not mgr._event_handler_registry.has_handlers("error")
