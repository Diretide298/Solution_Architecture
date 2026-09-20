#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Two backlog entries closed on what the package actually contains, and one wrong sentence of
mine withdrawn.

`check-backlog` failed on BL-155 — *"blocked on CF-21, which is closed — a blocker that outlives
its conflict hides work that is ready"*. It was right about the mechanism and wrong about the
remedy: **BL-155 is not ready to work, it is finished**, and had been since 18 August.

## BL-155 — outbound webhooks

The entry says *"No outbound webhooks and no third-party workflow integration"* and its `fix`
asks for *"an outbound webhook subscription with signing, retry and replay"*. All three exist,
in `contracts/satellite/public-api.yaml`:

    listWebhookSubscriptions, createWebhookSubscription, listWebhookDeliveries, replayEvents
    signing   WebhookSubscription.signingSecret — "how the receiver knows it was TICVAI"
    retry     WebhookDelivery.status: pending, delivered, failed, retrying, abandoned
    replay    replayEvents, bounded by the retention policy, WebhookDelivery.isReplay

**The entry was blocked on CF-21 and closed by CF-135**, and nothing connected the two. CF-135
walked domain 13, found four separable gaps, and *"events stop at the boundary"* was the fourth —
it built `public-api.yaml` on 18 August and closed. BL-155 sat pointing at a conflict that was
about scheduling workshops.

## BL-160 — and a sentence of mine that was wrong

BL-160 was reopened this morning because its `closedBy` recorded CF-136 device health against an
entry that names three different gaps. That reopening was correct. **What I wrote in
`reopenedWhy` about two of them was not.**

    "no firmware deployment"           CLOSED, and I said so
    "no device enrolment or            I wrote: "No operation retires or decommissions a
     retirement lifecycle"             device". **Wrong.** `enrolDevice` takes the whole
                                       matrix — registered, enrolled, provisioned, active,
                                       deactivated, retired — and has since 16.1.2. I searched
                                       for an operationId containing "retire" and concluded
                                       from its absence, which is not the same thing.
    "no device-to-asset link"          Correct. Nothing joined them in either direction.

**The real defect was worse than the one I named and it was next door.** `enrolDevice` moved a
device through six states and **wrote nothing** — `derive-lineage` had it reading
`platform.device` with an empty `writes` list, because the request body was an anonymous inline
object and the table had no column for `state` or `configurationProfileId`. Its `status` column
is `online/offline/error/consumableLow`, which is health: a decommissioned turnstile still on
the network is `online` and `retired` at once and nothing in the table could say so.

Closed by `bl-160-device-lifecycle-and-asset-link-20-september.py`, which added the three
columns, named the request body so the operation declares its write, and put `deviceId` on
`maintenance.asset` rather than `assetId` on `platform.device` — **`platform` is the foundation
tier and `maintenance` is operations, and a foreign key pointing the other way would have every
cell running a spine carry a column for a satellite it may not deploy.**

    python3 tools/applied/bl-155-and-bl-160-closed-on-evidence-20-september.py --apply
