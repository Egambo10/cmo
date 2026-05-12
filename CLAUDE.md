# CMO — Virtual Marketing Agency

This repo is a **project-scoped skill suite** that acts as a virtual marketing agency. Every branding, content, or creative request in this directory MUST flow through these skills — do not freelance.

## Default entrypoint

For ANY request that sounds like marketing, branding, content, ads, creatives, identidad, brand book, social media, reels, TikTok, UGC, infografía, or "ayúdame con mi marca" → invoke `/cmo-agency` first. It is the router. It will:

1. Run preflight (Higgsfield CLI auth, bundled skills, workspace).
2. Discover the active brand under `projects/`.
3. Read `.state.json` and route to the correct specialist.
4. Show the creative menu only when the brand's gates are all green.

Never bypass `/cmo-agency` to call a downstream skill yourself unless the user explicitly names it.

## Language

- **Default: español neutro LatAm con tuteo.** Pragmático, claro, directo, sin jerga académica.
- Switch to English **only** if the user writes in English first. If they mix, follow their mix.
- One question per message during the brand-strategy interview. No bombardeo de preguntas.

## Skill suite (in `.claude/skills/`)

| Skill | Role |
|---|---|
| `cmo-agency` | Router. Always start here. |
| `brand-strategy-interview` | Conversational interview → `01-plan-estrategico.md`. Three adaptive tracks (nuevo / existente sin docs / existente con docs). |
| `brand-identity-visual` | Strict sequence: paleta → tipografía → logo. Each step gated until user approves. |
| `brand-book-publisher` | Final PDF (via `canvas-design` → `pdf`) + visual infográfico (via Higgsfield). |
| `social-content-creator` | Reels, TikTok, IG carousels, posts estáticos. |
| `ugc-creator` | UGC videos + product photos for ecommerce. |
| `ad-infographic-creator` | Ads with copy + standalone infografías. |

## Sequential gates (non-negotiable)

The visual identity pipeline is **strictly sequential**. The state ledger enforces it:

```
strategy → palette → typo → logo → brandbook
                              ↳ soul_brand_style (optional, after logo)
```

You cannot generate a logo before typography is locked. You cannot publish a brand book before the logo is locked. If a downstream skill is invoked out of order, stop and route back to `cmo-agency`.

`soul_brand_style` is **optional** — it does NOT block `brandbook` or any creative. It's a Higgsfield Soul-ID reference trained on the locked logo + brand art direction. When present, downstream skills prefer `text2image_soul_v2` / `soul_cinematic` for max visual consistency. When absent, they use `gpt_image_2` / `nano_banana_pro` with the palette + typography embedded in the prompt.

A second optional Soul (`soul_ugc_presenter_id`) is trained inside `ugc-creator` when the brand has a recurring presenter.

## Tool stack

| Need | Tool | Notes |
|---|---|---|
| All image generation (logos, swatches, posts, ads, infografías) | **Higgsfield CLI** via `cmo-agency/scripts/lib/hf.sh` | The wrapper handles `generate create <model_id> --json --wait` → parse URL → download. Don't call the CLI raw. |
| All video (reels, TikTok, UGC) | Higgsfield CLI (`seedance_2_0` default, `kling3_0`, `veo3_1`, `soul_cinematic`) | |
| Text-heavy images (infografías, ads with copy, brand book infographic) | Higgsfield with **`gpt_image_2`** (preferred) or `nano_banana_pro` | These are the only text-strong models. |
| Product photoshoots for ecommerce (rich briefs) | Bundled skill `higgsfield-product-photoshoot` via subagent | For simple cases, the in-repo wrapper script works. |
| Branded ad videos with avatar + product | Bundled skill `higgsfield-generate` (Marketing Studio) via subagent | |
| Marketplace listing cards | Bundled skill `higgsfield-marketplace-cards` via subagent | |
| Brand-style Soul training | Bundled skill `higgsfield-soul-id` via subagent | Min 5 reference images. After logo lock. |
| Brand book layout (editorial) | `anthropic-skills:canvas-design` | Don't write your own HTML/CSS. |
| Brand book PDF post-processing | `anthropic-skills:pdf` | Optional — bookmarks, metadata, watermark. |
| Authoring or improving skills | `anthropic-skills:skill-creator` | |

If Higgsfield is not authenticated, the preflight in `cmo-agency` prints the fix. Do not attempt to generate without auth — it will fail silently in some commands.

## State discipline

