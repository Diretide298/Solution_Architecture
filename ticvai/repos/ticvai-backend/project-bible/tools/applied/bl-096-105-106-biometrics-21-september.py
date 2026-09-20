#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BL-096, BL-105 and BL-106 — the biometric cluster, built as one piece.

**Three entries, one model, and they cannot be done separately.** BL-105 wants the biometric check
switchable per ticket type; BL-106 wants Face Tag separated from Face Pass because their retention
obligations differ; BL-096 wants verification modelled apart from enrolment. All three are stalled
behind the same thing — **CF-35: biometric data is sensitive under PDPL**, heightened protection,
explicit consent, Article 21 DPIA. Building any one of them alone would decide the legal posture
for the other two by accident.

**Decided by Chinmay: build the functionality regardless of CF-35's outcome.** The venue turns
biometrics on and off per ticket type and takes consent accordingly. So the shape below is the one
that stays correct whichever way counsel comes back — **the capability exists and nothing is on by
default**, and turning it on is an act with a DPIA reference attached.

## The four pieces

**1 · A venue-level master switch that cannot be flipped quietly** (`VenueSettings.biometrics`).
This is CF-35's *"warning while turning it on"*, and it is stronger than a warning: `isEnabled`
cannot be true without a `dpiaReference` and a `consentNoticeAcknowledgedAt`, and 422 is the
answer where either is missing. **Article 21 requires the assessment before the processing**, so
the field is the law rather than a courtesy — and a venue that cannot name its assessment has not
done one.

**2 · `BiometricKind` — `facePass` and `faceTag` are two legal postures, not two settings.**

    facePass    enduring, enrolled deliberately on three surfaces, explicit consent,
                revocable by the guest, anchored to the entitlement's validity
    faceTag     same-visit, taken at a counter or a gate, consent still explicit but
                per-visit, anchored to the ticket and purged at close of day

**Face Tag still takes consent.** PDPL Article 4 is a closed list of exceptions with **no
legitimate-interests basis** — there is no route that makes a short-lived biometric consent-free,
only one that makes the consent shorter-lived. A design that skipped it because the data dies at
midnight would be wrong about the law rather than lenient about it.

**3 · `BiometricPolicy` on `perProductRules` — `disabled`, `offered`, `preferred`, and never
`required`.** A guest refused entry to a ticket they paid for because they declined a biometric is
consent under duress, which is **not consent under PDPL** — the withdrawable, voluntary test fails
at the turnstile. `preferred` means the fast lane uses a face and the ordinary lane still admits on
the entitlement. **`maxPassesPerBiometricIdentity` sits beside it** and is 2.14.7's quota: the 409
in `enrolFacePass` already refuses a second annual pass, and this is the number behind it rather
than a constant nobody can see.

**4 · `verifyIdentity` — matching is not enrolling, and conflating them is how templates get
kept.** 2.13.41 wants a presented document checked against the entitlement holder at a counter or
a gate. Enrolment persists; **verification persists nothing.** The comparison happens, the outcome
is returned, and the evidence — the document image, the live capture — is never written. What
`access.scan_event` records is that a verification occurred and what it concluded, never what was
compared, which is the same line BL-179 drew for the gender advisory an hour before this.

    python3 tools/applied/bl-096-105-106-biometrics-21-september.py --apply
