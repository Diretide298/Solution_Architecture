#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Eight payments operations no screen named, four of them added the same morning.

`x-ticvai-consumed-by` is **derived destructively** — `link-screens-contracts.py:120` strips every
block and rewrites it from `screens/`. So an operation the screens do not name loses its
annotation on the next refresh, which is exactly what happened to the four dunning operations
built for BL-100 a few hours earlier: they were written with a consumed-by, and the refresh
removed it because no screen's `apis` list mentioned them.

**Naming them on a screen is the fix; the annotation comes back on its own.**

## Where each lands, and one deliberate refusal

    getDunningPolicy      ADM-606  Partial Payment, Failure & Recovery Manager
    setDunningPolicy      ADM-606
    listDunningCases      ADM-606
    resolveDunningCase    ADM-606

**Not ADM-575 `Failover, Retry & Resilience Manager`, which is where they were first pointed.**
That screen configures `setPaymentFailoverPolicy` — retry *inside* one attempt, seconds, a
different provider. Dunning is retry *across days*, a fresh authorisation on a card that may since
have been replaced. **Putting both on one screen is the conflation the dunning contract was
written to prevent**, and a screen is where an operator would act on it.

    getPaymentRules       ADM-567  Payment Policy, Governance & Approval Manager
    setPaymentRules       ADM-567
    listDepositActivity   BO-327   Deposit, Partial Payment & Outstanding Balance Management
    recordDepositActivity BO-327

    python3 tools/applied/payments-screen-links-21-september.py --apply
"""
import io
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PLACEMENTS = {
    "ADM-606": [
        ("getDunningPolicy", "Read the retry schedule this venue runs", "onLoad"),
        ("setDunningPolicy", "Set attempts, spacing and what happens when they run out", "onSave"),
        ("listDunningCases", "The queue, ordered by attempts remaining", "onLoad"),
        ("resolveDunningCase", "Stop chasing, with a reason", "onAction"),
    ],
    "ADM-567": [
        ("getPaymentRules", "The rules currently in force", "onLoad"),
        ("setPaymentRules", "Amend them", "onSave"),
    ],
    "BO-327": [
        ("listDepositActivity", "What has happened against this deposit", "onLoad"),
        ("recordDepositActivity", "Record a capture, release or adjustment", "onAction"),
    ],
}

FILES = {"ADM-606": "P09-platform-admin-console.yaml",
         "ADM-567": "P09-platform-admin-console.yaml",
         "BO-327": "P08-venue-back-office.yaml"}


def main():
    apply = "--apply" in sys.argv[1:]
    by_file = {}
    for sid, items in PLACEMENTS.items():
        by_file.setdefault(FILES[sid], []).append((sid, items))

    # **Inserted as text, not by re-dumping the document.** `yaml.safe_dump` on
    # `P08-venue-back-office.yaml` would rewrite all 1,182 screens to add two lines to one of
    # them, and a diff nobody can read is a diff nobody reviews. The insert goes at the end of the
    # named screen's existing `apis:` list, which is where the parser would have put it anyway.
    added = 0
    for fname, groups in by_file.items():
        path = os.path.join(ROOT, "screens", fname)
        raw = io.open(path, encoding="utf-8").read()
        lines = raw.split("\n")
        doc = yaml.safe_load(raw)
        index = {s["id"]: s for s in doc["screens"]}

        for sid, items in groups:
            s = index.get(sid)
            if s is None:
                print("  !! %s not found in %s" % (sid, fname))
                return 1
            have = {a.get("operationId") for a in (s.get("apis") or [])}
            todo = [(o, p, t) for o, p, t in items if o not in have]
            for o in items:
                if o[0] in have:
                    print("    %-9s %-24s already named" % (sid, o[0]))
            if not todo:
                continue

            start = next((i for i, l in enumerate(lines) if l == "- id: %s" % sid), None)
            if start is None:
                print("  !! %s: could not locate `- id: %s`" % (fname, sid))
                return 1
            api = next((i for i in range(start, len(lines))
                        if lines[i] == "  apis:"), None)
            nxt = next((i for i in range(start + 1, len(lines))
                        if lines[i].startswith("- id: ")), len(lines))
            if api is None or api > nxt:
                print("  !! %s: %s has no `apis:` block" % (fname, sid))
                return 1
            end = next((i for i in range(api + 1, nxt)
                        if not lines[i].startswith("  - ") and not lines[i].startswith("    ")),
                       nxt)
            block = []
            for oid, purpose, trigger in todo:
                block += ["  - operationId: %s" % oid,
                          "    contract: payments",
                          "    purpose: %s" % purpose,
                          "    trigger: %s" % trigger]
                print("    %-9s +%-24s %s" % (sid, oid, purpose[:42]))
                added += 1
            lines[end:end] = block

        if apply and added:
            out = "\n".join(lines)
            check = yaml.safe_load(out)
            if len(check["screens"]) != len(doc["screens"]):
                print("  !! %s: screen count changed %d -> %d"
                      % (fname, len(doc["screens"]), len(check["screens"])))
                return 1
            io.open(path, "w", encoding="utf-8", newline="\n").write(out)
            print("    -> screens/%s  (%d screens intact)" % (fname, len(check["screens"])))

    # The claim this exists to make true, checked rather than assumed.
    pay = yaml.safe_load(io.open(os.path.join(ROOT, "contracts", "satellite", "payments.yaml"),
                                 encoding="utf-8").read())
    ops = {o["operationId"] for p in (pay.get("paths") or {}).values()
           for o in (p or {}).values() if isinstance(o, dict) and o.get("operationId")}
    placed = {o for items in PLACEMENTS.values() for o, _, _ in items}
    missing = placed - ops
    if missing:
        print("  !! placed operations that payments.yaml does not declare: %s" % sorted(missing))
        return 1
    print("\n    %d placement(s) · all eight resolve to real payments operations" % added)

    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    print("\n  Now run tools/link-screens-contracts.py to restore x-ticvai-consumed-by")
    return 0


if __name__ == "__main__":
    sys.exit(main())
