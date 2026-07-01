"""Load and validate Moonrust Agent capability manifests."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .agent_manifest_schema import AgentManifestDraft


def load_agent_manifest_file(path: Path) -> AgentManifestDraft:
    """Load one agent manifest.yaml file and validate it."""

    with path.open("r", encoding="utf-8") as handle:
        raw: Any = yaml.safe_load(handle)

    if not isinstance(raw, dict):
        raise ValueError(f"Agent manifest must be a mapping: {path}")

    return AgentManifestDraft.model_validate(raw)


def find_agent_manifest_files(agents_root: Path) -> list[Path]:
    """Find agent manifest files below moonrust/agents."""

    return sorted(agents_root.glob("*/*/manifest.yaml"))


def load_agent_manifests(agents_root: Path) -> list[AgentManifestDraft]:
    """Load all agent manifests under agents_root.

    CoDriver Agent Builder will eventually use this validated list as the safe
    capability lookup table. This only loads and validates; it does not grant
    runtime authority or invoke agents.
    """

    manifests = [load_agent_manifest_file(path) for path in find_agent_manifest_files(agents_root)]
    agent_ids = [manifest.agent_id for manifest in manifests]
    duplicates = sorted({agent_id for agent_id in agent_ids if agent_ids.count(agent_id) > 1})
    if duplicates:
        raise ValueError(f"Duplicate agent manifest IDs: {', '.join(duplicates)}")
    return manifests
