#!/usr/bin/env bash
# Generate the one-page brand book infographic via Higgsfield (gpt_image_2).
#
# Reads the brand's locked palette + logo + type from
#   /Users/erikgamboa/Documents/CMO/projects/<slug>/02-identidad-visual.md
# and builds a structured prompt for a 1-page brand book summary.
#
# Usage:
#   build_infographic.sh <slug> "<brand-name>" "<primary-hex>" "<secondary-hex>" "<accent-hex>" \
#                        "<bg-hex>" "<headline-font>" "<body-font>" "<personality-keywords-csv>"
#
# Output: /Users/erikgamboa/Documents/CMO/projects/<slug>/03-brand-book-infographic.png

set -euo pipefail

source "/Users/erikgamboa/Documents/CMO/.claude/skills/cmo-agency/scripts/lib/hf.sh"

if [ $# -lt 9 ]; then
    echo "uso: $0 <slug> <brand-name> <primary-hex> <secondary-hex> <accent-hex> <bg-hex> <headline-font> <body-font> <personality-keywords-csv>" >&2
    exit 2
fi

SLUG="$1"
BRAND="$2"
PRIMARY="$3"
SECONDARY="$4"
ACCENT="$5"
BG="$6"
H_FONT="$7"
B_FONT="$8"
PERSONALITY="$9"

PROJECT_ROOT="/Users/erikgamboa/Documents/CMO/projects/$SLUG"
OUT_FILE="$PROJECT_ROOT/03-brand-book-infographic.png"

PROMPT="One-page editorial brand book infographic poster for the brand '${BRAND}'. \
Portrait A3 ratio. Background color exactly ${BG}. \
\
TOP SECTION (large): The brand name '${BRAND}' rendered very large in ${H_FONT} bold, color ${PRIMARY}. \
Below the name, a thin horizontal rule in ${ACCENT}. Below that, the words 'BRAND BOOK' in small ${B_FONT} uppercase letterspaced, color ${SECONDARY}. \
\
MIDDLE-LEFT: A row of color swatches showing exactly these HEX values printed underneath each swatch in monospace 12px: ${PRIMARY}, ${SECONDARY}, ${ACCENT}, ${BG}. Label this section 'PALETA' in ${H_FONT} semibold 18px. \
\
MIDDLE-RIGHT: Typography specimen showing 'Aa Bb Cc 123' in ${H_FONT} bold 48px color ${PRIMARY}, and below it 'The quick brown fox jumps over the lazy dog.' in ${B_FONT} regular 14px color ${SECONDARY}. Label this section 'TIPOGRAFÍA' with the font names: '${H_FONT} / ${B_FONT}'. \
\
BOTTOM-LEFT: A vertical list of personality keywords (each on its own line, ${H_FONT} medium 22px, color ${PRIMARY}): ${PERSONALITY}. Label this section 'PERSONALIDAD'. \
\
BOTTOM-RIGHT: A short manifesto-style paragraph of 3-4 lines in ${B_FONT} regular 14px, color ${SECONDARY}, summarizing the brand essence. Label this section 'ESENCIA'. \
\
All text must be perfectly legible. Generous whitespace. Editorial layout. Agency quality. No stock photography, no decorative illustrations, no extra logos beyond the brand wordmark at top. \
Aspect ratio 3:4 portrait."

echo "Generando infográfico para '${BRAND}' con Higgsfield (gpt_image_2)..." >&2

hf_generate gpt_image_2 "$OUT_FILE" \
    --prompt "$PROMPT" \
    --aspect_ratio 3:4
