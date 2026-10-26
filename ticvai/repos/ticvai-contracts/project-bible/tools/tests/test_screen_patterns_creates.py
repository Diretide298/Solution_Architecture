"""Tests for screen_patterns.creates and param_for (CHG-R10GFP-002): a write on the screen that answers with the id
makes it, whatever its verb, so the entry parameter is written optional (WEB-024 and GST-066's `requestId`, which
exportSubjectData answers and getSubjectDataExport polls; ADAM CR-101).

    python -m pytest ticvai/tools/tests/test_screen_patterns_creates.py -q
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import screen_patterns as SP  # noqa: E402


class Pk:
    """The two things creates() and param_for() read from a package: operations and their answers."""

    def __init__(self, ops, answers):
        self.ops, self.answers = ops, answers

    def response_props(self, o):
        return set(self.answers.get(o, ()))


PK = Pk({
    "exportSubjectData": {"_method": "post", "_path": "/guests/{subjectId}/data-export"},
    "getSubjectDataExport": {"_method": "get", "_path": "/guests/{subjectId}/data-export/{requestId}"},
    "confirmThing": {"_method": "post", "_path": "/things/{thingId}/confirm"},
    "createWidget": {"_method": "post", "_path": "/widgets"},
}, {
    "exportSubjectData": ["requestId", "format"],
    "getSubjectDataExport": ["requestId", "status"],
    "confirmThing": ["thingId", "status"],
    "createWidget": ["@Widget"],
})


def screen(*ops):
    return {"id": "T-001", "apis": [{"operationId": o, "trigger": "onAction" if o != "getSubjectDataExport"
                                     else "onInterval"} for o in ops]}


def test_a_write_answering_the_id_makes_it_whatever_its_verb():
    assert SP.creates(PK, screen("exportSubjectData", "getSubjectDataExport"), "requestId") == "exportSubjectData"


def test_the_polled_id_is_optional_when_the_screen_makes_it():
    p = SP.param_for(PK, screen("exportSubjectData", "getSubjectDataExport"), "requestId")
    assert p.get("optional") is True and "exportSubjectData" in p["notes"]


def test_without_the_write_the_polled_id_stays_required():
    p = SP.param_for(PK, screen("getSubjectDataExport"), "requestId")
    assert not p.get("optional")


def test_a_write_that_takes_the_id_in_its_path_does_not_make_it():
    assert SP.creates(PK, screen("confirmThing"), "thingId") is None


def test_a_make_verb_still_makes_by_its_schema_name():
    assert SP.creates(PK, screen("createWidget"), "widgetId") == "createWidget"
