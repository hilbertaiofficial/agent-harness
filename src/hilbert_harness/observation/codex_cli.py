import json
import subprocess
from pathlib import Path
from typing import Any


def run_codex_cli(
    workspace: Path,
    instruction: str,
) -> list[dict[str, Any]]:
    command = [
        "codex",
        "exec",
        "--json",
        "--sandbox",
        "workspace-write",
        instruction,
    ]

    result = subprocess.run(
        command,
        cwd=workspace,
        capture_output=True,
        text=True,
        check=True,
    )

    events = [
        json.loads(line)
        for line in result.stdout.splitlines()
        if line.strip()
    ]

    return events