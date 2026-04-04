---
name: whispernote-models
description: "ASR and diarization model defaults, whispernote.json, and CLI overrides."
triggers:
  - asr model
  - diarization model
  - whispernote.json
  - -ma
  - -md
  - mlx whisper checkpoint
  - model override
dependencies:
  - whispernote-hf-setup
version: "1.0.0"
---

# WhisperNote — models and config

Use when changing **defaults**, **`whispernote.json`**, or **CLI flags** `-ma` / `-md`, or when explaining precedence.

## Defaults (single source in code)

[`defaults.py`](../../../src/whispernote/defaults.py):

- **`DEFAULT_ASR_MODEL`** — MLX Whisper `path_or_hf_repo` (default `mlx-community/whisper-tiny`).
- **`DEFAULT_DIARIZATION_MODEL`** — pyannote pipeline Hub id (default `pyannote/speaker-diarization-community-1`).

Keep [`whispernote.json.example`](../../../whispernote.json.example) aligned when defaults or keys change.

## `whispernote.json`

- **Filename** must be exactly `whispernote.json` ([`CONFIG_FILENAME`](../../../src/whispernote/config.py)).
- **Discovery** without `--config`: first existing file wins — `./whispernote.json`, then `~/.config/whispernote/whispernote.json`.
- **With `--config`:** full path; basename must be `whispernote.json` or load fails with `ValueError`.
- **Keys** (object): `asr_model`, `diarization_model` — Hub ids or **local paths** (strings). No token in JSON; use `HF_TOKEN` in the environment (see **whispernote-hf-setup**).

## Precedence

**CLI** (`-ma` / `-md`) **>** JSON values **>** **defaults** ([`cli.main`](../../../src/whispernote/cli.py)).

## ASR (MLX Whisper)

[`run_transcription`](../../../src/whispernote/transcribe.py) passes `model_path` to `mlx_whisper.transcribe(..., path_or_hf_repo=model_path, word_timestamps=True)`.

## Diarization (pyannote)

[`run_diarization`](../../../src/whispernote/diarize.py): `model_id` can be a Hub id or a **local directory** (expanded path). Local pipelines load **without** `HF_TOKEN`; Hub ids require token unless your environment already satisfies Hub auth another way — see **whispernote-hf-setup**.

## Offline / local pipeline

After accepting model terms, users may clone the pipeline and point `-md` or `diarization_model` at that directory — then no Hub download on load from disk.
