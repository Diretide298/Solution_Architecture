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
a `$ref` to an enum becomes text; an array of enum values becomes text[]; an array of objects is a
child table's business and is skipped rather than flattened into jsonb, because a nested array
silently becoming a column is how a child table goes missing. A `$ref` to a shape tagged
"none — computed/projection" is worked out on read and gets no column.

A field that is `nullable` is not NOT NULL even when it is `required`. Descriptions are carried
whole. Column names follow the mechanical parts of naming-and-style.md (see `conventional_name`).
`--strict` fails while any table holds only keys.
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


def _is_alias(body) -> bool:
    """A schema that is nothing but a pointer to another — `{"$ref": ...}`, perhaps described."""
    return isinstance(body, dict) and "$ref" in body and set(body) <= {"$ref", "description"}


def describe(spec) -> str:
    """A column's description: the contract's words, whole.

    **It used to be cut at 220 characters with no marker** (audit R019, 26 September). 266 of
    6,729 column rows stopped mid-sentence — `ledger.recognition_schedule.priority` ended on
    "Lowest priority wins, and **", and the rule it was about to state (two schedules at the same
    priority claiming the same kind are refused) reached no reader of the table. **A cut rule
    reads as a complete one**, because nothing says it was cut. Any shortening belongs to whoever
    renders the text, where it can be marked.
    """
    if not isinstance(spec, dict):
        return ""
    return " ".join((spec.get("description") or "").split())


def is_nullable(spec) -> bool:
    """Whether a property may legitimately hold null, in any of the forms OpenAPI allows.

    **`required` says the key is present; `nullable` says its value may be null.** Reading only the
    first made `Entitlement.subjectId` — required, `nullable: true`, "Null is legitimate" — a
    `subject_id uuid NOT NULL` (audit R089). A column is NOT NULL only when the field is required
    *and* cannot be null.
    """
    if not isinstance(spec, dict):
        return False
    if spec.get("nullable") is True:
        return True
    t = spec.get("type")
    if isinstance(t, list) and "null" in t:
        return True
    for key in ("oneOf", "anyOf", "allOf"):
        for part in spec.get(key) or []:
            if isinstance(part, dict) and (part.get("type") == "null" or part.get("nullable") is True):
                return True
    return False


# **A `$ref` to a shape nobody stores is not a column.** `x-ticvai-persistence: "none — computed"`
# (or a projection, a union, an aggregate) says the value is worked out on read. Landing it as
# `jsonb` gave `queue.queue.feed`, `marketing.guest_profile.consents` and `control.tenant.licences`
# — a second, unreconciled copy of data that has a real home (audit R111). **Embedded shapes are
# different**: "none — embedded in tenant_config" and "none — jsonb column" say the jsonb IS the
# store, so they keep their column.
_NOT_STORED = re.compile(r"^none\b.*\b(computed|projection|union|aggregated|composed|derived|"
                         r"response shape|transient)\b", re.I | re.S)


def _target_of(ref: str, schemas: dict):
    """The schema a `$ref` names, following bare aliases (bounded, because two aliases naming
    each other would otherwise loop)."""
    target = schemas.get(ref.rsplit("/", 1)[-1])
    for _ in range(4):
        if not _is_alias(target):
            break
        target = schemas.get(target["$ref"].rsplit("/", 1)[-1])
    return target


def _array_type(items, schemas: dict, persisted: dict) -> str:
    """The column type of an array property, or '' where the array is a child table's rows.

    **An array of enum values is a value list, and a value list is `text[]`.** This returned ''
    for any array whose items were a `$ref`, which is right for objects and wrong for enums:
    `ApprovalDelegation.kinds` (`[ApprovalKind]`) and `RegisteredDevice.capabilities`
    (`[DeviceCapability]`) produced no column and no child table, so the delegation stored no
    kinds and the device no capabilities (audit R179).

    **An array of `allOf` items is objects too.** It fell through to `text[]`, which is how
    `fnb.service_order.lines` became a `text[] NOT NULL` beside the `service_order_line` table
    that actually holds the lines (audit R111).
    """
    if not isinstance(items, dict):
        return "text[]"
    ref = items.get("$ref")
    if not ref:
        for part in items.get("allOf") or []:
            if isinstance(part, dict) and part.get("$ref"):
                ref = part["$ref"]
                break
        else:
            if items.get("allOf"):
                return ""
    if ref:
        if ref.rsplit("/", 1)[-1] in persisted:
            return ""                # rows of another table: a join or child table, not a column
        target = _target_of(ref, schemas)
        if isinstance(target, dict) and ("enum" in target or target.get("type") in
                                         ("string", "integer", "number", "boolean")):
            return "text[]"
        return ""                    # an array of objects: a child table, not a column
    if items.get("type") == "object" or items.get("properties") or items.get("oneOf") \
            or items.get("anyOf"):
        return ""
    return "text[]"


