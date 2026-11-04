#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A natural person's data lives in pii.*, is marked, is answered under the PII permission, and every module
exports and erases it.

**Why** (r13 system review, 3 November 2026: B-01 and C-11; the lead, 3 November 2026: personal data "Move the
columns"; CHG-R14M-001). ADR-0023's invariant ("PII lives in a separate erasable store, referenced by opaque subject
ID") did not hold for module tables: 57 columns of names, contacts, birth dates, ID and IP numbers sat in 25 tenant
tables, 94 of 96 contract fields with such names carried no data class, 37 lists returned them under ORDER_VIEW,
RENTAL_VIEW and the like, the export asked one module of eleven, and the AI erasure left prompts, answers and
messages. The vocabulary is tools/personal_data.py; this holds it:

  PD-COLUMN        a tenant-database column outside pii.* whose name is a natural person's identifier
                   (personal_data.COLUMN), unless its contract field is marked `x-ticvai-data-class: business`
  PD-UNMARKED      a contract property (components or inline) whose name is a person's identifier
                   (personal_data.PROPERTY) with no `x-ticvai-data-class`
  PD-NOT-MOVED     a property marked personal, named as an identifier, on a schema persisted to a tenant table
                   outside pii.*, with no `x-ticvai-pii`: it would be an identifier column of the module's table
                   (PD-COLUMN's name rule). A personal field kept on the row under another name (a suppression's
                   `address`, a report recipient's) is the module's to erase (PD-MODULE-ERASE)
  PD-STORE         an `x-ticvai-pii` that names no known store, is not marked personal, or names a subject property
                   the schema does not have (a uuid with `x-ticvai-subject-kind`)
  PD-RESPONSE      an operation whose success response carries a field marked personal, for a caller other than a
                   service, under a permission that is not a PII permission (personal_data.PII_PERMISSIONS) and
                   with no `x-ticvai-personal-data: gated|self` (nor `x-ticvai-self-scoped: subject`)
  PD-MODULE-PART   a module (contract) owning a table that holds a subject's data (handoff/subject-data-register.json)
                   with no job consuming identity.privacyRequestRaised that reads all of them (its part of the
                   export), Identity's own export job included
  PD-MODULE-ERASE  that job (or, for AI, `eraseSubject`; for Identity, `guestErasure`) does not write every table of
                   the module the erasure must reach: a table with a personal field kept outside pii.* (and, for AI,
                   every table that holds a subject's prompts, answers, messages or recommendations)

The control database is not judged here, nor the control plane's responses (CONTROL_CONTRACTS): it has no pii schema
and no PII permission, and where its people's data goes is ADR-0043's regional control database (review finding B-02),
the lead's control-plane decision. Its fields are marked all the same (PD-UNMARKED covers every contract).

    python3 tools/check-personal-data.py [--all] [--self-test]

Read-only. Exit 1 on a finding (there is no baseline: a new class gate starts at zero).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402
import personal_data as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RULES = {
    "PD-COLUMN": "a tenant column outside pii.* holds a natural person's identifier (B-01)",
    "PD-UNMARKED": "a contract field named as a person's identifier carries no x-ticvai-data-class (B-01)",
    "PD-NOT-MOVED": "a personal identifier field persisted to a module table has no x-ticvai-pii store (B-01)",
    "PD-STORE": "an x-ticvai-pii names no store, is not personal, or names no subject property (B-01)",
    "PD-RESPONSE": "a response carries personal fields outside the PII permission with no declared rule (B-01)",
    "PD-MODULE-PART": "a module holding a subject's data writes no part of the subject-data export (B-01)",
    "PD-MODULE-ERASE": "a module's erasure does not reach every table holding a subject's personal data (B-01, C-11)",
}
EVENT = "identity.privacyRequestRaised"
# The control plane's contracts (PlatformService: the control database). Its people's data and who may read it wait on
# the lead's control-plane decision (review finding B-02, ADR-0043): no PII permission exists in that plane yet.
CONTROL_CONTRACTS = ("subscription", "public-api", "platform-ops")
VERBS = ("get", "post", "put", "patch", "delete")


# ---------------------------------------------------------------- contracts
def load():
    docs = {stem: doc for stem, _rel, doc in g.contracts()}
    return docs


def resolve(docs, stem, ref):
    """(stem, schema dict, name) for a $ref, or (None, None, None)."""
    ref = str(ref or "")
    fp, _, ptr = ref.partition("#")
    tstem = Path(fp).stem if fp else stem
    doc = docs.get(tstem)
    if doc is None:
        return None, None, None
    cur = doc
    for part in ptr.strip("/").split("/"):
        cur = cur.get(part) if isinstance(cur, dict) else None
        if cur is None:
            return None, None, None
    return tstem, cur if isinstance(cur, dict) else None, ptr.rsplit("/", 1)[-1]


def walk_props(docs, stem, schema, where, out, seen=frozenset(), depth=0, follow=True):
    """Every (where, name, spec, owner schema dict, stem) under a schema node; follows $ref when `follow`."""
    if not isinstance(schema, dict) or depth > 8:
        return
    if "$ref" in schema:
        if not follow or schema["$ref"] in seen:
            return
        tstem, tgt, _n = resolve(docs, stem, schema["$ref"])
        walk_props(docs, tstem, tgt, where, out, seen | {schema["$ref"]}, depth + 1, follow)
        return
    for k in ("allOf", "oneOf", "anyOf"):
        for i, x in enumerate(schema.get(k) or []):
            walk_props(docs, stem, x, where, out, seen, depth + 1, follow)
    if isinstance(schema.get("items"), dict):
        walk_props(docs, stem, schema["items"], where + "[]", out, seen, depth + 1, follow)
    if isinstance(schema.get("additionalProperties"), dict):
        walk_props(docs, stem, schema["additionalProperties"], where + "{}", out, seen, depth + 1, follow)
    for p, v in (schema.get("properties") or {}).items():
        out.append((f"{where}.{p}", p, v, schema, stem))
        if isinstance(v, dict):
            # a value object kept as one jsonb column: its members are not columns (`@jsonb` in the path says so)
            sub = f"{where}.{p}" + ("@jsonb" if v.get("x-ticvai-persistence-column") == "jsonb" else "")
            walk_props(docs, stem, v, sub, out, seen, depth + 1, follow)


def operations(docs):
    for stem, doc in docs.items():
        for path, item in (doc.get("paths") or {}).items():
            if not isinstance(item, dict):
                continue
            for m in VERBS:
                op = item.get(m)
                if isinstance(op, dict) and op.get("operationId"):
                    yield stem, path, m, op


def inline_schemas(op):
    """(label, schema) for each inline schema an operation carries (request bodies, responses, parameters)."""
    rb = op.get("requestBody") or {}
    for ct, c in ((rb.get("content") or {}) if isinstance(rb, dict) else {}).items():
        if isinstance(c, dict) and isinstance(c.get("schema"), dict):
            yield "request", c["schema"]
    for code, r in (op.get("responses") or {}).items():
        if not isinstance(r, dict):
            continue
        for ct, c in (r.get("content") or {}).items():
            if isinstance(c, dict) and isinstance(c.get("schema"), dict):
                yield str(code), c["schema"]
    for prm in op.get("parameters") or []:
        if isinstance(prm, dict) and isinstance(prm.get("schema"), dict) and prm.get("name"):
            yield f"param.{prm['name']}", prm["schema"]


def persisted_table(schema):
    t = schema.get("x-ticvai-persistence") if isinstance(schema, dict) else None
    if not isinstance(t, str) or "." not in t or "—" in t or t.strip().lower().startswith("none"):
        return None
    return t.split("+")[0].strip()


def tenant_module_table(t):
    return bool(t) and t.split(".")[0] not in (pd.PII_SCHEMA, "control")


# ---------------------------------------------------------------- rules
def check_fields(guard, docs):
    """PD-UNMARKED, PD-NOT-MOVED, PD-STORE."""
    n_fields = 0
    for stem, doc in docs.items():
        for name, schema in (((doc.get("components") or {}).get("schemas")) or {}).items():
            out = []
            walk_props(docs, stem, schema, name, out, follow=False)
            n_fields += _judge_fields(guard, stem, out, persisted_table(schema), schema)
        for _s, path, m, op in operations({stem: doc}):
            for label, sch in inline_schemas(op):
                out = []
                walk_props(docs, stem, sch, f"{op['operationId']}.{label}", out, follow=False)
                n_fields += _judge_fields(guard, stem, out, persisted_table(sch), sch)
    guard.note(f"{n_fields} contract field(s) named as a person's identifier, every one with a data class")


def _judge_fields(guard, stem, out, table, top):
    n = 0
    for where, p, v, owner, _st in out:
        if not isinstance(v, dict):
            continue
        key = f"{stem}:{where}"
        cls = pd.data_class(v)
        mark = pd.pii_mark(v)
        if pd.is_identifier_property(p):
            n += 1
            if cls not in pd.DATA_CLASSES:
                guard.add("PD-UNMARKED", key, f"{key}: named as a person's identifier, no x-ticvai-data-class "
                          "(personal, or business for an organisation's)")
        # the table this property lands in: its own schema's, or the child table of an inline array item
        tbl = table if owner is top else (None if persisted_table(owner) is None else persisted_table(owner))
        if owner is not top and tbl is None and table and "[]" in where:
            tbl = table      # an inline array item of a persisted schema is a child table of the same module
        if "@jsonb" in where:
            tbl = None       # inside a jsonb value object: the column is the object, judged by its own data class
        if mark:
            if mark["store"] not in pd.STORES:
                guard.add("PD-STORE", key, f"{key}: x-ticvai-pii store {mark['store']!r} is not one of "
                          f"{', '.join(sorted(pd.STORES))}")
            if cls != "personal":
                guard.add("PD-STORE", key, f"{key}: x-ticvai-pii on a field not marked x-ticvai-data-class: personal")
            subj = (owner.get("properties") or {}).get(mark["subject"]) if isinstance(owner, dict) else None
            if not isinstance(subj, dict) or subj.get("format") != "uuid" \
                    or subj.get("x-ticvai-subject-kind") not in pd.SUBJECT_KINDS:
                guard.add("PD-STORE", key, f"{key}: its subject property {mark['subject']!r} is not on the schema as "
                          "a uuid with x-ticvai-subject-kind (guest, employee, contact or applicant)")
        elif cls == "personal" and pd.is_identifier_property(p) and tenant_module_table(tbl) \
                and v.get("x-ticvai-persisted") is not False \
                and pd.is_identifier_column(v.get("x-ticvai-column") or g.snake(p)):
            guard.add("PD-NOT-MOVED", key, f"{key}: a person's identifier persisted to {tbl}; keep it in pii.* "
                      "(x-ticvai-pii: {store, subject}) and give the row its subject")
    return n


def check_columns(guard, docs, S):
    cols = S.get("cols") or {}
    store = S.get("store") or {}
    n = 0
    for t, row in sorted(cols.items()):
        if "." not in t or ":" in t or not tenant_module_table(t) or store.get(t, "postgres") != "postgres":
            continue
        for c in row:
            name = c.get("column")
            if not pd.is_identifier_column(name):
                continue
            spec = source_spec(docs, c.get("source"))
            if pd.data_class(spec) == "business":
                continue
            n += 1
            guard.add("PD-COLUMN", f"{t}.{name}", f"{t}.{name}: a natural person's {name} outside pii.* "
                      f"(from {c.get('source') or 'storage'}); mark its field x-ticvai-pii, or business where it "
                      "is an organisation's")
    guard.note(f"{n} identifier column(s) outside pii.* in the tenant database")


def source_spec(docs, source):
    """The contract property a schema-reference column came from (`module.Schema.prop`, `module.Schema.arr[].prop`)."""
    src = str(source or "")
    parts = src.split(".")
    if len(parts) < 3 or parts[0] not in docs:
        return None
    sch = (((docs[parts[0]].get("components") or {}).get("schemas")) or {}).get(parts[1])
    cur = sch
    for seg in parts[2:]:
        if not isinstance(cur, dict):
            return None
        arr = seg.endswith("[]")
        seg = seg[:-2] if arr else seg
        if "$ref" in cur:
            _s, cur, _n = resolve(docs, parts[0], cur["$ref"])
        props = {}
        for b in [cur] + list((cur or {}).get("allOf") or []):
            if isinstance(b, dict) and "$ref" in b:
                _s, b, _n = resolve(docs, parts[0], b["$ref"])
            props.update((b or {}).get("properties") or {})
        cur = props.get(seg)
        if arr and isinstance(cur, dict):
            cur = cur.get("items")
            if isinstance(cur, dict) and "$ref" in cur:
                _s, cur, _n = resolve(docs, parts[0], cur["$ref"])
    return cur if isinstance(cur, dict) else None


def check_responses(guard, docs):
    n = 0
    for stem, path, m, op in operations(docs):
        aud = set(op.get("x-ticvai-audience") or [])
        if (aud and aud <= {"service"}) or stem in CONTROL_CONTRACTS:
            continue
        found = []
        for code, r in (op.get("responses") or {}).items():
            if not str(code).startswith("2"):
                continue
            if isinstance(r, dict) and "$ref" in r:
                _s, r, _n = resolve(docs, stem, r["$ref"])
            for ct, c in ((r or {}).get("content") or {}).items():
                out = []
                walk_props(docs, stem, (c or {}).get("schema"), "", out)
                found += [w for w, p, v, _o, _s in out if pd.data_class(v) == "personal"]
        if not found:
            continue
        n += 1
        perm = op.get("x-ticvai-permission")
        if perm in pd.PII_PERMISSIONS or op.get("x-ticvai-personal-data") in pd.PERSONAL_DATA_MODES \
                or op.get("x-ticvai-self-scoped") == "subject":
            continue
        oid = op["operationId"]
        guard.add("PD-RESPONSE", oid, f"{stem}#{oid} ({perm or 'no permission'}; audience "
                  f"{', '.join(sorted(aud)) or 'none'}) answers {', '.join(sorted(set(found))[:4])}"
                  f"{' ...' if len(set(found)) > 4 else ''}: declare x-ticvai-personal-data (gated or self) or take "
                  "GUEST_VIEW_PII")
    guard.note(f"{n} operation(s) answer a personal field to a caller other than a service")


def jobs_of(docs):
    out = {}
    for stem, doc in docs.items():
        for name, j in (doc.get("x-ticvai-jobs") or {}).items():
            if isinstance(j, dict):
                out[(stem, name)] = j
    return out


def op_writes(op):
    return {str(w.get("table")) for w in op.get("x-ticvai-writes") or [] if isinstance(w, dict)}


def check_modules(guard, docs, S, register):
    """PD-MODULE-PART and PD-MODULE-ERASE, per contract that owns subject tables (the register's `owners`)."""
    jobs = jobs_of(docs)
    ops = {op["operationId"]: (stem, op) for stem, _p, _m, op in operations(docs)}
    personal_tables = personal_columns_by_table(docs, S)
    owners = register.get("owners") or {}
    for contract, tables in sorted(owners.items()):
        # the control database's people wait on the control-plane decision (B-02): see the docstring
        tables = sorted({t for t in tables if not t.startswith("control.")})
        if contract in CONTROL_CONTRACTS or not tables:
            continue
        if contract == "identity":
            part = jobs.get(("identity", "subjectExport"))
            erase = jobs.get(("identity", "guestErasure"))
            reads = set((part or {}).get("reads") or [])
            writes = set((erase or {}).get("writes") or [])
            need_w = {t for t in tables if t.startswith("pii.")}
        else:
            mine = [j for (st, _n), j in jobs.items() if st == contract and EVENT in (j.get("consumes") or [])]
            # Marketing's part is an operation (writeSubjectDataExportPart, CHG-R11FXC-005)
            mine_ops = [o for st, o in ops.values() if st == contract and EVENT in (o.get("x-ticvai-consumes") or [])]
            reads = set().union(*[set(j.get("reads") or []) for j in mine]) if mine else set()
            reads |= set().union(*[{str(r.get("table")) for r in o.get("x-ticvai-reads") or [] if isinstance(r, dict)}
                                   for o in mine_ops]) if mine_ops else set()
            writes = set().union(*[set(j.get("writes") or []) for j in mine]) if mine else set()
            writes |= set().union(*[op_writes(o) for o in mine_ops]) if mine_ops else set()
            if contract == "ai":
                erase_op = (ops.get("eraseSubject") or (None, {}))[1]
                writes |= op_writes(erase_op)
                need_w = set(tables)
            else:
                need_w = {t for t in tables if t in personal_tables}
        missing_r = [t for t in tables if t not in reads]
        if missing_r:
            guard.add("PD-MODULE-PART", contract, f"{contract}: no export part reads {', '.join(missing_r[:6])}"
                      f"{' ...' if len(missing_r) > 6 else ''} (a job consuming {EVENT} whose reads list them)")
        missing_w = sorted(need_w - writes)
        if missing_w:
            guard.add("PD-MODULE-ERASE", contract, f"{contract}: its erasure does not write "
                      f"{', '.join(missing_w[:6])}{' ...' if len(missing_w) > 6 else ''}")
    guard.note(f"{len(owners)} contract(s) own a table that holds a subject's data")


def personal_columns_by_table(docs, S):
    """Tables with a column whose contract field is marked personal (kept outside pii.*: erasure must reach them)."""
    out = set()
    for t, row in (S.get("cols") or {}).items():
        if not tenant_module_table(t):
            continue
        for c in row:
            if c.get("dataClass") == "personal" or pd.data_class(source_spec(docs, c.get("source"))) == "personal":
                out.add(t)
                break
    return out


# ---------------------------------------------------------------- self-test
def self_test() -> int:
    ok = True

    def case(name, cond):
        nonlocal ok
        print(f"  {'ok  ' if cond else 'FAIL'} {name}")
        ok = ok and bool(cond)

    case("an email column is an identifier", pd.is_identifier_column("recipient_email"))
    case("a hash of one is not", not pd.is_identifier_column("email_hash"))
    case("a flag about one is not", not pd.is_identifier_column("prefers_email"))
    case("a face value is not", not pd.is_identifier_column("face_value_amount"))
    case("a subject column is not", not pd.is_identifier_column("holder_subject_id"))
    docs = {"m": {"components": {"schemas": {
        "Row": {"x-ticvai-persistence": "m.row", "properties": {
            "subjectId": {"type": "string", "format": "uuid", "x-ticvai-subject-kind": "guest"},
            "holderName": {"type": "string", "x-ticvai-data-class": "personal",
                           "x-ticvai-pii": {"store": "subject.displayName"}},
            "email": {"type": "string", "x-ticvai-data-class": "personal"},
            "phone": {"type": "string"}}}}},
        "paths": {"/rows": {"get": {"operationId": "listRows", "x-ticvai-permission": "ORDER_VIEW",
                                    "x-ticvai-audience": ["staff"], "responses": {"200": {"content": {
                                        "application/json": {"schema": {"type": "array", "items": {
                                            "$ref": "#/components/schemas/Row"}}}}}}}}}}}
    guard = g.Guard("self-test", RULES)
    check_fields(guard, docs)
    check_responses(guard, docs)
    f = guard.found
    case("an unmarked phone is PD-UNMARKED", "m:Row.phone" in f["PD-UNMARKED"])
    case("a personal email on a module row with no store is PD-NOT-MOVED", "m:Row.email" in f["PD-NOT-MOVED"])
    case("a moved name with its subject passes PD-STORE", not f["PD-STORE"])
    case("ORDER_VIEW answering personal fields is PD-RESPONSE", "listRows" in f["PD-RESPONSE"])
    docs["m"]["paths"]["/rows"]["get"]["x-ticvai-personal-data"] = "gated"
    docs["m"]["components"]["schemas"]["Row"]["properties"]["holderName"]["x-ticvai-pii"]["subject"] = "nobody"
    guard = g.Guard("self-test", RULES)
    check_fields(guard, docs)
    check_responses(guard, docs)
    case("a declared gate passes PD-RESPONSE", not guard.found["PD-RESPONSE"])
    case("a store naming no subject property is PD-STORE", "m:Row.holderName" in guard.found["PD-STORE"])
    S = {"cols": {"m.row": [{"column": "guest_name", "source": "m.Row.guestName"}],
                  "pii.subject": [{"column": "given_name"}],
                  "control.partner_contact": [{"column": "email"}]}}
    guard = g.Guard("self-test", RULES)
    check_columns(guard, docs, S)
    case("a guest name column in a module table is PD-COLUMN", "m.row.guest_name" in guard.found["PD-COLUMN"])
    case("pii.* and control are not judged", len(guard.found["PD-COLUMN"]) == 1)
    docs2 = {"m": {"x-ticvai-jobs": {"subjectData": {"consumes": [EVENT], "reads": ["m.a"], "writes": []}}},
             "ai": {"paths": {"/e": {"post": {"operationId": "eraseSubject",
                                              "x-ticvai-writes": [{"table": "ai.x"}]}}}}}
    guard = g.Guard("self-test", RULES)
    check_modules(guard, docs2, {"cols": {}}, {"owners": {"m": ["m.a", "m.b"], "ai": ["ai.x", "ai.y"]}})
    case("a module whose part misses a table is PD-MODULE-PART", "m" in guard.found["PD-MODULE-PART"])
    case("an AI table eraseSubject does not write is PD-MODULE-ERASE", "ai" in guard.found["PD-MODULE-ERASE"])
    print("self-test:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main() -> int:
    g.force_utf8()
    if self_test():
        return 1
    if "--self-test" in sys.argv:
        return 0
    guard = g.Guard("check-personal-data", RULES)
    docs = load()
    S = json.loads((ROOT / "handoff" / "schema-reference.json").read_text(encoding="utf-8"))
    register = g.load_json(ROOT / "handoff" / "subject-data-register.json", {}) or {}
    check_fields(guard, docs)
    check_columns(guard, docs, S)
    check_responses(guard, docs)
    check_modules(guard, docs, S, register)
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
