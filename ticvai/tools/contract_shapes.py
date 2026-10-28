#!/usr/bin/env python3
"""Read operations and response shapes out of the contracts, once, for every generator.

Two tools rebuild screens — `generate-screens-from-pack.py` for the 590 screens a workshop pack
describes, and `generate-screens-from-contracts.py` for the 501 it does not — and both need the
same three answers: what operations exist, what a given operation returns, and what fields that
shape has. **Two copies of that logic is two places for the pagination bug to live**, and it lived
in one of them for a day already.

## The pagination envelope is not the row

Every list response in this package is shaped

    allOf:
      - $ref: '.../Page'                       # items, nextCursor, hasMore
      - properties: { items: { items: { $ref: '#/.../Promotion' } } }

so taking the first `$ref` in the document returns `Page`, and a queue of approval requests binds
to a schema whose only properties are `items`, `nextCursor` and `hasMore`. That went unnoticed
because it is uniform: **every list operation was wrong in the same way**, so nothing looked odd
next to anything else. `response_schemas` returns the element type first.

## One level deep, deliberately

`schema_fields` merges `allOf` branches and reads properties one level down. **A checker that
half-resolves a `$ref` reports a real field as missing, and a wrong failure is worse than a missing
one** because somebody deletes the binding to make it pass.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

REF = re.compile(r"#/components/schemas/(\w+)")

# Wrappers, not subjects. A response that carries only one of these is a response whose element
# type was never declared, which is a finding rather than a binding.
ENVELOPES = {"Page", "Paged", "Cursor", "PageMeta", "Envelope"}


def load_contracts(root: Path) -> tuple[dict, dict]:
    """`(operations by operationId, schemas by name)` across every contract file."""
    ops, schemas = {}, {}
    for f in sorted((root / "contracts").rglob("*.yaml")):
        try:
            doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001 — an unreadable contract is check-package's business
            continue
        if not isinstance(doc, dict):
            continue
        for name, body in ((doc.get("components") or {}).get("schemas") or {}).items():
            if isinstance(body, dict):
                schemas.setdefault(name, body)
        for path, item in (doc.get("paths") or {}).items():
            if not isinstance(item, dict):
                continue
            for method, op in item.items():
                if isinstance(op, dict) and "operationId" in op:
                    ops[op["operationId"]] = {"file": f.name, "path": path, "method": method,
                                              "op": op}
    return ops, schemas


def response_schemas(op: dict) -> list[str]:
    """Schema names a success response carries, **element type before envelope**."""
    responses = op.get("responses") or {}
    for code in ("200", "201", "default"):
        for body in ((responses.get(code) or {}).get("content") or {}).values():
            schema = body.get("schema") or {}
            for branch in [schema] + (schema.get("allOf") or []):
                if not isinstance(branch, dict):
                    continue
                items = ((branch.get("properties") or {}).get("items") or {}).get("items") or {}
                if found := REF.findall(json.dumps(items)):
                    return found
            found = REF.findall(json.dumps(schema))
            ranked = ([f for f in found if f not in ENVELOPES]
                      + [f for f in found if f in ENVELOPES])
            if ranked:
                return ranked
    return []


def schema_fields(name: str, schemas: dict) -> dict:
    """`{property: body}` for one schema, with `allOf` branches merged. One level, no deeper."""
    body = schemas.get(name)
    if not isinstance(body, dict):
        return {}
    props = dict(body.get("properties") or {})
    for branch in body.get("allOf") or []:
        if isinstance(branch, dict):
            props.update(branch.get("properties") or {})
            for ref in REF.findall(json.dumps(branch.get("$ref") or "")):
                props.update((schemas.get(ref) or {}).get("properties") or {})
    return props


def path_params(op_entry: dict) -> list[str]:
    """Path parameters an operation requires — what the screen must arrive holding."""
    return re.findall(r"\{(\w+)\}", op_entry.get("path", ""))


def is_write(operation_id: str) -> bool:
    return not str(operation_id).startswith(("list", "get", "search", "export", "simulate",
                                             "preview", "validate"))


# ---------------------------------------------------------------------------------------------
# **The r10 patterns, written by default** (r10 lane E round 2, 26 October 2026, CHG-R10GEN-007). The lead, 26
# October: "the patterns we should update the build as well". Each rule r10 settled with a check and a one-off fixer
# is written here once, so the generators (draft-pack-operations, specify-pack-operations, the two screen
# generators) produce it without a fixer. The checks stay the proof; these only make the first draft right.
# ---------------------------------------------------------------------------------------------
R10_TAG = "(r10 pattern, CHG-R10GEN-007)"
# fix-order-and-refusals' never-null name keys, in its order (CHG-R10GEN-004).
ORDER_NAME_KEYS = ("displayName", "name", "title", "label", "code")
GUEST_AUDIENCES = {"guest", "anonymous", "public"}
GUEST_VENUE_REF = "../shared/common.yaml#/components/parameters/GuestVenue"
VENUE_REQUIRED_REF = "../shared/common.yaml#/components/responses/VenueRequired"
VENUE_Q = "tenancy#venueSettingsRecords"
REGION_Q = "tenancy#regionSettingsRecords"
SETTINGS_DEPLOYABLE = "commerce"      # Tenancy's (handoff/service-decomposition.json)
_GRANTED = None


def granted_in_process(reader_deployable: str, query: str, root: Path = None) -> bool:
    """Whether the lead granted `query` in process to `reader_deployable` across deployables: the `reads` of
    docs/active/cross-deployable-writes.yaml (ADAM CR-196, CHG-R9CR-005), the same set check-cross-module-reads
    XR-ROUTE allows. Since ADAM CR-296 (29 October 2026, CHG-R11RUL-001) the operations host reads Tenancy's four
    settings queries in process for every operation it hosts (XDR-004), so a generator drafting one of those reads for
    an operations-host operation writes `in-process`, not `service`, and the next draft needs no flip."""
    global _GRANTED
    if _GRANTED is None:
        root = root or Path(__file__).resolve().parents[1]
        p = root / "docs" / "active" / "cross-deployable-writes.yaml"
        doc = (yaml.safe_load(p.read_text(encoding="utf-8")) or {}) if p.exists() else {}
        _GRANTED = {(str(r.get("reader")), str(q)) for r in doc.get("reads") or [] for q in r.get("queries") or []}
    return (str(reader_deployable), str(query)) in _GRANTED


def read_route(reader_deployable: str, owner_deployable: str, query: str = None) -> str:
    """in-process within one deployable or where the lead granted the read in process (granted_in_process), else
    service (ADR-0055 rules 2 and 4 as amended)."""
    if reader_deployable == owner_deployable or (query and granted_in_process(reader_deployable, query)):
        return "in-process"
    return "service"


def order_sentence(props: dict, required) -> str:
    """(b) CHG-R10GEN-004, ADAM CR-206, CR-236, CR-190: the order a generated list states. A never-null name key, then
    `id`; a name key that can be null, its rows last (NULLS LAST) and `id` breaking ties; else newest first by
    `createdAt`; else `id` descending. The wording is fix-order-and-refusals', so check-list-order reads it."""
    req = set(required or ())
    for k in ORDER_NAME_KEYS:
        if k in (props or {}) and k in req:
            return f"**Order.** Sorted by `{k}` ascending, then by `id`. {R10_TAG}"
    for k in ORDER_NAME_KEYS:
        if k in (props or {}):
            return (f"**Order.** Sorted by `{k}` ascending. Where `{k}` is null the row sorts after the rows that "
                    f"have it (NULLS LAST), and `id` breaks every tie. {R10_TAG}")
    if "createdAt" in (props or {}):
        return f"**Order.** Newest first, by `createdAt` descending, then by `id`. {R10_TAG}"
    return f"**Order.** Sorted by `id` descending (a UUIDv7, so newest first). {R10_TAG}"