def resolve_type(spec: dict, schemas: dict, persisted: dict) -> tuple[str, str | None]:
    """Return (postgres type, referenced table or None). An empty type means no column."""
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
        target = _target_of(ref, schemas)
        if isinstance(target, dict):
            tag = persistence_of(target)
            if isinstance(tag, str) and _NOT_STORED.search(tag.strip()):
                return "", None      # computed on read: no stored copy
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
            # `Money` that is the amount alone: **currency and scale resolve rather than being
            # stored**, so holding AED against nine million rows in one region is nine million
            # copies of a fact that cannot differ.
            #
            # **Amended 20 September, and the rule survives the amendment.** ADR-0018 now lets a
            # venue set its own trading currency, frozen once it has traded — so "cannot differ"
            # is no longer true *between* venues. It is still true for any row, because every
            # amount resolves from something that denominates it and none of those moved:
            # a posting from `ledger.account.currency`, a payment from its own `tenderCurrency`,
            # a wallet from `wallet.wallet.currency`, everything else from the venue's frozen
            # value. **The one amount with nothing to resolve from was `ledger.settlement`** —
            # a provider file for a period, belonging to no account — and that gained a currency
            # of its own rather than a hole in this rule.
            col = target.get("x-ticvai-persistence-column")
            if col:
                return col, None
            if target.get("type") == "object":
                return "jsonb", None
        # A shared object with no declared column stays jsonb — splitting it would guess at an
        # invariant nobody wrote down.
        return "jsonb", None

    t = spec.get("type")
    if isinstance(t, list):          # OpenAPI 3.1: ["string", "null"] — nullability is separate
        t = next((x for x in t if x != "null"), None)
    if t == "array":
        return _array_type(spec.get("items") or {}, schemas, persisted), None
    if "enum" in spec:
        return "text", None
    return TYPE_MAP.get((t, spec.get("format")), TYPE_MAP.get((t, None), "text")), None



# **Column names follow `naming-and-style.md` §6.1 and §5.2, mechanically, where the rule is
# mechanical** (audit R093, 26 September). The wire keeps its field names; only the column moves,
# exactly as `x-ticvai-column` already does for the 24 September money renames. A field that
# carries `x-ticvai-column` is never renamed here — somebody chose that name.
#
# Covered: a foreign key names its target and ends `_id` (`<referenced_table>_id`; an actor
# `*_by` is `*_by_principal_id`, the form `collected_by_principal_id` already uses); a boolean
# reads as an assertion (`is_active`, never `active`); a reserved word is not a column name
# (`from`/`to` are the validity window §5.2 names `valid_from`/`valid_to`).
#
# **Not covered, because the standard does not settle them:** bare money names (`unit_price`,
# `line_total`, `balance` …) need a gross/net decision per column; `*_at` columns typed `date`
# need a decision on whether the field is a day or an instant; index and policy names are
# `derive-ddl.py`'s.
_RESERVED_RENAME = {"from": "valid_from", "to": "valid_to", "order": "sort_order",
                    "table": "table_name"}
_ASSERTING = {"is", "has", "have", "can", "requires", "require", "should", "allows", "allow",
              "was", "were", "will", "does", "needs", "must", "supports", "accepts", "carries",
              "contains", "counts", "crosses", "touches", "takes", "participates", "overrides",
              "breaches", "holds", "includes", "include", "may", "uses", "enforce", "enforces",
              "show", "shows", "notify", "exclude", "explain", "respect", "prevent", "restore",
              "retain", "release", "refund", "reroute", "revalidate", "skip", "extend", "degrade",
              "cache", "cascade", "failover", "alert", "offer", "force", "capture", "no"}


