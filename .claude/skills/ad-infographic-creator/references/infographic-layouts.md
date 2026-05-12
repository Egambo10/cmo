# Infographic layouts

Layouts probados según tipo de infografía. Elige el adecuado antes de armar el prompt.

## 1. Stat hero (un dato grande)

**Cuándo**: tienes UN número/dato impactante que quieres destacar.

```
┌──────────────────────────┐
│                          │
│      TÍTULO PEQUEÑO      │
│                          │
│         87%              │  ← número gigante
│                          │
│   Subtexto explicativo   │
│   en 1-2 líneas          │
│                          │
│   [Logo + fuente]        │
└──────────────────────────┘
```

## 2. Grid 2x2 / 3x3 (comparativo o categórico)

**Cuándo**: 4-9 elementos del mismo nivel jerárquico.

```
┌──────────────────────────┐
│   Título                 │
├──────────┬───────────────┤
│ Item 1   │ Item 2        │
│ + texto  │ + texto       │
├──────────┼───────────────┤
│ Item 3   │ Item 4        │
│ + texto  │ + texto       │
└──────────┴───────────────┘
```

## 3. Timeline / proceso (paso a paso)

**Cuándo**: secuencia temporal o pasos de un proceso.

```
┌──────────────────────────┐
│   Cómo funciona          │
│                          │
│   1 ───→ 2 ───→ 3 ───→ 4 │
│   txt    txt   txt   txt │
│                          │
│   [Logo]                 │
└──────────────────────────┘
```

(Horizontal mejor en 16:9; vertical mejor en 9:16 con flechas hacia abajo.)

## 4. Hub & spoke (centro + ramas)

**Cuándo**: un concepto central con 4-6 satélites relacionados.

```
┌──────────────────────────┐
│       SAT 1   SAT 2      │
│           \  /           │
│   SAT 6 ─ CENTRO ─ SAT 3 │
│           /  \           │
│       SAT 5   SAT 4      │
└──────────────────────────┘
```

## 5. Comparison table (vs. competencia o vs. alternativa)

**Cuándo**: contrastar 2-3 opciones en 3-5 dimensiones.

```
┌──────────────────────────┐
│            NOSOTROS  ELLOS│
│  Feature 1   ✓        ✗  │
│  Feature 2   ✓        ✗  │
│  Feature 3   ✓        ~  │
│  Feature 4   ✓        ✗  │
│  Feature 5   ✓        ~  │
└──────────────────────────┘
```

## 6. Numbered list (top N)

**Cuándo**: "5 razones por las que…", "Top 7 errores…", "10 pasos…"

```
┌──────────────────────────┐
│   5 razones por las que │
│   tu marca no vende     │
│                          │
│   1 — Razón uno         │
│   2 — Razón dos         │
│   3 — Razón tres        │
│   4 — Razón cuatro      │
│   5 — Razón cinco       │
└──────────────────────────┘
```

## Reglas de diseño

1. **Una idea por infografía.** Si tienes 12 ideas, son 3 infografías, no una.
2. **Jerarquía clara**: título grande, subtítulos medios, body pequeño. No mezcles tamaños similares.
3. **Whitespace es 50% del éxito**. La gente no lee paredes de texto.
4. **Solo 2 colores + neutros**: si usas más, se ve recargado y no on-brand.
5. **Icons opcional**: si los usas, todos del mismo estilo (line / filled / duotone). Nunca mezclados.
6. **Logo y fuente al final**, no compiten con el contenido.

## Cómo construir el layout-spec para Higgsfield

El layout-spec que pasas al script `generate_infographic.sh` debe describir literalmente qué texto va en cada zona. Higgsfield (gpt-image-2) renderiza el texto que le des entre comillas.

Ejemplo de layout-spec para una Stat hero:

```
At top center, a small label "ESTADO DE LA INDUSTRIA 2026" in 14px uppercase letterspaced. \
Centered vertically, the number "87%" in 240px bold. \
Below the number, in 20px regular: "de las marcas DTC no tienen brand book documentado". \
Bottom-left corner: small logo placeholder. Bottom-right: source attribution "Fuente: estudio interno".
```
