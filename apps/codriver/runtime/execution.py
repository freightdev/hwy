"""Execution Runtime owns execution lifecycle."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field

from .event_bus import EventBus
from .events import RuntimeEventType


class ExecutionStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMED_OUT = "timed_out"


class ExecutionRecord(BaseModel):
    execution_id: str = Field(default_factory=lambda: f"exec-{uuid4().hex[:12]}")
    flow_id: str | None = None
    status: ExecutionStatus = ExecutionStatus.PENDING
    started_at: datetime | None = None
    finished_at: datetime | None = None
    error: str | None = None
    reason: str | None = None


class ExecutionRuntime:
    def __init__(self, event_bus: EventBus | None = None) -> None:
        self.event_bus = event_bus or EventBus()
        self._executions: dict[str, ExecutionRecord] = {}

    def start(self, *, flow_id: str | None = None, execution_id: str | None = None) -> ExecutionRecord:
        record = ExecutionRecord(execution_id=execution_id or f"exec-{uuid4().hex[:12]}", flow_id=flow_id)
        record.status = ExecutionStatus.RUNNING
        record.started_at = datetime.now(timezone.utc)
        self._executions[record.execution_id] = record
        self.event_bus.publish(
            RuntimeEventType.EXECUTION_STARTED,
            record.execution_id,
            "Execution Runtime",
            {"status": record.status.value},
            flow_id=flow_id,
        )
        return record

    def finish(self, execution_id: str) -> ExecutionRecord:
        return self._transition(execution_id, ExecutionStatus.COMPLETED, RuntimeEventType.EXECUTION_COMPLETED)

    def fail(self, execution_id: str, error: str) -> ExecutionRecord:
        return self._transition(execution_id, ExecutionStatus.FAILED, RuntimeEventType.EXECUTION_FAILED, error=error)

    def cancel(self, execution_id: str, reason: str | None = None) -> ExecutionRecord:
        return self._transition(execution_id, ExecutionStatus.CANCELLED, RuntimeEventType.EXECUTION_CANCELLED, reason=reason)

    def timeout(self, execution_id: str, reason: str | None = None) -> ExecutionRecord:
        return self._transition(execution_id, ExecutionStatus.TIMED_OUT, RuntimeEventType.EXECUTION_TIMED_OUT, reason=reason)

    def get(self, execution_id: str) -> ExecutionRecord:
        return self._executions[execution_id]

    def _transition(
        self,
        execution_id: str,
        status: ExecutionStatus,
        event_type: RuntimeEventType,
        *,
        error: str | None = None,
        reason: str | None = None,
    ) -> ExecutionRecord:
        record = self._executions[execution_id]
        record.status = status
        record.finished_at = datetime.now(timezone.utc)
        record.error = error
        record.reason = reason
        self.event_bus.publish(
            event_type,
            execution_id,
            "Execution Runtime",
            {"status": status.value, "error": error, "reason": reason},
            flow_id=record.flow_id,
        )
        return record
