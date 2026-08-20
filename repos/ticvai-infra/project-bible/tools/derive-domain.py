#!/usr/bin/env python3
"""Derive a domain's membership by closure from a seed contract.

    python3 tools/derive-domain.py ai
    python3 tools/derive-domain.py finance --out handoff/domain-finance.json

Nothing here is hand-typed, which is the point. `handoff/ai-index.md` was maintained by hand
until 17 August and drifted four times in one day: `generateVenueLayout` wrote into
`seating.import_job` and the index did not say so; `askReportingQuestion` was brought under
governance and the lineage was not updated; the RAG register named eleven source tables the
lineage agreed with none of; and `Conversation` acquired a state model in a different contract
that no AI document mentioned. A derived set would have carried all four on the day they landed.

The closure is deliberately one-directional — it follows *outward* from the seed and stops at
artefacts that merely mention it. A screen calling one AI operation is in. An ADR that names AI
in passing is in, because an ADR is short and a false positive costs a reader nothing. A table
that AI reads is in; the 60 tables that read *that* table are not, or the answer is the whole
platform.

    seed        the contract's operations
      ↓ schemas they read and write
      ↓ enums those schemas use              → ConversationState
      ↓ state models on those enums          → conversation.yaml, which lives under marketing-crm
      ↓ events those states publish          → ai.ceilingApproaching, conversation.handedOver
      ↓ tables the lineage maps them to
      ↓ screens that call the operations
      ↓ flows whose steps call them
      ↓ ADRs and architecture notes that name them

The output drives two surfaces from one definition: a marker on each artefact where it already
sits in the artefact-kind tree, and a page that gathers the whole set across layers.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"
STATES = ROOT / "states"
EVENTS = ROOT / "events"
FLOWS = ROOT / "flows"
SCREENS = ROOT / "screens"
DOCS = ROOT / "docs"
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


def _schema_reference() -> dict:
    """The store map, from wherever the schema reference actually is.

    `Path.home()` resolved to `/root` under one shell and `/home/claude` under another on
    17 August, so every table silently reported as `postgres` and the analytical split — the
    thing ADR-0020 exists to enforce — vanished from the derived set without an error. Candidates
    are tried in order and the absence is loud.
    """
    data = _package_json("schema-reference.json", "schema_v4.json")
    if data:
        return data
    print("  warning: no schema reference found — store split not shown", file=sys.stderr)
    return {"store": {}}


def _load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _contract_path(name: str) -> Path:
    for tier in ("spine", "satellite"):
        p = CONTRACTS / tier / f"{name}.yaml"
        if p.exists():
            return p
    sys.exit(f"no contract named '{name}' in contracts/spine or contracts/satellite")


def _verbs(item: dict):
    for verb, op in item.items():
        if verb in ("get", "post", "put", "patch", "delete") and isinstance(op, dict):
            yield verb, op


def _schema_refs(node, out: set[str]) -> None:
    """Every #/components/schemas/X reachable from a node."""
    if isinstance(node, dict):
        ref = node.get("$ref")
        if isinstance(ref, str) and "#/components/schemas/" in ref:
            out.add(ref.rsplit("/", 1)[-1])
        for v in node.values():
            _schema_refs(v, out)
    elif isinstance(node, list):
        for v in node:
            _schema_refs(v, out)


