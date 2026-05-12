#!/usr/bin/env python3
"""Brand state ledger for the CMO agency skill suite.

Reads and writes `/Users/erikgamboa/Documents/CMO/projects/<slug>/.state.json`.
Single source of truth for the sequential gates (strategy → palette → typo → logo → brandbook).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECTS_ROOT = Path("/Users/erikgamboa/Documents/CMO/projects")
# Sequential gates the agency enforces.
# `soul_brand_style` is OPTIONAL — it never blocks downstream gates.
# It exists so the state file can record that a brand-style Soul exists for
# this brand, which downstream skills then prefer when generating on-brand visuals.
GATE_ORDER = ["strategy", "palette", "typo", "logo", "brandbook"]
OPTIONAL_GATES = {"soul_brand_style"}
ALL_GATES = GATE_ORDER + list(OPTIONAL_GATES)
TRACKS = {"nuevo", "existente_sin_docs", "existente_con_docs"}
ASSET_KEYS = {
    "logo_final",
    "palette_image",
    "typo_sample",
    "brandbook_pdf",            # the SINGLE formal PDF — built by brand-book-publisher at the end
    "brandbook_infographic",
    "soul_brand_style_id",      # Higgsfield Soul reference id for brand-style consistency
    "soul_ugc_presenter_id",    # Higgsfield Soul reference id for UGC presenter (optional)
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _path(slug: str) -> Path:
    return PROJECTS_ROOT / slug / ".state.json"


def _fresh(slug: str, name: str | None, track: str | None) -> dict:
    return {
        "version": 2,
        "slug": slug,
        "name": name or slug,
        "created_at": _now(),
        "updated_at": _now(),
        "language": "es-LATAM",
        "track": track,
        "gates": {g: {"done": False, "completed_at": None} for g in ALL_GATES},
        "assets": {k: None for k in ASSET_KEYS},
    }


def _load(slug: str) -> dict:
    p = _path(slug)
    if not p.exists():
        print(f"error: no state file for brand '{slug}' (expected at {p})", file=sys.stderr)
        sys.exit(2)
    try:
        return json.loads(p.read_text())
    except json.JSONDecodeError as e:
        print(f"error: corrupt state file for '{slug}': {e}", file=sys.stderr)
        sys.exit(3)


def _save(slug: str, state: dict) -> None:
    state["updated_at"] = _now()
    p = _path(slug)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")


def _ensure_complete(state: dict) -> dict:
    """Fill in any missing gate / asset keys without resetting existing values."""
    state.setdefault("version", 2)
    state.setdefault("language", "es-LATAM")
    state.setdefault("track", None)
    gates = state.setdefault("gates", {})
    for g in ALL_GATES:
        gates.setdefault(g, {"done": False, "completed_at": None})
    # Migrate legacy asset name `soul_id` (v1) -> `soul_brand_style_id` (v2).
    assets = state.setdefault("assets", {})
    if "soul_id" in assets and "soul_brand_style_id" not in assets:
        assets["soul_brand_style_id"] = assets.pop("soul_id")
    for k in ASSET_KEYS:
        assets.setdefault(k, None)
    return state


def cmd_init(args: argparse.Namespace) -> None:
    p = _path(args.slug)
    if p.exists() and not args.force:
        print(f"error: state already exists for '{args.slug}'. Use --force to overwrite.", file=sys.stderr)
        sys.exit(1)
    if args.track and args.track not in TRACKS:
        print(f"error: track must be one of {sorted(TRACKS)}", file=sys.stderr)
        sys.exit(1)
    state = _fresh(args.slug, args.name, args.track)
    _save(args.slug, state)
    (PROJECTS_ROOT / args.slug / "assets" / "colors").mkdir(parents=True, exist_ok=True)
    (PROJECTS_ROOT / args.slug / "assets" / "typography").mkdir(parents=True, exist_ok=True)
    (PROJECTS_ROOT / args.slug / "assets" / "logo").mkdir(parents=True, exist_ok=True)
    (PROJECTS_ROOT / args.slug / "assets" / "social").mkdir(parents=True, exist_ok=True)
    (PROJECTS_ROOT / args.slug / "assets" / "ugc").mkdir(parents=True, exist_ok=True)
    (PROJECTS_ROOT / args.slug / "assets" / "ads").mkdir(parents=True, exist_ok=True)
    (PROJECTS_ROOT / args.slug / "ingest").mkdir(parents=True, exist_ok=True)
    print(json.dumps(state, indent=2, ensure_ascii=False))


def cmd_get(args: argparse.Namespace) -> None:
    state = _ensure_complete(_load(args.slug))
    print(json.dumps(state, indent=2, ensure_ascii=False))


def cmd_done(args: argparse.Namespace) -> None:
    if args.gate not in ALL_GATES:
        print(f"error: gate must be one of {ALL_GATES}", file=sys.stderr)
        sys.exit(1)
    state = _ensure_complete(_load(args.slug))
    # Sequential enforcement only applies to GATE_ORDER (the required sequence).
    # Optional gates (soul_brand_style, etc.) can be locked at any time, but in
    # practice the Soul depends on a final logo — the skill enforces that.
    if args.gate in GATE_ORDER:
        idx = GATE_ORDER.index(args.gate)
        for prior in GATE_ORDER[:idx]:
            if not state["gates"][prior]["done"]:
                print(
                    f"error: cannot mark '{args.gate}' done — earlier gate '{prior}' is not done yet.",
                    file=sys.stderr,
                )
                sys.exit(4)
    state["gates"][args.gate]["done"] = True
    state["gates"][args.gate]["completed_at"] = _now()
    _save(args.slug, state)
    print(f"ok: {args.gate} -> done")


def cmd_reopen(args: argparse.Namespace) -> None:
    if args.gate not in ALL_GATES:
        print(f"error: gate must be one of {ALL_GATES}", file=sys.stderr)
        sys.exit(1)
    state = _ensure_complete(_load(args.slug))
    state["gates"][args.gate]["done"] = False
    state["gates"][args.gate]["completed_at"] = None
    _save(args.slug, state)
    print(f"ok: {args.gate} reopened")


def cmd_asset(args: argparse.Namespace) -> None:
    if args.key not in ASSET_KEYS:
        print(f"error: asset key must be one of {sorted(ASSET_KEYS)}", file=sys.stderr)
        sys.exit(1)
    state = _ensure_complete(_load(args.slug))
    state["assets"][args.key] = args.path
    _save(args.slug, state)
    print(f"ok: assets.{args.key} = {args.path}")


def cmd_next(args: argparse.Namespace) -> None:
    state = _ensure_complete(_load(args.slug))
    for g in GATE_ORDER:
        if not state["gates"][g]["done"]:
            print(g)
            return
    print("ready")


def cmd_list(_args: argparse.Namespace) -> None:
    if not PROJECTS_ROOT.exists():
        return
    for p in sorted(PROJECTS_ROOT.iterdir()):
        if not p.is_dir():
            continue
        sf = p / ".state.json"
        if not sf.exists():
            continue
        try:
            s = json.loads(sf.read_text())
            pending = next(
                (g for g in GATE_ORDER if not s.get("gates", {}).get(g, {}).get("done")),
                "ready",
            )
            print(f"{s.get('slug', p.name)}\t{s.get('name', '')}\t{pending}")
        except json.JSONDecodeError:
            print(f"{p.name}\t(corrupt)\t-")


def main() -> None:
    parser = argparse.ArgumentParser(description="Brand state ledger for CMO agency")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="Create a new brand state file")
    p_init.add_argument("slug")
    p_init.add_argument("--name", default=None)
    p_init.add_argument("--track", default=None, choices=sorted(TRACKS))
    p_init.add_argument("--force", action="store_true")
    p_init.set_defaults(func=cmd_init)

    p_get = sub.add_parser("get", help="Print the state file")
    p_get.add_argument("slug")
    p_get.set_defaults(func=cmd_get)

    p_done = sub.add_parser("done", help="Mark a gate done (enforces order)")
    p_done.add_argument("slug")
    p_done.add_argument("gate")
    p_done.set_defaults(func=cmd_done)

    p_reopen = sub.add_parser("reopen", help="Reopen a previously completed gate")
    p_reopen.add_argument("slug")
    p_reopen.add_argument("gate")
    p_reopen.set_defaults(func=cmd_reopen)

    p_asset = sub.add_parser("asset", help="Record an asset path")
    p_asset.add_argument("slug")
    p_asset.add_argument("key")
    p_asset.add_argument("path")
    p_asset.set_defaults(func=cmd_asset)

    p_next = sub.add_parser("next", help="Print the next pending gate, or 'ready'")
    p_next.add_argument("slug")
    p_next.set_defaults(func=cmd_next)

    p_list = sub.add_parser("list", help="List all brands with their next pending gate")
    p_list.set_defaults(func=cmd_list)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
