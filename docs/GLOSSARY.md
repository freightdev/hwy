# HWY Glossary

HWY has its own vocabulary.

This glossary keeps humans and AI agents using the same words the same way.

If a term changes meaning, update this file and any affected architecture documents.

---

## Action

A measured unit of work.

Actions help HWY understand cost, effort, usage, and operational weight.

Actions are not the same as Flows. A Flow may contain many Actions.

---

## Actor

A domain owner inside HWY.

Actors own business responsibilities.

Examples:

- Packet Pilot owns paperwork.
- Legal Logger owns official reports and preserved truth.
- Cargo Connect owns freight discovery.
- Error Echo owns active recovery.
- Big Bear owns root-cause investigation after recovery.

Actors should not steal responsibility from other actors.

---

## Actor Runtime

The runtime layer responsible for actor lifecycle.

Owns:

- Actor registration.
- Actor startup.
- Actor shutdown.
- Actor health.
- Actor capability lookup.
- Actor invocation boundaries.

Does not own actor business decisions.

---

## Agent

A specialist capability operating inside or for an Actor.

Agents perform focused work that supports Actor-owned domains.

Agents do not own the entire domain; the Actor owns the domain.

Agents are the capabilities Actors use to build, reason, analyze, verify, communicate, and operate.

Moonrust agent architecture lives under:

```text
moonrust/agents/<category>/<agent_name>/ARCHITECTURE.md
```

If an Actor needs a capability that does not exist, CoDriver initiates Agent Builder flow and creates a new Agent architecture document instead of bloating the Actor.

---

## CoDriver

The AI operating console for HWY.

CoDriver owns user interaction, intent understanding, context, response presentation, and command control.

CoDriver also initiates Agent Builder flow when an Actor cannot satisfy a requested capability with existing Agents.

CoDriver is not the entire platform.

CoDriver is the first application running on the HWY runtime.

---

## Direct Dispatch

The routing layer between CoDriver and runtime execution.

Direct Dispatch owns routing, actor selection, flow-chain selection, and execution coordination.

Direct Dispatch should remain a router.

It should not become a god object or the whole operating system.

---

## Event

A coordination signal that something happened or needs to happen.

Examples:

- ExecutionStarted.
- FlowStarted.
- ActorStarted.
- WorkerStarted.
- ApprovalRequested.
- FlowCompleted.
- FlowFailed.
- ReportPublished.

Events coordinate.

Telemetry measures.

---

## Event Bus

The runtime mechanism for publishing and subscribing to Events.

The Event Bus helps runtime components coordinate without hardwiring everything together.

---

## Execution

A runtime instance of work.

Every meaningful runtime operation should have an Execution ID.

Execution includes lifecycle, state, cancellation, retry, timeout, timeline, telemetry, and result handling.

---

## Execution ID

A unique identifier for a runtime execution.

Execution IDs make work traceable, replayable, measurable, and reportable.

---

## Execution Report

An official report describing an execution.

Legal Logger owns official Execution Reports.

Execution Runtime provides evidence and events.

Legal Logger writes the report.

---

## Execution Runtime

The runtime layer responsible for execution lifecycle.

Owns:

- Execution IDs.
- Start.
- Stop.
- Cancellation.
- Retry.
- Timeout.
- Runtime state.
- Runtime health.
- Execution events.
- Execution accounting.

Does not own actor business logic.

---

## Flow

A callable business process.

Flows perform repeatable business work.

A Flow may call Agents and Workers through the proper Actor boundary.

Every Flow should produce a FlowResult.

Every Flow should produce a Flow Report through Legal Logger.

---

## Flow Profile

A learned profile of a Flow across executions.

Flow Profiles are built from Flow Reports, telemetry, outcomes, warnings, recoveries, and recommendations.

Flow Profiles help future executions perform better.

---

## Flow Report

An official report describing what happened during a Flow.

A Flow Report explains:

- What happened.
- Why it happened.
- Who was involved.
- Which Actor ran.
- Which Agents ran.
- Which Workers ran.
- Actions used.
- Runtime.
- Warnings.
- Failures.
- Recoveries.
- Lessons learned.
- Recommendations for next execution.

Legal Logger owns official Flow Reports.

---

