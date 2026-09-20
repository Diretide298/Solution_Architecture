#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gap rows whose backlog entry is closed — are they still gaps?

`traceability.json` was written during the requirement walk and **nothing has re-read it since
18 August.** The package has gained 83 operations and lost fifteen tables since, and a row that
said *"needs an operation that does not exist"* is not re-tested by any tool — `check-traceability`
enforces that every gap is *routed*, not that it is still a gap.

**136 rows carry `GAP_CONTRACT` or `CONTRACTED_PARTIAL`. 45 of them route to a backlog entry
whose status is `done`.** Either those rows are stale, or entries were closed before the work
landed, and both possibilities are worth knowing.

## What this can and cannot prove, because the first version got it wrong

A closed entry records `closedBy`, naming the schemas that closed it. The first version of this
tool checked those names against the contracts and called a match proof. **It is not**, and
BL-160 is why.

BL-160's `what` is *"No firmware deployment, no device-to-asset link, and no device enrolment or
retirement lifecycle"* — three gaps. Its `closedBy` describes `RegisteredDevice` gaining
`batteryPercent` and `Workstation` gaining `healthScore`, which is **CF-136, device health, and
not one of the three.** Both schemas resolved because both already existed, and 21 rows were
proposed for closure on that basis.

Checking what the entry *claims to have built* cannot tell a schema that was built from one that
was already there. **So this tool no longer proposes verdicts.** It reports which rows are worth
re-reading and what could be checked about each, and a person closes them.

**It also reports the inverse, which is the more valuable half**: an entry marked `done` whose
stated gaps are still absent from the package. BL-160 is one — device retirement has no
operation and no column joins a device to a `maintenance.asset` — and a backlog entry closed
early takes its traceability rows out of view with it.

    python3 tools/retest-gap-rows.py
"""
import collections
import io
import json
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = os.path.join(ROOT, "handoff")

# A schema name as the backlog prose writes it: `FormDefinition`, Chargeback, FraudRule.
NAME = re.compile(r"`?\b([A-Z][A-Za-z0-9]{3,})\b`?")
# Words that look like schema names and are not.
NOISE = {"August", "September", "Closed", "Built", "Added", "Ready", "The", "This", "And",
         "Chinmay", "Softlabs", "ADR", "Every", "Where", "Both", "Three", "Four", "Two",
         "One", "Not", "None", "TICVAI", "Qossai", "Decision", "Reclassified", "Deferred",
         "Superseded", "Withdrawn", "Raised", "Moved", "Client", "Section", "Previously"}


def contract_schemas():
    out = set()
    for sub in ("spine", "satellite", "shared"):
        d = os.path.join(ROOT, "contracts", sub)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if fn.endswith((".yaml", ".yml")):
                doc = yaml.safe_load(io.open(os.path.join(d, fn), encoding="utf-8").read()) or {}
                out |= set((doc.get("components") or {}).get("schemas") or {})
    return out


def main():
    T = json.load(io.open(os.path.join(H, "traceability.json"), encoding="utf-8"))
    B = json.load(io.open(os.path.join(H, "contract-backlog.json"), encoding="utf-8"))
    entries = {e["id"]: e for e in B["entries"]}
    schemas = contract_schemas()

    gaps = [r for r in T["rows"] if r.get("verdict") in ("GAP_CONTRACT", "CONTRACTED_PARTIAL")]
    by_entry = collections.defaultdict(list)
    for r in gaps:
        if r.get("backlog"):
            by_entry[r["backlog"]].append(r)

    done, still_open = [], 0
    for bl, rows in sorted(by_entry.items()):
        e = entries.get(bl)
        if not e:
            continue
        if e.get("status") != "done":
            still_open += len(rows)
            continue
        claimed = {n for n in NAME.findall(str(e.get("closedBy") or "")) if n not in NOISE}
        done.append((bl, rows, sorted(claimed & schemas)))

    n = sum(len(r) for _, r, _ in done)
    print("  %d gap row(s); %d route to a CLOSED entry, %d to one still open"
          % (len(gaps), n, still_open))
    print()
    print("  **These are review candidates, not closures.** Matching a schema named in")
    print("  `closedBy` cannot tell one that was built from one that was already there.")
    print()
    print("  %-8s %5s  %-40s %s" % ("entry", "rows", "closedBy names in the contracts",
                                    "what the entry said was missing"))
    for bl, rows, hit in sorted(done, key=lambda x: -len(x[1])):
        print("  %-8s %5d  %-40s %s"
              % (bl, len(rows), ", ".join(hit[:3])[:40] or "—",
                 (entries[bl].get("what") or "")[:70]))

    print()
    print("  Nothing is written. A verdict is a judgement made during a requirement walk,")
    print("  and a tool that overwrote one in bulk would destroy the reasoning it holds.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
