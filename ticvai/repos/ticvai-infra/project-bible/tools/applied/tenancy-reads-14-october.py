#!/usr/bin/env python3
"""The reads the ADAM CR-080..083 fixes add to the lineage (14 October 2026, CHG-TEN-001, -002, -004).

**Found by the audit of 14 October** (ADAM CR-081, CR-083): a board save refused "an unknown or unsellable
variant" and `configureWorkstation` refused "a shift is open" while their lineage read neither Catalogue's variant
nor Orders' shift, so the refusal had no data behind it. The answer is a declared query on the owner
(`x-ticvai-queries` in catalogue.yaml and shift.yaml, asked through `x-ticvai-read-via` on the operation); the
lineage lists the owner's tables the query reads, so a reviewer sees what the operation depends on, and
`readVia` (copied from the contract by derive-lineage) says how it gets there.

* createSaleBoard, updateSaleBoard, addCartLine, addToWishlist: Catalogue's `variantsSellableAt` reads
  `catalogue.variant` and `catalogue.product`.
* configureWorkstation, revokeAllSessions, planTenantMigration: Orders' `openShiftForWorkstation` /
  `openShiftsInScope` read `orders.pos_shift`.
* publishBundle reads the board's pages as well as the board and its tiles (the bundle carries every page and
  tile; it listed the tile and not the page that holds it).

Run once; a second run changes nothing.

    python tools/applied/tenancy-reads-14-october.py [--apply]
"""
from __future__ import annotations

import argparse
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SELLABLE = "CHG-TEN-002: through Catalogue's variantsSellableAt (x-ticvai-read-via; ADAM CR-081)"
OPEN_SHIFT = "CHG-TEN-004: through Orders' "
LINEAGE = {
    "createSaleBoard": (["catalogue.variant", "catalogue.product"], SELLABLE + ", in process"),
    "updateSaleBoard": (["catalogue.variant", "catalogue.product"], SELLABLE + ", in process"),
    "addCartLine": (["catalogue.variant", "catalogue.product"], SELLABLE + ", in process"),
    "addToWishlist": (["catalogue.variant", "catalogue.product"], SELLABLE + ", by Catalogue's service route"),
    "configureWorkstation": (["orders.pos_shift"],
                             OPEN_SHIFT + "openShiftForWorkstation (x-ticvai-read-via; ADAM CR-083), in process"),
    # revokeAllSessions no longer asks Orders (CHG-R6G-006, tools/applied/r6g-lineage-14-october.py): Identity reads
    # nothing above it, so its entry is gone and a second run does not put the read back.
    "planTenantMigration": (["orders.pos_shift"],
                            OPEN_SHIFT + "openShiftsInScope (x-ticvai-read-via; ADAM CR-083), by Orders' service route"),
    # read through the view named for Catalogue since CHG-R6G-007 (tools/applied/r6g-lineage-14-october.py)
    "publishBundle": (["platform.sale_board_page_for_catalogue"],
                      "CHG-TEN-001: the bundle carries every page of a board (ADAM CR-080)"),
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    path = os.path.join(ROOT, "handoff", "api-data-lineage.json")
    raw = io.open(path, encoding="utf-8", newline="").read()
    lin = json.loads(raw)
    n = 0
    for op, (add, why) in LINEAGE.items():
        e = lin.get(op)
        if e is None:
            raise SystemExit("%s is not in the lineage" % op)
        reads = sorted(set(e.get("reads") or []) | set(add))
        if reads != sorted(e.get("reads") or []):
            e["reads"] = reads
            note = "14 October 2026: reads " + ", ".join(add) + " (" + why + ")"
            e["fixNote"] = (e["fixNote"] + "; " + note) if e.get("fixNote") else note
            n += 1
    print("lineage entries changed: %d of %d" % (n, len(LINEAGE)))
    if a.apply and n:
        out = json.dumps(lin, indent=1, ensure_ascii=False)
        if "\r\n" in raw:
            out = out.replace("\n", "\r\n")
        io.open(path, "w", encoding="utf-8", newline="").write(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
