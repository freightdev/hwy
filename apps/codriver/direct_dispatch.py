"""
HWY CoDriver — Direct Dispatch

"CoDriver decides what needs to happen. Direct Dispatch decides who should
do it." Registry-driven router: intent -> actor -> flow -> required
permissions -> expected outputs.

Direct Dispatch builds the ActorContext every actor receives, publishes
flow telemetry around the call, and routes actor invocation through
ActorRuntime. Direct Dispatch never writes a report itself — Legal Logger owns
official reports. Events coordinate runtime lifecycle; telemetry measures work.
"""

from __future__ import annotations

import time

from .actors.legal_logger import LegalLogger
from .logbook import LogbookStore
from .models import (
    ActorContext,
    DryRunEstimate,
    FlowResult,
    HUMAN_APPROVAL_REQUIRED,
    TelemetryLayer,
)
from .registry import ActorRegistry
from .runtime.actor_runtime import ActorRuntime
from .runtime.event_bus import EventBus
from .runtime.events import RuntimeEventType
from .runtime.execution import ExecutionRuntime
from .telemetry import TelemetryBus, new_execution_id


class DirectDispatch:
    def __init__(
        self,
        registry: ActorRegistry,
        logbook: LogbookStore,
        legal_logger: LegalLogger,
        telemetry_bus: TelemetryBus,
        event_bus: EventBus | None = None,
        execution_runtime: ExecutionRuntime | None = None,
        actor_runtime: ActorRuntime | None = None,
    ):
        self.registry = registry
        self.logbook = logbook
        self.legal_logger = legal_logger
        self.telemetry_bus = telemetry_bus
        self.event_bus = event_bus or EventBus()
        self.execution_runtime = execution_runtime or ExecutionRuntime(self.event_bus)
        self.actor_runtime = actor_runtime or ActorRuntime(registry=registry, event_bus=self.event_bus)

    # -- Dry run -------------------------------------------------------------

    def dry_run(self, flow_id: str) -> DryRunEstimate:
        flow = self.registry.flow(flow_id)
        owner = self.registry.manifest(flow.owner_actor)

        human_review = owner.requires_human_review or any(
            p in HUMAN_APPROVAL_REQUIRED for p in flow.required_permissions
        )

        profile = self.legal_logger.get_flow_profile(flow_id)
        estimated_actions = (
            round(profile.avg_actions) if profile and profile.total_runs > 0 else flow.estimated_actions
        )
        estimated_time = (
            int(profile.avg_runtime_ms / 1000) if profile and profile.total_runs > 0 else None
        )

        return DryRunEstimate(
            flow_id=flow_id,
            planned_actors=[flow.owner_actor, *flow.required_workers],
            planned_flows=[flow_id],
            estimated_actions=estimated_actions,
            estimated_time_seconds=estimated_time,
            required_data=flow.inputs,
            required_permissions=flow.required_permissions,
            human_review_required=human_review,
            possible_failure_points=[flow.failure_behavior],
        )

    # -- Execute -------------------------------------------------------------

    def execute(
        self,
        flow_id: str,
        payload: dict,
        *,
        object_type: str,
        object_id: str,
        execution_id: str | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
        load_id: str | None = None,
        driver_id: str | None = None,
        company_id: str | None = None,
    ) -> FlowResult:
        flow = self.registry.flow(flow_id)
        owner_name = flow.owner_actor

        execution_id = execution_id or new_execution_id()
        execution = self.execution_runtime.start(flow_id=flow_id, execution_id=execution_id)
        execution_id = execution.execution_id

        context = ActorContext(
            actor_id=owner_name,
            execution_id=execution_id,
            session_id=session_id,
            load_id=load_id,
            driver_id=driver_id,
            company_id=company_id,
            current_flow=flow_id,
            current_permissions=flow.required_permissions,
            current_action_budget=flow.estimated_actions,
        )

        self.telemetry_bus.publish(
            execution_id=execution_id,
            layer=TelemetryLayer.FLOW,
            event_type="actor_selected",
            source="Direct Dispatch",
            payload={"actor": owner_name, "flow_id": flow_id},
        )
        self.event_bus.publish(
            RuntimeEventType.FLOW_STARTED,
            execution_id,
            "Direct Dispatch",
            {"flow_id": flow_id, "actor": owner_name},
            flow_id=flow_id,
            actor=owner_name,
        )
        self.telemetry_bus.publish(
            execution_id=execution_id,
            layer=TelemetryLayer.FLOW,
            event_type="flow_started",
            source="Direct Dispatch",
            payload={"flow_id": flow_id, "estimated_actions": flow.estimated_actions},
        )

        start = time.perf_counter()
        self.telemetry_bus.publish(
            execution_id=execution_id,
            layer=TelemetryLayer.ACTOR,
            event_type="actor_entered",
            source=owner_name,
        )
        response = self.actor_runtime.invoke(owner_name, flow_id, payload, context)
        runtime_ms = (time.perf_counter() - start) * 1000
        self.telemetry_bus.publish(
            execution_id=execution_id,
            layer=TelemetryLayer.ACTOR,
            event_type="actor_exited",
            source=owner_name,
            runtime_ms=runtime_ms,
            payload={"actions_used": response.actions_used, "success": response.success},
        )

        # Force human approval if the flow's declared permissions require it,
        # even if the actor forgot to flag it itself.
        if any(p in HUMAN_APPROVAL_REQUIRED for p in flow.required_permissions):
            response.requires_human_approval = True
            response.approval_reason = response.approval_reason or (
                f"Flow {flow_id} requires permissions that need human approval: "
                + ", ".join(p.value for p in flow.required_permissions)
            )

        self.telemetry_bus.publish(
            execution_id=execution_id,
            layer=TelemetryLayer.FLOW,
            event_type="flow_finished",
            source="Direct Dispatch",
            payload={
                "flow_id": flow_id,
                "estimated_actions": flow.estimated_actions,
                "actual_actions": response.actions_used,
                "delta": response.actions_used - flow.estimated_actions,
            },
        )
        self.event_bus.publish(
            RuntimeEventType.FLOW_COMPLETED if response.success else RuntimeEventType.FLOW_FAILED,
            execution_id,
            "Direct Dispatch",
            {"flow_id": flow_id, "success": response.success, "error": response.error},
            flow_id=flow_id,
            actor=owner_name,
        )

        flow_result = self.legal_logger.process_execution(
            execution_id=execution_id,
            flow_id=flow_id,
            object_type=object_type,
            object_id=object_id,
            actor_response=response,
            context=context,
            runtime_ms=runtime_ms,
            estimated_actions=flow.estimated_actions,
        )
        self.event_bus.publish(
            RuntimeEventType.REPORT_PUBLISHED,
            execution_id,
            "Legal Logger",
            {
                "flow_report_id": flow_result.flow_report_id,
                "execution_report_id": flow_result.execution_report_id,
            },
            flow_id=flow_id,
            actor="Legal Logger",
        )
        self.event_bus.publish(
            RuntimeEventType.PROFILE_UPDATED,
            execution_id,
            "Legal Logger",
            {"flow_id": flow_id},
            flow_id=flow_id,
            actor="Legal Logger",
        )
        if response.success:
            self.execution_runtime.finish(execution_id)
        else:
            self.execution_runtime.fail(execution_id, response.error or "Actor failed")
        return flow_result
