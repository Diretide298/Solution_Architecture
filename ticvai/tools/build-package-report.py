#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The whole package measured in one pass, for the report that goes to the build team.

**Asked for on 21 September, Chinmay: "reckon we have everything to start the build -- build an
in-depth report. Coverage, connections, apis, screens, services, tasks, operations covered,
linking, the complete thing."**

**Every other report in this package answers one question.** `status.json` carries the headline
metrics, `service-decomposition.json` the seventeen services, `traceability.json` the requirement
walk, `screen-index.json` what each screen calls. A person deciding whether to start building has
to open five files and hold the joins in their head. **This does the joins.**

## The one thing it measures that nothing else does: the chain

A screen is buildable when the whole chain under it resolves --

    requirement -> operation -> screen -> service -> table -> store

**Each link is counted separately, because they fail separately.** An operation can have a screen
and no lineage; a table can have a relationship and no operation that reaches it. A single
"coverage" percentage hides exactly the link that is broken, so there is no single percentage
here.

## And the one number a backend team actually needs: edges that cross a service

`relationship-graph.json` has 1,351 declared references. **A reference inside one service is a
foreign key; a reference across two is a distributed join somebody has to design.** The split is
the cost of the service decomposition, stated as a number rather than as a diagram.

**Counts come from the derived files, never from prose.** Every figure here is read from a file
another tool wrote in the same refresh, which is why this runs last.

    python3 tools/build-package-report.py [--apply]
