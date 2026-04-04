# Skills Index

Kit version: see `.skills/_meta.yml` (optional metadata only).

Load a skill only when the task clearly requires it.
Read the full `SKILL.md` only at that point — never preemptively.

| name | description | triggers |
|------|-------------|----------|
| skill-template | Canonical skill format and authoring reference | new skill, create skill, skill format |
| skill-author | How to write a skill from scratch | write skill, author skill |
| whispernote-hf-setup | Hugging Face gated models, HF_TOKEN, cache, telemetry | HF_TOKEN, gated model, hugging face |
| whispernote-internals | CLI pipeline: ffmpeg, diarize, transcribe, merge, export | pipeline, architecture, preprocess |
| whispernote-export-formats | srt, txt, json, md exports and time formats | export, srt, TranscriptLine |
| whispernote-testing | pytest layout, testpaths, adding tests | pytest, run tests |
| whispernote-models | defaults, whispernote.json, -ma/-md precedence | asr model, whispernote.json, -ma |

Add a row here whenever a new skill is added to `.skills/_skills/`.
