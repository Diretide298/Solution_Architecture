"""derive-id-register keeps `updated` when nothing else changed (CHG-LCR-002).

    python -m pytest ticvai/tools/tests/test_derive_id_register.py -q
"""
import importlib.util
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("derive_id_register", TOOLS / "derive-id-register.py")
reg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(reg)


def test_second_run_leaves_the_file_byte_identical(tmp_path, monkeypatch):
    out = tmp_path / "_id-register.yaml"
    r = {"ADM": {1: "authored", 2: "authored"}}
    monkeypatch.setattr(reg.datetime, "date", type("D", (), {"today": staticmethod(lambda: "2026-01-01")}))
    reg.write_register(reg.build(r), out)
    first = out.read_bytes()
    monkeypatch.setattr(reg.datetime, "date", type("D", (), {"today": staticmethod(lambda: "2026-02-02")}))
    reg.write_register(reg.build(r), out)
    assert out.read_bytes() == first
    assert b"2026-01-01" in first


def test_a_new_id_changes_content_and_date(tmp_path, monkeypatch):
    out = tmp_path / "_id-register.yaml"
    monkeypatch.setattr(reg.datetime, "date", type("D", (), {"today": staticmethod(lambda: "2026-01-01")}))
    reg.write_register(reg.build({"ADM": {1: "authored"}}), out)
    monkeypatch.setattr(reg.datetime, "date", type("D", (), {"today": staticmethod(lambda: "2026-02-02")}))
    reg.write_register(reg.build({"ADM": {1: "authored", 2: "authored"}}), out)
    text = out.read_text(encoding="utf-8")
    assert "2026-02-02" in text and "highWaterMark: 2" in text
