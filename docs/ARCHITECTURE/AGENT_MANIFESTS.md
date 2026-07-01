# Agent Capability Manifests

Agent Capability Manifests are the machine-readable lookup table for CoDriver Agent Builder.

They convert human Agent architecture documents into structured capability drafts.

They do not wire runtime behavior.

They do not grant execution authority.

They prepare CoDriver to safely answer:

```text
Actor needs capability → existing Agent found or new Agent draft required
```

---

## Source documents

Every Moonrust Agent has a human architecture document:

```text
moonrust/agents/<category>/<agent_name>/ARCHITECTURE.md
```

Every Agent should also have a capability manifest draft:

```text
moonrust/agents/<category>/<agent_name>/manifest.yaml
```

The architecture document explains why the Agent exists.

The manifest states what CoDriver may search about that Agent.

---

## Current status

At the time this document was created:

- 317 Agent architecture documents existed.
- 317 Agent capability manifests were generated.
- These manifests are drafts.
- Unclear fields intentionally use `TODO`.

A TODO is safer than invented authority.

---

## Manifest fields

Each Agent manifest includes:

- `agent_id` — stable category-prefixed identifier, such as `advanced.intent-classifier`.
- `name` — human name.
- `category` — top-level catalog category.
- `capability_domain` — capability owned by the Agent.
- `mission` — what the Agent exists to do.
- `inputs` — accepted input shape or TODO.
- `outputs` — produced output shape or TODO.
- `allowed_callers` — callers allowed to request this Agent.
- `allowed_actors` — Actors allowed to use this Agent.
- `required_permissions` — permissions required by the Agent.
- `risk_level` — risk classification.
- `tools_needed` — dependencies or tools the Agent needs.
- `workers_needed` — Workers the Agent needs.
- `truth_rules` — truth, confidence, uncertainty, or verification rules.
- `logbooks_written` — Logbooks written or affected.
- `reports_contributed_to` — reports the Agent contributes to.
- `human_review_required_for` — actions requiring human review.
- `cannot_do` — explicit prohibitions.
- `architecture_source` — path back to the source `ARCHITECTURE.md`.

---

## Extraction rules

Manifest extraction follows these rules:

1. Read the Agent's `ARCHITECTURE.md`.
2. Extract only what the architecture says.
3. Do not invent capabilities.
4. Do not invent permissions.
5. Do not invent allowed Actors.
6. Do not invent runtime authority.
7. If unclear, write `TODO`.
8. Keep `architecture_source` pointing to the source document.
9. Validate with the Pydantic schema.

---

## CoDriver Agent Builder usage

CoDriver Agent Builder should use Agent manifests like this:

```text
Actor capability gap detected
↓
Load Agent Capability Manifests
↓
Search by capability_domain, mission, inputs, outputs, category, tools_needed
↓
Existing Agent found?
├── yes → route capability request through Agent boundary later
└── no  → create new Agent architecture draft
```

The manifest is a search and validation layer.

It is not runtime execution.

---

## Validation code

Pydantic schema:

```text
codriver/registry/agent_manifest_schema.py
```

Manifest loader:

```text
codriver/registry/load_agent_manifests.py
```

Generator script:

```text
scripts/generate_agent_manifests.py
```

Tests:

```text
tests/test_agent_manifest_registry.py
```

---

## Future phases

Future work may add:

- Agent capability search API.
- Agent Builder planner.
- Agent manifests referenced from Actor manifests.
- Agent Runtime.
- Agent health checks.
- Agent event timeline integration.
- Agent permission enforcement.

Do not add these until the architecture requires them.

---

## Rule

Architecture first.

Manifest second.

Search third.

Runtime wiring later.
