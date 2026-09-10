#!/usr/bin/env python3
"""Link integrity across every layer — the audit that has been run by hand until now.

**Nine validators check each artefact against its own schema. None checks the joins between them**,
and every serious defect this package has had lived in a join: 22 guest screens calling staff
operations, 37 screens claiming offline behaviour their operations could not deliver, 185
relationship edges holding an operation name in a column field, an event three transitions emitted
and none declared.

**The pattern is always the same.** One artefact makes a claim, another holds the fact, and nothing
reads them against each other.

This reports **nine directions**. A non-zero count is a link a reader can follow into nothing.

    python3 tools/audit-links.py            # summary
    python3 tools/audit-links.py --detail   # every broken link, named

Exit code is 1 if any direction is non-zero.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def load_json(name: str) -> dict:
    p = ROOT / "handoff" / name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def screens() -> dict:
    """Every screen, with the platform that owns it."""
    out = {}
    for f in sorted((ROOT / "screens").glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        code = (doc.get("platform") or {}).get("code", "")
        for s in doc.get("screens") or []:
            out[s["id"]] = (code, s)
    return out


# Board file -> the archive directory holding it, filled by `board_anchors()`.
ARCHIVED: dict[str, str] = {}

# **A hazard is not a break, and neither is a record of something that has been put away.**
# Both resolve today; both would mislead somebody if they went unsaid.
ARCHIVE_OK = {"anchor collision", "archived board frame"}


def board_anchors() -> dict:
    """Anchors per board file.

    **Case- and element-agnostic on purpose.** The Kiosk pack anchors on `KSK-001` in uppercase and
    the earlier pattern matched `<div id="[a-z0-9-]+"` only — nine correct frames read as broken
    links, which sends somebody to fix a good file.
    """
    out = {}
    for f in (ROOT / "wireframes").glob("*.dc.html"):
        txt = f.read_text(encoding="utf-8", errors="replace")
        out[f.name] = set(re.findall(r'(?<![-\w])id="([A-Za-z0-9_-]+)"', txt))
    # **An archived board is not a missing board.** 67 Claude Design boards were moved to
    # `_dump/` on 9 September because they are being redrawn, and the 217 `boardFrames` entries
    # recording which frame drew which screen went on pointing at them. Those entries are *true*
    # — that frame did draw that screen, and the file is still openable — so calling them broken
    # sends somebody to fix a correct record. They are reported separately instead.
    for d in sorted((ROOT / "_dump").glob("wireframes-*")):
        for f in d.glob("*.html"):
            if f.name in out:
                continue
            txt = f.read_text(encoding="utf-8", errors="replace")
            out[f.name] = set(re.findall(r'(?<![-\w])id="([A-Za-z0-9_-]+)"', txt))
            ARCHIVED[f.name] = d.name
    return out


def audit(detail: bool = False) -> dict:
    lin = load_json("api-data-lineage.json")
    sch = load_json("schema-reference.json")
    real = {t for t in (set(sch.get("cols") or {}) | set(sch.get("storage") or {}))
            if "." in t and ":" not in t}
    scr = screens()
    anchors = board_anchors()

    broken: dict[str, list] = {k: [] for k in (
        "screen -> operation", "screen -> screen", "screen -> board anchor",
        "flow -> screen", "flow -> operation", "state -> operation",
        "operation -> table", "diagram -> diagram", "operation audience",
        "anchor collision", "archived board frame",
    )}

    for sid, (code, s) in scr.items():
        for a in (s.get("apis") or []):
            oid = a.get("operationId")
            if oid and oid not in lin:
                broken["screen -> operation"].append(f"{sid} calls {oid}")
        for t in ((s.get("navigation") or {}).get("exitTo") or []):
            if t not in scr:
                broken["screen -> screen"].append(f"{sid} exits to {t}")
        # **A board pointer is two claims: the file, and the anchor inside it.** A link to an
        # anchor a board does not carry is a click that silently does nothing, which is worse than
        # no link — the reader believes they have seen the design.
        b = (s.get("wireframe") or {}).get("board")
        if b and "#" in b:
            fn, _, anc = b.partition("#")
            fn = os.path.basename(fn)
            if fn in ARCHIVED:
                broken["archived board frame"].append(f"{sid} -> {fn} (in {ARCHIVED[fn]})")
            elif fn not in anchors:
                broken["screen -> board anchor"].append(f"{sid} -> {fn} (no such board)")
            elif anc not in anchors[fn]:
                broken["screen -> board anchor"].append(f"{sid} -> {fn}#{anc} (no such anchor)")
        # **`boardFrames` is qualified from 31 August: `Board.dc.html#anchor`.** A bare anchor was
        # ambiguous because Claude Design adopted our screen ids as their frame ids — `adm-002` is
        # a frame on `P09 TICVAI Web` *and* on `Dashboards Board`, and 22 anchors collide that way.
        #
        # **The anchor addresses a frame in a document; the screen id names what it draws.** Those
        # are two jobs, and collapsing them worked until two boards drew the same screen.
        for fr in (s.get("boardFrames") or []):
            if "#" in fr:
                bn, _, an = fr.partition("#")
                if bn in ARCHIVED:
                    broken["archived board frame"].append(f"{sid} claims {fr} (in {ARCHIVED[bn]})")
                elif bn not in anchors:
                    broken["screen -> board anchor"].append(f"{sid} claims {fr} (no such board)")
                elif an not in anchors[bn]:
                    broken["screen -> board anchor"].append(f"{sid} claims {fr} (no such anchor)")
            elif not any(fr in v for v in anchors.values()):
                broken["screen -> board anchor"].append(f"{sid} claims frame {fr}")
            else:
                broken["screen -> board anchor"].append(
                    f"{sid} claims bare frame {fr} — qualify it as Board.dc.html#{fr}")

    for f in sorted((ROOT / "flows").glob("F*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        for st in (doc.get("steps") or []):
            if st.get("screen") and st["screen"] not in scr:
                broken["flow -> screen"].append(f"{doc.get('id')} step {st.get('step')} "
                                                f"-> {st['screen']}")
            for o in (st.get("operations") or []):
                if o not in lin:
                    broken["flow -> operation"].append(f"{doc.get('id')} -> {o}")

    for f in sorted((ROOT / "states").glob("*.yaml")):
        if f.stem.startswith("_"):
            continue
        doc = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        for tr in (doc.get("transitions") or []):
            o = tr.get("operation")
            if o and o not in lin:
                broken["state -> operation"].append(f"{f.stem} {tr.get('from')}->{tr.get('to')} "
                                                    f"names {o}")

    for o, v in lin.items():
        for t in v.get("reads", []) + v.get("writes", []):
            if "." in t and ":" not in t and t not in real:
                broken["operation -> table"].append(f"{o} -> {t}")
        if not v.get("audience"):
            broken["operation audience"].append(o)

    # **An anchor that appears on two boards no longer identifies a frame.** Claude Design adopted
    # our screen ids as their frame ids — well-intentioned, and it made Kiosk and Dashboards the
    # only packs that linked in one pass — but `ksk-001` now exists on `P05 Guest Kiosk` (ours,
    # generated) and on `Kiosk Board 1` (theirs), so a bare reference has two answers.
    #
    # **Reported rather than fixed.** The convention is worth keeping and the reference is what
    # needed qualifying, which is why `boardFrames` now carries the board.
    _seen: dict = {}
    for bn, ids in anchors.items():
        # **A collision needs two boards a reader could actually land on.** Archived boards are
        # indexed so their `boardFrames` records resolve, not so they can argue with live ones —
        # counting them turned 728 collisions into 1,049 without a single new hazard.
        if "Index" in bn or bn in ARCHIVED:
            continue
        for a in ids:
            if re.match(r"^[A-Za-z]{2,6}-\d", a):
                _seen.setdefault(a.lower(), []).append(bn)
    for a, boards in sorted(_seen.items()):
        if len(boards) > 1:
            broken["anchor collision"].append(f"{a} on {', '.join(sorted(boards))}")

    for f in (ROOT / "diagrams").rglob("*.yaml"):
        for m in re.finditer(r"(?:ref|index): (diagrams/[\w/.-]+)", f.read_text(encoding="utf-8")):
            if not (ROOT / m.group(1)).exists():
                broken["diagram -> diagram"].append(f"{f.name} -> {m.group(1)}")

    if detail:
        for k, v in broken.items():
            if v:
                print(f"\n{k} — {len(v)}")
                for x in v[:40]:
                    print(f"    {x}")
                if len(v) > 40:
                    print(f"    ... and {len(v) - 40} more")

    return {k: len(v) for k, v in broken.items()}


def coverage() -> dict:
    """Not integrity — reach. **A link that resolves is not the same as a link that exists.**"""
    lin = load_json("api-data-lineage.json")
    scr = screens()
    on_screen = {a.get("operationId") for _, s in scr.values() for a in (s.get("apis") or [])}
    in_flow = set()
    for f in (ROOT / "flows").glob("F*.yaml"):
        for st in ((yaml.safe_load(f.read_text(encoding="utf-8")) or {}).get("steps") or []):
            in_flow.update(st.get("operations") or [])
    drawn = Counter((s.get("wireframe") or {}).get("status") for _, s in scr.values())
    n = max(1, len(lin))
    return {
        "operations": len(lin),
        "on a screen": f"{round(100 * len(on_screen & set(lin)) / n)}%",
        "in a flow": f"{round(100 * len(in_flow & set(lin)) / n)}%",
        "screens drawn": f"{drawn.get('designed', 0)} of {sum(drawn.values())}",
        "screens with no board": sum(1 for _, s in scr.values()
                                     if not (s.get("wireframe") or {}).get("board")),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--detail", action="store_true")
    a = ap.parse_args()

    print("=== LINK INTEGRITY ===\n")
    res = audit(a.detail)
    for k, v in res.items():
        mark = "  " if v == 0 else ("~~" if k in ARCHIVE_OK else "!!")
        print(f"  {mark} {k:26}{v}")

    print("\n=== REACH ===\n")
    for k, v in coverage().items():
        print(f"     {k:26}{v}")

    # **A collision is a hazard, not a break.** Every reference that used a bare anchor is now
    # qualified with its board, so nothing resolves wrongly today — but the next tool to store a
    # bare anchor will, and that is worth saying every run rather than discovering twice.
    bad = sum(v for k, v in res.items() if k not in ARCHIVE_OK)
    print()
    if res.get("anchor collision"):
        print(f"  ~~ {res['anchor collision']} anchor collision(s) — references are qualified, so "
              "nothing resolves wrongly. A bare anchor stored anywhere would.")
    if res.get("archived board frame"):
        print(f"  ~~ {res['archived board frame']} pointer(s) into an archived board — the frame "
              "opens, it is just no longer part of the package. This is the record of what Claude "
              "Design drew, and it is kept so the redraw knows what existed.")
    if bad:
        print(f"  {bad} broken link(s). Run with --detail to see them.")
        return 1
    print("  every link resolves.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
