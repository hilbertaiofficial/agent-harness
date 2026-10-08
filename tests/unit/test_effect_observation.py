from hilbert_harness.ir.effects import EffectObservation
from hilbert_harness.ir import Trajectory


def test_verified_file_write_observation():
    observation = EffectObservation(
        operation="file_write",
        resource="example.txt",
        observed_at_step=2,
        evidence={
            "source": "filesystem_snapshot",
            "before_sha256": "abc123",
            "after_sha256": "def456",
        },
    )

    assert observation.operation == "file_write"
    assert observation.resource == "example.txt"
    assert observation.observed_at_step == 2
    assert observation.evidence["source"] == "filesystem_snapshot"
    assert observation.evidence["before_sha256"] != observation.evidence["after_sha256"]

def test_trajectory_can_store_effect_observations():
    observation = EffectObservation(
        operation="file_write",
        resource="example.txt",
        observed_at_step=2,
        evidence={
            "source": "filesystem_snapshot",
            "before_sha256": "abc123",
            "after_sha256": "def456",
        },
    )

    trajectory = Trajectory(
        run_id="codex-run-006",
        engine="codex",
        instruction="Update example.txt.",
        steps=[],
        effect_observations=[observation],
    )

    assert len(trajectory.effect_observations) == 1
    assert trajectory.effect_observations[0] == observation

    # Observations must not become agent actions.
    assert len(trajectory.steps) == 0
