#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every field a persisted contract schema carries has somewhere to live.

**Audit class A-STORAGE (docs/active/root-classes.md): 21 root issues, the largest single class
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
a table with no `recorded_at`. ST-PROPERTY-PERSISTENCE and ST-STALE-COLUMN (CHG-MKT-002, ADAM CR-087) -- a
persistence tag on a property, which derive-schema never reads, and a column the contract names or types otherwise
(the table kept an older run's columns: `marketing.wishlist_item.price text` against `list_price` Money).
ST-SECRET-FORM (CHG-MKT-001, CR-086) -- a stored write-only secret that does not say how it is stored
(`x-ticvai-secret`, ADR-0063 as amended 14 October 2026, ADR-0071).

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
    "ST-PROPERTY-PERSISTENCE": "x-ticvai-persistence on a property, which derive-schema never reads (CHG-MKT-002, CR-087)",
    "ST-STALE-COLUMN": "a column the contract names otherwise (x-ticvai-column) or a Money field in a non-numeric "
                       "column: the table kept an older run's columns (CHG-MKT-002, CR-087)",
    "ST-SECRET-FORM": "a stored write-only token, secret, credential, password or PIN that does not say how it is "
                      "stored (x-ticvai-secret; ADR-0063, ADR-0071) (CHG-MKT-001, CR-086)",
    "ST-GRAPH-TARGET-GONE": "a column the relationship graph adds points at a table the package no longer has "
                            "(CR-145, CHG-CRA-002)",
    "ST-DEFAULT-DESCRIBED": "a stored enum's description names its starting value (`x` until ...) and the contract "
                            "declares no default (CR-151, CHG-CRA-002)",
    "ST-CROSS-DATABASE": "a declared reference crosses the control/tenant database boundary and is not one of the "
                         "known crossings: data about a tenant sits in the tenant template (ADR-0039; CR-150, "
                         "CHG-CRA-003)",
}
# **Control-plane data kept in the tenant database** (class 4 of the 18 October triage, CHG-CRA-003). ADR-0039 made the
# control plane a database of its own, so a declared reference between it and a tenant database is no longer a
# constraint, only a rule application code must keep (backend/990-cross-database-references.sql). The plan catalogue and
# the records about a tenant rather than inside one (CR-097, CR-150) stayed in the tenant template, and
# `control.tenant.subscription_id -> subscription.contract` was the sign: the control plane's tenant row keyed into
# every tenant's database. These are the crossings known when the tables moved; each is a person or scope the control
# row names in the database that owns it. A new one fails until the table moves or the crossing is added here, with why.
KNOWN_CROSSINGS = {
    "control.cell.region_id", "control.cell_cluster.region_id", "control.channel_listing.product_id",
    "control.channel_listing.price_list_id", "control.migration_run.started_by_principal_id",
    "control.partner_agreement.approval_request_id", "control.partner_case.sla_policy_id",
    "control.partner_user.principal_id", "control.production_access_request.decided_by_principal_id",
    "control.rollout.started_by_principal_id", "control.rollout.approved_by_principal_id",
    "control.support_notice.published_by_principal_id", "control.tenant.account_manager_principal_id",
    "control.usage_record.venue_id", "platform.cell_endpoint.cell_id",
}
# **The description and the declared shape disagree** (class 11 of the 18 October triage, CHG-CRA-002). The generator
# writes what the contract declares, so a rule stated only in a description reaches the table as its opposite:
# `connectionStatus` was "`available` until its first reading" with no default (CR-151), and `control.release.plan_id`
# was rebuilt by the relationship graph from an edge to `control.subscription_plan`, renamed away on 20 September (CR-145).
DESCRIBED_START = r"(?<!as )`{v}`\s+(?:until|by default|at first)\b|(?:defaults? to|starts? as|initially)\s+`{v}`"
GRAPH_TARGET = re.compile(r"Points at ([a-z_]+\.[a-z_0-9]+)")
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
        # an enum of numbers stored as a number (`x-ticvai-persistence-column: integer`, CHG-CRD-002) is an int
        return "int" if ps.get("type") == "integer" and ps.get("x-ticvai-persistence-column") else "enum"
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


_GEN: dict = {}


