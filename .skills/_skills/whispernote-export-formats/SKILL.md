---
name: whispernote-export-formats
description: "Transcript export formats (srt, txt, json, md) and time formatting rules."
triggers:
  - export srt
  - export json
  - export markdown
  - subtitle format
  - TranscriptLine
  - output format
dependencies: []
version: "1.0.0"
---

# WhisperNote — export formats

Use when changing [`export.py`](../../../src/whispernote/export.py), adding a format, or explaining output layout.

## Data model

Exports consume **`List[TranscriptLine]`** from [`merge.assign_speakers_to_words`](../../../src/whispernote/merge.py):

- `speaker: str`
- `start`, `end`: seconds (`float`)
- `text: str`

## Formats

| `--format` | Function | Notes |
|------------|----------|--------|
| `srt` | `export_srt` | SubRip: 1-based index, **`HH:MM:SS,mmm`** (comma before ms), blank line between cues. Line text: `[{speaker}] {text}`. |
| `txt` | `export_txt` | One line per merged utterance: `[{speaker}] {text}` (no timestamps in plain export). |
| `json` | `export_json` | `json.dump` of `[asdict(line) ...]` with indent 2 — keys `speaker`, `start`, `end`, `text`. |
| `md` | `export_markdown` | Title `# Diarized Transcript`, then bullets: **speaker**, timestamps in backticks using **`HH:MM:SS.mmm`** (dot before ms, unlike SRT comma). |

## Time helpers

- SRT: `_format_srt_time` — comma separator for milliseconds.
- Markdown: `_format_markdown_time` — dot separator for milliseconds.

Keep new formats UTF-8 (`encoding="utf-8"`) like existing writers.
