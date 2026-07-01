from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.config import settings
from app.services.codriver_client import CoDriverClient


router = APIRouter(prefix="/api/v1/codriver", tags=["codriver"])


def get_codriver_client() -> CoDriverClient:
    return CoDriverClient(settings.codriver_runtime_url)


class ChatRequest(BaseModel):
    message: str
    session_id: str = "dev-session"
    user_id: str = "dev-user"
    payload: dict = Field(default_factory=dict)


class FlowRequest(BaseModel):
    flow_id: str
    payload: dict = Field(default_factory=dict)


@router.get("/health")
def health():
    return {"data": get_codriver_client().health()}


@router.post("/chat/send")
def chat_send(request: ChatRequest):
    return {
        "data": get_codriver_client().chat_send(
            request.message,
            session_id=request.session_id,
            user_id=request.user_id,
            payload=request.payload,
        )
    }


@router.get("/runtime/status")
def runtime_status():
    return {"data": get_codriver_client().runtime_status()}


@router.get("/actors/list")
def actors_list():
    return {"data": get_codriver_client().actors_list()}


@router.get("/executions/list")
def executions_list():
    return {"data": get_codriver_client().executions_list()}


@router.get("/executions/{execution_id}/timeline")
def execution_timeline(execution_id: str):
    return {"data": get_codriver_client().execution_timeline(execution_id)}


@router.get("/logbooks/recent")
def logbooks_recent():
    return {"data": get_codriver_client().logbooks_recent()}


@router.post("/flows/dry-run")
def dry_run(request: FlowRequest):
    return {"data": get_codriver_client().dry_run(request.flow_id, request.payload)}


@router.post("/flows/run")
def run_flow(request: FlowRequest):
    return {"data": get_codriver_client().run_flow(request.flow_id, request.payload)}
