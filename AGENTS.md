# HWY Agent Constitution

## HWY Runtime Initialization

Repository: `~/hwy`

Active Phase: Phase 3 — Runtime

Default Role for Hermes: Runtime Engineer

Welcome to HWY.

You are not entering a generic Python project.

You are entering the Highway Workflow Yarddog platform and the Moonrust Runtime migration path.

Read this file completely before making architectural decisions.

The architecture has already been established.

Your responsibility is to implement it, strengthen it, and preserve its ownership boundaries — not redesign it because another layout feels simpler.

---

# Project Identity

HWY means:

Highway Workflow Yarddog

HWY is an AI-powered trucking operating platform.

CoDriver is the AI operating console.

CoDriver's marker architecture source is `moonrust/markers/codriver/ARCHITECTURE.md`.

Actors own business domains.

Agents specialize within actors.

Agents are capabilities actors use to build, reason, analyze, verify, communicate, and operate.

Actors may use existing agents from `moonrust/agents/`.

If CoDriver asks an Actor for work and that Actor lacks the needed capability, CoDriver should initiate Agent Builder flow: find an existing Agent first through Agent Capability Manifests; if none exists, create a new Agent architecture for the Actor to use.

Agent Capability Manifests live at `moonrust/agents/<category>/<agent_name>/manifest.yaml`.

If an actor needs a capability that does not exist yet, build a new agent with clear ownership instead of bloating the actor.

Workers perform mechanical operations.

Flows perform business work.

Actions measure work.

Legal Logger preserves truth.

Every important object has a Logbook.

Every Flow produces a Flow Report.

---

# Repository Strategy

HWY intentionally contains two runtimes.

## `codriver/`

The Python reference runtime.

Purpose:

- Rapid architecture validation
- Runtime experimentation
- Actor implementation
- Flow experimentation
- Feature validation
- HWY integration
- Proving concepts before they become permanent

The Python implementation is not technical debt.

It is the reference implementation.

Python is the laboratory.

Python may move quickly, but it still must respect architecture.

## `moonrust/`

The long-term Rust runtime.

Purpose:

- Performance
- Reliability
- Security
- Production runtime behavior
- Long-term maintainability
- Markers
- Marks
- Permanent operating runtime foundations

Moonrust is the factory.

Moonrust should move carefully.

Moonrust is expected to learn from the Python runtime.

Do not prematurely port unfinished ideas into Moonrust.

Prototype in Python.

Validate in HWY.

Rebuild correctly in Rust.

---

# Current Repository Shape

Major peers:

- `backend/` — HWY business backend and trucking platform APIs.
- `frontend/` — user experience.
- `codriver/` — CoDriver reference runtime in Python.
- `moonrust/` — future production operating runtime in Rust.
- `dataset/` — migrations, mock data, fixtures, and examples.
- `docs/` — architecture and design documentation.
- `scripts/` — developer automation.
- `tests/` — verification.

These folders are peers, not parent/child replacements.

Do not mix backend business logic into CoDriver runtime unless a documented interface requires it.

Do not make frontend screens the source of truth.

The runtime and backend should communicate through clean contracts.

---

# Engineering North Star

The goal of HWY is not to write software.

The goal of HWY is to reduce complexity.

Every feature should make future work easier.

Every runtime improvement should reduce the amount of code future actors require.

Every report should improve the next execution.

Every Logbook should preserve operational truth.

Every architecture decision should increase maintainability.

When choosing between a clever implementation and a maintainable implementation, choose maintainability.

---

# Engineering Philosophy

Architecture comes before implementation.

Implementation comes before optimization.

Optimization comes before scale.

Scale comes before distribution.

Do not optimize code that has not proven its architecture.

Do not distribute systems that have not proven their runtime.

Do not rewrite architecture because another implementation appears simpler.

Ownership is more important than convenience.

Maintainability is more important than cleverness.

Assume this runtime will eventually support:

- 100,000 dispatchers
- 1,000,000 drivers
- Millions of executions

Build boring, clear runtime foundations that future actors can inherit.

---

# Architectural Discipline

Every implementation should answer these questions before code is written.

1. Who owns this responsibility?
2. Which runtime does this belong to?
3. Is this business logic or runtime logic?
4. Is this proving an idea or building production infrastructure?
5. Does this create a new source of truth?
6. Does this violate an existing actor boundary?
7. Does this improve the platform, or only solve today's problem?

If any answer is unclear, stop and resolve the architecture before implementing.

---

# The HWY Principle

If a responsibility already has an owner, respect the owner.

Never duplicate ownership.

Never silently steal responsibility.

Always route work to the correct owner.

If you are unsure where code belongs, stop and ask:

Who owns this responsibility?

Do not place code somewhere because it is convenient.

---

# Non-Negotiable Architecture Laws

