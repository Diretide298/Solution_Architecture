#!/usr/bin/env python3
"""One-off, batch STO (Block A storage audit, 14 October 2026): the lineage entries the storage fixes change.
derive-lineage adds entries and never updates one, so an existing entry is edited here. Already applied; kept as the
record of what was changed and why. Idempotent.

* CHG-STO-008 (D-STUB-TABLE): the readers of the three retired stubs read the table that holds the data
  (platform.device for a heartbeat; marketing.message_dispatch for a delivery; a payment's detail has no tip table).

    python3 tools/applied/sto-lineage-14-october.py [--apply]
"""
import json
import sys
from pathlib import Path

# operationId -> {"reads+": [...], "reads-": [...], "writes+": [...], "writes-": [...]}
LINEAGE = {
    # CHG-STO-008
    "getWorkstationHealth": {"reads-": ["platform.device_heartbeat"]},
    "listOrderPaymentDetail": {"reads-": ["orders.payment_tip"]},
    "getCampaignPerformance": {"reads-": ["marketing.message_delivery"]},
}


def main() -> int:
    apply = "--apply" in sys.argv
    tic = Path(__file__).resolve().parents[2]
    path = tic / "handoff" / "api-data-lineage.json"
    raw = path.read_text(encoding="utf-8")
    lin = json.loads(raw)
    n, bad = 0, 0
    for oid, ch in LINEAGE.items():
        e = lin.get(oid)
        if e is None:
            print(f"  ! lineage has no {oid}")
            bad += 1
            continue
        for key in ("reads", "writes"):
            cur = list(e.get(key) or [])
            new = [t for t in cur if t not in set(ch.get(key + "-", []))]
            new = sorted(set(new) | set(ch.get(key + "+", []))) if ch.get(key + "+") else new
            if new != cur:
                print(f"  {oid}.{key}: -{sorted(set(cur) - set(new))} +{sorted(set(new) - set(cur))}")
                e[key] = new
                n += 1
    print(f"  {n} entr(ies) changed, {bad} missing")
    if apply and n:
        indent = 1 if raw.startswith("{\n ") else None
        path.write_text(json.dumps(lin, indent=indent, ensure_ascii=False) + ("\n" if raw.endswith("\n") else ""),
                        encoding="utf-8")
    if not apply:
        print("dry run; pass --apply")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
