# CMO Agency — Setup & Usage Guide

Una agencia de marketing virtual que vive como un set de skills en tu máquina. Te entrevista para construir tu marca, genera identidad visual (paleta, tipografía, logo), publica un brand book, y produce reels, posts, ads, UGC e infografías — todo on-brand por construcción.

Diseñada para correr en **Claude Cowork** o **Claude Code** (CLI). Usa **Higgsfield.ai** para generar imágenes y video.

---

## Qué vas a obtener

```
projects/<tu-marca>/
├── 01-plan-estrategico.md      ← Entregable 1: estrategia + voz
├── 02-identidad-visual.md      ← Entregable 2 parte A: paleta + tipo + logo
├── 03-brand-book.pdf           ← Entregable 2 parte B: manual editorial
├── 03-brand-book-infographic.png   ← Resumen visual de 1 página
├── assets/
│   ├── colors/    ← swatches PNG
│   ├── typography/ ← muestras tipográficas
│   ├── logo/      ← variantes + logo final
│   ├── social/    ← reels, carruseles, posts
│   ├── ugc/       ← videos + fotos de producto
│   └── ads/       ← anuncios + infografías
└── ingest/        ← pitch decks / briefs que tú dropees
```

7 skills coordinadas por un router (`/cmo-agency`):

| Skill | Rol |
|---|---|
| `cmo-agency` | El partner virtual. Siempre arranca aquí. |
| `brand-strategy-interview` | Entrevista para misión, propuesta de valor, buyer persona, tono de voz. |
| `brand-identity-visual` | Genera paleta → tipografía → logo, en orden, cada paso aprobado. |
| `brand-book-publisher` | Publica el brand book (PDF editorial + infográfico). |
| `social-content-creator` | Reels, TikToks, carruseles IG, posts estáticos. |
| `ugc-creator` | UGC video (talking-head) y fotos de producto ecommerce. |
| `ad-infographic-creator` | Ads con copy + infografías independientes. |

Más 4 skills bundleadas de Higgsfield (product-photoshoot, soul-id, marketplace-cards, generate/Marketing Studio).

---

## Requisitos previos

- **macOS** (probado) o Linux. Windows con WSL2 también funciona.
- **Node.js 20+** y **npm** (para instalar el CLI de Higgsfield).
- **Python 3.10+** (para el ledger de estado).
- **jq** y **curl** (los usa el wrapper de Higgsfield).
- Una cuenta de **Higgsfield.ai** con créditos (el plan Plus alcanza para arrancar varias marcas).
- **Claude Cowork** o **Claude Code** instalado.

Verificá todo con un comando:

```bash
node --version && npm --version && python3 --version && jq --version && curl --version | head -1
```

Si te falta algo:

```bash
# Node.js (vía nvm, recomendado)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
nvm install --lts

# jq y curl (macOS)
brew install jq curl

# Python — viene con macOS, o brew install python@3.12
```

---

## Paso 1 — Bajar el repo

```bash
# Elegí dónde lo querés (típicamente ~/Documents o ~/dev)
cd ~/Documents

# Cloná el repo (reemplazá <usuario>/<repo> con la URL real)
git clone https://github.com/Egambo10/cmo.git
cd cmo
```

> **Importante:** muchos paths dentro de las skills son absolutos a `/Users/erikgamboa/Documents/CMO/`. Si lo clonás en otra ruta, hay que ajustar — abrí un issue o seguí la sección "Cambiar la ruta base" al final.

---

## Paso 2 — Instalar y autenticar Higgsfield

```bash
# Instalar el CLI
npm install -g @higgsfield/cli

# Verificar
higgsfield --version

# Autenticar (abre el browser para login)
higgsfield auth login
```

### Bug común: "Failed to create credentials dir"

El CLI guarda credenciales en `~/.config/higgsfield/`. Si esa carpeta es propiedad de `root` (pasa en macOS por instalaciones viejas de Homebrew), el login falla en silencio. Verificá:

```bash
ls -ld ~/.config
```

Si ves `root staff` en lugar de tu usuario:

```bash
sudo chown -R $(whoami):staff ~/.config
```

Después volvé a correr `higgsfield auth login`.

### Confirmar que estás autenticado

```bash
higgsfield account status
```

Debe mostrar tu email, plan y créditos disponibles. Si dice `Error: Not authenticated`, repetí el paso anterior.

