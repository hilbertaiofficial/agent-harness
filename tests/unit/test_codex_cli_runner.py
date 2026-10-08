import json
import subprocess
import pytest

from hilbert_harness.observation.codex_cli import run_codex_cli


def test_codex_cli_runner_collects_jsonl_events(tmp_path, monkeypatch):
    expected_events = [
        {
            "type": "thread.started",
            "thread_id": "test-thread-001",
        },
        {
            "type": "item.completed",
            "item": {
                "id": "item_1",
                "type": "command_execution",
                "command": "pwd",
                "exit_code": 0,
                "status": "completed",
                "aggregated_output": "",
            },
        },
    ]

    def fake_subprocess_run(command, **kwargs):
        assert command == [
            "codex",
            "exec",
            "--json",
            "--sandbox",
            "workspace-write",
            "Check the current directory.",
        ]

        assert kwargs["cwd"] == tmp_path
        assert kwargs["capture_output"] is True
        assert kwargs["text"] is True
        assert kwargs["check"] is True

        return subprocess.CompletedProcess(
            args=command,
            returncode=0,
            stdout="\n".join(
                json.dumps(event) for event in expected_events
            ),
            stderr="",
        )

    monkeypatch.setattr(subprocess, "run", fake_subprocess_run)

    events = run_codex_cli(
        workspace=tmp_path,
        instruction="Check the current directory.",
    )

    assert events == expected_events

def test_codex_cli_runner_raises_on_nonzero_exit(tmp_path, monkeypatch):
    def fake_subprocess_run(command, **kwargs):
        assert kwargs["cwd"] == tmp_path
        assert kwargs["check"] is True

        raise subprocess.CalledProcessError(
            returncode=1,
            cmd=command,
            output='{"type":"thread.started","thread_id":"test-thread"}\n',
            stderr="Codex execution failed",
        )

    monkeypatch.setattr(subprocess, "run", fake_subprocess_run)

    with pytest.raises(subprocess.CalledProcessError) as exc_info:
        run_codex_cli(
            workspace=tmp_path,
            instruction="Update example.txt.",
        )

    assert exc_info.value.returncode == 1
    assert exc_info.value.stderr == "Codex execution failed"