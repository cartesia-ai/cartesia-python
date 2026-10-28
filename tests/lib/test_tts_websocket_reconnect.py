from __future__ import annotations

import json
import asyncio
from typing import Any, List, AsyncGenerator
from contextlib import asynccontextmanager

import pytest
from websockets.asyncio.server import ServerConnection as AsyncServerConnection, serve

from cartesia import AsyncCartesia
from cartesia._exceptions import CartesiaError

# Bounds a hang only: every exchange here is local and completes in milliseconds.
HANG_TIMEOUT = 30.0
VOICE = {"mode": "id", "id": "voice"}


def _done(context_id: str) -> str:
    return json.dumps({"type": "done", "context_id": context_id, "done": True, "status_code": 200})


@asynccontextmanager
async def _server(close_after: str) -> AsyncGenerator[tuple[str, List[AsyncServerConnection]], None]:
    """Serve TTS contexts, ending each connection as `close_after` says.

    `"done"` closes a connection after answering its first context, as an idle timeout would
    between contexts. `"request"` closes it on the first request, before any answer.
    """
    connections: List[AsyncServerConnection] = []

    async def handler(websocket: AsyncServerConnection) -> None:
        connections.append(websocket)
        async for message in websocket:
            request = json.loads(message)
            if close_after == "request":
                return
            if not request["continue"]:
                await websocket.send(_done(request["context_id"]))
                return

    async with serve(handler, "127.0.0.1", 0) as server:
        port: int = next(iter(server.sockets)).getsockname()[1]
        yield f"ws://127.0.0.1:{port}", connections


async def _speak(connection: Any) -> List[str]:
    context = connection.context(model_id="sonic-3", voice=VOICE)
    await context.push("Hello.")
    await context.no_more_inputs()
    return [event.type async for event in context.receive()]


async def test_async_connection_reconnects_after_the_server_closes_it() -> None:
    async with _server(close_after="done") as (url, connections):
        client = AsyncCartesia(api_key="key", websocket_base_url=url)
        async with client.tts.websocket_connect() as connection:
            assert await asyncio.wait_for(_speak(connection), HANG_TIMEOUT) == ["done"]
            await asyncio.wait_for(connections[0].wait_closed(), HANG_TIMEOUT)

            assert await asyncio.wait_for(_speak(connection), HANG_TIMEOUT) == ["done"]
    assert len(connections) == 2


async def test_async_context_raises_when_the_connection_closes_before_it_completes() -> None:
    async with _server(close_after="request") as (url, _):
        client = AsyncCartesia(api_key="key", websocket_base_url=url)
        async with client.tts.websocket_connect() as connection:
            with pytest.raises(CartesiaError):
                await asyncio.wait_for(_speak(connection), HANG_TIMEOUT)
