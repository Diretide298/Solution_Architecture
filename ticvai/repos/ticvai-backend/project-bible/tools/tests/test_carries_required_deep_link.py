"""A required deep-link id is not a pre-select (r13 root R18, CHG-R13R18-001).

    python -m pytest ticvai/tools/tests/test_carries_required_deep_link.py -q

derive-carries-from-entrystate.py why_nothing() read every `from: deepLink` param as optional, so a menu edge into a
screen whose id is required said "only pre-selects ... opens on its own" (#28213 BO-103 -> BO-094, mapId). Only an
optional param pre-selects; a required one is found by the screen itself, read off a list it opens on, or the edge is
cold.
"""
import importlib.util
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("carries_r18", TOOLS / "derive-carries-from-entrystate.py")
dc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dc)


def screens(params):
    return {"A-001": {"id": "A-001", "name": "Menu", "module": "M", "navigation": {}},
            "A-002": {"id": "A-002", "name": "Editor", "module": "M", "entryState": {"params": params}}}


def run(params, finds=None, opens_on=None, monkeypatch=None):
    monkeypatch.setattr(dc, "reads_itself", lambda d, name, c: (finds or {}).get(name))
    monkeypatch.setattr(dc, "opening_list", lambda d, given, c: opens_on)
    return dc.why_nothing("A-001", "A-002", screens(params), None)


def test_optional_deep_link_pre_selects(monkeypatch):
    kind, why = run([{"name": "pathId", "from": "deepLink", "optional": True}], monkeypatch=monkeypatch)
    assert kind == "deepLink" and "pathId only pre-selects (optional)" in why


def test_required_deep_link_is_cold(monkeypatch):
    kind, why = run([{"name": "mapId", "from": "deepLink"}], monkeypatch=monkeypatch)
    assert kind == "cold" and "pre-select" not in why


def test_required_deep_link_on_a_list_is_a_gap_in_the_screen(monkeypatch):
    kind, why = run([{"name": "mapId", "from": "deepLink"}], opens_on="searchMedia", monkeypatch=monkeypatch)
    assert kind == "list" and "mapId has no source on A-002 yet" in why and "pre-select" not in why


def test_required_deep_link_the_screen_finds_itself(monkeypatch):
    kind, why = run([{"name": "performanceId", "from": "deepLink"}], finds={"performanceId": "listPerformances"},
                    monkeypatch=monkeypatch)
    assert kind == "self" and "finds performanceId (listPerformances) itself" in why
