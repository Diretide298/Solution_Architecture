#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BL-160, reopened on 20 September: the lifecycle operation that writes nothing, and the
turnstile that cannot raise a work order against itself.

BL-160 was marked `done` and its `closedBy` describes `RegisteredDevice` gaining `batteryPercent`
and `Workstation` gaining `healthScore` — **which is CF-136, device health, and not one of the
three gaps the entry states.** Re-reading the three against the package:

    "no firmware deployment"                CLOSED. listDeviceFirmware,
                                            startDeviceFirmwareRollout, rollbackDeviceFirmware
    "no device enrolment or retirement      HALF closed. `enrolDevice` takes the whole matrix —
     lifecycle"                             registered -> enrolled -> provisioned -> active ->
                                            deactivated -> retired — and **writes nothing.**
    "no device-to-asset link"               OPEN. Nothing joins platform.device to
                                            maintenance.asset in either direction.

**The lifecycle gap is sharper than the entry states it.** The operation is not missing; it has
nowhere to write. `enrolDevice` accepts a `state` and a `configurationProfileId`, and
`platform.device` carries neither — its `status` column is `online/offline/error/consumableLow`,
which is *health*, and a device can be `online` and `retired` at the same time without either
column contradicting the other. `derive-lineage` had already noticed: `enrolDevice` reads
`platform.device` and its `writes` list is empty, because the request body is an anonymous inline
object and lineage follows `$ref`s.

## Three changes

    RegisteredDevice     +enrolmentState, +retiredAt, +configurationProfileId
    DeviceEnrolment      new, x-ticvai-persistence: platform.device
                         enrolDevice's request body, which is what gives it its write
    Asset                +deviceId  ->  platform.device

**The reason does not become a column.** `tenancy.device_audit` already carries `action`,
`previousValue`, `newValue`, `actorPrincipalId` and `at` — the transition history is recorded
there and duplicating the latest one onto the device is two places to read and one to go stale.
**`retiredAt` is a column anyway**, because a retirement date you reconstruct from an audit log
is a date nobody filters on, and `maintenance.asset.retired_on` is the precedent three feet away.

## The link goes on the asset, and the tier decides it

| | |
|---|---|
| **Maintainability** | **the asset.** Not every device is on the asset register — a signature pad is not — and not every asset is a device. A sparse optional link belongs on the side that is sparse about it |
| **Readability** | **the asset.** `resourceId` is already there saying *"an AV rig is an asset to maintain and a resource to allocate"*; a turnstile is an asset to maintain and a device to operate, and that is the same sentence |
| **Optimised access** | **the asset.** *"Which asset is this broken turnstile"* is the query, and it is asked when somebody opens a work order |
| **DB strain** | **the asset.** `platform.device` is written on every heartbeat and read on every telemetry call. `maintenance.asset` is read when a work order opens. Widening the hot table for the cold reader is the wrong way round |
| **Cross-cell** | **the asset, and this is the one that settles it.** `platform` is TenancyService, tier `foundation`. `maintenance` is VenueOpsService, tier `operations`, and it already reads from TenancyService in four operations. Putting `assetId` on `platform.device` makes the foundation tier hold a foreign key into an operations schema — **a tier inversion**, and every cell that runs a spine would carry a column for a satellite it may not deploy |

    python3 tools/applied/bl-160-device-lifecycle-and-asset-link-20-september.py --apply
"""
import io
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEN = os.path.join(ROOT, "contracts", "spine", "tenancy.yaml")
MNT = os.path.join(ROOT, "contracts", "satellite", "maintenance.yaml")

# --- A. the lifecycle columns, onto RegisteredDevice ------------------------------------------

DEVICE_ANCHOR = "        lastHeartbeatAt: { type: string, format: date-time, nullable: true }\n"

DEVICE_COLS = """        enrolmentState:
          type: string
          enum: [registered, enrolled, provisioned, active, deactivated, retired]
          default: registered
          description: >
            BL-160. **Where the device is in its life, which is not the same question as whether
            it is answering.** `enrolDevice` has taken the whole matrix — registered, enrolled,
            provisioned, active, deactivated, retired — since 16.1.2, and until now there was no
            column for it to land in, so the operation read this table and wrote nothing.

            **Distinct from `status` and from `health`.** `status` is what the device last said
            and `health` is what we computed from it; a decommissioned turnstile still sitting on
            the network is `online` and `retired` at once, and neither column contradicts the
            other. **A device that is `retired` is refused at the gate whatever its status says.**

            The transition itself — who moved it, from what, and why — is a
            `tenancy.device_audit` record. It is not repeated here, because the latest transition
            stored in two places is one place to go stale.
        retiredAt:
          type: string
          format: date-time
          nullable: true
          description: >
            **Set when `enrolmentState` reaches `retired`, and null otherwise.** Derivable from
            `tenancy.device_audit`, and kept as a column for the same reason
            `maintenance.asset.retired_on` is one: a retirement date you reconstruct from an audit
            log is a date nobody filters a fleet by.
        configurationProfileId:
          type: string
          format: uuid
          nullable: true
          description: >
            **The profile this device was provisioned with.** `enrolDevice` has accepted one since
            16.1.3 and there was nowhere to keep it, so the answer to *"what is this reader
            configured as"* lived only in the request that set it.
