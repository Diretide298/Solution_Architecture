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


@pytest.mark.skipif(shutil.which("node") is None, reason="node is not installed")
def test_stand_in_self_tests():
    r = subprocess.run(["node", str(KIT / "stand-in-openproject.mjs"), "--self-test"], capture_output=True, text=True,
                       timeout=120)
    assert r.returncode == 0, r.stdout + r.stderr


def _bash():
    exe = os.environ.get("BASH_EXE") or shutil.which("bash")
    return None if not exe or "system32" in exe.lower() else exe   # WSL's bash cannot read this path


@pytest.mark.skipif(_bash() is None, reason="no Git Bash or Linux bash")
@pytest.mark.parametrize("args,env,said", [
    (["r7"], {}, "the first argument is r<N>-rc"),
    (["r7-rc", "--base", "nowhere", "--ports", "8787,8986,4374"], {}, "port 8787 belongs to another session"),
    (["r7-rc", "--ports", "8996,8986,4374"], {}, "--base is the last live pull"),
    (["live-repull", "r7", "--rehearsal", "nowhere", "--created", "nowhere"],
     {"ADAM_URL": "", "ADAM_EMAIL": "", "ADAM_PASSWORD": ""}, "set ADAM_URL, ADAM_EMAIL and ADAM_PASSWORD"),
    (["live-repull", "r7", "--rehearsal", "nowhere", "--created", "nowhere"],
     {"ADAM_URL": "http://127.0.0.1:4173", "ADAM_EMAIL": "a@b.c", "ADAM_PASSWORD": "x"}, "port 4173"),
])
def test_rehearse_refuses(args, env, said):
    r = subprocess.run([_bash(), str(KIT / "rehearse.sh"), *args], capture_output=True, text=True,
                       env={**os.environ, **env}, timeout=120)
    assert r.returncode == 2, r.stdout + r.stderr
    assert said in r.stderr, r.stderr
