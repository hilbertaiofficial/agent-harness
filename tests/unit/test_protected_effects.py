from hilbert_harness.contracts.authorization import (
    AuthorizationContract,
    ProtectedEffect,
)

def test_protected_effect_matches_exact_resource():
    contract = AuthorizationContract(
        protected_effects=[
            ProtectedEffect(
                effect_id="protect-auth-delete",
                operation="delete",
                resource="tests/old_auth.py",
                requirement="require_approval",
                authority_source="user",
            ),
        ],
    )

    matches = contract.protected_effects_for(
        operation="delete",
        resource="tests/old_auth.py",
    )

    assert len(matches) == 1

    assert matches[0].effect_id == (
        "protect-auth-delete"
    )

def test_protected_effect_matches_wildcard_resource():
    contract = AuthorizationContract(
        protected_effects=[
            ProtectedEffect(
                effect_id="protect-test-deletion",
                operation="delete",
                resource="tests/**",
                requirement="require_approval",
                authority_source="user",
            ),
        ],
    )

    matches = contract.protected_effects_for(
        operation="delete",
        resource="tests/old_auth.py",
    )

    assert len(matches) == 1

    assert matches[0].effect_id == (
        "protect-test-deletion"
    )

def test_protected_effect_does_not_match_unrelated_effect():
    contract = AuthorizationContract(
        protected_effects=[
            ProtectedEffect(
                effect_id="protect-test-deletion",
                operation="delete",
                resource="tests/**",
                requirement="require_approval",
                authority_source="user",
            ),
        ],
    )

    wrong_operation = contract.protected_effects_for(
        operation="modify",
        resource="tests/old_auth.py",
    )

    wrong_resource = contract.protected_effects_for(
        operation="delete",
        resource="src/auth.py",
    )

    assert wrong_operation == []
    assert wrong_resource == []