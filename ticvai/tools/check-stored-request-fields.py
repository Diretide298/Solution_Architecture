#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A request field the contract says is stored reaches a column (14 October 2026, CHG-CRD-009, ADAM CR-078).

**Found by ADAM CR-078** (ticket 27750, the r6 settlement): `createPrincipal` took `initialCredential` and
`mustChangeCredential`, `changeOwnCredential` took a new password that `ChangeCredentialRequest` said was "stored hashed
in `identity.principal_credential`", and the table those operations' lineage wrote held only `id` and a nullable
`principal_id`. Every check passed: the table existed, the lineage named it, the field was on the request. Nothing
asked whether a field the contract promises to keep has a column to be kept in.

  SR-STORED-NO-COLUMN  a write's request field that the contract says is stored (its description, or its request
                       schema's description, says `stored`; or it carries `x-ticvai-stored-as`) reaching no column of
                       a table the operation's lineage writes
  SR-STUB-WRITE        a write whose lineage writes a table holding only keys (`id` and `*_id` columns), with request
                       fields that reach no column of any table it writes: the table needs those fields and has none
  SR-SECRET-UNHASHED   a `writeOnly` credential field on a write (a password, PIN or credential) that is neither
                       `x-ticvai-persisted: false` (compared, never kept) nor `x-ticvai-stored-as` a `*_hash` column
                       (ADR-0071: a credential is stored as its hash, never as sent)

**How a field reaches a column.** `x-ticvai-stored-as: <schema>.<table>.<column>` names it, and the table must be one
the lineage writes; otherwise a written table has the field's snake-case name (or `x-ticvai-column`), a column named
for it plus a suffix (`price` -> `price_amount`), or a column whose contract source is the field. A field marked
`x-ticvai-persisted: false` or `readOnly` is not a stored field. Fields of request bodies are read one level deep,
through `$ref` and `allOf`; an array of objects is a child table's rows and is read as its item fields.

