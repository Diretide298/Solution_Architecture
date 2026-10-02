#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The starter repositories a developer is handed, against the package that describes them.

**Audit class A-STARTER (docs/active/root-classes.md), roots R025-R040 and R249.** The setup zip
creates `ticvai-backend` and `ticvai-frontend` from ADAM's `viewer/mcp/setup/starters/`. The pull
audit found screens naming apps the starter does not have (R249, R037), a back office tagged one
runtime in the starter and another in the package (R031), standards documents describing types and
projects the starter code does not contain (R025, R028), two id rules (R030), empty package stubs
(R029), and a CLAUDE.md with no path for migration, DevOps or onboarding tickets and no warning that
`.adam/` is git-ignored (R033, R039). S002 fixed those at the source; nothing held them. This reads
the starter read-only -- it lives outside the package, in the ADAM repository -- and says where it
and the package disagree. Where the starter is not beside the package (a mirror checkout), it notes
that and passes.

Read-only. Exit 1 on a finding not in `handoff/audit-baseline.json` (see tools/audit_guard.py).

    python3 tools/check-starter-fit.py [--all] [--update-baseline]
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {
    "SF-APP-MISSING": "a screen's implementation.app has no app in the frontend starter (R249 R037)",
    "SF-APP-RUNTIME": "a starter app's platform tag disagrees with the package manifest's runtime (R031)",
    "SF-DOCS-MIRROR": "a starter standards doc differs from the package's project-bible copy (R028 R030)",
    "SF-DOC-TYPES": "a standards doc names a backend type the starter code does not declare (R025 R028)",
    "SF-ID-RULE": "the starter carries a second id type beside UUIDv7 (ADR-0056) (R030)",
    "SF-EMPTY-STUB": "a shared frontend package is an empty `export {}` stub (R029)",
    "SF-CLAUDE-PATHS": "CLAUDE.md lacks the migration/DevOps paths or the .adam grep note (R033 R039)",
    "SF-DONE-GATES": "a Done-when gate names a command or runner the starter cannot run (R027 R032 R034)",
    "SF-OUTBOX-POLICIES": "a conflict policy the contracts use that offline-core does not declare (R035)",
    "SF-GLOSSARY": "a starter type named with a word the glossary bans (User for Principal) (R040)",
}


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-starter-fit", RULES)
    starters = g.ROOT.parent / "viewer" / "mcp" / "setup" / "starters"
    if not starters.exists():
        guard.note(f"no starter beside the package ({starters}); nothing to compare")
        return guard.finish()
    fe, be, docs = starters / "frontend", starters / "backend", starters / "docs"

    apps = {p.parent.name: p for p in (fe / "apps").glob("*/project.json")}
    for plat, s in g.screens():
        app = ((s.get("implementation") or {}).get("app"))
        if app and app not in apps:
            guard.add("SF-APP-MISSING", f"{app}", f"screens name app {app!r} (e.g. {s['id']}); the frontend starter has no apps/{app}")

    for m in sorted((g.ROOT / "frontend").glob("*.yaml")):
        man = g.load_yaml(m) or {}
        app = man.get("app") or m.stem
        if app not in apps:
            if app not in {k.split(":")[0] for k in guard.found.get("SF-APP-MISSING", {})}:
                guard.add("SF-APP-MISSING", app, f"frontend/{m.name} describes {app!r}; the frontend starter has no apps/{app}")
            continue
        try:
            tags = json.loads(apps[app].read_text(encoding="utf-8")).get("tags") or []
        except Exception:
            tags = []
        plat_tag = next((t.split(":", 1)[1] for t in tags if str(t).startswith("platform:")), None)
        runtime = str(man.get("runtime") or "")
        want = "web" if runtime.lower().endswith("web") or man.get("formFactor") == "web" else "native"
        tag_kind = "web" if plat_tag in ("web", "desktop", "browser") else "native"
        if plat_tag and tag_kind != want:
            guard.add("SF-APP-RUNTIME", app, f"apps/{app} is tagged platform:{plat_tag}; frontend/{m.name} says runtime {runtime}")

    bible = g.ROOT / "repos" / "ticvai-backend" / "project-bible" / "setup"
    for d in sorted(docs.glob("*.md")):
        twin = bible / d.name
        if twin.exists() and twin.read_text(encoding="utf-8") != d.read_text(encoding="utf-8"):
            guard.add("SF-DOCS-MIRROR", d.name, f"starters/docs/{d.name} differs from repos/ticvai-backend/project-bible/setup/{d.name}")

    code = " ".join(p.read_text(encoding="utf-8", errors="replace")
                    for p in (be / "src").rglob("*.cs") if "/obj/" not in p.as_posix() and "/bin/" not in p.as_posix())
    declared = set(re.findall(r"\b(?:interface|class|record|struct|enum)\s+([A-Z]\w+)", code))
    projects = {p.stem for p in be.rglob("*.csproj") if "/obj/" not in p.as_posix()}
    for doc in [docs / "backend-patterns.md", be / "CLAUDE.md"]:
        if not doc.exists():
            continue
        text = doc.read_text(encoding="utf-8")
        for t in sorted(set(re.findall(r"`(I[A-Z][A-Za-z]+)`", text))):
            if t not in declared:
                guard.add("SF-DOC-TYPES", f"{doc.name}:{t}", f"{doc.name} names {t}; no backend starter file declares it")
        for proj in sorted(set(re.findall(r"`((?:TICVAI|Ticvai)\.[A-Z][A-Za-z.]+)`", text))):
            if proj not in projects and not any(proj.startswith(p + ".") for p in projects):
                guard.add("SF-DOC-TYPES", f"{doc.name}:{proj}", f"{doc.name} names project {proj}; the starter has {', '.join(sorted(projects))}")
    if re.search(r"\b(Ulid|ULID)\w*", code):
        guard.add("SF-ID-RULE", "backend:Ulid", "the backend starter still declares or uses a ULID type (ADR-0056: UUIDv7 only)")
    for d in sorted(docs.glob("*.md")):
        for line in d.read_text(encoding="utf-8").split("\n"):
            if re.search(r"\bULID\b|\bUlid", line) and not re.search(r"not|never|instead|replac|was|superseded", line, re.I):
                guard.add("SF-ID-RULE", f"{d.name}", f"{d.name} prescribes a ULID: {line.strip()[:80]}")
                break

    for pkg in sorted((fe / "packages").glob("*/src/index.ts")):
        if re.fullmatch(r"\s*export\s*\{\s*\}\s*;?\s*", pkg.read_text(encoding="utf-8")):
            guard.add("SF-EMPTY-STUB", pkg.parent.parent.name, f"packages/{pkg.parent.parent.name} is `export {{}}`")

    for repo, needs in (("backend", [r"MIG-", r"SETUP-", r"\.adam/"]), ("frontend", [r"\.adam/"])):
        f = starters / repo / "CLAUDE.md"
        text = f.read_text(encoding="utf-8") if f.exists() else ""
        for pat in needs:
            if not re.search(pat, text):
                guard.add("SF-CLAUDE-PATHS", f"{repo}:{pat}", f"{repo}/CLAUDE.md never mentions {pat.replace(chr(92), '')}")
        if ".adam/" in text and not re.search(r"(git-?ignored|--no-ignore|skips it)", text):
            guard.add("SF-CLAUDE-PATHS", f"{repo}:grep-note", f"{repo}/CLAUDE.md mentions .adam/ without saying Grep skips it")

    # R027 R032 R034: what the tickets' Done-when lines ask a developer to run.
    desc = g.load_json(g.ROOT / "handoff" / "service-docs" / "op-descriptions.json", {}) or {}
    blob = "\n".join(desc.values())
    try:
        scripts = json.loads((fe / "package.json").read_text(encoding="utf-8")).get("scripts") or {}
    except Exception:
        scripts = {}
    for cmd in sorted(set(re.findall(r"`pnpm (\w+)`", blob))):
        if cmd not in scripts:
            guard.add("SF-DONE-GATES", f"pnpm:{cmd}", f"tickets ask for `pnpm {cmd}`; frontend package.json has no {cmd} script")
    tests = [p for p in be.rglob("*.csproj") if "Tests" in p.stem and "/obj/" not in p.as_posix()]
    if "dotnet test" in blob and not tests:
        guard.add("SF-DONE-GATES", "dotnet:test", "tickets ask for `dotnet test`; the backend starter has no test project")
    for runner in sorted(set(re.findall(r"`?\b([A-Z][A-Za-z]+Runner)\b`?", blob))):
        if runner not in declared:
            guard.add("SF-DONE-GATES", f"runner:{runner}", f"tickets name {runner}; no backend starter file declares it")
    if re.search(r"reference fixture", blob, re.I) and not any(
            re.search(r"fixture", p.name, re.I) for p in list(be.rglob("*")) if "/obj/" not in p.as_posix()):
        guard.add("SF-DONE-GATES", "fixture", "tickets require the reference fixture; nothing in the backend "
                                              "starter is named for it (SETUP-SEED builds it)")

    # R035: the conflict policies offline-core must carry through its outbox.
    oc = fe / "packages" / "offline-core" / "src"
    oc_text = " ".join(p.read_text(encoding="utf-8") for p in oc.glob("*.ts")) if oc.exists() else ""
    used = {str(f["op"].get("x-ticvai-conflict-policy")) for f in g.operations().values()
            if f["op"].get("x-ticvai-offline-capable") and f["op"].get("x-ticvai-conflict-policy")}
    for pol in sorted(used):
        if f"'{pol}'" not in oc_text and f'"{pol}"' not in oc_text:
            guard.add("SF-OUTBOX-POLICIES", pol, f"offline operations use conflict policy {pol!r}; "
                                                 f"offline-core's ConflictPolicy does not declare it")

    # R040: naming-and-style section 3 - Principal, never User.
    for t in sorted(declared):
        if re.search(r"User(?!Agent)", t) and not t.startswith("Test"):
            guard.add("SF-GLOSSARY", t, f"backend starter declares {t}; the glossary says Principal, never User")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
