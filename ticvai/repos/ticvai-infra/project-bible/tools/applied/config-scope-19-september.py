#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Give every configuration operation the level it applies at (ADR-0018).

**The August artefact audit's strongest finding, and the only one that did not close.**
The requirement matrix says "configurable" 321 times and 263 of those do not say at what
level. ADR-0018 settles it with a rule rather than 263 answers — three levels, nearest
ancestor wins, venue is the floor — and `check-config-scope` reported **57 operations**
that had not been held to it.

## The level is not a new decision

Forty-seven declare no `x-ticvai-config-scope` at all, and every one of them already
declares `x-ticvai-scope-level`: who may call it. The ADR's third rule ties the two
together — *"`x-ticvai-config-scope` never sits below `x-ticvai-scope-level`. An operation a
venue manager may call cannot set a tenant-wide value."*

So the config scope is the calling scope, clamped to the three levels the ADR allows:

    scope-level venue    -> venue      26 operations
    scope-level tenant   -> tenant     18
    scope-level platform -> tenant      3   tenant is the ceiling; nothing configures above it

**Nothing configures below venue.** A workstation is assigned a profile the venue defined,
not configured itself — forty workstations configured individually is forty things that
drift. No operation here sits at workstation scope, so the floor is not reached.

## The other ten were tagged and never read

They carry a scope the naming rules could not see, which the checker reports as worse than
an absent one — *"an unexamined tag"*. `setMediaTaxonomy`, `setAttractionType`,
`setGameOperationalConfiguration` and seven more configure a taxonomy, a class of
attraction, a kiosk journey. **The tag is the stronger signal and the nouns are the ones
the package settled on since August**, so `IS_CONFIG` is widened to reach them rather than
the operations renamed to suit a regex.

Idempotent. Run with no arguments to preview; `--apply` to write.
"""
import io
import os
import re
import subprocess
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# venue is the floor, tenant the ceiling — region is only ever declared by hand.
CLAMP = {"venue": "venue", "workstation": "venue", "region": "region",
         "tenant": "tenant", "platform": "tenant"}


def failing():
    """Ask the checker which operations it is unhappy about, rather than guessing."""
    out = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "check-config-scope.py")],
                         capture_output=True, text=True, encoding="utf-8",
                         errors="replace", cwd=ROOT).stdout
    need, unseen = set(), set()
    for line in out.splitlines():
        m = re.search(r"FAIL\s+[\w-]+\.(\w+): no x-ticvai-config-scope", line)
        if m:
            need.add(m.group(1))
        m = re.search(r"FAIL\s+[\w-]+\.(\w+): declares a config scope but the naming", line)
        if m:
            unseen.add(m.group(1))
    return need, unseen


def main():
    apply = "--apply" in sys.argv
    need, unseen = failing()
    print("  %d operation(s) declare no config scope · %d tagged but unexamined"
          % (len(need), len(unseen)))

    added = 0
    for tier in ("spine", "satellite"):
        d = os.path.join(ROOT, "contracts", tier)
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".yaml"):
                continue
            path = os.path.join(d, fn)
            raw = io.open(path, encoding="utf-8").read()
            doc = yaml.safe_load(raw) or {}
            hits = []
            for _p, m in (doc.get("paths") or {}).items():
                if not isinstance(m, dict):
                    continue
                for _v, op in m.items():
                    if not isinstance(op, dict):
                        continue
                    oid = op.get("operationId")
                    if oid in need and not op.get("x-ticvai-config-scope"):
                        lvl = CLAMP.get(op.get("x-ticvai-scope-level"), "venue")
                        hits.append((oid, lvl))
            if not hits:
                continue
            for oid, lvl in hits:
                # Insert beside the scope level it was derived from, so the pair reads together.
                pat = re.compile(r"(operationId:\s*%s\n(?:[^\n]*\n)*?"
                                 r"(\s*)x-ticvai-scope-level:[^\n]*\n)" % re.escape(oid))
                m = pat.search(raw)
                if not m:
                    print("    could not place %s" % oid)
                    continue
                raw = raw[:m.end(1)] + "%sx-ticvai-config-scope: %s\n" % (m.group(2), lvl) \
                    + raw[m.end(1):]
                added += 1
            print("  %-22s %d operation(s)" % (fn, len(hits)))
            if apply:
                io.open(path, "w", encoding="utf-8", newline="\n").write(raw)

    print("\n  %d config scope(s) added" % added)
    if unseen:
        print("  still to widen IS_CONFIG for: %s" % ", ".join(sorted(unseen)))
    if not apply:
        print("\n  nothing written — pass --apply")


if __name__ == "__main__":
    main()
