"""
HWY CoDriver — Memory Mark

"CoDriver should not directly trust: emails, websites, PDFs, OCR text,
user-uploaded documents, unknown files, external messages. Memory Mark
validates and sanitizes untrusted content before CoDriver uses it."

For v0.1 this is intentionally simple: strip obvious prompt-injection
patterns, cap length, and force every piece of external content to come back
labeled as a Claim with an appropriate (low-trust) TruthLabel. The point isn't
that this is a hardened sanitizer yet — it's that the SHAPE of "untrusted
content must pass through here before CoDriver touches it" exists and is
enforced structurally.
"""

from __future__ import annotations

import re

from ..models import ActorContext, ActorResponse, Claim, TruthLabel

_INJECTION_PATTERNS = [
    re.compile(r"ignore\s+(all\s+|any\s+)?(previous\s+|prior\s+)?instructions", re.IGNORECASE),
    re.compile(r"system prompt", re.IGNORECASE),
    re.compile(r"you are now", re.IGNORECASE),
    re.compile(r"disregard (the )?(above|previous)", re.IGNORECASE),
    re.compile(r"wire (the )?(deposit|money|payment|funds)", re.IGNORECASE),
]

MAX_CONTENT_CHARS = 20_000


class MemoryMark:
    name = "Memory Mark"

    def sanitize(
        self,
        *,
        content: str,
        source_type: str,  # "email" | "website" | "pdf" | "ocr" | "upload" | "message"
        source_label: str | None = None,
        context: ActorContext | None = None,
    ) -> ActorResponse:
        flags: list[str] = []

        for pattern in _INJECTION_PATTERNS:
            if pattern.search(content):
                flags.append(f"possible_injection:{pattern.pattern}")

        truncated = len(content) > MAX_CONTENT_CHARS
        clean = content[:MAX_CONTENT_CHARS]

        label = TruthLabel.TRANSCRIBED if source_type == "ocr" else TruthLabel.UNCERTAIN

        claim = Claim(
            text=clean,
            label=label,
            source=source_label or source_type,
        )

        return ActorResponse(
            actor=self.name,
            flow_id="memory_mark.sanitize",
            success=True,
            claims=[claim],
            requires_human_approval=bool(flags),
            approval_reason=(
                "Untrusted content flagged for possible prompt injection: "
                + ", ".join(flags)
                if flags
                else None
            ),
            actions_used=1,
            raw={"flags": flags, "truncated": truncated, "source_type": source_type},
        )
