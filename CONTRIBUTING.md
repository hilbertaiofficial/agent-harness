# Contributing to Hilbert Agent Harness

Thank you for helping improve open agent evaluation infrastructure. This project is early, so clear examples and careful definitions matter more than volume.

## Contribution types

We accept:

- taxonomy additions, clarifications, and corrections
- benchmark task proposals
- reproducible failure traces or reduced examples
- evaluator improvements
- documentation improvements
- small utilities that make the taxonomy easier to validate or consume

## Taxonomy contribution standard

Every taxonomy change should include:

1. The category or subcategory affected.
2. A short definition.
3. A concrete example of the failure.
4. A reason the change is distinct from existing categories.
5. At least one supporting reference, benchmark, or trace when available.

Prefer narrow changes. If a proposed category overlaps heavily with an existing category, explain the boundary.

## Benchmark task contribution standard

Every benchmark task proposal should include:

1. The user-facing task.
2. The agent tools or environment required.
3. The expected safe behavior.
4. The failure modes being tested.
5. The scoring approach.
6. Any hidden state, ambiguity, or fault injection used.

For production-like tasks, state whether the correct behavior is to act, verify, ask, escalate, or abort.

## Local development

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Pull request checklist

- The change is scoped and described clearly.
- Taxonomy JSON remains valid.
- Tests pass with `pytest`.
- New categories include examples and references when possible.
- Documentation and machine-readable files are kept in sync.

