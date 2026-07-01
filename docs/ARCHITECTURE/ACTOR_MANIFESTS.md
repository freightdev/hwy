# Actor Manifests

Actor Manifests are the bridge between human architecture and runtime-readable structure.

They do not execute actors yet.

They prepare Actor Runtime and Direct Dispatch to understand actor boundaries without reverse-engineering prose.

---

## Purpose

Every actor has a human architecture document:

```text
moonrust/actors/<actor_name>/ARCHITECTURE.md
```

Every actor should also have a machine-readable manifest draft:

```text
moonrust/actors/<actor_name>/manifest.yaml
```

The architecture document explains why the actor exists.

The manifest states what the runtime is allowed to know about that actor.

---

## Source of truth

`ARCHITECTURE.md` remains the source for actor intent.

`manifest.yaml` is extracted from the architecture document.

If the architecture is unclear, the manifest must say `TODO` instead of guessing.

Do not invent responsibilities to make a manifest look complete.

A TODO is better than false authority.

---

## Manifest fields

Each manifest includes:

- `actor_id` — stable snake_case actor identifier.
- `name` — human actor name.
- `category` — broad actor category.
- `ownership_domain` — what the actor owns.
- `mission` — the question the actor exists to answer.
- `allowed_callers` — who may call this actor.
- `allowed_callees` — who this actor may call.
- `owned_flows` — flows owned by this actor.
- `allowed_flows` — flows this actor may participate in.
- `required_permissions` — permissions needed for sensitive actions.
- `risk_level` — runtime risk level.
- `truth_rules` — truth, evidence, and uncertainty rules from architecture.
- `logbooks_written` — Logbooks this actor writes or affects.
- `reports_created` — reports this actor creates or contributes to.
- `human_review_required_for` — actions requiring human review.
- `depends_on` — explicit dependencies.
- `cannot_do` — prohibited responsibilities or actions.
- `architecture_source` — path back to the source architecture document.

---

## Extraction rules

Manifest extraction must follow these rules:

1. Read the actor's `ARCHITECTURE.md`.
2. Extract only what the architecture says.
3. Preserve actor ownership boundaries.
4. Do not infer permissions from convenience.
5. Do not invent flows.
6. Do not invent callees.
7. Do not invent risk levels.
8. If unclear, write `TODO`.
9. Keep `architecture_source` pointing to the source document.
10. Validate the manifest with the Pydantic schema.

---

## Runtime relationship

Actor Manifests are schema preparation for:

- Actor Runtime.
- Direct Dispatch.
- Runtime Health.
- Permission checks.
- Flow routing.
- Human review gates.
- Logbook routing.
- Report routing.

They are not runtime execution.

No actor should be executed merely because its manifest exists.

---

## Direct Dispatch usage later

Direct Dispatch will eventually use manifests to answer:

- Which actor owns this responsibility?
- Is this actor allowed to receive this request?
- Is this actor allowed to call another actor?
- Which flows may be selected?
- Does this action require human review?
- Which Logbooks should receive entries?
- Which reports should be created?
- What must not happen?

Direct Dispatch should use manifests as boundaries, not as business logic.

---

## Actor Runtime usage later

Actor Runtime will eventually use manifests to answer:

- How should this actor be registered?
- What lifecycle policies apply?
- What risk level should runtime health surface?
- Which permissions must be checked before invocation?
- Which actor boundaries should be monitored?

Actor Runtime should not decide actor ownership from scratch.

It should read ownership from manifests that were extracted from architecture.

---

## Validation code

Pydantic schema:

```text
codriver/registry/actor_manifest_schema.py
```

Manifest loader:

```text
codriver/registry/load_manifests.py
```

The loader validates every `manifest.yaml` under an actors directory.

Example:

```python
from pathlib import Path
from codriver.registry.load_manifests import load_actor_manifests

manifests = load_actor_manifests(Path("moonrust/actors"))
```

---

## Current status

Current manifests are drafts.

Many fields intentionally contain `TODO` because the actor architecture does not yet specify runtime permissions, flow ownership, allowed callers, allowed callees, or risk level with enough precision.

That is correct.

The next architecture pass should replace TODO values only when the source architecture clearly grants that responsibility.

---

## Rule

Never use a manifest to smuggle new authority into an actor.

Architecture first.

Manifest second.

Runtime execution third.
