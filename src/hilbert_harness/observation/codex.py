from collections.abc import Callable
from pathlib import Path
from typing import Any

from hilbert_harness.adapters.codex import adapt_codex_run
from hilbert_harness.ir.trajectory import Trajectory
from hilbert_harness.observation.execution import observe_execution


def observe_codex_run(
    workspace: Path,
    execute: Callable[[], list[dict[str, Any]]],
    run_id: str,
    instruction: str,
) -> Trajectory:
    events, observations = observe_execution(
        workspace=workspace,
        execute=execute,
        observed_at_step=1,
    )

    return adapt_codex_run(
        events,
        run_id=run_id,
        instruction=instruction,
        effect_observations=observations,
    )