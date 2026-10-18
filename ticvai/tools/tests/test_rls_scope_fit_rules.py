"""Tests for RF-INHERITED, RF-DEVICE-ABOVE and RF-PARENT-ACROSS in tools/check-rls-scope-fit.py (ADAM CR-095,
CR-108; CHG-RSF-001).

    python -m pytest ticvai/tools/tests/test_rls_scope_fit_rules.py -q
"""
import importlib.util
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("rf", TOOLS / "check-rls-scope-fit.py")
rf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rf)

MATRIX_SCOPE = {"approvals.matrix": ("apply_scope_rls", ""),
                "approvals.rule": ("apply_parent_rls", ", 'matrix_id', 'approvals.matrix'::regclass, 'id'")}
MATRIX_BENEATH = {"approvals.matrix": ("apply_read_beneath_rls", ""),
                  "approvals.rule": ("apply_parent_split_rls", ", 'matrix_id', 'approvals.matrix'::regclass, 'id', "
                                                               "'platform.in_scope(parent_row.scope_path)'")}
LIN = {"submitApprovalRequest": {"scope": "venue", "audience": ["staff"],
                                 "reads": ["approvals.matrix", "approvals.rule"]},
       "listApprovalMatrices": {"scope": "tenant", "audience": ["staff"], "reads": ["approvals.matrix"]}}


def keys(found):
    return sorted(k for _rule, k, _msg, _strict in found)


def test_a_venue_read_of_inherited_rows_is_found_with_its_child():
    got = rf.inherited_findings(LIN, MATRIX_SCOPE, rf.classes(MATRIX_SCOPE), {"approvals.matrix"})
    assert keys(got) == ["submitApprovalRequest:approvals.matrix", "submitApprovalRequest:approvals.rule"]
    assert all(strict for *_x, strict in got)


def test_read_beneath_lets_the_venue_read_them():
    assert rf.inherited_findings(LIN, MATRIX_BENEATH, rf.classes(MATRIX_BENEATH), {"approvals.matrix"}) == []


DEV_LIN = {"registerDevice": {"scope": "venue", "audience": ["staff"], "writes": ["platform.device"]},
           "recordDeviceHeartbeat": {"scope": "workstation", "audience": ["device"],
                                     "writes": ["platform.device", "platform.outbox"]}}
DEV_CL = {"platform.device": ("any", "scope"), "platform.outbox": ("scope", "scope")}
CREATORS = {"platform.device": {"venue"}, "platform.outbox": {"tenant"}}
HAS_PATH = {"platform.device", "platform.outbox"}


def test_a_device_writing_a_row_created_above_it_is_found():
    got = rf.device_findings(DEV_LIN, DEV_CL, HAS_PATH, CREATORS, {})
    assert keys(got) == ["recordDeviceHeartbeat:platform.device"]


def test_a_path_that_follows_the_workstation_fits():
    follows = {"platform.device": ("workstation_id", "platform.workstation", "workstation")}
    assert rf.device_findings(DEV_LIN, DEV_CL, HAS_PATH, CREATORS, follows) == []


POL = {"platform.outlet": ("apply_venue_rls", ""),
       "fnb.menu": ("apply_parent_rls", ", 'outlet_id', 'platform.outlet'::regclass, 'id'"),
       "fnb.menu_section": ("apply_parent_rls", ", 'menu_id', 'fnb.menu'::regclass, 'id'"),
       "orders.sales_order": ("apply_scope_rls", ""),
       "orders.order_line": ("apply_parent_rls", ", 'order_id', 'orders.sales_order'::regclass, 'id'")}
DEP = {"platform": "commerce", "orders": "commerce", "fnb": "operations"}
R6 = {"apply_parent_rls": "CREATE OR REPLACE FUNCTION platform.apply_parent_rls(target regclass) ... "
                          "format('EXISTS (SELECT 1 FROM %s parent_row WHERE ...)')"}
FIXED = {"apply_parent_rls": "CREATE OR REPLACE FUNCTION platform.apply_parent_rls(target regclass) ... "
                             "format('platform.parent_visible(%L::regclass, %I)', parent::text, fk_column)",
         "parent_visible": "CREATE OR REPLACE FUNCTION platform.parent_visible(parent regclass, key_value uuid, "
                           "for_write boolean DEFAULT false) RETURNS boolean LANGUAGE plpgsql STABLE SECURITY "
                           "DEFINER ... IF parent = 'platform.outlet'::regclass THEN ... IF parent = "
                           "'fnb.menu'::regclass THEN ... IF parent = 'orders.sales_order'::regclass THEN ..."}


def test_a_chain_into_another_deployable_needs_the_definer_function():
    assert rf.parent_chain("fnb.menu_section", POL) == ["fnb.menu", "platform.outlet"]
    got = rf.parent_across_findings(POL, DEP, R6)
    assert keys(got) == ["fnb.menu", "fnb.menu_section"]       # orders.order_line stays inside commerce
    assert all(strict for *_x, strict in got)


def test_the_definer_function_answering_each_parent_fits():
    assert rf.parent_across_findings(POL, DEP, FIXED) == []


def test_a_parent_the_function_does_not_answer_is_found():
    missing = dict(FIXED, parent_visible=FIXED["parent_visible"].replace("'platform.outlet'::regclass",
                                                                        "'x.y'::regclass"))
    assert keys(rf.parent_across_findings(POL, DEP, missing)) == ["fnb.menu", "fnb.menu_section"]


def test_only_the_hop_across_deployables_needs_the_function():
    # decision D9: fnb.menu asks the function for platform.outlet; fnb.menu_section keeps r6's EXISTS on fnb.menu,
    # which its own host may read
    pol = dict(POL, **{"fnb.menu": ("apply_parent_across_rls", POL["fnb.menu"][1])})
    bodies = dict(R6, apply_parent_across_rls=FIXED["apply_parent_rls"], parent_visible=FIXED["parent_visible"])
    assert rf.parent_chain("fnb.menu_section", pol) == ["fnb.menu", "platform.outlet"]
    assert rf.parent_across_findings(pol, DEP, bodies) == []
    assert rf.classes(pol)["fnb.menu_section"] == ("scope", "scope")


def test_devices_are_judged_now():
    assert "device" in rf.JUDGED_AUDIENCE
