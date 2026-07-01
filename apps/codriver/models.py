"""
HWY CoDriver — Core Models

These are the structural backbone of the Truth Model and Logbook Law described
in ARCHITECTURE.md. Truth labeling is enforced here as TYPES, not just prompted
behavior — every Claim an actor returns must carry a TruthLabel, and every
important event must produce a LogbookEntry.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Truth Model
# ---------------------------------------------------------------------------

class TruthLabel(str, Enum):
    OFFICIAL_SOURCE = "official_source"
    SOURCE_BACKED = "source_backed"
    PROFILE_BACKED = "profile_backed"
    LOGBOOK_BACKED = "logbook_backed"
    USER_PROVIDED = "user_provided"
    SPEAKER_CLAIMED = "speaker_claimed"
    TRANSCRIBED = "transcribed"
    CALCULATED = "calculated"
    ESTIMATED = "estimated"
    INFERRED = "inferred"
    UNCERTAIN = "uncertain"
    UNKNOWN = "unknown"


class Claim(BaseModel):
    """A single typed statement of fact, always carrying a truth label.

    CoDriver and actors never return bare strings as 'facts' — every piece of
    information that could be presented to a user as true gets wrapped in a
    Claim so the label travels with the data through the whole system.
    """

    text: str
    label: TruthLabel
    source: Optional[str] = None  # e.g. "rate_confirmation.pdf", "Legal Logger #1234"
    confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0)

    def is_verified(self) -> bool:
        return self.label in {
            TruthLabel.OFFICIAL_SOURCE,
            TruthLabel.SOURCE_BACKED,
            TruthLabel.LOGBOOK_BACKED,
        }


# ---------------------------------------------------------------------------
# Risk / Permissions
# ---------------------------------------------------------------------------

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"  # always requires human approval, no exceptions


class Permission(str, Enum):
    READ_LOAD = "read_load"
    READ_DOCUMENT = "read_document"
    WRITE_DOCUMENT = "write_document"
    SUBMIT_DOCUMENT = "submit_document"
    BOOK_FREIGHT = "book_freight"
    ACCEPT_RATE = "accept_rate"
    SIGN_DOCUMENT = "sign_document"
    SHARE_PROTECTED_DATA = "share_protected_data"
    CHANGE_AUTHORITY = "change_authority"
    READ_SECRET = "read_secret"


HUMAN_APPROVAL_REQUIRED: set[Permission] = {
    Permission.BOOK_FREIGHT,
    Permission.ACCEPT_RATE,
    Permission.SIGN_DOCUMENT,
    Permission.SUBMIT_DOCUMENT,
    Permission.SHARE_PROTECTED_DATA,
    Permission.CHANGE_AUTHORITY,
}


# ---------------------------------------------------------------------------
# Logbook Law
# ---------------------------------------------------------------------------

class LogbookEntry(BaseModel):
    """Append-only record. Nothing important happens without one of these."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    object_type: str          # e.g. "load", "flow", "actor", "document", "call"
    object_id: str
    event_type: str           # e.g. "flow_started", "approval_requested", "error"
    actor: str                # which actor produced this entry
    flow_id: Optional[str] = None
    agent: Optional[str] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    summary: str
    evidence: list[str] = Field(default_factory=list)
    truth_labels: list[Claim] = Field(default_factory=list)
    actions_used: int = 0
    status: str = "recorded"  # recorded | pending | failed | superseded
    previous_ref: Optional[str] = None  # chain to prior entry for this object
    metadata: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Flow Spec
# ---------------------------------------------------------------------------

class FlowSpec(BaseModel):
    flow_id: str
    owner_actor: str
    version: str = "0.1.0"
    description: str = ""
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    required_permissions: list[Permission] = Field(default_factory=list)
    required_workers: list[str] = Field(default_factory=list)  # actors this flow calls
    estimated_actions: int = 1
    supports_dry_run: bool = True
    failure_behavior: str = "escalate_to_error_echo"


class DryRunEstimate(BaseModel):
    flow_id: str
    planned_actors: list[str]
    planned_flows: list[str]
    estimated_actions: int
    estimated_time_seconds: Optional[int] = None
    required_data: list[str] = Field(default_factory=list)
    required_permissions: list[Permission] = Field(default_factory=list)
    human_review_required: bool
    possible_failure_points: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Actor Manifest (registry entry)
# ---------------------------------------------------------------------------