---

## Paso 3 — Instalar las skills bundleadas de Higgsfield

Estas son skills oficiales de Higgsfield que el router del CMO invoca cuando hace falta (product photos para ecommerce, Soul training, marketplace cards, Marketing Studio).

```bash
npx skills add higgsfield-ai/skills
```

Esto crea `~/.agents/skills/higgsfield-*` y deja symlinks dentro de `.claude/skills/` del repo. Verificá:

```bash
ls .claude/skills/ | grep higgsfield
```

Deberías ver 4 entradas: `higgsfield-generate`, `higgsfield-marketplace-cards`, `higgsfield-product-photoshoot`, `higgsfield-soul-id`.

---

## Paso 4 — Preflight check

Desde la raíz del repo:

```bash
bash .claude/skills/cmo-agency/scripts/preflight.sh
```

Debe imprimir `preflight: ok`. Si imprime "faltan dependencias", segui las instrucciones de fix que muestra (típicamente reinstalar `jq` o reautenticar Higgsfield).

---

## Paso 5 — Abrir en Claude Cowork / Claude Code

### Claude Cowork

1. Abrí Cowork.
2. **Open Project** → seleccioná la carpeta `CMO/`.
3. En el chat, escribí: `/cmo-agency`
4. El router corre preflight, detecta que no hay marcas, y te pide un slug para empezar.

### Claude Code (terminal)

```bash
cd ~/Documents/CMO
claude
```

Una vez dentro de Claude Code:

```
/cmo-agency
```

> El router carga automáticamente el contexto del proyecto desde `CLAUDE.md` (las reglas operativas) y `AGENTS.md` (symlink al mismo archivo, para otros runners).

---

## Cómo usarlo — flujo completo de una marca nueva

### 1. Arranque

Decile: *"Quiero empezar una marca de [lo que sea]"*. El router:

1. Corre preflight.
2. Te pide un slug en kebab-case (3-20 chars ASCII, por ejemplo `cafe-norte`).
3. Crea `projects/<slug>/.state.json` con todos los gates en `false`.
4. Te rutea a la entrevista.

### 2. Entrevista de estrategia

Una pregunta por mensaje, en español neutro LatAm con tuteo. El brand strategist virtual:

- Adapta el flujo según tres tracks:
  - **Nuevo** (pre-lanzamiento, no tenés nada)
  - **Existente sin docs** (negocio operando pero sin brand book)
  - **Existente con docs** (drop el pitch deck en `projects/<slug>/ingest/` y te lo lee)
- Te propone respuestas concretas — no solo pregunta, redacta.
- No acepta "no sé" como respuesta final: te da 2-3 opciones con pros/cons.
- Resuelve el nombre temprano (con metodologías de naming si no lo tenés).
- Valida cada bloque antes de avanzar.

Salida: `01-plan-estrategico.md` con misión, visión, valores, propuesta de valor, posicionamiento, público objetivo, buyer persona, personalidad, tono de voz.

### 3. Identidad visual

Secuencial: **paleta → tipografía → logo**. Cada paso bloqueado hasta que aprobás.

- **Paleta:** 2-3 candidatas, cada una con 5-6 colores + rationale + usos web/print. Generadas via Higgsfield.
- **Tipografía:** 2-3 pairings (headline + body) con sistema de tamaños px/pt. Generadas via Higgsfield.
- **Logo:** brief de concepto + 3-4 candidatos. Después de lockear, te propone entrenar un **Soul de estilo de marca** (referencia visual reusable para mantener consistencia en posts, ads y banners futuros).

Salida: `02-identidad-visual.md` + assets PNG + opcionalmente `soul_brand_style_id` registrado.

### 4. Brand book

Cuando los gates visuales están verdes:

```
/cmo-agency
```

(O simplemente decile *"armemos el brand book"*).

Genera:
- **`03-brand-book.pdf`** — manual editorial multi-página vía `canvas-design`.
- **`03-brand-book-infographic.png`** — resumen visual de 1 página vía Higgsfield.

### 5. Producción de creativos

Con todos los gates verdes, el router te muestra el menú:

```
Tu marca está lista. ¿Qué creamos hoy?

(1) Reel
(2) Carrusel de Instagram
(3) Post estático
(4) Video UGC
(5) Foto UGC para ecommerce
(6) Anuncio con copy
(7) Infografía
```

