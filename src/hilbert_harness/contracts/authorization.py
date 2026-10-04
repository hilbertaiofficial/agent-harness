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
    "persistance",
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
    
'''@dataclass
class AuthorizationContract:
    #allowed_read: list[str] = field(default_factory=list)
    #allowed_write: list[str] = field(default_factory=list)

    #forbidden_read: list[str] = field(default_factory=list)
    #forbidden_write: list[str] = field(default_factory=list)

    #allowed_commands: list[str] = field(default_factory=list)
    #forbidden_commands: list[str] = field(default_factory=list)

    #requires_approval: list[str] = field(default_factory=list)

    #active: bool = True

    rules: list[AuthorizationRule] = field(default_factory=list)

    protected_effects: list[ProtectedEffect] = field(default_factory=list)

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
                and fnmatch(resource, effect.resource)
            )
        ]
    
    
    
    def rules_for_action(
        self,
        action_type: str,
    ) -> list[AuthorizationRule]:
        return [
            rule
            for rule in self.rules
            if rule.action_type == action_type
        ]'''

@dataclass
class AuthorizationState:
    active: bool = True
    approvals: set[str] = field(default_factory= list) #set



    #def grant_approval(self, action_type: str) -> None:
     #   self.approvals.add(action_type)

    #def has_approval(self, action_type: str) -> bool:
     #   return action_type in self.approvals

    def grant_approval(
        self,
        subject_type: ApprovalSubjectType,
        subject: str,
        #action_type: str,
        resource: str,
        granted_by: str | None = None,
        granted_at_step: int | None = None,
        usage: ApprovalUsage = "once",
    ) -> None:
        self.approvals.append(
            ApprovalGrant(
                #action_type=action_type,
                subject_type=subject_type,
                subject=subject,
                resource=resource,
                granted_by=granted_by,
                granted_at_step=granted_at_step,
                usage=usage,
            )
        )

    '''def has_approval(
        self,
        action_type: str,
        resource: str | None,
    ) -> bool:
        if resource is None:
            return False

        return any(
            approval.action_type == action_type
            and fnmatch(resource, approval.resource)
            for approval in self.approvals
        )'''

    def find_approval(
        self,
        subject_type: ApprovalSubjectType,
        subject: str,
       # action_type: str,
        resource: str | None,
    ) -> ApprovalGrant | None:
        if resource is None:
            return None

        for approval in self.approvals:
            if (
                approval.subject_type == subject_type
                and approval.subject == subject
                #approval.action_type == action_type
                #subject_type: ApprovalSubjectType,
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