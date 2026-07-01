from pathlib import Path
import tempfile
import unittest


class AgentManifestRegistryTests(unittest.TestCase):
    def test_agent_manifest_schema_validates_required_fields(self):
        from codriver.registry.agent_manifest_schema import AgentManifestDraft

        manifest = AgentManifestDraft(
            agent_id="advanced.intent-classifier",
            name="Intent Classifier",
            category="advanced",
            capability_domain="intent classification",
            mission="Classify user intent for routing.",
            inputs=["user request"],
            outputs=["intent label"],
            allowed_callers=["CoDriver"],
            allowed_actors=["TODO"],
            required_permissions=["TODO"],
            risk_level="medium",
            tools_needed=["TODO"],
            workers_needed=["TODO"],
            truth_rules=["Do not claim certainty when intent is ambiguous."],
            logbooks_written=["TODO"],
            reports_contributed_to=["TODO"],
            human_review_required_for=["TODO"],
            cannot_do=["make business decisions"],
            architecture_source="moonrust/agents/advanced/intent-classifier/ARCHITECTURE.md",
        )

        self.assertEqual(manifest.agent_id, "advanced.intent-classifier")
        self.assertEqual(manifest.category, "advanced")

    def test_load_agent_manifests_validates_yaml_directory(self):
        from codriver.registry.load_agent_manifests import load_agent_manifests

        with tempfile.TemporaryDirectory() as tmp:
            agent_dir = Path(tmp) / "advanced" / "intent-classifier"
            agent_dir.mkdir(parents=True)
            (agent_dir / "manifest.yaml").write_text(
                "\n".join(
                    [
                        "agent_id: advanced.intent-classifier",
                        "name: Intent Classifier",
                        "category: advanced",
                        "capability_domain: intent classification",
                        "mission: Classify user intent for routing.",
                        "inputs:",
                        "  - user request",
                        "outputs:",
                        "  - intent label",
                        "allowed_callers:",
                        "  - CoDriver",
                        "allowed_actors:",
                        "  - TODO",
                        "required_permissions:",
                        "  - TODO",
                        "risk_level: medium",
                        "tools_needed:",
                        "  - TODO",
                        "workers_needed:",
                        "  - TODO",
                        "truth_rules:",
                        "  - Do not claim certainty when intent is ambiguous.",
                        "logbooks_written:",
                        "  - TODO",
                        "reports_contributed_to:",
                        "  - TODO",
                        "human_review_required_for:",
                        "  - TODO",
                        "cannot_do:",
                        "  - make business decisions",
                        "architecture_source: moonrust/agents/advanced/intent-classifier/ARCHITECTURE.md",
                    ]
                )
            )

            manifests = load_agent_manifests(Path(tmp))

        self.assertEqual([manifest.agent_id for manifest in manifests], ["advanced.intent-classifier"])

    def test_repository_agent_manifests_are_valid_and_source_backed(self):
        from codriver.registry.load_agent_manifests import load_agent_manifests

        repository_root = Path(__file__).resolve().parents[1]
        manifests = load_agent_manifests(repository_root / "moonrust" / "agents")

        self.assertEqual(len(manifests), 317)
        for manifest in manifests:
            self.assertTrue(manifest.architecture_path(repository_root).exists())
            for field_name in (
                "inputs",
                "outputs",
                "allowed_callers",
                "allowed_actors",
                "required_permissions",
                "tools_needed",
                "workers_needed",
                "truth_rules",
                "logbooks_written",
                "reports_contributed_to",
                "human_review_required_for",
                "cannot_do",
            ):
                values = getattr(manifest, field_name)
                self.assertNotIn("--", values, f"{manifest.agent_id}.{field_name} contains markdown separator")
                self.assertNotIn("---", values, f"{manifest.agent_id}.{field_name} contains markdown separator")


if __name__ == "__main__":
    unittest.main()
