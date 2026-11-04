#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Nothing ADAM tells an agent asks it to choose a release: developers and agents are always on the latest one.

**14 October 2026** (CHG-ADM-001). Chinmay: "the release system is creating confusion among the agents they ask if
r3 or r4. we always want agents to pull the latest." Until then adam_pull kept a ticket at the release tag of its
first pull, and the tool text, the /ticket command and the rule docs told the agent to stop, show a "Spec changed"
section and ask the person whether to adam_repin or keep building against the old tag. Now every pull is at the
release ADAM serves, the pin moves by itself (server-side, logged `auto`), and the only thing left to say is what
changed since the ticket's previous pull. This holds the text to that:

    LR-CHOOSE   a file that reaches an agent or a developer (the connector's tool text and next steps, the
                server's instructions, the hooks, the setup commands and CLAUDE.md starters, ADAM's server
                text, and the rule docs) tells them to choose or ask between releases, to re-pin, or that a
                started ticket stays on its start tag
    LR-LATEST   the places that must say it do not say "always on the latest release": adam_pull's description,
                both /ticket commands, ticvai/CLAUDE.md, and the release runbook
    LR-AUTO     ADAM's pin route no longer moves a pin that is behind on pull (the `auto` move and `movedFrom`)

**The latest release is only the latest if ADAM has its tag** (14 October 2026, PROCESS-LOG P-20, CHG-GTE-006). r5 was
tagged locally and never pushed: the runbook's "push both remotes" pushed the branch, a bare `git push` sends no tag,
and ADAM's server knows only the tags it fetched, so every pull served r4 while OpenProject said r5. Two more rules:

    LR-TAG-PUSH    the release runbook's step 5 (Tag) does not push the tag by name to both remotes
                   (`git push origin main r<N>`, `git push github main r<N>`), or its step 6 (Distribute) does not
                   end with one adam_pull whose release must say r<N>
    LR-TAG-REMOTE  with --remotes only (it needs the network; the gate runs without it): the newest `r<N>` tag here
                   is missing from `origin` or `github` (git ls-remote). Run it after pushing, step 5 of the runbook.

