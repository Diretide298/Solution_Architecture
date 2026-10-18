#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The scripts that run inside OpenProject's container use only what its Ruby has: 2.6, on OpenProject 10.0.2.

**15 October 2026** (tracker F43, CHG-REL-008). A fix script for the r6 release used `Array#tally`, which came
in Ruby 2.7; `rails runner` stopped on it with NoMethodError on the server. The scripts are only ever run there,
so nothing on a workstation catches it. This reads `tools/*.rb` for what Ruby 2.6 does not have:

    RB-NEWER   a method or syntax newer than Ruby 2.6: tally, filter_map, numbered block parameters (_1),
               endless methods (def x = ...), Array#intersect?, hash shorthand ({ a:, b: })

Rails 5.2's ActiveSupport additions (Hash#except, Array#excluding, Object#presence) are there and are not flagged.
Comments and string literals are skipped. Strict: never baselined.

Read-only. Exit 1 on a finding not in `handoff/audit-baseline.json` (tools/audit_guard.py).

    python3 tools/check-ruby-compat.py [--all]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {
    "RB-NEWER": "a script run in OpenProject's container (Ruby 2.6) uses nothing newer than Ruby 2.6 (tracker F43, CHG-REL-008)",
}

NEWER = [
    (re.compile(r"\.tally\b"), "Enumerable#tally (Ruby 2.7)"),
    (re.compile(r"\.filter_map\b"), "Enumerable#filter_map (Ruby 2.7)"),
    (re.compile(r"\.intersect\?"), "Array#intersect? (Ruby 3.1)"),
    (re.compile(r"(?<![\w@$])_[1-9]\b"), "a numbered block parameter (Ruby 2.7)"),
    (re.compile(r"^\s*def\s+[\w?!]+(\([^)]*\))?\s*=\s*\S"), "an endless method (Ruby 3.0)"),
    (re.compile(r"[{,(]\s*\w+:\s*(?=[,})])"), "hash shorthand { a: } (Ruby 3.1)"),
]


def code_only(line: str) -> str:
    """The line without its comment and string contents (a rough lexer: enough for these patterns)."""
    out, quote, i = [], None, 0
    while i < len(line):
        c = line[i]
        if quote:
            if c == "\\":
                i += 2
                continue
            if c == quote:
                quote = None
                out.append(c)
        elif c in "\"'":
            quote = c
            out.append(c)
        elif c == "#":
            break
        else:
            out.append(c)
        i += 1
    return "".join(out)


def findings(text: str) -> list:
    found = []
    for n, line in enumerate(text.splitlines(), 1):
        code = code_only(line)
        for rx, what in NEWER:
            if rx.search(code):
                found.append((n, what, line.strip()[:100]))
    return found


def self_test() -> list:
    fails = []
    bad = "x = list.tally\ny = list.filter_map { |v| v }\nz = list.map { _1 * 2 }\ndef twice(x) = x * 2\nh = { a:, b: }\n"
    if len(findings(bad)) != 5:
        fails.append(f"RB-NEWER found {len(findings(bad))} of 5 in the known-bad sample: {findings(bad)}")
    good = ("# tally is newer than 2.6\nputs \"tally: #{n}\"\nh = { a: 1, b: 2 }\nlist.group_by { |w| w }.map { |k, v| [k, v.size] }\n"
            "x = a ? b : c\nputs \"#{w.id}: #{a}\"\ndef ok(x)\n  x\nend\n")
    if findings(good):
        fails.append(f"RB-NEWER flagged Ruby 2.6 code: {findings(good)}")
    return fails


def main() -> int:
    guard = g.Guard("check-ruby-compat", RULES)
    fails = self_test()
    if fails:
        for f in fails:
            print(f"  self-test: {f}")
        return 2
    scripts = sorted((g.ROOT / "tools").glob("*.rb"))
    for path in scripts:
        for n, what, line in findings(path.read_text(encoding="utf-8", errors="replace")):
            guard.add("RB-NEWER", f"tools/{path.name}:{n}:{what}", f"tools/{path.name}:{n}: {what}: {line}")
    guard.note(f"{len(scripts)} scripts read; the self-tests pass")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