class ActorManifest(BaseModel):
    name: str
    domain: str  # ownership domain, e.g. "paperwork", "freight discovery"
    allowed_flows: list[str] = Field(default_factory=list)
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    permissions: list[Permission] = Field(default_factory=list)
    logbooks_written: list[str] = Field(default_factory=list)
    may_call_actors: list[str] = Field(default_factory=list)
    risk_level: RiskLevel = RiskLevel.LOW
    requires_human_review: bool = False
    free_tier: bool = False


# ---------------------------------------------------------------------------
# Flow Report (Legal Logger's official output)
# ---------------------------------------------------------------------------

class FlowReport(BaseModel):
    flow_id: str
    run_id: str = Field(default_factory=lambda: str(uuid4()))
    execution_id: Optional[str] = None
    execution_report_id: Optional[str] = None
    what_happened: str
    why_it_happened: str
    who_was_involved: list[str]
    actors_run: list[str]
    actions_used: int
    what_failed: Optional[str] = None
    what_was_learned: Optional[str] = None
    recommendation_for_next_run: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# ---------------------------------------------------------------------------
# Execution Report — raw per-run telemetry, the foundation everything else
# (Flow Report, Flow Profile) is built from. This is Legal Logger's lowest
# level of record; nobody else writes one.
# ---------------------------------------------------------------------------

