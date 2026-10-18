"""Tests for the ticket status adam-links.py caches for the gate (post-r6 plan item 9, CHG-CRF-001).

    python -m pytest ticvai/tools/tests/test_adam_links_status.py -q

The started-ticket rule (tools/audit_guard.py) reads ticket status offline from adam-links.json. These check that the
status carries when it was read, that a run without TICVAI_OP_TOKEN keeps the last statuses instead of dropping
them, and that --status-only rereads them without touching the links, and never writes on a failed read. No network:
snapshot() is replaced.
"""
import importlib.util
import json
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("adam_links", TOOLS / "adam-links.py")
al = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(al)


def row(wp, kind="table", ident="marketing.consent_record", status="New"):
    r = {"key": str(wp), "kind": kind, "id": ident, "url": f"https://pms.example/work_packages/{wp}"}
    if status:
        r.update({"subject": f"ticket {wp}", "status": status, "type": "Task", "assignee": "Pranay Shinde"})
    return r


def doc(*rows, read_at="2026-10-15T06:00:00Z"):
    return {"project": "ticvai", "openproject": "https://pms.example", "cached": True, "statusReadAt": read_at,
            "links": list(rows)}


def test_carried_status_reads_the_last_files_columns():
    snap, read_at = al.carried_status(doc(row(1), row(1, "operation", "identity#login"), row(2, status="")))
    assert snap == {1: {"subject": "ticket 1", "status": "New", "type": "Task", "assignee": "Pranay Shinde"}}
    assert read_at == "2026-10-15T06:00:00Z"
    assert al.carried_status({}) == ({}, "")


def test_status_source_reads_openproject_with_a_token(monkeypatch):
    monkeypatch.setattr(al, "snapshot", lambda token: {1: {"status": "In progress"}})
    monkeypatch.setattr(al, "_now", lambda: "2026-10-18T09:00:00Z")
    assert al.status_source("t", doc(row(1))) == ({1: {"status": "In progress"}}, "2026-10-18T09:00:00Z",
                                                  "read from OpenProject")


def test_status_source_carries_without_a_token(monkeypatch):
    monkeypatch.setattr(al, "snapshot", lambda token: (_ for _ in ()).throw(AssertionError("no read without a token")))
    snap, read_at, how = al.status_source("", doc(row(1)))
    assert snap[1]["status"] == "New" and read_at == "2026-10-15T06:00:00Z" and how.startswith("carried")
    assert al.status_source("", {}) == ({}, "", "none (no TICVAI_OP_TOKEN and no earlier file)")


def test_restatus_changes_the_columns_only():
    before = doc(row(1), row(2, "operation", "identity#login"))
    after = al.restatus(before, {1: {"subject": "s", "status": "Ready for QA", "type": "Task", "assignee": "A"}},
                        "2026-10-18T09:00:00Z")
    assert after["statusReadAt"] == "2026-10-18T09:00:00Z" and after["cached"] is True
    assert [(r["key"], r["kind"], r["id"]) for r in after["links"]] == [(r["key"], r["kind"], r["id"])
                                                                       for r in before["links"]]
    assert after["links"][0]["status"] == "Ready for QA" and "status" not in after["links"][1]
    assert al.restatus(before, {}, "x")["cached"] is False


def test_status_only_needs_the_token(monkeypatch, tmp_path, capsys):
    monkeypatch.delenv("TICVAI_OP_TOKEN", raising=False)
    monkeypatch.setattr(al, "DOCS", tmp_path)
    assert al.status_only() == 2
    assert "TICVAI_OP_TOKEN is not set" in capsys.readouterr().out
    assert not (tmp_path / "adam-links.json").exists()


def test_status_only_keeps_the_file_when_openproject_is_down(monkeypatch, tmp_path, capsys):
    monkeypatch.setenv("TICVAI_OP_TOKEN", "t")
    monkeypatch.setattr(al, "DOCS", tmp_path)
    (tmp_path / "adam-links.json").write_text(json.dumps(doc(row(1))), encoding="utf-8")
    was = (tmp_path / "adam-links.json").read_text(encoding="utf-8")

    def down(token):
        raise OSError("timed out")

    monkeypatch.setattr(al, "snapshot", down)
    assert al.status_only() == 2
    assert "OpenProject could not be read (OSError: timed out)" in capsys.readouterr().out
    assert (tmp_path / "adam-links.json").read_text(encoding="utf-8") == was
    monkeypatch.setattr(al, "snapshot", lambda token: {})
    assert al.status_only() == 2
    assert (tmp_path / "adam-links.json").read_text(encoding="utf-8") == was


def test_status_only_rewrites_statuses(monkeypatch, tmp_path, capsys):
    monkeypatch.setenv("TICVAI_OP_TOKEN", "t")
    monkeypatch.setattr(al, "DOCS", tmp_path)
    monkeypatch.setattr(al, "_now", lambda: "2026-10-18T09:00:00Z")
    (tmp_path / "adam-links.json").write_text(json.dumps(doc(row(1), row(2))), encoding="utf-8")
    monkeypatch.setattr(al, "snapshot", lambda token: {
        1: {"subject": "ticket 1", "status": "In progress", "type": "Task", "assignee": "Pranay Shinde"},
        2: {"subject": "ticket 2", "status": "New", "type": "Task", "assignee": "Pranay Shinde"}})
    assert al.status_only() == 0
    got = json.loads((tmp_path / "adam-links.json").read_text(encoding="utf-8"))
    assert got["statusReadAt"] == "2026-10-18T09:00:00Z"
    assert [r["status"] for r in got["links"]] == ["In progress", "New"]
    assert "1 of 2 link rows changed status" in capsys.readouterr().out
