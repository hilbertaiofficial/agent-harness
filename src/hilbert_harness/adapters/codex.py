from typing import Any

from hilbert_harness.ir import Trajectory, TrajectoryStep



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

        if item.get("type") != "file_change":
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