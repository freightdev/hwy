"""Clean backend client for the separate CoDriver runtime service.

Backend remains the business platform. CoDriver remains runtime.
This client is the boundary between them.
"""

from __future__ import annotations

from typing import Any

import httpx


class CoDriverClient:
    def __init__(self, base_url: str, timeout: float = 10.0, transport: httpx.BaseTransport | None = None):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.transport = transport

    def _request(self, method: str, path: str, *, json: dict[str, Any] | None = None) -> dict[str, Any]:
        try:
            with httpx.Client(timeout=self.timeout, transport=self.transport) as client:
                response = client.request(method, f"{self.base_url}{path}", json=json)
                response.raise_for_status()
                payload = response.json()
                data = payload.get("data", payload)
                return data if isinstance(data, dict) else {"value": data}
        except Exception:
            return {
                "status": "unavailable",
                "response": "CoDriver runtime unavailable. Backend is up, but the runtime service could not be reached.",
            }

    def health(self) -> dict[str, Any]:
        return self._request("GET", "/health")

    def chat_send(self, message: str, *, session_id: str = "dev-session", user_id: str = "dev-user", payload: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._request(
            "POST",
            "/chat/send",
            json={
                "message": message,
                "session_id": session_id,
                "user_id": user_id,
                "payload": payload or {},
            },
        )

    def runtime_status(self) -> dict[str, Any]:
        return self._request("GET", "/runtime/status")

    def actors_list(self) -> dict[str, Any]:
        return self._request("GET", "/actors/list")

    def executions_list(self) -> dict[str, Any]:
        return self._request("GET", "/executions/list")

    def execution_timeline(self, execution_id: str) -> dict[str, Any]:
        return self._request("GET", f"/executions/{execution_id}/timeline")

    def logbooks_recent(self) -> dict[str, Any]:
        return self._request("GET", "/logbooks/recent")

    def dry_run(self, flow_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._request("POST", "/flows/dry-run", json={"flow_id": flow_id, "payload": payload or {}})

    def run_flow(self, flow_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._request("POST", "/flows/run", json={"flow_id": flow_id, "payload": payload or {}})
