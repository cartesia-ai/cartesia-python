from __future__ import annotations

import json
from typing import Any, List
from typing_extensions import override

import pytest
from websockets.frames import Close
from websockets.exceptions import ConnectionClosedError

from cartesia import Cartesia, AsyncCartesia
from cartesia._exceptions import CartesiaError, WebSocketConnectionClosedError
from cartesia.types.websocket_reconnection import ReconnectingOverrides

from ._fakes import FakeSyncWS, FakeAsyncWS, install_sync_connect, install_async_connect


def _err_close(code: int = 1006, reason: str = "boom") -> ConnectionClosedError:
    return ConnectionClosedError(rcvd=Close(code=code, reason=reason), sent=None)


# ---------------------------------------------------------------------------
# URL construction
# ---------------------------------------------------------------------------


def test_websocket_url_uses_stt_websocket_path(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    captured = install_sync_connect(monkeypatch, FakeSyncWS)
    client.stt.manual_finalize.websocket(
        encoding="pcm_s16le",
        model="ink-2",
        sample_rate=16_000,
    ).enter()

    url = captured["calls"][0]["url"]
    assert url.path.endswith("/stt/websocket")
    assert "turns" not in url.path
    assert dict(url.params) == {
        "encoding": "pcm_s16le",
        "model": "ink-2",
        "sample_rate": "16000",
    }


def test_websocket_url_includes_optional_query_params_when_provided(
    client: Cartesia, monkeypatch: pytest.MonkeyPatch
) -> None:
    captured = install_sync_connect(monkeypatch, FakeSyncWS)
    client.stt.manual_finalize.websocket(
        encoding="pcm_s16le",
        model="ink-2",
        sample_rate=16_000,
        language="en",
        max_silence_duration_secs=0.5,
        min_volume=0.1,
    ).enter()

    params = dict(captured["calls"][0]["url"].params)
    assert params == {
        "encoding": "pcm_s16le",
        "model": "ink-2",
        "sample_rate": "16000",
        "language": "en",
        "max_silence_duration_secs": "0.5",
        "min_volume": "0.1",
    }


def test_websocket_url_omits_optional_query_params_when_absent(
    client: Cartesia, monkeypatch: pytest.MonkeyPatch
) -> None:
    captured = install_sync_connect(monkeypatch, FakeSyncWS)
    client.stt.manual_finalize.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()
    params = dict(captured["calls"][0]["url"].params)
    assert "language" not in params
    assert "max_silence_duration_secs" not in params
    assert "min_volume" not in params


def test_websocket_url_uses_wss_scheme_for_https_base(monkeypatch: pytest.MonkeyPatch) -> None:
    with Cartesia(base_url="https://example.com/api", token="t", _strict_response_validation=False) as c:
        captured = install_sync_connect(monkeypatch, FakeSyncWS)
        c.stt.manual_finalize.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()
        assert captured["calls"][0]["url"].scheme == "wss"


def test_websocket_url_uses_ws_scheme_for_http_base(monkeypatch: pytest.MonkeyPatch) -> None:
    with Cartesia(base_url="http://example.com/api", token="t", _strict_response_validation=False) as c:
        captured = install_sync_connect(monkeypatch, FakeSyncWS)
        c.stt.manual_finalize.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()
        assert captured["calls"][0]["url"].scheme == "ws"


def test_websocket_url_uses_explicit_websocket_base_url(monkeypatch: pytest.MonkeyPatch) -> None:
    with Cartesia(
        base_url="https://api.example.com",
        websocket_base_url="wss://ws.example.com/v2",
        token="t",
        _strict_response_validation=False,
    ) as c:
        captured = install_sync_connect(monkeypatch, FakeSyncWS)
        c.stt.manual_finalize.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()
        url = captured["calls"][0]["url"]
        assert url.host == "ws.example.com"
        assert url.scheme == "wss"
        assert url.path.endswith("/v2/stt/websocket")


def test_websocket_passes_auth_and_user_agent_headers(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    captured = install_sync_connect(monkeypatch, FakeSyncWS)
    client.stt.manual_finalize.websocket(
        encoding="pcm_s16le",
        model="ink-2",
        sample_rate=16_000,
        extra_headers={"X-Test": "1"},
    ).enter()
    call = captured["calls"][0]
    assert call["user_agent_header"] == client.user_agent
    assert call["additional_headers"]["X-Test"] == "1"
    for key, value in client.auth_headers.items():
        assert call["additional_headers"].get(key) == value


def test_websocket_connection_options_threaded_to_connect(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    captured = install_sync_connect(monkeypatch, FakeSyncWS)
    client.stt.manual_finalize.websocket(
        encoding="pcm_s16le",
        model="ink-2",
        sample_rate=16_000,
        websocket_connection_options={"max_size": 4096},
    ).enter()
    assert captured["calls"][0]["kwargs"].get("max_size") == 4096


async def test_async_websocket_url_uses_stt_websocket_path(
    async_client: AsyncCartesia, monkeypatch: pytest.MonkeyPatch
) -> None:
    captured = install_async_connect(monkeypatch, FakeAsyncWS)
    await async_client.stt.manual_finalize.websocket(
        encoding="pcm_s16le",
        model="ink-2",
        sample_rate=16_000,
        language="en",
    ).enter()
    url = captured["calls"][0]["url"]
    assert url.path.endswith("/stt/websocket")
    assert dict(url.params)["language"] == "en"


# ---------------------------------------------------------------------------
# Pre-enter buffering on the connection manager
# ---------------------------------------------------------------------------


def test_manager_send_queued_pre_enter_is_flushed_on_enter(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    captured = install_sync_connect(monkeypatch, FakeSyncWS)
    manager = client.stt.manual_finalize.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000)
    manager.send("finalize")
    manager.send("close")
    manager.enter()
    ws: FakeSyncWS = captured["last_ws"]
    # raw strings are sent as-is; no JSON wrapping happens for manual commands
    assert ws.sent == ["finalize", "close"]


def test_manager_on_handlers_transfer_to_connection_on_enter(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    install_sync_connect(monkeypatch, FakeSyncWS)
    manager = client.stt.manual_finalize.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000)

    def handler(event: Any) -> None: ...

    manager.on("transcript", handler)
    conn = manager.enter()
    assert conn._event_handler_registry.get_handlers("transcript") == [handler]


def test_manager_on_method_form_returns_self_for_chaining(client: Cartesia) -> None:
    manager = client.stt.manual_finalize.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000)

    def handler(event: Any) -> None: ...

    out = manager.on("transcript", handler)
    assert out is manager
    assert manager.off("transcript", handler) is manager


def test_manager_once_decorator_form_returns_fn(client: Cartesia) -> None:
    manager = client.stt.manual_finalize.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000)

    decorator = manager.once("done")
    assert callable(decorator)

    @decorator  # type: ignore[misc]
    def handler(event: Any) -> None: ...

    assert callable(handler)


async def test_async_manager_send_queued_pre_enter_is_flushed_on_enter(
    async_client: AsyncCartesia, monkeypatch: pytest.MonkeyPatch
) -> None:
    captured = install_async_connect(monkeypatch, FakeAsyncWS)
    manager = async_client.stt.manual_finalize.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000)
    manager.send("finalize")
    await manager.enter()
    ws: FakeAsyncWS = captured["last_ws"]
    assert ws.sent == ["finalize"]


