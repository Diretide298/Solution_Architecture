#!/usr/bin/env python3
"""Derive table columns from the contract schemas.

    python3 tools/derive-schema.py            # updates handoff/schema-reference.json
    python3 tools/derive-schema.py --dry-run

A schema carrying `x-ticvai-persistence: "orders.payment"` says which table it lands in. Its
properties become that table's columns. Nothing here is typed.

**This tool did not exist until 18 August**, which is why it matters. The schema reference was
derived once by an ad-hoc script and then hand-patched, so **76 of 287 tables had no columns** —
every table belonging to a contract written after that run, including all 13 `ai.*` tables. The
workbook showed them as rows with nothing in them, and nothing failed, because a table with no
columns is not an error to any checker that only asks whether the table exists.

Names convert camelCase to snake_case, which is the convention the existing 211 already follow.
Types map from OpenAPI to Postgres. A `$ref` to another persisted schema becomes a `_id` column;
a `$ref` to an enum becomes text; an array of objects is a child table's business and is skipped
rather than flattened into jsonb, because a nested array silently becoming a column is how a
child table goes missing.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

# **The last line of this tool crashed on Windows** — a `→` in the closing print against a
# cp1252 console, after the file had already been written. Every other deriver carries this guard;
# this one did not, so the tool reported a traceback on a run that had succeeded.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"
HANDOFF = ROOT / "handoff"

TYPE_MAP = {
    ("string", "uuid"): "uuid",
    ("string", "date-time"): "timestamptz",
    ("string", "date"): "date",
    ("string", "time"): "time",
    ("string", "password"): "text",
    ("string", "email"): "text",
    ("string", "uri"): "text",
    ("string", None): "text",
    ("integer", "int64"): "bigint",
    ("integer", None): "integer",
    ("number", None): "numeric",
    ("boolean", None): "boolean",
    ("object", None): "jsonb",
}


def snake(name: str) -> str:
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s).lower()


def load_contracts() -> dict[str, tuple[str, dict]]:
    out = {}
    for tier in ("spine", "satellite", "shared"):
        d = CONTRACTS / tier
        if not d.exists():
            continue
        for f in sorted(d.glob("*.yaml")):
            out[f.stem] = (tier, yaml.safe_load(f.read_text(encoding="utf-8")) or {})
    return out


def resolve_type(spec: dict, schemas: dict, persisted: dict) -> tuple[str, str | None]:
    """Return (postgres type, referenced table or None)."""
    if not isinstance(spec, dict):
        return "text", None

    ref = spec.get("$ref")
    if not ref and "allOf" in spec:
        for part in spec["allOf"]:
            if isinstance(part, dict) and part.get("$ref"):
                ref = part["$ref"]
                break
    if ref:
        name = ref.rsplit("/", 1)[-1]
        if name in persisted:
            return "uuid", persisted[name]
        target = schemas.get(name)
        if isinstance(target, dict):
            if "enum" in target:
                return "text", None
            # **A value object may declare the column it becomes.** 24 August: every column typed
            # `Money` was landing as `jsonb` — 129 of them — while `orders.cash_movement.amount`
            # was `numeric(18,4)` because somebody hand-typed it. **A jsonb price cannot be summed
            # in SQL**, so every total and variance moved into application code, and a shift
            # variance computed in .NET against a ledger computed in Postgres is two answers to
            # one question.
            #
            # `x-ticvai-persistence-column` is how a shared object says what it stores as. For
            # `Money` that is the amount alone: **currency and scale are region-scoped
            # (ADR-0018) and resolve from the scope walk**, so storing AED against nine million
            # rows in a UAE region is nine million copies of a fact that cannot differ.
            col = target.get("x-ticvai-persistence-column")
            if col:
                return col, None
            if target.get("type") == "object":
                return "jsonb", None
        # A shared object with no declared column stays jsonb — splitting it would guess at an
        # invariant nobody wrote down.
        return "jsonb", None

    t = spec.get("type")
    if t == "array":
        items = spec.get("items") or {}
        if isinstance(items, dict) and (items.get("type") == "object" or items.get("$ref")):
            return "", None          # a child table, not a column
        return "text[]", None
    if "enum" in spec:
        return "text", None
    return TYPE_MAP.get((t, spec.get("format")), TYPE_MAP.get((t, None), "text")), None



def retired_of(body) -> list[str]:
    """Columns a schema used to describe and has deliberately stopped describing.

    **Deleting a property is not enough to delete a column.** `Cell.tenantId` came out of the
    contract for ADR-0038 and `control.cell.tenant_id` survived it twice over: the merge below
    keeps any column whose source is not this contract, and the relationship graph re-creates it
    from an edge the graph derived from the column in the first place. The graph is generated from
    `schema-reference.json` in the next step of `refresh.sh`, so the loop feeds itself and a
    contract-side deletion can never reach the table.

    **A column that cannot be removed is worse than one that was never added**: it validates, it
    reaches the workbook and the DDL, and it goes on asserting the rule the ADR replaced.

    Read from the same branches as the persistence tag, because a schema composed with `allOf`
    carries both in the same place.
    """
    out: list[str] = []
    if not isinstance(body, dict):
        return out
    for src in [body] + [b for b in (body.get("allOf") or []) if isinstance(b, dict)]:
        v = src.get("x-ticvai-retired-columns")
        if isinstance(v, list):
            out += [str(x) for x in v]
    return out


def persistence_of(body) -> str | None:
    """The persistence tag, wherever it sits.

    **A schema composed with `allOf` carries its tag on the branch that adds the stored fields**,
    not at the top level — `Release` is `CreateReleaseRequest` plus an object holding `id`,
    `status` and `createdAt`, and the tag naming `control.release + control.release_component`
    lives on that second branch.

    Reading only the top level gave `control.release` **one column**, in the middle of the
    deployment surface, while every other parent-and-child pair in the package derived correctly.
    **It was the only broken one**, which is why it read as a stub rather than as a bug.
    """
    if not isinstance(body, dict):
        return None
    t = body.get("x-ticvai-persistence")
    if isinstance(t, str):
        return t
    for branch in (body.get("allOf") or []):
        if isinstance(branch, dict) and isinstance(branch.get("x-ticvai-persistence"), str):
            return branch["x-ticvai-persistence"]
    return None



def properties_of(body, schemas: dict | None = None, _seen=None) -> dict:
    """Properties, flattened across `allOf`.

    **`Release` is `CreateReleaseRequest` plus an object.** Its own `properties` at the top level
    is empty, so reading only there gave `control.release` one column while every other
    parent-and-child pair in the package derived correctly — it was the only broken one, which is
    why it read as a stub rather than as a bug.

    **Later branches win.** An `allOf` that redeclares a field is narrowing it, and the narrower
    statement is the one that should reach the column.
    """
    if not isinstance(body, dict):
        return {}
    _seen = _seen or set()
    out = dict(body.get("properties") or {})
    for branch in (body.get("allOf") or []):
        if not isinstance(branch, dict):
            continue
        # **A branch may be a `$ref` to the base schema, and that is where the key lives.**
        # `StockMovement` is `CreateStockMovementRequest` plus an object of derived fields —
        # flattening only the inline branch gave eleven columns and no `id`, so `check-package`
        # reported a row nothing can address. **The check was right and the flattening was half
        # done.**
        ref = branch.get("$ref")
        if ref and schemas is not None:
            name = ref.split("/")[-1]
            if name not in _seen:
                out.update(properties_of(schemas.get(name), schemas, _seen | {name}))
            continue
        out.update(properties_of(branch, schemas, _seen))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    contracts = load_contracts()
    all_schemas: dict[str, dict] = {}
    persisted: dict[str, str] = {}          # schema name -> table
    owner: dict[str, str] = {}              # table -> contract
    retired: dict[str, set[str]] = {}       # table -> columns the contract has withdrawn
    for name, (_, doc) in contracts.items():
        for sname, body in ((doc.get("components") or {}).get("schemas") or {}).items():
            all_schemas.setdefault(sname, body)
            if isinstance(body, dict):
                table = persistence_of(body)
                if isinstance(table, str) and "." in table and "—" not in table:
                    # A schema may name a parent and a child — `fnb.service_order + fnb.service_order_line`.
                    # **The properties belong to the parent**; the child comes from the nested array,
                    # which this tool deliberately skips rather than flattening. Taking the whole
                    # string as a table name created 25 tables that do not exist.
                    table = table.split("+")[0].strip()
                    persisted[sname] = table
                    owner[table] = name
                    for rc in retired_of(body):
                        retired.setdefault(table, set()).add(rc)

    # The relationship graph knows where a column points; the column did not say so. On 18 August
    # **all 514 relationships were invisible at column level** — `facility_id` on
    # `access.parking_entitlement` is a bare `uuid` in the contract, and the only record that it
    # points at `access.parking_facility` lived in a separate file. A reader looking at the column
    # in the workbook saw a uuid and nothing else.
    #
    # Contracts express almost none of these as `$ref` — 486 of 514 are conventions rather than
    # declared references — so the graph is the source and the column is annotated from it.
    graph_path = HANDOFF / "relationship-graph.json"
    edges: dict[tuple[str, str], dict] = {}
    if graph_path.exists():
        for r in json.loads(graph_path.read_text(encoding="utf-8")).get("rels", []):
            if r.get("to"):
                edges[(r["frm"], r["col"])] = r

    ref_path = HANDOFF / "schema-reference.json"
    S = json.loads(ref_path.read_text(encoding="utf-8"))
    existing = S.get("cols", {})

    # A `+`-separated persistence names a parent and a child: `orders.sales_order + orders.order_line`.
    # The parent's properties were taken and **the child was registered and never filled** — on
    # 18 August that left 31 tables carrying nothing but a foreign key. `identity.role_permission`
    # had `role_id` alone: **a join table that joins to nothing**, found by Hrushikant in review and
    # missed by the schema audit that ran the same day.
    #
    # **The audit asked whether every table had columns, a relationship and an owner, and this table
    # had all three.** What it never asked is whether one column can do the job the name claims.
    #
    # The child's columns come from the array property whose items are objects — that array *is* the
    # child rows, which is why it was skipped as a column in the first place.
    child_of: dict[str, tuple[str, str]] = {}
    for name, (_, doc) in contracts.items():
        for sname, body in ((doc.get("components") or {}).get("schemas") or {}).items():
            raw = persistence_of(body)
            if not isinstance(raw, str) or "+" not in raw or "—" in raw:
                continue
            parts = [x.strip() for x in raw.split("+")]
            for child in parts[1:]:
                if "." in child:
                    child_of[child] = (sname, parts[0])
                    owner[child] = name

    # A child table may also be implied rather than declared. `identity.role_permission` is named
    # by the lineage, described in prose and used by an operation, and **no schema declares it** —
    # its rows are `Role.permissions`, returned nested inside the parent.
    #
    # Where a known table is `<parent>_<thing>` and a schema persists to `<parent>` carrying an
    # array called `<thing>`, that array is the child's rows. **31 tables carried nothing but a
    # foreign key before this ran.**
    known_tables = set(S.get("storage") or {}) | set(existing)
    # **A table that a schema declares outright is not an implied child.** 24 August:
    # `RolePermission` was written with `x-ticvai-persistence: identity.role_permission`, and this
    # rule still fired on the `role_` prefix and unioned `Role`'s own columns into it — so the
    # grant table carried `is_system`, `principal_count` and `grant_count`.
    #
    # **The rule exists for tables nobody declared** and it has to yield to anybody who did.
    declared = {t for t in persisted.values() if isinstance(t, str)}
    for table in sorted(known_tables):
        if table in child_of or table in declared or "." not in table or ":" in table:
            continue
        schema_part, _, name = table.partition(".")
        for sname, ptable in persisted.items():
            short = ptable.split(".")[-1]
            if ptable == table or not name.startswith(short + "_"):
                continue
            tail = name[len(short) + 1:]
            body = all_schemas.get(sname) or {}
            for prop, spec in properties_of(body, all_schemas).items():
                if not (isinstance(spec, dict) and spec.get("type") == "array"):
                    continue
                if snake(prop).rstrip("s") != tail.rstrip("s"):
                    continue
                child_of[table] = (sname, ptable)
                break
            if table in child_of:
                break

    derived: dict[str, list[dict]] = {}
    standalone_wins: set = set()
    parent_key: dict = {}
    for child, (parent_schema, parent_table) in sorted(child_of.items()):
        body = all_schemas.get(parent_schema) or {}
        # the array of objects on the parent — the rows of the child
        arrays = [(k, v) for k, v in properties_of(body, all_schemas).items()
                  if isinstance(v, dict) and v.get("type") == "array"
                  and isinstance(v.get("items"), dict)]
        if not arrays:
            continue
        # the array whose name best matches the child's own name
        tail = child.split(".")[-1].replace(parent_table.split(".")[-1] + "_", "")
        key, spec = max(arrays, key=lambda kv: len(set(snake(kv[0])) & set(tail)))
        items = spec["items"]
        if "$ref" in items:
            resolved = all_schemas.get(items["$ref"].split("/")[-1])
            # **An array of enums is a value list, not a nested object.** `Role.permissions` is
            # `[Permission]`, and the child row is (role_id, permission) — two columns, which is
            # exactly what a join table is.
            if resolved and resolved.get("type") == "string":
                items = {"properties": {snake(key).rstrip("s"): {
                    "type": "string",
                    "description": f"One value from {items['$ref'].split('/')[-1]}.",
                }}, "required": [snake(key).rstrip("s")]}
            else:
                items = resolved or {}
        elif items.get("type") in ("string", "integer", "number"):
            items = {"properties": {snake(key).rstrip("s"): dict(items)},
                     "required": [snake(key).rstrip("s")]}
        # **`allOf` has to be flattened here too.** `OrderLine` is `CreateOrderLine` plus a server
        # block, so `items.properties` is empty and the child pass produced one column — the parent
        # key alone — which `len(cols) > 1` then discarded. **The result was `order_line` with no
        # `order_id`**, while its sibling `cart_line` had `cart_id`, and nothing compared them.
        if "allOf" in items:
            merged_props, merged_req = {}, set(items.get("required") or [])
            for part in items["allOf"]:
                if "$ref" in part:
                    part = all_schemas.get(part["$ref"].split("/")[-1]) or {}
                merged_props.update(part.get("properties") or {})
                merged_req |= set(part.get("required") or [])
            items = {"properties": merged_props, "required": sorted(merged_req)}

        req = set(items.get("required") or [])
        # **Where a schema persists to one table and carries an array of that table's own rows,
        # the child is the parent.** `NavigationConfig` persists to `whitelabel.navigation_item`
        # and holds `items[]` of navigation items — there is no second table, so a parent key
        # would be `navigation_item_id` on `navigation_item`, pointing at the row it sits on.
        #
        # Emit no parent key and let the array's own `id` be the key. Caught by the key check
        # added the same hour, after two narrower fixes each replaced one defect with another.
        parent_cols = [] if parent_table == child else [{
            "column": snake(parent_table.split(".")[-1]) + "_id",
            "type": "uuid", "required": "yes",
            "source": f"{owner.get(child, '')}.{parent_schema}.{key}",
            "description": f"The parent row. Derived from {parent_schema}.{key}.",
            "table": child, "references": parent_table,
        }]
        cols = list(parent_cols)
        for prop, pspec in (items.get("properties") or {}).items():
            ptype, fk = resolve_type(pspec, all_schemas, persisted)
            if not ptype:
                continue
            cols.append({
                "column": snake(prop), "type": ptype,
                "required": "yes" if prop in req else "no",
                "source": f"{owner.get(child, '')}.{parent_schema}.{key}[].{prop}",
                "description": (pspec.get("description") or "").strip().replace("\n", " ")[:220]
                if isinstance(pspec, dict) else "",
                "table": child,
                **({"references": fk} if fk else {}),
            })
        # **A table cannot be its own parent.** `whitelabel.navigation_item` derived a
        # `navigation_item_id` referencing itself on 20 August — a key that points at the row it
        # is on, which is not a link, and it left the table with no way to reach its real parent.
        # **A table cannot be its own parent.** `whitelabel.navigation_item` derived a
        # `navigation_item_id` referencing itself on 20 August — a key pointing at the row it is
        # on, which is not a link.
        #
        # **Drop the false parent key, not the row's own `id`.** The first cut removed the whole
        # first column and took the id with it, which turned a self-reference into a table with no
        # key at all — a worse defect than the one being fixed, and my own key check caught it.
        if cols and cols[0].get("references") == child and cols[0]["column"] != "id":
            cols = cols[1:]

        if len(cols) > 1:
            derived[child] = cols
            # **A table declared twice loses its parent key.** `orders.order_line` is both a
            # standalone `OrderLine` schema and the child half of `orders.sales_order +
            # orders.order_line`, and the standalone pass overwrites this one — so the line kept
            # its variant and performance and lost `order_id`.
            #
            # Its sibling `cart_line` carries `cart_id` and nothing flagged the difference: **a
            # line with no order is a row nobody can join, and the ER diagram simply drew it
            # floating.** Found on 20 August by a reviewer looking at the picture.
            standalone_wins.discard(child)
            parent_key[child] = cols[0]

    for sname, table in sorted(persisted.items()):
        body = all_schemas.get(sname) or {}
        required = set(body.get("required") or [])
        cols = []
        for prop, spec in properties_of(body, all_schemas).items():
            # **`x-ticvai-persisted: false` is a field that travels and is not stored.** 24 August:
            # `currency` and `currencyScale` sat on `orders.pos_shift`, `orders.sales_order`,
            # `platform.workstation` and `catalogue.price_list` — four tables whose value can only
            # ever be the region's (ADR-0018). **Storing AED against nine million rows in a UAE
            # region is nine million copies of a fact that cannot differ**, and a workstation with
            # its own currency is a workstation somebody can misconfigure into a mismatch with the
            # ledger it posts to.
            #
            # **It stays on the wire**: a client reading a figure should not walk a hierarchy to
            # know what it means. Four tables genuinely differ from their region and keep a stored
            # currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.account`,
            # `control.partner_agreement`. A guest paying USD at an AED venue is a real row.
            if isinstance(spec, dict) and spec.get("x-ticvai-persisted") is False:
                continue
            ptype, fk = resolve_type(spec, all_schemas, persisted)
            if not ptype:
                continue
            cols.append({
                "column": snake(prop),
                "type": ptype,
                "required": "yes" if prop in required else "no",
                "source": f"{owner.get(table, '')}.{sname}.{prop}",
                "description": (spec.get("description") or "").strip().replace("\n", " ")[:220]
                if isinstance(spec, dict) else "",
                "table": table,
                **({"references": fk} if fk else {}),
            })
        if table in parent_key and not any(c["column"] == parent_key[table]["column"] for c in cols):
            cols.insert(0, dict(parent_key[table]))
        for c in cols:
            e = edges.get((table, c["column"]))
            if e:
                c["references"] = e["to"]
                c["referenceKind"] = e.get("edgeKind", "reference")
                # How the link was established, because 486 of 514 are conventions rather than
                # declared references and a reader should know which they are looking at.
                c["referenceHow"] = e.get("how", "convention")
                c["enforced"] = "yes" if e.get("how") == "declared" else "no"
        if cols:
            # **Merge, do not overwrite.** `orders.order_line` is declared twice — standalone as
            # `OrderLine` and as the child half of `orders.sales_order + orders.order_line` — and
            # the standalone schema carries no properties at all, so overwriting dropped the
            # `order_id` the child pass had just derived.
            #
            # Its sibling `cart_line` has `cart_id` and nothing flagged the difference. **A line
            # with no order is a row nobody can join**, and the ER diagram drew it floating.
            prior = derived.get(table)
            if prior:
                have = {c["column"] for c in cols}
                cols = [c for c in prior if c["column"] not in have] + cols
            derived[table] = cols

    filled = [t for t in derived if not existing.get(t)]
    changed = [t for t in derived if existing.get(t) and len(existing[t]) != len(derived[t])]
    untouched = [t for t in existing if t not in derived]

    print(f"{len(persisted)} persisted schemas across {len(contracts)} contracts")
    print(f"  tables gaining columns for the first time: {len(filled)}")
    if filled:
        print("   ", ", ".join(sorted(filled)[:8]) + (" …" if len(filled) > 8 else ""))
    print(f"  tables whose column count changes: {len(changed)}")
    print(f"  tables the contracts do not describe (kept as-is): {len(untouched)}")

    if args.dry_run:
        return 0

    # Only fill what is empty and refresh what the contracts now describe better. A table the
    # contracts say nothing about keeps whatever it had — this tool adds knowledge, it does not
    # discard it.
    # **Merge by column, not by count.** The old rule replaced a table only when the derived set
    # was at least as long — so `identity.sso_group_mapping` gaining an `id` from its schema was
    # discarded, because the existing row already held two extra columns the relationship graph
    # had supplied. **A contract adding a primary key lost to an arithmetic comparison**, and the
    # key check found it three edits later while I kept fixing the wrong thing.
    #
    # Contract-derived columns win where they overlap; graph-derived columns the contracts do not
    # describe are kept.
    for table, cols in derived.items():
        prior = existing.get(table) or []
        if not prior:
            existing[table] = cols
            continue
        names = {c["column"] for c in cols}
        # **A column the contract used to describe and no longer does must go.** 24 August:
        # `RolePermission` was corrected to five properties and `identity.role_permission` kept
        # `is_system`, `principal_count` and `grant_count` from the previous run — the tool "adds
        # knowledge and does not discard it", which made a contract-side deletion invisible.
        #
        # **A stale column is worse than a missing one**: it validates, it appears in the workbook,
        # and a build team writes DDL for a field nobody meant.
        #
        # Kept: anything whose source is not this contract — relationship-graph columns and
        # hand-added notes the contracts never described.
        # A contract-derived column records its source as `<contract>.<Schema>.<property>`.
        # Anything else — `relationship-graph.json`, a hand note — the contracts never described
        # and must survive.
        keep = [c for c in prior
                if c["column"] not in names
                and str(c.get("source", "")).count(".") < 2]
        existing[table] = cols + keep
    # A relationship is evidence a column exists — applied after the merge so it reaches tables the
    # contracts do not describe at all. The graph names columns an API never returns: `ai.policy`
    # carries a tenant, `identity.authz_audit` an actor and a subject, `fnb.location_code` a
    # location. **Scope and audit columns are the usual case**, and they are exactly the ones a
    # reader must see — a policy table with no visible tenant column looks unscoped.
    for (table, col), e in sorted(edges.items()):
        # **An ambient edge names an operation, not a column.** `derive-relationships` records
        # `via reindexSource` where two tables are written together and no column joins them, and
        # on 18 August this loop turned 123 of those into columns — `fnb.menu.via createMenu` was
        # sitting in the workbook as a uuid.
        #
        # A coupling is real and it is not a column. Skipped here and kept in the graph.
        if e.get("edgeKind") == "ambient" or col.startswith("via "):
            continue
        # **A withdrawn column is not re-created from the graph.** The edge is still in
        # `relationship-graph.json` because the graph was derived from the column, and without this
        # the deletion is undone on the same run that makes it.
        if col in retired.get(table, ()):
            continue
        row = existing.setdefault(table, [])
        found = next((c for c in row if c["column"] == col), None)
        if found:
            found["references"] = e["to"]
            found["referenceKind"] = e.get("edgeKind", "reference")
            found["referenceHow"] = e.get("how", "convention")
            found["enforced"] = "yes" if e.get("how") == "declared" else "no"
            continue
        row.append({
            "column": col,
            "type": "uuid",
            "required": e.get("required") or "no",
            "source": "relationship-graph.json",
            "description": (f"Points at {e['to']}. **Not exposed by the contract** — an API returns "
                            "what a caller needs and a table carries what RLS and the joins need."),
            "table": table,
            "references": e["to"],
            "referenceKind": e.get("edgeKind", "reference"),
            "referenceHow": e.get("how", "convention"),
            # **A declared reference becomes a real constraint; a convention becomes an index.**
            # This looked for the literal string "DDL" in `how`, which only ever holds `declared`
            # or `convention` — so it was never true, and `derive-ddl.py` emitted 774 indexes and
            # **zero foreign keys**. A placeholder written before there was any DDL to enforce.
            #
            # **The distinction is ADR-0011**: 153 references are naming habits the contracts never
            # asserted, and constraining one fails on the first row that legitimately points
            # nowhere. The other 594 are declared and should be enforced by the database.
            "enforced": "yes" if e.get("how") == "declared" else "no",
        })

    # **Withdrawn columns come out last, after every source has had its say.** The merge above
    # keeps a column whose source is not the contract, and the loop above re-creates one the graph
    # still has an edge for — so a removal applied earlier is undone by the next statement. Applied
    # here it is applied to the answer.
    n_retired = 0
    for table, cols_out in sorted(retired.items()):
        row = existing.get(table)
        if not row:
            continue
        before = len(row)
        existing[table] = [c for c in row if c["column"] not in cols_out]
        n_retired += before - len(existing[table])
    if n_retired:
        print(f"  columns withdrawn by their contract: {n_retired}")
        for table, cols_out in sorted(retired.items()):
            print(f"     {table}: {', '.join(sorted(cols_out))}")

    # **A table needs a key in the DDL, not only a column that could serve as one.** 3 September:
    # `derive-ddl` emitted `PRIMARY KEY` only where a column was literally named `id`, so 84 of 374
    # tables reached Postgres with no key at all, and four foreign keys pointed at a column that is
    # not unique — which `psql` rejects outright rather than warning about.
    #
    # **The cause is upstream of the DDL.** These tables were built from API response shapes, and a
    # response is not a table: `Subscription` returns tenantId, planId and status — everything a
    # caller needs and not the row's own identity.
    #
    # The key is added here rather than in `derive-ddl` so the SQL and the schema reference agree.
    # **A column in one and not the other is the defect this pass exists to clear.**
    #
    # **`synthesised` marks every one.** No contract asserted this identity and the register must
    # not read as though one did — `check-package` counts them so they stay a visible worklist
    # rather than becoming the answer.
    def _own_key(table, names):
        if "id" in names:
            return "id"
        stem = table.split(".", 1)[1]
        for cand in (f"{stem}_id", f"{stem.rstrip('s')}_id", f"{stem}_code"):
            if cand in names:
                return cand
        return None

    _real = {t for t in existing if "." in t and ":" not in t}
    _synth = 0
    for _t in sorted(_real):
        _row = existing[_t]
        if not _row or _own_key(_t, [c["column"] for c in _row]):
            continue
        _row.insert(0, {
            "column": "id", "type": "uuid", "required": "yes",
            "source": "derive-schema.py (surrogate)",
            "description": ("**Synthesised key.** No contract asserts an identity for this table — "
                            "it was derived from a response shape, and a response is not a table. "
                            "A row still has to be addressable to be updated or deleted."),
            "table": _t, "synthesised": "surrogate key",
        })
        _synth += 1
    print(f"  surrogate keys added: {_synth}")

    # **Five columns pointed at the product definition instead of at what the guest holds.**
    # `ScanEvent.ticketId`, `WaitingGuest.entitlementId` and three others are plain strings in the
    # contracts — nothing declares a target — so the link was inferred, written to
    # `relationship-graph.json`, read back here as `declared` on the next run and has re-asserted
    # itself ever since. **A number that grows because it was measured**, in the words this file
    # already uses about the same feedback loop.
    #
    # `catalogue.entitlement_template` is the definition a product is sold against.
    # `access.entitlement` is the row a guest actually holds — added 18 August precisely because
    # five artefacts referred to a thing that did not exist. `access.yaml` says `ticketId` is
    # "a ULID, stable for the life of the ticket and independent of the media carrying it", and a
    # template has no such life.
    #
    # **A scan event pointing at the template says every guest holding that product was scanned.**
    MISTARGETED = {
        ("access.scan_event", "ticket_id"): "access.entitlement",
        ("queue.entry", "entitlement_id"): "access.entitlement",
        ("retail.shop_and_drop", "entitlement_id"): "access.entitlement",
        ("platform.cross_region_entitlement", "ticket_id"): "access.entitlement",
        ("ledger.inter_entity_obligation", "entitlement_id"): "access.entitlement",
    }
    _repointed = 0
    for (_t, _col), _to in MISTARGETED.items():
        for _c in existing.get(_t, []):
            if _c["column"] == _col and _c.get("references") != _to:
                _c["references"] = _to
                _repointed += 1
    print(f"  mistargeted references repointed: {_repointed}")

    # **A reference column takes its target's key type.** `resolve_type` returns the literal `uuid`
    # for every `$ref` to a persisted schema, whatever that target is actually keyed by — so a ULID
    # parent typed `text` collected 37 children typed `uuid`, and Postgres rejects every one of
    # those foreign keys. **Applied after the keys above, because the key is what carries the
    # type.**
    _keytype = {}
    for _t in _real:
        _k = _own_key(_t, [c["column"] for c in existing[_t]])
        if _k:
            _keytype[_t] = next((c.get("type") for c in existing[_t]
                                 if c["column"] == _k), None) or "text"
    _retyped = 0
    for _t in sorted(_real):
        for _c in existing[_t]:
            _tgt = _c.get("references")
            if _c.get("enforced") != "yes" or _tgt not in _keytype:
                continue
            if _c.get("type") != _keytype[_tgt]:
                _c["type"] = _keytype[_tgt]
                _retyped += 1
    print(f"  reference columns retyped to their target's key: {_retyped}")

    S["cols"] = existing
    ref_path.write_text(json.dumps(S), encoding="utf-8")

    empty = [t for t in (set(S["cols"]) | set(S.get("storage", {}))) if not S["cols"].get(t)]
    print(f"\n  tables still with no columns: {len(empty)}")
    if empty:
        print("   ", ", ".join(sorted(empty)[:10]) + (" …" if len(empty) > 10 else ""))
    print(f"  → {ref_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
