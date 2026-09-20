#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Re-derive `artefact-audit.md`'s verdict table from `traceability.json`.

**The document's own warning became true of itself.** It says the verdicts *"have not been
re-tested since 18 August"* and that *"some rows counted as gaps here are likely served now"* —
and on 21 September five of them were re-tested and moved. The table below it still showed the
20 September distribution.

    CONTRACTED          2,647 -> 2,650    2.13.41, 2.14.22, 3.2.9
    GAP_CONTRACT           93 -> 89       four of them, minus the one that went partial
    CONTRACTED_PARTIAL     43 -> 44       2.14.23 and 3.2.44 in, 3.2.9 out
    PARKED, GAP_DECISION   unchanged

**Every number is computed from `handoff/traceability.json`, never typed**, and the percentages
with it — a table where the counts are derived and the percentages are not is a table that drifts
in the column nobody checks.

**The note about re-testing stays**, and gains the fact that it happened once. Removing it would
claim a freshness the other 3,179 rows do not have.

    python3 tools/applied/artefact-audit-verdicts-21-september.py --apply
"""
import collections
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOC = os.path.join(ROOT, "handoff", "artefact-audit.md")
TRC = os.path.join(ROOT, "handoff", "traceability.json")

MEANING = {
    "CONTRACTED": "An operation or schema field demonstrably serves it",
    "PARKED": "AI-parked or workshop-blocked, with the reason named",
    "GAP_CONTRACT": "Needs an operation or schema that does not exist",
    "CONTRACTED_PARTIAL": "Served, but a field, operation or state is missing",
    "GAP_DECISION": "Undesignable without a client answer",
}
ORDER = ["CONTRACTED", "PARKED", "GAP_CONTRACT", "CONTRACTED_PARTIAL", "GAP_DECISION"]

OLD_NOTE = """> **The verdicts below were assigned during the walk and have not been re-tested since
> 18 August.**"""

NEW_NOTE = """> **The verdicts below were assigned during the walk and have not been re-tested since
> 18 August, except five re-tested on 21 September** — 2.13.41, 2.14.22, 2.14.23, 3.2.9 and
> 3.2.44, against the biometric cluster and the dunning model built that day.**"""


def main():
    apply = "--apply" in sys.argv[1:]
    T = json.load(io.open(TRC, encoding="utf-8"))
    rows = T["rows"]
    c = collections.Counter(r["verdict"] for r in rows)
    total = len(rows)
    print("    traceability.json: %d rows" % total)
    for v in ORDER:
        print("      %-20s %5d  %5.1f%%" % (v, c[v], 100.0 * c[v] / total))
    if set(c) - set(ORDER):
        print("  !! unknown verdict(s): %s" % sorted(set(c) - set(ORDER)))
        return 1

    s = io.open(DOC, encoding="utf-8").read()

    table = "\n".join(
        "| `%s` | %s | %.1f%% | %s |" % (v, "{:,}".format(c[v]), 100.0 * c[v] / total, MEANING[v])
        for v in ORDER)
    pat = re.compile(r"(\| Verdict \| Rows \| \| What it means \|\n\|---\|---:\|---:\|---\|\n)"
                     r"((?:\|[^\n]*\|\n)+)")
    m = pat.search(s)
    if not m:
        print("  !! the verdict table was not found in its expected shape")
        return 1
    if m.group(2).strip() == table.strip():
        print("    verdict table already current")
    else:
        s = s[:m.start(2)] + table + "\n" + s[m.end(2):]
        print("    verdict table re-derived")

    gapc, gapd = c["GAP_CONTRACT"], c["GAP_DECISION"]
    old_gap = re.search(r"\*\*(\d+) rows are a genuine gap\*\* — (\d+) needing contract work "
                        r"and (\d+) needing the client\.", s)
    if not old_gap:
        print("  !! the genuine-gap sentence was not found")
        return 1
    s = s[:old_gap.start()] + (
        "**%d rows are a genuine gap** — %d needing contract work and %d needing the client."
        % (gapc + gapd, gapc, gapd)) + s[old_gap.end():]
    print("    genuine gap  %s -> %d (%d contract + %d client)"
          % (old_gap.group(1), gapc + gapd, gapc, gapd))

    if s.count(OLD_NOTE) == 1:
        s = s.replace(OLD_NOTE, NEW_NOTE, 1)
        print("    re-test note  +the five moved on 21 September")
    elif "except five re-tested on 21 September" not in s:
        print("  !! the re-test note was not found and has not been updated")
        return 1

    for stale in ("2,647", "| 93 |", "| 43 |"):
        if stale in s:
            print("  !! %r still appears" % stale)
            return 1
    print("    no stale verdict figure left in the document")

    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    io.open(DOC, "w", encoding="utf-8", newline="\n").write(s)
    print("  -> handoff/artefact-audit.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
