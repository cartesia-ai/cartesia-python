"""Tests for the async WebSocket background dispatcher.

The async connection spins up a background task that continuously reads from
the WebSocket and routes events into per-context queues.  These unit tests
verify two key properties using a mock WebSocket (no API key required):

1. The WebSocket buffer never fills up — the background task drains it
   even before any user code calls ``ctx.receive()``.
2. A slow reader on one context does not block readers on other contexts.
"""

from __future__ import annotations

import json
import asyncio
from typing import Any

import pytest

from cartesia.lib._tts.connection_manager_3_0_2 import AsyncTTSResourceConnection_3_0_2

# ---------------------------------------------------------------------------
# Mock WebSocket
# ---------------------------------------------------------------------------


class MockAsyncWebsocket:
    """Fake async WebSocket whose receive buffer is an asyncio.Queue.

    Tests call ``inject_*`` helpers to push messages onto the queue.
    The ``AsyncTTSResourceConnection`` background task calls ``recv()``
    which pops from the same queue.
    """

    def __init__(self) -> None:
        self._queue: asyncio.Queue[bytes | None] = asyncio.Queue()
        self._closed = False
        self._sent: list[str] = []

    # -- WebSocket interface consumed by AsyncTTSResourceConnection ----------

    async def recv(self, *, decode: bool = True) -> bytes | str:
        msg = await self._queue.get()
        if msg is None:
            # Sentinel: simulate a clean close.
            from websockets.exceptions import ConnectionClosedOK

            raise ConnectionClosedOK(None, None)
        return msg.decode() if decode else msg

    async def send(self, data: str | bytes) -> None:
        if isinstance(data, bytes):
            data = data.decode()
        self._sent.append(data)

    async def close(self, code: int = 1000, reason: str = "") -> None:  # noqa: ARG002
        self._closed = True

    @property
    def state(self) -> Any:
        from websockets.protocol import State

        return State.CLOSED if self._closed else State.OPEN

    # -- Test helpers --------------------------------------------------------

    def inject_chunk(self, context_id: str, seq: int = 0) -> None:
        self._queue.put_nowait(
            json.dumps(
                {
                    "type": "chunk",
                    "context_id": context_id,
                    "data": f"audio_{seq}",
                    "done": False,
                    "status_code": 200,
                    "step_time": 0.0,
                }
            ).encode()
        )

    def inject_done(self, context_id: str) -> None:
        self._queue.put_nowait(
            json.dumps(
                {
                    "type": "done",
                    "context_id": context_id,
                    "done": True,
                    "status_code": 200,
                }
            ).encode()
        )


def _make_connection(ws: MockAsyncWebsocket) -> AsyncTTSResourceConnection_3_0_2:
    return AsyncTTSResourceConnection_3_0_2(ws)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_dispatcher_drains_websocket_buffer():
    """The background task should consume messages even before receive() is called.

    This ensures the WebSocket read buffer never fills up regardless of when
    user code starts reading from the context queue.
    """
    ws = MockAsyncWebsocket()
    conn = _make_connection(ws)

    NUM_CHUNKS = 50
    ctx_id = "buffer-test"

    # Register a context (creates the queue).
    ctx = conn.context(ctx_id)

    # Push many messages onto the fake wire *before* anyone calls receive().
    for i in range(NUM_CHUNKS):
        ws.inject_chunk(ctx_id, seq=i)
    ws.inject_done(ctx_id)

    # Start the background dispatcher (normally triggered by send()).
    conn._dispatch_listener()

    # Wait until the mock WebSocket queue is fully drained.
    for _ in range(200):
        if ws._queue.empty():
            break
        await asyncio.sleep(0.01)

    assert ws._queue.empty(), "Background task should have consumed all messages from the WebSocket"

    # All messages should now be sitting in the context queue.
    ctx_queue = conn._context_queues[ctx_id]
    assert ctx_queue.qsize() == NUM_CHUNKS + 1  # chunks + done

    # Now consume via receive() — everything should already be available.
    chunks: list[Any] = []
    async for event in ctx.receive():
        if event.type == "chunk":
            chunks.append(event)

    assert len(chunks) == NUM_CHUNKS

    await conn.close()


