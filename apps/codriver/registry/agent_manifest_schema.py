"""Pydantic schema for Moonrust Agent capability manifest drafts.

Agent manifests make ``moonrust/agents/**/ARCHITECTURE.md`` searchable by
CoDriver Agent Builder without granting runtime execution authority.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


RiskLevel = Literal["low", "medium", "high", "critical", "TODO"]


class AgentManifestDraft(BaseModel):
    """Machine-readable capability manifest extracted from Agent architecture.

    Use "TODO" when the source architecture does not clearly state a field.
    TODO is safer than inventing capability authority.
    """

    model_config = ConfigDict(extra="forbid")

    agent_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)
    capability_domain: str = Field(..., min_length=1)
    mission: str = Field(..., min_length=1)
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    allowed_callers: list[str] = Field(default_factory=list)
    allowed_actors: list[str] = Field(default_factory=list)
    required_permissions: list[str] = Field(default_factory=list)
    risk_level: RiskLevel
    tools_needed: list[str] = Field(default_factory=list)
    workers_needed: list[str] = Field(default_factory=list)
    truth_rules: list[str] = Field(default_factory=list)
    logbooks_written: list[str] = Field(default_factory=list)
    reports_contributed_to: list[str] = Field(default_factory=list)
    human_review_required_for: list[str] = Field(default_factory=list)
    cannot_do: list[str] = Field(default_factory=list)
    architecture_source: str = Field(..., min_length=1)

    @field_validator(
        "inputs",
        "outputs",
        "allowed_callers",
        "allowed_actors",
        "required_permissions",
        "tools_needed",
        "workers_needed",
        "truth_rules",
        "logbooks_written",
        "reports_contributed_to",
        "human_review_required_for",
        "cannot_do",
    )
    @classmethod
    def list_fields_must_not_be_empty_or_dirty(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError("agent manifest list fields must contain source-backed values or TODO")
        cleaned = [item.strip() for item in value]
        if any(item in {"--", "---"} for item in cleaned):
            raise ValueError("agent manifest list fields must not contain markdown separators")
        return cleaned

    @field_validator("agent_id")
    @classmethod
    def agent_id_must_include_category(cls, value: str) -> str:
        if " " in value or value != value.lower():
            raise ValueError("agent_id must be lowercase and must not contain spaces")
        if "." not in value:
            raise ValueError("agent_id must include category prefix, e.g. advanced.intent-classifier")
        return value

    def architecture_path(self, repository_root: Path) -> Path:
        return repository_root / self.architecture_source
