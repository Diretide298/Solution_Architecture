#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CF-64's last number, decided: several minutes is the default, near-zero stays selectable.

**Decided 21 September, Chinmay.** *"Make these one default but keep the other a configuration
[the tenant] can select."* Which is the recommendation ADR-0047 left pending, taken — and the
half that matters is the second half, because **a floor that nobody can rise above is not a
floor, it is a ceiling wearing the wrong name.**

    asynchronous    several-minute RPO, the default, what every tenant gets
    synchronous     near-zero RPO, selectable, and only on a pinned instance

## Why the selection has a precondition rather than being a free field

**Synchronous replication puts a network round-trip inside every write transaction.** On a shared
instance that cost is paid by every tenant on the host, including the ones who did not ask for it
and are not paying for it — and the paths it lands on are the two with no headroom to give:
`acquireInventoryHold`, which already serialises on contention and is the package's first
load-test, and `access.scan_event`, which runs tens of thousands of times a day at a gate.

So `synchronous` requires `pinnedInstance`. **That is not a restriction invented for this
decision** — ADR-0042 already says *"the pin is what a dedicated client is actually buying"*, and
a dedicated client is exactly the one who asks for near-zero. One decision serves CF-64 and
CF-168, and the commercial model already carries the pin.

**`CellInstance.supportsSynchronousReplication` is the topology fact underneath.** The same shape
as `DeviceCapability` and `genderVerification: deviceAssisted` a day earlier: **a capability
absent is a capability unavailable, not one assumed.** A tenant cannot select a durability the
host cannot deliver, and the refusal happens at selection rather than silently at the next
failover — which is the only moment anybody would otherwise find out.

## What this does not decide

Backup schedules, replication topology and restore drills stay infrastructure. **CF-60 was right
that 62 of the DR sheet is Dinesh's layer**, and DR-11 and DR-12 ask the platform to *support
configurable* objectives rather than to hit a number. This is the support.

**RTO is deliberately not modelled here.** DR-12 asks for it configurably too, but an RTO is a
promise about how fast an operator restores, not a property a row can carry — it belongs in the
SOW beside the runbook, and a column claiming it would be a column nothing enforces.

    python3 tools/applied/cf-064-rpo-floor-21-september.py --apply
"""
import io
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SUB = os.path.join(ROOT, "contracts", "satellite", "subscription.yaml")
ADR = os.path.join(ROOT, "docs", "adr", "0047-how-long-data-is-kept-and-where-it-goes-next.md")

MODE = """    ReplicationMode:
      type: string
      description: >
        CF-64, decided 21 September. **What a tenant's data durability costs the write path**, and
        therefore what RPO it can be sold.

        `asynchronous` — **the default, and the floor.** A several-minute recovery point, streaming
        replication, one site with a standby. Every tenant gets this and nothing is required of
        them to get it.

        `synchronous` — near-zero recovery point, **selectable rather than standard**, and
        available only on a pinned instance. Every commit waits for a remote acknowledgement, so
        the cost lands inside `acquireInventoryHold` and `access.scan_event` — the two paths in
        this package with the least headroom to give.

        **The floor is a default, not a limit.** DR-11 asks the platform to *support configurable*
        recovery point objectives; a platform that offered exactly one would have answered a
        different requirement.
      enum:
      - asynchronous
      - synchronous

"""

TENANT_OLD = """        pinnedInstance:
          type: boolean
          default: false
"""

TENANT_NEW = """        replicationMode:
          allOf:
          - $ref: '#/components/schemas/ReplicationMode'
          description: >
            CF-64, decided 21 September. **Asynchronous by default; synchronous is a configuration
            a tenant selects and cannot select alone.**

            **`synchronous` requires `pinnedInstance: true`**, and that is not a restriction
            invented for this field. Synchronous replication puts a network round-trip inside
            every write transaction, and on a shared instance that cost is paid by every tenant on
            the host — including the ones who did not ask for it and are not paying for it.
            ADR-0042 already says the pin is what a dedicated client is buying, and a dedicated
            client is exactly who asks for near-zero. **One decision serves CF-64 and CF-168.**

            **Also requires `CellInstance.supportsSynchronousReplication` on the instance that
            holds this tenant.** A capability absent is a capability unavailable, not one
            assumed — the refusal happens when somebody selects it rather than silently at the
            next failover, which is the only other moment anybody would find out.
        pinnedInstance:
          type: boolean
          default: false
"""

INST_OLD = """        maxConnections:
          type: integer
          nullable: true
"""

INST_NEW = """        supportsSynchronousReplication:
          type: boolean
          default: false
          description: >
            CF-64. **Whether this host has the standby and the link to offer a near-zero RPO**, and
            false is the honest default for an instance nobody has built one for.

            **Read rather than assumed**, the same way `maxConnections` is. A tenant selecting
            `replicationMode: synchronous` is refused where its instance reports false, so a
            durability promise cannot be made on behalf of a topology that does not exist.
        maxConnections:
          type: integer
          nullable: true
"""

ADR_OLD = """**The RPO floor**, which is the rest of CF-64 and belongs to Dinesh. The question is *not* what
Miral's RPO is — it is **the tightest RPO any tenant may ever buy**, because offering one near zero
requires synchronous replication and a second site, which is a topology decision made once.
**Recommendation: tie it to ADR-0042's pin** — asynchronous replication with a several-minute RPO as
standard, near-zero available only on a pinned dedicated instance, which is what a dedicated client
is already paying for. One decision then serves two conflicts, and the commercial model already
carries the pin.
"""

ADR_NEW = """**~~The RPO floor~~ — decided 21 September, Chinmay, and the recommendation was taken.**

    asynchronous    several-minute RPO -- the default, and what every tenant gets
    synchronous     near-zero RPO -- selectable, and only on a pinned instance

