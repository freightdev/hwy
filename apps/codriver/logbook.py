"""
HWY CoDriver — Logbook

Append-only. Every important object gets one. Legal Logger is the only actor
that writes OFFICIAL entries, but this store itself has no opinion about who's
calling it — access control belongs to Key Keeper, not to the storage layer.

Backed by JSONL on disk for now (local-first per build instructions). Swap the
LogbookStore.append/query internals for a real DB later without touching
callers — that's the whole point of keeping this behind an interface.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterator, Optional

from .models import LogbookEntry


class LogbookStore:
    def __init__(self, path: str | Path = "logbook.jsonl"):
        self.path = Path(path)
        self.path.touch(exist_ok=True)
        self._last_ref_by_object: dict[str, str] = {}
        self._rebuild_index()

    def _rebuild_index(self) -> None:
        for entry in self._read_all():
            key = f"{entry.object_type}:{entry.object_id}"
            self._last_ref_by_object[key] = entry.id

    def _read_all(self) -> Iterator[LogbookEntry]:
        if not self.path.exists():
            return
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    yield LogbookEntry.model_validate_json(line)

    def append(self, entry: LogbookEntry) -> LogbookEntry:
        """Append an entry, auto-chaining previous_ref for its object."""
        key = f"{entry.object_type}:{entry.object_id}"
        if entry.previous_ref is None:
            entry.previous_ref = self._last_ref_by_object.get(key)

        with self.path.open("a", encoding="utf-8") as f:
            f.write(entry.model_dump_json() + "\n")

        self._last_ref_by_object[key] = entry.id
        return entry

    def history_for(self, object_type: str, object_id: str) -> list[LogbookEntry]:
        return [
            e for e in self._read_all()
            if e.object_type == object_type and e.object_id == object_id
        ]

    def by_actor(self, actor: str) -> list[LogbookEntry]:
        return [e for e in self._read_all() if e.actor == actor]

    def all_entries(self) -> list[LogbookEntry]:
        return list(self._read_all())

    def latest_ref(self, object_type: str, object_id: str) -> Optional[str]:
        return self._last_ref_by_object.get(f"{object_type}:{object_id}")
