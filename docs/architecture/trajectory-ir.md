# Hilb Trajectory IR

## Purpose

The Hilb Trajectory Intermediate Representation (IR) provides a
vendor-neutral representation of agent execution.

Engine-specific traces are normalized into this representation before
reliability analysis.

Examples of possible producers include:

- Claude Code
- Codex
- AgentRx
- synthetic Hilb scenarios
- future agent frameworks

## Design Goals

The IR MUST:

- preserve chronological ordering;
- preserve actor identity;
- represent user instructions;
- represent agent actions;
- represent action targets;
- represent action arguments;
- represent execution results;
- represent approval and denial events;
- retain provenance to the original event where possible.

The IR SHOULD NOT:

- contain HAF classifications;
- determine whether an action is safe;
- contain engine-specific policy logic;
- assume a particular agent framework.

## Trajectory

A trajectory represents one evaluated agent run.

Example:

```yaml
run_id: run-001
engine: claude-code

task:
  instruction: "Update the authentication tests only."

steps:
  - index: 1
    actor: agent
    type: file_read
    target: src/auth.py

  - index: 2
    actor: agent
    type: file_write
    target: tests/test_auth.py

  - index: 3
    actor: agent
    type: file_write
    target: src/auth.py