# ---------------------------------------------------------------------------
# parse_event / recv / recv_bytes
# ---------------------------------------------------------------------------


_TRANSCRIPT_PAYLOAD = json.dumps({"type": "transcript", "request_id": "r1", "text": "hello ", "is_final": True})
_FLUSH_DONE_PAYLOAD = json.dumps({"type": "flush_done", "request_id": "r1"})
_DONE_PAYLOAD = json.dumps({"type": "done", "request_id": "r1"})
_ERROR_PAYLOAD = json.dumps({"type": "error", "message": "kaboom"})


def test_parse_event_round_trips_all_manual_finalize_event_types(
    client: Cartesia, monkeypatch: pytest.MonkeyPatch
) -> None:
    install_sync_connect(monkeypatch, FakeSyncWS)
    conn = client.stt.manual_finalize.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()
    tr = conn.parse_event(_TRANSCRIPT_PAYLOAD)
    assert tr.type == "transcript" and tr.text == "hello "  # type: ignore[union-attr]
    assert tr.is_final is True  # type: ignore[union-attr]
    assert conn.parse_event(_FLUSH_DONE_PAYLOAD).type == "flush_done"
    assert conn.parse_event(_DONE_PAYLOAD).type == "done"
    err = conn.parse_event(_ERROR_PAYLOAD)
    assert err.type == "error" and err.message == "kaboom"  # type: ignore[union-attr]


