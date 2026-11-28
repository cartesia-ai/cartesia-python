from __future__ import annotations

from cartesia._event_handler import EventHandlerRegistry


def handler(event: object) -> object:
    return event


def test_once_registration_does_not_remove_persistent_handler_on_another_event() -> None:
    registry = EventHandlerRegistry()

    registry.add("error", handler)
    registry.add("transcript", handler, once=True)

    registry.get_handlers("error")
    assert registry.get_handlers("error") == [handler]


def test_once_registration_is_tracked_per_event() -> None:
    registry = EventHandlerRegistry()

    registry.add("transcript", handler, once=True)
    registry.add("final", handler, once=True)

    registry.get_handlers("transcript")
    registry.get_handlers("final")
    assert not registry.has_handlers("final")


def test_persistent_and_once_registration_of_same_handler_on_same_event() -> None:
    registry = EventHandlerRegistry()

    registry.add("event", handler)
    registry.add("event", handler, once=True)

    assert len(registry.get_handlers("event")) == 2
    assert registry.get_handlers("event") == [handler]
