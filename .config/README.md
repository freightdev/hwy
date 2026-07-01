# HWY configs

Fast-change configuration for agents and humans.

Use this directory instead of scattering hostnames, ports, env defaults, and test assumptions through source files.

- frontend/app.config.js: Vite/frontend host, API, allowed-host, and proxy defaults.
- env/hwy.dev.env: Docker Compose development env file.
- env/hwy.dev.env.example: redacted/shareable dev env template.
- testing/playwright.config.js: Playwright defaults for frontend/e2e tests.

Rules for future agents:

1. Change config here first.
2. Do not hardcode public hostnames or ports in route components.
3. Do not put secrets in frontend config.
4. Keep production secrets in vault/gateway-managed secret stores, not this directory.
5. If a setting affects Docker, Vite, and tests, expose it here so all three can read the same value.
