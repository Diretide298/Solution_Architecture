#!/usr/bin/env python3
"""Sync repos/*/project-bible/ and repos/ticvai-docs/ from the package root.

`repos/update-bible.sh` says it plainly: **project-bible/ is a copy, not a source.** Nothing ran
it. On 20 August the mirror held 21 state files against the root's 113, 54 files differed, 144
existed only in the mirror and **305 root files had never reached it.**

The symptom that surfaced it was one file. `states/entitlement.yaml` was renamed to
`entitlement-status.yaml` at the root and repointed from `access.TicketStatus` — an object, not an
enum — to `orders.EntitlementStatus`. **The six mirrored copies kept the original**, anchored on
nothing, and `access.TicketStatus`'s own description claimed the file had been *removed 18 August*.

**A file that documents its own deletion and is still there is worse than a stale file**, because
the note stops the next person looking.

Two things this does that the shell script did not:

  1. **Deletes what the root no longer has.** A copy that only ever adds accumulates every file
     ever deleted upstream, which is how the mirror came to hold 144 orphans.
  2. **Reports rather than assumes.** The counts print, so a sync that moves 300 files is visible
     rather than silent.
"""
from __future__ import annotations

import filecmp
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPOS = ROOT / "repos"

# What a bible carries. `repos/` itself is excluded or the copy recurses.
#
# **`tools/` and `handoff/` are in.** They were left out on the first pass as *large and rebuilt
# by their own derivers*, and that reasoning is wrong for a mirror: a repo holding contracts it
# cannot validate, and derived artefacts three days behind the contracts beside them, is a repo
# whose checks pass against the wrong package. Seven validators and three handoff files were stale
# the moment the folder set was chosen.
# **"diagrams" added 24 August.** The HLD and the sixteen LLD files are derived artefacts the
# viewer renders, and they were in the root package and in no mirror — the same shape of defect
# that left 96 orphaned wireframe files in six repos.
MIRRORED = ("contracts", "states", "flows", "events", "screens", "docs", "frontend",
            "tools", "handoff", "sources", "diagrams")


def sync(src: Path, dst: Path) -> tuple[int, int, int]:
    added = updated = removed = 0
    wanted: set = set()

    for folder in MIRRORED:
        s = src / folder
        if not s.is_dir():
            continue
        for f in s.rglob("*"):
            if not f.is_file() or "__pycache__" in f.parts:
                continue
            rel = f.relative_to(src)
            wanted.add(rel)
            target = dst / rel
            if not target.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, target)
                added += 1
            elif not filecmp.cmp(f, target, shallow=False):
                shutil.copy2(f, target)
                updated += 1

    # **A folder dropped from MIRRORED is orphaned, not pruned.** Removing `wireframes` from the
    # set on 20 August left 96 board files sitting in six mirrors with nothing upstream — the
    # removal pass only walks folders still in the set, so what leaves the set stops being
    # managed at the moment it most needs to be.
    for stale in sorted(dst.iterdir()) if dst.is_dir() else []:
        if stale.is_dir() and stale.name not in MIRRORED and (ROOT / stale.name).is_dir() is False \
                and stale.name in ("wireframes",):
            shutil.rmtree(stale)
            removed += 1

    # **Removal is the half the shell script omitted.** Without it the mirror keeps every file the
    # root ever deleted, and a reader finds `entitlement.yaml` beside `entitlement-status.yaml`
    # with no way to tell which is current.
    for folder in MIRRORED:
        d = dst / folder
        if not d.is_dir():
            continue
        for f in sorted(d.rglob("*"), reverse=True):
            if f.is_file() and f.relative_to(dst) not in wanted:
                f.unlink()
                removed += 1
            elif f.is_dir() and not any(f.iterdir()):
                f.rmdir()

    return added, updated, removed


def main() -> int:
    if not REPOS.is_dir():
        print("  no repos/ — nothing to mirror")
        return 0

    targets = []
    docs = REPOS / "ticvai-docs"
    if docs.is_dir():
        targets.append(docs)
    for repo in sorted(REPOS.iterdir()):
        bible = repo / "project-bible"
        if bible.is_dir():
            targets.append(bible)

    total = [0, 0, 0]
    for t in targets:
        a, u, r = sync(ROOT, t)
        total = [total[0] + a, total[1] + u, total[2] + r]
        if a or u or r:
            print(f"  {t.relative_to(ROOT)}: +{a} ~{u} -{r}")

    if not any(total):
        print(f"  {len(targets)} mirror(s) already current")
    else:
        print(f"  {len(targets)} mirror(s): {total[0]} added, {total[1]} updated, {total[2]} removed")
    print("  → repos/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
