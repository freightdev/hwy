"""
HWY CoDriver — Bootstrap

Wires actor manifests + flow specs into the registry. This file IS the actor
registry's current source of truth (point 2 from the spec: "Actor registry is
not defined yet. It needs to exist."). As real actors get built, they register
themselves here the same way Packet Pilot does below.

A single TelemetryBus is built first and shared across every actor and
CoDriver itself — that's what lets Packet Pilot's worker telemetry and
CoDriver's intent-detection telemetry land on the same execution_id.
"""

from __future__ import annotations

from .actors.packet_pilot import PacketPilot
from .core import CoDriver
from .models import ActorManifest, FlowSpec, Permission, RiskLevel
from .registry import ActorRegistry
from .telemetry import TelemetryBus


def build_default_registry(telemetry_bus: TelemetryBus) -> ActorRegistry:
    registry = ActorRegistry()

    # -- Packet Pilot ---------------------------------------------------
    packet_pilot_manifest = ActorManifest(
        name="Packet Pilot",
        domain="paperwork",
        allowed_flows=["packet_pilot.fill_packet"],
        inputs=["carrier_name", "mc_number", "document_template"],
        outputs=["filled_packet", "review_summary"],
        permissions=[Permission.READ_DOCUMENT, Permission.WRITE_DOCUMENT],
        logbooks_written=["document"],
        may_call_actors=["Memory Mark", "Secret Safe", "Key Keeper", "Legal Logger"],
        risk_level=RiskLevel.MEDIUM,
        requires_human_review=True,
        free_tier=False,
    )
    registry.register_actor(packet_pilot_manifest, PacketPilot(telemetry_bus))

    registry.register_flow(
        FlowSpec(
            flow_id="packet_pilot.fill_packet",
            owner_actor="Packet Pilot",
            description="Fill a carrier packet from provided + on-file data.",
            inputs=["carrier_name", "mc_number"],
            outputs=["filled_packet"],
            required_permissions=[Permission.WRITE_DOCUMENT, Permission.SUBMIT_DOCUMENT],
            required_workers=["Browser Worker", "OCR Worker", "LLM Worker"],
            estimated_actions=3,
            supports_dry_run=True,
        )
    )

    return registry


def build_default_codriver(storage_prefix: str = ".") -> CoDriver:
    telemetry_bus = TelemetryBus(f"{storage_prefix}/telemetry.jsonl")
    registry = build_default_registry(telemetry_bus)
    codriver = CoDriver(registry, storage_prefix=storage_prefix, telemetry_bus=telemetry_bus)
    codriver.teach_intent("fill this carrier packet", "packet_pilot.fill_packet")
    codriver.teach_intent("fill a carrier packet", "packet_pilot.fill_packet")
    codriver.teach_intent("carrier packet", "packet_pilot.fill_packet")
    codriver.teach_intent("fill packet", "packet_pilot.fill_packet")
    return codriver
