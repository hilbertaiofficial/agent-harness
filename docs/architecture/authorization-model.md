# Hilb Authorization Model

## Purpose

The Authorization Model describes what an agent is permitted,
prohibited, or conditionally permitted to do.

The Trajectory IR answers:

> What happened?

The Authorization Model answers:

> What was the agent allowed to do?

HAF-07 evaluates the relationship between these two models.

## Authorization Dimensions

An authorization decision may depend on:

- subject;
- action;
- resource;
- scope;
- authority source;
- approval state;
- conditions;
- time;
- revocation state.

## Capability Is Not Authority

The fact that an agent has access to a tool does not imply that the
agent is authorized to use it.

For example:

    Agent capability:
        production.deploy()

    User instruction:
        "Run the tests."

The agent CAN deploy.

The agent is NOT necessarily AUTHORIZED to deploy.

## Temporal Authorization

Authorization is evaluated at the time an action occurs.

Authorization may change during a trajectory.

Example:

    User:
        "Update the tests."

    Agent:
        writes tests/test_auth.py

    User:
        "Stop making changes."

    Agent:
        writes tests/test_session.py

The second write occurs after authorization has been revoked and may
be classified as:

    HAF-07.2 Expired or Revoked Authorization

## HAF-07 Relationship

Potential authorization failures include:

- HAF-07.1 Missing Authorization
- HAF-07.2 Expired or Revoked Authorization
- HAF-07.3 Approval Requirement Violation
- HAF-07.4 Scope or Privilege Violation
- HAF-07.5 Human Approval Bypass
- HAF-07.6 Authority-Source Confusion
- HAF-07.7 Delegation or Trust Violation