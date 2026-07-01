"""Pydantic schema for runtime-readable actor manifest drafts.

These manifests are extracted from actor ARCHITECTURE.md files. They are not the
runtime execution system yet; they are structured preparation for Actor Runtime
and Direct Dispatch.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


RiskLevel = Literal["low", "medium", "high", "critical", "TODO"]


class ActorManifestDraft(BaseModel):
    """Machine-readable actor boundary draft.

    Values may be "TODO" when the source architecture document does not clearly
    define the answer. TODO is intentional: it prevents agents from inventing
    runtime authority that the architecture did not grant.
    """

    model_config = ConfigDict(extra="forbid")

    actor_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)
    ownership_domain: str = Field(..., min_length=1)
    mission: str = Field(..., min_length=1)
    allowed_callers: list[str] = Field(default_factory=list)
    allowed_callees: list[str] = Field(default_factory=list)
    owned_flows: list[str] = Field(default_factory=list)
    allowed_flows: list[str] = Field(default_factory=list)
    required_permissions: list[str] = Field(default_factory=list)
    risk_level: RiskLevel
    truth_rules: list[str] = Field(default_factory=list)
    logbooks_written: list[str] = Field(default_factory=list)
    reports_created: list[str] = Field(default_factory=list)
    human_review_required_for: list[str] = Field(default_factory=list)
    depends_on: list[str] = Field(default_factory=list)
    cannot_do: list[str] = Field(default_factory=list)
    architecture_source: str = Field(..., min_length=1)

    @field_validator(
        "allowed_callers",
        "allowed_callees",
        "owned_flows",
        "allowed_flows",
        "required_permissions",
        "truth_rules",
        "logbooks_written",
        "reports_created",
        "human_review_required_for",
        "depends_on",
        "cannot_do",
    )
    @classmethod
    def list_fields_must_not_be_empty(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError("manifest list fields must contain source-backed values or TODO")
        cleaned = [item.strip() for item in value]
        if any(item in {"--", "---"} for item in cleaned):
            raise ValueError("manifest list fields must not contain markdown separators")
        return cleaned

    @field_validator("actor_id")
    @classmethod
    def actor_id_must_be_snake_case(cls, value: str) -> str:
        if value != value.lower() or " " in value:
            raise ValueError("actor_id must be snake_case")
        return value

    def architecture_path(self, repository_root: Path) -> Path:
        return repository_root / self.architecture_source
