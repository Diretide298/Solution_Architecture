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

Kernel tables every deployable reads directly (`platform.scope`, `platform.idempotency_record`; ADAM CR-002) are not
cross-module reads. The reads already in the lineage on 14 October are baselined in handoff/audit-baseline.json; a
read by an operation the r6 batches fix (MUST_FIX) can never be baselined.

    python tools/check-cross-module-reads.py [--all] [--update-baseline]
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
        covered = set()
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
            if owner:
                covered.add(owner)
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
            if owner in covered:
                continue
            guard.add("XR-UNCOVERED", f"{o}:{t}", f"{o} ({reader}, {rdep}) reads {t}, which {owner} "
                      f"({dep_of.get(owner)}) owns, raw: ask a declared query (x-ticvai-read-via) or, within one "
                      f"deployable and for bulk data, read {schema}.{short}_for_{slug(reader)}", strict=strict)
            if reader in FOUNDATION_STRICT and tier_of.get(owner) != "foundation":
                guard.add("XR-FOUNDATION", f"{o}:{t}", f"{o} ({reader}, foundation) reads {t} of {owner} "
                          f"({tier_of.get(owner)}): Identity reads nothing above it but a projection", strict=strict)
    # XR-LINEAGE
    for o in sorted(set(ops) | {o for o, e in lin.items() if e.get("readVia")}):
        want = sorted(({k: str(r[k]) for k in ("query", "route", "for") if r.get(k)}
                       for r in (ops.get(o) or {}).get("x-ticvai-read-via") or [] if isinstance(r, dict)
                       and r.get("query")), key=lambda r: (r["query"], r.get("for", "")))
        if o in lin and (lin[o].get("readVia") or []) != want:
            guard.add("XR-LINEAGE", o, f"{o}: the lineage's readVia differs from the contract's x-ticvai-read-via "
                      "(python tools/derive-lineage.py --apply)")
    guard.note(f"{n_cross} cross-module table read(s) in the lineage; {len(queries)} declared quer(ies)")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
