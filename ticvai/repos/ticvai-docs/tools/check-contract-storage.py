#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every field a persisted contract schema carries has somewhere to live.

**Audit class A-STORAGE (audit/ticvai/ROOT-CLASSES.md): 21 root issues, the largest single class
in the contracts layer.** R086, R099, R107, R112, R115, R130, R135, R159, R172, R173, R179, R201,
R216, R217, R218, R248 are one finding per service: a schema declares `x-ticvai-persistence:
<schema.table>` and accepts or returns fields the DDL has no column or child table for, so a
developer building the operation invents the storage. R087 (stub tables), R113 (offline writes
with no `recorded_at`), R121 (no price source), R137 (a versioned thing stored in one row) and R168
(no licence storage) are the same gap seen from the table side. The root's own fix asked for this
check: *"add a package check that every property of an x-ticvai-persistence schema maps to a DDL
column."*

A property is stored when one of its schema's persistence tables has a column
  - named for it (`snake_case`, with `_id`, `_code` or a money suffix), or `x-ticvai-column`, or
  - whose `source` in `handoff/schema-reference.json` is this schema's field,
or a child table carries it (`<table>_<field>`, `<schema>.<field>`, or a table listed after `+`).
It is exempt when it says it is not stored: `readOnly` with `x-ticvai-derived`,
`x-ticvai-persisted: false`, or a `$ref` to a schema the reference lists as embedded/jsonb.

Also: S-OFFLINE-RECORDED-AT (R113) -- a schema written by an offline-capable operation persists to
a table with no `recorded_at`.

Read-only. Exit 1 on a finding not in `handoff/audit-baseline.json` (see tools/audit_guard.py).

    python3 tools/check-contract-storage.py [--all] [--update-baseline]
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {
    "ST-FIELD-NO-COLUMN": "a persisted schema's field has no column or child table (R086 R099 R107 ... R248)",
    "ST-TABLE-MISSING": "x-ticvai-persistence names a table the DDL does not have (R086)",
    "ST-OFFLINE-RECORDED-AT": "an offline-capable write persists to a table with no recorded_at (R113)",
    "ST-TYPE-MISMATCH": "a field and its column disagree on type (integer[] vs text[], boolean vs text) (R227)",
    "ST-ENUM-CHECK": "an enum field stored in a text column with no CHECK (R151)",
    "ST-REQUIRED-MISMATCH": "a required field in a nullable column, or NOT NULL for an optional one (R089)",
}
SERVER_SET = {"id", "scope_path", "created_at", "updated_at", "tenant_id", "venue_id", "region_id",
              "created_by_principal_id", "updated_by_principal_id", "version", "status", "recorded_at"}


def ddl_lines() -> dict:
    """table -> column -> the column's DDL line."""
    out = {}
    for f in (g.ROOT / "backend").glob("*/010-*.sql"):
        text = f.read_text(encoding="utf-8")
        for name, body in re.findall(r'CREATE TABLE IF NOT EXISTS ([a-z_]+\.(?:"[a-z_0-9]+"|[a-z_0-9]+))\s*\((.*?)\n\)',
                                     text, re.S):
            cols = out.setdefault(name.replace('"', ""), {})
            for raw in body.split("\n"):
                m = re.match(r'\s*"?([a-z_][a-z_0-9]*)"?\s+(\S+)', raw)
                if m and not re.match(r"\s*(CONSTRAINT|PRIMARY|UNIQUE|CHECK|FOREIGN)\b", raw):
                    cols[m.group(1)] = raw.strip().rstrip(",")
    return out


