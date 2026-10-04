#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""An id an operation is addressed or filtered by has a column to match (4 October 2026, CHG-FXC-003).

**Found by the Sprint 1-2 judging of 4 October** (`audit/ticvai/runs/fix-s12/contracts.tsv`).
`listIngredientSubstitutes` is `/recipes/{recipeId}/substitutes` and `fnb.ingredient_substitute` had no `recipe_id`;
`suggestResources` filters by `resourceTypeId` and `resources.resource` had only a fixed `kind`; `getUsageMetering` is
`/tenants/{tenantId}/usage` over a table with no tenant. Each read an id it had nothing to compare with, so the
developer had to invent the column, and nothing in the package compared a parameter with the tables behind it.

  P-PARAM-NO-COLUMN  an `<x>Id` path or query parameter where no table in the operation's lineage has an `<x>_id`
                     (or `<x>_ids`) column and none is named for `<x>` (the operation's own resource)
  P-NAMED-TABLE      a table the operation's own description names (`schema.table`, one the schema reference has)
                     that its lineage neither reads nor writes: `scheduleMenuPublish` creates a `fnb.menu_schedule`
                     its lineage only read, `settleDeposit` named `orders.deposit` and listed it nowhere
  P-DRAFTED-UNMAPPED a drafted workspace write whose request schema still says no table stores its fields while its
                     lineage writes one: `setCodeDistributionManager`, `approveMatrixMultiLevel` and
                     `setPdfPrintablePos` wrote tables with no field mapping, and the developer had to invent one

Scope ids (`venueId`, `regionId`, `brandId`, `countryId`, `scopeId`, `orgUnitId`) are matched through `scope_path` and
are not checked, nor is `tenantId` against a tenant database's own tables (the database is the tenant); nor is an operation whose lineage reaches no table (a computation, a call to another service).

Read-only. Exit 1 on a finding not in `handoff/audit-baseline.json` (tools/audit_guard.py): the known ones are the
backlog, and a new operation must not add to it.

    python3 tools/check-parameter-columns.py [--all] [--update-baseline]
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {
    "P-PARAM-NO-COLUMN": "an <x>Id path or query parameter that no table in the operation's lineage can match "
                         "(Sprint 1-2 judging, 4 October 2026)",
    "P-NAMED-TABLE": "a table the operation's description names that its lineage neither reads nor writes",
    "P-DRAFTED-UNMAPPED": "a drafted write whose request schema says no table stores it while its lineage writes one",
}
NAMED = re.compile(r"`([a-z][a-z0-9_]*\.[a-z][a-z0-9_]*)`")
UNMAPPED = "no existing table"
SCOPE = {"venue", "region", "brand", "country", "scope", "org_unit", "tenant_scope"}


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-parameter-columns", RULES)
    lin = g.load_json(g.ROOT / "handoff" / "api-data-lineage.json", {}) or {}
    ref = g.load_json(g.ROOT / "handoff" / "schema-reference.json", {}) or {}
    cols = {t: {c.get("column") for c in v} for t, v in (ref.get("cols") or {}).items()}
    for stem, _rel, doc in g.contracts():
        for path, item in ((doc or {}).get("paths") or {}).items():
            for verb, op in (item or {}).items():
                if verb not in g.VERBS or not isinstance(op, dict) or not op.get("operationId"):
                    continue
                oid = op["operationId"]
                e = lin.get(oid) or {}
                tables = [t for t in (e.get("reads") or []) + (e.get("writes") or []) if ":" not in t and "." in t]
                if not tables:
                    continue
                desc = str(op.get("description") or "")
                for t in sorted(set(NAMED.findall(desc))):
                    if t in cols and t not in tables:
                        guard.add("P-NAMED-TABLE", f"{oid}.{t}",
                                  f"{stem}.{oid}'s description names {t} and its lineage does not list it")
                body = ((((op.get("requestBody") or {}).get("content") or {}).get("application/json") or {})
                        .get("schema") or {})
                rname = str(body.get("$ref") or "").split("/")[-1]
                rs = (((doc.get("components") or {}).get("schemas") or {}).get(rname) or {}) if rname else {}
                if UNMAPPED in str(rs.get("x-ticvai-persistence") or "") and [t for t in (e.get("writes") or [])
                                                                             if ":" not in t]:
                    guard.add("P-DRAFTED-UNMAPPED", oid,
                              f"{stem}.{oid} writes {', '.join(t for t in e['writes'] if ':' not in t)} and "
                              f"{rname} says no table stores its fields")
                names = [p.get("name") for p in op.get("parameters") or []
                         if isinstance(p, dict) and p.get("in") in ("path", "query")]
                names += re.findall(r"\{(\w+)\}", path)
                for n in sorted({str(x) for x in names if x and str(x).endswith("Id")}):
                    col = g.snake(n)
                    base = col[:-3]
                    if base in SCOPE:
                        continue
                    # A tenant database holds one tenant, so a tenant id there is the database itself; in the
                    # control database, read across tenants, it is a column like any other.
                    if base == "tenant" and not any(t.startswith(("control.", "subscription.")) for t in tables):
                        continue
                    if any(col in cols.get(t, ()) or col + "s" in cols.get(t, ()) for t in tables):
                        continue
                    if any(base in t.split(".", 1)[1] or t.split(".", 1)[1] in base for t in tables):
                        continue
                    guard.add("P-PARAM-NO-COLUMN", f"{oid}.{n}",
                              f"{stem}.{oid} takes {n} and none of {', '.join(sorted(tables))} has {col}")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
