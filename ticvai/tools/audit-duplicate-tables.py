#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""An unreached table that is another table under a different name.

**`fnb.order` was found by accident.** `audit-array-relationships.py` resolved
`marketing.guest_profile.recent_order_ids` to a table that should not have existed, and only then
did anyone look. The bug that produced it is not rare and is not specific to F&B:

    phase 3 took every TAKE THEIRS whose target was not already a table of ours,
    and "a table of ours" was tested by NAME.

`fnb.order` was not a name we had. `fnb.service_order` was the thing it was. The same test says
`fnb.product` is missing while `catalogue.product` — 21 columns, **40 operations**, read by twelve
contracts including `fnb` — is the thing it is.

**A table nothing calls is where this lands, every time.** A duplicate cannot be wired, because
the operations it would need already exist and point at the original. So *unreached* and
*duplicate* are the same population seen twice, and checking the unreached ones against the
reached ones is cheap.

## What counts as a candidate

    same short name        `fnb.order` vs `orders.sales_order` does not match on this, but
                           `fnb.product` vs `catalogue.product` does, and so does
                           `retail.price_list` vs `catalogue.price_list`
    column overlap         Jaccard over column names, ignoring the bookkeeping columns every
                           table has. **`id, created_at, updated_at, is_active, scope_path` are
                           on everything** and matching on them would pair every table with
                           every other

**The unreached side must be the suspect and the reached side the original**, never the reverse:
a table with forty operations is not the copy.

## The signal that settles it

**Does the suspect's own schema already read the twin?** `fnb` operations read
`catalogue.product` and `catalogue.price` today. A domain that already reads a table does not
need a private copy of it, and that fact is worth more than any column comparison — it is the
difference between two tables that resemble each other and one table that was already doing the
job.

Column overlap is the weakest of the three signals and must not be the tiebreak. **A richer twin
shares proportionally less**: `catalogue.product` carries a lifecycle, an entitlement template
and an approval, so it overlaps `fnb.product` on nothing once the bookkeeping columns are
dropped, while `rental.product` — five operations, no relation — scored higher. Ranking on
overlap named the wrong original in the first run of this tool.

    python3 tools/audit-duplicate-tables.py
    python3 tools/audit-duplicate-tables.py --csv handoff/duplicate-candidates.csv
