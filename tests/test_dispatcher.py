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

from cartesia.resources.tts import AsyncTTSResourceConnection

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


def _make_connection(ws: MockAsyncWebsocket) -> AsyncTTSResourceConnection:
    return AsyncTTSResourceConnection(ws)  # type: ignore[arg-type]


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

    assert ws._queue.empty(), (
        "Background task should have consumed all messages from the WebSocket"
    )

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
