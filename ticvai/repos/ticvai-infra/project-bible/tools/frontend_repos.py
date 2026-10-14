#!/usr/bin/env python3
"""Which GitLab repository a screen is built in, and where in it: docs/active/frontend-repos.yaml (CHG-R6-059).

The screens were written against one Nx workspace, so `implementation.component` reads
`apps/venue-pos/src/routes/shift/BeginShiftWizard.tsx`. Since 13 October the frontend is one repository per app in
the GitLab group ticvai-frontend, and no `apps/<app>/` folder exists. The screens keep their authored path; every
generator that writes ticket text goes through here instead, so a ticket names the repository of its screen's
platform and a path relative to that repository, or says there is no repository yet.

The repository's inside is not known (nobody on the package team can read GitLab), so the path is a *suggested*
location: the root of the repository is assumed to hold what `apps/<app>/` held.

**Since 14 October each repository has a profile** (CHG-RPO-001..003, the Block A audit): what was observed in it,
over `layout.default`, with anything nobody observed named as assumed (profile()). The screens' component paths are
written from it (component_path(), applied by tools/apply-repo-layout.py), and so are a screen ticket's build gate
(gate_line()), the location wording (layout_note()) and ADAM setup's per-repository table (setup_block()).

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


PROFILE_FIELDS = ("stack", "workspace", "packageManager", "state", "navigation", "appRoot", "srcRoot", "screensDir",
                  "packages", "scripts")
OLD_SCREEN_DIR = re.compile(r"^apps/[a-z0-9-]+/src/routes/")


def profile(code: str) -> dict:
    """The layout generators write a platform's repository against (CHG-RPO-001, CHG-RPO-002).

    `layout.default` in frontend-repos.yaml, overlaid by what was observed in the repository (when it could be read)
    and then by the entry's own `profile:` (values nobody observed). Returns the fields of PROFILE_FIELDS plus
    `repo`, `read` (the repository's inside was read), `observedBy`, `observedDate`, `confirmed` and `assumed`: the
    fields whose value nobody observed. {} for a platform with no repository."""
    e = (mapping().get("platforms") or {}).get(str(code)[:3]) or {}
    if not e.get("repo"):
        return {}
    base = dict(((mapping().get("layout") or {}).get("default")) or {})
    obs = e.get("observed") if isinstance(e.get("observed"), dict) else {}
    read = bool(obs.get("reachable"))
    seen = {k: obs[k] for k in PROFILE_FIELDS if read and k in obs}
    own = {k: v for k, v in (e.get("profile") or {}).items() if k in PROFILE_FIELDS}
    out = {k: base.get(k) for k in PROFILE_FIELDS}
    out.update(seen)
    out.update(own)
    out["scripts"] = dict(base.get("scripts") or {}, **(seen.get("scripts") or {}), **(own.get("scripts") or {}))
    out.update({"repo": e["repo"], "read": read, "observedBy": obs.get("by"), "observedDate": obs.get("date"),
                "confirmed": bool(obs.get("confirmed")),
                "assumed": [k for k in PROFILE_FIELDS if k not in seen or k in own]})
    return out


def component_tail(component: str | None) -> str | None:
    """`<area>/<Component>.tsx` (or `<Component>.tsx`) of a component path, whichever layout wrote it: the old
    workspace's apps/<app>/src/routes/, or any profile's screensDir. None when the path has neither."""
    c = str(component or "")
    m = OLD_SCREEN_DIR.match(c)
    if m:
        return c[m.end():]
    dirs = {str(((mapping().get("layout") or {}).get("default") or {}).get("screensDir") or "src/routes")}
    for e in (mapping().get("platforms") or {}).values():
        if isinstance(e, dict) and (e.get("profile") or {}).get("screensDir"):
            dirs.add(str(e["profile"]["screensDir"]))
    for d in sorted(dirs, key=len, reverse=True):
        if c.startswith(d.rstrip("/") + "/"):
            return c[len(d.rstrip("/")) + 1:]
    return None


def component_path(code: str, component: str | None) -> str | None:
    """**The generator rule for a screen's component path** (CHG-RPO-002): `<screensDir>/<area>/<Component>.tsx`,
    relative to the root of the platform's repository, from its profile. A platform with no repository keeps the
    authored path (it is built nowhere yet, or in the one-workspace starter). tools/apply-repo-layout.py writes it
    into screens/P*.yaml; check-frontend-repos (FR-OLD-PATH) and check-frontend hold every screen to it."""
    p = profile(code)
    tail = component_tail(component)
    if not p or not tail:
        return component
    return f"{str(p.get('screensDir') or 'src/routes').rstrip('/')}/{tail}"


def gate_line(code: str) -> str:
    """The Done-when item for a screen ticket's own build gates, from its repository's profile (CHG-RPO-003).

    No repository: the one-workspace starter's `pnpm lint`, `pnpm typecheck` and `pnpm test`. A repository read
    (observed): its package manager, and the scripts it lacks named as lacking, never invented. A repository not
    read: its own scripts, with the package manager its lock file belongs to. Every form ends "scripts pass" or
    names pnpm, so check-ticket-text counts it as the generic gate it is."""
    p = profile(code)
    if not p:
        return "- [ ] `pnpm lint`, `pnpm typecheck` and `pnpm test` pass"
    if not p["read"]:
        return (f"- [ ] {p['repo']}'s own lint, typecheck and test scripts pass, run inside its folder with the package "
                f"manager its lock file belongs to (its layout has not been read yet)")
    sc = p.get("scripts") or {}
    have = [k for k in ("lint", "typecheck", "test") if sc.get(k) not in ("none", None, False)]
    lack = [k for k in ("lint", "typecheck", "test") if sc.get(k) in ("none", False)]
    s = (f"- [ ] {p['repo']}'s own {', '.join(have[:-1]) + ' and ' + have[-1] if len(have) > 1 else ''.join(have)} "
         f"scripts pass, run with {p.get('packageManager')} inside its folder as its package.json names them")
    if lack:
        s += f" (it has no {' or '.join(lack)} script, so none is run)"
    return s


def describe(code: str) -> dict:
    """One repository's profile as plain text cells: how it is known, stack, package manager, where screens go and
    the scripts (CHG-RPO-003). ADAM setup's frontend CLAUDE.md table is built from these (setup_block)."""
    p = profile(code)
    if not p:
        return {}
    known = (f"observed {p['observedDate']} by {p['observedBy']}" if p["read"] else
             f"not read: the clone of {p['observedDate'] or 'the audit'} was refused; assumed")
    assumed = [NAMES[k] for k in p["assumed"] if k in NAMES]
    if p["read"] and assumed:
        known += f" (assumed: the {', '.join(assumed)})"
    known += "; owner confirms" if not p["confirmed"] else "; confirmed by its owner"
    pk = p.get("packages")
    stack = (str(p.get("stack") or "") if p["read"] else
             f"assumed: {runtimes().get(str(code)[:3]) or '?'} (the package's runtime)")
    extra = [str(p[k]) for k in ("state", "navigation") if p.get(k)]
    if extra:
        stack += "; " + ", ".join(extra)
    if p.get("workspace") not in (None, "unknown"):
        stack += f"; workspace: {p['workspace']}"
    if isinstance(pk, list):
        stack += "; shared packages: " + (", ".join(pk) if pk else "none")
    sc = p.get("scripts") or {}
    scripts = ", ".join(f"{k} {v}" for k, v in sc.items() if v not in (None, "unknown")) or "as its package.json says"
    if any(v in (None, "unknown") for v in sc.values()) and scripts != "as its package.json says":
        scripts += "; the rest as its package.json says"
    return {"repo": p["repo"], "known": known, "stack": stack, "packageManager": str(p.get("packageManager")),
            "screens": f"`{str(p.get('screensDir')).rstrip('/')}/<area>/<Component>.tsx`"
                       + (" (assumed)" if "screensDir" in p["assumed"] else ""), "scripts": scripts}


NAMES = {"screensDir": "screens folder", "srcRoot": "source folder", "packageManager": "package manager",
         "workspace": "workspace"}


@lru_cache(maxsize=1)
def runtimes() -> dict:
    """{platform code: platform.runtime} from screens/P*.yaml (the package's stack for a repository not read)."""
    out = {}
    for f in sorted(SCREENS.glob("P*.yaml")):
        head = f.read_text(encoding="utf-8").split("\nscreens:", 1)[0]
        p = (yaml.safe_load(head) or {}).get("platform") or {}
        if p.get("code"):
            out[str(p["code"])] = p.get("runtime")
    return out


SETUP_BEGIN = ("<!-- frontend-repos profile: generated by tools/apply-repo-layout.py "
               "from docs/active/frontend-repos.yaml -->")
SETUP_END = "<!-- end of frontend-repos profile -->"


def setup_block() -> str:
    """The section ADAM setup's frontend CLAUDE.md carries between SETUP_BEGIN and SETUP_END (CHG-RPO-003)."""
    rows = []
    for code in sorted((mapping().get("platforms") or {})):
        d = describe(code)
        if d:
            rows.append(f"| `{d['repo']}` ({code}) | {d['known']} | {d['stack']} | {d['packageManager']} | "
                        f"{d['screens']} | {d['scripts']} |")
    return "\n".join([
        SETUP_BEGIN,
        "**What each repository holds**, as ADAM's package records it. A screen's `implementation.component` is the",
        "path in its repository, written from this profile. Where a row says *assumed*, nobody on the package team",
        "has read that part of the repository: look at the repository first, follow what it really has, and tell",
        "the lead where it differs (a change request), so the profile and every screen path are corrected for all.",
        "",
        "| Repository | How it is known | Stack | Package manager | Screens go in | Scripts |",
        "|---|---|---|---|---|---|",
        *rows,
        SETUP_END,
    ])


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


def layout_note(code: str | None) -> str:
    """How far the path can be trusted, from the repository's profile (CHG-RPO-003): observed, partly assumed, or
    not read. One clause, no markdown."""
    p = profile(code or "")
    wording = mapping()["layout"]["wording"]
    if not p:
        return wording
    if not p["read"]:
        return f"assumed: the repository's layout has not been read yet; {wording}"
    seen = f"its layout as observed {p['observedDate']}: {p.get('stack')}, {p.get('packageManager')}, {p.get('srcRoot')}/"
    guess = [NAMES[k] for k in p["assumed"] if k in ("screensDir", "srcRoot")]
    return seen + (f"; the {' and '.join(guess)} is assumed, {wording}" if guess else "")


def location_sentence(w: dict) -> str:
    """The route, the component and (with a repository) the suggested location, one line, no markdown."""
    bits = []
    if w.get("route"):
        bits.append(f"route `{w['route']}`")
    if w.get("componentName"):
        bits.append(f"component `{w['componentName']}`")
    if w.get("repo") and w.get("path"):
        bits.append(f"suggested location `{w['path']}` in {w['repo']} ({layout_note(w.get('platform'))})")
    return "; ".join(bits)
