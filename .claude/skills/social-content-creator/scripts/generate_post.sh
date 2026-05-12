#!/usr/bin/env bash
# Generate a single static social media post via Higgsfield.
#
# Usage:
#   generate_post.sh <slug> "<prompt>" <model> [aspect_ratio] [soul_id]
#
# model: gpt_image_2 (text-heavy, recommended for posts with copy)
#        nano_banana_pro (visual-heavy, character/lifestyle)
#        text2image_soul_v2 (use brand-style Soul ID for max consistency)
# aspect_ratio: 1:1 (default) | 4:5 | 9:16
# soul_id: required when model=text2image_soul_v2 (brand-style Soul reference)
#
# Output: /Users/erikgamboa/Documents/CMO/projects/<slug>/assets/social/<date>-post.png

set -euo pipefail

source "/Users/erikgamboa/Documents/CMO/.claude/skills/cmo-agency/scripts/lib/hf.sh"

if [ $# -lt 3 ]; then
    echo "uso: $0 <slug> <prompt> <model> [aspect_ratio] [soul_id]" >&2
    exit 2
fi

SLUG="$1"
PROMPT="$2"
MODEL="$3"
ASPECT="${4:-1:1}"
SOUL_ID="${5:-}"

PROJECT_ROOT="/Users/erikgamboa/Documents/CMO/projects/$SLUG"
DATE=$(date +%Y%m%d-%H%M%S)
OUT_FILE="$PROJECT_ROOT/assets/social/${DATE}-post.png"

echo "Generando post estático (${MODEL}, ${ASPECT})..." >&2

ARGS=(--prompt "$PROMPT" --aspect_ratio "$ASPECT")

if [ "$MODEL" = "text2image_soul_v2" ]; then
    if [ -z "$SOUL_ID" ]; then
        echo "error: text2image_soul_v2 requiere un soul_id. Crea uno con higgsfield soul-id create primero." >&2
        exit 2
    fi
    ARGS+=(--soul-id "$SOUL_ID" --quality 2k)
fi

hf_generate "$MODEL" "$OUT_FILE" "${ARGS[@]}"
