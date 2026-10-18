from __future__ import annotations

from typing import Any

import httpx
import pytest

from cartesia import Cartesia, AsyncCartesia


@pytest.mark.parametrize(
    "base_url",
    [
        "https://proxy.example",
        "https://proxy.example/api/v1/",
        "https://proxy.example/api/v1",
        "https://proxy.example/tenant%2Fname/",
    ],
)
@pytest.mark.parametrize("query", ["", "?route=speech&tag=a%2Fb"])
def test_tts_websocket_path_with_base_query(base_url: str, query: str, monkeypatch: pytest.MonkeyPatch) -> None:
    captured: list[httpx.URL] = []

    def connect(uri: str, **_kwargs: Any) -> object:
        captured.append(httpx.URL(uri))
        return object()

    monkeypatch.setattr("websockets.sync.client.connect", connect)
    with Cartesia(token="test-token", base_url=base_url + query) as client:
        client.tts.websocket_connect(extra_query={"extra": "value"}).enter()

    expected_path = httpx.URL(base_url).path.rstrip("/") + "/tts/websocket"
    assert captured[0].path == expected_path
    assert captured[0].copy_with(query=None).raw_path == httpx.URL(base_url).raw_path.rstrip(b"/") + b"/tts/websocket"
    assert captured[0].scheme == "wss"
    assert dict(captured[0].params) == {**dict(httpx.URL(base_url + query).params), "extra": "value"}


@pytest.mark.parametrize(
    "base_url",
    [
        "https://proxy.example",
        "https://proxy.example/api/v1/",
        "https://proxy.example/api/v1",
        "https://proxy.example/tenant%2Fname/",
    ],
)
@pytest.mark.parametrize("query", ["", "?route=speech&tag=a%2Fb"])
async def test_async_tts_websocket_path_with_base_query(
    base_url: str, query: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    captured: list[httpx.URL] = []

    async def connect(uri: str, **_kwargs: Any) -> object:
        captured.append(httpx.URL(uri))
        return object()

    monkeypatch.setattr("websockets.asyncio.client.connect", connect)
    async with AsyncCartesia(token="test-token", base_url=base_url + query) as client:
        await client.tts.websocket_connect(extra_query={"extra": "value"}).enter()

    expected_path = httpx.URL(base_url).path.rstrip("/") + "/tts/websocket"
    assert captured[0].path == expected_path
    assert captured[0].copy_with(query=None).raw_path == httpx.URL(base_url).raw_path.rstrip(b"/") + b"/tts/websocket"
    assert captured[0].scheme == "wss"
    assert dict(captured[0].params) == {**dict(httpx.URL(base_url + query).params), "extra": "value"}
