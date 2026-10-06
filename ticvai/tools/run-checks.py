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
    python3 tools/run-checks.py --jobs 4   # four checkers at a time; the same table, in the same order
    python3 tools/run-checks.py --out-dir DIR   # also keep each checker's full output in DIR/<name>.txt

**Four at a time, printed in the list's order** (council of 3 October 23:30, CHG-RSPD-001). The
checkers summed to 33 minutes run one after another; every one of them only reads the package
(`SERIAL`, below, says how that was established). `--jobs N` runs N at once, keeps each one's
output apart, and prints each row only when every row above it has printed -- so the table, the
exit code and every checker's output are the same as `--jobs 1`, which is the original loop and is
kept. A checker in `SERIAL` runs alone, with nothing before it still running and nothing after it
started, so whatever it writes is seen exactly as the sequential run saw it.
"""
import io
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

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
    # 2 October (CHG-DOOR-001..006): every app has a sign-in door, every staff and partner door is a sign-in
    # form with the second factor, the role prompt and (in a browser) SSO and no workstation, no form asks a
    # person for a token, and no door lands on a read gated by a right to act.
    "check-doors",
    # 2 October (Chinmay, pre-apply round, CHG-SBO-001): every TICVAI Console screen acting in a tenant carries
    # the R098 tenant picker and platform-staff grant, and every Console screen is core.
    "check-console-grant",
    "check-table-keys", "check-migration-tickets", "check-ticket-scope",
    # 3 October (Chinmay, Block A business rules, CHG-RUL-001..018): the contract side of the business rules
    # (bill split, streamed answers, visit plan, purchase orders, payment links, report runs, theme contrast,
    # dashboards, work orders, incidents, fares, door sessions, attendance, AI currency, admission QR, new guest
    # and incident operations), and two general rules: a streaming answer declares its events, and an update
    # declares the refusals of the create whose body it takes.
    "check-business-rules",
    # 3 October (the Block A audit's screen patterns, CHG-SPF-001..013): no form asks for a readOnly field,
    # no list dumps a schema, the no-access state names the read's and the actions' permissions, every
    # required entry parameter is carried, no screen wears another's route, a Block A screen is wave 1 and
    # says so, and Chinmay's 3 October screen decisions stay made.
    "check-screen-patterns",
    # 3 October (TODO step 9b, CHG-RONEC-006): the Block A flow design briefs (handoff/flow-briefs/*.yaml) carry
    # every required key, and every screen, flow and contract#operation they name exists, so a brief cannot
    # send Claude Design to an operation the contracts do not have.
    "check-flow-briefs",
    # 3 October (Chinmay's r1 additions, CHG-RONEC-001..005): the venue-map import formats and ADR-0069's closed
    # items, the blind close in every flow and the decided F32, the concierge's conversation polling, the
    # BO-1065 residency section and the payment-link cancel.
    "check-r1-additions",
    # 3 October (the r1 gate and the HLD/LLD cross-check, CHG-R1S-002..021): every write writes a table or
    # says why not and every emitter writes the outbox; the AI residency and scrubbing safeguards stay in the
    # contracts; an operation-specific error names its problem types (a falling ceiling).
    "check-write-lineage",
    "check-ai-residency",
    "check-problem-types",
    # 3 October (Chinmay's r1 additions and the r1 gate, CHG-RONEP-001..003): every operation a Block A screen binds is
    # built in Block A, and no artefact the last released plan built leaves the tickets without a reason; a ticket's
    # builds are real ids, a module test names what it tests, a setup ticket links only its own part.
    "check-plan-closure", "check-ticket-builds",
    # 4 October (the Sprint 1-2 fix round, contracts, CHG-FXC-003): an id an operation is addressed or filtered by
    # has a column to match (a ratchet over the 226 known). check-write-lineage gained W-CACHEKEY and W-CREATED.
    "check-parameter-columns",
    "check-channel-config",
    "check-device-tiers",
    "check-plan-owners",
    "check-terraform-pools",
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
    # check-candidate-decisions gates since 2 October 2026 (CHG-CLN-011): the five POS v2 candidates are decided
    # (POSV2-9..13, applied by CHG-SPO-001) and it passes with an empty baseline.
}


# **Run alone, never beside another checker** (CHG-RSPD-001). A checker belongs here when, run bare as
# this script runs it, it writes a file in the package or anywhere another checker reads -- then the
# order the sequential run gave it is the only order that is known to be right. Read on 4 October,
# every one of the 68 above writes only behind a flag this script never passes: `--write`
# (check-spec-coverage, check-rfp-coverage, audit-contracts, audit-screen-estate, index-sources),
# `--csv` (audit-screenless-operations, audit-unwired-tables, audit-duplicate-tables,
# audit-array-relationships, audit-uncontrolled-values), `--json` (check-screen-redundancy), `--fix`
# (check-doc-tables), `--bless` (check-authored-inputs), `--freeze` (check-contract-compat) and
# `--update-baseline` (check-binding-ratchet and the audit_guard checkers). check-contract-compat's
# one unflagged write is a fresh `tempfile.mkdtemp` per process, removed after. The git calls
# (check-package, check-changelog, check-cited-sources, check-plan-closure, check-binding-ratchet,
# audit-contracts, release_baseline's users) only read; git's own index refresh takes its lock
# without waiting and skips when another holds it. check-parameter-columns, the 69th (CHG-FXC-003, merged into
# r1-fix-merge on 4 October), only reads. So the set is empty, and a checker that starts
# writing a shared file must be added here in the same change.
SERIAL = set()


def _run_one(t):
    """(name, rc, output, seconds) -- the output is stdout then stderr, as the original loop joined them."""
    path = os.path.join(ROOT, "tools", "%s.py" % t)
    if not os.path.exists(path):
        return t, 127, None, 0.0
    t0 = time.time()
    p = subprocess.run([sys.executable, path], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", cwd=ROOT,
                       env=dict(os.environ, PYTHONIOENCODING="utf8"))
    return t, p.returncode, (p.stdout or "") + (p.stderr or ""), time.time() - t0


def _args(argv):
    gate, jobs, out_dir, only = True, 1, None, []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--no-gate":
            gate = False
        elif a in ("--jobs", "-j") or a.startswith("--jobs="):
            v = a.split("=", 1)[1] if "=" in a else (argv[i + 1] if i + 1 < len(argv) else "")
            i += 0 if "=" in a else 1
            if not v.isdigit() or int(v) < 1:
                raise SystemExit("run-checks: --jobs needs a whole number of at least 1")
            jobs = int(v)
        elif a == "--out-dir" or a.startswith("--out-dir="):
            out_dir = a.split("=", 1)[1] if "=" in a else (argv[i + 1] if i + 1 < len(argv) else "")
            i += 0 if "=" in a else 1
            if not out_dir:
                raise SystemExit("run-checks: --out-dir needs a directory")
        elif not a.startswith("-"):
            only.append(a)
        i += 1
    return gate, jobs, out_dir, only


def main():
    gate, jobs, out_dir, only = _args(sys.argv[1:])
    checks = [c for c in CHECKS if not only or c in only]
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    results = []

    def report(r):
        t, rc, out, secs = r
        if out is None:
            print("  %-26s MISSING" % t, flush=True)
            results.append((t, 127, "no such tool"))
            return
        if out_dir:
            with open(os.path.join(out_dir, t + ".txt"), "w", encoding="utf-8", newline="") as fh:
                fh.write(out)
            with open(os.path.join(out_dir, "results.tsv"), "a", encoding="utf-8", newline="\n") as fh:
                fh.write("%s\t%d\t%.1f\n" % (t, rc, secs))
        lines = [l for l in out.split("\n") if l.strip()]
        last = lines[-1].strip() if lines else ""
        mark = "ok  " if rc == 0 else "FAIL"
        if t in REPORT_ONLY and rc != 0:
            mark = "rpt "
        print("  %-26s %s rc=%-3d %5.1fs  %s" % (t, mark, rc, secs, last[:96]), flush=True)
        results.append((t, rc, last))

    if out_dir and os.path.exists(os.path.join(out_dir, "results.tsv")):
        os.remove(os.path.join(out_dir, "results.tsv"))
    if jobs == 1:
        # The original loop: one checker at a time, in the list's order.
        for t in checks:
            report(_run_one(t))
    else:
        with ThreadPoolExecutor(max_workers=jobs) as pool:
            pending = []
            for t in checks:
                if t in SERIAL:
                    for f in pending:              # everything before it, finished and printed
                        report(f.result())
                    pending = []
                    report(_run_one(t))            # then it, alone
                    continue
                pending.append(pool.submit(_run_one, t))
            for f in pending:                      # in the list's order, each as soon as it can be
                report(f.result())

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
