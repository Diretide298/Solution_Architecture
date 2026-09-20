#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Two things my own text broke, both caught by the package's own checkers within a minute.

**1 · `check-traceability` wants one operation or schema per row, not a list.** I wrote
`"setDunningPolicy, listDunningCases, resolveDunningCase"` into an `evidence` field that is
resolved against the contract, and three of the four rows I moved failed on it. **The detail
belongs in `note`, which is prose, and `evidence` is a name the checker can look up** — which is
the whole reason the field is narrow.

**2 · `build-cf-index` flagged CF-35 as reading resolved while sitting under an open section, and
it was right to.** The trigger is `**closed` — from my own sentence *"PDPL Article 4 is a
**closed list of exceptions**"*. The register's pattern looks for `**Closed`, which is how a row
announces it has been settled.

**The wording changes rather than the checker.** A pattern loosened to excuse one sentence stops
catching the thing it exists to catch, and this is the second time in two days that the honest fix
was to move my text rather than widen a guard — `check-config-scope` and `setLeaderboardNickname`
was the first.

**And CF-35 now says in the row that it stays open**, which it should have said anyway: the
deviation is recorded, the principle is settled, and **what counsel still owes is the form** —
whether a notice acknowledged at a counter is *explicit* for a same-visit tag, or whether a
signature is needed. One is operable at a gate and the other is not.

    python3 tools/applied/fix-evidence-and-cf35-wording-21-september.py --apply
"""
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TRC = os.path.join(ROOT, "handoff", "traceability.json")
REG = os.path.join(ROOT, "docs", "registers", "conflicts.md")

EVIDENCE = {
    "2.14.22": ("setDunningPolicy",
                "BL-100. All five things the requirement names: attemptOffsetDays is the "
                "configurable retry schedule, notifyGuestOnEachAttempt the reminders, graceDays "
                "the grace period, terminalAction:suspendBilling the service suspension, and "
                "resolveDunningCase the recovery workflow. listDunningCases is the queue a venue "
                "works from."),
    "2.14.23": ("listBillingStatements",
                "BL-100. Statements, payment history and credits are contracted; "
                "BillingStatementLine carries charge, refund, failedAttempt and adjustment, and "
                "getBillingStatement returns the lines. **Not whole: no downloadable PDF and no "
                "tax breakdown.** The tax half is CF-133 -- a statement is deliberately not a tax "
                "invoice (isTaxInvoice false, read-only)."),
    "3.2.9": ("AdmissionRules",
              "BL-105. perProductRules[].biometricPolicy is disabled | offered | preferred per "
              "product, which is the activate/deactivate the requirement asks for. No `required` "
              "-- a biometric a guest cannot refuse without losing a ticket they paid for is not "
              "voluntary consent under PDPL. Inert while VenueSettings.biometrics.isEnabled is "
              "false."),
    "3.2.44": ("enrolFaceTag",
               "BL-106. BiometricKind.faceTag is its own kind with its own retention anchor, "
               "registrable at a ticket counter or an entry gate, purged at close of the "
               "operating day. **Deliberate deviation: the requirement says Face Tag `does not "
               "require the customer to explicitly sign a consent form` and the package requires "
               "consent anyway.** PDPL Article 4 admits no legitimate-interests basis, so a short "
               "retention shortens what the consent is for rather than removing the need for it. "
               "Recorded on CF-35."),
}

OLD_CF35 = (
    "PDPL Article 4 is a **closed list of exceptions with no legitimate-interests basis**, so "
    "there is no lawful route to a consent-free biometric capture"
)

NEW_CF35 = (
    "**PDPL Article 4 admits no legitimate-interests basis** — its exceptions are an exhaustive "
    "list — so there is no lawful route to a consent-free biometric capture"
)

OLD_TAIL = (
    "`VenueSettings.biometrics` already makes the venue name a DPIA and "
    "acknowledge a consent notice before any of it can be switched on."
)

NEW_TAIL = (
    "`VenueSettings.biometrics` already makes the venue name a DPIA and "
    "acknowledge a consent notice before any of it can be switched on. **This conflict stays "
    "open on that one question** — the functionality is built and the principle is settled; what "
    "is outstanding is the form of consent counsel will accept at a gate."
)


def main():
    apply = "--apply" in sys.argv[1:]
    T = json.load(io.open(TRC, encoding="utf-8"))
    reg = io.open(REG, encoding="utf-8").read()

    if OLD_CF35 not in reg and "2.14.22" not in str(EVIDENCE):
        print("  already applied")
        return 0

    idx = {r["packageRef"]: r for r in T["rows"]}
    changed = 0
    for ref, (ev, note) in EVIDENCE.items():
        r = idx.get(ref)
        if r is None:
            print("  !! %s missing from traceability.json" % ref)
            return 1
        if r["evidence"] != ev:
            print("    %-8s evidence  %-52s -> %s" % (ref, r["evidence"][:52], ev))
            r["evidence"] = ev
            r["note"] = note
            changed += 1

    for label, old, new in (("CF-35  `**closed list` -> no false resolve marker",
                             OLD_CF35, NEW_CF35),
                            ("CF-35  +stays open, on the form of consent", OLD_TAIL, NEW_TAIL)):
        if reg.count(old) != 1:
            print("  !! %s matched %d times" % (label, reg.count(old)))
            return 1
        reg = reg.replace(old, new, 1)
        print("    %s" % label)
        changed += 1

    # The two guards this script exists to satisfy, checked here rather than only downstream.
    import re
    RESOLVED = re.compile(
        r"\*\*Closed \d|Closed \d+ \w+\.|\*\*Closed\b|Recovered —|"
        r"(?:Added|Built|Fixed|Resolved|Corrected|Implemented|Decided) "
        r"(?:—|\d{1,2} (?:January|February|March|April|May|June|July|August|September|"
        r"October|November|December))", re.I)
    STILL = re.compile(r"stays open|remains open|still open|open on one|one number", re.I)
    line = [l for l in reg.split("\n") if l.startswith("| **CF-35** |")]
    if len(line) != 1:
        print("  !! CF-35 appears %d times" % len(line))
        return 1
    hits = RESOLVED.findall(line[0])
    if hits and not STILL.search(line[0]):
        print("  !! CF-35 still reads resolved: %s" % hits)
        return 1
    print("    CF-35  resolve-marker hits %s, 'stays open' present: %s"
          % (hits or "none", bool(STILL.search(line[0]))))

    if not changed:
        print("  nothing to change")
        return 0
    if not apply:
        print("\n  %d change(s) - pass --apply" % changed)
        return 0
    io.open(TRC, "w", encoding="utf-8", newline="\n").write(
        json.dumps(T, indent=1, ensure_ascii=False))
    io.open(REG, "w", encoding="utf-8", newline="\n").write(reg)
    print("  -> handoff/traceability.json, docs/registers/conflicts.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
