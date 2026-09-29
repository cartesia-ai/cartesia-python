from __future__ import annotations

import time
import asyncio
import threading
from typing import Iterator

import pytest
from websockets.exceptions import ConnectionClosedError
from websockets.sync.server import ServerConnection, serve

from cartesia import AsyncCartesia


class _Server:
    """Accepts a connection and closes it with `code` after the first message."""

    def __init__(self, code: int) -> None:
        self.code = code
        self._server = serve(self._handle, "127.0.0.1", 0)
        self.url = f"ws://127.0.0.1:{self._server.socket.getsockname()[1]}"
        threading.Thread(target=self._server.serve_forever, daemon=True).start()

    def _handle(self, ws: ServerConnection) -> None:
        try:
            next(iter(ws))
            time.sleep(0.05)
            ws.close(self.code)
        except Exception:
            pass

    def close(self) -> None:
        self._server.shutdown()


@pytest.fixture
def abnormal_server() -> Iterator[_Server]:
    srv = _Server(1011)
    yield srv
    srv.close()


@pytest.fixture
def normal_server() -> Iterator[_Server]:
    srv = _Server(1000)
    yield srv
    srv.close()


async def test_async_receive_raises_when_server_closes_connection(abnormal_server: _Server) -> None:
    client = AsyncCartesia(api_key="key", websocket_base_url=abnormal_server.url)

    async with client.tts.websocket_connect() as connection:
        ctx = connection.context()
        await ctx.push("Hello", voice={"mode": "id", "id": "voice"})

        async def drain() -> None:
            async for _ in ctx.receive():
                pass

        with pytest.raises(ConnectionClosedError):
            await asyncio.wait_for(drain(), timeout=3)


async def test_async_receive_ends_when_server_closes_connection_cleanly(normal_server: _Server) -> None:
    client = AsyncCartesia(api_key="key", websocket_base_url=normal_server.url)

    async with client.tts.websocket_connect() as connection:
        ctx = connection.context()
        await ctx.push("Hello", voice={"mode": "id", "id": "voice"})

        async def drain() -> None:
            async for _ in ctx.receive():
                pass

        await asyncio.wait_for(drain(), timeout=3)
