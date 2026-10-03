from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Finding:
    haf_code: str
    category: str
    critical_step: int
    reason: str

    action_type: str | None = None
    target: str | None = None

    severity: str = "H1"
    confidence: float = 1.0

    evidence: dict[str, Any] | None = None