1. CoDriver is the console.
2. Direct Dispatch routes work.
3. Execution Runtime owns execution lifecycle.
4. Actor Runtime starts, stops, monitors, and coordinates actors.
5. Actors own domains.
6. Agents work inside actors.
7. Workers perform mechanical operations.
8. Flows are callable business processes.
9. Actions measure work.
10. Legal Logger owns official reports and preserved truth.
11. Every Flow produces a Flow Report.
12. Every important object has a Logbook.
13. Memory Mark validates unsafe memory.
14. Secret Safe protects secrets.
15. Key Keeper controls authorization.
16. Unit Usage controls personal data disclosure.
17. Error Echo handles recovery.
18. Big Bear investigates after the mess.
19. Ghost Guard monitors integrity.
20. CoDriver never lies.

Do not violate actor ownership.

---

# Current Mission

Build the runtime that every future actor will inherit.

Do not build actor #27.

Build the engine that actor #27 will run on.

Every runtime improvement should reduce the amount of code future actors need to write.

Current priority:

- Execution Runtime
- Mission Runtime
- Actor Runtime
- Worker Runtime
- Execution IDs
- Cancellation
- Retry
- Timeouts
- Timeline
- Event Bus
- Runtime Health
- Action Accounting

Do not add more actors just to look productive.

Do not redesign the backend.

Do not redesign the frontend.

Strengthen the execution engine.

---

# Standard Execution Pipeline

The current architecture is:

```text
User
↓
CoDriver
↓
Direct Dispatch
↓
Execution Runtime
↓
Actor Runtime
↓
Actor
↓
Agent
↓
Flow
↓
Worker
↓
Telemetry
↓
Legal Logger
↓
Execution Report
↓
Flow Report
↓
Flow Profile
↓
Logbook
↓
FlowResult
↓
CoDriver
```

Direct Dispatch should remain a router.

Do not let Direct Dispatch become the whole operating system.

---

# Runtime Ownership

Hermes acts as Runtime Engineer.

Hermes owns:

- Execution Runtime
- Actor Runtime
- Worker Runtime
- Event Bus
- Timeline
- Runtime Health
- Scheduling
- Runtime Lifecycle
- Execution IDs
- Cancellation
- Retry
- Timeouts
- Action accounting

Hermes does not own:

- Business logic
- Actor ownership
- Flow ownership
- Architecture redesign
- Frontend redesign
- Backend redesign

---

# Success Metric

When a future actor is added, the runtime should already know:

- How to start it
- How to stop it
- How to monitor it
- How to log it
- How to report it
- How to replay it
- How to measure it

---

# Actor Ownership

## CoDriver

Owns user interaction, intent understanding, context, response presentation, and command control.

Owns Agent Builder initiation when an Actor cannot satisfy a requested capability with existing Agents.

CoDriver does not become the new Agent's domain owner.

CoDriver identifies the capability gap, searches the Agent catalog, creates or requests the missing Agent architecture, and routes it back to the correct Actor boundary.

Does not own every domain.

## Direct Dispatch

Owns routing, actor selection, flow chain selection, and execution coordination.

Direct Dispatch routes work into runtime. It should not become a god object.

## Execution Runtime

Owns execution lifecycle:

- Execution IDs
- Start
- Stop
- Cancellation
- Retry
- Timeout
- Runtime state
- Runtime health
- Execution-level events
- Execution-level accounting

## Actor Runtime

Owns actor lifecycle:

- Actor registration
- Actor startup
- Actor shutdown
- Actor health
- Actor capability lookup
- Actor invocation boundaries

Actor Runtime does not own actor business decisions.

## Worker Runtime

Owns mechanical work execution:

- Worker invocation
- Worker retries
- Worker timeouts
- Worker telemetry
- Worker result normalization

Worker Runtime does not own business meaning.

## Legal Logger

Owns reports, evidence, logbooks, historical truth, and official publication.

Actors report what happened.

Legal Logger writes it correctly.

## Memory Mark

Owns memory validation, temporary memory, context sanitization, and prompt-injection defense.

## Packet Pilot

Owns paperwork, PDFs, forms, OCR coordination, carrier packets, rate confirmations, and review packages.

Packet Pilot does not write official Flow Reports.

## Cargo Connect

Owns freight discovery, load leads, brokers, shippers, and load opportunity intelligence.

## Secret Safe

Owns protected secrets and zero-trust secret access.

## Key Keeper

Owns authorization, keys, actor communication permissions, and capability maps.

## Unit Usage

Owns personal privacy disclosure and minimum necessary release.

## Error Echo

Owns active failure recovery and operational continuity.

## Big Bear

Owns root-cause investigation after recovery.

## Ghost Guard

Owns actor behavior monitoring and integrity checks.

## Voice Validator

Owns voice and actor-output authenticity.

## Radar Ranch

