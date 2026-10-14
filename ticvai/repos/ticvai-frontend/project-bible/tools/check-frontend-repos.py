#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every frontend platform and app has its repository entry, and ADAM setup names the same repositories.

**13 October 2026** (CHG-R6-059). The frontend became one GitLab repository per app in the group
ticvai-frontend, and the tickets still named folders of the old single Nx workspace (`apps/venue-pos/...`). The
mapping from a platform to its repository is authored once, in `docs/active/frontend-repos.yaml`, and the ticket
generators read it through `tools/frontend_repos.py`. This checks that root:

    FR-PLATFORM-MISSING  a platform in screens/P*.yaml has no entry, or an entry names a platform no screen file has
    FR-APP-MISSING       an app with a frontend/*.yaml manifest (or a platform's app) is on no entry
    FR-APP-MISMATCH      an entry's app is not the app its platform's screen file declares
    FR-REPO-TWICE        one repository is mapped to two platforms with no `shared` reason on each
    FR-FIELDS            a repository entry with no `assumed: true|false`, a repository name outside the group's
                         ticvai-<name> form, or no `url` template naming {repo}
    FR-SETUP-TABLE       viewer/mcp/setup/starters/frontend/CLAUDE.md (the table ADAM setup gives a developer) names
                         another repository for a platform, or one the root does not have

**14 October 2026, CHG-SWP-003** (the sweep after #27741). The developer's agent on the guest app found
ticvai-guest-app a single React Native CLI app at the repository root, on npm, with `src/`; ADAM's screen said
`apps/guest-app/src/routes/...` (the Nx/pnpm workspace) and the package names workspace packages (design-tokens,
ui, api-client, offline-core) the repository does not have. What a repository really holds is recorded on its
entry as `observed:` (`by`, `date`, `workspace: none|nx`, `packageManager`, `srcRoot`, `packages: [...]`); what
the package says about it is the screens' `implementation.component`, the platform's `packages` and the suggested
location frontend_repos.py derives. These read one against the other:

    FR-OLD-PATH          a screen on a platform with a repository names its component under apps/<app>/, the
                         one-workspace layout, and ADAM serves the screen as written
    FR-LAYOUT-UNCONFIRMED a platform's repository has no `observed:` layout while frontend-repos.yaml says the layout
                         is assumed: every location its tickets suggest is a guess
    FR-LAYOUT-MISMATCH   an `observed:` layout contradicts the package: the suggested locations are not under its
                         `srcRoot`, the platform names a shared package the repository does not have, or the
                         repository is no Nx workspace while a screen path still names apps/<app>/

**14 October 2026, CHG-RPO-001..003** (the Block A audit, the lead's decision 3: layouts are read from the
repositories and recorded as observed; owners confirm afterwards). Every repository's entry now has `observed:`,
with `reachable: false` where the clone was refused (nothing inside read: its profile stays the assumed default
and the check notes it), and each repository has a profile (tools/frontend_repos.py profile()). These rules read
against the profile now:

    FR-OLD-PATH          also: a screen's component is not the path its repository's profile gives it
                         (frontend_repos.component_path, written by tools/apply-repo-layout.py)
    FR-LAYOUT-MISMATCH   compares only a layout that was read (reachable: true)
    FR-FIELDS            also: an `observed:` block with no by, date or reachable, or one read with no workspace,
                         packageManager or srcRoot
    FR-SETUP-TABLE       also: setup's frontend CLAUDE.md block of what each repository holds differs from the
                         profile (frontend_repos.setup_block)

Read-only. Exit 1 on a finding not in `handoff/audit-baseline.json` (tools/audit_guard.py).

    python3 tools/check-frontend-repos.py [--all]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402
import frontend_repos as fr  # noqa: E402  (CHG-SWP-003)

RULES = {
    "FR-PLATFORM-MISSING": "every screen platform has a repository entry, and every entry a platform (CHG-R6-059)",
    "FR-APP-MISSING": "every frontend app is on an entry (CHG-R6-059)",
    "FR-APP-MISMATCH": "an entry's app is its platform's app (CHG-R6-059)",
    "FR-REPO-TWICE": "a repository serves one platform unless `shared` says why (CHG-R6-059)",
    "FR-FIELDS": ("an entry with a repository says assumed true or false; names and url follow the group; "
                  "an observed block says by, date, reachable (CHG-R6-059, CHG-RPO-001)"),
    "FR-SETUP-TABLE": ("ADAM setup's frontend CLAUDE.md names the same repository per platform and the same profile "
                       "(CHG-R6-059, CHG-RPO-003)"),
    "FR-OLD-PATH": ("a screen with a repository names its component under the old apps/<app>/ workspace, or not where "
                    "its repository's profile puts it (CHG-SWP-003, CHG-RPO-002)"),
    "FR-LAYOUT-UNCONFIRMED": "a repository's layout is assumed and nothing observed is recorded (CHG-SWP-003)",
    "FR-LAYOUT-MISMATCH": "a repository's observed layout contradicts what the package says of it (#27741, CHG-SWP-003)",
}
MAPPING = g.ROOT / "docs" / "active" / "frontend-repos.yaml"
STARTER = g.ROOT.parent / "viewer" / "mcp" / "setup" / "starters" / "frontend" / "CLAUDE.md"
REPO_NAME = re.compile(r"^ticvai-[a-z0-9]+(-[a-z0-9]+)*$")


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-frontend-repos", RULES)
    if not MAPPING.exists():
        guard.add("FR-PLATFORM-MISSING", "mapping", "docs/active/frontend-repos.yaml is missing")
        return guard.finish()
    doc = g.load_yaml(MAPPING) or {}
    entries = doc.get("platforms") or {}
    if "{repo}" not in str(doc.get("url") or ""):
        guard.add("FR-FIELDS", "url", "frontend-repos.yaml has no `url` template naming {repo}")

    declared = {}                                   # P04 -> app, from the screen files
    for stem, p in g.platforms().items():
        if p.get("code"):
            declared[str(p["code"])] = p.get("app")
    for code, app in sorted(declared.items()):
        e = entries.get(code)
        if not isinstance(e, dict):
            guard.add("FR-PLATFORM-MISSING", code, f"{code} ({app}) has screens and no entry in frontend-repos.yaml")
            continue
        if e.get("app") != app:
            guard.add("FR-APP-MISMATCH", code, f"{code}: the entry says app {e.get('app')!r}, the screens say {app!r}")
    for code in sorted(set(entries) - set(declared)):
        guard.add("FR-PLATFORM-MISSING", code, f"frontend-repos.yaml has {code}, which no screens/P*.yaml declares")

    apps = {e.get("app") for e in entries.values() if isinstance(e, dict)}
    manifests = {f.stem for f in (g.ROOT / "frontend").glob("*.yaml")}
    for app in sorted((manifests | {a for a in declared.values() if a}) - apps):
        guard.add("FR-APP-MISSING", app, f"app {app} has no entry in frontend-repos.yaml (give it repo: null if it has "
                                         "no repository yet)")

    by_repo: dict = {}
    for code, e in sorted(entries.items()):
        if not isinstance(e, dict):
            continue
        repo = e.get("repo")
        if "repo" not in e:
            guard.add("FR-FIELDS", f"{code}:repo", f"{code}: no `repo` (null when there is no repository yet)")
        if repo is None:
            continue
        if not REPO_NAME.match(str(repo)):
            guard.add("FR-FIELDS", f"{code}:name", f"{code}: repository {repo!r} is not of the form ticvai-<name>")
        if not isinstance(e.get("assumed"), bool):
            guard.add("FR-FIELDS", f"{code}:assumed", f"{code}: {repo} has no `assumed: true|false`")
        obs = e.get("observed")
        if isinstance(obs, dict):                   # CHG-RPO-001: what was seen, by whom, when, and whether it was
            need = ["by", "date", "reachable"]      # read at all; a read layout says what it is
            if obs.get("reachable") is True:
                need += ["workspace", "packageManager", "srcRoot"]
            for k in need:
                if obs.get(k) in (None, ""):
                    guard.add("FR-FIELDS", f"{code}:observed:{k}", f"{code}: {repo}'s `observed:` has no {k}")
            if "reachable" in obs and not isinstance(obs.get("reachable"), bool):
                guard.add("FR-FIELDS", f"{code}:observed:reachable", f"{code}: {repo}'s `observed.reachable` is not "
                                                                      "true or false")
        by_repo.setdefault(repo, []).append(code)
    for repo, codes in sorted(by_repo.items()):
        if len(codes) > 1 and not all(entries[c].get("shared") for c in codes):
            guard.add("FR-REPO-TWICE", repo, f"{repo} is mapped to {', '.join(codes)} with no `shared` reason on each")

    # The table ADAM setup writes into a frontend workspace: | P04 Venue POS - ... | `ticvai-pos` |
    if STARTER.exists():
        seen = {}
        for line in STARTER.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^\|\s*(P\d\d)\b[^|]*\|\s*`(ticvai-[a-z0-9-]+)`\s*\|", line)
            if m:
                seen[m.group(1)] = m.group(2)
        for code, repo in sorted(seen.items()):
            want = (entries.get(code) or {}).get("repo")
            if repo != want:
                guard.add("FR-SETUP-TABLE", code, f"setup's frontend CLAUDE.md maps {code} to {repo}; "
                                                  f"frontend-repos.yaml says {want or 'no repository'}")
        for code, e in sorted(entries.items()):
            if isinstance(e, dict) and e.get("repo") and code not in seen:
                guard.add("FR-SETUP-TABLE", code, f"frontend-repos.yaml maps {code} to {e['repo']}; setup's frontend "
                                                  "CLAUDE.md table does not list it")
        # CHG-RPO-003: the block of what each repository holds is the profile's, word for word.
        text = STARTER.read_text(encoding="utf-8").replace("\r\n", "\n")
        if fr.SETUP_BEGIN not in text or fr.SETUP_END not in text:
            guard.add("FR-SETUP-TABLE", "profile", "setup's frontend CLAUDE.md has no block of what each repository "
                                                   "holds (run tools/apply-repo-layout.py --setup)")
        elif fr.SETUP_BEGIN + text.split(fr.SETUP_BEGIN, 1)[1].split(fr.SETUP_END, 1)[0] + fr.SETUP_END \
                != fr.setup_block():
            guard.add("FR-SETUP-TABLE", "profile", "setup's frontend CLAUDE.md block of what each repository holds "
                                                   "differs from frontend-repos.yaml (run tools/apply-repo-layout.py "
                                                   "--setup)")
    else:
        guard.note("viewer/mcp/setup/starters/frontend/CLAUDE.md not found: the setup table was not compared")
    layouts(guard, doc, entries)
    return guard.finish()


def layouts(guard, doc: dict, entries: dict) -> None:
    """CHG-SWP-003: what the package says a repository holds against what was seen in it."""
    plats = {str(p.get("code")): p for p in g.platforms().values() if p.get("code")}
    by_platform: dict = {}
    for stem, s in g.screens():
        by_platform.setdefault(stem[:3], []).append(s)
    assumed = bool((doc.get("layout") or {}).get("assumed"))
    old, unread = {}, []
    for code, e in sorted(entries.items()):
        if not isinstance(e, dict) or not e.get("repo"):
            continue
        app = e.get("app")
        paths = []
        for s in by_platform.get(code, []):
            comp = str((s.get("implementation") or {}).get("component") or "")
            if not comp:
                continue
            paths.append(fr.relative_path(comp, app))
            if fr.OLD_APP_PATH.match(comp):
                guard.add("FR-OLD-PATH", s["id"], f"{code} {s['id']}: component {comp} is in the one-workspace "
                                                  f"layout; the screen is built in {e['repo']}")
                old[code] = old.get(code, 0) + 1
            elif fr.component_path(code, comp) != comp:
                # CHG-RPO-002: the path its repository's profile gives it, nothing else.
                guard.add("FR-OLD-PATH", s["id"], f"{code} {s['id']}: component {comp} is not where {e['repo']}'s "
                                                  f"profile puts it ({fr.component_path(code, comp)}; run "
                                                  "tools/apply-repo-layout.py)")
                old[code] = old.get(code, 0) + 1
        obs = e.get("observed")
        if not isinstance(obs, dict):
            if assumed:
                guard.add("FR-LAYOUT-UNCONFIRMED", code, f"{code} {e['repo']}: no `observed:` layout; the "
                                                         f"{len(paths)} locations its tickets suggest are assumed")
            continue
        if obs.get("reachable") is not True:
            # CHG-RPO-001: the clone was refused; that is what was observed. Its profile stays the assumed default.
            unread.append(f"{code} {e['repo']} ({len(paths)} screens)")
            continue
        src = str(obs.get("srcRoot") or "").strip("/")
        if src:
            off = [p for p in paths if p and not p.startswith(src + "/")]
            if off:
                guard.add("FR-LAYOUT-MISMATCH", f"{code}:srcRoot", f"{code} {e['repo']}: {len(off)} suggested "
                                                                   f"location(s) are not under {src}/, e.g. {off[0]}")
        have = {str(x) for x in obs.get("packages") or []}
        for pkg in sorted(str(x) for x in (plats.get(code) or {}).get("packages") or []):
            if pkg not in have:
                guard.add("FR-LAYOUT-MISMATCH", f"{code}:package:{pkg}",
                          f"{code} {e['repo']}: the package names shared package {pkg}; the repository has "
                          f"{', '.join(sorted(have)) or 'none'} (observed {obs.get('date', '?')})")
        if str(obs.get("workspace") or "").lower() not in ("", "nx") and old.get(code):
            guard.add("FR-LAYOUT-MISMATCH", f"{code}:workspace",
                      f"{code} {e['repo']}: a {obs.get('workspace')} repository ({obs.get('packageManager') or '?'}), "
                      f"and {old[code]} of its screens name apps/{app}/")
    if old:
        guard.note("FR-OLD-PATH by platform: " + ", ".join(f"{c} {n}" for c, n in sorted(old.items())))
    if unread:
        guard.note("observed but not read (the clone was refused; profile assumed until the owner confirms): "
                   + "; ".join(unread))


if __name__ == "__main__":
    sys.exit(main())
