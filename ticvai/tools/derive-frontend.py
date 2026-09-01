#!/usr/bin/env python3
"""Derive frontend/<app>.yaml from screens/*.yaml.

Every manifest carries the line **"Derived from screens/*.yaml. Do not hand-edit."** and until
18 August nothing derived them. Adding P14 broke `check-package` because the app existed in the
screens and not in the manifests, and the fix was to hand-write the file the header forbids
hand-writing.

**A header that lies about how a file is maintained is worse than no header** — it tells the next
person not to edit the thing they now have to edit.

Everything here comes from the screens: which platforms an app serves, which contracts it reaches
through their operations, which packages it needs, and the deployment posture the platform
declares.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCREENS = ROOT / "screens"
FRONTEND = ROOT / "frontend"
HANDOFF = ROOT / "handoff"


def main() -> int:
    lineage = json.loads((HANDOFF / "api-data-lineage.json").read_text(encoding="utf-8"))

    apps: dict[str, dict] = {}
    for f in sorted(SCREENS.glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        p = doc["platform"]
        app = p.get("app")
        if not app:
            continue
        entry = apps.setdefault(app, {
            "app": app,
            "operator": p.get("operator", p.get("audience")),
            "audience": p.get("audience"),
            "formFactor": p.get("formFactor"),
            "status": p.get("appStatus", "not scaffolded"),
            "runtime": p.get("runtime"),
            "offlineCapable": False,
            "directions": set(),
            "platforms": [],
            "contracts": set(),
            "deployment": p.get("deployment"),
        })
        entry["offlineCapable"] = entry["offlineCapable"] or bool(p.get("offlineCapable"))
        entry["directions"] |= set(p.get("directions") or [])
        entry["platforms"].append(f"{p['code']} {p['name']}")
        for s in doc["screens"]:
            for a in (s.get("apis") or []):
                oid = a.get("operationId")
                if oid in lineage:
                    entry["contracts"].add(lineage[oid]["contract"])

    written = 0
    for app, e in sorted(apps.items()):
        e["directions"] = sorted(e["directions"]) or ["ltr"]
        e["contracts"] = sorted(e["contracts"])
        e["servesMultiplePlatforms"] = len(e["platforms"]) > 1
        # **The package set is not derived and is not invented here.** An existing manifest's
        # choice is preserved; a new app gets the three every app needs. Guessing which packages
        # a team will split out is not something a screen file can answer.
        path = FRONTEND / f"{app}.yaml"
        existing = yaml.safe_load(path.read_text(encoding="utf-8")) if path.exists() else {}
        e["packages"] = existing.get("packages") or ["design-tokens", "ui", "api-client"]
        for k, v in existing.items():
            e.setdefault(k, v)

        ordered = {k: e[k] for k in (
            "app", "operator", "audience", "formFactor", "status", "runtime", "offlineCapable",
            "directions", "platforms", "servesMultiplePlatforms", "packages", "contracts",
            "deployment") if e.get(k) is not None}
        for k, v in e.items():
            ordered.setdefault(k, v)

        head = (f"# {app} — operated by {e['operator']} · {e['audience']} on {e['formFactor']}\n"
                f"# Serves: {', '.join(e['platforms'])}\n"
                f"# Derived by tools/derive-frontend.py from screens/*.yaml. Do not hand-edit.\n\n")
        path.write_text(head + yaml.safe_dump(ordered, sort_keys=False, allow_unicode=True, width=98),
                        encoding="utf-8")
        written += 1

    stale = sorted(p.stem for p in FRONTEND.glob("*.yaml") if p.stem not in apps)
    print(f"  {written} app manifest(s) derived from {len(list(SCREENS.glob('P*.yaml')))} platforms")
    if stale:
        print(f"  {len(stale)} manifest(s) for apps no screen declares: {', '.join(stale)}")
    print("  → frontend/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
