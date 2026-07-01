#!/usr/bin/env python3
"""Generate configs/env/hwy.dev.env from configs/env/hwy.dev.env.example and vault JSON.

This script is local-only. It never prints secret values.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV_DIR = ROOT / "configs" / "env"
EXAMPLE = ENV_DIR / "hwy.dev.env.example"
TARGET = ENV_DIR / "hwy.dev.env"
VAULT = ROOT / "vault"


def parse_env_lines(path: Path) -> tuple[list[str], dict[str, str]]:
    lines = path.read_text().splitlines()
    values: dict[str, str] = {}
    for line in lines:
        if not line or line.lstrip().startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key] = value
    return lines, values


def load_vault_secrets() -> dict[str, str]:
    secrets: dict[str, str] = {}
    if not VAULT.exists():
        return secrets
    for path in sorted(VAULT.glob("*.json")):
        try:
            data = json.loads(path.read_text())
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        cloudflare_key = data.get("CLOUDFLARE_API_KEY")
        if cloudflare_key:
            secrets["CLOUDFLARE_API_TOKEN"] = str(cloudflare_key)
        account_tag = data.get("AccountTag")
        if account_tag:
            secrets["CLOUDFLARE_ACCOUNT_TAG"] = str(account_tag)
        tunnel_id = data.get("TunnelID")
        if tunnel_id:
            secrets["CLOUDFLARE_TUNNEL_ID"] = str(tunnel_id)
    if os.getenv("CLOUDFLARE_API_TOKEN"):
        secrets["CLOUDFLARE_API_TOKEN"] = os.environ["CLOUDFLARE_API_TOKEN"]
    if os.getenv("CLOUDFLARE_ZONE_ID"):
        secrets["CLOUDFLARE_ZONE_ID"] = os.environ["CLOUDFLARE_ZONE_ID"]
    for path in sorted(VAULT.glob("*.json")):
        path.chmod(0o600)
    return secrets


def main() -> int:
    lines, values = parse_env_lines(EXAMPLE)
    values.update(load_vault_secrets())
    output: list[str] = []
    for line in lines:
        if not line or line.lstrip().startswith("#") or "=" not in line:
            output.append(line)
            continue
        key, _ = line.split("=", 1)
        output.append(f"{key}={values.get(key, '')}")
    TARGET.write_text("\n".join(output) + "\n")
    TARGET.chmod(0o600)
    print(f"wrote {TARGET} with {len(values)} keys; secret values were not printed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
