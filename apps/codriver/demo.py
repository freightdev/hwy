"""
Demo: prove the Phase 4 telemetry/observability layer works end to end.

    CoDriver -> Direct Dispatch -> Packet Pilot -> [Browser/OCR/LLM Worker telemetry]
         -> Telemetry Bus (publish) -> Legal Logger (subscribe)
         -> Execution Report -> Flow Report -> Flow Profile -> Logbook
         -> Timeline (reconstructed from raw telemetry)

Run: python demo.py
"""

import shutil
from pathlib import Path

from codriver.bootstrap import build_default_codriver
from codriver.core import CoDriverSession


def main():
    storage = Path("demo_storage")
    if storage.exists():
        shutil.rmtree(storage)
    storage.mkdir()

    codriver = build_default_codriver(storage_prefix=str(storage))
    session = CoDriverSession(user_id="jesse", session_id="sess-001")

    print("=" * 70)
    print("1) EXECUTE — Fill a carrier packet")
    print("=" * 70)
    result = codriver.handle_message(
        session,
        "Fill this carrier packet.",
        payload={"carrier_name": "Dyer Logistics", "mc_number": "MC123456"},
        object_type="document",
        object_id="packet-001",
    )
    print(f"execution_id={result.execution_id}")
    print(f"completed={result.completed} actions_used={result.actions_used}")
    print(f"flow_report_id={result.flow_report_id}")

    print("\n" + "=" * 70)
    print("2) TIMELINE — reconstructed entirely from telemetry events")
    print("=" * 70)
    print(codriver.timeline.render(result.execution_id))

    print("\n" + "=" * 70)
    print("3) EXECUTION REPORT — worker telemetry folded in automatically")
    print("=" * 70)
    execution_reports = codriver.legal_logger.get_execution_reports(
        "packet_pilot.fill_packet", limit=1
    )
    print(execution_reports[0].model_dump_json(indent=2))

    print("\n" + "=" * 70)
    print("4) RUN 2 MORE TIMES — watch Flow Profile aggregate real telemetry")
    print("=" * 70)
    for i, (carrier, mc) in enumerate(
        [("Nabrith Freight", "MC654321"), ("Unknown Carrier", None)], start=2
    ):
        r = codriver.handle_message(
            session,
            "Fill this carrier packet.",
            payload={"carrier_name": carrier, "mc_number": mc},
            object_type="document",
            object_id=f"packet-{i:03d}",
        )
        print(f"  run {i}: execution_id={r.execution_id} actions={r.actions_used}")

    profile = codriver.legal_logger.get_flow_profile("packet_pilot.fill_packet")
    print("\nFlow Profile after 3 runs:")
    print(profile.model_dump_json(indent=2))

    print("\n" + "=" * 70)
    print("5) RAW TELEMETRY for run 1 by layer — proves the worker layers exist")
    print("=" * 70)
    from codriver.models import TelemetryLayer

    for layer in [TelemetryLayer.BROWSER, TelemetryLayer.OCR, TelemetryLayer.LLM]:
        events = codriver.telemetry_bus.history_by_layer(result.execution_id, layer)
        for e in events:
            print(f"  [{layer.value}] {e.source}: {e.payload}")

    print("\n" + "=" * 70)
    print(f"Storage written to: {storage}/")
    print("=" * 70)
    for f in sorted(storage.iterdir()):
        print(f"  - {f.name}")


if __name__ == "__main__":
    main()
