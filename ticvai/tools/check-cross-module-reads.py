#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every read of another module's data takes a route ADR-0055 allows (amended 14 October 2026, CHG-GEN-009).

**ADR-0055 rule 2** says a module reads another module's schemas only through views the owner publishes or the
owner's in-process query interface, and rule 4 says that across deployables modules talk by event or by the published
contract, never by shared SQL. Nothing checked either: on 14 October `handoff/api-data-lineage.json` held 941
cross-module table reads in 517 of 2,796 operations, and the refusals the developers raised that day (ADAM CR-081,
CR-083, CR-084) were rule questions answered by reading another module's tables raw, some across deployables, some
not in the lineage at all. The amendment of 14 October makes the pattern one: **a rule question is asked of the owner
by a declared query**.

  * The owner declares the question in a top-level `x-ticvai-queries:` map in its contract:
    `<queryName>: {module, inputs, returns, rule, served: [in-process, service, projection]}`.
  * The asking operation names it: `x-ticvai-read-via: [{query: <contract>#<queryName>, route, for}]`, copied into
    the lineage as `readVia` by `tools/derive-lineage.py`. `in-process` is the owner's C# query interface, called in
    the caller's transaction, within one deployable; `service` is the owner's serviceAuth operation, across
    deployables; `projection` is a local copy the asker keeps, fed by the owner's events.
  * A generated view `<table>_for_<reader>` (DB-READ-VIEWS) is for bulk data reads within one deployable only.

Rules:

    XR-UNCOVERED    a lineage read of a table another module owns that is not a view named for the reader and is
                    not covered by a readVia to a query of the owning module
    XR-VIEW-ACROSS  a `<table>_for_<reader>` view read from another deployable (across deployables: service or
                    projection, never a view)
    XR-QUERY        a readVia that names no declared query, a query declared without module, inputs, returns, rule
                    or served, or a query whose module does not own the contract that declares it
    XR-ROUTE        a route that is not in-process, service or projection, not one the query serves, or in-process
                    across deployables
    XR-FOUNDATION   Identity (the foundation module every request resolves through, ADR-0028 tiers) reads a module
                    above it other than through a projection
    XR-LINEAGE      the lineage's readVia differs from the contract's x-ticvai-read-via (derive-lineage --apply)
    XR-FACT         an operation's own text (description, parameters, request and response descriptions, the
                    fields of its contract's schemas it uses) names a table another module owns, a field of a
                    schema another module's contract persists, or a phrase of FACTS, and the operation asks no
                    query over that table (ADAM CR-096 and CR-135, 15-17 October 2026; CHG-RTE-001). The
                    lineage holds only the tables behind response schemas (derive-lineage.py), so a rule stated in
                    words read data no rule above could see.

