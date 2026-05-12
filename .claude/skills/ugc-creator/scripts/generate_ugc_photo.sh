#!/usr/bin/env bash
# Generate an ecommerce product photo via Higgsfield product-photoshoot.
#
# Uses the dedicated `higgsfield product-photoshoot create` subcommand, which
# runs a backend prompt enhancer specialized for ecommerce/brand product imagery.
#
# This script is a thin wrapper. For richer briefs (multi-image references,
# brand-context tuning, etc.) the ugc-creator skill should delegate to the
# `higgsfield-product-photoshoot` bundled skill via subagent — it has the full
# mode catalog and reference-image handling.
#
# Usage:
#   generate_ugc_photo.sh <slug> "<intent-prompt>" <mode> [aspect_ratio] [reference_image] [count]
#
# mode: product_shot | lifestyle_scene | closeup_product_with_person |
#       moodboard_pin | hero_banner | social_carousel | ad_creative_pack |
#       virtual_model_tryout | conceptual_product | restyle
# aspect_ratio: optional — overrides the mode's default (e.g. 1:1, 4:5, 3:4)
# reference_image: optional local path OR upload-id of the product image
# count: number of variants (1-10, default 1)
#
# Output: /Users/erikgamboa/Documents/CMO/projects/<slug>/assets/ugc/<date>-<mode>-N.png

set -euo pipefail

source "/Users/erikgamboa/Documents/CMO/.claude/skills/cmo-agency/scripts/lib/hf.sh"

if [ $# -lt 3 ]; then
    echo "uso: $0 <slug> <intent-prompt> <mode> [aspect_ratio] [reference_image] [count]" >&2
    echo "modes: product_shot | lifestyle_scene | closeup_product_with_person | moodboard_pin | hero_banner | social_carousel | ad_creative_pack | virtual_model_tryout | conceptual_product | restyle" >&2
    exit 2
fi

hf_require higgsfield jq curl

SLUG="$1"
INTENT="$2"
MODE="$3"
ASPECT="${4:-}"
REF_IMG="${5:-}"
COUNT="${6:-1}"

PROJECT_ROOT="/Users/erikgamboa/Documents/CMO/projects/$SLUG"
OUT_DIR="$PROJECT_ROOT/assets/ugc"
mkdir -p "$OUT_DIR"
DATE=$(date +%Y%m%d-%H%M%S)

ARGS=(--mode "$MODE" --prompt "$INTENT" --count "$COUNT")
if [ -n "$ASPECT" ]; then
    ARGS+=(--aspect_ratio "$ASPECT")
fi
if [ -n "$REF_IMG" ]; then
    ARGS+=(--image "$REF_IMG")
fi

echo "Generando foto UGC product-photoshoot (mode=${MODE}, count=${COUNT})..." >&2

# product-photoshoot returns JSON with a result array.
RESP=$(higgsfield product-photoshoot create --json "${ARGS[@]}" 2>&1) || {
    echo "error: higgsfield product-photoshoot create falló:" >&2
    echo "$RESP" >&2
    exit 3
}

# Extract URLs. Real shapes from product-photoshoot:
#   - top-level array of jobs, each with result_url (single)
#   - top-level array of jobs, each with result_urls (multi-variant)
#   - legacy nested: results[].url / assets[].url
URLS=$(printf '%s' "$RESP" | jq -r '
    (if type == "array" then . else [.] end)
    | .[]
    | (
        (.result_urls // []) | if type == "array" then .[] else . end
      ),
      .result_url,
      (
        (.results // .result // .assets // .images // [])
        | if type == "array" then .[] else . end
        | (.url // .signed_url // .download_url // .result_url // empty)
      )
    | select(. != null and . != "")
' 2>/dev/null)

if [ -z "$URLS" ]; then
    echo "error: no encontré URLs de assets en el JSON:" >&2
    printf '%s\n' "$RESP" | head -60 >&2
    exit 4
fi

i=1
while IFS= read -r URL; do
    [ -z "$URL" ] && continue
    OUT_FILE="$OUT_DIR/${DATE}-${MODE}-${i}.png"
    if curl --fail --silent --show-error --location --output "$OUT_FILE" "$URL"; then
        echo "$OUT_FILE"
    else
        echo "warn: no pude descargar variante ${i} desde $URL" >&2
    fi
    i=$((i + 1))
done <<< "$URLS"
