# Handing off to canvas-design

This is a prompt template for invoking the `anthropic-skills:canvas-design` skill from `brand-book-publisher`. Fill the placeholders before invoking.

---

## Request template

```
I need a 10-12 page editorial brand book PDF.

Brand: {{BRAND_NAME}}
Output path: /Users/erikgamboa/Documents/CMO/projects/{{SLUG}}/03-brand-book.pdf
Format: A4 portrait, agency-quality editorial layout, generous whitespace, type-led, no stock photos.

# Visual system (use exactly these)

- Primary color: {{PRIMARY_HEX}}
- Secondary color: {{SECONDARY_HEX}}
- Accent color: {{ACCENT_HEX}}
- Neutral light: {{NEUTRAL_LIGHT_HEX}}
- Neutral dark: {{NEUTRAL_DARK_HEX}}
- Headline font: {{HEADLINE_FONT}}
- Body font: {{BODY_FONT}}
- Logo asset: {{LOGO_PATH}}
- Palette swatch image: {{PALETTE_IMAGE_PATH}}
- Type specimen image: {{TYPE_SAMPLE_PATH}}

# Pages

1. **Cover** — Brand name (hero size), "Brand Book", year, logo centered or top-left.
2. **Tabla de contenidos** — numbered, with page references, using the body font.
3. **Estrategia I** — Misión + Visión. One per section, large headline + supporting paragraph.
4. **Estrategia II** — Valores (3-5). Card-like blocks, one short title + 2-line explanation each.
5. **Estrategia III** — Propuesta de valor + Posicionamiento. Two columns or stacked.
6. **Audiencia** — Buyer persona summary card: nombre/etiqueta, demografía, psicografía, goals, pain points, comportamiento, objeciones, canales, mensaje clave.
7. **Personalidad + Tono de voz** — Rasgos + frases "Somos X, no Y". Tone dimensions table. Ejemplos por canal.
8. **Logo** — Show final logo large + variants (color, monochrome, on dark, isolated symbol if applicable). Usos correctos vs incorrectos with subtle red/green indicators.
9. **Paleta de colores** — Reference {{PALETTE_IMAGE_PATH}} or render swatches inline with HEX, usos web (CTA, títulos, texto, fondos, hover) y print (ads, promo, packaging).
10. **Tipografía** — Reference {{TYPE_SAMPLE_PATH}} or render specimen inline. Include size system table (H1, H2, H3, body, caption, button) in px y pt with weights.
11. **Aplicaciones de marca** — Mockups conceptuales: hero web, post de Instagram, packaging primary. Sin photos reales — diagramatic.
12. **Cierre** — Una frase de manifiesto + contacto si el usuario lo pidió.

# Content (paste in)

## Misión
{{MISION}}

## Visión
{{VISION}}

## Valores
{{VALORES_LIST}}

## Propuesta de valor
{{PROPUESTA_VALOR}}

## Posicionamiento
{{POSICIONAMIENTO}}

## Buyer persona
{{BUYER_PERSONA_TABLE}}

## Personalidad
Rasgos: {{PERSONALIDAD_RASGOS}}
Somos / No somos: {{PERSONALIDAD_SOMOS_NO}}

## Tono de voz — dimensiones
{{TONO_DIMENSIONES_TABLE}}

## Tono de voz — ejemplos por canal
{{TONO_EJEMPLOS}}

## Cómo NO hablamos
{{TONO_NO}}

## Concepto de logo
{{LOGO_CONCEPTO}}

## Usos correctos del logo
{{LOGO_USOS_CORRECTOS}}

## Usos incorrectos del logo
{{LOGO_USOS_INCORRECTOS}}

## Paleta — usos
{{PALETA_USOS_TABLE}}

## Tipografía — sistema de tamaños
{{TIPOGRAFIA_TABLE}}
```

---

## Notes

- Don't add or change content beyond what's in the brief.
- Don't use stock photos — this is a type-led editorial document.
- The logo file at `{{LOGO_PATH}}` is the master asset; do not regenerate it.
- Aim for ~10-12 pages, not 30. Density per page is high, but each page has one job.
- Output must be a single PDF saved at the path specified.
