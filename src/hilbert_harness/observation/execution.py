from collections.abc import Callable
from pathlib import Path
from typing import TypeVar

from hilbert_harness.ir.effects import EffectObservation
from hilbert_harness.observation.filesystem import (
    capture_filesystem_snapshot,
    compare_filesystem_snapshots,
)


T = TypeVar("T")


def observe_execution(
    workspace: Path,
    execute: Callable[[], T],
    observed_at_step: int,
) -> tuple[T, list[EffectObservation]]:
    before = capture_filesystem_snapshot(workspace)

    try:
        result = execute()
    except Exception as exc:
        after = capture_filesystem_snapshot(workspace)

        observations = compare_filesystem_snapshots(
            before,
            after,
            observed_at_step=observed_at_step,
        )

        exc.effect_observations = observations
        raise

    after = capture_filesystem_snapshot(workspace)

    observations = compare_filesystem_snapshots(
        before,
        after,
        observed_at_step=observed_at_step,
    )

    return result, observations