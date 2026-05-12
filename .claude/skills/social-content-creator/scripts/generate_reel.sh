#!/usr/bin/env bash
# Generate a Reel/TikTok video via Higgsfield (seedance_2_0 default, kling3_0/veo3_1 optional).
#
# Usage:
#   generate_reel.sh <slug> "<scene-prompt>" <duration-s> [model] [aspect_ratio] [start_image]
#
# model: seedance_2_0 (default, SOTA multi-shot) | kling3_0 (cinematic, single-plane) | veo3_1 (UGC realism)
# aspect_ratio: 9:16 (default for vertical) | 16:9 | 1:1
# start_image: optional local path or upload-id for image-to-video
#
# Output: /Users/erikgamboa/Documents/CMO/projects/<slug>/assets/social/<date>-reel.mp4

set -euo pipefail

source "/Users/erikgamboa/Documents/CMO/.claude/skills/cmo-agency/scripts/lib/hf.sh"

if [ $# -lt 3 ]; then
    echo "uso: $0 <slug> <scene-prompt> <duration-s> [model] [aspect_ratio] [start_image]" >&2
    exit 2
fi

SLUG="$1"
SCENE="$2"
DUR="$3"
MODEL="${4:-seedance_2_0}"
ASPECT="${5:-9:16}"
START_IMG="${6:-}"

PROJECT_ROOT="/Users/erikgamboa/Documents/CMO/projects/$SLUG"
DATE=$(date +%Y%m%d-%H%M%S)
OUT_FILE="$PROJECT_ROOT/assets/social/${DATE}-reel.mp4"

echo "Generando reel ${DUR}s con Higgsfield (${MODEL}, ${ASPECT})..." >&2

ARGS=(--prompt "$SCENE" --aspect_ratio "$ASPECT" --duration "$DUR")
if [ -n "$START_IMG" ]; then
    ARGS+=(--start-image "$START_IMG")
fi

hf_generate "$MODEL" "$OUT_FILE" "${ARGS[@]}"
