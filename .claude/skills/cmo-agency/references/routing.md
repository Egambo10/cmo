# Routing decision tree

The orchestrator's job is to look at brand state + user intent and pick the right specialist. This file documents the full tree including edge cases.

## Primary tree (no explicit user intent)

```
Is there a project under CMO/projects/?
├── No  → ask for slug, init state, → brand-strategy-interview
└── Yes → multiple?
         ├── Yes → ask which (or "nueva marca")
         └── No  → use it
         ↓
     Load .state.json
     ↓
     strategy.done == false?
     ├── Yes → brand-strategy-interview
     └── No  → palette.done && typo.done && logo.done?
              ├── No  → brand-identity-visual (resumes at first false gate)
              └── Yes → brandbook.done == false?
                       ├── Yes → brand-book-publisher
                       └── No  → show creative menu
```

## Explicit user intent (override the tree)

| User says | If brand is ready | If brand exists but incomplete | If brand doesn't exist |
|---|---|---|---|
| "hazme un reel" / "necesito un tiktok" / "post para IG" | → social-content-creator | Explain we need strategy + visuals first; route to first incomplete gate | Propose creating the brand first |
| "video UGC" / "foto de producto" | → ugc-creator | Same | Same |
| "ad con copy" / "infografía" | → ad-infographic-creator | Same | Same |
| "empecemos la marca" / "otra marca" / "marca nueva" | Treat as new — ask for slug, init state, → brand-strategy-interview | Same | Same |
| "el brand book" | → brand-book-publisher (if visual gates green) | Walk back to first incomplete visual gate | → brand-strategy-interview |
| "cambiar los colores" / "rehacer logo" | → brand-identity-visual with the relevant gate manually reopened (set that gate to false in state) | Same | Propose creating brand first |

## Edge cases

### Ingest path inside the interview
The interview handles ingestion of an existing document. The orchestrator just hands off — don't try to parse documents at the orchestrator level.

### User wants to skip strategy
If the user insists on skipping the strategic interview (e.g. "no quiero entrevista, dame el logo ya"), explain in one sentence that we need minimum brand voice + audience to make anything consistent, and offer a **5-question fast-track** route by passing `--fast-track` to `brand-strategy-interview`. The interview supports a stripped-down mode for impatient users.

### Corrupted state
If `.state.json` is missing keys or unparseable, don't crash. Show what's there, offer to either:
- (a) repair: reset only the missing gates to `false`,
- (b) reset entirely.

### Brand slug collision
If user proposes a slug that already exists, list the existing brands and ask: is this an addition to an existing one, or a new brand that needs a different slug?

### State file structure for a fresh brand
See `state-schema.md`. `state.py init <slug>` creates it correctly.
