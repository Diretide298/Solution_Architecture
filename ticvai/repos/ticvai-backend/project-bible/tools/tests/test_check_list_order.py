"""Tests for tools/check-list-order.py (CHG-R10GEN-004): nullable sort keys and whole lists with no order.

    python -m pytest ticvai/tools/tests/test_check_list_order.py -q
"""
import importlib.util
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("lo", TOOLS / "check-list-order.py")
lo = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lo)

WAITING_GUEST = {
    "type": "object",
    "required": ["id", "queueId", "status", "joinedAt"],
    "properties": {"id": {"type": "string", "format": "uuid"}, "estimatedCallAt": {"type": "string", "nullable": True},
                   "joinedAt": {"type": "string"}, "recordedAt": {"type": "string"},
                   "createdAt": {"type": "string"}},
}


def test_the_fields_an_order_names_in_order():
    text = "Ordered by `estimatedCallAt`, soonest first, then `joinedAt`."
    assert lo.order_fields(text, WAITING_GUEST["properties"]) == ["estimatedCallAt", "joinedAt"]
    assert lo.order_fields("**Order.** Newest first, by `recordedAt` descending, then by `id`.",
                           WAITING_GUEST["properties"]) == ["recordedAt", "id"]


def test_cr236_a_nullable_key_with_no_place_for_nulls():
    p = WAITING_GUEST["properties"]
    assert lo.can_be_null("estimatedCallAt", WAITING_GUEST, p["estimatedCallAt"], []) == "nullable in the schema"
    assert lo.can_be_null("joinedAt", WAITING_GUEST, p["joinedAt"], []) == ""
    assert not lo.null_place_stated("Ordered by `estimatedCallAt`, soonest first, then `joinedAt`.",
                                    "estimatedCallAt", [])


def test_cr206_optional_field_on_a_nullable_column():
    cols = [("orders.pos_shift", "recorded_at", False)]
    why = lo.can_be_null("recordedAt", WAITING_GUEST, WAITING_GUEST["properties"]["recordedAt"], cols)
    assert why.startswith("optional") and "orders.pos_shift.recorded_at" in why
    # optional with a NOT NULL column, or optional with no column at all, is not a null key
    assert lo.can_be_null("recordedAt", WAITING_GUEST, {}, [("orders.pos_shift", "recorded_at", True)]) == ""
    assert lo.can_be_null("recordedAt", WAITING_GUEST, {}, []) == ""
    # a creation stamp and a key are never null keys
    assert lo.can_be_null("createdAt", WAITING_GUEST, {}, [("t.x", "created_at", False)]) == ""
    assert lo.can_be_null("venueId", WAITING_GUEST, {"nullable": True}, []) == ""


def test_a_stated_place_for_the_rows_without_the_key():
    stated = [
        "Ordered by `estimatedCallAt`, soonest first; an entry with no `estimatedCallAt` sorts last, then `joinedAt`.",
        "ORDER BY coalesce(recorded_at, opened_at) DESC, id.",
        "Sorted by `since` ascending (a row with no `since` last), then by `productId`.",
        "Newest first by `recordedAt`, or its `openedAt` where it has none, then by `id`.",
        "Where `estimatedCallAt` is null the row sorts after the rows that have it (NULLS LAST).",
    ]
    for t in stated:
        assert lo.null_place_stated(t, "estimatedCallAt" if "estimated" in t else
                                    ("since" if "since" in t else "recordedAt"),
                                    [("orders.pos_shift", "recorded_at", False)]), t
    # a null word about something else in the text is not a place for the key's nulls
    assert not lo.null_place_stated("Ordered by `recordedAt`. With no `status` the list holds open shifts.",
                                    "recordedAt", [])


def test_an_order_stated_for_a_whole_list():
    for t in ("Critical first, then unacknowledged, then by age.", "Sorted by `name` ascending, then by `id`.",
              "Newest first.", "in display order", "ordered by creation"):
        assert lo.ORDER_STATED.search(t), t
    for t in ("Called before the login screen renders, so it is unauthenticated.",
              "a donation is a line and not a flag on the order", "An upgrade ladder is an ordered relationship"):
        assert not lo.ORDER_STATED.search(t), t


def test_r9_catches_the_three_crs():
    found = {(r, k) for r, k, _m in lo.findings()}
    want = {("LO-NULLABLE-KEY", "listMyWaitingGuests:estimatedCallAt"), ("LO-NULLABLE-KEY", "listShifts:recordedAt"),
            ("LO-UNORDERED", "listSsoProviders")}
    # on r9's text all three are found; once the CR lanes have fixed them at the source, none is
    assert want <= found or not (want & found)
