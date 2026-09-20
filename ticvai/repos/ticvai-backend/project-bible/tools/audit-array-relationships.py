#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Relationships we store as an array, and what each one costs.

**The backend team's workbook normalised six of ours and we took all six** — `entry_rule_point`,
`menu_item_modifier`, `seat_block_item`, `plan_benefit`, `payment_method_config`, `tier_module`
— each because an array cannot carry per-row state.
`access.admission_rules.allowed_access_point_ids` is the proof: their `entry_rule_point` **is**
that array as a table.

**Their workbook only happened to cover six.** The rest are the same modelling decision and
nobody has looked at them, which is not a merge question — it is ours.

## What an `_ids` array costs

    cannot be joined          a query wanting the rows behind it reads the array, then reads
                              each row, or unnests in SQL the planner cannot use an index for
    cannot carry state        "which seats in this block are released" has nowhere to live,
                              which is exactly why seat_block_item was taken
    rewritten whole           adding one member rewrites the row and every other array on it
    needs a GIN index         for a membership test, and even then the query reads oddly

## What an array is genuinely for

A closed list of values that are not rows: `tags`, `allergens`, `channels`, `blackout_dates`,
`scopes`, `card_schemes`. **Those are not relationships and are not reported.** The test used
here is whether the column's stem names a real table — the same test `derive-relationships`
uses to find a convention edge, so this reports exactly the arrays that *would* be foreign keys
if they were columns.

    python3 tools/audit-array-relationships.py
    python3 tools/audit-array-relationships.py --csv handoff/array-relationships.csv
"""
import collections
import csv
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = os.path.join(ROOT, "handoff")

# A value list, not a relationship, however it is spelled.
VALUE_WORDS = {"tags", "allergens", "dates", "scopes", "codes", "channels", "kinds", "types",
               "placements", "values", "reasons", "fields", "schemes", "currencies", "locales",
               "languages", "permissions", "capabilities", "modules", "features", "roles"}


def stems(tables):
    """The same resolution `derive-relationships` uses: whole name, then unique prefix, then
    unique suffix. If a stem resolves, the array is a relationship wearing an array's clothes."""
    out, prefixes, suffixes = {}, collections.defaultdict(list), collections.defaultdict(list)
    for t in tables:
        short = t.split(".", 1)[1]
        out.setdefault(short, t)
        prefixes[short.split("_")[0]].append(t)
        if "_" in short:
            suffixes[short.split("_", 1)[1]].append(t)
    for head, m in prefixes.items():
        if len(m) == 1 and head not in out:
            out[head] = m[0]
    for tail, m in suffixes.items():
        if len(m) == 1 and tail not in out:
            out[tail] = m[0]
    return out


def main():
    S = json.load(io.open(os.path.join(H, "schema-reference.json"), encoding="utf-8"))
    cols = S.get("cols") or {}
    rg = json.load(io.open(os.path.join(H, "relationship-graph.json"), encoding="utf-8"))
    ops, scr = rg.get("tab_ops") or {}, rg.get("tab_screens") or {}
    tables = [t for t in cols if ":" not in t]
    stem = stems(tables)

    rows = []
    for t in sorted(tables):
        for c in cols[t]:
            ty = (c.get("type") or "")
            if not ty.endswith("[]"):
                continue
            name = c["column"]
            singular = name[:-1] if name.endswith("s") else name
            if name in VALUE_WORDS or singular in VALUE_WORDS:
                continue
            # The stem is what a foreign key would have resolved to.
            base = singular[:-3] if singular.endswith("_id") else None
            if base is None:
                continue
            parts = base.split("_")
            target = next((stem["_".join(parts[i:])] for i in range(len(parts))
                           if "_".join(parts[i:]) in stem), None)
            if not target:
                continue
            o, s = len(ops.get(t, [])), len(scr.get(t, []))
            rows.append({
                "table": t, "column": name, "type": ty, "would_point_at": target,
                "self_reference": "yes" if target == t else "",
                "operations": o, "screens": s, "weight": o + s,
            })

    rows.sort(key=lambda r: (-r["weight"], r["table"]))
    by_table = len({r["table"] for r in rows})
    print("  %d array column(s) on %d table(s) encode a relationship" % (len(rows), by_table))
    print("  (a value list - tags, allergens, channels, blackout dates - is not reported)\n")
    print("  %-44s %-26s %4s %4s" % ("column", "would point at", "ops", "scr"))
    for r in rows[:26]:
        print("  %-44s %-26s %4d %4d%s"
              % (r["table"] + "." + r["column"], r["would_point_at"],
                 r["operations"], r["screens"], "  self" if r["self_reference"] else ""))
    if len(rows) > 26:
        print("  ... %d more" % (len(rows) - 26))

    self_refs = [r for r in rows if r["self_reference"]]
    if self_refs:
        print("\n  %d are self-references — a tree or a graph stored as an array, which is the "
              "shape that hurts most:" % len(self_refs))
        for r in self_refs[:6]:
            print("      %s.%s" % (r["table"], r["column"]))

    argv = sys.argv[1:]
    if "--csv" in argv:
        out = os.path.join(ROOT, argv[argv.index("--csv") + 1])
        with io.open(out, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]) if rows else ["table"])
            w.writeheader()
            w.writerows(rows)
        print("\n  -> %s" % os.path.relpath(out, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