def derive(seed: str) -> dict:
    contract = _load(_contract_path(seed))
    schemas = (contract.get("components") or {}).get("schemas") or {}

    # 1. operations
    operations: dict[str, dict] = {}
    for path, item in (contract.get("paths") or {}).items():
        if not isinstance(item, dict):
            continue
        for verb, op in _verbs(item):
            oid = op.get("operationId")
            if oid:
                operations[oid] = {
                    "path": path,
                    "verb": verb.upper(),
                    "summary": (op.get("summary") or "")[:120],
                    "permission": op.get("x-ticvai-permission"),
                    "guestCallable": bool("guest" in (op.get("x-ticvai-audience") or [])),
                    "scopeLevel": op.get("x-ticvai-scope-level"),
                }

    # 2. schemas those operations touch, transitively
    named: set[str] = set()
    for path, item in (contract.get("paths") or {}).items():
        if isinstance(item, dict):
            _schema_refs(item, named)
    frontier = set(named)
    while frontier:
        nxt: set[str] = set()
        for name in frontier:
            body = schemas.get(name)
            if body is None:
                continue
            found: set[str] = set()
            _schema_refs(body, found)
            nxt |= found - named
        named |= nxt
        frontier = nxt

    # 3. enums those schemas use, named or inline — the step that reaches outside the contract
    enums: set[str] = set()
    for name in sorted(named):
        body = schemas.get(name)
        if not isinstance(body, dict):
            continue
        if body.get("type") == "string" and "enum" in body:
            enums.add(name)
        for prop, spec in (body.get("properties") or {}).items():
            if isinstance(spec, dict) and "enum" in spec and prop.lower() in ("status", "state"):
                enums.add(f"{name}.{prop}")
    # a schema whose `status` is a $ref to a named enum carries that enum's name
    for name in sorted(named):
        body = schemas.get(name)
        if not isinstance(body, dict):
            continue
        for prop, spec in (body.get("properties") or {}).items():
            if isinstance(spec, dict) and prop.lower() in ("status", "state"):
                ref = spec.get("$ref")
                if isinstance(ref, str):
                    enums.add(ref.rsplit("/", 1)[-1])

    # 4. state models on those enums — wherever they live
    states = []
    for f in sorted(STATES.glob("*.yaml")):
        if "_schema" in f.name:
            continue
        d = _load(f)
        enum = d.get("enum", "")
        if enum in enums or enum.split(".")[0] in enums or d.get("contract") == seed:
            states.append({
                "file": f.name,
                "entity": d.get("entity"),
                "contract": d.get("contract"),
                "enum": enum,
                "foreignContract": d.get("contract") != seed,
                "emits": sorted({e for t in d.get("transitions", []) for e in (t.get("emits") or [])}),
            })

    # 5. events — published by those states, or naming the seed as publisher or consumer
    emitted = {e for s in states for e in s["emits"]}
    events = []
    for f in sorted(EVENTS.glob("*.yaml")):
        if "_schema" in f.name:
            continue
        d = _load(f)
        name = d.get("name")
        consumes = any(c.get("context") == seed for c in (d.get("consumers") or []))
        publishes = d.get("publisher") == seed
        if name in emitted or consumes or publishes:
            events.append({
                "name": name,
                "publisher": d.get("publisher"),
                "role": "publishes" if publishes else ("consumes" if consumes else "emitted by a state model"),
                "critical": any(c.get("isCritical") for c in (d.get("consumers") or [])),
            })

    # 5b. the reverse hop — a state model that emits an event the seed consumes belongs to the
    # picture, even though it lives in another contract. This is what reaches `conversation.yaml`
    # from `ai.yaml`: AI never names ConversationState, but it consumes `conversation.handedOver`,
    # and the model that emits it is where the handover behaviour is actually specified. Without
    # this hop the AI set contains the event and not the thing that causes it.
    in_set = {e["name"] for e in events}
    known = {s["file"] for s in states}
    for f in sorted(STATES.glob("*.yaml")):
        if "_schema" in f.name or f.name in known:
            continue
        d = _load(f)
        emits = {e for t in d.get("transitions", []) for e in (t.get("emits") or [])}
        if not emits & in_set:
            continue
        states.append({
            "file": f.name,
            "entity": d.get("entity"),
            "contract": d.get("contract"),
            "enum": d.get("enum", ""),
            "foreignContract": d.get("contract") != seed,
            "reachedVia": sorted(emits & in_set),
            "emits": sorted(emits),
        })
        enums.add(d.get("enum", ""))

    # 6. tables, from the lineage
    lineage = json.loads((HANDOFF / "api-data-lineage.json").read_text(encoding="utf-8"))
    reads: set[str] = set()
    writes: set[str] = set()
    for oid in operations:
        v = lineage.get(oid)
        if v:
            reads |= set(v.get("reads") or [])
            writes |= set(v.get("writes") or [])
    for oid, v in lineage.items():
        # an operation in another contract that writes a seed-owned table belongs to the picture
        if v.get("contract") != seed:
            owned = [t for t in (v.get("writes") or []) if t.startswith(f"{seed}.")]
            if owned:
                operations.setdefault(oid, {
                    "path": v.get("path"), "verb": v.get("verb"),
                    "summary": v.get("summary"), "permission": v.get("perm"),
                    "guestCallable": False, "scopeLevel": v.get("scope"),
                    "foreignContract": v.get("contract"),
                })
                writes |= set(owned)

    # 7. screens
    screens = []
    for f in sorted(SCREENS.glob("P*.yaml")):
        d = _load(f)
        platform = d["platform"]
        for s in d["screens"]:
            hit = sorted({a["operationId"] for a in (s.get("apis") or [])
                          if a.get("operationId") in operations})
            if hit:
                screens.append({
                    "id": s["id"], "name": s["name"],
                    "platform": platform["code"], "platformName": platform["shortName"],
                    "wave": s.get("wave"), "operations": hit,
                })

    # 8. flows
    flows = []
    for f in sorted(FLOWS.glob("F*.yaml")):
        d = _load(f)
        hit = sorted({o for st in d.get("steps", []) for o in (st.get("operations") or [])
                      if o in operations})
        if hit:
            flows.append({"id": d["id"], "name": d["name"], "wave": d.get("wave"), "operations": hit})

    # 9. ADRs and architecture notes that name the seed or any of its operations
    tokens = {seed} | set(operations) | {t for t in reads | writes if t.startswith(f"{seed}.")}
    documents = []
    for f in sorted(list((DOCS / "adr").glob("0*.md")) + list((DOCS / "architecture").glob("*.md"))
                    + list((DOCS / "active").glob("*.md"))):
        text = f.read_text(encoding="utf-8")
        named_here = sorted({t for t in tokens if re.search(rf"\b{re.escape(t)}\b", text)})
        if not named_here:
            continue
        status = ""
        m = re.search(r"^\*\*Status:\*\* *(.+)$", text, re.M)
        if m:
            status = m.group(1).replace("*", "").strip()[:60]
        documents.append({
            "file": str(f.relative_to(ROOT)),
            "title": (text.split("\n", 1)[0]).lstrip("# ").strip()[:110],
            "status": status,
            "mentions": len(named_here),
        })

    # 10. open conflicts naming the seed
    conflicts = []
    reg = DOCS / "registers" / "conflicts.md"
    if reg.exists():
        section = ""
        for line in reg.read_text(encoding="utf-8").split("\n"):
            if line.startswith("## ") or line.startswith("### "):
                section = line.lstrip("# ").strip()
            m = re.match(r"^\| \*?\*?(CF-\d+)\*?\*? \|(.*)", line)
            if m and re.search(rf"\b{re.escape(seed)}\b", m.group(2), re.I):
                conflicts.append({
                    "id": m.group(1),
                    "open": "Open" in section,
                    "section": section,
                })

    # 6b. foreign tables holding a key into a seed-owned table. Bounded and few — two on 17 August
    # — and each one is a place another domain reaches into this one, which is exactly what a
    # reviewer wants to see. `marketing.conversation_message.ai_interaction_id` is the case:
    # it links a guest's message to its tokens and cost, and is why conversation spend is
    # attributable at all (CF-14).
    inbound = []
    links_path = next((c for c in (ROOT.parent / "work" / "links.json",
                                   Path("/home/claude/work/links.json"),
                                   Path.home() / "work" / "links.json") if c.exists()), None)
    if links_path:
        owned = {t for t in reads | writes if t.startswith(f"{seed}.")}
        for r in json.loads(links_path.read_text(encoding="utf-8")).get("rels", []):
            if r.get("to") in owned and not str(r.get("frm", "")).startswith(f"{seed}."):
                inbound.append({"from": r["frm"], "column": r["col"], "to": r["to"]})
                reads.add(r["frm"])

    # computed last, after every hop has finished adding tables — an earlier version ran before
    # 6b and reported every table as postgres, which hid that the interaction log is analytical.
    stores: dict[str, list[str]] = {}
    schema = _schema_reference()
    for t in sorted(reads | writes):
        stores.setdefault(schema["store"].get(t, "postgres"), []).append(t)

    return {
        "domain": seed,
        "derivedFrom": "closure over contracts, states, events, lineage, screens, flows and docs",
        "note": ("Nothing in this file is hand-typed. Regenerate with "
                 f"`python3 tools/derive-domain.py {seed}` after any change."),
        "operations": dict(sorted(operations.items())),
        "schemas": sorted(named),
        "enums": sorted(enums),
        "states": states,
        "events": events,
        "tables": {"reads": sorted(reads), "writes": sorted(writes), "byStore": stores,
                   "inboundKeys": inbound},
        "screens": screens,
        "flows": flows,
        "documents": documents,
        "conflicts": conflicts,
        "counts": {
            "operations": len(operations), "schemas": len(named), "states": len(states),
            "events": len(events), "tables": len(reads | writes), "screens": len(screens),
            "flows": len(flows), "documents": len(documents),
            "openConflicts": sum(1 for c in conflicts if c["open"]),
        },
    }


