#!/usr/bin/env bash
# Verify the Higgsfield CLI is installed and authenticated.
# Exit 0 if ready, 1 with a copy-pasteable fix otherwise.

set -u

if ! command -v higgsfield >/dev/null 2>&1; then
    cat <<'EOF'
higgsfield CLI no está instalado.

Instálalo (una de las dos):
   npm install -g @higgsfield/cli
   curl -fsSL https://raw.githubusercontent.com/higgsfield-ai/cli/main/install.sh | sh

Y autentícate:
   higgsfield auth login

Cuando termines, vuelve y dime "listo".
EOF
    exit 1
fi

if higgsfield account status >/dev/null 2>&1; then
    echo "higgsfield: ok (autenticado)"
    exit 0
fi

cat <<'EOF'
higgsfield está instalado pero no se detecta una sesión activa.

Autentícate:
   higgsfield auth login

Cuando termines, vuelve y dime "listo".
EOF
exit 1
