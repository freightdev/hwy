"""HTTP/WebSocket API for the CoDriver reference runtime.

This service is the dev/runtime boundary HWY backend and frontend talk to.
It keeps CoDriver out of backend CRUD while still making runtime state visible.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import httpx
from fastapi import FastAPI, WebSocket
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field

from .bootstrap import build_default_codriver
from .models import DryRunEstimate, FlowResult
from .runtime.timeline import RuntimeTimeline


class ChatRequest(BaseModel):
    message: str
    session_id: str = "dev-session"
    user_id: str = "dev-user"
    payload: dict[str, Any] = Field(default_factory=dict)


class FlowRequest(BaseModel):
    flow_id: str
    payload: dict[str, Any] = Field(default_factory=dict)
    session_id: str = "dev-session"
    user_id: str = "dev-user"
    object_type: str = "dev"
    object_id: str = "dev-object"


class CoDriverApiState:
    def __init__(
        self,
        *,
        storage_prefix: str,
        ollama_base_url: str | None = None,
        ollama_model: str | None = None,
        ollama_timeout: float | None = None,
    ) -> None:
        Path(storage_prefix).mkdir(parents=True, exist_ok=True)
        self.storage_prefix = storage_prefix
        self.codriver = build_default_codriver(storage_prefix=storage_prefix)
        self.timeline = RuntimeTimeline(self.codriver.dispatch.event_bus)
        self.ollama_base_url = ollama_base_url or os.getenv("OLLAMA_BASE_URL", "")
        self.ollama_model = ollama_model or os.getenv("OLLAMA_MODEL", "llama3.1")
        self.ollama_timeout = float(ollama_timeout or os.getenv("OLLAMA_TIMEOUT", "5"))

    def envelope(self, data: Any) -> dict[str, Any]:
        return {"data": jsonable_encoder(data)}

    def runtime_status(self) -> dict[str, Any]:
        return {
            "status": "ok",
            "service": "codriver",
            "storage_prefix": self.storage_prefix,
            "actors": len(self.codriver.registry.all_actors()),
            "flows": len(self.codriver.registry.all_flows()),
            "executions": len(self.codriver.dispatch.execution_runtime._executions),
            "events": len(self.codriver.dispatch.event_bus.history()),
            "ollama_configured": bool(self.ollama_base_url),
        }

    def actors(self) -> list[dict[str, Any]]:
        return [actor.model_dump(mode="json") for actor in self.codriver.registry.all_actors()]

    def executions(self) -> list[dict[str, Any]]:
        records = self.codriver.dispatch.execution_runtime._executions.values()
        return [record.model_dump(mode="json") for record in sorted(records, key=lambda r: r.started_at or "")]

    def timeline_for(self, execution_id: str) -> list[dict[str, Any]]:
        return [event.model_dump(mode="json") for event in self.timeline.for_execution(execution_id)]

    def recent_logbooks(self, limit: int = 20) -> list[dict[str, Any]]:
        entries = self.codriver.logbook.all_entries()
        return [entry.model_dump(mode="json") for entry in entries[-limit:]]

    def dry_run(self, request: FlowRequest) -> DryRunEstimate:
        return self.codriver.dispatch.dry_run(request.flow_id)

    def run_flow(self, request: FlowRequest) -> FlowResult:
        return self.codriver.dispatch.execute(
            request.flow_id,
            request.payload,
            object_type=request.object_type,
            object_id=request.object_id,
            user_id=request.user_id,
            session_id=request.session_id,
        )

    async def try_ollama(self, message: str) -> tuple[str, bool, str]:
        if not self.ollama_base_url:
            return "Model unavailable: OLLAMA_BASE_URL is not configured. Returning structural runtime response.", False, "unavailable"
        try:
            async with httpx.AsyncClient(timeout=self.ollama_timeout) as client:
                response = await client.post(
                    f"{self.ollama_base_url.rstrip('/')}/api/generate",
                    json={"model": self.ollama_model, "prompt": message, "stream": False},
                )
                response.raise_for_status()
                payload = response.json()
                text = payload.get("response") or "Model returned no response text."
                return text, True, "ok"
        except Exception:
            return "Model unavailable: Ollama could not be reached. Returning structural runtime response.", False, "unavailable"

    async def chat(self, request: ChatRequest) -> dict[str, Any]:
        from .core import CoDriverSession

        session = CoDriverSession(user_id=request.user_id, session_id=request.session_id)
        result = self.codriver.handle_message(
            session,
            request.message,
            payload=request.payload,
            object_type="codriver_chat",
            object_id=request.session_id,
        )

        if isinstance(result, FlowResult):
            timeline = self.timeline_for(result.execution_id)
            logbooks = self.recent_logbooks(limit=10)
            actor = timeline[1].get("actor") if len(timeline) > 1 else None
            return {
                "response": self._flow_response_text(result),
                "model_success": False,
                "model_status": "not_required",
                "execution_id": result.execution_id,
                "flow_id": result.result.get("flow_id", "packet_pilot.fill_packet"),
                "actor": actor or "Packet Pilot",
                "completed": result.completed,
                "flow_status": "completed" if result.completed else "failed",
                "flow_result": result.model_dump(mode="json"),
                "timeline": timeline,
                "logbook_entries": logbooks,
            }

        if isinstance(result, DryRunEstimate):
            return {
                "response": "Dry run complete.",
                "model_success": False,
                "model_status": "not_required",
                "execution_id": None,
                "flow_id": result.flow_id,
                "actor": result.planned_actors[0] if result.planned_actors else None,
                "completed": True,
                "flow_status": "dry_run",
                "dry_run": result.model_dump(mode="json"),
                "timeline": [],
                "logbook_entries": self.recent_logbooks(limit=10),
            }

        model_text, model_success, model_status = await self.try_ollama(request.message)
        structural = str(result)
        response_text = f"{model_text}\n\nRuntime note: {structural}"
        return {
            "response": response_text,
            "model_success": model_success,
            "model_status": model_status,
            "execution_id": None,
            "flow_id": None,
            "actor": None,
            "completed": False,
            "flow_status": "model_unavailable" if not model_success else "answered",
            "timeline": [],
            "logbook_entries": self.recent_logbooks(limit=10),
        }

    def _flow_response_text(self, result: FlowResult) -> str:
        return (
            "CoDriver routed the request through Direct Dispatch. "
            f"Execution {result.execution_id} completed. "
            f"Legal Logger wrote Flow Report {result.flow_report_id}."
        )


def create_app(
    *,
    storage_prefix: str | None = None,
    ollama_base_url: str | None = None,
    ollama_model: str | None = None,
    ollama_timeout: float | None = None,
) -> FastAPI:
    storage = storage_prefix or os.getenv("CODRIVER_STORAGE_DIR", ".codriver-dev")
    state = CoDriverApiState(
        storage_prefix=storage,
        ollama_base_url=ollama_base_url,
        ollama_model=ollama_model,
        ollama_timeout=ollama_timeout,
    )
    app = FastAPI(title="HWY CoDriver Runtime API", version="0.1.0")
    app.state.codriver_api = state

    @app.get("/health")
    def health() -> dict[str, Any]:
        return state.envelope({"status": "ok", "service": "codriver"})

    @app.post("/chat/send")
    async def chat_send(request: ChatRequest) -> dict[str, Any]:
        return state.envelope(await state.chat(request))

    @app.get("/runtime/status")
    def runtime_status() -> dict[str, Any]:
        return state.envelope(state.runtime_status())

    @app.get("/actors/list")
    def actors_list() -> dict[str, Any]:
        return state.envelope({"actors": state.actors()})

    @app.get("/executions/list")
    def executions_list() -> dict[str, Any]:
        return state.envelope({"executions": state.executions()})

    @app.get("/executions/{execution_id}/timeline")
    def execution_timeline(execution_id: str) -> dict[str, Any]:
        return state.envelope({"execution_id": execution_id, "events": state.timeline_for(execution_id)})

    @app.get("/logbooks/recent")
    def logbooks_recent(limit: int = 20) -> dict[str, Any]:
        return state.envelope({"entries": state.recent_logbooks(limit=limit)})

    @app.post("/flows/dry-run")
    def flows_dry_run(request: FlowRequest) -> dict[str, Any]:
        return state.envelope(state.dry_run(request))

    @app.post("/flows/run")
    def flows_run(request: FlowRequest) -> dict[str, Any]:
        result = state.run_flow(request)
        return state.envelope(
            {
                "flow_result": result,
                "timeline": state.timeline_for(result.execution_id),
                "logbook_entries": state.recent_logbooks(limit=10),
            }
        )

    @app.websocket("/ws/chat")
    async def ws_chat(websocket: WebSocket) -> None:
        await websocket.accept()
        while True:
            payload = await websocket.receive_json()
            result = await state.chat(ChatRequest.model_validate(payload))
            await websocket.send_json(jsonable_encoder({"data": result}))

    return app


app = create_app()


# ----------------------------------------------------------------------
# Moonrust Migration Notes
# ----------------------------------------------------------------------
#
# Rust Crate:
#     moonrust/crates/runtime
#
# Ownership:
#     CoDriver Runtime API boundary
#
# Dependencies:
#     Execution Runtime
#     Event Bus
#     Actor Runtime
#     Legal Logger
#
# Stable:
#     No
#
# Port Status:
#     Prototype
#
# Migration Requirements:
#     Must prove HWY TMS integration and runtime visibility before porting.
#
# ----------------------------------------------------------------------
