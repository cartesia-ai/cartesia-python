"""Assert cartesia-python identifies itself on every outbound API surface."""

from __future__ import annotations

import pytest

from cartesia import Cartesia, AsyncCartesia

from .resources.stt._fakes import FakeSyncWS, FakeAsyncWS, install_sync_connect, install_async_connect

EXPECTED_USER_AGENT_PREFIX = "Cartesia/Python "
EXPECTED_CLIENT_HEADER_PREFIX = "cartesia-python/"


def _expected_identity(client: Cartesia | AsyncCartesia) -> tuple[str, str]:
    user_agent = client.user_agent
    client_header = client.client_header
    assert user_agent.startswith(EXPECTED_USER_AGENT_PREFIX)
    assert client_header.startswith(EXPECTED_CLIENT_HEADER_PREFIX)
    assert user_agent.endswith(client._version)
    assert client_header.endswith(client._version)
    return user_agent, client_header


@pytest.mark.parametrize(
    "service_name,get_headers",
    [
        ("REST default_headers", lambda client: client.default_headers),
    ],
)
def test_rest_identifies_as_cartesia_python(
    client: Cartesia,
    service_name: str,
    get_headers,
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
        (
            "STT auto-finalize WebSocket",
            lambda client: client.stt.auto_finalize.websocket(
                encoding="pcm_s16le",
                model="ink-2",
                sample_rate=16_000,
            ).enter(),
        ),
        (
            "STT manual-finalize WebSocket",
            lambda client: client.stt.manual_finalize.websocket(
                encoding="pcm_s16le",
                model="ink-2",
                sample_rate=16_000,
            ).enter(),
        ),
    ],
)
def test_stt_websocket_identifies_as_cartesia_python(
    client: Cartesia,
    monkeypatch: pytest.MonkeyPatch,
    service_name: str,
    connect,
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
