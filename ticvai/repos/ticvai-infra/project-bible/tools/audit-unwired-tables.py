#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tables no operation reads and no operation writes.

**`check-package` rule 36 catches a table written by something and read by nothing.** It does not
catch a table touched by nothing at all, because the rule walks `writes` and a table nobody writes
never enters the loop. That is the larger hole: a written-and-unread table is a half-built
feature, and an untouched table is a schema with no way in or out — closer to a note than a
feature.

**122 tables were in that state on 20 September**, 89 of them added by the schema merge. The merge
took the backend team's columns because their columns were better; it did not take operations,
because they had none to take. So the package gained tables it had argued for and no way to reach
any of them.

## The five states this reports, and only three are work

    storage only                 **already answered.** `handoff/schema-storage-only.md` names the
                                 tables that must have no API and says why for each: a credential
                                 hash, the transactional outbox, a default partition, the
                                 migration runner's own bookkeeping. **That document existed and
                                 nothing read it** - the first run of this tool reported
                                 `identity.authz_audit` as a gap, and it is the one table the
                                 package had most deliberately decided to leave unreachable
    child of a wired parent      **not a defect.** `ledger.journal_line` is read through
                                 `ledger.journal_entry` and always was. Rule 36 already exempts
                                 these and so does this - 41 of the 122
    child of an unwired parent   the parent is the work; the child follows it
    referenced, no parent        something points at it, so a reader will reach it and find
                                 nothing to call
    referenced by nothing        no inbound edge, no parent, no operation. **A table in this
                                 state is either a feature nobody wired or a table that should
                                 not exist**, and only a person can say which

The schema name and contract are reported with each, because that is what an operation would have
to be written against and finding it by hand is most of the work.

    python3 tools/audit-unwired-tables.py
    python3 tools/audit-unwired-tables.py --csv handoff/unwired-tables.csv
