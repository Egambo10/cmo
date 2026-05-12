---
name: brand-book-publisher
description: Produce the final brand book in two formats — a polished editorial PDF (via canvas-design + pdf skills) and a one-page visual infographic (via Higgsfield with text-strong model). Use this skill when the user has a brand whose strategy AND visual identity (palette, typography, logo) are all locked, and they say "armemos el brand book", "exporta el brand book", "dame el PDF final", "necesito el manual de marca", "infografía de marca", "brand book final", or anytime the brand is ready for delivery. Reads `01-plan-estrategico.md` + `02-identidad-visual.md` + the locked palette/logo/type assets, hands them to `anthropic-skills:canvas-design` for layout, optionally runs through `anthropic-skills:pdf` for post-processing, and generates the visual infographic with Higgsfield gpt-image-2. Flips the `brandbook` gate to done.
---

# Brand Book Publisher

You produce the **final brand book deliverable** for a brand whose strategy and visual identity are already locked. Two outputs:

1. `03-brand-book.pdf` — multi-page editorial PDF (the formal manual)
2. `03-brand-book-infographic.png` — one-page visual summary (shareable, posters, decks)

## Required gates

Read the active brand's `.state.json` via `state.py get <slug>`. Required:

- `strategy.done == true`
- `palette.done == true`
- `typo.done == true`
- `logo.done == true`

If any of these is false, **stop and explain**. Route the user back to `cmo-agency` so it can pick the right earlier skill.

Required files:
- `01-plan-estrategico.md`
- `02-identidad-visual.md`
- `assets/logo/logo-final.png`
- `assets/colors/palette-final.png` (or HEX list inside `02-identidad-visual.md`)
- `assets/typography/type-sample-final.png`

## Pipeline

### 1. Compile the brand brief (in-memory)

Read both markdown files. Extract:

- Brand name + tagline (if any)
- Misión, visión, valores
- Propuesta de valor + posicionamiento
- Buyer persona summary
- Personalidad + tono de voz
- Palette HEX list with usos
- Typography pairings with sizes
- Logo concept + final logo path
- Usos correctos / incorrectos del logo

### 2. Build the PDF via `anthropic-skills:canvas-design`

Invoke the `canvas-design` skill with a structured request. **Do not write your own HTML/CSS** — let canvas-design handle layout. Pass it:

```
Goal: Produce a 10-12 page editorial brand book PDF for "<brand-name>".
Output path: /Users/erikgamboa/Documents/CMO/projects/<slug>/03-brand-book.pdf
Format: A4, portrait, agency-quality editorial layout.

Pages (one section per page or spread):
1. Cover — brand name, "Brand Book", year
2. Tabla de contenidos
3. Estrategia — misión, visión
4. Estrategia — valores
5. Estrategia — propuesta de valor + posicionamiento
6. Audiencia — buyer persona
7. Personalidad + tono de voz
8. Logo — versiones + usos correctos / incorrectos
9. Paleta de colores — HEX + usos web/print (use swatches)
10. Tipografía — pairings + sistema de tamaños
11. Aplicaciones de marca (web, social, packaging)
12. Cierre / contacto

Visual style: respect the brand palette <HEX list>. Use brand typography <headline-font> for titles and <body-font> for body. Logo lives at <logo-final.png> — feature it on cover and section dividers. Color palette swatches at <palette-final.png>. Type specimen at <type-sample-final.png>.

Tone: editorial agency style. Generous whitespace. No stock photos. Type-led.
```

Canvas-design produces the PDF directly. Read the result and confirm it exists at the expected path.

### 3. Optional — post-process with `anthropic-skills:pdf`

If you need to:
- Add bookmarks / table-of-contents links
- Merge the infographic as an appendix page
- Add metadata (title, author, keywords)
- Encrypt or watermark

…invoke `anthropic-skills:pdf` to handle the post-processing on `03-brand-book.pdf`. Otherwise, canvas-design's output is final.

### 4. Generate the visual infographic via Higgsfield

Run `scripts/build_infographic.sh <slug>`. This wraps `higgsfield generate --model gpt-image-2` with a structured prompt that builds a 1-page infographic showing:

- Brand name as hero
- Logo
- Palette swatches with HEX
- Typography sample
- Personality keywords
- Tono de voz quick reference

Output: `/Users/erikgamboa/Documents/CMO/projects/<slug>/03-brand-book-infographic.png`.

### 5. Show previews and confirm

Show both outputs to the user:

> *"Listo. Te dejé dos entregables:*
> *• `03-brand-book.pdf` — el manual completo (12 páginas).*
> *• `03-brand-book-infographic.png` — el resumen visual de 1 página.*
> *Ábrelos y dime si quieres que ajustemos algo antes de cerrar."*

If they ask for changes, route the specific change:
- "El logo se ve chico" → regenera el PDF con canvas-design pidiendo más prominencia.
- "Cambia un color de la paleta" → te dice que no, hay que reabrir el gate `palette` con `state.py reopen` y volver a `brand-identity-visual`.
- "Mejor sin la página de contacto" → ajusta el brief a canvas-design.

### 6. Lock the gate

Cuando el usuario apruebe:

```bash
python3 /Users/erikgamboa/Documents/CMO/.claude/skills/cmo-agency/scripts/state.py asset <slug> brandbook_pdf 03-brand-book.pdf
python3 /Users/erikgamboa/Documents/CMO/.claude/skills/cmo-agency/scripts/state.py asset <slug> brandbook_infographic 03-brand-book-infographic.png
python3 /Users/erikgamboa/Documents/CMO/.claude/skills/cmo-agency/scripts/state.py done <slug> brandbook
```

Anuncia:

> *"Cerrado. La marca está completa. Cuando quieras contenido (reels, posts, ads, UGC), invoca `cmo-agency` y te muestro el menú."*

## Failure modes

- **`canvas-design` no disponible**: explica que la skill `anthropic-skills:canvas-design` debe estar habilitada. No intentes generar HTML+CSS+browser→PDF a mano.
- **`pdf` no disponible**: si el paso 3 (post-procesado) era necesario, explica el bloqueo. Si era opcional, omítelo y entrega lo que canvas-design produjo.
- **Higgsfield no autenticado**: ejecuta `/Users/erikgamboa/Documents/CMO/.claude/skills/brand-identity-visual/scripts/check_higgsfield.sh` para imprimir la guía de auth.

## Antipatrones

- ❌ Bypasear `canvas-design` para "ahorrar tiempo" haciendo tu propio HTML.
- ❌ Generar el brand book si algún gate visual está sin lockear.
- ❌ Tocar `.state.json` directamente — siempre `state.py`.
- ❌ Producir el infográfico con un modelo de Higgsfield que NO sea text-strong (nano-banana-pro o gpt-image-2). El infográfico tiene mucho texto.
