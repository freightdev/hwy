"""
HWY CoDriver — the console.

"What needs to happen next, and who should do it?"

v0.1 intent matching is deliberately simple (keyword -> flow_id) so the
ROUTING SHAPE is correct and testable now. Swap `_detect_intent` for a real
classifier/LLM call later — every other layer (Direct Dispatch, registry,
Logbook, truth labels, telemetry) stays the same, which is the point of
building it this way: CoDriver shouldn't need to change when intent
detection gets smarter.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .actors.legal_logger import LegalLogger
from .actors.memory_mark import MemoryMark
from .direct_dispatch import DirectDispatch
from .logbook import LogbookStore
from .models import DryRunEstimate, FlowResult, TelemetryLayer
from .registry import ActorRegistry
from .telemetry import TelemetryBus, new_execution_id
from .timeline import Timeline


@dataclass
class CoDriverSession:
    user_id: str
    session_id: str
    untrusted_content_seen: list[str] = field(default_factory=list)


class CoDriver:
    def __init__(
        self,
        registry: ActorRegistry,
        storage_prefix: str = ".",
        telemetry_bus: TelemetryBus | None = None,
    ):
        self.registry = registry
        self.logbook = LogbookStore(f"{storage_prefix}/logbook.jsonl")
        self.telemetry_bus = telemetry_bus or TelemetryBus(f"{storage_prefix}/telemetry.jsonl")
        self.legal_logger = LegalLogger(
            logbook=self.logbook,
            telemetry_bus=self.telemetry_bus,
            execution_reports_path=f"{storage_prefix}/execution_reports.jsonl",
            flow_reports_path=f"{storage_prefix}/flow_reports.jsonl",
            flow_profiles_path=f"{storage_prefix}/flow_profiles.json",
        )
        self.dispatch = DirectDispatch(registry, self.logbook, self.legal_logger, self.telemetry_bus)
        self.memory_mark = MemoryMark()
        self.timeline = Timeline(self.telemetry_bus)

        # naive keyword router for v0.1 — see docstring
        self._intent_keywords: dict[str, str] = {}

    def teach_intent(self, keyword: str, flow_id: str) -> None:
        self._intent_keywords[keyword.lower()] = flow_id

    def _detect_intent(self, message: str) -> Optional[str]:
        msg = message.lower()
        for keyword, flow_id in self._intent_keywords.items():
            if keyword in msg:
                return flow_id
        return None

    def handle_message(
        self,
        session: CoDriverSession,
        message: str,
        *,
        payload: dict | None = None,
        object_type: str = "general",
        object_id: str | None = None,
        dry_run: bool = False,
    ) -> FlowResult | DryRunEstimate | str:
        execution_id = new_execution_id()
        flow_id = self._detect_intent(message)

        self.telemetry_bus.publish(
            execution_id=execution_id,
            layer=TelemetryLayer.ACTOR,
            event_type="intent_detected",
            source="CoDriver",
            payload={"message": message, "matched_flow": flow_id},
        )

        if flow_id is None:
            return (
                "I'm not sure which actor should handle that yet — CoDriver's "
                "intent routing is v0.1 and only knows the flows it's been "
                "taught. (This is where Quick Quote would normally take over.)"
            )

        object_id = object_id or session.session_id

        if dry_run:
            return self.dispatch.dry_run(flow_id)

        return self.dispatch.execute(
            flow_id,
            payload or {},
            execution_id=execution_id,
            object_type=object_type,
            object_id=object_id,
            user_id=session.user_id,
            session_id=session.session_id,
        )

    def ingest_untrusted(
        self, *, content: str, source_type: str, source_label: str | None = None
    ):
        """Route any external content through Memory Mark before CoDriver
        treats it as anything other than raw text."""
        return self.memory_mark.sanitize(
            content=content, source_type=source_type, source_label=source_label
        )
