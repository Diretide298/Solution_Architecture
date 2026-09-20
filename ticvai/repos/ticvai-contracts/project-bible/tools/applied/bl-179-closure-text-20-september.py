#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rewrite BL-179's closure note, which a shell ate.

The first attempt passed the text through `bash -c "..."`, where a backtick pair is command
substitution — so every `` `identifier` `` in the note was executed instead of quoted, and
`RegisteredDevice.capabilities` came back as *command not found* with a hole where the name
should be. **The repo's own note about this says to use the Write tool rather than a shell
string**, and this is what happens when that is skipped.

The entry closed correctly; only the prose was damaged.
"""
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PATH = os.path.join(ROOT, "handoff", "contract-backlog.json")

CLOSED_BY = (
    "**Closed 20 September.** `RegisteredDevice.capabilities` carries a `DeviceCapability`, "
    "whose first member is `genderClassification` — so a driver can now report what it does, and "
    "`segregatedAccess.genderVerification: deviceAssisted` stops being a switch with nothing "
    "behind it. **A capability absent is a capability unavailable, not one assumed**: a venue "
    "setting that needs hardware is refused where no device in scope reports it, rather than "
    "silently doing nothing at the gate.\n\n"
    "`ValidationResult.advisory` is the path to the steward — a classification, a **confidence** "
    "and the device that reported it. The confidence is not decoration: "
    "`overrideRateAlertThreshold` already exists to catch a steward who has stopped deciding, and "
    "**that number means nothing unless the steward could see how sure the device was.**\n\n"
    "**It is never persisted, and that is a PDPL position rather than a storage preference.** An "
    "inferred classification kept against a guest is sensitive personal data with no consent "
    "behind it — **a guest agreed to be admitted, not to be classified.** Face Pass and Face Tag "
    "carry `consent_purpose_id` and `consent_given_at` because somebody enrolled; **nobody enrols "
    "in being looked at by a turnstile.** `ValidationResult` stays "
    "`x-ticvai-persistence: none`, so `access.scan_event` records that an override happened and "
    "never what the device thought — which keeps the override-rate metric working without "
    "building a register nobody agreed to.\n\n"
    "**Advisory, never decisive.** It cannot reach `outcome` or `denyReason`, and "
    "`entitlementGated` stays `true` and read-only: the gate admits on the entitlement and "
    "everything else sits on top without replacing it. 3.2.45 asks for rejection and CF-130 "
    "records why the package deviates — a Ladies Night ticket is already gendered at the point of "
    "sale, and these events are staffed.\n\n"
    "**Remaining: the steward's display, which is a screen rather than a contract.**"
)


def main():
    apply = "--apply" in sys.argv[1:]
    B = json.load(io.open(PATH, encoding="utf-8"))
    e = next(x for x in B["entries"] if x["id"] == "BL-179")
    if e.get("closedBy") == CLOSED_BY:
        print("  already applied")
        return 0
    before = len(e.get("closedBy") or "")
    e["closedBy"] = CLOSED_BY
    print("    BL-179 closedBy  %d chars -> %d" % (before, len(CLOSED_BY)))
    print("    status %s · lane %s · closed %s"
          % (e.get("status"), e.get("lane"), e.get("closed")))
    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    io.open(PATH, "w", encoding="utf-8", newline="\n").write(
        json.dumps(B, indent=1, ensure_ascii=False))
    print("  -> handoff/contract-backlog.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
