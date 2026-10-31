"""Tests for tools/check-schema-drift.py (CHG-R12LV-001): the self-test's fixture snapshots, one per bucket and
lesson of the 30 October live check, and the package inputs the tool judges by. No Docker.

    python -m pytest ticvai/tools/tests/test_check_schema_drift.py -q
"""
import importlib.util
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("schema_drift", TOOLS / "check-schema-drift.py")
sd = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sd)


def test_self_test():
    assert sd.self_test() == []


def test_package_inputs_parse():
    fails, rows, tasks, _adjusted = sd.check_package()
    assert fails == [] and rows > 0 and tasks > 0