"""
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PATH = os.path.join(ROOT, "handoff", "contract-backlog.json")
TODAY = "2026-09-20"

BL155_CLOSED_BY = (
    "**Built 18 August by CF-135 and never connected back to this entry**, which stayed blocked "
    "on CF-21 — a conflict about scheduling workshops for three uncontracted domains. CF-135 "
    "walked domain 13 and found four separable gaps; *\"events stop at the boundary\"* was the "
    "fourth, and it produced `contracts/satellite/public-api.yaml`.\n\n"
    "All three halves of the stated fix are there. **Signing**: "
    "`WebhookSubscription.signingSecret` — *\"how the receiver knows it was TICVAI\"*. "
    "**Retry**: `WebhookDelivery.status` carries `pending, delivered, failed, retrying, "
    "abandoned`, and `listWebhookDeliveries` is what BO-1078 Monitoring, Retry & Reconciliation "
    "reads. **Replay**: `replayEvents`, bounded by the retention policy (13.3.20), with "
    "`isReplay` on the delivery so a consumer that cannot tell a replay from a live event is not "
    "silently given one.\n\n"
    "**Third-party workflow integration** (11.1.65) is `listIntegrationListings`, "
    "`submitIntegrationListing` and `certifyIntegration`, under ADR-0026's rule that third-party "
    "code does not execute inside TICVAI."
)

BL160_CLOSED_BY = (
    "**Reopened 20 September because the 20 August closure recorded CF-136 device health against "
    "an entry naming three different gaps, and closed the same day against all three.**\n\n"
    "**Firmware deployment** was already done and the entry had never been re-read: "
    "`listDeviceFirmware`, `startDeviceFirmwareRollout`, `rollbackDeviceFirmware`.\n\n"
    "**The lifecycle was half done in a way that looked whole.** `enrolDevice` has taken the "
    "full matrix — registered, enrolled, provisioned, active, deactivated, retired — since "
    "16.1.2, and **wrote nothing**. `derive-lineage` had it reading `platform.device` with an "
    "empty `writes` list, because its request body was an anonymous inline object and the table "
    "had no column for `state` or `configurationProfileId`. `status` is `online/offline/error/"
    "consumableLow`, which is health — **a decommissioned turnstile still on the network is "
    "`online` and `retired` at once**, and neither column could say so. Closed by "
    "`RegisteredDevice` gaining `enrolmentState`, `retiredAt` and `configurationProfileId`, and "
    "by naming the body `DeviceEnrolment` on `platform.device` so the operation declares its "
    "write. The transition reason stays on `tenancy.device_audit` rather than becoming a column, "
    "because the latest transition stored twice is one copy to go stale.\n\n"
    "**The device-to-asset link is `maintenance.asset.deviceId`**, beside `resourceId`, which "
    "already says an AV rig is an asset to maintain and a resource to allocate — a turnstile is "
    "the same sentence. **It lives on the asset and not the device** because `platform` is "
    "TenancyService, tier `foundation`, and `maintenance` is VenueOpsService, tier `operations`, "
    "which already reads from Tenancy in four operations: a foreign key the other way would "
    "invert the tiers and make every cell running a spine carry a column for a satellite it may "
    "not deploy. It is nullable on both sides because most assets are not devices and most "
    "devices are not on the asset register."
)

# The sentence in my own reopening note that was wrong, and what replaces it.
OLD_CLAIM = ("**The other two are not.** No operation retires or decommissions a device — "
             "`revokeDeviceCredential` revokes a credential, which is not a lifecycle — and ")
NEW_CLAIM = ("**The other two were not what I first wrote.** I said no operation retires a "
             "device; `enrolDevice` does, and has since 16.1.2 — I searched for an operationId "
             "containing \"retire\", found none, and concluded from its absence. **The real "
             "defect was next door and worse**: `enrolDevice` moved a device through six states "
             "and wrote nothing, because `platform.device` had no column to hold the state. And ")


def main():
    apply = "--apply" in sys.argv[1:]
    B = json.load(io.open(PATH, encoding="utf-8"))
    by_id = {e["id"]: e for e in B["entries"]}

    for bl in ("BL-155", "BL-160"):
        if by_id[bl].get("status") == "done" and by_id[bl].get("closed") == TODAY:
            print("  already applied")
            return 0

    e = by_id["BL-155"]
    if e.get("blockedOnConflicts") != ["CF-21"]:
        print("  !! BL-155 blockedOnConflicts is %r, expected ['CF-21']"
              % e.get("blockedOnConflicts"))
        return 1
    e["blockedOnConflicts"] = []
    e["blockedOnDomains"] = []
    e["status"], e["lane"], e["closed"] = "done", "settled", TODAY
    e["closedBy"] = BL155_CLOSED_BY
    print("    BL-155  open/deferred -> done/settled · CF-21 and domain 13 blockers cleared")

    e = by_id["BL-160"]
    why = e.get("reopenedWhy") or ""
    if OLD_CLAIM not in why:
        print("  !! BL-160 reopenedWhy does not contain the sentence to withdraw")
        return 1
    e["reopenedWhy"] = why.replace(OLD_CLAIM, NEW_CLAIM)
    e["status"], e["lane"], e["closed"] = "done", "settled", TODAY
    e["closedBy"] = BL160_CLOSED_BY
    print("    BL-160  open/decision -> done/settled · reopening note corrected")

    n_open = sum(1 for x in B["entries"] if x.get("status") == "open")
    print("    %d entries · open now %d" % (len(B["entries"]), n_open))

    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    io.open(PATH, "w", encoding="utf-8", newline="\n").write(
        json.dumps(B, indent=1, ensure_ascii=False))
    print("  -> handoff/contract-backlog.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
