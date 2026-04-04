---
name: whispernote-hf-setup
description: "Hugging Face gated models, HF_TOKEN, and local-first alternatives for WhisperNote."
triggers:
  - hugging face
  - HF_TOKEN
  - gated model
  - accept terms
  - model card
  - download failed
  - authentication
dependencies: []
version: "1.0.0"
---

# WhisperNote — Hugging Face setup

Use when the user hits **401/403**, **missing token**, or **gated model** errors, or when configuring Hub access for the default pyannote pipeline or MLX Whisper Hub checkpoints.

## Rules (do not skip)

1. **On the website, in order:** accept **user conditions** on **each** gated model card you need, **then** create a token at [hf.co/settings/tokens](https://huggingface.co/settings/tokens). A token does **not** replace accepting terms.
2. **Locally:** set **`HF_TOKEN`** (e.g. copy [`.env.example`](../../../.env.example) to `.env` in the **current working directory** when you run `whispernote`). `python-dotenv` loads `.env` from the process cwd ([`cli.main`](../../../src/whispernote/cli.py)); you can also `export HF_TOKEN=...` in the shell.
3. **Default diarization** [`pyannote/speaker-diarization-community-1`](https://huggingface.co/pyannote/speaker-diarization-community-1) is gated — see pyannote’s community-1 docs for the acceptance flow.

## Runtime behavior (code)

- [`run_diarization`](../../../src/whispernote/diarize.py): if `model_id` resolves to an **existing local path**, the pipeline loads **without** `HF_TOKEN`. If it is a **Hub id**, **`HF_TOKEN` must be set** or WhisperNote raises a clear `ValueError`.
- ASR via **mlx-whisper** Hub repos follows mlx-whisper / Hugging Face Hub behavior for that checkpoint; gated MLX models still need card acceptance + token as usual.

## Cache

Hub artifacts cache under `~/.cache/huggingface/hub` (standard Hugging Face cache).

## Telemetry

WhisperNote sets `PYANNOTE_METRICS_ENABLED` to `0` by default before importing pyannote (see [`diarize.py`](../../../src/whispernote/diarize.py) and [README](../../../README.md)). Opt-in only if the user sets `PYANNOTE_METRICS_ENABLED=1` before starting Python.
