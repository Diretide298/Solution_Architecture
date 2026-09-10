#!/usr/bin/env python3
"""Write `wireframes/undrawn.json` — the screens no person has drawn, in the order to draw them.

**682 of 1,091 screens have no drawn frame, and that number is useless as a work item.** It is too
large to schedule, and it hides the fact that most of it is Wave 3. Grouped by wave it becomes
tractable: **89 screens are Wave 1 or 2**, which is a fortnight rather than a quarter.

`board-index.json` decides what *drawn* means and this file only re-groups it, so the two can never
disagree. **A frame in a `generated` board is not a drawing** — it is the screen's own YAML rendered
as boxes — so only `clientPack` and `claudeDesign` frames count here, which is why all 1,091 screens
having a `wireframe.board` says nothing about design coverage.

Run: python3 tools/list-undrawn.py
"""
import json
import sys
from urllib.parse import unquote
from collections import Counter
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "wireframes" / "board-index.json"
OUT = ROOT / "wireframes" / "undrawn.json"

# The two classes that are evidence somebody designed something. See `index-boards.py`.
DRAWN_BY = ("clientPack", "claudeDesign")


# `p08-data.js` is Claude Design's assembly map: every P08 screen carries a `route` naming the
# frame a builder would work from, and a `bp` pattern id.
P08_DATA = ROOT / "wireframes" / "claude-design" / "p08-data.js"


def pattern_routes(idx) -> dict:
    """Screen -> the pattern frame it routes to, and whether that frame is itself drawn.

    **Routing is not drawing, and Chinmay decided so on 9 September**: a screen that points at
    somebody else's frame has not been designed, it has been assigned a precedent. So these
    screens stay in the undrawn list and the routing is recorded beside them rather than counted.

    **The distinction is the whole value of the field.** A screen routed to a drawn pattern frame
    is a morning's work against a worked example; one routed to a pattern nobody has drawn is a
    blank page. Reporting a single P08 number hides which of the two a screen is.
    """
    if not P08_DATA.exists():
        return {}
    text = P08_DATA.read_text(encoding="utf-8")
    try:
        data = json.loads(text[text.index("{"):text.rindex("}") + 1])
    except ValueError:
        return {}
    anchors = {b["file"]: set(b.get("anchors") or []) for b in idx["boards"]}
    drawn_files = {b["file"] for b in idx["boards"] if b["provenance"] in DRAWN_BY}
    out = {}
    for s in data.get("screens", []):
        r = s.get("route") or {}
        if not r.get("file"):
            continue
        board = unquote(r["file"])
        # The boards live under `claude-design/`; the route names them bare.
        hit = next((f for f in anchors if f.endswith(board)), None)
        out[s["id"]] = {
            "patternFrame": f"{board}#{r.get('anchor')}" if r.get("anchor") else board,
            "pattern": r.get("bp"),
            "routesToOwnFrame": bool(r.get("self")),
            # **Drawn means the frame it points at exists on a board a person drew.**
            "patternFrameDrawn": bool(hit and hit in drawn_files
                                      and (r.get("anchor") or "").lower() in anchors[hit]),
        }
    return out


def main() -> int:
    if not INDEX.exists():
        print("  no wireframes/board-index.json — run tools/index-boards.py first")
        return 1
    idx = json.loads(INDEX.read_text(encoding="utf-8"))
    # **Read the adjudicated set; do not re-derive it.** Coverage is not a board's stamps alone —
    # ten client-pack frames carry no stamp at all, and eighteen frames are claimed by two screens
    # and settled by the frame's own title. Recomputing that here from `boards[].screens` reported
    # 696 undrawn against the index's 682, which is two artefacts disagreeing about a number one
    # of them had already worked out.
    drawn = set(idx.get("screensDrawn") or [])
    if not drawn:
        for b in idx["boards"]:
            if b["provenance"] in DRAWN_BY:
                drawn |= set(b["screens"])
    routes = pattern_routes(idx)

    platforms, rows = [], []
    for f in sorted((ROOT / "screens").glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        p = doc["platform"]
        undrawn = [s for s in doc["screens"] if s["id"] not in drawn]
        platforms.append({
            "code": p["code"], "name": p["name"], "surface": p.get("surface"),
            "runtime": p.get("runtime"), "offlineCapable": bool(p.get("offlineCapable")),
            "screens": len(doc["screens"]), "drawn": len(doc["screens"]) - len(undrawn),
            "undrawn": len(undrawn),
            "undrawnByWave": dict(sorted(Counter(s.get("wave") for s in undrawn).items())),
        })
        for s in undrawn:
            rows.append({
                "id": s["id"], "platform": p["code"], "wave": s.get("wave"),
                "name": s.get("name", ""), "module": s.get("module", ""),
                "requiresModule": s.get("requiresModule"),
                "purpose": s.get("purpose", ""),
                "template": ((s.get("layout") or {}).get("template")),
                "operations": len(s.get("apis") or []),
                # **The two fields that make a screen expensive to draw.** An open question is a
                # thing to answer before drawing, not after; a screen with no `entryState` cannot
                # say what it arrives holding, which the frame has to show.
                "openQuestions": s.get("openQuestions") or [],
                "hasEntryState": bool(s.get("entryState")),
                **(routes.get(s["id"]) or {}),
            })

    rows.sort(key=lambda r: (r["wave"] or 9, r["platform"], r["id"]))
    doc = {
        "generatedBy": "tools/list-undrawn.py",
        "generated": date.today().isoformat(),
        "basedOn": {"boardIndex": idx.get("generated"), "packageScreens": idx["counts"]["packageScreens"]},
        "note": ("Screens with no `clientPack` or `claudeDesign` frame. **Wave is the schedule** — "
                 "the Wave 1 and 2 rows are the tranche worth starting; Wave 3 is most of the "
                 "total and none of the urgency."),
        "counts": {
            "undrawn": len(rows),
            "byWave": dict(sorted(Counter(r["wave"] for r in rows).items())),
            "wave1and2": sum(1 for r in rows if r["wave"] in (1, 2)),
            "withOpenQuestions": sum(1 for r in rows if r["openQuestions"]),
            "withoutEntryState": sum(1 for r in rows if not r["hasEntryState"]),
            # **Routing is not drawing** — decided 9 September. Recorded, never counted as drawn.
            "routedToADrawnPatternFrame": sum(1 for r in rows if r.get("patternFrameDrawn")),
            "noDrawingAndNoPattern": sum(1 for r in rows if not r.get("patternFrameDrawn")),
        },
        "platforms": platforms,
        "screens": rows,
    }
    OUT.write_text(json.dumps(doc, indent=1), encoding="utf-8")
    c = doc["counts"]
    print(f"  {c['undrawn']} undrawn · by wave {c['byWave']}")
    print(f"  Wave 1+2 (start here)          : {c['wave1and2']}")
    print(f"  carrying an open question      : {c['withOpenQuestions']}")
    print(f"  with no entryState declared    : {c['withoutEntryState']}")
    print(f"  routed to a drawn pattern frame: {c['routedToADrawnPatternFrame']}"
          f"  (undrawn, but with a worked example)")
    print(f"  no drawing and no pattern      : {c['noDrawingAndNoPattern']}")
    for p in platforms:
        if p["undrawn"]:
            print(f"    {p['code']}  {p['undrawn']:>4} undrawn of {p['screens']:>4}   {p['undrawnByWave']}")
    print(f"  -> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
