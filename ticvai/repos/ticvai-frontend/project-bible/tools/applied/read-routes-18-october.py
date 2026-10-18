#!/usr/bin/env python3
"""Read routes between modules, 18 October 2026 (ADAM CR-096, CR-135, CR-110's tax codes; CHG-RTE-001).

ADR-0055 rule 2 as amended 14 October: another module's data is asked of its owner through a declared query. The
fourteen Sprint 1 operations of CR-096 and allocateDepositBox (CR-135) named facts of other modules in their text
and asked nothing. This writes, at their own lines:

  QUERIES   the eight owner queries the published answers declare, each in the contract that persists its table;
  EXPLICIT  the read routes the answers name, operation by operation;
  the sweep every other operation whose text names one of the same facts (check-cross-module-reads XR-FACT, the
            phrase detector, `how == fact`), routed to the owner's query for that table (decision D1);
  served    each query's `served` gains the route its new askers take, and the rule's last sentence says so.

An Identity operation asking above the foundation tier is not routed (only a projection answers it, ADR-0028); it is
printed for the lead. Run after the check's XR-FACT exists. A second run writes nothing. The contracts keep their own
line endings.

    python tools/applied/read-routes-18-october.py            # what it would write
    python tools/applied/read-routes-18-october.py --apply
"""
from __future__ import annotations

import argparse
import importlib.util
import re
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))
import audit_guard as g  # noqa: E402

ROUTES = ("in-process", "service", "projection")


