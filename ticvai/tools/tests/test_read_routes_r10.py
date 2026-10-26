"""Tests for tools/fix-read-routes.py and the read rule it shares with check-cross-module-reads (CHG-R10GEN-001).

    python -m pytest ticvai/tools/tests/test_read_routes_r10.py -q
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


rr = _load("rr10", TOOLS / "fix-read-routes.py")
xr = _load("xr10", TOOLS / "check-cross-module-reads.py")

CONTRACT = """openapi: 3.0.3
x-ticvai-queries:
  thingRecords:
    module: things
    table: things.thing
    rule: >-
      A data read, not a rule question (MOD audit of 14 October 2026, CHG-MOD-001; ADR-0055 rule 2 as amended 14
      October). Things answers with its things.thing rows. It is asked from another deployable through Things'
      service route (serviceAuth).
    served: [service]
paths:
  /a:
    post:
      operationId: makeA
      x-ticvai-read-via:
        - query: things#thingRecords
          route: service
          for: 'deeper than its key, as addCartLine''s list is'
      summary: Make an A
  /b:
    get:
      operationId: getB
      summary: Get a B
"""
SERVICES = {"ThingService": {"deployable": "operations", "tier": "domain"},
            "OtherService": {"deployable": "commerce", "tier": "domain"},
            "IdentityService": {"deployable": "commerce", "tier": "foundation"}}
SVC_OF = {"things": "ThingService", "other": "OtherService", "identity": "IdentityService"}


def test_a_list_indented_deeper_than_its_key_gets_items_at_its_own_indent():
    out, n = rr.add_read_via(CONTRACT, "makeA", [("other#xRecords", "service", "new")])
    assert n == 1
    via = yaml.safe_load(out)["paths"]["/a"]["post"]["x-ticvai-read-via"]
    assert [v["query"] for v in via] == ["things#thingRecords", "other#xRecords"]
    assert rr.add_read_via(out, "makeA", [("other#xRecords", "service", "new")]) == (out, 0)


def test_only_its_own_routes_are_removed():
    mine = "what its text calls \"x\": other.x, Other's data (CHG-R10GEN-001)"
    out, _ = rr.add_read_via(CONTRACT, "getB", [("other#xRecords", "service", mine)])
    back, n = rr.remove_own(out, "getB", "other#xRecords")
    assert n == 1 and "x-ticvai-read-via" not in yaml.safe_load(back)["paths"]["/b"]["get"]
    assert rr.remove_own(CONTRACT, "makeA", "things#thingRecords") == (CONTRACT, 0)
    assert rr.is_own({"for": "holdUntil ... (r10 read routes; CHG-R10GEN-001)"})
    assert not rr.is_own({"for": "what its text calls \"x\": other.x, Other's data (CHG-RTE-001)"})


def test_a_per_table_query_is_named_as_chg_mod_001_names_them():
    assert rr.records_name("orders.deposit_policy") == "depositPolicyRecords"
    assert rr.records_name("ledger.journal_line") == "journalLineRecords"


def test_the_owners_records_query_is_preferred_and_a_projection_alone_is_not_asked():
    queries = {"things#liveThings": ("things", {"table": "things.thing", "served": ["projection"]}),
               "things#thingRule": ("things", {"table": "things.thing", "served": ["service"]}),
               "things#thingRecords": ("things", {"table": "things.thing", "served": ["service"]}),
               "other#thingRecords": ("other", {"table": "things.thing", "served": ["service"]})}
    assert rr.pick_query("things.thing", "ThingService", queries, SVC_OF) == "things#thingRecords"
    del queries["things#thingRecords"]
    assert rr.pick_query("things.thing", "ThingService", queries, SVC_OF) == "things#thingRule"
    del queries["things#thingRule"]
    assert rr.pick_query("things.thing", "ThingService", queries, SVC_OF) is None


def test_the_plan_routes_by_deployable_declares_a_missing_query_and_holds_identity_above_foundation():
    ctx = {"services": SERVICES, "svc_of_contract": SVC_OF, "by": {},
           "queries": {"things#thingRecords": ("things", {"table": "things.thing", "served": ["service"]})},
           "persist": {("other", "OtherWidget"): "other.widget", ("other", "Widget"): "other.widget"}}
    findings = [("makeA", "OtherService", "things.thing", "ThingService", "table", "things.thing"),
                ("makeB", "ThingService", "other.widget", "OtherService", "fact", "the widget's own"),
                ("signIn", "IdentityService", "things.thing", "ThingService", "schema", "`Thing`")]
    plan, new_q, held, facts = rr.plan_routes(findings, ctx)
    assert plan["makeA"][0][:2] == ("things#thingRecords", "service")
    assert plan["makeB"][0][:2] == ("other#widgetRecords", "service")
    assert new_q == {"other#widgetRecords": ("other", "other.widget", "Widget")}   # the schema named like the table
    assert "signIn" not in plan and "ADR-0028" in held[0]
    assert facts and facts[0].startswith("makeB")
    assert plan["makeA"][0][2].endswith("(CHG-R10GEN-001)") and rr.is_own({"for": plan["makeA"][0][2]})


def test_a_new_data_query_is_written_once_in_the_chg_mod_001_shape():
    block = rr.rr.data_query("widgetRecords", "other", "other.widget", "Other", "commerce", ["service"], "Widget",
                             rr.SRC)
    out, added = rr.rr.add_query(CONTRACT, "widgetRecords", block)
    q = yaml.safe_load(out)["x-ticvai-queries"]["widgetRecords"]
    assert added and q["table"] == "other.widget" and q["served"] == ["service"]
    assert "CHG-R10GEN-001" in q["rule"] and q["returns"]["items"] == {"$ref": "#/components/schemas/Widget"}
    assert rr.rr.add_query(out, "widgetRecords", block) == (out, False)
    gone, removed = rr.remove_query(out, "widgetRecords")
    assert removed and "widgetRecords" not in yaml.safe_load(gone)["x-ticvai-queries"]
    assert rr.remove_query(CONTRACT, "thingRecords") == (CONTRACT, False)   # not this script's


def test_a_get_counts_a_response_fact_only_when_it_is_worked_out_on_read():
    def named(c):
        return {"platform.workstation": [("field", "x")]} if "Workstation" in c else {}
    computed = ["computed on read from the box's expected cash against `tenancy.Workstation.cashDrawerLimit`"]
    stored = ["Set once when the shift opens from `tenancy.Workstation.cashDrawerLimit`"]
    assert xr.get_counts("get", "platform.workstation", {}, computed, named)          # CR-218
    assert not xr.get_counts("get", "platform.workstation", {}, stored, named)        # fix round 1: the writer's
    assert xr.get_counts("get", "platform.workstation", {"platform.workstation": []}, stored, named)   # own words
    assert xr.get_counts("post", "platform.workstation", {}, stored, named)           # a write always
    assert xr.READ_ON_READ.search("none — projection over marketing.case and approvals.request")
    assert xr.READ_ON_READ.search("The signals behind the scores, as `ai.AiApprovalRequestScore.signals`.")


def test_a_scoped_not_read_leaves_the_operation_that_computes_the_metric():
    table = "| Metric | Source |\n|---|---|\n| `conversion` | `orders.cart` against `orders.sales_order` |"
    assert "orders.cart" not in xr.strip_not_read("setAlertRule", table)
    assert "orders.cart" in xr.strip_not_read("getKpiValues", table)


def test_a_contrast_sentence_is_not_a_read():
    owner = {"marketing": "MarketingService", "ledger": "LedgerService"}
    tables = {"marketing.campaign", "ledger.fx_rate"}
    assert xr.facts_named("A commercial campaign. **Not `marketing.campaign`**, which is the CRM send campaign.",
                          "CatalogueService", owner, tables) == {}
    assert xr.facts_named("A campaign is read from `marketing.campaign`.", "CatalogueService", owner, tables)