def is_public_guest_venue_read(method: str, path: str, audience, scope: str, params=()) -> bool:
    """(f) ADAM CR-198 option A, CHG-R10ID-010 and -022 (check-business-rules BR-GUEST-VENUE): a GET a guest calls
    without a session, at venue scope, whose path and required query do not already name the venue."""
    if str(method).lower() != "get" or not set(audience or ()) & GUEST_AUDIENCES or scope != "venue":
        return False
    if "{venueId}" in str(path or ""):
        return False
    return not any(isinstance(p, dict) and p.get("name") == "venueId" and p.get("in") == "query"
                   and p.get("required") for p in params or ())


def add_guest_venue(op: dict, method: str, path: str) -> bool:
    """(f) Gives a public guest read of venue data the shared GuestVenue header and `400 venue-required` (CR-198).
    Mutates `op`; returns whether it applies. A second call changes nothing."""
    if not is_public_guest_venue_read(method, path, op.get("x-ticvai-audience"), op.get("x-ticvai-scope-level"),
                                      op.get("parameters") or ()):
        return False
    params = op.setdefault("parameters", [])
    if not any(isinstance(p, dict) and str(p.get("$ref", "")).endswith("/parameters/GuestVenue") for p in params):
        params.append({"$ref": GUEST_VENUE_REF})
    resp = op.setdefault("responses", {})
    if "400" not in resp:
        resp["400"] = {"$ref": VENUE_REQUIRED_REF}
    return True


