from __future__ import annotations
from hilbert_harness.ir.effects import EffectObservation
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class TrajectoryStep:
    index: int
    actor: str
    action_type: str
    actor_role: str | None = None

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
    state_transitions: list[StateTransition] = field(default_factory=list)
    effect_observations: list[EffectObservation] = field(default_factory=list)                                                 


@dataclass(frozen=True)
class StateTransition:
    resource: str
    operation: str
    caused_by_step: int | None = None