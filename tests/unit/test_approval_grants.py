from hilbert_harness.contracts.authorization import (
    AuthorizationState,
)


def test_action_approval_can_be_found():
    state = AuthorizationState()

    state.grant_approval(
        subject_type="action",
        subject="file_delete",
        resource="tests/old_auth.py",
        granted_by="user",
        granted_at_step=1,
        usage="once",
    )

    approval = state.find_approval(
        subject_type="action",
        subject="file_delete",
        resource="tests/old_auth.py",
    )

    assert approval is not None
    assert approval.subject_type == "action"
    assert approval.subject == "file_delete"


def test_effect_approval_can_be_found():
    state = AuthorizationState()

    state.grant_approval(
        subject_type="effect",
        subject="delete",
        resource="tests/old_auth.py",
        granted_by="user",
        granted_at_step=1,
        usage="once",
    )

    approval = state.find_approval(
        subject_type="effect",
        subject="delete",
        resource="tests/old_auth.py",
    )

    assert approval is not None
    assert approval.subject_type == "effect"
    assert approval.subject == "delete"


def test_action_approval_does_not_satisfy_effect_approval():
    state = AuthorizationState()

    state.grant_approval(
        subject_type="action",
        subject="file_delete",
        resource="tests/old_auth.py",
        granted_by="user",
        granted_at_step=1,
        usage="once",
    )

    effect_approval = state.find_approval(
        subject_type="effect",
        subject="delete",
        resource="tests/old_auth.py",
    )

    assert effect_approval is None