#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every file a decision document cites is inside the repository, so every clone can open it.

**2 October 2026** (CHG-SEED-002, CHG-SEED-012). The 30 September minutes were cited by the design-input
index while the file sat outside git; the release runbook and the change rules cited
`audit/ticvai/ROOT-CLASSES.md` and the council's transcripts, which the repository's `.gitignore` keeps out
(`audit/`). Chinmay: *"we cannot cite them, they are outside of git; we can have them, but the HTML is
final, so that is the input."* So the council's final HTML reports are in `docs/active/council/`, the root
classes in `docs/active/root-classes.md`, and this checks that it stays that way.

It reads the documents decisions are taken from (`docs/registers/`, `docs/active/`, `docs/adr/`,
`changes/entries/`, `handoff/design-inputs/` and `CLAUDE.md`), takes every path in them that starts with a
package or repository root (`sources/`, `docs/`, `handoff/`, `tools/`, `contracts/`, `screens/`, `flows/`,
`audit/` ...), and fails on

    CS-OUTSIDE-GIT  a path under `audit/`, a scratchpad or a temp directory: git ignores them, so the
                    citation resolves on one machine only
    CS-MISSING      a path git does not track (resolved from ticvai/, the repository root, or the citing
                    file's folder): a renamed, deleted or never-committed file

Patterns (`*`, `<id>`, `{...}`) are not citations and are skipped. The findings that were there when the
check was written are its baseline (`handoff/audit-baseline.json`, `audit_guard.py`): only a new one fails,
and `--update-baseline` after a fix tightens it.

    python3 tools/check-cited-sources.py [--all] [--update-baseline]
"""
from __future__ import annotations

import collections
import re
import subprocess
import sys
from pathlib import Path

import audit_guard as g

ROOT = g.ROOT                     # ticvai/
REPO = ROOT.parent
SCOPE = ["docs/registers", "docs/active", "docs/adr", "changes/entries", "handoff/design-inputs"]
SCOPE_FILES = ["CLAUDE.md"]
EXTS = (".md", ".yaml", ".yml", ".json")
ROOTS = ("ticvai/", "sources/", "docs/", "handoff/", "tools/", "contracts/", "screens/", "flows/", "states/",
         "events/", "wireframes/", "diagrams/", "repos/", "checks/", "changes/", "audit/", "viewer/",
         "scratchpad/", "scratch/", "deploy/", "backend/", "frontend/", "services/", "designs/", "ui-design/")
PATH = re.compile(r"(?<![\w./-])((?:" + "|".join(re.escape(r) for r in ROOTS) + r")[A-Za-z0-9_./()+-]*"
                  r"\.[A-Za-z0-9]{1,5})(?![\w/])")
OUTSIDE = re.compile(r"^(audit/|scratchpad/|scratch/)|/scratchpad/|AppData/Local/Temp")
RULES = {
    "CS-OUTSIDE-GIT": "a decision document cites a path under audit/ or a scratchpad (outside git)",
    "CS-MISSING": "a decision document cites a file git does not track",
}


def tracked() -> set | None:
    try:
        p = subprocess.run(["git", "ls-files", "-z"], cwd=REPO, capture_output=True)
        if p.returncode != 0:
            return None
        return {x.decode("utf-8", "replace") for x in p.stdout.split(b"\0") if x}
    except Exception:
        return None


def documents() -> list[Path]:
    out = [ROOT / f for f in SCOPE_FILES if (ROOT / f).exists()]
    for d in SCOPE:
        base = ROOT / d
        if base.is_dir():
            out += sorted(p for p in base.rglob("*") if p.is_file() and p.suffix in EXTS)
    return out


def resolves(path: str, doc: Path, files: set | None) -> bool:
    cands = []
    rel_doc = doc.parent.relative_to(REPO).as_posix()
    for c in ([path[len("ticvai/"):]] if path.startswith("ticvai/") else []) + [path]:
        cands += [f"ticvai/{c}", c, f"{rel_doc}/{c}"]
    if files is None:
        return any((REPO / c).exists() for c in cands)
    return any(c in files for c in cands)


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-cited-sources", RULES)
    files = tracked()
    if files is None:
        guard.note("git is not available: existence checked on disk instead of in git")
    per_doc = collections.Counter()
    n_cites = 0
    for doc in documents():
        rel = doc.relative_to(ROOT).as_posix()
        text = doc.read_text(encoding="utf-8", errors="replace")
        for m in sorted(set(PATH.findall(text))):
            p = m.rstrip(".,;:)")
            if any(ch in p for ch in "*<>{}"):
                continue
            n_cites += 1
            if OUTSIDE.search(p):
                guard.add("CS-OUTSIDE-GIT", f"{rel}|{p}", f"{rel}: cites {p}")
                per_doc[rel] += 1
            elif not resolves(p, doc, files):
                guard.add("CS-MISSING", f"{rel}|{p}", f"{rel}: cites {p}, which git does not track")
                per_doc[rel] += 1
    guard.note(f"{len(documents())} document(s), {n_cites} cited path(s)")
    if per_doc:
        guard.note("most findings: " + ", ".join(f"{d} ({n})" for d, n in per_doc.most_common(8)))
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
