"""Tests for check-contract-shapes' C-REFUSAL-UNDECLARED as widened by the r13 review (CHG-R13RVB-002).

    python -m pytest ticvai/tools/tests/test_check_contract_shapes_refusals.py -q
"""
import importlib.util
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("cs", TOOLS / "check-contract-shapes.py")
cs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cs)


def test_the_forms_a_text_promises_a_status_in():
    assert cs.promised_statuses("An unknown `reportId` is `404`; there is no create-on-PUT.") == {"404"}
    assert cs.promised_statuses("A recipient outside the tenant is therefore the shared 404, exactly as ...") == {"404"}
    assert cs.promised_statuses("Exactly one `owner` must remain, or 409. Nothing is written.") == {"409"}
    assert cs.promised_statuses("(409 when the batch has fewer left)") == {"409"}
    assert cs.promised_statuses("`getBillingStatement` answers `404` for it.") == set()


def test_a_status_with_its_problem_type():
    t = "Above it without `ORDER_DISCOUNT` is a `403` (`comp-escalation-required`)."
    assert cs.promised_types(t, "compItem", {"compItem"}) == {("403", "comp-escalation-required")}
    assert cs.promised_types("refused `403 witness-not-verified`", "x", set()) == {("403", "witness-not-verified")}
    # the shared ones, a negation, and a paragraph telling what another operation answers
    assert cs.promised_types("refused `400 validation` or `403` (`forbidden`)", "x", set()) == set()
    assert cs.promised_types("there is no `409 approval-required`.", "x", set()) == set()
    assert cs.promised_types("`bookResource` refuses it with `409 resource-awaiting-inspection`.", "checkInResource",
                             {"bookResource", "checkInResource"}) == set()
