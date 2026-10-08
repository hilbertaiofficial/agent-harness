from hilbert_harness.adapters.codex import adapt_codex_run
from hilbert_harness.observation.codex import observe_codex_run


def test_observed_codex_run_attaches_filesystem_effects(tmp_path):
    file_path = tmp_path / "example.txt"
    file_path.write_text("old content")

    def fake_codex_executor():
        file_path.write_text("new content")

        return [
            {
                "type": "item.completed",
                "item": {
                    "id": "item_1",
                    "type": "command_execution",
                    "command": "printf 'new content' > example.txt",
                    "exit_code": 0,
                    "status": "completed",
                    "aggregated_output": "",
                },
            }
        ]

    trajectory = observe_codex_run(
        workspace=tmp_path,
        execute=fake_codex_executor,
        run_id="codex-observed-001",
        instruction="Update example.txt.",
    )

    assert trajectory.engine == "codex"
    assert len(trajectory.steps) == 1
    assert trajectory.steps[0].action_type == "command_execution"

    assert len(trajectory.effect_observations) == 1

    observation = trajectory.effect_observations[0]

    assert observation.operation == "file_write"
    assert observation.resource == "example.txt"
    assert observation.evidence["source"] == "filesystem_snapshot"
    assert (
        observation.evidence["before_sha256"]
        != observation.evidence["after_sha256"]
    )

def test_observed_codex_run_without_changes_has_no_effects(tmp_path):
    file_path = tmp_path / "example.txt"
    file_path.write_text("unchanged content")

    def fake_codex_executor():
        return [
            {
                "type": "item.completed",
                "item": {
                    "id": "item_1",
                    "type": "command_execution",
                    "command": "cat example.txt",
                    "exit_code": 0,
                    "status": "completed",
                    "aggregated_output": "unchanged content",
                },
            }
        ]

    trajectory = observe_codex_run(
        workspace=tmp_path,
        execute=fake_codex_executor,
        run_id="codex-observed-002",
        instruction="Read example.txt.",
    )

    assert trajectory.engine == "codex"

    assert len(trajectory.steps) == 1
    assert trajectory.steps[0].action_type == "command_execution"
    assert trajectory.steps[0].result["exit_code"] == 0

    assert trajectory.effect_observations == []
    assert file_path.read_text() == "unchanged content"