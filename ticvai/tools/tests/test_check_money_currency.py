"""Tests for tools/check-money-currency.py and tools/fix-money-currency.py (CHG-R10GEN-002; ADAM CR-197,
CR-202, CR-217, CR-234, CR-235).

    python -m pytest ticvai/tools/tests/test_check_money_currency.py -q

The synthetic tests give the detector a few schemas and columns; the last one reads the real package and checks that
the five operations the CRs named answer or accept Money with no currency of their own (true before and after the
fixer, which adds the read and leaves the rows as they are).
"""
import importlib.util
from pathlib import Path

import yaml

TOOLS = Path(__file__).resolve().parents[1]


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


mc = _load("mc", TOOLS / "check-money-currency.py")
fx = _load("fx", TOOLS / "fix-money-currency.py")

MONEY = {"$ref": "../shared/common.yaml#/components/schemas/Money"}
BY = {
    ("common", "Money"): {"type": "object"},
    ("fnb", "TableVisit"): {"x-ticvai-persistence": "fnb.table_visit", "properties": {
        "runningTotal": MONEY, "orders": {"type": "array", "items": {"$ref": "#/components/schemas/FnbOrder"}}}},
    ("fnb", "FnbOrder"): {"x-ticvai-persistence": "fnb.service_order", "properties": {"grossAmount": MONEY}},
    ("fnb", "Summary"): {"properties": {"total": MONEY}},
    ("fnb", "Wrapper"): {"properties": {"visit": {"$ref": "#/components/schemas/TableVisit"}}},
}
COLS = {
    "fnb.table_visit": [{"column": "id"}, {"column": "outlet_id", "references": "platform.outlet"},
                        {"column": "running_total"}],
    "fnb.service_order": [{"column": "visit_id", "references": "fnb.table_visit", "required": "yes"}],
    "ledger.account": [{"column": "currency"}],
    "ledger.posting": [{"column": "account_id", "references": "ledger.account", "required": "no"}],
    "ledger.line": [{"column": "posting_id", "references": "ledger.posting", "required": "no"}],
    "ledger.req_line": [{"column": "posting_id", "references": "ledger.posting", "required": "yes"}],
    "ledger.root": [{"column": "line_id", "references": "ledger.req_line", "required": "yes"}],
    "orders.payment": [{"column": "tender_currency"}],
    "orders.sale": [{"column": "payment_id", "references": "orders.payment"}],
    "fnb.priced": [{"column": "payment_id", "references": "orders.payment"}],
    "payments.provider": [{"column": "supported_currencies"}],
    "catalogue.template": [{"column": "scope_path"}, {"column": "included_value"}],
    "fnb.rule": [{"column": "region_id"}],
    "fnb.lonely": [{"column": "id"}],
}


def module_of(t):
    return t.split(".", 1)[0].replace("payments", "orders")


def test_money_is_found_through_refs_with_the_row_that_stores_it():
    hits = mc.money_hits("fnb", {"$ref": "#/components/schemas/Wrapper"}, BY, set(COLS))
    assert ("fnb", "TableVisit", "fnb.table_visit", "TableVisit.runningTotal") in hits
    assert ("fnb", "FnbOrder", "fnb.service_order", "FnbOrder.grossAmount") in hits


def test_a_computed_answer_has_no_row():
    hits = mc.money_hits("fnb", {"$ref": "#/components/schemas/Summary"}, BY, set(COLS))
    assert hits == [("fnb", "Summary", None, "Summary.total")]


def test_a_currency_column_of_its_own_or_of_a_parent_of_its_module_denominates():
    assert mc.currency_source("orders.payment", COLS, module_of) == "orders.payment"
    assert mc.currency_source("orders.sale", COLS, module_of) == "orders.payment"
    assert mc.currency_source("ledger.posting", COLS, module_of) == "ledger.account"
    # the second hop only by a required key
    assert mc.currency_source("ledger.line", COLS, module_of) is None
    assert mc.currency_source("ledger.root", COLS, module_of) is None  # three hops up
    # another module's currency is not this row's
    assert mc.currency_source("fnb.priced", COLS, module_of) is None
    # a list of currencies a provider may charge is not a denomination
    assert mc.currency_source("payments.provider", COLS, module_of) is None
    assert mc.currency_source("fnb.table_visit", COLS, module_of) is None


def test_judge_names_the_rows_that_store_the_amount_only():
    hits = [("fnb", "TableVisit", "fnb.table_visit", "TableVisit.runningTotal"),
            ("orders", "Sale", "orders.sale", "Sale.total"), ("fnb", "Summary", None, "Summary.total")]
    assert mc.judge(hits, COLS, module_of, False) == (["fnb.table_visit"], ["fnb.Summary"])
    # a computed answer beside a read of a row that keeps a currency passes (precision first)
    assert mc.judge(hits, COLS, module_of, True) == (["fnb.table_visit"], [])


