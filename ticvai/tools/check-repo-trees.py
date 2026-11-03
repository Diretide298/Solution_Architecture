#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""repos/ holds each repository's project documents, never a code tree, and its copies match their sources.

**3 November 2026** (the r13 system review, D-06 with D-01, D-02, D-03, D-04, D-05, D-07 and D-08; the lead: "Retire
the code trees", keep the project documents, generated from the starters; CHG-R14J-002). repos/ticvai-backend,
-frontend and -ai held hand-written code trees that no tool kept in step with ADAM's starters, the code the setup zip
really creates: the backend did not compile, its permission resolver let an ancestor's allow beat a descendant's deny,
its tenancy was one tenant per cell, the offline outbox reordered writes, the migration checker was a September fork,
and their rules page taught .NET 8, one tenant per jurisdiction and ULIDs. check-starter-fit compared the starters
with the docs and never looked here. The code is gone; tools/derive-mirrors.py writes what stays, and this holds it:

    RT-CODE        a file under repos/<repository>/ that is not one of its project documents: README.md, CLAUDE.md
                   and project-bible/ everywhere; the whole of ticvai-docs/ (a mirror); the contracts repository's
                   publishing files (openapi/, scripts/, standards/, Makefile and its CI and editor settings) and
                   AGENTS.md; the infrastructure repository's terraform/, runbooks/, CI and AGENTS.md (the package's
                   own sources for both); repos/README.md. A repository folder not in that list fails too.
    RT-STARTER     a copy that differs from its source: the CLAUDE.md of ticvai-backend, -frontend and -ai against
                   ADAM's starter (viewer/mcp/setup/starters/<role>/CLAUDE.md); every bible's setup/*.md against the
                   starter docs, and a setup/ file the starter docs do not have; every bible's repos/*.md against its
                   rules source (derive-mirrors RULE_PAGES). **Fails closed** when the starters are not beside the
                   package: a check that passes when it cannot look is how the code trees went unseen.
    RT-SHADOW      a bible folder that shadows a mirrored docs/ folder with an older partial copy (adr/, architecture/,
                   active/, registers/), or the August .synced-at stamp.
    RT-OPENAPI     a contracts/ folder with OpenAPI files that the contracts repository's openapi/ does not mirror
                   (D-10: contracts/devices/ never reached it).
    RT-PUBLISH     the contracts repository's publishing cannot work (D-10): a single-bracket `[ ... == *glob* ]`
                   test (no pattern matching in `[`), a client for net8.0 or pydantic v1, openapi-generator in a job
                   whose image has no Java, or a TypeScript client published without a package.json written for it.

Derive before check: run after tools/derive-mirrors.py (the refresh does). Read-only. Exit 1 on a finding not in
handoff/audit-baseline.json (tools/audit_guard.py).

    python tools/check-repo-trees.py [--all] [--self-test]
"""
from __future__ import annotations

import importlib.util
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {
    "RT-CODE": "a file under repos/<repository>/ that is not one of its project documents (the code trees are retired: "
               "D-06; CHG-R14J-002)",
    "RT-STARTER": "a repository's CLAUDE.md, a bible's setup/ or repos/ page that differs from its source (ADAM's "
                  "starters, docs/repos/rules), or the starters are not beside the package (D-04, D-06; CHG-R14J-002)",
    "RT-SHADOW": "a bible folder that shadows a mirrored docs/ folder with an older partial copy (CHG-R14J-002)",
    "RT-OPENAPI": "a contracts/ folder the contracts repository's openapi/ does not mirror (D-10; CHG-R14J-003)",
    "RT-PUBLISH": "the contracts repository's publishing scripts or pipeline cannot work as written (D-10; CHG-R14J-003)",
}

DOCS_EVERYWHERE = ("README.md", "CLAUDE.md", "project-bible/")
ALLOWED = {
    "ticvai-backend": DOCS_EVERYWHERE,
    "ticvai-frontend": DOCS_EVERYWHERE,
    "ticvai-ai": DOCS_EVERYWHERE,
    "ticvai-docs": ("",),
    "ticvai-contracts": DOCS_EVERYWHERE + ("AGENTS.md", "openapi/", "scripts/", "standards/", "Makefile",
                                           ".editorconfig", ".githooks/", ".gitlab-ci.yml", ".gitmessage",
                                           ".redocly.yaml"),
    "ticvai-infra": DOCS_EVERYWHERE + ("AGENTS.md", "terraform/", "runbooks/", ".gitlab-ci.yml"),
}
TOP_ALLOWED = ("README.md",)
SKIP_PARTS = {".git", "__pycache__", "node_modules", ".diff", "dist"}


def mirrors_module(root: Path):
    spec = importlib.util.spec_from_file_location("derive_mirrors", str(root / "tools" / "derive-mirrors.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def files_under(repos: Path) -> list:
    out = []
    for f in repos.rglob("*"):
        if f.is_file() and not (set(f.relative_to(repos).parts) & SKIP_PARTS):
            out.append(f.relative_to(repos).as_posix())
    return sorted(out)


def code_findings(rels: list) -> list:
    """[(rel, why)] for files under repos/ outside the project documents."""
    out = []
    for rel in rels:
        parts = rel.split("/", 1)
        if len(parts) == 1:
            if rel not in TOP_ALLOWED:
                out.append((rel, "a file at the top of repos/ other than README.md"))
            continue
        repo, inner = parts
        allowed = ALLOWED.get(repo)
        if allowed is None:
            out.append((rel, f"repos/{repo}/ is not one of the six repositories"))
        elif not any(inner == a or (a.endswith("/") and inner.startswith(a)) or a == "" for a in allowed):
            out.append((rel, f"not a project document of {repo} (code trees are retired; the code lives in the team's "
                             "repository, started from ADAM's starter)"))
    return out


def norm(text: str) -> str:
    return text.replace("\r\n", "\n")


def starter_findings(repos: Path, want: dict, starter_docs: set) -> list:
    """[(rel, why)] for copies that differ from what derive-mirrors writes, and setup/ files the starters lack."""
    out = []
    for rel, body in sorted(want.items()):
        f = repos / rel
        if not f.is_file():
            out.append((rel, "missing: run tools/derive-mirrors.py"))
        elif norm(f.read_text(encoding="utf-8", errors="replace")) != norm(body):
            out.append((rel, "differs from its source: edit the source (ADAM's starter or docs/repos/rules), then run "
                             "tools/derive-mirrors.py"))
    for f in sorted(repos.glob("**/setup/*.md")):
        rel = f.relative_to(repos).as_posix()
        if f.name != "README.md" and f.name not in starter_docs and rel not in want:
            out.append((rel, "a setup/ page ADAM's starter docs do not have"))
    return out


def publish_findings(texts: dict) -> list:
    """[(file, why)] over the contracts repository's publishing files: {repo-relative path: text}."""
    out = []
    for rel, text in sorted(texts.items()):
        for n, line in enumerate(text.split("\n"), 1):
            code = line.split("#", 1)[0] if rel.endswith(".sh") else line
            if rel.endswith(".sh") and re.search(r"(?<!\[)\[ [^]]*==\s*\*", code):
                out.append((f"{rel}:{n}", "`[ ... == *glob* ]` never matches: `[` does no pattern matching, use `[[ ]]`"))
            if re.search(r"targetFramework=net[5-9]\.0\b", code):
                out.append((f"{rel}:{n}", "a C# client for an older .NET than the backend's net10.0"))
            if "python-pydantic-v1" in code:
                out.append((f"{rel}:{n}", "a Python client on pydantic v1; the AI runtime pins pydantic 2"))
    ci = texts.get(".gitlab-ci.yml", "")
    gen = texts.get("scripts/generate-clients.sh", "")
    if "openapi-generator" in gen:
        for job in re.split(r"\n(?=\S[^\n]*:\s*\n)", ci):
            if "make generate" in job and not re.search(r"jre|jdk|java|openjdk|temurin", job, re.I):
                out.append((".gitlab-ci.yml", "the job that runs `make generate` has no Java runtime, which "
                                              "openapi-generator-cli needs"))
    if "npm publish" in ci and '"name": "@ticvai/api-client"' not in gen:
        out.append(("scripts/generate-clients.sh", "the pipeline publishes the TypeScript client and nothing writes "
                                                    "its package.json (@ticvai/api-client)"))
    return out


def self_test() -> int:
    cases = []
    rels = ["README.md", "update-bible.sh", "ticvai-backend/README.md", "ticvai-backend/CLAUDE.md",
            "ticvai-backend/project-bible/x.md", "ticvai-backend/src/Ticvai.Api/A.cs", "ticvai-docs/anything/x.py",
            "ticvai-contracts/scripts/a.sh", "ticvai-infra/terraform/main.tf", "ticvai-frontend/apps/pos/project.json",
            "ticvai-kiosk/README.md"]
    cases.append(("code trees, a stray top file and an unknown repository fail",
                  sorted(r for r, _ in code_findings(rels)),
                  ["ticvai-backend/src/Ticvai.Api/A.cs", "ticvai-frontend/apps/pos/project.json",
                   "ticvai-kiosk/README.md", "update-bible.sh"]))
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "ticvai-backend").mkdir()
        (r / "ticvai-backend" / "CLAUDE.md").write_text("# old\n", encoding="utf-8")
        (r / "ticvai-docs" / "setup").mkdir(parents=True)
        (r / "ticvai-docs" / "setup" / "a.md").write_bytes(b"A\r\n")
        (r / "ticvai-docs" / "setup" / "stray.md").write_text("S\n", encoding="utf-8")
        want = {"ticvai-backend/CLAUDE.md": "# new\n", "ticvai-docs/setup/a.md": "A\n", "ticvai-ai/CLAUDE.md": "x"}
        cases.append(("a stale copy, a missing copy and a stray setup page fail; line endings do not",
                      sorted(x for x, _ in starter_findings(r, want, {"a.md"})),
                      ["ticvai-ai/CLAUDE.md", "ticvai-backend/CLAUDE.md", "ticvai-docs/setup/stray.md"]))
    bad = {"scripts/breaking-change-check.sh": 'if [ "${PR_LABELS:-}" == *"contract:major"* ]; then',
           "scripts/generate-clients.sh": "openapi-generator-cli generate -g csharp "
                                          "--additional-properties=targetFramework=net8.0\n-g python-pydantic-v1",
           ".gitlab-ci.yml": "publish:\n  image: mcr.microsoft.com/dotnet/sdk:8.0\n  script:\n    - make generate\n"
                             "    - (cd dist/clients/typescript && npm publish)\n"}
    cases.append(("the r13 contracts publishing fails five ways", len(publish_findings(bad)), 5))
    good = {"scripts/breaking-change-check.sh": 'if [[ "${PR_LABELS:-}" == *contract:major* ]]; then',
            "scripts/generate-clients.sh": 'openapi-generator-cli generate -g python\ntargetFramework=net10.0\n'
                                           '"name": "@ticvai/api-client"',
            ".gitlab-ci.yml": "publish:\n  image: node:20\n  script:\n    - apt-get install -y default-jre-headless\n"
                              "    - make generate\n    - (cd dist/clients/typescript && npm publish)\n"}
    cases.append(("the fixed publishing passes", publish_findings(good), []))
    fails = [f"{name}: got {got!r}, expected {want!r}" for name, got, want in cases if got != want]
    for f in fails:
        print("  FAIL", f)
    print(f"check-repo-trees self-test: {len(cases) - len(fails)} of {len(cases)} passed")
    return 1 if fails else 0


def main() -> int:
    g.force_utf8()
    if "--self-test" in sys.argv[1:]:
        return self_test()
    if self_test():
        return 1
    guard = g.Guard("check-repo-trees", RULES)
    repos = g.ROOT / "repos"
    if not repos.is_dir():
        guard.note("no repos/: nothing to hold")
        return guard.finish()
    mod = mirrors_module(g.ROOT)
    rels = files_under(repos)
    for rel, why in code_findings(rels):
        guard.add("RT-CODE", f"repos/{rel}", f"repos/{rel}: {why}")
    if not mod.STARTERS.is_dir():
        guard.add("RT-STARTER", "starters", f"ADAM's starters are not at {mod.STARTERS}: nothing can say whether the "
                                            "repositories' documents are what developers get")
    else:
        starter_docs = {f.name for f in (mod.STARTERS / "docs").glob("*.md")}
        for rel, why in starter_findings(repos, mod.project_documents(), starter_docs):
            guard.add("RT-STARTER", f"repos/{rel}", f"repos/{rel}: {why}")
    bibles = [repos / "ticvai-docs"] + sorted(p for p in repos.glob("*/project-bible") if p.is_dir())
    for b in bibles:
        for folder in mod.SHADOWED:
            if (b / folder).is_dir() and (g.ROOT / "docs" / folder).is_dir():
                rel = (b / folder).relative_to(repos).as_posix()
                guard.add("RT-SHADOW", f"repos/{rel}", f"repos/{rel}/ shadows docs/{folder}/ with an older copy "
                                                       f"(project-bible/docs/{folder}/ is the current one)")
        if (b / ".synced-at").is_file():
            guard.add("RT-SHADOW", f"repos/{b.relative_to(repos).as_posix()}/.synced-at",
                      "the August sync stamp of a tool that no longer runs")
    contracts = repos / "ticvai-contracts"
    if contracts.is_dir():
        for d in sorted((g.ROOT / "contracts").iterdir()):
            if d.is_dir() and any(d.glob("*.yaml")):
                missing = [f.name for f in sorted(d.glob("*.yaml")) if not (contracts / "openapi" / d.name / f.name).is_file()]
                if missing:
                    guard.add("RT-OPENAPI", f"contracts/{d.name}", f"contracts/{d.name}/ ({', '.join(missing[:4])}) is "
                                                                    "not in repos/ticvai-contracts/openapi/")
        texts = {}
        for rel in ("scripts/breaking-change-check.sh", "scripts/generate-clients.sh", ".gitlab-ci.yml", "Makefile"):
            f = contracts / rel
            if f.is_file():
                texts[rel] = norm(f.read_text(encoding="utf-8", errors="replace"))
        for where, why in publish_findings(texts):
            guard.add("RT-PUBLISH", f"ticvai-contracts/{where}", f"repos/ticvai-contracts/{where}: {why}")
    guard.note(f"{len(rels)} file(s) under repos/")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
