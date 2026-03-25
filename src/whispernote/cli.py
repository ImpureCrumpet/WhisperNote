import argparse
import os
import subprocess
import tempfile

from .diarize import run_diarization
from .transcribe import run_transcription
from .merge import assign_speakers_to_words
from .export import export_srt, export_txt, export_json

def preprocess_audio(input_path: str, output_path: str):
    """Uses ffmpeg to create a 16kHz mono WAV file."""
    print(f"Normalizing audio: {input_path}...")
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", input_path,
            "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le",
            output_path,
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

def main():
    parser = argparse.ArgumentParser(
        description="MLX Whisper + pyannote speaker diarization"
    )
    parser.add_argument("input_file", help="Path to input audio/video file")
    parser.add_argument(
        "--format",
        choices=["srt", "txt", "json"],
        default="srt",
        help="Output format",
    )
    args = parser.parse_args()

    base_name = os.path.splitext(os.path.basename(args.input_file))[0]
    out_file = f"{base_name}.{args.format}"

    fd, temp_wav = tempfile.mkstemp(suffix=".wav", prefix="whispernote_")
    os.close(fd)
    try:
        preprocess_audio(args.input_file, temp_wav)

        segments = run_diarization(temp_wav)
        words = run_transcription(temp_wav)

        transcript = assign_speakers_to_words(words, segments)

        if args.format == "srt":
            export_srt(transcript, out_file)
        elif args.format == "txt":
            export_txt(transcript, out_file)
        else:
            export_json(transcript, out_file)

        print(f"\nSuccess! Saved to {out_file}")
    finally:
        if os.path.exists(temp_wav):
            os.remove(temp_wav)

if __name__ == "__main__":
    main()
