"""Merge diarization segments with word-level ASR (midpoint rule). See `.skills/_skills/whispernote-internals/SKILL.md`."""
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class DiarizationSegment:
    speaker: str
    start: float
    end: float

@dataclass
class TranscriptLine:
    speaker: str
    start: float
    end: float
    text: str

def assign_speakers_to_words(
    words: List[Dict],
    segments: List[DiarizationSegment]
) -> List[TranscriptLine]:
    transcript: List[TranscriptLine] = []

    for w in words:
        word_text = w['word']
        w_start = w['start']
        w_end = w['end']
        midpoint = (w_start + w_end) / 2

        current_speaker = "UNKNOWN"
        for seg in segments:
            if seg.start <= midpoint <= seg.end:
                current_speaker = seg.speaker
                break

        if transcript and transcript[-1].speaker == current_speaker:
            transcript[-1].text += f" {word_text.strip()}"
            transcript[-1].end = w_end
        else:
            transcript.append(TranscriptLine(
                speaker=current_speaker,
                start=w_start,
                end=w_end,
                text=word_text.strip()
            ))

    return transcript
