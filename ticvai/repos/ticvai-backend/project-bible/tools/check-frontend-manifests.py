#!/usr/bin/env python3
"""A frontend manifest says, for each platform it serves, what that platform declares.

**3 November 2026, the r13 system review F-11** (the lead, "All four, one release"; CHG-R14J-031). frontend/guest-app.yaml
serves P02 (the guest app: React Native, offline, the app stores) and P05 (the kiosk: React web, online only, a
kiosk-mode shell), and gave both `runtime: reactNative`, `offlineCapable: true` and the app stores' deployment, because
tools/derive-frontend.py took them from the app's first platform. The kiosk developer was told to build the wrong app.
derive-frontend now writes `platformProfiles` (one per platform) and an app-level value only where every platform
agrees (`mixedAcross` names the rest); this fails a manifest that says otherwise.

    FM-PLATFORM   a manifest's app-level formFactor, runtime, offlineCapable or deployment is not the one value every
                  platform it serves declares (or is present where they differ), its mixedAcross is not the keys they
                  differ on, or a platformProfiles entry is not what its platform declares in screens/P*.yaml

    python tools/check-frontend-manifests.py [--self-test]
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {"FM-PLATFORM": "a frontend manifest whose app-level or per-platform runtime, offline, deployment or form factor "
                        "is not what its platforms declare (review F-11, CHG-R14J-031)"}


def derive_module():
    spec = importlib.util.spec_from_file_location("derive_frontend", g.ROOT / "tools" / "derive-frontend.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def findings(manifests: dict, platforms_by_app: dict, mod) -> list:
    """[(app, message)]. manifests: {app: manifest dict}; platforms_by_app: {app: [platform dict, ...]}."""
    out = []
    for app, man in sorted(manifests.items()):
        plats = platforms_by_app.get(app) or []
        if not plats:
            continue
        profiles = [mod.platform_profile(p) for p in plats]
        want = mod.app_level(profiles)
        for k in mod.PER_PLATFORM:
            if man.get(k) != want[k]:
                said = "absent" if k not in man else repr(man.get(k))
                out.append((app, f"{app}: app-level {k} is {said}; its platforms "
                                 f"({', '.join(p['platform'] for p in profiles)}) declare "
                                 f"{'different values' if want[k] is None else repr(want[k])}"))
        if (man.get("mixedAcross") or None) != want["mixedAcross"]:
            out.append((app, f"{app}: mixedAcross is {man.get('mixedAcross')!r}, its platforms differ on "
                             f"{want['mixedAcross']!r}"))
        got = {str(pr.get("platform")): pr for pr in man.get("platformProfiles") or [] if isinstance(pr, dict)}
        for pr in profiles:
            if got.get(pr["platform"]) != pr:
                out.append((app, f"{app}: platformProfiles {pr['platform']} is {got.get(pr['platform'])!r}; the "
                                 f"platform declares {pr!r}"))
        extra = sorted(set(got) - {pr["platform"] for pr in profiles})
        if extra:
            out.append((app, f"{app}: platformProfiles names {', '.join(extra)}, which the app does not serve"))
    return out


def self_test(mod) -> int:
    native = {"code": "P02", "formFactor": "mobileApp", "runtime": "reactNative", "offlineCapable": True,
              "deployment": {"target": "stores"}}
    kiosk = {"code": "P05", "formFactor": "kiosk", "runtime": "reactWeb", "offlineCapable": False,
             "deployment": {"target": "kiosk shell"}}
    good = {"mixedAcross": ["formFactor", "runtime", "offlineCapable", "deployment"],
            "platformProfiles": [mod.platform_profile(native), mod.platform_profile(kiosk)]}
    first = dict(good, formFactor="mobileApp", runtime="reactNative", offlineCapable=True,
                 deployment={"target": "stores"})
    one = {"formFactor": "kiosk", "runtime": "reactWeb", "offlineCapable": False,
           "deployment": {"target": "kiosk shell"}, "platformProfiles": [mod.platform_profile(kiosk)]}
    cases = [
        ("two platforms that differ, said per platform, pass", {"a": good}, {"a": [native, kiosk]}, 0),
        ("the first platform's values at app level fail (r13's guest-app)", {"a": first}, {"a": [native, kiosk]}, 4),
        ("one platform, its values at app level, passes", {"a": one}, {"a": [kiosk]}, 0),
        ("a profile that is not its platform's fails",
         {"a": dict(one, platformProfiles=[dict(mod.platform_profile(kiosk), offlineCapable=True)])}, {"a": [kiosk]},
         1),
        ("a manifest with no profiles fails", {"a": {k: v for k, v in one.items() if k != "platformProfiles"}},
         {"a": [kiosk]}, 1),
    ]
    fails = [f"{name}: {len(got)} finding(s), expected {want}: {got}" for name, man, plats, want in cases
             for got in [findings(man, plats, mod)] if len(got) != want]
    for f in fails:
        print("  FAIL", f)
    print(f"check-frontend-manifests self-test: {len(cases) - len(fails)} of {len(cases)} passed")
    return 1 if fails else 0


def main() -> int:
    g.force_utf8()
    mod = derive_module()
    if "--self-test" in sys.argv[1:]:
        return self_test(mod)
    if self_test(mod):
        return 1
    guard = g.Guard("check-frontend-manifests", RULES)
    by_app: dict = {}
    for stem, p in g.platforms().items():
        if p.get("app") and p.get("code"):
            by_app.setdefault(p["app"], []).append(p)
    manifests = {}
    for f in sorted((g.ROOT / "frontend").glob("*.yaml")):
        man = g.load_yaml(f) or {}
        manifests[str(man.get("app") or f.stem)] = man
    for app, msg in findings(manifests, by_app, mod):
        guard.add("FM-PLATFORM", f"{app}:{msg.split(':', 2)[1].strip()[:60]}", msg)
    guard.note(f"{len(manifests)} manifest(s) against the platforms of {len(by_app)} app(s)")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
