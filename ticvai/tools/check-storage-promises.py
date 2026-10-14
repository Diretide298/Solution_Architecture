#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""What an operation promises about storage, the derived DDL keeps (ADAM CR-065, CR-068, CR-069, CR-070, CR-073, CR-074).

The backend developer found, building Block A's first modules, five ways the contract promised something
the derived database could not keep. Each is a rule here, read against `handoff/schema-reference.json`
(what `derive-ddl.py` writes the DDL from) and the contracts, never against the frozen r1 SQL:

  SP-ARRAY-NOWHERE     (CR-073) a persisted schema carries an array of objects that no column and no child
                       table holds, so the values an operation accepts are dropped (`Outlet.openingHours`;
                       derive-schema prints these as "arrays stored nowhere"). **Not baselinable for a schema an
                       operation in handoff/delivery-slice.json takes or returns**: that operation is being
                       built now. Outside the slice the known ones are baselined and only shrink.
  SP-DUPLICATE-409     (CR-068, CR-074) a create or update answers 409 because a code, SKU, number or name is
                       "already in use" and the request field carries no `x-ticvai-unique`, or carries one at a
                       level other than the one the 409 names ("in this venue" is `venue`); without the unique
                       index two concurrent requests both pass the handler's look-up.
  SP-REQUEST-NOT-NULL  (CR-065) a NOT NULL column whose only source is a `*Request` schema persisted beside the
                       table's own schema: the row exists before that request is made, so the column cannot be
                       required (`orders.pos_shift.cashier_reason` from `ShiftVarianceReasonRequest.reason`).
                       derive-schema.py now derives such a column nullable; this keeps it so.
  SP-KEY-UNDECLARED    (CR-069) a NOT NULL `*_id` column that points at a table in its own database by naming
                       convention only (an index, no foreign key), so 900 has no key and 920 cannot scope the
                       row through its owner. Declare it (`x-ticvai-references: <table>`) or say it is not a key
                       (`x-ticvai-references: none`). Known ones baselined.
  SP-KEY-GUESSED       (CR-070) a convention reference whose target the name rule picked from another module
                       than the column's own and its own module has no such table: `refund.tax_reversal_entry_id`
                       -> `queue.entry`. Known ones baselined; a new guess fails until it is declared or refused.
  SP-KEY-TENANT-FALLBACK (CR-090) SP-KEY-UNDECLARED's consequence: a NOT NULL convention key whose table fell back to
                       the tenant-root policy (no scope column, no declared owner) while the table it points at is
                       scoped, and an operation below tenant that a staff or partner principal calls writes the
                       table. A venue's write fails with 42501 (`consent_question_version`, #27922). Declaring the
                       key gives the row its parent's policy. **Not baselinable for a table a delivery-slice
                       operation writes**: the 14 October members are held in code (FALLBACK_DEBT) and only shrink.
                       SP-KEY-UNDECLARED saw `consent_question_version.question_id` and it was baselined with 391
                       others at CHG-DDL-004, because that rule does not know which undeclared keys cost a policy.

