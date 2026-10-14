#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A settled change request reaches its ticket: a comment for the agent when it is open, a child task when closed.

**14 October 2026** (CHG-ADM-002). Chinmay: "whenever we have a cr we should create new tickets if ticket is closed.
if not then add comment for the AI agent when he pulls", and "we create child tasks for CR remember that". ADAM's
`viewer/api/settle_changes.py` (the workstation script) and its resolve route (`viewer/api/main.py`) share the
decision and the words in `viewer/api/cr_notice.py`. This runs the script's settle loop against stand-ins for ADAM
and OpenProject (no network) and reads the route's order:

    CS-OPEN-COMMENT   a request settled from an open ticket does not leave exactly one comment for the agent on it
                      (heading "ADAM CR-nnn · <status> — read before building", what was decided, what to do)
    CS-CLOSED-CHILD   a request accepted or done from a closed ticket does not file exactly one child task of it
                      through ADAM's ticket machinery, before the request is marked done
    CS-REJECTED       a rejection on a closed ticket files a ticket (there is nothing to build)
    CS-DRY-RUN        a run without --apply changes something
    CS-ONCE           a second run comments or files again
    CS-ROUTE          the resolve route does not tell the ticket before it writes the status, or the CSV bulk settle
                      does not tell it at all

Read-only. Exit 1 on a finding not in `handoff/audit-baseline.json` (tools/audit_guard.py).

    python3 tools/check-adam-cr-settlement.py [--all]
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {
    "CS-OPEN-COMMENT": "an open ticket gets one comment for the agent when its CR is settled (CHG-ADM-002)",
    "CS-CLOSED-CHILD": "a closed ticket gets one child task for an accepted or done CR, filed before Done (CHG-ADM-002)",
    "CS-REJECTED": "a rejection on a closed ticket files nothing (CHG-ADM-002)",
    "CS-DRY-RUN": "settle_changes.py changes nothing without --apply (CHG-ADM-002)",
    "CS-ONCE": "a second run neither comments nor files again (CHG-ADM-002)",
    "CS-ROUTE": "the resolve route and the bulk settle tell the ticket, before the status is written (CHG-ADM-002)",
}
API = g.ROOT.parent / "viewer" / "api"


class FakeAdam:
    """ADAM's change requests, with the guard the real preview has: no ticket for a done request."""

    def __init__(self, rows):
        self.rows = {r["id"]: dict(r) for r in rows}
        self.resolves, self.tickets, self.next = [], [], 9000

    def changes(self, project):
        return {k: dict(v) for k, v in self.rows.items()}

    def _by_number(self, number):
        return next(r for r in self.rows.values() if r["number"] == number)

    def resolve(self, project, number, status, resolution, ref):
        row = self._by_number(number)
        self.resolves.append((row["id"], status))
        row.update(status=status, resolution=resolution, resolvedRef=ref)

    def new_ticket(self, project, number):
        row = self._by_number(number)
        if row["status"] == "done":
            raise RuntimeError(f"ADAM 409: {row['id']} is already done")
        if row.get("childTicket"):
            raise RuntimeError(f"ADAM 409: {row['id']} already has a ticket")
        self.next += 1
        row["childTicket"] = str(self.next)
        self.tickets.append((row["id"], row.get("ticket"), str(self.next), row["status"], row.get("resolution")))
        return {"key": str(self.next)}

    def raise_change(self, project, fields):
        raise AssertionError("not used")


class FakeOp:
    def __init__(self, closed):
        self.closed = set(closed)
        self.threads: dict = {}

    def is_closed(self, wp):
        return str(wp) in self.closed

    def comments(self, wp):
        return list(self.threads.get(str(wp), []))

    def comment(self, wp, text, notify):
        self.threads.setdefault(str(wp), []).append(text)

    def attachment_names(self, wp):
        return set()