"""
import io
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ACC = os.path.join(ROOT, "contracts", "spine", "access.yaml")
TEN = os.path.join(ROOT, "contracts", "spine", "tenancy.yaml")

# --- 1 · the venue master switch (CF-35's warning, with teeth) -------------------------------

TEN_ANCHOR = "        segregatedAccess:\n          type: object\n          nullable: true\n"

BIOMETRICS = """        biometrics:
          type: object
          nullable: true
          description: >
            CF-35, BL-096, BL-105, BL-106. **The venue-level master switch, and the one place a
            person is asked whether the paperwork exists.** Biometric data is sensitive under
            PDPL (Federal Decree-Law 45/2021) — heightened protection, explicit consent, and an
            Article 21 assessment before the processing rather than after it.

            **Nothing below this switch operates while it is off.** `AdmissionRules` may carry a
            `biometricPolicy` per ticket type and those rules are inert until a venue enables
            biometrics here, which means a profile copied between venues cannot start capturing
            faces at the destination.

            **Venue level because that is where the assessment is filed.** Region owns tax and
            currency; the DPIA, the consent notice and the hardware are a venue's.
          properties:
            isEnabled:
              type: boolean
              default: false
              description: >
                **Off by default, and turning it on is refused without the two fields below.**
                `setVenueSettings` answers 422 rather than accepting an enable it cannot
                evidence — **a DPIA nobody can name is a DPIA nobody did**, and the point of the
                refusal is that the person switching this on is asked at the moment they switch
                it on rather than by an auditor a year later.
            dpiaReference:
              type: string
              nullable: true
              maxLength: 200
              description: >
                **The venue's own reference for its Article 21 assessment.** The platform does
                not hold the document and does not judge it; it records that one was named, by
                whom, and when — which is what an audit asks for and what the venue can produce.
            consentNoticeAcknowledgedAt:
              type: string
              format: date-time
              nullable: true
              description: >
                **When somebody confirmed the consent forms are in place at the point of
                capture.** A guest consenting in an app is a record; a guest consenting at a
                ticket counter is a notice somebody has to have printed and a question somebody
                has to have asked.
            acknowledgedByPrincipalId:
              type: string
              format: uuid
              nullable: true
              description: >
                **Who confirmed it.** An acknowledgement with no name behind it cannot be
                followed up, and this is the field that makes the switch an act rather than a
                setting.
            faceTagPurgeMinutesAfterClose:
              type: integer
              nullable: true
              default: 0
              description: >
                BL-106. **How long a same-visit Face Tag survives past the close of the
                operating day**, and zero is the default because that is what 3.2.44 describes.
                A non-zero value is an operational allowance for a late reconciliation, not a
                retention period — **`facePass` ignores this entirely** and is bounded by its
                entitlement.
"""

# --- 2 · the kinds, the anchors, the policy ---------------------------------------------------

ACC_ENUM_ANCHOR = ("    FacePassEnrolment:\n      type: object\n"
                   "      x-ticvai-persistence: pii.subject_biometric\n")

ENUMS = """    BiometricKind:
      type: string
      description: >
        BL-106, CF-35. **Two different legal postures, not two settings on one record.** 3.2.44
        describes a temporary facial model taken at a counter or a gate and deleted when the
        ticket expires; 3.2.43 describes an enduring Face Pass enrolled deliberately on three
        surfaces. **Storing both as one record with a date makes the stricter rule depend on a
        field nobody enforces**, which is what BL-106 was raised to stop.

        `facePass` — enduring, explicit consent, revocable by the guest, anchored to the validity
        of the entitlement it belongs to.

        `faceTag` — same-visit, **consent still explicit and still recorded**, anchored to the
        ticket and purged at close of the operating day. **PDPL Article 4 is a closed list of
        exceptions with no legitimate-interests basis**, so a short life does not remove the need
        for consent — it only shortens what the consent is for.
      enum:
      - facePass
      - faceTag

    BiometricRetentionAnchor:
      type: string
      readOnly: true
      description: >
        BL-106, ADR-0047. **What the expiry is measured from, derived from the kind rather than
        chosen.** A retention period a person can type is a retention period somebody will type
        wrongly; the anchor follows the kind, and the kind follows how the biometric was taken.

        `entitlementValidity` — `facePass`. The face cannot outlive the pass it was enrolled for.

        `ticketValidity` — `faceTag` against a dated ticket.

        `operatingDayClose` — `faceTag` where the ticket has no end of its own, plus
        `VenueSettings.biometrics.faceTagPurgeMinutesAfterClose`.
      enum:
      - entitlementValidity
      - ticketValidity
      - operatingDayClose

    BiometricPolicy:
      type: string
      description: >
        BL-105, 3.2.9. **Whether a ticket type asks for a biometric, and there is deliberately no
        `required`.**

        `disabled` — the default, and what every product does until a venue decides otherwise.

        `offered` — the guest may enrol and nothing changes if they decline.

        `preferred` — the biometric lane is the fast one and **the ordinary lane still admits on
        the entitlement**.

        **`required` is absent because it would not be lawful.** A guest refused entry to a ticket
        they have paid for unless they surrender a biometric has not consented voluntarily, and
        **consent that cannot be refused without losing what you bought is not consent under
        PDPL** — it fails the voluntary and withdrawable tests at the same moment. The venue keeps
        the commercial lever it actually wants, which is a faster lane, without the platform
        offering a switch that turns a ticket into a condition.

        **Inert while `VenueSettings.biometrics.isEnabled` is false.**
      enum:
      - disabled
      - offered
      - preferred

