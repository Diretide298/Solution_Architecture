#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Five matrix rows move, one of them is a deviation I built without recording, and one claim of
mine was too wide.

**3.2.44 asks for Face Tag and says, in the requirement text, that it *"does not require the
customer to explicitly sign a consent form"*.** BL-106 built Face Tag **requiring explicit
consent**, on the reasoning that PDPL Article 4 is a closed list of exceptions with no
legitimate-interests basis. That reasoning stands. **What did not happen is recording that the
package had refused what the requirement asked for** — and a deviation nobody wrote down is a
deviation the client discovers in UAT.

**This is CF-130's exact shape** (3.2.45 asks for rejection; the package deviates and the conflict
says why), and it belongs on **CF-35**, which is open, owned by Allam and counsel, and is the
conflict about biometrics under PDPL.

**Separately, BL-096's closure claimed 2.14.7 and should not have.** The requirement is *"annual-
pass **reservation** quota engine linked to biometric identity, with self-service
reschedule/cancel"* — visit slots booked by a pass holder. `maxPassesPerBiometricIdentity` caps how
many passes one face may hold, which is a different thing wearing a similar word. The row stays
`CONTRACTED_PARTIAL` and the closure text is corrected.

## What actually moves, read against the requirement text rather than against the entry that
## cited it

    2.13.41  GAP -> CONTRACTED          "Identity Verification" -- verifyIdentity
    2.14.22  GAP -> CONTRACTED          retry schedules, reminders, grace, suspension and
                                        recovery -- all five are DunningPolicy fields
    3.2.9    PARTIAL -> CONTRACTED      activate/deactivate per ticket type -- biometricPolicy
    2.14.23  GAP -> CONTRACTED_PARTIAL  statements and history yes; **no PDF export and no
                                        tax breakdown**, so not whole
    3.2.44   GAP -> CONTRACTED_PARTIAL  built, and deliberately not as asked

**2.14.19, 2.14.20, 2.14.21, 3.3.38 and 5.7.96 are deliberately not touched.** They sit near
today's work and are not answered by it — the billing-cycle and downgrade rows are served by
provisional drafts awaiting review, and 3.3.38 asks for access-investigation reporting, which one
segregation report is not.

    python3 tools/applied/traceability-and-3244-deviation-21-september.py --apply
