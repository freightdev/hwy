# HWY packages

Reusable package boundaries for the HWY operating system.

These packages prevent frontend pages, backend routers, CoDriver runtime code, and Moonrust migration work from sharing one-off duplicated logic.

## Current scaffold

- `auth` — identity/session contracts.
- `permissions` — roles, permission keys, policy contracts.
- `profiles` — user/company/driver/equipment profiles.
- `payments` — invoices, settlements, billing/provider abstractions.
- `ui` — mobile-first design system and app chrome.
- `codriver-contracts` — CoDriver runtime API contracts.
- `compliance` — documents, authority, audit, expiration flows.
- `shared` — cross-package errors, naming, schema conventions.

## Boundary rule

- `frontend/` owns Svelte app UI.
- `backend/` owns FastAPI APIs and persistence.
- `codriver/` owns Python reference runtime.
- `moonrust/` owns long-term Rust runtime path.
- `packages/` owns reusable contracts and library code.
