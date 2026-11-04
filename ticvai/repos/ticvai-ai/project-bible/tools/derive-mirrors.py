#!/usr/bin/env python3
"""Sync repos/*/project-bible/ and repos/ticvai-docs/ from the package root.

`repos/update-bible.sh` (retired 3 November 2026, CHG-R14J-002) said it plainly: **project-bible/ is a copy, not a
source.** Nothing ran it. On 20 August the mirror held 21 state files against the root's 113, 54 files differed, 144
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
import subprocess
import sys
from pathlib import Path

# Windows consoles are cp1252 and this tool closes by printing a unicode arrow. **The write
# has already happened by then**, so the traceback reported a failure on a run that succeeded
# — the most misleading shape an error can take.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

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


def ignored_at_root() -> set:
    """Files under the mirrored folders that git ignores at the root (package-relative paths).

    **A file the package keeps out of git is not mirrored** (1 October): the 24 MB single-file guest build
    in sources/designs/ is excluded at the root and is copied into a refresh worktree as an input, and this
    copied it into all six mirrors, where nothing ignores it -- 144 MB of untracked files one `git add`
    away from a commit. The same rule keeps the design videos out."""
    try:
        out = subprocess.run(["git", "-C", str(ROOT), "ls-files", "--others", "--ignored", "--exclude-standard",
                              "-z", "--", *MIRRORED], capture_output=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return set()
    return {Path(p) for p in out.decode("utf-8", "replace").split("\0") if p}


def sync(src: Path, dst: Path, skip: frozenset = frozenset()) -> tuple[int, int, int]:
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
            if rel in skip:
                continue
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


# **The contracts repository's `openapi/` is a copy of `contracts/`** (20 October 2026, r8 cause FOUNDATION-AI-C51,
# ticket 27640 SETUP-CLIENTS, CHG-R8GEN-011). It was copied once on 14 August and never again: it still held
# `spine/cross-cell.yaml` (renamed cross-region since) and lacked the satellite contracts added after, so the clients
# SETUP-CLIENTS generates from it were two months behind the package. Synced like a bible: added, updated, removed.
# **Every contract folder, not a list of three** (r13 system review D-10; CHG-R14J-003): contracts/devices/ (the ticket
# printer, OpenAPI 3.1, ADAM CR-448) was added after the list was written and never reached the repository the clients
# are generated from. The folders are read from contracts/ itself, so a new one cannot be left out.
OPENAPI = tuple((f"contracts/{d.name}", d.name) for d in sorted((ROOT / "contracts").iterdir())
                if d.is_dir() and any(d.glob("*.yaml")))


def sync_openapi() -> tuple[int, int, int]:
    dst = REPOS / "ticvai-contracts" / "openapi"
    if not dst.parent.is_dir():
        return 0, 0, 0
    added = updated = removed = 0
    wanted = {}
    for src, sub in OPENAPI:
        for f in sorted((ROOT / src).glob("*.yaml")):
            wanted[Path(sub) / f.name] = f
    if (ROOT / "contracts" / "README.md").is_file():
        wanted[Path("README.md")] = ROOT / "contracts" / "README.md"
    for rel, f in wanted.items():
        target = dst / rel
        if not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, target)
            added += 1
        elif not filecmp.cmp(f, target, shallow=False):
            shutil.copy2(f, target)
            updated += 1
    for f in sorted(dst.rglob("*"), reverse=True) if dst.is_dir() else []:
        if f.is_file() and f.relative_to(dst) not in wanted:
            f.unlink()
            removed += 1
        elif f.is_dir() and not any(f.iterdir()):
            f.rmdir()
    return added, updated, removed


# **Every README under repos/ comes from its own source** (2 November 2026, r13 root R13, CHG-R13R13-001; the Block A
# developer pull of 31 October: #27626 SETUP-CI, #27627 SETUP-ENV, #27633, #27634 and #27637 onboarding, #27640
# SETUP-CLIENTS). 104 README.md files under repos/ were byte copies of docs/active/README.md (the Active page) from
# the first commit on: the setup README every onboarding ticket links, each repository's own README and the infra
# README SETUP-ENV extends. No tool wrote them, so nothing put them right. Now this writes all of them:
#   - a repository's own README (and the cell module's) from its authored source in docs/repos/ (README_SOURCES);
#   - every other README that is no mirror of a package file -- one in a folder of ticvai-docs/ or a project-bible/
#     that is not a mirrored folder (setup/, the older documentation folders, the bible's root), or in INDEXED -- as
#     an index of its own folder's files.
# tools/check-repo-readmes.py fails when a README under repos/ is a copy of a package file other than its source.
README_SOURCES = {
    "README.md": "docs/repos/index.md",
    "ticvai-ai/README.md": "docs/repos/ticvai-ai.md",
    "ticvai-backend/README.md": "docs/repos/ticvai-backend.md",
    "ticvai-contracts/README.md": "docs/repos/ticvai-contracts.md",
    "ticvai-docs/README.md": "docs/repos/ticvai-docs.md",
    "ticvai-frontend/README.md": "docs/repos/ticvai-frontend.md",
    "ticvai-infra/README.md": "docs/repos/ticvai-infra.md",
    "ticvai-infra/terraform/modules/cell/README.md": "docs/repos/ticvai-infra-cell.md",
}
INDEXED = ("ticvai-contracts/standards",)
SOURCE_HEADER = "<!-- Written by tools/derive-mirrors.py from ticvai/{src}: edit that file, not this one. -->\n\n"
INDEX_HEADER = ("<!-- Written by tools/derive-mirrors.py: the index of this folder's files. Edit the files, "
                "not this index. -->\n\n")
TITLES = {"setup": "Setup standards", "project-bible": "The project bible"}


def first_heading(f: Path) -> str:
    """A file's first '# ' heading, or its name."""
    if f.suffix.lower() == ".md":
        try:
            for line in f.read_text(encoding="utf-8", errors="replace").splitlines()[:40]:
                if line.startswith("# "):
                    return line[2:].strip()
        except OSError:
            pass
    return f.name


