"""In-process runtime event bus.

Events coordinate runtime lifecycle. This bus is intentionally separate from
TelemetryBus.
"""

from __future__ import annotations

from typing import Callable

from .events import RuntimeEvent, RuntimeEventType

RuntimeSubscriber = Callable[[RuntimeEvent], None]


class EventBus:
    def __init__(self) -> None:
        self._events: list[RuntimeEvent] = []
        self._subscribers: list[RuntimeSubscriber] = []

    def subscribe(self, callback: RuntimeSubscriber) -> None:
        self._subscribers.append(callback)

    def publish(
        self,
        event_type: RuntimeEventType,
        execution_id: str,
        source: str,
        payload: dict | None = None,
        *,
        flow_id: str | None = None,
        actor: str | None = None,
    ) -> RuntimeEvent:
        event = RuntimeEvent(
            event_type=event_type,
            execution_id=execution_id,
            source=source,
            flow_id=flow_id,
            actor=actor,
            payload=payload or {},
        )
        self._events.append(event)
        for subscriber in self._subscribers:
            subscriber(event)
        return event

    def history(self, execution_id: str | None = None) -> list[RuntimeEvent]:
        events = self._events if execution_id is None else [e for e in self._events if e.execution_id == execution_id]
        return sorted(events, key=lambda event: event.timestamp)
