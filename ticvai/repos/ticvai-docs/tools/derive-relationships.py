#!/usr/bin/env python3
"""Derive handoff/relationship-graph.json from the schema reference and the lineage.

The graph was hand-maintained and drifted. On 18 August it described 540 relationships across
192 tables while the package held 352 tables — **it had not been touched since the schema grew
past it**, and "Tables with a relationship" read 79% because 160 tables the graph had never
heard of counted as orphans.

Sources, in order of authority:

  1. Declared: what the contracts assert — a `$ref` to a persisted schema,
     `x-ticvai-references`, or the parent key of a child table — read off the contracts
     themselves, plus hand-written columns and legacy `declared` labels that the naming
     evidence does not refute (audit root R082). Only these become enforced foreign keys.
  2. Convention: a `*_id` column naming a table that exists. Weaker, and marked as such; it
     becomes an index, never a constraint. Precedent is the same, carried from declarations.
  3. The lineage: two tables written by one operation are related in fact even where no column
     says so. Marked `ambient` — it is a real coupling and not a foreign key.

**A hand-maintained graph that drifts is worse than none**, because it reports confidently. This
replaces it with something that cannot drift without the schema drifting first.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# Windows consoles are cp1252 and this tool closes by printing a unicode arrow. **The write
# has already happened by then**, so the traceback reported a failure on a run that succeeded
# — the most misleading shape an error can take.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
HANDOFF = ROOT / "handoff"



# ---------------------------------------------------------------------------------------------
# What the contracts actually assert.
#
# **A stored `referenceHow: declared` is not a declaration.** Audit root R082 (26 September):
# `schema-reference.json` carried 665 references marked `declared` and enforced, and **only 43 of
# them are asserted by a contract** — a `$ref` to a persisted schema, an `x-ticvai-references`
# annotation, or the parent key of a child table. The rest are bare `uuid` properties whose
# target was a name guess somebody once wrote into a hand-maintained graph, and this deriver
# read the stored label back as fact on every run. That is how `payments.token.provider_id`
# became an enforced foreign key into `ai.provider`, `inventory.movement.location_id` one into
# `fnb.delivery_location`, and `reporting.alert.rule_id` one into `approvals.rule` — while the
# right table sat in the same schema each time.
#
# So the contract is read directly, and the stored label is only a *legacy assertion* that has
# to survive a check against the naming evidence before it is carried forward (see
# `_refuted` below).
# ---------------------------------------------------------------------------------------------

def _load_derive_schema():
    """derive-schema.py, imported for its readers. Its `main()` is guarded and is not run."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("_derive_schema",
                                                  Path(__file__).resolve().parent / "derive-schema.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def contract_declarations(tables: set) -> tuple[dict, bool]:
    """Map `<Schema>.<property>` -> (table the contract says it points at, the only column name
    that declaration applies to, or None for any).

    Keyed without the contract prefix of a column's `source`, because schema names are global
    in the registry and the prefix is the table owner's contract, not always the schema's.

    Returns (that map, ok). `ok` is False when the contracts could not be read, and the
    caller then falls back to the stored labels rather than stripping every declaration.
    """
    try:
        ds = _load_derive_schema()
        contracts = ds.load_contracts()
    except Exception as exc:                     # pragma: no cover - environment problem
        print(f"  ! contracts unreadable ({exc}); stored referenceHow used as-is")
        return {}, False
    all_schemas: dict = {}
    persisted: dict = {}
    for _cname, (_, doc) in contracts.items():
        for sname, body in ((doc.get("components") or {}).get("schemas") or {}).items():
            prev = all_schemas.get(sname)
            if prev is None or (ds._is_alias(prev) and not ds._is_alias(body)):
                all_schemas[sname] = body
            if isinstance(body, dict):
                t = ds.persistence_of(body)
                if isinstance(t, str) and "." in t and "—" not in t:
                    persisted[sname] = t.split("+")[0].strip()

    def xref(spec) -> str | None:
        """`x-ticvai-references` names a schema (`assets.MediaAsset`) or a table."""
        if not isinstance(spec, dict):
            return None
        v = spec.get("x-ticvai-references")
        if not isinstance(v, str) or not v.strip():
            return None
        v = v.strip()
        if v in tables:
            return v
        return persisted.get(v.rsplit(".", 1)[-1])

    def target_of(spec) -> str | None:
        if not isinstance(spec, dict):
            return None
        try:
            _, fk = ds.resolve_type(spec, all_schemas, persisted)
        except TypeError:          # `type: [string, "null"]` on a schema nothing persists
            fk = None
        return fk or xref(spec)

    def items_props(arr) -> dict:
        if not isinstance(arr, dict):
            return {}
        items = arr.get("items") or {}
        if isinstance(items, dict) and items.get("$ref"):
            items = all_schemas.get(items["$ref"].rsplit("/", 1)[-1]) or {}
        return ds.properties_of(items, all_schemas)

    out: dict = {}
    for sname, body in all_schemas.items():
        props = ds.properties_of(body, all_schemas)
        for prop, spec in props.items():
            if isinstance(spec, dict) and spec.get("type") == "array":
                # The parent key of a child table has source `<contract>.<Parent>.<arrayProp>`
                # and is named `<parent>_id`. **Only that column** — an array of scalars
                # (`tags`, `menu_item_ids`) has the same source shape and is not a key.
                if sname in persisted and items_props(spec):
                    parent = persisted[sname]
                    out[f"{sname}.{prop}"] = (parent, parent.split(".", 1)[1] + "_id")
                for cprop, cspec in items_props(spec).items():
                    t = target_of(cspec)
                    if t:
                        out[f"{sname}.{prop}[].{cprop}"] = (t, None)
                continue
            t = target_of(spec)
            if t:
                out[f"{sname}.{prop}"] = (t, None)
    return out, True


