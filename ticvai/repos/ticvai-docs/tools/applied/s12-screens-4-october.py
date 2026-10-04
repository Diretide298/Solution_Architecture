#!/usr/bin/env python3
"""Fix the screens the Sprint 1-2 judging of 4 October found unbuildable (CHG-FXS-001 to -007).

**The judge read every Sprint 1 and Sprint 2 ticket of r1 (main 857986c1) as a developer pulls it**
and found 73 screen tickets not buildable and 436 blockers across the package
(`audit/ticvai/runs/fix-s12/screens.tsv`). Chinmay, 4 October: fix all of it in one round, then one
refresh, then r1. The screen kinds:

  - **"Needs a person" screens planned in Sprints 1-2**: the generator gave a prose-only pack page no
    content region and said a person must define it. Each is defined here from what the package
    already holds (the bound operations' schemas, the design notes, the flow briefs, the decisions);
    where the package truly lacks what a person must decide, the screen keeps its gap and the plan
    is asked to move it out of Sprint 1-2 (`runs/fix-s12/LEDGER.md`).
  - Fields bound to no schema property, and forms missing a field the request requires.
  - Missing data sources: an id a call needs that nothing on the screen reads.
  - Stale gap notes on screens that are filled.

Where a fix needs an operation or a field the contracts do not have, the screen binds the name
agreed in the ledger with the contracts agent, and the request is written there.

Every edit is described in `s12-screens-4-october-specs.py` as data, one entry per screen, and
applied here; a screen already in its fixed form is left alone, so a second run says there is
nothing to do. Screens are spliced back one at a time by the 3 October pattern fix's writer, at the
file's own dump width, so nothing else in a file moves.

    python tools/applied/s12-screens-4-october.py            # dry run: what would change
    python tools/applied/s12-screens-4-october.py --apply
    python tools/applied/s12-screens-4-october.py --only BO-772,ADM-503
"""
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def _mod(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


spf = _mod("spf", "spec-screen-patterns-3-october.py")
sp = spf.sp

PERSON = ("needs a person", "gives this screen nothing that can be drawn",
          "no display, metric or configuration directory",
          "operations return no schema with described properties")


def _contract_of(pk, op, given):
    o = pk.ops.get(op)
    return (o or {}).get("_contract") or given


def _prov_for(pk, comp, chg):
    b, op = comp.get("bindsTo"), comp.get("operation")
    if b and op and op in pk.ops:
        return f"contract {pk.ops[op]['_contract']}.yaml {b} (defined 4 October 2026, {chg})"
    if b and op:
        return f"agreed operation `{op}`, runs/fix-s12/LEDGER.md (defined 4 October 2026, {chg})"
    return f"defined 4 October 2026 ({chg})"


def build_component(pk, c, chg):
    c = {k: v for k, v in c.items() if v is not None}
    c.setdefault("provenance", _prov_for(pk, c, chg))
    return c


def apply_fix(pk, s, fx) -> list:
    """Edit screen `s` in place from spec `fx`; return what changed."""
    chg = fx["chg"]
    log = []
    before = json.dumps({k: v for k, v in s.items() if not k.startswith("_")}, sort_keys=True,
                        default=str)
    marker = f"({chg})"
    if marker in str(s.get("notes") or "") and not fx.get("force"):
        return []
    # gaps
    gaps = list(s.get("gaps") or [])
    drop = fx.get("drop_gaps") or ()
    if drop:
        keep = []
        for g in gaps:
            why = str(g.get("why") or "")
            if ("person" in drop and any(p in why for p in PERSON)) or \
                    (g.get("operation") and g.get("operation") in drop) or \
                    any(isinstance(d, str) and d.startswith("~") and d[1:] in why for d in drop) or \
                    "all" in drop:
                continue
            keep.append(g)
        if len(keep) != len(gaps):
            log.append(f"{len(gaps) - len(keep)} gap(s) closed")
        gaps = keep
    for g in fx.get("gaps_add") or ():
        if any(x.get("why") == g.get("why") for x in gaps):
            continue
        gaps.append(dict(g))
        log.append("gap recorded: " + str(g.get("operation")))
    if gaps:
        s["gaps"] = gaps
    else:
        s.pop("gaps", None)
    # apis
    if fx.get("apis_drop"):
        n = len(s.get("apis") or [])
        s["apis"] = [a for a in s.get("apis") or [] if a["operationId"] not in fx["apis_drop"]]
        if len(s["apis"]) != n:
            log.append("dropped " + ", ".join(fx["apis_drop"]))
    for a in fx.get("apis_add") or ():
        a = dict(a)
        a["contract"] = _contract_of(pk, a["operationId"], a.get("contract"))
        a.setdefault("provenance", f"defined 4 October 2026 ({chg})")
        cur = [x for x in s.get("apis") or [] if x["operationId"] == a["operationId"]]
        if cur:
            cur[0].update({k: v for k, v in a.items() if k in ("trigger", "purpose")})
        else:
            s.setdefault("apis", []).append({k: a[k] for k in ("operationId", "contract", "purpose",
                                                                "trigger", "provenance") if k in a})
            log.append("bound " + a["operationId"])
    for op, upd in (fx.get("apis_set") or {}).items():
        for x in s.get("apis") or []:
            if x["operationId"] == op:
                x.update(upd)
    # layout
    if fx.get("regions") is not None:
        lay = s.setdefault("layout", {})
        if fx.get("template"):
            lay["template"] = fx["template"]
        lay["regions"] = [{"name": rn, "components": [build_component(pk, c, chg) for c in comps]}
                          for rn, comps in fx["regions"]]
        log.append("layout defined")
    if fx.get("comp_drop"):
        for r in (s.get("layout") or {}).get("regions") or []:
            n = len(r.get("components") or [])
            r["components"] = [c for c in r.get("components") or []
                               if c.get("label") not in fx["comp_drop"]]
            if len(r["components"]) != n:
                log.append(f"dropped {n - len(r['components'])} component(s) from {r.get('name')}")
    for rn, comp in fx.get("add_comps") or ():
        regs = s.setdefault("layout", {}).setdefault("regions", [])
        r = next((x for x in regs if x.get("name") == rn), None)
        if r is None:
            r = {"name": rn, "components": []}
            regs.append(r)
        if any(x.get("kind") == comp.get("kind") and x.get("label") == comp.get("label")
               for x in r.get("components") or []):
            continue
        r.setdefault("components", []).append(build_component(pk, comp, chg))
        log.append(f"added {comp.get('kind')} '{comp.get('label')}'")
    for label, upd in (fx.get("comp_set") or {}).items():
        for _, c in sp.components(s):
            hit = (c.get("kind") == label[5:] and not c.get("label"))                 if isinstance(label, str) and label.startswith("kind:") else c.get("label") == label
            if hit:
                for k, v in upd.items():
                    if v is None:
                        c.pop(k, None)
                    else:
                        c[k] = v
                c["provenance"] = _prov_for(pk, c, chg)
                log.append(f"rebound '{label}'")
    if "overlays" in fx:
        if fx["overlays"]:
            s["overlays"] = fx["overlays"]
        else:
            s.pop("overlays", None)
    for o in fx.get("overlays_add") or ():
        ov = s.setdefault("overlays", [])
        at = next((i for i, x in enumerate(ov) if x.get("id") == o["id"]), None)
        if at is None:
            ov.append(o)
        else:
            ov[at] = o
    if fx.get("overlays_drop"):
        s["overlays"] = [o for o in s.get("overlays") or [] if o.get("id") not in fx["overlays_drop"]]
        if not s["overlays"]:
            s.pop("overlays")
    # entry state
    if fx.get("entry") is not None:
        es = s.setdefault("entryState", {})
        es["params"] = fx["entry"]
        if not es["params"]:
            es.pop("params")
        if not es:
            s.pop("entryState")
    for k, v in (fx.get("entry_set") or {}).items():
        s.setdefault("entryState", {})[k] = v
    # navigation edges that carry a parameter
    # top-level fields
    for k in ("pattern", "patternReason"):
        if fx.get(k):
            s[k] = fx[k]
    for k, v in (fx.get("set") or {}).items():
        if v is None:
            s.pop(k, None)
        else:
            s[k] = v
    if fx.get("states"):
        st = s.setdefault("states", {})
        st.update(fx["states"])
    if s.get("apis") and fx.get("regions") is not None or fx.get("apis_add") or fx.get("apis_drop"):
        txt = sp.no_access_text(pk, s)
        if txt and "emptyNoAccess" in (s.get("states") or {}):
            s["states"]["emptyNoAccess"] = txt
    if fx.get("apisNote"):
        s["apisNote"] = fx["apisNote"]
    elif fx.get("regions") is not None and "labels bound to a contract property" in str(
            s.get("apisNote") or ""):
        s["apisNote"] = (f"Defined by hand 4 October 2026 ({chg}) from the bound operations' "
                         "schemas, the design notes and the decisions; every field names its "
                         "contract property.")
    note = f"**{fx['note']}** {marker}" if fx.get("note") else None
    if note and note not in str(s.get("notes") or ""):
        v = str(s.get("notes") or "")
        s["notes"] = (v.rstrip() + "\n\n" + note) if v else note
        log.append("note")
    after = json.dumps({k: v for k, v in s.items() if not k.startswith("_")}, sort_keys=True,
                       default=str)
    return log if before != after else []


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    specs = _mod("s12specs", "s12-screens-4-october-specs.py")
    specs.sp = sp
    for part in sorted(HERE.glob("s12-screens-4-october-specs-*.py")):   # one file per area
        exec(compile(part.read_text(encoding="utf-8"), str(part), "exec"), specs.__dict__)
    only = set(x for x in a.only.split(",") if x)
    F = spf.ScreenFiles()
    pk = sp.Package(str(ROOT), screens=F.screens)
    out = []
    for fx in specs.FIXES:
        sid = fx["sid"]
        if only and sid not in only:
            continue
        if sid not in F.screens:
            out.append(f"{sid}: NOT FOUND")
            continue
        log = apply_fix(pk, F.screens[sid], fx)
        if log:
            F.dirty.add(sid)
            out.append(f"{fx['chg']} {sid}: " + "; ".join(log))
    for fn in getattr(specs, "EDGES", ()):          # rules over many screens, and carried edges
        for sid, msg in fn(F.screens, pk):
            if only and sid not in only:
                continue
            F.dirty.add(sid)
            out.append(msg)
    print("\n".join(out) if out else "nothing to do")
    if a.apply and F.dirty:
        print("written: " + ", ".join(F.write()))
    elif F.dirty:
        print(f"{len(F.dirty)} screen(s) would change — pass --apply")
    return 0


if __name__ == "__main__":
    sys.exit(main())
