#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BL-179: `deviceAssisted` says *"available only where the driver reports the capability"*, and
no driver reports any capability.

**The deliberate half of CF-130.** `VenueSettings.segregatedAccess.genderVerification` accepts
`off`, `staffAssisted` and `deviceAssisted`. The third is a switch a venue can turn on and
**nothing answers it** — `RegisteredDevice` carries `kind`, `driver`, `identifier`, `model`,
`firmwareVersion` and `status`, and no way for a driver to say what it can do.

**The order is right and CF-130 argued it well.** The platform does not infer gender: a Ladies
Night ticket is already gendered at the point of sale, so the gate checks the entitlement the
platform issued rather than the face in front of it — deterministic, auditable, already
contracted through `admissionRules`. And these events are staffed; **a classifier that overrules
a person who can see more than it can is a machine and a human disagreeing while a guest waits.**

So this adds the capability flag and the advisory path, and nothing else changes.

## Three constraints, and the third is the one that shapes the schema

**1. Advisory, never decisive.** 3.2.45 asks for rejection and the package deviates deliberately.
The advisory cannot appear in `outcome` or `denyReason`, which are the decisive fields, and
`entitlementGated` stays `true` and `readOnly` — *"the gate admits on the entitlement. Everything
below is advisory on top of that, and nothing replaces it."*

**2. It must carry a confidence and the device that reported it.** An advisory with no confidence
is read as a fact, and `overrideRateAlertThreshold` already exists to detect the failure this
creates — *"an override rate near zero means the steward has stopped deciding, and that is the
number that says whether the human safeguard is working or decorative."* That number is only
meaningful if the steward knows how sure the device was.

**3. It is never persisted, and that is a PDPL position rather than a storage preference.**

> An inferred gender classification stored against a guest is **sensitive personal data under
> PDPL with no consent behind it** — the guest agreed to be admitted, not to be classified.
> Face Pass and Face Tag have consent columns (`consent_purpose_id`, `consent_given_at`) because
> a guest enrolled. **Nobody enrols in being looked at by a turnstile.**

`ValidationResult` is already `x-ticvai-persistence: none — computed, persisted as scan_event`,
so the advisory reaches the steward's screen and is gone. **`scan_event` records that an
override happened and never what the device thought**, which keeps the override-rate metric
working without building a gender register nobody consented to.

**What remains after this is a screen**, not a contract: the steward's display. BL-179 named that
too and it is design work.

    python3 tools/applied/bl-179-device-gender-capability-20-september.py --apply
"""
import io
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEN = os.path.join(ROOT, "contracts", "spine", "tenancy.yaml")
ACC = os.path.join(ROOT, "contracts", "spine", "access.yaml")

# --- A. the capability, on the device -------------------------------------------------------

DEV_ANCHOR = "        lastHeartbeatAt: { type: string, format: date-time, nullable: true }\n"

DEV_CAPS = """        capabilities:
          type: array
          items:
            $ref: '#/components/schemas/DeviceCapability'
          description: >
            BL-179. **What this driver reports it can do, beyond reading media.** ADR-0015 is
            standards-first — the device does what the device does — and until now a venue could
            switch on a feature that depended on hardware without anything being able to say
            whether the hardware was there.

            **A capability absent is a capability unavailable**, not a capability assumed. A
            venue setting that requires one is refused where no device in scope reports it,
            rather than silently doing nothing at the gate.
"""

CAP_SCHEMA = """    DeviceCapability:
      type: string
      description: >
        BL-179. **Something a driver reports, not something the platform provides.** The list
        grows as vendors are added, which is ADR-0015's whole position: adding a vendor is a
        driver plus configuration rather than a core change.

        **`genderClassification` is here because `VenueSettings.segregatedAccess.
        genderVerification` already offers `deviceAssisted` and nothing answered it** — a switch
        with no driver behind it. Where a venue's access hardware performs the check and the
        venue chooses to use it, the result is **advisory to the steward and never decisive at
        the turnstile** (`ValidationResult.advisory`). 3.2.45 asks for rejection; the package
        deviates deliberately and CF-130 records why.
      enum:
      - genderClassification

"""

# --- B. the advisory, on the scan result ----------------------------------------------------

ACC_ANCHOR = """        serverEvaluatedAt:
          type: string
          format: date-time