Cada opción tiene su propia skill especializada que lee tu paleta + tipografía + voz y arma prompts on-brand automáticamente.

---

## Comandos rápidos de referencia

```bash
# Estado del proyecto
STATE=.claude/skills/cmo-agency/scripts/state.py
python3 $STATE list                # todas las marcas + gate pendiente
python3 $STATE get <slug>          # estado completo
python3 $STATE next <slug>         # siguiente gate pendiente
python3 $STATE done <slug> <gate>  # marcar gate como hecho (sólo después de aprobación)
python3 $STATE reopen <slug> <gate> # reabrir gate (ej. cambiar paleta)

# Preflight
bash .claude/skills/cmo-agency/scripts/preflight.sh

# Higgsfield
higgsfield account status          # saldo y plan
higgsfield auth login              # re-autenticar
higgsfield model list --image      # modelos de imagen disponibles
higgsfield model list --video      # modelos de video disponibles
```

---

## Antipatrones (no hagas esto)

- ❌ Editar `.state.json` con un editor — usá siempre `state.py`.
- ❌ Saltar el preflight — los errores de Higgsfield son silenciosos downstream.
- ❌ Generar el brand book con HTML hecho a mano — invoca `canvas-design`.
- ❌ Pasarle Veo/Kling/Seedance a una imagen con texto — esos modelos smear el texto. Usá `gpt_image_2`.
- ❌ Usar nombres de modelo con guiones (`gpt-image-2`) — los reales son snake_case (`gpt_image_2`).
- ❌ Saltar gates ("vamos directo al logo sin paleta lockeada") — el ledger lo bloquea.

---

## Troubleshooting

### `preflight: faltan dependencias`

Leé el mensaje. Casi siempre es:
- Higgsfield no autenticado → `higgsfield auth login`
- `jq` faltante → `brew install jq`
- Skills bundleadas faltantes → `npx skills add higgsfield-ai/skills`

### `Error: no encontré URL del asset en el JSON`

Significa que Higgsfield procesó el job pero el parser no entiende la respuesta. Si pasa, contame el JSON y abrimos issue. El parser está en `.claude/skills/cmo-agency/scripts/lib/hf.sh`.

### `Failed to create credentials dir`

Permisos de `~/.config`. Mirá Paso 2 arriba.

### El brand book no se genera

Probablemente falta la skill `canvas-design`. En Claude Code: `/anthropic-skills:canvas-design` debe estar disponible. Si no, instalala desde el marketplace.

### Cambiar la ruta base del repo

Si clonaste en una ruta distinta a `/Users/erikgamboa/Documents/CMO/`, hay que reemplazar la ruta absoluta en:

```bash
grep -rln "/Users/erikgamboa/Documents/CMO" .claude/ CLAUDE.md
```

Reemplazá todas las ocurrencias por tu ruta. Próxima versión va a hacer esto automático con una variable de entorno.

---

## Costos aproximados (Higgsfield)

| Output | Modelo | Créditos aprox |
|---|---|---|
| Paleta swatch (1 imagen 2K) | gpt_image_2 | 5-10 |
| Tipografía sample (1 imagen 2K) | gpt_image_2 | 5-10 |
| Logo (4 candidatos) | gpt_image_2 | 20-40 |
| Brand book infográfico | gpt_image_2 | 10-15 |
| Post estático | gpt_image_2 / nano_banana_pro | 5-10 |
| Reel 15s | seedance_2_0 | 30-60 |
| UGC video 15s | seedance_2_0 | 30-60 |
| Foto producto (1 variante) | product-photoshoot | 10-20 |

Una marca completa (estrategia → brand book → 5 creativos) cuesta típicamente 150-300 créditos. Plan Plus arranca con 1000+.

---

## Siguiente paso

Cuando tengas todo verde, escribí:

```
/cmo-agency
```

Y respondé las dos primeras preguntas del partner virtual:

1. ¿Qué producto o servicio quieres lanzar?
2. ¿Es una marca nueva, ya operás, o tenés documentos?

A partir de ahí, va guiando todo. Una pregunta por mensaje. Sin bombardeo.

---

## Soporte

- Issues / bugs: abrí un issue en este repo.
- Cambios en Higgsfield API: el wrapper en `cmo-agency/scripts/lib/hf.sh` es el único lugar que toca el CLI — fixes ahí.
