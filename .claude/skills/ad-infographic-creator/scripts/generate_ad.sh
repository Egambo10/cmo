#!/usr/bin/env bash
# Generate a display ad with copy via Higgsfield (gpt_image_2 — best for legible copy at multiple sizes).
#
# Usage:
#   generate_ad.sh <slug> "<headline>" "<sub>" "<cta>" "<visual-concept>" \
#                  "<primary-hex>" "<bg-hex>" "<accent-hex>" \
#                  "<headline-font>" "<body-font>" "<aspect_ratio>" [model]
#
# aspect_ratio: 1:1 | 9:16 | 16:9 | 1.91:1 (Meta feed)
# model: gpt_image_2 (default, text-dense) | nano_banana_pro (less text)
#
# Output: /Users/erikgamboa/Documents/CMO/projects/<slug>/assets/ads/<date>-ad-<aspect>.png

set -euo pipefail

source "/Users/erikgamboa/Documents/CMO/.claude/skills/cmo-agency/scripts/lib/hf.sh"

if [ $# -lt 11 ]; then
    echo "uso: $0 <slug> <headline> <sub> <cta> <visual-concept> <primary-hex> <bg-hex> <accent-hex> <headline-font> <body-font> <aspect_ratio> [model]" >&2
    exit 2
fi

SLUG="$1"
HEAD="$2"
SUB="$3"
CTA="$4"
CONCEPT="$5"
PRIMARY="$6"
BG="$7"
ACCENT="$8"
H_FONT="$9"
B_FONT="${10}"
ASPECT="${11}"
MODEL="${12:-gpt_image_2}"

PROJECT_ROOT="/Users/erikgamboa/Documents/CMO/projects/$SLUG"
DATE=$(date +%Y%m%d-%H%M%S)
ASPECT_SAFE=$(echo "$ASPECT" | tr ':' 'x')
OUT_FILE="$PROJECT_ROOT/assets/ads/${DATE}-ad-${ASPECT_SAFE}.png"

PROMPT="Display advertisement, aspect ratio ${ASPECT}. Background color exactly ${BG}. \
Visual concept: ${CONCEPT}. \
Headline in ${H_FONT} bold, large size, color exactly ${PRIMARY}, text: \"${HEAD}\". \
Sub-headline in ${B_FONT} regular, medium size, color ${PRIMARY} at 80% opacity, text: \"${SUB}\". \
Call-to-action button at the bottom or visible area: ${B_FONT} semibold, white text on solid ${ACCENT} background, rounded corners, text: \"${CTA}\". \
Every text element must be perfectly legible. Editorial, agency quality, no decorative clutter. \
Composition follows the visual concept above. No on-screen text other than the headline, sub, and CTA. No watermarks, no website URLs."

echo "Generando ad ${ASPECT} con Higgsfield (${MODEL})..." >&2

hf_generate "$MODEL" "$OUT_FILE" \
    --prompt "$PROMPT" \
    --aspect_ratio "$ASPECT"
