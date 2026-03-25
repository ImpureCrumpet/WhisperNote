from whispernote.diarize import segments_from_pipeline_output
from whispernote.merge import DiarizationSegment


class _Turn:
    def __init__(self, start: float, end: float):
        self.start = start
        self.end = end


def test_segments_from_community_style_output():
    class Out:
        speaker_diarization = [
            (_Turn(0.0, 1.0), "SPEAKER_00"),
            (_Turn(1.5, 2.0), "SPEAKER_01"),
        ]

    segs = segments_from_pipeline_output(Out())
    assert segs == [
        DiarizationSegment(speaker="SPEAKER_00", start=0.0, end=1.0),
        DiarizationSegment(speaker="SPEAKER_01", start=1.5, end=2.0),
    ]


def test_segments_from_legacy_annotation():
    class Turn:
        def __init__(self, start: float, end: float):
            self.start = start
            self.end = end

    class Ann:
        def itertracks(self, yield_label=True):
            yield Turn(0.0, 0.5), None, "A"
            yield Turn(1.0, 2.0), None, "B"

    segs = segments_from_pipeline_output(Ann())
    assert len(segs) == 2
    assert segs[0].speaker == "A"
    assert segs[1].end == 2.0
