"""The generators write the r10 patterns by default (CHG-R10GEN-007): one test per generator rule.

    python -m pytest ticvai/tools/tests/test_generators_r10_patterns.py -q

(a) Money reads its currency source, (b) a list states its order, nulls last then id, (d) a generated screen binds
only what its declared operations answer or send, (e) a fact another module owns is asked of its owner's query,
(f) a public guest read of venue data takes GuestVenue and declares 400 venue-required (CR-198), (g) a permission is
evaluated per scope (CR-189). (c) has no generator rule: no generator writes a refusal.
"""
import importlib.util
import sys
from pathlib import Path

import yaml

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
import contract_shapes as CS  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, TOOLS / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


dpo = _load("dpo_r10", "draft-pack-operations.py")
spo = _load("spo_r10", "specify-pack-operations.py")
lo = _load("lo_r10", "check-list-order.py")
MONEY = {"$ref": "../shared/common.yaml#/components/schemas/Money"}


# --- the shared rules (contract_shapes) -----------------------------------------------------------------------------

def test_b_a_list_order_puts_nulls_last_then_id_in_words_check_list_order_reads():
    nullable = CS.order_sentence({"id": {}, "name": {}}, ["id"])
    assert "NULLS LAST" in nullable and "`id`" in nullable
    assert lo.ORDER_STATED.search(nullable) and lo.ANYWHERE.search(nullable)
    assert CS.order_sentence({"id": {}, "name": {}}, ["id", "name"]).startswith(
        "**Order.** Sorted by `name` ascending, then by `id`.")
    assert "createdAt" in CS.order_sentence({"id": {}, "createdAt": {}}, ["id"])
    assert "`id` descending" in CS.order_sentence({"id": {}}, ["id"])


def test_f_a_public_guest_read_of_venue_data_takes_guestvenue_and_400_once():
    op = {"x-ticvai-audience": ["guest"], "x-ticvai-scope-level": "venue", "responses": {"200": {}}}
    assert CS.add_guest_venue(op, "get", "/things")
    assert op["parameters"] == [{"$ref": CS.GUEST_VENUE_REF}] and op["responses"]["400"] == {
        "$ref": CS.VENUE_REQUIRED_REF}
    assert CS.add_guest_venue(op, "get", "/things") and len(op["parameters"]) == 1     # a second call adds nothing
    assert not CS.add_guest_venue(dict(op, parameters=[]), "get", "/venues/{venueId}/things")
    assert not CS.add_guest_venue({"x-ticvai-audience": ["staff"], "x-ticvai-scope-level": "venue"}, "get", "/x")
    assert not CS.add_guest_venue({"x-ticvai-audience": ["guest"], "x-ticvai-scope-level": "venue"}, "post", "/x")


def test_g_a_permission_is_evaluated_per_scope():
    assert "permissionsByScope" in CS.scope_sentence("GUEST_VIEW", "venue", True)
    assert "403" in CS.scope_sentence("GUEST_VIEW", "venue", True)
    assert "tenant root" in CS.scope_sentence("ROLE_MANAGE", "tenant", False)
    assert "venue the operation acts on" in CS.scope_sentence("CAT_EDIT", "venue", False)
    assert CS.scope_sentence(None, "venue", False) == ""


def test_a_money_asks_the_venue_or_region_settings_by_deployable():
    v = CS.money_read_via(True, "venue", "commerce")
    assert v[0]["query"] == "tenancy#venueSettingsRecords" and v[0]["route"] == "in-process"
    # ADAM CR-296 (CHG-R11RUL-001): the operations host reads Tenancy's settings in process (XDR-004); a deployable
    # with no grant still asks them over the service route.
    assert CS.money_read_via(True, "outlet", "operations")[0]["route"] == "in-process"
    assert CS.money_read_via(True, "venue", "access")[0]["route"] == "service"
    assert CS.read_route("operations", "commerce", "tenancy#scopeRecords") == "in-process"
    assert CS.read_route("operations", "commerce", "identity#principalRecords") == "service"
    assert CS.money_read_via(True, "region", "commerce")[0]["query"] == "tenancy#regionSettingsRecords"
    assert CS.money_read_via(True, "tenant", "commerce") == []          # nothing denominates: the check asks
    assert CS.money_read_via(False, "venue", "commerce") == []
    assert CS.has_money({"A": {"properties": {"b": {"$ref": "#/components/schemas/B"}}}},
                        {"B": {"properties": {"p": MONEY}}})


