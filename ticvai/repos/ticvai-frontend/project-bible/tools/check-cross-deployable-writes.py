#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every write into another deployable's schema takes a route the database will allow (ADAM CR-002, CHG-R6-020).

**DB-ROLES gives each deployable's PostgreSQL role DML only on the schemas its own modules own** (ADR-0055: five
units, `commerce`, `access`, `operations`, `workers` and `ticvai-ai`; the owners in
`handoff/service-decomposition.json`). On 12 October 2026 the backend developer raised ADAM CR-002 on DB-ROLES:
`handoff/api-data-lineage.json` still recorded 81 writes by 72 operations into tables another deployable owns,
as plain SQL writes, and PostgreSQL refuses every one of them. Chinmay decided option A, which ADR-0055 rule 4
already says: such a write travels **by event** (ADR-0057, `events/`) that the owning module consumes and
performs, or **by a call to the owner's published operation**. Within one deployable rule 3 stands: a module
calls the owner's in-process API.

The route is stated on the operation in its contract, as `x-ticvai-write-via` (one `{table, event}` or
`{table, operation}` per routed table), and `tools/derive-lineage.py` copies it into the lineage as `writeVia`.
The kernel tables every host needs, and the writes that cannot route yet, are in
`docs/active/cross-deployable-writes.yaml`.

    X-KERNEL     the kernel grants are exactly platform.outbox INSERT, platform.scope SELECT,
                 platform.audit_record INSERT, platform.idempotency_record SELECT/INSERT/UPDATE and
                 platform.outbox_sequence SELECT/INSERT/UPDATE (CR-166)
    X-UNROUTED   a write into another deployable's table (a kernel table only where the kernel grants a write)
                 has neither a route nor an exception
    X-EVENT      an event route names an event that is not catalogued, that the operation does not emit
                 (`emittedBy`, `x-ticvai-emits`), or that no consumer of the table's owning module `writes`
    X-OPERATION  an operation route names an operation that does not exist or that the table's owner does not serve
    X-STALE      a route or an exception for a write that is not cross-deployable, or a write both routed and
                 excepted, or an exception entry missing a field
    X-EXPIRED    an exception whose removal release is already tagged
    X-LINEAGE    the lineage's `writeVia` differs from the contract's `x-ticvai-write-via` (run derive-lineage
                 --apply)
    X-DOC        handoff/cross-deployable-writes.md is not what this check would write (run with --write)

    python tools/check-cross-deployable-writes.py           # check
    python tools/check-cross-deployable-writes.py --write   # (re)write handoff/cross-deployable-writes.md, then check
