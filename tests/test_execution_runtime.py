from pathlib import Path
import tempfile
import unittest

from codriver.models import ActorContext, ActorManifest, ActorResponse, FlowSpec, Permission, RiskLevel
from codriver.registry import ActorRegistry


class RecordingHandler:
    def __init__(self):
        self.calls = []

    def handle(self, flow_id: str, payload: dict, context: ActorContext) -> ActorResponse:
        self.calls.append((flow_id, payload, context))
        return ActorResponse(
            actor="Packet Pilot",
            flow_id=flow_id,
            success=True,
            actions_used=1,
            raw={"handled_by": "packet_pilot", "execution_id": context.execution_id},
        )


def build_registry(handler: RecordingHandler | None = None) -> ActorRegistry:
    registry = ActorRegistry()
    registry.register_actor(
        ActorManifest(
            name="Packet Pilot",
            domain="paperwork",
            allowed_flows=["packet_pilot.fill_packet"],
            permissions=[Permission.READ_DOCUMENT],
            logbooks_written=["document"],
            may_call_actors=["Legal Logger"],
            risk_level=RiskLevel.MEDIUM,
            requires_human_review=False,
        ),
        handler or RecordingHandler(),
    )
    registry.register_flow(
        FlowSpec(
            flow_id="packet_pilot.fill_packet",
            owner_actor="Packet Pilot",
            required_permissions=[Permission.READ_DOCUMENT],
            estimated_actions=1,
        )
    )
    return registry


class ExecutionRuntimeTests(unittest.TestCase):
    def test_execution_runtime_creates_execution_ids(self):
        from codriver.runtime.execution import ExecutionRuntime, ExecutionStatus

        runtime = ExecutionRuntime()
        execution = runtime.start(flow_id="packet_pilot.fill_packet")

        self.assertTrue(execution.execution_id.startswith("exec-"))
        self.assertEqual(execution.status, ExecutionStatus.RUNNING)

    def test_event_bus_publishes_runtime_events(self):
        from codriver.runtime.event_bus import EventBus
        from codriver.runtime.events import RuntimeEventType

        bus = EventBus()
        seen = []
        bus.subscribe(seen.append)

        event = bus.publish(
            event_type=RuntimeEventType.EXECUTION_STARTED,
            execution_id="exec-test",
            source="Execution Runtime",
            payload={"flow_id": "packet_pilot.fill_packet"},
        )

        self.assertEqual(seen, [event])
        self.assertEqual(event.event_type, RuntimeEventType.EXECUTION_STARTED)

    def test_timeline_records_ordered_events(self):
        from codriver.runtime.event_bus import EventBus
        from codriver.runtime.events import RuntimeEventType
        from codriver.runtime.timeline import RuntimeTimeline

        bus = EventBus()
        timeline = RuntimeTimeline(bus)

        bus.publish(RuntimeEventType.EXECUTION_STARTED, "exec-test", "Execution Runtime")
        bus.publish(RuntimeEventType.FLOW_STARTED, "exec-test", "Direct Dispatch")
        bus.publish(RuntimeEventType.FLOW_COMPLETED, "exec-test", "Direct Dispatch")

        events = timeline.for_execution("exec-test")

        self.assertEqual(
            [event.event_type for event in events],
            [
                RuntimeEventType.EXECUTION_STARTED,
                RuntimeEventType.FLOW_STARTED,
                RuntimeEventType.FLOW_COMPLETED,
            ],
        )

    def test_actor_runtime_invokes_packet_pilot_through_registry(self):
        from codriver.runtime.actor_runtime import ActorRuntime
        from codriver.runtime.event_bus import EventBus
        from codriver.runtime.events import RuntimeEventType

        handler = RecordingHandler()
        registry = build_registry(handler)
        bus = EventBus()
        actor_runtime = ActorRuntime(registry=registry, event_bus=bus)
        context = ActorContext(
            actor_id="Packet Pilot",
            execution_id="exec-test",
            current_flow="packet_pilot.fill_packet",
        )

        response = actor_runtime.invoke(
            actor_name="Packet Pilot",
            flow_id="packet_pilot.fill_packet",
            payload={"carrier_name": "Acme"},
            context=context,
        )

        self.assertTrue(response.success)
        self.assertEqual(len(handler.calls), 1)
        self.assertEqual(
            [event.event_type for event in bus.history("exec-test")],
            [RuntimeEventType.ACTOR_STARTED, RuntimeEventType.ACTOR_COMPLETED],
        )

    def test_direct_dispatch_routes_actor_calls_through_actor_runtime(self):
        from codriver.actors.legal_logger import LegalLogger
        from codriver.direct_dispatch import DirectDispatch
        from codriver.logbook import LogbookStore
        from codriver.runtime.actor_runtime import ActorRuntime
        from codriver.runtime.event_bus import EventBus
        from codriver.telemetry import TelemetryBus

        class RecordingActorRuntime(ActorRuntime):
            def __init__(self, registry, event_bus):
                super().__init__(registry=registry, event_bus=event_bus)
                self.invocations = []

            def invoke(self, actor_name, flow_id, payload, context):
                self.invocations.append((actor_name, flow_id, payload, context.execution_id))
                return super().invoke(actor_name, flow_id, payload, context)

        handler = RecordingHandler()
        registry = build_registry(handler)
        event_bus = EventBus()
        actor_runtime = RecordingActorRuntime(registry, event_bus)
        with tempfile.TemporaryDirectory() as tmp:
            telemetry_bus = TelemetryBus(str(Path(tmp) / "telemetry.jsonl"))
            logbook = LogbookStore(str(Path(tmp) / "logbook.jsonl"))
            legal_logger = LegalLogger(
                logbook=logbook,
                telemetry_bus=telemetry_bus,
                execution_reports_path=str(Path(tmp) / "execution_reports.jsonl"),
                flow_reports_path=str(Path(tmp) / "flow_reports.jsonl"),
                flow_profiles_path=str(Path(tmp) / "flow_profiles.json"),
            )
            dispatch = DirectDispatch(
                registry,
                logbook,
                legal_logger,
                telemetry_bus,
                event_bus=event_bus,
                actor_runtime=actor_runtime,
            )

            dispatch.execute(
                "packet_pilot.fill_packet",
                {"carrier_name": "Acme"},
                object_type="load",
                object_id="load-1",
                execution_id="exec-test",
            )

        self.assertEqual(len(actor_runtime.invocations), 1)
        self.assertEqual(len(handler.calls), 1)

    def test_direct_dispatch_still_returns_legal_logger_flow_result(self):
        from codriver.bootstrap import build_default_codriver
        from codriver.core import CoDriverSession
        from codriver.models import FlowResult

        with tempfile.TemporaryDirectory() as tmp:
            codriver = build_default_codriver(storage_prefix=tmp)
            result = codriver.handle_message(
                CoDriverSession(user_id="user-1", session_id="session-1"),
                "fill packet",
                payload={"carrier_name": "Acme Carrier", "mc_number": "123456"},
                object_type="load",
                object_id="load-1",
            )

        self.assertIsInstance(result, FlowResult)
        self.assertTrue(result.execution_id.startswith("exec-"))
        self.assertTrue(result.flow_report_id)
        self.assertTrue(result.execution_report_id)
        self.assertTrue(result.completed)


if __name__ == "__main__":
    unittest.main()
