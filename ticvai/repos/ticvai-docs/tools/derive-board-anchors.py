#!/usr/bin/env python3
"""Give every screen the board anchor its platform already declares.

**A screen with no `wireframe.board` is a card nothing can link to.** `check-wireframes` calls it
"no board anchor", and it is the same fault class as a broken link: the board renders the screen,
the screen does not know where it was rendered, and every index built from the screen layer loses
it.

**Why this is derived and not authored.** The anchor is `platform.wireframeBoard` plus the screen
id in lower case -- `wireframes/P04 Venue POS.dc.html#pos-025`. `derive-wireframes.py` renders
every screen with exactly that id, so there is nothing to decide. 1,229 of 1,234 screens had one
already; the five that did not were added to P04 by hand from the client-approved POS prototype on
10 September, and the tool that added them wrote no `wireframe` block at all.

**A pack anchor always wins.** A screen the client drew keeps its `boardFrames` link to the
client's own frame -- that is the point of the field. This only fills the generated-board anchor,
which is what `wireframe.board` has always meant, and only where it is missing. It never rewrites
one that exists, so a hand-edited anchor survives every run.

Idempotent by construction: a second run finds nothing to do.

    python3 tools/derive-board-anchors.py [--apply]
"""

from __future__ import annotations

import argparse
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]


def _utf8() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def main() -> int:
    _utf8()
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    filled, skipped = [], []
    for f in sorted((ROOT / "screens").glob("P*.yaml")):
        text = f.read_text(encoding="utf-8")
        doc = yaml.safe_load(text) or {}
        plat = doc.get("platform") or {}
        code = plat.get("code") or f.name.split("-")[0]
        board = plat.get("wireframeBoard")
        if not board:
            skipped.append((code, "the platform declares no wireframeBoard"))
            continue

        changed = False
        for sc in (doc.get("screens") or []):
            wf = sc.get("wireframe")
            if isinstance(wf, dict) and wf.get("board"):
                continue
            anchor = board + "#" + sc["id"].lower()
            if not isinstance(wf, dict):
                # **The block is absent, not merely incomplete.** `status` and `provenance` are
                # what every other screen carries, and a half-written block reads as a screen
                # somebody started drawing.
                sc["wireframe"] = {"status": "notStarted", "provenance": "generated",
                                   "board": anchor}
            else:
                wf["board"] = anchor
            filled.append((code, sc["id"], anchor))
            changed = True

        if changed and a.apply:
            f.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100),
                         encoding="utf-8")

    for code, sid, anchor in filled:
        print("  %-5s %-9s -> %s" % (code, sid, anchor))
    for code, why in skipped:
        print("  skip  %-5s %s" % (code, why))

    if not filled:
        print("nothing to do -- every screen already carries its board anchor")
        return 0
    print("\n%d screen(s) given a board anchor" % len(filled))
    if not a.apply:
        print("run with --apply to write")
    else:
        print("run tools/derive-wireframes.py so the boards agree, "
              "then tools/check-wireframes.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