def conventional_name(column: str, ctype: str, references: str | None) -> str:
    """The column name the naming standard asks for; the input unchanged where it already fits."""
    if column in ("from", "to"):
        # Only an instant or a day is a validity window; a time-of-day `from` is left for a person.
        return _RESERVED_RENAME[column] if ctype in ("timestamptz", "date") else column
    if column in _RESERVED_RENAME:
        return _RESERVED_RENAME[column]
    if references and ctype in ("uuid", "text") and column != "id" and not column.endswith("_id"):
        stem = references.split(".", 1)[-1]
        if column.endswith("_by") and references == "identity.principal":
            return column + "_principal_id"
        base = column[:-4] if column.endswith("_ref") else column
        if stem == base or stem.startswith(base + "_"):
            return stem + "_id"
        return base + "_id"
    if ctype == "boolean":
        tokens = column.split("_")
        if tokens[0] in _ASSERTING:
            return column
        if len(tokens) == 1 and not column.endswith("s"):
            return "is_" + column            # enabled -> is_enabled, active -> is_active
        if tokens[0] == "auto":
            return "is_" + column            # auto_switch -> is_auto_switch
        if len(tokens) > 1 and re.search(r"(ed|able|ible)$", tokens[-1]):
            return "is_" + column            # attendee_capture_required -> is_attendee_capture_required
    return column


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


def required_of(body, schemas: dict | None = None, _seen=None) -> set:
    """Required property names, flattened across `allOf` exactly as `properties_of` flattens.

    **Reading only the top level made every composed schema optional.** `SeatMap` is
    `SeatMapSummary` plus an object, so its `id`, `name` and `venueId` lost NOT NULL the moment the
    summary stopped lending its own required list to the table (audit R109).
    """
    if not isinstance(body, dict):
        return set()
    _seen = _seen or set()
    out = set(body.get("required") or [])
    for branch in (body.get("allOf") or []):
        if not isinstance(branch, dict):
            continue
        ref = branch.get("$ref")
        if ref and schemas is not None:
            name = ref.split("/")[-1]
            if name not in _seen:
                out |= required_of(schemas.get(name), schemas, _seen | {name})
            continue
        out |= required_of(branch, schemas, _seen)
    return out


