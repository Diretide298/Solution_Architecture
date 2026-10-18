#!/usr/bin/env python3
"""The lineage half of the 18 October answers on storage promises (class 8; CHG-CRA-004).

`tools/derive-lineage.py` adds the tables an operation's schemas persist to and never removes one, so a read or write
the published answers took away, or one an operation makes in prose (through another module's operation), is set
here. The pattern of tools/applied/xdw-routes-14-october.py.

* replayEvents (ADAM CR-140): validates and inserts a `control.webhook_replay` row; it reads no outbox (the workers
  host's dispatcher does) and writes no delivery (the dispatcher does).
* publishTenantConfig (CR-154): raises the review request through approvals' createApprovalRequest
  (`x-ticvai-write-via`), so it writes `approvals.request` by that route.
* setPublishReviewPolicy (CR-154): switching the review on creates the tenant default matrix through
  setApprovalMatrix, so it writes `approvals.matrix` by that route.
* receivePaymentProviderWebhook (CR-165): reads `payments.provider` to check the connection's provider.

Run after `python tools/derive-lineage.py --apply`; a second run changes nothing.

    python tools/applied/promises-kept-18-october.py [--apply]
"""
from __future__ import annotations

import argparse
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# operation -> ({field: (add, remove)}, why)
EDIT = {
    "replayEvents": ({"reads": (["control.webhook_replay"], ["platform.outbox"]),
                      "writes": (["control.webhook_replay"], ["control.webhook_delivery"])},
                     "CHG-CRA-004 (ADAM CR-140): queues a control.webhook_replay row; the workers dispatcher reads "
                     "the outbox and writes the deliveries"),
    "publishTenantConfig": ({"writes": (["approvals.request"], [])},
                            "CHG-CRA-004 (ADAM CR-154): the review request, through createApprovalRequest (writeVia)"),
    "setPublishReviewPolicy": ({"writes": (["approvals.matrix"], [])},
                               "CHG-CRA-004 (ADAM CR-154): the tenant default matrix, through setApprovalMatrix "
                               "(writeVia)"),
    "receivePaymentProviderWebhook": ({"reads": (["payments.provider"], [])},
                                      "CHG-CRA-004 (ADAM CR-165): the connection's provider is checked against the "
                                      "path"),
}


def note(e: dict, text: str) -> None:
    text = "18 October 2026: " + text
    if text not in str(e.get("fixNote") or ""):
        e["fixNote"] = (e["fixNote"] + "; " + text) if e.get("fixNote") else text


def apply(lin: dict) -> int:
    missing = [o for o in EDIT if o not in lin]
    if missing:
        raise SystemExit("not in the lineage (run tools/derive-lineage.py --apply first): " + ", ".join(missing))
    n = 0
    for o, (fields, why) in EDIT.items():
        e = lin[o]
        changed = False
        for k, (add, remove) in fields.items():
            old = list(e.get(k) or [])
            new = sorted((set(old) | set(add)) - set(remove))
            if new != sorted(old):
                e[k] = new
                changed = True
        rc = e.get("readColumns")
        for t in fields.get("reads", ([], []))[1]:
            if isinstance(rc, dict) and t in rc:
                del rc[t]
                changed = True
        if changed:
            note(e, why)
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