def folder_index(folder: Path) -> str:
    """The README of a folder that has no source: its files, each with its first heading, and its subfolders."""
    title = TITLES.get(folder.name, f"{folder.name}/")
    rel = folder.relative_to(REPOS).as_posix()
    files = sorted((f for f in folder.iterdir() if f.is_file() and f.name != "README.md"
                    and not f.name.startswith(".")), key=lambda f: f.name.lower())
    subs = sorted((d for d in folder.iterdir() if d.is_dir() and not d.name.startswith(".")
                   and d.name != "__pycache__"), key=lambda d: d.name.lower())
    out = [INDEX_HEADER + f"# {title}", "", f"What `repos/{rel}/` holds.", ""]
    if files:
        out += ["| File | What it is |", "|---|---|"]
        out += [f"| [{f.name}]({f.name.replace(' ', '%20')}) | {first_heading(f).replace('|', '/')} |" for f in files]
        out.append("")
    if subs:
        out.append("Folders: " + ", ".join(
            f"[{d.name}/]({d.name.replace(' ', '%20')}/{'README.md' if (d / 'README.md').is_file() else ''})"
            for d in subs) + ".")
        out.append("")
    if not files and not subs:
        out += ["Nothing else is in this folder yet.", ""]
    return "\n".join(out)


def readme_targets() -> dict:
    """Every README under repos/ this tool writes: repos-relative path -> ("source", package path) or ("index", None)."""
    want = {rel: ("source", src) for rel, src in README_SOURCES.items() if (ROOT / src).is_file()}
    roots = [REPOS / "ticvai-docs"] + sorted(p for p in REPOS.glob("*/project-bible") if p.is_dir())
    for root in roots:
        if not root.is_dir():
            continue
        for f in sorted(root.rglob("README.md")):
            inner = f.relative_to(root).parts
            if inner[0] in MIRRORED:          # a mirror of a package file: sync() writes it
                continue
            want.setdefault(f.relative_to(REPOS).as_posix(), ("index", None))
    for folder in INDEXED:
        if (REPOS / folder).is_dir():
            want.setdefault(f"{folder}/README.md", ("index", None))
    return want


