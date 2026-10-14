#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A blocker is always a CR, then the next workable ticket: every text an agent reads says so, and ADAM can answer it.

**14 October 2026** (CHG-ADM-004). Chinmay: "if there is blocker we log it as CR always. and than scour for next
tasks that can be completed and if existing blockers effect it". When the package blocks a ticket, the agent raises
a CR with `blocking: true`, proposes the ticket On hold naming it, never works around it and never builds a guess,
and then takes the next ticket no open blocking CR affects (`adam_board` with `only: "workable"`). This holds:

    BR-RULE        a place an agent or a developer reads at the moment of a blocker does not carry the rule: the
                   connector's BLOCKER_RULE and the tool texts that use it (adam_board, adam_draft_change, adam_pull,
                   adam_raise_change's next step), the server's instructions, the /ticket /board /cr /done commands
                   and the CLAUDE.md starters, ticvai/CLAUDE.md and the developer brief
    BR-WORKAROUND  one of those texts suggests working around a blocker or building on a guess ("work around it"
                   without a never/don't before it; "build whatever the question does not touch"; "carry on with
                   the rest of the ticket")
    BR-SERVER      ADAM cannot answer which tickets an open blocking CR affects: no api/blockers.py `affecting`,
                   no `blockedBy` on the board or the work package, or no `only` filter on the board

Read-only. Exit 1 on a finding not in `handoff/audit-baseline.json` (tools/audit_guard.py).

    python3 tools/check-adam-blocker-rule.py [--all]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {
    "BR-RULE": "every text an agent reads at a blocker says: CR always, On hold, never a workaround, next workable (CHG-ADM-004)",
    "BR-WORKAROUND": "no such text suggests working around a blocker or building on a guess (CHG-ADM-004)",
    "BR-SERVER": "ADAM answers which tickets an open blocking CR affects, on the board and the pull (CHG-ADM-004)",
}
VIEWER = g.ROOT.parent / "viewer"
STARTERS = VIEWER / "mcp" / "setup" / "starters"

# A suggestion to go around, unless a negation stands just before it.
AROUND = re.compile(r"work(s|ing|ed)? around|build(s|ing)? (on )?(a|the) (sensible )?guess|"
                    r"build whatever the question does not touch|carry on with the rest of the ticket", re.I)
NEGATION = re.compile(r"\b(never|not|no|don't|do not|nor|without|instead of|rather than)\b[^.]{0,40}$", re.I)


def flat(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace") if path.is_file() else ""
    text = re.sub(r"'\s*\+\s*'|`\s*\+\s*'|'\s*\+\s*`", "", text)
    return re.sub(r"\s+", " ", text)


def rel(path: Path) -> str:
    try:
        return path.relative_to(g.ROOT.parent).as_posix()
    except ValueError:
        return path.as_posix()


def description(src: str, tool: str) -> str:
    m = re.search(rf"name: '{tool}', description:(.*?)inputSchema", src)
    return m.group(1) if m else ""


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-adam-blocker-rule", RULES)
    tools, server = VIEWER / "mcp" / "tools.mjs", VIEWER / "mcp" / "server.mjs"
    src = flat(tools)

    rule = re.search(r"export const BLOCKER_RULE = (.*?);", src)
    body = rule.group(1) if rule else ""
    for need in ("always raise a change request", "blocking: true", "On hold", "Never work around",
                 "never build a guess", 'only: "workable"', "say yes"):
        if need.lower() not in body.lower():
            guard.add("BR-RULE", f"BLOCKER_RULE:{need}", f"viewer/mcp/tools.mjs BLOCKER_RULE does not say \"{need}\"")
    for tool in ("adam_board", "adam_draft_change"):
        if "BLOCKER_RULE" not in description(src, tool):
            guard.add("BR-RULE", f"{tool}:description", f"{tool}'s description does not carry BLOCKER_RULE")
    if "Blocked by" not in description(src, "adam_pull") or 'only: "workable"' not in description(src, "adam_pull"):
        guard.add("BR-RULE", "adam_pull:description", "adam_pull's description does not name \"Blocked by\" and the "
                                                      "next workable ticket")
    if not re.search(r"Filed as \$\{change\.id\}\. Propose .{0,400}only: \"workable\"", src):
        guard.add("BR-RULE", "adam_raise_change:next", "adam_raise_change's next step does not lead to On hold and the "
                                                       "next workable ticket")
    if "BLOCKER_RULE" not in flat(server):
        guard.add("BR-RULE", "server.mjs:instructions", "the connector's instructions do not carry BLOCKER_RULE")

    needs = {}
    for side in ("backend", "frontend"):
        cmd = STARTERS / side / ".claude" / "commands"
        needs[cmd / "ticket.md"] = ["A blocker is always a change request", "On hold", 'only: "workable"']
        needs[cmd / "board.md"] = ["firstWorkable", "never a workaround"]
        needs[cmd / "cr.md"] = ["blocking: true", "never a workaround", 'only: "workable"']
        needs[cmd / "done.md"] = ["On hold"]
        needs[STARTERS / side / "CLAUDE.md"] = ["A blocker is always a change request", "never build a guess",
                                                'only: "workable"']
    needs[g.ROOT / "CLAUDE.md"] = ["A blocker is always a CR", "never builds a guess", 'only: "workable"']
    needs[g.ROOT / "docs" / "active" / "developer-brief.md"] = ["A blocker is always a CR", "On hold",
                                                               "never build a guess"]
    for path, phrases in needs.items():
        text = flat(path).lower()
        for phrase in phrases:
            if phrase.lower() not in text:
                guard.add("BR-RULE", f"{rel(path)}:{phrase}", f"{rel(path)} does not say \"{phrase}\"")

    for path in [tools, server] + list(needs):
        text = flat(path)
        for m in AROUND.finditer(text):
            if NEGATION.search(text[max(0, m.start() - 60):m.start()]):
                continue
            guard.add("BR-WORKAROUND", f"{rel(path)}:{m.group(0).lower()}",
                      f"{rel(path)}: \"{text[max(0, m.start() - 60):m.end() + 40].strip()}\"")

    blockers = VIEWER / "api" / "blockers.py"
    if "def affecting(" not in (blockers.read_text(encoding="utf-8") if blockers.is_file() else ""):
        guard.add("BR-SERVER", "blockers.py", "viewer/api/blockers.py has no `affecting`")
    main_py = (VIEWER / "api" / "main.py").read_text(encoding="utf-8", errors="replace")
    board = re.search(r"def my_board\(.*?(?=\n@app\.)", main_py, re.S)
    wp = re.search(r"def read_work_package\(.*?(?=\n# ── |\n@app\.)", main_py, re.S)
    if not board or '"blockedBy"' not in board.group(0) or "only: str" not in board.group(0):
        guard.add("BR-SERVER", "my_board", "/api/board/mine has no `blockedBy` per item or no `only` filter")
    if not wp or '"blockedBy"' not in wp.group(0):
        guard.add("BR-SERVER", "read_work_package", "/api/work-packages/{key} has no `blockedBy`")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
