"""Transcript exporters (`srt`, `txt`, `json`, `md`).

Format rules: `.skills/_skills/whispernote-export-formats/SKILL.md`."""
import json
from typing import List
from dataclasses import asdict
from .merge import TranscriptLine

def _format_srt_time(seconds: float) -> str:
    """Converts seconds to HH:MM:SS,mmm format for SRT."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def _format_markdown_time(seconds: float) -> str:
    """Converts seconds to HH:MM:SS.mmm format for Markdown."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"

def export_srt(transcript: List[TranscriptLine], output_path: str):
    """Exports to SubRip Subtitle (.srt) format."""
    with open(output_path, "w", encoding="utf-8") as f:
        for i, line in enumerate(transcript, 1):
            f.write(f"{i}\n")
            f.write(f"{_format_srt_time(line.start)} --> {_format_srt_time(line.end)}\n")
            f.write(f"[{line.speaker}] {line.text}\n\n")

def export_txt(transcript: List[TranscriptLine], output_path: str):
    """Exports to a plain text file."""
    with open(output_path, "w", encoding="utf-8") as f:
        for line in transcript:
            f.write(f"[{line.speaker}] {line.text}\n")

def export_json(transcript: List[TranscriptLine], output_path: str):
    """Exports raw structured data for API/Web consumption."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump([asdict(line) for line in transcript], f, indent=2)

def export_markdown(transcript: List[TranscriptLine], output_path: str):
    """Exports to a simple Markdown transcript."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Diarized Transcript\n\n")
        for line in transcript:
            start = _format_markdown_time(line.start)
            end = _format_markdown_time(line.end)
            f.write(f"- **{line.speaker}** (`{start} - {end}`): {line.text}\n")
