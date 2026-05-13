# Hola, soy Marko. 👋

**Soy tu CMO virtual.** Vivo dentro de Claude Code como una agencia de marketing completa que entrevista, diseña, construye brand books y produce contenido — siempre on-brand, sin que tengas que repetirle a un freelancer cuál es tu paleta.

> *Marko, de marca. El que se encarga de que tu marca quede bien hecha desde el día uno.*

Este repositorio contiene el **skill suite que da vida a Marko**: 7 skills coordinadas que viven en `.claude/skills/`. No se instala como una app — Claude Code las descubre solas cuando abres esta carpeta.

---

## Qué hace Marko

Te lleva, paso por paso, del *"tengo una idea de negocio"* hasta *"tengo brand book, reels, ads y fotos de producto, todos coherentes"*. Una entrevista de estrategia, una identidad visual con secuencia estricta (paleta → tipografía → logo), un brand book editorial PDF, y producción continua de creativos después.

Cada decisión la valida contigo antes de avanzar. Una pregunta por mensaje. Habla en español neutro LatAm con tuteo.

## Cómo se invoca

Abre Claude Code dentro de esta carpeta y escribe el comando del agente:

```
/cmo-agency
```

> El nombre técnico de la skill es `cmo-agency` (el "qué hace" — Chief Marketing Officer + agency).
> El nombre del agente que la corre es **Marko** (el "quién" — tu CMO virtual).
> Cuando invocas la skill, el que te saluda es Marko.

A partir de ese momento, Marko revisa preflight (Higgsfield CLI + auth + bundled skills), detecta si tienes alguna marca empezada en `projects/`, y arranca el flujo correcto.

## Las 7 skills detrás de Marko

| Skill | Lo que hace |
|---|---|
| `cmo-agency` | **El cerebro de Marko.** Router maestro. Revisa el estado de tu marca, decide qué especialista invocar, o muestra el menú creativo cuando la marca ya está lista. |
| `brand-strategy-interview` | Entrevista estratégica conversacional. Produce `01-plan-estrategico.md` con misión, visión, valores, propuesta de valor, posicionamiento, buyer persona, personalidad, tono de voz. |
| `brand-identity-visual` | Paleta → tipografía → logo, en orden estricto, cada paso bloqueado hasta tu aprobación. Produce `02-identidad-visual.md`. |
| `brand-book-publisher` | **El entregable formal:** brand book editorial PDF (vía `canvas-design`) + infográfico visual (vía Higgsfield). Es el único PDF de marca que produce el sistema — incluye estrategia + identidad visual + aplicaciones. |
| `social-content-creator` | Reels, TikTok, carruseles de Instagram, posts estáticos. |
| `ugc-creator` | Videos UGC tipo testimonial + fotos de producto para ecommerce (Shopify, Amazon). |
| `ad-infographic-creator` | Anuncios pagados con copy (Meta, Google, LinkedIn) + infografías educativas independientes. |

---

## Setup mínimo

Si es la primera vez, Marko necesita dos cosas en tu computadora:

```bash
# 1. Higgsfield CLI — la única vía para generar imágenes y video
npm install -g @higgsfield/cli
higgsfield auth login

# 2. Skills bundleadas de Higgsfield (product-photoshoot, soul-id, marketplace-cards, marketing-studio)
npx skills add higgsfield-ai/skills
```

El primer `/cmo-agency` corre un preflight y te dice exactamente qué falta con copy-pasteables para arreglarlo.

> **Guía completa para usuarios no técnicos** (paso a paso con capturas, sin terminal): consulta la [guía en Notion](https://www.notion.so/35e8d0332af48136a9ccf1af15be82c5) que tiene el prompt mágico que Marko se instala solo.

---

## Layout del workspace por marca

Cada marca que construyas vive en su propia carpeta bajo `projects/<slug>/` y es **estrictamente privada** — el `.gitignore` la excluye de git para que nunca subas tu estrategia confidencial al repo público por accidente.

```
projects/mi-marca/
├── .state.json                      ← ledger de gates (no editar a mano — usa state.py)
├── 01-plan-estrategico.md           ← documento de trabajo de la estrategia
├── 02-identidad-visual.md           ← paleta, tipografía, logo
├── 03-brand-book.pdf                ← entregable formal (único PDF de la marca)
├── 03-brand-book-infographic.png    ← resumen visual de 1 página
├── assets/
│   ├── colors/    swatches de paleta
│   ├── typography/ muestras tipográficas
│   ├── logo/      candidatos + logo final
│   ├── social/    reels, posts, carruseles
│   ├── ugc/       videos UGC + fotos de producto
│   └── ads/       anuncios + infografías
└── ingest/                          ← deja aquí pitch decks / briefs que Marko deba leer
```

---

## State helper

El ledger de gates de cada marca vive en `.state.json`. Marko lo gestiona automáticamente, pero si quieres inspeccionarlo manualmente:

```bash
STATE=./.claude/skills/cmo-agency/scripts/state.py

# Lista todas tus marcas y dónde está cada una en el pipeline
python3 $STATE list

# Inspecciona el estado completo de una marca
python3 $STATE get mi-marca

# Pregunta cuál es el siguiente gate pendiente
python3 $STATE next mi-marca
```

**Nunca edites `.state.json` a mano** — Marko ya tiene el helper para hacerlo seguro.

---

## Tool stack

| Necesidad | Herramienta |
|---|---|
| Imágenes (logos, swatches, slides, posts, ads, infografías) | Higgsfield CLI + `gpt_image_2` / `nano_banana_pro` |
| Video (reels, TikTok, UGC) | Higgsfield CLI + `seedance_2_0` / `veo3_1` / `kling3_0` |
| Fotos de producto para ecommerce | Higgsfield bundled skill `product-photoshoot` (vía subagent) |
| Cards de marketplace (Amazon, MercadoLibre) | Higgsfield bundled skill `marketplace-cards` (vía subagent) |
| Consistencia visual (Soul reference) | Higgsfield bundled skill `soul-id` (vía subagent) |
| Brand book PDF editorial | `anthropic-skills:canvas-design` (genera Python+reportlab a partir de un design philosophy) |
| Post-procesado PDF (bookmarks, metadata) | `anthropic-skills:pdf` |
| Crear o mejorar las skills mismas | `anthropic-skills:skill-creator` |

---

## Voice

Todas las skills de Marko hablan **español neutro LatAm con tuteo** por defecto. Cambian a inglés si tú escribes en inglés primero.

---

## Por qué Marko, no "CMO Agency"

Las herramientas técnicas dan miedo. Un agente con nombre, no.

`cmo-agency` es el slug del skill (descriptivo, busca-able). Pero cuando lo invocas y empieza a hablarte, no es un sistema — es **Marko**, tu partner virtual. Marko hace las preguntas, Marko te propone opciones, Marko valida cada decisión antes de avanzar. Y cuando algo se va a romper, Marko te avisa antes de tocar nada.

Es la misma idea por la que Don Memo de Electriclick no es "el segmento B2B-pro primario" — es Don Memo. Las personas hablan con personas.

---

## Soporte

Encontraste un bug, tienes una idea, o Marko se quedó atorado en algo extraño: abre un issue en este repo. Cuanto más específico el reporte (captura de pantalla del error, qué brand estaba activa, qué gate intentaba avanzar), más rápido se arregla.
