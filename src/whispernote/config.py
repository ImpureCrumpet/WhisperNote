"""Optional JSON model overrides (HF Hub ids or local paths).

Discovery rules and keys: `.skills/_skills/whispernote-models/SKILL.md`; manifest `.skills/_index.md`.
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional

CONFIG_FILENAME = "whispernote.json"


def _expand(path: str) -> str:
    return os.path.abspath(os.path.expanduser(path))


def config_location_help() -> str:
    """Human-readable rules for config path and search order (for errors and docs)."""
    return (
        f"Config must be a file named {CONFIG_FILENAME!r}. "
        "Without --config, the first existing file wins: "
        f"(1) ./{CONFIG_FILENAME} (current working directory), "
        f"(2) ~/.config/whispernote/{CONFIG_FILENAME} (machine-wide, lowest precedence). "
        f"With --config, give the full path to a {CONFIG_FILENAME} file."
    )


def load_models_config(explicit_path: Optional[str]) -> Dict[str, Any]:
    """Load model overrides from whispernote.json.

    If explicit_path is set (--config), that path must exist and its basename must be
    CONFIG_FILENAME (no fallback to other locations).

    If explicit_path is None, use the first existing file among the default locations.
    """
    if explicit_path is not None:
        path = _expand(explicit_path.strip())
        if os.path.basename(path) != CONFIG_FILENAME:
            raise ValueError(
                f"Invalid config path {explicit_path!r}: expected basename "
                f"{CONFIG_FILENAME!r}, got {os.path.basename(path)!r}.\n"
                + config_location_help()
            )
        if not os.path.isfile(path):
            raise ValueError(
                f"Config file not found: {path}\n" + config_location_help()
            )
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            raise ValueError(f"Config must be a JSON object: {path}")
        return data

    candidates = [
        os.path.join(os.getcwd(), CONFIG_FILENAME),
        os.path.expanduser(f"~/.config/whispernote/{CONFIG_FILENAME}"),
    ]
    seen: set[str] = set()
    for path in candidates:
        if path in seen:
            continue
        seen.add(path)
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError(f"Config must be a JSON object: {path}")
            return data
    return {}
