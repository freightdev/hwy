# Agent Builder Architecture

CoDriver is the builder of Agents when Actors lack required capabilities.

The source CoDriver architecture document lives at:

```text
moonrust/markers/codriver/ARCHITECTURE.md
```

This document explains the Agent Builder responsibility in encyclopedia form.

This does not mean CoDriver owns every domain.

It means CoDriver detects capability gaps and creates or requests the specialized Agent an Actor needs to complete work correctly.

---

## Core rule

If CoDriver asks an Actor to perform work and that Actor does not have the required capability, CoDriver should not force the Actor to fake the work.

CoDriver should build the missing Agent capability.

Agent Capability Manifests provide CoDriver's safe lookup table:

```text
moonrust/agents/<category>/<agent_name>/manifest.yaml
```

See:

```text
docs/ARCHITECTURE/AGENT_MANIFESTS.md
```

---

## Ownership boundaries

### CoDriver owns

- User request understanding.
- Capability-gap detection.
- Agent catalog search.
- Agent Builder flow initiation.
- Agent architecture draft creation when no Agent exists.
- Routing the new capability back to the correct Actor boundary.

### Actor owns

- Business domain.
- Domain-specific decision making.
- Which capabilities are needed to complete domain work.
- Whether an Agent's output satisfies the Actor's business responsibility.

### Agent owns

- Specialized capability.
- Inputs and outputs for that capability.
- Capability-specific rules.
- Capability-specific risk and review requirements.

### Worker owns

- Mechanical operation.
- Tool execution.
- Low-level repeatable tasks.

---

## Agent Builder flow

```text
User asks CoDriver
↓
CoDriver understands intent
↓
Direct Dispatch selects Actor
↓
Actor lacks capability
↓
CoDriver identifies capability gap
↓
CoDriver searches moonrust/agents/**
↓
CoDriver loads Agent Capability Manifests
↓
Existing Agent found?
├── yes
│   ↓
│   Route Actor through existing Agent boundary
│
└── no
    ↓
    Create new Agent architecture draft
    ↓
    Define identity, mission, inputs, outputs, risk, review, cannot-do rules
    ↓
    Attach to future Actor capability map when schema supports it
    ↓
    Runtime implementation comes later
```

---

## What CoDriver must not do

CoDriver must not:

- Pretend the Actor has a capability it does not have.
- Stuff the capability directly into the Actor for convenience.
- Treat a new Agent architecture document as runtime permission.
- Bypass Actor ownership.
- Bypass Legal Logger.
- Bypass Key Keeper, Secret Safe, Unit Usage, or Memory Mark for sensitive work.
- Create an Agent without a clear owner, mission, input/output boundary, and cannot-do list.

---

## Agent architecture requirements

A new Agent architecture document should live at:

```text
moonrust/agents/<category>/<agent_name>/ARCHITECTURE.md
```

It should define:

- Identity.
- Mission.
- Capability owned.
- Inputs.
- Outputs.
- Allowed callers.
- Allowed callees if any.
- Dependencies.
- Risk level.
- Human review requirements.
- Truth rules.
- Logbooks affected.
- Reports affected.
- What the Agent cannot do.

---

## Runtime future

Later phases may add:

- Agent manifests.
- Agent capability registry.
- Agent Runtime.
- Actor Manifest `allowed_agents` fields.
- Agent permission checks.
- Agent health monitoring.
- Agent timeline events.

Do not add those fields or runtime paths until the architecture needs them.

---

## Principle

Actors own domains.

Agents supply capabilities.

CoDriver builds missing Agents so Actors can do their jobs.

Workers execute mechanical operations.

Legal Logger preserves truth.
