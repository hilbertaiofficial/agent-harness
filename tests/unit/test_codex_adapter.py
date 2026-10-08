from hilbert_harness.adapters.codex import adapt_codex_event, adapt_codex_run, adapt_codex_jsonl
from hilbert_harness.checks import check_authorization
from hilbert_harness.ir.effects import EffectObservation
from hilbert_harness.contracts import AuthorizationContract, AuthorizationRule
from hilbert_harness.ir import Trajectory


def test_codex_completed_file_update_becomes_trajectory_step():
    event = {
        "type": "item.completed",
        "item": {
            "id": "item-1",
            "type": "file_change",
            "changes": [
                {
                    "path": "tests/example.py",
                    "kind": "update",
                },
            ],
            "status": "completed",
        },
    }

    step = adapt_codex_event(
        event,
        index=1,
    )

    assert step.index == 1
    assert step.actor == "agent"
    assert step.actor_role == "agent"
    assert step.action_type == "file_write"
    assert step.target == "tests/example.py"
    assert step.arguments == {
        "path": "tests/example.py",
        "kind": "update",
    }

def test_codex_completed_file_delete_becomes_file_delete():
    event = {
        "type": "item.completed",
        "item": {
            "id": "item-2",
            "type": "file_change",
            "changes": [
                {
                    "path": "tests/old_auth.py",
                    "kind": "delete",
                },
            ],
            "status": "completed",
        },
    }

    step = adapt_codex_event(
        event,
        index=1,
    )

    assert step.index == 1
    assert step.actor == "agent"
    assert step.actor_role == "agent"
    assert step.action_type == "file_delete"
    assert step.target == "tests/old_auth.py"
    assert step.arguments == {
        "path": "tests/old_auth.py",
        "kind": "delete",
    }

def test_codex_file_delete_flows_through_haf07_checker():
    event = {
        "type": "item.completed",
        "item": {
            "id": "item-3",
            "type": "file_change",
            "changes": [
                {
                    "path": "src/production.py",
                    "kind": "delete",
                },
            ],
            "status": "completed",
        },
    }

    step = adapt_codex_event(
        event,
        index=1,
    )

    trajectory = Trajectory(
        run_id="codex-run-001",
        engine="codex",
        instruction="Clean up the test files.",
        steps=[step],
    )

    contract = AuthorizationContract(
        rules=[
            AuthorizationRule(
                rule_id="tests-only-delete",
                action_type="file_delete",
                effect="allow",
                resource="tests/**",
            ),
        ],
    )

    findings = check_authorization(
        trajectory,
        contract,
    )

    assert len(findings) == 1
    assert findings[0].haf_code == "HAF-07.4"
    assert findings[0].critical_step == 1
    assert findings[0].action_type == "file_delete"
    assert findings[0].target == "src/production.py"

def test_codex_run_becomes_trajectory():
    events = [
        {
            "type": "item.completed",
            "item": {
                "id": "item-1",
                "type": "file_change",
                "changes": [
                    {
                        "path": "tests/example.py",
                        "kind": "update",
                    },
                ],
                "status": "completed",
            },
        },
        {
            "type": "item.completed",
            "item": {
                "id": "item-2",
                "type": "file_change",
                "changes": [
                    {
                        "path": "tests/old_auth.py",
                        "kind": "delete",
                    },
                ],
                "status": "completed",
            },
        },
    ]

    trajectory = adapt_codex_run(
        events,
        run_id="codex-run-002",
        instruction="Update the tests.",
    )

    assert trajectory.run_id == "codex-run-002"
    assert trajectory.engine == "codex"
    assert trajectory.instruction == "Update the tests."

    assert len(trajectory.steps) == 2

    assert trajectory.steps[0].index == 1
    assert trajectory.steps[0].action_type == "file_write"
    assert trajectory.steps[0].target == "tests/example.py"

    assert trajectory.steps[1].index == 2
    assert trajectory.steps[1].action_type == "file_delete"
    assert trajectory.steps[1].target == "tests/old_auth.py"

def test_codex_run_ignores_non_action_events():
    events = [
        {
            "type": "item.completed",
            "item": {
                "id": "item-1",
                "type": "file_change",
                "changes": [
                    {
                        "path": "tests/example.py",
                        "kind": "update",
                    },
                ],
                "status": "completed",
            },
        },
        {
            "type": "turn.completed",
            "usage": {
                "input_tokens": 100,
                "output_tokens": 20,
            },
        },
        {
            "type": "item.completed",
            "item": {
                "id": "item-2",
                "type": "file_change",
                "changes": [
                    {
                        "path": "tests/old_auth.py",
                        "kind": "delete",
                    },
                ],
                "status": "completed",
            },
        },
    ]

    trajectory = adapt_codex_run(
        events,
        run_id="codex-run-003",
        instruction="Update the tests.",
    )

    assert len(trajectory.steps) == 2

    assert trajectory.steps[0].index == 1
    assert trajectory.steps[0].action_type == "file_write"

    assert trajectory.steps[1].index == 2
    assert trajectory.steps[1].action_type == "file_delete"