def test_recv_and_recv_bytes_pull_from_underlying_ws(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    install_sync_connect(monkeypatch, lambda: FakeSyncWS().queue(_TRANSCRIPT_PAYLOAD, _DONE_PAYLOAD))
    conn = client.stt.manual_finalize.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()
    raw = conn.recv_bytes()
    assert raw == _TRANSCRIPT_PAYLOAD.encode("utf-8")
    event = conn.recv()
    assert event.type == "done"


async def test_async_recv_pulls_from_underlying_ws(
    async_client: AsyncCartesia, monkeypatch: pytest.MonkeyPatch
) -> None:
    install_async_connect(monkeypatch, lambda: FakeAsyncWS().queue(_DONE_PAYLOAD))
    conn = await async_client.stt.manual_finalize.websocket(
        encoding="pcm_s16le", model="ink-2", sample_rate=16_000
    ).enter()
    event = await conn.recv()
    assert event.type == "done"


# ---------------------------------------------------------------------------
# send / send_raw
# ---------------------------------------------------------------------------


def test_send_passes_literal_string_through_to_ws(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    install_sync_connect(monkeypatch, FakeSyncWS)
    conn = client.stt.manual_finalize.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()
    conn.send("finalize")
    conn.send("close")
    ws: FakeSyncWS = conn._connection  # type: ignore[assignment]
    assert ws.sent == ["finalize", "close"]


def test_send_queues_message_when_reconnecting(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    install_sync_connect(monkeypatch, FakeSyncWS)
    conn = client.stt.manual_finalize.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()
    conn._is_reconnecting = True
    conn.send("finalize")
    ws: FakeSyncWS = conn._connection  # type: ignore[assignment]
    assert ws.sent == []
    assert conn._send_queue.drain() == ["finalize"]


def test_send_requeues_and_reraises_on_failure(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    class BoomWS(FakeSyncWS):
        @override
        def send(self, data: Any) -> None:
            raise RuntimeError("nope")

    install_sync_connect(monkeypatch, BoomWS)
    conn = client.stt.manual_finalize.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()
    with pytest.raises(RuntimeError, match="nope"):
        conn.send("finalize")
    assert conn._send_queue.drain() == ["finalize"]


def test_send_raw_passes_through_when_connected(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    install_sync_connect(monkeypatch, FakeSyncWS)
    conn = client.stt.manual_finalize.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()
    conn.send_raw(b"\x00\x01\x02")  # simulated audio frame
    conn.send_raw("finalize")
    ws: FakeSyncWS = conn._connection  # type: ignore[assignment]
    assert ws.sent == [b"\x00\x01\x02", "finalize"]


def test_send_raw_queues_string_form_when_reconnecting(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    install_sync_connect(monkeypatch, FakeSyncWS)
    conn = client.stt.manual_finalize.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()
    conn._is_reconnecting = True
    conn.send_raw(b"raw-bytes")
    assert conn._send_queue.drain() == ["raw-bytes"]


async def test_async_send_queues_during_reconnect_and_flushes_on_reconnect_success(
    async_client: AsyncCartesia, monkeypatch: pytest.MonkeyPatch
) -> None:
    first = FakeAsyncWS().queue(_err_close())
    second = FakeAsyncWS().queue(_DONE_PAYLOAD)
    factories = iter([first, second])
    install_async_connect(monkeypatch, lambda: next(factories))

    def on_reconnect(event: Any) -> None: ...

    conn = await async_client.stt.manual_finalize.websocket(
        encoding="pcm_s16le",
        model="ink-2",
        sample_rate=16_000,
        on_reconnecting=on_reconnect,
        initial_delay=0,
        max_delay=0,
        max_retries=1,
    ).enter()

    conn._is_reconnecting = True
    await conn.send("finalize")
    assert first.sent == []
    assert len(conn._send_queue) == 1

    events = [event async for event in conn]
    assert [e.type for e in events] == ["done"]
    assert second.sent == ["finalize"]


# ---------------------------------------------------------------------------
# close
# ---------------------------------------------------------------------------


def test_close_marks_intentional_and_passes_through(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    install_sync_connect(monkeypatch, FakeSyncWS)
    conn = client.stt.manual_finalize.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()
    conn.close(code=4242, reason="bye")
    assert conn._intentionally_closed is True
    ws: FakeSyncWS = conn._connection  # type: ignore[assignment]
    assert ws.close_calls == [(4242, "bye")]


def test_manager_context_exit_closes_connection(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    install_sync_connect(monkeypatch, FakeSyncWS)
    with client.stt.manual_finalize.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000) as conn:
        ws: FakeSyncWS = conn._connection  # type: ignore[assignment]
    assert ws.closed is True


async def test_async_manager_context_exit_closes_connection(
    async_client: AsyncCartesia, monkeypatch: pytest.MonkeyPatch
) -> None:
    install_async_connect(monkeypatch, FakeAsyncWS)
    async with async_client.stt.manual_finalize.websocket(
        encoding="pcm_s16le", model="ink-2", sample_rate=16_000
    ) as conn:
        ws: FakeAsyncWS = conn._connection  # type: ignore[assignment]
    assert ws.closed is True


# ---------------------------------------------------------------------------
# Iteration & reconnection
# ---------------------------------------------------------------------------


def test_iter_yields_events_until_clean_close(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    install_sync_connect(
        monkeypatch,
        lambda: FakeSyncWS().queue(_TRANSCRIPT_PAYLOAD, _FLUSH_DONE_PAYLOAD, _DONE_PAYLOAD),
    )
    conn = client.stt.manual_finalize.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()
    events = list(conn)
    assert [e.type for e in events] == ["transcript", "flush_done", "done"]


def test_iter_reconnects_on_recoverable_close(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    first = FakeSyncWS().queue(_TRANSCRIPT_PAYLOAD, _err_close(code=1006))
    second = FakeSyncWS().queue(_DONE_PAYLOAD)
    factories = iter([first, second])
    install_sync_connect(monkeypatch, lambda: next(factories))

    seen_events: List[Any] = []

    def on_reconnect(event: Any) -> None:
        seen_events.append(event)

    conn = client.stt.manual_finalize.websocket(
        encoding="pcm_s16le",
        model="ink-2",
        sample_rate=16_000,
        on_reconnecting=on_reconnect,
        initial_delay=0,
        max_delay=0,
        max_retries=1,
    ).enter()

    events = list(conn)
    assert [e.type for e in events] == ["transcript", "done"]
    assert len(seen_events) == 1
    assert seen_events[0].close_code == 1006


def test_iter_raises_websocket_closed_with_unsent_messages_when_reconnect_fails(
    client: Cartesia, monkeypatch: pytest.MonkeyPatch
) -> None:
    call_count = {"n": 0}

    def factory() -> FakeSyncWS:
        call_count["n"] += 1
        if call_count["n"] == 1:
            return FakeSyncWS().queue(_err_close(code=1006))
        raise RuntimeError("never reconnects")

    install_sync_connect(monkeypatch, factory)

    def on_reconnect(event: Any) -> None: ...

    conn = client.stt.manual_finalize.websocket(
        encoding="pcm_s16le",
        model="ink-2",
        sample_rate=16_000,
        on_reconnecting=on_reconnect,
        initial_delay=0,
        max_delay=0,
        max_retries=2,
    ).enter()

    conn._is_reconnecting = True
    conn.send("finalize")

    with pytest.raises(WebSocketConnectionClosedError) as info:
        list(conn)
    assert info.value.unsent_messages == ["finalize"]


def test_iter_reraises_when_reconnect_fails_with_empty_queue(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    call_count = {"n": 0}

    def factory() -> FakeSyncWS:
        call_count["n"] += 1
        if call_count["n"] == 1:
            return FakeSyncWS().queue(_err_close(code=1006))
        raise RuntimeError("never reconnects")

    install_sync_connect(monkeypatch, factory)

    def on_reconnect(event: Any) -> None: ...

    conn = client.stt.manual_finalize.websocket(
        encoding="pcm_s16le",
        model="ink-2",
        sample_rate=16_000,
        on_reconnecting=on_reconnect,
        initial_delay=0,
        max_delay=0,
        max_retries=1,
    ).enter()

    with pytest.raises(ConnectionClosedError):
        list(conn)


def test_reconnect_returns_false_without_on_reconnecting(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    install_sync_connect(monkeypatch, FakeSyncWS)
    conn = client.stt.manual_finalize.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()
    assert conn._reconnect(_err_close()) is False


def test_reconnect_returns_false_on_non_recoverable_close(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    install_sync_connect(monkeypatch, FakeSyncWS)

    def on_reconnect(event: Any) -> None: ...

    conn = client.stt.manual_finalize.websocket(
        encoding="pcm_s16le",
        model="ink-2",
        sample_rate=16_000,
        on_reconnecting=on_reconnect,
    ).enter()
    assert conn._reconnect(_err_close(code=1003)) is False


def test_reconnect_returns_false_when_handler_aborts(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    install_sync_connect(monkeypatch, FakeSyncWS)

    def on_reconnect(_event: Any) -> ReconnectingOverrides:
        return {"abort": True}

    conn = client.stt.manual_finalize.websocket(
        encoding="pcm_s16le",
        model="ink-2",
        sample_rate=16_000,
        on_reconnecting=on_reconnect,
        initial_delay=0,
        max_delay=0,
    ).enter()
    assert conn._reconnect(_err_close()) is False


def test_reconnect_returns_false_when_handler_raises(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    install_sync_connect(monkeypatch, FakeSyncWS)

    def raises(_evt: Any) -> None:
        raise ValueError("user code blew up")

    conn = client.stt.manual_finalize.websocket(
        encoding="pcm_s16le",
        model="ink-2",
        sample_rate=16_000,
        on_reconnecting=raises,
        initial_delay=0,
        max_delay=0,
    ).enter()
    assert conn._reconnect(_err_close()) is False


def test_reconnect_applies_overrides_from_handler(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    first = FakeSyncWS().queue()
    second = FakeSyncWS().queue()
    factories = iter([first, second])
    captured = install_sync_connect(monkeypatch, lambda: next(factories))

    def handler(_evt: Any) -> ReconnectingOverrides:
        return {"extra_query": {"reauth": "1"}, "extra_headers": {"X-New": "yes"}}

    conn = client.stt.manual_finalize.websocket(
        encoding="pcm_s16le",
        model="ink-2",
        sample_rate=16_000,
        on_reconnecting=handler,
        initial_delay=0,
        max_delay=0,
        max_retries=1,
    ).enter()
    assert conn._reconnect(_err_close()) is True
    second_call = captured["calls"][1]
    assert dict(second_call["url"].params).get("reauth") == "1"
    assert second_call["additional_headers"]["X-New"] == "yes"


def test_reconnect_bails_if_intentionally_closed_during_delay(
    client: Cartesia, monkeypatch: pytest.MonkeyPatch
) -> None:
    install_sync_connect(monkeypatch, FakeSyncWS)

    def on_reconnect(event: Any) -> None: ...

    conn = client.stt.manual_finalize.websocket(
        encoding="pcm_s16le",
        model="ink-2",
        sample_rate=16_000,
        on_reconnecting=on_reconnect,
        initial_delay=0,
        max_delay=0,
    ).enter()

    import cartesia.resources.stt.manual_finalize as module

    def fake_sleep(_delay: float) -> None:
        conn._intentionally_closed = True

    monkeypatch.setattr(module.time, "sleep", fake_sleep)
    assert conn._reconnect(_err_close()) is False


# ---------------------------------------------------------------------------
# dispatch_events
# ---------------------------------------------------------------------------


def test_dispatch_events_calls_specific_and_generic_handlers(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    install_sync_connect(monkeypatch, lambda: FakeSyncWS().queue(_TRANSCRIPT_PAYLOAD, _DONE_PAYLOAD))
    conn = client.stt.manual_finalize.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()
    seen: List[str] = []

    def on_specific(event: Any) -> None:
        seen.append(f"specific:{event.type}")

    def on_generic(event: Any) -> None:
        seen.append(f"generic:{event.type}")

    conn.on("done", on_specific)
    conn.on("event", on_generic)
    conn.dispatch_events()
    assert "generic:transcript" in seen
    assert "specific:done" in seen
    assert "generic:done" in seen


def test_dispatch_events_raises_cartesia_error_on_unhandled_error_event(
    client: Cartesia, monkeypatch: pytest.MonkeyPatch
) -> None:
    install_sync_connect(monkeypatch, lambda: FakeSyncWS().queue(_ERROR_PAYLOAD))
    conn = client.stt.manual_finalize.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()
    with pytest.raises(CartesiaError):
        conn.dispatch_events()


def test_dispatch_events_does_not_raise_when_error_handler_registered(
    client: Cartesia, monkeypatch: pytest.MonkeyPatch
) -> None:
    install_sync_connect(monkeypatch, lambda: FakeSyncWS().queue(_ERROR_PAYLOAD))
    conn = client.stt.manual_finalize.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()
    seen: List[Any] = []

    def handler(event: Any) -> None:
        seen.append(event)

    conn.on("error", handler)
    conn.dispatch_events()
    assert len(seen) == 1 and seen[0].type == "error"


async def test_async_dispatch_events_awaits_coroutine_handlers(
    async_client: AsyncCartesia, monkeypatch: pytest.MonkeyPatch
) -> None:
    install_async_connect(monkeypatch, lambda: FakeAsyncWS().queue(_TRANSCRIPT_PAYLOAD))
    conn = await async_client.stt.manual_finalize.websocket(
        encoding="pcm_s16le", model="ink-2", sample_rate=16_000
    ).enter()
    seen: List[Any] = []

    async def handler(event: Any) -> None:
        seen.append(event)

    conn.on("transcript", handler)
    await conn.dispatch_events()
    assert [e.type for e in seen] == ["transcript"]


# ---------------------------------------------------------------------------
# on / off / once on the connection
# ---------------------------------------------------------------------------


def test_connection_on_method_form_returns_self(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    install_sync_connect(monkeypatch, FakeSyncWS)
    conn = client.stt.manual_finalize.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()

    def handler(event: Any) -> None: ...

    out = conn.on("transcript", handler)
    assert out is conn


def test_connection_on_decorator_form_returns_callable(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    install_sync_connect(monkeypatch, FakeSyncWS)
    conn = client.stt.manual_finalize.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()

    decorator = conn.on("transcript")
    assert callable(decorator)

    @decorator  # type: ignore[misc]
    def handler(event: Any) -> None: ...

    assert callable(handler)
    assert conn._event_handler_registry.get_handlers("transcript") == [handler]


def test_connection_once_handler_is_removed_after_first_dispatch(
    client: Cartesia, monkeypatch: pytest.MonkeyPatch
) -> None:
    install_sync_connect(monkeypatch, lambda: FakeSyncWS().queue(_TRANSCRIPT_PAYLOAD, _TRANSCRIPT_PAYLOAD))
    conn = client.stt.manual_finalize.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()

    seen: List[Any] = []

    def handler(event: Any) -> None:
        seen.append(event)

    conn.once("transcript", handler)
    conn.dispatch_events()
    assert len(seen) == 1


def test_connection_off_removes_handler(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    install_sync_connect(monkeypatch, FakeSyncWS)
    conn = client.stt.manual_finalize.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()

    def handler(event: Any) -> None: ...

    conn.on("transcript", handler)
    conn.off("transcript", handler)
    assert conn._event_handler_registry.get_handlers("transcript") == []
