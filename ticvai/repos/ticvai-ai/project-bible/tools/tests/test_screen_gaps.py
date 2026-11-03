"""Tests for tools/screen_gaps.py (CHG-R13RVB-004): a generated gap or note its own record has overtaken.

    python -m pytest ticvai/tools/tests/test_screen_gaps.py -q
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import screen_gaps as sg  # noqa: E402

OPS = {
    "listSegregationRules": {"method": "get", "op": {"responses": {"200": {"content": {"application/json": {
        "schema": {"$ref": "#/components/schemas/SegregationRule"}}}}}}},
    "setSegregationRules": {"method": "put", "op": {}},
    "listProductionPlans": {"method": "get", "op": {}},
    "getKitchenSla": {"method": "get", "op": {"description": "(contract gap logged in CHG-WIR-011 for KIT-009; built "
                                                             "in CHG-CSA-045)"}},
}
SCHEMAS = {"SegregationRule": {"properties": {"id": {}, "actions": {}}}}


def screen(sid, apis, gaps, **kw):
    return {"id": sid, "apis": [{"operationId": a} for a in apis], "gaps": gaps, **kw}


def test_a_write_and_a_schema_the_gap_says_are_missing():
    s = screen("ADM-340", ["listSegregationRules", "setSegregationRules"], [
        {"operation": None, "why": "**Segregation of Duties declares no operation that writes anything**"},
        {"operation": None, "why": "**This screen's operations return no schema with described properties**"},
        {"operation": None, "why": "**The pack names 2 actions on this screen and the screen declares 0 operations.**"}])
    assert sg.stale_gaps(s, OPS, SCHEMAS) == [(0, "gap-no-write", "drop"), (1, "gap-no-schema", "drop"),
                                              (2, "gap-op-count", ("count", 2))]
    assert sg.stale_gaps(s, OPS, SCHEMAS, skip={"ADM-340"}) == []   # a twin is its copying tool's


def test_a_read_the_gap_says_is_missing_and_a_built_contract_gap():
    s = screen("KIT-009", ["listProductionPlans", "getKitchenSla"], [
        {"operation": None, "why": "Contract gap recorded 2 October 2026 (CHG-WIR-011): No read of production plans "
                                   "(list or get)."},
        {"operation": None, "why": "Contract gap recorded 2 October 2026 (CHG-WIR-011): something else."},
        {"operation": None, "why": "No read of the kitchen display rules."}])
    assert sg.stale_gaps(s, OPS, SCHEMAS) == [(0, "gap-no-read", "drop"), (1, "gap-built", "drop")]


def test_the_board_import_sentence():
    s = screen("EMP-002", ["listProductionPlans"], [], layout={"regions": []}, states={"loading": "x"},
               notes="Definition derived from the wireframe board on 14 August. Components, states and operations\n"
                     "still to be written.")
    assert sg.still_to_be_written(s)
    s["apis"] = []
    assert not sg.still_to_be_written(s)
