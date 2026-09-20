#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase 3 of the schema merge: the tables we accepted, generated from their columns.

**Their columns, not ours.** We accepted these tables, so we take the shape they specified
rather than inventing one — every column, type, length and nullability below is read out of
`TICVAI_16_Services_AND_Tables_UPDATED (1).xlsx`, which is the only honest source for a table
we did not design.

Three transforms are applied on the way in, and each is a position we already stated:

    the prefix              access_change_id -> id, access_point_code -> code. **This is the
                            645-of-743 position applied in practice** rather than argued: they
                            prefix every column with its table name and we do not
    the scope column        their scope_id / tenant_scope_id is a uuid pointing at a scope row.
                            Ours is scope_path, a materialised path, because ADR-0018 addresses
                            configuration by path and 58 profiles already do
    the placement           a table goes where the decision log put it, not where their sheet
                            has it: their four payment tables into `payments`, their tier
                            tables into `subscription`, their rental agreement into `rental`

**No operations and no paths are added.** A component schema carrying `x-ticvai-persistence`
is enough for `derive-schema` to produce the table, so phase 3 lands 60-odd tables without
adding a single screen to the backlog. Wiring them to operations is the next phase and is
deliberately separate, because that is the part that grows the drawing work.

    python3 tools/applied/schema-merge-phase-3-additive-20-september.py --apply
"""
import collections
import io
import json
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
H = os.path.join(ROOT, "handoff")

# Where a schema's new tables are written. `pricing` has no contract of its own and does not
# need one: decision 5 assigns it to CatalogueService, so its schemas live beside the other
# catalogue ones and only the persistence tag says `pricing.`.
CONTRACT_OF = {
    "access": "spine/access.yaml",
    "catalogue": "spine/catalogue.yaml",
    "pricing": "spine/catalogue.yaml",
    "fnb": "satellite/fnb.yaml",
    "identity": "spine/identity.yaml",
    "inventory": "satellite/inventory.yaml",
    "marketing": "satellite/marketing-crm.yaml",
    "orders": "spine/orders.yaml",
    "payments": "satellite/payments.yaml",
    "platform": "spine/tenancy.yaml",
    "rental": "satellite/rental.yaml",
    "retail": "satellite/retail.yaml",
    "seating": "satellite/seating.yaml",
    "subscription": "satellite/subscription.yaml",
    "sync": "spine/cross-region.yaml",
    "wallet": "satellite/wallet.yaml",
    "whitelabel": "satellite/white-label.yaml",
    "workforce": "satellite/workforce.yaml",
}

# their table -> ours, where the decision log moved it. Everything else keeps its name.
PLACEMENT = {
    "orders.currency_rule": "payments.currency_rule",
    "orders.payment_eligibility_rule": "payments.eligibility_rule",
    "orders.payment_fee_rule": "payments.fee_rule",
    "orders.payment_method_config": "payments.method_config",
    "orders.deposit_activity": "payments.deposit_activity",
    "platform.tier_allowance": "subscription.tier_allowance",
    "platform.tier_module": "subscription.tier_module",
    "resources.rental_inspection_item": "rental.inspection_item",
    "resources.rental_agreement": "rental.agreement",
    "resources.rental_agreement_item": "rental.agreement_item",
    "identity.customer_extra_field": "marketing.guest_extra_field",
    "identity.customer_extra_option": "marketing.guest_extra_option",
    "identity.customer_extra_value": "marketing.guest_extra_value",
    "catalogue.membership_benefit": "catalogue.membership_benefit",
    "catalogue.membership_program": "catalogue.membership_programme",
}

# Tables we accepted but that are NOT new here: phase 2 already created the destination, or
# the columns belong on a table we hold. Taken as a body, not as a table.
NOT_NEW = {
    "marketing.points_earning_rule",   # phase 2 renamed marketing.loyalty_tier into this
}

# Their scope column, whatever they called it, is our scope_path.
SCOPE_COLS = {"scope_id", "tenant_scope_id", "tenancy_scope_id", "venue_scope_id"}

TYPES = {
    "uniqueidentifier": ("string", "uuid"),
    "nvarchar": ("string", None),
    "varchar": ("string", None),
    "nchar": ("string", None),
    "char": ("string", None),
    "text": ("string", None),
    "ntext": ("string", None),
    "bit": ("boolean", None),
    "int": ("integer", None),
    "bigint": ("integer", None),
    "smallint": ("integer", None),
    "tinyint": ("integer", None),
    "decimal": ("number", None),
    "numeric": ("number", None),
    "money": ("number", None),
    "float": ("number", None),
    "real": ("number", None),
    "date": ("string", "date"),
    "datetime": ("string", "date-time"),
    "datetime2": ("string", "date-time"),
    "datetimeoffset": ("string", "date-time"),
    "time": ("string", None),
    "varbinary": ("string", None),
    "xml": ("string", None),
    "geography": ("string", None),
}


def camel(snake_name):
    parts = snake_name.split("_")
    return parts[0] + "".join(p[:1].upper() + p[1:] for p in parts[1:])


def pascal(table):
    return "".join(p[:1].upper() + p[1:] for p in table.replace(".", "_").split("_"))


def prefixes_of(short):
    """Every way their habit could spell this table's name, longest first.

    A table called `payment_fee_rule` landing as `payments.fee_rule` carries columns named
    `fee_name` and `fee_category` as well as `payment_fee_rule_id`, so the candidates are the
    whole name, every leading run of its tokens, and its last token on its own."""
    parts = short.split("_")
    cands = {short}
    for i in range(1, len(parts) + 1):
        cands.add("_".join(parts[:i]))
    cands.add(parts[-1])
    return sorted(cands, key=len, reverse=True)


KEEP = {"created_at", "updated_at", "created_by", "updated_by", "valid_from", "valid_to"}


def strip_prefix(col, short):
    """Their habit: every column carries its table's name. Ours do not."""
    if col in KEEP:
        return col
    # **Only the full table name may produce a bare `id`.** On `access.access_change` the
    # candidate `access` would otherwise turn `access_id`, a foreign key to another table,
    # into this table's own key — which is how a rename silently becomes a data error.
    if col == short + "_id":
        return "id"
    for cand in prefixes_of(short):
        if col.startswith(cand + "_") and len(col) > len(cand) + 1:
            rest = col[len(cand) + 1:]
            if rest == "id" or rest.isdigit() or not rest:
                continue
            return rest
    return col


