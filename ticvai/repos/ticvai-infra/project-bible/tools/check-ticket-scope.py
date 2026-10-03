#!/usr/bin/env python3
"""A setup ticket's title says how many operations its screen has, and that count is the screen's.

**3 October 2026, CHG-TBF-005** (Block A audit on live r2, pattern 7: "ticket scope out of step with its screen
after the 2 October moves"; `changes/entries/CHG-AUD-001-block-a-audit-patterns-for-r3.yaml`). A Block A setup
screen is built only as far as the first release needs (its setup operations); the rest of the screen is a
later ticket. The title said "BO-009 Pricing Rules (setup: 5 operations)" on an 11-operation screen, so a
reader took it for the whole screen, and 94 Block A titles disagreed with their screens. The title now reads
"(setup: 5 of its 11 operations)" and the later one "(the rest of the screen: 6 of its 11 operations)"
(`tools/build-service-docs.py` setup_scope / rest_scope).

**What fails** (from handoff/service-docs/plan-tasks.csv against screens/P*.yaml):

  S-SCREEN-COUNT    the title's "of its N" (or "all N") is not the number of distinct operations the screen binds
  S-SETUP-COUNT     a setup title's K is not the number of its listed setup operations the screen binds, or a
                    title still in the old form "(setup: N operations)", which does not say the screen's size
  S-SETUP-OP-GONE   a setup ticket lists an operation the screen no longer binds (moved on 2 October)
  S-REST-COUNT      a rest-of-the-screen title's K is not N minus the setup operations on the screen

Read-only. Exit 1 on a finding not in `handoff/audit-baseline.json` (tools/audit_guard.py).

    python3 tools/check-ticket-scope.py [--all]
"""
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {
    "S-SCREEN-COUNT": "a ticket title's screen operation count is not the screen's (CHG-TBF-005)",
    "S-SETUP-COUNT": "a setup title's operation count is not its setup operations on the screen (CHG-TBF-005)",
    "S-SETUP-OP-GONE": "a setup ticket lists an operation its screen no longer binds (CHG-TBF-005)",
    "S-REST-COUNT": "a rest-of-the-screen title's count is not the screen's other operations (CHG-TBF-005)",
}
SETUP = re.compile(r"\(setup: (?:(\d+) of its (\d+)|all (\d+)) operations\)")
OLD = re.compile(r"\(setup: \d+ operations?\)")
REST = re.compile(r"\(the rest of the screen: (\d+) of its (\d+) operations\)")


def op_ids(s: dict) -> set:
    """The same count build-service-docs.py puts in the title (screen_op_ids)."""
    return {a["operationId"] for a in s.get("apis") or [] if isinstance(a, dict) and a.get("operationId")}


def listed(text: str, head: str) -> set:
    m = re.search(re.escape(head) + r"\s*([A-Za-z0-9, ]+?)(?:\)|\.|;|$)", text or "")
    return {x.strip() for x in m.group(1).split(",") if x.strip()} if m else set()


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-ticket-scope", RULES)
    plan = g.ROOT / "handoff" / "service-docs" / "plan-tasks.csv"
    if not plan.exists():
        guard.note("handoff/service-docs/plan-tasks.csv missing - run tools/build-service-docs.py")
        return guard.finish()
    screens = {s["id"]: s for _, s in g.screens()}
    with plan.open(encoding="utf-8", newline="") as fh:
        rows = [r for r in csv.DictReader(fh) if r["type"] == "Task" and r["track"] == "Frontend"
                and "#" not in r["key"]]
    n_checked = 0
    for r in rows:
        subj = r["subject"]
        m_sid = re.match(r"^\[FE\] ([A-Z]+-\d+[A-Z]?) ", subj)
        if not m_sid or not (SETUP.search(subj) or OLD.search(subj) or REST.search(subj)):
            continue
        sid, key = m_sid.group(1), r["key"]
        s = screens.get(sid)
        if not s:
            continue
        n_checked += 1
        ops = op_ids(s)
        if OLD.search(subj):
            guard.add("S-SETUP-COUNT", key, f"{key}: '{subj[:90]}' does not say how many operations {sid} has "
                                            f"({len(ops)})")
            continue
        m = SETUP.search(subj)
        if m:
            k, n = (int(m.group(1)), int(m.group(2))) if m.group(1) else (int(m.group(3)), int(m.group(3)))
            setup = listed(r["description"], "In the slice:")
            if n != len(ops):
                guard.add("S-SCREEN-COUNT", key, f"{key}: title says {sid} has {n} operations, the screen binds "
                                                 f"{len(ops)}")
            if k != len(setup & ops):
                guard.add("S-SETUP-COUNT", key, f"{key}: title says {k} setup operations, {len(setup & ops)} of "
                                                f"its listed ones are on {sid}")
            gone = setup - ops
            if gone:
                guard.add("S-SETUP-OP-GONE", key, f"{key}: lists {', '.join(sorted(gone))}, which {sid} no longer "
                                                  "binds")
            continue
        m = REST.search(subj)
        k, n = int(m.group(1)), int(m.group(2))
        setup = listed(r["description"], "Block A built only its setup operations (")
        if n != len(ops):
            guard.add("S-SCREEN-COUNT", key, f"{key}: title says {sid} has {n} operations, the screen binds "
                                             f"{len(ops)}")
        if k != len(ops) - len(setup & ops):
            guard.add("S-REST-COUNT", key, f"{key}: title says {k} more operations, {sid} has "
                                           f"{len(ops) - len(setup & ops)} beyond its setup ones")
    guard.note(f"{n_checked} setup and rest-of-the-screen ticket(s) checked against their screens")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
