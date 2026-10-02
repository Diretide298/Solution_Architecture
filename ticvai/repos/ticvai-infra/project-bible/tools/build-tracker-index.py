#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The two workshop task trackers, read once into an index the design batches can carry.

**Chinmay, 1 October: "Reference all the material, mom, matrix assisted task."** The Claude Design
bundles carried the screens, the contracts and (since that morning) the client's design inputs from
the minutes, and nothing from the task trackers -- the list of what was promised in each workshop,
who owns it and where it stands. A designer drawing the seat map builder could not see that the
client asked for "a single unified seat map builder screen" on 21 August and that it is still open.

**The trackers are workbooks at the repository root, outside git** (the root ignore rule keeps
`/*` files out). So the export cannot read them: on any other clone they are absent, and a bundle
that changed depending on whose machine refreshed it would be worse than one that never had them.
This reads them once, on the machine that has them, into a committed index:

    handoff/design-inputs/task-tracker-index.json

    TICVAI_Task_Track_From_Workshops.xlsx   sheets Actions (A1..A342) and Client Inputs (C1..C66):
                                            the item, category, owner, priority, status as assessed,
                                            the evidence and the meeting date it names
    TICVAI_Task_Tracker_30-September.xlsx   sheet Tracker (S1.., T1..): the main tasks as of 30 Sep;
                                            sheet "Old rows, closed": where each A/C row went on 30 Sep

**Rows only; no screen mapping here.** Which screen an item concerns is decided by
`tools/design_spec.py` at export time against today's screens (explicit screen ids, then a short
keyword table), so a screen renamed or retired never leaves a stale mapping committed.

**Intake, not a rebuild step** (named in `tools/refresh.sh` `_EXCLUDED`): run it when a new tracker
arrives. It reads the workbooks read-only.

    python3 tools/build-tracker-index.py                       # the workbooks at the repository root
    python3 tools/build-tracker-index.py --src DIR             # somewhere else