**The second line is the half that matters.** A floor nobody can rise above is not a floor, it is
a ceiling wearing the wrong name — and DR-11 asks the platform to *support configurable* recovery
point objectives, so a platform offering exactly one would have answered a different requirement.

**`synchronous` requires `pinnedInstance`, and that precondition was not invented for this
decision.** Synchronous replication puts a network round-trip inside every write transaction; on a
shared instance that cost is paid by every tenant on the host, and it lands on the two paths in
this package with the least headroom — `acquireInventoryHold`, which already serialises on
contention and is the first thing to load-test, and `access.scan_event`, which runs tens of
thousands of times a day at a gate. ADR-0042 already holds that *"the pin is what a dedicated
client is actually buying"*, and a dedicated client is exactly who asks for near-zero. **One
decision serves CF-64 and CF-168.**

**`CellInstance.supportsSynchronousReplication` is the topology fact underneath**, in the same
shape as `DeviceCapability`: a capability absent is a capability unavailable rather than one
assumed, and the refusal happens at selection rather than silently at the next failover.

**RTO is deliberately not modelled.** DR-12 asks for it configurably too, but an RTO is a promise
about how fast an operator restores rather than a property a row can carry. It belongs in the SOW
beside the runbook; a column claiming it would be a column nothing enforces.

**What stays with Dinesh is building the standby**, not deciding whether to offer one — backup
schedules, replication topology and restore drills are the 62 DR requirements CF-60 placed in
infrastructure.
"""


def main():
    apply = "--apply" in sys.argv[1:]
    s = io.open(SUB, encoding="utf-8").read()
    a = io.open(ADR, encoding="utf-8").read()

    if "ReplicationMode:" in s:
        print("  already applied")
        return 0

    for label, old, new in (("+ReplicationMode", "    CellTenant:\n", MODE + "    CellTenant:\n"),
                            ("CellTenant  +replicationMode", TENANT_OLD, TENANT_NEW),
                            ("CellInstance  +supportsSynchronousReplication", INST_OLD, INST_NEW)):
        if s.count(old) != 1:
            print("  !! %s anchor matched %d times" % (label, s.count(old)))
            return 1
        s = s.replace(old, new)
        print("    %s" % label)

    if a.count(ADR_OLD) != 1:
        print("  !! ADR-0047 pending paragraph matched %d times" % a.count(ADR_OLD))
        return 1
    a = a.replace(ADR_OLD, ADR_NEW)
    a = a.replace("**Status:** Accepted — two numbers pending sign-off, marked below",
                  "**Status:** Accepted — the RPO floor decided 21 September; "
                  "one number pending sign-off, marked below", 1)
    a = a.replace("**Two numbers, both marked in place above, in the same way ADR-0042 left its "
                  "threshold.**",
                  "**One number left. The RPO floor was decided 21 September and is recorded "
                  "below rather than removed**, because a register that deletes its questions "
                  "when they are answered cannot show what was decided.", 1)
    print("    ADR-0047  RPO floor decided, status line and heading follow")

    try:
        doc = yaml.safe_load(s)
    except Exception as e:
        print("  !! subscription.yaml would not parse: %s" % str(e)[:200])
        return 1
    have = set((doc.get("components") or {}).get("schemas") or {})
    for ref in set(re.findall(r"(?<![\w./-])#/components/schemas/([A-Za-z0-9_]+)",
                              yaml.safe_dump(doc))):
        if ref not in have:
            print("  !! refs %s and does not define it" % ref)
            return 1
    text_n = len(re.findall(r"^      operationId:", s, re.M))
    parsed_n = sum(1 for p in (doc.get("paths") or {}).values() for o in (p or {}).values()
                   if isinstance(o, dict) and o.get("operationId"))
    if text_n != parsed_n:
        print("  !! %d operationId lines, %d parsed" % (text_n, parsed_n))
        return 1
    print("    subscription.yaml  parses, refs resolve, %d operations" % parsed_n)

    modes = doc["components"]["schemas"]["ReplicationMode"]["enum"]
    if modes != ["asynchronous", "synchronous"]:
        print("  !! ReplicationMode is %s" % modes)
        return 1
    ct = doc["components"]["schemas"]["CellTenant"]["properties"]
    if "replicationMode" not in ct or "pinnedInstance" not in ct:
        print("  !! CellTenant is missing the selection or the pin it depends on")
        return 1
    ci = doc["components"]["schemas"]["CellInstance"]["properties"]
    if ci.get("supportsSynchronousReplication", {}).get("default") is not False:
        print("  !! supportsSynchronousReplication does not default to false")
        return 1
    print("    asynchronous is the default · synchronous needs a pin and a host that reports it")

    if "pending sign-off" not in a:
        print("  !! ADR-0047 lost its pending section")
        return 1

    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    io.open(SUB, "w", encoding="utf-8", newline="\n").write(s)
    io.open(ADR, "w", encoding="utf-8", newline="\n").write(a)
    print("  -> contracts/satellite/subscription.yaml, docs/adr/0047-*.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