"""
import argparse
import collections
import io
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = os.path.join(ROOT, "handoff")
MD = os.path.join(H, "package-report.md")
JS = os.path.join(H, "package-report.json")


def load(name):
    p = os.path.join(H, name)
    if not os.path.exists(p):
        return None
    return json.load(io.open(p, encoding="utf-8"))


def pct(a, b):
    return 0 if not b else int(round(100.0 * a / b))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    status = load("status.json")
    lineage = load("api-data-lineage.json") or {}
    screens = load("screen-index.json") or {}
    svc = load("service-decomposition.json") or {"services": {}}
    graph = load("relationship-graph.json") or {"rels": []}
    trace = load("traceability.json") or {"rows": []}
    schema = load("schema-reference.json") or {}
    caps = load("module-capabilities.json") or {}

    if status is None:
        print("  !! handoff/status.json is missing - run tools/build-status.py first")
        return 1

    c = status["counts"]
    out = {"generated": status["generated"],
           "note": ("The package measured in one pass. Derived by tools/build-package-report.py "
                    "from the files the refresh writes -- never from prose."),
           "counts": c}

    # ---- the chain, link by link -------------------------------------------------------------
    ops = set(lineage)
    on_screen = set()
    for s in screens.values():
        on_screen |= set(s.get("operations") or [])
    with_reads = {o for o, d in lineage.items() if d.get("reads") or d.get("writes")}
    with_perm = {o for o, d in lineage.items() if d.get("perm")}
    with_service = {o for o, d in lineage.items() if d.get("service")}
    screens_with_ops = {k for k, s in screens.items() if s.get("operations")}

    # A table is *reached* when some operation names it in reads or writes. This is the join the
    # DDL cannot make for itself: a table nothing reaches is either a missing operation or a
    # table that should not exist, and the audit that says which is a judgement (audit-unwired).
    reached = set()
    for d in lineage.values():
        reached |= set(d.get("reads") or [])
        reached |= set(d.get("writes") or [])
    reached = {t for t in reached if "." in t and not t.startswith(("cache:", "vault:"))}

    # **`cols` is the table set, not `storage`.** `storage` carries five more keys than any
    # table exists for -- the pseudo-rows a store declaration needs -- and a denominator that is
    # five too big makes every coverage figure below it quietly wrong.
    tables = {k for k in (schema.get("cols") or {})
              if "." in k and not k.startswith(("cache:", "vault:"))}

    edges = graph.get("rels") or []
    in_edge = set()
    for e in edges:
        in_edge.add(e.get("frm"))
        in_edge.add(e.get("to"))

    chain = [
        ("Requirements in scope", len([r for r in trace["rows"]
                                       if r.get("verdict") != "PARKED"]),
         len(trace["rows"]), "matrix rows, less the ones deliberately parked"),
        ("Requirements contracted", len([r for r in trace["rows"]
                                         if r.get("verdict") == "CONTRACTED"]),
         len([r for r in trace["rows"] if r.get("verdict") != "PARKED"]),
         "an operation or schema field demonstrably serves it"),
        ("Operations declaring a service", len(with_service), len(ops),
         "the operation is owned by one of the seventeen deployables"),
        ("Operations declaring a permission", len(with_perm), len(ops),
         "the checklist a grant screen renders is built from these"),
        ("Operations with resolved lineage", len(with_reads), len(ops),
         "names the tables it reads and writes -- the join the DDL cannot make itself"),
        ("Operations reaching a screen", len(ops & on_screen), len(ops),
         "sync, webhook and job operations legitimately have none"),
        ("Screens naming an operation", len(screens_with_ops), len(screens),
         "the rest are static, navigation shells or workshop-blocked"),
        ("Tables reached by an operation", len(reached & tables), len(tables),
         "a table nothing reaches is a missing operation or a table that should not exist"),
        ("Tables carrying a relationship", len(in_edge & tables), len(tables),
         "either end of a declared reference"),
    ]
    out["chain"] = [{"link": n, "done": d, "total": t, "percent": pct(d, t), "note": w}
                    for n, d, t, w in chain]

    print("  the chain")
    for n, d, t, w in chain:
        print("    %-34s %6d / %-6d %3d%%" % (n, d, t, pct(d, t)))

    # ---- what crosses a service boundary -----------------------------------------------------
    # **The cost of the decomposition, as a number.** A reference inside one service is a foreign
    # key the database enforces. A reference across two is a call, a cache or an eventual read
    # that somebody has to design, and it is the whole reason the boundaries were drawn on the
    # data first (ADR-0011).
    schema_of = {}
    for name, s in svc["services"].items():
        for sc in s.get("schemas") or []:
            schema_of[sc] = name

    def owner(t):
        return schema_of.get((t or "").split(".", 1)[0])

    inside = collections.Counter()
    across = collections.Counter()
    target = collections.Counter()
    unowned = 0
    for e in edges:
        f, t = owner(e.get("frm")), owner(e.get("to"))
        if not f or not t:
            unowned += 1
        elif f == t:
            inside[f] += 1
        else:
            across[(f, t)] += 1
            target[e.get("to")] += 1
    n_across = sum(across.values())
    # **The crossings concentrate rather than spread, which is the finding.** If they were spread
    # evenly across 627 tables the decomposition would be wrong. They are not: the top three
    # targets are the principal, the scope tree and the PII subject -- the two foundation
    # services, which exist precisely to be read by everything (ADR-0011, ADR-0023).
    top_targets = target.most_common(10)
    concentrated = sum(n for _, n in target.most_common(3))
    out["boundaries"] = {
        "edgesTotal": len(edges),
        "insideOneService": sum(inside.values()),
        "crossingTwoServices": n_across,
        "endpointNotOwned": unowned,
        "note": ("A reference inside one service is a foreign key the database enforces. A "
                 "reference across two is a distributed read somebody has to design."),
        "heaviest": [{"from": f, "to": t, "edges": n}
                     for (f, t), n in across.most_common(12)],
        "topTargets": [{"table": t, "edges": n} for t, n in top_targets],
        "inTopThreeTargets": concentrated,
    }
    print("\n  boundaries: %d edge(s) -- %d inside one service, %d crossing two, %d unowned end"
          % (len(edges), sum(inside.values()), n_across, unowned))

    # ---- per service -------------------------------------------------------------------------
    rows = []
    for name, s in sorted(svc["services"].items(),
                          key=lambda kv: -(kv[1].get("operations") or 0)):
        sops = {o for o, d in lineage.items() if d.get("service") == name}
        rows.append({
            "service": name,
            "tier": s.get("tier"),
            "contracts": len(s.get("contracts") or []),
            "schemas": len(s.get("schemas") or []),
            "operations": s.get("operations"),
            "tables": s.get("tables"),
            "screens": s.get("screens"),
            "operationsOnAScreen": len(sops & on_screen),
            "edgesOut": sum(n for (f, _), n in across.items() if f == name),
            "edgesIn": sum(n for (_, t), n in across.items() if t == name),
        })
    out["services"] = rows

    # ---- per contract ------------------------------------------------------------------------
    by_contract = collections.defaultdict(list)
    for o, d in lineage.items():
        by_contract[d.get("contract") or "?"].append(o)
    crows = []
    for name in sorted(by_contract):
        o = set(by_contract[name])
        crows.append({
            "contract": name,
            "operations": len(o),
            "onAScreen": len(o & on_screen),
            "withLineage": len(o & with_reads),
            "withPermission": len(o & with_perm),
            "percentOnAScreen": pct(len(o & on_screen), len(o)),
        })
    out["contracts"] = crows

    # ---- per platform ------------------------------------------------------------------------
    prows = []
    for p in status.get("platformBreakdown") or []:
        mine = {k: s for k, s in screens.items() if s.get("platform") == p["code"]}
        withops = {k for k, s in mine.items() if s.get("operations")}
        ops_here = set()
        for s in mine.values():
            ops_here |= set(s.get("operations") or [])
        prows.append(dict(p, screensWithOperations=len(withops),
                          distinctOperations=len(ops_here),
                          percentWithOperations=pct(len(withops), len(mine) or 1)))
    out["platforms"] = prows

    # ---- what is still open ------------------------------------------------------------------
    verdicts = collections.Counter(r.get("verdict") for r in trace["rows"])
    caps_mod = (caps.get("modules") or {})
    open_work = {
        "conflictsOpen": (status.get("conflicts") or {}).get("open"),
        "conflictsBlocking": (status.get("conflicts") or {}).get("blocking"),
        "requirementsGapContract": verdicts.get("GAP_CONTRACT", 0),
        "requirementsGapDecision": verdicts.get("GAP_DECISION", 0),
        "requirementsPartial": verdicts.get("CONTRACTED_PARTIAL", 0),
        "operationsNoScreen": len(ops - on_screen),
        "screensNoOperation": len(screens) - len(screens_with_ops),
        "operationsNoLineage": len(ops - with_reads),
        "tablesNotReached": len(tables - reached),
        "permissionsWithoutLabel": (caps.get("unlabelled") or {}).get("count"),
        "capabilityPairs": sum(m.get("capabilityCount") or 0 for m in caps_mod.values()),
        "modulesWithCapabilities": len(caps_mod),
    }
    out["open"] = open_work
    print("\n  open")
    for k, v in open_work.items():
        print("    %-30s %s" % (k, v))

    # ---- markdown ----------------------------------------------------------------------------
    L = []
    w = L.append
    w("# Package report")
    w("")
    w("**Generated %s by `tools/build-package-report.py`.** Every figure is read from a file "
      "another tool wrote in the same refresh." % status["generated"])
    w("")
    w("## Scale")
    w("")
    w("| | |")
    w("|---|---|")
    for k in ("contracts", "operations", "screens", "platforms", "apps", "tables", "stores",
              "foreignKeys", "indexes", "relationships", "flows", "boards", "adrs"):
        if k in c:
            w("| %s | %s |" % (k[0].upper() + re.sub(r"([A-Z])", r" \1", k[1:]), c[k]))
    w("| Services | %d |" % len(svc["services"]))
    w("")
    w("## The chain")
    w("")
    w("**A screen is buildable when the whole chain under it resolves.** Each link is counted "
      "separately, because they fail separately.")
    w("")
    w("| Link | | | |")
    w("|---|---:|---:|---|")
    for n, d, t, note in chain:
        w("| %s | %d / %d | %d%% | %s |" % (n, d, t, pct(d, t), note))
    w("")
    w("## What crosses a service boundary")
    w("")
    w("**%d declared references. %d stay inside one service; %d cross two.**" %
      (len(edges), sum(inside.values()), n_across))
    w("")
    w("**%d of the %d crossings land on three tables** -- `%s`. The crossings concentrate on the "
      "foundation tier rather than spreading, which is what the tier is for." %
      (concentrated, n_across, "`, `".join(t for t, _ in top_targets[:3])))
    w("")
    w("| From | To | Edges |")
    w("|---|---|---:|")
    for (f, t), n in across.most_common(12):
        w("| %s | %s | %d |" % (f, t, n))
    w("")
    w("| Most-referenced table across a boundary | Edges |")
    w("|---|---:|")
    for t, n in top_targets:
        w("| `%s` | %d |" % (t, n))
    w("")
    w("## Services")
    w("")
    w("| Service | Tier | Ops | On a screen | Tables | Screens | Out | In |")
    w("|---|---|---:|---:|---:|---:|---:|---:|")
    for r in rows:
        w("| %s | %s | %s | %s | %s | %s | %s | %s |" %
          (r["service"], r["tier"], r["operations"], r["operationsOnAScreen"], r["tables"],
           r["screens"], r["edgesOut"], r["edgesIn"]))
    w("")
    w("## Contracts")
    w("")
    w("| Contract | Ops | On a screen | With lineage | With a permission |")
    w("|---|---:|---:|---:|---:|")
    for r in crows:
        w("| %s | %d | %d | %d | %d |" % (r["contract"], r["operations"], r["onAScreen"],
                                          r["withLineage"], r["withPermission"]))
    w("")
    w("## Platforms")
    w("")
    w("| Code | Platform | App | Screens | Naming an operation | Distinct operations |")
    w("|---|---|---|---:|---:|---:|")
    for r in prows:
        w("| %s | %s | %s | %d | %d | %d |" % (r["code"], r["name"], r["app"], r["screens"],
                                               r["screensWithOperations"],
                                               r["distinctOperations"]))
    w("")
    w("## Open")
    w("")
    w("| | |")
    w("|---|---:|")
    for k, v in open_work.items():
        w("| %s | %s |" % (k[0].upper() + re.sub(r"([A-Z])", r" \1", k[1:]), v))
    w("")
    md = "\n".join(L) + "\n"

    if not a.apply:
        print("\n  nothing written - pass --apply")
        return 0
    io.open(MD, "w", encoding="utf-8", newline="\n").write(md)
    io.open(JS, "w", encoding="utf-8", newline="\n").write(
        json.dumps(out, indent=1, ensure_ascii=False))
    print("\n  -> handoff/package-report.md")
    print("  -> handoff/package-report.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