A read counts as covered only by a query over that table (its `table`, its projection's `source`, its `reads`),
or by a rule query of the owner that names no table: until 18 October any query of the owner covered every one of
its tables, and allocateDepositBox's workstation query would have covered Tenancy's denominations (CR-135).
`--list-facts` prints the XR-FACT class query: operation, reader, table, owner, how, phrase.

Kernel tables every deployable reads directly (`platform.scope`, `platform.idempotency_record`; ADAM CR-002) are not
cross-module reads. The reads already in the lineage on 14 October are baselined in handoff/audit-baseline.json; a
read by an operation the r6 batches fix (MUST_FIX) can never be baselined.

    python tools/check-cross-module-reads.py [--all] [--update-baseline] [--list-facts]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {
    "XR-UNCOVERED": "a read of another module's table that is neither a view named for the reader nor covered by a "
                    "readVia to the owner's declared query (ADR-0055 rule 2, amended 14 Oct; CHG-GEN-009)",
    "XR-VIEW-ACROSS": "a view named for the reader read from another deployable (rule 4: service or projection)",
    "XR-QUERY": "a readVia naming no declared query, or a query declared incompletely or by a module that does not "
                "own its contract",
    "XR-ROUTE": "a route not in-process / service / projection, not served by the query, or in-process across "
                "deployables",
    "XR-FOUNDATION": "Identity reads a module above it other than through a projection (ADR-0028 tiers)",
    "XR-LINEAGE": "the lineage's readVia differs from the contract's x-ticvai-read-via",
    "XR-FACT": "an operation's text names another module's table, field or fact (FACTS) and asks no query over that "
               "table (ADAM CR-096, CR-135; CHG-RTE-001)",
}
ROUTES = ("in-process", "service", "projection")
QUERY_FIELDS = ("module", "inputs", "returns", "rule", "served")
# Kernel tables every deployable's role reads directly (ADAM CR-002, docs/active/cross-deployable-writes.yaml).
KERNEL_READ = {"platform.scope", "platform.idempotency_record"}
# The module that reads nothing above it but through a projection (ADR-0028 "Foundation ... reads nothing above").
# Tenancy shares the foundation tier but asks commerce modules in-process inside `commerce` (CR-083: configureWorkstation
# asks Orders whether a shift is open), as the amendment of 14 October records.
FOUNDATION_STRICT = {"IdentityService"}
# **Reads the r6 batches fix, which may never be baselined** (audit of 14 October): the operation and the owning
# modules whose data its refusal or step-up asks about.
MUST_FIX = {
    "createSaleBoard": {"CatalogueService"},          # CR-081, batch TEN
    "updateSaleBoard": {"CatalogueService"},          # CR-081, batch TEN
    "configureWorkstation": {"OrderService"},         # CR-083, batch TEN
    "deleteGuestAccount": {"AccessService", "OrderService"},   # CR-084, batch GDL
    "exportSubjectData": {"AccessService", "OrderService"},    # CR-084, batch GDL
    # CR-078: the PIN step-up operations verify a PIN through Identity's published query (batch CRD)
    "reopenShift": {"IdentityService"},
    "closeShift": {"IdentityService"},
    "acceptShiftVariance": {"IdentityService"},
    "rejectShiftVariance": {"IdentityService"},
    "withdrawFromDepositBox": {"IdentityService"},
    "cancelPerformance": {"IdentityService"},
    "recountStockCount": {"IdentityService"},
    "closeTransferShort": {"IdentityService"},
    "listActiveSessions": {"IdentityService"},
}


def slug(service: str) -> str:
    return re.sub(r"Service$", "", service).lower()


def contract_ops() -> dict:
    """operationId -> the operation, from every contract."""
    return {o: f["op"] for o, f in g.operations().items()}


def declared_queries() -> dict:
    """`<contract>#<queryName>` -> (contract stem, the declaration)."""
    out = {}
    for stem, rel, doc in g.contracts():
        for name, q in ((doc or {}).get("x-ticvai-queries") or {}).items():
            out[f"{stem}#{name}"] = (stem, q if isinstance(q, dict) else {})
    return out


# **A fact named in an operation's text is a read too** (ADAM CR-096 and CR-135; CHG-RTE-001). The words that name
# another module's fact, phrase -> the table that holds it. A phrase joins or leaves with the change that shows the
# need, as check-error-sources' ENTITIES do. Each is one a CR of 15-17 October found unrouted.
FACTS = {
    r"\bregion'?s (?:time ?zone|clock|calendar)": "platform.region_settings",      # createPerformances (CR-096)
    r"\bregion settings?\b": "platform.region_settings",
    r"\bvenue settings?\b": "platform.venue_settings",                              # publishPromotion (CR-096)
    r"\bvenue'?s `?cashDrawerLimit\b": "platform.venue_settings",                   # allocateDepositBox (CR-135)
    r"\bvenue'?s (?:frozen )?trading currency\b": "platform.venue_settings",        # CR-135
    r"\bactive venues\b|\bscope node is active\b": "platform.scope",                # setAnalyticsProvider (CR-096)
    r"\banother tenant\b": "control.tenant_domain",                                 # claimCustomDomain (CR-096)
    r"\blicen[cs]e allows\b|\badd-on keyed\b": "control.licence_add_on",            # setBrandIdentity (CR-096)
    r"\blive promotions?\b": "promotions.promotion",                                # lookupMerchandise (CR-096)
    r"\bticket and pass templates\b": "orders.ticket_template",                     # createPreview (CR-096)
    r"\bdenominations?\b": "platform.denomination",                                 # allocateDepositBox (CR-135)
    r"\bcell serving\b|\bits cell\b": "control.cell",                               # getPlatformSubdomain (CR-096)
    r"\bcollection point\b": "fnb.delivery_location",                               # createShopAndDrop (CR-096)
    r"\btax codes?\b": "ledger.tax_code",                                           # publishBundle (CR-110)
    r"\bno rate for\b|\bexchange rates?\b": "ledger.fx_rate",                       # setVenueSettings (CR-096)
}
FACT_RES = [(re.compile(p, re.I), t) for p, t in FACTS.items()]
# Phrases where a fact's words are not a read of it, removed before matching (check-error-sources NOT_ENTITY works
# the same way). Each one names the operations whose text showed the need (the CHG-RTE-001 dry run, 18 October).
NOT_READ: tuple = tuple(re.compile(p, re.I) for p in (
    r"never from another tenant's data",        # getAiVenueSettings, setAiVenueSettings: no other tenant is read
    r"phone number or collection point",        # deliverCredential: a credential's collection desk, not F&B's
    r"moves with the exchange rate",            # listChannelListings, setChannelListing, listPartnerAgreements
    r"not the denomination of an amount",       # setCurrencyRoundingRule: the word, not a till denomination
    r"Denominations, (?:validity, activation|whether an open amount)",   # setGiftCardProduct: gift card values
    r"rather than a venue setting",             # listDiningOutlets: says what is not a venue setting
    r"introduced later as a venue setting",     # createJournalEntry: a setting that does not exist yet
    r"appears on tax codes, FX rates",          # listProducts, cloneProduct and the product family: a comparison
))
TABLE_IN_TEXT = re.compile(r"(?<![\w.])([a-z][a-z0-9_]*)\.([a-z][a-z0-9_]+)\b")
FIELD_IN_TEXT = re.compile(r"(?<![\w.])(?:([a-z][a-z-]+)\.)?([A-Z][A-Za-z0-9]+)\.([a-z][A-Za-z0-9]+)\b")
SCHEMA_IN_TEXT = re.compile(r"`([A-Z][A-Za-z0-9]+)`")
ID_LIKE = re.compile(r"(?:^id$|Ids?$|Ref$)")
# **The facts the CRs named, which may never be baselined** (XR-FACT): (operation, table).
MUST_FIX_FACTS = {
    ("createPerformances", "platform.region_settings"),
    ("setVenueSettings", "ledger.fx_rate"),
    ("setVenueSettings", "payments.provider"),
    ("createShopAndDrop", "fnb.delivery_location"),
    ("lookupMerchandise", "promotions.promotion"),
    ("setBrandIdentity", "control.licence_add_on"),
    ("setBrandIdentity", "assets.media_asset"),
    ("setAnalyticsProvider", "platform.scope"),
    ("setMaintenanceMode", "platform.scope"),
    ("createPreview", "orders.ticket_template"),
    ("claimCustomDomain", "control.tenant_domain"),
    ("getPlatformSubdomain", "control.cell"),
    ("allocateDepositBox", "platform.denomination"),
    ("allocateDepositBox", "platform.venue_settings"),
}


def query_tables(q: dict) -> set:
    """The tables a declared query answers over: its `table`, its projection's `source` (`a.b + c.d`), its `reads`."""
    out = set()
    if q.get("table"):
        out.add(str(q["table"]).strip())
    pr = q.get("projection") if isinstance(q.get("projection"), dict) else {}
    if pr.get("source"):
        out |= {s.strip() for s in str(pr["source"]).split("+") if s.strip()}
    out |= {str(t).strip() for t in q.get("reads") or []}
    return out


def covered_by(via: list, queries: dict) -> tuple:
    """(tables asked over, owners asked a rule query that names no table) for an operation's readVia. `queries` maps
    `<contract>#<name>` to (owning service, the query's tables)."""
    tables, owners = set(), set()
    for r in via or []:
        owner, tabs = queries.get(str((r or {}).get("query") or ""), (None, set()))
        if tabs:
            tables |= tabs
        elif owner:
            owners.add(owner)
    return tables, owners


def is_covered(table: str, owner, tables: set, owners: set) -> bool:
    """Covered by a query over that table, or by a rule query of its owner that names no table."""
    return table in tables or owner in owners


def persisted(by: dict, tables: set) -> dict:
    """(contract, schema) -> the first table its x-ticvai-persistence names, where the schema reference has it."""
    out = {}
    for key, s in by.items():
        m = re.match(r'\s*"?([a-z][a-z0-9_]*\.[a-z][a-z0-9_]+)', str((s or {}).get("x-ticvai-persistence") or ""))
        if m and m.group(1) in tables:
            out[key] = m.group(1)
    return out


def op_text(stem: str, op: dict, item: dict, by: dict) -> str:
    """Everything an operation says in words: summary, description, parameters, request and response descriptions,
    the descriptions and x-ticvai-persistence of its own contract's schemas they use (`$ref` followed, every level),
    and of an own schema named in backticks (`ConflictAnalysis`), one hop. A field that only holds a key (`id`,
    `...Id`, `...Ids`, `...Ref`, a uuid) is skipped: naming the record it points at is not reading it."""
    out, seen = [], set()

    def walk(node, depth=0, name=""):
        if depth > 8 or (name and ID_LIKE.search(name)):
            return
        if isinstance(node, dict):
            if node.get("format") == "uuid":
                return
            for k, v in node.items():
                k = str(k)
                if k in ("description", "summary") and isinstance(v, str):
                    out.append(v)
                elif k == "x-ticvai-persistence" and isinstance(v, str):
                    out.append(v)
                elif k == "$ref" and isinstance(v, str):
                    n = v.rsplit("/", 1)[-1]
                    if v.startswith("#") and (stem, n) in by and (stem, n) not in seen:
                        seen.add((stem, n))
                        walk(by[(stem, n)], depth + 1)
                elif k == "properties" and isinstance(v, dict):
                    for pn, pv in v.items():
                        walk(pv, depth + 1, str(pn))
                elif k.startswith("x-ticvai-") or k == "429":
                    continue
                else:
                    walk(v, depth)
        elif isinstance(node, list):
            for x in node:
                walk(x, depth)

    walk({"op": op, "parameters": (item or {}).get("parameters")})
    for n in sorted({m.group(1) for t in list(out) for m in SCHEMA_IN_TEXT.finditer(t)}):
        if (stem, n) in by and (stem, n) not in seen:
            seen.add((stem, n))
            walk(by[(stem, n)], 1)
    return "\n".join(out)


def facts_named(text: str, reader: str, owner_of_schema: dict, tables: set, persist: dict = None,
                names: dict = None, svc_of_contract: dict = None) -> dict:
    """table -> [(how, phrase)]: every table of a module other than `reader` the text names, by its name (`table`),
    by a field or a backticked name of a schema another module's contract persists to it (`field`, `schema`), or by
    a phrase of FACTS (`fact`). The kernel tables every role reads are not facts by name."""
    for rx in NOT_READ:
        text = rx.sub(" ", text)
    out: dict = {}

    def note(t, how, phrase):
        own = owner_of_schema.get(t.split(".", 1)[0])
        if own and own != reader and t in tables:
            out.setdefault(t, []).append((how, phrase))

    for m in TABLE_IN_TEXT.finditer(text):
        t = f"{m.group(1)}.{m.group(2)}"
        if t not in KERNEL_READ:
            note(t, "table", m.group(0))
    if persist is not None and names is not None and svc_of_contract is not None:
        def schema_table(contract, schema):
            for stem in names.get(schema) or []:
                if contract and stem != contract:
                    continue
                if svc_of_contract.get(stem) == reader:
                    return None
                return persist.get((stem, schema))
            return None

        for m in FIELD_IN_TEXT.finditer(text):
            c, sch, fld = m.groups()
            if not ID_LIKE.search(fld):
                t = schema_table(c, sch)
                if t:
                    note(t, "field", m.group(0))
        for m in SCHEMA_IN_TEXT.finditer(text):
            t = schema_table(None, m.group(1))
            if t:
                note(t, "schema", m.group(0))
    for rx, t in FACT_RES:
        m = rx.search(text)
        if m:
            note(t, "fact", m.group(0))
    return out


def fact_findings() -> list:
    """[(operation, reader, table, owner, how, phrase)] for every fact an operation's text names that no query it
    asks covers, the operation's own lineage reads and writes left to the rules that judge them. Shared by main(),
    `--list-facts` and tools/applied/read-routes-18-october.py."""
    lin = g.load_json(g.ROOT / "handoff" / "api-data-lineage.json", {}) or {}
    services = (g.load_json(g.ROOT / "handoff" / "service-decomposition.json", {}) or {}).get("services") or {}
    owner_of_schema = {sc: s for s, v in services.items() for sc in v.get("schemas") or []}
    svc_of_contract = {c: s for s, v in services.items() for c in v.get("contracts") or []}
    tables = set((g.load_json(g.ROOT / "handoff" / "schema-reference.json", {}) or {}).get("cols") or {})
    by, names = g.schemas()
    persist = persisted(by, tables)
    qtables = {k: (svc_of_contract.get(stem), query_tables(q)) for k, (stem, q) in declared_queries().items()}
    out = []
    for o, f in sorted(g.operations().items()):
        e = lin.get(o) or {}
        reader = e.get("service") or svc_of_contract.get(f["contract"])
        if reader not in services:
            continue
        # The contract's own routes as well as the lineage's, so the class query sees a route as soon as it is
        # written, before derive-lineage copies it (XR-LINEAGE keeps the two equal).
        via = [r for r in (f["op"].get("x-ticvai-read-via") or []) if isinstance(r, dict)] + (e.get("readVia") or [])
        cov_t, cov_o = covered_by(via, qtables)
        skip = set(e.get("reads") or []) | set(e.get("writes") or [])
        skip |= {str(w.get("table")) for w in e.get("writeVia") or [] if isinstance(w, dict)}
        skip |= {t.rsplit("_for_", 1)[0] for t in e.get("reads") or [] if "_for_" in t}
        text = op_text(f["contract"], f["op"], f["item"], by)
        for t, hits in sorted(facts_named(text, reader, owner_of_schema, tables, persist, names,
                                          svc_of_contract).items()):
            owner = owner_of_schema.get(t.split(".", 1)[0])
            if t in skip or is_covered(t, owner, cov_t, cov_o):
                continue
            how, phrase = hits[0]
            out.append((o, reader, t, owner, how, phrase))
    return out


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-cross-module-reads", RULES)
    lin = g.load_json(g.ROOT / "handoff" / "api-data-lineage.json", {}) or {}
    dec = g.load_json(g.ROOT / "handoff" / "service-decomposition.json", {}) or {}
    services = dec.get("services") or {}
    dep_of = {s: v.get("deployable") for s, v in services.items()}
    tier_of = {s: v.get("tier") for s, v in services.items()}
    owner_of_schema = {sc: s for s, v in services.items() for sc in v.get("schemas") or []}
    svc_of_contract = {c: s for s, v in services.items() for c in v.get("contracts") or []}
    names_of = {s: {slug(s), *(v.get("contracts") or []), *(v.get("schemas") or [])} for s, v in services.items()}

    def module(name: str) -> str | None:
        """A query's `module`: a service name (`OrderService`), or one of its contracts or schemas."""
        n = str(name or "")
        if n in services:
            return n
        for s, ns in names_of.items():
            if n.lower() in {x.lower() for x in ns} or n.lower() == slug(s):
                return s
        return None

    queries = declared_queries()
    ops = contract_ops()
    if "--list-facts" in sys.argv[1:]:
        for row in fact_findings():
            print("\t".join(str(x).replace("\t", " ").replace("\n", " ") for x in row))
        return 0
    qtables = {k: (svc_of_contract.get(stem), query_tables(q)) for k, (stem, q) in queries.items()}
    # XR-QUERY on the declarations themselves
    for key, (stem, q) in sorted(queries.items()):
        miss = [f for f in QUERY_FIELDS if not q.get(f)]
        if miss:
            guard.add("XR-QUERY", key, f"{key} declares no {', '.join(miss)}")
        mod = module(q.get("module"))
        if mod is None or mod != svc_of_contract.get(stem):
            guard.add("XR-QUERY", f"{key}:module", f"{key}: module {q.get('module')!r} is not "
                      f"{svc_of_contract.get(stem)}, which owns contracts/{stem}")
        bad = [r for r in (q.get("served") or []) if r not in ROUTES]
        if bad:
            guard.add("XR-QUERY", f"{key}:served", f"{key}: served {bad} is not one of {', '.join(ROUTES)}")

    n_cross = 0
    for o, e in sorted(lin.items()):
        reader = e.get("service")
        if reader not in services:
            continue
        rdep = dep_of.get(reader)
        via = e.get("readVia") or []
        for r in via:
            key = str(r.get("query") or "")
            route = str(r.get("route") or "")
            if key not in queries:
                guard.add("XR-QUERY", f"{o}:{key}", f"{o} reads via {key!r}, which no contract declares in "
                          "x-ticvai-queries")
                continue
            stem, q = queries[key]
            owner = svc_of_contract.get(stem)
            if route not in ROUTES:
                guard.add("XR-ROUTE", f"{o}:{key}", f"{o} asks {key} by {route!r}; a route is one of {', '.join(ROUTES)}")
            elif route not in (q.get("served") or []):
                guard.add("XR-ROUTE", f"{o}:{key}", f"{o} asks {key} by {route}, which the query does not serve "
                          f"({', '.join(q.get('served') or []) or 'none'})")
            if route == "in-process" and owner and dep_of.get(owner) != rdep:
                guard.add("XR-ROUTE", f"{o}:{key}", f"{o} ({rdep}) asks {key} in-process, and {owner} is in "
                          f"{dep_of.get(owner)}: across deployables a query is a service call or a projection")
            if reader in FOUNDATION_STRICT and owner and tier_of.get(owner) != "foundation" and route != "projection":
                guard.add("XR-FOUNDATION", f"{o}:{key}", f"{o} ({reader}, foundation) asks {key} of {owner} "
                          f"({tier_of.get(owner)}) by {route}: Identity reads nothing above it but a projection")
        cov_t, cov_o = covered_by(via, qtables)
        for t in e.get("reads") or []:
            if ":" in t or "." not in t or t in KERNEL_READ:
                continue
            schema, short = t.split(".", 1)
            owner = owner_of_schema.get(schema)
            if not owner or owner == reader:
                continue
            n_cross += 1
            strict = owner in MUST_FIX.get(o, set())
            m = re.match(r"^(.+)_for_([a-z0-9_]+)$", short)
            if m and m.group(2) in {x.replace("-", "_") for x in names_of.get(reader, set())}:
                if dep_of.get(owner) != rdep:
                    guard.add("XR-VIEW-ACROSS", f"{o}:{t}", f"{o} ({rdep}) reads the view {t} of {owner} "
                              f"({dep_of.get(owner)}): across deployables use the owner's service or a projection",
                              strict=strict)
                continue
            if is_covered(t, owner, cov_t, cov_o):
                continue
            guard.add("XR-UNCOVERED", f"{o}:{t}", f"{o} ({reader}, {rdep}) reads {t}, which {owner} "
                      f"({dep_of.get(owner)}) owns, raw: ask a declared query (x-ticvai-read-via) or, within one "
                      f"deployable and for bulk data, read {schema}.{short}_for_{slug(reader)}", strict=strict)
            if reader in FOUNDATION_STRICT and tier_of.get(owner) != "foundation":
                guard.add("XR-FOUNDATION", f"{o}:{t}", f"{o} ({reader}, foundation) reads {t} of {owner} "
                          f"({tier_of.get(owner)}): Identity reads nothing above it but a projection", strict=strict)
    # XR-FACT (CHG-RTE-001): what the text names, beyond the lineage
    facts = fact_findings()
    for o, reader, t, owner, how, phrase in facts:
        guard.add("XR-FACT", f"{o}:{t}",
                  f"{o} ({reader}) names {t} ({how}: {phrase!r}), which {owner} owns, and asks no query over it: add "
                  f"an x-ticvai-read-via to {owner}'s query for {t} (ADR-0055 rule 2; CR-096)",
                  strict=(o, t) in MUST_FIX_FACTS)
    # XR-LINEAGE
    for o in sorted(set(ops) | {o for o, e in lin.items() if e.get("readVia")}):
        want = sorted(({k: str(r[k]) for k in ("query", "route", "for") if r.get(k)}
                       for r in (ops.get(o) or {}).get("x-ticvai-read-via") or [] if isinstance(r, dict)
                       and r.get("query")), key=lambda r: (r["query"], r.get("for", "")))
        if o in lin and (lin[o].get("readVia") or []) != want:
            guard.add("XR-LINEAGE", o, f"{o}: the lineage's readVia differs from the contract's x-ticvai-read-via "
                      "(python tools/derive-lineage.py --apply)")
    guard.note(f"{n_cross} cross-module table read(s) in the lineage; {len(facts)} fact(s) named in text and not "
               f"asked; {len(queries)} declared quer(ies)")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
