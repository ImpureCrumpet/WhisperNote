#!/usr/bin/env bash
# Normalize audio to 16 kHz mono WAV (same settings as whispernote.cli.preprocess_audio).
# Pipeline context: .skills/_skills/whispernote-internals/SKILL.md; agents: AGENTS.md.
set -euo pipefail
INPUT="${1:?usage: normalize_audio.sh INPUT OUTPUT}"
OUTPUT="${2:?usage: normalize_audio.sh INPUT OUTPUT}"
ffmpeg -y -i "$INPUT" -ar 16000 -ac 1 -c:a pcm_s16le "$OUTPUT"
