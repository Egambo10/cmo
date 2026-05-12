#!/usr/bin/env bash
# Generate an Instagram carousel — multiple slides as separate PNGs.
#
# Each slide-spec is a complete prompt for one slide. The caller (the skill) is
# responsible for embedding brand palette/typography/voice into each spec.
#
# Usage:
#   generate_carousel.sh <slug> <out-dir-name> "<slide-spec-1>" "<slide-spec-2>" ...
#
# Output dir: /Users/erikgamboa/Documents/CMO/projects/<slug>/assets/social/<out-dir-name>/

set -euo pipefail

source "/Users/erikgamboa/Documents/CMO/.claude/skills/cmo-agency/scripts/lib/hf.sh"

if [ $# -lt 3 ]; then
    echo "uso: $0 <slug> <out-dir-name> <slide-spec-1> [slide-spec-2] ..." >&2
    exit 2
fi

SLUG="$1"
OUT_NAME="$2"
shift 2

PROJECT_ROOT="/Users/erikgamboa/Documents/CMO/projects/$SLUG"
OUT_DIR="$PROJECT_ROOT/assets/social/$OUT_NAME"
mkdir -p "$OUT_DIR"

i=1
for SLIDE_SPEC in "$@"; do
    PADDED=$(printf "%02d" "$i")
    OUT_FILE="$OUT_DIR/slide-${PADDED}.png"

    echo "Generando slide ${i} (gpt_image_2)..." >&2

    if ! hf_generate gpt_image_2 "$OUT_FILE" \
        --prompt "$SLIDE_SPEC" \
        --aspect_ratio 1:1; then
        echo "warn: no se generó slide ${i}" >&2
    fi

    i=$((i + 1))
done
