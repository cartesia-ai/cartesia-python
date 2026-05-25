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
from cartesia.types.stt.stt_turns_websocket_request import STTTurnsWebsocketRequest

from ._fakes import FakeSyncWS, FakeAsyncWS, install_sync_connect, install_async_connect


def _err_close(code: int = 1006, reason: str = "boom") -> ConnectionClosedError:
    return ConnectionClosedError(rcvd=Close(code=code, reason=reason), sent=None)


# ---------------------------------------------------------------------------
# URL construction
# ---------------------------------------------------------------------------


def test_websocket_url_uses_turns_path(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    captured = install_sync_connect(monkeypatch, FakeSyncWS)
    client.stt.turn_detecting.websocket(
        encoding="pcm_s16le",
        model="ink-2",
        sample_rate=16_000,
    ).enter()

    url = captured["calls"][0]["url"]
    assert url.raw_path.endswith(b"/stt/turns/websocket") or url.path.endswith("/stt/turns/websocket")
    assert dict(url.params) == {
        "encoding": "pcm_s16le",
        "model": "ink-2",
        "sample_rate": "16000",
    }


def test_websocket_url_uses_wss_scheme_for_https_base(monkeypatch: pytest.MonkeyPatch) -> None:
    with Cartesia(base_url="https://example.com/api", token="t", _strict_response_validation=False) as c:
        captured = install_sync_connect(monkeypatch, FakeSyncWS)
        c.stt.turn_detecting.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()
        assert captured["calls"][0]["url"].scheme == "wss"


def test_websocket_url_uses_ws_scheme_for_http_base(monkeypatch: pytest.MonkeyPatch) -> None:
    with Cartesia(base_url="http://example.com/api", token="t", _strict_response_validation=False) as c:
        captured = install_sync_connect(monkeypatch, FakeSyncWS)
        c.stt.turn_detecting.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()
        assert captured["calls"][0]["url"].scheme == "ws"


def test_websocket_url_uses_explicit_websocket_base_url(monkeypatch: pytest.MonkeyPatch) -> None:
    with Cartesia(
        base_url="https://api.example.com",
        websocket_base_url="wss://ws.example.com/v2",
        token="t",
        _strict_response_validation=False,
    ) as c:
        captured = install_sync_connect(monkeypatch, FakeSyncWS)
        c.stt.turn_detecting.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()
        url = captured["calls"][0]["url"]
        assert url.host == "ws.example.com"
        assert url.scheme == "wss"
        assert url.path.endswith("/v2/stt/turns/websocket")


def test_websocket_passes_auth_and_user_agent_headers(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    captured = install_sync_connect(monkeypatch, FakeSyncWS)
    client.stt.turn_detecting.websocket(
        encoding="pcm_s16le",
        model="ink-2",
        sample_rate=16_000,
        extra_headers={"X-Test": "1"},
    ).enter()
    call = captured["calls"][0]
    assert call["user_agent_header"] == client.user_agent
    assert call["additional_headers"]["X-Test"] == "1"
    # auth header from the client should be threaded through
    for key, value in client.auth_headers.items():
        assert call["additional_headers"].get(key) == value


def test_websocket_connection_options_threaded_to_connect(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    captured = install_sync_connect(monkeypatch, FakeSyncWS)
    client.stt.turn_detecting.websocket(
        encoding="pcm_s16le",
        model="ink-2",
        sample_rate=16_000,
        websocket_connection_options={"max_size": 4096},
    ).enter()
    assert captured["calls"][0]["kwargs"].get("max_size") == 4096


async def test_async_websocket_url_uses_turns_path(
    async_client: AsyncCartesia, monkeypatch: pytest.MonkeyPatch
) -> None:
    captured = install_async_connect(monkeypatch, FakeAsyncWS)
    await async_client.stt.turn_detecting.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()
    url = captured["calls"][0]["url"]
    assert url.path.endswith("/stt/turns/websocket")
    assert dict(url.params) == {
        "encoding": "pcm_s16le",
        "model": "ink-2",
        "sample_rate": "16000",
    }


# ---------------------------------------------------------------------------
# Pre-enter buffering on the connection manager
# ---------------------------------------------------------------------------


def test_manager_send_queued_pre_enter_is_flushed_on_enter(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    captured = install_sync_connect(monkeypatch, FakeSyncWS)
    manager = client.stt.turn_detecting.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000)
    manager.send({"type": "close"})
    manager.send(STTTurnsWebsocketRequest(type="close"))
    manager.enter()
    ws: FakeSyncWS = captured["last_ws"]
    assert len(ws.sent) == 2
    for data in ws.sent:
        assert json.loads(data) == {"type": "close"}


def test_manager_on_handlers_transfer_to_connection_on_enter(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    install_sync_connect(monkeypatch, FakeSyncWS)
    manager = client.stt.turn_detecting.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000)

    def _h(event: Any) -> None: ...

    manager.on("turn.start", _h)
    conn = manager.enter()
    assert conn._event_handler_registry.get_handlers("turn.start") == [_h]


def test_manager_on_method_form_returns_self_for_chaining(client: Cartesia) -> None:
    manager = client.stt.turn_detecting.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000)

    def handler(event: Any) -> None: ...

    out = manager.on("turn.start", handler)
    assert out is manager
    assert manager.off("turn.start", handler) is manager


def test_manager_once_decorator_form_returns_fn(client: Cartesia) -> None:
    manager = client.stt.turn_detecting.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000)

    decorator = manager.once("turn.end")
    assert callable(decorator)

    @decorator  # type: ignore[misc]
    def handler(event: Any) -> None: ...

    assert callable(handler)


async def test_async_manager_send_queued_pre_enter_is_flushed_on_enter(
    async_client: AsyncCartesia, monkeypatch: pytest.MonkeyPatch
) -> None:
    captured = install_async_connect(monkeypatch, FakeAsyncWS)
    manager = async_client.stt.turn_detecting.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000)
    manager.send({"type": "close"})
    await manager.enter()
    ws: FakeAsyncWS = captured["last_ws"]
    assert ws.sent == [json.dumps({"type": "close"})]


