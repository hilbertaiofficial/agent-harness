from __future__ import annotations

from dataclasses import dataclass, field
from fnmatch import fnmatch
from typing import Literal

AuthorizationEffect = Literal[
    "allow",
    "deny",
    "require_approval",
]

ApprovalUsage = Literal[
    "once",
    "persistent",
]

EffectRequirement = Literal[
    "require_approval",
]

ApprovalSubjectType = Literal[
    "action",
    "effect",
]

@dataclass
class AuthorizationContract:
    rules: list[AuthorizationRule] = field(
        default_factory=list
    )

    protected_effects: list[ProtectedEffect] = field(
        default_factory=list
    )

    def rules_for_action(
        self,
        action_type: str,
    ) -> list[AuthorizationRule]:
        return [
            rule
            for rule in self.rules
            if rule.action_type == action_type
        ]

    def protected_effects_for(
        self,
        operation: str,
        resource: str,
    ) -> list[ProtectedEffect]:
        return [
            effect
            for effect in self.protected_effects
            if (
                effect.operation == operation
                and fnmatch(
                    resource,
                    effect.resource,
                )
            )
        ]


@dataclass
class AuthorizationState:
    active: bool = True
    approvals: list[ApprovalGrant] = field(default_factory=list) #set

    def grant_approval(
        self,
        subject_type: ApprovalSubjectType,
        subject: str,
        resource: str,
        granted_by: str | None = None,
        granted_at_step: int | None = None,
        usage: ApprovalUsage = "once",
    ) -> None:
        self.approvals.append(
            ApprovalGrant(
                subject_type=subject_type,
                subject=subject,
                resource=resource,
                granted_by=granted_by,
                granted_at_step=granted_at_step,
                usage=usage,
            )
        )      

    def find_approval(
        self,
        subject_type: ApprovalSubjectType,
        subject: str,
        resource: str | None,
    ) -> ApprovalGrant | None:
        if resource is None:
            return None

        for approval in self.approvals:
            if (
                approval.subject_type == subject_type
                and approval.subject == subject
                and fnmatch(resource, approval.resource)
            ):
                return approval

        return None

    def consume_approval(
        self,
        approval: ApprovalGrant,
    ) -> None:
        if approval.usage == "once":
            self.approvals.remove(approval)

    
    def revoke(self) -> None:
        self.active = False

@dataclass(frozen=True)
class AuthorizationRule:

    action_type: str
    effect: AuthorizationEffect
    resource: str = "**/*"

    rule_id: str | None = None

    authority_source: str | None = None

@dataclass(frozen=True)
class ApprovalGrant:
    subject_type: ApprovalSubjectType
    subject: str
    #action_type: str
    resource: str
    granted_by: str | None = None
    granted_at_step: int | None = None
    usage: ApprovalUsage = "once"


@dataclass(frozen=True)
class ProtectedEffect:
    operation: str
    resource: str
    requirement: EffectRequirement
    effect_id: str | None = None
    authority_source: str | None = None