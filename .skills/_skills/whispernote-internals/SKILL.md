---
name: whispernote-internals
description: "WhisperNote CLI pipeline: ffmpeg prep, diarize, transcribe, merge, export."
triggers:
  - pipeline
  - architecture
  - where does
  - preprocess
  - lazy import
  - main flow
  - refactor whispernote
dependencies: []
version: "1.0.0"
---

# WhisperNote — internals and pipeline

Use when tracing execution, refactoring the CLI, or matching **audio prep** to other tools (e.g. [`scripts/normalize_audio.sh`](../../../scripts/normalize_audio.sh)).

## Entry point

- Console script: `whispernote` → [`whispernote.cli:main`](../../../src/whispernote/cli.py) ([`pyproject.toml`](../../../pyproject.toml) `[project.scripts]`).

## Pipeline order (always this order)

1. **`load_dotenv()`** — `.env` from cwd.
2. **Config:** [`load_models_config`](../../../src/whispernote/config.py) — merge with CLI overrides for `asr_model` / `diarization_model` (see **whispernote-models** skill).
3. **Output path:** basename from input; default `./<basename>.<format>` unless `--output` is a file or directory.
4. **Audio prep:** [`preprocess_audio`](../../../src/whispernote/cli.py) — `ffmpeg` to **16 kHz mono PCM** temp WAV (`pcm_s16le`). Same parameters as [`scripts/normalize_audio.sh`](../../../scripts/normalize_audio.sh).
5. **Diarization:** [`run_diarization`](../../../src/whispernote/diarize.py) on the temp WAV → list of [`DiarizationSegment`](../../../src/whispernote/merge.py).
6. **ASR:** [`run_transcription`](../../../src/whispernote/transcribe.py) on the **same** temp WAV → word list (`word`, `start`, `end`).
7. **Merge:** [`assign_speakers_to_words`](../../../src/whispernote/merge.py) — speaker per word by **midpoint** of each word interval vs diarization segments.
8. **Export:** [`export_*`](../../../src/whispernote/export.py) by `--format` (`srt` | `txt` | `json` | `md`).
9. **Cleanup:** delete temp WAV.

## Lazy imports

[`cli.main`](../../../src/whispernote/cli.py) imports `diarize` and `transcribe` **inside** the `try` block after argparse so **`whispernote --help`** does not load MLX/pyannote/torch.

## Device

Diarization uses **MPS** if available, else **CPU** ([`diarize.py`](../../../src/whispernote/diarize.py)).