class ExecutionReport(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    execution_id: str
    flow_id: str
    run_id: str  # ties this execution to its FlowReport
    actor_chain: list[str] = Field(default_factory=list)
    flow_chain: list[str] = Field(default_factory=list)
    actions_used: int = 0
    estimated_actions: int = 0
    runtime_ms: float = 0.0
    models_used: list[str] = Field(default_factory=list)
    workers_used: list[str] = Field(default_factory=list)
    cache_hits: int = 0
    cache_misses: int = 0
    errors: list[str] = Field(default_factory=list)
    retries: int = 0
    recovered: bool = False
    success: bool
    human_review_required: bool = False
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# ---------------------------------------------------------------------------
# Flow Profile — the living, aggregated document per flow. Updated
# incrementally by Legal Logger after every Execution Report. This is the
# evidence base Big Bear will eventually read from instead of asking actors
# directly.
# ---------------------------------------------------------------------------

class FlowProfile(BaseModel):
    flow_id: str
    version: str = "0.1.0"
    total_runs: int = 0
    avg_actions: float = 0.0
    min_actions: Optional[int] = None
    max_actions: Optional[int] = None
    avg_runtime_ms: float = 0.0
    success_count: int = 0
    failure_count: int = 0
    recovery_count: int = 0
    human_review_count: int = 0
    success_rate: float = 0.0
    failure_rate: float = 0.0
    recovery_rate: float = 0.0
    human_review_rate: float = 0.0
    common_failures: dict[str, int] = Field(default_factory=dict)
    common_recoveries: dict[str, int] = Field(default_factory=dict)
    optimization_suggestions: list[str] = Field(default_factory=list)
    last_updated: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def record(self, execution: ExecutionReport) -> None:
        """Incrementally fold one Execution Report into this profile."""
        n = self.total_runs

        self.avg_actions = (self.avg_actions * n + execution.actions_used) / (n + 1)
        self.avg_runtime_ms = (self.avg_runtime_ms * n + execution.runtime_ms) / (n + 1)
        self.min_actions = (
            execution.actions_used
            if self.min_actions is None
            else min(self.min_actions, execution.actions_used)
        )
        self.max_actions = (
            execution.actions_used
            if self.max_actions is None
            else max(self.max_actions, execution.actions_used)
        )

        self.total_runs = n + 1
        if execution.success:
            self.success_count += 1
        else:
            self.failure_count += 1
        if execution.recovered:
            self.recovery_count += 1
        if execution.human_review_required:
            self.human_review_count += 1

        for err in execution.errors:
            self.common_failures[err] = self.common_failures.get(err, 0) + 1
        if execution.recovered:
            for err in execution.errors:
                self.common_recoveries[err] = self.common_recoveries.get(err, 0) + 1

        self.success_rate = self.success_count / self.total_runs
        self.failure_rate = self.failure_count / self.total_runs
        self.recovery_rate = (
            self.recovery_count / self.failure_count if self.failure_count else 0.0
        )
        self.human_review_rate = self.human_review_count / self.total_runs

        self.last_updated = datetime.now(timezone.utc)


# ---------------------------------------------------------------------------
# Actor Context — every actor receives the same shape of context, not just
# a prompt. Built by Direct Dispatch before each handler call.
# ---------------------------------------------------------------------------

class ActorContext(BaseModel):
    actor_id: str
    actor_version: str = "0.1.0"
    execution_id: str
    session_id: Optional[str] = None
    load_id: Optional[str] = None
    driver_id: Optional[str] = None
    company_id: Optional[str] = None
    current_flow: Optional[str] = None
    current_permissions: list[Permission] = Field(default_factory=list)
    current_truth_context: list[Claim] = Field(default_factory=list)
    current_logbooks: list[str] = Field(default_factory=list)
    current_reports: list[str] = Field(default_factory=list)
    current_action_budget: Optional[int] = None


# ---------------------------------------------------------------------------
# Flow Result — what every flow execution returns to CoDriver. Notice that
# most of this is produced by Legal Logger, not by the actor itself.
# ---------------------------------------------------------------------------

class FlowResult(BaseModel):
    execution_id: str
    result: dict[str, Any] = Field(default_factory=dict)
    flow_report_id: str
    execution_report_id: str
    logbook_refs: list[str] = Field(default_factory=list)
    actions_used: int
    estimated_actions: int
    truth_labels: list[Claim] = Field(default_factory=list)
    completed: bool
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Actor response envelope — what every actor returns to Direct Dispatch
# ---------------------------------------------------------------------------

class ActorResponse(BaseModel):
    actor: str
    flow_id: str
    success: bool
    claims: list[Claim] = Field(default_factory=list)
    requires_human_approval: bool = False
    approval_reason: Optional[str] = None
    logbook_entries: list[LogbookEntry] = Field(default_factory=list)
    actions_used: int = 0
    error: Optional[str] = None
    raw: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Telemetry — observability, not logging. "What actually happened during
# this Flow?" Every event carries an execution_id so the whole chain can be
# reconstructed later. Telemetry PUBLISHES; Legal Logger SUBSCRIBES. Neither
# one calls the other directly.
# ---------------------------------------------------------------------------

class TelemetryLayer(str, Enum):
    SYSTEM = "system"
    ACTOR = "actor"
    FLOW = "flow"
    WORKER = "worker"
    LLM = "llm"
    BROWSER = "browser"
    OCR = "ocr"
    SEARCH = "search"


class TelemetryEvent(BaseModel):
    """The generic envelope every telemetry publication uses. `payload`
    holds the layer-specific typed data (see the *Telemetry payload models
    below), dumped to a dict so the envelope itself stays uniform."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    execution_id: str
    layer: TelemetryLayer
    event_type: str  # e.g. "actor_entered", "llm_call", "browser_navigation"
    source: str       # actor name, worker name, or "CoDriver" / "Direct Dispatch"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    runtime_ms: Optional[float] = None
    payload: dict[str, Any] = Field(default_factory=dict)


class SystemTelemetry(BaseModel):
    cpu_time_ms: Optional[float] = None
    memory_mb: Optional[float] = None
    runtime_ms: Optional[float] = None
    queue_wait_ms: Optional[float] = None
    queue_depth: Optional[int] = None
    thread: Optional[str] = None
    worker_id: Optional[str] = None


class ActorTelemetry(BaseModel):
    actor: str
    runtime_ms: Optional[float] = None
    actions_used: int = 0
    agent_count: int = 0
    flow_count: int = 0


class FlowTelemetry(BaseModel):
    flow_id: str
    estimated_actions: int
    actual_actions: int
    estimated_runtime_ms: Optional[float] = None
    actual_runtime_ms: Optional[float] = None

    @property
    def action_delta(self) -> int:
        return self.actual_actions - self.estimated_actions


class LLMTelemetry(BaseModel):
    """Captured for optimization, not billing."""

    model: str
    provider: str
    prompt_tokens: int
    completion_tokens: int
    context_size: int
    temperature: Optional[float] = None
    runtime_ms: float
    retry_count: int = 0
    cache_hit: bool = False


class BrowserTelemetry(BaseModel):
    """Packet Pilot's goldmine."""

    page_load_ms: Optional[float] = None
    selector_failures: int = 0
    retry_count: int = 0
    js_errors: list[str] = Field(default_factory=list)
    dom_mutations: int = 0
    captcha_detected: bool = False
    navigation_count: int = 0


class OCRTelemetry(BaseModel):
    pages: int
    confidence: float = Field(ge=0.0, le=1.0)
    tables_found: int = 0
    signatures_found: int = 0
    handwriting_found: bool = False


class SearchTelemetry(BaseModel):
    sources_searched: int
    sources_accepted: int
    sources_rejected: int
    runtime_ms: float


# ---------------------------------------------------------------------------
# Timeline — not logs. A reconstructed, human-readable chain of events for
# one execution_id.
# ---------------------------------------------------------------------------

class TimelineEntry(BaseModel):
    timestamp: datetime
    source: str
    event: str
    detail: Optional[str] = None