Read-only. Exit 1 on a finding not in handoff/audit-baseline.json (tools/audit_guard.py).

    python3 tools/check-storage-promises.py [--all] [--update-baseline]
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {
    "SP-ARRAY-NOWHERE": "a persisted schema's array of objects has no column and no child table (CR-073, R179)",
    "SP-DUPLICATE-409": "a 409 for a code already in use has no x-ticvai-unique at the level it names (CR-068, CR-074)",
    "SP-REQUEST-NOT-NULL": "a NOT NULL column sourced only from a request schema beside the row's own (CR-065)",
    "SP-KEY-UNDECLARED": "a NOT NULL key into its own database is a naming convention, not declared (CR-069, CR-013)",
    "SP-KEY-GUESSED": "a convention key the name rule pointed into another module's table (CR-070, CR-013)",
    "SP-KEY-TENANT-FALLBACK": "an undeclared key left a table written below tenant at the tenant-root policy while "
                              "its parent is scoped (CR-090)",
}
BELOW_TENANT = {"region", "brand", "venue", "workstation"}
JUDGED_AUDIENCE = {"staff", "partner"}
# The policies derive-ddl's parent rule passes on to a child. A split parent (read-beneath, grant-holder-read)
# passes none (SPLIT_CHILDREN), so a key to it (`identity.principal`) names who, not an owner.
PARENT_POLICIES = {"apply_scope_rls", "apply_venue_rls", "apply_parent_rls", "apply_subject_rls"}
# A rule whose findings may not be baselined for an operation the first release builds.
SLICE_RULES = {"SP-ARRAY-NOWHERE"}
DUPLICATE = re.compile(r"\b(already (?:in use|exists?|taken|used)|duplicate|not unique|is taken)\b", re.I)
SCOPE_WORDS = [("venue", re.compile(r"\b(this|the same|that) venue\b|\bper venue\b|\b(?:in|at|within) (?:the|its|this) venue\b",
                                    re.I)),
               ("tenant", re.compile(r"\b(this|the|that) tenant\b|\bper tenant\b|\bacross (?:the )?tenant\b", re.I))]
GENERIC = {"entry", "item", "line", "record", "event", "request", "node", "type", "document", "authorisation",
           "session", "message", "version", "task", "job", "run", "zone", "point", "rule", "policy"}
CODEISH = re.compile(r"(code|sku|number|name|slug|label|key|reference|handle|email)$", re.I)


# **The arrays stored nowhere that a delivery-slice operation already takes or returns, on 14 October 2026.**
# Kept here, in code, and never in handoff/audit-baseline.json: `--update-baseline` cannot add a slice
# member, so a new one fails until its storage is decided (a child table with `A + B`, a column with
# `x-ticvai-persistence-column`, or `x-ticvai-persisted: false`). Each of these is a storage decision for its
# module's owner, listed for the lead with CHG-DDL-007; remove a line when it is decided. Only shrinks.
SLICE_DEBT = frozenset(k + "@slice" for k in """
ai.AiForecastScenario.changes ai.AiGuidedChoiceSuggestion.questions ai.AiHistoryImport.findings
ai.AiIncident.containment ai.AiModel.taskFitness ai.AiProvider.fitnessWarnings ai.AiVenueSettings.openingHours
approvals.ApprovalRequest.escalations approvals.ApprovalRequest.pendingApprovers assets.MediaAssetDetail.collections
assets.MediaAssetDetail.derivatives assets.MediaAssetDetail.previousVersions catalogue.CatalogueImportJob.findings
catalogue.EntitlementTemplate.validTimeWindows catalogue.Product.displayTags identity.Principal.roles
marketing-crm.CookieBannerPreferenceCenterDesignerView.buttons
marketing-crm.CookieBannerPreferenceCenterDesignerView.categories
marketing-crm.CookieBannerPreferenceCenterDesignerView.links orders.Cart.conflicts orders.Cart.consentQuestions
public-api.ApiVersion.changes reporting.SemanticModel.domains reporting.SemanticModel.relationships
resources.ResourceSchedule.exceptions resources.ResourceSchedule.windows seating.AccessibleSeating.spaces
seating.SeatRecommendationRules.profiles transport.TransportNetworkImport.findings venue-map.PlacedResource.boundary
venue-map.VenueMapImportJob.findings venue-map.VenuePoint.media venue-map.VisitPlan.days venue-map.VisitPlan.excluded
wallet.WalletConfigurationVersion.findings wallet.WalletFundingRules.bonusRules wallet.WalletFundingRules.presetAmounts
white-label.ConfigVersion.pendingBuildTimeChanges
""".split())


