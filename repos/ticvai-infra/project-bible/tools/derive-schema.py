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
from pathlib import Path

import yaml

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
            if target.get("type") == "object":
                return "jsonb", None
        # Money and other shared value objects land as jsonb rather than being flattened —
        # `Money` is amount, currency and scale together, and splitting it loses the invariant.
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


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    contracts = load_contracts()
    all_schemas: dict[str, dict] = {}
    persisted: dict[str, str] = {}          # schema name -> table
    owner: dict[str, str] = {}              # table -> contract
    for name, (_, doc) in contracts.items():
        for sname, body in ((doc.get("components") or {}).get("schemas") or {}).items():
            all_schemas.setdefault(sname, body)
            if isinstance(body, dict):
                table = body.get("x-ticvai-persistence")
                if isinstance(table, str) and "." in table and "—" not in table:
                    # A schema may name a parent and a child — `fnb.fnb_order + fnb.fnb_order_line`.
                    # **The properties belong to the parent**; the child comes from the nested array,
                    # which this tool deliberately skips rather than flattening. Taking the whole
                    # string as a table name created 25 tables that do not exist.
                    table = table.split("+")[0].strip()
                    persisted[sname] = table
                    owner[table] = name

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
            raw = isinstance(body, dict) and body.get("x-ticvai-persistence")
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
    for table in sorted(known_tables):
        if table in child_of or "." not in table or ":" in table:
            continue
        schema_part, _, name = table.partition(".")
        for sname, ptable in persisted.items():
            short = ptable.split(".")[-1]
            if ptable == table or not name.startswith(short + "_"):
                continue
            tail = name[len(short) + 1:]
            body = all_schemas.get(sname) or {}
            for prop, spec in (body.get("properties") or {}).items():
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
        arrays = [(k, v) for k, v in (body.get("properties") or {}).items()
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
        cols = [{
            "column": snake(parent_table.split(".")[-1]) + "_id",
            "type": "uuid", "required": "yes",
            "source": f"{owner.get(child, '')}.{parent_schema}.{key}",
            "description": f"The parent row. Derived from {parent_schema}.{key}.",
            "table": child, "references": parent_table,
        }]
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
        for prop, spec in (body.get("properties") or {}).items():
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
                c["enforced"] = "yes" if "DDL" in str(e.get("how", "")) else "no"
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
    for table, cols in derived.items():
        if not existing.get(table) or len(cols) >= len(existing[table]):
            existing[table] = cols
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
        row = existing.setdefault(table, [])
        found = next((c for c in row if c["column"] == col), None)
        if found:
            found["references"] = e["to"]
            found["referenceKind"] = e.get("edgeKind", "reference")
            found["referenceHow"] = e.get("how", "convention")
            found["enforced"] = "yes" if "DDL" in str(e.get("how", "")) else "no"
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
            "enforced": "yes" if "DDL" in str(e.get("how", "")) else "no",
        })

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
