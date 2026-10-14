#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Write every screen's component path, and ADAM setup's repository table, from each repository's profile.

**14 October 2026, CHG-RPO-002 and CHG-RPO-003** (the Block A audit, class check-frontend-repos/FR-OLD-PATH). The
screens were written against one Nx workspace, so 1,935 screens on the six platforms with a GitLab repository named
their component `apps/<app>/src/routes/<area>/<Component>.tsx`, a folder no repository has; ADAM served that path
and #27741's developer found the guest app a single React Native CLI app with `src/` at its root (problem 3).

A repository's profile is authored once, in `docs/active/frontend-repos.yaml` (`observed:` over `layout.default`,
with the entry's own `profile:` for what nobody observed), and read through `tools/frontend_repos.py`. This is the
generator rule that applies it:

1. **screens/P*.yaml**: on a platform with a repository, each `implementation.component` becomes
   `frontend_repos.component_path()`: `<screensDir>/<area>/<Component>.tsx`, relative to the repository's root.
   Line-level: only the `component:` line of a screen whose path changes is rewritten, nothing else in the file
   moves. A platform with no repository keeps its authored path.
2. **viewer/mcp/setup/starters/frontend/CLAUDE.md** (`--setup`): the block between `frontend_repos.SETUP_BEGIN` and
   `SETUP_END`, what each repository holds, from `frontend_repos.setup_block()`. That file ships in ADAM's setup
   zip, so a change to it needs an ADAM deploy.

Run it after any change to a repository's profile (an owner confirming or correcting a layout), then re-derive
the ticket text. check-frontend-repos holds both: FR-OLD-PATH (a screen not where its profile puts it) and
FR-SETUP-TABLE (the setup block differs from the profile). Not run by refresh: it writes authored inputs.

    python3 tools/apply-repo-layout.py [--setup] [--check]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import frontend_repos as fr  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SCREENS = ROOT / "screens"
STARTER = ROOT.parent / "viewer" / "mcp" / "setup" / "starters" / "frontend" / "CLAUDE.md"
CODE = re.compile(r"^  code:\s*['\"]?(P\d\d)['\"]?\s*$")
SID = re.compile(r"^- id:\s*['\"]?([A-Z]{2,5}-\d{3,4})['\"]?\s*$")
COMP = re.compile(r"^(\s+component:\s*)(['\"]?)([^'\"\s#]+)\2(\s*)$")


def screens_pass(write: bool) -> dict:
    """{platform: [(screen id, old, new)]} for every component line whose path the profile changes."""
    changed: dict = {}
    for f in sorted(SCREENS.glob("P*.yaml")):
        raw = f.read_bytes().decode("utf-8")
        nl = "\r\n" if "\r\n" in raw else "\n"
        lines = raw.split(nl)
        code, sid, in_impl, edits = None, None, False, 0
        for i, ln in enumerate(lines):
            m = CODE.match(ln)
            if m and code is None:
                code = m.group(1)
                continue
            m = SID.match(ln)
            if m:
                sid, in_impl = m.group(1), False
                continue
            if re.match(r"^  implementation:\s*$", ln):
                in_impl = True
                continue
            if in_impl and re.match(r"^  \S", ln):
                in_impl = False
            m = COMP.match(ln) if in_impl and code else None
            if not m:
                continue
            old = m.group(3)
            new = fr.component_path(code, old)
            if new and new != old:
                changed.setdefault(code, []).append((sid, old, new))
                lines[i] = f"{m.group(1)}{m.group(2)}{new}{m.group(2)}{m.group(4)}"
                edits += 1
        if write and edits:
            f.write_bytes(nl.join(lines).encode("utf-8"))
    return changed


def setup_pass(write: bool) -> bool:
    """True when the setup block differs from the profile (and, with write, rewrites it)."""
    if not STARTER.exists():
        print(f"  {STARTER} not found: the setup block was not written")
        return False
    raw = STARTER.read_bytes().decode("utf-8")
    nl = "\r\n" if "\r\n" in raw else "\n"
    text = raw.replace("\r\n", "\n")
    block = fr.setup_block()
    if fr.SETUP_BEGIN in text and fr.SETUP_END in text:
        head, rest = text.split(fr.SETUP_BEGIN, 1)
        old, tail = rest.split(fr.SETUP_END, 1)
        new_text = head + block + tail
    else:
        # First time: after the platform-to-repository table, before "A screen names its platform".
        anchor = "\nA screen names its platform"
        if anchor not in text:
            print("  setup CLAUDE.md has no anchor for the block; not written")
            return True
        new_text = text.replace(anchor, "\n" + block + "\n" + anchor, 1)
    if new_text == text:
        return False
    if write:
        STARTER.write_bytes(new_text.replace("\n", nl).encode("utf-8"))
    return True


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--setup", action="store_true", help="also write the setup CLAUDE.md block")
    ap.add_argument("--check", action="store_true", help="write nothing; exit 1 when anything would change")
    a = ap.parse_args()
    changed = screens_pass(not a.check)
    total = sum(len(v) for v in changed.values())
    verb = "would change" if a.check else "changed"
    print(f"  {total} component path(s) {verb}" + (": " + ", ".join(f"{c} {len(v)}" for c, v in sorted(changed.items()))
                                                    if changed else ""))
    for c, v in sorted(changed.items()):
        sid, old, new = v[0]
        print(f"    e.g. {c} {sid}: {old} -> {new}")
    setup = setup_pass(a.setup and not a.check) if (a.setup or a.check) else False
    if setup:
        print(f"  setup CLAUDE.md block {'differs from the profile' if a.check else 'written'}")
    return 1 if a.check and (total or setup) else 0


if __name__ == "__main__":
    sys.exit(main())