def kind(ps: dict, by: dict, stem: str) -> str:
    """The contract field's storage kind: bool, int, num, str, enum, arr:<kind>, obj."""
    if "$ref" in ps:
        tgt = by.get((stem, g.ref_name(ps["$ref"]))) or {}
        if tgt.get("enum"):
            return "enum"
        return "obj" if tgt.get("properties") or tgt.get("allOf") else (tgt.get("type") or "obj")
    if ps.get("enum"):
        return "enum"
    t = ps.get("type")
    if isinstance(t, list):
        t = next((x for x in t if x != "null"), None)
    if t == "array":
        it = ps.get("items") if isinstance(ps.get("items"), dict) else {}
        return "arr:" + kind(it, by, stem)
    return {"boolean": "bool", "integer": "int", "number": "num", "string": "str"}.get(t or "", "obj")


def compatible(k: str, coltype: str) -> bool:
    ct = coltype.lower()
    if ct.startswith("jsonb") or ct.startswith("json"):
        return True
    if k.startswith("arr:"):
        if not ct.endswith("[]"):
            return False
        return compatible(k[4:], ct[:-2])
    if ct.endswith("[]"):
        return False
    return {
        "bool": ct.startswith("boolean"),
        "int": ct.startswith(("integer", "bigint", "smallint", "numeric")),
        "num": ct.startswith(("numeric", "double", "real", "integer")),
        "str": not ct.startswith(("boolean", "integer", "bigint", "smallint")),
        "enum": ct.startswith(("text", "varchar", "character", "citext")) or "." in ct,
    }.get(k, True)
SUFFIXES = ("", "_id", "_ids", "_code", "_amount", "_minor", "_at", "_json", "_ref", "_path", "_key",
            "_hash", "_count")


def singular(w: str) -> str:
    if w.endswith("ies"):
        return w[:-3] + "y"
    if w.endswith("ses") or w.endswith("xes"):
        return w[:-2]
    if w.endswith("s") and not w.endswith("ss"):
        return w[:-1]
    return w


