import json
import unittest
import urllib.error
import urllib.request
from uuid import uuid4

BASE = "http://localhost:18000/api/v1"


def post(path, payload, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(payload).encode(),
        headers=headers,
        method="POST",
    )
    try:
        return urllib.request.urlopen(req, timeout=10).status, json.loads(urllib.request.urlopen(req, timeout=10).read())
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read())


def request(method, path, payload=None, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(
        BASE + path,
        data=None if payload is None else json.dumps(payload).encode(),
        headers=headers,
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read())


class AdminAuthPermissionTests(unittest.TestCase):
    def setUp(self):
        self.email = f"test-admin-{uuid4().hex[:8]}@hwytms.test"
        self.password = "StrongPass123!"

    def register(self, email=None, password=None, role="Admin"):
        status, body = request("POST", "/auth/register", {
            "name": "Test Admin",
            "email": email or self.email,
            "password": password or self.password,
            "phone": "555-0100",
            "role": role,
        })
        self.assertEqual(status, 200, body)
        return body["data"]

    def auth_token(self):
        return self.register()["access_token"]

    def test_register_returns_session_user_and_permissions(self):
        data = self.register()
        self.assertIn("access_token", data)
        self.assertIn("refresh_token", data)
        self.assertEqual(data["user"]["email"], self.email)
        self.assertIn("permissions", data["user"])
        self.assertTrue(data["user"]["permissions"])

    def test_password_policy_rejects_short_passwords(self):
        status, body = request("POST", "/auth/register", {
            "name": "Weak User",
            "email": f"weak-{uuid4().hex[:8]}@hwytms.test",
            "password": "short",
        })
        self.assertEqual(status, 422, body)

    def test_admin_can_list_users_and_permission_matrix(self):
        token = self.auth_token()
        status, body = request("GET", "/admin/users", token=token)
        self.assertEqual(status, 200, body)
        self.assertGreaterEqual(len(body["data"]["users"]), 1)

        status, body = request("GET", "/admin/permissions", token=token)
        self.assertEqual(status, 200, body)
        data = body["data"]
        self.assertIn("roles", data)
        self.assertIn("permissions", data)
        admin_role = next(role for role in data["roles"] if role["key"] == "admin")
        self.assertTrue(admin_role["locked"])

    def test_admin_permissions_are_locked(self):
        token = self.auth_token()
        status, body = request("PATCH", "/admin/permissions/admin/manage_users", {"allowed": False}, token=token)
        self.assertEqual(status, 400, body)


if __name__ == "__main__":
    unittest.main()