# **The tables a delivery-slice operation writes below tenant that an undeclared key left at the tenant root, on
# 14 October 2026** (SP-KEY-TENANT-FALLBACK, CHG-CNS-002). Same rule as SLICE_DEBT: held here, never in the
# baseline file, and a new member fails. Each is a venue write that answers 42501 today: declare the key
# (`x-ticvai-references`, as CR-090 did for `marketing.consent_question_version`) or decide the owner in
# derive-ddl.py ROW_OWNER, then remove its line. Only shrinks.
FALLBACK_DEBT = frozenset(k + "@slice" for k in """
""".split())   # emptied by CHG-STO-001: every member's key is declared
DEBT = {"SP-ARRAY-NOWHERE": SLICE_DEBT, "SP-KEY-TENANT-FALLBACK": FALLBACK_DEBT}


class SliceGuard(g.Guard):
    """A Guard whose slice members (SP-ARRAY-NOWHERE, SP-KEY-TENANT-FALLBACK) are never read from or written to
    the baseline file: the code holds them."""

    def _baseline(self) -> dict:
        base = dict(super()._baseline())
        for r, debt in DEBT.items():
            rule = [k for k in (base.get(r) or []) if not k.endswith("@slice")]
            base[r] = rule + sorted(debt)
        return base

    def _write_baseline(self):
        kept = {r: self.found.get(r) or {} for r in DEBT}
        for r in DEBT:
            self.found[r] = {k: v for k, v in kept[r].items() if not k.endswith("@slice")}
        try:
            super()._write_baseline()
        finally:
            self.found.update(kept)


