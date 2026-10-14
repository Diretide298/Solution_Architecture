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
                     its lineage only read, `settleDeposit` named `orders.deposit` and listed it nowhere. A table
                     named only to explain the operation (a contrast, the table another module's operation writes)
                     is listed in `x-ticvai-names-for-context` (CHG-STO-020), held to the text and the lineage
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


def declared(name: str) -> list:
    """`RENAMES` or `COLUMN_RENAMES` from tools/derive-schema-history.py, read without running it."""
    import ast
    try:
        tree = ast.parse((g.ROOT / "tools" / "derive-schema-history.py").read_text(encoding="utf-8"))
    except (OSError, SyntaxError):
        return []
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == name for t in node.targets):
            return ast.literal_eval(node.value)
    return []


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-parameter-columns", RULES)
    lin = g.load_json(g.ROOT / "handoff" / "api-data-lineage.json", {}) or {}
    ref = g.load_json(g.ROOT / "handoff" / "schema-reference.json", {}) or {}
    cols = {t: {c.get("column") for c in v} for t, v in (ref.get("cols") or {}).items()}
    # **A renamed table still answers to the wire's name for it** (CHG-R6-010, 12 October 2026): CR-011 renamed
    # tables and columns on the database side only, so `getSeatHold` keeps `holdId` for `seating.seat_reservation`.
    # The old names a declared rename retired (tools/derive-schema-history.py) count as the table's and column's.
    aka: dict = {}
    for r in declared("RENAMES"):
        aka.setdefault(r["to"], set()).add(str(r["from"]).split(".", 1)[-1])
    for r in declared("COLUMN_RENAMES"):
        cols.setdefault(r["table"], set()).add(r["from"])
    for stem, _rel, doc in g.contracts():
        for path, item in ((doc or {}).get("paths") or {}).items():
            for verb, op in (item or {}).items():
                if verb not in g.VERBS or not isinstance(op, dict) or not op.get("operationId"):
                    continue
                oid = op["operationId"]
                e = lin.get(oid) or {}
                tables = [t for t in (e.get("reads") or []) + (e.get("writes") or []) if ":" not in t and "." in t]
                # a read through the view named for the reader (`<table>_for_<reader>`, DB-READ-VIEWS) reads its
                # table (CHG-R6G-007: publishBundle reads the sale boards through Catalogue's views)
                tables += [b for t in (e.get("reads") or []) for b in [g.viewed_table(t, cols)] if b]
                if not tables:
                    continue
                desc = str(op.get("description") or "")
                # **A table named to explain the operation, which it neither reads nor writes, is declared so**
                # (CHG-STO-020, `x-ticvai-names-for-context`): "not `approvals.sla_policy`, which times an approval",
                # "written by OrderService (`access.entitlement`)". The declaration is held to the text and the
                # lineage: a listed table the description does not name, or the lineage uses, is a finding too.
                context = {str(x) for x in (op.get("x-ticvai-names-for-context") or [])}
                named = set(NAMED.findall(desc))
                for t in sorted(context):
                    if t not in named or t in tables:
                        guard.add("P-NAMED-TABLE", f"{oid}.{t}:context",
                                  f"{stem}.{oid} declares {t} named for context, and "
                                  + ("its lineage uses it" if t in tables else "its description does not name it"))
                for t in sorted(named - context):
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
                pdecl = {str(p.get("name")): p for p in (item.get("parameters") or []) + (op.get("parameters") or [])
                         if isinstance(p, dict) and p.get("name")}
                for n in sorted({str(x) for x in names if x and str(x).endswith("Id")}):
                    col = g.snake(n)
                    base = col[:-3]
                    # a scope id with a role in front (`effectiveForVenueId`) is matched through scope_path too
                    if base in SCOPE or base.split("_")[-1] in SCOPE:
                        continue
                    # **The parameter names the column it matches** (CHG-STO-019): `x-ticvai-column:
                    # <schema>.<table>.<column>`, a column of a table the lineage reads or writes (`templateId` is
                    # `catalogue.plan_benefit.entitlement_template_id`, a path id is its row's `id`); `none` for an id
                    # that selects no row and is an input to what the operation computes (the customer a price
                    # simulation is for), as `x-ticvai-references: none` says a field is not a key.
                    mark = str((pdecl.get(n) or {}).get("x-ticvai-column") or "")
                    if mark == "none":
                        continue
                    if mark:
                        mt, _, mc = mark.rpartition(".")
                        if mt in tables and mc in cols.get(mt, ()):
                            continue
                        guard.add("P-PARAM-NO-COLUMN", f"{oid}.{n}",
                                  f"{stem}.{oid} takes {n}, declared x-ticvai-column {mark}, which is not a column of "
                                  f"a table its lineage reads or writes")
                        continue
                    # A tenant database holds one tenant, so a tenant id there is the database itself; in the
                    # control database, read across tenants, it is a column like any other.
                    if base == "tenant" and not any(t.startswith(("control.", "subscription.")) for t in tables):
                        continue
                    if any(col in cols.get(t, ()) or col + "s" in cols.get(t, ()) for t in tables):
                        continue
                    if any(base in t.split(".", 1)[1] or t.split(".", 1)[1] in base for t in tables):
                        continue
                    if any(base in o or o in base for t in tables for o in aka.get(t, ())):
                        continue
                    guard.add("P-PARAM-NO-COLUMN", f"{oid}.{n}",
                              f"{stem}.{oid} takes {n} and none of {', '.join(sorted(tables))} has {col}")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
