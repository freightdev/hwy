# Runtime Architecture

The runtime is the product.

CoDriver is the first application running on the runtime.

Trucking is the first domain used to prove the runtime.

Moonrust is the long-term production runtime path.

The Python runtime is the reference implementation that proves the architecture before Rust migration.

---

## Why the runtime exists

HWY should not require every Actor to reinvent execution, health, retries, timeouts, cancellation, timeline, telemetry, reporting, and lifecycle management.

The runtime exists to make future Actors cheaper, safer, and more consistent to build.

The runtime should answer:

- How does work start?
- How does work stop?
- How is work cancelled?
- How is work retried?
- How is work timed out?
- How is work monitored?
- How is work measured?
- How is work logged?
- How is work reported?
- How is work replayed?

If a future Actor is added, it should inherit these behaviors instead of implementing them from scratch.

---

## Current runtimes

### `codriver/`

Python reference runtime.

Purpose:

- Prototype runtime architecture.
- Validate Actor and Flow concepts.
- Integrate with HWY quickly.
- Produce evidence before Rust migration.
- Preserve author intent with Moonrust migration breadcrumbs.

The Python runtime is not technical debt.

It is the proving ground.

### `moonrust/`

Rust production runtime.

Purpose:

- Long-term runtime foundation.
- Performance.
- Reliability.
- Security.
- Marker and Mark operating model.
- Durable platform runtime for HWY and future domains.

Moonrust should learn from Python.

Moonrust should not become a second experimental codebase.

---

## Runtime migration principle

Prototype.

Validate.

Measure.

Rewrite.

Never rewrite assumptions.

Rewrite proven architecture.

Python is the laboratory.

Moonrust is the factory.

---

## Runtime owns

The runtime owns platform mechanics, not business meaning.

Runtime responsibilities:

- Execution lifecycle.
- Mission lifecycle.
- Actor lifecycle.
- Worker lifecycle.
- Event routing.
- Runtime health.
- Scheduling.
- Cancellation.
- Retry.
- Timeout.
- Timeline reconstruction.
- Action accounting.
- Runtime-level observability.
- Runtime result normalization.

---

## Current Python runtime modules

The current reference runtime layer lives in:

```text
codriver/runtime/
```

Current modules:

- `execution.py` — Execution IDs and lifecycle status.
- `events.py` — runtime event types and event envelope.
- `event_bus.py` — in-process runtime event publishing.
- `timeline.py` — timeline reconstruction from events.
- `actor_runtime.py` — standard actor invocation boundary.
- `health.py` — runtime health snapshot types.

This is the beginning of the engine.

It does not replace Legal Logger.

It does not replace Telemetry.

It coordinates runtime lifecycle so those systems can keep their own responsibilities.

---

## Events vs Telemetry

Events coordinate.

Telemetry measures.

Runtime events include:

- ExecutionStarted.
- ExecutionCompleted.
- ExecutionFailed.
- ExecutionCancelled.
- ExecutionTimedOut.
- FlowStarted.
- FlowCompleted.
- FlowFailed.
- ActorStarted.
- ActorCompleted.
- ActorFailed.
- ReportPublished.
- ProfileUpdated.

Telemetry still records runtime duration, action count, worker latency, token count, cache hits, retries, errors, and model usage.

Do not merge runtime events and telemetry.

---

## Runtime does not own

The runtime does not own business domains.

The runtime does not decide that Packet Pilot owns paperwork.

The architecture decides that.

The runtime enforces and supports the boundary.

The runtime does not own:

- Business logic.
- Actor domain meaning.
- Flow business purpose.
- Official report authorship.
- Secret access policy.
- Authorization policy.
- Frontend presentation.
- Database truth outside its boundary.

---

## Standard execution flow

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

This flow prevents CoDriver, Direct Dispatch, Actors, and Workers from collapsing into one large object.

---

## Relationship to CoDriver

CoDriver is the console.

CoDriver talks to the user.

CoDriver presents status, results, and decisions.

CoDriver should not personally perform every business task.

CoDriver routes work through Direct Dispatch into the runtime.

---

## Relationship to Direct Dispatch

Direct Dispatch is the router.

It selects Actors and Flow chains.

It routes requests into Execution Runtime.

Direct Dispatch should not become the runtime.

Direct Dispatch should not become a god object.

---

## Relationship to Actors

Actors own domains.

Actor Runtime owns actor lifecycle.

The runtime starts, stops, monitors, and invokes Actors.

Actors decide domain work inside their ownership boundaries.

Runtime should make Actors easier to build without stealing their meaning.

---

## Relationship to Workers

Workers perform mechanical operations.

Worker Runtime owns invocation, retry, timeout, cancellation, telemetry, and normalized results.

Workers should be small, observable, replaceable, and portable.

---

## Relationship to Legal Logger

Legal Logger preserves official truth.

Runtime provides evidence:

- Execution events.
- Timeline data.
- Telemetry.
- Worker results.
- Flow outcomes.
- Failures.
- Recoveries.

Legal Logger writes official reports and Logbook entries.

Runtime should not bypass Legal Logger for official history.

---

## Relationship to Moonrust

Moonrust is the Rust production runtime.

Moonrust should receive proven architecture from Python, not raw experiments.

Major Python runtime modules should leave Moonrust Migration Notes that identify:

- Intended Rust crate.
- Ownership.
- Dependencies.
- Stability.
- Port status.
- Migration requirements.

The goal is for future Rust engineers to read intent, not reverse-engineer Python.

---

## How the runtime evolves

Runtime evolution should follow this path:

1. Identify a repeated runtime need.
2. Confirm ownership.
3. Prototype in Python.
4. Validate inside HWY.
5. Measure behavior and failure modes.
6. Document the architecture.
7. Add migration breadcrumbs.
8. Rewrite proven architecture in Moonrust.

Do not move unstable ideas into Moonrust.

Do not keep proven runtime architecture trapped in ad hoc Python modules.

---

## Success metric

When a future Actor is added, the runtime should already know:

- How to start it.
- How to stop it.
- How to monitor it.
- How to log it.
- How to report it.
- How to replay it.
- How to measure it.

Every runtime improvement should reduce the amount of code future Actors require.
