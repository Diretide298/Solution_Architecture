"""Tests for tools/check-screen-value-sources.py (CHG-R10GEN-003): each rule on the r9 form of the CR it comes from,
and the screens that hold their values, which must stay clean.

    python -m pytest ticvai/tools/tests/test_check_screen_value_sources.py -q
"""
import importlib.util
from pathlib import Path

import yaml

TOOLS = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("sv", TOOLS / "check-screen-value-sources.py")
sv = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sv)

CONTRACT = yaml.safe_load("""
paths:
  /options:
    get:
      operationId: getPlannerOptions
      x-ticvai-audience: [guest]
      responses:
        '200':
          content: {application/json: {schema: {$ref: '#/components/schemas/PlannerOptions'}}}
  /plans:
    post:
      operationId: makePlan
      x-ticvai-audience: [guest]
      requestBody:
        content: {application/json: {schema: {$ref: '#/components/schemas/PlanRequest'}}}
      responses:
        '201':
          content: {application/json: {schema: {$ref: '#/components/schemas/Plan'}}}
  /products:
    get:
      operationId: listProducts
      x-ticvai-audience: [guest, staff]
      responses:
        '200':
          content: {application/json: {schema: {type: array, items: {$ref: '#/components/schemas/Product'}}}}
  /tokens:
    get:
      operationId: listPaymentTokens
      x-ticvai-audience: [guest, staff]
      responses:
        '200':
          content: {application/json: {schema: {type: array, items: {$ref: '#/components/schemas/PaymentToken'}}}}
  /cases/{caseId}/retry:
    post:
      operationId: retryPayment
      x-ticvai-audience: [guest]
      parameters: [{name: caseId, in: path}]
      requestBody:
        content: {application/json: {schema: {$ref: '#/components/schemas/RetryRequest'}}}
      responses:
        '200':
          content: {application/json: {schema: {$ref: '#/components/schemas/Case'}}}
  /seats:
    get:
      operationId: getSeats
      x-ticvai-audience: [guest]
      responses:
        '200':
          content: {application/json: {schema: {$ref: '#/components/schemas/Seats'}}}
  /config:
    get:
      operationId: getConfig
      x-ticvai-audience: [guest]
      responses:
        '200':
          content: {application/json: {schema: {$ref: '#/components/schemas/Config'}}}
  /me/profile:
    patch:
      operationId: updateMyProfile
      x-ticvai-audience: [guest]
      requestBody:
        content: {application/json: {schema: {properties: {preferredLanguage: {type: string}}}}}
      responses:
        '200': {description: ok}
components:
  schemas:
    PlannerOptions:
      properties: {interestTags: {type: array, items: {type: string}}}
    PlanRequest:
      properties: {cuisineTags: {type: array, items: {type: string}}, pace: {type: string}}
    Plan:
      properties: {days: {type: array, items: {type: object}}}
    Point:
      x-ticvai-persistence: map.point
      properties: {cuisineTags: {type: array, items: {type: string}}, interestTags: {type: array}}
    Product:
      x-ticvai-persistence: catalogue.product
      properties:
        name: {type: string}
        media: {type: array, items: {$ref: '#/components/schemas/ProductMedia'}}
    ProductMedia:
      properties:
        assetId: {type: string, format: uuid, x-ticvai-references: assets.media_asset}
        kind: {type: string}
    PaymentToken:
      properties: {id: {type: string}, last4: {type: string}}
    RetryRequest:
      properties: {paymentTokenId: {type: string, format: uuid}}
    Case:
      properties: {id: {type: string}, state: {type: string}}
    Seats:
      properties: {seats: {type: array}, holdExpiresAt: {type: string}}
    Cart:
      x-ticvai-persistence: orders.cart
      properties: {expiresAt: {type: string}}
    Settings:
      x-ticvai-persistence: platform.venue_settings
      properties:
        seating:
          type: object
          properties: {maxSeatsPerGuestOrder: {type: integer}}
        pinLength: {type: integer}
    Config:
      properties: {languages: {type: array, items: {type: string}}}
""")


def screen(sid, components=(), apis=(), overlays=(), states=None, entry=None):
    s = {"id": sid, "layout": {"regions": [{"name": "body", "components": list(components)}]},
         "apis": [{"operationId": o, "trigger": t} for o, t in apis], "states": states or {}}
    if overlays:
        s["overlays"] = list(overlays)
    if entry:
        s["entryState"] = entry
    return s


def run(*screens, platform="P01-guest-web-storefront"):
    pk = sv.Package(contracts=[("things", "contracts/x/things.yaml", CONTRACT)],
                    screens=[(platform, s) for s in screens])
    return {(r, k) for r, k, _m in sv.findings(pk)}


def test_cr220_a_choice_with_no_read_before_it():
    planner = screen("GST-051", components=[
        {"kind": "multiSelect", "label": "Interests", "operation": "getPlannerOptions",
         "notes": "Interest tags from the venue's points (`Point.interestTags`)."},
        {"kind": "selectField", "label": "Lunch",
         "notes": "**Cuisines from the dining points** (`Point.cuisineTags` of restaurants); sent as `cuisineTags`."},
        {"kind": "selectField", "label": "Pace", "notes": "Packed or relaxed, sent as `pace`."},
    ], apis=[("getPlannerOptions", "onLoad"), ("makePlan", "onAction")])
    got = run(planner)
    assert ("SV-OPTIONS", "GST-051:Lunch:cuisineTags") in got
    # the interest tags come from the load read; the pace is the guest's own input, stored nowhere
    assert not any("Interests" in k or "pace" in k for _r, k in got)


