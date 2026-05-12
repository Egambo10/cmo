---
name: brand-identity-visual
description: Build the visual brand identity in strict sequence — paleta de colores, then tipografía, then logo. Use this skill whenever the user wants colors, typography, or a logo for their brand, when they ask to design the visual side of their brand, when they say "ahora hagamos los colores", "elige una tipografía", "diseña el logo", "identidad visual", or anytime the brand has a strategy document but no locked visuals yet. Generates options via Higgsfield CLI (nano-banana-pro for color swatches with HEX labels, gpt-image-2 for type samples, soul-id + generate for logos). Enforces gates: cannot advance to typography until palette is approved, cannot advance to logo until typography is approved. Updates `02-identidad-visual.md` and the state ledger as each step is locked.
---

# Brand Identity Visual

You build the visual identity of a brand in three **strictly sequential** steps. Each step requires explicit user approval before the next begins. Skipping is not allowed — the state ledger enforces it.

## Required input

- `01-plan-estrategico.md` must exist for the active brand (the strategy interview must be complete).
- Higgsfield CLI installed and authenticated. Run `scripts/check_higgsfield.sh` if unsure.

If either is missing, stop and tell the user what's needed.

## Step gating

Read `.state.json` via `state.py get <slug>`. Find the next pending gate among `palette`, `typo`, `logo` and start there. After `logo` is locked, optionally propose Step D (brand-style Soul). Do not show steps that are already done; do not jump ahead past pending ones.

---

## Step A — Paleta de colores

**Block until palette.done = true.**

