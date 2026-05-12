# Tool stack reference

This is the canonical mapping of "what to generate" → "which tool to use." Every specialist skill should defer to this.

## Generation gateway: Higgsfield CLI

All image and video generation flows through the `higgsfield` CLI. Real surface:

- **Command shape:** `higgsfield generate create <model_id> --prompt "..." [--aspect_ratio X:Y] [--duration N] [--image <path-or-id>] [--soul-id <ref>] --wait`
- Flags are **snake_case** (`--aspect_ratio`, not `--aspect`).
- The CLI does NOT take `--output`. It returns a JSON job; the wrapper in `cmo-agency/scripts/lib/hf.sh` parses the result URL and downloads it.
- Auth check: `higgsfield account status`. Login: `higgsfield auth login`.

### Real model IDs

| Output | Higgsfield model_id | Notes |
|---|---|---|
| Logo (wordmark + iconography) | `gpt_image_2` | Best at brand text + clean composition. `nano_banana_pro` for pure iconography. |
| Color palette swatches (with HEX labels) | `gpt_image_2` | HEX labels must be legible — gpt_image_2 wins on small text. |
| Typography sample (px/pt labels) | `gpt_image_2` | Best multi-size text rendering. |
| Brand book infographic (1-page summary) | `gpt_image_2` | Dense text + layout. |
| Ad with copy (headline + sub + CTA) | `gpt_image_2` | Use `nano_banana_pro` only if it's headline-only. |
| Standalone infographic | `gpt_image_2` | Text density. |
| IG carousel slide (text-heavy) | `gpt_image_2` | Text legibility. |
| IG post (visual-heavy) | `nano_banana_pro` | Visual quality. Use `text2image_soul_v2` + brand-style Soul for max consistency. |
| Reel / TikTok video (default) | `seedance_2_0` | SOTA multi-shot, image-to-video, 4-15s. |
| Reel / TikTok video (cinematic single-plane, cheaper) | `kling3_0` | |
| UGC video (generic) | `seedance_2_0` | |
| UGC video with brand presenter Soul | `soul_cinematic` + `--soul-id <ugc-presenter-ref>` | |
| UGC product photo / packshot | `higgsfield product-photoshoot create --mode <m>` | Bundled subcommand with specialized prompt enhancer. Use `higgsfield-product-photoshoot` via subagent for rich briefs. |
| Marketplace listing card | `higgsfield marketplace-cards create --scope ...` | Use `higgsfield-marketplace-cards` skill. |
| Branded ad video with avatar + product | Marketing Studio (`marketing_studio_video`) | Use `higgsfield-generate` (Marketing Studio workflow). |
| Video virality analysis | `brain_activity` | Returns text report, not media. |

### Two Souls per brand (optional but recommended)

Brand-grade consistency is achieved via two optional Higgsfield Soul references — both registered in `.state.json` via `state.py asset <slug> <key> <ref-id>`:

| Soul | Key in state | Trained from | Used for |
|---|---|---|---|
| Brand-style Soul | `soul_brand_style_id` | logo final + 4-5 hero frames of brand art direction | Posts, ads, hero banners, on-brand visuals. Plug into `text2image_soul_v2` or `soul_cinematic`. |
| UGC-presenter Soul | `soul_ugc_presenter_id` | 5+ photos of the brand's presenter | UGC videos with consistent face. |

Creation requires **minimum 5 reference images** (Higgsfield's `--soul-2`). Delegate training to the `higgsfield-soul-id` bundled skill via subagent.

### Delegation map — CMO specialist → Higgsfield bundled skill

| In CMO specialist | Direct script | Delegate to bundled skill |
|---|---|---|
| `brand-identity-visual` (palette/typo/logo) | scripts/*.sh | After logo lock: subagent → `higgsfield-soul-id` to train brand-style Soul |
| `brand-book-publisher` infographic | scripts/build_infographic.sh | — |
| `social-content-creator` | scripts/*.sh | — |
| `ad-infographic-creator` | scripts/*.sh | — |
| `ugc-creator` video (generic UGC) | scripts/generate_ugc_video.sh | — |
| `ugc-creator` video (Marketing Studio ad with avatar+product) | — | subagent → `higgsfield-generate` (Marketing Studio workflow) |
| `ugc-creator` photo (simple brief) | scripts/generate_ugc_photo.sh | — |
| `ugc-creator` photo (rich brief: multi-image refs, brand context, modes catalog) | — | subagent → `higgsfield-product-photoshoot` |
| Marketplace listing cards | — | subagent → `higgsfield-marketplace-cards` |

## Layout & export tools

| Need | Tool | Notes |
|---|---|---|
| Brand book editorial layout | `anthropic-skills:canvas-design` | Agency-quality static design. Outputs PNG and PDF directly. |
| Brand book PDF post-processing | `anthropic-skills:pdf` | Merge, add metadata, encrypt, combine PDF + infographic into one file if desired. |
| Markdown ingestion (parsing pitch decks, briefs) | Built-in Read tool | No special skill needed. |

## Authoring

| Need | Tool |
|---|---|
| Create or iterate a skill in this suite | `anthropic-skills:skill-creator` |

## Failure modes

- **Higgsfield not installed**: preflight catches this. Don't try to fall back to direct OpenAI/Gemini calls — that's a different auth surface and the user explicitly chose Higgsfield as the single gateway.
- **`canvas-design` unavailable**: brand book layout cannot be built. Fail loudly. The user can install it via the skill marketplace.
- **`pdf` unavailable**: only matters for post-processing. Without it, `canvas-design`'s PDF output is still usable as-is.
