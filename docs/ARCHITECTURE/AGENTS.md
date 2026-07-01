# Agent Architecture

Agents are capabilities that Actors use.

Actors own domains.

Agents specialize inside or for Actors.

Workers perform mechanical operations.

This distinction matters because the repository now contains a large Moonrust agent catalog:

```text
moonrust/agents/**
```

At the time this document was created, that catalog contained 317 agent architecture documents.

---

## Why agents exist

Actors should not become bloated with every capability they might need.

An Actor should own the business domain.

Agents should provide specialized capability.

If an Actor needs to classify intent, validate a response, check risk, translate language, run a smoke test, count tokens, analyze anomalies, or perform another reusable specialty, the Actor should use an Agent instead of absorbing that responsibility directly.

---

## Actor vs Agent

### Actor

An Actor owns a domain.

Examples:

- Packet Pilot owns paperwork operations.
- Cargo Connect owns freight discovery.
- Legal Logger owns official reports and preserved truth.
- Error Echo owns active failure recovery.
- Big Bear owns root-cause investigation after recovery.

Actors answer:

```text
Who owns this responsibility?
```

### Agent

An Agent owns a specialized capability that may help one or more Actors.

Examples from the Moonrust catalog include:

- intent-classifier
- risk-assessor
- root-cause-analyzer
- translator
- response-validator
- token-counter
- deployment-verifier
- webhook-handler

Agents answer:

```text
Which capability is needed to perform this work correctly?
```

---

## Agent catalog location

The Moonrust agent catalog lives under:

```text
moonrust/agents/<category>/<agent_name>/ARCHITECTURE.md
```

Top-level categories currently include:

- advanced
- ai-ml
- business
- cicd
- communication
- content
- data
- database
- developer-tools
- devops
- finance
- generic
- geospatial
- infra
- network
- scientific
- security
- specialized
- system
- testing
- utility

---

## Agent usage rule

Before creating a new capability inside an Actor, check whether an Agent already exists.

If the Agent exists, route the capability through that Agent boundary.

If the Agent does not exist, CoDriver should initiate the Agent Builder flow.

CoDriver is responsible for recognizing the gap between what it is asking an Actor to do and what that Actor's current Agents can support.

Do not add capability directly to an Actor just because it is convenient.

---

## CoDriver as Agent Builder

CoDriver is the operating console and the capability-gap detector.

When CoDriver asks an Actor to perform work and the Actor lacks a required capability, CoDriver should not force the Actor to fake it.

CoDriver should:

1. Identify the missing capability.
2. Search `moonrust/agents/**` for an existing Agent.
3. If an Agent exists, route the Actor to use that Agent.
4. If no Agent exists, create a new Agent architecture document.
5. Attach the new Agent to the Actor's future capability map.
6. Preserve actor ownership: the Actor still owns the business domain.
7. Preserve agent ownership: the Agent owns the specialized capability.
8. Preserve worker ownership: Workers still perform mechanical operations.

CoDriver builds or requests Agents so Actors can do their jobs.

CoDriver does not absorb the Actor's domain.

CoDriver does not silently grant the new Agent runtime authority.

Architecture comes before runtime wiring.

---

## Agent Builder flow

```text
CoDriver request
↓
Direct Dispatch selects Actor
↓
Actor capability gap detected
↓
CoDriver searches Agent catalog
↓
Existing Agent found?
├── yes → route Actor through Agent boundary
└── no  → create Agent architecture draft
          ↓
          document ownership, inputs, outputs, risk, review
          ↓
          update future manifest/capability map when schema supports it
          ↓
          runtime implementation later
```

The Agent Builder flow is not an excuse to generate code immediately.

First build the Agent's architecture.

Then validate whether the Agent belongs in the catalog.

Then wire runtime behavior.

---

## Agent creation rule

When a new Agent is needed, create:

```text
moonrust/agents/<category>/<agent_name>/ARCHITECTURE.md
```

The architecture document should explain:

- Identity.
- Mission.
- Capability owned.
- Inputs.
- Outputs.
- Allowed callers.
- Dependencies.
- Risk level.
- Human review requirements.
- What the Agent cannot do.

Agent architecture comes before agent runtime implementation.

---

## Relationship to Actor Manifests

Actor Manifests should eventually reference allowed or required Agents.

Today, Actor Manifests define Actor authority.

Future manifest phases may add fields such as:

- `allowed_agents`
- `required_agents`
- `agent_permissions`
- `agent_risk_rules`

Do not add those fields until the runtime needs them and the architecture is clear.

---

## Relationship to Moonrust

The agent catalog is part of the Moonrust operating runtime direction.

Agents are not random helper scripts.

They are named capabilities that Actors can compose.

As Moonrust matures, Agent Runtime should be able to discover, validate, invoke, monitor, and report agent capability usage.

---

## Rule

Actors own domains.

Agents own capabilities.

Workers execute mechanical operations.

Do not collapse these layers.
