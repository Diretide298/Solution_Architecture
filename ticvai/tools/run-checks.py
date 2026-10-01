#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run every checker, keep its exit code, print the table, and fail the run if any gate failed.

**The loop in `refresh.sh` could not fail.** It ran

    printf "  %-22s" "$t"; python3 "tools/$t.py" 2>&1 | tail -1 || true

which discards the exit code twice over — the pipe makes `tail`'s status the pipeline's, and
`|| true` swallows what is left — and keeps only the final line of output. A checker emitting four
hundred errors contributed one line and did not fail the run.

**The reasoning behind it was sound and the fix was too wide.** Under `set -e` with `pipefail`,
one non-zero checker killed the script: *"for most of 9 September this script died at check-flows
and nobody saw the eight checks below it, including the ones that were passing."* The answer to
*one failure stops the report* is to collect failures, not to discard them.

**Three checkers report rather than gate, and that is deliberate** — `refresh.sh` says so:
`audit-unwired-tables`, `audit-duplicate-tables` and `audit-array-relationships` each ask a
question only a person can close, and *"a checker that fails the package on a judgement gets
silenced rather than answered"*. They run, they print, and they do not gate. **Any other tool
added to `REPORT_ONLY` needs that argument made in writing beside it.**

    python3 tools/run-checks.py            # print the table, exit non-zero if a gate failed
    python3 tools/run-checks.py --no-gate  # print the table, always exit 0
"""
import io
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CHECKS = [
    "check-screens", "check-frontend", "check-flows", "check-board-flows",
    "check-session-entry", "check-step-up", "check-states", "check-config-scope",
    "check-wireframes", "check-backlog", "check-traceability", "check-package",
    "check-screen-redundancy", "check-bindings", "check-migrations", "check-lineage",
    "check-doc-tables", "check-contract-split", "check-spec-coverage", "check-rfp-coverage",
    "check-authored-inputs", "check-output-paths", "audit-screenless-operations",
    "audit-unwired-tables", "audit-duplicate-tables", "audit-array-relationships",
    "audit-links", "audit-workbooks", "audit-pack-citations", "audit-contracts",
    "audit-screen-estate", "audit-uncontrolled-values", "index-sources", "check-contract-compat",
    # 30 September: a plan change must not make a second OpenProject ticket for work that has one.
    "check-key-stability",
    # 1 October (plan item 1C, C3): after the tag r1 the baseline migrations are frozen; a table change is
    # a new forward migration. check-key-stability (C4) and check-contract-compat also compare with r1.
    "check-migration-freeze",
    # 2 October (Chinmay's finance decisions, CHG-FIN-001..011): revenue labels, blind close, one taxable base,
    # the finance KPIs and chart encodings, the guest-selected currency.
    "check-finance-rules",
    # 1 October (plan item 1F, C12): the audit-class guards (docs/active/root-classes.md). Each fails
    # only on a member not in handoff/audit-baseline.json; --update-baseline after a fix tightens it.
    "check-ticket-text", "check-screen-wiring", "check-navigation", "check-contract-shapes",
    "check-ddl-conventions", "check-contract-storage", "check-starter-fit", "check-glossary-terms",
    "check-wireframe-coverage",
    # 1 October: the process design notes (handoff/design-notes/*.yaml) reach every design session through
    # BUNDLE.md; every rule there must carry a source that exists. Passes while the folder is empty.
    "check-design-notes",
    # 2 October (council of 2 October, docs/active/council/council-report-2026-10-02-opus.html): every change is a changes/entries/
    # file with its decision and why, and closes only on a prevention that exists and runs here.
    "check-changelog",
    # 2 October (same council, "the one thing to do first"): the design-handoff generator's three binding
    # counts (unbound controls, undefined operations, unknown fields) per app and block may only fall.
    "check-binding-ratchet",
    # 2 October (same council, typed properties): audience, needs-a-session, caller or named customer.
    "check-audience-match", "check-preauth-session", "check-subject",
    # 2 October (Chinmay's answers, CHG-SEED-005 and -012): a design import's differences carry a decision, and
    # decision documents cite only files git tracks.
    "check-candidate-decisions", "check-cited-sources",
]

# Report, do not gate. Each needs its reason stated here or it does not belong in this list.
REPORT_ONLY = {
    "audit-unwired-tables":
        "whether a table nothing reaches is a missing operation or a table that should not "
        "exist is a judgement",
    "audit-duplicate-tables":
        "whether a twin is a duplicate or a deliberate copy is a judgement",
    "audit-array-relationships":
        "whether an array should be a table is a judgement",
    "check-bindings":
        "runs as a baseline; --strict is the gating form and fails on unbound boilerplate",
    "check-contract-split":
        "reports concentration drift for a person to read; there is no threshold to fail on",
    "audit-uncontrolled-values":
        "whether a charge with no configuration is a missing control or an amount a provider "
        "set is a judgement; the answers live in handoff/values-without-configuration.md and "
        "the tool reads them back, so an answered row stops being reported",
    # 2 October: the three typed-property checks start as reports. They have no baseline yet, and their
    # current findings are the guest fixes (public theme and policy reads, staff fields off guest screens)
    # and the POS loyalty swap, which are in flight. When those land, the lead records the baseline
    # (--update-baseline) and takes each out of this list; from then a new finding blocks.
    "check-audience-match":
        "gates once the guest fixes land and the lead records its baseline (council of 2 October)",
    "check-preauth-session":
        "gates once the public theme and policy reads land and the lead records its baseline",
    "check-subject":
        "gates once the POS loyalty swap lands and the lead records its baseline",
    "check-candidate-decisions":
        "gates once the five undecided POS v2 candidates (POS-000, -003, -004, -012, -023) are decided and "
        "the lead records its baseline (CHG-SEED-005)",
}


def main():
    gate = "--no-gate" not in sys.argv[1:]
    only = [a for a in sys.argv[1:] if not a.startswith("-")]
    checks = [c for c in CHECKS if not only or c in only]

    results = []
    for t in checks:
        path = os.path.join(ROOT, "tools", "%s.py" % t)
        if not os.path.exists(path):
            print("  %-26s MISSING" % t)
            results.append((t, 127, "no such tool"))
            continue
        t0 = time.time()
        p = subprocess.run([sys.executable, path], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", cwd=ROOT,
                           env=dict(os.environ, PYTHONIOENCODING="utf8"))
        rc = p.returncode
        lines = [l for l in ((p.stdout or "") + (p.stderr or "")).split("\n") if l.strip()]
        last = lines[-1].strip() if lines else ""
        mark = "ok  " if rc == 0 else "FAIL"
        if t in REPORT_ONLY and rc != 0:
            mark = "rpt "
        print("  %-26s %s rc=%-3d %5.1fs  %s" % (t, mark, rc, time.time() - t0, last[:96]))
        results.append((t, rc, last))

    bad = [(t, rc) for t, rc, _ in results if rc != 0 and t not in REPORT_ONLY]
    rpt = [(t, rc) for t, rc, _ in results if rc != 0 and t in REPORT_ONLY]

    print("\n  %d checker(s) run · %d gate failure(s) · %d report-only non-zero"
          % (len(results), len(bad), len(rpt)))
    for t, rc in rpt:
        print("    rpt  %-26s rc=%d — %s" % (t, rc, REPORT_ONLY[t]))
    for t, rc in bad:
        print("    FAIL %-26s rc=%d" % (t, rc))

    if bad and gate:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
