#!/usr/bin/env python3
"""Emit what each audience reaches, as a filter set.

    python3 tools/build-audience.py       → handoff/audience-index.json

**A guest mode is not a filter on operations.** A guest reaches operations, and through them
screens, tables, flows and events — and showing the whole package to somebody reviewing the guest
experience buries the 51 things that concern them under 725 that do not.

Audience is one field on the operation (`x-ticvai-audience`), and everything else is reached
through it:

    audience → operations that declare it
             → screens on that audience's platforms which call them
             → tables those operations read and write
             → flows whose steps call them
             → events those tables' contracts publish

**Platform, not operation, decides which screens count.** An operation marked `[staff, guest]` is
called by staff on the back office and by a guest in the app; only the second belongs in guest
mode, and the platform's own `operator` field says which is which.
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "handoff"
CONTRACTS = ROOT / "contracts"

# Which platforms serve which audience. From each platform's declared `operator`, not guessed.
# P11 declares `public` and is not `guest` — an external reviewer holding a real permission is
# neither, and conflating them is what marked `decideApprovalRequest` guest-callable on 17 August.
OPERATOR_AUDIENCE = {
    "guest": "guest",
    "venue": "staff",
    "ticvai": "staff",
    "partner": "partner",
    "public": "public",
}


def main() -> int:
    lineage = json.loads((HANDOFF / "api-data-lineage.json").read_text(encoding="utf-8"))

    audience_of: dict[str, list[str]] = {}
    for tier in ("spine", "satellite"):
        for f in sorted((CONTRACTS / tier).glob("*.yaml")):
            doc = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
            for item in (doc.get("paths") or {}).values():
                if not isinstance(item, dict):
                    continue
                for verb, op in item.items():
                    if verb in ("get", "post", "put", "patch", "delete") and isinstance(op, dict):
                        oid = op.get("operationId")
                        if oid:
                            audience_of[oid] = op.get("x-ticvai-audience") or ["staff"]

    screens: dict[str, dict] = {}
    platforms: dict[str, dict] = {}
    for f in sorted((ROOT / "screens").glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        p = doc["platform"]
        platforms[p["code"]] = {
            "name": p["shortName"], "app": p["app"], "operator": p.get("operator"),
            "audience": OPERATOR_AUDIENCE.get(p.get("operator"), "staff"),
        }
        for s in doc["screens"]:
            screens[s["id"]] = {
                "name": s["name"], "platform": p["code"], "wave": s.get("wave"),
                "operations": [a["operationId"] for a in (s.get("apis") or []) if a.get("operationId")],
            }

    flows = []
    for f in sorted((ROOT / "flows").glob("F*.yaml")):
        d = yaml.safe_load(f.read_text(encoding="utf-8"))
        flows.append({
            "id": d["id"], "name": d["name"], "actor": d.get("actor"), "wave": d.get("wave"),
            "operations": sorted({o for st in d.get("steps", []) for o in (st.get("operations") or [])}),
            "screens": sorted({st["screen"] for st in d.get("steps", []) if st.get("screen")}),
        })

    out: dict[str, dict] = {}
    for aud in sorted({a for v in audience_of.values() for a in v} | {"partner", "public"}):
        ops = sorted(o for o, a in audience_of.items() if aud in a)
        # Only screens on platforms serving this audience. An operation shared with staff appears
        # in both modes; the screen it appears on does not.
        plats = {c for c, p in platforms.items() if p["audience"] == aud}
        scr = sorted(s for s, v in screens.items()
                     if v["platform"] in plats and set(v["operations"]) & set(ops))
        reads: set[str] = set()
        writes: set[str] = set()
        contracts: set[str] = set()
        for o in ops:
            v = lineage.get(o)
            if not v:
                continue
            reads |= set(v.get("reads") or [])
            writes |= set(v.get("writes") or [])
            contracts.add(v.get("contract"))
        fl = sorted(f["id"] for f in flows if set(f["operations"]) & set(ops)
                    and (not plats or set(f["screens"]) & set(scr) or f.get("actor") == aud))
        out[aud] = {
            "platforms": sorted(plats),
            "operations": ops,
            "screens": scr,
            "flows": fl,
            "contracts": sorted(c for c in contracts if c),
            "tables": sorted(reads | writes),
            "counts": {
                "operations": len(ops), "screens": len(scr), "flows": len(fl),
                "contracts": len(contracts), "tables": len(reads | writes),
            },
        }

    total_ops = len(audience_of)
    doc = {
        "generated": __import__("datetime").date.today().isoformat(),
        "note": ("Derived from `x-ticvai-audience` on every operation. **One field, five values** — "
                 "`x-ticvai-guest-callable` and `x-ticvai-auth` were two vocabularies answering the "
                 "same question differently and were collapsed on 18 August (ADR-0025)."),
        "field": "x-ticvai-audience",
        "values": ["staff", "guest", "anonymous", "device", "service"],
        "platformAudience": platforms,
        "totals": {"operations": total_ops, "screens": len(screens), "flows": len(flows)},
        "audiences": out,
    }
    (HANDOFF / "audience-index.json").write_text(json.dumps(doc, indent=1), encoding="utf-8")

    print(f"{total_ops} operations across {len(out)} audiences")
    for aud, v in sorted(out.items(), key=lambda x: -x[1]["counts"]["operations"]):
        c = v["counts"]
        print(f"  {aud:11}{c['operations']:>4} ops · {c['screens']:>3} screens · "
              f"{c['flows']:>2} flows · {c['tables']:>3} tables")
    print("  → handoff/audience-index.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