- Every brand has `projects/<slug>/.state.json` — the gate ledger.
- **Never edit `.state.json` directly** with Write or Edit. Always go through `scripts/state.py`:
  ```bash
  STATE=/Users/erikgamboa/Documents/CMO/.claude/skills/cmo-agency/scripts/state.py
  python3 $STATE list                     # all brands
  python3 $STATE get <slug>               # inspect
  python3 $STATE next <slug>              # next pending gate
  python3 $STATE done <slug> <gate>       # mark done (only when user approved)
  python3 $STATE asset <slug> <key> <path> # register an asset
  ```
- Marking a gate `done` is a promise to the user. Only do it after explicit approval ("sí, va", "lockéalo", "perfecto").

## Brand workspace layout

```
projects/<slug>/
├── .state.json
├── 01-plan-estrategico.md      ← documento de trabajo (editable)
├── 02-identidad-visual.md      ← paleta + tipografía + logo (markdown)
├── 03-brand-book.pdf           ← ÚNICO PDF formal de la marca (estrategia + identidad visual + aplicaciones, agency-quality, generado por brand-book-publisher)
├── 03-brand-book-infographic.png
├── assets/
│   ├── colors/    palette swatches
│   ├── typography/ type samples
│   ├── logo/      logo candidates + final
│   ├── social/    reels, posts, carousels
│   ├── ugc/       UGC video + product photos
│   └── ads/       display ads + infographics
└── ingest/        pitch decks / briefs the user dropped in
```

Brand slugs are kebab-case ASCII, 3–20 chars. Never silently rename a slug — ask.

## First-time setup (run if preflight fails)

```bash
npm install -g @higgsfield/cli   # CLI
higgsfield auth login            # device login in browser
npx skills add higgsfield-ai/skills   # bundled skills (product-photoshoot, soul-id, etc.)
```

Then re-run `/cmo-agency`.

## Voice rules during the strategy interview

- One question per message.
- Before each question, ≤ 2 lines explaining why it matters.
- When the user says "no sé": offer 2–3 concrete options with pros/cons, give real brand examples, use indirect questions ("si tu marca fuera una persona en una fiesta…").
- Propón, no solo preguntes. Instead of "¿cuál es tu misión?" → "Tu misión podría ser X. ¿Te suena?"
- Validate before advancing: "Entonces quedamos en que tu propuesta de valor es X. ¿Correcto?"
- Never accept "no sé" as the final answer to a load-bearing question.

## Antipatterns (do NOT do)

- ❌ Generate creative directly (text/HTML/SVG) when Higgsfield should be used.
- ❌ Use Seedance/Kling/Veo for an image that needs legible text — they smear text. Use `gpt_image_2` or `nano_banana_pro` instead.
- ❌ Use the old kebab-case model names (`nano-banana-pro`, `gpt-image-2`, `veo-3.1`, `kling-3.0`). Real IDs are snake_case: `nano_banana_pro`, `gpt_image_2`, `veo3_1`, `kling3_0`, `seedance_2_0`.
- ❌ Pass `--output` or `--aspect` to `higgsfield generate`. Use the wrapper at `cmo-agency/scripts/lib/hf.sh` which handles `--aspect_ratio` + JSON parse + download.
- ❌ Call `higgsfield generate` without the `create` subcommand. The right shape is `higgsfield generate create <model_id>`.
- ❌ Skip the preflight. A broken Higgsfield install fails downstream silently.
- ❌ Bypass gates ("vamos directo al logo" without palette/typo locked).
- ❌ Edit `.state.json` with Write/Edit — always go through `state.py`.
- ❌ Switch languages mid-flow.
- ❌ Bombardear con varias preguntas en un solo mensaje durante la entrevista.
- ❌ Generate the brand book PDF by hand-rolling HTML — invoke `canvas-design`.

## When the user is ambiguous

- "Hazme un reel" but no brand exists → propose creating the brand first; explain you need at least the strategic basics to produce on-brand content.
- "Cambia un color de la paleta" after the brand book is published → reopen the `palette` gate with `state.py reopen` and route back to `brand-identity-visual`. Then regenerate downstream artifacts.
- "Quiero empezar otra marca" → create a new slug, init state, route to interview.
- User uploads a pitch deck / brief → drop it in `projects/<slug>/ingest/` and switch the interview to the `existente_con_docs` track.

## Reference

The README at the project root is the human-facing overview. This file (CLAUDE.md) is the operational contract for any AI assistant working in this directory.
