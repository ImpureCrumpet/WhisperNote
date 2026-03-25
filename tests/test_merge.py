from whispernote.merge import assign_speakers_to_words, DiarizationSegment

def test_midpoint_merge_logic():
    words = [
        {"word": "Hello", "start": 0.0, "end": 0.5},
        {"word": "world", "start": 0.6, "end": 1.0},
        {"word": "Hi", "start": 1.5, "end": 1.8},
    ]

    segments = [
        DiarizationSegment(speaker="SPEAKER_01", start=0.0, end=1.2),
        DiarizationSegment(speaker="SPEAKER_02", start=1.3, end=2.0),
    ]

    transcript = assign_speakers_to_words(words, segments)

    assert len(transcript) == 2
    assert transcript[0].speaker == "SPEAKER_01"
    assert transcript[0].text == "Hello world"

    assert transcript[1].speaker == "SPEAKER_02"
    assert transcript[1].text == "Hi"
