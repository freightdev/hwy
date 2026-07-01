import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient


class CoDriverApiServiceTests(unittest.TestCase):
    def test_chat_send_activates_packet_pilot_and_exposes_timeline_and_logbook(self):
        from codriver.api import create_app

        with tempfile.TemporaryDirectory() as tmp:
            app = create_app(storage_prefix=tmp)
            client = TestClient(app)

            response = client.post(
                "/chat/send",
                json={"message": "Fill a carrier packet test", "session_id": "test-session", "user_id": "dev-user"},
            )

            self.assertEqual(response.status_code, 200)
            data = response.json()["data"]
            self.assertTrue(data["execution_id"].startswith("exec-"))
            self.assertEqual(data["actor"], "Packet Pilot")
            self.assertEqual(data["flow_id"], "packet_pilot.fill_packet")
            self.assertTrue(data["completed"])
            self.assertIn("timeline", data)
            self.assertGreaterEqual(len(data["timeline"]), 4)
            self.assertIn("logbook_entries", data)
            self.assertGreaterEqual(len(data["logbook_entries"]), 1)

            execution_id = data["execution_id"]
            timeline_response = client.get(f"/executions/{execution_id}/timeline")
            self.assertEqual(timeline_response.status_code, 200)
            events = timeline_response.json()["data"]["events"]
            event_types = [event["event_type"] for event in events]
            self.assertIn("ExecutionStarted", event_types)
            self.assertIn("ActorStarted", event_types)
            self.assertIn("ReportPublished", event_types)
            self.assertIn("ExecutionCompleted", event_types)

    def test_required_codriver_endpoints_exist(self):
        from codriver.api import create_app

        with tempfile.TemporaryDirectory() as tmp:
            client = TestClient(create_app(storage_prefix=tmp))
            checks = [
                ("GET", "/health", None),
                ("GET", "/runtime/status", None),
                ("GET", "/actors/list", None),
                ("GET", "/executions/list", None),
                ("GET", "/logbooks/recent", None),
                ("POST", "/flows/dry-run", {"flow_id": "packet_pilot.fill_packet"}),
                ("POST", "/flows/run", {"flow_id": "packet_pilot.fill_packet", "payload": {}}),
            ]
            for method, path, body in checks:
                if method == "GET":
                    response = client.get(path)
                else:
                    response = client.post(path, json=body)
                self.assertLess(response.status_code, 500, f"{method} {path} failed: {response.text}")
                self.assertIn("data", response.json())

    def test_ollama_unavailable_degrades_without_fake_success(self):
        from codriver.api import create_app

        with tempfile.TemporaryDirectory() as tmp:
            client = TestClient(create_app(storage_prefix=tmp, ollama_base_url="http://127.0.0.1:9"))
            response = client.post("/chat/send", json={"message": "hello model"})

            self.assertEqual(response.status_code, 200)
            data = response.json()["data"]
            self.assertEqual(data["model_status"], "unavailable")
            self.assertFalse(data["model_success"])
            self.assertIn("model unavailable", data["response"].lower())


if __name__ == "__main__":
    unittest.main()