"""
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TRC = os.path.join(ROOT, "handoff", "traceability.json")
REG = os.path.join(ROOT, "docs", "registers", "conflicts.md")
BLG = os.path.join(ROOT, "handoff", "contract-backlog.json")

MOVES = {
    "2.13.41": ("CONTRACTED", "access", "verifyIdentity",
                "BL-096. Matching modelled apart from enrolling: documentToHolder compares a "
                "presented document with the entitlement holder, liveCaptureToEnrolment compares "
                "a capture with an existing enrolment. IdentityVerification is persistence:none "
                "and returns no evidence."),
    "2.14.22": ("CONTRACTED", "payments", "setDunningPolicy, listDunningCases, resolveDunningCase",
                "BL-100. All five things the requirement names: attemptOffsetDays is the "
                "configurable retry schedule, notifyGuestOnEachAttempt the reminders, graceDays "
                "the grace period, terminalAction:suspendBilling the service suspension, and "
                "resolveDunningCase the recovery workflow."),
    "3.2.9": ("CONTRACTED", "access", "AdmissionRules.perProductRules[].biometricPolicy",
              "BL-105. disabled | offered | preferred per product, which is the activate/"
              "deactivate the requirement asks for. No `required` -- a biometric a guest cannot "
              "refuse without losing a ticket they paid for is not voluntary consent under PDPL."),
    "2.14.23": ("CONTRACTED_PARTIAL", "orders", "listBillingStatements, getBillingStatement",
                "BL-100. Statements, payment history and credits are contracted; "
                "BillingStatementLine carries charge, refund, failedAttempt and adjustment. "
                "**Not whole: no downloadable PDF and no tax breakdown.** The tax half is CF-133 "
                "-- a statement is deliberately not a tax invoice (isTaxInvoice false, "
                "read-only)."),
    "3.2.44": ("CONTRACTED_PARTIAL", "access", "BiometricKind.faceTag, enrolFaceTag",
               "BL-106. Face Tag is modelled as its own kind with its own retention anchor, "
               "registrable at a ticket counter or an entry gate, purged at close of the "
               "operating day. **Deliberate deviation: the requirement says Face Tag `does not "
               "require the customer to explicitly sign a consent form` and the package requires "
               "consent anyway.** PDPL Article 4 is a closed list of exceptions with no "
               "legitimate-interests basis, so a short retention shortens what the consent is "
               "for rather than removing the need for it. Recorded on CF-35."),
}

CF35_ADD = (
    " **A deviation was built on 21 September and is recorded here rather than discovered in "
    "UAT.** 3.2.44 describes Face Tag and states that it *\"does not require the customer to "
    "explicitly sign a consent form\"*. **BL-106 built it requiring explicit consent anyway.** "
    "PDPL Article 4 is a **closed list of exceptions with no legitimate-interests basis**, so "
    "there is no lawful route to a consent-free biometric capture — a short life shortens what "
    "the consent is *for* and does not remove the need for it. **This is CF-130's shape**: a "
    "requirement asking for something the law does not allow, built the lawful way, with the "
    "difference written down. **What counsel needs to confirm is the form rather than the "
    "principle** — whether a notice acknowledged at a counter satisfies *explicit* for a "
    "same-visit tag, or whether a signature is required, because the first is operable at a gate "
    "and the second is not. `VenueSettings.biometrics` already makes the venue name a DPIA and "
    "acknowledge a consent notice before any of it can be switched on."
)

OLD_CLAIM = (
    "**2.14.7's annual-pass quota is `maxPassesPerBiometricIdentity`** on the product's own "
    "rules. `enrolFacePass` already answered 409 where a face was on another annual pass; the "
    "number behind that refusal was one and was invisible. **Null means unlimited**, which is "
    "right for everything that is not an annual pass — a quota applied where nobody asked for "
    "one turns a family sharing a day ticket into a fraud alert."
)

NEW_CLAIM = (
    "**`maxPassesPerBiometricIdentity` caps how many passes one face may hold.** "
    "`enrolFacePass` already answered 409 where a face was on another annual pass; the number "
    "behind that refusal was one and was invisible. **Null means unlimited**, which is right for "
    "everything that is not an annual pass — a quota applied where nobody asked for one turns a "
    "family sharing a day ticket into a fraud alert.\n\n"
    "**Correction, 21 September: this closure first claimed 2.14.7 and should not have.** That "
    "requirement is an *\"annual-pass **reservation** quota engine linked to biometric identity, "
    "with self-service reschedule/cancel\"* — visit slots booked by a pass holder, not a cap on "
    "passes per face. A different thing wearing a similar word, and the row stays "
    "`CONTRACTED_PARTIAL`."
)


def main():
    apply = "--apply" in sys.argv[1:]
    T = json.load(io.open(TRC, encoding="utf-8"))
    reg = io.open(REG, encoding="utf-8").read()
    B = json.load(io.open(BLG, encoding="utf-8"))

    if "A deviation was built on 21 September" in reg:
        print("  already applied")
        return 0

    idx = {r["packageRef"]: r for r in T["rows"]}
    for ref, (verdict, contract, evidence, note) in MOVES.items():
        r = idx.get(ref)
        if r is None:
            print("  !! %s is not in traceability.json" % ref)
            return 1
        print("    %-8s %-18s -> %-18s  %s" % (ref, r["verdict"], verdict, evidence[:46]))
        r["verdict"] = verdict
        r["contract"] = contract
        r["evidence"] = evidence
        r["note"] = note
    T["generated"] = "21 September 2026"

    if reg.count("| **CF-35** |") != 1:
        print("  !! CF-35 appears %d times" % reg.count("| **CF-35** |"))
        return 1
    old = ("the current design treats biometrics as ordinary identity data | "
           "Allam + counsel | 13 Aug |")
    if reg.count(old) != 1:
        print("  !! CF-35 tail matched %d times" % reg.count(old))
        return 1
    reg = reg.replace(old, ("the current design treats biometrics as ordinary identity data."
                            + CF35_ADD + " | Allam + counsel | 13 Aug |"), 1)
    print("    CF-35  +the 3.2.44 consent deviation, %d chars" % len(CF35_ADD))

    e = next(x for x in B["entries"] if x["id"] == "BL-096")
    if e.get("closedBy", "").count(OLD_CLAIM) != 1:
        print("  !! BL-096's 2.14.7 claim matched %d times"
              % e.get("closedBy", "").count(OLD_CLAIM))
        return 1
    e["closedBy"] = e["closedBy"].replace(OLD_CLAIM, NEW_CLAIM, 1)
    print("    BL-096  2.14.7 overclaim corrected in place")

    import collections
    c = collections.Counter(r["verdict"] for r in T["rows"])
    print("\n    verdicts now: %s" % ", ".join("%s %d" % kv for kv in c.most_common()))

    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    io.open(TRC, "w", encoding="utf-8", newline="\n").write(
        json.dumps(T, indent=1, ensure_ascii=False))
    io.open(REG, "w", encoding="utf-8", newline="\n").write(reg)
    io.open(BLG, "w", encoding="utf-8", newline="\n").write(
        json.dumps(B, indent=1, ensure_ascii=False))
    print("  -> handoff/traceability.json, docs/registers/conflicts.md, "
          "handoff/contract-backlog.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
