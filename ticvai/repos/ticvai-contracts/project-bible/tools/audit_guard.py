#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shared plumbing for the audit-class guards (plan item 1F, C12; docs/active/root-classes.md).

The 26 September pull audit found 293 root issues. Each belongs to a class of mistake, and a class
is closed only when something fails the next time it happens. The `check-*.py` guards written for
that read the package, never write it, and are **baseline-aware**: where a class still has members
today, the known ones are listed in `handoff/audit-baseline.json` and only a NEW member fails.

    python3 tools/check-<name>.py                    # exit 1 on a finding not in the baseline
    python3 tools/check-<name>.py --all              # list every finding, known ones too
    python3 tools/check-<name>.py --update-baseline  # record today's findings as known (an act,
                                                     # like --freeze: do it in a reviewed commit)

A baseline entry that no longer occurs is reported as `gone`, so the list only ever shrinks: run
`--update-baseline` after a fix to tighten it. Adding entries by hand to silence a new finding is
the thing this file exists to prevent; the commit that does it must say why.
"""
import datetime
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
BASELINE = ROOT / "handoff" / "audit-baseline.json"
CONTRACTS = ROOT / "contracts"
SCREENS = ROOT / "screens"
VERBS = ("get", "post", "put", "patch", "delete")

_CACHE: dict = {}


def load_yaml(path):
    """YAML with the C loader where it can; the pure loader where a file defeats it (surrogate
    escapes in subscription.yaml do)."""
    path = Path(path)
    key = str(path)
    if key in _CACHE:
        return _CACHE[key]
    text = path.read_text(encoding="utf-8")
    try:
        doc = yaml.load(text, Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader))
    except Exception:
        doc = yaml.load(text, Loader=yaml.SafeLoader)
    _CACHE[key] = doc
    return doc


def load_json(path, default=None):
    path = Path(path)
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def contract_files():
    return sorted(p for p in CONTRACTS.glob("*/*.yaml"))


def contracts():
    """[(stem, relpath, doc)] for every contract file."""
    out = []
    for f in contract_files():
        doc = load_yaml(f) or {}
        out.append((f.stem, f.relative_to(ROOT).as_posix(), doc))
    return out


def operations():
    """operationId -> {contract, file, method, path, op, item}."""
    key = "__ops__"
    if key in _CACHE:
        return _CACHE[key]
    out = {}
    for stem, rel, doc in contracts():
        for path, item in (doc.get("paths") or {}).items():
            if not isinstance(item, dict):
                continue
            for m in VERBS:
                op = item.get(m)
                if isinstance(op, dict) and op.get("operationId"):
                    out[op["operationId"]] = {"contract": stem, "file": rel, "method": m,
                                              "path": path, "op": op, "item": item}
    _CACHE[key] = out
    return out


def schemas():
    """(contract stem, schema name) -> schema dict, plus a name -> [stem] index."""
    key = "__schemas__"
    if key in _CACHE:
        return _CACHE[key]
    by = {}
    names: dict = {}
    for stem, rel, doc in contracts():
        for n, s in (((doc.get("components") or {}).get("schemas")) or {}).items():
            if isinstance(s, dict):
                by[(stem, n)] = s
                names.setdefault(n, []).append(stem)
    _CACHE[key] = (by, names)
    return by, names


def screens():
    """[(platform file stem, screen dict)] for every screen in screens/P*.yaml."""
    key = "__screens__"
    if key in _CACHE:
        return _CACHE[key]
    out = []
    for f in sorted(SCREENS.glob("P*.yaml")):
        doc = load_yaml(f) or {}
        for s in doc.get("screens") or []:
            if isinstance(s, dict) and s.get("id"):
                out.append((f.stem, s))
    _CACHE[key] = out
    return out


def platforms():
    out = {}
    for f in sorted(SCREENS.glob("P*.yaml")):
        doc = load_yaml(f) or {}
        out[f.stem] = doc.get("platform") or {}
    return out


def snake(name: str) -> str:
    s = re.sub(r"(?<=[a-z0-9])([A-Z])", r"_\1", str(name))
    s = re.sub(r"(?<=[A-Z])([A-Z][a-z])", r"_\1", s)
    return s.lower()


def ref_name(ref: str) -> str:
    return str(ref).rsplit("/", 1)[-1]


def head_commit() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True,
                              text=True).stdout.strip()
    except Exception:
        return ""


class Guard:
    """Collects findings by rule, compares them with the baseline, prints, and sets the exit code.

    A finding is (rule, key, message). The key is what the baseline stores, so it must be stable
    across runs: an id, never a line number.
    """

    def __init__(self, name: str, rules: dict):
        self.name = name
        self.rules = rules          # rule id -> one line: what it catches and the roots it closes
        self.found: dict = {r: {} for r in rules}
        self.notes: list = []
        args = sys.argv[1:]
        self.show_all = "--all" in args
        self.update = "--update-baseline" in args

    def add(self, rule: str, key: str, message: str):
        self.found.setdefault(rule, {})[str(key)] = message

    def note(self, text: str):
        self.notes.append(text)

    def _baseline(self) -> dict:
        data = load_json(BASELINE, {}) or {}
        return ((data.get(self.name) or {}).get("rules")) or {}

    def _write_baseline(self):
        data = load_json(BASELINE, {}) or {}
        data.setdefault("_about", (
            "Known members of the audit classes (docs/active/root-classes.md) still present when a "
            "guard was baselined. A guard fails only on a finding not listed here. Written by "
            "`python3 tools/check-<name>.py --update-baseline`; never add an entry by hand to "
            "silence a new finding."))
        data[self.name] = {
            "updated": datetime.date.today().isoformat(),
            "commit": head_commit(),
            "rules": {r: sorted(k) for r, k in sorted(self.found.items()) if k},
        }
        ordered = {"_about": data["_about"]}
        for k in sorted(k for k in data if k != "_about"):
            ordered[k] = data[k]
        BASELINE.write_text(json.dumps(ordered, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    def finish(self, limit: int = 12) -> int:
        base = self._baseline()
        total_new = 0
        total_known = 0
        gone_total = 0
        new_rules = []
        print(f"{self.name}: {len(self.rules)} rule(s)")
        for rule, desc in self.rules.items():
            cur = self.found.get(rule) or {}
            known = set(base.get(rule) or [])
            new = sorted(k for k in cur if k not in known)
            gone = sorted(k for k in known if k not in cur)
            total_new += len(new)
            total_known += len(cur) - len(new)
            gone_total += len(gone)
            mark = "FAIL" if new else "ok  "
            print(f"  {mark} {rule:<22} {len(cur):>5} found, {len(new):>4} new, "
                  f"{len(gone):>4} gone  - {desc}")
            if new:
                new_rules.append(rule)
            shown = sorted(cur) if self.show_all else new
            for k in shown[:limit if not self.show_all else None]:
                tag = "NEW " if k in new else "    "
                print(f"       {tag}{cur[k]}")
            if not self.show_all and len(new) > limit:
                print(f"       ... and {len(new) - limit} more new (--all lists every one)")
        for n in self.notes:
            print(f"  note: {n}")
        if self.update:
            self._write_baseline()
            print(f"baseline written: {sum(len(v) for v in self.found.values())} known finding(s) "
                  f"in {BASELINE.relative_to(ROOT).as_posix()}")
            return 0
        tail = (f"; {gone_total} baseline entr{'y' if gone_total == 1 else 'ies'} gone - run "
                f"--update-baseline to tighten") if gone_total else ""
        if total_new:
            print(f"FAIL - {total_new} new finding(s) in {', '.join(new_rules)}; "
                  f"{total_known} known{tail}")
            return 1
        print(f"PASS - 0 new, {total_known} known (baseline){tail}")
        return 0


def force_utf8():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