def load_script():
    spec = importlib.util.spec_from_file_location("settle_changes_under_check", API / "settle_changes.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def rows():
    base = {"title": "Loan period", "resolution": "", "resolvedRef": "", "artefacts": ["screen:WEB-001"],
            "childTicket": "", "status": "open"}
    return [dict(base, id="CR-001", number=1, ticket="7001"),       # open ticket
            dict(base, id="CR-002", number=2, ticket="7005"),       # closed ticket, accepted
            dict(base, id="CR-003", number=3, ticket="7006"),       # closed ticket, done
            dict(base, id="CR-004", number=4, ticket="7007")]       # closed ticket, rejected


DECISIONS = {"project": "ticvai", "ref": "r6", "items": [
    {"cr": "CR-001", "status": "accepted", "resolution": "Notices say 21 days."},
    {"cr": "CR-002", "status": "accepted", "resolution": "Show 21 days on the receipt."},
    {"cr": "CR-003", "status": "done", "resolution": "Recompute the due date."},
    {"cr": "CR-004", "status": "rejected", "resolution": "Right as shipped."},
]}


def run(mod, adam, op, apply):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = mod.settle(adam, op, DECISIONS, "ticvai", "r6", apply, False, g.ROOT.parent)
    return code, out.getvalue()


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-adam-cr-settlement", RULES)
    try:
        mod = load_script()
        if not hasattr(mod, "settle") or not hasattr(mod, "tell_ticket"):
            raise AttributeError("settle_changes.py has no settle() / tell_ticket() to run")
    except Exception as exc:  # noqa: BLE001 — every rule fails when the script cannot be run
        for rule in ("CS-OPEN-COMMENT", "CS-CLOSED-CHILD", "CS-REJECTED", "CS-DRY-RUN", "CS-ONCE"):
            guard.add(rule, "settle_changes.py", f"viewer/api/settle_changes.py could not be run: {exc}")
        mod = None

    if mod:
        closed = {"7005", "7006", "7007"}
        adam, op = FakeAdam(rows()), FakeOp(closed)
        code, text = run(mod, adam, op, apply=False)
        if adam.resolves or adam.tickets or op.threads:
            guard.add("CS-DRY-RUN", "dry-run", f"a dry run wrote: resolves {adam.resolves}, tickets {adam.tickets}, "
                                               f"comments on {sorted(op.threads)}")

        code, text = run(mod, adam, op, apply=True)
        if code != 0:
            guard.add("CS-OPEN-COMMENT", "exit", f"the applied run failed (exit {code}):\n{text}")
        open_thread = op.threads.get("7001", [])
        mine = [t for t in open_thread if t.startswith("**ADAM CR-001 · accepted — read before building**")]
        if len(mine) != 1 or "For the AI agent" not in (mine[0] if mine else "") \
                or "**What was decided:** Notices say 21 days." not in (mine[0] if mine else "") \
                or "**What to do now:**" not in (mine[0] if mine else ""):
            guard.add("CS-OPEN-COMMENT", "7001", f"the open ticket's thread is {open_thread!r}")
        if any(t[0] == "CR-001" for t in adam.tickets):
            guard.add("CS-OPEN-COMMENT", "7001-ticket", "an open ticket's CR filed a ticket instead of commenting")

        for cr, parent, status in (("CR-002", "7005", "accepted"), ("CR-003", "7006", "done")):
            filed = [t for t in adam.tickets if t[0] == cr]
            if len(filed) != 1 or filed[0][1] != parent:
                guard.add("CS-CLOSED-CHILD", cr, f"{cr} from closed #{parent} filed {filed!r} (want one child task)")
                continue
            if filed[0][3] == "done" or not filed[0][4]:
                guard.add("CS-CLOSED-CHILD", f"{cr}-order", f"{cr}'s child was filed with the request {filed[0][3]!r} "
                                                           f"and resolution {filed[0][4]!r}")
            if adam.rows[cr]["status"] != status:
                guard.add("CS-CLOSED-CHILD", f"{cr}-status", f"{cr} ended {adam.rows[cr]['status']!r}, not {status!r}")
            if not any(t.startswith(f"**ADAM {cr} · {status}") for t in op.threads.get(filed[0][2], [])):
                guard.add("CS-CLOSED-CHILD", f"{cr}-comment", f"{cr}'s child task #{filed[0][2]} has no comment for the agent")

        if any(t[0] == "CR-004" for t in adam.tickets):
            guard.add("CS-REJECTED", "CR-004", "a rejection on a closed ticket filed a ticket")
        if not any(t.startswith("**ADAM CR-004 · rejected") for t in op.threads.get("7007", [])):
            guard.add("CS-REJECTED", "CR-004-comment", "a rejection on a closed ticket left no comment")

        counts = (len(adam.tickets), sum(len(v) for v in op.threads.values()))
        run(mod, adam, op, apply=True)
        again = (len(adam.tickets), sum(len(v) for v in op.threads.values()))
        if again != counts:
            guard.add("CS-ONCE", "rerun", f"a second run went from (tickets, comments) {counts} to {again}")

    main_py = API / "main.py"
    src = main_py.read_text(encoding="utf-8", errors="replace") if main_py.is_file() else ""
    route = re.search(r"def resolve_change\(.*?(?=\n@app\.|\n# ── )", src, re.S)
    body = route.group(0) if route else ""
    tell = body.find("_tell_ticket(")
    write = body.find("UPDATE change_request SET status = ?")
    if tell < 0 or write < 0 or tell > write:
        guard.add("CS-ROUTE", "resolve_change", "the resolve route does not call _tell_ticket before it writes the status")
    bulk = re.search(r"def apply_changes\(.*?(?=\n@app\.|\Z)", src, re.S)
    if not bulk or "_tell_ticket(" not in bulk.group(0):
        guard.add("CS-ROUTE", "apply_changes", "the CSV bulk settle does not tell the tickets")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
