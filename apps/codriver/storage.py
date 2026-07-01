"""
HWY CoDriver — Storage primitives

Two shapes show up everywhere in Legal Logger:
  1. Append-only event logs (Execution Reports, Flow Reports, Logbook entries)
  2. Living keyed documents that get overwritten in place (Flow Profiles)

These two generic stores back all of that so each report type doesn't
reinvent file I/O.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Generic, Iterator, Type, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class JSONLStore(Generic[T]):
    """Append-only JSONL store for one pydantic model type."""

    def __init__(self, path: str | Path, model: Type[T]):
        self.path = Path(path)
        self.model = model
        self.path.touch(exist_ok=True)

    def append(self, item: T) -> T:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(item.model_dump_json() + "\n")
        return item

    def all(self) -> list[T]:
        return list(self._read_all())

    def filter(self, **kwargs) -> list[T]:
        return [
            item
            for item in self._read_all()
            if all(getattr(item, k, None) == v for k, v in kwargs.items())
        ]

    def latest(self, n: int = 1, **kwargs) -> list[T]:
        matches = self.filter(**kwargs) if kwargs else self.all()
        return matches[-n:]

    def _read_all(self) -> Iterator[T]:
        if not self.path.exists():
            return
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    yield self.model.model_validate_json(line)


class KeyedJSONStore(Generic[T]):
    """A single JSON file holding {key: model_dict}. Good for small numbers
    of living documents (e.g. one Flow Profile per flow_id) that get read,
    mutated, and rewritten — not appended.
    """

    def __init__(self, path: str | Path, model: Type[T]):
        self.path = Path(path)
        self.model = model
        if not self.path.exists():
            self.path.write_text("{}", encoding="utf-8")

    def _load(self) -> dict[str, dict]:
        raw = self.path.read_text(encoding="utf-8").strip()
        return json.loads(raw) if raw else {}

    def _save(self, data: dict[str, dict]) -> None:
        self.path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")

    def get(self, key: str) -> T | None:
        data = self._load()
        if key not in data:
            return None
        return self.model.model_validate(data[key])

    def set(self, key: str, value: T) -> T:
        data = self._load()
        data[key] = json.loads(value.model_dump_json())
        self._save(data)
        return value

    def all(self) -> dict[str, T]:
        return {k: self.model.model_validate(v) for k, v in self._load().items()}
