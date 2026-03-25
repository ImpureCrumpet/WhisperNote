from pathlib import Path

from whispernote.export import export_markdown
from whispernote.merge import DiarizationSegment, TranscriptLine, assign_speakers_to_words


def test_export_markdown(tmp_path: Path):
    transcript = assign_speakers_to_words(
        words=[
            {"word": "Hello", "start": 0.0, "end": 0.5},
            {"word": "world", "start": 0.6, "end": 1.0},
        ],
        segments=[
            DiarizationSegment(speaker="SPEAKER_01", start=0.0, end=1.2),
        ],
    )

    out_file = tmp_path / "out.md"
    export_markdown(transcript, str(out_file))

    content = out_file.read_text(encoding="utf-8")
    assert content.startswith("# Diarized Transcript")
    assert "- **SPEAKER_01** (`00:00:00.000 - 00:00:01.000`): Hello world" in content

