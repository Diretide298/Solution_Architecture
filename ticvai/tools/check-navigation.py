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
  N-SIGNIN-RETURN a guest screen whose no-access state "is offered sign-in and brought back" has the edge the
                  `guestSignInReturn` rule of screens/_patterns.yaml implies: the rule is declared, and the app's
                  sign-in screen (P01 WEB-016, P02 GST-042) takes `returnTo` and `returnParams` from navigation

**The sign-in edge is a rule's, not each screen's** (r8 integration, CHG-R8INT-006; WHITE-C13, the surface lane's
request). 82 guest screens say their no-access state offers sign-in and brings the guest back; drawing that edge on
each would change approved navigation, so `screens/_patterns.yaml` `meta.rules` `guestSignInReturn` states it once.
This check reads the rule as an edge from each such screen to its app's sign-in screen carrying `returnTo` (the
screen's own id, which it always holds) and `returnParams`, and fails when the rule or the sign-in screen's two
parameters are missing. It never asks for the edge to be written into a screen.

Read-only. Exit 1 on a finding not in `handoff/audit-baseline.json` (see tools/audit_guard.py).

    python3 tools/check-navigation.py [--all] [--update-baseline]
"""
import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {
    "N-ENTRY-MIRROR": "entryFrom parent does not list the child in exitTo (R251)",
    "N-CARRIES-HELD": "a transition carries an id the source screen does not hold (R251 R262)",
    "N-TWIN-WAVE": "guest web and app twins ship in different waves, unsanctioned (R281)",
    "N-TWIN-OPS": "guest web and app twins call different operations, unsanctioned (R281)",
    "N-SIGNIN-RETURN": "a guest screen offers sign-in and return, and the guestSignInReturn rule or the sign-in "
                       "screen's returnTo/returnParams is missing (WHITE-C13, CHG-R8INT-006)",
}
SIGNIN = {"P01": "WEB-016", "P02": "GST-042"}
SIGNIN_PHRASE = "offered sign-in and brought back"


def signin_return(screens: dict, plat_of: dict, rules: list) -> tuple:
    """(findings as (key, message), implied edges as (from, to)) for the guestSignInReturn rule."""
    found, edges = [], []
    has_rule = any(isinstance(r, dict) and r.get("id") == "guestSignInReturn" for r in rules or [])
    for sid, s in sorted(screens.items()):
        if SIGNIN_PHRASE not in str((s.get("states") or {}).get("emptyNoAccess") or ""):
            continue
        code = str(plat_of.get(sid) or "")[:3]
        target = SIGNIN.get(code)
        if not target:
            found.append((sid, f"{sid} offers sign-in and return, but {code or 'its app'} has no guest sign-in "
                               f"screen the guestSignInReturn rule names (P01 WEB-016, P02 GST-042)"))
            continue
        if not has_rule:
            found.append((sid, f"{sid} offers sign-in and return, and screens/_patterns.yaml declares no "
                               f"meta.rules guestSignInReturn to draw the edge to {target}"))
            continue
        t = screens.get(target) or {}
        params = {p.get("name"): p for p in ((t.get("entryState") or {}).get("params") or []) if isinstance(p, dict)}
        missing = [n for n in ("returnTo", "returnParams")
                   if n not in params or params[n].get("from") != "navigation"]
        if missing:
            found.append((f"{target}:{','.join(missing)}",
                          f"{target} is the sign-in screen the guestSignInReturn rule sends {sid} to, and does not "
                          f"take {' and '.join(missing)} from navigation"))
            continue
        edges.append((sid, target))
    return found, edges


def self_test() -> list:
    """signin_return on made-up screens: the rule and the sign-in parameters make an edge; each missing piece fails."""
    rule = [{"id": "guestSignInReturn"}]
    sign = {"id": "WEB-016", "entryState": {"params": [{"name": "returnTo", "from": "navigation"},
                                                       {"name": "returnParams", "from": "navigation"}]}}
    guest = {"id": "WEB-019", "states": {"emptyNoAccess": "A signed-out guest is offered sign-in and brought back."}}
    plat = {"WEB-016": "P01-guest-web-storefront", "WEB-019": "P01-guest-web-storefront",
            "BO-001": "P08-venue-back-office"}
    bad = []
    f, e = signin_return({"WEB-016": sign, "WEB-019": guest}, plat, rule)
    if f or e != [("WEB-019", "WEB-016")]:
        bad.append(f"the rule and both parameters: expected one edge and no finding, got {f} {e}")
    f, _ = signin_return({"WEB-016": sign, "WEB-019": guest}, plat, [])
    if len(f) != 1:
        bad.append(f"no rule declared: expected one finding, got {f}")
    f, _ = signin_return({"WEB-016": {"id": "WEB-016"}, "WEB-019": guest}, plat, rule)
    if len(f) != 1 or "returnTo and returnParams" not in f[0][1]:
        bad.append(f"sign-in screen without the parameters: expected one finding, got {f}")
    f, _ = signin_return({"BO-001": dict(guest, id="BO-001")}, plat, rule)
    if len(f) != 1:
        bad.append(f"a staff screen with the sentence: expected one finding, got {f}")
    f, e = signin_return({"WEB-016": sign, "WEB-019": dict(guest, states={})}, plat, rule)
    if f or e:
        bad.append(f"a screen without the sentence: expected nothing, got {f} {e}")
    return bad


def _deriver():
    """`derive-carries-from-entrystate.py`, loaded as it is.

    **No YAML shim any more** (r8 integration, CHG-R8INT-006). The check used to swap the deriver's `yaml` for one
    whose `safe_load(fh)` read `fh.name` through the fast loader; since CHG-R8GEN-016 the deriver loads with the C
    loader itself and hands `yaml` the text, not the file, so the shim failed ("'str' object has no attribute
    'name'") and N-CARRIES-HELD reported the deriver unavailable instead of checking anything."""
    path = Path(__file__).resolve().parent / "derive-carries-from-entrystate.py"
    spec = importlib.util.spec_from_file_location("derive_carries", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    g.force_utf8()
    tests = self_test()
    for x in tests:
        print(f"  SELF-TEST  {x}")
    if tests:
        print(f"FAIL {len(tests)} self-test(s)")
        return 1
    if "--self-test" in sys.argv:
        print("PASS - the N-SIGNIN-RETURN self-tests")
        return 0
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

    rules = ((g.load_yaml(g.SCREENS / "_patterns.yaml") or {}).get("meta") or {}).get("rules") or []
    found, edges = signin_return(screens, plat_of, rules)
    for key, msg in found:
        guard.add("N-SIGNIN-RETURN", key, msg)
    print(f"  note: {len(edges)} sign-in-and-return edge(s) implied by the guestSignInReturn rule")

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
