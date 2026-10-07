from typing import Any

from hilbert_harness.ir import Trajectory, TrajectoryStep
import json



def adapt_codex_event(
    event: dict[str, Any],
    index: int,
) -> TrajectoryStep:
    item = event["item"]

    if item["type"] == "file_change":
        change = item["changes"][0]

        action_type = {
            "add": "file_write",
            "update": "file_write",
            "delete": "file_delete",
        }[change["kind"]]

        return TrajectoryStep(
            index=index,
            actor="agent",
            actor_role="agent",
            action_type=action_type,
            target=change["path"],
            arguments={
                "path": change["path"],
                "kind": change["kind"],
            },
        )
    
    if item["type"] == "command_execution":
        return TrajectoryStep(
            index=index,
            actor="agent",
            actor_role="agent",
            action_type="command_execution",
            target=None,
            arguments={
                "command": item["command"],
            },
            result={
                "exit_code": item["exit_code"],
                "status": item["status"],
                "aggregated_output": item["aggregated_output"],
            },
        )
    
    raise ValueError(
        f"Unsupported Codex item type: {item['type']}"
    )

def adapt_codex_run(
    events: list[dict[str, Any]],
    run_id: str,
    instruction: str,
) -> Trajectory:
    steps = []

    for event in events:
        if event.get("type") != "item.completed":
            continue

        item = event.get("item", {})

        #if item.get("type") != "file_change":
        if item.get("type") not in {
            "file_change",
            "command_execution",
        }:
            continue

        step = adapt_codex_event(
            event,
            index=len(steps) + 1,
        )
        steps.append(step)

    return Trajectory(
        run_id=run_id,
        engine="codex",
        instruction=instruction,
        steps=steps,
    )

def adapt_codex_jsonl(
    jsonl: str,
    run_id: str,
    instruction: str,
) -> Trajectory:
    events = [
        json.loads(line)
        for line in jsonl.splitlines()
        if line.strip()
    ]

    return adapt_codex_run(
        events,
        run_id=run_id,
        instruction=instruction,
    )