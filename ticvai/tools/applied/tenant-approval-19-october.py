#!/usr/bin/env python3
"""The lineage half of ADAM CR-172 (option (a), decided by Chinmay Parab on 19 October 2026; CHG-CRA-005).

suspendTenant and reactivateTenant raise their own approval request through approvals' createApprovalRequest
(`x-ticvai-write-via`), so each writes `approvals.request` by that route; derive-lineage copies the route into
`writeVia` but records no prose write, so both are set here (the pattern of tools/applied/xdw-routes-14-october.py).

**The approval request is all either call writes** (fix round 3, lane-H review 2 I-2). The tenant row and the outbox
row are written by Subscription's approval.granted consumer (events/approval-granted.yaml lists control.tenant and
control.outbox), so `control.tenant`, `control.outbox` and `platform.outbox` are removed from the two calls' writes.
derive-lineage never removes a write, and this script runs after it, so a derive cannot bring them back: the event
file no longer names suspendTenant as an emitter, and nothing else derives them. Reads are left alone (both calls
read the tenant for their 409s).

Run after `python tools/derive-lineage.py --apply`; a second run changes nothing.

    python tools/applied/tenant-approval-19-october.py [--apply]
"""
from __future__ import annotations

import argparse
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROUTE = [{"table": "approvals.request", "operation": "createApprovalRequest"}]
# Written by Subscription's approval.granted consumer, never by the two calls (ADAM CR-172, fix round 3).
APPLIED_BY_THE_GRANT = {"control.tenant", "control.outbox", "platform.outbox"}
WHY = ("19 October 2026: CHG-CRA-005 (ADAM CR-172): raises its own approval request through createApprovalRequest "
       "(writeVia); the change is applied on approval.granted")
WHY3 = ("19 October 2026, fix round 3: the approval request is all the call writes; the tenant row and the outbox are "
        "written by Subscription's approval.granted consumer")


def apply(lin: dict) -> int:
    n = 0
    for o in ("suspendTenant", "reactivateTenant"):
        e = lin.get(o)
        if e is None:
            raise SystemExit(f"{o} is not in the lineage (run tools/derive-lineage.py --apply first)")
        writes = sorted((set(e.get("writes") or []) - APPLIED_BY_THE_GRANT) | {"approvals.request"})
        if writes != sorted(e.get("writes") or []) or e.get("writeVia") != ROUTE:
            e["writes"], e["writeVia"] = writes, ROUTE
            for why in (WHY, WHY3):
                if why not in str(e.get("fixNote") or ""):
                    e["fixNote"] = (e["fixNote"] + "; " + why) if e.get("fixNote") else why
            n += 1
    return n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    path = os.path.join(ROOT, "handoff", "api-data-lineage.json")
    raw = io.open(path, encoding="utf-8", newline="").read()
    lin = json.loads(raw)
    n = apply(lin)
    print("lineage entries changed: %d" % n)
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
