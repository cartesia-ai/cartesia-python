from __future__ import annotations

from typing import Any, Dict, List, Tuple, Union, Callable
from collections import deque

import httpx
import pytest
from websockets.exceptions import ConnectionClosedOK

RecvItem = Union[bytes, str, BaseException]


class FakeSyncWS:
    """Duck-typed stand-in for websockets.sync.client.ClientConnection."""

    def __init__(self) -> None:
        self.sent: List[Any] = []
        self.closed: bool = False
        self.close_calls: List[Tuple[int, str]] = []
        self._script: "deque[RecvItem]" = deque()

    def queue(self, *items: RecvItem) -> "FakeSyncWS":
        self._script.extend(items)
        return self

    def recv(self, decode: bool = True) -> Any:
        if not self._script:
            raise ConnectionClosedOK(rcvd=None, sent=None)
        item = self._script.popleft()
        if isinstance(item, BaseException):
            raise item
        if isinstance(item, str) and decode is False:
            return item.encode("utf-8")
        return item

    def send(self, data: Any) -> None:
        self.sent.append(data)

    def close(self, *, code: int = 1000, reason: str = "") -> None:
        self.closed = True
        self.close_calls.append((code, reason))


class FakeAsyncWS:
    """Duck-typed stand-in for websockets.asyncio.client.ClientConnection."""

    def __init__(self) -> None:
        self.sent: List[Any] = []
        self.closed: bool = False
        self.close_calls: List[Tuple[int, str]] = []
        self._script: "deque[RecvItem]" = deque()

    def queue(self, *items: RecvItem) -> "FakeAsyncWS":
        self._script.extend(items)
        return self

    async def recv(self, decode: bool = True) -> Any:
        if not self._script:
            raise ConnectionClosedOK(rcvd=None, sent=None)
        item = self._script.popleft()
        if isinstance(item, BaseException):
            raise item
        if isinstance(item, str) and decode is False:
            return item.encode("utf-8")
        return item

    async def send(self, data: Any) -> None:
        self.sent.append(data)

    async def close(self, *, code: int = 1000, reason: str = "") -> None:
        self.closed = True
        self.close_calls.append((code, reason))


def install_sync_connect(monkeypatch: pytest.MonkeyPatch, ws_factory: Callable[[], FakeSyncWS]) -> Dict[str, Any]:
    """Patch ``websockets.sync.client.connect`` to return WS objects from ``ws_factory``.

    Returns a dict that accumulates per-call metadata under ``"calls"`` and
    the most recent ws under ``"last_ws"``.
    """
    captured: Dict[str, Any] = {"calls": [], "last_ws": None}

    def fake_connect(
        uri: str,
        *args: Any,
        additional_headers: Any = None,
        user_agent_header: Any = None,
        **kwargs: Any,
    ) -> FakeSyncWS:
        ws = ws_factory()
        captured["calls"].append(
            {
                "url": httpx.URL(uri),
                "additional_headers": dict(additional_headers) if additional_headers else None,
                "user_agent_header": user_agent_header,
                "args": args,
                "kwargs": kwargs,
            }
        )
        captured["last_ws"] = ws
        return ws

    monkeypatch.setattr("websockets.sync.client.connect", fake_connect)
    return captured


def install_async_connect(monkeypatch: pytest.MonkeyPatch, ws_factory: Callable[[], FakeAsyncWS]) -> Dict[str, Any]:
    """Async variant of :func:`install_sync_connect`."""
    captured: Dict[str, Any] = {"calls": [], "last_ws": None}

    async def fake_connect(
        uri: str,
        *args: Any,
        additional_headers: Any = None,
        user_agent_header: Any = None,
        **kwargs: Any,
    ) -> FakeAsyncWS:
        ws = ws_factory()
        captured["calls"].append(
            {
                "url": httpx.URL(uri),
                "additional_headers": dict(additional_headers) if additional_headers else None,
                "user_agent_header": user_agent_header,
                "args": args,
                "kwargs": kwargs,
            }
        )
        captured["last_ws"] = ws
        return ws

    monkeypatch.setattr("websockets.asyncio.client.connect", fake_connect)
    return captured
