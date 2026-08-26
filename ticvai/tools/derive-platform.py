#!/usr/bin/env python3
"""Derive a page per platform, with the gaps that need filling.

    python3 tools/derive-platform.py           # all twelve
    python3 tools/derive-platform.py P01

Emits `handoff/platform-<code>.json` and `handoff/platform-<code>.md`.

**The point is the gaps section.** A platform page that lists what exists is a directory; one that
lists what is missing is a worklist. Four kinds of gap are derivable without anyone typing them:

**Operations with no screen** — an operation whose contract this platform already uses, on a
surface this platform serves, that no screen here calls. Either a screen is missing or the
endpoint should not exist.

**Modules present in one wave and absent from another** — a platform that sells in Wave 1 and has
no refund screen until Wave 3 is a platform that can take money and not give it back.

**Screens with no board anchor** — drawn nowhere, so nobody has seen them.

**Flows that step through this platform and land on a screen it does not have** — the flow says
the journey needs it.

Nothing here is typed. Membership is the platform's own screen file; everything else is closure
over the lineage, the flows and the boards.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

import yaml
import sys

# A cp1252 console cannot encode the arrows and dashes this tool prints, and the
# failure lands *after* the work is done — so the output is written, the summary
# line raises UnicodeEncodeError, and a correct run exits 1. Reconfiguring at
# import means anything importing this module gets it too, refresh.sh included.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:      # a captured stream may not be reconfigurable; harmless
    pass


ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "handoff"
SCREENS = ROOT / "screens"


def load_all():
    lineage = json.loads((HANDOFF / "api-data-lineage.json").read_text(encoding="utf-8"))
    platforms = {}
    screens = {}
    for f in sorted(SCREENS.glob("P*.yaml")):
        d = yaml.safe_load(f.read_text(encoding="utf-8"))
        p = d["platform"]
        platforms[p["code"]] = {"meta": p, "file": f.name, "screens": d["screens"]}
        for s in d["screens"]:
            screens[s["id"]] = (p["code"], s)
    flows = [yaml.safe_load(f.read_text(encoding="utf-8")) for f in sorted((ROOT / "flows").glob("F*.yaml"))]
    return lineage, platforms, screens, flows


def derive(code: str, lineage, platforms, screens, flows) -> dict:
    P = platforms[code]
    meta, rows = P["meta"], P["screens"]
    audience = meta.get("operator")

    ops_here = {a["operationId"] for s in rows for a in (s.get("apis") or []) if a.get("operationId")}
    contracts = Counter(lineage[o]["contract"] for o in ops_here if o in lineage)
    modules = Counter(s.get("module") for s in rows)
    waves = Counter(s["wave"] for s in rows)

    # gap 1 — an operation in a contract this platform uses, callable by its audience, and reaching
    # **no screen on any platform serving that audience**.
    #
    # The audience qualifier is what makes this a worklist rather than noise. Without it, every
    # staff operation living on the staff app counted as a gap for the back office as well, and
    # P08 reported 309 gaps it did not have. An operation belongs to an audience, not to one
    # screen — the question is whether that audience can reach it anywhere.
    # Reaching *any* screen counts. An operation on a guest screen and callable by staff is not a
    # missing back-office screen — it is an operation somebody can already reach, and listing it
    # made P08 report 229 gaps against a platform-wide total of 180 operations reaching no screen
    # at all. A number larger than the population it is drawn from is a rule that is wrong.
    ops_anywhere = {a["operationId"]
                    for _, s in screens.values()
                    for a in (s.get("apis") or []) if a.get("operationId")}
    ops_audience = ops_anywhere
    reachable = []
    for oid, v in lineage.items():
        if v["contract"] not in contracts or oid in ops_audience:
            continue
        aud = v.get("audience") or ["staff"]
        want = "staff" if audience in ("venue", "ticvai") else audience
        if want not in aud:
            continue
        reachable.append({"operation": oid, "contract": v["contract"], "verb": v["verb"],
                          "summary": v.get("summary", "")[:90]})

    # gap 2 — a module that appears in an early wave and not in a later one, or the reverse.
    by_module_wave = defaultdict(set)
    for s in rows:
        by_module_wave[s.get("module")].add(s["wave"])
    split = [{"module": m, "waves": sorted(w)} for m, w in sorted(by_module_wave.items())
             if len(w) > 1]

    # gap 3 — screens nobody has drawn
    undrawn = [{"id": s["id"], "name": s["name"], "wave": s["wave"]}
               for s in rows if (s.get("wireframe") or {}).get("status") == "notStarted"]

    # gap 4 — a flow steps through this platform and names a screen it does not have
    mine = {s["id"] for s in rows}
    flow_gaps = []
    for f in flows:
        touches = [st for st in f.get("steps", []) if st.get("screen") in mine]
        if not touches:
            continue
        for st in f.get("steps", []):
            sid = st.get("screen")
            if sid and sid not in screens:
                flow_gaps.append({"flow": f["id"], "screen": sid, "step": st.get("step")})

    return {
        "code": code,
        "name": meta.get("name") or meta.get("shortName"),
        "shortName": meta.get("shortName"),
        "app": meta.get("app"),
        "operator": audience,
        "audience": meta.get("audience"),
        "formFactor": meta.get("formFactor"),
        "offlineCapable": bool(meta.get("offlineCapable")),
        "generated": date.today().isoformat(),
        "note": ("Derived by tools/derive-platform.py. **The gaps section is the point** — a page "
                 "listing what exists is a directory; one listing what is missing is a worklist."),
        "counts": {
            "screens": len(rows),
            "operations": len(ops_here),
            "contracts": len(contracts),
            "modules": len(modules),
            "undrawn": len(undrawn),
            "operationsWithNoScreen": len(reachable),
        },
        "waves": {f"wave{k}": v for k, v in sorted(waves.items())},
        "modules": [{"module": m, "screens": n,
                     "waves": sorted(by_module_wave[m])} for m, n in modules.most_common()],
        "contracts": [{"contract": c, "operations": n} for c, n in contracts.most_common()],
        "screens": [{"id": s["id"], "name": s["name"], "module": s.get("module"),
                     "wave": s["wave"], "route": s["implementation"]["route"],
                     "operations": len(s.get("apis") or []),
                     "drawn": (s.get("wireframe") or {}).get("status") != "notStarted"}
                    for s in sorted(rows, key=lambda x: x["id"])],
        "gaps": {
            "operationsWithNoScreen": sorted(reachable, key=lambda x: (x["contract"], x["operation"])),
            "modulesSplitAcrossWaves": split,
            "screensNotDrawn": undrawn,
            "flowsNamingAMissingScreen": flow_gaps,
        },
    }


def render(d: dict) -> str:
    L = []
    w = L.append
    c = d["counts"]
    w(f"# {d['code']} {d['shortName']} — platform")
    w("")
    w(f"**Derived.** `python3 tools/derive-platform.py {d['code']}`. "
      f"App `{d['app']}` · {d['operator']} · {d['formFactor']}"
      + (" · offline-capable" if d["offlineCapable"] else ""))
    w("")
    w("| | |")
    w("|---|---|")
    for k, v in c.items():
        label = "".join(" " + x.lower() if x.isupper() else x for x in k).strip().capitalize()
        w(f"| {label} | {v} |")
    w(f"| Waves | " + " · ".join(f"{k} {v}" for k, v in d["waves"].items()) + " |")
    w("")

    g = d["gaps"]
    total = sum(len(v) for v in g.values())
    w("## Gaps")
    w("")
    if not total:
        w("**None derivable.** Every operation this platform's contracts expose to its audience "
          "reaches a screen, every module spans one wave, everything is drawn, and no flow names "
          "a screen that does not exist.")
        w("")
    else:
        if g["operationsWithNoScreen"]:
            w(f"### {len(g['operationsWithNoScreen'])} operations with no screen here")
            w("")
            w("**In a contract this platform uses, callable by its audience, and reaching no screen "
              "on any platform serving that audience.** Either a screen is missing or the endpoint "
              "should not exist — and the second is worth considering first.")
            w("")
            w("| Operation | Contract | | |")
            w("|---|---|---|---|")
            for x in g["operationsWithNoScreen"][:40]:
                w(f"| `{x['operation']}` | {x['contract']} | {x['verb']} | {x['summary']} |")
            if len(g["operationsWithNoScreen"]) > 40:
                w(f"| … | | | {len(g['operationsWithNoScreen']) - 40} more |")
            w("")
        if g["modulesSplitAcrossWaves"]:
            w(f"### {len(g['modulesSplitAcrossWaves'])} modules split across waves")
            w("")
            w("**A platform that sells in one wave and cannot refund until a later one can take "
              "money and not give it back.** Not always wrong — worth a look each time.")
            w("")
            for x in g["modulesSplitAcrossWaves"]:
                w(f"- **{x['module']}** — waves {', '.join(str(y) for y in x['waves'])}")
            w("")
        if g["screensNotDrawn"]:
            w(f"### {len(g['screensNotDrawn'])} screens nobody has drawn")
            w("")
            for x in g["screensNotDrawn"]:
                w(f"- `{x['id']}` {x['name']} — wave {x['wave']}")
            w("")
        if g["flowsNamingAMissingScreen"]:
            w(f"### {len(g['flowsNamingAMissingScreen'])} flows naming a screen that does not exist")
            w("")
            for x in g["flowsNamingAMissingScreen"]:
                w(f"- **{x['flow']}** step {x['step']} → `{x['screen']}`")
            w("")

    w("## Modules")
    w("")
    w("| Module | Screens | Waves |")
    w("|---|---|---|")
    for m in d["modules"]:
        w(f"| {m['module']} | {m['screens']} | {', '.join(str(x) for x in m['waves'])} |")
    w("")

    w("## Screens")
    w("")
    w("| | Name | Module | Wave | Ops | Drawn |")
    w("|---|---|---|---|---|---|")
    for s in d["screens"]:
        w(f"| `{s['id']}` | {s['name']} | {s['module']} | {s['wave']} | {s['operations']} | "
          f"{'yes' if s['drawn'] else '**no**'} |")
    w("")
    return "\n".join(L) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("code", nargs="?", help="e.g. P01. Omit for all.")
    args = ap.parse_args()

    lineage, platforms, screens, flows = load_all()
    codes = [args.code] if args.code else sorted(platforms)
    index = {}
    for code in codes:
        if code not in platforms:
            raise SystemExit(f"no platform {code}. Have: {', '.join(sorted(platforms))}")
        d = derive(code, lineage, platforms, screens, flows)
        (HANDOFF / f"platform-{code}.json").write_text(json.dumps(d, indent=1), encoding="utf-8")
        (HANDOFF / f"platform-{code}.md").write_text(render(d), encoding="utf-8")
        index[code] = {k: d[k] for k in ("shortName", "app", "operator", "counts", "waves")}
        g = sum(len(v) for v in d["gaps"].values())
        print(f"  {code} {d['shortName'][:26]:28}{d['counts']['screens']:>4} screens · "
              f"{d['counts']['operations']:>4} ops · {g:>3} gaps")
    if not args.code:
        (HANDOFF / "platform-index.json").write_text(json.dumps(index, indent=1), encoding="utf-8")
        print(f"\n  → handoff/platform-*.json + .md, and platform-index.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
