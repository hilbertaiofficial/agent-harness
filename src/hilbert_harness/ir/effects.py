from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class EffectObservation:
    operation: str
    resource: str
    observed_at_step: int
    evidence: dict[str, Any] = field(default_factory=dict)