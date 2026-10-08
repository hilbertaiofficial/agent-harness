import hashlib
from pathlib import Path

from hilbert_harness.ir.effects import EffectObservation


def capture_filesystem_snapshot(
    root: Path,
) -> dict[str, str]:
    snapshot = {}

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        relative_path = path.relative_to(root).as_posix()

        content = path.read_bytes()
        digest = hashlib.sha256(content).hexdigest()

        snapshot[relative_path] = digest

    return snapshot


def compare_filesystem_snapshots(
    before: dict[str, str],
    after: dict[str, str],
    observed_at_step: int,
) -> list[EffectObservation]:
    observations = []

    for resource in sorted(before.keys() | after.keys()):
        before_hash = before.get(resource)
        after_hash = after.get(resource)

        if before_hash == after_hash:
            continue

        operation = (
            "file_delete"
            if after_hash is None
            else "file_write"
        )

        observations.append(
            EffectObservation(
                operation=operation,
                resource=resource,
                observed_at_step=observed_at_step,
                evidence={
                    "source": "filesystem_snapshot",
                    "before_sha256": before_hash,
                    "after_sha256": after_hash,
                },
            )
        )

    return observations