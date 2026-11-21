from __future__ import annotations

import json
import queue
import threading
from typing import Any, Iterator

import pytest
from websockets.sync.server import serve

from cartesia import Cartesia, AsyncCartesia


@pytest.fixture
def tts_server() -> Iterator[tuple[str, queue.Queue[dict[str, Any]]]]:
    received: queue.Queue[dict[str, Any]] = queue.Queue()

    def receive(connection: Any) -> None:
        for message in connection:
            received.put(json.loads(message))

    with serve(receive, "127.0.0.1", 0) as server:
        thread = threading.Thread(target=server.serve_forever)
        thread.start()
        try:
            yield f"http://127.0.0.1:{server.socket.getsockname()[1]}", received
        finally:
            server.shutdown()
            thread.join(timeout=5)


def _assert_final_request(received: queue.Queue[dict[str, Any]]) -> None:
    first = received.get(timeout=5)
    final = received.get(timeout=5)
    expected = dict(first, transcript="", **{"continue": False})
    expected.pop("flush", None)
    assert final == expected


@pytest.mark.parametrize("context_defaults", [False, True])
def test_finalization_keeps_per_request_settings(tts_server: Any, context_defaults: bool) -> None:
    url, received = tts_server
    defaults = {"model_id": "sonic-3", "voice": {"id": "default-voice"}} if context_defaults else {}
    with Cartesia(
        base_url=url, websocket_base_url=url.replace("http:", "ws:"), token="test"
    ).tts.websocket_connect() as connection:
        context = connection.context(**defaults)
        context.push(
            "Hello",
            voice={"id": "selected-voice"},
            model_id="sonic-3.6",
            output_format={"container": "raw", "encoding": "pcm_s16le", "sample_rate": 16000},
            language="fr",
            generation_config={"speed": 1.1},
            flush=True,
        )
        context.no_more_inputs()
        context.no_more_inputs()
        _assert_final_request(received)


@pytest.mark.parametrize("context_defaults", [False, True])
async def test_async_finalization_keeps_per_request_settings(tts_server: Any, context_defaults: bool) -> None:
    url, received = tts_server
    defaults = {"model_id": "sonic-3", "voice": {"id": "default-voice"}} if context_defaults else {}
    async with AsyncCartesia(
        base_url=url, websocket_base_url=url.replace("http:", "ws:"), token="test"
    ).tts.websocket_connect() as connection:
        context = connection.context(**defaults)
        await context.push(
            "Hello",
            voice={"id": "selected-voice"},
            model_id="sonic-3.6",
            output_format={"container": "raw", "encoding": "pcm_s16le", "sample_rate": 16000},
            language="fr",
            generation_config={"speed": 1.1},
            flush=True,
        )
        await context.no_more_inputs()
        await context.no_more_inputs()
        _assert_final_request(received)
