# WhisperNote — agent notes

**WhisperNote** is a local CLI for diarized transcription on **Apple Silicon**: MLX Whisper for ASR and pyannote.audio for speaker diarization. Package lives under `src/whispernote/`; install via `uv sync --extra dev` and run with `uv run whispernote` (see [`pyproject.toml`](pyproject.toml)). Tests: `uv run pytest` with `pythonpath = ["src"]`. For user-facing setup and flags, see [`README.md`](README.md).

## Skills (agnostic / multi-ecosystem)

This repository is configured for **Path B**: portable skills only—**no** tool-specific runtime harness is installed in this tree.

- **Manifest:** [`.skills/_index.md`](.skills/_index.md) lists every skill under `.skills/_skills/`.
- **Harness templates** under [`.skills/_harness/`](.skills/_harness/) (`*_template.md`) are **reference** for clones or consumers who adopt a single-ecosystem harness elsewhere. **Do not** paste those templates into this file or commit Cursor/Codex/Claude-specific harness bodies here unless the project explicitly moves to Path A.
- **Authoring:** Use bundled `skill-template` / `skill-author` and keep the index in sync when adding skills. Load a skill’s full `SKILL.md` only when the task clearly needs it.

### WhisperNote domain skills (summary)

| Skill | Use when |
|-------|----------|
| `whispernote-hf-setup` | Gated Hub models, `HF_TOKEN`, `.env`, download/auth errors |
| `whispernote-internals` | End-to-end pipeline, `ffmpeg` prep, lazy imports, refactor flow |
| `whispernote-export-formats` | Changing or adding `srt` / `txt` / `json` / `md` output |
| `whispernote-testing` | Running `pytest`, adding tests, `pythonpath` |
| `whispernote-models` | `whispernote.json`, `-ma` / `-md`, defaults vs overrides |

[`pyproject.toml`](pyproject.toml), [`README.md`](README.md), [`scripts/`](scripts/), and `src/whispernote/` are kept aligned with these skills; prefer skills for procedural detail and README for end-user documentation.
