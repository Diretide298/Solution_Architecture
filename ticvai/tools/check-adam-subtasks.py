#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A pull shows the work under a ticket and the ticket above it; /ticket with no number starts work without asking.

**18 October 2026** (CHG-ADM-006). On live ADAM, pulling #27735 ([BE] OrderService: claimCart, createCart, extendCart,
getCart) listed none of its sub-tasks #30681-#30684, pulling #30681 did not name #27735, the board showed 0 sub-tasks
when the whole-project read failed, `/ticket` with no number made agents ask for one, and a frontend session opened in
an app's clone had no ADAM tools and did not say why. This holds:

    ST-PULL       the pull has no "Sub-tasks" section (every depth, every status, read for the ticket and not from the
                  held project read, said when it could not be read) or no "Part of" line
    ST-BOARD      the board does not say when its sub-tasks could not be read (`subtasksKnown`, shown as ?) or has no
                  `startHere`, or /board does not relay the note
    ST-NO-NUMBER  /ticket, CLAUDE.md "Working a ticket" or the connector's instructions do not start `startHere` when
                  no ticket is named, or /ticket still requires a number
    ST-WORKSPACE  the frontend starter does not tell an agent without ADAM's tools to say "open the workspace folder"

Read-only. Exit 1 on a finding not in `handoff/audit-baseline.json` (tools/audit_guard.py).

    python3 tools/check-adam-subtasks.py [--all]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {
    "ST-PULL": "a pull lists every sub-task with status and holder, read for the ticket, and names a sub-task's parent (CHG-ADM-006)",
    "ST-BOARD": "the board says when sub-tasks could not be read and where work starts (startHere) (CHG-ADM-006)",
    "ST-NO-NUMBER": "/ticket with no number starts startHere and never asks for a number (CHG-ADM-006)",
    "ST-WORKSPACE": "a frontend agent without ADAM's tools says: open the workspace folder (CHG-ADM-006)",
}
VIEWER = g.ROOT.parent / "viewer"
STARTERS = VIEWER / "mcp" / "setup" / "starters"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.is_file() else ""


def flat(path: Path) -> str:
    text = re.sub(r"'\s*\+\s*'|`\s*\+\s*'|'\s*\+\s*`", "", read(path))
    return re.sub(r"\s+", " ", text)


def block(src: str, start: str) -> str:
    """A top-level Python definition from `start` up to the next top-level one, route or section rule."""
    m = re.search(re.escape(start) + r".*?(?=\n(?:@app\.|def |class |# ── )|\Z)", src, re.S)
    return m.group(0) if m else ""


def rel(path: Path) -> str:
    try:
        return path.relative_to(g.ROOT.parent).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-adam-subtasks", RULES)
    main_py = read(VIEWER / "api" / "main.py")
    op_py = read(VIEWER / "api" / "openproject.py")
    tools = flat(VIEWER / "mcp" / "tools.mjs")

    wp = block(main_py, "def read_work_package(")
    for need in ('"subtasks"', '"partOf"', "openproject.descendants"):
        if need not in wp:
            guard.add("ST-PULL", f"read_work_package:{need}", f"/api/work-packages/{{key}} has no {need}")
    if "_project_tree" in wp or "_project_read" in wp:
        guard.add("ST-PULL", "read_work_package:held-read",
                  "/api/work-packages/{key} reads sub-tasks from the held project read, which a failed read empties")
    walk = block(op_py, "def descendants(") + block(op_py, "def _descendants_by_filter(")
    if "def descendants(" not in walk:
        guard.add("ST-PULL", "openproject.descendants", "viewer/api/openproject.py has no `descendants`")
    elif '{"status": {"operator": "*"' not in walk:
        guard.add("ST-PULL", "descendants:every-status", "descendants does not ask for every status: a closed "
                                                          "sub-task would be left out")
    for need in ("## Sub-tasks (", "Could not be read from OpenProject", "line('Part of'"):
        if need not in tools:
            guard.add("ST-PULL", f"tools.mjs:{need}", f"viewer/mcp/tools.mjs README has no {need}")

    board = block(main_py, "def my_board(")
    for need in ('"subtasksKnown"', '"startHere"'):
        if need not in board:
            guard.add("ST-BOARD", f"my_board:{need}", f"/api/board/mine has no {need}")
    m = re.search(r"name: 'adam_board',(.*?)name: 'adam_team'", tools)
    adam_board = m.group(1) if m else ""
    for need in ("subtaskNote", "startHere", "'?'"):
        if need not in adam_board:
            guard.add("ST-BOARD", f"adam_board:{need}", f"adam_board has no {need}")

    for side in ("backend", "frontend"):
        commands = STARTERS / side / ".claude" / "commands"
        ticket = commands / "ticket.md"
        hint = re.search(r"^argument-hint:\s*(.*)$", read(ticket), re.M)
        if not hint or hint.group(1).strip() == "<ticket number>":
            guard.add("ST-NO-NUMBER", f"{rel(ticket)}:argument-hint",
                      f"{rel(ticket)} still asks for a ticket number as its argument")
        for path, phrases in ((ticket, ("startHere", "do not ask me for a number")),
                              (STARTERS / side / "CLAUDE.md", ("startHere", "do not ask for a number")),
                              (commands / "board.md", ("subtaskNote", "startHere"))):
            text = flat(path).lower()
            for phrase in phrases:
                if phrase.lower() not in text:
                    rule = "ST-BOARD" if path.name == "board.md" else "ST-NO-NUMBER"
                    guard.add(rule, f"{rel(path)}:{phrase}", f"{rel(path)} does not say \"{phrase}\"")
    server = flat(VIEWER / "mcp" / "server.mjs").lower()
    for phrase in ("startHere", "never ask for a number"):
        if phrase.lower() not in server:
            guard.add("ST-NO-NUMBER", f"server.mjs:{phrase}", f"the connector's instructions do not say \"{phrase}\"")

    frontend = STARTERS / "frontend" / "CLAUDE.md"
    text = flat(frontend).lower()
    for phrase in ("open the workspace folder", "not among your tools"):
        if phrase not in text:
            guard.add("ST-WORKSPACE", f"{rel(frontend)}:{phrase}", f"{rel(frontend)} does not say \"{phrase}\"")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
