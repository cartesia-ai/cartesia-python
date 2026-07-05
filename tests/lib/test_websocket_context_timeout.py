import asyncio

from cartesia.lib._tts import AsyncWebSocketContext


class _FakeConnection:
    """Minimal stand-in exposing only what AsyncWebSocketContext.receive() touches."""

    def __init__(self) -> None:
        self._context_queues: dict = {}


async def test_async_receive_cleans_up_context_queue_on_timeout() -> None:
    connection = _FakeConnection()
    context_id = "ctx-timeout"
    # Queue is never fed, so the receive loop hits its timeout.
    connection._context_queues[context_id] = asyncio.Queue()

    context = AsyncWebSocketContext(connection, context_id, timeout=0.01)  # type: ignore[arg-type]

    raised = False
    try:
        async for _ in context.receive():
            pass
    except (TimeoutError, asyncio.TimeoutError):
        raised = True

    assert raised, "receive() should propagate the timeout to the caller"
    # The per-context queue must be removed so it does not leak on the connection.
    # Before Python 3.11 asyncio.wait_for raised asyncio.TimeoutError (not the
    # builtin TimeoutError), so the old `except TimeoutError` missed it and this
    # cleanup was skipped.
    assert context_id not in connection._context_queues
