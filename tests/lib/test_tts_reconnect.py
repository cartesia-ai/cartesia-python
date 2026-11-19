from __future__ import annotations

import json
import time
import asyncio
import threading
from typing import Any, Iterator

import pytest
from websockets.sync.server import ServerConnection, serve

from cartesia import Cartesia, AsyncCartesia


class _Server:
    def __init__(self) -> None:
        self.connections: list[ServerConnection] = []
        self.received: list[str] = []
        self.reply = False
        self._server = serve(self._handle, "127.0.0.1", 0)
        self.url = f"ws://127.0.0.1:{self._server.socket.getsockname()[1]}"
        threading.Thread(target=self._server.serve_forever, daemon=True).start()

    def _handle(self, ws: ServerConnection) -> None:
        self.connections.append(ws)
        try:
            for message in ws:
                self.received.append(str(message))
                context_id = json.loads(message).get("context_id")
                if self.reply and context_id is not None:
                    ws.send(json.dumps({"type": "done", "context_id": context_id, "done": True}))
        except Exception:
            pass

    def wait_for(self, count: int) -> None:
        deadline = time.monotonic() + 5
        while len(self.connections) < count and time.monotonic() < deadline:
            time.sleep(0.01)

    def close(self) -> None:
        self._server.shutdown()


@pytest.fixture
def server() -> Iterator[_Server]:
    srv = _Server()
    yield srv
    srv.close()


_EVENT: Any = {"context_id": "ctx", "cancel": True}


def test_tts_send_reconnects_after_server_closes_connection(server: _Server) -> None:
    client = Cartesia(api_key="key", websocket_base_url=server.url)

    with client.tts.websocket_connect() as connection:
        server.wait_for(1)
        server.connections[0].close()
        time.sleep(0.2)

        connection.send(_EVENT)

        server.wait_for(2)
        assert len(server.connections) == 2


async def test_async_tts_send_reconnects_after_server_closes_connection(server: _Server) -> None:
    client = AsyncCartesia(api_key="key", websocket_base_url=server.url)

    async with client.tts.websocket_connect() as connection:
        server.wait_for(1)
        await asyncio.to_thread(server.connections[0].close)
        await asyncio.sleep(0.2)

        await connection.send(_EVENT)

        server.wait_for(2)
        assert len(server.connections) == 2


async def test_async_context_receives_after_reconnect(server: _Server) -> None:
    server.reply = True
    client = AsyncCartesia(api_key="key", websocket_base_url=server.url)

    async with client.tts.websocket_connect() as connection:
        server.wait_for(1)
        context = connection.context()
        await asyncio.to_thread(server.connections[0].close)
        await asyncio.sleep(0.2)

        await context.send(transcript="hello", voice={"mode": "id", "id": "voice"})

        events = [event async for event in context.receive()]
        assert [event.type for event in events] == ["done"]