"""

ENROLMENT_SCHEMA = """    DeviceEnrolment:
      x-ticvai-persistence: "platform.device"
      type: object
      description: >
        BL-160. **The body `enrolDevice` accepts, named so that it writes.**

        It was an anonymous inline object, and `derive-lineage` reads writes from the schema an
        operation accepts — so the one operation that moves a device through its whole lifecycle
        recorded no writes at all, and `platform.device` looked like a table only
        `registerDevice` touched.

        **Provisioning is inside enrolment rather than beside it**, which is why
        `configurationProfileId` is here: a device that is enrolled but unprovisioned is a device
        that will fail at the gate on its first morning.
      required:
      - state
      properties:
        state:
          type: string
          enum:
          - enrolled
          - provisioned
          - active
          - deactivated
          - retired
          description: >
            **The target state, not the current one.** `registered` is absent because
            `registerDevice` is what produces it and nothing transitions back to it.
        configurationProfileId:
          type: string
          format: uuid
          nullable: true
        reason:
          type: string
          nullable: true
          description: >
            **Recorded on the `tenancy.device_audit` row, not on the device.** Required in
            practice for `deactivated` and `retired`, where an investigation six months later
            needs to know why a gate stopped working.

"""

OLD_BODY = """      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
              - state
              properties:
                state:
                  type: string
                  enum:
                  - enrolled
                  - provisioned
                  - active
                  - deactivated
                  - retired
                configurationProfileId:
                  type: string
                  format: uuid
                  nullable: true
                reason:
                  type: string
                  nullable: true
"""

NEW_BODY = """      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/DeviceEnrolment'
"""

# --- C. the asset link ------------------------------------------------------------------------

ASSET_ANCHOR = """                **`resources` owns the calendar and this owns the condition.** An asset out of service
                makes its resource unbookable, which is one link rather than two models of availability.
"""

ASSET_COL = """            deviceId:
              type: string
              format: uuid
              nullable: true
              description: >
                BL-160. **Where this asset is also a registered device.** A turnstile is an asset
                to maintain and a device to operate, and — exactly as with `resourceId` above —
                they are the same object seen from two sides.

                **Nothing joined them before this.** A turnstile controller reporting
                `needsAttention` could not raise a work order against itself, and an engineer
                closing one had no way back to the device whose firmware caused it.

                **Null for most assets and for most devices.** A chiller is not a device and a
                signature pad is not on the asset register; the link is sparse, and it lives here
                rather than on `platform.device` because `platform` is the foundation tier and a
                foreign key pointing from it into `maintenance` would invert the tiers — every
                cell running a spine would carry a column for a satellite it may not deploy.
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
    print("    %-16s parses, refs resolve, %d operations intact" % (label, parsed_n))
    return doc


def main():
    apply = "--apply" in sys.argv[1:]
    t = io.open(TEN, encoding="utf-8").read()
    m = io.open(MNT, encoding="utf-8").read()

    if "enrolmentState:" in t and "DeviceEnrolment:" in t and "deviceId:" in m:
        print("  already applied")
        return 0

    if t.count(DEVICE_ANCHOR) != 1:
        print("  !! RegisteredDevice.lastHeartbeatAt matched %d times" % t.count(DEVICE_ANCHOR))
        return 1
    t = t.replace(DEVICE_ANCHOR, DEVICE_ANCHOR + DEVICE_COLS)
    print("    RegisteredDevice  +enrolmentState +retiredAt +configurationProfileId")

    if t.count("\n    ScopeLevel:\n") != 1:
        print("  !! ScopeLevel anchor matched %d times" % t.count("\n    ScopeLevel:\n"))
        return 1
    t = t.replace("\n    ScopeLevel:\n", "\n" + ENROLMENT_SCHEMA + "    ScopeLevel:\n")
    print("    DeviceEnrolment   new schema on platform.device")

    if t.count(OLD_BODY) != 1:
        print("  !! enrolDevice request body matched %d times" % t.count(OLD_BODY))
        return 1
    t = t.replace(OLD_BODY, NEW_BODY)
    print("    enrolDevice       body named -> the operation now writes platform.device")

    if m.count(ASSET_ANCHOR) != 1:
        print("  !! Asset.resourceId anchor matched %d times" % m.count(ASSET_ANCHOR))
        return 1
    m = m.replace(ASSET_ANCHOR, ASSET_ANCHOR + ASSET_COL)
    print("    Asset             +deviceId -> platform.device")

    dt = check(TEN, t, "tenancy.yaml")
    dm = check(MNT, m, "maintenance.yaml")
    if dt is None or dm is None:
        return 1

    body = (dt["paths"]["/devices/{deviceId}/enrolment"]["post"]["requestBody"]
            ["content"]["application/json"]["schema"])
    if body.get("$ref") != "#/components/schemas/DeviceEnrolment":
        print("  !! enrolDevice body did not land on DeviceEnrolment")
        return 1
    print("    enrolDevice body -> DeviceEnrolment, persistence platform.device")

    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    io.open(TEN, "w", encoding="utf-8", newline="\n").write(t)
    io.open(MNT, "w", encoding="utf-8", newline="\n").write(m)
    print("  -> contracts/spine/tenancy.yaml, contracts/satellite/maintenance.yaml")
    print("\n  derive-schema and derive-lineage pick up the columns and the write on the next run.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
