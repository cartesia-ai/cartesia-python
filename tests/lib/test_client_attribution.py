"""Assert cartesia-python identifies itself on every outbound API surface."""

from __future__ import annotations

from collections.abc import Callable

import pytest

from cartesia import Cartesia, AsyncCartesia
from cartesia._types import Omit

from .resources.stt._fakes import FakeSyncWS, FakeAsyncWS, install_sync_connect, install_async_connect

EXPECTED_CLIENT_HEADER_PREFIX = "cartesia-python/"


def _rest_default_headers(client: Cartesia) -> dict[str, str | Omit]:
    return client.default_headers


def _stt_auto_finalize_connect(client: Cartesia) -> None:
    client.stt.auto_finalize.websocket(
        encoding="pcm_s16le",
        model="ink-2",
        sample_rate=16_000,
    ).enter()


def _stt_manual_finalize_connect(client: Cartesia) -> None:
    client.stt.manual_finalize.websocket(
        encoding="pcm_s16le",
        model="ink-2",
        sample_rate=16_000,
    ).enter()


def _expected_identity(client: Cartesia | AsyncCartesia) -> tuple[str, str]:
    user_agent = client.user_agent
    client_header = client.client_header
    assert client_header.startswith(EXPECTED_CLIENT_HEADER_PREFIX)
    assert client_header.endswith(client._version)
    assert user_agent == client_header
    return user_agent, client_header


@pytest.mark.parametrize(
    "service_name,get_headers",
    [
        ("REST default_headers", _rest_default_headers),
    ],
)
def test_rest_identifies_as_cartesia_python(
    client: Cartesia,
    service_name: str,
    get_headers: Callable[[Cartesia], dict[str, str | Omit]],
) -> None:
    user_agent, client_header = _expected_identity(client)
    headers = get_headers(client)
    assert headers["User-Agent"] == user_agent, service_name
    assert headers["X-Cartesia-Client"] == client_header, service_name


def test_tts_websocket_identifies_as_cartesia_python(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    user_agent, client_header = _expected_identity(client)
    captured = install_sync_connect(monkeypatch, FakeSyncWS)
    client.tts.websocket_connect().enter()
    call = captured["calls"][0]
    assert call["user_agent_header"] == user_agent
    assert call["additional_headers"]["User-Agent"] == user_agent
    assert call["additional_headers"]["X-Cartesia-Client"] == client_header


@pytest.mark.parametrize(
    "service_name,connect",
    [
        ("STT auto-finalize WebSocket", _stt_auto_finalize_connect),
        ("STT manual-finalize WebSocket", _stt_manual_finalize_connect),
    ],
)
def test_stt_websocket_identifies_as_cartesia_python(
    client: Cartesia,
    monkeypatch: pytest.MonkeyPatch,
    service_name: str,
    connect: Callable[[Cartesia], None],
) -> None:
    user_agent, client_header = _expected_identity(client)
    captured = install_sync_connect(monkeypatch, FakeSyncWS)
    connect(client)
    call = captured["calls"][0]
    assert call["user_agent_header"] == user_agent, service_name
    assert call["additional_headers"]["X-Cartesia-Client"] == client_header, service_name


@pytest.mark.asyncio
async def test_async_stt_websocket_identifies_as_cartesia_python(
    async_client: AsyncCartesia,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    user_agent, client_header = _expected_identity(async_client)
    captured = install_async_connect(monkeypatch, FakeAsyncWS)
    await async_client.stt.auto_finalize.websocket(
        encoding="pcm_s16le",
        model="ink-2",
        sample_rate=16_000,
    ).enter()
    call = captured["calls"][0]
    assert call["user_agent_header"] == user_agent
    assert call["additional_headers"]["X-Cartesia-Client"] == client_header
