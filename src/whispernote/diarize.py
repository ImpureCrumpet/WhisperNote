import os
import torch
from pyannote.audio import Pipeline
from typing import List
from .merge import DiarizationSegment

def run_diarization(audio_path: str) -> List[DiarizationSegment]:
    """Runs pyannote.audio diarization pipeline."""
    hf_token = os.environ.get("HF_TOKEN")
    if not hf_token:
        raise ValueError(
            "HF_TOKEN environment variable is missing. "
            "Set it to your Hugging Face token (see .env.example)."
        )

    print("Loading pyannote diarization pipeline (this may take a moment)...")
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=hf_token,
    )

    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    pipeline.to(device)

    print(f"Running diarization on {device}...")
    diarization = pipeline(audio_path)

    segments = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        segments.append(DiarizationSegment(
            speaker=speaker,
            start=turn.start,
            end=turn.end
        ))

    del pipeline
    if torch.backends.mps.is_available():
        torch.mps.empty_cache()

    return segments