@pytest.mark.asyncio
async def test_slow_reader_does_not_block_fast_reader():
    """A slow consumer on one context must not delay other contexts.

    With the background dispatcher, each context reads from its own
    independent queue.  A slow reader sleeping between iterations cannot
    block a fast reader on a different context.
    """
    ws = MockAsyncWebsocket()
    conn = _make_connection(ws)

    NUM_CHUNKS = 20
    SLOW_DELAY = 0.05  # seconds per event for slow reader

    ctx_slow = conn.context("slow-ctx")
    ctx_fast = conn.context("fast-ctx")

    # Inject interleaved messages for both contexts.
    for i in range(NUM_CHUNKS):
        ws.inject_chunk("slow-ctx", seq=i)
        ws.inject_chunk("fast-ctx", seq=i)
    ws.inject_done("slow-ctx")
    ws.inject_done("fast-ctx")

    # Start dispatcher.
    conn._dispatch_listener()

    # Wait for dispatcher to drain the mock wire.
    for _ in range(200):
        if ws._queue.empty():
            break
        await asyncio.sleep(0.01)

    # Slow reader: sleeps between every event.
    async def slow_collect() -> list[Any]:
        chunks: list[Any] = []
        async for event in ctx_slow.receive():
            if event.type == "chunk":
                chunks.append(event)
            await asyncio.sleep(SLOW_DELAY)
        return chunks

    # Fast reader: no delays.
    fast_start: float = 0
    fast_end: float = 0

    async def fast_collect() -> list[Any]:
        nonlocal fast_start, fast_end
        loop = asyncio.get_event_loop()
        fast_start = loop.time()
        chunks: list[Any] = []
        async for event in ctx_fast.receive():
            if event.type == "chunk":
                chunks.append(event)
        fast_end = loop.time()
        return chunks

    slow_chunks, fast_chunks = await asyncio.gather(
        slow_collect(),
        fast_collect(),
    )

    assert len(slow_chunks) == NUM_CHUNKS
    assert len(fast_chunks) == NUM_CHUNKS

    # The fast reader should finish nearly instantly (all events already queued).
    # The slow reader needs at least NUM_CHUNKS * SLOW_DELAY ≈ 1 second.
    fast_duration = fast_end - fast_start
    slow_min_duration = NUM_CHUNKS * SLOW_DELAY

    assert fast_duration < slow_min_duration / 2, (
        f"Fast reader took {fast_duration:.3f}s but slow reader needs "
        f"~{slow_min_duration:.1f}s — fast reader should not be blocked"
    )

    await conn.close()


# ---------------------------------------------------------------------------
# Tests for the new TTSContextsConnection / AsyncTTSContextsConnection
# background reader (in cartesia.lib._tts.contexts)
#
# These tests drive the bg reader manually via _reader_loop / _route_event,
# bypassing the real WebSocket. They verify event routing into per-context
# queues, and lifecycle event emission (close / reconnecting / reconnected).
# ---------------------------------------------------------------------------


import queue as _queue_mod
import threading
from typing import Dict, List, Tuple, Iterator, Optional, AsyncIterator as TypingAsyncIterator, cast
from unittest.mock import MagicMock

from cartesia.types import ReconnectingEvent
from cartesia.lib._tts.contexts import (
    TTSContextsConnection,
    AsyncTTSContextsConnection,
)
from cartesia.types.websocket_response import Done, Chunk, Error as WSResponseError

