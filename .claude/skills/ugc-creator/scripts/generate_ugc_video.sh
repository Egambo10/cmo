#!/usr/bin/env bash
# Generate a UGC-style video via Higgsfield.
#
# Two modes:
#   1. Generic UGC scene (no specific presenter): seedance_2_0 (default, SOTA realism)
#      or veo3_1 if you need character-led generation.
#   2. With a brand-specific presenter Soul: soul_cinematic + --soul-id <ref>.
#
# For UGC ADS with a Marketing Studio avatar + product, DO NOT use this script —
# delegate to the higgsfield-generate skill (Marketing Studio video workflow).
#
# Usage:
#   generate_ugc_video.sh <slug> "<scene-prompt>" <duration-s> [model] [soul_id]
#
# model: seedance_2_0 (default) | veo3_1 | soul_cinematic
# soul_id: required if model=soul_cinematic — the ugc-presenter Soul reference
#
# Output: /Users/erikgamboa/Documents/CMO/projects/<slug>/assets/ugc/<date>-ugc-video.mp4

set -euo pipefail

source "/Users/erikgamboa/Documents/CMO/.claude/skills/cmo-agency/scripts/lib/hf.sh"

if [ $# -lt 3 ]; then
    echo "uso: $0 <slug> <scene-prompt> <duration-s> [model] [soul_id]" >&2
    exit 2
fi

SLUG="$1"
SCENE="$2"
DUR="$3"
MODEL="${4:-seedance_2_0}"
SOUL_ID="${5:-}"

PROJECT_ROOT="/Users/erikgamboa/Documents/CMO/projects/$SLUG"
DATE=$(date +%Y%m%d-%H%M%S)
OUT_FILE="$PROJECT_ROOT/assets/ugc/${DATE}-ugc-video.mp4"

echo "Generando video UGC ${DUR}s con Higgsfield (${MODEL})..." >&2

ARGS=(--prompt "$SCENE" --aspect_ratio 9:16 --duration "$DUR")

if [ "$MODEL" = "soul_cinematic" ]; then
    if [ -z "$SOUL_ID" ]; then
        echo "error: soul_cinematic requiere --soul-id. Pasa el ugc-presenter Soul ref." >&2
        exit 2
    fi
    ARGS+=(--soul-id "$SOUL_ID")
fi

hf_generate "$MODEL" "$OUT_FILE" "${ARGS[@]}"