"""

# --- 3 · FacePassEnrolment gains a kind and an anchor -----------------------------------------

OLD_REQ = """      required:
      - id
      - subjectId
      - entitlementId
      - source
      - capturedAt
"""

NEW_REQ = """      required:
      - id
      - kind
      - subjectId
      - entitlementId
      - source
      - capturedAt
"""

OLD_SOURCE = """        source:
          type: string
          enum:
          - guestApp
          - ticketCounter
          - annualPassCounter
        capturedAt:
"""

NEW_SOURCE = """        kind:
          $ref: '#/components/schemas/BiometricKind'
        retentionAnchor:
          allOf:
          - $ref: '#/components/schemas/BiometricRetentionAnchor'
          description: >
            BL-106. **Derived from `kind`, never sent.** `facePass` anchors to the entitlement,
            `faceTag` to the ticket or to the close of the operating day.
        source:
          type: string
          enum:
          - guestApp
          - ticketCounter
          - annualPassCounter
          - entryGate
          description: >
            **`entryGate` is valid for `faceTag` only**, and 3.2.43's omission of it from Face
            Pass is deliberate: an enduring enrolment is a considered act with consent attached,
            not something done in a queue. 3.2.44 puts a Face Tag at a gate precisely because it
            dies the same day.
        capturedAt:
"""

OLD_EXPIRES = """        expiresAt:
          type: string
          format: date-time
          nullable: true
          description: '**Bounded by the entitlement it belongs to.** A face outliving the pass it was
            enrolled for is a biometric held for no stated purpose, which CF-64 has to settle.

            '
"""

NEW_EXPIRES = """        expiresAt:
          type: string
          format: date-time
          nullable: true
          description: '**Bounded by whatever `retentionAnchor` names**, and a face outliving it is
            a biometric held for no stated purpose.

            **Settled 20 September by ADR-0047**, which CF-64 had been carrying since 6 August: a
            `facePass` cannot outlive its entitlement and a `faceTag` does not survive the close of
            the operating day. **These are ceilings rather than defaults** — they cannot be
            configured upward, because a retention that a tenant can extend without limit is the
            breach ADR-0047 gave the platform a ceiling to prevent.

            '
"""

# --- 4 · the per-product switch (BL-105) and the quota (2.14.7) --------------------------------

OLD_PPR = """              allowedAccessPointIds:
                type: array
                items:
                  type: string
                  format: uuid
        name:
          type: string
          maxLength: 200
"""

NEW_PPR = """              allowedAccessPointIds:
                type: array
                items:
                  type: string
                  format: uuid
              biometricPolicy:
                allOf:
                - $ref: '#/components/schemas/BiometricPolicy'
                description: >
                  BL-105, 3.2.9. **The biometric check is a property of the product, not of the
                  venue** — memberships checked, day tickets not. It sits here rather than on the
                  profile because `perProductRules` is already where a ticket type states its own
                  terms, and a profile per product would multiply profiles to carry one flag.

                  **Absent means `disabled`**, and `disabled` is the answer for every product
                  until somebody chooses otherwise. **Inert while
                  `VenueSettings.biometrics.isEnabled` is false**, so a rules profile copied to
                  another venue cannot begin capturing faces there.
              maxPassesPerBiometricIdentity:
                type: integer
                nullable: true
                minimum: 1
                description: >
                  BL-096, 2.14.7. **The annual-pass quota, keyed to biometric identity.**
                  `enrolFacePass` already answers 409 where a face is on another annual pass; the
                  constant behind that refusal was one and was invisible. **Null means unlimited**
                  and is the answer for every product that is not an annual pass — a quota applied
                  where nobody asked for one turns a family sharing a day ticket into a fraud
                  alert.
        name:
          type: string
          maxLength: 200
