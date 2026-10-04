from hilbert_harness.ir.trajectory import (
    StateTransition,
    Trajectory,
    TrajectoryStep,
)


def test_trajectory_can_record_state_transition():
    trajectory = Trajectory(
        run_id="run-state-001",
        engine="synthetic",
        instruction="Delete the obsolete test file.",
        steps=[
            TrajectoryStep(
                index=1,
                actor="agent",
                action_type="command",
                target="rm tests/old_auth.py",
            ),
        ],
        state_transitions=[
            StateTransition(
                resource="tests/old_auth.py",
                operation="delete",
                caused_by_step=1,
            ),
        ],
    )

    assert len(trajectory.state_transitions) == 1

    transition = trajectory.state_transitions[0]

    assert transition.resource == "tests/old_auth.py"
    assert transition.operation == "delete"
    assert transition.caused_by_step == 1


def test_trajectory_defaults_to_no_state_transitions():
    trajectory = Trajectory(
        run_id="run-state-002",
        engine="synthetic",
        instruction="Read the authentication file.",
        steps=[
            TrajectoryStep(
                index=1,
                actor="agent",
                action_type="file_read",
                target="src/auth.py",
            ),
        ],
    )

    assert trajectory.state_transitions == []

def test_state_transition_can_reference_causing_step():
    trajectory = Trajectory(
        run_id="run-state-003",
        engine="synthetic",
        instruction="Remove the obsolete test file.",
        steps=[
            TrajectoryStep(
                index=1,
                actor="agent",
                action_type="file_read",
                target="tests/old_auth.py",
            ),
            TrajectoryStep(
                index=2,
                actor="agent",
                action_type="command",
                target="rm tests/old_auth.py",
            ),
        ],
        state_transitions=[
            StateTransition(
                resource="tests/old_auth.py",
                operation="delete",
                caused_by_step=2,
            ),
        ],
    )

    transition = trajectory.state_transitions[0]

    causing_step = next(
        step
        for step in trajectory.steps
        if step.index == transition.caused_by_step
    )

    assert causing_step.action_type == "command"
    assert causing_step.index == 2