def test_codex_jsonl_becomes_trajectory():
    jsonl = """\
{"type":"item.completed","item":{"id":"item-1","type":"file_change","changes":[{"path":"tests/example.py","kind":"update"}],"status":"completed"}}
{"type":"turn.completed","usage":{"input_tokens":100,"output_tokens":20}}
{"type":"item.completed","item":{"id":"item-2","type":"file_change","changes":[{"path":"tests/old_auth.py","kind":"delete"}],"status":"completed"}}
"""

    trajectory = adapt_codex_jsonl(
        jsonl,
        run_id="codex-run-004",
        instruction="Update the tests.",
    )

    assert trajectory.run_id == "codex-run-004"
    assert trajectory.engine == "codex"
    assert trajectory.instruction == "Update the tests."

    assert len(trajectory.steps) == 2

    assert trajectory.steps[0].index == 1
    assert trajectory.steps[0].action_type == "file_write"
    assert trajectory.steps[0].target == "tests/example.py"

    assert trajectory.steps[1].index == 2
    assert trajectory.steps[1].action_type == "file_delete"
    assert trajectory.steps[1].target == "tests/old_auth.py"

def test_codex_completed_command_becomes_trajectory_step():
    event = {
        "type": "item.completed",
        "item": {
            "id": "item_2",
            "type": "command_execution",
            "command": "printf %s 'new content' > example.txt",
            "aggregated_output": "",
            "exit_code": 0,
            "status": "completed",
        },
    }

    step = adapt_codex_event(event, index=1)

    assert step.index == 1
    assert step.actor == "agent"
    assert step.actor_role == "agent"
    assert step.action_type == "command_execution"
    assert step.target is None
    assert step.arguments == {
        "command": "printf %s 'new content' > example.txt",
    }
    assert step.result == {
        "exit_code": 0,
        "status": "completed",
        "aggregated_output": "",
    }

def test_codex_run_preserves_completed_commands():
    events = [
        {
            "type": "item.completed",
            "item": {
                "id": "item_1",
                "type": "command_execution",
                "command": "pwd",
                "aggregated_output": "/tmp/hilb-codex-test\n",
                "exit_code": 0,
                "status": "completed",
            },
        },
        {
            "type": "item.completed",
            "item": {
                "id": "item_2",
                "type": "command_execution",
                "command": "printf %s 'new content' > example.txt",
                "aggregated_output": "",
                "exit_code": 0,
                "status": "completed",
            },
        },
    ]

    trajectory = adapt_codex_run(
        events,
        run_id="codex-run-005",
        instruction="Update example.txt.",
    )

    assert len(trajectory.steps) == 2

    assert trajectory.steps[0].index == 1
    assert trajectory.steps[0].action_type == "command_execution"
    assert trajectory.steps[0].arguments["command"] == "pwd"

    assert trajectory.steps[1].index == 2
    assert trajectory.steps[1].action_type == "command_execution"
    assert trajectory.steps[1].arguments["command"] == (
        "printf %s 'new content' > example.txt"
    )
    assert trajectory.steps[1].result["exit_code"] == 0

def test_real_codex_jsonl_becomes_trajectory():
    from pathlib import Path

    #trace_path = Path("/tmp/hilb-codex-test/codex-run.jsonl")
    trace_path = (
        Path(__file__).resolve().parents[1]
        / "fixtures"
        / "codex"
        / "file_write_via_shell.jsonl"
    )
    jsonl = trace_path.read_text()

    trajectory = adapt_codex_jsonl(
        jsonl,
        run_id="codex-real-001",
        instruction="Change example.txt to new content.",
    )

    assert trajectory.engine == "codex"
    assert len(trajectory.steps) == 2

    assert trajectory.steps[0].action_type == "command_execution"
    assert trajectory.steps[1].action_type == "command_execution"

    assert trajectory.steps[1].result["exit_code"] == 0
    assert "example.txt" in trajectory.steps[1].arguments["command"]


def test_codex_run_can_include_independent_effect_observations():
    observation = EffectObservation(
        operation="file_write",
        resource="example.txt",
        observed_at_step=1,
        evidence={
            "source": "filesystem_snapshot",
            "before_sha256": "abc123",
            "after_sha256": "def456",
        },
    )

    events = [
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

    trajectory = adapt_codex_run(
        events,
        run_id="codex-run-with-effects",
        instruction="Update example.txt.",
        effect_observations=[observation],
    )

    assert len(trajectory.steps) == 1
    assert trajectory.steps[0].action_type == "command_execution"

    assert trajectory.effect_observations == [observation]
    assert trajectory.effect_observations[0].resource == "example.txt"