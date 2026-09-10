#!/usr/bin/env python3
"""Write wireframes/board-index.json — one record per board, so a board is read once.

**Every count in this session was recomputed from scratch by parsing 165 HTML files**, and three
of them came out wrong the first time: frame anchors confused with mentions (1,091 instead of
304), the P08 assembly routing missed entirely, and `Marketing Board 1.dc.html` reported as never
built when it was sitting in `wireframes/`. **A number that is expensive to derive gets derived
carelessly**, so this derives them once and records them.

Each record carries a `sha256`. A board whose hash has not changed does not need re-reading, which
is what makes the next audit cheap and what stops the counts drifting between two people who both
"just checked".

## Provenance is the field that matters

Five classes, and they are not interchangeable:

  `generated`     — `derive-wireframes.py` writes it from `screens/P*.yaml`. Rewritten on refresh.
  `workshop`      — `derive-pack-boards.py` writes it, one per workshop board of ten.
  `clientPack`    — the client drew it. **Never touched**, and the only class that is evidence of
                    a design decision rather than a restatement of the package.
  `claudeDesign`  — Claude Design's own board set, `wireframes/claude-design/`.
  `unrecognised`  — this package cannot account for it. Usually a rename's leftover.

**Coverage is not a board's stamps.** Ten client-pack frames are real drawings at a real anchor
carrying no `data-screen-id` at all, and eighteen frames are claimed by two screens each. So a
screen counts as drawn when a board stamps it, *or* when its own `wireframe.board` names an anchor
that board really has — and where two screens claim one frame, **the frame's title decides**, which
settles all eighteen. The drawing is the evidence; the stamp is an assertion about it.

**A frame in a `generated` board is not a drawn screen.** It is the screen's own YAML rendered as
boxes, which is why `wireframe.board` resolving for all 1,091 screens says nothing about design
coverage. Only `clientPack` and `claudeDesign` frames are drawings.

Run: python3 tools/index-boards.py
"""
import hashlib
import html
import json
import re
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
WIRE = ROOT / "wireframes"
OUT = WIRE / "board-index.json"

# **A frame carries three attributes and only one of them is the screen id.** The boards render
# `<div id="pos-2f" data-screen-label="POS-2F" data-screen-id="POS-007">`, where `id` is a
# lowercase label slug and the screen id is in `data-screen-id`. Matching `id="..."` alone worked
# only because `data-screen-id="POS-007"` contains that substring -- an accident, and one that
# would have broken silently the first time a board quoted the attribute differently. Named
# explicitly now, and it changes no count today: both forms match the same 2,098 frames.
ANCHOR = re.compile(r'''(?:data-screen-id|id)\s*=\s*["']([A-Za-z]{2,4}-\d{2,4})["']''')
# Every `id` in the file, screen-shaped or not, so a `wireframe.board` claim can be checked
# against the anchor it names rather than believed.
SLUG = re.compile(r'''\bid\s*=\s*["']([A-Za-z][A-Za-z0-9-]{1,40})["']''')
PLATFORM_BOARD = re.compile(r"^P\d\d ")
WORKSHOP_BOARD = re.compile(r"^WS\d\d ")

# **`generated` means `derive-wireframes.py` wrote it, and that deriver writes exactly two shapes**:
# `<code> <shortName>.dc.html` per platform, and the index `TICVAI Wireframe Boards.dc.html`.
# Claiming every filename starting with `TICVAI` was a guess at the naming rather than a reading of
# the tool, and it swept up three files the deriver has never written -- one of which,
# `TICVAI Boards v2.dc.html`, holds hand-drawn frames. **A drawn screen was being counted undrawn
# because of a prefix match on a filename.**
GENERATED_INDEX = "TICVAI Wireframe Boards.dc.html"