def _declared_renames() -> list[dict]:
    """The table renames declared in derive-schema-history.py (`RENAMES`), read from its source
    so importing it cannot run anything. Empty if the file cannot be read."""
    import ast
    try:
        tree = ast.parse((ROOT / "tools" / "derive-schema-history.py").read_text(encoding="utf-8"))
    except (OSError, SyntaxError):
        return []
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "RENAMES"
                                                for t in node.targets):
            return ast.literal_eval(node.value)
    return []


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--strict", action="store_true",
                    help="exit non-zero while any table holds only keys (audit R087)")
    args = ap.parse_args()

    contracts = load_contracts()
    all_schemas: dict[str, dict] = {}
    persisted: dict[str, str] = {}          # schema name -> table
    owner: dict[str, str] = {}              # table -> contract
    retired: dict[str, set[str]] = {}       # table -> columns the contract has withdrawn
    schema_contract: dict[str, str] = {}    # schema name -> contract it was registered from
    for name, (_, doc) in contracts.items():
        for sname, body in ((doc.get("components") or {}).get("schemas") or {}).items():
            # **An alias does not claim a name over a definition.** `subscription.ModuleKey` became a
            # bare `$ref` to `common.ModuleKey` on 22 September, and because `satellite/` loads
            # before `shared/`, first-wins registered the alias — a body with no `enum` and no
            # `type` — as *the* `ModuleKey`. Every reference then fell through to `jsonb`, and
            # `whitelabel.module_enablement.module_key` regressed from `text NOT NULL` without a
            # line of `white-label.yaml` changing. **A pure-`$ref` schema is legal OpenAPI**; the
            # fault was the registry treating a pointer as a definition.
            prev = all_schemas.get(sname)
            if prev is None or (_is_alias(prev) and not _is_alias(body)):
                all_schemas[sname] = body
            if isinstance(body, dict):
                table = persistence_of(body)
                if isinstance(table, str) and "." in table and "—" not in table:
                    # A schema may name a parent and a child — `fnb.service_order + fnb.service_order_line`.
                    # **The properties belong to the parent**; the child comes from the nested array,
                    # which this tool deliberately skips rather than flattening. Taking the whole
                    # string as a table name created 25 tables that do not exist.
                    table = table.split("+")[0].strip()
                    persisted[sname] = table
                    schema_contract[sname] = name
                    for rc in retired_of(body):
                        retired.setdefault(table, set()).add(rc)

    # **A summary is a projection of a row, not a second source of its columns** (audit R109).
    # `orders.EntitlementSummary` — one entitlement a guest holds — carried
    # `x-ticvai-persistence: catalogue.entitlement_template`, and merging it with
    # `EntitlementTemplate` gave the pre-sale template `entitlement_id NOT NULL`, `status NOT NULL`,
    # `entries_used` and `last_used_at`: an instance's fields on a definition, a template ->
    # entitlement -> template cycle, and a create operation that cannot supply its own NOT NULLs.
    #
    # Where a table is persisted by a full schema and by a `*Summary`, the full schema alone
    # names the columns. The summary still resolves as a reference to the table (a `$ref` to it
    # is still a key), and a table persisted *only* by a summary keeps it.
    by_table: dict[str, list[str]] = {}
    for sname, table in persisted.items():
        by_table.setdefault(table, []).append(sname)
    projection_only: set[str] = set()
    for table, snames in by_table.items():
        if len(snames) > 1 and any(not s.endswith("Summary") for s in snames):
            projection_only |= {s for s in snames if s.endswith("Summary")}
    # The owner is the contract of a schema that contributes columns — last wins, as before.
    for sname, table in persisted.items():
        if sname not in projection_only:
            owner[table] = schema_contract[sname]

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
    declared_children: set[str] = set()     # children a `+` persistence tag names outright
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
                    declared_children.add(child)

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
            # **An implied child lives in its parent's schema.** Matching on the bare name let the
            # retired `control.footer_config_column` claim `whitelabel.footer_config`'s `columns`
            # after R163 moved the footer, so the old table was re-derived every run and the
            # declared rename never took. It was the only cross-schema match in the package.
            if ptable.split(".")[0] != schema_part:
                continue
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
    child_rows: set[tuple[str, str]] = set()     # (parent schema, array property) held as rows
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
            if isinstance(pspec, dict) and pspec.get("x-ticvai-persisted") is False:
                continue
            ptype, fk = resolve_type(pspec, all_schemas, persisted)
            if not ptype:
                continue
            chosen = pspec.get("x-ticvai-column") if isinstance(pspec, dict) else None
            cols.append({
                "column": chosen or conventional_name(snake(prop), ptype, fk),
                "type": ptype,
                "required": "yes" if prop in req and not is_nullable(pspec) else "no",
                "source": f"{owner.get(child, '')}.{parent_schema}.{key}[].{prop}",
                "description": describe(pspec),
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
            # **The array that became this child's rows is not also a column on the parent.**
            # `Role.permissions` is `identity.role_permission`; a `permissions text[]` on the role
            # beside it would be the same data in two places with no source of truth (audit R111).
            child_rows.add((parent_schema, key))

    def _held_as_rows(sname: str, table: str, prop: str) -> bool:
        """An array property whose values live in a child table rather than on this row."""
        if (sname, prop) in child_rows:
            return True
        tail = snake(prop).rstrip("s")
        short = table.split(".")[-1]
        schema_part = table.split(".")[0]
        return any(t.startswith(f"{schema_part}.{short}_")
                   and t[len(schema_part) + len(short) + 2:].rstrip("s") == tail
                   for t in known_tables)

    homeless: list[str] = []
    for sname, table in sorted(persisted.items()):
        if sname in projection_only:
            continue
        body = all_schemas.get(sname) or {}
        required = required_of(body, all_schemas)
        cols = []
        for prop, spec in properties_of(body, all_schemas).items():
            if isinstance(spec, dict) and spec.get("type") == "array" \
                    and _held_as_rows(sname, table, prop):
                continue
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
                # **An array of objects with no child table is data with nowhere to go** (audit
                # R179): `Outlet.openingHours` produced no column and no table, so an outlet
                # stores no hours. Listed so the contract can declare the child (`A + B`) or mark
                # the field `x-ticvai-persisted: false`; a table is not invented here.
                if isinstance(spec, dict) and spec.get("type") == "array" \
                        and not _held_as_rows(sname, table, prop):
                    homeless.append(f"{table} <- {sname}.{prop}")
                continue
            chosen = spec.get("x-ticvai-column") if isinstance(spec, dict) else None
            cols.append({
                # **`x-ticvai-column` names the column when the field's name would break the standard**
                # (24 September): naming-and-style 5.1 bans `total`, `price` and `value` alone, so
                # `PurchaseOrder.total` lands as `gross_amount` while the wire keeps `total`.
                # Without one, the mechanical parts of the standard apply (`conventional_name`).
                "column": chosen or conventional_name(snake(prop), ptype, fk),
                "type": ptype,
                "required": "yes" if prop in required and not is_nullable(spec) else "no",
                "source": f"{owner.get(table, '')}.{sname}.{prop}",
                "description": describe(spec),
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

    # **What a summary used to contribute is withdrawn, not merely no longer derived.** The graph
    # was built from those columns, so without this `entitlement_template.entitlement_id` comes
    # straight back as a relationship-graph column on the same run — the loop `retired_of`
    # describes.
    for sname in sorted(projection_only):
        table = persisted[sname]
        have = {c["column"] for c in derived.get(table, [])}
        for prop, spec in properties_of(all_schemas.get(sname) or {}, all_schemas).items():
            ptype, fk = resolve_type(spec, all_schemas, persisted)
            chosen = spec.get("x-ticvai-column") if isinstance(spec, dict) else None
            for name in {chosen or snake(prop), chosen or conventional_name(snake(prop), ptype, fk)}:
                if name not in have:
                    retired.setdefault(table, set()).add(name)

    filled = [t for t in derived if not existing.get(t)]
    changed = [t for t in derived if existing.get(t) and len(existing[t]) != len(derived[t])]
    untouched = [t for t in existing if t not in derived]

    print(f"{len(persisted)} persisted schemas across {len(contracts)} contracts")
    print(f"  tables gaining columns for the first time: {len(filled)}")
    if filled:
        print("   ", ", ".join(sorted(filled)[:8]) + (" …" if len(filled) > 8 else ""))
    print(f"  tables whose column count changes: {len(changed)}")
    print(f"  arrays stored nowhere (no column, no child table): {len(homeless)}")
    for h in homeless:
        print(f"     {h}")
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
        # **The graph's `required` is not evidence that a column cannot be null.** An actor
        # column paired with a nullable instant is nullable with it: `revoked_by` is empty for
        # exactly as long as `revoked_at` is, and `identity.delegated_access.revoked_by NOT NULL`
        # made every live delegation unwritable (audit R089).
        _req = e.get("required") or "no"
        _m = re.match(r"^(.*)_by(?:_principal_id)?$", col)
        if _req == "yes" and _m:
            _at = next((c for c in row if c["column"] == _m.group(1) + "_at"), None)
            if _at is not None and _at.get("required") != "yes":
                _req = "no"
        row.append({
            "column": col,
            "type": "uuid",
            "required": _req,
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

    def _from_contract(c) -> bool:
        return str(c.get("source", "")).count(".") >= 2 and not str(c.get("source", "")).startswith(
            "derive-schema.py")

    def _from_graph(c) -> bool:
        return c.get("source") == "relationship-graph.json"

    # **One parent, one key** (audit R102). The graph was built from a hand-patched schema
    # reference, and wherever it named a column differently from the contract the loop above
    # appended a second one: `catalogue.performance` had `admission_rules_id` (the contract's, a
    # convention index) *and* `admission_profile_id NOT NULL` (the graph's, the real foreign key);
    # `orders.cart_line` had `inventory_hold_id` and `lease_id`; `reporting.report_column` had
    # `report_definition_id` and `definition_id`. Two keys to one row that nothing keeps equal.
    #
    # **The contract's column is the one kept, and it takes the edge's enforcement.** A graph-only
    # key is dropped where the table already has exactly one contract column pointing at the same
    # table *and* that column is named for it. Actor and scope targets (`identity.principal`,
    # `platform.scope`) are left alone: `created_by`, `revoked_by` and `approved_by` are three
    # different people, not one key under three names. A same-role pair (`collected_by` and
    # `collected_by_principal_id`) is caught by the naming pass below instead.
    _MANY_ROLES = {"identity.principal", "platform.scope"}
    _deduped = []
    for table, row in existing.items():
        drop = []
        for g in row:
            tgt = g.get("references")
            if not (_from_graph(g) and tgt) or tgt in _MANY_ROLES or not g["column"].endswith("_id"):
                continue
            same = [c for c in row if c is not g and _from_contract(c) and c.get("references") == tgt]
            if len(same) != 1:
                continue
            keep = same[0]
            stem, kstem = tgt.split(".", 1)[-1], keep["column"][:-3] if keep["column"].endswith("_id") else ""
            if not kstem or not (kstem == stem or stem.endswith("_" + kstem) or kstem.endswith(stem)):
                continue
            if g.get("enforced") == "yes" and keep.get("enforced") != "yes":
                keep["referenceHow"] = "declared"
                keep["enforced"] = "yes"
                keep.setdefault("referenceKind", g.get("referenceKind", "reference"))
            drop.append(g["column"])
            _deduped.append(f"{table}.{g['column']} -> {keep['column']}")
        if drop:
            existing[table] = [c for c in row if not (_from_graph(c) and c["column"] in drop)]
    print(f"  duplicate graph keys folded into the contract's column: {len(_deduped)}")
    for d in _deduped:
        print(f"     {d}")

    # **A `+` persistence tag declares a parent** (audit R200). `StockCount` persists to
    # `inventory.count + inventory.count_line`: the contract says outright that a count line
    # belongs to a count. Its `count_id` was still a convention — indexed, never constrained —
    # while `cart_line`, `order_line` and `purchase_order_line` were real foreign keys, and because
    # only enforced references are retyped below, `count_line.count_id uuid` never matched
    # `count.id text`. The parent key of a declared child is a declared reference.
    _promoted = 0
    for child in sorted(declared_children):
        # The key the child pass derived, or — where the parent schema carries no nested array,
        # as `StockCount` does not — the `<parent>_id` the child's own schema already has.
        parent_table = child_of[child][1]
        pk = parent_key.get(child) or {
            "column": snake(parent_table.split(".")[-1]) + "_id", "references": parent_table}
        if pk["references"] == child:
            continue
        for c in existing.get(child, []):
            if c["column"] == pk["column"] and c.get("enforced") != "yes":
                c["references"] = pk["references"]
                c["referenceKind"] = c.get("referenceKind") or "reference"
                c["referenceHow"] = "declared"
                c["enforced"] = "yes"
                _promoted += 1
    print(f"  declared-child parent keys made foreign keys: {_promoted}")

    # **Names, once every source has contributed a column** (audit R093). Contract columns were
    # named at derivation; this catches the graph's and any hand-kept ones, whose edges still
    # carry last run's names until `derive-relationships` re-reads this file. Where the
    # conventional name is already taken, a graph-sourced duplicate goes; two contract columns
    # colliding are left for a person, and printed.
    _renamed, _clash = [], []
    for table, row in existing.items():
        if "." not in table or ":" in table:
            continue
        for c in list(row):
            new = conventional_name(c["column"], c.get("type", ""), c.get("references"))
            if new == c["column"] or not _from_graph(c) and _from_contract(c):
                continue
            other = next((x for x in row if x is not c and x["column"] == new), None)
            if other is None:
                _renamed.append(f"{table}.{c['column']} -> {new}")
                c["column"] = new
            elif _from_graph(c):
                if c.get("enforced") == "yes" and other.get("references") == c.get("references"):
                    other["referenceHow"], other["enforced"] = "declared", "yes"
                row.remove(c)
            else:
                _clash.append(f"{table}.{c['column']} (wants {new}, taken)")
        # A contract column renamed at derivation leaves last run's graph copy under the new name
        # beside it: keep the contract's.
        seen: dict[str, dict] = {}
        for c in list(row):
            prev = seen.get(c["column"])
            if prev is None:
                seen[c["column"]] = c
                continue
            loser = c if _from_graph(c) or not _from_graph(prev) else prev
            winner = prev if loser is c else c
            if loser.get("enforced") == "yes" and winner.get("references") == loser.get("references"):
                winner["referenceHow"], winner["enforced"] = "declared", "yes"
            row.remove(loser)
            seen[c["column"]] = winner
    print(f"  columns renamed to the naming standard after the merge: {len(_renamed)}")
    for d in _renamed:
        print(f"     {d}")
    if _clash:
        print(f"  columns that break the naming standard and cannot be renamed here: {len(_clash)}")
        for d in _clash:
            print(f"     {d}")

    # **An actor column is nullable with its instant**, whichever source added it (audit R089).
    # The append above handles a new column; this handles one a previous run already kept.
    _relaxed = 0
    for table, row in existing.items():
        names = {c["column"]: c for c in row}
        for c in row:
            m = re.match(r"^(.*)_by(?:_principal_id)?$", c["column"])
            if not (m and _from_graph(c) and c.get("required") == "yes"):
                continue
            at = names.get(m.group(1) + "_at")
            if at is not None and at.get("required") != "yes":
                c["required"] = "no"
                _relaxed += 1
    print(f"  actor columns made nullable with their instant: {_relaxed}")

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

    # **A table holding nothing but keys is a stub, whatever its comment promises** (audit R087).
    # `identity.principal_credential` is (id, principal_id) under a comment about a credential
    # hash; `games.credit_ledger` is (id, card_id) under "credits bought, played and won". Every
    # structural check passed them: they have columns, a key and a relationship. **What none asked
    # is whether any column holds the thing the table is for.**
    #
    # This cannot be fixed here — the missing columns are contract content (a hash, an amount, an
    # expiry) that nobody has written. It is printed on every run so the list stays visible, and
    # `--strict` fails on it once the contracts are expected to be complete.
    _stubs = []
    for _t in sorted(_real):
        _row = existing.get(_t) or []
        _k = _own_key(_t, [c["column"] for c in _row])
        if _row and not [c for c in _row if c["column"] != _k and not c.get("references")]:
            # A join table is keys by design (`<a>_<b>`, naming-and-style §6.1): every target it
            # points at is named in its own name.
            _fks = [c["references"] for c in _row if c.get("references")]
            _stem = _t.split(".", 1)[1]
            if len(_fks) >= 2 and all(f.split(".", 1)[1].split("_")[-1] in _stem for f in _fks):
                continue
            _stubs.append(f"{_t} ({', '.join(c['column'] for c in _row)})")
    print(f"  tables holding only keys — contract content missing: {len(_stubs)}")
    for _s in _stubs:
        print(f"     {_s}")

    # **A declared rename retires the old name here, or nowhere.** This tool keeps any table the
    # contracts no longer describe (it adds knowledge, it does not discard it), so when audit R165
    # renamed `resources.session_participant` to `performance_participant` and R163 moved
    # `control.footer_config*` to `whitelabel.*`, the contracts produced the new tables and the old
    # ones stayed beside them -- the DDL created both, the relationship graph re-derived edges for
    # both, and `derive-schema-history` reported every one NOT APPLIED. The renames are a
    # judgement already written down in `derive-schema-history.py`; this reads them rather than
    # restating them. Only where the new name has columns and the contracts no longer describe the old one:
    # a rename declared ahead of its contract edit must not delete a table that is still live.
    # The hand-written note travels with the table, because it describes the same rows.
    _renamed_tables = []
    for _r in _declared_renames():
        _old, _new = _r["from"], _r["to"]
        # `existing`, not `derived`, for the new name: a child table (`footer_config_column`) is
        # built from its parent's nested array and never appears in `derived`.
        if _old not in existing or _old in derived or not existing.get(_new):
            continue
        existing.pop(_old, None)
        _storage = S.get("storage") or {}
        _note = str(_storage.get(_old) or "")
        if _note and "No description has been written" not in _note and (
                "No description has been written" in str(_storage.get(_new) or "")
                or not str(_storage.get(_new) or "").strip()):
            _storage[_new] = _note
        for _k in ("storage", "store", "origin", "lineage"):
            if isinstance(S.get(_k), dict) and _old in S[_k]:
                if _k == "store":
                    S[_k].setdefault(_new, S[_k][_old])
                S[_k].pop(_old, None)
        _renamed_tables.append(f"{_old} -> {_new}")
    print(f"  tables retired by a declared rename: {len(_renamed_tables)}")
    for _d in _renamed_tables:
        print(f"     {_d}")

    S["cols"] = existing
    ref_path.write_text(json.dumps(S), encoding="utf-8")

    empty = [t for t in (set(S["cols"]) | set(S.get("storage", {}))) if not S["cols"].get(t)]
    print(f"\n  tables still with no columns: {len(empty)}")
    if empty:
        print("   ", ", ".join(sorted(empty)[:10]) + (" …" if len(empty) > 10 else ""))
    print(f"  → {ref_path.relative_to(ROOT)}")
    if args.strict and _stubs:
        print(f"  --strict: {len(_stubs)} table(s) hold only keys", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