# ---------------------------------------------------------------------------
# parse_event / recv / recv_bytes
# ---------------------------------------------------------------------------


_CONNECTED_PAYLOAD = json.dumps({"type": "connected", "request_id": "r1"})
_TURN_START_PAYLOAD = json.dumps({"type": "turn.start", "request_id": "r1"})
_TURN_UPDATE_PAYLOAD = json.dumps({"type": "turn.update", "request_id": "r1", "transcript": "hi"})
_TURN_END_PAYLOAD = json.dumps({"type": "turn.end", "request_id": "r1", "transcript": "hi there"})
_ERROR_PAYLOAD = json.dumps({"type": "error", "message": "kaboom"})


def test_parse_event_round_trips_all_turn_event_types(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    install_sync_connect(monkeypatch, FakeSyncWS)
    conn = client.stt.turn_detecting.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()
    assert conn.parse_event(_CONNECTED_PAYLOAD).type == "connected"
    assert conn.parse_event(_TURN_START_PAYLOAD).type == "turn.start"
    update = conn.parse_event(_TURN_UPDATE_PAYLOAD)
    assert update.type == "turn.update" and update.transcript == "hi"  # type: ignore[union-attr]
    end = conn.parse_event(_TURN_END_PAYLOAD)
    assert end.type == "turn.end" and end.transcript == "hi there"  # type: ignore[union-attr]
    err = conn.parse_event(_ERROR_PAYLOAD)
    assert err.type == "error" and err.message == "kaboom"  # type: ignore[union-attr]


def test_recv_and_recv_bytes_pull_from_underlying_ws(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    def factory() -> FakeSyncWS:
        return FakeSyncWS().queue(_CONNECTED_PAYLOAD, _TURN_START_PAYLOAD)

    install_sync_connect(monkeypatch, factory)
    conn = client.stt.turn_detecting.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()
    raw = conn.recv_bytes()
    assert raw == _CONNECTED_PAYLOAD.encode("utf-8")
    event = conn.recv()
    assert event.type == "turn.start"


async def test_async_recv_pulls_from_underlying_ws(
    async_client: AsyncCartesia, monkeypatch: pytest.MonkeyPatch
) -> None:
    def factory() -> FakeAsyncWS:
        return FakeAsyncWS().queue(_TURN_END_PAYLOAD)

    install_async_connect(monkeypatch, factory)
    conn = await async_client.stt.turn_detecting.websocket(
        encoding="pcm_s16le", model="ink-2", sample_rate=16_000
    ).enter()
    event = await conn.recv()
    assert event.type == "turn.end"


# ---------------------------------------------------------------------------
# send / send_raw
# ---------------------------------------------------------------------------


def test_send_serializes_base_model_with_api_names(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    install_sync_connect(monkeypatch, FakeSyncWS)
    manager = client.stt.turn_detecting.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000)
    conn = manager.enter()
    conn.send(STTTurnsWebsocketRequest(type="close"))
    ws: FakeSyncWS = conn._connection  # type: ignore[assignment]
    assert ws.sent == [
        STTTurnsWebsocketRequest(type="close").to_json(use_api_names=True, exclude_defaults=True, exclude_unset=True)
    ]


def test_send_serializes_typed_dict_to_json(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    install_sync_connect(monkeypatch, FakeSyncWS)
    conn = client.stt.turn_detecting.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()
    conn.send({"type": "close"})
    ws: FakeSyncWS = conn._connection  # type: ignore[assignment]
    assert ws.sent == [json.dumps({"type": "close"})]


def test_send_queues_message_when_reconnecting(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    install_sync_connect(monkeypatch, FakeSyncWS)
    conn = client.stt.turn_detecting.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()
    conn._is_reconnecting = True
    conn.send({"type": "close"})
    ws: FakeSyncWS = conn._connection  # type: ignore[assignment]
    assert ws.sent == []  # nothing went out
    assert len(conn._send_queue) == 1


def test_send_requeues_and_reraises_on_failure(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    class BoomWS(FakeSyncWS):
        @override
        def send(self, data: Any) -> None:
            raise RuntimeError("nope")

    install_sync_connect(monkeypatch, BoomWS)
    conn = client.stt.turn_detecting.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()
    with pytest.raises(RuntimeError, match="nope"):
        conn.send({"type": "close"})
    assert len(conn._send_queue) == 1


def test_send_raw_passes_through_when_connected(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    install_sync_connect(monkeypatch, FakeSyncWS)
    conn = client.stt.turn_detecting.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()
    conn.send_raw(b"raw-bytes")
    conn.send_raw("raw-str")
    ws: FakeSyncWS = conn._connection  # type: ignore[assignment]
    assert ws.sent == [b"raw-bytes", "raw-str"]


def test_send_raw_queues_string_form_when_reconnecting(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    install_sync_connect(monkeypatch, FakeSyncWS)
    conn = client.stt.turn_detecting.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()
    conn._is_reconnecting = True
    conn.send_raw(b"raw-bytes")
    assert len(conn._send_queue) == 1
    # drained items are strings even when raw bytes were enqueued
    assert conn._send_queue.drain() == ["raw-bytes"]


async def test_async_send_queues_during_reconnect_and_flushes_on_reconnect_success(
    async_client: AsyncCartesia, monkeypatch: pytest.MonkeyPatch
) -> None:
    first = FakeAsyncWS().queue(_err_close())
    second = FakeAsyncWS().queue(_TURN_END_PAYLOAD)
    factories = iter([first, second])
    install_async_connect(monkeypatch, lambda: next(factories))

    conn = await async_client.stt.turn_detecting.websocket(
        encoding="pcm_s16le",
        model="ink-2",
        sample_rate=16_000,
        on_reconnecting=lambda _evt: None,
        initial_delay=0,
        max_delay=0,
        max_retries=1,
    ).enter()

    # mark reconnecting and queue a message; it must end up on the *new* socket
    conn._is_reconnecting = True
    await conn.send({"type": "close"})
    assert first.sent == []  # first socket never received it
    assert len(conn._send_queue) == 1

    events = [event async for event in conn]
    assert [e.type for e in events] == ["turn.end"]
    assert second.sent == [json.dumps({"type": "close"})]


# ---------------------------------------------------------------------------
# close
# ---------------------------------------------------------------------------


def test_close_marks_intentional_and_passes_through(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    install_sync_connect(monkeypatch, FakeSyncWS)
    conn = client.stt.turn_detecting.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()
    conn.close(code=4242, reason="bye")
    assert conn._intentionally_closed is True
    ws: FakeSyncWS = conn._connection  # type: ignore[assignment]
    assert ws.close_calls == [(4242, "bye")]


def test_manager_context_exit_closes_connection(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    install_sync_connect(monkeypatch, FakeSyncWS)
    with client.stt.turn_detecting.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000) as conn:
        ws: FakeSyncWS = conn._connection  # type: ignore[assignment]
    assert ws.closed is True


async def test_async_manager_context_exit_closes_connection(
    async_client: AsyncCartesia, monkeypatch: pytest.MonkeyPatch
) -> None:
    install_async_connect(monkeypatch, FakeAsyncWS)
    async with async_client.stt.turn_detecting.websocket(
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
        lambda: FakeSyncWS().queue(_CONNECTED_PAYLOAD, _TURN_END_PAYLOAD),
    )
    conn = client.stt.turn_detecting.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()
    events = list(conn)
    assert [e.type for e in events] == ["connected", "turn.end"]


def test_iter_reconnects_on_recoverable_close(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    first = FakeSyncWS().queue(_CONNECTED_PAYLOAD, _err_close(code=1006))
    second = FakeSyncWS().queue(_TURN_END_PAYLOAD)
    factories = iter([first, second])
    install_sync_connect(monkeypatch, lambda: next(factories))

    seen_events: List[Any] = []

    def on_reconnect(event: Any) -> None:
        seen_events.append(event)

    conn = client.stt.turn_detecting.websocket(
        encoding="pcm_s16le",
        model="ink-2",
        sample_rate=16_000,
        on_reconnecting=on_reconnect,
        initial_delay=0,
        max_delay=0,
        max_retries=1,
    ).enter()

    events = list(conn)
    assert [e.type for e in events] == ["connected", "turn.end"]
    assert len(seen_events) == 1
    assert seen_events[0].close_code == 1006
    assert seen_events[0].attempt == 1


def test_iter_raises_websocket_closed_with_unsent_messages_when_reconnect_fails(
    client: Cartesia, monkeypatch: pytest.MonkeyPatch
) -> None:
    # The second connect attempt always fails, exhausting retries
    call_count = {"n": 0}

    def factory() -> FakeSyncWS:
        call_count["n"] += 1
        if call_count["n"] == 1:
            return FakeSyncWS().queue(_err_close(code=1006))
        raise RuntimeError("never reconnects")

    install_sync_connect(monkeypatch, factory)

    manager = client.stt.turn_detecting.websocket(
        encoding="pcm_s16le",
        model="ink-2",
        sample_rate=16_000,
        on_reconnecting=lambda _evt: None,
        initial_delay=0,
        max_delay=0,
        max_retries=2,
    )
    manager.send({"type": "close"})  # queue an unsent message before the connect even happens
    conn = manager.enter()

    # The pre-queued message will be flushed on enter, draining it. Re-queue something
    # by marking the connection as reconnecting before iteration.
    conn._is_reconnecting = True
    conn.send({"type": "close"})

    with pytest.raises(WebSocketConnectionClosedError) as info:
        list(conn)
    assert info.value.unsent_messages == [json.dumps({"type": "close"})]


def test_iter_reraises_when_reconnect_fails_with_empty_queue(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    call_count = {"n": 0}

    def factory() -> FakeSyncWS:
        call_count["n"] += 1
        if call_count["n"] == 1:
            return FakeSyncWS().queue(_err_close(code=1006))
        raise RuntimeError("never reconnects")

    install_sync_connect(monkeypatch, factory)

    conn = client.stt.turn_detecting.websocket(
        encoding="pcm_s16le",
        model="ink-2",
        sample_rate=16_000,
        on_reconnecting=lambda _evt: None,
        initial_delay=0,
        max_delay=0,
        max_retries=1,
    ).enter()

    with pytest.raises(ConnectionClosedError):
        list(conn)


def test_reconnect_returns_false_without_on_reconnecting(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    install_sync_connect(monkeypatch, FakeSyncWS)
    conn = client.stt.turn_detecting.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()
    # The connection manager only forwards `make_ws` when on_reconnecting is set,
    # so without it, _reconnect should bail immediately.
    assert conn._reconnect(_err_close()) is False


def test_reconnect_returns_false_on_non_recoverable_close(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    install_sync_connect(monkeypatch, FakeSyncWS)
    conn = client.stt.turn_detecting.websocket(
        encoding="pcm_s16le",
        model="ink-2",
        sample_rate=16_000,
        on_reconnecting=lambda _evt: None,
    ).enter()
    # 1003 (unsupported data) is not in the recoverable set.
    assert conn._reconnect(_err_close(code=1003)) is False


def test_reconnect_returns_false_when_handler_aborts(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    install_sync_connect(monkeypatch, FakeSyncWS)

    def on_reconnect(_event: Any) -> ReconnectingOverrides:
        return {"abort": True}

    conn = client.stt.turn_detecting.websocket(
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

    conn = client.stt.turn_detecting.websocket(
        encoding="pcm_s16le",
        model="ink-2",
        sample_rate=16_000,
        on_reconnecting=raises,
        initial_delay=0,
        max_delay=0,
    ).enter()
    assert conn._reconnect(_err_close()) is False


def test_reconnect_applies_overrides_from_handler(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    first = FakeSyncWS().queue()  # initial connect; no scripted events needed
    second = FakeSyncWS().queue()
    factories = iter([first, second])
    captured = install_sync_connect(monkeypatch, lambda: next(factories))

    def handler(_evt: Any) -> ReconnectingOverrides:
        return {"extra_query": {"reauth": "1"}, "extra_headers": {"X-New": "yes"}}

    conn = client.stt.turn_detecting.websocket(
        encoding="pcm_s16le",
        model="ink-2",
        sample_rate=16_000,
        on_reconnecting=handler,
        initial_delay=0,
        max_delay=0,
        max_retries=1,
    ).enter()
    assert conn._reconnect(_err_close()) is True
    # second call's URL must include the new query param, and additional_headers
    # must include the new header.
    second_call = captured["calls"][1]
    assert dict(second_call["url"].params).get("reauth") == "1"
    assert second_call["additional_headers"]["X-New"] == "yes"


def test_reconnect_bails_if_intentionally_closed_during_delay(
    client: Cartesia, monkeypatch: pytest.MonkeyPatch
) -> None:
    install_sync_connect(monkeypatch, FakeSyncWS)

    conn = client.stt.turn_detecting.websocket(
        encoding="pcm_s16le",
        model="ink-2",
        sample_rate=16_000,
        on_reconnecting=lambda _evt: None,
        initial_delay=0,
        max_delay=0,
    ).enter()

    import cartesia.resources.stt.turn_detecting as module

    def fake_sleep(_delay: float) -> None:
        conn._intentionally_closed = True

    monkeypatch.setattr(module.time, "sleep", fake_sleep)
    assert conn._reconnect(_err_close()) is False


# ---------------------------------------------------------------------------
# dispatch_events
# ---------------------------------------------------------------------------


def test_dispatch_events_calls_specific_and_generic_handlers(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    install_sync_connect(monkeypatch, lambda: FakeSyncWS().queue(_CONNECTED_PAYLOAD, _TURN_END_PAYLOAD))
    conn = client.stt.turn_detecting.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()
    seen: List[str] = []

    def on_specific(event: Any) -> None:
        seen.append(f"specific:{event.type}")

    def on_generic(event: Any) -> None:
        seen.append(f"generic:{event.type}")

    conn.on("turn.end", on_specific)
    conn.on("event", on_generic)
    conn.dispatch_events()
    # turn.end has a specific handler; both fire. connected only matches generic.
    assert "generic:connected" in seen
    assert "specific:turn.end" in seen
    assert "generic:turn.end" in seen


def test_dispatch_events_raises_cartesia_error_on_unhandled_error_event(
    client: Cartesia, monkeypatch: pytest.MonkeyPatch
) -> None:
    install_sync_connect(monkeypatch, lambda: FakeSyncWS().queue(_ERROR_PAYLOAD))
    conn = client.stt.turn_detecting.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()
    with pytest.raises(CartesiaError):
        conn.dispatch_events()


def test_dispatch_events_does_not_raise_when_error_handler_registered(
    client: Cartesia, monkeypatch: pytest.MonkeyPatch
) -> None:
    install_sync_connect(monkeypatch, lambda: FakeSyncWS().queue(_ERROR_PAYLOAD))
    conn = client.stt.turn_detecting.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()
    seen: List[Any] = []

    def handler(event: Any) -> None:
        seen.append(event)

    conn.on("error", handler)
    conn.dispatch_events()
    assert len(seen) == 1 and seen[0].type == "error"


async def test_async_dispatch_events_awaits_coroutine_handlers(
    async_client: AsyncCartesia, monkeypatch: pytest.MonkeyPatch
) -> None:
    install_async_connect(monkeypatch, lambda: FakeAsyncWS().queue(_TURN_END_PAYLOAD))
    conn = await async_client.stt.turn_detecting.websocket(
        encoding="pcm_s16le", model="ink-2", sample_rate=16_000
    ).enter()
    seen: List[Any] = []

    async def handler(event: Any) -> None:
        seen.append(event)

    conn.on("turn.end", handler)
    await conn.dispatch_events()
    assert [e.type for e in seen] == ["turn.end"]


# ---------------------------------------------------------------------------
# on / off / once on the connection
# ---------------------------------------------------------------------------


def test_connection_on_method_form_returns_self(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    install_sync_connect(monkeypatch, FakeSyncWS)
    conn = client.stt.turn_detecting.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()

    def handler(event: Any) -> None: ...

    out = conn.on("turn.start", handler)
    assert out is conn


def test_connection_on_decorator_form_returns_callable(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    install_sync_connect(monkeypatch, FakeSyncWS)
    conn = client.stt.turn_detecting.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()

    decorator = conn.on("turn.start")
    assert callable(decorator)

    @decorator  # type: ignore[misc]
    def handler(event: Any) -> None: ...

    assert callable(handler)
    assert conn._event_handler_registry.get_handlers("turn.start") == [handler]


def test_connection_once_handler_is_removed_after_first_dispatch(
    client: Cartesia, monkeypatch: pytest.MonkeyPatch
) -> None:
    install_sync_connect(monkeypatch, lambda: FakeSyncWS().queue(_TURN_END_PAYLOAD, _TURN_END_PAYLOAD))
    conn = client.stt.turn_detecting.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()

    seen: List[Any] = []

    def handler(event: Any) -> None:
        seen.append(event)

    conn.once("turn.end", handler)

    conn.dispatch_events()
    # two events arrived; the once-handler fired only once
    assert len(seen) == 1


def test_connection_off_removes_handler(client: Cartesia, monkeypatch: pytest.MonkeyPatch) -> None:
    install_sync_connect(monkeypatch, FakeSyncWS)
    conn = client.stt.turn_detecting.websocket(encoding="pcm_s16le", model="ink-2", sample_rate=16_000).enter()

    def handler(e: Any) -> None: ...

    conn.on("turn.start", handler)
    conn.off("turn.start", handler)
    assert conn._event_handler_registry.get_handlers("turn.start") == []
