#!/usr/bin/env python3
"""Lineage fixes of the module-boundaries audit batch (14 October 2026, batch MOD).

* **listDelegations reads nothing above Identity** (CHG-MOD-002). Its lineage read marketing.guest_profile, which
  Marketing (engagement tier, operations deployable) owns; Identity is the foundation tier and reads nothing above it
  but a projection (ADR-0028; ADR-0055 rule 4 as amended 14 October; check-cross-module-reads XR-FOUNDATION).
  DelegatedAccess carries no profile field: the names a delegation list shows are the guests' own, in pii.subject,
  which Identity owns and the operation already reads. The read goes.
* **setCustomerGuestAccount announces the orders it attaches to a guest** (CHG-MOD-006). It writes
  orders.sales_order and touches pii.* (whom the order belongs to) without an event, so Identity's projection
  identity.subject_holding never learned the guest holds the order (check-error-sources E-UNFED, the
  orders#openOrdersForSubject projection; CHG-GDL-003). It now emits order.linkedToGuest for each order it attaches
  (events/order-linkedToGuest.yaml emittedBy), written to the outbox in its own transaction (ADR-0033), so its
  lineage writes platform.outbox (check-write-lineage W-OUTBOX).

Run once, before derive-lineage; a second run changes nothing.

    python tools/applied/mod-lineage-14-october.py [--apply]
"""
from __future__ import annotations

import argparse
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# operation -> (reads to drop, writes to add, why)
LINEAGE = {
    "listDelegations": (["marketing.guest_profile"], [],
                        "CHG-MOD-002: Identity reads nothing above it (ADR-0028); the names are the guests' own in "
                        "pii.subject"),
    "setCustomerGuestAccount": ([], ["platform.outbox"],
                                "CHG-MOD-006: emits order.linkedToGuest for each order it attaches to a guest, through "
                                "the outbox (ADR-0033)"),
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    path = os.path.join(ROOT, "handoff", "api-data-lineage.json")
    raw = io.open(path, encoding="utf-8", newline="").read()
    lin = json.loads(raw)
    n = 0
    for op, (drop, add, why) in LINEAGE.items():
        e = lin.get(op)
        if e is None:
            raise SystemExit("%s is not in the lineage" % op)
        reads = sorted(t for t in (e.get("reads") or []) if t not in drop)
        writes = sorted(set(e.get("writes") or []) | set(add))
        if reads == sorted(e.get("reads") or []) and writes == sorted(e.get("writes") or []):
            continue
        gone = sorted(t for t in (e.get("reads") or []) if t in drop)
        new = sorted(set(add) - set(e.get("writes") or []))
        e["reads"], e["writes"] = reads, writes
        rc = e.get("readColumns")
        if isinstance(rc, dict):
            for t in gone:
                rc.pop(t, None)
        bits = ([t + " no longer read" for t in gone] + ["writes " + t for t in new])
        note = "14 October 2026: " + ", ".join(bits) + " (" + why + ")"
        e["fixNote"] = (e["fixNote"] + "; " + note) if e.get("fixNote") else note
        n += 1
    print("lineage entries changed: %d of %d" % (n, len(LINEAGE)))
    if a.apply and n:
        out = json.dumps(lin, indent=1, ensure_ascii=False)
        if raw.endswith("\n"):
            out += "\n"
        if "\r\n" in raw:
            out = out.replace("\n", "\r\n")
        io.open(path, "w", encoding="utf-8", newline="").write(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
