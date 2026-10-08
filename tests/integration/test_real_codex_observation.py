import os
from pathlib import Path
import subprocess
import pytest

from hilbert_harness.observation.codex import observe_codex_run
from hilbert_harness.observation.codex_cli import run_codex_cli


@pytest.mark.skipif(
    os.environ.get("HILB_RUN_REAL_CODEX") != "1",
    reason="Real Codex integration test is opt-in",
)
def test_real_codex_file_write_is_observed(tmp_path):
    workspace = tmp_path
    file_path = workspace / "example.txt"
    file_path.write_text("old content")

    subprocess.run(
        ["git", "init", "-q"],
        cwd=workspace,
        check=True,
    )

    subprocess.run(
        ["git", "add", "example.txt"],
        cwd=workspace,
        check=True,
    )

    subprocess.run(
        [
            "git",
            "-c", "user.name=Hilb Test",
            "-c", "user.email=hilb-test@example.com",
            "commit", "-q", "-m", "initial test fixture",
        ],
        cwd=workspace,
        check=True,
    )

    instruction = (
        "Update example.txt so its entire content is exactly "
        "'new content'. Do not modify any other files."
    )

    trajectory = observe_codex_run(
        workspace=workspace,
        execute=lambda: run_codex_cli(
            workspace=workspace,
            instruction=instruction,
        ),
        run_id="real-codex-integration-001",
        instruction=instruction,
    )

    assert trajectory.engine == "codex"
    assert len(trajectory.steps) >= 1

    assert file_path.read_text() == "new content"

    observations = [
        observation
        for observation in trajectory.effect_observations
        if observation.resource == "example.txt"
    ]

    assert len(observations) == 1
    assert observations[0].operation == "file_write"
    assert observations[0].evidence["source"] == "filesystem_snapshot"