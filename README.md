# WhisperNote

Diarized transcription on **Apple Silicon**: [MLX Whisper](https://github.com/ml-explore/mlx-examples/tree/main/whisper) for ASR and [pyannote.audio](https://github.com/pyannote/pyannote-audio) for speaker diarization. Word-level timestamps are merged with diarization using a midpoint rule, then exported as `srt`, `txt`, `json`, or `md`.

## Quick start

1. Install `ffmpeg` (used for audio normalization), e.g. with Homebrew:
   ```bash
   brew install ffmpeg
   ```
   Other installs work too; `whispernote` only requires `ffmpeg` on your `PATH`.

2. Install the Python package:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   ```

3. Hugging Face token (for gated pyannote pipelines and Hub downloads):
   ```bash
   cp .env.example .env
   # edit .env: HF_TOKEN=hf_...
   ```
   `python-dotenv` loads `.env` from the current working directory when you run `whispernote`. You can still `export HF_TOKEN=...` in the shell if you prefer.

4. Run:
   ```bash
   whispernote path/to/recording.m4a --format srt
   ```
   Optional output location:
   ```bash
   whispernote path/to/recording.m4a --format json --output ./out.json
   whispernote path/to/recording.m4a --format srt --output ./out_dir
   whispernote path/to/recording.m4a --format md --output ./out_dir
   ```

## Supported input/output

| Input (what ffmpeg can decode) | Output |
|---|---|
| any audio/video format supported by `ffmpeg` (e.g. `mp3`, `wav`, `m4a`, `mp4`) | `--format srt` -> `.srt`, `--format txt` -> `.txt`, `--format json` -> `.json`, `--format md` -> `.md` |

## Model behavior (local-first)

Inference runs on your machine. On first use, Hub weights are downloaded into:

```text
~/.cache/huggingface/hub
```

That matches how [`mlx_whisper.transcribe`](https://pypi.org/project/mlx-whisper/) resolves `path_or_hf_repo`: a Hub id triggers a one-time download, then reuse from cache.

### Defaults (no overrides)

| Component | Default | Notes |
|---|---|---|
| ASR | `mlx-community/whisper-tiny` | Same default as [`mlx-whisper` on PyPI](https://pypi.org/project/mlx-whisper/) (`path_or_hf_repo`). |
| Diarization | `pyannote/speaker-diarization-community-1` | Open-source pipeline from pyannote on Hugging Face ([model card](https://huggingface.co/pyannote/speaker-diarization-community-1)); **gated**—log in, accept terms, set `HF_TOKEN`. |

### Overrides (CLI and config)

Priority: **CLI flags** > **config file** > **defaults**.

- CLI:
  - `--asr-model` — MLX Whisper Hub repo id or local directory (passed to `mlx_whisper.transcribe(..., path_or_hf_repo=...)`).
  - `--diarization-model` — pyannote pipeline Hub id or **local path** to an offline clone.

- Config (optional JSON), first file found wins:
  1. path from `--config`
  2. `./whispernote.json`
  3. `~/.config/whispernote/config.json`

  Keys: `asr_model`, `diarization_model`. See `whispernote.json.example`.

Example:
```bash
whispernote audio.m4a --asr-model mlx-community/whisper-large-v3-mlx
```

### Offline / local pyannote pipeline

After you have accepted the model terms and cloned the pipeline (see [offline use](https://huggingface.co/pyannote/speaker-diarization-community-1)), you can point `--diarization-model` (or `diarization_model` in JSON) at that directory. In that case **no `HF_TOKEN` is required** for loading the pipeline from disk.

### What we do not support

- **pyannote “precision-2” / pyannoteAI cloud** and other paid or remote-only flows are out of scope for this repo.

### Choosing other MLX Whisper checkpoints

Browse the Hugging Face **[mlx-community Whisper collection](https://huggingface.co/collections/mlx-community/whisper)** and pass any compatible repo id via `--asr-model` or `asr_model` in config.

## Tests

```bash
pytest
```

## License

MIT