def prop_of(col, short):
    name = col["column"]
    if name in SCOPE_COLS:
        return "scopePath", {"type": "string", "nullable": True}, False
    name = strip_prefix(name, short)
    base, fmt = TYPES.get((col.get("type") or "").lower(), ("string", None))
    spec = {"type": base}
    if fmt:
        spec["format"] = fmt
    size = (col.get("size") or "").strip()
    if base == "string" and not fmt and size.isdigit() and int(size) <= 4000:
        spec["maxLength"] = int(size)
    if col.get("nullable"):
        spec["nullable"] = True
    return camel(name), spec, not col.get("nullable")


def render(schema_name, table, purpose, props, required):
    """Four-space indented block, matching every other schema in these files."""
    out = ["    %s:" % schema_name,
           "      type: object",
           "      x-ticvai-persistence: %s" % table]
    if purpose:
        text = re.sub(r"\s+", " ", purpose).strip().replace("'", "''")
        out.append("      description: '**Taken from the backend workbook, 20 September.** %s'"
                   % text[:400])
    if required:
        out.append("      required:")
        out.extend("      - %s" % r for r in required)
    out.append("      properties:")
    for name, spec in props:
        out.append("        %s:" % name)
        for k in ("type", "format", "maxLength", "nullable"):
            if k not in spec:
                continue
            v = spec[k]
            v = "true" if v is True else "false" if v is False else str(v)
            out.append("          %s: %s" % (k, v))
    return "\n".join(out) + "\n"


def main():
    apply = "--apply" in sys.argv[1:]
    verdicts = json.load(io.open(os.path.join(H, "merge-verdicts.json"), encoding="utf-8"))
    theirs = json.load(io.open(os.path.join(H, "their-columns.json"), encoding="utf-8"))
    ours = set(json.load(io.open(os.path.join(H, "schema-reference.json"),
                                 encoding="utf-8")).get("cols") or {})

    TAKE = {"ADDITIVE", "TAKE THEIRS", "MERGE"}
    wanted = []
    for t in sorted(verdicts):
        if verdicts[t][0] not in TAKE:
            continue
        target = PLACEMENT.get(t, t)
        if target in ours or target in NOT_NEW:
            continue
        if t not in theirs["tables"]:
            print("    !! %-36s no columns in their workbook" % t)
            continue
        wanted.append((t, target))

    by_file = collections.defaultdict(list)
    skipped = []
    for src, target in wanted:
        schema, short = target.split(".", 1)
        rel = CONTRACT_OF.get(schema)
        if not rel:
            skipped.append(target)
            continue
        props, required = [], []
        seen = set()
        for col in theirs["tables"][src]:
            name, spec, req = prop_of(col, short)
            if name in seen:
                continue
            seen.add(name)
            props.append((name, spec))
            if req and name != "id":
                required.append(name)
        by_file[rel].append(
            (pascal(target), target, theirs["purpose"].get(src, ""), props, required[:8]))

    print("  %d new table(s) across %d contract(s)" % (len(wanted), len(by_file)))
    for rel in sorted(by_file):
        print("    %-28s %d" % (rel, len(by_file[rel])))
    if skipped:
        print("    !! no contract mapped: %s" % ", ".join(sorted(skipped)))

    written = 0
    for rel, items in sorted(by_file.items()):
        p = os.path.join(ROOT, "contracts", rel)
        s = io.open(p, encoding="utf-8").read()
        m = re.search(r"^  schemas:\n", s, re.M)
        if not m:
            print("    !! %s has no components.schemas block" % rel)
            continue
        existing = set(re.findall(r"^    ([A-Za-z][A-Za-z0-9]*):\n", s, re.M))
        blocks = []
        for schema_name, table, purpose, props, required in items:
            name = schema_name
            while name in existing:
                name += "Table"
            existing.add(name)
            blocks.append(render(name, table, purpose, props, required))
            written += 1
        out = s[:m.end()] + "".join(blocks) + s[m.end():]
        try:
            yaml.safe_load(out)
        except Exception as e:
            print("    !! %s would not parse after insert: %s" % (rel, str(e)[:120]))
            continue
        print("    %-28s +%d schema(s), parses" % (rel, len(blocks)))
        if apply:
            io.open(p, "w", encoding="utf-8", newline="\n").write(out)

    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    print("\n  %d schema(s) written. Run tools/refresh.sh: derive-schema reads the tags and the\n"
          "  tables appear. No operation was added, so no screen was either." % written)
    return 0


if __name__ == "__main__":
    sys.exit(main())
