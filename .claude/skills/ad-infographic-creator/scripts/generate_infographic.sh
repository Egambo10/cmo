#!/usr/bin/env bash
# Generate a standalone infographic via Higgsfield (gpt_image_2 — best at dense text).
#
# Usage:
#   generate_infographic.sh <slug> "<title>" "<layout-spec>" "<aspect_ratio>" "<primary-hex>" "<bg-hex>" "<headline-font>" "<body-font>"
#
# layout-spec: free-form description of the layout — sections, content per section.
#              The caller (the skill) is responsible for assembling this from the user's brief.
# aspect_ratio: 1:1 | 3:4 | 9:16 | 4:5
#
# Output: /Users/erikgamboa/Documents/CMO/projects/<slug>/assets/ads/<date>-infographic.png

set -euo pipefail

source "/Users/erikgamboa/Documents/CMO/.claude/skills/cmo-agency/scripts/lib/hf.sh"

if [ $# -lt 8 ]; then
    echo "uso: $0 <slug> <title> <layout-spec> <aspect_ratio> <primary-hex> <bg-hex> <headline-font> <body-font>" >&2
    exit 2
fi

SLUG="$1"
TITLE="$2"
LAYOUT="$3"
ASPECT="$4"
PRIMARY="$5"
BG="$6"
H_FONT="$7"
B_FONT="$8"

PROJECT_ROOT="/Users/erikgamboa/Documents/CMO/projects/$SLUG"
DATE=$(date +%Y%m%d-%H%M%S)
OUT_FILE="$PROJECT_ROOT/assets/ads/${DATE}-infographic.png"

PROMPT="Editorial infographic poster. Aspect ratio ${ASPECT}. Background color exactly ${BG}. \
Title at top: \"${TITLE}\" rendered in ${H_FONT} bold large, color exactly ${PRIMARY}. \
\
Layout: ${LAYOUT} \
\
All headers use ${H_FONT}, body text uses ${B_FONT}. Primary text color ${PRIMARY}. \
All text must be perfectly legible — numbers, labels, captions everything. \
Generous whitespace between sections. Editorial agency quality. No decorative clutter, no stock photography, no watermarks. \
Use only the two colors specified (${PRIMARY} and ${BG}), plus white if needed for contrast."

echo "Generando infografía con Higgsfield (gpt_image_2)..." >&2

hf_generate gpt_image_2 "$OUT_FILE" \
    --prompt "$PROMPT" \
    --aspect_ratio "$ASPECT"
