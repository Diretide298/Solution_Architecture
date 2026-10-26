"""Tests for tools/check-state-refusals.py (CHG-R10GEN-005): a 409's states against the state model.

    python -m pytest ticvai/tools/tests/test_check_state_refusals.py -q
"""
import importlib.util
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("sr", TOOLS / "check-state-refusals.py")
sr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sr)

QUEUE = {
    "entity": "Queue entry",
    "initial": ["waiting"],
    "terminal": ["redeemed", "expired", "noShow", "cancelled", "released"],
    "transitions": [
        {"from": "waiting", "to": "called", "operation": "callNextParties", "trigger": "operation"},
        {"from": "called", "to": "redeemed", "operation": "redeemWaitingGuest", "trigger": "operation"},
        {"from": "called", "to": "expired", "trigger": "timer"},
        {"from": "called", "to": "noShow", "operation": "overrideWaitingGuest", "trigger": "operation"},
        {"from": "called", "to": "waiting", "operation": "overrideWaitingGuest", "trigger": "operation"},
        {"from": "waiting", "to": "cancelled", "operation": "leaveQueue", "trigger": "operation"},
        {"from": "waiting", "to": "released", "operation": "setQueueStatus", "trigger": "cascade"},
    ],
}
OVERRIDE_409 = ("The entry was already `redeemed` (`queue-entry-already-redeemed`), or was `cancelled` or `released` "
                "from the queue (`queue-entry-cancelled`); there is no failed redemption to override.")


def _judge(model, op, text, types=()):
    sr.ALL_STATES.clear()
    sr.ALL_STATES.update(sr.model_states(model))
    moves = sr.moves_from(model)[op]
    return sr.judge("queue-entry.yaml", model, op, {a for a, _ in moves}, {b for _, b in moves}, text, list(types))


def test_cr237_override_leaves_two_terminal_states_unanswered():
    out = _judge(QUEUE, "overrideWaitingGuest", OVERRIDE_409, ["queue-entry-already-redeemed", "queue-entry-cancelled"])
    assert [r for r, _k, _m in out] == ["SR-TERMINAL-UNANSWERED"]
    msg = out[0][2]
    assert "expired, noShow" in msg and "moves it from called only" in msg and "waiting" in msg


def test_a_409_that_answers_every_ended_state_passes():
    text = "The entry is already `redeemed`, `expired`, `noShow`, `cancelled` or `released`."
    assert _judge(QUEUE, "overrideWaitingGuest", text) == []
    assert _judge(QUEUE, "overrideWaitingGuest", "The entry already has an outcome, or was `cancelled`.") == []


def test_a_refusal_of_a_state_the_model_moves_from():
    out = _judge(QUEUE, "redeemWaitingGuest", "The entry is `called` but the window has closed.")
    # "is `called` but ..." is a condition on more than the state, not a refusal of it
    assert out == []
    out = _judge(QUEUE, "redeemWaitingGuest", "The entry is `called` or `redeemed`.")
    assert [r for r, _k, _m in out][0] == "SR-REFUSES-ALLOWED" and "refuses called" in out[0][2]


def test_allowed_states_named_after_not_must_match_the_moves():
    assert _judge(QUEUE, "overrideWaitingGuest", "The entry is not `called`.") == []
    out = _judge(QUEUE, "overrideWaitingGuest", "The entry is not `called` or `waiting`.")
    assert [r for r, _k, _m in out] == ["SR-ALLOWS-NO-MOVE"] and "allows waiting" in out[0][2]


def test_moves_not_made_by_the_call_are_left_out():
    m = {"initial": ["draft"], "terminal": ["superseded"], "transitions": [
        {"from": "draft", "to": "published", "operation": "publishThing", "trigger": "operation"},
        {"from": "published", "to": "superseded", "operation": "publishThing", "trigger": "operation"},
        {"from": "published", "to": "draft", "operation": "publishThing", "trigger": "cascade"}]}
    assert sr.moves_from(m) == {"publishThing": {("draft", "published")}}


def test_already_into_state_does_not_refuse_the_other_moves_from_it():
    m = {"entity": "Journey", "initial": ["draft"], "terminal": ["archived"], "transitions": [
        {"from": "draft", "to": "active", "operation": "activateJourney", "trigger": "operation"},
        {"from": "active", "to": "paused", "operation": "activateJourney", "trigger": "operation"}]}
    assert _judge(m, "activateJourney", "Activating one already `active` is refused.") == []


def test_a_409_about_another_entity_is_not_judged():
    sr.ALL_STATES.clear()
    sr.ALL_STATES.update(sr.model_states(QUEUE) | {"onSale"})
    moves = sr.moves_from(QUEUE)["overrideWaitingGuest"]
    assert sr.judge("queue-entry.yaml", QUEUE, "overrideWaitingGuest", {a for a, _ in moves},
                    {b for _, b in moves}, "The performance is `onSale`, or the entry is `redeemed`.", []) == []
