from pathlib import Path
import tempfile
import unittest


class ActorManifestRegistryTests(unittest.TestCase):
    def test_actor_manifest_schema_validates_required_fields(self):
        from codriver.registry.actor_manifest_schema import ActorManifestDraft

        manifest = ActorManifestDraft(
            actor_id="packet_pilot",
            name="Packet Pilot",
            category="business_actor",
            ownership_domain="paperwork operations",
            mission="What paperwork is needed?",
            allowed_callers=["TODO"],
            allowed_callees=["legal_logger"],
            owned_flows=["TODO"],
            allowed_flows=["TODO"],
            required_permissions=["TODO"],
            risk_level="medium",
            truth_rules=["Never present unknown document data as verified."],
            logbooks_written=["Load Logbook"],
            reports_created=["TODO"],
            human_review_required_for=["signing documents"],
            depends_on=["Legal Logger"],
            cannot_do=["make business decisions"],
            architecture_source="moonrust/actors/packet_pilot/ARCHITECTURE.md",
        )

        self.assertEqual(manifest.actor_id, "packet_pilot")
        self.assertEqual(manifest.risk_level, "medium")

    def test_load_manifests_validates_yaml_directory(self):
        from codriver.registry.load_manifests import load_actor_manifests

        with tempfile.TemporaryDirectory() as tmp:
            actor_dir = Path(tmp) / "packet_pilot"
            actor_dir.mkdir()
            (actor_dir / "manifest.yaml").write_text(
                "\n".join(
                    [
                        "actor_id: packet_pilot",
                        "name: Packet Pilot",
                        "category: business_actor",
                        "ownership_domain: paperwork operations",
                        "mission: What paperwork is needed?",
                        "allowed_callers:",
                        "  - TODO",
                        "allowed_callees:",
                        "  - legal_logger",
                        "owned_flows:",
                        "  - TODO",
                        "allowed_flows:",
                        "  - TODO",
                        "required_permissions:",
                        "  - TODO",
                        "risk_level: medium",
                        "truth_rules:",
                        "  - Never present unknown document data as verified.",
                        "logbooks_written:",
                        "  - Load Logbook",
                        "reports_created:",
                        "  - TODO",
                        "human_review_required_for:",
                        "  - signing documents",
                        "depends_on:",
                        "  - Legal Logger",
                        "cannot_do:",
                        "  - make business decisions",
                        "architecture_source: moonrust/actors/packet_pilot/ARCHITECTURE.md",
                    ]
                )
            )

            manifests = load_actor_manifests(Path(tmp))

        self.assertEqual([manifest.actor_id for manifest in manifests], ["packet_pilot"])

    def test_repository_actor_manifests_are_valid_and_source_backed(self):
        from codriver.registry.load_manifests import load_actor_manifests

        repository_root = Path(__file__).resolve().parents[1]
        manifests = load_actor_manifests(repository_root / "moonrust" / "actors")

        self.assertGreaterEqual(len(manifests), 1)
        for manifest in manifests:
            self.assertTrue(manifest.architecture_path(repository_root).exists())
            for field_name in (
                "truth_rules",
                "logbooks_written",
                "reports_created",
                "human_review_required_for",
                "cannot_do",
            ):
                values = getattr(manifest, field_name)
                self.assertNotIn("--", values, f"{manifest.actor_id}.{field_name} contains markdown separator")


if __name__ == "__main__":
    unittest.main()
