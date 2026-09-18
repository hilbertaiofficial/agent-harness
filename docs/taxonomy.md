# Hilbert Agent Failure Taxonomy v0.1

The Hilbert Agent Failure taxonomy is a working structure for describing how AI agents fail in production-like workflows. It is designed for benchmarks, incident review, red-team exercises, and recovery policy design.

The taxonomy emphasizes observable agent behavior: what the agent believed, which tool or action it chose, what state it changed, and whether it verified, asked, escalated, aborted, or recovered safely.

## Design goals

- Separate task success from operational safety.
- Make failures easy to label from traces.
- Support both normal-condition reliability tests and adversarial evaluations.
- Cover tool use, memory, state, authorization, recovery, and side effects.
- Leave room for benchmark-specific scoring without hiding the failure mechanism.

## Categories

### HAF-01 Goal and Reasoning Failure

The agent misunderstands the task, constraints, plan, or evidence.

Subcategories: goal misinterpretation, constraint misinterpretation, planning failure, plan-adherence failure, unsupported assumption, fabricated information.

### HAF-02 Tool Selection Failure

The agent chooses the wrong tool, omits a required tool, invokes an unsupported capability, or sequences tools incorrectly.

Subcategories: wrong tool, unnecessary tool, missing required tool, unsupported capability, wrong tool sequence.

### HAF-03 Tool Execution Failure

The agent invokes a tool incorrectly or handles tool runtime conditions poorly.

Subcategories: invalid invocation, invalid arguments, schema violation, timeout, rate limit, tool unavailable, malformed response.

### HAF-04 Data and Observation Failure

The agent uses stale, missing, incorrect, conflicting, misread, or unverified data.

Subcategories: stale data, missing data, incorrect data, conflicting data, tool-output misinterpretation, unverified data.

### HAF-05 Context and Memory Failure

The agent loses relevant context, uses irrelevant context, pollutes memory, or confuses instruction priority.

Subcategories: relevant context lost, irrelevant context used, context contamination, memory poisoning, cross-session contamination, instruction-priority confusion.

### HAF-06 State and Concurrency Failure

The agent acts on state that changed, is only partially updated, or cannot be verified.

Subcategories: stale state, state changed during execution, concurrent modification, partial state transition, acknowledgement loss, execution status unknown, state verification failure.

### HAF-07 Authorization and Authority Failure

The agent lacks authorization, exceeds scope, bypasses approval, or trusts the wrong authority source.

Subcategories: missing authorization, expired or revoked authorization, approval threshold violation, scope or privilege violation, human approval bypass, authority-source confusion, delegation or trust violation.

### HAF-08 Security and Adversarial Failure

The agent is compromised or manipulated by attacks against prompts, tools, plugins, data, credentials, memory, or inter-agent trust.

Subcategories: direct prompt injection, indirect prompt injection, goal hijacking, tool or plugin poisoning, data exfiltration, credential or secret exposure, memory poisoning, inter-agent trust attack.

### HAF-09 Recovery and Retry Failure

The agent recovers unsafely, retries without verification, loops excessively, rolls back incorrectly, or aborts too early.

Subcategories: unsafe retry under unknown state, non-idempotent retry, missing verification before retry, excessive retry loop, incorrect rollback, unsafe fallback, premature abort, failure to recover.

### HAF-10 Side-Effect Failure

The agent creates the wrong external effect, duplicates an action, affects the wrong target, or increases blast radius.

Subcategories: duplicate action, incorrect target, incorrect value or amount, partial execution, irreversible unsafe action, excessive blast radius, action after cancellation or revocation, unintended external effect.

### HAF-11 Autonomy and Human-Handoff Failure

The agent fails to ask, escalate, abort, respect rejection, or correctly interpret human instruction.

Subcategories: failure to ask, failure to escalate, failure to abort, unnecessary escalation, human rejection ignored, human instruction misinterpreted, premature autonomous action.

## Initial references

This v0.1 taxonomy is informed by work on agent reliability, safety, prompt injection, function calling, stateful tool use, privacy, and recovery under production-like faults, including AgentRx, Agent-SafetyBench, AgentDojo, BFCL, ToolSandbox, Agent Security Bench, ToolEmu, ReliabilityBench, R-Judge, ToolPrivacyBench, AgentSpec, and Inspect.