"""
from __future__ import annotations

import collections
import glob
import io
import json
import os
import re
import subprocess
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINEAGE = os.path.join(ROOT, "handoff", "api-data-lineage.json")
DECOMP = os.path.join(ROOT, "handoff", "service-decomposition.json")
AUTHORED = os.path.join(ROOT, "docs", "active", "cross-deployable-writes.yaml")
DOC = os.path.join(ROOT, "handoff", "cross-deployable-writes.md")

# Chinmay, 12 October 2026 (ADAM CR-002): the only tables every deployable's role is granted directly.
KERNEL = {
    "platform.outbox": ("INSERT",),
    "platform.scope": ("SELECT",),
    "platform.audit_record": ("INSERT",),
    "platform.idempotency_record": ("SELECT", "INSERT", "UPDATE"),
    # ADAM CR-166, 18 October 2026 (CHG-CRA-005): every host allocates its outbox sequence from the counter in the
    # transaction that writes the outbox row, so access and operations allocate like commerce.
    "platform.outbox_sequence": ("SELECT", "INSERT", "UPDATE"),
}
WRITE_PRIVS = {"INSERT", "UPDATE", "DELETE"}
EXC_FIELDS = ("id", "operation", "table", "kind", "reason", "added", "removal_release")
EXC_KINDS = ("misplaced-table", "owner-operation-missing")


def yl(p):
    return yaml.load(io.open(p, encoding="utf-8"), Loader=yaml.CSafeLoader) or {}


def contract_routes() -> dict:
    """operationId -> [{table, event|operation}] from `x-ticvai-write-via` in the contracts."""
    out = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "contracts", "*", "*.yaml"))):
        for item in (yl(f).get("paths") or {}).values():
            for op in (item or {}).values():
                if isinstance(op, dict) and op.get("operationId") and op.get("x-ticvai-write-via"):
                    out[op["operationId"]] = sorted(
                        ({k: str(w[k]) for k in ("table", "event", "operation") if w.get(k)}
                         for w in op["x-ticvai-write-via"] if isinstance(w, dict)), key=lambda w: w.get("table", ""))
    return out


def contract_emits() -> dict:
    out = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "contracts", "*", "*.yaml"))):
        for item in (yl(f).get("paths") or {}).values():
            for op in (item or {}).values():
                if isinstance(op, dict) and op.get("operationId") and op.get("x-ticvai-emits"):
                    e = op["x-ticvai-emits"]
                    out[op["operationId"]] = {str(x) for x in (e if isinstance(e, list) else [e])}
    return out


def events() -> dict:
    out = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "events", "*.yaml"))):
        if os.path.basename(f).startswith("_"):
            continue
        e = yl(f)
        if e.get("name"):
            out[e["name"]] = e
    return out


def released_tags() -> set:
    try:
        r = subprocess.run(["git", "tag", "--list", "r*"], cwd=ROOT, capture_output=True, text=True, timeout=30)
        return {t.strip() for t in r.stdout.split() if re.match(r"^r\d+$", t.strip())}
    except Exception:  # noqa: BLE001
        return set()


def analyse():
    lin = json.load(io.open(LINEAGE, encoding="utf-8"))
    dec = json.load(io.open(DECOMP, encoding="utf-8"))
    auth = yl(AUTHORED)
    services = dec.get("services") or {}
    dep_of = {s: v.get("deployable") for s, v in services.items()}
    owner_of_schema = {sc: s for s, v in services.items() for sc in v.get("schemas") or []}
    # A consumer's `context` is a contract name (`platform-ops`) or a schema name (`marketing`, `ledger`).
    svc_of_context = {c: s for s, v in services.items() for c in v.get("contracts") or []}
    for sc, s in owner_of_schema.items():
        svc_of_context.setdefault(sc, s)
    bad = []

    # X-KERNEL
    kern = {}
    for k in auth.get("kernel") or []:
        kern[str(k.get("table"))] = tuple(sorted(str(p).upper() for p in k.get("privileges") or []))
    want = {t: tuple(sorted(p)) for t, p in KERNEL.items()}
    for t in sorted(set(kern) | set(want)):
        if t not in want:
            bad.append(("X-KERNEL", t, "is granted to every deployable in the kernel list, and only the five agreed "
                                       "tables may be (ADAM CR-002)"))
        elif t not in kern:
            bad.append(("X-KERNEL", t, "is missing from the kernel list"))
        elif kern[t] != want[t]:
            bad.append(("X-KERNEL", t, "is granted %s, and the agreed grant is %s" % ("/".join(kern[t]),
                                                                                    "/".join(want[t]))))
    kernel_writable = {t for t, p in KERNEL.items() if set(p) & WRITE_PRIVS}

    # Every cross-deployable write in the lineage.
    cross = {}
    for o, e in sorted(lin.items()):
        wdep = dep_of.get(e.get("service"))
        for t in e.get("writes") or []:
            if ":" in t or "." not in t or t in kernel_writable:
                continue
            osvc = owner_of_schema.get(t.split(".", 1)[0])
            if not osvc or dep_of.get(osvc) == wdep:
                continue
            cross[(o, t)] = {"operation": o, "writer": e.get("service"), "writer_dep": wdep, "table": t,
                             "owner": osvc, "owner_dep": dep_of.get(osvc), "contract": e.get("contract")}

    routes = contract_routes()
    route_of = {(o, w["table"]): w for o, ws in routes.items() for w in ws}
    exc = {}
    for x in auth.get("exceptions") or []:
        miss = [f for f in EXC_FIELDS if not x.get(f)]
        if miss:
            bad.append(("X-STALE", str(x.get("id")), "an exception without %s" % ", ".join(miss)))
            continue
        if x.get("kind") not in EXC_KINDS:
            bad.append(("X-STALE", x["id"], "kind is one of %s" % ", ".join(EXC_KINDS)))
        if not re.match(r"^r\d+$", str(x.get("removal_release"))):
            bad.append(("X-STALE", x["id"], "removal_release is a release tag, r<N>"))
        exc[(str(x["operation"]), str(x["table"]))] = x

    evs = events()
    emits = contract_emits()
    for (o, t), w in sorted(route_of.items()):
        if (o, t) not in cross:
            bad.append(("X-STALE", o, "routes %s, which it does not write into another deployable" % t))
            continue
        c = cross[(o, t)]
        if (o, t) in exc:
            bad.append(("X-STALE", o, "%s is both routed and on the exception list (%s)" % (t, exc[(o, t)]["id"])))
        if w.get("event") and w.get("operation"):
            bad.append(("X-STALE", o, "routes %s both by event and by operation; name one" % t))
        if w.get("event"):
            ev = evs.get(w["event"])
            if not ev:
                bad.append(("X-EVENT", o, "routes %s by %s, which is not in the event catalogue" % (t, w["event"])))
                continue
            by = {str(x).split(".")[-1] for x in ev.get("emittedBy") or []}
            if o not in by and w["event"] not in emits.get(o, set()):
                bad.append(("X-EVENT", o, "routes %s by %s, which it does not emit (emittedBy, x-ticvai-emits)"
                            % (t, w["event"])))
            ok = [k for k in ev.get("consumers") or []
                  if svc_of_context.get(str(k.get("context"))) == c["owner"] and t in (k.get("writes") or [])]
            if not ok:
                bad.append(("X-EVENT", o, "routes %s by %s, and no consumer of %s (the owner) writes it"
                            % (t, w["event"], c["owner"])))
        elif w.get("operation"):
            tgt = lin.get(w["operation"])
            if not tgt:
                bad.append(("X-OPERATION", o, "routes %s by %s, which no contract declares" % (t, w["operation"])))
            elif tgt.get("service") != c["owner"]:
                bad.append(("X-OPERATION", o, "routes %s by %s, which %s serves, not the owner %s"
                            % (t, w["operation"], tgt.get("service"), c["owner"])))
        else:
            bad.append(("X-STALE", o, "routes %s by neither an event nor an operation" % t))
    for (o, t), x in sorted(exc.items()):
        if (o, t) not in cross:
            bad.append(("X-STALE", x["id"], "excepts %s writing %s, which is not a cross-deployable write" % (o, t)))
    tags = released_tags()
    for (o, t), x in sorted(exc.items()):
        if str(x.get("removal_release")) in tags:
            bad.append(("X-EXPIRED", x["id"], "%s writing %s was to be removed by %s, which is tagged"
                        % (o, t, x["removal_release"])))
    for (o, t), c in sorted(cross.items()):
        if (o, t) not in route_of and (o, t) not in exc:
            bad.append(("X-UNROUTED", o, "%s (%s) writes %s, which %s owns in %s, with its own SQL; name a route "
                        "(x-ticvai-write-via: event or operation) or an exception" % (c["writer"], c["writer_dep"], t,
                                                                                        c["owner"], c["owner_dep"])))
    # X-LINEAGE
    for o in sorted(set(routes) | {o for o, e in lin.items() if e.get("writeVia")}):
        if o in lin and (lin[o].get("writeVia") or []) != routes.get(o, []):
            bad.append(("X-LINEAGE", o, "the lineage's writeVia differs from the contract's x-ticvai-write-via "
                                        "(python tools/derive-lineage.py --apply)"))
    return cross, route_of, exc, auth, bad


def render(cross, route_of, exc, auth) -> str:
    n_ev = sum(1 for k in cross if k in route_of and route_of[k].get("event"))
    n_op = sum(1 for k in cross if k in route_of and route_of[k].get("operation"))
    n_ex = sum(1 for k in cross if k in exc)
    ops = len({o for o, _ in cross})
    L = ["# Cross-deployable writes: how each one reaches its owner", "",
         "**Generated by `python tools/check-cross-deployable-writes.py --write`; do not edit by hand.** The routes "
         "are `x-ticvai-write-via` on each operation in `contracts/` (copied into `handoff/api-data-lineage.json` as "
         "`writeVia`); the kernel grants and the exceptions are `docs/active/cross-deployable-writes.yaml`. ADAM "
         "CR-002 on DB-ROLES, decided by Chinmay on 12 October 2026 (CHG-R6-020).", "",
         "**Why.** DB-ROLES gives each deployable's PostgreSQL role DML only on the schemas its own modules own "
         "(ADR-0055; `handoff/service-decomposition.json`). A write into another deployable's schema made with the "
         "caller's own SQL is refused at runtime. ADR-0055 rule 4: across deployables a write travels by event "
         "(ADR-0057) or by the owner's published HTTP operation. Within one deployable, rule 3 stands: call the "
         "owner module's in-process API inside your transaction.", "",
         "## How to build each route", "",
         "- **event `<name>`**: write the event to `platform.outbox` in the same transaction as your own change "
         "(ADR-0033). The owning module's consumer (in the `workers` host, its idempotency key in the event file "
         "under `events/`) performs the write; the consumer that does it lists the table under `writes`. Your "
         "operation does not touch the table.",
         "- **operation `<operationId>`**: call the owner's published operation over HTTP with an "
         "`Idempotency-Key` derived from your own record's id, so a retry is safe. The owner's write is in the "
         "owner's transaction, not yours.",
         "- **exception `XDW-nnn`**: the write cannot route yet. DB-ROLES grants the writer's role DML on that one "
         "table until the removal release; the reason says what removes it.", "",
         "## Summary", "",
         "| | writes |", "|---|---:|",
         "| Cross-deployable writes in the lineage (%d operations) | %d |" % (ops, len(cross)),
         "| by event | %d |" % n_ev, "| by the owner's operation | %d |" % n_op, "| on the exception list | %d |" % n_ex,
         "", "## The kernel tables every deployable is granted directly", "",
         "| Table | Privileges | Why |", "|---|---|---|"]
    for k in auth.get("kernel") or []:
        L.append("| `%s` | %s | %s |" % (k.get("table"), ", ".join(k.get("privileges") or []),
                                         " ".join(str(k.get("why") or "").split())))
    L += ["", "Every other table in another deployable's schema is reached by one of the routes below.", "",
          "## Every cross-deployable write", "",
          "Sorted by the owning deployable, then the table.", "",
          "| Operation | Writer (deployable / module) | Table | Owner (deployable / module) | Route |",
          "|---|---|---|---|---|"]
    for (o, t), c in sorted(cross.items(), key=lambda kv: (kv[1]["owner_dep"] or "", kv[0][1], kv[0][0])):
        w = route_of.get((o, t))
        if w and w.get("event"):
            r = "event `%s`" % w["event"]
        elif w and w.get("operation"):
            r = "operation `%s`" % w["operation"]
        elif (o, t) in exc:
            r = "exception %s (until %s)" % (exc[(o, t)]["id"], exc[(o, t)]["removal_release"])
        else:
            r = "**unrouted**"
        L.append("| `%s` | %s / %s | `%s` | %s / %s | %s |" % (o, c["writer_dep"], c["writer"], t, c["owner_dep"],
                                                             c["owner"], r))
    L += ["", "## The exceptions", "",
          "| Id | Operation | Table | Kind | Added | Removed by | Reason |", "|---|---|---|---|---|---|---|"]
    for x in sorted(exc.values(), key=lambda x: str(x["id"])):
        L.append("| %s | `%s` | `%s` | %s | %s | %s | %s |" % (x["id"], x["operation"], x["table"], x["kind"],
                                                             x["added"], x["removal_release"],
                                                             " ".join(str(x["reason"]).split())))
    return "\n".join(L) + "\n"


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
    cross, route_of, exc, auth, bad = analyse()
    text = render(cross, route_of, exc, auth)
    if "--write" in sys.argv:
        io.open(DOC, "w", encoding="utf-8", newline="\n").write(text)
        print("  wrote handoff/cross-deployable-writes.md")
    cur = io.open(DOC, encoding="utf-8").read() if os.path.exists(DOC) else ""
    if cur != text:
        bad.append(("X-DOC", "handoff/cross-deployable-writes.md",
                    "is not what the routes say (python tools/check-cross-deployable-writes.py --write)"))
    n_ev = sum(1 for k in cross if k in route_of and route_of[k].get("event"))
    n_op = sum(1 for k in cross if k in route_of and route_of[k].get("operation"))
    n_ex = sum(1 for k in cross if k in exc)
    print("  %d cross-deployable write(s) by %d operation(s): %d by event, %d by the owner's operation, "
          "%d on the exception list" % (len(cross), len({o for o, _ in cross}), n_ev, n_op, n_ex))
    by = collections.Counter(r for r, _, _ in bad)
    for r, o, d in bad[:80]:
        print("  %-11s %-34s %s" % (r, o, d))
    if bad:
        print("FAIL %d finding(s): %s" % (len(bad), ", ".join("%s %d" % kv for kv in sorted(by.items()))))
        return 1
    print("ok: every cross-deployable write is routed by event or by the owner's operation, or is a dated "
          "exception; the kernel grants are the five agreed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
