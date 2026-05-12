# `.state.json` schema

Every brand under `/Users/erikgamboa/Documents/CMO/projects/<slug>/` has a `.state.json` that acts as the gate ledger. **Always read it through `scripts/state.py`** — never edit by hand.

## Schema (v1)

```json
{
  "version": 1,
  "slug": "ejemplo-marca",
  "name": "Ejemplo Marca",
  "created_at": "2026-05-11T14:00:00Z",
  "updated_at": "2026-05-11T14:30:00Z",
  "language": "es-LATAM",
  "track": "nuevo | existente_sin_docs | existente_con_docs",
  "gates": {
    "strategy":  { "done": false, "completed_at": null },
    "palette":   { "done": false, "completed_at": null },
    "typo":      { "done": false, "completed_at": null },
    "logo":      { "done": false, "completed_at": null },
    "brandbook": { "done": false, "completed_at": null }
  },
  "assets": {
    "logo_final":     null,
    "palette_image":  null,
    "typo_sample":    null,
    "brandbook_pdf":  null,
    "brandbook_infographic": null,
    "soul_id":        null
  }
}
```

## Gate order

Gates must be flipped in this order. Skipping ahead is forbidden:

1. `strategy` — set true by `brand-strategy-interview`
2. `palette` — set true by `brand-identity-visual` step A
3. `typo` — set true by `brand-identity-visual` step B
4. `logo` — set true by `brand-identity-visual` step C
5. `brandbook` — set true by `brand-book-publisher`

## Helper API (`scripts/state.py`)

```bash
# Initialize a new brand
python /Users/erikgamboa/Documents/CMO/.claude/skills/cmo-agency/scripts/state.py init <slug> [--name "Display Name"] [--track nuevo|existente_sin_docs|existente_con_docs]

# Read the current state
python /Users/erikgamboa/Documents/CMO/.claude/skills/cmo-agency/scripts/state.py get <slug>

# Mark a gate done
python /Users/erikgamboa/Documents/CMO/.claude/skills/cmo-agency/scripts/state.py done <slug> <gate>     # gate ∈ strategy|palette|typo|logo|brandbook

# Reopen a gate (for "redo the palette")
python /Users/erikgamboa/Documents/CMO/.claude/skills/cmo-agency/scripts/state.py reopen <slug> <gate>

# Record an asset path
python /Users/erikgamboa/Documents/CMO/.claude/skills/cmo-agency/scripts/state.py asset <slug> <key> <path>

# Find next pending gate
python /Users/erikgamboa/Documents/CMO/.claude/skills/cmo-agency/scripts/state.py next <slug>            # prints gate name or "ready"
```

## Recovery

If `state.json` is corrupt or unparseable, `state.py get` exits non-zero with a clear message. The orchestrator can offer the user (a) repair (fill missing gates with `false`) or (b) reset (`state.py init <slug> --force`).