def test_d_a_generated_binding_with_no_declared_source_is_unbound():
    ops = {"getThing": {"op": {"responses": {"200": {"content": {"application/json": {"schema": {
        "$ref": "#/components/schemas/Thing"}}}}}}},
           "setThing": {"op": {"requestBody": {"content": {"application/json": {"schema": {
               "$ref": "#/components/schemas/ThingInput"}}}}}}}
    answered, sent = CS.declared_io(["getThing", "setThing"], ops, {})
    assert answered == {"Thing"} and sent == {"ThingInput"}
    regions = [{"name": "contentBody", "components": [
        {"kind": "detailPanel", "bindsTo": "Thing", "provenance": "contract x.yaml GET /t"},
        {"kind": "textField", "bindsTo": "ThingInput.name", "provenance": "contract x.yaml PUT /t"},
        {"kind": "detailPanel", "bindsTo": "Cart.expiresAt", "provenance": "contract x.yaml GET /t"},   # CR-187
        {"kind": "detailPanel", "bindsTo": "Cart", "provenance": "authored by a person"}]}]
    assert CS.drop_unsourced(regions, [], answered, sent, mine=("contract ",)) == 1
    comps = regions[0]["components"]
    assert "bindsTo" not in comps[2] and "Cart.expiresAt" in comps[2]["notes"]
    assert comps[0]["bindsTo"] == "Thing" and comps[1]["bindsTo"] == "ThingInput.name"
    assert comps[3]["bindsTo"] == "Cart"                                  # not this generator's to change


def test_e_a_fact_named_in_the_text_is_asked_of_its_owners_query():
    routes = CS.fact_routes("refused 422 when the venue settings say no", "CatalogueService")
    assert any(r["query"] == "tenancy#venueSettingsRecords" and r["route"] == "in-process" for r in routes)
    assert CS.fact_routes("a plain sentence about nothing in particular", "CatalogueService") == []


# --- draft-pack-operations.block -------------------------------------------------------------------------------------

def _drafted(verb, aud, scope, array, routes, route="/things", perm="GUEST_VIEW"):
    b = dpo.block("listThings" if array else "setThing", verb, "P05 GST-001 Things", "Things", "Shows things",
                  perm, scope, aud, "DraftedRecord", array, 3, "Mod", route=route, reader="CatalogueService",
                  routes=routes)
    return yaml.safe_load("x:\n  %s:\n%s" % (verb, b))["x"][verb]


def test_draft_pack_operations_a_drafted_list_states_its_order_and_reach():
    op = _drafted("get", "staff", "venue", True, [])
    assert "NULLS LAST" in op["description"] and "permissionsByScope" in op["description"]


def test_draft_pack_operations_a_drafted_guest_read_names_its_venue():
    op = _drafted("get", "guest", "venue", True, [])
    assert op["parameters"] == [{"$ref": CS.GUEST_VENUE_REF}] and op["responses"]["400"]["$ref"].endswith(
        "VenueRequired")
    assert "parameters" not in _drafted("get", "guest", "venue", True, [], route="/venues/{venueId}/things")


def test_draft_pack_operations_a_drafted_write_at_tenant_level_needs_the_tenant_root():
    op = _drafted("put", "staff", "tenant", False, [])
    assert "tenant root" in op["description"] and "parameters" not in op


def test_draft_pack_operations_writes_the_read_routes_its_purpose_calls_for():
    op = _drafted("get", "staff", "venue", True, [{"query": "tenancy#venueSettingsRecords", "route": "in-process",
                                                   "for": "the venue's own"}])
    assert op["x-ticvai-read-via"] == [{"query": "tenancy#venueSettingsRecords", "route": "in-process",
                                        "for": "the venue's own"}]


# --- specify-pack-operations.apply_r10 -------------------------------------------------------------------------------

def _shaped(method, scope, aud, schemas, is_list, routes=()):
    new = {"operationId": "listGuestThings", "x-ticvai-consumed-by": ["P05 GST-1 Things"], "x-ticvai-audience": aud,
           "summary": "s", "description": "d", "x-ticvai-permission": "GUEST_VIEW", "x-ticvai-scope-level": scope,
           "responses": {"200": {}}}
    props = next(iter(schemas.values()))["properties"]
    return spo.apply_r10(new, schemas, "catalogue", method, "/guest-things", "shows things", is_list, props,
                         list(routes))


def test_specify_pack_operations_money_declares_its_currency_read_after_consumed_by():
    out = _shaped("get", "venue", ["staff"], {"ThingView": {"properties": {"price": MONEY, "name": {}}}}, True)
    assert out["x-ticvai-read-via"][0]["query"] == "tenancy#venueSettingsRecords"
    assert list(out).index("x-ticvai-read-via") == list(out).index("x-ticvai-consumed-by") + 1
    assert "x-ticvai-read-via" not in _shaped("get", "venue", ["staff"], {"V": {"properties": {"name": {}}}}, True)


def test_specify_pack_operations_a_shaped_list_states_order_and_reach_and_a_guest_read_its_venue():
    out = _shaped("get", "venue", ["guest"], {"V": {"properties": {"name": {}}}}, True)
    assert "NULLS LAST" in out["description"] and "permissionsByScope" in out["description"]
    assert out["parameters"] == [{"$ref": CS.GUEST_VENUE_REF}] and "400" in out["responses"]


def test_specify_pack_operations_merges_fact_routes_without_repeating_the_money_read():
    r = [{"query": "tenancy#venueSettingsRecords", "route": "in-process", "for": "x"},
         {"query": "catalogue#productRecords", "route": "in-process", "for": "y"}]
    out = _shaped("post", "venue", ["staff"], {"V": {"properties": {"price": MONEY}}}, False, r)
    assert [v["query"] for v in out["x-ticvai-read-via"]] == ["tenancy#venueSettingsRecords",
                                                              "catalogue#productRecords"]