"""
import collections
import csv
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = os.path.join(ROOT, "handoff")

TAG = re.compile(r"^    ([A-Za-z0-9_]+):\s*$")
PERSIST = re.compile(r"^      x-ticvai-persistence:\s*(\S+)\s*$")

# `handoff/schema-storage-only.md` is a table of `| `schema.table`[, `schema.table`] | why |`.
BACKTICKED = re.compile(r"`([a-z][a-z0-9_]*\.[a-z][a-z0-9_]*)`")


def storage_only():
    """Tables the package has already decided must have no API, and the reason given.

    **Reading this is the difference between a checker and a re-litigation.** The document says
    why `identity.principal_credential` has no response it belongs in and why
    `orders.sales_order_unassigned` is a default partition rather than a table. Reporting either
    as a missing operation asks a question that was answered, in writing, on purpose.
    """
    p = os.path.join(H, "schema-storage-only.md")
    out = {}
    if not os.path.exists(p):
        return out
    for line in io.open(p, encoding="utf-8"):
        if not line.startswith("|") or line.count("|") < 3:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2 or cells[0].startswith("---") or cells[0] == "Table":
            continue
        for t in BACKTICKED.findall(cells[0]):
            out[t] = cells[1]
    return out


def schema_index():
    """Schema name and contract file for every table a contract declares it persists."""
    out = {}
    for sub in ("spine", "satellite", "shared"):
        d = os.path.join(ROOT, "contracts", sub)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.endswith((".yaml", ".yml")):
                continue
            name = None
            for line in io.open(os.path.join(d, fn), encoding="utf-8"):
                m = TAG.match(line)
                if m:
                    name = m.group(1)
                    continue
                p = PERSIST.match(line)
                if p and name and "." in p.group(1):
                    out.setdefault(p.group(1), (name, "%s/%s" % (sub, fn)))
    return out


def main():
    S = json.load(io.open(os.path.join(H, "schema-reference.json"), encoding="utf-8"))
    L = json.load(io.open(os.path.join(H, "api-data-lineage.json"), encoding="utf-8"))
    G = json.load(io.open(os.path.join(H, "relationship-graph.json"), encoding="utf-8"))
    cols = S.get("cols") or {}
    lineage = S.get("lineage") or {}
    idx = schema_index()
    declared_storage_only = storage_only()

    real = [t for t in cols if "." in t and ":" not in t]
    touched = collections.defaultdict(set)
    for op, v in L.items():
        for k in ("reads", "writes"):
            for t in (v.get(k) or []):
                touched[t].add(op)

    inbound = collections.defaultdict(set)
    for r in (G.get("rels") or []):
        if r.get("frm") and r.get("to") and r["frm"] != r["to"]:
            inbound[r["to"]].add(r["frm"])

    rows = []
    for t in sorted(real):
        if touched.get(t):
            continue
        parent = (lineage.get(t) or {}).get("parent") or ""
        if t in declared_storage_only:
            state = "storageOnly"
        elif parent:
            state = "childOfWiredParent" if touched.get(parent) else "childOfUnwiredParent"
        else:
            state = "referenced" if inbound[t] else "unreferenced"
        schema, contract = idx.get(t, ("", ""))
        rows.append({
            "table": t, "state": state, "columns": len(cols[t]), "parent": parent,
            "inbound": len(inbound[t]), "schema": schema, "contract": contract,
            "referenced_by": " ".join(sorted(inbound[t])[:4]),
            "declared_reason": declared_storage_only.get(t, ""),
        })

    by_state = collections.Counter(r["state"] for r in rows)
    work = [r for r in rows if r["state"] not in ("childOfWiredParent", "storageOnly")]
    print("  %d of %d table(s) are reached by no operation" % (len(rows), len(real)))
    print("    %-24s %3d   already answered in schema-storage-only.md"
          % ("storageOnly", by_state["storageOnly"]))
    print("    %-24s %3d   not a defect — reached through the parent"
          % ("childOfWiredParent", by_state["childOfWiredParent"]))
    for k, label in (("childOfUnwiredParent", "the parent is the work"),
                     ("referenced", "something points at it and will find nothing to call"),
                     ("unreferenced", "no operation, no parent, no inbound edge")):
        print("    %-24s %3d   %s" % (k, by_state[k], label))
    if not work:
        print("\n  PASS — every unreached table is explained")
        return 0

    # **"Needs an operation" is not "needs a verdict".** The 223 schema-merge verdicts are closed
    # and stay closed — whether to accept a table was settled on 20 September. What is open here
    # is how to reach one, which is contract work, and saying "decision" for both invited the
    # reasonable question of which decisions had come untied. None had.
    print("\n  %d still need an operation written, by schema:" % len(work))
    for sch, n in collections.Counter(r["table"].split(".")[0] for r in work).most_common():
        names = [r["table"].split(".", 1)[1] for r in work if r["table"].startswith(sch + ".")]
        print("    %-14s %3d   %s" % (sch, n, ", ".join(sorted(names)[:6])
                                      + (" ..." if n > 6 else "")))

    # **No contract schema and not in the storage-only list is the sharpest case.** The table
    # exists in the reference because `derive-schema` materialises a table from a relationship
    # edge, and the edge exists because a column carries `references` — the two derivers feed
    # each other, which their own comments call "the worst kind of drift". A table in this state
    # is either a storage-only decision nobody wrote down or an artefact of that loop, and the
    # fix for the first is one line in `schema-storage-only.md`.
    missing = [r for r in work if not r["schema"]]
    if missing:
        print("\n  %d have no contract schema and no storage-only entry — either an undocumented "
              "storage decision or an artefact of the derive loop:" % len(missing))
        for r in missing[:10]:
            print("      %-34s %d column(s), %s" % (r["table"], r["columns"],
                                                    r["referenced_by"] or "referenced by nothing"))

    argv = sys.argv[1:]
    if "--csv" in argv:
        out = os.path.join(ROOT, argv[argv.index("--csv") + 1])
        with io.open(out, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        print("\n  -> %s" % os.path.relpath(out, ROOT))
    # **Reporting, not failing.** Whether an untouched table is a missing operation or a table
    # that should not exist is a judgement, and a checker that fails the package on a judgement
    # gets silenced rather than answered.
    return 0


if __name__ == "__main__":
    sys.exit(main())
