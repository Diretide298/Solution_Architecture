#!/usr/bin/env python3
"""Derive one wireframe board per workshop board from the screens the pack produced.

**SUPERSEDED 10 September 2026, and out of `refresh.sh`.** Drawing each pack screen twice —
once on its platform board, once here — meant a reviewer met two drawings of one screen with
no way to tell them apart from a near-duplicate nobody had merged. `derive-wireframes.py`
now puts the `WS##` code on the card as a badge and offers a filter that regroups a platform
board by workshop board, which is the only thing these files bought. The 74 files it wrote
are in `_dump/wireframes-workshop-boards-10-september/`.

**Kept runnable on purpose.** If the client asks for the separate files, this rebuilds them
exactly — but it also rewrites `wireframe.workshopBoard` on 728 screens, and nothing in the
package reads that field, so those pointers go stale in silence. Clear them if you run it
and then archive the output again.

**The 590 pack screens were rendered, and their boards were not.** `derive-wireframes.py` writes
one file per platform, so all 590 landed inside five platform boards grouped by module. That is
right for a team that owns a platform and wrong for the client, who specified this work as 59
boards of ten screens and will review it the same way. The board is the unit the workshop used,
and it survived on every screen as `source.pack` + `source.board` — so it can be rebuilt rather
than re-decided.

**Nothing here re-renders a screen.** `render_screen` is imported from `derive-wireframes.py`, so
a card on a workshop board and the same card on its platform board cannot drift: there is one
renderer and this tool only regroups what it emits.

**These are generated files and they are not client packs.** `wireframes/` already holds hand-drawn
boards that must never be written over, so these take a `WS##` prefix that says where they came
from, and `derive-wireframes.py` is taught the prefix so its manifest files them as generated
rather than as something it cannot account for.

Run: `python3 tools/derive-pack-boards.py [--apply]`
"""
from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SCREENS = ROOT / "screens"
WIRE = ROOT / "wireframes"
INDEX = "TICVAI Workshop Boards.dc.html"


