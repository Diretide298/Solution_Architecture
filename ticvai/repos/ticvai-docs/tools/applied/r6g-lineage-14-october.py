#!/usr/bin/env python3
"""Two lineage fixes from the first full r6 gate (14 October 2026, batch R6G).

* **publishBundle reads the sale boards through the views named for Catalogue** (CHG-R6G-007). Catalogue builds the
  signed bundle from the boards Tenancy owns: bulk data, inside one deployable (commerce), which is what a generated
  `<table>_for_<reader>` view is for (ADR-0055 rule 2 as amended 14 October; DB-READ-VIEWS). The lineage named the
  boards raw (platform.sale_board, platform.sale_board_page, platform.sale_board_tile), and the page, added by
  CHG-TEN-001, failed check-cross-module-reads XR-UNCOVERED. All three now read through
  `platform.sale_board_for_catalogue`, `platform.sale_board_page_for_catalogue` and
  `platform.sale_board_tile_for_catalogue`.
* **revokeAllSessions reads nothing above Identity** (CHG-R6G-006). It asked Orders' openShiftsInScope in process
  (CHG-TEN-004), and Identity, the foundation tier, reads nothing above it but a projection (ADR-0028;
  check-cross-module-reads XR-FOUNDATION). It no longer reports open shifts: the console calls Orders' listShifts
  beside it (P08 BO-053). Its read of orders.pos_shift goes.

Run once; a second run changes nothing.

    python tools/applied/r6g-lineage-14-october.py [--apply]
"""
from __future__ import annotations

import argparse
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

VIEWS = "CHG-R6G-007: the boards through the views named for Catalogue, bulk data within commerce (ADR-0055 rule 2)"
# operation -> ({read to replace: its replacement, or None to drop it}, why)
LINEAGE = {
    "publishBundle": ({"platform.sale_board": "platform.sale_board_for_catalogue",
                       "platform.sale_board_page": "platform.sale_board_page_for_catalogue",
                       "platform.sale_board_tile": "platform.sale_board_tile_for_catalogue"}, VIEWS),
    "revokeAllSessions": ({"orders.pos_shift": None},
                          "CHG-R6G-006: Identity reads nothing above it (ADR-0028); the console asks Orders' "
                          "listShifts beside it"),
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    path = os.path.join(ROOT, "handoff", "api-data-lineage.json")
    raw = io.open(path, encoding="utf-8", newline="").read()
    lin = json.loads(raw)
    n = 0
    for op, (swap, why) in LINEAGE.items():
        e = lin.get(op)
        if e is None:
            raise SystemExit("%s is not in the lineage" % op)
        old = list(e.get("reads") or [])
        reads = sorted({swap.get(t, t) for t in old if not (t in swap and swap[t] is None)})
        if reads != sorted(old):
            e["reads"] = reads
            gone = sorted(t for t in old if t in swap)
            note = ("14 October 2026: " + ", ".join(
                (t + " read as " + swap[t]) if swap[t] else (t + " no longer read") for t in gone) + " (" + why + ")")
            e["fixNote"] = (e["fixNote"] + "; " + note) if e.get("fixNote") else note
            rc = e.get("readColumns")
            if isinstance(rc, dict):
                for t in gone:
                    if t in rc:
                        cols = rc.pop(t)
                        if swap[t]:
                            rc[swap[t]] = cols
            n += 1
    print("lineage entries changed: %d of %d" % (n, len(LINEAGE)))
    if a.apply and n:
        out = json.dumps(lin, indent=1, ensure_ascii=False)
        if raw.endswith("\n"):
            out += "\n"                      # keep the file's last line ending
        if "\r\n" in raw:
            out = out.replace("\n", "\r\n")
        io.open(path, "w", encoding="utf-8", newline="").write(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
