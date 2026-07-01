# HWY CoDriver Dev Integration

This document explains the local/dev integration path for making CoDriver wake up inside HWY TMS.

This is development-only.

Do not use this for production config.

Do not commit secrets.

---

## Goal

Open HWY TMS, go to the AI tab, send a message, and see CoDriver respond through the runtime path:

```text
HWY TMS AI tab
↓
Backend CoDriver proxy
↓
CoDriver Runtime API
↓
Direct Dispatch
↓
Execution Runtime
↓
Actor Runtime
↓
Packet Pilot
↓
Legal Logger
↓
Timeline / Logbook / FlowResult
↓
HWY TMS AI tab
```

---

## Local URLs

Default dev URLs:

- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:18000/api/v1`
- CoDriver Runtime API: `http://localhost:8010`
- Postgres: `localhost:55432`

---

## Config files

Safe example:

```text
configs/env/hwy.dev.env.example
```

Local generated config:

```text
configs/env/hwy.dev.env
```

Generate `configs/env/hwy.dev.env` with:

```bash
python3 scripts/generate_dev_env.py
```

The generator may read:

```text
vault/*.json
```

It must not print secret values.

---

## Run the stack

```bash
docker compose --env-file configs/env/hwy.dev.env up --build
```

Health checks:

```bash
curl http://localhost:18000/api/v1/health
curl http://localhost:8010/health
curl http://localhost:8010/runtime/status
```

Actor activation demo:

```bash
curl -s http://localhost:8010/chat/send \
  -H 'content-type: application/json' \
  -d '{"message":"Fill a carrier packet test","session_id":"dev-demo","user_id":"dev-user"}'
```

Expected result:

- execution ID is created
- Direct Dispatch routes to Packet Pilot
- Actor Runtime invokes Packet Pilot
- Legal Logger writes reports/logbook entries
- timeline contains runtime events

---

## Backend proxy

Backend routes live under:

```text
/api/v1/codriver/*
```

The backend calls CoDriver through:

```text
backend/app/services/codriver_client.py
```

Backend remains the business platform.

CoDriver remains the runtime.

---

## Frontend AI tab

The AI tab calls:

```text
/api/v1/codriver/chat/send
```

The UI displays:

- chat messages
- CoDriver response
- active execution ID
- actor activated
- flow status
- timeline event count and recent timeline events
- recent logbook entries

It should feel like the CoDriver console, not only a chatbot.

---

## Ollama

CoDriver reads:

- `OLLAMA_BASE_URL`
- `OLLAMA_MODEL`
- `OLLAMA_TIMEOUT`

If Ollama is unavailable, CoDriver returns a structural runtime response that says the model is unavailable.

Do not fake model success.

---

## Cloudflare dev DNS

DNS helper:

```text
scripts/setup_cloudflare_dev_dns.py
```

Dry run:

```bash
python3 scripts/setup_cloudflare_dev_dns.py
```

It will not create records unless run with `--apply`.

Do not run `--apply` until the dev target IP/hostname is known and confirmed.

Supported dev record names come from `CF_DEV_RECORDS`, defaulting to:

- `dev.hwydriver.com`
- `dev.hwytms.com`
- `dev.hwytrucking.com`
- `codriver-dev.hwytrucking.com`

---

## Logs

Docker logs:

```bash
docker compose logs backend
docker compose logs frontend
docker compose logs codriver
docker compose logs db
```

CoDriver runtime files are stored under `CODRIVER_STORAGE_DIR` in the container and mounted through the `codriver_data` volume.

Important local runtime artifacts:

- telemetry JSONL
- logbook JSONL
- execution reports JSONL
- flow reports JSONL
- flow profiles JSON

Do not log secrets.