def scope_sentence(permission, scope: str, is_list: bool) -> str:
    """(g) ADAM CR-189 option A, CHG-R10ID-001 (Session.permissionsByScope): how a generated operation's permission is
    evaluated: per scope, never from the flat set."""
    if not permission:
        return ""
    if is_list:
        return (f"**Reach.** `{permission}` is evaluated per scope (`Session.permissionsByScope`, ADAM CR-189): the "
                f"list returns the rows under the scope paths where it holds, and a filter outside them is `403`. "
                f"{R10_TAG}")
    if scope == "tenant":
        return (f"**Permission.** `{permission}` must hold at the tenant root, read from the per-scope set "
                f"(`Session.permissionsByScope`, ADAM CR-189). {R10_TAG}")
    return (f"**Permission.** `{permission}` is evaluated at the {scope or 'scope'} the operation acts on, or one of "
            f"its ancestors, from the per-scope set (`Session.permissionsByScope`, ADAM CR-189). {R10_TAG}")


def has_money(node, schemas: dict = None, seen=frozenset()) -> bool:
    """Whether a schema (or a dict of them) refers to common Money, `$ref` followed within `schemas`."""
    s = json.dumps(node, default=str)
    if "/schemas/Money" in s:
        return True
    for ref in REF.findall(s):
        if schemas and ref in schemas and ref not in seen and has_money(schemas[ref], schemas, seen | {ref}):
            return True
    return False


def money_read_via(money: bool, scope: str, reader_deployable: str) -> list:
    """(a) naming-and-style 5.1, ADR-0018, CHG-R10GEN-002 (ADAM CR-234, CR-197, CR-217, CR-235, CR-202): the currency
    read a generated operation that answers or accepts common Money declares. A venue- or outlet-level operation asks
    the venue's settings, a region-level one the region's; in process within commerce and from the operations host
    (XDR-004, ADAM CR-296), service across otherwise. Above a region nothing denominates by default, so nothing is
    written and check-money-currency asks the author."""
    if not money:
        return []
    q = {"venue": VENUE_Q, "outlet": VENUE_Q, "region": REGION_Q}.get(scope)
    if not q:
        return []
    route = read_route(reader_deployable, SETTINGS_DEPLOYABLE, q)
    what = "region's" if q == REGION_Q else "venue's frozen"
    return [{"query": q, "route": route,
             "for": f"the {what} trading currency and scale for the Money it answers or accepts "
                    f"(naming-and-style 5.1, ADR-0018) {R10_TAG}"}]


_FR = None