def _check():
    spec = importlib.util.spec_from_file_location("xr", TOOLS / "check-cross-module-reads.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def route_for(reader_deployable: str, owner_deployable: str) -> str:
    return "in-process" if reader_deployable == owner_deployable else "service"


_CRLF: dict = {}


def _read(path: Path) -> str:
    """The file's text with LF line ends; the file's own ends are restored by _write."""
    raw = path.read_bytes().decode("utf-8")
    _CRLF[path] = "\r\n" in raw
    return raw.replace("\r\n", "\n")


def _write(path: Path, text: str) -> None:
    if _CRLF.get(path):
        text = text.replace("\n", "\r\n")
    path.write_bytes(text.encode("utf-8"))


def _op_block(lines: list, op: str):
    i = next((n for n, l in enumerate(lines) if re.match(r"^\s+operationId:\s*%s\s*$" % re.escape(op), l)), None)
    if i is None:
        raise SystemExit(f"{op}: no such operationId")
    ind = re.match(r"^(\s+)", lines[i]).group(1)
    end = i + 1
    while end < len(lines) and (not lines[end].strip() or len(lines[end]) - len(lines[end].lstrip()) >= len(ind)):
        end += 1
    return i, end, ind


def add_read_via(text: str, op: str, entries: list):
    """entries: [(query, route, for)]. Appends to the operation's x-ticvai-read-via (one entry per query), or writes
    the list after operationId and its x-ticvai-consumed-by. Returns (text, entries added)."""
    lines = text.split("\n")
    i, end, ind = _op_block(lines, op)
    have = set()
    k = next((n for n in range(i, end) if lines[n] == f"{ind}x-ticvai-read-via:"), None)
    if k is not None:
        at = k + 1
        while at < end and (lines[at].startswith(f"{ind}- ") or lines[at].startswith(f"{ind}  ")):
            m = re.match(r"^\s+- query:\s*(\S+)", lines[at])
            if m:
                have.add(m.group(1))
            at += 1
        new = []
    else:
        at = i + 1
        if at < end and lines[at] == f"{ind}x-ticvai-consumed-by:":
            at += 1
            while at < end and (lines[at].startswith(f"{ind}  ") or lines[at].startswith(f"{ind}- ")):
                at += 1
        new = [f"{ind}x-ticvai-read-via:"]
    added = 0
    for q, route, why in entries:
        if q in have:
            continue
        have.add(q)
        added += 1
        new += [f"{ind}- query: {q}", f"{ind}  route: {route}", f"{ind}  for: '" + why.replace("'", "''") + "'"]
    if not added:
        return text, 0
    lines[at:at] = new
    return "\n".join(lines), added


def _query_block(lines: list, name: str):
    i = next((n for n, l in enumerate(lines) if l == f"  {name}:"), None)
    if i is None:
        raise SystemExit(f"query {name}: not declared")
    end = i + 1
    while end < len(lines) and (not lines[end].strip() or lines[end].startswith("    ")):
        end += 1
    return i, end


def route_sentence(label: str, deployable: str, served: list) -> str:
    owner = label + ("'" if label.endswith("s") else "'s")
    parts = []
    if "in-process" in served:
        parts.append(f"asked in process within {deployable}, through the C# query interface {label} implements")
    if "service" in served:
        parts.append(f"asked from another deployable through {owner} service route (serviceAuth)")
    if "projection" in served:
        parts.append("kept by the asker as a projection the owner's events feed")
    return "It is " + ", and ".join(parts) + "."


def served_of(text: str, name: str) -> list:
    lines = text.split("\n")
    i, end = _query_block(lines, name)
    s = next(n for n in range(i, end) if re.match(r"^    served:\s*\[", lines[n]))
    return [x.strip() for x in re.match(r"^    served:\s*\[(.*)\]", lines[s]).group(1).split(",") if x.strip()]


def set_served(text: str, name: str, routes: list, deployable: str):
    """Sets query `name`'s served list (in ROUTES order) and rewrites the rule's "It is asked ..." sentence, which
    CHG-MOD-001 wrote from the routes. `deployable` is the owner's. Returns (text, changed)."""
    lines = text.split("\n")
    i, end = _query_block(lines, name)
    s = next(n for n in range(i, end) if re.match(r"^    served:\s*\[", lines[n]))
    cur = [x.strip() for x in re.match(r"^    served:\s*\[(.*)\]", lines[s]).group(1).split(",") if x.strip()]
    new = [r for r in ROUTES if r in routes]
    if new == cur:
        return text, False
    lines[s] = f"    served: [{', '.join(new)}]"
    r0 = next((n for n in range(i, end) if lines[n].startswith("    rule:")), None)
    body = [n for n in range(r0 + 1, end) if lines[n].startswith("      ")] if r0 is not None else []
    para = " ".join(lines[n].strip() for n in body)
    m = (re.search(r"\. (\S+) answers with its", para) or re.search(r"query interface (\S+) implements", para)
         or re.search(r"through (\S+?)'s? service route", para))
    if body and m and "It is asked" in para:
        para = para[:para.index("It is asked")] + route_sentence(m.group(1), deployable, new)
        lines[body[0]:body[-1] + 1] = textwrap.wrap(para, width=116, initial_indent="      ",
                                                     subsequent_indent="      ", break_long_words=False,
                                                     break_on_hyphens=False)
    return "\n".join(lines), True


def add_served(text: str, name: str, route: str, deployable: str):
    """Adds `route` to query `name`'s served list. Returns (text, changed)."""
    cur = served_of(text, name)
    if route in cur:
        return text, False
    return set_served(text, name, cur + [route], deployable)


def served_for(declared: list, used: set) -> list:
    """A query's served list: what its owner declared (r6, or the new query's own block) and every route an asker
    takes, in ROUTES order. A route the sweep added and no asker takes any more goes (fix round 1)."""
    return [r for r in ROUTES if r in declared or r in used]


SWEPT_FOR = re.compile(r"^what its text calls \".*\(CHG-RTE-001\)$")


def is_swept(route: dict) -> bool:
    """A read route this script's sweep wrote (its `for` says what the operation's text calls the fact)."""
    return bool(SWEPT_FOR.match(str((route or {}).get("for") or "")))


def remove_read_via(text: str, op: str, query: str):
    """Removes the operation's swept route to `query` (only one this sweep wrote); drops the list when it empties.
    Returns (text, removed)."""
    lines = text.split("\n")
    i, end, ind = _op_block(lines, op)
    k = next((n for n in range(i, end) if lines[n] == f"{ind}x-ticvai-read-via:"), None)
    if k is None:
        return text, 0
    at, items = k + 1, []
    while at < end and (lines[at].startswith(f"{ind}- ") or lines[at].startswith(f"{ind}  ")):
        if lines[at].startswith(f"{ind}- "):
            items.append([at, at + 1])
        else:
            items[-1][1] = at + 1
        at += 1
    for a, b in items:
        block = lines[a:b]
        q = re.match(r"^\s+- query:\s*(\S+)", block[0])
        why = next((re.match(r"^\s+for:\s*'(.*)'\s*$", l) for l in block if re.match(r"^\s+for:", l)), None)
        if q and q.group(1) == query and why and is_swept({"for": why.group(1).replace("''", "'")}):
            del lines[a:b]
            if len(items) == 1:
                del lines[k]
            return "\n".join(lines), 1
    return text, 0


def sweep_skips(method: str, table: str, own_facts: dict) -> bool:
    """A read (GET) is swept only where its own words (summary, description, parameters, request body) name the fact;
    a phrase that sits only in a shared response schema is a rule the writing operation keeps (fix round 1)."""
    return method.lower() == "get" and table not in own_facts


def add_query(text: str, name: str, block: str):
    """Appends `block` (indented two spaces, a whole query) to the top-level x-ticvai-queries map, once."""
    lines = text.split("\n")
    q = next((n for n, l in enumerate(lines) if l.rstrip() == "x-ticvai-queries:"), None)
    if q is None:
        raise SystemExit("no x-ticvai-queries map")
    end = q + 1
    while end < len(lines) and (not lines[end].strip() or lines[end].startswith(" ") or lines[end].startswith("#")):
        end += 1
    if any(l == f"  {name}:" for l in lines[q:end]):
        return text, False
    # a blank line or a top-level comment just before the next key belongs to that key, not to the map
    while end > q + 1 and (not lines[end - 1].strip() or lines[end - 1].startswith("#")):
        end -= 1
    lines[end:end] = block.rstrip("\n").split("\n")
    return "\n".join(lines), True


DATA_RULE = ("A data read, not a rule question ({src}; ADR-0055 rule 2 as amended 14 October). {label} answers "
             "with its {table} rows, as it stores them and as the caller's scope lets it see them (the table's "
             "row-level security, under the caller's connection and transaction). It decides nothing: an asker "
             "that refuses or chooses on these rows states that rule in its own operation, and a question with a "
             "rule of its own (open, live, sellable) is declared as a query of its own. {routes}")


def data_query(name, module, table, label, deployable, served, item_ref, src):
    rule = DATA_RULE.format(src=src, label=label, table=table, routes=route_sentence(label, deployable, served))
    body = textwrap.wrap(rule, width=116, initial_indent="      ", subsequent_indent="      ",
                         break_long_words=False, break_on_hyphens=False)
    return "\n".join([
        f"  {name}:",
        f"    module: {module}",
        f"    table: {table}",
        "    inputs:",
        f"      ids: {{type: array, items: {{type: string, format: uuid}}, description: 'The {table} rows asked for, "
        "by id.'}",
        "      where: {type: object, additionalProperties: true, description: 'Or the rows whose columns equal these "
        "values (a key the asker holds, such as subjectId, orderId or venueId); ids and where together narrow.'}",
        "    returns:",
        "      type: array",
        f"      description: 'The rows found, each as {label} stores it; an id with no visible row is absent.'",
        f"      items: {{$ref: '#/components/schemas/{item_ref}'}}",
        "    rule: >-",
        *body,
        f"    served: [{', '.join(served)}]",
    ]) + "\n"


CR096 = "ADAM CR-096, 15 October 2026, CHG-RTE-001"

# file (relative to ticvai/) -> [(query name, YAML block)]
QUERIES = {
    "contracts/spine/orders.yaml": [
        ("ticketTemplateRecords", data_query("ticketTemplateRecords", "orders", "orders.ticket_template", "Orders",
                                             "commerce", ["service"], "TicketTemplate", CR096)),
        ("venueChargeCurrencies", """  venueChargeCurrencies:
    module: orders
    table: payments.provider
    inputs:
      venueId: {type: string, format: uuid, description: 'The venue whose settings are being saved.'}
    returns:
      type: array
      description: 'The ISO 4217 codes the venue''s payment providers can charge, as a set; empty when it has none.'
      items: {type: string, pattern: '^[A-Z]{3}$'}
    rule: >-
      A rule question (ADAM CR-096, 15 October 2026, CHG-RTE-001; decision D7). The venue's payment providers are the
      active payments.provider rows (is_active) at the nearest level that has any: the venue's own, then its
      region's, then the tenant's (ADR-0018, nearest wins). The answer is the union of their presentment_currencies
      (PaymentProvider.presentmentCurrencies). setVenueSettings refuses a chargeCurrencies code outside it with 400.
      It is asked in process within commerce, through the C# query interface Orders implements.
    served: [in-process]
"""),
    ],
    "contracts/spine/tenancy.yaml": [
        ("activeVenues", """  activeVenues:
    module: tenancy
    table: platform.scope
    inputs:
      venueIds: {type: array, items: {type: string, format: uuid}, description: 'The venues asked about; omitted, every active venue of the tenant.'}
    returns:
      type: array
      description: 'The active venues in name order; a venue asked about that is not active, or that the caller cannot see, is absent.'
      items:
        type: object
        required: [venueId, name]
        properties:
          venueId: {type: string, format: uuid}
          name: {type: string}
    rule: >-
      A rule question (ADAM CR-096, 15 October 2026, CHG-RTE-001). A venue is active when its node in the scope
      tree (platform.scope, level venue) has is_active true. Tenancy answers for the tenant whose database the caller
      is connected to, under the caller's scope. White Label refuses a venueId that is absent (setAnalyticsProvider,
      422) and lists only these venues in TenantAppStatus.venues. It is asked from another deployable through
      Tenancy's service route (serviceAuth).
    served: [service]
"""),
    ],
    "contracts/satellite/fnb.yaml": [
        ("deliveryLocationRecords", data_query("deliveryLocationRecords", "fnb", "fnb.delivery_location", "F&B",
                                               "operations", ["in-process"], "DeliveryLocation", CR096)),
    ],
    "contracts/satellite/promotions.yaml": [
        ("liveEffectivePrice", """  liveEffectivePrice:
    module: promotions
    table: promotions.promotion
    inputs:
      venueId: {type: string, format: uuid}
      channel: {$ref: '../shared/common.yaml#/components/schemas/SalesChannel'}
      items:
        type: array
        items:
          type: object
          required: [itemRef, unitPrice]
          properties:
            itemRef: {type: string, description: 'The asker''s key for the item (a merchandise or variant id).'}
            productId: {type: string, format: uuid, nullable: true}
            unitPrice: {$ref: '../shared/common.yaml#/components/schemas/Money'}
    returns:
      type: array
      description: 'One entry per item asked, in the order asked.'
      items:
        type: object
        required: [itemRef, effectiveUnitPrice, promotionIds]
        properties:
          itemRef: {type: string}
          effectiveUnitPrice: {$ref: '../shared/common.yaml#/components/schemas/Money'}
          promotionIds: {type: array, items: {type: string, format: uuid}}
    rule: >-
      A rule question (ADAM CR-096, 15 October 2026, CHG-RTE-001). The promotions live now for the venue and channel
      (status live, not paused, valid_from at or before now, valid_to null or after now), applied to a basket of
      one unit of each item as evaluatePromotions applies them (stacking, precedence, the zero floor). A buyer's own
      conditions (segments, codes) are not applied, so this is the price any buyer pays. An item no promotion
      touches comes back at its unitPrice with no promotionIds. It is asked from another deployable through
      Catalogue's service route (serviceAuth).
    served: [service]
"""),
    ],
    "contracts/spine/finance.yaml": [
        ("taxCodeRecords", data_query("taxCodeRecords", "finance", "ledger.tax_code", "Ledger", "commerce",
                                      ["in-process"], "TaxCode", "ADAM CR-110, 15 October 2026, CHG-RTE-001")),
    ],
    "contracts/satellite/platform-ops.yaml": [
        ("hostnameHeldByAnotherTenant", """  hostnameHeldByAnotherTenant:
    module: platform-ops
    table: control.tenant_domain
    inputs:
      hostname: {type: string, description: 'The hostname being claimed.'}
    returns:
      type: object
      required: [held]
      properties:
        held: {type: boolean, description: 'True when another tenant holds it; who holds it is never returned.'}
    rule: >-
      A rule question (ADAM CR-096, 15 October 2026, CHG-RTE-001). True when a control.tenant_domain row with
      lower(hostname) equal to the asked hostname's, whose status is active, belongs to a tenant other than the
      caller's. Platform answers on its control connection, across tenants, and returns nothing about the holder.
      claimCustomDomain refuses the claim when it is true. It is asked in process within operations, through the C#
      query interface Platform implements.
    served: [in-process]
"""),
    ],
    "contracts/satellite/subscription.yaml": [
        ("cellRecords", data_query("cellRecords", "subscription", "control.cell", "Platform", "operations",
                                   ["in-process"], "Cell", CR096)),
    ],
}

# The routes the published answers name: (operation, query, route, for).
EXPLICIT = [
    ("createPerformances", "tenancy#regionSettingsRecords", "in-process",
     "the region's time zone the series is read in: daysOfWeek, until, firstStart and lastStart (ADAM CR-096)"),
    ("publishPromotion", "tenancy#venueSettingsRecords", "in-process",
     "the venue setting promotions.nearZeroLinePrice, the near-zero floor (ADAM CR-096)"),
    ("analysePromotionConflicts", "tenancy#venueSettingsRecords", "in-process",
     "the venue setting promotions.nearZeroLinePrice, the near-zero minimum (ADAM CR-096)"),
    ("setVenueSettings", "finance#fxRateRecords", "in-process",
     "displayCurrencies: a code the region has no rate for is refused 400 (ADAM CR-096)"),
    ("setVenueSettings", "orders#venueChargeCurrencies", "in-process",
     "chargeCurrencies: each must be one the venue's payment provider can charge (ADAM CR-096)"),
    ("createShopAndDrop", "orders#orderLineRecords", "service",
     "the retail lines lineIds names on the orderId path (ADAM CR-096)"),
    ("createShopAndDrop", "fnb#deliveryLocationRecords", "in-process",
     "collectionPointClosed: the collection point and its serving outlets (ADAM CR-096; the hours rule is CR-104)"),
    ("lookupMerchandise", "promotions#liveEffectivePrice", "service",
     "the price after any live promotion (ADAM CR-096)"),
    ("getCurrentSession", "tenancy#workstationRecords", "in-process",
     "the session's workstation fields: code, regionId and devices (ADAM CR-096)"),
    ("getCurrentSession", "tenancy#regionSettingsRecords", "in-process",
     "currency, currencyScale and timezone, from the workstation's region (ADAM CR-096)"),
    ("setBrandIdentity", "subscription#licenceAddOnRecords", "in-process",
     "showPoweredBy false: the tenant's licence add-on keyed poweredByRemoval, else 403 powered-by-locked "
     "(ADAM CR-096)"),
    ("setBrandIdentity", "assets#mediaAssetRecords", "in-process",
     "each asset's type, size and dimensions: PNG or SVG, up to 2 MB (ADAM CR-096)"),
    ("setAppIcons", "assets#mediaAssetRecords", "in-process",
     "the 1024x1024 source's type, size and dimensions (ADAM CR-096)"),
    ("setAnalyticsProvider", "tenancy#activeVenues", "service",
     "422: a venueId not among the tenant's active venues (ADAM CR-096)"),
    ("setMaintenanceMode", "tenancy#activeVenues", "service",
     "TenantAppStatus.venues: only the active venues are listed (ADAM CR-096)"),
    ("createPreview", "orders#ticketTemplateRecords", "service",
     "the ticket and pass templates the PDF ticket and Wallet passes are rendered from (ADAM CR-096)"),
    ("createPreview", "catalogue#productRecords", "service",
     "productId: the product whose own ticket is rendered (ADAM CR-096)"),
    ("claimCustomDomain", "platform-ops#hostnameHeldByAnotherTenant", "in-process",
     "refused where another tenant already holds the hostname (ADAM CR-096)"),
    ("getPlatformSubdomain", "platform-ops#tenantDomainRecords", "in-process",
     "the platform-issued address, the tenant's platform subdomain row (ADAM CR-096)"),
    ("getPlatformSubdomain", "subscription#cellRecords", "in-process",
     "the tenant's cell, whose name the address carries (ADAM CR-096)"),
    ("publishBundle", "finance#taxCodeRecords", "in-process",
     "the tax codes the bundle carries (ADAM CR-110)"),
    ("allocateDepositBox", "tenancy#denominationRecords", "in-process",
     "the face values of openingDenominations (ADAM CR-135)"),
    ("allocateDepositBox", "tenancy#venueSettingsRecords", "in-process",
     "the venue's trading currency (currencyCode) and its cashDrawerLimit where the workstation has none "
     "(ADAM CR-135)"),
]

# The query each fact of check-cross-module-reads' FACTS is asked through, by its table (the sweep, decision D1).
QUERY_FOR = {
    "platform.region_settings": "tenancy#regionSettingsRecords",
    "platform.venue_settings": "tenancy#venueSettingsRecords",
    "platform.denomination": "tenancy#denominationRecords",
    "platform.scope": "tenancy#activeVenues",
    "control.tenant_domain": "platform-ops#hostnameHeldByAnotherTenant",
    "control.licence_add_on": "subscription#licenceAddOnRecords",
    "promotions.promotion": "promotions#liveEffectivePrice",
    "orders.ticket_template": "orders#ticketTemplateRecords",
    "control.cell": "subscription#cellRecords",
    "fnb.delivery_location": "fnb#deliveryLocationRecords",
    "ledger.tax_code": "finance#taxCodeRecords",
    "ledger.fx_rate": "finance#fxRateRecords",
}
# Where a reader asks a different question of the same table: (table, reader) -> query. A queue's priority rule asks
# whether a guest qualifies for a promotion that is live (createQueue: "qualify for a live promotion in
# `promotionIds`"), which is the promotion's own row, not a price after promotions.
QUERY_FOR_READER = {
    ("promotions.promotion", "VenueOpsService"): "promotions#promotionRecords",
}
# The name a module's own queries use for it ("F&B answers with its ..."), where it is not the service's.
LABEL = {"FnbService": "F&B"}
# What the owners declared before this script, for the existing queries it may route to (r6, 86a3fa6f): a route it
# added is withdrawn when no asker takes it any more, but these never drop (fix round 1).
R6_SERVED = {
    "tenancy#regionSettingsRecords": ["in-process", "service"], "tenancy#venueSettingsRecords": ["in-process"],
    "tenancy#denominationRecords": ["in-process"], "tenancy#workstationRecords": ["in-process", "service"],
    "subscription#licenceAddOnRecords": ["in-process"], "finance#fxRateRecords": ["in-process", "service"],
    "promotions#promotionRecords": ["in-process", "service"], "assets#mediaAssetRecords": ["service"],
    "platform-ops#tenantDomainRecords": ["service"], "orders#orderLineRecords": ["in-process", "service"],
    "catalogue#productRecords": ["in-process", "service"],
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    services = (g.load_json(ROOT / "handoff" / "service-decomposition.json", {}) or {}).get("services") or {}
    dep_of = {s: v.get("deployable") for s, v in services.items()}
    tier_of = {s: v.get("tier") for s, v in services.items()}
    svc_of_contract = {c: s for s, v in services.items() for c in v.get("contracts") or []}
    texts = {}

    def text(rel):
        if rel not in texts:
            texts[rel] = _read(ROOT / rel)
        return texts[rel]

    # 1. the new queries
    for rel, qs in QUERIES.items():
        for name, block in qs:
            texts[rel], added = add_query(text(rel), name, block)
            print(f"  query {rel.split('/')[-1][:-5]}#{name}: {'added' if added else 'present'}")
    # 2. the routes: explicit first, then the sweep
    plan, skipped = {}, []
    for op, q, route, why in EXPLICIT:
        plan.setdefault(op, []).append((q, route, why))
    explicit_ops = {e[0] for e in EXPLICIT}
    xr = _check()
    ops = g.operations()
    owner_of_schema = {sc: sv for sv, v in services.items() for sc in v.get("schemas") or []}
    tables = set((g.load_json(ROOT / "handoff" / "schema-reference.json", {}) or {}).get("cols") or {})
    by, names = g.schemas()
    persist = xr.persisted(by, tables)
    get_skipped = []
    for op, reader, t, owner, how, phrase in xr.fact_findings(ignore=is_swept):
        if how != "fact" or t not in QUERY_FOR or op in explicit_ops:
            continue
        f = ops[op]
        own = xr.op_text(f["contract"], {k: v for k, v in f["op"].items() if k != "responses"}, f["item"], by)
        own_facts = {tt: [h for h in hs if h[0] == "fact"] for tt, hs in xr.facts_named(
            own, reader, owner_of_schema, tables, persist, names, svc_of_contract).items()}
        own_facts = {tt: hs for tt, hs in own_facts.items() if hs}
        if sweep_skips(f["method"], t, own_facts):
            get_skipped.append(f"{op}: {t} ({phrase!r} only in its response schema)")
            continue
        if reader == "IdentityService" and tier_of.get(owner) != "foundation":
            skipped.append(f"{op}: {t} ({owner}) - Identity asks above the foundation tier only by projection")
            continue
        words = phrase.replace("`", "").strip()
        label = LABEL.get(owner, owner[:-len("Service")])
        plan.setdefault(op, []).append((QUERY_FOR_READER.get((t, reader), QUERY_FOR[t]),
                                        route_for(dep_of.get(reader), dep_of.get(owner)),
                                        f'what its text calls "{words}": {t}, {label}\'s data (CHG-RTE-001)'))
    n_via = 0
    for op, entries in sorted(plan.items()):
        rel = ops[op]["file"]
        texts[rel], n = add_read_via(text(rel), op, entries)
        n_via += n
        for q, route, why in entries:
            if n:
                print(f"  {op}: {q} ({route}) - {why}")
    # 3. a swept route the sweep no longer justifies goes (fix round 1)
    wanted = {(op, q) for op, entries in plan.items() for q, _r, _w in entries}
    n_gone = 0
    for op, f in sorted(ops.items()):
        for r in f["op"].get("x-ticvai-read-via") or []:
            if isinstance(r, dict) and is_swept(r) and (op, r.get("query")) not in wanted:
                texts[f["file"]], n = remove_read_via(text(f["file"]), op, r.get("query"))
                n_gone += n
                if n:
                    print(f"  {op}: {r.get('query')} removed - no longer named in its own text")
    # 4. served routes: what the owner declared and every route an asker now takes
    used = {}
    for rel in sorted({f["file"] for f in ops.values()}):
        for m in re.finditer(r"- query:\s*(\S+)\s*\n\s+route:\s*(\S+)", text(rel)):
            used.setdefault(m.group(1), set()).add(m.group(2))
    declared = dict(R6_SERVED)
    for rel, qs in QUERIES.items():
        stem = rel.split("/")[-1][:-5]
        for name, block in qs:
            declared[f"{stem}#{name}"] = re.search(r"served: \[(.*)\]", block).group(1).split(", ")
    for q in sorted(declared):
        stem, name = q.split("#", 1)
        rel = next(r for r in (f"contracts/spine/{stem}.yaml", f"contracts/satellite/{stem}.yaml")
                   if (ROOT / r).exists())
        want = served_for(declared[q], used.get(q, set()))
        texts[rel], changed = set_served(text(rel), name, want, dep_of.get(svc_of_contract.get(stem)))
        if changed:
            print(f"  served {q}: {want}")
    for s in get_skipped:
        print(f"  NOT SWEPT (a read whose own text does not name it) {s}")
    for s in skipped:
        print(f"  NOT ROUTED (for the lead) {s}")
    print(f"{n_gone} swept route(s) removed")
    changed = [rel for rel, t in texts.items() if t != _read(ROOT / rel)]
    print(f"{n_via} read route(s) in {len(plan)} operation(s); {len(changed)} contract file(s) change"
          + ("" if a.apply else " (nothing written, pass --apply)"))
    if a.apply:
        for rel in changed:
            _write(ROOT / rel, texts[rel])
    return 0


if __name__ == "__main__":
    sys.exit(main())
