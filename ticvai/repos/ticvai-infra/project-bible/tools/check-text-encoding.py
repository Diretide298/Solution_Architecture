#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every tool names the encoding of the text it reads and writes (r14, review E-10, CHG-R14I-006).

**Why.** `tools/build-cluster-index.py` read its two JSON inputs with a bare `.read_text()` and wrote UTF-8. On
Windows a bare read is the locale's encoding (cp1252), so the em dashes in the backlog came back as `â€”`:
docs/registers/clusters.md was committed with 26 mojibake sequences, and the same refresh on Linux wrote the right
character, so the derived file depended on the machine. cp1252 also has undefined bytes (0x81, 0x8D, 0x90) that occur
in Arabic UTF-8, so Arabic text in an input would have crashed the builder on Windows. check-migrations read the
backend SQL the same way. refresh.sh, refresh-safe.sh and run-checks.py now set PYTHONUTF8=1, and this check keeps
the tools from depending on it.

Fails on any call in tools/*.py (the tools refresh.sh and run-checks.py run) that opens text without `encoding=`:

    open(...)  io.open(...)  codecs.open(...)   in a text mode (no `b` in the mode)
    <path>.read_text(...)  <path>.write_text(...)
    <path>.open("r"|"w"|"a"|"rt"|"wt"|"at"|"r+"|"w+" ...)   a text mode given as a literal

    python3 tools/check-text-encoding.py
"""
import ast
import glob
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXT_MODES = {"r", "w", "a", "x", "rt", "wt", "at", "xt", "r+", "w+", "a+", "rt+", "wt+"}


def _mode(call, pos):
    if len(call.args) > pos and isinstance(call.args[pos], ast.Constant):
        return call.args[pos].value
    for k in call.keywords:
        if k.arg == "mode":
            return k.value.value if isinstance(k.value, ast.Constant) else "?"
    return None


def findings(src, name="<src>"):
    """[(line, text)] for every text open without an encoding in `src`."""
    out = []
    tree = ast.parse(src, filename=name)
    for n in ast.walk(tree):
        if not isinstance(n, ast.Call):
            continue
        if any(k.arg == "encoding" for k in n.keywords) or any(k.arg is None for k in n.keywords):
            continue
        f = n.func
        what = None
        if isinstance(f, ast.Name) and f.id == "open":
            m = _mode(n, 1)
            if not (isinstance(m, str) and "b" in m):
                what = "open() in text mode"
        elif isinstance(f, ast.Attribute):
            base = f.value.id if isinstance(f.value, ast.Name) else None
            if f.attr == "open" and base in ("io", "codecs"):
                m = _mode(n, 1)
                if not (isinstance(m, str) and "b" in m):
                    what = "%s.open() in text mode" % base
            elif f.attr in ("read_text", "write_text"):
                what = ".%s()" % f.attr
            elif f.attr == "open" and _mode(n, 0) in TEXT_MODES:
                what = ".open(%r)" % _mode(n, 0)
        if what:
            out.append((n.lineno, "%s without encoding=: %s" % (what, ast.unparse(n)[:100])))
    return out


def self_test():
    cases = [
        ("x = p.read_text()", 1), ("x = p.read_text(encoding='utf-8')", 0), ("open(f)", 1), ("open(f, 'rb')", 0),
        ("open(f, 'w', newline='')", 1), ("open(f, 'w', encoding='utf-8')", 0), ("io.open(f)", 1),
        ("p.open('w')", 1), ("p.open('rb')", 0), ("Image.open(f)", 0), ("p.write_text(s)", 1), ("open(f, **kw)", 0),
    ]
    return ["%r: expected %d finding(s), got %d" % (src, want, len(findings(src)))
            for src, want in cases if len(findings(src)) != want]


def main():
    bad = self_test()
    for b in bad:
        print("  FAIL self-test %s" % b)
    if bad:
        print("FAIL - %d self-test(s)" % len(bad))
        return 1
    found = []
    files = sorted(glob.glob(os.path.join(ROOT, "tools", "*.py")))
    for path in files:
        rel = os.path.relpath(path, ROOT).replace("\\", "/")
        try:
            src = open(path, encoding="utf-8").read()
            found += [(rel, ln, t) for ln, t in findings(src, rel)]
        except (SyntaxError, UnicodeDecodeError) as e:
            found.append((rel, 0, "does not parse as UTF-8 Python: %s" % e))
    for rel, ln, t in found:
        print("  FAIL ENC %s:%d %s" % (rel, ln, t))
    if found:
        print("FAIL - %d text open(s) without an encoding in tools/" % len(found))
        return 1
    print("PASS - %d tool(s): every text read and write names its encoding; %d self-test(s) pass"
          % (len(files), 12))
    return 0


if __name__ == "__main__":
    sys.exit(main())
