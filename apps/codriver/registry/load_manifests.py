"""Load and validate actor manifest drafts from actor directories."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .actor_manifest_schema import ActorManifestDraft


def load_actor_manifest_file(path: Path) -> ActorManifestDraft:
    """Load one manifest.yaml file and validate it."""

    with path.open("r", encoding="utf-8") as handle:
        raw: Any = yaml.safe_load(handle)

    if not isinstance(raw, dict):
        raise ValueError(f"Actor manifest must be a mapping: {path}")

    return ActorManifestDraft.model_validate(raw)


def find_actor_manifest_files(actors_root: Path) -> list[Path]:
    """Find actor manifest files below an actors directory."""

    return sorted(actors_root.glob("*/manifest.yaml"))


def load_actor_manifests(actors_root: Path) -> list[ActorManifestDraft]:
    """Load all actor manifests under actors_root.

    Direct Dispatch will eventually use this validated list as runtime-readable
    actor boundary data. This function only loads and validates; it does not
    execute actors.
    """

    manifests = [load_actor_manifest_file(path) for path in find_actor_manifest_files(actors_root)]
    actor_ids = [manifest.actor_id for manifest in manifests]
    duplicates = sorted({actor_id for actor_id in actor_ids if actor_ids.count(actor_id) > 1})
    if duplicates:
        raise ValueError(f"Duplicate actor manifest IDs: {', '.join(duplicates)}")
    return manifests
