#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A refusal that depends on another module's records says what it is and where it is read from (ADAM CR-084, CHG-GDL-001).

**Found by ADAM CR-084 on 14 October 2026** (ticket 30654). `deleteGuestAccount` answered `409` "Open orders or an
unexpired entitlement exist" with no problem type and no definition of either, and its lineage read only
`pii.subject`: the condition lived in Orders' and Access's tables, which Identity, Foundation, does not read
(ADR-0028), one of them in another deployable (ADR-0055 rule 4). The developer could neither test the refusal nor
build it without inventing a cross-module read. The audit found the same shape on `configureWorkstation` ("a shift
is open", CR-083) and `createSaleBoard` ("unknown or unsellable variant", CR-081).

The r6 convention (Chinmay, 14 October 2026; ADR-0055 amendment): the owner declares the rule question in its
contract's top-level `x-ticvai-queries` (`<queryName>: {module, inputs, returns, rule, served}`), and the asking
operation names it in `x-ticvai-read-via: [{query: <contract>#<queryName>, route, for}]`. This check covers the
error side of that convention; batch GEN's `check-cross-module-reads` covers the lineage side.

    E-PROBLEM-TYPE  a 4xx response (not a shared `$ref`, not 429) whose description names an entity another module
                    owns declares no `x-ticvai-problem-types`, so the client cannot tell the cause apart
    E-READ-VIA      the same response's operation declares no `x-ticvai-read-via` whose query the entity's owning
                    module answers, so nothing says how the condition is read
    E-QUERY         an `x-ticvai-read-via` entry names a query no contract declares in `x-ticvai-queries`, or a route
                    the query does not serve (in-process, service, projection)

**An entity** is one of the records in ENTITIES below (`order`, `entitlement`, `shift`, `variant`, ...), each named with
the table that holds it; its owner is the service whose schemas hold that table (handoff/service-decomposition.json),
and the operation's module is its lineage `service`. A few phrases where the word is not the entity ("in order to",
"sort order") are ignored. `--entities` lists the vocabulary with the owners.

Read-only. Exit 1 on a finding not in `handoff/audit-baseline.json` (tools/audit_guard.py): the known ones are the
backlog, and a new refusal must not add to it.

    python3 tools/check-error-sources.py [--all] [--update-baseline] [--entities]
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {
    "E-PROBLEM-TYPE": "a 4xx naming another module's entity declares x-ticvai-problem-types (ADAM CR-084)",
    "E-READ-VIA": "a 4xx naming another module's entity has an x-ticvai-read-via to that module's query (ADAM CR-084)",
    "E-QUERY": "an x-ticvai-read-via names a declared x-ticvai-queries entry and a route it serves",
}
ROUTES = ("in-process", "service", "projection")

# **The records a refusal commonly depends on**, word -> the table that holds them. The word list is a judgement (one
# derived from every persisted schema name was mostly ordinary English: "event", "account", "plan"); the owner is not:
# it is read from handoff/service-decomposition.json through the table's schema, so a table that moves module moves
# its refusals with it. Longer names are matched first ("purchase order" is Inventory's, not Orders'). A word joins or
# leaves the list with the change that shows the need.
ENTITIES = {
    "order": "orders.sales_order",
    "purchase order": "inventory.purchase_order",
    "work order": "maintenance.work_order",
    "service order": "fnb.service_order",
    "f&b order": "fnb.service_order",
    "kitchen order": "fnb.service_order",
    "entitlement": "access.entitlement",
    "shift": "orders.pos_shift",
    "variant": "catalogue.variant",
    "product": "catalogue.product",
    "performance": "catalogue.performance",
    "payment": "orders.payment",
    "refund": "orders.refund",
    "chargeback": "orders.chargeback",
    "cart": "orders.cart",
    "seat": "seating.seat",
    "voucher": "promotions.voucher",
    "promotion": "promotions.promotion",
    "wallet": "wallet.wallet",
    "gift card": "wallet.gift_card",
    "settlement": "ledger.settlement",
    "posting": "ledger.posting",
    "workstation": "platform.workstation",
    "outlet": "platform.outlet",
    "supplier": "inventory.supplier",
    "requisition": "inventory.requisition",
    "membership": "identity.customer_membership",
}
# **The same word for a module's own record.** In Inventory "the order" is its purchase order, in Maintenance a work
# order, in F&B a service order, and in Access "the shift" is a podium shift: an operation whose module owns one of
# these tables reads the word as its own. (Workforce's `workforce.shift` is deliberately not here: Tenancy owns it, and
# Tenancy's configureWorkstation refusing on an open till shift is exactly the case to catch, CR-083.)
HOMONYMS = {
    "order": ("inventory.purchase_order", "maintenance.work_order", "fnb.service_order"),
    "shift": ("access.podium_shift",),
}
# Phrases where an entity word is ordinary English, removed before matching.
NOT_ENTITY = re.compile(r"\b(?:in order (?:to|for)|sort order|display order|order of|"
                        r"the order in which|in the order|in any order|out of order|sequence order|"
                        r"(?:ascending|descending) order|order (?:by|matters))\b", re.I)


