# WhisperNote

Diarized transcription on **Apple Silicon**: [MLX Whisper](https://github.com/ml-explore/mlx-examples/tree/main/whisper) for ASR and [pyannote.audio](https://github.com/pyannote/pyannote-audio) for speaker diarization. Word-level timestamps are merged with diarization using a midpoint rule, then exported as SRT, plain text, or JSON.

## Requirements

- **macOS** with Apple Silicon (MLX targets Metal; diarization uses MPS when available, otherwise CPU).
- **Python** 3.10+
- **ffmpeg** on your `PATH` (for audio normalization).
- **Hugging Face** account and token with access to the gated [speaker-diarization-3.1](https://huggingface.co/pyannote/speaker-diarization-3.1) model.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Copy `.env.example` to `.env` and set `HF_TOKEN`, or export it in your shell:

```bash
export HF_TOKEN=hf_...
```

## Hugging Face Model Cache (Local-first)

WhisperNote is designed to run locally. Hugging Face models are downloaded and reused from:

```text
~/.cache/huggingface/hub
```

This is the preferred workflow: local model cache + local inference.

## Usage

```bash
whispernote path/to/recording.m4a --format srt
```

Or:

```bash
python -m whispernote path/to/recording.m4a --format json
```

Outputs `<basename>.srt` (or `.txt` / `.json`) in the current working directory.

Optional shell helper (same normalization as the CLI):

```bash
chmod +x scripts/normalize_audio.sh
./scripts/normalize_audio.sh input.mp3 normalized.wav
```

## Tests

```bash
pytest
```

## License

MIT