_OUTPUT_FORMAT: Any = {"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100}
_VOICE: Any = {"mode": "id", "id": "test-voice"}


class _FakeManagerAttrs:
    """Minimal stub matching the attributes TTSContextsConnection reads off the manager."""

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


class _MockSyncInnerConnection:
    """Mocks the auto-gen TTSResourceConnection that the new bg reader iterates over."""

    def __init__(self) -> None:
        self._events: "_queue_mod.Queue[Any]" = _queue_mod.Queue()
        self.sent: List[Any] = []
        self._closed = False

    def __iter__(self) -> Iterator[Any]:
        while True:
            item = self._events.get()
            if item is None:
                return
            yield item

    def send(self, event: Any) -> None:
        self.sent.append(event)

    def close(self, *, code: int = 1000, reason: str = "") -> None:  # noqa: ARG002
        self._closed = True
        # Sentinel to break the iterator loop.
        self._events.put_nowait(None)

    def inject(self, event: Any) -> None:
        self._events.put_nowait(event)


class _MockAsyncInnerConnection:
    """Async mock matching the auto-gen AsyncTTSResourceConnection.

    The reader uses ``async for response in connection`` which expects
    ``__aiter__`` to be an async generator function.
    """

    def __init__(self) -> None:
        self._events: "asyncio.Queue[Any]" = asyncio.Queue()
        self.sent: List[Any] = []
        self._closed = False

    async def __aiter__(self) -> TypingAsyncIterator[Any]:
        while True:
            item = await self._events.get()
            if item is None:
                return
            yield item

    async def send(self, event: Any) -> None:
        self.sent.append(event)

    async def close(self, *, code: int = 1000, reason: str = "") -> None:  # noqa: ARG002
        self._closed = True
        await self._events.put(None)

    def inject(self, event: Any) -> None:
        self._events.put_nowait(event)


def _make_sync_conn() -> Tuple[TTSContextsConnection, _MockSyncInnerConnection]:
    conn = TTSContextsConnection(cast(Any, _FakeManagerAttrs()))
    inner = _MockSyncInnerConnection()
    conn._inner_connection = cast(Any, inner)
    conn._ensure_connected = lambda: None  # type: ignore[method-assign]
    return conn, inner


def _make_async_conn() -> Tuple[AsyncTTSContextsConnection, _MockAsyncInnerConnection]:
    conn = AsyncTTSContextsConnection(cast(Any, _FakeManagerAttrs()))
    inner = _MockAsyncInnerConnection()
    conn._inner_connection = cast(Any, inner)

    async def _noop() -> None:
        return None

    conn._ensure_connected = _noop  # type: ignore[method-assign]
    return conn, inner


def _chunk_event(context_id: str, seq: int = 0) -> Chunk:
    return Chunk(
        type="chunk",
        context_id=context_id,
        data=f"audio_{seq}",
        done=False,
        status_code=200,
        step_time=0.0,
    )


def _done_event(context_id: str) -> Done:
    return Done(type="done", context_id=context_id, done=True, status_code=200)


def _error_event(context_id: Optional[str] = None, *, done: bool = True) -> WSResponseError:
    return WSResponseError(
        type="error",
        done=done,
        context_id=context_id,
        error_code="test_error",
        message="t",
    )


# ---- sync ----


def test_sync_dispatcher_drains_buffer_to_context_queue() -> None:
    """Bg reader should drain the inner-connection iterator and route to context queues."""
    conn, inner = _make_sync_conn()
    ctx = conn.context(model_id="m", voice=_VOICE, output_format=_OUTPUT_FORMAT, context_id="c1")

    NUM = 5
    for i in range(NUM):
        inner.inject(_chunk_event("c1", seq=i))
    inner.inject(_done_event("c1"))

    # Drive the bg reader synchronously in this thread.
    t = threading.Thread(target=conn._reader_loop, args=(cast(Any, inner),), daemon=True)
    t.start()
    # Drain in the main thread via ctx.receive() — terminal event will end iteration.
    chunks: List[Any] = []
    for ev in ctx.receive():
        if ev.type == "chunk":
            chunks.append(ev)
    assert len(chunks) == NUM

    inner.close()
    t.join(timeout=2.0)


def test_sync_dispatcher_drops_events_for_unknown_context() -> None:
    conn, inner = _make_sync_conn()
    received_errors: List[Any] = []

    def err_handler(e: Any) -> None:
        received_errors.append(e)

    conn.on_error(err_handler)
    # Chunk for unknown context: silently dropped.
    conn._route_event(_chunk_event("does-not-exist"))
    # Error with no context_id: dispatched to handlers.
    err = _error_event(context_id=None)
    conn._route_event(err)
    assert received_errors == [err]
    inner.close()


def test_sync_dispatcher_clears_contexts_on_terminal_disconnect() -> None:
    """Terminal disconnect should mark all open contexts closed."""
    conn, inner = _make_sync_conn()
    ctx = conn.context(model_id="m", voice=_VOICE, output_format=_OUTPUT_FORMAT, context_id="c1")
    inner.close()
    conn._reader_loop(cast(Any, inner))
    assert ctx.is_closed is True
    assert conn.list_contexts() == []


def test_sync_dispatcher_forwards_user_reconnecting_callback() -> None:
    """The user-supplied on_reconnecting callback is forwarded as-is by the wrapper."""
    received: List[ReconnectingEvent] = []

    def user_cb(event: ReconnectingEvent) -> None:
        received.append(event)
        return None

    conn = TTSContextsConnection(cast(Any, _FakeManagerAttrs(on_reconnecting=user_cb)))
    inner: Any = MagicMock()
    conn._inner_connection = inner
    conn._ensure_connected = lambda: None  # type: ignore[method-assign]

    wrapped = conn._wrap_on_reconnecting()
    assert wrapped is not None
    evt = ReconnectingEvent(attempt=1, max_attempts=5, delay=0.5, close_code=1006, extra_query={}, extra_headers={})
    wrapped(evt)
    assert received == [evt]


def test_sync_dispatcher_routes_to_multiple_contexts() -> None:
    conn, inner = _make_sync_conn()
    ctx_a = conn.context(model_id="m", voice=_VOICE, output_format=_OUTPUT_FORMAT, context_id="a")
    ctx_b = conn.context(model_id="m", voice=_VOICE, output_format=_OUTPUT_FORMAT, context_id="b")

    inner.inject(_chunk_event("a"))
    inner.inject(_chunk_event("b"))
    inner.inject(_chunk_event("a"))
    inner.inject(_done_event("a"))
    inner.inject(_done_event("b"))

    t = threading.Thread(target=conn._reader_loop, args=(cast(Any, inner),), daemon=True)
    t.start()

    a_events = list(ctx_a.receive())
    b_events = list(ctx_b.receive())

    assert sum(1 for e in a_events if e.type == "chunk") == 2
    assert sum(1 for e in b_events if e.type == "chunk") == 1

    inner.close()
    t.join(timeout=2.0)


# ---- async ----


@pytest.mark.asyncio
async def test_async_dispatcher_routes_events_to_context_queue() -> None:
    conn, inner = _make_async_conn()
    ctx = await conn.context(model_id="m", voice=_VOICE, output_format=_OUTPUT_FORMAT, context_id="c1")

    NUM = 5
    for i in range(NUM):
        inner.inject(_chunk_event("c1", seq=i))
    inner.inject(_done_event("c1"))

    # Patch __aiter__ to use our generator.
    task = asyncio.create_task(conn._reader_loop(cast(Any, inner)))

    chunks: List[Any] = []
    async for ev in ctx.receive():
        if ev.type == "chunk":
            chunks.append(ev)
    assert len(chunks) == NUM

    await inner.close()
    await asyncio.wait_for(task, timeout=2.0)


@pytest.mark.asyncio
async def test_async_dispatcher_clears_contexts_on_terminal_disconnect() -> None:
    """Terminal disconnect should mark all open contexts closed."""
    conn, inner = _make_async_conn()
    ctx = await conn.context(model_id="m", voice=_VOICE, output_format=_OUTPUT_FORMAT, context_id="c1")
    await inner.close()
    await conn._reader_loop(cast(Any, inner))
    assert ctx.is_closed is True
    assert conn.list_contexts() == []
