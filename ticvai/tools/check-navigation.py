#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Navigation that was inferred, read back against what each end of the edge holds.

**Audit class A-SCREEN-NAV (docs/active/root-classes.md), roots R251, R262, R281, R287.** Exit
lists came from module nav-sets and `carries` was copied from the destination's params without
asking whether the source had them, so a Stock Count "carried" `eventId`, `feedId` and `queueId`
into a Queue Directory; a child's `entryFrom` named a parent whose `exitTo` did not name the
child; and guest web and app twins drifted apart in wave and operations after they were decided to
be one product (12 September). `derive-carries-from-entrystate.py` was fixed on 27 September and
`check-screens.py` checks only that targets exist. This checks the edges themselves:

  N-ENTRY-MIRROR  a screen's `entryFrom` parent names it in `exitTo` (same platform)
  N-CARRIES-HELD  every id a transition carries is one the source screen holds -- declared,
                  preloaded, or read off one of its own operations (the deriver's own `holds()`)
  N-TWIN-WAVE     a paired guest group ships in one wave on web and app, unless sanctioned
  N-TWIN-OPS      a paired guest group calls the same operations on web and app, unless sanctioned

Read-only. Exit 1 on a finding not in `handoff/audit-baseline.json` (see tools/audit_guard.py).

    python3 tools/check-navigation.py [--all] [--update-baseline]
"""
import importlib.util
import sys
import types
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {
    "N-ENTRY-MIRROR": "entryFrom parent does not list the child in exitTo (R251)",
    "N-CARRIES-HELD": "a transition carries an id the source screen does not hold (R251 R262)",
    "N-TWIN-WAVE": "guest web and app twins ship in different waves, unsanctioned (R281)",
    "N-TWIN-OPS": "guest web and app twins call different operations, unsanctioned (R281)",
}


def _deriver():
    """`derive-carries-from-entrystate.py`, with its YAML reads routed through the fast loader."""
    path = Path(__file__).resolve().parent / "derive-carries-from-entrystate.py"
    spec = importlib.util.spec_from_file_location("derive_carries", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    shim = types.SimpleNamespace(safe_load=lambda fh: g.load_yaml(fh.name))
    mod.yaml = shim
    return mod


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-navigation", RULES)
    plat_of = {}
    screens = {}
    for plat, s in g.screens():
        screens[s["id"]] = s
        plat_of[s["id"]] = plat

    for sid, s in screens.items():
        for parent in ((s.get("navigation") or {}).get("entryFrom") or []):
            p = screens.get(parent)
            if not p or parent == sid or plat_of[parent] != plat_of[sid]:
                continue
            if sid not in ((p.get("navigation") or {}).get("exitTo") or []):
                guard.add("N-ENTRY-MIRROR", f"{parent}->{sid}",
                          f"{sid} is entered from {parent}, and {parent}.exitTo does not name {sid}")

    try:
        d = _deriver()
        contracts = d.Contracts()
        for sid, s in screens.items():
            held = None
            for t in ((s.get("navigation") or {}).get("transitions") or []):
                if not isinstance(t, dict) or not t.get("carries"):
                    continue
                if held is None:
                    held = d.holds(s, contracts)
                dst = d.base(t.get("to"))
                for name in t.get("carries") or []:
                    if name not in held:
                        guard.add("N-CARRIES-HELD", f"{sid}->{dst}:{name}",
                                  f"{sid} -> {dst} carries {name}, which {sid} neither declares, "
                                  f"preloads nor reads")
    except Exception as e:  # the deriver moved; say so rather than pass silently
        guard.add("N-CARRIES-HELD", "deriver-unavailable",
                  f"could not load derive-carries-from-entrystate.holds(): {e}")

    pairs = g.load_yaml(g.SCREENS / "_guest-pairs.yaml") or {}
    for grp in pairs.get("groups") or []:
        if grp.get("kind") != "paired":
            continue
        key = grp.get("key")
        sanctioned = grp.get("sanctioned") or {}
        web = [screens[x] for x in grp.get("web") or [] if x in screens]
        app = [screens[x] for x in grp.get("app") or [] if x in screens]
        if not web or not app:
            continue
        ww = min(int(x.get("wave") or 99) for x in web)
        aw = min(int(x.get("wave") or 99) for x in app)
        if ww != aw and "wave" not in sanctioned:
            guard.add("N-TWIN-WAVE", key, f"guest group {key}: web wave {ww}, app wave {aw}")
        wo = {a.get("operationId") for x in web for a in (x.get("apis") or []) if isinstance(a, dict)}
        ao = {a.get("operationId") for x in app for a in (x.get("apis") or []) if isinstance(a, dict)}
        if wo != ao and not ({"operations", "apis", "ops"} & set(sanctioned)):
            diff = sorted((wo ^ ao) - {None})
            guard.add("N-TWIN-OPS", key, f"guest group {key}: {len(diff)} operation(s) on one shell "
                                         f"only, e.g. {', '.join(diff[:4])}")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
