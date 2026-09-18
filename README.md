# Hilbert Agent Harness

Open research infrastructure for testing agent reliability, safety, recovery behavior, and production readiness.

Hilbert Agent Harness starts from a simple premise: agent evaluation should not stop at whether a task eventually succeeds. Production agents also need to make good decisions when tools fail, context is stale, authorization is unclear, external state is ambiguous, or a retry could create a harmful side effect.

This repository contains the initial Hilbert Agent Failure taxonomy, contribution workflow, and starter code for maintaining machine-readable benchmark definitions.

## What is included

- `docs/taxonomy.md` describes the Hilbert Agent Failure taxonomy v0.1.
- `taxonomy/haf-v0.1.json` provides the same taxonomy in machine-readable form.
- `src/hilbert_harness/` contains lightweight Python helpers for loading taxonomy files.
- `tests/` contains a minimal validation test.
- `.github/ISSUE_TEMPLATE/` contains templates for proposing taxonomy changes and benchmark tasks.

## Research scope

The project focuses on agent behavior under operational stress:

- reliability under repeated runs, perturbations, and injected faults
- tool selection and tool execution failures
- state, concurrency, and external side effects
- privacy, authorization, and authority boundaries
- prompt injection and adversarial tool or memory conditions
- recovery decisions such as act, verify, ask, escalate, or abort

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

Load the taxonomy:

```python
from hilbert_harness.taxonomy import load_taxonomy

taxonomy = load_taxonomy("taxonomy/haf-v0.1.json")
print(taxonomy["name"])
```

## Contributing

We welcome contributions that make agent evaluation more concrete, reproducible, and useful to builders.

Good first contributions include:

- adding citations or notes to an existing taxonomy category
- proposing a new subcategory with a concrete failure example
- adding a benchmark task description
- improving the validation scripts
- adding small, reproducible examples of agent failure and recovery behavior

Before opening a pull request, read `CONTRIBUTING.md` and `docs/taxonomy.md`.

## License

Code is licensed under the Apache License 2.0. Documentation, taxonomy text, and benchmark descriptions are licensed under CC BY 4.0. See `LICENSE` and `LICENSE-DOCS.md`.

