#!/usr/bin/env python3
"""Which GitLab repository a screen is built in, and where in it: docs/active/frontend-repos.yaml (CHG-R6-059).

The screens were written against one Nx workspace, so `implementation.component` reads
`apps/venue-pos/src/routes/shift/BeginShiftWizard.tsx`. Since 13 October the frontend is one repository per app in
the GitLab group ticvai-frontend, and no `apps/<app>/` folder exists. The screens keep their authored path; every
generator that writes ticket text goes through here instead, so a ticket names the repository of its screen's
platform and a path relative to that repository, or says there is no repository yet.

The repository's inside is not known (nobody on the package team can read GitLab), so the path is a *suggested*
location: the root of the repository is assumed to hold what `apps/<app>/` held.

Used by derive-frontend.py, op-descriptions.py, op-release.py, build-service-docs.py, check-ticket-text.py and
check-frontend-repos.py.
"""
from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MAPPING = ROOT / "docs" / "active" / "frontend-repos.yaml"
SCREENS = ROOT / "screens"
OLD_APP_PATH = re.compile(r"(?<![\w.-])apps/([a-z0-9-]+)/")   # a folder of the old one-workspace layout
SCREEN_ID = re.compile(r"\b[A-Z]{2,5}-\d{3,4}\b")


@lru_cache(maxsize=1)
def mapping() -> dict:
    return yaml.safe_load(MAPPING.read_text(encoding="utf-8")) or {}


def url_of(repo: str | None) -> str | None:
    return mapping()["url"].format(repo=repo) if repo else None


def platform_entry(code: str) -> dict:
    """The entry for a platform code (P04), with its url; {} when the platform is not listed."""
    e = dict((mapping().get("platforms") or {}).get(str(code)[:3]) or {})
    if e:
        e["code"] = str(code)[:3]
        e["url"] = url_of(e.get("repo"))
    return e


def repo_of(code: str) -> str | None:
    return platform_entry(code).get("repo")


def relative_path(component: str | None, app: str | None = None) -> str:
    """The authored component path without its old app folder: apps/venue-pos/src/x.tsx -> src/x.tsx."""
    c = str(component or "")
    if app and c.startswith(f"apps/{app}/"):
        return c[len(f"apps/{app}/"):]
    return OLD_APP_PATH.sub("", c, count=1) if c.startswith("apps/") else c


def component_name(component: str | None) -> str:
    """The component's own name, with no folder: apps/venue-pos/src/routes/shift/BeginShiftWizard.tsx -> BeginShiftWizard."""
    return Path(str(component or "")).stem


@lru_cache(maxsize=1)
def screen_index() -> dict:
    """{screen id: {platform, app, route, component}} from screens/P*.yaml."""
    out = {}
    for f in sorted(SCREENS.glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        p = doc.get("platform") or {}
        for s in doc.get("screens") or []:
            if isinstance(s, dict) and s.get("id"):
                imp = s.get("implementation") or {}
                out[s["id"]] = {"platform": p.get("code"), "app": imp.get("app") or p.get("app"),
                                "route": imp.get("route"), "component": imp.get("component")}
    return out


def screen_of_ticket(key: str, subject: str = "") -> str | None:
    """The screen a frontend ticket builds: the id its key ends in (APP-POS-POS-001, VM-BO-102-REST), else the first
    known screen its subject names (APP-KIOSK-CONFIG names KSK-001; VM-FE-ADM-582-KIOSK names ADM-582)."""
    idx = screen_index()
    m = re.search(r"([A-Z]+-\d{3,4})(?:-REST)?$", key.partition("#")[0])
    if m and m.group(1) in idx:
        return m.group(1)
    for sid in SCREEN_ID.findall(subject or ""):
        if sid in idx:
            return sid
    return None


def where(sid: str) -> dict:
    """Everything a ticket says about where screen `sid` is built."""
    s = screen_index().get(sid) or {}
    e = platform_entry(s.get("platform") or "")
    comp = s.get("component")
    return {"screen": sid, "platform": e.get("code") or s.get("platform"), "platformName": e.get("name"),
            "app": s.get("app"), "repo": e.get("repo"), "url": e.get("url"), "assumed": bool(e.get("assumed")),
            "route": s.get("route"), "componentName": component_name(comp) if comp else None,
            "path": relative_path(comp, s.get("app")) if comp and e.get("repo") else None}


def repo_sentence(w: dict) -> str:
    """'Repository: ticvai-pos (url)' or 'No repository yet: ask the lead ...', one line, no markdown."""
    if w.get("repo"):
        s = f"Repository: {w['repo']} ({w['url']})"
        if w.get("assumed"):
            s += f"; {w['platform']} is mapped to it by the lead's assumption, not yet confirmed"
        return s
    return (f"No repository yet: ask the lead. {w.get('platform') or 'This platform'} "
            f"{w.get('platformName') or ''} has no repository in the {mapping()['group']} group, so build it nowhere "
            "until the lead names one.").replace("  ", " ")


def location_sentence(w: dict) -> str:
    """The route, the component and (with a repository) the suggested location, one line, no markdown."""
    bits = []
    if w.get("route"):
        bits.append(f"route `{w['route']}`")
    if w.get("componentName"):
        bits.append(f"component `{w['componentName']}`")
    if w.get("repo") and w.get("path"):
        bits.append(f"suggested location `{w['path']}` in {w['repo']} ({mapping()['layout']['wording']})")
    return "; ".join(bits)
