import unittest

import httpx


class BackendCoDriverClientTests(unittest.TestCase):
    def test_client_posts_chat_to_codriver_runtime(self):
        from app.services.codriver_client import CoDriverClient

        seen = {}

        def handler(request: httpx.Request) -> httpx.Response:
            seen["url"] = str(request.url)
            seen["body"] = request.read().decode()
            return httpx.Response(200, json={"data": {"response": "ok", "execution_id": "exec-test"}})

        client = CoDriverClient(
            base_url="http://codriver:8010",
            transport=httpx.MockTransport(handler),
        )

        result = client.chat_send("Fill a carrier packet test", session_id="s1", user_id="u1")

        self.assertEqual(seen["url"], "http://codriver:8010/chat/send")
        self.assertIn("Fill a carrier packet test", seen["body"])
        self.assertEqual(result["response"], "ok")
        self.assertEqual(result["execution_id"], "exec-test")

    def test_client_reports_unavailable_without_throwing_secret_details(self):
        from app.services.codriver_client import CoDriverClient

        def handler(request: httpx.Request) -> httpx.Response:
            raise httpx.ConnectError("boom secret-ish transport detail", request=request)

        client = CoDriverClient(
            base_url="http://codriver:8010",
            transport=httpx.MockTransport(handler),
        )

        result = client.chat_send("hello")

        self.assertEqual(result["status"], "unavailable")
        self.assertIn("CoDriver runtime unavailable", result["response"])
        self.assertNotIn("secret-ish", result["response"])


if __name__ == "__main__":
    unittest.main()