def test_the_settings_read_by_query_or_view_counts():
    qt = {"tenancy#venueSettingsRecords": {"platform.venue_settings"}, "x#other": {"x.y"}}
    assert mc.asks_settings([{"query": "tenancy#venueSettingsRecords"}], qt, [])
    assert not mc.asks_settings([{"query": "x#other"}], qt, ["fnb.table_visit"])
    assert mc.asks_settings([], qt, ["platform.region_settings_for_fnb"])


def test_the_fixer_classifies_by_what_the_row_holds():
    f = {"contract": "fnb", "op": {}, "item": {}}
    assert fx.classify(f, ["fnb.service_order"], [], ["fnb.service_order"], COLS, BY, set()) == "venue"  # parent
    assert fx.classify(f, ["fnb.rule"], [], ["fnb.rule"], COLS, BY, set()) == "region"
    assert fx.classify(f, ["catalogue.template"], [], ["catalogue.template"], COLS, BY, set()) == "scope"
    assert fx.classify(f, ["control.invoice"], [], ["control.invoice"], COLS, BY, set()) == "platform"
    assert fx.classify(f, ["fnb.lonely"], [], ["fnb.lonely"], COLS, BY, set()) == "no venue"
    assert fx.classify(f, [], ["fnb.Summary"], [], COLS, BY, set()) == "no row"
    named = {"contract": "fnb", "op": {"parameters": [{"name": "venueId", "in": "query"}]}, "item": {}}
    assert fx.classify(named, ["fnb.lonely"], [], ["fnb.lonely"], COLS, BY, set()) == "venue"


def test_a_scope_path_row_is_routed_only_once_tenancy_declares_scope_records():
    assert fx.queries_for("scope", set()) == []
    assert fx.queries_for("scope", {fx.SCOPE_Q}) == [fx.SCOPE_Q, fx.VENUE_Q]
    assert fx.queries_for("venue", set()) == [fx.VENUE_Q]
    assert fx.queries_for("platform", {fx.SCOPE_Q}) == []


CONTRACT = """paths:
  /a:
    post:
      operationId: makeA
      x-ticvai-read-via:
        - query: other#xRecords
          route: service
          for: "already there"
      summary: Make an A
  /b:
    get:
      operationId: getB
      x-ticvai-consumed-by:
        - "P08 BO-001 Something"
      summary: Get a B
"""


def test_a_route_is_written_at_the_lists_own_indent_once():
    w = fx.why("venue", fx.VENUE_Q, "answers", ["A.total"])
    out, n = fx.add_read_via(CONTRACT, "makeA", [(fx.VENUE_Q, "in-process", w)])
    assert n == 1
    via = yaml.safe_load(out)["paths"]["/a"]["post"]["x-ticvai-read-via"]
    assert [v["query"] for v in via] == ["other#xRecords", fx.VENUE_Q]
    assert fx.add_read_via(out, "makeA", [(fx.VENUE_Q, "in-process", w)]) == (out, 0)
    out2, n2 = fx.add_read_via(CONTRACT, "getB", [(fx.VENUE_Q, "service", w)])
    op = yaml.safe_load(out2)["paths"]["/b"]["get"]
    assert n2 == 1 and op["x-ticvai-read-via"][0]["route"] == "service"
    assert op["x-ticvai-consumed-by"] == ["P08 BO-001 Something"]


def test_only_a_route_this_script_wrote_is_removed():
    w = fx.why("venue", fx.VENUE_Q, "answers", ["A.total"])
    assert fx.is_own({"for": w}) and not fx.is_own({"for": "already there"})
    out, _ = fx.add_read_via(CONTRACT, "makeA", [(fx.VENUE_Q, "in-process", w)])
    back, n = fx.remove_own(out, "makeA", fx.VENUE_Q)
    assert n == 1 and yaml.safe_load(back) == yaml.safe_load(CONTRACT)
    assert fx.remove_own(CONTRACT, "makeA", "other#xRecords") == (CONTRACT, 0)


def test_the_five_operations_the_crs_named_answer_money_with_no_currency_of_their_own():
    ctx = mc.load()
    tables = set(ctx["cols_of"])

    def mod(t):
        return ctx["owner_of_schema"].get(t.split(".", 1)[0])

    want = {"mergeTableVisits": "fnb.table_visit", "createEntitlementTemplate": "catalogue.entitlement_template",
            "setEntitlementTemplateBlackoutDates": "catalogue.entitlement_template",
            "generateInvoice": "control.invoice", "getGuestBundle": "promotions.GuestBundle"}
    for op, where in want.items():
        f = ctx["ops"][op]
        bare, computed = mc.judge(mc.op_money(f["contract"], f["op"], ctx["by"], tables), ctx["cols_of"], mod, False)
        assert where in bare + computed, (op, bare, computed)
