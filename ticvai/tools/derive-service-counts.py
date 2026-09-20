#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Recompute the derived halves of `service-decomposition.json`, and say which schema has no owner.

**`service-decomposition.json` is an authored input and half of it is arithmetic.** The note said
*"32 contracts and 520 tables become 17 deployable services"* while the package held 623, and
`check-authored-inputs` reported it as an issue because a file that states a count is making a
claim that can go stale silently.

Five tools read this file — `derive-diagrams`, `derive-burst-scope`, both workbooks and
`check-package` — and **service allocation is read off it**, so a stale table count is a stale
estimate.

## What is authored and what is arithmetic

    authored      tier, contracts, schemas, why, scale, risk
                  **Which schemas a service owns is a boundary decision** and nothing here
                  touches it
    arithmetic    operations, tables, readsFrom, writesOutside
                  Counted from the contracts and the lineage every run

Same division as `derive-lineage`: a judgement is preserved, a derivation is re-made. **A count
that is remembered rather than re-derived is the drift `derive-relationships` calls the worst
kind, because it looks like progress.**

## The schema with no owner

`pricing` was owned by nothing. Decision 5 of the schema merge took all three `pricing` tables
and said the schema *"needs an owner"*, and that stayed open because the tables had no
operations — a service is inferred from the contract that declares them. The operations were
written on 20 September into `catalogue.yaml`, which answers it: **`pricing` belongs to
CatalogueService**, beside the price lists and products a dynamic rule adjusts.

An unowned schema is reported rather than assigned. **Where a table is deployed is a boundary
decision**, and a tool that picks one by proximity would be guessing at the thing this file
exists to record.

    python3 tools/derive-service-counts.py
    python3 tools/derive-service-counts.py --apply
"""
import collections
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = os.path.join(ROOT, "handoff")
PATH = os.path.join(H, "service-decomposition.json")


def main():
    apply = "--apply" in sys.argv[1:]
    D = json.load(io.open(PATH, encoding="utf-8"))
    S = json.load(io.open(os.path.join(H, "schema-reference.json"), encoding="utf-8"))
    L = json.load(io.open(os.path.join(H, "api-data-lineage.json"), encoding="utf-8"))
    services = D["services"]

    owner_of_schema, owner_of_contract = {}, {}
    for name, sv in services.items():
        for sch in sv.get("schemas") or []:
            owner_of_schema[sch] = name
        for c in sv.get("contracts") or []:
            owner_of_contract[c] = name

    tables = [t for t in (S.get("cols") or {}) if "." in t and ":" not in t]
    schemas = sorted({t.split(".", 1)[0] for t in tables})
    unowned = [s for s in schemas if s not in owner_of_schema]

    # A service's operations are the operations of the contracts it owns.
    ops_by_service = collections.Counter()
    for op, v in L.items():
        svc = owner_of_contract.get(v.get("contract"))
        if svc:
            ops_by_service[svc] += 1
    tables_by_service = collections.Counter()
    for t in tables:
        svc = owner_of_schema.get(t.split(".", 1)[0])
        if svc:
            tables_by_service[svc] += 1

    # **A cross-service read is an operation of one service touching a table of another**, which
    # is the coupling the tiers exist to bound. Counted per operation, not per table: an
    # operation reading three tables of one service is one call, not three.
    reads = collections.defaultdict(collections.Counter)
    writes = collections.defaultdict(collections.Counter)
    for op, v in L.items():
        me = owner_of_contract.get(v.get("contract"))
        if not me:
            continue
        for key, sink in (("reads", reads), ("writes", writes)):
            hit = set()
            for t in (v.get(key) or []):
                if "." not in t or ":" in t:
                    continue
                other = owner_of_schema.get(t.split(".", 1)[0])
                if other and other != me:
                    hit.add(other)
            for o in hit:
                sink[me][o] += 1

    changes = []
    for name, sv in sorted(services.items()):
        for field, new in (("operations", ops_by_service[name]),
                           ("tables", tables_by_service[name])):
            if sv.get(field) != new:
                changes.append("%-22s %-11s %s -> %s" % (name, field, sv.get(field), new))
                sv[field] = new
        for field, src in (("readsFrom", reads), ("writesOutside", writes)):
            new = dict(sorted(src[name].items(), key=lambda kv: (-kv[1], kv[0])))
            if sv.get(field) != new:
                sv[field] = new

    total_ops = sum(ops_by_service.values())
    note = D.get("note") or ""
    want = ("How %d contracts and %d tables become %d deployable services."
            % (len({c for sv in services.values() for c in (sv.get("contracts") or [])}),
               len(tables), len(services)))
    if not note.startswith(want):
        tail = note.split(".", 1)[1] if "." in note else ""
        D["note"] = want + tail
        changes.append("note                   restated: %d tables" % len(tables))

    print("  %d service(s) · %d operation(s) · %d table(s)"
          % (len(services), total_ops, len(tables)))
    if changes:
        print("\n  %d field(s) restated:" % len(changes))
        for c in changes[:24]:
            print("    %s" % c)
    else:
        print("  every derived field already agrees")

    if unowned:
        print("\n  **%d schema(s) belong to no service.** Where a table deploys is a boundary "
              "decision,\n  so this reports rather than assigns:" % len(unowned))
        for s in unowned:
            n = sum(1 for t in tables if t.startswith(s + "."))
            print("      %-16s %d table(s)" % (s, n))

    ghosts = [s for s in owner_of_schema if s not in schemas]
    if ghosts:
        print("\n  %d schema(s) owned by a service and not in the schema reference — a datastore "
              "rather\n  than a Postgres schema, or a name that has moved: %s"
              % (len(ghosts), ", ".join(sorted(ghosts))))

    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    io.open(PATH, "w", encoding="utf-8", newline="\n").write(
        json.dumps(D, indent=1, ensure_ascii=False))
    print("\n  -> handoff/service-decomposition.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
