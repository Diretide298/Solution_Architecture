#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The schema merge task sheet, generated from the verdicts rather than typed.

**The first cut of this sheet said 26 decided when the review had settled 31.** The
verdicts lived in prose and the sheet was written by hand from memory of them, so the
sheet and the review drifted the moment either moved. `handoff/merge-verdicts.json` is
the source of truth now and this builds the workbook from it, which is why the count on
the Summary sheet cannot disagree with the count in the review again.

Three sheets:

    Tasks     one row per unmatched table of theirs, with our verdict and its reason
    Open      only the rows somebody still has to choose, so the meeting has an agenda
    Summary   the tallies, and the grouping the response document uses

The verdict vocabulary grew as the review ran, which is normal — a category is a thing
you discover, not a thing you declare up front. `GROUP` folds fourteen verdicts into the
three answers a reader actually wants: are we taking it, are we keeping ours, or does
somebody have to decide.

    python3 tools/build-merge-workbook.py
"""
import collections
import io
import json
import os
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = os.path.join(ROOT, "handoff")
OUT = os.path.join(H, "TICVAI_Schema_Merge_Tasks.xlsx")

# The three answers a reader wants, and which verdicts give each one.
GROUP = {
    "We accept": ["ADDITIVE", "TAKE THEIRS", "TAKE BODY", "MERGE", "EITHER", "TAKE EITHER"],
    "We decline": ["DECLINE", "KEEP OURS"],
    "Needs a choice": ["DECIDE", "COLLISION", "PLACEMENT", "SPLIT"],
    "Correction": ["NO MATCH", "RECLASSIFY"],
}
OF = {v: g for g, vs in GROUP.items() for v in vs}

HEAD = PatternFill("solid", fgColor="1F3864")
BAND = {
    "We accept": PatternFill("solid", fgColor="E2EFDA"),
    "We decline": PatternFill("solid", fgColor="FCE4D6"),
    "Needs a choice": PatternFill("solid", fgColor="FFF2CC"),
    "Correction": PatternFill("solid", fgColor="E7E6E6"),
}


def load(name):
    return json.load(io.open(os.path.join(H, name), encoding="utf-8"))


def sheet(wb, title, cols, rows, widths):
    ws = wb.create_sheet(title)
    ws.append(cols)
    for c in range(1, len(cols) + 1):
        cell = ws.cell(row=1, column=c)
        cell.fill = HEAD
        cell.font = Font(bold=True, color="FFFFFF")
        cell.alignment = Alignment(vertical="center")
        ws.column_dimensions[get_column_letter(c)].width = widths[c - 1]
    for r in rows:
        ws.append(r)
        band = BAND.get(r[1])
        if band:
            for c in range(1, len(cols) + 1):
                ws.cell(row=ws.max_row, column=c).fill = band
        ws.cell(row=ws.max_row, column=len(cols)).alignment = Alignment(wrap_text=True,
                                                                       vertical="top")
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    return ws


def main():
    verdicts = load("merge-verdicts.json")
    cls = load("mismatch-classification.json")

    rows = []
    for t in sorted(verdicts):
        v, why = verdicts[t]
        d = cls.get(t) or {}
        rows.append([t, OF.get(v, "?"), v, d.get("category", ""), d.get("purpose", ""), why])

    cols = ["Their table", "Answer", "Verdict", "How it was classified", "Their stated purpose",
            "Our reason"]
    widths = [38, 16, 14, 22, 62, 72]

    wb = Workbook()
    wb.remove(wb.active)
    sheet(wb, "Tasks", cols, rows, widths)
    sheet(wb, "Open", cols, [r for r in rows if r[1] == "Needs a choice"], widths)

    ws = wb.create_sheet("Summary")
    ws.append(["Schema merge — where the 223 unmatched tables landed"])
    ws.cell(row=1, column=1).font = Font(bold=True, size=13)
    ws.append([])
    by_group = collections.Counter(r[1] for r in rows)
    ws.append(["Answer", "Tables"])
    for c in (1, 2):
        ws.cell(row=ws.max_row, column=c).fill = HEAD
        ws.cell(row=ws.max_row, column=c).font = Font(bold=True, color="FFFFFF")
    for g in ("We accept", "We decline", "Needs a choice", "Correction"):
        ws.append([g, by_group.get(g, 0)])
        ws.cell(row=ws.max_row, column=1).fill = BAND[g]
        ws.cell(row=ws.max_row, column=2).fill = BAND[g]
    ws.append(["Total", sum(by_group.values())])
    ws.cell(row=ws.max_row, column=1).font = Font(bold=True)
    ws.cell(row=ws.max_row, column=2).font = Font(bold=True)
    ws.append([])
    ws.append(["Verdict", "Tables", "Answer"])
    for c in (1, 2, 3):
        ws.cell(row=ws.max_row, column=c).fill = HEAD
        ws.cell(row=ws.max_row, column=c).font = Font(bold=True, color="FFFFFF")
    for v, n in collections.Counter(r[2] for r in rows).most_common():
        ws.append([v, n, OF.get(v, "?")])
    ws.column_dimensions["A"].width = 22
    ws.column_dimensions["B"].width = 10
    ws.column_dimensions["C"].width = 18

    wb.save(OUT)
    print("  %d row(s) -> handoff/TICVAI_Schema_Merge_Tasks.xlsx" % len(rows))
    for g in ("We accept", "We decline", "Needs a choice", "Correction"):
        print("    %-16s %3d" % (g, by_group.get(g, 0)))
    missing = sorted(set(cls) - set(verdicts))
    if missing:
        print("  %d table(s) classified with no verdict:" % len(missing))
        for t in missing[:10]:
            print("      %s" % t)
    return 0


if __name__ == "__main__":
    sys.exit(main())