def write_readmes() -> tuple[int, int]:
    """Write every README of readme_targets(); returns (written, unchanged)."""
    written = same = 0
    for rel, (kind, src) in sorted(readme_targets().items()):
        target = REPOS / rel
        if not target.parent.is_dir():
            continue
        if kind == "source":
            body = SOURCE_HEADER.format(src=src) + (ROOT / src).read_text(encoding="utf-8")
        else:
            body = folder_index(target.parent)
        old = target.read_text(encoding="utf-8", errors="replace") if target.is_file() else None
        if old == body:
            same += 1
            continue
        with open(target, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(body)
        written += 1
    return written, same


# **The repositories' project documents come from what developers get, and no code is kept** (the lead, 3 November
# 2026, on the r13 system review's D-06: "Retire the code trees", keep the project documents, generated from the
# starters; CHG-R14J-002). repos/ticvai-backend, -frontend and -ai held hand-written code trees nothing kept in step
# with ADAM's starters, the code the setup zip really creates: every starter fix of 26 September onwards (the decimal
# ban, the permission resolver's deny-overrides-allow, many tenants per cell, the outbox ordering, lastWriterWins)
# never reached them, and their rules page (project-bible/repos/backend.md) still taught .NET 8, one tenant per
# jurisdiction and ULIDs (D-04). The code is gone; what stays is written here at every refresh:
#   - each of those repositories' CLAUDE.md, a copy of the starter's (viewer/mcp/setup/starters/<role>/CLAUDE.md);
#   - every bible's setup/, a copy of the starter docs (the files setup.ps1 gives every clone as project-bible/setup/);
#   - every bible's repos/ (one rules page per repository): backend, frontend and ai from the starter's CLAUDE.md,
#     contracts, infra and docs from their authored sources in docs/repos/rules/;
#   - the bible folders that only shadowed a mirrored docs/ folder with an older partial copy (adr/, architecture/,
#     active/, registers/: 18 of 73 ADRs) and the August `.synced-at` stamp are removed: project-bible/docs/ holds the
#     whole current set, and the read orders point there.
# tools/check-repo-trees.py fails on anything else under repos/<repository>/ and on a copy that differs from its source,
# and fails closed when the starters are not beside the package.
STARTERS = ROOT.parent / "viewer" / "mcp" / "setup" / "starters"
STARTER_ROLES = {"ticvai-backend": "backend", "ticvai-frontend": "frontend", "ticvai-ai": "ai"}
RULE_PAGES = {"backend.md": ("starter", "backend/CLAUDE.md"), "frontend.md": ("starter", "frontend/CLAUDE.md"),
              "ai.md": ("starter", "ai/CLAUDE.md"), "contracts.md": ("package", "docs/repos/rules/contracts.md"),
              "infra.md": ("package", "docs/repos/rules/infra.md"), "docs.md": ("package", "docs/repos/rules/docs.md")}
SHADOWED = ("adr", "architecture", "active", "registers")
STARTER_HEADER = ("<!-- Written by tools/derive-mirrors.py from ADAM's starter viewer/mcp/setup/starters/{src}, the file "
                  "the setup zip gives the repository: edit that file, not this one. -->\n\n")


def rule_page(kind: str, src: str) -> str | None:
    f = (STARTERS / src) if kind == "starter" else (ROOT / src)
    if not f.is_file():
        return None
    head = STARTER_HEADER.format(src=src) if kind == "starter" else SOURCE_HEADER.format(src=src)
    return head + f.read_text(encoding="utf-8")


def project_documents() -> dict:
    """{repos-relative path: text} for every project document this tool writes from a starter or a rules source."""
    out = {}
    for repo, role in STARTER_ROLES.items():
        if (REPOS / repo).is_dir():
            body = rule_page("starter", f"{role}/CLAUDE.md")
            if body is not None:
                out[f"{repo}/CLAUDE.md"] = body
    bibles = [REPOS / "ticvai-docs"] + sorted(p for p in REPOS.glob("*/project-bible") if p.is_dir())
    docs = sorted((STARTERS / "docs").glob("*.md")) if (STARTERS / "docs").is_dir() else []
    for b in bibles:
        if not b.is_dir():
            continue
        rel = b.relative_to(REPOS).as_posix()
        for d in docs:
            out[f"{rel}/setup/{d.name}"] = d.read_text(encoding="utf-8")
        for name, (kind, src) in RULE_PAGES.items():
            body = rule_page(kind, src)
            if body is not None:
                out[f"{rel}/repos/{name}"] = body
    return out


def write_project_documents() -> tuple[int, int, int]:
    """Write project_documents(); prune what a written folder no longer has and the shadowed folders. (w, same, rm)"""
    if not STARTERS.is_dir():
        print(f"  ! ADAM's starters are not at {STARTERS}: the repositories' CLAUDE.md, setup/ and rules pages were not "
              "written (check-repo-trees fails until they are)")
        return 0, 0, 0
    written = same = removed = 0
    want = project_documents()
    for rel, body in sorted(want.items()):
        target = REPOS / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        old = target.read_text(encoding="utf-8", errors="replace") if target.is_file() else None
        if old == body:
            same += 1
            continue
        with open(target, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(body)
        written += 1
    bibles = [REPOS / "ticvai-docs"] + sorted(p for p in REPOS.glob("*/project-bible") if p.is_dir())
    for b in bibles:
        rel = b.relative_to(REPOS).as_posix()
        for folder in ("setup", "repos"):
            d = b / folder
            for f in sorted(d.glob("*")) if d.is_dir() else []:
                if f.is_file() and f.name != "README.md" and f"{rel}/{folder}/{f.name}" not in want:
                    f.unlink()
                    removed += 1
        for folder in SHADOWED:
            if (b / folder).is_dir() and (ROOT / "docs" / folder).is_dir():
                removed += sum(1 for f in (b / folder).rglob("*") if f.is_file())
                shutil.rmtree(b / folder)
        if (b / ".synced-at").is_file():
            (b / ".synced-at").unlink()
            removed += 1
    return written, same, removed


def main() -> int:
    if not REPOS.is_dir():
        print("  no repos/ — nothing to mirror")
        return 0
    a, u, r = sync_openapi()
    if a or u or r:
        print(f"  repos/ticvai-contracts/openapi: +{a} ~{u} -{r} (a copy of contracts/)")

    targets = []
    docs = REPOS / "ticvai-docs"
    if docs.is_dir():
        targets.append(docs)
    for repo in sorted(REPOS.iterdir()):
        bible = repo / "project-bible"
        if bible.is_dir():
            targets.append(bible)

    total = [0, 0, 0]
    skip = frozenset(ignored_at_root())
    for t in targets:
        a, u, r = sync(ROOT, t, skip)
        total = [total[0] + a, total[1] + u, total[2] + r]
        if a or u or r:
            print(f"  {t.relative_to(ROOT)}: +{a} ~{u} -{r}")

    if not any(total):
        print(f"  {len(targets)} mirror(s) already current")
    else:
        print(f"  {len(targets)} mirror(s): {total[0]} added, {total[1]} updated, {total[2]} removed")
    w, s_, r = write_project_documents()
    print(f"  project documents: {w} written, {s_} already current, {r} removed (ADAM's starters, docs/repos/rules)")
    # After the mirrors: an index lists its folder's files as the sync left them.
    w, s = write_readmes()
    print(f"  repository READMEs: {w} written, {s} already current (docs/repos/ sources and folder indexes)")
    print("  → repos/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
