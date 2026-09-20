#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Close BL-096, BL-105 and BL-106 against the model built this morning.

Written to a file rather than passed through a shell, which ate two closure notes yesterday.
"""
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PATH = os.path.join(ROOT, "handoff", "contract-backlog.json")

SHARED = (
    "\n\n**Built as one piece with BL-096, BL-105 and BL-106**, because all three were stalled on "
    "CF-35 and building any one alone would have decided the legal posture for the other two by "
    "accident. **CF-35 stays open** — counsel has not answered — and the shape chosen is the one "
    "that stays correct either way: **the capability exists and nothing is on by default.**"
)

NOTES = {
    "BL-096": (
        "**Closed 21 September.** `verifyIdentity` models matching apart from enrolling, which is "
        "what the entry asked for and what the package could not do — `enrolFacePass` binds a face "
        "to an entitlement, and nothing anywhere read a presented document and checked it against "
        "the holder.\n\n"
        "**Two methods, because 2.13.41 asks two different questions.** `documentToHolder` compares "
        "a presented document with the entitlement holder's recorded details; "
        "`liveCaptureToEnrolment` compares a capture with an existing `facePass` or `faceTag` and "
        "**requires one to exist** — it is the check, never a back door to enrolment.\n\n"
        "**`IdentityVerification` is `x-ticvai-persistence: none` and carries no evidence.** The "
        "document image and the live template are write-only, compared and discarded; "
        "`access.scan_event` records that a verification happened and what it concluded and "
        "**never what was compared**. That is the same line BL-179 drew for the gender advisory a "
        "day earlier, and for the same reason — a scanned or inferred attribute kept against a "
        "guest is sensitive personal data with no consent behind it.\n\n"
        "**`inconclusive` is a real outcome and the one the counter screen is designed around.** A "
        "matcher that never returns it has been tuned to look confident, and a guest at a counter "
        "pays for that tuning by being told they are not themselves. **Advisory, not decisive** — "
        "the entitlement admits, and a `noMatch` tells an agent to ask a question rather than "
        "refusing entry, because a document that does not match is far more often a bad scan than "
        "a fraud.\n\n"
        "**2.14.7's annual-pass quota is `maxPassesPerBiometricIdentity`** on the product's own "
        "rules. `enrolFacePass` already answered 409 where a face was on another annual pass; the "
        "number behind that refusal was one and was invisible. **Null means unlimited**, which is "
        "right for everything that is not an annual pass — a quota applied where nobody asked for "
        "one turns a family sharing a day ticket into a fraud alert."
    ),
    "BL-105": (
        "**Closed 21 September.** `AdmissionRules.perProductRules[].biometricPolicy` makes the "
        "biometric check a property of the product, which is what 3.2.9 asks for — memberships "
        "checked, day tickets not. It sits on `perProductRules` rather than on the profile because "
        "**that is already where a ticket type states its own terms** (BL-059 put it there), and a "
        "profile per product would multiply profiles to carry one flag.\n\n"
        "**`disabled`, `offered`, `preferred` — and deliberately no `required`.** A guest refused "
        "entry to a ticket they have paid for unless they surrender a biometric has not consented "
        "voluntarily, and **consent that cannot be refused without losing what you bought is not "
        "consent under PDPL**: it fails the voluntary and the withdrawable tests in the same "
        "moment. `preferred` gives the venue the lever it actually wants — a faster lane — without "
        "the platform shipping a switch that turns a ticket into a condition.\n\n"
        "**Absent means `disabled`, and the whole thing is inert while "
        "`VenueSettings.biometrics.isEnabled` is false.** A rules profile copied to another venue "
        "cannot begin capturing faces at the destination, which is the failure a per-product flag "
        "with no venue gate would have introduced."
    ),
    "BL-106": (
        "**Closed 21 September.** `BiometricKind` splits `facePass` from `faceTag`, and "
        "`BiometricRetentionAnchor` gives each its own anchor — which is exactly what "
        "[ADR-0047](../adr/0047-how-long-data-is-kept-and-where-it-goes-next.md) said this entry "
        "needed: *a kind and two different anchors, not a new model*. `pii.subject_biometric` "
        "already carried `expires_at`, `is_active`, `consent_purpose_id` and `consent_given_at`.\n\n"
        "**The two are different legal postures rather than two settings on one record.** A "
        "`facePass` is enduring, enrolled deliberately on the three surfaces 3.2.43 names, "
        "revocable by the guest, and anchored to the validity of its entitlement. A `faceTag` is "
        "same-visit, taken at a ticket counter **or an entry gate** — a gate is present here "
        "exactly where 3.2.43 omits it from Face Pass — and anchored to the ticket or to the close "
        "of the operating day. **Storing both as one record with a date made the stricter rule "
        "depend on a field nobody enforced**, which is what this entry was raised to stop.\n\n"
        "**Face Tag still takes explicit consent.** PDPL Article 4 is a closed list of exceptions "
        "with **no legitimate-interests basis**, so there is no route that makes a short-lived "
        "biometric consent-free — only one that makes the consent shorter-lived. A design that "
        "skipped it because the data dies at midnight would have been wrong about the law rather "
        "than lenient about it.\n\n"
        "**`retentionAnchor` is derived from `kind` and never sent.** A retention period somebody "
        "can type is a retention period somebody will type wrongly. The anchors are ceilings and "
        "cannot be configured upward, per ADR-0047.\n\n"
        "**The schema is still named `FacePassEnrolment` and that is a deliberate non-rename.** "
        "Its 19 references are all inside `access.yaml`, but the derived design bundles already "
        "handed to designers carry the name, and renaming for tidiness would make delivered work "
        "inconsistent to fix nothing."
    ),
}

CF35 = (
    "**CF-35's warning is `VenueSettings.biometrics`, and it is stronger than a warning.** "
    "`isEnabled` is false by default and cannot be set true without a `dpiaReference` and a "
    "`consentNoticeAcknowledgedAt`, with `acknowledgedByPrincipalId` recording who confirmed it; "
    "`setVenueSettings` answers 422 otherwise. **PDPL Article 21 requires the assessment before "
    "the processing**, so the field is the law rather than a courtesy — and a venue that cannot "
    "name its assessment has not done one. The person switching it on is asked at the moment they "
    "switch it on, rather than by an auditor a year later."
)


def main():
    apply = "--apply" in sys.argv[1:]
    B = json.load(io.open(PATH, encoding="utf-8"))
    changed = 0
    for bid, note in NOTES.items():
        e = next(x for x in B["entries"] if x["id"] == bid)
        text = note + ("\n\n" + CF35 if bid == "BL-105" else "") + SHARED
        if e.get("closedBy") == text and e.get("status") == "done":
            print("    %s already closed" % bid)
            continue
        e["status"] = "done"
        e["lane"] = "settled"
        e["closed"] = "2026-09-21"
        e["closedBy"] = text
        e["blockedOnConflicts"] = []
        print("    %s  -> done · settled · 2026-09-21 · %d chars" % (bid, len(text)))
        changed += 1

    o = sum(1 for x in B["entries"] if x.get("status") != "done")
    print("\n    open backlog entries after this: %d" % o)
    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    if changed:
        io.open(PATH, "w", encoding="utf-8", newline="\n").write(
            json.dumps(B, indent=1, ensure_ascii=False))
        print("  -> handoff/contract-backlog.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
