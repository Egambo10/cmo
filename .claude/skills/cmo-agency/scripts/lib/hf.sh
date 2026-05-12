#!/usr/bin/env bash
# Shared Higgsfield CLI helpers for the CMO agency skill suite.
#
# Source this file (do not execute):
#   source "/Users/erikgamboa/Documents/CMO/.claude/skills/cmo-agency/scripts/lib/hf.sh"
#
# The real `higgsfield generate create` command prints JSON (with --json) and
# writes the produced media URLs into the job object. It does NOT take an
# --output flag. This helper wraps the create → parse-URL → download flow so the
# 8 generation scripts in this suite stay short and uniform.

set -uo pipefail

# Resolve realpath of the file that sourced us, for diagnostics.
HF_LIB_SELF="${BASH_SOURCE[0]}"

hf_require() {
    # hf_require <cmd> [<cmd>...]  — exit 127 with a copy-pasteable hint
    for cmd in "$@"; do
        if ! command -v "$cmd" >/dev/null 2>&1; then
            echo "error: '$cmd' no está disponible en PATH." >&2
            case "$cmd" in
                higgsfield) echo "  Instálalo: npm install -g @higgsfield/cli" >&2;;
                jq)         echo "  Instálalo: brew install jq" >&2;;
                curl)       echo "  Instálalo: brew install curl" >&2;;
            esac
            exit 127
        fi
    done
}

hf_check_auth() {
    # Returns 0 if a session is active. Prints the fix and returns 1 otherwise.
    if higgsfield account status >/dev/null 2>&1; then
        return 0
    fi
    cat >&2 <<'EOF'
higgsfield no está autenticado.

Autentícate:
   higgsfield auth login

Cuando termines, vuelve a correr este comando.
EOF
    return 1
}

# hf_generate <model_id> <out_file> <args...>
# Submits `higgsfield generate create <model_id> --json --wait <args...>`,
# parses the produced media URL from the job result, downloads it to <out_file>.
# All extra args are passed through verbatim — pass --prompt, --aspect_ratio,
# --image, --duration, --soul-id, --quality, etc. as needed.
hf_generate() {
    hf_require higgsfield jq curl
    if [ $# -lt 2 ]; then
        echo "uso: hf_generate <model_id> <out_file> <args...>" >&2
        return 2
    fi
    local model="$1"; shift
    local out="$1"; shift
    local outdir
    outdir="$(dirname "$out")"
    mkdir -p "$outdir"

    # Run create + wait, capturing the final job JSON.
    local job_json
    if ! job_json=$(higgsfield generate create "$model" --json --wait "$@" 2>/tmp/hf_stderr.$$); then
        local rc=$?
        echo "error: 'higgsfield generate create $model' falló (exit $rc):" >&2
        cat /tmp/hf_stderr.$$ >&2
        rm -f /tmp/hf_stderr.$$
        return $rc
    fi
    rm -f /tmp/hf_stderr.$$

    # Extract the first asset URL. The CLI returns an array of jobs (one per
    # variant). Real shapes seen in the wild:
    #   - top-level: result_url (single URL, most common for imagegen)
    #   - top-level: result_urls (array, for multi-variant jobs)
    #   - nested: results[].url / assets[].url / images[].url (older / legacy)
    local url
    url=$(printf '%s' "$job_json" | jq -r '
        if type == "array" then .[0] else . end
        | (
            .result_url
            // (.result_urls // [] | if type == "array" then .[0] else . end)
            // .url
            // (
                (.results // .result // .assets // .images // [])
                | if type == "array" then .[0] else . end
                | (.url // .signed_url // .download_url // .result_url // empty)
              )
          )
        // empty
    ' 2>/dev/null)

    if [ -z "$url" ] || [ "$url" = "null" ]; then
        echo "error: no encontré URL del asset en el JSON del job:" >&2
        printf '%s\n' "$job_json" | head -40 >&2
        return 3
    fi

    if ! curl --fail --silent --show-error --location --output "$out" "$url"; then
        echo "error: no pude descargar $url -> $out" >&2
        return 4
    fi

    echo "$out"
}

# hf_upload <local_file>  → prints the upload_id on stdout
hf_upload() {
    hf_require higgsfield jq
    local f="$1"
    if [ ! -f "$f" ]; then
        echo "error: archivo no existe: $f" >&2
        return 2
    fi
    local resp
    resp=$(higgsfield upload create "$f" --json 2>&1) || {
        echo "error: 'higgsfield upload create $f' falló:" >&2
        echo "$resp" >&2
        return 3
    }
    printf '%s' "$resp" | jq -r '.id // .upload_id // empty'
}