def _load_deriver():
    """`derive-wireframes.py` is not an importable name, and copying it would be worse."""
    spec = importlib.util.spec_from_file_location("dw", ROOT / "tools" / "derive-wireframes.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


DW = _load_deriver()


def module_of(pack: str) -> str:
    """`Access Control Module_Reference.pdf` is the module the workshop called it."""
    stem = re.sub(r"\.pdf$", "", pack, flags=re.I)
    stem = re.sub(r"[_ ]*Reference$", "", stem, flags=re.I)
    stem = re.sub(r"[_ ]*Module$", "", stem, flags=re.I)
    return stem.replace("_", " ").strip() or pack


def collect() -> dict:
    """Every pack screen, keyed by the board the workshop put it on."""
    boards: dict = defaultdict(list)
    for f in sorted(SCREENS.glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        plat = doc["platform"]
        for s in doc["screens"]:
            src = s.get("source") or {}
            if not src.get("pack"):
                continue
            boards[(module_of(src["pack"]), int(src["board"]))].append((s, plat, f.name))
    return boards


def codes(boards: dict) -> dict:
    """`WS01`… in the order the workshop numbered them, so a code is stable across runs."""
    return {k: "WS%02d" % i for i, k in enumerate(sorted(boards), 1)}


def board_html(code: str, module: str, n: int, rows: list) -> str:
    plats = {p["code"]: p for _, p, _ in rows}
    dark = any(p["code"] in DW.DARK for p in plats.values())
    offline = any(bool(p.get("offlineCapable")) for p in plats.values())
    cards = []
    for s, plat, _ in rows:
        card = DW.render_screen(s, dark, offline, plat)
        # **The link back is the whole point of splitting them out.** A reviewer on a workshop
        # board has to be able to reach the platform that owns the screen, because that is where
        # the screen is built and where its neighbours are.
        home = (s.get("wireframe") or {}).get("board") or ""
        if home.startswith("wireframes/"):
            href = home[len("wireframes/"):].replace(" ", "%20")
            card += ('<div class="ws-home"><a href="%s">%s %s &rarr;</a></div>'
                     % (href, DW.esc(plat["code"]), DW.esc(plat["shortName"])))
        cards.append(card)

    owners = " · ".join("%s %s" % (p["code"], p["shortName"])
                        for p in sorted(plats.values(), key=lambda x: x["code"]))
    split = ("" if len(plats) == 1 else
             " <strong>This board is split across %d platforms.</strong> The workshop specified it"
             " as one board; the package places a screen on the platform that owns it, and these"
             " did not all land in the same place." % len(plats))
    extra_css = (
        ".ws-home{margin:-6px 0 18px;font:600 12px/1 'IBM Plex Mono',monospace}"
        ".ws-home a{color:#6B7280;text-decoration:none;border-bottom:1px solid #D1D5DB}"
        ".ws-home a:hover{color:#111827}")
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{code} {module} board {n} — workshop board</title>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&family=IBM+Plex+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>{css}
{extra}</style></head><body>
<div class="wrap">
  <a class="home" href="{index}">&larr; All workshop boards</a>
  <div class="head">
    <div><span class="mark">TICVAI</span>
      <h1>{code} · {module} <span style="font-weight:600;color:#6B7280">board {n} ({count} screens)</span></h1></div>
    <div class="meta">{owners}</div>
  </div>
  <p class="lede"><strong>A workshop board, as the client specified it</strong> — ten screens
  named in {module}. The cards are the ones the platform board renders; only the grouping
  differs, so the two cannot disagree.{split}</p>
  <div class="stack">{cards}</div>
  <div class="bottom">
    <span>Generated by tools/derive-pack-boards.py from screens/P*.yaml — do not hand-edit</span>
    <span>{code} · {count} screens</span>
  </div>
</div></body></html>""".format(
        code=DW.esc(code), module=DW.esc(module), n=n, css=DW.CSS, extra=extra_css,
        index=INDEX.replace(" ", "%20"), owners=DW.esc(owners), count=len(rows),
        split=split, cards="".join(cards))


def index_html(boards: dict, code_of: dict) -> str:
    by_mod: dict = defaultdict(list)
    for key in sorted(boards):
        by_mod[key[0]].append(key)
    secs = []
    for mod, keys in by_mod.items():
        items = []
        for k in keys:
            code = code_of[k]
            href = ("%s %s Board %d.dc.html" % (code, mod, k[1])).replace(" ", "%20")
            items.append('<li><a href="%s"><b>%s</b> board %d <span>%d screens</span></a></li>'
                         % (href, DW.esc(code), k[1], len(boards[k])))
        secs.append('<div class="grp">%s · %d boards</div><ul class="wsix">%s</ul>'
                    % (DW.esc(mod), len(keys), "".join(items)))
    total = sum(len(v) for v in boards.values())
    extra_css = (
        ".wsix{list-style:none;padding:0;margin:0 0 26px;display:grid;"
        "grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:8px}"
        ".wsix a{display:flex;justify-content:space-between;gap:10px;padding:11px 13px;"
        "border:1px solid #E5E7EB;border-radius:9px;text-decoration:none;color:#111827;"
        "font:600 13px/1.3 Manrope,sans-serif;background:#fff}"
        ".wsix a:hover{border-color:#9CA3AF}"
        ".wsix span{color:#6B7280;font:400 12px/1.3 'IBM Plex Mono',monospace}")
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>TICVAI — workshop boards</title>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&family=IBM+Plex+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>{css}
{extra}</style></head><body>
<div class="wrap">
  <a class="home" href="TICVAI%20Wireframe%20Boards.dc.html">&larr; Platform boards</a>
  <div class="head">
    <div><span class="mark">TICVAI</span>
      <h1>Workshop boards <span style="font-weight:600;color:#6B7280">({nboards} boards · {total} screens)</span></h1></div>
    <div class="meta">derived from sources/workshop/pack.json</div>
  </div>
  <p class="lede"><strong>The 59 boards the workshop specified, ten screens each.</strong> The
  platform boards remain the place a team builds from — a team owns a platform, and these screens
  are spread across five of them. <strong>This index is the client's view of the same work</strong>,
  and it exists because the board is the unit the pack was written in.</p>
  {secs}
  <div class="bottom">
    <span>Generated by tools/derive-pack-boards.py — do not hand-edit</span>
    <span>{nboards} boards · {total} screens</span>
  </div>
</div></body></html>""".format(css=DW.CSS, extra=extra_css, nboards=len(boards),
                               total=total, secs="".join(secs))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    DW._utf8_stdout()

    boards = collect()
    code_of = codes(boards)
    sizes = sorted({len(v) for v in boards.values()})
    split = [k for k, v in boards.items() if len({p["code"] for _, p, _ in v}) > 1]
    print("%d workshop boards · %d screens"
          % (len(boards), sum(len(v) for v in boards.values())))
    print("  screens per board          %s" % sizes)
    print("  boards split across plats  %d" % len(split))
    if not a.apply:
        print("\n  nothing written - pass --apply")
        return 0

    written = []
    for key, rows in sorted(boards.items()):
        mod, n = key
        name = "%s %s Board %d.dc.html" % (code_of[key], mod, n)
        (WIRE / name).write_text(board_html(code_of[key], mod, n, rows), encoding="utf-8")
        written.append(name)
    (WIRE / INDEX).write_text(index_html(boards, code_of), encoding="utf-8")
    print("  wrote %d board(s) + %s" % (len(written), INDEX))

    # **The screen says which workshop board it came from.** `wireframe.board` keeps pointing at
    # the platform board, because that is where the screen is built; this is a second surface, not
    # a replacement, and overwriting the first would break every link that already resolves.
    touched = 0
    for f in sorted(SCREENS.glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        hit = False
        for s in doc["screens"]:
            src = s.get("source") or {}
            if not src.get("pack"):
                continue
            key = (module_of(src["pack"]), int(src["board"]))
            ref = "wireframes/%s %s Board %d.dc.html#%s" % (
                code_of[key], key[0], key[1], s["id"].lower())
            if (s.get("wireframe") or {}).get("workshopBoard") != ref:
                s.setdefault("wireframe", {})["workshopBoard"] = ref
                hit = True
                touched += 1
        if hit:
            f.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100),
                         encoding="utf-8")
            print("  -> screens/%s" % f.name)
    print("  %d screen(s) linked to a workshop board" % touched)
    return 0


if __name__ == "__main__":
    sys.exit(main())
