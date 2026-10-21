"""The look of every state of a client-verified screen, and the ticket text that names it (CHG-R9UI-003, CHG-R9UI-004).

    python -m pytest ticvai/tools/tests/test_state_views.py -q

The synthetic tests run tools/check-state-views.py's rules on a made-up screen and mapping; the last ones read the
real package (screens/_state-patterns.yaml, docs/active/left-out.yaml, handoff/design-frames.json).
"""
import copy
import importlib.util
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

import audit_guard as g  # noqa: E402
import ticket_done as td  # noqa: E402


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, TOOLS / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


csv_ = load("check_state_views", "check-state-views.py")

PROTO = "sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html"
MAPPING = {"platforms": {"P01": {
    "prototypes": {"web": PROTO}, "board": "wireframes/P01 Guest Web.dc.html",
    "patterns": {"status-card": {"name": "the status card", "prototype": "web", "find": ["Something went wrong on our side"],
                                 "frame": "web-029"},
                 "turnstile-loader": {"name": "the turnstile loader", "prototype": "web", "find": ["TURNSTILE LOADER"]}},
    "states": {"error": "status-card", "loading": "turnstile-loader"}}}}
SCREEN = {"id": "WEB-900", "states": {"loading": "x", "error": "y", "offline": "z"},
          "wireframe": {"provenance": "client-verified",
                        "stateViews": {"loading": "P01/turnstile-loader", "error": "P01/status-card"}}}
GAP = {"id": "LO-T-001", "kind": "design-gap", "platform": "P01", "states": ["offline"], "what": "w", "source": "s",
       "reason": "r", "target": "t", "added": "2026-10-21", "change": "CHG-R9UI-003"}


def run(screens, mapping, items):
    gd = g.Guard("check-state-views (test)", csv_.RULES)
    csv_.run(gd, screens, mapping, items, None)
    return {r: set(v) for r, v in gd.found.items() if v}


def test_a_state_with_no_view_and_no_left_out_line_fails():
    assert run([("P01", SCREEN)], MAPPING, []) == {"SV-NO-VIEW": {"WEB-900:offline"}}


def test_a_listed_design_gap_passes():
    assert run([("P01", SCREEN)], MAPPING, [GAP]) == {}


def test_stale_views_and_an_invented_pattern_fail():
    s = copy.deepcopy(SCREEN)
    s["wireframe"]["stateViews"].pop("error")
    m = copy.deepcopy(MAPPING)
    m["platforms"]["P01"]["patterns"]["turnstile-loader"]["find"] = ["a text the prototype does not hold"]
    found = run([("P01", s)], m, [GAP])
    assert found["SV-STALE"] == {"WEB-900"}
    assert any(k.startswith("P01/turnstile-loader:") for k in found["SV-PATTERN"])


def test_a_closed_gap_and_a_bad_left_out_item_fail():
    s = copy.deepcopy(SCREEN)
    s["states"].pop("offline")
    bad = dict(GAP, id="LO-T-002", reason="")
    found = run([("P01", s)], MAPPING, [GAP, bad])
    assert "LO-T-001:offline" in found["SV-LEFT-OUT"] and "LO-T-002:fields" in found["SV-LEFT-OUT"]


def test_the_probe_fails_on_the_real_package_and_the_tree_passes():
    assert csv_.probe() == 0


def test_web_007_names_its_design_and_each_state_look():
    text = td.design_sentence("WEB-007")
    assert text.startswith(td.DESIGN_HEAD)
    assert "wireframe-web-007.html" in text and "the status card of WEB-029" in text and "turnstile loader" in text
    assert "Choose ... to see the seats" in text
    assert "structure only, not the look" in text


def test_the_build_done_when_is_the_visual_check_only_where_a_design_is_approved():
    fe = {"type": "Task", "track": "Frontend", "key": "APP-WEB-WEB-007", "description": ""}
    approved = td.done_when(fe, "build", ["screen WEB-007"])
    assert "the visual check passes for every state" in approved and "1440×900 and 390×844" in approved
    unapproved = td.done_when(dict(fe, key="VM-BO-085"), "build", ["screen BO-085"])
    assert "visual check" not in unapproved and "structure only" in unapproved
    assert td.state_look("GST-003", "offline").startswith("look: not drawn by the approved design (LO-R9UI-")