def rls_policies() -> dict:
    """table -> the apply_*_rls helper the databases get (the baseline, then every forward migration), read the
    way check-rls-scope-fit reads it. Derive before check: derive-ddl writes a policy change into the next V-file."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "rls_scope_fit", str(Path(__file__).resolve().parent / "check-rls-scope-fit.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return {t: helper for t, (helper, _) in mod.policies(g.ROOT / "backend").items()}


def deref(node, stem, by, depth=0):
    while isinstance(node, dict) and "$ref" in node and depth < 10:
        ref = str(node["$ref"])
        if not ref.startswith("#/components/schemas/"):
            m = re.match(r"^(?:\.\./)?(?:[\w-]+/)?([\w-]+)\.yaml#/components/schemas/(\w+)$", ref)
            if not m:
                return node, stem
            stem = m.group(1)
            node = by.get((stem, m.group(2))) or {}
        else:
            node = by.get((stem, g.ref_name(ref))) or {}
        depth += 1
    return node, stem


def props_of(schema, stem, by, depth=0) -> dict:
    out = {}
    schema, stem = deref(schema, stem, by)
    if not isinstance(schema, dict) or depth > 5:
        return out
    for sub in schema.get("allOf") or []:
        out.update(props_of(sub, stem, by, depth + 1))
    for k, v in (schema.get("properties") or {}).items():
        out[k] = v if isinstance(v, dict) else {}
    return out


def reachable(roots, by) -> set:
    """Every (stem, schema name) reachable from the given (stem, node) roots through $ref, properties,
    items and the combinators."""
    seen, out = set(), set()
    todo = list(roots)
    while todo:
        stem, node = todo.pop()
        if not isinstance(node, dict):
            continue
        if "$ref" in node:
            ref = str(node["$ref"])
            m = re.match(r"^(?:(?:\.\./)?(?:[\w-]+/)?([\w-]+)\.yaml)?#/components/schemas/(\w+)$", ref)
            if not m:
                continue
            key = (m.group(1) or stem, m.group(2))
            if key in seen:
                continue
            seen.add(key)
            out.add(key)
            todo.append((key[0], by.get(key) or {}))
            continue
        for k in ("allOf", "oneOf", "anyOf"):
            for sub in node.get(k) or []:
                todo.append((stem, sub))
        if isinstance(node.get("items"), dict):
            todo.append((stem, node["items"]))
        for v in (node.get("properties") or {}).values():
            todo.append((stem, v))
    return out


def body_schemas(op) -> list:
    out = []
    for media in ((op.get("requestBody") or {}).get("content") or {}).values():
        if isinstance(media, dict) and media.get("schema") is not None:
            out.append(("req", media["schema"]))
    for code, r in (op.get("responses") or {}).items():
        if not str(code).startswith("2") or not isinstance(r, dict):
            continue
        for media in (r.get("content") or {}).values():
            if isinstance(media, dict) and media.get("schema") is not None:
                out.append(("res", media["schema"]))
    return out


def main() -> int:
    g.force_utf8()
    guard = SliceGuard("check-storage-promises", RULES)
    ref = g.load_json(g.ROOT / "handoff" / "schema-reference.json", {}) or {}
    cols = ref.get("cols") or {}
    origin = ref.get("origin") or {}
    store = ref.get("store") or {}
    embedded = {n for _, n, why in (ref.get("nomap") or []) if re.search(r"jsonb|embedded", str(why))}
    slice_ops = set(((g.load_json(g.ROOT / "handoff" / "delivery-slice.json", {}) or {}).get("operations") or {}))
    by, _ = g.schemas()
    ops = g.operations()

    in_slice: dict = {}
    for oid in sorted(slice_ops):
        f = ops.get(oid)
        if not f:
            continue
        for _, node in body_schemas(f["op"]):
            for key in reachable([(f["contract"], node)], by):
                in_slice.setdefault(key, oid)

    sources: dict = {}
    for t, cs in cols.items():
        for c in cs:
            sources.setdefault(str(c.get("source") or ""), []).append((t, c))

    # ---- SP-ARRAY-NOWHERE (CR-073) ---------------------------------------------------------------
    # The same question derive-schema.py asks when it prints "arrays stored nowhere": an array whose items
    # are objects, that the schema does not mark as not stored or as a declared column
    # (`x-ticvai-persistence-column`), whose items are not rows of a table of their own (a persisted
    # schema), and that no child table holds (a column sourced from `<Schema>.<prop>[]`, or the implied
    # child `<table>_<prop>`).
    def persisted_table(node, st):
        tgt, _ = deref(node, st, by)
        tag = str((tgt or {}).get("x-ticvai-persistence") or "").strip() if isinstance(tgt, dict) else ""
        return bool(tag) and not tag.lower().startswith("none") and "—" not in tag and "." in tag

    def singular(w):
        return w[:-3] + "y" if w.endswith("ies") else (w[:-1] if w.endswith("s") and not w.endswith("ss") else w)

    for (stem, name), s in sorted(by.items()):
        persist = str(s.get("x-ticvai-persistence") or "").strip()
        if not persist or persist.lower().startswith("none") or "—" in persist:
            continue
        tables = [t.strip() for t in persist.split("+") if t.strip() in cols]
        if not tables:
            continue
        have = set().union(*({c.get("column") for c in cols[t]} for t in tables))
        for p, ps in sorted(props_of(s, stem, by).items()):
            if ps.get("type") != "array" or ps.get("x-ticvai-persisted") is False or ps.get("x-ticvai-derived") \
                    or str(ps.get("x-ticvai-persistence-column") or "").strip():
                continue
            raw_items = ps.get("items") or {}
            items, _ = deref(raw_items, stem, by)
            if not isinstance(items, dict) or "enum" in items \
                    or not (items.get("properties") or items.get("allOf") or items.get("type") == "object"):
                continue                                 # an array of scalars or enums is a column
            if g.ref_name(str(raw_items.get("$ref") or "")) in embedded or persisted_table(raw_items, stem):
                continue
            col = ps.get("x-ticvai-column") or g.snake(p)
            if col in have:
                continue
            tail = "." + name + "." + p
            if any((tail + "[]") in src for src in sources):
                continue
            sn = singular(g.snake(p))
            if any(f"{t}_{sn}" in cols or f"{t}_{g.snake(p)}" in cols for t in tables) \
                    or any(sn in t.split(".")[1] for t in tables[1:]):
                continue
            key = f"{stem}.{name}.{p}"
            op = in_slice.get((stem, name))
            msg = (f"{key} persists to {', '.join(tables)} and no column or child table holds it"
                   + (f"; {op} (delivery slice) takes or returns it" if op else ""))
            guard.add("SP-ARRAY-NOWHERE", key + ("@slice" if op else ""), msg)

    # ---- SP-DUPLICATE-409 (CR-068, CR-074) ---------------------------------------------------------
    for oid, f in sorted(ops.items()):
        op = f["op"]
        if f["method"] not in ("post", "put", "patch"):
            continue
        r409 = (op.get("responses") or {}).get("409") or (op.get("responses") or {}).get(409)
        if not isinstance(r409, dict):
            continue
        req = next((n for k, n in body_schemas(op) if k == "req"), None)
        if req is None:
            continue
        props = props_of(req, f["contract"], by)
        # the persisted schema may carry the marker where the request does not (derive-ddl reads both)
        resource = re.sub(r"^(Create|Update)(\w+)Request$", r"\2", g.ref_name(str(req.get("$ref") or "")))
        rprops = props_of({"$ref": f"#/components/schemas/{resource}"}, f["contract"], by) if resource else {}
        for k, n in body_schemas(op):                    # an inline request: the resource it answers with
            if k == "res" and isinstance(n, dict) and n.get("$ref"):
                rprops = {**props_of(n, f["contract"], by), **rprops}
                break
        if "$ref" in r409:
            # the shared `DuplicateCode` 409 is a uniqueness promise too: some field must carry the marker
            if g.ref_name(str(r409["$ref"])) == "DuplicateCode" \
                    and not any(isinstance(v, dict) and v.get("x-ticvai-unique")
                                for v in list(props.values()) + list(rprops.values())):
                guard.add("SP-DUPLICATE-409", f"{oid}.duplicate-code",
                          f"{oid}: answers 409 DuplicateCode and no request field carries x-ticvai-unique")
            continue
        desc = " ".join(str(r409.get("description") or "").split())
        if not DUPLICATE.search(desc):
            continue
        named = [p for p in props if CODEISH.search(p) and re.search(r"\b" + re.escape(p) + r"\b|"
                 + re.escape(" ".join(g.snake(p).split("_"))), desc, re.I)]
        if not named:
            named = [p for p in props if re.fullmatch(r"(code|sku|\w+Code|\w+Number)", p)
                     and re.search(g.snake(p).split("_")[-1], desc, re.I)]
        if not named:
            continue
        level = next((lvl for lvl, rx in SCOPE_WORDS if rx.search(desc)), "tenant")
        for p in named:
            mark = props[p].get("x-ticvai-unique")
            if mark is None:
                mark = (rprops.get(p) or {}).get("x-ticvai-unique")
            if mark != level:
                guard.add("SP-DUPLICATE-409", f"{oid}.{p}",
                          f"{oid}: 409 '{desc[:70]}' promises {p} unique per {level}; the field has "
                          + (f"x-ticvai-unique: {mark}" if mark else "no x-ticvai-unique"))

    # ---- SP-REQUEST-NOT-NULL (CR-065) ---------------------------------------------------------------
    # The generator rule is derive-schema.py `_later_writer`: a `*Request` persisted beside the row's own schema
    # that does not create the row (not `Create*`, no `id` of its own) writes nullable columns.
    by_name = {}
    for (stem, name), s in by.items():
        by_name.setdefault(name, (stem, s))
    for t, cs in sorted(cols.items()):
        own = str(origin.get(t) or "")
        for c in cs:
            src = str(c.get("source") or "")
            bits = src.split(".")
            if c.get("required") != "yes" or len(bits) != 3 or not bits[1].endswith("Request") \
                    or bits[1].startswith("Create"):
                continue
            rstem, rbody = by_name.get(bits[1], (None, {}))
            if "id" in props_of(rbody, rstem, by):
                continue                                  # it creates the row (SubmitInspectionRequest)
            if own and own.split(".")[-1] != bits[1]:
                guard.add("SP-REQUEST-NOT-NULL", f"{t}.{c['column']}",
                          f"{t}.{c['column']} is NOT NULL from {src}; the row is {own}'s and exists before that request")

    # ---- SP-KEY-UNDECLARED and SP-KEY-GUESSED (CR-069, CR-070) -------------------------------------
    def area(t):
        return "control" if t.split(".")[0] == "control" else "tenant"
    for t, cs in sorted(cols.items()):
        if store.get(t, "postgres") not in ("postgres", "postgres-analytical"):
            continue
        for c in cs:
            to = c.get("references")
            if not to or c.get("enforced") == "yes" or to not in cols or area(to) != area(t):
                continue
            if c.get("required") == "yes" and c.get("column", "").endswith("_id"):
                guard.add("SP-KEY-UNDECLARED", f"{t}.{c['column']}",
                          f"{t}.{c['column']} NOT NULL -> {to} by {c.get('referenceHow') or 'convention'} only")
            # A guess: the name rule matched the column's last word to a table of another module, the column
            # does not name that module, and either does not carry the table's whole name or the name is one
            # generic word (`tax_reversal_entry_id` -> `queue.entry`, `deposit_authorisation_id` ->
            # `games.authorisation`). `approval_request_id` -> `approvals.request` names its module and passes.
            tschema, tshort = to.split(".")
            words = str(c["column"])[:-3].split("_") if str(c["column"]).endswith("_id") else []
            if c.get("referenceHow") == "convention" and tschema != t.split(".")[0] and words \
                    and tschema not in ("identity", "platform", "pii") \
                    and not any(w in (tschema, tschema.rstrip("s"), tschema.replace("_", "")) for w in words) \
                    and (tshort not in "_".join(words) or (tshort in GENERIC and len(words) > 1)):
                guard.add("SP-KEY-GUESSED", f"{t}.{c['column']}",
                          f"{t}.{c['column']} -> {to}: the name rule's pick from another module")

    # ---- SP-KEY-TENANT-FALLBACK (CR-090) ------------------------------------------------------------
    # A table at the tenant-root policy (apply_tenant_rls) with a NOT NULL convention key to a table that has any
    # other policy (scope, venue, parent, subject): had the key been declared, the parent rule would have scoped
    # it. Judged only where an operation below tenant that staff or partners call writes the table.
    pol = rls_policies()
    lin = g.load_json(g.ROOT / "handoff" / "api-data-lineage.json", {}) or {}
    writers: dict = {}
    for oid, e in lin.items():
        if not isinstance(e, dict) or e.get("scope") not in BELOW_TENANT \
                or not (set(e.get("audience") or []) & JUDGED_AUDIENCE):
            continue
        for t in e.get("writes") or []:
            writers.setdefault(t, []).append(oid)
    for t, cs in sorted(cols.items()):
        if pol.get(t) != "apply_tenant_rls" or t not in writers:
            continue
        for c in cs:
            to = c.get("references")
            if not to or c.get("enforced") == "yes" or c.get("required") != "yes" or to not in cols \
                    or area(to) != area(t) or pol.get(to) not in PARENT_POLICIES:
                continue
            ws = sorted(writers[t])
            sl = [o for o in ws if o in slice_ops]
            key = f"{t}.{c['column']}" + ("@slice" if sl else "")
            guard.add("SP-KEY-TENANT-FALLBACK", key,
                      f"{t} is tenant-root only; {c['column']} -> {to} ({pol.get(to)}) is a convention, not a "
                      f"declared key, and {', '.join((sl or ws)[:3])}" + (" (delivery slice)" if sl else "")
                      + " writes it below tenant",
                      strict=bool(sl) and key not in FALLBACK_DEBT)
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
