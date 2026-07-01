"""Actor Runtime invokes actors through one standard boundary."""

from __future__ import annotations

from ..models import ActorContext, ActorResponse
from ..registry import ActorRegistry
from .event_bus import EventBus
from .events import RuntimeEventType


class ActorRuntime:
    def __init__(self, *, registry: ActorRegistry, event_bus: EventBus):
        self.registry = registry
        self.event_bus = event_bus

    def invoke(
        self,
        actor_name: str,
        flow_id: str,
        payload: dict,
        context: ActorContext,
    ) -> ActorResponse:
        self.event_bus.publish(
            RuntimeEventType.ACTOR_STARTED,
            context.execution_id,
            "Actor Runtime",
            {"flow_id": flow_id},
            flow_id=flow_id,
            actor=actor_name,
        )
        handler = self.registry.handler(actor_name)
        try:
            response = handler.handle(flow_id, payload, context)
        except Exception as exc:
            response = ActorResponse(actor=actor_name, flow_id=flow_id, success=False, error=str(exc))
        self.event_bus.publish(
            RuntimeEventType.ACTOR_COMPLETED if response.success else RuntimeEventType.ACTOR_FAILED,
            context.execution_id,
            "Actor Runtime",
            {"flow_id": flow_id, "success": response.success, "error": response.error},
            flow_id=flow_id,
            actor=actor_name,
        )
        return response
