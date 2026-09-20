#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Two tables phase 3 created that phase 1 had already renamed. My deviation caused it.

**Phase 1 declined their `fnb.order` and used `fnb.service_order` instead**, because `order` is
a reserved word in Postgres and `orders.sales_order` had already solved that once. The verdict
still read TAKE THEIRS.

**Phase 3 takes every TAKE THEIRS whose target is not already a table of ours.** `fnb.order` was
not a table of ours — phase 1 had made it `fnb.service_order` — so phase 3 generated it from
their columns, and the package ended up holding both. Same for `fnb.order_item` against
`fnb.service_order_line`.

    fnb.order          12 columns, theirs      fnb.service_order       14 columns, ours
    fnb.order_item     12 columns, theirs      fnb.service_order_line  12 columns, ours

**The collision guard made it harder to see, not easier.** `pascal("fnb.order")` is `FnbOrder`,
which already existed, so the guard appended a suffix and produced `FnbOrderTable` — a distinct
schema name for a table that was not distinct. **A name collision was the signal and the guard
silenced it**; it should have asked whether the two were the same thing.

Found by `audit-array-relationships.py`, which resolved
`marketing.guest_profile.recent_order_ids` to `fnb.order` and made the duplicate visible. The
audit was written for something else.

## What their version adds, which we keep

    fnb.order.sales_order_id    **we had no link from an F&B order to the sales order.**
                                fnb.service_order carried outlet, table visit and kitchen ticket
                                and nothing joining it to what was actually sold
    fnb.order.updated_at        ours has recorded_at and synced_at, both offline-sync fields,
                                and no plain updated_at

`selected_modifiers_json` is not taken: ours is `modifier_option_ids`, and an array is the
better of the two even by the argument this merge has been making against arrays — a json blob
is worse than an array, which is worse than a table. **`fnb.menu_item_modifier` is the table,
and we already accepted it.**

    python3 tools/applied/schema-merge-phase-3c-fnb-duplicate-20-september.py --apply
"""
import io
import json
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
H = os.path.join(ROOT, "handoff")
FNB = os.path.join(ROOT, "contracts", "satellite", "fnb.yaml")

DROP_SCHEMAS = ["FnbOrderTable", "FnbOrderItem"]
DROP_TABLES = ["fnb.order", "fnb.order_item"]

# Into FnbOrder (which persists fnb.service_order), before `grossAmount`.
ADD_TO_ORDER = """        salesOrderId:
          type: string
          format: uuid
          nullable: true
          description: >
            **Taken from their `fnb.order`, 20 September.** We carried outlet, table visit and
            kitchen ticket on an F&B order and nothing joining it to what was actually sold, so
            an F&B line could not be reconciled to the order that paid for it.
        updatedAt:
          type: string
          format: date-time
          nullable: true
          description: >
            Taken from their `fnb.order`. Ours had `recordedAt` and `syncedAt`, which are both
            offline-sync fields, and no plain updated timestamp.
"""


def cut_schema(text, name):
    m = re.search(r"^    %s:\n" % re.escape(name), text, re.M)
    if not m:
        return text, False
    nxt = re.search(r"^    [A-Za-z]", text[m.end():], re.M)
    end = m.end() + (nxt.start() if nxt else len(text) - m.end())
    return text[:m.start()] + text[end:], True


def main():
    apply = "--apply" in sys.argv[1:]
    s = io.open(FNB, encoding="utf-8").read()

    for name in DROP_SCHEMAS:
        s, hit = cut_schema(s, name)
        print("    %-18s %s" % (name, "removed" if hit else "not found"))

    if "salesOrderId" not in s.split("x-ticvai-persistence: fnb.service_order")[-1][:3000]:
        anchor = None
        i = s.find("x-ticvai-persistence: fnb.service_order")
        if i > 0:
            m = re.search(r"^        grossAmount:\n", s[i:], re.M)
            if m:
                anchor = i + m.start()
        if anchor:
            s = s[:anchor] + ADD_TO_ORDER + s[anchor:]
            print("    FnbOrder           +salesOrderId, +updatedAt")
        else:
            print("    !! could not find grossAmount on the service_order schema")

    try:
        yaml.safe_load(s)
    except Exception as e:
        print("    !! fnb.yaml would not parse: %s" % str(e)[:140])
        return 1
    print("    fnb.yaml parses")

    # The derived files cannot drop a table by themselves.
    sp = os.path.join(H, "schema-reference.json")
    S = json.load(io.open(sp, encoding="utf-8"))
    dropped = 0
    for section in ("cols", "origin", "storage", "store", "lineage"):
        d = S.get(section)
        if isinstance(d, dict):
            for t in DROP_TABLES:
                if d.pop(t, None) is not None:
                    dropped += 1
    # `fnb.service_order_line.fnb_order_id` is a leftover parent key from the old name.
    stray = 0
    row = (S.get("cols") or {}).get("fnb.service_order_line") or []
    keep = [c for c in row if c.get("column") != "fnb_order_id"]
    if len(keep) != len(row):
        S["cols"]["fnb.service_order_line"] = keep
        stray = 1
    print("    schema-reference: %d section entr(y/ies) dropped, %d stray parent key removed"
          % (dropped, stray))

    gp = os.path.join(H, "relationship-graph.json")
    G = json.load(io.open(gp, encoding="utf-8"))
    before = len(G.get("rels") or [])
    G["rels"] = [r for r in (G.get("rels") or [])
                 if r.get("frm") not in DROP_TABLES and r.get("to") not in DROP_TABLES
                 and not (r.get("frm") == "fnb.service_order_line" and r.get("col") == "fnb_order_id")]
    for key in ("tab_ops", "tab_screens"):
        for t in DROP_TABLES:
            (G.get(key) or {}).pop(t, None)
    print("    relationship-graph: %d edge(s) dropped" % (before - len(G["rels"])))

    lp = os.path.join(H, "api-data-lineage.json")
    L = json.load(io.open(lp, encoding="utf-8"))
    touched = 0
    for op, v in L.items():
        for k in ("reads", "writes"):
            row = v.get(k)
            if isinstance(row, list) and any(t in row for t in DROP_TABLES):
                v[k] = [t for t in row if t not in DROP_TABLES]
                touched += 1
    print("    lineage: %d entr(y/ies) cleaned" % touched)

    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    io.open(FNB, "w", encoding="utf-8", newline="\n").write(s)
    for path, data in ((sp, S), (gp, G), (lp, L)):
        io.open(path, "w", encoding="utf-8", newline="\n").write(
            json.dumps(data, indent=1 if path != sp else None, ensure_ascii=False))
    print("  -> contracts/satellite/fnb.yaml and three handoff files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
