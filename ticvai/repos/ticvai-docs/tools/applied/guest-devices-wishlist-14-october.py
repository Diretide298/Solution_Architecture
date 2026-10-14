#!/usr/bin/env python3
"""The lineage half of the r6 guest devices and wishlist settlement (14 October 2026, batch MKT: ADAM CR-086, CR-087,
CR-088).

**Found by the audit of the CRs raised on 14 October** (developer of SVC-MARKETING-GUEST-1, tickets 30705 to 30708):
`getWishlist` returns Catalogue's name, picture, current price and availability while its lineage read only
`marketing.wishlist_item`, and the two path-inferred entries beside it wrote the wrong table: `removeFromWishlist` and
`revokeGuestDevice` were recorded as writing `marketing.guest_profile`, though one deletes a wishlist row and the other
revokes a device row. The contracts were edited by hand in the same commits (contracts/satellite/marketing-crm.yaml,
contracts/spine/catalogue.yaml); this one-off gives `handoff/api-data-lineage.json` the reads and writes those edits
declare, the way `tenancy-reads-14-october.py` did for CHG-TEN-002. `derive-lineage --apply` adds and never updates,
so an existing entry only changes through a tool like this one, and it copies `readVia` from the contract's
`x-ticvai-read-via`.

* CHG-MKT-002 (CR-087): `addToWishlist` and `getWishlist` read, through Catalogue's `variantListingFacts` on its
  service route, the tables that query reads: the variant, its product and primary media, the price list that
  prices it and the saved performance. `removeFromWishlist` reads and deletes `marketing.wishlist_item`.
* CHG-MKT-001 (CR-086): `revokeGuestDevice` reads and updates `marketing.guest_device`.

Run once; a second run changes nothing.

    python tools/applied/guest-devices-wishlist-14-october.py [--apply]
"""
from __future__ import annotations

import argparse
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

FACTS = ["catalogue.variant", "catalogue.product", "catalogue.product_media", "catalogue.price",
         "catalogue.price_list", "catalogue.price_assignment", "catalogue.performance"]
VIA = "CHG-MKT-002: through Catalogue's variantListingFacts (x-ticvai-read-via; ADAM CR-087), by Catalogue's service route"
# op: (reads to add, writes to add, reads to remove, writes to remove, why)
LINEAGE = {
    "addToWishlist": (FACTS, [], [], [], VIA),
    "getWishlist": (FACTS, [], [], [], VIA),
    "removeFromWishlist": (["marketing.wishlist_item"], ["marketing.wishlist_item"], ["marketing.guest_profile"],
                           ["marketing.guest_profile"],
                           "CHG-MKT-002: it deletes the guest's wishlist row, not the guest profile (ADAM CR-087)"),
    "revokeGuestDevice": (["marketing.guest_device"], ["marketing.guest_device"], ["marketing.guest_profile"],
                          ["marketing.guest_profile"],
                          "CHG-MKT-001: it revokes the device row and clears its token, not the guest profile "
                          "(ADAM CR-086)"),
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    path = os.path.join(ROOT, "handoff", "api-data-lineage.json")
    raw = io.open(path, encoding="utf-8", newline="").read()
    lin = json.loads(raw)
    sref = json.load(io.open(os.path.join(ROOT, "handoff", "schema-reference.json"), encoding="utf-8"))["cols"]
    n = 0
    for op, (r_add, w_add, r_del, w_del, why) in LINEAGE.items():
        e = lin.get(op)
        if e is None:
            raise SystemExit("%s is not in the lineage" % op)
        for t in r_add + w_add:
            if t not in sref:
                raise SystemExit("%s: %s is not a table" % (op, t))
        reads = sorted((set(e.get("reads") or []) | set(r_add)) - set(r_del))
        writes = sorted((set(e.get("writes") or []) | set(w_add)) - set(w_del))
        if reads != sorted(e.get("reads") or []) or writes != sorted(e.get("writes") or []):
            e["reads"], e["writes"] = reads, writes
            note = "14 October 2026: " + why
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
