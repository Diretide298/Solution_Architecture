#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Re-measure `schema-viewer-notes.md` against 625 tables, deriving every number rather than typing it.

The document's own instruction is *"every number below comes from `handoff/relationships.csv` and
`handoff/schema-reference.json`; run `tools/derive-relationships.py` to reproduce them"* — so this
script reproduces them and refuses to write if a number it is replacing is not the one currently
in the file.

**What moved, and only one of it is interesting.** Two tables arrived with BL-100:
`payments.dunning_policy` and `payments.dunning_case`.

    625 tables, 1,351 edges     was 623 and 1,349
    pii.subject   68 -> 69      dunning_case.subject_id -- a recurring charge is a
                                charge against a person, which is why it is an edge
    no edge at all  66 -> 67    dunning_policy: configuration, referenced by nothing,
                                which is what a policy table looks like
    71 of 629                   derive-relationships' own figure, four column-less
                                storage tables ahead of schema-reference as before

**`identity.principal` at 143 and `platform.scope` at 94 have not moved**, and that is worth
leaving visible: the two most-referenced tables in the package absorbed a day of contract work
without gaining an edge, which is what a stable spine looks like.

    python3 tools/applied/schema-viewer-notes-remeasured-21-september.py --apply
"""
import collections
import csv
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOC = os.path.join(ROOT, "handoff", "schema-viewer-notes.md")
REF = os.path.join(ROOT, "handoff", "schema-reference.json")
CSV = os.path.join(ROOT, "handoff", "relationships.csv")
GRAPH = os.path.join(ROOT, "handoff", "relationship-graph.json")


def measure():
    S = json.load(io.open(REF, encoding="utf-8"))
    tbl = {t for t in (S.get("cols") or {}) if "." in t and ":" not in t}
    rows = list(csv.DictReader(io.open(CSV, encoding="utf-8")))
    inb = collections.Counter()
    touched = set()
    for r in rows:
        touched.add(r["from_table"])
        touched.add(r["to_table"])
        inb[r["to_table"]] += 1
    G = json.load(io.open(GRAPH, encoding="utf-8"))
    gt = G.get("tables") or G.get("nodes") or {}
    return {
        "tables": len(tbl),
        "edges": len(rows),
        "principal": inb["identity.principal"],
        "scope": inb["platform.scope"],
        "subject": inb["pii.subject"],
        "noEdge": len(tbl - touched),
        "graphTables": len(gt) if hasattr(gt, "__len__") else None,
        "graphNoEdge": None,
    }


SUBS = [
    ("Re-measured 20 September against 623 tables and 1,349 edges.",
     "Re-measured 21 September against {tables} tables and {edges:,} edges."),
    ("`identity.principal` is the target of **143 edges**. `platform.scope` of **94**. "
     "`pii.subject`\nof **68**.",
     "`identity.principal` is the target of **{principal} edges**. `platform.scope` of "
     "**{scope}**. `pii.subject`\nof **{subject}**."),
    ("**66 of 623 tables carry no edge at all.** `derive-relationships` reports 70 of 627",
     "**{noEdge} of {tables} tables carry no edge at all.** `derive-relationships` reports "
     "{gNo} of {gTot}"),
]


def main():
    apply = "--apply" in sys.argv[1:]
    m = measure()
    s = io.open(DOC, encoding="utf-8").read()

    # derive-relationships' own two figures, read from its output rather than restated
    import subprocess
    out = subprocess.run(
        [sys.executable, os.path.join(ROOT, "tools", "derive-relationships.py")],
        capture_output=True, text=True, encoding="utf-8",
        env=dict(os.environ, PYTHONIOENCODING="utf8")).stdout
    gtot = gno = None
    for line in out.split("\n"):
        if " tables linked" in line:
            gtot = int(line.split(" of ")[1].split()[0])
        if line.strip().startswith(("71 with no relationship", "7")) and "no relationship" in line:
            gno = int(line.strip().split()[0])
    if gtot is None or gno is None:
        print("  !! could not read derive-relationships' own figures from its output")
        return 1
    m["gTot"], m["gNo"] = gtot, gno

    print("    measured: %d tables · %s edges · principal %d · scope %d · subject %d"
          % (m["tables"], "{:,}".format(m["edges"]), m["principal"], m["scope"], m["subject"]))
    print("              %d with no edge · derive-relationships says %d of %d"
          % (m["noEdge"], m["gNo"], m["gTot"]))

    if "Re-measured 21 September" in s:
        print("  already applied")
        return 0

    for old, tmpl in SUBS:
        if s.count(old) != 1:
            print("  !! passage matched %d times: %r" % (s.count(old), old[:60]))
            return 1
        s = s.replace(old, tmpl.format(**m), 1)
        print("    %s" % tmpl.format(**m).split("\n")[0][:96])

    if "623" in s:
        left = [l for l in s.split("\n") if "623" in l]
        print("  !! 623 still appears on %d line(s): %r" % (len(left), left[0][:90]))
        return 1
    print("    no `623` left in the document")

    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    io.open(DOC, "w", encoding="utf-8", newline="\n").write(s)
    print("  -> handoff/schema-viewer-notes.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
