from __future__ import annotations

from typing import Any

import httpx
import pytest

from cartesia import Cartesia, AsyncCartesia
from cartesia._types import Omit
from cartesia._models import FinalRequestOptions
from cartesia._base_client import make_request_options


def test_request_extra_query_omits_values(client: Cartesia) -> None:
    request = client._build_request(
        FinalRequestOptions(
            method="post",
            url="/foo",
            **make_request_options(
                query={"foo": "1", "bar": Omit()},
                extra_query={"foo": Omit(), "baz": "2"},
            ),
        ),
    )

    assert dict(request.url.params) == {"baz": "2"}


def test_tts_websocket_extra_query_omits_values(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    captured_url: httpx.URL | None = None

    def fake_connect(uri: str, *_args: Any, **_kwargs: Any) -> object:
        nonlocal captured_url
        captured_url = httpx.URL(uri)
        return object()

    monkeypatch.setattr("websockets.sync.client.connect", fake_connect)

    client.tts.websocket_connect(extra_query={"keep": "1", "skip": Omit()}).enter()

    assert captured_url is not None
    assert dict(captured_url.params) == {"keep": "1"}


async def test_async_tts_websocket_extra_query_omits_values(
    async_client: AsyncCartesia, monkeypatch: pytest.MonkeyPatch
) -> None:
    captured_url: httpx.URL | None = None

    async def fake_connect(uri: str, *_args: Any, **_kwargs: Any) -> object:
        nonlocal captured_url
        captured_url = httpx.URL(uri)
        return object()

    monkeypatch.setattr("websockets.asyncio.client.connect", fake_connect)

    await async_client.tts.websocket_connect(extra_query={"keep": "1", "skip": Omit()}).enter()

    assert captured_url is not None
    assert dict(captured_url.params) == {"keep": "1"}


def test_stt_external_vad_websocket_query_omits_values(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    captured_url: httpx.URL | None = None

    def fake_connect(uri: str, *_args: Any, **_kwargs: Any) -> object:
        nonlocal captured_url
        captured_url = httpx.URL(uri)
        return object()

    monkeypatch.setattr("websockets.sync.client.connect", fake_connect)

    client.stt.external_vad.websocket(
        encoding="pcm_s16le",
        model="ink-2",
        sample_rate=16_000,
        extra_query={"keep": "1", "skip": Omit()},
    ).enter()

    assert captured_url is not None
    assert dict(captured_url.params) == {
        "encoding": "pcm_s16le",
        "model": "ink-2",
        "sample_rate": "16000",
        "keep": "1",
    }


async def test_async_stt_external_vad_websocket_query_omits_values(
    async_client: AsyncCartesia, monkeypatch: pytest.MonkeyPatch
) -> None:
    captured_url: httpx.URL | None = None

    async def fake_connect(uri: str, *_args: Any, **_kwargs: Any) -> object:
        nonlocal captured_url
        captured_url = httpx.URL(uri)
        return object()

    monkeypatch.setattr("websockets.asyncio.client.connect", fake_connect)

    await async_client.stt.external_vad.websocket(
        encoding="pcm_s16le",
        model="ink-2",
        sample_rate=16_000,
        extra_query={"keep": "1", "skip": Omit()},
    ).enter()

    assert captured_url is not None
    assert dict(captured_url.params) == {
        "encoding": "pcm_s16le",
        "model": "ink-2",
        "sample_rate": "16000",
        "keep": "1",
    }


def test_stt_turn_detecting_websocket_query_omits_values(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    captured_url: httpx.URL | None = None

    def fake_connect(uri: str, *_args: Any, **_kwargs: Any) -> object:
        nonlocal captured_url
        captured_url = httpx.URL(uri)
        return object()

    monkeypatch.setattr("websockets.sync.client.connect", fake_connect)

    client.stt.turn_detecting.websocket(
        encoding="pcm_s16le",
        model="ink-2",
        sample_rate=16_000,
        extra_query={"keep": "1", "skip": Omit()},
    ).enter()

    assert captured_url is not None
    assert dict(captured_url.params) == {
        "encoding": "pcm_s16le",
        "model": "ink-2",
        "sample_rate": "16000",
        "keep": "1",
    }


async def test_async_stt_turn_detecting_websocket_query_omits_values(
    async_client: AsyncCartesia, monkeypatch: pytest.MonkeyPatch
) -> None:
    captured_url: httpx.URL | None = None

    async def fake_connect(uri: str, *_args: Any, **_kwargs: Any) -> object:
        nonlocal captured_url
        captured_url = httpx.URL(uri)
        return object()

    monkeypatch.setattr("websockets.asyncio.client.connect", fake_connect)

    await async_client.stt.turn_detecting.websocket(
        encoding="pcm_s16le",
        model="ink-2",
        sample_rate=16_000,
        extra_query={"keep": "1", "skip": Omit()},
    ).enter()

    assert captured_url is not None
    assert dict(captured_url.params) == {
        "encoding": "pcm_s16le",
        "model": "ink-2",
        "sample_rate": "16000",
        "keep": "1",
    }
