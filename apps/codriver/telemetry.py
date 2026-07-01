"""
HWY CoDriver — Telemetry Bus

Telemetry should answer one question: "What actually happened during this
Flow?" It's a publish layer, not a logging call. Legal Logger (and later,
Big Bear) SUBSCRIBE to it — they don't reach into it and Telemetry doesn't
know who's listening. That decoupling is the point: workers, actors, and
Direct Dispatch publish freely without needing to know what consumes it.

Every event also persists to disk so a Timeline can be reconstructed for any
execution_id after the fact, not just while a subscriber happens to be live.
"""

from __future__ import annotations

from typing import Callable
from uuid import uuid4

from .models import TelemetryEvent, TelemetryLayer
from .storage import JSONLStore

Subscriber = Callable[[TelemetryEvent], None]


def new_execution_id() -> str:
    return f"exec-{uuid4().hex[:12]}"


class TelemetryBus:
    def __init__(self, path: str = "telemetry.jsonl"):
        self._store = JSONLStore(path, TelemetryEvent)
        self._subscribers: list[Subscriber] = []

    def subscribe(self, callback: Subscriber) -> None:
        self._subscribers.append(callback)

    def publish(
        self,
        *,
        execution_id: str,
        layer: TelemetryLayer,
        event_type: str,
        source: str,
        runtime_ms: float | None = None,
        payload: dict | None = None,
    ) -> TelemetryEvent:
        event = TelemetryEvent(
            execution_id=execution_id,
            layer=layer,
            event_type=event_type,
            source=source,
            runtime_ms=runtime_ms,
            payload=payload or {},
        )
        self._store.append(event)
        for callback in self._subscribers:
            callback(event)
        return event

    def history(self, execution_id: str) -> list[TelemetryEvent]:
        events = self._store.filter(execution_id=execution_id)
        return sorted(events, key=lambda e: e.timestamp)

    def history_by_layer(self, execution_id: str, layer: TelemetryLayer) -> list[TelemetryEvent]:
        return [e for e in self.history(execution_id) if e.layer == layer]
