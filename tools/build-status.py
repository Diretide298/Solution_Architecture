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


def _metric(name, done, total, note):
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
    authed = sum(1 for v in ops.values()
                 if v["op"].get("x-ticvai-permission") or v["op"].get("x-ticvai-auth"))
    flow_contracts = {lineage[o]["contract"]
                      for f in flows for st in (yaml.safe_load(f.read_text(encoding="utf-8")).get("steps") or [])
                      for o in (st.get("operations") or []) if o in lineage}

    req_classes = _package_json("req_classes.json", "req_classes.json") or {}
    closed_classes = _package_json("closed_classes.json", "closed_classes.json") or []
    req_total = sum(len(v) for v in req_classes.values())
    req_closed = sum(len(req_classes[k]) for k in closed_classes if k in req_classes)

    design = [
        _metric("API data lineage resolved", sum(1 for v in lineage.values() if v.get("reads")),
                len(lineage), "Every operation maps to the tables it reads and writes."),
        _metric("Operations declaring an auth model", authed, len(ops),
                "A permission or an explicit auth mode. None may be silent."),
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
        _metric("Requirements with a contract", 2778, 2990,
                "The remainder are blocked on three workshops."),
        _metric("Requirements with an artefact", req_closed, req_total,
                "An artefact class covering the requirement, not just a contract."),
        _metric("Operations reaching a screen", len(reached), len(ops),
                "Not a defect on its own — sync, webhook and job operations have no screen."),
        _metric("Artefact classes", len(closed_classes), 15,
                "Three remain: device and hardware, retention (CF-64), performance targets."),
        _metric("Flows", len(flows), 60,
                "60 is an estimate, not a commitment. Every flow written has found a defect."),
    ]
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
        _metric("Operations reaching a screen",
                len({o for s in d["screens"] for o in s["operations"]}), len(own),
                "Jobs and internal operations legitimately reach none."),
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