"""

# --- 5 · the operations ------------------------------------------------------------------------

PATHS_ANCHOR = "  /face-pass/enrolments:\n"

PATHS = """  /face-tag/enrolments:
    post:
      operationId: enrolFaceTag
      x-ticvai-consumed-by:
        - "P08 BO-188 Face Tag Temporary Enrollment"
      x-ticvai-audience:
      - staff
      summary: Capture a same-visit facial model that dies at close of day
      description: '3.2.44. **A Face Tag is not a short Face Pass.** It is taken at a ticket counter
        or an entry gate, it is anchored to the ticket rather than to a pass, and it is purged at the
        close of the operating day — which is the posture that makes it defensible at all.

        **Consent is still explicit and still recorded.** PDPL Article 4 is a closed list of
        exceptions with **no legitimate-interests basis**, so there is no route that makes a
        short-lived biometric consent-free. What a short life changes is what the consent is *for*,
        not whether it is needed — and a design that skipped it because the data dies at midnight
        would be wrong about the law rather than lenient about it.

        **Refused where `VenueSettings.biometrics.isEnabled` is false**, and that switch cannot be
        turned on without a DPIA reference and a consent-notice acknowledgement (CF-35).

        **A template is stored, never an image**, and the template cannot reconstruct the face.

        '
      tags:
      - access
      x-ticvai-permission: GUEST_MANAGE
      x-ticvai-scope-level: venue
      x-ticvai-offline-capable: false
      x-ticvai-conflict-policy: serverWins
      parameters:
      - $ref: ../shared/common.yaml#/components/parameters/IdempotencyKey
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
              - subjectId
              - entitlementId
              - template
              - capturedAt
              - consent
              - source
              properties:
                subjectId:
                  type: string
                  format: uuid
                entitlementId:
                  type: string
                  format: uuid
                template:
                  type: string
                  format: password
                  description: '**Write-only, never returned.** A template, not an image.

                    '
                capturedAt:
                  type: string
                  format: date-time
                source:
                  type: string
                  enum:
                  - ticketCounter
                  - entryGate
                  description: '**The two surfaces 3.2.44 allows**, and a gate is present here
                    exactly where it is absent from Face Pass: this one does not outlive the visit.

                    '
                consent:
                  type: object
                  required:
                  - purposeId
                  - givenAt
                  description: '**Per-visit rather than enduring, and still explicit.**

                    '
                  properties:
                    purposeId:
                      type: string
                      format: uuid
                    givenAt:
                      type: string
                      format: date-time
                    guardianSubjectId:
                      type: string
                      format: uuid
                      nullable: true
                      description: Required where the subject is a minor (3.2.12).
                    guardianRelationship:
                      type: string
                      nullable: true
      responses:
        '201':
          description: Tagged
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/FacePassEnrolment'
        '409':
          description: '**Biometrics are not enabled at this venue**, or this ticket type''s
            `biometricPolicy` is `disabled`.

            '
          content:
            application/problem+json:
              schema:
                $ref: ../shared/common.yaml#/components/schemas/Problem
        '422':
          description: Capture quality too low to match against later in the visit.
          content:
            application/problem+json:
              schema:
                $ref: ../shared/common.yaml#/components/schemas/Problem
  /identity-verifications:
    post:
      operationId: verifyIdentity
      x-ticvai-consumed-by:
        - "P07 SCN-003 Ready to scan"
        - "P04 POS-014 Sales Exceptions, Controls & Operational Actions"
      x-ticvai-audience:
      - staff
      summary: Check the person presenting against the person entitled
      description: '2.13.41. **Matching is not enrolling, and this contract exists because the
        package could only do the second.** `enrolFacePass` binds a face to an entitlement;
        nothing anywhere read a presented document and checked it against the holder.

        **Nothing here is persisted.** The document image and the live capture are compared and
        discarded — `x-ticvai-persistence: none`. What `access.scan_event` records is that a
        verification happened and what it concluded, **never what was compared**, which is the
        same line drawn for the gender advisory in BL-179: an inferred or scanned attribute kept
        against a guest is sensitive personal data with no consent behind it.

        **Advisory to the person at the counter, not decisive.** The entitlement admits. A
        `noMatch` tells a counter agent to ask a question; it does not refuse entry on its own,
        because a document that does not match is far more often a bad scan than a fraud.

        **Refused where the venue has not enabled biometrics** and the comparison requested is a
        biometric one (CF-35). A document-to-name comparison needs no such switch.

        '
      tags:
      - access
      x-ticvai-permission: ACCESS_VALIDATE
      x-ticvai-scope-level: venue
      x-ticvai-offline-capable: false
      x-ticvai-conflict-policy: serverWins
      parameters:
      - $ref: ../shared/common.yaml#/components/parameters/IdempotencyKey
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
              - entitlementId
              - method
              properties:
                entitlementId:
                  type: string
                  format: uuid
                method:
                  type: string
                  enum:
                  - documentToHolder
                  - liveCaptureToEnrolment
                  description: '**Two different questions.** `documentToHolder` reads a presented
                    document and compares it with the entitlement holder''s recorded details.
                    `liveCaptureToEnrolment` compares a capture with an existing `facePass` or
                    `faceTag` and **requires one to exist** — it is the check, not the enrolment.

                    '
                documentEvidence:
                  type: string
                  format: password
                  description: '**Write-only and never stored.** Read by the matcher and
                    discarded; `access.scan_event` keeps the outcome and not this.

                    '
                liveTemplate:
                  type: string
                  format: password
                  description: '**Write-only and never stored.** A template rather than an image,
                    compared and discarded.

                    '
                accessPointId:
                  type: string
                  format: uuid
                  nullable: true
      responses:
        '200':
          description: Compared
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/IdentityVerification'
        '409':
          description: '**Nothing to compare against** — `liveCaptureToEnrolment` where the
            entitlement has no enrolment, or a biometric method at a venue that has not enabled
            biometrics.

            '
          content:
            application/problem+json:
              schema:
                $ref: ../shared/common.yaml#/components/schemas/Problem
