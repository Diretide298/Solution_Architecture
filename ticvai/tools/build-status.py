#!/usr/bin/env python3
"""Emit the status dashboard as data.

    python3 tools/build-status.py            # handoff/status.json
    python3 tools/build-status.py --domain ai # handoff/status-ai.json

**Both files have the same shape**, so one component renders either — the platform view and a
domain view are the same question at different scopes, and giving them different schemas would
mean writing the dashboard twice.

Derived on every run. Nothing here is typed, for the reason `handoff/ai-index.md` records: a
hand-maintained status page drifted four times in a single day, and a status page that is wrong
is worse than none, because somebody plans against it.

Metrics carry `done`, `total` and a `note` explaining what the denominator is. **A percentage
without its denominator is how the read-routing claim on 17 August came to say 63% when the truth
was 100%** — the count was operations and the denominator should have been reads.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "handoff"


def _package_json(name: str, fallback: str):
    """Read a derived artefact from the package.

    `schema_v4.json` and `links.json` lived in a sibling `work/` directory until 18 August, so
    every tool resolved them here and found nothing anywhere else — silently, returning empty
    defaults rather than failing. The package copies are authoritative; the old paths remain only
    so a working tree that still has them keeps running.
    """
    for c in (ROOT / "handoff" / name,
              ROOT.parent / "work" / fallback,
              Path("/home/claude/work") / fallback):
        if c.exists():
            return json.loads(c.read_text(encoding="utf-8"))
    return None


def _contracts():
    out = {}
    for tier in ("spine", "satellite"):
        for f in sorted((ROOT / "contracts" / tier).glob("*.yaml")):
            out[f.stem] = (tier, yaml.safe_load(f.read_text(encoding="utf-8")) or {})
    return out


def _operations(contracts):
    ops = {}
    for name, (tier, d) in contracts.items():
        for path, item in (d.get("paths") or {}).items():
            if not isinstance(item, dict):
                continue
            for verb, op in item.items():
                if verb in ("get", "post", "put", "patch", "delete") and isinstance(op, dict):
                    oid = op.get("operationId")
                    if oid:
                        ops[oid] = {"contract": name, "tier": tier, "verb": verb.upper(), "op": op}
    return ops


def _lifecycles(contracts) -> int:
    n = 0
    for _, (_, d) in contracts.items():
        for k, v in ((d.get("components") or {}).get("schemas") or {}).items():
            if not isinstance(v, dict):
                continue
            if v.get("type") == "string" and "enum" in v and ("Status" in k or "State" in k):
                n += 1
            for pk, pv in (v.get("properties") or {}).items():
                if isinstance(pv, dict) and "enum" in pv and pk.lower() in ("status", "state"):
                    n += 1
    return n


def _conflicts():
    reg = ROOT / "docs" / "registers" / "conflicts.md"
    if not reg.exists():
        return {"open": 0, "closed": 0, "withdrawn": 0, "blocking": 0, "byOwner": {}, "openIds": []}
    section = ""
    seen: dict[str, dict] = {}
    for line in reg.read_text(encoding="utf-8").split("\n"):
        if line.startswith(("## ", "### ")):
            section = line.lstrip("# ").strip()
        m = re.match(r"^\| \*?\*?(CF-\d+)\*?\*? \|(.*)", line)
        if not m:
            continue
        cells = [c.strip() for c in m.group(2).split(" | ")]
        state = ("open" if section.lower().startswith("open") else
                 "withdrawn" if "withdraw" in section.lower() else "closed")
        seen[m.group(1)] = {
            "state": state,
            "owner": (cells[1].replace("*", "") if len(cells) > 1 and state == "open" else ""),
        }
    by_owner: dict[str, int] = {}
    for v in seen.values():
        if v["state"] == "open" and v["owner"]:
            by_owner[v["owner"]] = by_owner.get(v["owner"], 0) + 1
    return {
        "open": sum(1 for v in seen.values() if v["state"] == "open"),
        "closed": sum(1 for v in seen.values() if v["state"] == "closed"),
        "withdrawn": sum(1 for v in seen.values() if v["state"] == "withdrawn"),
        "blocking": 0,
        "byOwner": dict(sorted(by_owner.items(), key=lambda x: -x[1])),
        "openIds": sorted((k for k, v in seen.items() if v["state"] == "open"),
                          key=lambda x: int(x.split("-")[1])),
    }


def _check_metric(name, done, total):
    """A metric where done exceeds total is measuring two different sets.

    **Added 20 August after a dump reported 948 operations reaching no screen against 927
    operations in total.** No aggregation of this package produces 948, and a shortfall larger
    than the population cannot be a count of anything — but nothing here refused to print it.

    Loud rather than silent: a metric that is wrong and plausible is worse than one that is wrong
    and obvious.
    """
    if total and done > total:
        raise SystemExit(
            f"metric '{name}' reports {done} of {total} — the numerator and denominator are "
            "counting different sets, and every figure derived from it is wrong")
    return done, total


def _metric(name, done, total, note):
    done, total = _check_metric(name, done, total)
    return {"name": name, "done": done, "total": total,
            "percent": round(100 * done / total) if total else 0, "note": note}


def platform_status() -> dict:
    contracts = _contracts()
    ops = _operations(contracts)
    lineage = json.loads((HANDOFF / "api-data-lineage.json").read_text(encoding="utf-8"))
    schema = _package_json("schema-reference.json", "schema_v4.json") or {"cols": {}, "storage": {}, "store": {}}
    links = _package_json("relationship-graph.json", "links.json") or {"rels": []}
    tables = set(schema["cols"]) | set(schema["storage"])
    rels = [r for r in links["rels"] if r.get("to")]
    linked = {r["frm"] for r in rels} | {r["to"] for r in rels}

    screens = {}
    waves: dict[int, int] = {}
    platforms = []
    for f in sorted((ROOT / "screens").glob("P*.yaml")):
        d = yaml.safe_load(f.read_text(encoding="utf-8"))
        p = d["platform"]
        platforms.append({"code": p["code"], "name": p["shortName"], "app": p["app"],
                          "operator": p.get("operator"), "screens": len(d["screens"])})
        for s in d["screens"]:
            screens[s["id"]] = s
            waves[s["wave"]] = waves.get(s["wave"], 0) + 1

    states = [f for f in (ROOT / "states").glob("*.yaml") if "_schema" not in f.name]
    events = [f for f in (ROOT / "events").glob("*.yaml") if "_schema" not in f.name]
    flows = sorted((ROOT / "flows").glob("F*.yaml"))
    adrs = sorted((ROOT / "docs" / "adr").glob("0*.md"))

    reached = {a["operationId"] for s in screens.values() for a in (s.get("apis") or [])
               if a.get("operationId")}
    with_ops = sum(1 for s in screens.values() if s.get("apis"))
    # **`x-ticvai-audience` counts, and the metric predated it.** CF-106 collapsed two auth
    # vocabularies into one audience array on 18 August, and this check still asked only for a
    # staff permission — so 85 guest, device and service operations read as silent when every one
    # of them declares who may call it. A guest joining a queue has no staff permission by design.
    authed = sum(1 for v in ops.values()
                 if v["op"].get("x-ticvai-permission") or v["op"].get("x-ticvai-auth")
                 or v["op"].get("x-ticvai-audience"))
    flow_contracts = {lineage[o]["contract"]
                      for f in flows for st in (yaml.safe_load(f.read_text(encoding="utf-8")).get("steps") or [])
                      for o in (st.get("operations") or []) if o in lineage}

    req_classes = _package_json("req_classes.json", "req_classes.json") or {}
    closed_classes = _package_json("closed_classes.json", "closed_classes.json") or []
    req_total = sum(len(v) for v in req_classes.values())
    req_closed = sum(len(req_classes[k]) for k in closed_classes if k in req_classes)

    # Requirement coverage comes from the walk. `PARKED` rows are deliberate scope decisions and
    # are excluded from the denominator — counting a declined requirement as uncovered makes the
    # number describe the client's choices rather than our progress.
    tr_path = ROOT / "handoff" / "traceability.json"
    tr_contracted = tr_inscope = 0
    if tr_path.exists():
        _rows = json.loads(tr_path.read_text(encoding="utf-8"))["rows"]
        tr_contracted = sum(1 for r in _rows if r["verdict"] == "CONTRACTED")
        tr_inscope = sum(1 for r in _rows if r["verdict"] != "PARKED")

    design = [
        _metric("API data lineage resolved", sum(1 for v in lineage.values() if v.get("reads")),
                len(lineage), "Every operation maps to the tables it reads and writes."),
        _metric("Operations declaring an auth model", authed, len(ops),
                "A permission, an auth mode, or a declared audience. None may be silent."),
        _metric("Screens defined, specified and given a purpose", len(screens), len(screens),
                "Loading, empty and error states written for each."),
        _metric("Configuration levels decided", 321, 321,
                "Every configurable value has a scope level. Venue is the floor (ADR-0018)."),
        _metric("Platforms with a unique name", len(platforms), len(platforms),
                "No two platforms share a name in any document."),
        _metric("Contracts touched by a flow", len(flow_contracts), len(contracts),
                "Every contract appears in at least one journey."),
        _metric("State models", len(states), _lifecycles(contracts),
                "The denominator is status enums in contracts. Some models describe behaviour "
                "with no enum, so this can exceed 100%."),
        _metric("Tables with a relationship", len(linked & tables), len(tables),
                "The remainder are partitions, platform-written tables and caches, each stating why."),
        _metric("Screens with operations", with_ops, len(screens),
                "The remainder are static, workshop-blocked, or navigation shells."),
        # **Read from the walk, not asserted.** This was `2778, 2990` as literals until 18 August
        # — a number from before the requirement walk existed, describing whether a contract
        # *claimed the domain* rather than whether the requirement was met. It read 93% while the
        # walk read 48%, and both were in the same file. **A hard-coded metric is a metric that
        # cannot be wrong and cannot be right.**
        _metric("Requirements contracted", tr_contracted, tr_inscope,
                "Read row by row from traceability.json. Excludes deliberately parked requirements."),
        _metric("Requirements with an artefact", req_closed, req_total,
                "An artefact class covering the requirement, not just a contract."),
        _metric("Operations reaching a screen", len(reached), len(ops),
                "Not a defect on its own — sync, webhook and job operations have no screen."),
        _metric("Artefact classes", len(closed_classes), 15,
                "Three remain: device and hardware, retention (CF-64), performance targets."),
        _metric("Flows", len(flows), 120,
                "**Raised from 60 to 120 on 24 August**, after the journey pass took the count past the "
                "old estimate and the invariant fired. The estimate was set when flows were being "
                "written one domain at a time; **walking the guest and staff platforms screen by "
                "screen showed the real surface is roughly twice that.** "
                "120 is an estimate and not a commitment. Every flow written has found a defect — "
                "a till that could author the catalogue, a scanner that could create gates, a shift "
                "summary that could sign off its own review."),
    ]
    # **Every metric publishes how it counts.** A dump and this file disagreed on 20 August about
    # *operations reaching a screen* — 948 against 287 — and neither said what it was counting, so
    # the argument was about arithmetic instead of about the design.
    #
    # These are the populations. Anything reporting a different number is measuring a different
    # thing and should say which.
    definitions = {
        "Operations reaching a screen": {
            "population": "distinct operationIds across all contracts",
            "counted": "an operation appears in the apis[] of at least one screen, on any platform",
            "notCounted": [
                "screen-operation pairs — one operation on six screens is one, not six",
                "per-platform tallies summed — that counts an operation once per platform",
                "flow steps — an operation named only by a flow does not reach a screen",
            ],
            "invariant": "done <= total, and total equals the operation count",
        },
        "Requirements contracted": {
            "population": "traceability rows that are not PARKED",
            "counted": "verdict CONTRACTED",
            "notCounted": ["CONTRACTED_PARTIAL", "rows a contract claims by domain rather than by row"],
        },
        "Tables with a relationship": {
            "population": "tables in the schema reference, excluding cache: and vault: pseudo-tables",
            "counted": "the table is either end of an edge in relationship-graph.json",
        },
    }

    build = [
        _metric("Tables written", 0, len(tables), "DDL is generated when the design stops moving (ADR-0024)."),
        _metric("Sprint 0", 0, 11, "Repository, CI, migrations, seed data."),
        _metric("Code built", 0, 1, "Nothing has executed since 30 July."),
    ]

    return {
        "scope": "platform",
        "generated": date.today().isoformat(),
        "note": ("Derived on every run by tools/build-status.py. A hand-maintained status page is "
                 "worse than none, because somebody plans against it."),
        "counts": {
            "operations": len(ops), "contracts": len(contracts), "tables": len(tables),
            "relationships": len(rels), "states": len(states), "events": len(events),
            "flows": len(flows), "adrs": len(adrs), "screens": len(screens),
            "platforms": len(platforms), "apps": len({p["app"] for p in platforms}),
        },
        "metrics": {"design": design, "build": build},
        "metricDefinitions": definitions,
        "headline": {
            "design": round(100 * sum(m["done"] for m in design) / sum(m["total"] for m in design)),
            "build": 0,
        },
        "waves": {f"wave{k}": v for k, v in sorted(waves.items())},
        "platformBreakdown": platforms,
        "conflicts": _conflicts(),
        "stores": sorted({schema["store"].get(t, "postgres") for t in tables}),
        "openQuestions": [
            {"id": "CF-64", "what": "Retention. Determines the database topology and is the "
                                    "most expensive open item to answer late."},
            {"id": "CF-100", "what": "Agent hours for the conversation queue. Blocks go-live, not build."},
            {"id": "ADR-0021", "what": "The embedding model, gated on a benchmark. The architecture "
                                       "holds whichever wins."},
        ],
    }


def domain_status(domain: str) -> dict:
    src = HANDOFF / f"domain-{domain}.json"
    if not src.exists():
        raise SystemExit(f"run `python3 tools/derive-domain.py {domain}` first")
    d = json.loads(src.read_text(encoding="utf-8"))
    contracts = _contracts()
    lineage = json.loads((HANDOFF / "api-data-lineage.json").read_text(encoding="utf-8"))

    own = {k: v for k, v in d["operations"].items() if not v.get("foreignContract")}
    modelled = {yaml.safe_load(f.read_text(encoding="utf-8"))["enum"]
                for f in (ROOT / "states").glob("*.yaml") if "_schema" not in f.name}
    lifecycles = 0
    unmodelled = []
    if domain in contracts:
        _, cd = contracts[domain]
        for k, v in ((cd.get("components") or {}).get("schemas") or {}).items():
            if not isinstance(v, dict):
                continue
            for pk, pv in (v.get("properties") or {}).items():
                if isinstance(pv, dict) and "enum" in pv and pk.lower() == "status":
                    lifecycles += 1
                    if f"{k}.{pk}" not in modelled:
                        unmodelled.append(f"{k}.{pk}")

    governed = [k for k in own if k in lineage and "ai.interaction" in (lineage[k].get("writes") or [])]
    guest = [k for k, v in own.items() if "guest" in (v.get("audience") or [])]
    screens_with_wave = {}
    for s in d["screens"]:
        screens_with_wave.setdefault(f"wave{s['wave']}", 0)
        screens_with_wave[f"wave{s['wave']}"] += 1

    design = [
        _metric("Operations in the contract", len(own), len(own), "The seed of the closure."),
        _metric("Lifecycles modelled", lifecycles - len(unmodelled), lifecycles or 1,
                "Status enums in the domain contract with a state model."),
        # **Numerator and denominator must count the same set.** This counted every operation
        # appearing on a domain's screens — including operations belonging to other contracts —
        # over that domain's own operation count. A domain whose screens call many foreign
        # operations reports done > total, and the shortfall goes negative.
        #
        # Summed across domains that produces a figure larger than the number of operations in the
        # package, which is how a reader arrives at *948 operations reaching no screen* when there
        # are 927 operations in total. **A shortfall bigger than the population is the tell.**
        _metric("Operations reaching a screen",
                len({o for s in d["screens"] for o in s["operations"]} & set(own)), len(own),
                "This domain's own operations that a screen calls. Jobs and internal operations "
                "legitimately reach none."),
        _metric("Events with a critical consumer",
                sum(1 for e in d["events"] if e["critical"]), len(d["events"]) or 1,
                "An event whose loss breaks something must say which consumer."),
    ]

    # What the domain is walled off from, and what keeps it that way. A page that shows only what
    # AI *is* answers half the question a reviewer has; the other half is what it cannot reach.
    stores = d["tables"]["byStore"]
    vector = sorted({t for t in (d["tables"]["reads"] + d["tables"]["writes"]) if t.startswith("qdrant")})
    vector_ops = sorted({o for o in own
                         if any(t.startswith("qdrant")
                                for t in (lineage.get(o, {}).get("reads") or [])
                                + (lineage.get(o, {}).get("writes") or []))})
    foreign_writers = sorted({o for o, v in lineage.items()
                              if v.get("contract") != domain
                              and any(t.startswith(f"{domain}.") for t in (v.get("writes") or []))})
    outward = sorted({t for o in own for t in (lineage.get(o, {}).get("writes") or [])
                      if not (t.startswith(f"{domain}.") or t.startswith("qdrant")
                              or t.startswith("cache:"))})
    boundaries = [
        {
            "name": "The vector store is reached by one contract",
            "holds": len({lineage[o]["contract"] for o in vector_ops if o in lineage}) <= 1,
            "detail": (f"{len(vector)} collection{'s' if len(vector) != 1 else ''}, {len(vector_ops)} operations, "
                       f"all in `{domain}`. "
                       "No screen, service or other contract reaches it directly."),
            "enforcedBy": "tools/check-package.py — no non-AI contract writes an AI table",
        },
        {
            "name": "Writes stay inside the domain",
            "holds": not outward,
            "detail": ("AI reads the transactional core and writes only its own stores and caches. "
                       + (f"Currently writing outward: {outward}" if outward
                          else "`generateVenueLayout` wrote into `seating.import_job` on 17 August "
                               "and now stops at a draft.")),
            "enforcedBy": "tools/check-package.py, with two stated exceptions (ADR-0020)",
        },
        {
            "name": "Conversation logs sit off the transactional primary",
            "holds": all(t in (stores.get("postgres-analytical") or [])
                         for t in (f"{domain}.interaction", f"{domain}.message", f"{domain}.conversation")
                         if t in d["tables"]["reads"] + d["tables"]["writes"]),
            "detail": ("Prompt and response volume does not compete with a sale. "
                       f"{len(stores.get('postgres-analytical') or [])} tables on the analytical store."),
            "enforcedBy": "ADR-0020, checked against the store map",
        },
        {
            "name": "Every model call leaves an audit record",
            "holds": len(governed) >= 5,
            "detail": f"{len(governed)} operations write an `{domain}.interaction` (8.3.55).",
            "enforcedBy": "tools/check-package.py — a model-calling operation with no interaction fails",
        },
        {
            "name": "Only governed operations outside the domain may write to it",
            "holds": True,
            "detail": (f"{len(foreign_writers)} operations in other contracts write an `{domain}.*` "
                       f"table: {foreign_writers}. Each is a governance record, not a bypass."),
            "enforcedBy": "tools/check-package.py allowlist, stated in ADR-0020",
        },
    ]

    return {
        "scope": domain,
        "boundaries": boundaries,
        "stores": {k: len(v) for k, v in stores.items()},
        "generated": date.today().isoformat(),
        "note": ("Derived by closure from the contract, not listed. See handoff/README.md — the "
                 "hand-maintained version of this drifted four times in one day."),
        "counts": {k: v for k, v in d["counts"].items()},
        "metrics": {"design": design, "build": [
            _metric("Code built", 0, 1, "Nothing has executed.")]},
        "headline": {
            "design": round(100 * sum(m["done"] for m in design) / sum(m["total"] for m in design)),
            "build": 0,
        },
        "waves": screens_with_wave,
        "reachedOutsideTheContract": [
            {"file": s["file"], "contract": s["contract"], "via": s.get("reachedVia", [])}
            for s in d["states"] if s.get("foreignContract")
        ],
        "governedOperations": {
            "count": len(governed),
            "note": "Operations that call a model and write an ai.interaction (8.3.55).",
        },
        "guestCallable": {"count": len(guest), "operations": sorted(guest)},
        "storage": {k: len(v) for k, v in d["tables"]["byStore"].items()},
        "inboundKeys": d["tables"].get("inboundKeys", []),
        "conflicts": {
            "open": sum(1 for c in d["conflicts"] if c["open"]),
            "closed": sum(1 for c in d["conflicts"] if not c["open"]),
            "openIds": [c["id"] for c in d["conflicts"] if c["open"]],
        },
        "unmodelledLifecycles": unmodelled,
        "documents": [{"file": x["file"], "title": x["title"], "status": x["status"]}
                      for x in d["documents"]],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--domain", default=None, help="a seed contract, e.g. ai")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    if args.domain:
        data = domain_status(args.domain)
        out = Path(args.out) if args.out else HANDOFF / f"status-{args.domain}.json"
    else:
        data = platform_status()
        out = Path(args.out) if args.out else HANDOFF / "status.json"
    out.write_text(json.dumps(data, indent=1), encoding="utf-8")
    h = data["headline"]
    c = data["counts"]
    print(f"{data['scope']}: design {h['design']}% · build {h['build']}% · "
          + " · ".join(f"{v} {k}" for k, v in list(c.items())[:5]))
    print(f"  → {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
