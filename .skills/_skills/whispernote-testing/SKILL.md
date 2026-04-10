---
name: whispernote-testing
description: "Running and extending pytest for WhisperNote (layout, scope, config tests)."
triggers:
  - pytest
  - run tests
  - add test
  - test whispernote
dependencies: []
version: "1.0.0"
---

# WhisperNote — testing

Use when running the suite, adding tests, or debugging CI/local test failures.

## How to run

From the **repository root**, with dev extras installed (`uv sync --extra dev`):

```bash
uv run pytest
```

[`pyproject.toml`](../../../pyproject.toml) sets `[tool.pytest.ini_options]`:

- `testpaths = ["tests"]`
- `pythonpath = ["src"]` — **do not** require `PYTHONPATH` for `from whispernote...` imports in tests.

## What exists (orient here)

| Area | File(s) |
|------|---------|
| Config loading / basename rules | [`tests/test_config.py`](../../../tests/test_config.py) |
| Merge / speaker assignment | [`tests/test_merge.py`](../../../tests/test_merge.py) |
| Diarization segment parsing | [`tests/test_diarize_segments.py`](../../../tests/test_diarize_segments.py) |
| Markdown export | [`tests/test_export_markdown.py`](../../../tests/test_export_markdown.py) |

## Heavy dependencies

Tests that import **`whispernote.diarize`** or **`whispernote.transcribe`** pull **torch / pyannote / mlx** stacks. Prefer **unit tests** that avoid full inference when possible; integration-style tests need the runtime environment available (Apple Silicon assumptions for MPS may apply).

## Adding tests

- Mirror package behavior under `tests/`; use `tmp_path` / `monkeypatch` like `test_config.py`.
- For new export or merge behavior, add focused assertions on strings or data structures rather than full CLI subprocess unless e2e is required.
