import mlx_whisper
from typing import List, Dict

def run_transcription(
    audio_path: str,
    model_path: str = "mlx-community/whisper-large-v3-mlx"
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
