#!/usr/bin/env bash
# Render a color palette swatch image via Higgsfield (gpt_image_2 — best for legible HEX labels).
#
# Usage:
#   render_palette.sh <slug> <palette-name> "<hex1,hex2,hex3,hex4,hex5,hex6>" "<label1,label2,label3,label4,label5,label6>"
#
# Output: /Users/erikgamboa/Documents/CMO/projects/<slug>/assets/colors/palette-<palette-name>-v1.png

set -euo pipefail

source "/Users/erikgamboa/Documents/CMO/.claude/skills/cmo-agency/scripts/lib/hf.sh"

if [ $# -lt 4 ]; then
    echo "uso: $0 <slug> <palette-name> <hex-csv> <label-csv>" >&2
    exit 2
fi

SLUG="$1"
PALETTE_NAME="$2"
HEX_CSV="$3"
LABEL_CSV="$4"

PROJECT_ROOT="/Users/erikgamboa/Documents/CMO/projects/$SLUG"
OUT_FILE="$PROJECT_ROOT/assets/colors/palette-${PALETTE_NAME}-v1.png"

PROMPT="Editorial color palette swatch sheet for a brand book. White background. \
Six rectangular swatches arranged in a clean 2x3 grid, generous spacing. \
Colors in order: ${HEX_CSV}. \
Under each swatch print, in a small clean sans-serif: the HEX code in monospace AND the label '${LABEL_CSV}' \
(the labels map 1:1 with the colors in order). \
Minimal, agency quality, no decorative elements, no extra text, no logos. \
Square 1:1 aspect ratio."

echo "Generando paleta '${PALETTE_NAME}' con Higgsfield (gpt_image_2)..." >&2

hf_generate gpt_image_2 "$OUT_FILE" \
    --prompt "$PROMPT" \
    --aspect_ratio 1:1
