"""Tests for tools/applied/read-routes-18-october.py (CHG-RTE-001): the YAML it writes at its own lines.

    python -m pytest ticvai/tools/tests/test_read_routes_apply.py -q
"""
import importlib.util
from pathlib import Path

import yaml

TOOLS = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("rr", TOOLS / "applied" / "read-routes-18-october.py")
rr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rr)

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
      x-ticvai-consumed-by:
        - "P08 BO-001 Something"
      x-ticvai-audience: [staff]
      summary: Make an A
  /b:
    get:
      operationId: getB
      x-ticvai-read-via:
      - query: things#thingRecords
        route: service
        for: 'already there'
      summary: Get a B
"""


def test_a_read_via_block_goes_after_consumed_by():
    out, n = rr.add_read_via(CONTRACT, "makeA", [("things#thingRecords", "in-process", "the venue's thing")])
    assert n == 1
    op = yaml.safe_load(out)["paths"]["/a"]["post"]
    assert op["x-ticvai-read-via"] == [{"query": "things#thingRecords", "route": "in-process",
                                         "for": "the venue's thing"}]
    assert op["x-ticvai-consumed-by"] == ["P08 BO-001 Something"]


def test_an_existing_list_is_appended_to_once():
    out, n = rr.add_read_via(CONTRACT, "getB", [("things#thingRecords", "service", "again"),
                                                ("other#xRecords", "service", "new")])
    assert n == 1
    via = yaml.safe_load(out)["paths"]["/b"]["get"]["x-ticvai-read-via"]
    assert [v["query"] for v in via] == ["things#thingRecords", "other#xRecords"]
    again, n2 = rr.add_read_via(out, "getB", [("other#xRecords", "service", "new")])
    assert n2 == 0 and again == out


def test_served_gains_a_route_and_the_rule_says_so():
    out, changed = rr.add_served(CONTRACT, "thingRecords", "in-process", "operations")
    q = yaml.safe_load(out)["x-ticvai-queries"]["thingRecords"]
    assert changed and q["served"] == ["in-process", "service"]
    assert q["rule"].endswith("It is asked in process within operations, through the C# query interface Things "
                              "implements, and asked from another deployable through Things' service route "
                              "(serviceAuth).")
    assert rr.add_served(out, "thingRecords", "in-process", "operations") == (out, False)


def test_a_query_is_added_once():
    block = "  newRecords:\n    module: things\n    table: things.new\n    served: [in-process]\n"
    out, added = rr.add_query(CONTRACT, "newRecords", block)
    assert added and "newRecords" in yaml.safe_load(out)["x-ticvai-queries"]
    assert rr.add_query(out, "newRecords", block) == (out, False)


def test_route_follows_the_deployables():
    assert rr.route_for("operations", "operations") == "in-process"
    assert rr.route_for("operations", "commerce") == "service"


SWEPT = """paths:
  /c:
    get:
      operationId: getC
      x-ticvai-read-via:
      - query: things#thingRecords
        route: service
        for: 'its read of things.thing, Things''s data (CHG-MOD-001)'
      - query: other#xRecords
        route: service
        for: 'what its text calls "x": other.x, Other''s data (CHG-RTE-001)'
      summary: Get a C
  /d:
    get:
      operationId: getD
      x-ticvai-read-via:
      - query: other#xRecords
        route: service
        for: 'what its text calls "x": other.x, Other''s data (CHG-RTE-001)'
      summary: Get a D
"""


def test_a_swept_route_no_longer_justified_is_removed_and_nothing_else():
    out, n = rr.remove_read_via(SWEPT, "getC", "other#xRecords")
    assert n == 1
    doc = yaml.safe_load(out)["paths"]
    assert [v["query"] for v in doc["/c"]["get"]["x-ticvai-read-via"]] == ["things#thingRecords"]
    out2, n2 = rr.remove_read_via(out, "getD", "other#xRecords")
    assert n2 == 1 and "x-ticvai-read-via" not in yaml.safe_load(out2)["paths"]["/d"]["get"]
    # a route this script did not write is never removed
    assert rr.remove_read_via(SWEPT, "getC", "things#thingRecords") == (SWEPT, 0)


def test_served_follows_its_askers_but_never_drops_below_what_the_owner_declared():
    out, _ = rr.add_served(CONTRACT, "thingRecords", "in-process", "operations")
    back, changed = rr.set_served(out, "thingRecords", ["service"], "operations")
    assert changed and yaml.safe_load(back)["x-ticvai-queries"]["thingRecords"]["served"] == ["service"]
    assert yaml.safe_load(back)["x-ticvai-queries"]["thingRecords"]["rule"].endswith(
        "It is asked from another deployable through Things' service route (serviceAuth).")
    assert rr.served_for(["service"], {"in-process"}) == ["in-process", "service"]
    assert rr.served_for(["service"], set()) == ["service"]


def test_a_read_is_swept_only_where_its_own_text_names_the_fact():
    # fix round 1: a GET whose phrase sits only in a shared response schema (a write rule) is not swept
    assert rr.sweep_skips("get", "platform.scope", {})
    assert not rr.sweep_skips("get", "platform.scope", {"platform.scope": [("fact", "active venues")]})
    assert not rr.sweep_skips("post", "platform.scope", {})
