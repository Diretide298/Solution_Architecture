"""The check rules ADAM CR-313, CR-316 and CR-320 added (CHG-CR313-001, CHG-CR316-001, CHG-CR320-001).

    python -m pytest ticvai/tools/tests/test_cr_forms_r11.py -q

C-REFUSAL-UNDECLARED (check-contract-shapes): an operation's own text that promises a refusal by status.
ST-TYPE-MISMATCH (check-contract-storage): an array of records stored in a scalar array column.
C-FINDING-RULE (check-contract-shapes): a finding kind its kind table gives no "reported when" rule.
"""
import importlib.util
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]


def _load(name: str, file: str):
    spec = importlib.util.spec_from_file_location(name, TOOLS / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


shapes = _load("check_contract_shapes", "check-contract-shapes.py")
storage = _load("check_contract_storage", "check-contract-storage.py")


def test_promised_refusals_are_read():
    # setCodeDistributionManager's text before CR-316: the 409 it described and did not declare
    assert shapes.promised_statuses("move to `assigned` (409\n        when the batch has fewer left)") == {"409"}
    assert shapes.promised_statuses("validation that contradicts the type is refused (422).") == {"422"}
    assert shapes.promised_statuses("covers, is refused with 409 `tableHasOpenVisit`") == {"409"}
    assert shapes.promised_statuses("(`409 not-enough-codes-in-batch` when the batch has fewer left") == {"409"}


def test_other_mentions_are_not_promises():
    assert shapes.promised_statuses("rather than 404") == set()
    assert shapes.promised_statuses("never a `404` when nothing is set") == set()
    assert shapes.promised_statuses("outside the caller's grants is refused (403)") == set()
    assert shapes.promised_statuses("answers `410 superseded`, not 404") == set()


def test_an_array_of_records_is_not_a_scalar_array():
    by = {}
    options = {"type": "array", "items": {"type": "object", "required": ["value"],
                                          "properties": {"value": {"type": "string"}, "label": {"type": "object"}}}}
    k = storage.kind(options, by, "marketing-crm")
    assert k == "arr:rec"
    assert not storage.compatible(k, "text[]")       # CR-313: form_definition_field.options
    assert storage.compatible(k, "jsonb")             # option_labels


def test_scalar_and_unresolved_arrays_keep_their_rule():
    by = {}
    assert storage.compatible(storage.kind({"type": "array", "items": {"type": "string"}}, by, "x"), "text[]")
    # a $ref to another file this check cannot resolve stays `obj`, compatible as before (SalesChannel lists)
    unresolved = {"type": "array", "items": {"$ref": "../shared/common.yaml#/components/schemas/SalesChannel"}}
    assert storage.kind(unresolved, by, "x") == "arr:obj"
    assert storage.compatible("arr:obj", "text[]")


# C-FINDING-RULE (check-contract-shapes; ADAM CR-320, CHG-CR320-001): a finding kind with no rule beside it.
_TABLE = ("Severity first.\n\n| kind | severity | reported when |\n|---|---|---|\n"
          "| missingTranslation | warning | a LocalisedText field has no text in a language |\n"
          "| bookingFlowMissing | error | an active venue has a product no enabled flow serves |\n")


def test_every_kind_with_a_rule_passes():
    assert shapes.finding_rule_gaps({"enum": ["missingTranslation", "bookingFlowMissing"],
                                     "description": _TABLE}) == []


def test_a_kind_without_a_row_or_an_empty_rule_is_a_gap():
    s = {"enum": ["missingTranslation", "bookingFlowMissing", "noVisibleNavigationItems"], "description": _TABLE}
    assert shapes.finding_rule_gaps(s) == ["noVisibleNavigationItems"]
    s = {"enum": ["missingTranslation"], "description": "| kind | severity | reported when |\n|---|---|---|\n"
                                                         "| missingTranslation | warning |  |\n"}
    assert shapes.finding_rule_gaps(s) == ["missingTranslation"]


def test_a_table_without_the_rule_column_leaves_every_kind_without_a_rule():
    s = {"enum": ["a", "b"], "description": "| kind | severity |\n|---|---|\n| a | error |\n| b | error |\n"}
    assert shapes.finding_rule_gaps(s) == ["a", "b"]


def test_an_enum_with_no_kind_table_is_not_judged():
    assert shapes.finding_rule_gaps({"enum": ["a"], "description": "The publish checks."}) == []
