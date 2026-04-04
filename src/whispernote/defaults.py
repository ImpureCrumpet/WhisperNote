"""Default model ids (no heavy imports).

Override via `whispernote.json` or CLI; see `.skills/_skills/whispernote-models/SKILL.md`."""

# https://pypi.org/project/mlx-whisper/
DEFAULT_ASR_MODEL = "mlx-community/whisper-tiny"

# https://huggingface.co/pyannote/speaker-diarization-community-1
DEFAULT_DIARIZATION_MODEL = "pyannote/speaker-diarization-community-1"
