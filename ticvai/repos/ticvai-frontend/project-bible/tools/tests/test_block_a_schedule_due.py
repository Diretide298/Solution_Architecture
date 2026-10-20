"""A hand-written task due on a date lands in that date's sprint and moves no other task (block-a-extra-tasks.json `due`,
tools/sprint_plan.py due_of and schedule, CHG-R8INT-032).

    python -m pytest ticvai/tools/tests/test_block_a_schedule_due.py -q
"""
import json
import sys
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
import sprint_plan as sp  # noqa: E402


def item(key, who, points=8, deps=(), days=None, due=None):
    return {"key": key, "who": who, "pool": "be", "track": "Backend", "service": "", "points": points,
            "days": days, "notBefore": 0.0, "deps": list(deps), "client": False, "block": "A", "due": due}


PEOPLE = [{"name": "Pranay Shinde", "pace": 1.0, "pools": ["be"], "fromIndex": 0}]


def test_due_of_gives_the_working_day_of_the_date():
    due = sp.due_of([{"key": "R8-X", "assignee": "Pranay Shinde", "due": "2026-10-21"}, {"key": "OTHER"}])
    assert due == {"R8-X": 12.0}                                  # Wednesday of Sprint 2 (5 October is day 0)
    assert sp.sprint_of_index(due["R8-X"]) == 2
    assert sp.due_of([{"key": "R8-Y", "assignee": "Pranay Shinde", "due": "2026-10-24"}]) == {"R8-Y": 15.0}  # Saturday


@pytest.mark.parametrize("bad", [{"key": "R8-X", "assignee": "A", "due": "21 October"},
                                 {"key": "R8-X", "assignee": "A", "due": "2026-09-01"},
                                 {"key": "R8-X", "due": "2026-10-21"}])
def test_due_of_refuses_a_bad_date_or_no_owner(bad):
    with pytest.raises(SystemExit):
        sp.due_of([bad])


def test_a_due_task_sits_at_its_date_whatever_its_order_and_moves_nothing():
    # a ten-day task crossing day 12 and the work after it: the chore due on day 12 comes last in build order
    plan = [item("LONG", "Pranay Shinde", days=10.0, deps=()), item("NEXT", "Pranay Shinde", points=20)]
    before = sp.schedule([dict(x) for x in plan], PEOPLE)
    after = sp.schedule([dict(x) for x in plan] + [item("R8-DB-LOCAL-X", "Pranay Shinde", points=1, due=12.0)], PEOPLE)
    assert after["R8-DB-LOCAL-X"]["start"] == 12.0 and after["R8-DB-LOCAL-X"]["who"] == "Pranay Shinde"
    assert sp.sprint_of_index(after["R8-DB-LOCAL-X"]["start"]) == 2
    for k in before:                                              # holds no slot: nothing else moves
        assert after[k] == before[k]


def test_a_due_task_does_not_re_pace_the_plan():
    team = {"sprintPlan": {"pace": {"tasksPerDevDay": 5}}}
    plan = [item("A", "P", points=8), item("B", "P", points=4)]
    _, line, base = sp.pace_model(team, plan)
    _, line2, base2 = sp.pace_model(team, plan + [item("R8", "P", points=1, due=12.0)])
    assert base == base2


def test_the_r8_database_tasks_are_due_in_sprint_2():
    extra = json.loads((TOOLS.parent / "docs" / "active" / "block-a-extra-tasks.json").read_text(encoding="utf-8"))
    due = sp.due_of(extra["tasks"])
    r8 = {k for k in due if k.startswith("R8-DB-")}
    assert "R8-DB-SHARED" in r8 and len(r8) == 11
    assert {sp.sprint_of_index(due[k]) for k in r8} == {2}