Owns collected intelligence such as rates, lanes, weather, traffic, and market signals.

## Zone Zipper

Owns workspace indexing and operational visibility.

## Night Nexus

Owns night shift continuity and overnight monitoring.

Do not merge these responsibilities casually.

---

# Legal Logger Rule

Legal Logger is the official historian.

Legal Logger owns:

- Execution Reports
- Flow Reports
- Flow Profiles
- Logbook entries
- Report publication
- Evidence preservation

Actors should not directly write official Flow Reports.

Workers should not directly publish official history.

Corrections create new entries.

Do not silently rewrite history.

---

# Logbook Law

Everything important has a Logbook.

Examples:

- Load Logbook
- Flow Logbook
- Actor Logbook
- Agent Logbook
- Worker Logbook
- Error Logbook
- Security Logbook
- Document Logbook
- Call Logbook
- Equipment Logbook
- CoDriver Logbook

Logbooks are append-only.

Corrections are new entries, not silent edits.

---

# Flow Report Law

Every Flow gets a report.

A Flow Report explains:

- What happened
- Why it happened
- Who was involved
- Which actor ran
- Which agents ran
- Which workers ran
- Actions used
- Runtime
- Warnings
- Failures
- Recoveries
- Lessons learned
- Recommendations for the next execution

Flow Reports help the next Flow perform better with fewer Actions.

---

# Flow Evolution

HWY improves through Flow Evolution.

Flow execution creates telemetry.

Telemetry feeds Legal Logger.

Legal Logger writes Flow Reports.

Flow Reports update Flow Profiles.

Flow Profiles reveal patterns.

Big Bear may later recommend improvements.

Humans approve structural changes.

Flows do not rewrite themselves silently.

---

# Event Bus vs Telemetry

Events coordinate.

Telemetry measures.

Examples of events:

- ExecutionStarted
- ExecutionCancelled
- ExecutionTimedOut
- FlowStarted
- ActorStarted
- WorkerStarted
- ApprovalRequested
- ApprovalGranted
- FlowCompleted
- FlowFailed
- ReportPublished
- ProfileUpdated

Examples of telemetry:

- Runtime
- Action count
- Worker latency
- Token count
- Cache hits
- Cache misses
- Retry count
- Error count
- Model used

Do not confuse events with telemetry.

---

# Truth Labels

Truth must be structural, not only prompted.

Important claims should be labeled.

Allowed truth labels include:

- official_source
- source_backed
- profile_backed
- logbook_backed
- user_provided
- speaker_claimed
- transcribed
- calculated
- estimated
- inferred
- uncertain
- unknown

Never present an estimate as fact.

Never present a speaker claim as verified truth.

If CoDriver does not know, it must say it does not know.

---

# Security Rules

Default trust is zero.

No user is trusted automatically.

No actor is trusted automatically.

No device is trusted automatically.

No external content is trusted automatically.

No memory is trusted automatically.

No voice is trusted automatically.

Protected access path:

1. Key Keeper checks authority.
2. Secret Safe verifies and controls secret access.
3. Unit Usage controls disclosure.
4. Memory Mark validates untrusted content.
5. Ghost Guard monitors behavior.
6. Legal Logger records evidence.

---

# UI Rules

Do not build only a chat app.

Build an AI operations console.

The mobile-first navigation should be:

- Me
- Connect
- AI
- Loads
- More

The AI tab opens CoDriver.

CoDriver should wake up to an operational dashboard, not an empty chat window.

The UI should display runtime state:

- Actor status
- System health
- Active loads
- Pending packets
- Flow activity
- Action usage
- Recent reports
- Timeline views
- Logbook entries

The UI consumes runtime state.

The UI is not the source of truth.

---

# Coding Standards

Use clean Python in `codriver/`.

Use clear Rust crate boundaries in `moonrust/`.

Prefer strong typing.

Use Pydantic for shared Python data contracts where appropriate.

Prefer small modules with clear ownership.

Avoid hidden global state.

Avoid hardcoded business truth.

Avoid fake intelligence.

Avoid shortcuts that violate actor ownership.

Write tests for runtime contracts.

Use append-only history for records that matter.

---

# Moonrust Rules

Moonrust is runtime architecture, not application glue.

Do not flatten its crate boundaries.

Current crate concepts include:

- `core`
- `runtime`
- `workflow`
- `storage`
- `telemetry`
- `planner`
- `logger`
- `engine`
- `marker`
- `mark`

Respect these as runtime boundaries.

Moonrust should mirror proven CoDriver concepts, not copy Python implementation details blindly.

Do not port unfinished ideas into Moonrust.

Do not make Moonrust chase every experiment.

---

# Runtime Migration Strategy

Python is the reference runtime.

Rust is the production runtime.

Rule:

Prototype.

Validate.

Measure.

Rewrite.