"""
import collections
import csv
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = os.path.join(ROOT, "handoff")

# On almost every table, so they carry no evidence of sameness.
BOILERPLATE = {"id", "created_at", "updated_at", "is_active", "scope_path", "venue_id",
               "tenant_id", "created_by_principal_id", "deleted_at", "notes", "code", "name",
               "description", "status", "sort_order", "display_order"}

FLOOR = 0.34

# **How much of the SUSPECT the original covers, which is not the same question as overlap.**
# `identity.user_access` is `identity.delegated_access` with six columns missing, and Jaccard
# scored it 0.26 — under the floor — because the rich original is punished for being rich. The
# shape being hunted is containment: a poor table wholly inside a well-used one.
CONTAINED = 0.6


def stem(col):
    """Compare `permission_id` with `permission`, and `granted_by_principal_id` with `granted_by`.

    **Three of the strongest signals scored zero for being spelled differently.** A foreign key
    and the thing it names are the same column to a reader, and `_principal` is this package's
    way of saying which kind of id — `granted_by_principal_id` against `granted_by` is one
    column, not two.
    """
    c = col[:-3] if col.endswith("_id") else col
    return c.replace("_principal", "")


def main():
    S = json.load(io.open(os.path.join(H, "schema-reference.json"), encoding="utf-8"))
    L = json.load(io.open(os.path.join(H, "api-data-lineage.json"), encoding="utf-8"))
    cols = S.get("cols") or {}
    lineage = S.get("lineage") or {}

    ops = collections.defaultdict(set)
    # Which schemas' operations already touch a table — `fnb` reads `catalogue.product`.
    readers = collections.defaultdict(set)
    for op, v in L.items():
        contract = v.get("contract") or ""
        for k in ("reads", "writes"):
            for t in (v.get(k) or []):
                ops[t].add(op)
                if contract:
                    readers[t].add(contract)

    real = [t for t in cols if "." in t and ":" not in t]
    names = {t: {c["column"] for c in cols[t]} for t in real}
    sig = {t: {stem(c) for c in names[t]} - {stem(b) for b in BOILERPLATE} for t in real}
    short = {t: t.split(".", 1)[1] for t in real}

    # A child read through its parent is reached; it is not a candidate for being a copy.
    def reached(t):
        if ops.get(t):
            return True
        p = (lineage.get(t) or {}).get("parent")
        return bool(p and ops.get(p))

    # **A storage-only table is answered, not a suspect.** `schema-storage-only.md` says why
    # `identity.authz_audit` has no API; pairing it with a table that does have one asks a
    # question that document already closed.
    import re as _re
    storage = set()
    _p = os.path.join(H, "schema-storage-only.md")
    if os.path.exists(_p):
        for line in io.open(_p, encoding="utf-8"):
            if line.startswith("|") and line.count("|") >= 3:
                c = [x.strip() for x in line.strip().strip("|").split("|")]
                if len(c) >= 2 and not c[0].startswith("---") and c[0] != "Table":
                    storage.update(_re.findall(r"`([a-z][a-z0-9_]*\.[a-z][a-z0-9_]*)`", c[0]))

    # **A two-column table is contained in everything.** `platform.sale_board_tile` is `id` and
    # `page_id`; once the boilerplate goes it has one column left, and one column inside a
    # fifteen-column table scores a perfect containment while meaning nothing.
    MIN_SIGNATURE = 3
    suspects = [t for t in real
                if not reached(t) and t not in storage and len(sig[t]) >= MIN_SIGNATURE]
    originals = [t for t in real if ops.get(t)]

    def domain_reads(schema, table):
        """`marketing-crm` is the contract and `marketing` the schema, so this is lenient."""
        return any(c == schema or c.startswith(schema + "-") or schema.startswith(c)
                   for c in readers.get(table, ()))

    rows = []
    for a in sorted(suspects):
        a_schema = a.split(".", 1)[0]
        best = []
        for b in originals:
            if b == a:
                continue
            same_name = short[a] == short[b]
            inter = sig[a] & sig[b]
            union = sig[a] | sig[b]
            j = (len(inter) / len(union)) if union else 0.0
            # **Containment is the second test and it catches what Jaccard cannot.**
            covered = (len(inter) / len(sig[a])) if sig[a] else 0.0
            if not same_name and j < FLOOR and covered < CONTAINED:
                continue
            already = domain_reads(a_schema, b)
            best.append((same_name, already, len(ops[b]), round(max(j, covered), 3), b,
                         sorted(inter), round(covered, 3)))
        if not best:
            continue
        # **Name, then whether the domain already reads it, then operation count.** Overlap is
        # last and never decides: a richer twin shares proportionally less.
        best.sort(key=lambda x: (-int(x[0]), -int(x[1]), -x[2], -x[3]))
        same_name, already, n, j, b, inter, covered = best[0]
        rows.append({
            "suspect": a, "suspect_columns": len(names[a]),
            "original": b, "original_columns": len(names[b]), "original_operations": n,
            "same_short_name": "yes" if same_name else "",
            "domain_already_reads_it": "yes" if already else "",
            "column_overlap": j, "suspect_covered": covered,
            "shared": " ".join(inter[:8]),
            "other_candidates": " ".join(x[4] for x in best[1:4]),
        })

    rows.sort(key=lambda r: (-int(bool(r["domain_already_reads_it"])),
                             -int(bool(r["same_short_name"])), -r["original_operations"]))
    exact = [r for r in rows if r["same_short_name"]]
    print("  %d unreached table(s) checked against %d reached one(s)" % (len(suspects),
                                                                        len(originals)))
    if not rows:
        print("  PASS — none of them is a reached table under another name")
        return 0
    settled = [r for r in rows if r["domain_already_reads_it"]]
    print("  %d look like a table that already exists, %d by name, **%d where the suspect's own "
          "domain\n  already reads the twin**:\n" % (len(rows), len(exact), len(settled)))
    print("  %-32s %-32s %4s %6s  %s" % ("unreached", "already exists as", "ops", "shared",
                                         "evidence"))
    for r in rows[:30]:
        ev = []
        if r["domain_already_reads_it"]:
            ev.append("%s already reads it" % r["suspect"].split(".", 1)[0])
        if r["same_short_name"]:
            ev.append("same name")
        print("  %-32s %-32s %4d %6s  %s"
              % (r["suspect"], r["original"], r["original_operations"],
                 r["column_overlap"], ", ".join(ev)))
    if len(rows) > 30:
        print("  ... %d more" % (len(rows) - 30))

    print("\n  **An unreached table with a reached twin cannot be wired.** The operations it "
          "would\n  need exist and point at the twin, so the question is not what to call it — "
          "it is\n  whether the twin is missing a column or the table is missing a reason.")

    argv = sys.argv[1:]
    if "--csv" in argv:
        out = os.path.join(ROOT, argv[argv.index("--csv") + 1])
        with io.open(out, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        print("\n  -> %s" % os.path.relpath(out, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
