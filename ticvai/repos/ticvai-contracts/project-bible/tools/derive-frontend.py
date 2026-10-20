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

**And the repository each platform is built in** (CHG-R6-060). Since 13 October the frontend is one GitLab
repository per app (docs/active/frontend-repos.yaml, through tools/frontend_repos.py), so each manifest carries
`repositories` (per platform: repo, repoUrl, assumed), `repo` and `repoUrl` when every platform of the app is
built in one repository (null otherwise, or when there is none yet), and its screens with their path relative to
that repository (`path`), not the `apps/<app>/` folder of the old single workspace. The screen list, `screenCount`
and `byWave` are derived from the screens on every run; until now they were carried over from the previous file
and had drifted (audit-guest-parity's "frontend manifest" finding).
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

import yaml


def _yload(src):
    """YAML with the C loader, the pure one where a file defeats it (20 October 2026, CHG-R8GEN-016): the screen files
    are 25 MB and the pure loader took most of each refresh step's minute; the loaded data is the same."""
    text = src.read() if hasattr(src, "read") else src
    try:
        return yaml.load(text, Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader))
    except Exception:
        return yaml.safe_load(text)

sys.path.insert(0, str(Path(__file__).resolve().parent))
import frontend_repos as fr  # noqa: E402

# Windows consoles are cp1252 and this tool closes by printing a unicode arrow. **The write
# has already happened by then**, so the traceback reported a failure on a run that succeeded
# — the most misleading shape an error can take.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
SCREENS = ROOT / "screens"
FRONTEND = ROOT / "frontend"
HANDOFF = ROOT / "handoff"


def main() -> int:
    lineage = json.loads((HANDOFF / "api-data-lineage.json").read_text(encoding="utf-8"))

    apps: dict[str, dict] = {}
    for f in sorted(SCREENS.glob("P*.yaml")):
        doc = _yload(f.read_text(encoding="utf-8"))
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
            "screens": [],
        })
        entry["offlineCapable"] = entry["offlineCapable"] or bool(p.get("offlineCapable"))
        entry["directions"] |= set(p.get("directions") or [])
        entry["platforms"].append(f"{p['code']} {p['name']}")
        entry.setdefault("_codes", []).append(p["code"])
        repo = fr.repo_of(p["code"])
        for s in doc["screens"]:
            imp = s.get("implementation") or {}
            row = {"id": s["id"], "name": s.get("name"), "platform": p["code"], "route": imp.get("route"),
                   "repo": repo}
            if repo and imp.get("component"):
                row["path"] = fr.relative_path(imp["component"], app)
            row["wave"] = s.get("wave")
            if imp.get("status"):
                row["status"] = imp["status"]
            entry["screens"].append(row)
            for a in (s.get("apis") or []):
                oid = a.get("operationId")
                if oid in lineage:
                    entry["contracts"].add(lineage[oid]["contract"])

    written = 0
    for app, e in sorted(apps.items()):
        e["directions"] = sorted(e["directions"]) or ["ltr"]
        e["contracts"] = sorted(e["contracts"])
        e["servesMultiplePlatforms"] = len(e["platforms"]) > 1
        codes = e.pop("_codes")
        e["repositories"] = [{"platform": c, "repo": fr.repo_of(c), "repoUrl": fr.url_of(fr.repo_of(c)),
                              "assumed": bool(fr.platform_entry(c).get("assumed"))} for c in codes]
        one = {r["repo"] for r in e["repositories"]}
        e["repo"] = next(iter(one)) if len(one) == 1 else None
        e["repoUrl"] = fr.url_of(e["repo"])
        e["screenCount"] = len(e["screens"])
        waves = defaultdict(int)
        for s in e["screens"]:
            waves[f"wave{s['wave']}" if s.get("wave") is not None else "unwaved"] += 1
        e["byWave"] = dict(sorted(waves.items()))
        # **The package set is not derived and is not invented here.** An existing manifest's
        # choice is preserved; a new app gets the three every app needs. Guessing which packages
        # a team will split out is not something a screen file can answer.
        path = FRONTEND / f"{app}.yaml"
        existing = _yload(path.read_text(encoding="utf-8")) if path.exists() else {}
        e["packages"] = existing.get("packages") or ["design-tokens", "ui", "api-client"]
        for k, v in existing.items():
            e.setdefault(k, v)

        ordered = {k: e[k] for k in (
            "app", "operator", "audience", "formFactor", "status", "runtime", "offlineCapable",
            "directions", "platforms", "servesMultiplePlatforms", "repo", "repoUrl", "repositories",
            "packages", "contracts", "deployment", "screenCount", "byWave", "screens")
            if e.get(k) is not None or k in ("repo", "repoUrl")}
        for k, v in e.items():
            ordered.setdefault(k, v)

        repos = "; ".join(f"{r['platform']} {r['repo'] or 'none yet (ask the lead)'}" for r in e["repositories"])
        head = (f"# {app} — operated by {e['operator']} · {e['audience']} on {e['formFactor']}\n"
                f"# Serves: {', '.join(e['platforms'])}\n"
                f"# Repository: {repos} (docs/active/frontend-repos.yaml)\n"
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
