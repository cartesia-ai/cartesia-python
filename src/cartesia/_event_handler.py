# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import threading
from typing import Any, Callable

EventHandler = Callable[..., Any]


class EventHandlerRegistry:
    """Thread-safe (optional) registry of event handlers."""

    def __init__(self, *, use_lock: bool = False) -> None:
        self._handlers: dict[str, list[tuple[EventHandler, bool]]] = {}
        self._lock: threading.Lock | None = threading.Lock() if use_lock else None

    def _acquire(self) -> None:
        if self._lock is not None:
            self._lock.acquire()

    def _release(self) -> None:
        if self._lock is not None:
            self._lock.release()

    def add(self, event_type: str, handler: EventHandler, *, once: bool = False) -> None:
        self._acquire()
        try:
            self._handlers.setdefault(event_type, []).append((handler, once))
        finally:
            self._release()

    def remove(self, event_type: str, handler: EventHandler) -> None:
        self._acquire()
        try:
            handlers = self._handlers.get(event_type)
            if handlers is not None:
                for i, (registered, _) in enumerate(handlers):
                    if registered == handler:
                        del handlers[i]
                        break
        finally:
            self._release()

    def get_handlers(self, event_type: str) -> list[EventHandler]:
        """Return a snapshot of handlers for the given event type, removing once-handlers."""
        self._acquire()
        try:
            handlers = self._handlers.get(event_type)
            if not handlers:
                return []
            result = [handler for handler, _ in handlers]
            self._handlers[event_type] = [entry for entry in handlers if not entry[1]]
            return result
        finally:
            self._release()

    def has_handlers(self, event_type: str) -> bool:
        self._acquire()
        try:
            return bool(self._handlers.get(event_type))
        finally:
            self._release()

    def merge_into(self, target: EventHandlerRegistry) -> None:
        """Move all handlers from this registry into *target*, then clear self."""
        self._acquire()
        try:
            for event_type, handlers in self._handlers.items():
                for handler, once in handlers:
                    target.add(event_type, handler, once=once)
            self._handlers.clear()
        finally:
            self._release()