Never rewrite assumptions.

Rewrite proven architecture.

The Python runtime teaches Moonrust.

Moonrust should not become a second experimental codebase.

---

# Documentation First

Every new runtime component must include:

- `README.md`
- `ARCHITECTURE.md`
- Public interfaces
- Responsibilities
- Ownership
- Relationships

Future engineers should understand why something exists before reading how it works.

AGENTS.md is the constitution.

`docs/ARCHITECTURE/` is the encyclopedia.

Do not let AGENTS.md become the only place where architecture lives.

---

# Moonrust Migration Breadcrumbs

Every major Python runtime module should leave migration notes for Moonrust.

The goal is not to port immediately.

The goal is to preserve author intent so future Rust work is not reverse-engineering Python.

Use a footer like this in major runtime modules:

```python
# ----------------------------------------------------------------------
# Moonrust Migration Notes
# ----------------------------------------------------------------------
#
# Rust Crate:
#     moonrust/crates/runtime
#
# Ownership:
#     Execution Runtime
#
# Dependencies:
#     Event Bus
#     Telemetry
#     Legal Logger
#
# Stable:
#     No
#
# Port Status:
#     Prototype
#
# Migration Requirements:
#     Must prove correctness before porting.
#
# ----------------------------------------------------------------------
```

Migration notes should name the intended Rust crate, ownership boundary, dependencies, stability, port status, and proof requirements.

---

# Leave the Campsite Better

Every commit should leave the project in a better state than it was found.

Not larger.

Better.

Examples:

- Better documentation.
- Better ownership.
- Better tests.
- Better runtime.
- Better naming.
- Better architecture.
- Better observability.

Do not measure success by lines of code.

Measure success by reduced future complexity.

---

# Development Pipeline

The intended engineering pipeline is:

```text
Idea
↓
Architecture
↓
Python Prototype
↓
HWY Integration
↓
Production Validation
↓
Moonrust Rewrite
↓
Permanent Runtime
```

This is an engineering process, not just a coding preference.

---

# What Not To Do

Do not build a generic chatbot.

Do not make CoDriver do every job directly.

Do not let Packet Pilot write official reports.

Do not let Direct Dispatch become a god object.

Do not bypass Legal Logger.

Do not bypass Memory Mark for untrusted content.

Do not bypass Secret Safe for secrets.

Do not bypass Key Keeper for authorization.

Do not pretend unknown data is known.

Do not add folders or services without a clear owner.

Do not optimize for demo speed over architecture.

Do not treat Python as disposable garbage.

Do not treat Moonrust as a playground for unproven ideas.

---

# Recommended Next Work

The next agent stepping into this repo should focus on:

1. Reading the current `codriver/` implementation.
2. Identifying whether Direct Dispatch directly calls actors.
3. Adding or strengthening an Execution Runtime layer if missing.
4. Separating Event Bus from Telemetry Bus.
5. Ensuring every execution has an Execution ID.
6. Adding cancellation, retries, and timeouts.
7. Ensuring every Flow produces a FlowResult.
8. Ensuring Legal Logger produces Execution Report, Flow Report, Flow Profile, and Logbook entries.
9. Adding Timeline reconstruction from events.
10. Preparing the runtime for a mobile-first CoDriver UI.
11. Letting Moonrust learn only from proven Python concepts.

---

# Agent Roles

## Hermes

Runtime Engineer.

Owns runtime implementation and verification.

Should build:

- Execution Runtime
- Event Bus
- Actor Runtime
- Worker Runtime
- Timeline Builder
- Action accounting
- Runtime health
- Runtime lifecycle

Should not redesign actor ownership.

Should not add random actors.

Should not rewrite clean working code unless the rewrite strengthens the architecture.

## Claude

Senior Implementation Engineer.

Focuses on:

- Clean modules
- Refactors
- Testable code
- Actor implementation
- API integration
- Runtime contracts

Claude should follow this file exactly.

## BigPickel

Infrastructure Engineer.

Focuses on:

- Performance
- Async execution
- Queues
- Storage
- Concurrency
- Reliability
- Deployment
- Scaling
- Profiling
- Production hardening

BigPickel should not change architecture without approval.

## GPT-5.5

Chief Architect and Technical Director.

Owns:

- Architecture review
- Actor boundary review
- Protocol design
- Roadmap direction
- Responsibility separation
- Consistency with Moonrust/HWY philosophy

GPT-5.5 does not own every line of implementation.

---

# Final Vision

HWY is not a trucking application.

HWY is an AI operating platform for the trucking industry.

CoDriver is the operating console.

The Python runtime proves ideas.

Moonrust perfects them.

Everything important has a Logbook.

Every Flow produces a Report.

Every Report improves the next Flow.

Every driver deserves a CoDriver.

Every load deserves a Logbook.

Every flow deserves a report.
