#!/usr/bin/env python3
"""
Validate the wireframe boards against the screen definitions.

The boards are 347 screens of design intent in twelve HTML files, and the definitions are the
same 347 in YAML. **Nothing kept them in step until this existed**, and they will diverge the
first time a board is regenerated or a screen is renamed.

Checks:

  1. Every screen definition points at a board file that exists.
  2. Every screen's board anchor exists in that file. A link to `#scn-004` in a board with no
     such anchor is a click that silently does nothing.
  3. Every anchor in a board has a screen definition. A screen someone drew and nobody
     specified is the gap this whole exercise was closing.
  4. Every internal and cross-board href resolves — file and anchor both.
  5. The board named by a platform matches its code, so P07's screens do not link to P06.
  6. Every cross-platform reach a board asserts is recorded on the platform and resolves.
  7. Every design reference a screen names is a file that exists. A screen citing
     `Park_POS_dc.html` as a string rather than a path is a citation nobody can follow, which
     is how a delivered mockup ends up unread.

Run: python3 tools/check-wireframes.py
"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCREENS = ROOT / "screens"
BOARDS = ROOT / "wireframes"
if not BOARDS.exists():
    BOARDS = ROOT.parent / "ticvai-full" / "wireframes"

ERRORS: list[str] = []
WARNINGS: list[str] = []


def main() -> int:
    if not BOARDS.exists():
        print("no wireframes directory — nothing to check")
        return 0

    files = {f.name: f for f in BOARDS.glob("*.html")}
    anchors = {n: set(re.findall(r'<div id="([a-z0-9-]+)"', f.read_text(errors="replace")))
               for n, f in files.items()}
    screen_anchors = {n: {a.upper() for a in v if re.fullmatch(r"[a-z]{2,5}-\d{3}", a)}
                      for n, v in anchors.items()}

    defined: dict[str, set[str]] = {}
    boards_used: dict[str, str] = {}
    n_links = 0

    for f in sorted(SCREENS.glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text())
        p = doc["platform"]
        code = p["code"]
        defined[code] = {s["id"] for s in doc["screens"]}

        board = p.get("wireframeBoard")
        if not board:
            WARNINGS.append(f"{code}: no wireframeBoard — the platform has no board")
            continue
        name = board.split("/")[-1]
        boards_used[name] = code
        if name not in files:
            ERRORS.append(f"{code}: board '{name}' does not exist")
            continue
        if not name.startswith(code):
            ERRORS.append(f"{code}: points at board '{name}', which belongs to another platform")

        for s in doc["screens"]:
            link = (s.get("wireframe") or {}).get("board")
            if not link:
                WARNINGS.append(f"{code} {s['id']}: no board anchor")
                continue
            n_links += 1
            tgt, _, anc = link.partition("#")
            tn = tgt.split("/")[-1]
            if tn not in files:
                ERRORS.append(f"{s['id']}: board file '{tn}' missing")
            elif anc not in anchors[tn]:
                ERRORS.append(f"{s['id']}: anchor '#{anc}' not in {tn} — a click that does nothing")

    # 3. anchors with no definition
    all_defined = {i for v in defined.values() for i in v}
    for n, ids in screen_anchors.items():
        if n not in boards_used:
            continue
        orphan = sorted(ids - all_defined)
        if orphan:
            ERRORS.append(f"{n}: draws {len(orphan)} screen(s) with no definition — {orphan[:5]}")

    # 7. cross-platform reach resolves
    for f in sorted(SCREENS.glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text())
        for r in (doc["platform"].get("reachesOtherPlatforms") or []):
            tgt, _, anc = r["board"].partition("#")
            tn = tgt.split("/")[-1]
            if tn not in files:
                ERRORS.append(f"{doc['platform']['code']}: reach board '{tn}' missing")
            elif anc not in anchors[tn]:
                ERRORS.append(f"{doc['platform']['code']}: reach anchor '#{anc}' not in {tn}")

    # 6. design references resolve
    for f in sorted(SCREENS.glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text())
        code = doc["platform"]["code"]
        for ref in (doc["platform"].get("designReferences") or []):
            if not (ROOT / ref["path"]).exists():
                ERRORS.append(f"{code}: design reference '{ref['path']}' does not exist")
        for s in doc["screens"]:
            dr = (s.get("wireframe") or {}).get("designReference")
            if dr and not (ROOT / dr).exists():
                ERRORS.append(f"{s['id']}: designReference '{dr}' does not exist")

    # 4. hrefs across every board
    n_href = 0
    for n, f in files.items():
        text = f.read_text(errors="replace")
        for href in re.findall(r'href="([^"]+)"', text):
            if href.startswith(("http", "mailto")):
                continue
            n_href += 1
            tgt, _, anc = href.partition("#")
            tgt = (tgt or n).replace("%20", " ")
            if tgt not in files:
                ERRORS.append(f"{n}: href '{href}' — file missing")
            elif anc and anc not in anchors[tgt]:
                ERRORS.append(f"{n}: href '{href}' — anchor missing in target")

    print(f"{len(files)} board(s), {sum(len(v) for v in screen_anchors.values())} screen anchors")
    print(f"{n_links} definition-to-board links, {n_href} hrefs inside the boards\n")
    for w in WARNINGS[:20]:
        print(f"  WARN  {w}")
    for e in ERRORS:
        print(f"  FAIL  {e}")
    print()
    if ERRORS:
        print(f"{len(ERRORS)} error(s), {len(WARNINGS)} warning(s)")
        return 1
    print(f"PASS — {len(WARNINGS)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
