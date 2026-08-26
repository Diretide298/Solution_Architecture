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




def check_unmatched_boards(referenced: set) -> None:
    """**A board nobody references is a board nobody reviews.**

    `P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` were written from the first
    generation, carried one anchor per screen, and nothing in the package pointed at either.
    The Python suite passed because it only ever checked the other direction — a screen naming a
    board that does not exist — and the viewer was the thing that noticed.

    **The stem match fails too**: `p15 kitchen display.dc` is not `p15`, so a lenient fallback
    would not have saved it either.
    """
    for f in sorted(BOARDS.glob("*.dc.html")):
        rel = f"wireframes/{f.name}"
        if rel in referenced:
            continue
        if f.name.startswith("TICVAI"):      # the index and the client's own board index
            continue
        WARNINGS.append(f"{rel}: no screen and no platform references this board. Either a "
                        "platform declares it as wireframeBoard or it is stale — a board nobody "
                        "references is a board nobody reviews")

def main() -> int:
    referenced: set = set()
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
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        p = doc["platform"]
        code = p["code"]
        defined[code] = {s["id"] for s in doc["screens"]}
        for sc in doc["screens"]:
            b = str((sc.get("wireframe") or {}).get("board", "")).split("#")[0]
            if b:
                referenced.add(b)

        board = p.get("wireframeBoard")
        if not board:
            WARNINGS.append(f"{code}: no wireframeBoard — the platform has no board")
            continue
        name = board.split("/")[-1]
        referenced.add(board)
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
    # A board may draw a state of a screen as well as a screen. When five scanner outcomes became
    # states of one screen on 18 August, their drawings stayed correct — **an admitted flash and a
    # denial with a reason are different visuals** — and only their status changed from route to
    # state. `wireframe.stateBoards` records which anchor draws which state.
    state_drawn: set = set()
    for f in sorted(SCREENS.glob("P*.yaml")):
        for s in yaml.safe_load(f.read_text(encoding="utf-8"))["screens"]:
            for sb in ((s.get("wireframe") or {}).get("stateBoards") or []):
                anchor = str(sb.get("board", "")).split("#")[-1]
                if anchor:
                    state_drawn.add(anchor.upper())

    all_defined = {i for v in defined.values() for i in v} | state_drawn
    for n, ids in screen_anchors.items():
        if n not in boards_used:
            continue
        orphan = sorted(ids - all_defined)
        if orphan:
            ERRORS.append(f"{n}: draws {len(orphan)} screen(s) with no definition — {orphan[:5]}")

    # 7. cross-platform reach resolves
    for f in sorted(SCREENS.glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        for r in (doc["platform"].get("reachesOtherPlatforms") or []):
            tgt, _, anc = r["board"].partition("#")
            tn = tgt.split("/")[-1]
            if tn not in files:
                ERRORS.append(f"{doc['platform']['code']}: reach board '{tn}' missing")
            elif anc not in anchors[tn]:
                ERRORS.append(f"{doc['platform']['code']}: reach anchor '#{anc}' not in {tn}")

    # 6. design references resolve
    for f in sorted(SCREENS.glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
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
                # **A pack that names a board still to arrive is a delivery gap, not a defect.**
                # The Claude Design F&B pack links `TICVAI Boards v2`, `Inventory Board 1` and
                # `Retail Board 1` — three boards the client has not sent yet, and 27 dead links.
                # **A warning keeps them visible; an error would block the package on somebody
                # else's delivery schedule.**
                if any(k in str(href) for k in ("Boards%20v2", "Inventory%20Board", "Retail%20Board", "Boards v2", "Inventory Board", "Retail Board")):
                    WARNINGS.append(f"{n}: links '{href}' — a board still to arrive")
                else:
                    ERRORS.append(f"{n}: href '{href}' — file missing")
            elif anc and anc not in anchors[tgt]:
                ERRORS.append(f"{n}: href '{href}' — anchor missing in target")

    print(f"{len(files)} board(s), {sum(len(v) for v in screen_anchors.values())} screen anchors")
    print(f"{n_links} definition-to-board links, {n_href} hrefs inside the boards\n")
    # **A board nothing points at is invisible to every other check here.** They all start from a
    # screen and ask whether its board exists; none starts from a board and asks whether anything
    # wants it. `P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` each shipped with
    # exactly one anchor per screen, correctly generated, and **not one screen referenced either** —
    # the Python suite passed while the viewer flagged both.
    #
    # **The direction that catches omission is the one that starts from the artefact**, because
    # nothing about an unreferenced file announces itself.
    referenced = set()
    for _f in sorted(SCREENS.glob("P*.yaml")):
        _d = yaml.safe_load(_f.read_text(encoding="utf-8"))
        _pl = _d.get("platform") or {}
        if _pl.get("wireframeBoard"):
            referenced.add(_pl["wireframeBoard"].split("#")[0].split("/")[-1])
        for _s in _d.get("screens") or []:
            _b = (_s.get("wireframe") or {}).get("board")
            if _b:
                referenced.add(_b.split("#")[0].split("/")[-1])
    for _f in sorted(BOARDS.glob("*.dc.html")):
        if _f.name not in referenced and "Index" not in _f.name:
            WARNINGS.append(f"{_f.name}: on disk and nothing points at it. Either a screen "
                            "declares it or it should not ship")


    for w in WARNINGS[:20]:
        print(f"  WARN  {w}")
    for e in ERRORS:
        print(f"  FAIL  {e}")
    print()
    if ERRORS:
        print(f"{len(ERRORS)} error(s), {len(WARNINGS)} warning(s)")
        return 1
    print(f"PASS — {len(WARNINGS)} warning(s)")
    check_unmatched_boards(referenced)

    return 0


if __name__ == "__main__":
    sys.exit(main())