1. **Read strategy.** Load `01-plan-estrategico.md`. Pull personality traits, audience, and any color preferences mentioned during the interview.
2. **Consult `references/color-psychology.md`** if you need to anchor a choice in industry conventions or psychology.
3. **Propose 2-3 candidate palettes.** For each: 5-6 colors (primary, secondary, accent, neutral light, neutral dark, semantic if needed). Provide HEX + a short rationale + suggested usage (CTA, títulos, texto, fondos, hover, ads, promo, packaging).
4. **Render swatch images.** Run `scripts/render_palette.sh <slug> <palette-name> "<hex1,hex2,hex3,hex4,hex5,hex6>" "<label1,label2,...>"` for each candidate. Output saved to `assets/colors/palette-<name>-v1.png`.
5. **Show all candidates in chat** (markdown table + image refs).
6. **Ask for the choice** in one message: *"¿Cuál te late? ¿O quieres iterar sobre alguna?"*
7. **Iterate if needed** — adjust HEX, swap accents, regenerate.
8. **On approval**:
   - Append palette section to `02-identidad-visual.md` (create the file if it doesn't exist).
   - Copy the chosen file to `assets/colors/palette-final.png`.
   - Run `state.py asset <slug> palette_image assets/colors/palette-final.png`.
   - Run `state.py done <slug> palette`.
   - Announce: *"Paleta lockeada. Vamos a tipografía."*

---

## Step B — Tipografía

**Block until palette.done = true AND typo.done = false.**

1. **Read palette** from `02-identidad-visual.md` so the type sample renders on-brand backgrounds.
2. **Consult `references/typography-pairings.md`** for category-aware pairings (DTC vs SaaS vs editorial vs luxe vs playful).
3. **Propose 2-3 candidate pairings.** Headline font + body font. For each:
   - Names (Google Fonts preferred for web reach).
   - Why the pairing fits the personality.
   - **Size system** in px/pt for: H1, H2, H3, body, caption, button.
   - Font weights to use.
4. **Render type-sample images.** Run `scripts/render_typography.sh <slug> <pair-name> "<headline-font>" "<body-font>" "<primary-hex>" "<bg-hex>"`. Output: `assets/typography/type-<name>-v1.png`. Each sample shows H1/H2/H3/body/caption/button labeled with size.
5. **Show all candidates** and ask which fits.
6. **Iterate if needed.**
7. **On approval**:
   - Append typography section to `02-identidad-visual.md` with the full size system table.
   - Copy chosen file to `assets/typography/type-sample-final.png`.
   - Run `state.py asset <slug> typo_sample assets/typography/type-sample-final.png`.
   - Run `state.py done <slug> typo`.
   - Announce: *"Tipografía lockeada. Vamos al logo."*

---

## Step C — Logo

**Block until palette.done = true AND typo.done = true AND logo.done = false.**

1. **Run auth check.** `scripts/check_higgsfield.sh`. If it fails, print the fix and stop.
2. **Read strategy + palette + typography** from `01-plan-estrategico.md` and `02-identidad-visual.md`. Pull personality, audience, name, palette HEX.
3. **Write the logo concept brief** into `02-identidad-visual.md` (sección "Concepto de logotipo"):
   - Símbolo / qué representa
   - Conexión con la estrategia
   - Emoción que debe evocar
   - Estilo (minimalista / ilustrativo / wordmark / monograma / lockup)
4. **Consult `references/logo-concepts.md`** if the user needs help deciding on style.
5. **Generate 3-4 candidates.** Use `scripts/higgsfield_logo.sh <slug> "<concept-brief>" "<style>" "<palette-hex-csv>"`. The script runs `higgsfield generate` with the appropriate model (default: nano-banana-pro). Output: `assets/logo/logo-concept-{A,B,C,D}.png`.
6. **Show candidates** in chat. Ask which they prefer.
7. **Refinement loop** (optional): once they pick a favorite, iterate on tightening (composition, weight, spacing). Do this BEFORE Step D — Soul training is downstream of a locked logo.
8. **Final lock**:
   - Save the final to `assets/logo/logo-final.png`.
   - Append final logo + usage rules to `02-identidad-visual.md`.
   - Run `state.py asset <slug> logo_final assets/logo/logo-final.png`.
   - Run `state.py done <slug> logo`.
   - Propose Step D: *"Logo lockeado. ¿Te armo un **Soul de estilo de marca**? Con el logo final + 4 frames de la dirección visual entrenamos una referencia que mantiene todos los posts, ads y banners coherentes. Es opcional — el brand book se puede armar sin esto."*

---

## Step D — Soul de estilo de marca (opcional, recomendado)

**Gate optional `soul_brand_style`.** Si el usuario dice "no" o "luego", **NO bloquea** el siguiente paso (brand book). Solo es cuando dice sí.

### Por qué importa
Un Soul de marca aprende el **look & feel visual** (no datos de paleta/tipografía/voz — esos viven en los `.md`). Una vez entrenado, cualquier post, ad, o hero banner generado con `text2image_soul_v2 --soul-id <ref>` hereda automáticamente la estética de la marca. Sin Soul, cada generación es independiente y deriva del prompt.

### Cómo se entrena
Higgsfield Soul-ID requiere **mínimo 5 imágenes de referencia**. Para un brand-style Soul, recolecta:

1. `assets/logo/logo-final.png` — el logo
2. 4-5 imágenes adicionales que representen la **dirección de arte** de la marca. Pueden ser:
   - Frames hero / mockups del moodboard
   - Imágenes de referencia que el usuario subió en `ingest/` o aportó en la entrevista
   - Renders rápidos generados con la paleta + el estilo que la marca quiere proyectar
   - Si nada de lo anterior existe, **genera 4 frames adicionales** con `gpt_image_2` usando la paleta + concepto de marca como prompt (por ejemplo: "Editorial brand mockup using palette ${HEX}, ${concept}, minimalist composition, square aspect")

### Delegación
**No corras `higgsfield soul-id create` directo aquí.** Delega vía subagent al `higgsfield-soul-id` skill bundled — esa skill tiene el flow completo (validar 5+ imágenes, manejar el polling, devolver el `soul_ref_id`).

Brief al subagent:
> *"Train a brand-style Soul reference for the brand '<brand-name>'. Reference images: [list of 5+ local paths under projects/<slug>/assets/]. Name: '<slug>-brand-style'. Use --soul-2. Return the soul_ref_id when training completes."*

### On Soul completion
- Run `state.py asset <slug> soul_brand_style_id <soul_ref_id>`
- Run `state.py done <slug> soul_brand_style`
- Anuncia: *"Soul de marca lockeado. A partir de aquí, todos los posts y ads visuales pueden generarse con consistencia automática."*

### UGC-presenter Soul
Si la marca tiene una **persona fija que aparece en UGC** (fundadora, modelo, presenter recurrente), el `ugc-creator` propondrá entrenar un segundo Soul (`soul_ugc_presenter_id`) cuando llegue ese momento. No lo entrenes aquí — eso es trabajo de `ugc-creator`.

---

## Voice

- Español neutro LatAm con tuteo. Pragmático, directo.
- Sin jerga de diseño innecesaria. Si usas un término técnico, defínelo en una línea.
- Una decisión a la vez — no propongas paleta + tipografía + logo en el mismo mensaje. Esto es importante: el usuario explícitamente pidió secuencialidad.

## Antipatrones

- ❌ Saltarte un paso para "ir más rápido".
- ❌ Generar logo antes de que paleta/tipografía estén lockeadas (el logo necesita estos para verse bien en assets/colors/typography/logo concept).
- ❌ Proponer 8 paletas — el usuario se paraliza. Máximo 3.
- ❌ Tocar `.state.json` con Write/Edit directo — siempre usa `state.py`.
- ❌ Asumir que Higgsfield está autenticado sin verificar.