def bool_column(sn: str) -> str:
    """The column derive-schema names a boolean property (`conventional_name`, CHG-STO-009: `offline_capability` is
    stored as `supports_offline`), read from the generator so this check cannot disagree with it."""
    if "conv" not in _GEN:
        import importlib.util
        spec = importlib.util.spec_from_file_location("derive_schema", str(g.ROOT / "tools" / "derive-schema.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _GEN["conv"] = mod.conventional_name
    return _GEN["conv"](sn, "boolean", None)


def required_of(schema: dict, stem: str, by: dict, depth=0) -> set:
    """The names a schema requires, through `allOf` and local `$ref`s, as derive-schema reads them (CHG-STO-012: a
    schema built as `allOf: [Create...Request, {required: [...]}]` was read as requiring nothing)."""
    out = set()
    if not isinstance(schema, dict) or depth > 4:
        return out
    if "$ref" in schema:
        ref = schema["$ref"]
        if ref.startswith("#/components/schemas/"):
            return required_of(by.get((stem, g.ref_name(ref))) or {}, stem, by, depth + 1)
        return out
    out |= set(schema.get("required") or [])
    for sub in schema.get("allOf") or []:
        out |= required_of(sub, stem, by, depth + 1)
    return out


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
    # **A column whose fix is the migration owner's is waiting, not wrong** (CHG-STO-013, as D-SCOPE-NOTNULL reads a
    # scope_path on its way to NOT NULL): ST-TYPE-MISMATCH, ST-ENUM-CHECK and ST-REQUIRED-MISMATCH read the frozen r1
    # DDL, which only a forward migration changes. Where the generator's DDL already agrees with the contract and
    # handoff/migration-review.md lists the column's change ("column changed", "not null"), it is a note.
    pending = set()
    review = g.ROOT / "handoff" / "migration-review.md"
    if review.exists():
        pending = set(re.findall(r"^\| (?:column changed|not null) \| \w+ \| `([a-z_]+\.[a-z_0-9]+\.[a-z_0-9]+)` \|",
                                 review.read_text(encoding="utf-8"), re.M))
    # A CHECK the generated forward migrations add is the fix itself, no longer waiting on a person (r8 walk fix,
    # CHG-R8WFM-001 moved the widened CHECKs from migration-review.md into V0108): `ALTER TABLE s.t ADD CONSTRAINT
    # ... CHECK (col IN (...))` in any backend/*/V01*.sql counts the column as fixed, not as a finding.
    for mig in sorted((g.ROOT / "backend").glob("*/V01*.sql")):
        for t, c in re.findall(r"^ALTER TABLE ([a-z_]+\.[a-z_0-9]+) ADD CONSTRAINT \w+ CHECK \((\w+) IN \(",
                               mig.read_text(encoding="utf-8", errors="replace"), re.M):
            pending.add(f"{t}.{c}")

    def add_or_note(rule, key, msg, col_key):
        if col_key in pending:
            guard.note(f"{msg}: its change is listed in handoff/migration-review.md for the migration owner")
        else:
            guard.add(rule, key, msg)

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
            elif kind(ps, by, stem) == "bool":
                cands.add(bool_column(sn))        # the generator names a boolean as an assertion (CHG-STO-009)
            hit = cands & have
            if hit:
                col_name = str(col) if col and str(col) in have else (sn if sn in have else sorted(hit)[0])
                t = next((t for t in present if col_name in (lines.get(t) or {})), None)
                line = (lines.get(t) or {}).get(col_name, "") if t else ""
                if line and col_name == sn:
                    ctype = line.split()[1] if len(line.split()) > 1 else ""
                    k = kind(ps, by, stem)
                    if ctype and not compatible(k, ctype):
                        add_or_note("ST-TYPE-MISMATCH", f"{stem}.{name}.{p}",
                                    f"{stem}.{name}.{p} is {k}, column {t}.{col_name} is {ctype}", f"{t}.{col_name}")
                    if k == "enum" and ctype.lower().startswith("text") and " CHECK " not in line.upper()                             and "_chk" not in line:
                        add_or_note("ST-ENUM-CHECK", f"{t}.{col_name}",
                                    f"{t}.{col_name} holds {stem}.{name}.{p}, an enum, as text with no CHECK",
                                    f"{t}.{col_name}")
                    required = p in required_of(s, stem, by)
                    notnull = "NOT NULL" in line.upper()
                    # Only against the schema the table was derived from: a Summary or a request
                    # shape may leave out what the row requires.
                    origin = str((ref.get("origin") or {}).get(t) or "")
                    if col_name not in SERVER_SET and not ps.get("readOnly") and len(present) == 1                             and origin.split(".")[-1] == name:
                        if required and not notnull and not ps.get("nullable"):
                            add_or_note("ST-REQUIRED-MISMATCH", f"{t}.{col_name}",
                                        f"{stem}.{name}.{p} is required; {t}.{col_name} is nullable",
                                        f"{t}.{col_name}")
                        elif notnull and not required and "DEFAULT" not in line.upper():
                            add_or_note("ST-REQUIRED-MISMATCH", f"{t}.{col_name}",
                                        f"{stem}.{name}.{p} is optional; {t}.{col_name} is NOT NULL with no default",
                                        f"{t}.{col_name}")
                continue
            if any(f"{stem}.{name}.{p}" == src or src.endswith(f".{name}.{p}") for src in sources
                   if src.endswith("." + p)):
                continue
            # **The same storage SP-ARRAY-NOWHERE and derive-schema see** (CHG-STO-011): a child table whose columns
            # come from this array (`<Schema>.<prop>[].<field>` sources), items that are rows of a table of their own
            # (`MenuSection.items` are `fnb.menu_item` rows), or a `$ref` to a shape the contract says is computed on
            # read (`none — computed`), which derive-schema gives no column on purpose.
            if any(f".{name}.{p}[]" in src for src in sources):
                continue
            tgt = by.get((stem, target)) if target else None
            ttag = str((tgt or {}).get("x-ticvai-persistence") or "").strip() if isinstance(tgt, dict) else ""
            if ttag and (NOT_STORED.search(ttag) or (not ttag.lower().startswith("none") and "." in ttag
                                                     and "—" not in ttag)):
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
    check_stale_and_secrets(guard, cols, by)
    check_described_shape(guard, cols, by)
    check_cross_database(guard, cols)
    return guard.finish()


def check_cross_database(guard, cols: dict) -> None:
    """ST-CROSS-DATABASE (class 4 of the 18 October triage, CHG-CRA-003): a declared reference between the control
    database and a tenant database that is not a known crossing."""
    def db(t):
        return "control" if t.split(".")[0] == "control" else "tenant"
    for t, cs in sorted(cols.items()):
        for c in cs:
            ref = str(c.get("references") or "")
            if not ref or ref not in cols or c.get("enforced") != "yes" or db(t) == db(ref):
                continue
            key = f"{t}.{c.get('column')}"
            if key not in KNOWN_CROSSINGS:
                guard.add("ST-CROSS-DATABASE", key,
                          f"{key} -> {ref} crosses from the {db(t)} database to the {db(ref)} one: a record about a "
                          f"tenant belongs in control (ADR-0039), or the crossing is listed in KNOWN_CROSSINGS with why")


def check_described_shape(guard, cols: dict, by: dict) -> None:
    """ST-GRAPH-TARGET-GONE and ST-DEFAULT-DESCRIBED (class 11 of the 18 October triage, CHG-CRA-002)."""
    for t, cs in sorted(cols.items()):
        for c in cs:
            if not str(c.get("source") or "").startswith("relationship-graph"):
                continue
            m = GRAPH_TARGET.search(str(c.get("description") or ""))
            target = c.get("references") or (m.group(1) if m else None)
            if target and target not in cols:
                guard.add("ST-GRAPH-TARGET-GONE", f"{t}.{c.get('column')}",
                          f"{t}.{c.get('column')} comes from the relationship graph and points at {target}, which the "
                          f"package no longer has: retire it (x-ticvai-retired-columns) or declare it on the contract")
    for (stem, name), s in sorted(by.items()):
        persist = str(s.get("x-ticvai-persistence") or "").strip()
        if not persist or persist.lower().startswith("none"):
            continue
        for p, ps in sorted(props_of(s, stem, by).items()):
            if not isinstance(ps, dict) or ps.get("x-ticvai-persisted") is False:
                continue
            tgt = (by.get((stem, g.ref_name(ps["$ref"]))) or {}) if ps.get("$ref") else {}
            values = ps.get("enum") or tgt.get("enum") or []
            if not values or "default" in ps or "default" in tgt:
                continue
            text = " ".join(str(ps.get("description") or "").split())
            for v in values:
                if re.search(DESCRIBED_START.format(v=re.escape(str(v))), text, re.I):
                    guard.add("ST-DEFAULT-DESCRIBED", f"{stem}.{name}.{p}",
                              f"{stem}.{name}.{p} says it is `{v}` until something writes it, and declares no "
                              f"default: the column has no value until then (declare `default: {v}`)")
                    break


# derive-schema.py `_NOT_STORED`: a shape worked out on read gets no column (audit R111)
NOT_STORED = re.compile(r"^none\b.*\b(computed|projection|union|aggregated|composed|derived|response shape|transient)\b",
                        re.I | re.S)
MONEY_REF = re.compile(r"(^|/)Money$")
SECRET_WORDS = re.compile(r"token|secret|credential|password|\bpin\b|apiKey|private", re.I)
SECRET_FORMS = {"vault-reference", "field-encrypted", "blind-index", "argon2id-phc"}


def _field_spec(src: str, by: dict):
    """The contract property a schema-reference column's `source` names (`contract.Schema.prop` or
    `contract.Schema.array[].prop`), or None when the contract no longer has it."""
    bits = src.split(".", 2)
    if len(bits) != 3 or not (bits[0], bits[1]) in by:
        return None
    stem, schema, path = bits
    node = by[(stem, schema)]
    for i, part in enumerate(path.split("[].")):
        p = props_of(node, stem, by).get(part)
        if not isinstance(p, dict):
            return None
        if i < path.count("[]."):
            items = p.get("items") if isinstance(p.get("items"), dict) else {}
            node = items
        else:
            return p
    return None


def check_stale_and_secrets(guard, cols: dict, by: dict) -> None:
    """ST-PROPERTY-PERSISTENCE, ST-STALE-COLUMN (CHG-MKT-002, ADAM CR-087) and ST-SECRET-FORM (CHG-MKT-001, CR-086).

    **A table the contract no longer derives keeps the columns of an older run.** `Wishlist.items` carried its own
    `x-ticvai-persistence`, which derive-schema never reads (it reads the tag on a schema), so
    `marketing.wishlist_item` was never re-derived: the contract said `list_price` Money (naming-and-style 5.1, the
    CR-011/014/072 renames) and the table kept `price text`, and no rule looked, because the wrapper schema is `none`
    and this check walked only persisted schemas. Now: a property-level persistence tag is a finding; and every
    schema-reference column whose source is a contract field is read back against that field, whatever schema it is
    on: an `x-ticvai-column` naming another column, or a `Money` field in a column that is not numeric, is stale.

    **A stored secret says how it is stored** (ADR-0063 section 4, ADR-0071). `GuestDevice.tokenRef` was "a vault
    reference" with no vault abstraction behind it and `tokenFingerprint` "a hash" with no algorithm, so a developer
    had to invent both. A write-only stored property whose name says it is a token, secret, credential, password or
    PIN declares `x-ticvai-secret`: `vault-reference` (a Key Vault secret's name, for a few provider credentials),
    `field-encrypted` (ciphertext under the tenant's data key), `blind-index` (a keyed hash for lookup) or
    `argon2id-phc` (a password or PIN hash)."""
    for (stem, name), s in sorted(by.items()):
        for p, ps in sorted(props_of(s, stem, by).items()):
            if isinstance(ps, dict) and ps.get("x-ticvai-persistence"):
                guard.add("ST-PROPERTY-PERSISTENCE", f"{stem}.{name}.{p}",
                          f"{stem}.{name}.{p} carries x-ticvai-persistence on the property; derive-schema reads it "
                          f"only on a schema, so the table is never derived from it: give the rows a schema of their own")
    for t, cs in sorted(cols.items()):
        for c in cs:
            src = str(c.get("source") or "")
            if src.count(".") < 2 or src.startswith(("derive-", "relationship-graph")):
                continue
            ps = _field_spec(src, by)
            if not isinstance(ps, dict):
                continue
            col, ctype = str(c.get("column") or ""), str(c.get("type") or "").lower()
            chosen = ps.get("x-ticvai-column")
            if chosen and str(chosen) != col:
                guard.add("ST-STALE-COLUMN", f"{t}.{col}",
                          f"{t}.{col} holds {src}, which the contract stores as {chosen} (x-ticvai-column): the table "
                          f"was not re-derived from the contract")
            ref = str(ps.get("$ref") or "")
            if not ref:
                for k in ("allOf", "oneOf"):
                    parts = ps.get(k) if isinstance(ps.get(k), list) else []
                    ref = next((str(x.get("$ref")) for x in parts if isinstance(x, dict) and x.get("$ref")), ref)
            if MONEY_REF.search(ref) and ctype and not ctype.startswith("numeric"):
                guard.add("ST-STALE-COLUMN", f"{t}.{col}:type",
                          f"{t}.{col} holds {src}, a Money, as {ctype}; every Money column is numeric(18,4)")
            if ps.get("writeOnly") and SECRET_WORDS.search(src.rsplit(".", 1)[-1]) \
                    and str(ps.get("x-ticvai-secret") or "") not in SECRET_FORMS:
                guard.add("ST-SECRET-FORM", f"{t}.{col}",
                          f"{t}.{col} stores {src}, a write-only secret, and the contract does not say how "
                          f"(x-ticvai-secret: {' | '.join(sorted(SECRET_FORMS))}; ADR-0063, ADR-0071)")


if __name__ == "__main__":
    sys.exit(main())
