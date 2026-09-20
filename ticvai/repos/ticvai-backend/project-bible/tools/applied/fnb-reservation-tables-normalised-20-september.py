#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The seventh time this merge has met an `_ids` array with a table beside it.

`fnb.table_reservation.table_ids` is an array of dining tables. `fnb.reservation_table` is that
array as a table, taken from the backend workbook on 20 September. **We took their table and kept
our array**, so the reservation has two answers to the same question and nothing joins them.

This is exactly the case the merge has already decided six times. `audit-array-relationships`
states it:

    The backend team's workbook normalised six of ours and we took all six —
    entry_rule_point, menu_item_modifier, seat_block_item, plan_benefit,
    payment_method_config, tier_module — each because an array cannot carry per-row state.
    access.admission_rules.allowed_access_point_ids is the proof: their entry_rule_point
    IS that array as a table.

## Scored, though the answer is the same as the other six

| | |
|---|---|
| **Maintainability** | **the table.** A reservation seated across three tables that releases one early has nowhere to say so in an array |
| **Readability** | **the table.** `tableIds: [uuid, uuid]` against a row that says which table, when it was assigned and by what |
| **Optimised access** | **the table, and this is the operational one.** *"Which reservations are on table 7 tonight"* is a GIN scan over every reservation against an index seek |
| **DB strain** | **the table.** Adding a table to a party rewrites the reservation row, and a busy outlet reseats constantly |
| **Cross-cell** | none. A reservation and its tables are one outlet |

**`tableIds` is retired rather than deleted.** `x-ticvai-retired-columns` is the package's
mechanism — `control.cell` uses it for `tenant_id` — and it is what stops `derive-schema`
re-creating the column from a relationship edge on the next run.

The reservation now carries `tables`, which is what wires `fnb.reservation_table`: it had no
operation and no inbound reference, and six operations already exist on the reservation that
should have been returning this all along.

**The comment on `tableIds` was right about the thing it was about.** *"Usually empty until
seating. Committing a specific table at booking time refuses later bookings against a constraint
that did not need to exist."* That is still true and it is about *when* tables are assigned, not
about how they are stored — so it moves onto the new field.

    python3 tools/applied/fnb-reservation-tables-normalised-20-september.py --apply
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

OLD = """        tableIds:
          type: array
          description: 'Usually empty until seating. **Committing a specific table at booking time refuses
            later bookings against a constraint that did not need to exist.**

            '
          items:
            type: string
            format: uuid
"""

NEW = """        tables:
          type: array
          description: >
            The dining tables assigned to this reservation, one row each.

            **Usually empty until seating.** Committing a specific table at booking time refuses
            later bookings against a constraint that did not need to exist — that was true of the
            `tableIds` array this replaces and it is still true, because it is about *when* a
            table is assigned rather than how the assignment is stored.

            **Replaces `tableIds`, retired 20 September.** An array cannot carry per-row state,
            which is the same reason this merge took `entry_rule_point`, `menu_item_modifier`,
            `seat_block_item`, `plan_benefit`, `payment_method_config` and `tier_module` from the
            backend workbook. A party seated across three tables that releases one early has
            nowhere to say so in an array, and *"which reservations are on table 7 tonight"* is a
            GIN scan over every reservation instead of an index seek.
          items:
            $ref: '#/components/schemas/FnbReservationTable'
"""

RETIRE = """      x-ticvai-retired-columns:
      - table_ids
"""


def main():
    apply = "--apply" in sys.argv[1:]
    s = io.open(FNB, encoding="utf-8").read()

    if "x-ticvai-retired-columns" in s and "FnbReservationTable'" in s:
        print("  already applied")
        return 0

    if s.count(OLD) != 1:
        print("  !! tableIds block matched %d times" % s.count(OLD))
        return 1
    s = s.replace(OLD, NEW)
    print("    TableReservation  tableIds -> tables[FnbReservationTable]")

    tag = "      x-ticvai-persistence: fnb.table_reservation\n"
    i = s.find(tag)
    if i < 0:
        print("  !! persistence tag not found")
        return 1
    s = s[:i + len(tag)] + RETIRE + s[i + len(tag):]
    print("    fnb.table_reservation  table_ids retired")

    try:
        doc = yaml.safe_load(s)
    except Exception as e:
        print("  !! would not parse: %s" % str(e)[:180])
        return 1
    have = set((doc.get("components") or {}).get("schemas") or {})
    for ref in set(re.findall(r"(?<![\w./-])#/components/schemas/([A-Za-z0-9_]+)",
                              yaml.safe_dump(doc))):
        if ref not in have:
            print("  !! fnb.yaml refs %s and does not define it" % ref)
            return 1
    text_n = len(re.findall(r"^      operationId:", s, re.M))
    parsed_n = sum(1 for p in (doc.get("paths") or {}).values() for o in (p or {}).values()
                   if isinstance(o, dict) and o.get("operationId"))
    if text_n != parsed_n:
        print("  !! %d operationId lines, %d parsed" % (text_n, parsed_n))
        return 1
    print("    parses, refs resolve, no operation discarded")

    # The derived column goes with the contract's.
    sp = os.path.join(H, "schema-reference.json")
    S = json.load(io.open(sp, encoding="utf-8"))
    row = (S.get("cols") or {}).get("fnb.table_reservation") or []
    keep = [c for c in row if c.get("column") != "table_ids"]
    dropped = len(row) - len(keep)
    if dropped:
        S["cols"]["fnb.table_reservation"] = keep
    print("    schema-reference: %d column(s) removed" % dropped)

    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    io.open(FNB, "w", encoding="utf-8", newline="\n").write(s)
    io.open(sp, "w", encoding="utf-8", newline="\n").write(json.dumps(S, ensure_ascii=False))
    print("  -> contracts/satellite/fnb.yaml, handoff/schema-reference.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
