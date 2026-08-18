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

    ref_path = HANDOFF / "schema-reference.json"
    S = json.loads(ref_path.read_text(encoding="utf-8"))
    existing = S.get("cols", {})

    derived: dict[str, list[dict]] = {}
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
        if cols:
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
