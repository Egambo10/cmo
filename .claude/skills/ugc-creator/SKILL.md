---
name: ugc-creator
description: Generate UGC (user-generated-content style) videos and product photos for ecommerce. Use this skill whenever the user asks for UGC, video de cliente, testimonio, video estilo casero, foto de producto, packshot, lifestyle shot, foto para tienda, foto para Shopify, foto para Amazon, ecommerce photo, or product photoshoot. Two paths: UGC video (Higgsfield Veo 3.1 for talking-head realism) and UGC product photo (delegates to the existing `higgsfield-product-photoshoot` skill from `higgsfield-ai/skills`). Reads brand voice from `01-plan-estrategico.md` to write scripts. Requires the brand's full identity locked.
---

# UGC Creator

You generate UGC-style assets for ecommerce — videos that look like real customer testimonials, and product photos that work in marketplace and DTC contexts.

## Required gates

- `strategy.done == true` AND `palette.done == true` AND `typo.done == true` AND `logo.done == true`.

If any are missing, route back to `cmo-agency`.

## On entry

Read `01-plan-estrategico.md` (voz, audiencia, propuesta de valor) and `02-identidad-visual.md` (logo si lo necesitas para photo composition).

Ask one routing question:

> *"¿Qué necesitas? (1) Video UGC (talking-head testimonial), (2) Foto UGC de producto (lifestyle / packshot / in-context para ecommerce)."*

## Route 1 — Video UGC

### Routing por sub-tipo (importante)

Antes de empezar, decide el sub-tipo:

| Sub-tipo | Cómo se genera |
|---|---|
| **UGC genérico** (talking-head sin avatar fijo, sin producto importado) | Script `scripts/generate_ugc_video.sh` con `seedance_2_0` o `veo3_1` |
| **UGC con presenter recurrente de la marca** | Si ya existe `soul_ugc_presenter_id` en `.state.json`: usa `soul_cinematic` + `--soul-id`. Si no existe, propón entrenar el Soul (ver "Entrenar UGC-presenter Soul" abajo). |
| **UGC ad con avatar + producto** (Marketing Studio) | **Delegar via subagent** al skill `higgsfield-generate` (Marketing Studio video workflow). Brief: producto + avatar + hook/setting. No uses el script local. |
| **Foto/video de producto sin presenter** (packshot, lifestyle scene) | Cae bajo Route 2 — Foto UGC. |

### Entrenar UGC-presenter Soul (cuando aplica)

Si la marca tiene una persona fija (fundadora, modelo, presenter), propón entrenar un Soul:

> *"Para que todos tus videos UGC mantengan la misma cara, lo cleanest es entrenar un **Soul del presenter**. Necesito 5+ fotos suyas (frontales, de lado, ángulos distintos, iluminación variada). ¿Las tienes?"*

Si dice sí:
- Recolecta los paths a las 5+ imágenes.
- **Delega al skill `higgsfield-soul-id` via subagent** con un brief:
  > *"Train a UGC-presenter Soul reference for brand '<brand-name>'. Reference images: [paths]. Name: '<slug>-ugc-presenter'. Use --soul-2. Return the soul_ref_id."*
- Cuando regrese: `state.py asset <slug> soul_ugc_presenter_id <ref>` y úsalo en adelante.

### Flujo para UGC genérico / con Soul

1. **Ask intent**: *"¿Qué objetivo tiene? (a) Testimonio post-compra, (b) Hook awareness para ads, (c) Educacional/explicativo. Y dime qué producto + dolor que resuelve."*

2. **Write the UGC script** based on brand voice. UGC ≠ corporativo. Estructura:
   - **Hook (2-3s)**: Frase casual que para el scroll. Ej: *"Acabo de probar X y honestamente…"*
   - **Problema (5-8s)**: Conecta con dolor real. *"Llevaba meses buscando algo que…"*
   - **Producto + beneficio (10-15s)**: Cómo entró, qué cambió. Específico.
   - **CTA (3-5s)**: Suave, no de venta hard. *"Si te identificas, deberías probarlo"*.

