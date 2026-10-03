# Hilb Harness Architecture

Hilb Harness evaluates the operational reliability of autonomous and
tool-using AI agents.

Hilb separates:

1. environmental faults,
2. agent observations,
3. external system state,
4. agent decisions,
5. behavioral failures,
6. consequences, and
7. severity.

The basic execution model is:

    Fault / Condition
            ↓
    Environment State
            ↓
    Agent Observation
            ↓
    Agent Decision
            ↓
    HAF Classification
            ↓
    Consequence
            ↓
    Severity

## Core Components

### Engine Adapter

An engine adapter converts engine-specific traces from systems such as
Claude Code or Codex into the Hilb Trajectory IR.

### Trajectory IR

The Trajectory Intermediate Representation is a vendor-neutral record
of what happened during an agent run.

### Reliability Contract

A Reliability Contract defines behavioral requirements that must hold
during execution.

Authorization rules are one type of Reliability Contract.

### Checker

A checker evaluates trajectory events against applicable contracts and
known environment state.

### HAF

The Hilb Agent Failure Taxonomy classifies observed agent behavioral
failures.

### Important Principle

Environmental faults are not automatically agent failures.

For example, an API timeout is an environmental fault.

If an agent responds to the timeout by retrying a non-idempotent action
without verifying whether the original action committed, the unsafe
recovery behavior may constitute a HAF failure.