"""Runtime timeline built from events."""

from __future__ import annotations

from .event_bus import EventBus
from .events import RuntimeEvent


class RuntimeTimeline:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    def for_execution(self, execution_id: str) -> list[RuntimeEvent]:
        return self.event_bus.history(execution_id)
