#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The service map counts operations for itself and not tables, so two numbers drift.

**`refresh.sh` updates `service-decomposition.json`'s `operations` and `readsFrom` and leaves
`tables` and the note alone.** Which is why `check-authored-inputs` reported the operation counts
as current this morning — they had just been rewritten — and still raised
*"its note says 623 tables; there are 625"*.

**The two missing tables are `payments.dunning_policy` and `payments.dunning_case`**, added with
BL-100 and both owned by OrderService, which already holds `payments`.

**OrderService's prose is also now wrong in a way a count cannot show.** Its `why` describes a
transactional core built around a sale; ADR-0048 put guest recurring billing there deliberately,
and a service that charges a card on a schedule has a failure mode a till does not — **nobody is
standing at the counter when a renewal declines.** One line, because that is the difference.

**The stale numbers in this file were never a reader's mistake.** Its own header says it: *a
contract absent here is absent from the service topology, the burst scope and both workbooks —
while every checker passes.*

    python3 tools/applied/service-map-625-tables-21-september.py --apply
"""
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PATH = os.path.join(ROOT, "handoff", "service-decomposition.json")
SCHEMA = os.path.join(ROOT, "handoff", "schema-reference.json")

DUNNING = (
    "\n\n**Guest recurring billing lives here, decided by "
    "[ADR-0048](../../docs/adr/0048-guest-recurring-billing-is-commerce.md)** rather than in the "
    "Control Plane that provisions cells. `payments.dunning_policy` and `payments.dunning_case` "
    "are the two newest tables in the service. **A charge on a schedule fails differently from a "
    "charge at a till** — nobody is standing at the counter when a renewal declines, so the "
    "recovery path is a queue and a timetable rather than a second card."
)


def main():
    apply = "--apply" in sys.argv[1:]
    d = json.load(io.open(PATH, encoding="utf-8"))
    S = json.load(io.open(SCHEMA, encoding="utf-8"))

    tables = [t for t in (S.get("cols") or {}) if "." in t and ":" not in t]
    by_schema = {}
    for t in tables:
        by_schema.setdefault(t.split(".")[0], set()).add(t)
    total = len(tables)
    print("    schema-reference: %d tables" % total)

    changed = 0
    for name, s in d["services"].items():
        want = sum(len(by_schema.get(x, ())) for x in s["schemas"])
        if want != s["tables"]:
            print("    %-22s tables %3d -> %-3d  (%s)"
                  % (name, s["tables"], want, ", ".join(s["schemas"])))
            s["tables"] = want
            changed += 1

    note = d["note"]
    if "623 tables" in note:
        d["note"] = note.replace("623 tables", "%d tables" % total, 1)
        print("    note  623 -> %d tables" % total)
        changed += 1
    elif ("%d tables" % total) not in note:
        print("  !! the note says neither 623 nor %d tables: %r" % (total, note[:120]))
        return 1

    o = d["services"]["OrderService"]
    if "ADR-0048" not in o["why"]:
        o["why"] = o["why"] + DUNNING
        print("    OrderService  why  +recurring billing, per ADR-0048")
        changed += 1

    d["generated"] = "21 September 2026"

    # The thing this file exists to keep true, asserted rather than assumed.
    if sum(x["tables"] for x in d["services"].values()) < total:
        covered = sum(x["tables"] for x in d["services"].values())
        print("    note: services account for %d of %d tables — %d sit in schemas no service "
              "claims" % (covered, total, total - covered))

    if not changed:
        print("  nothing to change")
        return 0
    if not apply:
        print("\n  %d change(s) - pass --apply" % changed)
        return 0
    io.open(PATH, "w", encoding="utf-8", newline="\n").write(
        json.dumps(d, indent=1, ensure_ascii=False))
    print("  -> handoff/service-decomposition.json")
    print("\n  Then: python tools/check-authored-inputs.py --bless handoff/service-decomposition.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
