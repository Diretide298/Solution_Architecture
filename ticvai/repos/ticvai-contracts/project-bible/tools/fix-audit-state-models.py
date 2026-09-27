#!/usr/bin/env python3
"""Bring the state models in line with the stricter check-states.py (audit R081).

check-states now fails a state declared terminal that a real operation leaves, and a transition
credited to a GET. Both were always in states/*.yaml; the checker had just not looked. This reads
the checker's own FAIL lines and fixes exactly those:

  terminal but transitions to X via <op>   the write is the evidence: the state is not terminal,
                                           so it comes off the `terminal:` list
  credited to '<op>', which is a GET        a read cannot move a state: `operation` is dropped and
                                           the trigger becomes `job` (the side effect that records it)
  enum <contract>.<Schema>.status not found the contract now names the enum (<Schema>Status):
                                           the header points at it as a named enum

Text edits, so comments and layout stay. Dry run by default; --apply writes.
    python tools/fix-audit-state-models.py [--apply]
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPLY = "--apply" in sys.argv

out = subprocess.run([sys.executable, str(ROOT / "tools" / "check-states.py")], cwd=ROOT,
                     capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
fails = [l.strip()[len("FAIL"):].strip() for l in out.splitlines() if l.strip().startswith("FAIL")]
changes, skipped = [], []

for line in fails:
    fname, _, msg = line.partition(": ")
    path = ROOT / "states" / fname
    if not path.exists():
        skipped.append(line)
        continue
    text = path.read_text(encoding="utf-8")
    new = text
    m = re.match(r"'([^']+)' is declared terminal but transitions to '[^']+' via \S+", msg)
    g = re.match(r"transition (\S+)->(\S+) is credited to '([^']+)', which is a GET", msg)
    e = re.match(r"enum (\w+)\.(\w+)\.status not found in the contracts", msg)
    if m:
        state = m.group(1)
        # the `terminal:` list, one `- state` per line, up to the next top-level key
        block = re.search(r"(?m)^terminal:\r?\n((?:[ ]*-[^\n]*\n)+)", new)
        if block and re.search(rf"(?m)^[ ]*-[ ]*['\"]?{re.escape(state)}['\"]?[ ]*\r?$", block.group(1)):
            items = re.sub(rf"(?m)^[ ]*-[ ]*['\"]?{re.escape(state)}['\"]?[ ]*\r?\n", "", block.group(1), count=1)
            new = new[:block.start(1)] + items + new[block.end(1):]
            if not items.strip():
                new = re.sub(r"(?m)^terminal:\r?\n", "terminal: []\n", new, count=1)
    elif g:
        frm, to, op = g.groups()
        pat = re.compile(rf"(?m)^(- from: {re.escape(frm)}\r?\n  to: {re.escape(to)}\r?\n(?:  (?!operation:)[^\n]*\n)*?)"
                         rf"  operation: {re.escape(op)}\r?\n")
        hit = pat.search(new)
        if hit:
            head = re.sub(r"(?m)^  trigger: [^\n]*\n", "  trigger: job\n", hit.group(1), count=1)
            new = new[:hit.start()] + head + new[hit.end():]
    elif e:
        schema = e.group(2)
        named = f"{schema}Status"
        new = re.sub(r"(?m)^enum: [^\n]*$", f"enum: {named}", new, count=1)
        new = re.sub(r"(?m)^enumKind: inline$", "enumKind: named", new, count=1)
        new = re.sub(r"(?m)^enumSchema: [^\n]*$", f"enumSchema: {named}", new, count=1)
        new = re.sub(r"(?m)^enumProperty: [^\n]*\r?\n", "", new, count=1)
        new = re.sub(r"(?m)^# Contract: (\w+)\.[\w.]+$", rf"# Contract: \g<1>.{named}", new, count=1)
    if new != text:
        changes.append(f"{fname}: {msg[:110]}")
        if APPLY:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(new)
    else:
        skipped.append(line)

for c in changes:
    print("  fix ", c)
for s in skipped:
    print("  left", s[:160])
print(f"{len(changes)} fixed, {len(skipped)} left for a person" + ("" if APPLY else " (dry run - pass --apply)"))