def owner_maps():
    dec = g.load_json(g.ROOT / "handoff" / "service-decomposition.json", {}) or {}
    services = dec.get("services") or {}
    owner_of_schema = {sc: s for s, v in services.items() for sc in v.get("schemas") or []}
    service_of_contract = {c: s for s, v in services.items() for c in v.get("contracts") or []}
    return owner_of_schema, service_of_contract


def entities(owner_of_schema):
    """entity word -> owning service, for the ENTITIES whose table the schema reference has."""
    cols = (g.load_json(g.ROOT / "handoff" / "schema-reference.json", {}) or {}).get("cols") or {}
    out = {}
    for w, t in ENTITIES.items():
        owner = owner_of_schema.get(t.split(".", 1)[0])
        if owner and (not cols or t in cols):
            out[w] = owner
    return out


def pattern(vocab):
    alts = sorted(vocab, key=len, reverse=True)
    return re.compile(r"(?<![\w&])(%s)s?\b" % "|".join(re.escape(w).replace(r"\ ", r"\s+") for w in alts), re.I)


def queries(service_of_contract):
    """'<contract>#<query>' -> (owning service, served routes) from every contract's top-level x-ticvai-queries."""
    out = {}
    for stem, _rel, doc in g.contracts():
        for q, spec in ((doc or {}).get("x-ticvai-queries") or {}).items():
            spec = spec if isinstance(spec, dict) else {}
            served = spec.get("served") or []
            out["%s#%s" % (stem, q)] = (service_of_contract.get(stem), [str(s) for s in served])
    return out


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-error-sources", RULES)
    owner_of_schema, service_of_contract = owner_maps()
    vocab = entities(owner_of_schema)
    if "--entities" in sys.argv[1:]:
        for w, o in sorted(vocab.items()):
            print("  %-16s %-26s %s" % (w, ENTITIES[w], o))
        for w in sorted(set(ENTITIES) - set(vocab)):
            print("  %-16s %-26s (no such table or owner: not checked)" % (w, ENTITIES[w]))
        return 0
    words = pattern(vocab)
    declared = queries(service_of_contract)
    lin = g.load_json(g.ROOT / "handoff" / "api-data-lineage.json", {}) or {}

    for oid, o in sorted(g.operations().items()):
        op = o["op"]
        mine = (lin.get(oid) or {}).get("service") or service_of_contract.get(o["contract"])
        reached = set()
        for v in op.get("x-ticvai-read-via") or []:
            if not isinstance(v, dict):
                continue
            q = str(v.get("query") or "")
            if q not in declared:
                guard.add("E-QUERY", "%s|%s" % (oid, q),
                          "%s: x-ticvai-read-via names %s, which no contract declares in x-ticvai-queries" % (oid, q))
                continue
            svc, served = declared[q]
            route = str(v.get("route") or "")
            if route not in ROUTES or (served and route not in served):
                guard.add("E-QUERY", "%s|%s|%s" % (oid, q, route),
                          "%s: x-ticvai-read-via reaches %s by route '%s', and it serves %s"
                          % (oid, q, route, ", ".join(served) or "nothing"))
            reached.add(svc)
        for code, r in sorted((op.get("responses") or {}).items(), key=lambda kv: str(kv[0])):
            c = str(code)
            if not c.startswith("4") or c == "429" or not isinstance(r, dict) or "$ref" in r:
                continue
            text = NOT_ENTITY.sub(" ", str(r.get("description") or ""))
            foreign = {}
            for m in words.finditer(text):
                w = re.sub(r"\s+", " ", m.group(1).lower())
                if w in HOMONYMS and mine in {owner_of_schema.get(t.split(".", 1)[0]) for t in HOMONYMS[w]}:
                    continue
                if vocab.get(w) and vocab[w] != mine:
                    foreign.setdefault(vocab[w], set()).add(w)
            if not foreign:
                continue
            named = ", ".join("%s (%s)" % ("/".join(sorted(ws)), s) for s, ws in sorted(foreign.items()))
            if not r.get("x-ticvai-problem-types"):
                guard.add("E-PROBLEM-TYPE", "%s|%s" % (oid, c),
                          "%s %s names %s and declares no x-ticvai-problem-types" % (oid, c, named))
            missing = sorted(s for s in foreign if s not in reached)
            if missing:
                guard.add("E-READ-VIA", "%s|%s" % (oid, c),
                          "%s %s names %s and has no x-ticvai-read-via to a query of %s"
                          % (oid, c, named, ", ".join(missing)))
    guard.note("%d entity words; %d declared queries" % (len(vocab), len(declared)))
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
