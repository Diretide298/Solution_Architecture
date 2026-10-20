#!/usr/bin/env python3
"""No authored YAML file may name the same key twice in one mapping.

**20 October 2026 (r8 integration, CHG-R8INT-001).** A YAML loader keeps the last of two equal keys and
drops the first without a word. Two had reached the contracts and no checker saw them:

  retail.yaml      a second `GuestMerchandiseItem` schema (the guest projection of `PriceCheck`, added by
                   the r8 walk for `lookupMerchandise`) replaced the guest projection of `MerchandiseItem`
                   that `listMerchandise` returns, so every generator read the wrong shape for that list.
  tenancy.yaml     `DeviceBinding` carried two `description` keys (ADAM CR-095 and CR-155); the CR-095
                   sentence that a binding moves the device row to the workstation's scope was lost.

Every tool in this package reads YAML with `yaml.safe_load`, so the duplicate is invisible downstream: the
derived DDL, the tickets and the screens all see one key. Only a loader that looks at the mapping before it
is built can see two. This one does, over every authored YAML file git tracks under the folders below.

    python3 tools/check-yaml-keys.py            # fail on any duplicate key
    python3 tools/check-yaml-keys.py --self-test

It proves itself first: a mapping with a repeated key must be reported and one without must pass.
"""
import argparse
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

# The authored inputs (CLAUDE.md rule 1) that are YAML, plus the plan inputs kept as YAML in docs/active.
AUTHORED = ["contracts", "screens", "flows", "states", "events", "changes/entries", "docs/active",
            "docs/registers", "design-notes", "roles.yaml"]


_BASE = getattr(yaml, "CSafeLoader", yaml.SafeLoader)   # the C parser where libyaml is installed: 2 min -> seconds


class _Loader(_BASE):
    """SafeLoader that records every mapping key seen twice, with its line."""


def _mapping(loader, node, deep=False):
    seen = {}
    for key_node, _ in node.value:
        key = loader.construct_object(key_node, deep=True)
        try:
            hash(key)
        except TypeError:
            continue
        if key in seen:
            loader.duplicates.append((key, seen[key], key_node.start_mark.line + 1))
        else:
            seen[key] = key_node.start_mark.line + 1
    return _BASE.construct_mapping(loader, node, deep=True)


_Loader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)


def duplicates(text):
    """Every (key, first line, repeated line) in a YAML document stream."""
    loader = _Loader(text)
    loader.duplicates = []
    try:
        while loader.check_data():
            loader.get_data()
    finally:
        loader.dispose()
    return loader.duplicates


def self_test():
    bad = "a:\n  b: 1\n  c: 2\n  b: 3\n"
    good = "a:\n  b: 1\n  c: 2\nd:\n  b: 3\n"
    got = duplicates(bad)
    assert got == [("b", 2, 4)], got
    assert duplicates(good) == [], duplicates(good)
    assert duplicates("---\nx: 1\n---\nx: 1\n") == []
    return 3


def authored_files():
    out = subprocess.run(["git", "-C", str(ROOT), "ls-files", "-z", "--", *AUTHORED],
                         capture_output=True, check=True).stdout.decode("utf-8")
    return [p for p in out.split("\0") if p.endswith((".yaml", ".yml"))]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    n = self_test()
    if args.self_test:
        print("check-yaml-keys: %d self-tests pass" % n)
        return 0
    findings = []
    files = authored_files()
    for rel in files:
        try:
            text = (ROOT / rel).read_text(encoding="utf-8")
            for key, first, again in duplicates(text):
                findings.append("%s:%d: key %r repeats the one at line %d" % (rel, again, key, first))
        except yaml.YAMLError as e:
            findings.append("%s: not valid YAML: %s" % (rel, str(e).splitlines()[0]))
    for f in findings:
        print("ERROR " + f)
    print("check-yaml-keys: %d file(s), %d self-tests pass, %d duplicate key(s)%s"
          % (len(files), n, len(findings), "" if findings else ": pass"))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