"""

RESULT = """    IdentityVerification:
      type: object
      x-ticvai-persistence: none — computed, and the outcome alone is kept as access.scan_event
      description: >
        BL-096, 2.13.41. **The result of a comparison, and deliberately not enough to repeat it.**
        There is no template here, no document image and no stored evidence — the comparison
        happened, this is what it concluded, and the material is gone.
      required:
      - outcome
      - method
      - comparedAt
      properties:
        outcome:
          type: string
          enum:
          - match
          - noMatch
          - inconclusive
          description: >
            **`inconclusive` is a real answer and the one to design the counter screen around.** A
            matcher that never returns it has been tuned to look confident, and the cost of that
            tuning is paid by a guest at a counter being told they are not themselves.
        method:
          type: string
          enum:
          - documentToHolder
          - liveCaptureToEnrolment
        confidence:
          type: number
          minimum: 0
          maximum: 1
          nullable: true
          description: >
            **Shown to the agent, not thresholded silently.** The same reasoning as BL-179's
            advisory: an outcome with no confidence beside it is read as a fact, and the person
            deciding needs to know how sure the machine was.
        comparedAt:
          type: string
          format: date-time
        accessPointId:
          type: string
          format: uuid
          nullable: true

"""


def check(path, s, label):
    try:
        doc = yaml.safe_load(s)
    except Exception as e:
        print("  !! %s would not parse: %s" % (label, str(e)[:200]))
        return None
    have = set((doc.get("components") or {}).get("schemas") or {})
    for ref in set(re.findall(r"(?<![\w./-])#/components/schemas/([A-Za-z0-9_]+)",
                              yaml.safe_dump(doc))):
        if ref not in have:
            print("  !! %s refs %s and does not define it" % (label, ref))
            return None
    text_n = len(re.findall(r"^      operationId:", s, re.M))
    parsed_n = sum(1 for p in (doc.get("paths") or {}).values() for o in (p or {}).values()
                   if isinstance(o, dict) and o.get("operationId"))
    if text_n != parsed_n:
        print("  !! %s: %d operationId lines, %d parsed" % (label, text_n, parsed_n))
        return None
    print("    %-14s parses, refs resolve, %d operations" % (label, parsed_n))
    return doc


def sub(s, old, new, label):
    if s.count(old) != 1:
        print("  !! %s matched %d times" % (label, s.count(old)))
        return None
    print("    %s" % label)
    return s.replace(old, new)


def main():
    apply = "--apply" in sys.argv[1:]
    a = io.open(ACC, encoding="utf-8").read()
    t = io.open(TEN, encoding="utf-8").read()

    if "BiometricKind:" in a and "biometrics:" in t:
        print("  already applied")
        return 0

    print("  tenancy.yaml — CF-35's switch")
    t = sub(t, TEN_ANCHOR, BIOMETRICS + TEN_ANCHOR, "VenueSettings  +biometrics")
    if t is None:
        return 1

    print("  access.yaml — BL-106, the kinds and the anchors")
    a = sub(a, ACC_ENUM_ANCHOR, ENUMS + ACC_ENUM_ANCHOR,
            "+BiometricKind, +BiometricRetentionAnchor, +BiometricPolicy")
    if a is None:
        return 1
    a = sub(a, OLD_REQ, NEW_REQ, "FacePassEnrolment  kind now required")
    if a is None:
        return 1
    a = sub(a, OLD_SOURCE, NEW_SOURCE, "FacePassEnrolment  +kind, +retentionAnchor, source +entryGate")
    if a is None:
        return 1
    a = sub(a, OLD_EXPIRES, NEW_EXPIRES, "FacePassEnrolment  expiresAt anchored by ADR-0047")
    if a is None:
        return 1

    print("  access.yaml — BL-105, the per-product switch")
    a = sub(a, OLD_PPR, NEW_PPR, "perProductRules  +biometricPolicy, +maxPassesPerBiometricIdentity")
    if a is None:
        return 1

    print("  access.yaml — BL-096, verification apart from enrolment")
    a = sub(a, PATHS_ANCHOR, PATHS + PATHS_ANCHOR, "+enrolFaceTag, +verifyIdentity")
    if a is None:
        return 1
    a = sub(a, ACC_ENUM_ANCHOR, RESULT + ACC_ENUM_ANCHOR, "+IdentityVerification")
    if a is None:
        return 1

    da = check(ACC, a, "access.yaml")
    dt = check(TEN, t, "tenancy.yaml")
    if da is None or dt is None:
        return 1

    # The three things that must stay true, asserted rather than trusted.
    pol = da["components"]["schemas"]["BiometricPolicy"]["enum"]
    if "required" in pol:
        print("  !! BiometricPolicy offers `required` — that is consent under duress")
        return 1
    print("    BiometricPolicy has no `required`: %s" % ", ".join(pol))

    iv = da["components"]["schemas"]["IdentityVerification"]
    if not str(iv.get("x-ticvai-persistence", "")).startswith("none"):
        print("  !! IdentityVerification is persisted — the evidence would be stored")
        return 1
    if any(k in (iv.get("properties") or {}) for k in ("template", "liveTemplate",
                                                       "documentEvidence")):
        print("  !! IdentityVerification returns evidence")
        return 1
    print("    IdentityVerification  persistence none, carries no evidence")

    bio = (dt["components"]["schemas"]["VenueSettings"]["properties"]["biometrics"]
           ["properties"])
    for f in ("isEnabled", "dpiaReference", "consentNoticeAcknowledgedAt"):
        if f not in bio:
            print("  !! VenueSettings.biometrics is missing %s" % f)
            return 1
    if bio["isEnabled"].get("default") is not False:
        print("  !! biometrics.isEnabled does not default to false")
        return 1
    print("    VenueSettings.biometrics  off by default, DPIA reference required to enable")

    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    io.open(ACC, "w", encoding="utf-8", newline="\n").write(a)
    io.open(TEN, "w", encoding="utf-8", newline="\n").write(t)
    print("  -> contracts/spine/access.yaml, contracts/spine/tenancy.yaml")
    return 0


if __name__ == "__main__":
    sys.exit(main())
