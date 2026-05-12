# CMO — Virtual Marketing Agency

This directory holds the **CMO agency skill suite** (project-scoped, lives in `.claude/skills/`) AND the operational state for every brand you build with it.

The skills are local to this project — they are NOT installed globally. Claude Code auto-discovers them when you're working inside this directory.

## How it works

Open Claude Code in this directory, then invoke any of these:

| Skill | What it does |
|---|---|
| `/cmo-agency` | **Start here.** Master router. Checks brand state, routes to the right specialist, or shows the creative menu when the brand is ready. |
| `/brand-strategy-interview` | Conversational strategic interview in Spanish. Produces `01-plan-estrategico.md`. |
| `/brand-identity-visual` | Sequential paleta → tipografía → logo (each behind an approval gate). Produces `02-identidad-visual.md`. |
| `/brand-book-publisher` | Final brand book PDF (via `canvas-design` → `pdf`) + visual infographic (via Higgsfield). |
| `/social-content-creator` | Reels, TikTok, IG carousels, static posts. |
| `/ugc-creator` | UGC videos + product photos for ecommerce. |
| `/ad-infographic-creator` | Ads with copy + standalone infographics. |

## First-time setup

```bash
# Higgsfield CLI — single gateway for all image/video generation
npm install -g @higgsfield/cli
higgsfield auth login

# Higgsfield bundled skills (gives us product-photoshoot, soul-id, etc.)
npx skills add higgsfield-ai/skills
```

`/cmo-agency` runs a preflight on first invocation and tells you what's missing.

## Brand workspace layout

Each brand lives under `projects/<slug>/`:

```
projects/mi-marca/
├── .state.json                      ← gate ledger (don't edit by hand)
├── 01-plan-estrategico.md           ← strategy
├── 02-identidad-visual.md           ← visual identity (palette, type, logo concept)
├── 03-brand-book.pdf                ← final brand book
├── 03-brand-book-infographic.png    ← visual summary
├── assets/
│   ├── colors/    palette swatches
│   ├── typography/ type samples
│   ├── logo/      logo candidates + final
│   ├── social/    reels, posts, carousels
│   ├── ugc/       UGC video + product photos
│   └── ads/       display ads + infographics
└── ingest/                          ← drop pitch decks / briefs here
```

## State helper

The state ledger lives in `.state.json` for each brand. Use the helper:

```bash
# Run from the CMO directory
STATE=./.claude/skills/cmo-agency/scripts/state.py

# List all brands and where they are
python3 $STATE list

# Inspect one
python3 $STATE get mi-marca

# Find next pending gate
python3 $STATE next mi-marca
```

## Directory layout

```
CMO/
├── README.md
├── .gitignore
├── .claude/
│   └── skills/                      ← 7 project-scoped skills live here
│       ├── cmo-agency/
│       ├── brand-strategy-interview/
│       ├── brand-identity-visual/
│       ├── brand-book-publisher/
│       ├── social-content-creator/
│       ├── ugc-creator/
│       └── ad-infographic-creator/
└── projects/                        ← each brand you build is a folder here
    └── <brand-slug>/...
```

## Voice

All skills speak **español neutro LatAm con tuteo** by default. They switch to English if you write in English first.

## Tool stack

| Need | Tool |
|---|---|
| All image generation (logos, swatches, slides, posts, ads, infographics) | Higgsfield CLI |
| All video generation (reels, TikTok, UGC) | Higgsfield CLI (Veo / Kling / Seedance) |
| Product photoshoots for ecommerce | Higgsfield `product-photoshoot` skill |
| Brand book layout (editorial design) | `anthropic-skills:canvas-design` |
| Brand book PDF export / post-processing | `anthropic-skills:pdf` |
| Authoring or improving the skills themselves | `anthropic-skills:skill-creator` |
