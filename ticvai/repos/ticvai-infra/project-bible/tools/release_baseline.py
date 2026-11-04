#!/usr/bin/env python3
"""The release a guard compares against: the git tag `r1`, read without touching the working tree.

**Three checks freeze something at the first release** (plan item 1C, council of 1 October): the
baseline migrations (`check-migration-freeze.py`, and `derive-ddl.py`'s frozen mode), the pushed
ticket keys (`check-key-stability.py`), and the contracts (`check-contract-compat.py`). Until the
tag exists each of them passes and says it is not frozen yet; the tag is the act that freezes.

**But "no tag" is no longer "before the first release"** (r14, review E-05, CHG-R14I-004). Thirteen releases are out
and handoff/service-docs/pms-map.json holds thousands of pushed tickets, yet a clone without tags (`--no-tags`, a
shallow CI clone, a tarball, a fresh agent checkout) made every freeze check pass and let `derive-ddl.py --apply`
rewrite migrations already applied to live databases. So when the package shows it has been released
(`released()`: op-release.json names a release r1 or later, or pms-map.json holds a pushed ticket) and the default
tag is missing, `baseline_commit()` stops the tool with the fetch to run. `--baseline REF` (testing) is unchanged.

**`--baseline REF` exists for testing.** Any commit-ish works (`HEAD`, a branch), so a freeze can be
exercised in a throwaway worktree without creating a real `r1` tag that would freeze the package.

**Paths are relative to the package** (`ticvai/`), not the repository: every git call runs with the
package as its working directory and uses `REF:./path`, so the package can sit at any depth.

    from release_baseline import baseline_commit, show, ls_tree, changed_since
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TAG = "r1"


def _git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=check)


class MissingReleaseTag(SystemExit):
    """The package has been released and the release tag is not in this clone."""


def released(root: Path = ROOT) -> str | None:
    """Why the package counts as released ("op-release.json release r13"), or None when it has not been."""
    sd = root / "handoff" / "service-docs"
    try:
        rel = json.loads((sd / "op-release.json").read_text(encoding="utf-8")).get("release")
        if re.fullmatch(r"r\d+", str(rel or "")) and int(str(rel)[1:]) >= 1:
            return f"handoff/service-docs/op-release.json names release {rel}"
    except (OSError, ValueError):
        pass
    try:
        mp = json.loads((sd / "pms-map.json").read_text(encoding="utf-8"))
        if mp:
            return f"handoff/service-docs/pms-map.json holds {len(mp)} pushed ticket(s)"
    except (OSError, ValueError):
        pass
    return None


def baseline_commit(ref: str | None = None) -> str | None:
    """The commit `ref` (default: the tag r1) points at, or None when it does not exist.

    A bare name is tried as a tag first, so a branch that happens to be called `r1` never freezes
    anything. With no `ref` and no r1 tag in a package that has been released, it raises
    MissingReleaseTag (a SystemExit naming the fetch): a missing tag is a broken clone, not a package before r1."""
    explicit = ref is not None
    ref = ref or DEFAULT_TAG
    for cand in (f"refs/tags/{ref}", ref):
        p = _git("rev-parse", "-q", "--verify", f"{cand}^{{commit}}", check=False)
        if p.returncode == 0 and p.stdout.strip():
            return p.stdout.decode().strip()
    why = None if explicit else released()
    if why:
        raise MissingReleaseTag(
            f"FAIL - the release tag {ref} is not in this clone, but the package has been released ({why}); "
            f"without it every freeze would pass and derive-ddl would regenerate frozen migrations. "
            f"Fetch the tags (git fetch --tags origin) and run again.")
    return None


def show(commit: str, path: str) -> bytes | None:
    """A file's blob at `commit` (git's stored form, LF line ends), or None when it did not exist."""
    p = _git("show", f"{commit}:./{path}", check=False)
    return p.stdout if p.returncode == 0 else None


def ls_tree(commit: str, path: str) -> list[str]:
    """Every file under `path` at `commit`, relative to the package."""
    p = _git("ls-tree", "-r", "--name-only", commit, "--", path, check=False)
    return [l for l in p.stdout.decode("utf-8", "replace").splitlines() if l.strip()]


def changed_since(commit: str, path: str) -> list[tuple[str, str]]:
    """[(status, path)] for every file under `path` whose content differs from `commit`, working tree
    included: M modified, D deleted, A added (committed or staged since), ? untracked.

    **Through git, not by reading bytes.** `core.autocrlf` is true on this machine, so a checked-out
    `.sql` file has CRLF line ends and its blob has LF; a byte comparison would call every file
    changed. `git diff` applies the same clean filter a commit would."""
    out = []
    p = _git("diff", "--no-renames", "--relative", "--name-status", commit, "--", path, check=False)
    for line in p.stdout.decode("utf-8", "replace").splitlines():
        status, _, name = line.partition("\t")
        if name:
            out.append((status[:1], name))
    p = _git("ls-files", "--others", "--exclude-standard", "--", path, check=False)
    out += [("?", l) for l in p.stdout.decode("utf-8", "replace").splitlines() if l.strip()]
    return out


def describe(ref: str | None, commit: str) -> str:
    """`r1 (5bf9b05)` for messages."""
    return f"{ref or DEFAULT_TAG} ({commit[:7]})"
