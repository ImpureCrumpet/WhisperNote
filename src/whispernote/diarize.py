import os
from typing import Any, List

# pyannote.audio optional Hub telemetry: default off unless user set PYANNOTE_METRICS_ENABLED
# (see README — upstream docs: https://github.com/pyannote/pyannote-audio#telemetry).
os.environ.setdefault("PYANNOTE_METRICS_ENABLED", "0")

import torch
from pyannote.audio import Pipeline

from .defaults import DEFAULT_DIARIZATION_MODEL
from .merge import DiarizationSegment


def segments_from_pipeline_output(output: Any) -> List[DiarizationSegment]:
    """Normalize pyannote pipeline output to DiarizationSegment list.

    Supports:
    - community-1 style: iterable `output.speaker_diarization` of (turn, speaker)
    - legacy Annotation: `itertracks(yield_label=True)`
    """
    segments: List[DiarizationSegment] = []
    if hasattr(output, "speaker_diarization"):
        for turn, speaker in output.speaker_diarization:
            segments.append(
                DiarizationSegment(
                    speaker=str(speaker),
                    start=float(turn.start),
                    end=float(turn.end),
                )
            )
        return segments

    for turn, _, speaker in output.itertracks(yield_label=True):
        segments.append(
            DiarizationSegment(
                speaker=str(speaker),
                start=float(turn.start),
                end=float(turn.end),
            )
        )
    return segments


def _pipeline_from_pretrained(model_id: str, hf_token: str) -> Pipeline:
    try:
        return Pipeline.from_pretrained(model_id, token=hf_token)
    except TypeError:
        return Pipeline.from_pretrained(model_id, use_auth_token=hf_token)


def run_diarization(
    audio_path: str,
    *,
    model_id: str = DEFAULT_DIARIZATION_MODEL,
) -> List[DiarizationSegment]:
    """Runs pyannote.audio diarization pipeline (Hub id or local clone path)."""
    resolved = os.path.abspath(os.path.expanduser(model_id))
    is_local = os.path.exists(resolved)

    hf_token = os.environ.get("HF_TOKEN")
    if not is_local and not hf_token:
        raise ValueError(
            "HF_TOKEN environment variable is missing. "
            "Set it in `.env` or your shell (see .env.example), "
            "or pass a local pipeline path (offline clone)."
        )

    print(f"Loading pyannote diarization pipeline: {model_id!r} (this may take a moment)...")
    if is_local:
        pipeline = Pipeline.from_pretrained(resolved)
    else:
        pipeline = _pipeline_from_pretrained(model_id, hf_token)

    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    pipeline.to(device)

    print(f"Running diarization on {device}...")
    diarization = pipeline(audio_path)
    segments = segments_from_pipeline_output(diarization)

    del pipeline
    if torch.backends.mps.is_available():
        torch.mps.empty_cache()

    return segments
