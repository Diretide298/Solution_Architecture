#!/usr/bin/env python3
"""Applied 3 November 2026 (r13 review, CHG-R13RVB-004): the screen notes and gaps their own records had overtaken.

What tools/screen_gaps.py judges stale, removed from the authored screen records, by text so each file keeps its
own layout:

  * the board-import sentence "Components, states and operations still to be written." on a screen with a layout,
    states and operations (85 screens; EMP-044 and EMP-045, which declare no operation, keep it);
  * a generated gap the screen's declarations contradict: "declares no operation that writes anything" beside a
    write, "operations return no schema with described properties" beside an answer that has them, "No read of X"
    or "(Y has no get)" beside that read, and a 2 October contract gap whose operation says it was built for this
    screen: dropped;
  * "the screen declares N operations" with the wrong N: the count corrected, the unserved actions kept;
  * by hand, four 2 October contract gaps their declared operation now answers (HAND).

Kept for the record; check-screen-wiring S-NOTES-STALE now fails on any of these. A second run changes nothing.

    python tools/applied/r13-review-stale-screen-text.py [--apply]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import audit_guard as g  # noqa: E402
import contract_shapes as cs  # noqa: E402
import screen_gaps as sg  # noqa: E402

# screen id -> (a phrase of the gap's text, the operation that now answers it)
HAND = {
    "BO-008": ("renders the PDF ticket and Wallet pass preview", "previewProductTickets (CHG-CSP-038)"),
    "BO-007": ("A catalogue-contract bulk product write", "bulkUpdateCatalogueProducts (CHG-FUP-011)"),
    "BO-065": ("No staff-audience read of delivery locations", "listDeliveryLocations, staff since CHG-CSA-045"),
    "BO-454": ("No staff-audience read of a game card", "getGameCard, staff since CHG-SCR-015"),
}


def _block(lines: list, sid: str):
    start = next((i for i, l in enumerate(lines) if l.rstrip() == f"- id: {sid}"), None)
    if start is None:
        return None
    end = start + 1
    while end < len(lines) and not (lines[end].startswith("- ") or (lines[end][:1].strip() and
                                                                       not lines[end].startswith("#"))):
        end += 1
    return start, end


def _gap_items(lines: list, start: int, end: int):
    """(line of `  gaps:`, [(item start, item end)]) inside a screen block."""
    k = next((i for i in range(start, end) if lines[i].rstrip() == "  gaps:"), None)
    if k is None:
        return None, []
    items, i = [], k + 1
    while i < end and lines[i].startswith("  - "):
        j = i + 1
        while j < end and lines[j].startswith("    "):
            j += 1
        items.append((i, j))
        i = j
    return k, items


def main() -> int:
    apply = "--apply" in sys.argv[1:]
    g.force_utf8()
    ops = g.operations()
    _, schemas = cs.load_contracts(ROOT)
    by_file: dict = {}
    skip = sg.twins(g.screens())
    for plat, s in g.screens():
        by_file.setdefault(plat, []).append(s)
    total = {"still": 0, "drop": 0, "count": 0, "hand": 0}
    for plat, screens in sorted(by_file.items()):
        path = ROOT / "screens" / f"{plat}.yaml"
        raw = path.read_bytes().decode("utf-8")
        crlf = "\r\n" in raw
        lines = raw.replace("\r\n", "\n").split("\n")
        changed = False
        for s in screens:
            sid = s["id"]
            stale = sg.stale_gaps(s, ops, schemas, skip)
            hand = HAND.get(sid)
            if hand:
                for i, gap in enumerate(s.get("gaps") or []):
                    if hand[0] in re.sub(r"\s+", " ", str(gap.get("why") if isinstance(gap, dict) else gap)):
                        stale.append((i, "hand", "drop"))
            still = sg.still_to_be_written(s)
            if not stale and not still:
                continue
            blk = _block(lines, sid)
            if not blk:
                print(f"  {plat} {sid}: block not found; by hand")
                continue
            start, end = blk
            k, items = _gap_items(lines, start, end)
            gaps = s.get("gaps") or []
            if stale and len(items) != len(gaps):
                print(f"  {plat} {sid}: {len(items)} gap items in the text, {len(gaps)} parsed; by hand")
                continue
            drop = sorted({i for i, _k, fx in stale if fx == "drop"}, reverse=True)
            for i, kind, fx in stale:
                if isinstance(fx, tuple):
                    a, b = items[i]
                    text = "\n".join(lines[a:b])
                    n = fx[1]
                    new = sg.OP_COUNT.sub(lambda m: f"{m.group(1)}{n}{m.group(3)[:len(m.group(3)) - len(m.group(3).lstrip())]}"
                                          f"operation{'s' if n != 1 else ''}", text, count=1)
                    lines[a:b] = new.split("\n")
                    total["count"] += 1
                    print(f"  {sid}: {kind} -> {n}")
            for i in drop:
                a, b = items[i]
                del lines[a:b]
                total["hand" if any(x == (i, "hand", "drop") for x in stale) else "drop"] += 1
                print(f"  {sid}: gap {i} dropped ({next(kd for ii, kd, _ in stale if ii == i)})")
            if drop and len(drop) == len(items):
                lines[k] = "  gaps: []"
            if still:
                blk = _block(lines, sid)
                start, end = blk
                text = "\n".join(lines[start:end])
                new = re.sub(r"\s*Components,\s+states\s+and\s+operations\s+still\s+to\s+be\s+written\.", "", text,
                             count=1)
                if new != text:
                    lines[start:end] = new.split("\n")
                    total["still"] += 1
            changed = True
        if changed and apply:
            out = "\n".join(lines)
            path.write_bytes((out.replace("\n", "\r\n") if crlf else out).encode("utf-8"))
    print(f"{'applied' if apply else 'would apply'}: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
