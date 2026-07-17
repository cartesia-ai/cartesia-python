from __future__ import annotations

import asyncio
from typing import Any, cast

import httpx
import pytest

from cartesia import Cartesia, AsyncCartesia
from cartesia._types import Omit
from cartesia._models import FinalRequestOptions
from cartesia.lib._tts import AsyncWebSocketContext, AsyncTTSResourceConnection
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


def test_stt_manual_finalize_websocket_query_omits_values(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    captured_url: httpx.URL | None = None

    def fake_connect(uri: str, *_args: Any, **_kwargs: Any) -> object:
        nonlocal captured_url
        captured_url = httpx.URL(uri)
        return object()

    monkeypatch.setattr("websockets.sync.client.connect", fake_connect)

    client.stt.manual_finalize.websocket(
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


async def test_async_stt_manual_finalize_websocket_query_omits_values(
    async_client: AsyncCartesia, monkeypatch: pytest.MonkeyPatch
) -> None:
    captured_url: httpx.URL | None = None

    async def fake_connect(uri: str, *_args: Any, **_kwargs: Any) -> object:
        nonlocal captured_url
        captured_url = httpx.URL(uri)
        return object()

    monkeypatch.setattr("websockets.asyncio.client.connect", fake_connect)

    await async_client.stt.manual_finalize.websocket(
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


def test_stt_auto_finalize_websocket_query_omits_values(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    captured_url: httpx.URL | None = None

    def fake_connect(uri: str, *_args: Any, **_kwargs: Any) -> object:
        nonlocal captured_url
        captured_url = httpx.URL(uri)
        return object()

    monkeypatch.setattr("websockets.sync.client.connect", fake_connect)

    client.stt.auto_finalize.websocket(
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


async def test_async_receive_cleans_up_context_queue_on_timeout() -> None:
    """AsyncWebSocketContext.receive() must drop its per-context queue on timeout.

    Before Python 3.11 ``asyncio.wait_for`` raises ``asyncio.TimeoutError`` (a distinct
    class from the builtin ``TimeoutError``), so an ``except TimeoutError`` handler would
    miss it and skip the ``finally`` cleanup — leaking the queue on the connection. The
    handler catches both, so cleanup runs on every supported Python version.
    """
    # The connection only needs a real ``_context_queues`` dict; the underlying socket is
    # never touched because ``receive()`` reads from the queue, not the wire.
    connection = AsyncTTSResourceConnection(cast(Any, object()))
    context_id = "ctx-timeout"
    # Queue is never fed, so the receive loop hits its timeout.
    connection._context_queues[context_id] = asyncio.Queue()

    context = AsyncWebSocketContext(connection, context_id, timeout=0.01)

    with pytest.raises((TimeoutError, asyncio.TimeoutError)):
        async for _ in context.receive():
            pass

    # The per-context queue must be removed so it does not leak on the connection.
    assert context_id not in connection._context_queues


async def test_async_stt_auto_finalize_websocket_query_omits_values(
    async_client: AsyncCartesia, monkeypatch: pytest.MonkeyPatch
) -> None:
    captured_url: httpx.URL | None = None

    async def fake_connect(uri: str, *_args: Any, **_kwargs: Any) -> object:
        nonlocal captured_url
        captured_url = httpx.URL(uri)
        return object()

    monkeypatch.setattr("websockets.asyncio.client.connect", fake_connect)

    await async_client.stt.auto_finalize.websocket(
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
