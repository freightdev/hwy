"""Runtime health snapshots."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class RuntimeHealthStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    FAILED = "failed"


class RuntimeHealth(BaseModel):
    status: RuntimeHealthStatus = RuntimeHealthStatus.HEALTHY
    checks: dict[str, str] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
