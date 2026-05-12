#!/usr/bin/env bash
# Render a typography sample image via Higgsfield (gpt_image_2 — best at text).
#
# Usage:
#   render_typography.sh <slug> <pair-name> "<headline-font>" "<body-font>" "<primary-hex>" "<bg-hex>"
#
# Output: /Users/erikgamboa/Documents/CMO/projects/<slug>/assets/typography/type-<pair-name>-v1.png

set -euo pipefail

source "/Users/erikgamboa/Documents/CMO/.claude/skills/cmo-agency/scripts/lib/hf.sh"

if [ $# -lt 6 ]; then
    echo "uso: $0 <slug> <pair-name> <headline-font> <body-font> <primary-hex> <bg-hex>" >&2
    exit 2
fi

SLUG="$1"
PAIR="$2"
H_FONT="$3"
B_FONT="$4"
PRIMARY="$5"
BG="$6"

PROJECT_ROOT="/Users/erikgamboa/Documents/CMO/projects/$SLUG"
OUT_FILE="$PROJECT_ROOT/assets/typography/type-${PAIR}-v1.png"

PROMPT="Typography specimen sheet for a brand book. \
Background color exactly ${BG}. Primary text color exactly ${PRIMARY}. \
Show, top to bottom, each on its own line, left-aligned, with generous spacing: \
'H1 — ${H_FONT} 56px / Bold' rendered AS ACTUAL H1 IN ${H_FONT} bold at 56px. \
'H2 — ${H_FONT} 40px / Semibold' rendered AS ACTUAL H2 in ${H_FONT} semibold 40px. \
'H3 — ${H_FONT} 28px / Medium' rendered AS ACTUAL H3 in ${H_FONT} medium 28px. \
'Body — ${B_FONT} 16px / Regular — The quick brown fox jumps over the lazy dog' \
rendered in ${B_FONT} regular 16px. \
'Caption — ${B_FONT} 12px / Regular' rendered in ${B_FONT} regular 12px. \
A button labeled 'PRIMARY BUTTON' in ${B_FONT} semibold 14px, uppercase, with the primary color as background and white text. \
Every text label and font name must be perfectly legible. Editorial layout, minimal, agency quality. \
Aspect ratio 4:5."

echo "Generando muestra tipográfica '${PAIR}' con Higgsfield (gpt_image_2)..." >&2

hf_generate gpt_image_2 "$OUT_FILE" \
    --prompt "$PROMPT" \
    --aspect_ratio 4:5
