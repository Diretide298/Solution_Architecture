"""The rehearsal kit's self-tests (tools/rehearse/), for pytest. Each module also runs its own first, every time.

    python -m pytest ticvai/tools/tests/test_rehearse.py -q
"""
import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

KIT = Path(__file__).resolve().parents[1] / "rehearse"
sys.path.insert(0, str(KIT))


def load(name):
    spec = importlib.util.spec_from_file_location(f"rehearse_{name}", KIT / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_judge_self_tests():
    assert load("judge").self_test() == []


def test_simulate_self_tests():
    assert load("simulate").self_test() == []


def test_prepare_self_tests():
    assert load("prepare").self_test() == []
