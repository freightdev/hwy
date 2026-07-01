#!/usr/bin/env python3
"""Prepare Cloudflare dev DNS operations without printing secrets.

Default mode is dry-run. Use --apply only after explicit confirmation.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from urllib import request

ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = ROOT / "configs" / "env" / "hwy.dev.env"


def load_env(path: Path) -> dict[str, str]:
    values = dict(os.environ)
    if path.exists():
        for line in path.read_text().splitlines():
            if not line or line.lstrip().startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            values.setdefault(key, value)
    return values


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Actually create/update DNS records")
    args = parser.parse_args()

    env = load_env(ENV_FILE)
    token = env.get("CLOUDFLARE_API_TOKEN", "")
    zone_id = env.get("CLOUDFLARE_ZONE_ID", "")
    target = env.get("CF_DEV_TARGET", "")
    records = [r.strip() for r in env.get("CF_DEV_RECORDS", "").split(",") if r.strip()]

    if not records:
        print("No CF_DEV_RECORDS configured.")
        return 1
    if not target:
        print("Target IP/hostname is unknown. Set CF_DEV_TARGET before creating dev DNS records.")
        return 1
    if not token or not zone_id:
        print("Cloudflare credentials are not configured in env/vault. DNS setup skipped.")
        return 1

    record_type = "CNAME" if not target.replace(".", "").isdigit() and ":" not in target else ("AAAA" if ":" in target else "A")
    print(f"Prepared {len(records)} Cloudflare {record_type} records for target {target}. Secret values not printed.")
    for name in records:
        print(f"- {name} -> {target}")

    if not args.apply:
        print("Dry run only. Re-run with --apply after confirming target/scope.")
        return 0

    for name in records:
        payload = json.dumps({"type": record_type, "name": name, "content": target, "ttl": 120, "proxied": False}).encode()
        req = request.Request(
            f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records",
            data=payload,
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            method="POST",
        )
        with request.urlopen(req, timeout=15) as resp:
            if resp.status >= 300:
                raise RuntimeError(f"Cloudflare request failed for {name}: HTTP {resp.status}")
        print(f"created_or_requested {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
