# @hwy/codriver-contracts

Shared contracts between frontend/backend and CoDriver runtime.

## Ownership

This package is a scaffolded boundary for reusable HWY platform code. Keep route-specific UI in `frontend/`, API execution in `backend/`, runtime behavior in `codriver/`, and production-runtime migration work in `moonrust/`.

## Initial contracts

- Public interfaces live under `src/`.
- Package internals must not import Svelte routes or FastAPI routers directly.
- Backend and frontend adapters may consume these contracts.
