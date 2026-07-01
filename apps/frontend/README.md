# HWY frontend

Mobile-first SvelteKit application boundary.

The frontend app now lives inside this directory:

- `src/` — routes, app shell, stores, API client, and browser runtime config.
- `static/` — public assets and `hwy-config.js` browser override.
- `tests/` — Playwright/e2e specs for frontend-visible behavior.
- `package.json` / `package-lock.json` / `node_modules/` — frontend Node dependency boundary.
- `vite.config.js` / `svelte.config.js` — frontend build/dev config.
- `Dockerfile` — frontend container build.

Fast-change config lives at the repo root under `configs/`:

- `configs/frontend/app.config.js` for Vite host/proxy/allowed-host defaults.
- `configs/env/hwy.dev.env` for Compose/local dev env.
- `configs/testing/playwright.config.js` for e2e runner config.

Root `package.json` is only an orchestration wrapper. Frontend feature work should happen here, not in the repository root.

Ownership:
- Public landing, signup, login, app shell, admin panel, and mobile chrome.
- Uses backend APIs from `backend/`.
- Uses contracts/design primitives from `packages/`.
- Does not own CoDriver runtime logic or backend persistence.