def test_cr221_a_photo_that_is_only_an_asset_id():
    got = run(screen("WEB-003", components=[
        {"kind": "cardList", "label": "Suggestions", "bindsTo": "Product", "operation": "listProducts",
         "columns": ["Product.name", "Product.media"]}], apis=[("listProducts", "onLoad")]))
    assert got == {("SV-MEDIA", "WEB-003:Product.media")}


def test_cr233_an_id_to_pick_with_no_list_declared():
    form = {"id": "formRetry", "component": "modal", "bindsTo": "RetryRequest",
            "body": "Collects what `retryPayment` sends. Optional: `paymentTokenId`.",
            "confirm": {"operation": "retryPayment"}, "dismiss": {"discards": ["paymentTokenId"]}}
    bare = screen("WEB-023", apis=[("retryPayment", "onAction")], overlays=[form])
    assert run(bare) == {("SV-PICK", "WEB-023:formRetry:paymentTokenId")}
    listed = screen("WEB-023", apis=[("retryPayment", "onAction"), ("listPaymentTokens", "onAction")],
                    overlays=[form])
    assert run(listed) == set()


def test_cr187_a_countdown_and_a_cap_the_screen_never_reads():
    seats = screen("WEB-007", components=[
        {"kind": "banner", "notes": "**One countdown: `Cart.expiresAt`** (the earliest lease), always visible."},
        {"kind": "seatMap", "label": "Seats", "operation": "getSeats",
         "notes": "**At most `Settings.seating.maxSeatsPerGuestOrder` seats per booking**."},
    ], apis=[("getSeats", "onLoad")], overlays=[
        {"id": "formRecommend", "body": "The party size (a stepper, at most `maxSeatsPerGuestOrder`)."}])
    got = run(seats)
    assert ("SV-SCHEMA", "WEB-007:Cart") in got
    assert ("SV-SCHEMA", "WEB-007:formRecommend:maxSeatsPerGuestOrder") in got
    # the seat map's own notes explain its operation's rule, so only the form's stepper counts for the cap
    assert not any(k.startswith("WEB-007:Settings") for _r, k in got)


def test_cr186_a_save_the_screen_never_calls():
    lang = {"kind": "selectField", "label": "Language", "bindsTo": "Config.languages", "operation": "getConfig",
            "notes": "The choice is stored on the device and, for a signed-in guest, as the profile's language."}
    assert run(screen("GST-043", components=[lang], apis=[("getConfig", "onLoad")])) == {
        ("SV-WRITE", "GST-043:Language")}
    assert run(screen("GST-043", components=[lang], apis=[("getConfig", "onLoad"),
                                                          ("updateMyProfile", "onAction")])) == set()


def test_rule_citations_and_held_values_are_not_gaps():
    s = screen("POS-000", components=[
        {"kind": "pinField", "label": "PIN",
         "notes": "Of the tenant's PIN length (`Settings.pinLength`); the denied state counts against `Settings.pinLength`."},
        {"kind": "detailPanel", "label": "Seats", "bindsTo": "Seats", "operation": "getSeats",
         "columns": ["Seats.seats", "Seats.holdExpiresAt"]},
        {"kind": "multiSelect", "label": "Filter by", "columns": ["Product", "Status"],
         "notes": "Sends `?status=`."},
    ], apis=[("getSeats", "onLoad")], states={"error": "Could not load (`Cart.expiresAt` aside)."},
        entry={"preloaded": ["Config (languages), loaded by the app shell"]})
    assert run(s, platform="P04-point-of-sale") == set()


def test_a_preloaded_schema_is_a_source():
    s = screen("WEB-009", components=[{"kind": "banner", "notes": "Shows `Config.languages`."}])
    assert run(s) == {("SV-SCHEMA", "WEB-009:Config")}
    s["entryState"] = {"preloaded": ["Config, loaded once by the app shell"]}
    assert run(s) == set()


def test_a_binding_to_a_schema_nothing_answers_is_one_finding_per_schema():
    s = screen("ACC-005", components=[
        {"kind": "detailPanel", "label": "Badge", "bindsTo": "Cart"},
        {"kind": "metricTile", "label": "Expires", "bindsTo": "Cart.expiresAt"}], apis=[("getSeats", "onLoad")])
    assert run(s) == {("SV-SCHEMA", "ACC-005:Cart")}


def test_a_merged_screen_is_judged_on_its_target():
    """CHG-R10UI-016: ADM-097, ADM-252 and ADM-611 were merged on 2 October (CHG-MOV-002); their target declares the reads."""
    s = screen("ADM-097", components=[{"kind": "detailPanel", "label": "Badge", "bindsTo": "Cart"}])
    assert run(s) == {("SV-SCHEMA", "ADM-097:Cart")}
    s["notes"] = "**Merged into BO-441 Price Priority & Conflict Rules** (decided 2 October 2026)."
    assert run(s) == set()


def test_paren_and_shown_word_helpers():
    t = "The limit is set per country (`A.b`). One countdown: `C.d`."
    assert sv.in_parens(t, t.index("`A.b`")) and not sv.in_parens(t, t.index("`C.d`"))
    assert sv.shown(t, t.index("`C.d`")) and not sv.shown(t, t.index("`A.b`"))