def screen_ids() -> dict:
    out = {}
    for f in sorted((ROOT / "screens").glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        for s in doc["screens"]:
            out[s["id"]] = doc["platform"]["code"]
    return out


def screen_names() -> dict:
    out = {}
    for f in sorted((ROOT / "screens").glob("P*.yaml")):
        for s in yaml.safe_load(f.read_text(encoding="utf-8"))["screens"]:
            out[s["id"]] = s.get("name", "")
    return out


def norm(s) -> str:
    """Compare a frame title to a screen name without tripping on typography.

    HTML-escaped ampersands and spacing around a slash are not differences: the frame reads
    *Order Routing & KDS / Printer Rules* and the screen is named `Order Routing & KDS/Printer
    Rules`. **Without this the last of the eighteen contested frames stays unresolved on a space.**
    """
    s = html.unescape(s or "").replace("/", " / ")
    return " ".join(s.split()).lower()


# The frame's heading, which is the only part of a board that says what was drawn.
FRAME_TITLE = re.compile(r'font-weight:800;letter-spacing:-\.015em">([^<]+)<')


def frame_title(path: Path, anchor: str) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    i = text.find('id="%s"' % anchor)
    if i < 0:
        return ""
    m = FRAME_TITLE.search(text[i:i + 900])
    return norm(m.group(1)) if m else ""


def classify(path: Path) -> str:
    if path.parent.name == "claude-design":
        return "claudeDesign"
    if WORKSHOP_BOARD.match(path.name):
        return "workshop"
    if PLATFORM_BOARD.match(path.name) or path.name == GENERATED_INDEX:
        return "generated"
    # An index or aggregate this package did not write and cannot attribute. **Not `clientPack`** --
    # that class is evidence the client drew something, and guessing a board into it would inflate
    # the only coverage number that means anything.
    # `TICVAI Boards v2.dc.html` reads as a client board and not an index: its frames carry
    # titles and `data-screen-id` stamps in the same convention as the pack boards, and Claude
    # Design's own pack-frame map counts them. The two remaining `TICVAI*` files frame nothing.
    if path.name == "TICVAI Boards v2.dc.html":
        return "clientPack"
    if path.name.startswith("TICVAI"):
        return "unrecognised"
    return "clientPack"


def main() -> int:
    screens = screen_ids()
    prior = {}
    if OUT.exists():
        prior = {b["file"]: b for b in json.loads(OUT.read_text(encoding="utf-8"))["boards"]}

    boards, reused = [], 0
    for f in sorted(WIRE.rglob("*.dc.html")):
        rel = f.relative_to(WIRE).as_posix()
        raw = f.read_bytes()
        sha = hashlib.sha256(raw).hexdigest()[:16]
        was = prior.get(rel)
        if was and was.get("sha256") == sha:
            # **Unchanged boards are not re-parsed.** This is the whole point of the index -- but
            # only the *parse* is cached, never the classification. Provenance is a function of
            # this tool's rules, not of the board's bytes, so a cached class survives a fix to
            # `classify()` and the run reports success having changed nothing. That is how the
            # `TICVAI Boards v2` misclassification outlived its own correction on the first
            # attempt: 170 boards "unchanged", 170 classes stale.
            was["lastSeen"] = date.today().isoformat()
            was["provenance"] = classify(f)
            boards.append(was)
            reused += 1
            continue
        text = raw.decode("utf-8", errors="replace")
        anchors = {a.upper() for a in ANCHOR.findall(text)}
        # **Every anchor in the file, not only the ones carrying a screen id.** Ten frames on
        # client packs are real drawings at a real anchor and carry no `data-screen-id` at all --
        # `Seat Board 2.dc.html#seat-2a` is `BO-015`, and the board never says so. Counting stamps
        # alone called all ten undrawn. The screen's own `wireframe.board` names them, and this set
        # is what lets that claim be *verified* rather than trusted.
        slugs = {a.lower() for a in SLUG.findall(text)}
        mine = sorted(a for a in anchors if a in screens)
        boards.append({
            "file": rel,
            "provenance": classify(f),
            "bytes": len(raw),
            "sha256": sha,
            "frames": len(anchors),
            "screensFramed": len(mine),
            "screens": mine,
            "orphanFrames": sorted(a for a in anchors if a not in screens),
            "anchors": sorted(slugs),
            "platforms": sorted({screens[a] for a in mine}),
            "firstIndexed": (was or {}).get("firstIndexed", date.today().isoformat()),
            "lastSeen": date.today().isoformat(),
        })

    drawn_by = {}
    for cls in ("clientPack", "claudeDesign", "workshop", "generated"):
        covered = set()
        for b in boards:
            if b["provenance"] == cls:
                covered |= set(b["screens"])
        drawn_by[cls] = sorted(covered)

    # **A frame can be a drawing and say nothing about whose it is.** Ten client-pack frames carry
    # a real anchor, a real title and no `data-screen-id` -- `Seat Board 2.dc.html#seat-2a` is
    # `BO-015` and the board never says so. Counting stamps called all ten undrawn; trusting the
    # screen's `wireframe.board` outright would count a claim nobody checked. **So the claim is
    # honoured only where the board really has that anchor**, which is stronger than either side
    # on its own and is what reconciled 111 against Claude Design's 123.
    by_file = {b["file"]: b for b in boards}
    names = screen_names()
    declared = {"clientPack": set(), "claudeDesign": set()}
    unverified, per_frame = [], {}
    for f in sorted((ROOT / "screens").glob("P*.yaml")):
        for s in yaml.safe_load(f.read_text(encoding="utf-8"))["screens"]:
            claims = [(s.get("wireframe") or {}).get("board")] + list(s.get("boardFrames") or [])
            for claim in [c for c in claims if c and "#" in c]:
                ref, anchor = claim.rsplit("#", 1)
                rec = by_file.get(ref.split("wireframes/")[-1])
                if not rec or rec["provenance"] not in declared:
                    continue
                if anchor.lower() in set(rec.get("anchors") or []):
                    per_frame.setdefault((rec["file"], anchor.lower()), set()).add(s["id"])
                else:
                    unverified.append((s["id"], claim))

    # **Eighteen frames are claimed by two screens each, and a frame drawn once depicts one
    # screen.** Counting both inflates coverage by 22; dropping both hides real drawings. **The
    # frame's own title settles every one of the eighteen** — `fnb-4a` is titled *Restaurant
    # Service Command Center*, which is `EMP-051`, while the frame is stamped `EMP-058`. The
    # drawing is the evidence and the stamp is the assertion, so the drawing wins.
    contested = []
    for (bf, anchor), ids in sorted(per_frame.items()):
        prov = by_file[bf]["provenance"]
        if len(ids) == 1:
            declared[prov] |= ids
            continue
        title = frame_title(WIRE / bf, anchor)
        win = [i for i in sorted(ids) if norm(names.get(i)) == title]
        contested.append({"frame": f"{bf}#{anchor}", "title": title,
                          "claimants": sorted(ids), "resolvedTo": win[0] if len(win) == 1 else None})
        # An unresolved frame counts for nobody. **A tie broken by sort order is a number that
        # cannot be defended**, and there is exactly one, which is cheaper to carry than to guess.
        declared[prov] |= set(win) if len(win) == 1 else set()

    designed = set(drawn_by["claudeDesign"]) | declared["claudeDesign"]
    client = set(drawn_by["clientPack"]) | declared["clientPack"]
    doc = {
        "generatedBy": "tools/index-boards.py",
        "generated": date.today().isoformat(),
        "note": ("One record per board file under `wireframes/`, keyed by content hash so an "
                 "unchanged board is never re-read. **A frame in a `generated` board is the "
                 "screen's own YAML rendered as boxes, not a drawing** — only `clientPack` and "
                 "`claudeDesign` frames are evidence that somebody designed something."),
        "counts": {
            "boards": len(boards),
            "boardsByProvenance": {c: sum(1 for b in boards if b["provenance"] == c)
                                   for c in ("generated", "workshop", "clientPack",
                                             "claudeDesign", "unrecognised")},
            "packageScreens": len(screens),
            "screensDrawnByClaudeDesign": len(designed),
            "screensOnClientPacks": len(client),
            "screensDrawnByEither": len(designed | client),
            "screensWithNoDrawnFrame": len(set(screens) - designed - client),
        },
        # **The set, not just the count.** `list-undrawn.py` recomputed coverage from stamps and
        # reported 696 undrawn against this file's own 682 — two artefacts disagreeing because one
        # re-derived what the other had already adjudicated. Consumers read this.
        "screensDrawn": sorted(designed | client),
        "screensDrawnByClaudeDesign": sorted(designed),
        "unverifiedClaims": [{"screen": a, "claim": b} for a, b in sorted(unverified)],
        "contestedFrames": contested,
        "boards": boards,
    }
    OUT.write_text(json.dumps(doc, indent=1), encoding="utf-8")
    c = doc["counts"]
    print(f"  {c['boards']} boards indexed ({reused} unchanged, re-used from the last run)")
    print(f"    by provenance: {c['boardsByProvenance']}")
    print(f"  screens drawn by Claude Design : {c['screensDrawnByClaudeDesign']}")
    print(f"  screens on client packs        : {c['screensOnClientPacks']}")
    print(f"  drawn by either                : {c['screensDrawnByEither']} of {c['packageScreens']}")
    print(f"  no drawn frame anywhere        : {c['screensWithNoDrawnFrame']}")
    if unverified:
        print(f"  claims naming a missing anchor : {len(unverified)}")
    if contested:
        un = sum(1 for c in contested if not c["resolvedTo"])
        print(f"  frames claimed by two screens  : {len(contested)} "
              f"({len(contested) - un} settled by frame title, {un} unresolved)")
    print(f"  -> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