The table columns come from `handoff/schema-reference.json`, which `derive-schema` writes: derive before you check.
Read-only. Exit 1 on a finding not in `handoff/audit-baseline.json` (tools/audit_guard.py): the known ones are the
backlog of the class (CR-082's request-only fields are the wider sweep), and a new operation must not add one.

    python3 tools/check-stored-request-fields.py [--all] [--update-baseline]
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {
    "SR-STORED-NO-COLUMN": "a request field the contract says is stored reaches no column the lineage writes "
                           "(ADAM CR-078, 14 October 2026)",
    "SR-STUB-WRITE": "a write into a table holding only keys, with request fields that reach no written column "
                     "(ADAM CR-078: createPrincipal.initialCredential, mustChangeCredential)",
    "SR-SECRET-UNHASHED": "a writeOnly credential field neither compared-only nor stored as a *_hash column (ADR-0071)",
}
STORED = re.compile(r"\bstored\b", re.I)
NOT_STORED = re.compile(r"\b(never|not|nothing|isn't|is not)\s+(be\s+)?stored\b", re.I)
SECRET = re.compile(r"(credential|password|passcode|(^|[a-z])pin$|^pin)", re.I)
KEY_COL = re.compile(r"^(id|.+_id)$")


def resolve(node, by_name, stem, depth=0):
    """Follow a local or cross-file `$ref` to the schema dict, or return the node."""
    if depth > 6 or not isinstance(node, dict):
        return node if isinstance(node, dict) else {}
    ref = node.get("$ref")
    if not ref:
        return node
    name = g.ref_name(ref)
    target = by_name.get((stem, name))
    if target is None:
        for (s, n), sch in by_name.items():
            if n == name:
                target = sch
                break
    return resolve(target or {}, by_name, stem, depth + 1)


def fields(schema, by_name, stem, depth=0):
    """[(name, spec, owning schema dict)] for the body's fields, one level, through $ref and allOf;
    an array of objects contributes its item fields (they are a child table's rows)."""
    out = []
    s = resolve(schema, by_name, stem)
    if depth > 4 or not isinstance(s, dict):
        return out
    for part in s.get("allOf") or []:
        out += fields(part, by_name, stem, depth + 1)
    for name, spec in (s.get("properties") or {}).items():
        spec_r = resolve(spec, by_name, stem) if isinstance(spec, dict) else {}
        if isinstance(spec, dict) and "$ref" in spec and spec_r.get("x-ticvai-persistence"):
            continue  # a persisted object travels by its own table (its id is the field)
        if isinstance(spec_r, dict) and spec_r.get("type") == "array":
            items = resolve(spec_r.get("items") or {}, by_name, stem)
            if isinstance(items, dict) and (items.get("properties") or items.get("allOf")):
                for n2, sp2, own2 in fields(items, by_name, stem, depth + 1):
                    out.append((name + "[]." + n2, sp2, own2))
                continue
        out.append((name, spec if isinstance(spec, dict) else {}, s))
    return out


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-stored-request-fields", RULES)
    lin = g.load_json(g.ROOT / "handoff" / "api-data-lineage.json", {}) or {}
    ref = g.load_json(g.ROOT / "handoff" / "schema-reference.json", {}) or {}
    cols = {t: v for t, v in (ref.get("cols") or {}).items()}
    by, _ = g.schemas()
    for oid, o in sorted(g.operations().items()):
        op = o["op"]
        if o["method"] == "get":
            continue
        body = ((((op.get("requestBody") or {}).get("content") or {}).get("application/json") or {})
                .get("schema") or {})
        if not body:
            continue
        e = lin.get(oid) or {}
        writes = sorted(t for t in (e.get("writes") or []) if ":" not in t and "." in t)
        if not writes:
            continue
        names = {t: {c.get("column") for c in cols.get(t, [])} for t in writes}
        sources = {t: {str(c.get("source") or "").rsplit(".", 1)[-1] for c in cols.get(t, [])} for t in writes}
        stub = [t for t in writes if names[t] and all(KEY_COL.match(c or "") for c in names[t])]
        stem = o["contract"]
        missing = []
        for fname, spec, owner in fields(body, by, stem):
            leaf = fname.rsplit(".", 1)[-1]
            spec_r = resolve(spec, by, stem)
            if spec.get("readOnly") or spec_r.get("readOnly"):
                continue
            if spec.get("x-ticvai-persisted") is False:
                continue  # travels and is compared or used, never kept
            stored_as = str(spec.get("x-ticvai-stored-as") or "")
            col = str(spec.get("x-ticvai-column") or g.snake(leaf))
            if stored_as:
                t, _, c = stored_as.rpartition(".")
                reaches = t in writes and c in names.get(t, set())
            else:
                reaches = any(col in names[t] or any(str(x or "").startswith(col + "_") for x in names[t])
                              or leaf in sources[t] for t in writes)
            desc = str(spec.get("description") or "")
            owner_desc = str(owner.get("description") or "")
            claimed = bool(stored_as) or (STORED.search(desc) and not NOT_STORED.search(desc)) or (
                STORED.search(owner_desc) and not NOT_STORED.search(owner_desc))
            if claimed and not reaches:
                guard.add("SR-STORED-NO-COLUMN", f"{oid}.{fname}",
                          f"{stem}.{oid}: {fname} is said to be stored and reaches no column of "
                          f"{', '.join(writes)}" + (f" (x-ticvai-stored-as {stored_as})" if stored_as else ""))
            # A `...Ref` names a secret held elsewhere (Key Vault), not the secret itself.
            if spec.get("writeOnly") and SECRET.search(leaf) and not re.search(r"Refs?$", leaf):
                # A credential TICVAI presents to a provider cannot be a hash: it is a Key Vault secret whose name the
                # row keeps (ADR-0063 as amended 14 October 2026, `x-ticvai-secret: vault-reference`; CHG-STO-014).
                if str(spec.get("x-ticvai-secret") or "") == "vault-reference":
                    continue
                if not (stored_as and stored_as.endswith("_hash") and reaches):
                    guard.add("SR-SECRET-UNHASHED", f"{oid}.{fname}",
                              f"{stem}.{oid}: {fname} is a writeOnly credential that is neither "
                              "x-ticvai-persisted: false nor stored as a *_hash column (ADR-0071)")
            if not reaches:
                missing.append(fname)
        if stub and missing:
            guard.add("SR-STUB-WRITE", oid,
                      f"{stem}.{oid} writes {', '.join(stub)}, which holds only keys, and "
                      f"{', '.join(sorted(missing))} reach no column it writes")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
