"""
HWY CoDriver — Packet Pilot (stub)

Owns the "paperwork" domain. Still a thin stub on the business logic, but
now instrumented with the worker telemetry layers it will actually depend on
once real Browser/OCR workers exist (Packet Pilot is the goldmine for that
telemetry per the build plan). These are SIMULATED worker calls with
realistic, varying values — not artificial failures — just enough to prove
the Browser/OCR/LLM telemetry layers flow correctly end to end.
"""

from __future__ import annotations

import random

from ..models import ActorContext, ActorResponse, Claim, TelemetryLayer, TruthLabel
from ..telemetry import TelemetryBus


class PacketPilot:
    name = "Packet Pilot"

    def __init__(self, telemetry_bus: TelemetryBus):
        self.telemetry_bus = telemetry_bus

    def handle(self, flow_id: str, payload: dict, context: ActorContext) -> ActorResponse:
        if flow_id == "packet_pilot.fill_packet":
            return self._fill_packet(payload, context)
        return ActorResponse(
            actor=self.name,
            flow_id=flow_id,
            success=False,
            error=f"Packet Pilot does not own flow: {flow_id}",
        )

    def _fill_packet(self, payload: dict, context: ActorContext) -> ActorResponse:
        carrier_name = payload.get("carrier_name", "UNKNOWN")
        mc_number = payload.get("mc_number")
        exec_id = context.execution_id

        # -- Browser Worker: open the carrier portal -------------------
        page_load_ms = random.uniform(80, 220)
        self.telemetry_bus.publish(
            execution_id=exec_id,
            layer=TelemetryLayer.BROWSER,
            event_type="browser_navigation",
            source="Browser Worker",
            runtime_ms=page_load_ms,
            payload={
                "page_load_ms": page_load_ms,
                "selector_failures": 0,
                "retry_count": 0,
                "navigation_count": 1,
                "captcha_detected": False,
            },
        )

        # -- OCR Worker: read the carrier packet template ---------------
        ocr_runtime_ms = random.uniform(900, 1800)
        confidence = random.uniform(0.91, 0.99)
        self.telemetry_bus.publish(
            execution_id=exec_id,
            layer=TelemetryLayer.OCR,
            event_type="ocr_completed",
            source="OCR Worker",
            runtime_ms=ocr_runtime_ms,
            payload={
                "pages": 2,
                "confidence": round(confidence, 3),
                "tables_found": 1,
                "signatures_found": 0,
                "handwriting_found": False,
            },
        )

        # -- LLM Worker: extract structured fields from OCR text --------
        llm_runtime_ms = random.uniform(300, 700)
        self.telemetry_bus.publish(
            execution_id=exec_id,
            layer=TelemetryLayer.LLM,
            event_type="llm_call",
            source="LLM Worker",
            runtime_ms=llm_runtime_ms,
            payload={
                "model": "claude-sonnet-5",
                "provider": "anthropic",
                "prompt_tokens": 1840,
                "completion_tokens": 220,
                "context_size": 8192,
                "temperature": 0.0,
                "retry_count": 0,
                "cache_hit": False,
            },
        )

        claims = [
            Claim(
                text=f"Carrier packet drafted for {carrier_name}",
                label=TruthLabel.CALCULATED,
                source=self.name,
            )
        ]
        if mc_number:
            claims.append(
                Claim(
                    text=f"MC number provided: {mc_number}",
                    label=TruthLabel.USER_PROVIDED,
                    source="user input",
                )
            )
        else:
            claims.append(
                Claim(
                    text="MC number not provided — packet incomplete",
                    label=TruthLabel.UNKNOWN,
                )
            )

        return ActorResponse(
            actor=self.name,
            flow_id="packet_pilot.fill_packet",
            success=True,
            claims=claims,
            requires_human_approval=True,  # submitting paperwork needs sign-off
            approval_reason="Carrier packet must be reviewed before submission.",
            actions_used=3,
            raw={"carrier_name": carrier_name, "mc_number": mc_number},
        )
