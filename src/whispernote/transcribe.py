"""MLX Whisper ASR (word timestamps). Model path: `.skills/_skills/whispernote-models/SKILL.md`."""
import mlx_whisper
from typing import List, Dict

from .defaults import DEFAULT_ASR_MODEL

def run_transcription(
    audio_path: str,
    model_path: str = DEFAULT_ASR_MODEL,
) -> List[Dict]:
    """Runs mlx_whisper and flattens the output into a list of word dictionaries."""
    print(f"Running MLX Whisper transcription with {model_path}...")

    result = mlx_whisper.transcribe(
        audio_path,
        path_or_hf_repo=model_path,
        word_timestamps=True
    )

    flat_words = []
    for segment in result.get("segments", []):
        for word in segment.get("words", []):
            flat_words.append({
                "word": word["word"],
                "start": word["start"],
                "end": word["end"]
            })

    return flat_words
