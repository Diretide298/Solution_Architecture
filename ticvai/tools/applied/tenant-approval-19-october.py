#!/usr/bin/env python3
"""The lineage half of ADAM CR-172 (option (a), decided by Chinmay Parab on 19 October 2026; CHG-CRA-005).

suspendTenant and reactivateTenant raise their own approval request through approvals' createApprovalRequest
(`x-ticvai-write-via`), so each writes `approvals.request` by that route; derive-lineage copies the route into
`writeVia` but records no prose write, so both are set here (the pattern of tools/applied/xdw-routes-14-october.py).

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
WHY = ("19 October 2026: CHG-CRA-005 (ADAM CR-172): raises its own approval request through createApprovalRequest "
       "(writeVia); the change is applied on approval.granted")


def apply(lin: dict) -> int:
    n = 0
    for o in ("suspendTenant", "reactivateTenant"):
        e = lin.get(o)
        if e is None:
            raise SystemExit(f"{o} is not in the lineage (run tools/derive-lineage.py --apply first)")
        writes = sorted(set(e.get("writes") or []) | {"approvals.request"})
        if writes != sorted(e.get("writes") or []) or e.get("writeVia") != ROUTE:
            e["writes"], e["writeVia"] = writes, ROUTE
            if WHY not in str(e.get("fixNote") or ""):
                e["fixNote"] = (e["fixNote"] + "; " + WHY) if e.get("fixNote") else WHY
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