def fact_routes(text: str, reader: str, root: Path = None) -> list:
    """(e) ADR-0055 rule 2, CHG-RTE-001, CHG-R10GEN-001: the read routes a generated operation's own words call for,
    each fact another module owns asked of its owner's query (tools/fix-read-routes.py's plan, on the new text alone).
    A fact with no owner query, or an Identity read above the foundation tier, is left to check-cross-module-reads
    and fix-read-routes, which declare the query or hold it for the lead."""
    import importlib.util
    import sys as _sys
    global _FR
    root = root or Path(__file__).resolve().parents[1]

    def load(name, path):
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    if _FR is None:
        _sys.path.insert(0, str(root / "tools"))
        import audit_guard as g
        xr = load("xr_gen", root / "tools" / "check-cross-module-reads.py")
        fr = load("fr_gen", root / "tools" / "fix-read-routes.py")
        services = (g.load_json(root / "handoff" / "service-decomposition.json", {}) or {}).get("services") or {}
        tables = set((g.load_json(root / "handoff" / "schema-reference.json", {}) or {}).get("cols") or {})
        by, names = g.schemas()
        _FR = {"xr": xr, "fr": fr, "services": services, "tables": tables, "by": by, "names": names,
               "persist": xr.persisted(by, tables), "queries": xr.declared_queries(),
               "owner_of_schema": {sc: s for s, v in services.items() for sc in v.get("schemas") or []},
               "svc_of_contract": {c: s for s, v in services.items() for c in v.get("contracts") or []}}
    c = _FR
    named = c["xr"].facts_named(text, reader, c["owner_of_schema"], c["tables"], c["persist"], c["names"],
                                c["svc_of_contract"])
    rows = [("generated", reader, t, c["owner_of_schema"].get(t.split(".", 1)[0]), hits[0][0], hits[0][1])
            for t, hits in sorted(named.items())]
    ctx = {k: c[k] for k in ("services", "queries", "svc_of_contract", "persist", "by")}
    plan, new_q, _held, _facts = c["fr"].plan_routes(rows, ctx)
    return [{"query": q, "route": r, "for": w} for q, r, w in plan.get("generated", []) if q not in new_q]


def declared_io(op_ids, ops: dict, schemas: dict) -> tuple:
    """(d) (answered, sent): the schema names a screen's declared operations return (element types, and the schemas
    they reach one level down) and take as a request body."""
    answered, sent = set(), set()
    for oid in op_ids or ():
        entry = ops.get(oid) or {}
        op = entry.get("op") if isinstance(entry.get("op"), dict) else entry
        for n in response_schemas(op or {}):
            answered.add(n)
            answered |= set(REF.findall(json.dumps((schemas or {}).get(n) or {}, default=str)))
        body = set(REF.findall(json.dumps((op or {}).get("requestBody") or {}, default=str)))
        for n in list(body):
            body |= set(REF.findall(json.dumps((schemas or {}).get(n) or {}, default=str)))
        sent |= body
    return answered, sent


def unsourced_bindings(components, answered: set, sent: set) -> list:
    """(d) CHG-R10GEN-003 (ADAM CR-187, CR-220, CR-221, CR-233): the components a generated screen binds to a schema
    none of its declared operations answers or sends. `bindsTo` is `Schema` or `Schema.field`."""
    out = []
    for c in components or ():
        b = str((c or {}).get("bindsTo") or "")
        if b and b.split(".", 1)[0] not in (answered | sent):
            out.append(c)
    return out


def drop_unsourced(regions, overlays, answered: set, sent: set, mine=None) -> int:
    """(d) Unbinds, in place, every generated component bound to a schema the screen's operations neither answer nor
    send, with a note saying so, so the screen never shows a value it has no source for. `mine`: the provenance
    prefixes of the generator's own components; one another source wrote is not this generator's to change.
    Returns how many."""
    n = 0
    comps = [c for r in (regions or []) for c in ((r or {}).get("components") or [])] + list(overlays or [])
    for c in comps:
        if mine and not str((c or {}).get("provenance") or "").startswith(tuple(mine)):
            continue
        stack = [c] + list((c or {}).get("components") or []) + list((c or {}).get("fields") or [])
        for x in unsourced_bindings(stack, answered, sent):
            b = x.pop("bindsTo")
            x["notes"] = ((x.get("notes") or "") + f" Unbound: no operation the screen declares answers or sends "
                          f"`{b}` {R10_TAG}.").strip()
            n += 1
    return n