## FlowResult

The normalized runtime result of a Flow.

A FlowResult returns structured outcome data back through the runtime to CoDriver.

FlowResult is not the same as a Flow Report.

The FlowResult is operational output.

The Flow Report is official history and analysis.

---

## HWY

Highway Workflow Yarddog.

An AI-powered trucking operating platform.

HWY uses trucking as the first domain to prove a more general runtime architecture.

---

## Knowledge

Structured learning derived from runtime evidence.

Knowledge should come from Flow Reports, Logbooks, Flow Profiles, source-backed data, and explicitly labeled claims.

Knowledge should not be magical self-modification.

---

## Legal Logger

The official historian of HWY.

Legal Logger owns:

- Execution Reports.
- Flow Reports.
- Flow Profiles.
- Logbook entries.
- Report publication.
- Evidence preservation.

Legal Logger preserves truth.

---

## Logbook

An append-only history for an important object or process.

Everything important has a Logbook.

Examples:

- Load Logbook.
- Flow Logbook.
- Actor Logbook.
- Agent Logbook.
- Worker Logbook.
- Error Logbook.
- Security Logbook.
- Document Logbook.
- Call Logbook.
- Equipment Logbook.
- CoDriver Logbook.

Corrections create new entries.

Do not silently rewrite history.

---

## Lookout

A monitoring or observation role that watches for relevant signals, risks, or changes.

A Lookout should report observations through the correct runtime, Actor, or Logbook boundary.

A Lookout should not silently take ownership of the thing it observes.

---

## Mark

A marker-owned trace, state, capability, memory, action, or understanding.

A Mark belongs to a Marker and should be interpreted within its owning Spot and permission boundary.

Do not treat Marks as generic global notes.

---

## Marker

A Moonrust identity for an agent-like operating unit.

A Marker owns identity, behavior, memory, tools, and Marks.

Markers operate inside Spots and must respect Spot boundaries.

---

## Mission

A coordinated unit of work that may contain one or more Executions, Flows, Actors, Agents, and Workers.

Mission Runtime should coordinate mission-level lifecycle without stealing Actor or Flow ownership.

---

## Moonrust

The long-term Rust production runtime for HWY and future platforms.

Moonrust should learn from the Python reference runtime.

Moonrust should not become a second experimental codebase.

Prototype in Python.

Validate in HWY.

Measure behavior.

Rewrite proven architecture in Rust.

---

## Python Reference Runtime

The `codriver/` runtime.

This is not technical debt.

It is the reference implementation used to prove runtime architecture before Moonrust migration.

---

## Runtime

The execution foundation that actors and applications run on.

The runtime owns lifecycle, coordination, measurement, health, cancellation, retry, timeout, scheduling, and timeline reconstruction.

The runtime is the product.

CoDriver is the first application running on it.

---

## Runtime Health

A runtime view of whether execution, actors, workers, event delivery, telemetry, and reporting are functioning correctly.

Runtime Health should support monitoring, debugging, recovery, and future operations dashboards.

---

## Spot

A bounded workspace, container, jurisdiction, or ownership boundary.

A Spot can own resources, services, data, rules, permissions, capabilities, markers, marks, and responsibilities.

Inside its Spot, a Marker may act according to that Spot's rules.

Outside its Spot, the Marker must request permission from the owning or parent Spot.

---

## Telemetry

Measurement about runtime work.

Examples:

- Runtime.
- Action count.
- Worker latency.
- Token count.
- Cache hits.
- Cache misses.
- Retry count.
- Error count.
- Model used.

Telemetry measures.

Events coordinate.

---

## Timeline

A reconstructed ordered view of runtime activity.

Timeline is built from events, telemetry, execution state, and reports.

Timeline helps humans and systems understand what happened.

---

## Worker

A mechanical operation unit.

Workers should be small, observable, replaceable, and portable.

Workers do not own business domains.

Workers execute specific tasks inside Actor, Flow, and Runtime boundaries.

---

## Worker Runtime

The runtime layer responsible for Worker invocation and behavior.

Owns:

- Worker invocation.
- Worker retry.
- Worker timeout.
- Worker cancellation.
- Worker telemetry.
- Worker result normalization.

Does not own business meaning.
