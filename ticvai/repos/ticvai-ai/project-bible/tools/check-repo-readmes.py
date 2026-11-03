#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""No README under repos/ is a copy of a package file other than its own source.

**2 November 2026** (r13 root R13, CHG-R13R13-001). From the first commit on, 104 README.md files under repos/ were byte
copies of docs/active/README.md, the Active page: the setup README every onboarding ticket links (#27633, #27634,
#27637), each repository's own README (#27640 SETUP-CLIENTS, the contracts repository), and the infra README
SETUP-ENV's Done-when extends (#27626, #27627). No tool wrote them, so no refresh put them right, and no check compared
them with anything. tools/derive-mirrors.py now writes every one of them; this holds the result:

    RR-COPY   a README.md under repos/ has the content of a package file (outside repos/) other than its declared
              source. The declared source is: for a mirror (a mirrored folder of ticvai-docs/ or a project-bible/),
              the package file at the same path; for a repository README, its docs/repos/ file (derive-mirrors
              README_SOURCES); for ticvai-contracts/openapi/README.md, contracts/README.md; a folder index has none.

Content is compared without the line derive-mirrors writes at the top, with line endings normalised. Derive before
check: run after tools/derive-mirrors.py (the refresh does).

Read-only. Exit 1 on a finding not in handoff/audit-baseline.json (tools/audit_guard.py).

    python3 tools/check-repo-readmes.py [--all] [--self-test]
"""
from __future__ import annotations

import hashlib
import importlib.util
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {"RR-COPY": "no README under repos/ is a copy of a package file other than its declared source "
                    "(R13, CHG-R13R13-001)"}
ROOT = g.ROOT
REPOS = ROOT / "repos"


def mirrors_module():
    spec = importlib.util.spec_from_file_location("derive_mirrors", ROOT / "tools" / "derive-mirrors.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def norm(text: str) -> str:
    """Content without derive-mirrors' header line, LF endings, trimmed."""
    text = text.replace("\r\n", "\n")
    if text.startswith("<!-- Written by tools/derive-mirrors.py"):
        text = text.split("\n", 1)[1] if "\n" in text else ""
    return text.strip()


def digest(text: str) -> str:
    return hashlib.sha256(norm(text).encode("utf-8")).hexdigest()


def declared_source(rel: str, sources: dict, mirrored) -> str | None:
    """The package path a README under repos/ (repos-relative) is meant to copy, or None (an index)."""
    if rel in sources:
        return sources[rel]
    if rel == "ticvai-contracts/openapi/README.md":
        return "contracts/README.md"
    parts = rel.split("/")
    if parts[0] == "ticvai-docs" and len(parts) > 2 and parts[1] in mirrored:
        return "/".join(parts[1:])
    if len(parts) > 3 and parts[1] == "project-bible" and parts[2] in mirrored:
        return "/".join(parts[2:])
    return None


def findings(readmes: dict, package: dict, sources: dict, mirrored) -> list:
    """(rel, copied package paths) for each README whose content is a package file other than its source.
    readmes: repos-relative path -> text; package: package path -> text (outside repos/)."""
    by_hash: dict = {}
    for p, text in package.items():
        if norm(text):
            by_hash.setdefault(digest(text), []).append(p)
    out = []
    for rel, text in sorted(readmes.items()):
        src = declared_source(rel, sources, mirrored)
        others = [p for p in by_hash.get(digest(text), []) if p != src]
        if others and not (src and src in by_hash.get(digest(text), [])):
            out.append((rel, sorted(others)))
    return out


def self_test() -> int:
    sources = {"ticvai-ai/README.md": "docs/repos/ticvai-ai.md"}
    mirrored = ("docs", "contracts")
    package = {"docs/active/README.md": "# Active\n", "docs/repos/ticvai-ai.md": "# ticvai-ai\n",
               "contracts/README.md": "# Contracts\n"}
    cases = [
        ("a repository README that is the Active page fails",
         findings({"ticvai-ai/README.md": "# Active\n"}, package, sources, mirrored), [("ticvai-ai/README.md", ["docs/active/README.md"])]),
        ("a repository README from its source, with the header, passes",
         findings({"ticvai-ai/README.md": "<!-- Written by tools/derive-mirrors.py from x -->\n\n# ticvai-ai\r\n"},
                  package, sources, mirrored), []),
        ("the mirror of docs/active/README.md passes",
         findings({"ticvai-docs/docs/active/README.md": "# Active\n",
                   "ticvai-ai/project-bible/docs/active/README.md": "# Active\n"}, package, sources, mirrored), []),
        ("a legacy folder's README that is the Active page fails",
         [r for r, _ in findings({"ticvai-docs/setup/README.md": "# Active\n",
                                  "ticvai-ai/project-bible/setup/README.md": "# Active\n"}, package, sources, mirrored)],
         ["ticvai-ai/project-bible/setup/README.md", "ticvai-docs/setup/README.md"]),
        ("openapi/README.md is the copy of contracts/README.md it is meant to be",
         findings({"ticvai-contracts/openapi/README.md": "# Contracts\n"}, package, sources, mirrored), []),
        ("a folder index passes", findings({"ticvai-docs/setup/README.md": "# Setup standards\n"}, package, sources, mirrored), []),
    ]
    fails = [f"{name}: got {got!r}, expected {want!r}" for name, got, want in cases if got != want]
    for f in fails:
        print("  FAIL", f)
    print(f"check-repo-readmes self-test: {len(cases) - len(fails)} of {len(cases)} passed")
    return 1 if fails else 0


def main() -> int:
    g.force_utf8()
    if "--self-test" in sys.argv[1:]:
        return self_test()
    guard = g.Guard("check-repo-readmes", RULES)
    if not REPOS.is_dir():
        guard.note("no repos/: nothing compared")
        return guard.finish()
    mod = mirrors_module()
    readmes = {f.relative_to(REPOS).as_posix(): f.read_text(encoding="utf-8", errors="replace")
               for f in sorted(REPOS.rglob("README.md")) if "node_modules" not in f.parts}
    tracked = subprocess.run(["git", "-C", str(ROOT), "ls-files", "-z", "--", "*.md"], capture_output=True).stdout
    package = {}
    for p in tracked.decode("utf-8", "replace").split("\0"):
        if not p or p.startswith("repos/"):
            continue
        f = ROOT / p
        if f.is_file():
            package[p] = f.read_text(encoding="utf-8", errors="replace")
    for rel, others in findings(readmes, package, mod.README_SOURCES, mod.MIRRORED):
        guard.add("RR-COPY", f"repos/{rel}",
                  f"repos/{rel} is a copy of {', '.join(others[:3])}"
                  f"{' and more' if len(others) > 3 else ''}, not of its own source: run tools/derive-mirrors.py, "
                  "and give it a source in docs/repos/ (README_SOURCES) if it is a repository's README")
    guard.note(f"{len(readmes)} README(s) under repos/ against {len(package)} package Markdown file(s)")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
