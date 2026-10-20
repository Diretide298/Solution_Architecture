"""A task the lead holds takes no capacity in the schedule (tools/derive-block-a-schedule.py, CHG-R8DEC-004).

    python -m pytest ticvai/tools/tests/test_block_a_schedule_hold.py -q
"""
import importlib.util
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
_spec = importlib.util.spec_from_file_location("derive_block_a_schedule", TOOLS / "derive-block-a-schedule.py")
dbs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dbs)
sp = dbs.sp


def item(key, who, points=8, deps=()):
    return {"key": key, "who": who, "pool": "web", "track": "Frontend", "service": "", "points": points,
            "days": None, "notBefore": 0.0, "deps": list(deps), "client": False, "block": "A"}


PEOPLE = [{"name": "Sanket Keluskar", "pace": 1.0, "pools": ["web"], "fromIndex": 0}]


def test_held_keys_reads_every_hold(tmp_path):
    f = tmp_path / "held.yaml"
    f.write_text("holds:\n  a: {keys: [K-1, K-2]}\n  b: {keys: [K-3]}\n", encoding="utf-8")
    assert dbs.held_keys(f) == {"K-1", "K-2", "K-3"}
    assert dbs.held_keys(tmp_path / "none.yaml") == set()


def test_a_held_task_gets_no_week_and_its_owner_starts_the_next_task_at_once():
    items = [item("BO-HELD", "Sanket Keluskar"), item("PRD-W1-X", "Sanket Keluskar"),
             item("TEST-X", "Sanket Keluskar", deps=["BO-HELD", "PRD-W1-X"])]
    before = sp.schedule(items, PEOPLE)
    assert before["PRD-W1-X"]["start"] > 0                       # waits behind the back-office screen
    res = sp.schedule(dbs.without_held(items, {"BO-HELD"}), PEOPLE)
    assert "BO-HELD" not in res                                  # no start, no sprint, no owner
    assert res["PRD-W1-X"]["start"] == 0.0                        # the owner's capacity is free for it
    assert res["TEST-X"]["start"] >= res["PRD-W1-X"]["end"]       # a wait on a held task does not hold it back


def test_the_real_held_tasks_are_left_out():
    held = dbs.held_keys()
    items = [item(k, "Sanket Keluskar") for k in sorted(held)[:3]] + [item("OTHER", "Sanket Keluskar")]
    assert [it["key"] for it in dbs.without_held(items, held)] == ["OTHER"] or not held
