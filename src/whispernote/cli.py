import argparse
import os
import subprocess
import sys
import tempfile

from dotenv import load_dotenv

from .config import CONFIG_FILENAME, load_models_config
from .defaults import DEFAULT_ASR_MODEL, DEFAULT_DIARIZATION_MODEL
from .merge import assign_speakers_to_words
from .export import export_srt, export_txt, export_json, export_markdown

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
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="MLX Whisper + pyannote speaker diarization"
    )
    parser.add_argument("input_file", help="Path to input audio/video file")
    parser.add_argument(
        "--format",
        choices=["srt", "txt", "json", "md"],
        default="srt",
        help="Output format",
    )
    parser.add_argument(
        "--output",
        default=None,
        help=(
            "Output file path OR output directory. "
            "If omitted, defaults to '<basename>.<format>' in the current directory."
        ),
    )
    parser.add_argument(
        "--config",
        default=None,
        help=(
            f"Path to {CONFIG_FILENAME} (basename must be exactly that). "
            "If omitted, the first existing file is used: ./whispernote.json, "
            "then ~/.config/whispernote/whispernote.json."
        ),
    )
    parser.add_argument(
        "-ma",
        "--model-asr",
        default=None,
        dest="asr_model",
        metavar="ID_OR_PATH",
        help=(
            f"MLX Whisper Hub id or local dir, path_or_hf_repo (default: {DEFAULT_ASR_MODEL!r}). "
            "Overrides config."
        ),
    )
    parser.add_argument(
        "-md",
        "--model-diarization",
        default=None,
        dest="diarization_model",
        metavar="ID_OR_PATH",
        help=(
            f"pyannote diarization pipeline Hub id or local path (default: {DEFAULT_DIARIZATION_MODEL!r}). "
            "Overrides config."
        ),
    )
    args = parser.parse_args()

    try:
        cfg = load_models_config(args.config)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        sys.exit(2)
    asr_model = args.asr_model or cfg.get("asr_model") or DEFAULT_ASR_MODEL
    diarization_model = (
        args.diarization_model or cfg.get("diarization_model") or DEFAULT_DIARIZATION_MODEL
    )

    base_name = os.path.splitext(os.path.basename(args.input_file))[0]
    default_out_file = os.path.join(os.getcwd(), f"{base_name}.{args.format}")
    out_file = default_out_file
    if args.output:
        output_path = os.path.expanduser(args.output)
        if os.path.isdir(output_path) or args.output.endswith(os.sep):
            out_file = os.path.join(output_path, f"{base_name}.{args.format}")
        else:
            out_file = output_path

    parent_dir = os.path.dirname(out_file)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)

    fd, temp_wav = tempfile.mkstemp(suffix=".wav", prefix="whispernote_")
    os.close(fd)
    try:
        preprocess_audio(args.input_file, temp_wav)

        # Lazy imports so `--help` doesn't trigger heavyweight ML imports.
        from .diarize import run_diarization
        from .transcribe import run_transcription

        segments = run_diarization(temp_wav, model_id=diarization_model)
        words = run_transcription(temp_wav, model_path=asr_model)

        transcript = assign_speakers_to_words(words, segments)

        if args.format == "srt":
            export_srt(transcript, out_file)
        elif args.format == "txt":
            export_txt(transcript, out_file)
        elif args.format == "md":
            export_markdown(transcript, out_file)
        else:
            export_json(transcript, out_file)

        print(f"\nSuccess! Saved to {out_file}")
    finally:
        if os.path.exists(temp_wav):
            os.remove(temp_wav)

if __name__ == "__main__":
    main()
