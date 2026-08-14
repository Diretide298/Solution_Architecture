#!/usr/bin/env python3
"""
Validate the screen-to-frontend linkage.

Screens declare which app implements them; everything else is derived. This checks the
things that go wrong when a route table and a screen inventory drift apart:

  1. Every app a screen names exists in the frontend repo. Four do not, and that is the
     point of the check — 73 screens are assigned to apps nobody has scaffolded.
  2. Routes are unique within an app. Two screens on one route is a bug that surfaces as
     "sometimes the wrong page loads".
  3. Component paths follow the convention, so a file can be found from a screen id and
     a screen id from a file.
  4. Offline-capable apps declare offline-core as a dependency. An app that queues writes
     without it does not queue them anywhere.

Run: python3 tools/check-frontend.py
"""
import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCREENS = ROOT / "screens"
FRONTEND = ROOT.parent / "ticvai" / "ticvai-frontend"
if not FRONTEND.exists():
    FRONTEND = ROOT.parent / "ticvai-frontend"

ERRORS: list[str] = []
WARNINGS: list[str] = []


def main() -> int:
    existing = {p.name for p in (FRONTEND / "apps").iterdir() if p.is_dir()} if (FRONTEND / "apps").exists() else set()
    packages = {p.name for p in (FRONTEND / "packages").iterdir() if p.is_dir()} if (FRONTEND / "packages").exists() else set()

    routes: dict[str, set[str]] = defaultdict(set)
    by_app: dict[str, int] = defaultdict(int)
    unscaffolded: dict[str, int] = defaultdict(int)

    for f in sorted(SCREENS.glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text())
        plat = doc["platform"]
        app = plat.get("app")
        if not app:
            ERRORS.append(f"{f.name}: platform declares no app")
            continue

        if app not in existing:
            unscaffolded[app] += len(doc["screens"])

        for pkg in plat.get("packages", []):
            if packages and pkg not in packages:
                ERRORS.append(f"{f.name}: declares package '{pkg}' which does not exist")

        if plat.get("offlineCapable") and "offline-core" not in plat.get("packages", []):
            ERRORS.append(
                f"{f.name}: {app} is offline-capable but does not depend on offline-core — "
                "an app that queues writes without it does not queue them anywhere")

        for s in doc["screens"]:
            imp = s.get("implementation")
            if not imp:
                ERRORS.append(f"{f.name}: {s['id']} has no implementation block")
                continue
            by_app[app] += 1

            route = imp.get("route", "")
            if route in routes[app]:
                ERRORS.append(f"{f.name}: {s['id']} route '{route}' collides within {app}")
            routes[app].add(route)
            if not route.startswith("/"):
                ERRORS.append(f"{f.name}: {s['id']} route '{route}' is not absolute")

            comp = imp.get("component", "")
            if not comp.startswith(f"apps/{app}/src/routes/") or not comp.endswith(".tsx"):
                ERRORS.append(f"{f.name}: {s['id']} component path '{comp}' breaks the convention")

    print(f"apps in the repo: {len(existing)} — {', '.join(sorted(existing))}\n")
    for app in sorted(by_app):
        mark = "" if app in existing else "   NOT SCAFFOLDED"
        print(f"  {app:18}{by_app[app]:>3} screens{mark}")

    if unscaffolded:
        total = sum(unscaffolded.values())
        WARNINGS.append(
            f"{total} screens across {len(unscaffolded)} apps that do not exist: "
            + ", ".join(f"{a} ({n})" for a, n in sorted(unscaffolded.items())))

    print()
    for w in WARNINGS:
        print(f"  WARN  {w}")
    for e in ERRORS:
        print(f"  FAIL  {e}")
    print()
    if ERRORS:
        print(f"{len(ERRORS)} error(s), {len(WARNINGS)} warning(s)")
        return 1
    print(f"PASS — {len(WARNINGS)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
