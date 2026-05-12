#!/usr/bin/env bash
# CMO Agency preflight check — verifies tools + skills + workspace.
# Exits 0 if everything's ready, 1 with copy-pasteable fixes otherwise.

set -u
PROJECTS_ROOT="/Users/erikgamboa/Documents/CMO/projects"
PROBLEMS=()

# ── Higgsfield CLI ────────────────────────────────────────────────────────────
if ! command -v higgsfield >/dev/null 2>&1; then
    PROBLEMS+=("Higgsfield CLI no está instalado.
   Instálalo:   npm install -g @higgsfield/cli
   o:           curl -fsSL https://raw.githubusercontent.com/higgsfield-ai/cli/main/install.sh | sh
   Autentícate: higgsfield auth login")
else
    if ! higgsfield account status >/dev/null 2>&1; then
        PROBLEMS+=("Higgsfield está instalado pero no autenticado.
   Ejecuta: higgsfield auth login")
    fi
fi

# ── jq + curl (needed by the hf.sh helper) ───────────────────────────────────
if ! command -v jq >/dev/null 2>&1; then
    PROBLEMS+=("'jq' no está instalado (lo necesita el wrapper de Higgsfield).
   Instálalo: brew install jq")
fi
if ! command -v curl >/dev/null 2>&1; then
    PROBLEMS+=("'curl' no está instalado (lo necesita el wrapper de Higgsfield).
   Instálalo: brew install curl")
fi

# ── Higgsfield bundled skills ─────────────────────────────────────────────────
# Best-effort detection — different versions store these in different places.
HIGGSFIELD_SKILLS_DIR=""
for candidate in "$HOME/.higgsfield/skills" "$HOME/.npm/_npx" "$HOME/.config/higgsfield/skills"; do
    if [ -d "$candidate" ]; then
        HIGGSFIELD_SKILLS_DIR="$candidate"
        break
    fi
done
if [ -z "$HIGGSFIELD_SKILLS_DIR" ]; then
    PROBLEMS+=("No se detectaron las skills empaquetadas de Higgsfield (product-photoshoot, soul-id, marketing-studio, marketplace-cards).
   Instálalas: npx skills add higgsfield-ai/skills")
fi

# ── Anthropic skills (canvas-design, pdf, skill-creator) ──────────────────────
# These are managed by the Claude harness; the orchestrator can't programmatically
# list them, so we trust the user's environment. If a brand-book run fails because
# canvas-design or pdf isn't available, the brand-book-publisher skill prints a
# clear error pointing at the missing skill.

# ── Workspace ─────────────────────────────────────────────────────────────────
if [ ! -d "$PROJECTS_ROOT" ]; then
    mkdir -p "$PROJECTS_ROOT" 2>/dev/null || PROBLEMS+=("No pude crear $PROJECTS_ROOT. Créalo a mano:
   mkdir -p $PROJECTS_ROOT")
fi

# ── state.py works ────────────────────────────────────────────────────────────
if ! python3 "$(dirname "$0")/state.py" list >/dev/null 2>&1; then
    PROBLEMS+=("state.py no se ejecuta correctamente. Verifica que tengas python3 en el PATH.")
fi

# ── Report ────────────────────────────────────────────────────────────────────
if [ ${#PROBLEMS[@]} -eq 0 ]; then
    echo "preflight: ok"
    exit 0
fi

echo "preflight: faltan dependencias"
echo ""
for i in "${!PROBLEMS[@]}"; do
    echo "($((i+1))) ${PROBLEMS[$i]}"
    echo ""
done
exit 1
