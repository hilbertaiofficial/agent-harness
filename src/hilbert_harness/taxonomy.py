"""Utilities for loading Hilbert Agent Failure taxonomy files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Union


def load_taxonomy(path: Union[str, Path]) -> dict[str, Any]:
    """Load a taxonomy JSON file and perform minimal structural validation."""
    taxonomy_path = Path(path)
    data = json.loads(taxonomy_path.read_text(encoding="utf-8"))

    required = {"name", "version", "categories"}
    missing = required.difference(data)
    if missing:
        missing_list = ", ".join(sorted(missing))
        raise ValueError(f"taxonomy is missing required keys: {missing_list}")

    if not isinstance(data["categories"], list) or not data["categories"]:
        raise ValueError("taxonomy categories must be a non-empty list")

    for category in data["categories"]:
        if not category.get("id") or not category.get("name"):
            raise ValueError("each category must include id and name")
        if not isinstance(category.get("subcategories"), list):
            raise ValueError(f"{category['id']} must include subcategories")

    return data