def main() -> int:
    schema = json.loads((HANDOFF / "schema-reference.json").read_text(encoding="utf-8"))
    lineage = json.loads((HANDOFF / "api-data-lineage.json").read_text(encoding="utf-8"))

    cols: dict = schema.get("cols", {})
    storage: dict = schema.get("storage", {})
    # ,  and  are stores rather than tables.
    # **They appear in the lineage and are not relatable** — a foreign key into a cache is not a
    # thing, and counting them as orphans would understate the real coverage.
    tables = {t for t in (set(cols) | set(storage)) if "." in t and ":" not in t}

    rels: list[dict] = []
    seen: set = set()

    def add(frm: str, col: str, to: str, how: str, kind: str, required: str = "") -> None:
        key = (frm, col, to)
        # **Self-references are real edges.** `parent_location_id`, `failover_provider_id` and
        # `compound_on_tax_code_id` all point at their own table, and dropping them loses the
        # hierarchy they express.
        if key in seen or frm not in tables or to not in tables:
            return
        seen.add(key)
        rels.append({
            "frm": frm, "col": col, "to": to, "how": how,
            "cross": "yes" if frm.split(".")[0] != to.split(".")[0] else "",
            "required": required, "edgeKind": kind,
        })

    # 1. Declared references.
    #
    # **`referenceHow` is read, not just `references`.** The two derivers feed each other —
    # derive-schema annotates a column *from* this graph — so reading `references` alone promotes
    # last run's convention guess to this run's declaration. On 18 August that inflated declared
    # edges from 518 to 705 in one pass, and it would have kept climbing.
    #
    # **A number that grows because it was measured is the worst kind of drift**: it looks like
    # progress.
    #
    # **And reading `referenceHow` was not enough either (audit root R082, 26 September).** The
    # stored label is itself last run's output, and a missing label defaulted to `declared`, so a
    # guess that was ever labelled declared stayed declared — and became an enforced foreign key
    # in `900-foreign-keys.sql` — forever. A declaration is now read off the contract:
    #
    #   * contract-declared — a `$ref` to a persisted schema, `x-ticvai-references`, or the parent
    #     key of a child table. Always declared; the contract's target wins over anything stored.
    #   * hand-written — a column whose source is neither a contract property nor this graph
    #     (`storage only — pii schema`). Its stored label is the only statement there is, and kept.
    #   * legacy — a bare `uuid` property, or a column this graph created, still carrying a stored
    #     `declared` from the hand-maintained graph of August. Kept as declared **only if the
    #     naming evidence does not refute it** (`_refuted`); otherwise dropped, and the column is
    #     resolved afresh as a convention — which is an index, never a constraint.
    #
    #   Stored `convention` and `precedent` targets are never read back: they are recomputed.
    decl_by_prop, contracts_ok = contract_declarations(tables)

    col_type: dict = {}
    for table, columns in cols.items():
        for c in columns:
            col_type[(table, c["column"])] = (c.get("type") or "").lower()

    def is_contract_source(src: str) -> bool:
        return (src.count(".") >= 2 and src != "relationship-graph.json"
                and not src.startswith("derive-schema.py"))

    def own_key(table: str, name: str) -> bool:
        """`guest_link.guest_link_id`, `media_upload.upload_id`: the row's own identifier, not a link.

        `platform.guest_link` shipped `FOREIGN KEY (guest_link_id) REFERENCES
        platform.guest_link(guest_link_id)` — a key pointing at itself.
        """
        short = table.split(".", 1)[-1]
        stem = name[:-3] if name.endswith("_id") else name
        # `media_upload.upload_id` is its own key because no table is called `upload`;
        # `cell_tenant.tenant_id` is a link to `control.tenant`, which is.
        return (name == "id" or stem == short
                or (short.endswith("_" + stem) and not exact.get(stem)))

    def polymorphic(table: str, name: str) -> bool:
        """`source_id` beside `source_type`: the column points at one of several tables.

        `inventory.movement.source_id` was an enforced key into `ai.index_source` while its own
        `source_type` says "an order, a count, a transfer"; `approvals.request.subject_id` beside
        `subject_contract` was a key into `pii.subject`. **A column whose target is named by
        another column cannot be a foreign key**, and guessing one is how a stock movement came
        to reference a language-model index.
        """
        stem = name[:-3]
        return any((table, stem + sfx) in col_type
                   for sfx in ("_type", "_kind", "_contract", "_table", "_entity"))

    # **Column types are not evidence here.** `schema-reference.json` holds reference columns
    # whose type derive-schema has not yet aligned to the target's key (it retypes them after
    # this runs), so a type test refused `access.entitlement.order_line_id -> orders.order_line`
    # and sent it to `inventory.purchase_order_line` instead.

    FK_HOWS = ("declared", "convention", "precedent")
    schemas = {t.split(".", 1)[0] for t in tables}
    decided: dict = {}          # (table, column) -> how, one foreign-key edge per column
    declared_edges: list = []   # (table, column, target) — the only votes for precedent
    legacy: dict = {}           # (table, column) -> stored target awaiting its check
    legacy_req: dict = {}       # (table, column) -> the column's `required`, kept on the edge
    stats = {"contract": 0, "hand": 0, "legacy_kept": 0, "legacy_dropped": 0}
    dropped_examples: list = []

    def add_fk(table, name, target, how, required=""):
        if (table, name) in decided:
            return
        before = len(rels)
        add(table, name, target, how, "foreignKey", required)
        if len(rels) > before:
            decided[(table, name)] = how

    for table, columns in cols.items():
        for c in columns:
            name = c["column"]
            src = str(c.get("source", ""))
            req = "yes" if c.get("required") in ("yes", True) else ""
            stored = c.get("references")
            how = c.get("referenceHow")
            if how == "lineage" and stored:
                add(table, name, stored, "lineage", "ambient", req)
                continue
            if contracts_ok and is_contract_source(src):
                declared, only = decl_by_prop.get(src.split(".", 1)[1]) or (None, None)
                if declared and only and name != only:
                    declared = None
                if declared:
                    add_fk(table, name, declared, "declared", req)
                    declared_edges.append((table, name, declared))
                    stats["contract"] += 1
                elif stored and how == "declared":
                    legacy[(table, name)] = stored
                    legacy_req[(table, name)] = req
                continue
            if not contracts_ok and stored:
                # Contracts unreadable: keep the stored labels rather than strip every
                # declaration — but **an unlabelled reference is not a declaration** (R082).
                h = how if how in FK_HOWS else "convention"
                add_fk(table, name, stored, h, req)
                if h == "declared":
                    declared_edges.append((table, name, stored))
                continue
            if stored and src != "relationship-graph.json" and not is_contract_source(src):
                h = how if how in FK_HOWS else "convention"
                add_fk(table, name, stored, h, req)
                if h == "declared":
                    declared_edges.append((table, name, stored))
                    stats["hand"] += 1
                continue
            if stored and how == "declared":
                legacy[(table, name)] = stored
                legacy_req[(table, name)] = req

    # 2. Convention. A `*_id` column whose stem names a real table, in this schema or a
    #    well-known one. Weaker than declared and marked so — a reader should be able to tell
    #    which edges were asserted and which were inferred from a naming habit.
    # **A stem may be a prefix of the table name as well as the whole of it.** `developer_id`
    # points at `control.developer_account` and `entitlement_id` at `access.entitlement`; matching
    # only the full name left 23 tables orphaned on 18 August, most of them added that day.
    #
    # Exact match wins over prefix, and a prefix that matches two tables is ambiguous and is
    # skipped — **guessing between `control.tenant` and `platform.tenant` would be worse than
    # leaving the column unlinked.**
    #
    # **23 short names are held by two or more schemas** — `provider` by `ai` and `payments`,
    # `policy` by `whitelabel` and `ai`, `product` by `catalogue` and `rental`, `deposit` by
    # `ledger` and `orders`. `payments.fee_rule.provider_id` resolved to `ai.provider`: a card
    # fee pointing at a language-model vendor. **Resolution is per referring schema**, because a
    # table's own schema is the strongest evidence available about what it meant.
    exact: dict[str, list] = {}
    prefixes: dict[str, list] = {}
    suffixes: dict[str, list] = {}
    for t in tables:
        short = t.split(".", 1)[1]
        exact.setdefault(short, []).append(t)
        if "_" in short:
            head, rest = short.split("_", 1)
            prefixes.setdefault(head, []).append(t)
            suffixes.setdefault(rest, []).append(t)
        else:
            prefixes.setdefault(short, [])

    # **A link table is not the thing it links to.** `fnb.delivery_location_outlet` joins a
    # delivery location to an outlet; read as a suffix match it is "an outlet", and it captured
    # every `outlet_id` in `fnb` from `platform.outlet`. A name that splits into a table of its
    # own schema followed by any existing table name, and carrying a key for that second name,
    # is a link, and is not offered as a suffix candidate. (The head must be same-schema:
    # `reporting.delivery` + `inventory.location` does not make `fnb.delivery_location` a link.)
    shorts = {t.split(".", 1)[1] for t in tables}
    links = set()
    for t in tables:
        sch, short = t.split(".", 1)
        bits = short.split("_")
        for i in range(1, len(bits)):
            tail = "_".join(bits[i:])
            # ...and the row must carry a key for the second half. `fnb.menu_item` is `menu` +
            # `item` by spelling and holds no `item_id`: it is an item, not a link.
            if (f"{sch}.{'_'.join(bits[:i])}" in tables and tail in shorts
                    and any(c["column"] == tail + "_id" or c["column"].endswith("_" + tail + "_id")
                            for c in cols.get(t, []))):
                links.add(t)
                break
    for k in list(suffixes):
        suffixes[k] = [t for t in suffixes[k] if t not in links]

    # **A prefix match names what a table is *about*, and some of those are not the thing.**
    # `rental.location_rule` is a rule about a location, `whitelabel.tenant_config` a tenant's
    # settings, `marketing.customer_badge` a badge — and each captured every `location_id`,
    # `tenant_id` and `customer_id` in its schema. `developer_account` and `api_client` stay
    # matchable: an account *is* the developer as far as a key is concerned.
    ABOUT = {"rule", "rules", "config", "configuration", "setting", "settings", "policy", "log",
             "history", "audit", "snapshot", "member", "line", "mapping", "link", "stat",
             "stats", "summary", "version", "badge", "outlet", "template", "exception",
             "session", "code", "window", "slot", "event", "note", "tag", "grant",
             "membership"}

    def prefix_ok(stem: str, t: str) -> bool:
        short = t.split(".", 1)[1]
        if not short.startswith(stem + "_"):
            return True                    # a suffix match; judged elsewhere
        return short[len(stem) + 1:] not in ABOUT

    # 2a. **A media asset is not a maintenance asset.** Every `*_asset_id` resolved to the stem
    #     `asset`, which is `maintenance.asset` — the only table whose short name is `asset`.
    #     That made an icon, a product image, a terms PDF and two signature scans into pieces of
    #     venue equipment, and inflated the rental-to-maintenance coupling by 70% at the moment
    #     that coupling was the argument in a schema merge.
    #
    #     `outgoing`, `incoming`, `returned`, `missing` and `available` are rental equipment
    #     movements and stay with `maintenance.asset`, as does a bare `asset_id`. **Any other
    #     qualifier is left unlinked**, which is what this comment always said and the stem
    #     rules never did: `ai.knowledge_document.source_asset_id` and `venuemap.map.base_asset_id`
    #     (the illustrated map a guest sees) both landed on `maintenance.asset`.
    MEDIA_PREFIXES = ['icon', 'image', 'photo', 'logo', 'cover', 'background', 'branding', 'badge', 'signature', 'document', 'terms_document', 'mandate_text', 'schema', 'evidence', 'artefact']
    EQUIPMENT_PREFIXES = ['outgoing', 'incoming', 'returned', 'missing', 'available']
    _media = 0

    def area(t: str) -> str:
        """ADR-0039: `control` is its own database; every other schema is the tenant database."""
        return "control" if t.split(".", 1)[0] == "control" else "tenant"

    def same_db(table: str, pick: list) -> list:
        """**A tie across the database boundary is not a tie.** `tenant_id` names both
        `control.tenant` and `platform.tenant`; from a tenant-database table only one of them can
        ever be joined, and Postgres cannot enforce the other at all."""
        return [t for t in pick if area(t) == area(table)]

    head = lambda t: t.split(".", 1)[1].split("_")[0]

    def resolve(table: str, name: str) -> tuple:
        """(target, tiers) for a `*_id` column by naming alone.

        `tiers` lists every (tier, candidates) examined, in order, so a legacy target can be
        checked against the evidence. Target is None when the evidence is absent or ambiguous.

        **Six tests in strict order, per stem, longest stem first:**

          0. `<own table>_<stem>` in the referring schema — `reporting.alert.rule_id` is the
             alert's rule, `reporting.alert_rule`, not `approvals.rule`
          1. an EXACT name in the referring schema
          1b. a table in the referring schema whose name *ends* in the stem and which is of the
             same family (same first word) — `fnb.kitchen_exception.ticket_id` is a
             `fnb.kitchen_ticket`, `promotions.coupon_code.campaign_id` a
             `promotions.coupon_campaign`. Each of those lost to an exact name in another schema
             (`access.entitlement` by precedent, `marketing.campaign`) and shipped as an
             enforced key.
          2. an exact name anywhere, if only one table has it (a tie settled by the database
             boundary, ADR-0039)
          1c. a same-schema suffix table of another family — only when no exact name competes;
             when one does, the column is *contested* and left unlinked
             (`maintenance.work_order.source_plan_id`)
          3. a prefix in the referring schema (not one naming what the table is *about*)
          4. a prefix or suffix anywhere, if unambiguous

        Before all of them, a column that names a schema (`inventory_item_id`,
        `ledger_entry_id`) is looked up in that schema.

        `payments.fee_rule.provider_id` needs 1 before 3: `payments.provider` is exact and
        `payments.provider_connection` shares the prefix. `fnb.reservation_table.reservation_id`
        needs 1b/3 after 2 refuses: `retail.reservation` and `orders.reservation` are two exact
        matches and `fnb.table_reservation` is waiting in the suffix set.

        **The table itself is never a candidate for its own key**, and another table beats the
        table itself, and the table itself beats nothing — `maintenance.asset_category.
        parent_category_id` is a real self-reference.
        """
        tiers: list = []
        if table not in tables:
            return None, tiers
        schema = table.split(".", 1)[0]
        own = table.split(".", 1)[1]
        if not name.endswith("_id") or own_key(table, name) or polymorphic(table, name):
            return None, tiers
        stem_all = name[:-3]
        if stem_all.endswith("_asset"):
            q = stem_all[:-len("_asset")]
            if q in MEDIA_PREFIXES and "assets.media_asset" in tables:
                tiers.append(("media", ["assets.media_asset"]))
                return "assets.media_asset", tiers
            if q.split("_")[-1] not in EQUIPMENT_PREFIXES and schema not in ("maintenance", "rental"):
                return None, tiers
        parts = stem_all.split("_")
        # **A column that names a schema has said where to look.** `inventory_item_id` is an
        # `item` in `inventory` — not `fnb.sold_out_item` because the referring table is in
        # `fnb` — and `orders.refund.ledger_entry_id` is an `entry` in `ledger`, not
        # `queue.entry` because `entry` is only an exact name there.
        for k in range(1, len(parts)):
            # At any position (`from_inventory_item_id`), and singular (`approval_request_id`
            # names `approvals`).
            qs = parts[k - 1]
            qs = qs if qs in schemas else (qs + "s" if qs + "s" in schemas else "")
            if not qs:
                continue
            rest = "_".join(parts[k:])
            inq = lambda xs: [t for t in xs if t.split(".", 1)[0] == qs and t != table]
            for pick in (inq(exact.get(rest) or []), inq(suffixes.get(rest) or []),
                         inq([t for t in (prefixes.get(rest) or []) if prefix_ok(rest, t)])):
                if pick:
                    tiers.append(("q", pick))
                    if len(pick) == 1:
                        return pick[0], tiers
                    break
        for i in range(len(parts)):
            stem = "_".join(parts[i:])
            n_before = len(tiers)
            # **A self-reference needs a qualifier.** `parent_category_id` and
            # `replaced_by_token_id` point at their own table; a bare `request_id` on
            # `platform.dsar_request` does not — it is how a row became its own parent.
            me = (lambda xs: [t for t in xs if t != table]) if i == 0 else (lambda xs: list(xs))
            ex = me(exact.get(stem) or [])
            # Children of the referring table (`control.tenant_migration_plan` for
            # `control.tenant.plan_id`) are the table's own detail, not what its key names.
            sx = me(t for t in (suffixes.get(stem) or [])
                    if not t.split(".", 1)[1].startswith(own + "_"))
            px = me(t for t in (prefixes.get(stem) or []) if prefix_ok(stem, t))
            same = lambda xs: [t for t in xs if t.split(".", 1)[0] == schema]
            t0 = [t for t in (exact.get(own + "_" + stem) or [])
                  if t.split(".", 1)[0] == schema and t not in links]
            sx_same = same(sx)
            fam = [t for t in sx_same if t == table or head(t) == head(table)]
            rest = [t for t in sx_same if t not in fam]
            ex_other = [t for t in ex if t != table]
            if len(ex_other) > 1:
                ex_other = same_db(table, ex_other)
            if not t0 and not same(ex) and not fam and rest and len(ex_other) == 1:
                # **Two readings and nothing to choose by.** `maintenance.work_order.
                # source_plan_id` could be `subscription.plan` (the exact name) or
                # `maintenance.preventive_plan` (a plan, in its own schema); `marketing.lost_item.
                # last_seen_point_id` could be `venuemap.point` or `marketing.touch_point`. Each
                # rule is right somewhere and wrong somewhere else, so neither is taken: the
                # column stays unlinked until its contract says, which is the answer this
                # deriver already gives `template_id`.
                tiers.append(("contest", sorted(set(rest) | set(ex))))
                return None, tiers
            order = [("0", t0), ("1", same(ex)), ("1b", fam), ("2", ex), ("1c", rest),
                     ("3", same(px)), ("4", sorted(set(px) | set(sx)))]
            for tier, pick in order:
                if tier == "4" and len(ex_other) > 1:
                    # **An exact name held by two tables is a known name, not a hint.** Once
                    # `deposit` is both `ledger.deposit` and `orders.deposit`, a third table that
                    # merely starts with it (`orders.deposit_box`) is not a better answer.
                    break
                if not pick:
                    continue
                tiers.append((tier, pick))
                ns = [t for t in pick if t != table]
                if tier == "2" and len(ns) > 1 and len(same_db(table, ns)) == 1:
                    ns = same_db(table, ns)
                if len(ns) == 1:
                    return ns[0], tiers
                if not ns and len(pick) == 1:
                    return pick[0], tiers
            if len(tiers) > n_before:
                # **A longer stem that matched and could not choose ends the search.** Falling
                # through to a shorter one answered `import_job_id` with `ai.index_job` after
                # `import_job` tied — the next run, once the old pick was gone, would have
                # produced exactly the guess the tie refused.
                return None, tiers
        return None, tiers

    def _refuted(table: str, name: str, target: str) -> str:
        """Why a legacy `declared` target cannot stand, or '' if it may.

        **A legacy declaration survives only where the naming evidence does not contradict it.**
        `venue_id -> platform.scope` and `ticket_id -> access.entitlement` in `access` are domain
        aliases no stem can see, and stand. What falls:

          * the row's own key pointing at itself;
          * a polymorphic column (`source_id` beside `source_type`);
          * a target the evidence resolves elsewhere — `inventory.location` over
            `fnb.delivery_location`, `pii.subject` over `wallet.wallet`.

        A pick between equals in *another* schema returns "tie" and is judged by `_tie_holds`.
        """
        if target == table and own_key(table, name):
            return "own key"
        if name.endswith("_id") and polymorphic(table, name):
            return "polymorphic"
        got, tiers = resolve(table, name) if name.endswith("_id") else (None, [])
        if got == target:
            return ""
        schema = table.split(".", 1)[0]
        for _tier, pick in tiers:
            if _tier == "contest" and target in pick:
                # The old pick is one of the two readings. Its own schema's reading stands
                # (`orders.sales_order.shift_id -> orders.pos_shift` against `workforce.shift`);
                # the other schema's does not (`subscription.plan` for a work order).
                return "" if target.split(".", 1)[0] == schema else "contested"
            if target in pick and got and got != target and pick is tiers[-1][1]:
                return "resolves to " + got          # e.g. a tie the database boundary settled
            if target in pick:
                # First tier holding the target. A tie among the referring schema's own tables
                # is one the legacy author could settle; a tie across schemas is not.
                if len([t for t in pick if t != table]) > 1 and target.split(".", 1)[0] != schema:
                    return "tie"
                return ""
        if not got:
            return ""
        # **How strong the contrary evidence is decides whether it overrides the old pick.**
        stems = ["_".join(name[:-3].split("_")[i:]) for i in range(len(name[:-3].split("_")))]
        tshort = target.split(".", 1)[1]
        named = any(tshort == st or tshort.startswith(st + "_") or tshort.endswith("_" + st)
                    for st in stems)      # the old pick matches the column's name at all
        gtier = tiers[-1][0] if tiers else ""
        if gtier in ("0", "1", "q", "media"):
            # The referring schema has a table of exactly that name, or the column named the
            # schema: `inventory.location`, `reporting.alert_rule`, `payments.provider`.
            return "resolves to " + got
        if gtier == "1b":
            # Same schema, same family, or the table itself: `fnb.kitchen_ticket` over
            # `access.entitlement`, `journal_entry.reversal_of_entry_id` over `ledger.posting`.
            return "resolves to " + got
        if gtier == "1c":
            # A same-schema table of another family beats a same-named table elsewhere
            # (`workforce.integration_source` over `ai.index_source`), but not a domain alias:
            # `admission_profile_id -> access.admission_rules` is not overturned by some
            # `*_profile` in `catalogue`.
            if named and target.split(".", 1)[0] != schema:
                return "resolves to " + got
            return ""
        if (gtier == "2" and not named and tshort != name[:-3]
                and got.split(".", 1)[1] == name[:-3]):
            # An exact, unique name for the *whole* column beats an alias: `subject_id` is
            # `pii.subject`, not `wallet.wallet`. `venue_id -> platform.scope` has no exact name
            # to lose to, and `collection_point_id` is not overturned by a bare `point`.
            return "resolves to " + got
        # A prefix or suffix somewhere else is weaker than any recorded pick.
        return ""

    # **A tie is settled by how the rest of the package uses the name, never by the column
    # itself.** `orders.chargeback.provider_id` chose `ai.provider` over `payments.provider` with
    # nothing to choose by, and `ledger.journal_entry.source_id` chose `ai.index_source` out of
    # every `*_source` table — while `product_id -> catalogue.product` and
    # `order_id -> orders.sales_order` are the same shape of pick and are right.
    #
    # The difference is corroboration. A tied pick stands only when legacy declarations of
    # columns ending in the same word, **in schemas other than the referring one and the
    # target's own**, name the same target at least twice and make up two thirds of those votes. `product_id` and
    # `order_id` are corroborated across a dozen schemas; `provider_id` into `ai.provider` from
    # outside `ai` and `payments` has one vote, and `source_id` into `ai.index_source` from
    # outside `ai` and `ledger` has none left once the polymorphic columns are refuted.
    verdicts = {k: _refuted(k[0], k[1], t) for k, t in legacy.items()}
    tie_votes: dict = {}
    for (table, name), target in legacy.items():
        if verdicts[(table, name)] in ("", "tie"):
            tie_votes.setdefault(name[:-3].split("_")[-1], []).append(
                (table.split(".", 1)[0], target))

    def _tie_holds(table: str, name: str, target: str) -> bool:
        # Keyed by the column's last word, so `related_order_id` is corroborated by `order_id`.
        schema, tschema = table.split(".", 1)[0], target.split(".", 1)[0]
        votes_ = [t for s_, t in tie_votes.get(name[:-3].split("_")[-1], [])
                  if s_ not in (schema, tschema)]
        agree = sum(1 for t in votes_ if t == target)
        return agree >= 2 and agree * 3 >= len(votes_) * 2

    for (table, name), target in legacy.items():
        why = verdicts[(table, name)]
        if why == "tie":
            why = "" if _tie_holds(table, name, target) else "uncorroborated tie"
            if why:
                # **And nothing weaker takes its place.** Once `ai.layout_draft.import_job_id`
                # loses `venuemap.import_job` to a tie, the next stem down (`job`) would offer
                # `ai.index_job` — a guess worse than the pick it replaced. Left unlinked.
                decided[(table, name)] = "unlinked"
        if why:
            stats["legacy_dropped"] += 1
            if len(dropped_examples) < 80:
                dropped_examples.append(f"{table}.{name} -> {target} ({why})")
            continue
        add_fk(table, name, target, "declared", legacy_req.get((table, name), ""))
        declared_edges.append((table, name, target))
        stats["legacy_kept"] += 1

    # 2b. Precedent. A column name the contracts declare a target for everywhere they
    #     mention it, applied to the columns that name it and declare nothing.
    #
    # **The stem rules cannot see a domain alias and should not guess one.** A venue is
    # `platform.scope`, so `venue_id` matches no stem. `order_id` is the opposite problem:
    # `order` is a suffix of `sales_order`, `work_order` and `purchase_order`, so the ambiguity
    # rule correctly refuses it, and the declared columns say which one is meant.
    #
    # **Votes come from declarations only** (R082). Counting every stored `references` let a
    # convention guess vote for itself on the next run. A name is carried over when every
    # declaration of it agrees and at least two exist — one author's choice is not yet a
    # convention — and **only after the naming rules found nothing**: a same-schema table named
    # for the thing (`fnb.kitchen_ticket`) is better evidence than what `ticket_id` means in
    # `access`.
    #
    # **And only from other schemas.** `ai.index_job.source_id -> ai.index_source` is right
    # inside `ai` and says nothing about `ledger.posting.source_id`; counting it carried the
    # language-model index back onto the ledger one run after it had been refuted. A vote from
    # the referring schema or the target's own schema is not counted.
    pvotes: dict[str, list] = {}
    for _t, name, tgt in declared_edges:
        pvotes.setdefault(name, []).append((_t.split(".", 1)[0], tgt))

    def precedent_for(table: str, name: str) -> str | None:
        schema = table.split(".", 1)[0]
        tgts = {t for _s, t in pvotes.get(name, [])}
        if len(tgts) != 1:
            return None                       # the declarations disagree
        tgt = next(iter(tgts))
        n = sum(1 for s_, _t2 in pvotes[name] if s_ not in (schema, tgt.split(".", 1)[0]))
        return tgt if n >= 2 else None

    carried = 0
    for table, columns in cols.items():
        for c in columns:
            name = c["column"]
            if (table, name) in decided or not name.endswith("_id"):
                continue
            got, _tiers = resolve(table, name)
            if got:
                add_fk(table, name, got, "convention")
                if got == "assets.media_asset":
                    _media += 1
                continue
            p = precedent_for(table, name)
            if p and p != table and not own_key(table, name) and not polymorphic(table, name):
                add_fk(table, name, p, "precedent")
                carried += 1 if decided.get((table, name)) == "precedent" else 0

    print(f"  declared: {stats['contract']} by contract, {stats['hand']} hand-written, "
          f"{stats['legacy_kept']} legacy kept, {stats['legacy_dropped']} legacy refuted")
    for line in dropped_examples:
        print(f"     refuted: {line}")
    if _media:
        print("  %d media asset edge(s) sent to assets.media_asset, not maintenance.asset" % _media)
    if carried:
        print("  %d edge(s) from declared precedent" % carried)

    # 3. Ambient coupling from the lineage. Two tables written by one operation are related in
    #    fact — an order and its lines, a shift and its deposit box — even where the column-level
    #    reference is absent because one side holds no id.
    #
    #    **Capped per operation.** An operation writing eight tables would otherwise produce
    #    twenty-eight edges and drown the declared ones.
    for oid, v in lineage.items():
        writes = [t for t in v.get("writes", []) if t in tables]
        if len(writes) < 2 or len(writes) > 4:
            continue
        anchor = writes[0]
        for other in writes[1:]:
            add(anchor, f"via {oid}", other, "lineage", "ambient")

    tab_ops: dict[str, list[str]] = {}
    for oid, v in lineage.items():
        for t in set(v.get("reads", [])) | set(v.get("writes", [])):
            if t in tables:
                tab_ops.setdefault(t, []).append(oid)

    tab_screens: dict[str, list[str]] = {}
    idx_path = HANDOFF / "screen-index.json"
    if idx_path.exists():
        idx = json.loads(idx_path.read_text(encoding="utf-8"))
        for sid, s in idx.items():
            for t in set(s.get("reads", [])) | set(s.get("writes", [])):
                if t in tables:
                    tab_screens.setdefault(t, []).append(sid)

    linked = {r["frm"] for r in rels} | {r["to"] for r in rels}
    out = {
        "generated": "2026-08-18",
        "note": ("Derived by tools/derive-relationships.py from schema-reference.json and "
                 "api-data-lineage.json. **Not hand-maintained** — the previous graph described "
                 "540 relationships across 192 tables while the package held 352, because it had "
                 "not been touched since the schema grew past it."),
        # Read by tools/fix-audit-stale-graph-refs.py to know the graph was derived with
        # declarations read off the contracts (audit root R082), not off stored labels.
        "declarations": "contract",
        "rels": rels,
        "tab_ops": tab_ops,
        "tab_screens": tab_screens,
    }
    (HANDOFF / "relationship-graph.json").write_text(json.dumps(out, indent=1), encoding="utf-8")

    # `handoff/relationships.csv` is what the viewer's ER diagram draws from, and it was
    # hand-maintained: **515 rows against this graph's 846**, and it marked
    # `identity.delegated_access.principal_id` as `ambient` where the graph has it declared.
    #
    # The viewer hides ambient edges by default — `principal_id` is a real foreign key and it was
    # **drawn as nothing**, which is what a reviewer saw. **A stale copy that downgrades an edge is
    # worse than a missing one**: the diagram looks complete and the line is absent.
    #
    # The two vocabularies differ, so the mapping is explicit rather than a pass-through:
    #   declared / convention foreign key -> `reference`, drawn as the ordinary case
    #   an edge into the row's own parent -> `child`, drawn strongly
    #   lineage coupling                  -> `ambient`, hidden unless asked for
    # **A child is a row that cannot exist without its parent, not merely one with a required
    # foreign key.** A first pass marked every required FK as parentage and produced 335 child
    # edges out of 848 — including `access.entitlement.product_id`, which is a reference: a product
    # does not own the entitlements issued against it, and deleting one must not take them.
    #
    # The reliable signal is the name. `orders.order_line` names `orders.sales_order` in its own
    # table name; `access.entitlement` does not name `catalogue.product`. That is exactly the
    # `<parent>_<thing>` relationship the schema deriver already uses to fill child tables.
    child_edges = set()
    for r in rels:
        if r["how"] == "lineage":
            continue
        parent_short = r["to"].split(".")[-1]
        own_short = r["frm"].split(".")[-1]
        same_schema = r["frm"].split(".")[0] == r["to"].split(".")[0]
        if same_schema and own_short.startswith(parent_short + "_"):
            child_edges.add((r["frm"], r["col"], r["to"]))
    lines = ["from_table,from_column,to_table,edge_kind,how,cross_schema,required"]
    for r in sorted(rels, key=lambda x: (x["frm"], x["col"])):
        if r["how"] == "lineage":
            kind = "ambient"
        elif (r["frm"], r["col"], r["to"]) in child_edges:
            kind = "child"
        else:
            kind = "reference"
        lines.append(",".join([r["frm"], r["col"], r["to"], kind, r["how"],
                               r["cross"], r["required"]]))
    (HANDOFF / "relationships.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  {len(rels)} rows → handoff/relationships.csv")

    by_kind: dict[str, int] = {}
    for r in rels:
        by_kind[r["how"]] = by_kind.get(r["how"], 0) + 1
    print(f"  {len(rels)} relationships · {', '.join(f'{v} {k}' for k, v in sorted(by_kind.items()))}")
    print(f"  {len(linked & tables)} of {len(tables)} tables linked")
    orphans = sorted(tables - linked)
    if orphans:
        print(f"  {len(orphans)} with no relationship: {', '.join(orphans[:6])}"
              + (" …" if len(orphans) > 6 else ""))
    print("  → handoff/relationship-graph.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
