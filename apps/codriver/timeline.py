"""
HWY CoDriver — Timeline

Not logs. A reconstructed chain of what happened, in order, for one
execution_id — built entirely from TelemetryEvents the bus already
persisted. This is read-only and stateless on purpose: anything that
publishes telemetry shows up here automatically, with no Timeline-specific
instrumentation required.
"""

from __future__ import annotations

from .models import TelemetryEvent, TimelineEntry
from .telemetry import TelemetryBus

# Friendly labels for common event types — falls back to the raw event_type
# string for anything not in this table, so new telemetry never breaks it.
_EVENT_LABELS: dict[str, str] = {
    "intent_detected": "Intent Detected",
    "actor_selected": "Actor Selected",
    "flow_started": "Flow Started",
    "actor_entered": "Started",
    "browser_navigation": "Opened Portal",
    "ocr_completed": "OCR Completed",
    "llm_call": "LLM Call",
    "actor_exited": "Finished",
    "flow_finished": "Flow Completed",
    "flow_report_written": "Flow Report Written",
}


class Timeline:
    def __init__(self, bus: TelemetryBus):
        self.bus = bus

    def build(self, execution_id: str) -> list[TimelineEntry]:
        events = self.bus.history(execution_id)
        return [self._to_entry(e) for e in events]

    @staticmethod
    def _to_entry(event: TelemetryEvent) -> TimelineEntry:
        label = _EVENT_LABELS.get(event.event_type, event.event_type)
        detail = None
        if event.runtime_ms is not None:
            detail = f"{event.runtime_ms:.1f}ms"
        elif event.payload:
            # Show the single most informative field if present
            for key in ("summary", "carrier_name", "model", "pages", "selector_failures"):
                if key in event.payload:
                    detail = f"{key}={event.payload[key]}"
                    break
        return TimelineEntry(timestamp=event.timestamp, source=event.source, event=label, detail=detail)

    def render(self, execution_id: str) -> str:
        entries = self.build(execution_id)
        lines: list[str] = []
        for entry in entries:
            ts = entry.timestamp.strftime("%H:%M:%S.%f")[:-3]
            lines.append(ts)
            lines.append(entry.source)
            lines.append(entry.event + (f"  ({entry.detail})" if entry.detail else ""))
            lines.append("─" * 12)
        if lines:
            lines.pop()  # drop trailing separator
        return "\n".join(lines)
