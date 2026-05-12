#!/usr/bin/env bash
# Generate logo candidates via Higgsfield (gpt_image_2 default — best for legible wordmarks).
#
# Usage:
#   higgsfield_logo.sh <slug> "<concept-brief>" "<style>" "<palette-hex-csv>" [count] [model]
#
# style: minimalist | illustrative | wordmark | monogram | lockup
# count: number of candidates (default 4)
# model: gpt_image_2 (default, legible wordmarks) | nano_banana_pro (cleaner iconography)
#
# Output: /Users/erikgamboa/Documents/CMO/projects/<slug>/assets/logo/logo-concept-{A,B,C,D}.png

set -euo pipefail

source "/Users/erikgamboa/Documents/CMO/.claude/skills/cmo-agency/scripts/lib/hf.sh"

if [ $# -lt 4 ]; then
    echo "uso: $0 <slug> <concept-brief> <style> <palette-hex-csv> [count] [model]" >&2
    exit 2
fi

SLUG="$1"
CONCEPT="$2"
STYLE="$3"
PALETTE="$4"
COUNT="${5:-4}"
MODEL="${6:-gpt_image_2}"

PROJECT_ROOT="/Users/erikgamboa/Documents/CMO/projects/$SLUG"
OUT_DIR="$PROJECT_ROOT/assets/logo"
mkdir -p "$OUT_DIR"

LETTERS=(A B C D E F G H)

for i in $(seq 0 $((COUNT - 1))); do
    LETTER="${LETTERS[$i]}"
    OUT_FILE="$OUT_DIR/logo-concept-${LETTER}.png"

    PROMPT="Brand logo design. Style: ${STYLE}. Brand concept: ${CONCEPT}. \
Use only colors from this palette: ${PALETTE}. \
Pure white background, centered, generous negative space, vector-style clean lines, \
high contrast, scalable, no extra text outside the logo itself, no mockups, no shadows, \
no realistic textures, suitable for print and digital use. \
Iteration ${LETTER} of ${COUNT} — explore distinct compositional approaches across iterations. \
Square 1:1 aspect ratio."

    echo "Generando logo concepto ${LETTER}/${COUNT} (${MODEL})..." >&2

    if ! hf_generate "$MODEL" "$OUT_FILE" \
        --prompt "$PROMPT" \
        --aspect_ratio 1:1; then
        echo "warn: falló logo concepto ${LETTER} — continuo con el siguiente" >&2
    fi
done
