from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class TrajectoryStep:
    index: int
    actor: str
    action_type: str

    target: str | None = None
    arguments: dict[str, Any] = field(default_factory=dict)
    result: dict[str, Any] = field(default_factory=dict)

    timestamp: str | None = None
    provenance: dict[str, Any] = field(default_factory=dict)


@dataclass
class Trajectory:
    run_id: str
    engine: str
    instruction: str
    steps: list[TrajectoryStep] = field(default_factory=list)