3. **Show the script** al usuario. Pide aprobación.

4. **Build the Higgsfield prompt** describiendo el "actor", ambiente, vestimenta, iluminación, tono. UGC realism: cámara fija o handheld leve, luz natural, encuadre frontal mid-shot. **NO over-producir**.

5. **Generate** con `scripts/generate_ugc_video.sh <slug> "<scene-prompt>" "<duration-s>" [model] [soul_id]`.
   - Default model: `seedance_2_0` (SOTA general).
   - Si la marca tiene `soul_ugc_presenter_id`: usa `soul_cinematic` + el soul-id (lee `.state.json` con `state.py get <slug>` para obtenerlo).
   - `veo3_1` solo si necesitas character-driven extra.

6. **Output**: `assets/ugc/<date>-ugc-video.mp4`. Muestra preview.

7. **Iterate or approve**. Si aprueba, escribe sidecar `.md` con script + uso sugerido (ads / orgánico / email).

## Route 2 — Foto UGC de producto

1. **Ask intent**: *"¿Qué tipo? Te leo los modos:*
   *• `product_shot` — packshot puro (fondo limpio, hero shot)*
   *• `lifestyle_scene` — producto en uso, escena real*
   *• `closeup_product_with_person` — closeup con manos sosteniéndolo*
   *• `hero_banner` — banner ancho para web*
   *• `social_carousel` — para slides de IG*
   *• `ad_creative_pack` — set para Meta/Google ads*
   *• `virtual_model_tryout` — modelo usando/probando el producto*
   *• `moodboard_pin` — Pinterest aesthetic*
   *• `conceptual_product` — surreal / CGI*
   *• `restyle` — variar la estética de una foto existente*
   *Y dime: producto + persona/lugar si aplica."*

2. **Decide direct vs subagent**:
   - **Brief simple** (un modo, sin imagen de referencia, intent en una línea) → corre `scripts/generate_ugc_photo.sh` directo.
   - **Brief rico** (múltiples imágenes de referencia, brand_context, product_context, varias variantes) → **delega vía subagent al skill `higgsfield-product-photoshoot`** que tiene el flow completo de prompt enhancement y manejo de referencias.

3. **Build the shot brief** con detalles necesarios:
   - Producto (qué es, materiales, color)
   - Modo (de la lista arriba)
   - Ambiente / setting si aplica
   - Iluminación (natural / estudio / dramática)
   - Modelo / no modelo
   - Aspect ratio (1:1 para marketplace, 4:5 para IG, 3:4 para Pinterest, 16:9 para hero)
   - Imagen de referencia del producto si existe (path local o upload-id)

4. **Run** `scripts/generate_ugc_photo.sh <slug> "<intent-prompt>" <mode> [aspect_ratio] [reference_image] [count]`. El script llama `higgsfield product-photoshoot create` con el modo y prompt.

5. **Output**: `assets/ugc/<product>-<type>-<date>.png`. Muestra preview.

6. **Itera** si necesita ajustar (más cálido, distinta pose, otro fondo). UGC product photos suelen necesitar 2-3 iteraciones.

## Voice & coaching

- UGC funciona porque NO se siente producido. Si tu script suena como "ad", lo estás haciendo mal.
- Frases casuales > frases pulidas. "Honestamente…" / "Sin mentir…" / "No esperaba…" funcionan.
- Personas: para video UGC en Latam, descripciones específicas de etnia + edad + lugar ayudan. Higgsfield maneja diversidad mejor cuando le das contexto cultural.

## Antipatrones

- ❌ Scripts demasiado pulidos — pierde el feel UGC.
- ❌ Productos con sombras dramáticas para "lifestyle" (mata el feel orgánico).
- ❌ Usar Kling para UGC humano (es cinematográfico — usa Veo).
- ❌ Generar antes de mostrar y aprobar el script.
