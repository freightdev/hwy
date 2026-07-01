"""
HWY CoDriver — Legal Logger (complete)

"Legal Logger writes official reports. CoDriver does not write official Flow
Reports. Actors tell Legal Logger what happened. Legal Logger writes the
record correctly."

Legal Logger owns, exclusively:
    Execution Report -> Flow Report -> Flow Profile -> Telemetry -> Logbook

Nothing else writes these. Direct Dispatch calls `process_execution` exactly
once per flow run and gets back a FlowResult — most of whose fields Legal
Logger generated, not the actor that did the work.

This is also the only place Big Bear will ever query later ("show me the
last 5,000 Packet Pilot Flow Reports") — Big Bear's intelligence isn't built
yet, on purpose, but the evidence it will eventually read from is.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Optional

from ..logbook import LogbookStore
from ..models import (
    ActorContext,
    ActorResponse,
    Claim,
    ExecutionReport,
    FlowProfile,
    FlowReport,
    FlowResult,
    LogbookEntry,
    TelemetryEvent,
    TelemetryLayer,
    TruthLabel,
)
from ..storage import JSONLStore, KeyedJSONStore
from ..telemetry import TelemetryBus

_WORKER_LAYERS = {
    TelemetryLayer.WORKER,
    TelemetryLayer.BROWSER,
    TelemetryLayer.OCR,
    TelemetryLayer.LLM,
    TelemetryLayer.SEARCH,
}


class LegalLogger:
    name = "Legal Logger"

    def __init__(
        self,
        *,
        logbook: LogbookStore,
        telemetry_bus: TelemetryBus,
        execution_reports_path: str = "execution_reports.jsonl",
        flow_reports_path: str = "flow_reports.jsonl",
        flow_profiles_path: str = "flow_profiles.json",
    ):
        self.logbook = logbook
        self.telemetry_bus = telemetry_bus
        self.execution_reports = JSONLStore(execution_reports_path, ExecutionReport)
        self.flow_reports = JSONLStore(flow_reports_path, FlowReport)
        self.flow_profiles = KeyedJSONStore(flow_profiles_path, FlowProfile)

        # Telemetry publishes; Legal Logger subscribes. Events get buffered
        # by execution_id until process_execution() asks for them — Legal
        # Logger never reaches into the bus's storage directly.
        self._telemetry_buffer: dict[str, list[TelemetryEvent]] = defaultdict(list)
        self.telemetry_bus.subscribe(self._on_telemetry)

    def _on_telemetry(self, event: TelemetryEvent) -> None:
        self._telemetry_buffer[event.execution_id].append(event)

    # -- The main entry point: one call per flow execution -----------------

    def process_execution(
        self,
        *,
        execution_id: str,
        flow_id: str,
        object_type: str,
        object_id: str,
        actor_response: ActorResponse,
        context: ActorContext,
        runtime_ms: float,
        estimated_actions: int,
        retries: int = 0,
        recovered: bool = False,
    ) -> FlowResult:

        # Pull this execution's buffered telemetry — the only place Legal
        # Logger reads telemetry from. Worker layers feed actions_used,
        # models_used, cache hits, and extra retries/errors automatically.
        events = self._telemetry_buffer.pop(execution_id, [])
        workers_used = sorted({e.source for e in events if e.layer in _WORKER_LAYERS})
        models_used = sorted(
            {e.payload["model"] for e in events if e.layer == TelemetryLayer.LLM and "model" in e.payload}
        )
        cache_hits = sum(
            1 for e in events if e.layer == TelemetryLayer.LLM and e.payload.get("cache_hit")
        )
        telemetry_retries = sum(
            e.payload.get("retry_count", 0)
            for e in events
            if e.layer in {TelemetryLayer.BROWSER, TelemetryLayer.LLM}
        )
        telemetry_errors = [
            err for e in events for err in e.payload.get("js_errors", [])
        ]

        # 1. Execution Report — raw telemetry, lowest level of record.
        execution_report = ExecutionReport(
            execution_id=execution_id,
            flow_id=flow_id,
            run_id=f"run-{context.session_id or 'no-session'}-{flow_id}",
            actor_chain=[context.actor_id],
            flow_chain=[flow_id],
            actions_used=actor_response.actions_used,
            estimated_actions=estimated_actions,
            runtime_ms=runtime_ms,
            models_used=models_used,
            workers_used=workers_used,
            cache_hits=cache_hits,
            errors=([actor_response.error] if actor_response.error else []) + telemetry_errors,
            retries=retries + telemetry_retries,
            recovered=recovered,
            success=actor_response.success,
            human_review_required=actor_response.requires_human_approval,
        )
        self.execution_reports.append(execution_report)

        # 2. Flow Report — built FROM the Execution Report, not by the actor.
        flow_report = FlowReport(
            flow_id=flow_id,
            execution_id=execution_id,
            execution_report_id=execution_report.id,
            what_happened=self._summarize(actor_response),
            why_it_happened=f"User-initiated flow via session {context.session_id}",
            who_was_involved=[context.actor_id, *workers_used],
            actors_run=[context.actor_id],
            actions_used=actor_response.actions_used,
            what_failed=actor_response.error,
            what_was_learned=self._learning(execution_report),
            recommendation_for_next_run=self._recommendation(execution_report),
        )
        self.flow_reports.append(flow_report)

        self.telemetry_bus.publish(
            execution_id=execution_id,
            layer=TelemetryLayer.FLOW,
            event_type="flow_report_written",
            source=self.name,
            payload={"flow_report_id": flow_report.run_id},
        )

        # 3. Flow Profile — living aggregate, updated incrementally.
        profile = self.flow_profiles.get(flow_id) or FlowProfile(flow_id=flow_id)
        profile.record(execution_report)
        self.flow_profiles.set(flow_id, profile)

        # 4. Approval entry, if needed.
        logbook_refs: list[str] = []
        if actor_response.requires_human_approval:
            approval_entry = self.record_approval_request(
                object_type=object_type,
                object_id=object_id,
                reason=actor_response.approval_reason or "Human approval required.",
                session_id=context.session_id,
            )
            logbook_refs.append(approval_entry.id)

        # 5. Logbook entry — the durable, queryable record of this run.
        logbook_entry = LogbookEntry(
            object_type=object_type,
            object_id=object_id,
            event_type="flow_completed" if actor_response.success else "flow_failed",
            actor=self.name,
            flow_id=flow_id,
            user_id=None,
            session_id=context.session_id,
            summary=flow_report.what_happened,
            evidence=[execution_report.id, flow_report.run_id],
            truth_labels=[
                Claim(text=flow_report.what_happened, label=TruthLabel.LOGBOOK_BACKED, source=self.name)
            ],
            actions_used=actor_response.actions_used,
            status="recorded" if actor_response.success else "failed",
            metadata={
                "execution_id": execution_id,
                "execution_report_id": execution_report.id,
                "flow_report_id": flow_report.run_id,
            },
        )
        self.logbook.append(logbook_entry)
        logbook_refs.append(logbook_entry.id)

        # 6. FlowResult — the unified envelope CoDriver actually sees.
        return FlowResult(
            execution_id=execution_id,
            result=actor_response.raw,
            flow_report_id=flow_report.run_id,
            execution_report_id=execution_report.id,
            logbook_refs=logbook_refs,
            actions_used=actor_response.actions_used,
            estimated_actions=estimated_actions,
            truth_labels=actor_response.claims,
            completed=actor_response.success,
            warnings=[],
            errors=execution_report.errors,
            recommendations=(
                [flow_report.recommendation_for_next_run]
                if flow_report.recommendation_for_next_run
                else []
            ),
        )

    # -- Supporting writes ---------------------------------------------------

    def record_approval_request(
        self, *, object_type: str, object_id: str, reason: str, session_id: str | None
    ) -> LogbookEntry:
        entry = LogbookEntry(
            object_type=object_type,
            object_id=object_id,
            event_type="approval_requested",
            actor=self.name,
            session_id=session_id,
            summary=reason,
            status="pending",
            truth_labels=[Claim(text=reason, label=TruthLabel.USER_PROVIDED, source="CoDriver")],
        )
        self.logbook.append(entry)
        return entry

    # -- Read paths (what Big Bear will eventually call instead of actors) -

    def get_flow_profile(self, flow_id: str) -> Optional[FlowProfile]:
        return self.flow_profiles.get(flow_id)

    def get_flow_reports(self, flow_id: str, limit: int = 50) -> list[FlowReport]:
        return self.flow_reports.latest(n=limit, flow_id=flow_id)

    def get_execution_reports(self, flow_id: str, limit: int = 50) -> list[ExecutionReport]:
        return self.execution_reports.latest(n=limit, flow_id=flow_id)

    # -- Internal helpers -----------------------------------------------------

    @staticmethod
    def _summarize(response: ActorResponse) -> str:
        if not response.success:
            return f"{response.actor} failed: {response.error}"
        if response.claims:
            return response.claims[0].text
        return f"{response.actor} completed {response.flow_id}"

    @staticmethod
    def _learning(execution: ExecutionReport) -> Optional[str]:
        if execution.errors:
            return f"Flow produced {len(execution.errors)} error(s): {'; '.join(execution.errors)}"
        return None

    @staticmethod
    def _recommendation(execution: ExecutionReport) -> Optional[str]:
        if execution.retries > 0:
            return "Flow required retries — investigate root cause before next run."
        if not execution.success:
            return "Flow failed — review Execution Report before retrying."
        return None
