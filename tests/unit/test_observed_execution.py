from hilbert_harness.observation.execution import observe_execution
import pytest


def test_execution_boundary_detects_file_write(tmp_path):
    file_path = tmp_path / "example.txt"
    file_path.write_text("old content")

    def fake_executor():
        file_path.write_text("new content")
        return ["fake-codex-event"]

    result, observations = observe_execution(
        workspace=tmp_path,
        execute=fake_executor,
        observed_at_step=1,
    )

    assert result == ["fake-codex-event"]

    assert len(observations) == 1

    observation = observations[0]

    assert observation.operation == "file_write"
    assert observation.resource == "example.txt"
    assert observation.observed_at_step == 1

    assert observation.evidence["source"] == "filesystem_snapshot"
    assert (
        observation.evidence["before_sha256"]
        != observation.evidence["after_sha256"]
    )

def test_execution_boundary_without_changes_produces_no_observations(tmp_path):
    file_path = tmp_path / "example.txt"
    file_path.write_text("unchanged content")

    def fake_executor():
        return ["fake-codex-event"]

    result, observations = observe_execution(
        workspace=tmp_path,
        execute=fake_executor,
        observed_at_step=1,
    )

    assert result == ["fake-codex-event"]
    assert observations == []
    assert file_path.read_text() == "unchanged content"

def test_execution_failure_preserves_filesystem_changes(tmp_path):
    file_path = tmp_path / "example.txt"
    file_path.write_text("old content")

    def failing_executor():
        file_path.write_text("new content")
        raise RuntimeError("Agent execution failed")

    with pytest.raises(RuntimeError) as exc_info:
        observe_execution(
            workspace=tmp_path,
            execute=failing_executor,
            observed_at_step=1,
        )

    assert str(exc_info.value) == "Agent execution failed"

    observations = exc_info.value.effect_observations

    assert len(observations) == 1

    observation = observations[0]

    assert observation.operation == "file_write"
    assert observation.resource == "example.txt"
    assert observation.observed_at_step == 1
    assert observation.evidence["source"] == "filesystem_snapshot"
    assert (
        observation.evidence["before_sha256"]
        != observation.evidence["after_sha256"]
    )

    assert file_path.read_text() == "new content"