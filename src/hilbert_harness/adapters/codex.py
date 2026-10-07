from typing import Any

from hilbert_harness.ir import TrajectoryStep



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