"""

ADVISORY = """        advisory:
          type: object
          nullable: true
          description: >
            BL-179, CF-130. **What a device observed, for the steward, never for the gate.**
            Present only where an access point's device reports the matching
            `DeviceCapability` and the venue has turned the corresponding setting on.

            **Never persisted.** This schema is computed and stored as `access.scan_event`, and
            the advisory is deliberately not part of what is stored: an inferred classification
            kept against a guest is sensitive personal data with no consent behind it. **A guest
            agreed to be admitted, not to be classified** — Face Pass and Face Tag carry
            `consent_purpose_id` and `consent_given_at` because somebody enrolled, and nobody
            enrols in being looked at by a turnstile. `scan_event` records that an override
            happened and never what the device thought, which keeps
            `overrideRateAlertThreshold` working without building a register nobody agreed to.

            **It cannot reach `outcome` or `denyReason`.** Those are decisive and
            `entitlementGated` is `true` and read-only: the gate admits on the entitlement, and
            everything here sits on top of that without replacing any of it.
          properties:
            genderClassification:
              type: string
              enum: [women, men, undetermined]
              description: >
                **`undetermined` is a real answer and the most common one to design for.** A
                classifier that never returns it is one that has been tuned to look confident.
            confidence:
              type: number
              minimum: 0
              maximum: 1
              description: >
                **Required reading for the steward, not decoration.** An advisory with no
                confidence is read as a fact, and `overrideRateAlertThreshold` exists to catch
                exactly the failure that produces — *an override rate near zero means the steward
                has stopped deciding.* That number only means anything if the steward could see
                how sure the device was.
            reportedByDeviceId:
              type: string
              format: uuid
              description: >
                **Which device said it.** A classifier that degrades is one camera, not a venue,
                and an advisory nobody can trace to hardware cannot be investigated or switched
                off alone.
"""


def check(path, s, label):
    try:
        doc = yaml.safe_load(s)
    except Exception as e:
        print("  !! %s would not parse: %s" % (label, str(e)[:180]))
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
    print("    %-14s parses, refs resolve, %d operations intact" % (label, parsed_n))
    return doc


def main():
    apply = "--apply" in sys.argv[1:]
    t = io.open(TEN, encoding="utf-8").read()
    a = io.open(ACC, encoding="utf-8").read()

    if "DeviceCapability:" in t and "advisory:" in a:
        print("  already applied")
        return 0

    if t.count(DEV_ANCHOR) != 1:
        print("  !! RegisteredDevice anchor matched %d times" % t.count(DEV_ANCHOR))
        return 1
    t = t.replace(DEV_ANCHOR, DEV_ANCHOR + DEV_CAPS)
    print("    RegisteredDevice  +capabilities[DeviceCapability]")

    if t.count("\n    ScopeLevel:\n") != 1:
        print("  !! ScopeLevel anchor matched %d times" % t.count("\n    ScopeLevel:\n"))
        return 1
    t = t.replace("\n    ScopeLevel:\n", "\n" + CAP_SCHEMA + "    ScopeLevel:\n")
    print("    DeviceCapability  new enum: genderClassification")

    if a.count(ACC_ANCHOR) != 1:
        print("  !! ValidationResult anchor matched %d times" % a.count(ACC_ANCHOR))
        return 1
    a = a.replace(ACC_ANCHOR, ACC_ANCHOR + ADVISORY)
    print("    ValidationResult  +advisory (transient, never persisted)")

    dt = check(TEN, t, "tenancy.yaml")
    da = check(ACC, a, "access.yaml")
    if dt is None or da is None:
        return 1

    vr = (da["components"]["schemas"].get("ValidationResult") or {})
    if vr.get("x-ticvai-persistence", "").split("—")[0].strip() != "none":
        print("  !! ValidationResult is no longer persistence:none — the advisory would be stored")
        return 1
    print("    ValidationResult persistence is still `none` — the advisory is not stored")

    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    io.open(TEN, "w", encoding="utf-8", newline="\n").write(t)
    io.open(ACC, "w", encoding="utf-8", newline="\n").write(a)
    print("  -> contracts/spine/tenancy.yaml, contracts/spine/access.yaml")
    print("\n  Remaining on BL-179: the steward's display. That is a screen, not a contract.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
