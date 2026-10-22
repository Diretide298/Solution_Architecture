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

A file the package deleted by a recorded decision (tools/check-migration-freeze.py `RETIRED`, CHG-SQL-001) is
noted, not failed: the change entry that deleted it has to name it (CHG-R4-009).

**A forward migration's name carries the day the gate first wrote it** (22 October 2026, CHG-R9INT-002).
tools/derive-ddl.py names a new one `backend/<db>/V<nnnn>__after_<tag>_<yyyymmdd>.sql` with the date of the run that
writes it, and keeps that name once the file is committed. The r9 CR lane cited the V0114 its own run of 21 October
wrote and never committed; the integration gate of 22 October wrote it again as `..._20261022.sql`, and five entries
cited a file that did not exist. A CS-MISSING citation of a forward migration therefore says which file git has under
that number, or that none is committed yet (bring the gate's file into the branch, as the gate does on PASS, and cite
that name).

Patterns (`*`, `<id>`, `{...}`) are not citations and are skipped. The findings that were there when the
check was written are its baseline (`handoff/audit-baseline.json`, `audit_guard.py`): only a new one fails,
and `--update-baseline` after a fix tightens it.

    python3 tools/check-cited-sources.py [--all] [--update-baseline]
"""
from __future__ import annotations

import collections
import functools
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


@functools.lru_cache(maxsize=None)
def retired_files() -> frozenset:
    """Files the package deleted by a recorded decision (check-migration-freeze.py RETIRED, CHG-SQL-001; CHG-R4-009):
    a change entry that cites one is history, not a missing source. Any other deleted file still fails."""
    import importlib.util
    f = ROOT / "tools" / "check-migration-freeze.py"
    if not f.exists():
        return frozenset()
    spec = importlib.util.spec_from_file_location("cmf", f)
    m = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(m)
    except Exception:
        return frozenset()
    return frozenset(getattr(m, "RETIRED", ()))


FORWARD = re.compile(r"^(?:ticvai/)?backend/(\w+)/(V\d{4}[a-z]?)__[\w.-]+\.sql$")


def forward_hint(path: str, files: set | None) -> str:
    """For a forward migration git does not track: the file git has under its number, or that none is committed."""
    m = FORWARD.match(path)
    if not m or files is None:
        return ""
    area, version = m.groups()
    have = sorted(f[len("ticvai/"):] for f in files
                  if f.startswith(f"ticvai/backend/{area}/{version}__") and f.endswith(".sql"))
    if have:
        return f" (git has {', '.join(have)}: a forward migration keeps the name of the day the gate first wrote it)"
    return (f" ({version} is not committed: derive-ddl names a new forward migration by the day of the run that writes "
            "it, so bring the gate's file into the branch and cite that name)")


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
            elif p.removeprefix("ticvai/") in retired_files():
                guard.note(f"{rel}: cites {p}, retired by decision (check-migration-freeze RETIRED, CHG-SQL-001)")
            elif not resolves(p, doc, files):
                guard.add("CS-MISSING", f"{rel}|{p}", f"{rel}: cites {p}, which git does not track"
                          + forward_hint(p, files))
                per_doc[rel] += 1
    guard.note(f"{len(documents())} document(s), {n_cites} cited path(s)")
    if per_doc:
        guard.note("most findings: " + ", ".join(f"{d} ({n})" for d, n in per_doc.most_common(8)))
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
