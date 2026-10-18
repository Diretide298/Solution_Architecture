"""Tests for the started-ticket rule in tools/audit_guard.py (post-r6 plan item 9, CHG-CRF-001).

    python -m pytest ticvai/tools/tests/test_audit_guard_started.py -q

A baselined finding fails once a ticket that builds its operation or table has started (a status other than New, On
hold or Rejected, on a task or sub-task), read offline from the cached columns of adam-links.json. The synthetic
tests wire a baseline and a links file in a temporary folder into audit_guard; the last test reads the real package.
"""
import json
import sys
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
import audit_guard as g  # noqa: E402

KEY = "exportSubjectData:marketing.consent_record"


def link(wp, kind, ident, status="New", typ="Task", who="Pranay Shinde"):
    return {"key": str(wp), "kind": kind, "id": ident, "url": f"https://pms.example/work_packages/{wp}",
            "subject": f"ticket {wp}", "status": status, "type": typ, "assignee": who}


@pytest.fixture
def pkg(tmp_path, monkeypatch):
    base, links = tmp_path / "audit-baseline.json", tmp_path / "adam-links.json"
    monkeypatch.setattr(g, "BASELINE", base)
    monkeypatch.setattr(g, "LINKS", links)
    g._CACHE.clear()

    def write(baseline=None, rows=None, cached=True, read_at="2026-10-18T09:00:00Z"):
        if baseline is not None:
            base.write_text(json.dumps(baseline), encoding="utf-8")
        if rows is not None:
            links.write_text(json.dumps({"project": "ticvai", "cached": cached, "statusReadAt": read_at,
                                         "links": rows}), encoding="utf-8")
        g._CACHE.clear()

    yield write, base
    g._CACHE.clear()


def run(monkeypatch, findings, *argv):
    monkeypatch.setattr(sys, "argv", ["check-x.py", *argv])
    guard = g.Guard("check-x", {"R-A": "a rule", "R-B": "another rule"})
    for rule, key in findings:
        guard.add(rule, key, f"{rule} {key}")
    g._CACHE.clear()
    return guard.finish()


def last_line(out):
    return [x for x in out.splitlines() if x.strip()][-1]


def test_index_names_operations_and_tables(pkg):
    write, _ = pkg
    write(rows=[link(1, "operation", "identity#exportSubjectData"), link(2, "table", "marketing.consent_record"),
                link(3, "operation", "incident#addIncidentPerson"), link(4, "table", "pii.subject"),
                link(5, "screen", "BO-001"), link(6, "operation", "orders#linkGuestCheckout")])
    idx = g.link_index()
    assert idx["cached"] and idx["exists"] and idx["readAt"] == "2026-10-18T09:00:00Z"
    assert g.finding_artefacts(KEY, idx) == {("operation", "identity#exportSubjectData"),
                                             ("table", "marketing.consent_record")}
    assert g.finding_artefacts("addIncidentPerson.pii.subject", idx) == {("operation", "incident#addIncidentPerson"),
                                                                        ("table", "pii.subject")}
    assert g.finding_artefacts("linkGuestCheckout|403", idx) == {("operation", "orders#linkGuestCheckout")}
    assert g.finding_artefacts("identity#exportSubjectData", idx) == {("operation", "identity#exportSubjectData")}
    assert g.finding_artefacts("BO-001:Export", idx) == set()            # screens are not judged
    assert g.finding_artefacts("access.AccessArea.colour", idx) == set()  # a schema field names no ticket's work
    assert idx["wps"][5]["status"] == "New"


def test_started_means_off_new_hold_rejected_on_the_work(pkg):
    write, _ = pkg
    t = ("table", "marketing.consent_record")
    write(rows=[link(1, *t, status="New"), link(2, *t, status="On hold"), link(3, *t, status="Rejected"),
                link(4, *t, status="In progress", typ="Feature"), link(5, *t, status="In progress", typ="Epic"),
                link(6, *t, status="Ready for QA"), link(7, *t, status="Closed", typ="Sub Task"),
                link(6, *t, status="Ready for QA")])
    got = g.started_tickets({t}, g.link_index())
    assert [x["wp"] for x in got] == [6, 7]
    assert got[0]["on"] == "table marketing.consent_record"


def test_known_finding_on_a_started_ticket_fails(pkg, monkeypatch, capsys):
    write, _ = pkg
    write(baseline={"check-x": {"rules": {"R-A": [KEY]}}},
          rows=[link(27677, "table", "marketing.consent_record", status="Ready for QA", who="Hrushikant Patkar")])
    assert run(monkeypatch, [("R-A", KEY)]) == 1
    out = capsys.readouterr().out
    assert "1 built on" in out
    assert "BUILT R-A " + KEY + " -- started: #27677 Ready for QA (Hrushikant Patkar)" in out
    assert last_line(out).startswith("FAIL - 1 known finding(s) built on by a started ticket in R-A")