"""
from __future__ import annotations

import argparse
import datetime
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "handoff" / "design-inputs" / "task-tracker-index.json"
WORKSHOPS = "TICVAI_Task_Track_From_Workshops.xlsx"
TRACKER = "TICVAI_Task_Tracker_30-September.xlsx"
# The workshop tracker is also inside the package (an older copy); the root one is the latest.
FALLBACK = {WORKSHOPS: ROOT / "sources" / "specifications" / "planning" / WORKSHOPS}

MONTHS = {m: i for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)}
SCREEN_ID = re.compile(r"\b([A-Z]{2,4})-(\d{3})(?:\s*(?:to|–|-)\s*(\d{3}))?\b")
SCREEN_PREFIXES = {"WEB", "GST", "KSK", "POS", "KIT", "EMP", "SCN", "BO", "ADM", "PRT", "ACC", "SUP",
                   "CMS", "DEV", "ANL", "SGN"}


def _cell(v) -> str:
    return "" if v is None else " ".join(str(v).split())


def _date(text: str, default: str = "") -> str:
    """The last meeting date a row names: '(20-Aug)', '24-Sep:', '21-Aug'. Year 2026."""
    found = re.findall(r"\b(\d{1,2})[- ](Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b", text)
    if not found:
        return default
    best = max(datetime.date(2026, MONTHS[m], int(d)) for d, m in found)
    return best.isoformat()


def _screens(text: str) -> list[str]:
    """Screen ids a row names, ranges expanded: 'GST-051 to 054' is five screens."""
    out = []
    for pre, a, b in SCREEN_ID.findall(text):
        if pre not in SCREEN_PREFIXES:
            continue
        lo, hi = int(a), int(b or a)
        if hi < lo or hi - lo > 30:
            hi = lo
        out += [f"{pre}-{n:03d}" for n in range(lo, hi + 1)]
    return sorted(set(out))


def _rows(ws):
    for r in ws.iter_rows(values_only=True):
        yield [_cell(c) for c in r]


def read_workshops(path: pathlib.Path) -> list[dict]:
    import openpyxl
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    out = []
    # Actions: # | Deliverable / task | Category | Owner | Priority | Status | Evidence
    head = False
    for r in _rows(wb["Actions"]):
        if r[:2] == ["#", "Deliverable / task"]:
            head = True
            continue
        if not head or not r[0].isdigit():
            continue
        text, cat, owner, prio, status, ev = (r + [""] * 7)[1:7]
        out.append({"id": f"A{r[0]}", "source": WORKSHOPS, "sheet": "Actions", "text": text,
                    "category": cat, "owner": owner, "priority": prio, "status": status,
                    "evidence": ev, "date": _date(ev), "screens": _screens(text + " " + ev)})
    # Client Inputs: # | Input requested | Owner | Category | Status | Evidence | TICVAI comments
    head = False
    for r in _rows(wb["Client Inputs"]):
        if r[:2] == ["#", "Input requested"]:
            head = True
            continue
        if not head or not r[0].isdigit():
            continue
        text, owner, cat, status, ev, comment = (r + [""] * 7)[1:7]
        out.append({"id": f"C{r[0]}", "source": WORKSHOPS, "sheet": "Client Inputs", "text": text,
                    "category": cat, "owner": owner, "priority": "", "status": status,
                    "evidence": " ".join(x for x in (ev, comment) if x), "date": _date(ev),
                    "screens": _screens(text + " " + ev)})
    return out


def read_tracker(path: pathlib.Path) -> tuple[list[dict], dict]:
    import openpyxl
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    rows, closed = [], {}
    head = False
    for r in _rows(wb["Tracker"]):
        if r[:2] == ["#", "Task"]:
            head = True
            continue
        if not head or not re.match(r"^[ST]\d+$", r[0]):
            continue
        text, owner, tag, status, due, notes = (r + [""] * 7)[1:7]
        rows.append({"id": r[0], "source": TRACKER, "sheet": "Tracker", "text": text, "category": tag,
                     "owner": owner, "priority": "", "status": status, "due": due, "evidence": notes,
                     "date": "2026-09-30", "screens": _screens(text + " " + notes)})
    head = False
    for r in _rows(wb["Old rows, closed"]):
        if r[:2] == ["Old #", "Task or input"]:
            head = True
            continue
        if not head or not re.match(r"^[AC]\d+$", r[0]):
            continue
        closed[r[0]] = {"statusNow": r[4], "whereNow": r[5]}
    return rows, closed


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", help="folder holding the two workbooks (default: the repository root)")
    a = ap.parse_args()
    src = pathlib.Path(a.src).resolve() if a.src else ROOT.parent

    def find(name):
        p = src / name
        if p.exists():
            return p
        fb = FALLBACK.get(name)
        return fb if fb and fb.exists() else None

    w, t = find(WORKSHOPS), find(TRACKER)
    if not w or not t:
        print(f"tracker index: {WORKSHOPS if not w else TRACKER} not found in {src}; index left as it is")
        return 0 if OUT.exists() else 1
    rows = read_workshops(w)
    trk, closed = read_tracker(t)
    for r in rows:
        if r["id"] in closed:
            r.update(closed[r["id"]])
    rows += trk
    doc = {
        "generatedBy": "tools/build-tracker-index.py",
        "generated": datetime.date.today().isoformat(),
        # Where each was read: the repository root, or the package's own copy of the workshop tracker.
        "sources": {name: (str(p.relative_to(ROOT)).replace("\\", "/") if p.is_relative_to(ROOT)
                           else f"(repository root)/{name}") for name, p in ((WORKSHOPS, w), (TRACKER, t))},
        "note": ("Rows of the two workshop task trackers, read-only from the workbooks at the repository root "
                 "(outside git). A = Actions and C = Client Inputs of the workshop tracker, with where each went "
                 "on 30 September (statusNow, whereNow); S and T = the 30 September tracker. Screen mapping is "
                 "done at export time by tools/design_spec.py. Rebuild with tools/build-tracker-index.py; never edit."),
        "rows": rows,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=1, ensure_ascii=False), encoding="utf-8")
    n_scr = sum(1 for r in rows if r["screens"])
    print(f"tracker index: {len(rows)} rows ({sum(1 for r in rows if r['id'][0] == 'A')} actions, "
          f"{sum(1 for r in rows if r['id'][0] == 'C')} client inputs, {len(trk)} on the 30 Sep tracker); "
          f"{n_scr} name a screen -> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