**The tag ADAM serves carries its own release bundle** (2 November 2026, r13 root R12, CHG-R13R12-001). ADAM shows a
ticket's text from `handoff/service-docs/op-release.json` only when that bundle is the served tag's; otherwise it falls
back to the plan row, which lacks the pointer's scope, repository and design lines. In the r12 rehearsal the candidate's
committed bundle was r11's, and #27985 APP-SETUP-DEV-008 lost those lines. One more rule:

    LR-BUNDLE      with --tag r<N> (the runbook's step 5 runs it before `git tag`), or when HEAD already carries an
                   r<N> tag: the committed bundle's `release` is not r<N>. Rebuild it at r<N>
                   (`python3 tools/op-release.py --release r<N>`) and commit it before the tag.

    LR-COMMITS     with --tag r<N> (or an r<N> tag on HEAD): `check-changelog.py --since r<N-1>` fails, so a commit
                   since the last release touches an authored input and names no change id. The tag is refused
                   (r14, review E-03, CHG-R14I-003): r10 and r11 were tagged with three such commits, because the
                   commit rule was a manual runbook step; it is now in the gate (run-checks.py ARGS) and here.

What ADAM serves cannot be read offline; the runbook's closing adam_pull is the check on the server itself.

Read-only. Exit 1 on a finding not in `handoff/audit-baseline.json` (tools/audit_guard.py).

    python3 tools/check-adam-latest-release.py [--all] [--remotes] [--tag r<N>] [--self-test]
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {
    "LR-CHOOSE": "no text tells an agent to choose or ask between releases, or to re-pin (CHG-ADM-001)",
    "LR-LATEST": "adam_pull, /ticket and the rule docs say the agent is always on the latest release (CHG-ADM-001)",
    "LR-AUTO": "ADAM's pin route moves a pin that is behind to the latest release on pull (CHG-ADM-001)",
    "LR-TAG-PUSH": "the runbook pushes the release tag by name to both remotes and ends with an adam_pull that "
                   "must say r<N> (P-20, CHG-GTE-006)",
    "LR-TAG-REMOTE": "with --remotes: the newest r<N> tag is on origin and github (P-20, CHG-GTE-006)",
    "LR-BUNDLE": "the tag being cut carries its own release bundle: op-release.json's release is r<N> (R12, "
                 "CHG-R13R12-001)",
    "LR-COMMITS": "the tag being cut: every commit since the last release names its change id (check-changelog "
                  "--since; review E-03, CHG-R14I-003)",
}
BUNDLE = g.ROOT / "handoff" / "service-docs" / "op-release.json"
REMOTES = ("origin", "github")
VIEWER = g.ROOT.parent / "viewer"

# Instructions to choose, ask or stay. Each is an instruction, not a mention: "there is nothing to re-pin" and
# "adam_repin is not needed" are what the new text says, and none of these match them.
CHOOSE = [
    r"keep building against (the )?(pin|pinned|older|old|start)",
    r"re-?pin (is )?required",
    r"makes? the re-?pin required",
    r"either take the change",
    r"whether to (take the change|re-?pin|accept the change|take it)",
    r"choose between taking",
    r"ask me; do not choose",
    r"files? stay at the pinned release",
    r"still the (pinned release|release you are pinned to)",
    r"keeps? serving the developer",
    r"until they re-?pin",
    r"you stay on your pin",
    r"re-?pin to the new release",
    r"both sides re-?pin",
    r"as a diff, and you decide",
    r"stays? on (its|the|their) start(ed)? tag",
    r"release tag they started on",
    r"take the change \(adam_repin",
    r"run adam_repin before building",
]
CHOOSE_RE = re.compile("|".join(f"(?:{p})" for p in CHOOSE), re.I)
LATEST_RE = re.compile(r"always (on|build(ing)? against) the latest release", re.I)


def scanned() -> list:
    """Every file whose words reach an agent or a developer about releases."""
    files = [
        VIEWER / "mcp" / "tools.mjs", VIEWER / "mcp" / "server.mjs", VIEWER / "mcp" / "adam-hook.mjs",
        VIEWER / "mcp" / "README.md", VIEWER / "mcp" / "setup" / "README.txt",
        VIEWER / "api" / "main.py", VIEWER / "api" / "cr_notice.py", VIEWER / "api" / "settle_changes.py",
        VIEWER / "api" / "README.md",
        g.ROOT / "CLAUDE.md", g.ROOT / "docs" / "active" / "release-runbook.md",
        g.ROOT / "docs" / "active" / "developer-brief.md", g.ROOT / "changes" / "README.md",
    ]
    files += sorted((VIEWER / "mcp" / "hooks").glob("*"))
    for side in sorted((VIEWER / "mcp" / "setup" / "starters").glob("*")):
        files += [side / "CLAUDE.md"] + sorted((side / ".claude" / "commands").glob("*.md"))
    return [f for f in files if f.is_file()]


def rel(path: Path) -> str:
    try:
        return path.relative_to(g.ROOT.parent).as_posix()
    except ValueError:
        return path.as_posix()


def tag_rules(guard) -> None:
    """LR-TAG-PUSH on the runbook's text; LR-TAG-REMOTE against the remotes when --remotes is given."""
    book = g.ROOT / "docs" / "active" / "release-runbook.md"
    text = book.read_text(encoding="utf-8", errors="replace") if book.is_file() else ""
    sections = {m.group(1): m.group(2) for m in re.finditer(r"^## (\d+)\.[^\n]*\n(.*?)(?=^## |\Z)", text, re.M | re.S)}
    tag = re.sub(r"\s+", " ", sections.get("5", ""))
    for remote in REMOTES:
        if f"git push {remote} main r<N>" not in tag:
            guard.add("LR-TAG-PUSH", f"runbook:5:{remote}",
                      f"the release runbook's step 5 does not push the tag by name to {remote} "
                      f"(`git push {remote} main r<N>`): a bare push sends no tag and ADAM serves the release before")
    bullets = re.split(r"^- ", sections.get("6", ""), flags=re.M)
    last = re.sub(r"\s+", " ", bullets[-1] if len(bullets) > 1 else "")
    if "adam_pull" not in last or "r<N>" not in last:
        guard.add("LR-TAG-PUSH", "runbook:6:pull",
                  "the release runbook's step 6 does not end with one adam_pull whose release must say r<N>")

    if "--remotes" not in sys.argv[1:]:
        guard.note("remotes not compared (pass --remotes after pushing the tag, the runbook's step 5)")
        return
    import subprocess
    here = g.ROOT.parent
    out = subprocess.run(["git", "-C", str(here), "tag", "-l", "r*"], capture_output=True, text=True).stdout
    tags = sorted((t for t in out.split() if re.fullmatch(r"r\d+", t)), key=lambda t: int(t[1:]))
    if not tags:
        guard.note("no r<N> tag here: nothing to compare")
        return
    newest = tags[-1]
    for remote in REMOTES:
        res = subprocess.run(["git", "-C", str(here), "ls-remote", "--tags", remote, f"refs/tags/{newest}"],
                             capture_output=True, text=True)
        if res.returncode != 0:
            guard.add("LR-TAG-REMOTE", f"{remote}:unreachable",
                      f"{remote} could not be read (git ls-remote exit {res.returncode}): whether it has {newest} is unknown")
        elif not res.stdout.strip():
            guard.add("LR-TAG-REMOTE", f"{remote}:{newest}",
                      f"{newest}, the newest release tag here, is not on {remote}: run `git push {remote} main {newest}`; "
                      "ADAM serves the newest tag its server fetched")
    guard.note(f"{newest} compared with {', '.join(REMOTES)}")


def bundle_finding(bundle_release, tag):
    """The LR-BUNDLE message for a bundle at `bundle_release` and a tag `tag`, or None when they agree."""
    if not tag or bundle_release == tag:
        return None
    have = f"is {bundle_release}'s" if bundle_release else "is missing or names no release"
    return (f"handoff/service-docs/op-release.json {have}, and the tag being cut is {tag}: ADAM would show each "
            f"ticket's plan row instead of its pointer. Rebuild it (`python3 tools/op-release.py --release {tag}`) "
            "and commit it before the tag")


def tag_being_cut(argv):
    """--tag r<N>, else an r<N> tag already on HEAD, else None."""
    if "--tag" in argv:
        i = argv.index("--tag")
        return argv[i + 1] if i + 1 < len(argv) else ""
    try:
        out = subprocess.run(["git", "-C", str(g.ROOT.parent), "tag", "--points-at", "HEAD"],
                             capture_output=True, text=True).stdout
    except OSError:
        return None
    tags = sorted((t for t in out.split() if re.fullmatch(r"r\d+", t)), key=lambda t: int(t[1:]))
    return tags[-1] if tags else None


def bundle_rule(guard, argv) -> None:
    tag = tag_being_cut(argv)
    if tag is None:
        guard.note("no tag being cut (pass --tag r<N> before `git tag`, the runbook's step 5): bundle not compared")
        return
    if not re.fullmatch(r"r\d+", tag or ""):
        guard.add("LR-BUNDLE", f"tag:{tag or '?'}", f"--tag {tag or '(empty)'} is not r<N>")
        return
    try:
        release = json.loads(BUNDLE.read_text(encoding="utf-8")).get("release")
    except (OSError, ValueError):
        release = None
    msg = bundle_finding(release, tag)
    if msg:
        guard.add("LR-BUNDLE", f"bundle:{tag}", msg)
    else:
        guard.note(f"the bundle is {tag}'s, the tag being cut")
    commits_rule(guard, tag)


def previous_release(tag):
    """The newest r<M> tag with M < N, or None."""
    try:
        out = subprocess.run(["git", "-C", str(g.ROOT), "tag", "-l", "r*"], capture_output=True, text=True).stdout
    except OSError:
        return None
    n = int(tag[1:])
    older = [t for t in out.split() if re.fullmatch(r"r\d+", t) and int(t[1:]) < n]
    return max(older, key=lambda t: int(t[1:])) if older else None


def commits_rule(guard, tag) -> None:
    """LR-COMMITS: every commit since the last release names its change (check-changelog's commit rule)."""
    prev = previous_release(tag)
    if prev is None:
        if int(tag[1:]) > 1:
            guard.add("LR-COMMITS", f"commits:{tag}", f"no release tag before {tag} in this clone: the commit rule "
                                                      "cannot be checked (git fetch --tags origin)", strict=True)
        return
    p = subprocess.run([sys.executable, str(g.ROOT / "tools" / "check-changelog.py"), "--since", prev],
                       cwd=str(g.ROOT), capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env=dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8"))
    if p.returncode != 0:
        bad = [l.strip() for l in (p.stdout or "").splitlines() if "names no change id" in l][:3]
        guard.add("LR-COMMITS", f"commits:{tag}", f"check-changelog --since {prev} fails: the tag {tag} is refused "
                                                  f"until every commit since {prev} names its change id"
                                                  + (" (" + "; ".join(bad)[:300] + ")" if bad else ""), strict=True)
    else:
        guard.note(f"every commit since {prev} names its change id (check-changelog --since {prev})")


def self_test() -> int:
    fails = []
    for got, want, name in (
            (bundle_finding("r12", "r12"), None, "the bundle is the tag's"),
            (bool(bundle_finding("r11", "r12")), True, "a bundle one release behind (the r12 rehearsal)"),
            (bool(bundle_finding(None, "r13")), True, "no bundle"),
            (bundle_finding("r12", None), None, "no tag being cut"),
            ("op-release.py --release r13" in (bundle_finding("r12", "r13") or ""), True, "names the rebuild"),
            (tag_being_cut(["--tag", "r13"]), "r13", "--tag names the tag"),
            (tag_being_cut(["--tag"]), "", "--tag with nothing after it")):
        if got != want:
            fails.append(f"{name}: got {got!r}, expected {want!r}")
    for f in fails:
        print("  FAIL", f)
    print(f"check-adam-latest-release self-test: {7 - len(fails)} of 7 passed")
    return 1 if fails else 0


def main() -> int:
    g.force_utf8()
    if "--self-test" in sys.argv[1:]:
        return self_test()
    guard = g.Guard("check-adam-latest-release", RULES)
    tag_rules(guard)
    bundle_rule(guard, sys.argv[1:])
    if not VIEWER.exists():
        guard.note("viewer/ not found beside ticvai/: nothing compared")
        return guard.finish()

    for path in scanned():
        text = path.read_text(encoding="utf-8", errors="replace")
        # Joined across line breaks: the tool text is concatenated strings and the docs are wrapped.
        flat = re.sub(r"'\s*\+\s*'|`\s*\+\s*'|'\s*\+\s*`", "", text)
        flat = re.sub(r"\s+", " ", flat)
        for m in CHOOSE_RE.finditer(flat):
            phrase = m.group(0).lower()
            guard.add("LR-CHOOSE", f"{rel(path)}:{phrase}",
                      f"{rel(path)}: \"{flat[max(0, m.start() - 60):m.end() + 60].strip()}\"")

    must = {
        VIEWER / "mcp" / "tools.mjs": "adam_pull's description",
        VIEWER / "mcp" / "setup" / "starters" / "backend" / ".claude" / "commands" / "ticket.md": "/ticket (backend)",
        VIEWER / "mcp" / "setup" / "starters" / "frontend" / ".claude" / "commands" / "ticket.md": "/ticket (frontend)",
        g.ROOT / "CLAUDE.md": "the binding rules",
        g.ROOT / "docs" / "active" / "release-runbook.md": "the release runbook",
    }
    for path, what in must.items():
        text = path.read_text(encoding="utf-8", errors="replace") if path.is_file() else ""
        flat = re.sub(r"\s+", " ", re.sub(r"'\s*\+\s*'", "", text))
        if path.name == "tools.mjs":
            m = re.search(r"name: 'adam_pull',\s*description:(.*?)inputSchema", flat, re.S)
            flat = m.group(1) if m else ""
        if not LATEST_RE.search(flat):
            guard.add("LR-LATEST", rel(path), f"{what} ({rel(path)}) does not say the agent is always on the latest release")

    main_py = VIEWER / "api" / "main.py"
    src = main_py.read_text(encoding="utf-8", errors="replace") if main_py.is_file() else ""
    m = re.search(r"def set_pin\(.*?(?=\n@app\.)", src, re.S)
    body = m.group(0) if m else ""
    if '"auto"' not in body or "movedFrom" not in body:
        guard.add("LR-AUTO", "viewer/api/main.py:set_pin",
                  "set_pin does not move a pin that is behind on pull (no `auto` move answered with `movedFrom`)")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