def markers(result: dict) -> dict:
    """The within-tree surface: one flat map from artefact id to the domains it belongs to.

    The viewer reads this to put a dot beside an artefact where it already sits. `ai.yaml` stays
    in Contracts; `conversation.yaml` stays in Domain under `marketing-crm` where it correctly
    belongs. Neither moves — each just wears a marker, and the artefact-kind organisation
    survives.
    """
    d = result["domain"]
    out: dict[str, list[str]] = {}

    def mark(key: str, reason: str) -> None:
        out.setdefault(key, []).append(f"{d}:{reason}")

    for oid in result["operations"]:
        mark(f"operation:{oid}", "seed" if not result["operations"][oid].get("foreignContract") else "writes a domain table")
    for st in result["states"]:
        mark(f"state:{st['file']}", "reached via " + ", ".join(st.get("reachedVia", [])) if st.get("reachedVia") else "domain contract")
    for e in result["events"]:
        mark(f"event:{e['name']}", e["role"])
    for t in result["tables"]["reads"] + result["tables"]["writes"]:
        mark(f"table:{t}", "owned" if t.startswith(f"{d}.") else "read or written")
    for s in result["screens"]:
        mark(f"screen:{s['id']}", f"calls {len(s['operations'])}")
    for f in result["flows"]:
        mark(f"flow:{f['id']}", "steps through")
    for doc in result["documents"]:
        mark(f"document:{doc['file']}", "names it")
    for c in result["conflicts"]:
        mark(f"conflict:{c['id']}", "open" if c["open"] else "closed")
    return {k: sorted(set(v)) for k, v in sorted(out.items())}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("domain", help="the seed contract, e.g. ai")
    ap.add_argument("--out", default=None)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    result = derive(args.domain)
    out = Path(args.out) if args.out else HANDOFF / f"domain-{args.domain}.json"
    out.write_text(json.dumps(result, indent=1), encoding="utf-8")
    # the within-tree surface, merged across every domain already derived so one file serves them all
    mpath = HANDOFF / "domain-markers.json"
    merged = json.loads(mpath.read_text(encoding="utf-8")) if mpath.exists() else {}
    merged = {k: [x for x in v if not x.startswith(f"{args.domain}:")] for k, v in merged.items()}
    for k, v in markers(result).items():
        merged.setdefault(k, []).extend(v)
    merged = {k: sorted(set(v)) for k, v in sorted(merged.items()) if v}
    mpath.write_text(json.dumps(merged, indent=1), encoding="utf-8")
    if not args.quiet:
        c = result["counts"]
        print(f"{args.domain}: " + " · ".join(f"{v} {k}" for k, v in c.items()))
        foreign = [s for s in result["states"] if s["foreignContract"]]
        if foreign:
            print("  reached outside the contract: " +
                  ", ".join(f"{s['file']} (in {s['contract']})" for s in foreign))
        print(f"  → {out.relative_to(ROOT)} and handoff/domain-markers.json "
              f"({len(json.loads((HANDOFF / 'domain-markers.json').read_text(encoding="utf-8")))} marked artefacts)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