def test_known_finding_on_new_tickets_passes(pkg, monkeypatch, capsys):
    write, _ = pkg
    write(baseline={"check-x": {"rules": {"R-A": [KEY]}}}, rows=[link(27677, "table", "marketing.consent_record")])
    assert run(monkeypatch, [("R-A", KEY)]) == 0
    assert last_line(capsys.readouterr().out) == "PASS - 0 new, 1 known (baseline)"


def test_new_finding_message_is_unchanged(pkg, monkeypatch, capsys):
    write, _ = pkg
    write(baseline={}, rows=[])
    assert run(monkeypatch, [("R-A", "opX")]) == 1
    assert last_line(capsys.readouterr().out) == "FAIL - 1 new finding(s) in R-A; 0 known"


def test_acknowledge_needs_a_request_or_change(pkg, monkeypatch, capsys):
    write, base = pkg
    write(baseline={"check-x": {"rules": {"R-A": [KEY]}}},
          rows=[link(27677, "table", "marketing.consent_record", status="Ready for QA")])
    assert run(monkeypatch, [("R-A", KEY)], "--acknowledge-started=because it is fine") == 1
    assert "started" not in json.loads(base.read_text(encoding="utf-8"))["check-x"]


def test_acknowledge_may_cite_a_tracker_row_instead_of_a_request(pkg, monkeypatch, capsys):
    write, base = pkg
    write(baseline={"check-x": {"rules": {"R-A": [KEY]}}},
          rows=[link(27677, "table", "marketing.consent_record", status="Ready for QA")])
    assert run(monkeypatch, [("R-A", KEY)], "--acknowledge-started", "F14: tracked on the follow-ups sheet") == 0
    ack = json.loads(base.read_text(encoding="utf-8"))["check-x"]["started"]["R-A|" + KEY]
    assert ack["why"].startswith("F14") and ack["tickets"] == [27677]
    # a bare word that only looks like a row is not a reason
    assert run(monkeypatch, [("R-A", KEY)], "--acknowledge-started", "Fix later, see FAQ") == 1


def test_acknowledged_tickets_pass_and_a_new_one_fails(pkg, monkeypatch, capsys):
    write, base = pkg
    rows = [link(27677, "table", "marketing.consent_record", status="Ready for QA")]
    write(baseline={"check-x": {"rules": {"R-A": [KEY]}}}, rows=rows)
    assert run(monkeypatch, [("R-A", KEY)], "--acknowledge-started", "CR-108: the row security fix reworks it") == 0
    ack = json.loads(base.read_text(encoding="utf-8"))["check-x"]["started"]["R-A|" + KEY]
    assert ack["tickets"] == [27677] and ack["why"].startswith("CR-108")
    assert json.loads(base.read_text(encoding="utf-8"))["check-x"]["rules"] == {"R-A": [KEY]}
    capsys.readouterr()
    assert run(monkeypatch, [("R-A", KEY)]) == 0
    assert "1 known finding(s) on started tickets acknowledged" in capsys.readouterr().out
    write(rows=rows + [link(30526, "table", "marketing.consent_record", status="In progress", typ="Sub Task")])
    assert run(monkeypatch, [("R-A", KEY)]) == 1
    out = capsys.readouterr().out
    assert "started: #30526 In progress" in out and "#27677" not in out


def test_update_baseline_keeps_acknowledgements_of_found_findings_only(pkg, monkeypatch, capsys):
    write, base = pkg
    write(baseline={"check-x": {"rules": {"R-A": [KEY, "opGone"]},
                                "started": {"R-A|" + KEY: {"tickets": [1], "why": "CR-1", "on": "2026-10-18"},
                                            "R-A|opGone": {"tickets": [2], "why": "CR-2", "on": "2026-10-18"}}}},
          rows=[])
    assert run(monkeypatch, [("R-A", KEY)], "--update-baseline") == 0
    entry = json.loads(base.read_text(encoding="utf-8"))["check-x"]
    assert entry["rules"] == {"R-A": [KEY]}
    assert list(entry["started"]) == ["R-A|" + KEY]


def test_uncached_status_is_said_not_judged(pkg, monkeypatch, capsys):
    write, _ = pkg
    write(baseline={"check-x": {"rules": {"R-A": [KEY]}}},
          rows=[link(27677, "table", "marketing.consent_record", status="Ready for QA")], cached=False)
    assert run(monkeypatch, [("R-A", KEY)]) == 0
    assert "ticket status is not cached" in capsys.readouterr().out


def test_missing_links_file_is_said_not_judged(pkg, monkeypatch, capsys):
    write, _ = pkg
    write(baseline={"check-x": {"rules": {"R-A": [KEY]}}})
    assert run(monkeypatch, [("R-A", KEY)]) == 0
    assert "ticket status is not cached" in capsys.readouterr().out


def test_real_package_links_resolve_a_baselined_key():
    path = g.ROOT / "handoff" / "service-docs" / "adam-links.json"
    if not path.exists():
        pytest.skip("no adam-links.json in this checkout")
    g._CACHE.clear()
    idx = g.link_index(path)
    got = g.finding_artefacts(KEY, idx)
    assert ("table", "marketing.consent_record") in got
    assert any(kind == "operation" and ident.endswith("#exportSubjectData") for kind, ident in got)
