"""Optional JSON model overrides (local-first; HF Hub ids or local paths)."""

from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional


def _expand(path: str) -> str:
    return os.path.abspath(os.path.expanduser(path))


def load_models_config(explicit_path: Optional[str]) -> Dict[str, Any]:
    """Load the first existing JSON config from explicit path, then default locations."""
    candidates = []
    if explicit_path:
        candidates.append(_expand(explicit_path))
    candidates.append(os.path.join(os.getcwd(), "whispernote.json"))
    candidates.append(os.path.expanduser("~/.config/whispernote/config.json"))

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
