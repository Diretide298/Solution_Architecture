#!/usr/bin/env python3
"""List the screens nothing can draw, and the ones only just drawable, as a workbook.

Writes `docs/active/thin-screens.xlsx`. **The question it answers is "which screens does somebody
still have to think about", and the answer is much smaller than it was this morning.**

## Why the number moved from 203 to 32

203 screens came out of the pack rebuild with no content region: their pack pages carry a purpose,
an acceptance condition and worked examples, and no directory of metrics, columns or fields.

**But 197 of them declare operations, and those operations return schemas with 3,959 fields between
them.** The contracts generator would have given every one of them columns — and skipped all 203,
because its hand-off rule was *"skip anything with a pack entry"*. A pack entry is not the same as
being served by one, and the hole in the hand-off sat exactly where the pack was thinnest.

That leaves **32 screens with genuinely nothing** — and those are the sheet worth reading.

## The three sheets

  **Hollow** — nothing draws them: no pack directory, and no operation returning a described
  shape. Each carries its purpose and acceptance condition, which is what a person would have to
  work from.

  **Recovered** — was hollow, now filled from its own contracts. Listed so the fill can be checked
  rather than trusted; a column count of forty is a schema dumped onto a screen, not a design.

  **Thin** — has a content region and fewer than four columns in it. Not broken, but the next tier
  of concern, and the place where a bad derivation is easiest to miss.

Run: python tools/build-thin-screens-workbook.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

sys.path.insert(0, str(Path(__file__).resolve().parent))
from contract_shapes import load_contracts, response_schemas, schema_fields  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SCREENS = ROOT / "screens"
PACK = ROOT / "sources" / "workshop" / "pack.json"
OUT = ROOT / "docs" / "active" / "thin-screens.xlsx"

PLUMBING = {"createdAt", "updatedAt", "createdBy", "updatedBy", "deletedAt", "version", "etag",
            "tenantId", "cellId", "schemaVersion", "_links", "meta"}

HEAD = PatternFill("solid", fgColor="0B1324")
WARN = PatternFill("solid", fgColor="FFF7E6")
OK = PatternFill("solid", fgColor="E7F4F2")


def clean(v):
    """**A lone surrogate kills the whole save and names neither the screen nor the field.**
    `derive-wireframes.py` already carries this guard, for the same reason: a source file edited by
    a tool that split a surrogate pair reaches here as an unencodable string, and encoding is the
    only place it surfaces. Cheaper to strip than to find again."""
    if isinstance(v, str):
        v = v.encode("utf-8", "ignore").decode("utf-8")
        return "".join(ch for ch in v if ch >= " " or ch in (chr(9), chr(10)))
    return v


def sheet(wb, title, headers, rows, widths, note):
    ws = wb.create_sheet(title)
    ws["A1"] = note
    ws["A1"].font = Font(italic=True, color="5A6577", size=9)
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(headers))
    ws.row_dimensions[1].height = 30
    ws["A1"].alignment = Alignment(wrap_text=True, vertical="center")
    for i, h in enumerate(headers, 1):
        c = ws.cell(row=2, column=i, value=h)
        c.font = Font(bold=True, color="FFFFFF", size=9)
        c.fill = HEAD
        c.alignment = Alignment(vertical="center")
    for r, row in enumerate(rows, 3):
        for i, v in enumerate(row, 1):
            c = ws.cell(row=r, column=i, value=clean(v))
            c.alignment = Alignment(wrap_text=True, vertical="top")
            c.font = Font(size=9)
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A3"
    ws.auto_filter.ref = f"A2:{get_column_letter(len(headers))}{max(len(rows) + 2, 3)}"
    return ws


def main() -> int:
    pack = {(e["source"], str(e["number"]), str(e["page"])): e
            for e in json.loads(PACK.read_text(encoding="utf-8"))}
    ops, schemas = load_contracts(ROOT)

    hollow, recovered, thin, every = [], [], [], []
    for f in sorted(SCREENS.glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        code = doc["platform"]["code"]
        for s in doc["screens"]:
            regions = (s.get("layout") or {}).get("regions") or []
            body = [r for r in regions if r.get("name") == "contentBody" and r.get("components")]
            cols = sum(len(c.get("columns") or []) for r in regions
                       for c in r.get("components") or [])
            src = s.get("source") or {}
            entry = pack.get((src.get("pack"), str(src.get("number")), str(src.get("page"))))
            bullets = sum(len(v) for v in (entry or {}).get("sections", {}).values())
            op_ids = [a.get("operationId") for a in (s.get("apis") or []) if a.get("operationId")]
            # what its own operations could still offer
            avail = 0
            for oid in op_ids:
                if oid in ops:
                    for sch in response_schemas(ops[oid]["op"]):
                        avail += len([p for p in schema_fields(sch, schemas) if p not in PLUMBING])
            common = [code, s["id"], s["name"], s.get("module"), s.get("wave"),
                      s.get("pattern"), " · ".join(op_ids) or "none declared",
                      (s.get("purpose") or "").strip(), (s.get("purposeNote") or "").strip(),
                      src.get("pack") or "no pack", src.get("page"), bullets]
            if not body:
                hollow.append(common + [avail,
                                        " | ".join(g["why"][:180] for g in (s.get("gaps") or []))])
            elif any(str(c.get("provenance", "")).startswith("contract ")
                     for r in body for c in r["components"]) and entry:
                recovered.append(common + [cols, avail])
            elif cols < 4:
                thin.append(common + [cols, avail])
            # **The same audit against every screen, not only the thin ones.** What a screen shows
            # against what its own sources could give it: a screen displaying six of a schema's
            # forty fields may be a good edit or an oversight, and the delta is the only way to
            # tell them apart at 1,091 screens.
            origin = ("frame" if any(str(c.get("provenance", "")).startswith("frame ")
                                     for r in regions for c in r.get("components") or [])
                      else "pack" if any(str(c.get("provenance", "")).startswith("pack ")
                                         for r in regions for c in r.get("components") or [])
                      else "contract" if any(str(c.get("provenance", "")).startswith("contract ")
                                             for r in regions for c in r.get("components") or [])
                      else "none")
            every.append([code, s["id"], s["name"], s.get("module"), s.get("wave"),
                          s.get("pattern"), origin, len(op_ids),
                          sum(len(r.get("components") or []) for r in regions),
                          cols, avail, max(avail - cols, 0), bullets,
                          len(s.get("overlays") or []), len(s.get("gaps") or []),
                          "yes" if body else "NO",
                          (s.get("purpose") or "").strip()])

    wb = Workbook()
    wb.remove(wb.active)

    sheet(wb, "Hollow", [
        "Platform", "Screen", "Name", "Module", "Wave", "Pattern", "Operations", "Purpose",
        "Acceptance condition", "Pack", "Page", "Pack bullets", "Fields its APIs could give",
        "Recorded gap"],
        hollow,
        [9, 10, 34, 20, 6, 14, 34, 60, 60, 30, 7, 12, 12, 70],
        "SCREENS NOTHING CAN DRAW. No directory of metrics, columns or fields in their source, and "
        "no operation returning a described shape. The purpose and acceptance condition are what a "
        "person would have to work from — they say what the screen is for, not what is on it.")

    sheet(wb, "Recovered", [
        "Platform", "Screen", "Name", "Module", "Wave", "Pattern", "Operations", "Purpose",
        "Acceptance condition", "Pack", "Page", "Pack bullets", "Columns now", "Fields available"],
        recovered,
        [9, 10, 34, 20, 6, 14, 34, 60, 60, 30, 7, 12, 12, 12],
        "WAS HOLLOW, NOW FILLED FROM ITS OWN CONTRACTS. Listed so the fill can be checked rather "
        "than trusted: a response schema says what a screen CAN show, not what it SHOULD, and a "
        "column count near forty is a schema dumped onto a screen rather than a design.")

    sheet(wb, "Thin", [
        "Platform", "Screen", "Name", "Module", "Wave", "Pattern", "Operations", "Purpose",
        "Acceptance condition", "Pack", "Page", "Pack bullets", "Columns", "Fields available"],
        thin,
        [9, 10, 34, 20, 6, 14, 34, 60, 60, 30, 7, 12, 10, 12],
        "FEWER THAN FOUR COLUMNS. Not broken, but the tier where a bad derivation is easiest to "
        "miss — a screen with two columns looks specified and usually is not.")

    every.sort(key=lambda r: -r[11])
    sheet(wb, "All screens", [
        "Platform", "Screen", "Name", "Module", "Wave", "Pattern", "Content from", "Operations",
        "Components", "Columns shown", "Fields available", "Not shown", "Pack bullets",
        "Overlays", "Gaps", "Has content", "Purpose"],
        every,
        [9, 10, 34, 20, 6, 14, 12, 10, 11, 13, 14, 10, 12, 9, 7, 11, 60],
        "EVERY SCREEN, sorted by how much its own sources could give it that it does not show. "
        "'Not shown' is fields available minus columns shown — a large number is either a "
        "deliberate edit or an oversight, and this column is the only way to tell them apart at "
        "1,091 screens. 'Content from' says which source actually filled the screen.")

    wb.save(OUT)
    shown = sum(r[9] for r in every); could = sum(r[10] for r in every)
    print(f"hollow {len(hollow)} · recovered {len(recovered)} · thin {len(thin)} · all {len(every)}")
    print(f"{shown:,} columns shown against {could:,} fields available "
          f"({could - shown:,} not shown)")
    print(f"-> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
