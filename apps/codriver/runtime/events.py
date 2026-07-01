"""Runtime events coordinate execution.

Do not put telemetry measurements here. Telemetry still lives in
``codriver.telemetry`` and answers what happened quantitatively. Runtime events
answer which lifecycle transition occurred.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class RuntimeEventType(str, Enum):
    EXECUTION_STARTED = "ExecutionStarted"
    EXECUTION_COMPLETED = "ExecutionCompleted"
    EXECUTION_FAILED = "ExecutionFailed"
    EXECUTION_CANCELLED = "ExecutionCancelled"
    EXECUTION_TIMED_OUT = "ExecutionTimedOut"
    FLOW_STARTED = "FlowStarted"
    FLOW_COMPLETED = "FlowCompleted"
    FLOW_FAILED = "FlowFailed"
    ACTOR_STARTED = "ActorStarted"
    ACTOR_COMPLETED = "ActorCompleted"
    ACTOR_FAILED = "ActorFailed"
    REPORT_PUBLISHED = "ReportPublished"
    PROFILE_UPDATED = "ProfileUpdated"


class RuntimeEvent(BaseModel):
    id: str = Field(default_factory=lambda: f"evt-{uuid4().hex[:12]}")
    event_type: RuntimeEventType
    execution_id: str
    source: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    flow_id: str | None = None
    actor: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
