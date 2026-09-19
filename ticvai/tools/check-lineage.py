#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check `handoff/api-data-lineage.json` against the contracts, the schema and the services.

**Twenty-plus tools read the lineage as authoritative and nothing checked it.** It is the
first thing `refresh.sh` runs and the input to `check-package`, `check-screens`,
`derive-relationships`, both workbooks and the viewer — and it is written by a tool that
**adds and never updates**, which is correct for preserving hand judgements and wrong for
anything that moves.

That is not hypothetical. On 19 September, in one day:

  * seven `release*` entries survived a rename to `relinquish*` on 8 September, so the
    lineage claimed 1,981 operations against 1,974 that exist;
  * fifteen operations moved from `retail.yaml` and `games.yaml` into `wallet.yaml` and
    their entries went on naming `retail`, and therefore `RetailService`;
  * twenty-six entries still listed `retail.wallet` in `reads` and `writes` after that
    table became `wallet.wallet`, and **every refresh rebuilt the dropped table from
    them** — through `derive-schema`, which reads the relationship graph, which
    `derive-relationships` rebuilds from the schema the lineage repopulated.

`check-package` caught the first of those. Nothing caught the other two, because no check
compared an entry against the contract that defines it.

## What it checks

  1. Every lineage entry names an operation some contract declares.
  2. Every operation a contract declares has a lineage entry.
  3. The `contract` on an entry is the file that actually defines the operation.
  4. The `service` is the one `service-decomposition.json` names for that contract.
  5. No entry has a null service — `derive-diagrams` sorts on it and raises on `None`.
  6. Every table in `reads`/`writes` exists in `schema-reference.json`.
  7. Every postgres table belongs to exactly one service.

**Coverage is reported, never failed.** A third of operations reach no table, and most of
that is correct — a service-to-service call, a computed projection, a health probe. It is
printed because it is worth watching, not because a number is wrong.
"""
import collections
import glob
import io
import json
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = os.path.join(ROOT, "handoff")
VERBS = ("get", "post", "put", "patch", "delete")
ERRORS, WARNINGS = [], []


def load_json(name, required=True):
    p = os.path.join(H, name)
    if not os.path.exists(p):
        if required:
            ERRORS.append("handoff/%s is missing" % name)
        return {}
    try:
        return json.load(io.open(p, encoding="utf-8"))
    except Exception as e:
        ERRORS.append("handoff/%s is unreadable: %s" % (name, e))
        return {}


def contract_operations():
    """operationId -> contract name, read off the file that declares it."""
    out = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "contracts", "*", "*.yaml"))):
        name = os.path.basename(f)[:-5]
        try:
            d = yaml.safe_load(io.open(f, encoding="utf-8")) or {}
        except yaml.YAMLError as e:
            ERRORS.append("%s does not parse: %s" % (name, e))
            continue
        for _p, m in (d.get("paths") or {}).items():
            if not isinstance(m, dict):
                continue
            for v, op in m.items():
                if v in VERBS and isinstance(op, dict) and op.get("operationId"):
                    out[op["operationId"]] = name
    return out


def main():
    quiet = "--quiet" in sys.argv
    lin = load_json("api-data-lineage.json")
    ref = load_json("schema-reference.json")
    dec = load_json("service-decomposition.json", required=False)
    if not lin:
        print("FAIL - no lineage to check")
        return 1

    ops = contract_operations()
    cols = ref.get("cols") or {}
    svc_of_contract, schema_owner = {}, collections.defaultdict(list)
    for name, s in (dec.get("services") or {}).items():
        for c in (s.get("contracts") or []):
            svc_of_contract[c] = name
        for sch in (s.get("schemas") or []):
            schema_owner[sch].append(name)

    # 1 + 2 — the two sets must be the same set.
    ghosts = sorted(set(lin) - set(ops))
    absent = sorted(set(ops) - set(lin))
    for g in ghosts:
        ERRORS.append("lineage has '%s', which no contract defines — `--apply` never "
                      "removes, so a renamed operation stays forever" % g)
    for a in absent:
        ERRORS.append("'%s' is in a contract and not in the lineage — run "
                      "tools/derive-lineage.py --apply" % a)

    # 3 + 4 + 5 — attribution.
    wrong_contract = wrong_service = null_service = 0
    for o, e in sorted(lin.items()):
        if o not in ops:
            continue
        if e.get("contract") != ops[o]:
            wrong_contract += 1
            ERRORS.append("%s: lineage says contract '%s', it is declared in '%s'"
                          % (o, e.get("contract"), ops[o]))
        if not e.get("service"):
            null_service += 1
            ERRORS.append("%s: no service — derive-diagrams sorts on this and raises on None"
                          % o)
        elif svc_of_contract and ops[o] in svc_of_contract \
                and e["service"] != svc_of_contract[ops[o]]:
            wrong_service += 1
            ERRORS.append("%s: lineage says %s, service-decomposition puts '%s' in %s"
                          % (o, e["service"], ops[o], svc_of_contract[ops[o]]))

    # 6 — a table an operation claims to touch has to exist.
    unknown = collections.Counter()
    for o, e in lin.items():
        for t in list(e.get("reads") or []) + list(e.get("writes") or []):
            if ":" in t:          # cache:idempotency, qdrant:knowledge — not postgres
                continue
            if t not in cols:
                unknown[t] += 1
    for t, n in unknown.most_common():
        ERRORS.append("%d operation(s) read or write '%s', which is in no schema — a table "
                      "that does not exist is rebuilt by derive-schema from these entries"
                      % (n, t))

    # 7 — ownership.
    orphan_tables = [t for t in cols
                     if ":" not in t and not schema_owner.get(t.split(".")[0])]
    if orphan_tables and dec:
        WARNINGS.append("%d table(s) belong to no service — %s%s"
                        % (len(orphan_tables), ", ".join(sorted(orphan_tables)[:5]),
                           "…" if len(orphan_tables) > 5 else ""))
    for sch, owners in sorted(schema_owner.items()):
        if len(owners) > 1:
            ERRORS.append("schema '%s' is claimed by %s — a service that shares a schema is "
                          "not separately deployable" % (sch, " and ".join(owners)))

    # Coverage — reported, never failed.
    no_table = [o for o, e in lin.items() if not (e.get("reads") or e.get("writes"))]
    by_service = collections.Counter(e.get("service") for e in lin.values())

    if not quiet:
        print("  %d lineage entries · %d contract operations · %d tables"
              % (len(lin), len(ops), len(cols)))
        print("  %d service(s) · %d operation(s) reach no table (%.0f%%)"
              % (len(by_service), len(no_table), 100.0 * len(no_table) / max(1, len(lin))))
        print()
        for e in ERRORS[:40]:
            print("  FAIL  %s" % e)
        if len(ERRORS) > 40:
            print("  ... and %d more" % (len(ERRORS) - 40))
        for w in WARNINGS:
            print("  WARN  %s" % w)
        if ERRORS:
            print()

    print("%s — %d error(s), %d warning(s)"
          % ("FAIL" if ERRORS else "PASS", len(ERRORS), len(WARNINGS)))
    return 1 if ERRORS else 0


if __name__ == "__main__":
    sys.exit(main())