def props_of(schema: dict, stem: str, by: dict, depth=0) -> dict:
    out = {}
    if not isinstance(schema, dict) or depth > 4:
        return out
    if "$ref" in schema:
        ref = schema["$ref"]
        if ref.startswith("#/components/schemas/"):
            return props_of(by.get((stem, g.ref_name(ref))) or {}, stem, by, depth + 1)
        return out
    for sub in schema.get("allOf") or []:
        out.update(props_of(sub, stem, by, depth + 1))
    for k, v in (schema.get("properties") or {}).items():
        out[k] = v if isinstance(v, dict) else {}
    return out


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-contract-storage", RULES)
    ref = g.load_json(g.ROOT / "handoff" / "schema-reference.json", {}) or {}
    cols = ref.get("cols") or {}
    colnames = {t: {c.get("column") for c in cs} for t, cs in cols.items()}
    sources = {}
    for t, cs in cols.items():
        for c in cs:
            if c.get("source"):
                sources.setdefault(str(c["source"]), set()).add(t)
    embedded = {n for _, n, why in (ref.get("nomap") or []) if re.search(r"jsonb|embedded", str(why))}
    by, _ = g.schemas()
    all_tables = set(cols)
    lines = ddl_lines()

    written_offline = {}
    for oid, f in g.operations().items():
        op = f["op"]
        if op.get("x-ticvai-offline-capable") and f["method"] in ("post", "put", "patch"):
            rb = op.get("requestBody") or {}
            for media in (rb.get("content") or {}).values():
                r = (media or {}).get("schema") or {}
                if isinstance(r, dict) and str(r.get("$ref", "")).startswith("#/components/schemas/"):
                    written_offline.setdefault((f["contract"], g.ref_name(r["$ref"])), []).append(oid)

    for (stem, name), s in sorted(by.items()):
        persist = str(s.get("x-ticvai-persistence") or "").strip()
        if not persist or persist.lower().startswith("none"):
            continue
        tables = re.findall(r"\b([a-z_]+\.[a-z_0-9]+)\b", persist)
        tables = [t for t in tables if not t.endswith((".sql", ".md", ".yaml"))]
        if not tables:
            continue
        missing_t = [t for t in tables if t not in all_tables]
        for t in missing_t:
            guard.add("ST-TABLE-MISSING", f"{stem}.{name}:{t}", f"{stem}.{name} persists to {t}, which the schema reference lacks")
        present = [t for t in tables if t in all_tables]
        if not present:
            continue
        have = set().union(*(colnames[t] for t in present))
        for p, ps in sorted(props_of(s, stem, by).items()):
            if ps.get("x-ticvai-persisted") is False or ps.get("x-ticvai-derived") \
                    or ps.get("x-ticvai-persistence") or p.startswith("_"):
                continue
            items = ps.get("items") if isinstance(ps.get("items"), dict) else {}
            target = g.ref_name(ps.get("$ref") or items.get("$ref") or "")
            if target and target in embedded:
                continue
            col = ps.get("x-ticvai-column")
            sn = g.snake(p)
            cands = {sn + suf for suf in SUFFIXES} | {singular(sn) + "_ids", singular(sn) + "_id",
                                                      re.sub(r"_id$", "", sn) + "_id"}
            if col:
                cands.add(str(col))
            hit = cands & have
            if hit:
                col_name = str(col) if col and str(col) in have else (sn if sn in have else sorted(hit)[0])
                t = next((t for t in present if col_name in (lines.get(t) or {})), None)
                line = (lines.get(t) or {}).get(col_name, "") if t else ""
                if line and col_name == sn:
                    ctype = line.split()[1] if len(line.split()) > 1 else ""
                    k = kind(ps, by, stem)
                    if ctype and not compatible(k, ctype):
                        guard.add("ST-TYPE-MISMATCH", f"{stem}.{name}.{p}",
                                  f"{stem}.{name}.{p} is {k}, column {t}.{col_name} is {ctype}")
                    if k == "enum" and ctype.lower().startswith("text") and " CHECK " not in line.upper()                             and "_chk" not in line:
                        guard.add("ST-ENUM-CHECK", f"{t}.{col_name}",
                                  f"{t}.{col_name} holds {stem}.{name}.{p}, an enum, as text with no CHECK")
                    required = p in set(s.get("required") or [])
                    notnull = "NOT NULL" in line.upper()
                    # Only against the schema the table was derived from: a Summary or a request
                    # shape may leave out what the row requires.
                    origin = str((ref.get("origin") or {}).get(t) or "")
                    if col_name not in SERVER_SET and not ps.get("readOnly") and len(present) == 1                             and origin.split(".")[-1] == name:
                        if required and not notnull and not ps.get("nullable"):
                            guard.add("ST-REQUIRED-MISMATCH", f"{t}.{col_name}",
                                      f"{stem}.{name}.{p} is required; {t}.{col_name} is nullable")
                        elif notnull and not required and "DEFAULT" not in line.upper():
                            guard.add("ST-REQUIRED-MISMATCH", f"{t}.{col_name}",
                                      f"{stem}.{name}.{p} is optional; {t}.{col_name} is NOT NULL with no default")
                continue
            if any(f"{stem}.{name}.{p}" == src or src.endswith(f".{name}.{p}") for src in sources
                   if src.endswith("." + p)):
                continue
            child = {f"{t}_{singular(sn)}" for t in present} | {f"{t.split('.')[0]}.{singular(sn)}" for t in present} \
                | {f"{t}_{sn}" for t in present}
            if child & all_tables or (len(present) > 1 and any(singular(sn) in t for t in present[1:])):
                continue
            guard.add("ST-FIELD-NO-COLUMN", f"{stem}.{name}.{p}",
                      f"{stem}.{name}.{p} persists to {', '.join(present)} and no column or child table holds it")
        if (stem, name) in written_offline:
            if not any("recorded_at" in colnames[t] for t in present):
                guard.add("ST-OFFLINE-RECORDED-AT", f"{stem}.{name}",
                          f"{stem}.{name} is written offline by {written_offline[(stem, name)][0]} and "
                          f"{', '.join(present)} has no recorded_at")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
