#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The ten open backlog entries, re-tested against the package rather than re-read.

BL-155 was closed today after sitting blocked on CF-21 — a conflict about scheduling workshops —
while CF-135 built what it asked for on 18 August. BL-160 was closed in August against evidence
for a different gap. **Both failures are the same one: an entry is written once and then only
ever re-read, never re-run against the package.** So all ten open entries were re-tested.

Six are genuinely open and stay untouched: **BL-073** (cookie consent, blocked on CF-127),
**BL-096**, **BL-105** and **BL-106** (all blocked on CF-35, biometrics and PDPL), **BL-110**
(ABAC against a deliberately role-based model, 43 rows, an architecture decision) and
**BL-179**, whose fix is fully specified and which nothing blocks — `check-backlog` warns about
exactly that and it is right to.

Four move.

## BL-161 — closed. All six requirements are contracted

*"A device does not authenticate to the platform, and there is no tamper detection. **Nothing
anywhere** for device authentication, device authorisation, encrypted device communication or
tamper detection."*

Every one of its six refs is now claimed in `contracts/spine/tenancy.yaml`, by name:

    16.7.35-37   issueDeviceCredential — "Give the device an identity it can prove.
                 A device that authenticates with a shared key is a device that cannot be
                 revoked alone." Plus revokeDeviceCredential and the DeviceCredential
                 schema on tenancy.device_credential, per device, with an expiry
    16.7.38-39   listDeviceAuditRecords, on tenancy.device_audit — administration and
                 access interleaved, "because an investigation needs the order"
    16.7.40      listDeviceTamperEvents and recordDeviceTamperEvent, on
                 tenancy.device_tamper_event — "a state, not a log line"

**Its blocker was CF-64, which is retention and RPO.** Nothing in CF-64 touches device
authentication. That is the BL-155 failure exactly — a blocker naming a conflict about a
different subject, holding an entry shut long after the work landed — and it is the second
instance found today, which makes it a pattern rather than an accident.

## BL-173 — narrowed to leaderboards, and this is the one worth being careful about

Its traceability rows read `CONTRACTED` against `Challenge`, and **most of it is built**:
`createChallenge` ("define a challenge, mission or streak"), `getMyChallenges`, `listBadges`,
`setBadge`, `awardBadge`, `listCustomerBadges`, and `Challenge.kind` carrying `streak` and
`milestone`.

**It is not closed, because it names leaderboards and there is no leaderboard.** The screen
`BO-831 Progress, Leaderboards & Hub` is served by `getLoyaltyPosition`, which returns *a
guest's own points and tier* — no operation anywhere returns guests ranked against each other,
and `Challenge` has no ranking field. **Closing this entry on the strength of `Challenge`
resolving would be the BL-160 mistake with today's date on it**: a schema that exists is not
evidence for a gap it does not address.

## BL-100 — narrowed to three of the eight things it names

Present now: auto-renewal (`setRenewalAutoMembership`, `listRenewalAuto`,
`autoRenewEligible`), grace periods (`graceDays`), billing cycles, downgrade, and mandates in
`payments`. **Absent: dunning, retry schedules and billing statements** — none of the three
appears anywhere in `contracts/`.

**And the entry's own argument has been overtaken.** It said *"`subscription` looks like the
answer and is not — it is the Control Plane, and a guest paying monthly for an annual pass is a
different ledger, a different payer and a different failure mode."* `setRenewalAutoMembership`
and `listMembershipRenewalRetention` are guest membership billing and they are **in
`subscription.yaml`**. Either the boundary moved deliberately or guest billing landed in the
control-plane contract; **that is a decision, so it is recorded here and not made.**

## BL-140 — given the blocker it always had

Its refs include 5.7.93. CF-133 opens *"the platform cannot issue a tax invoice, and in the UAE
that is a VAT obligation rather than a document feature — 5.7.93 requires tax invoices..."*
**The same requirement, open with the client, and the entry recorded no blocker at all.** The
inverse of BL-155: there a blocker outlived its conflict, here a conflict never reached its
entry, and both leave the register saying something untrue about what is ready to work.

    python3 tools/applied/open-backlog-retested-20-september.py --apply
"""
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PATH = os.path.join(ROOT, "handoff", "contract-backlog.json")
TODAY = "2026-09-20"

BL161_CLOSED_BY = (
    "**All six requirements are contracted in `contracts/spine/tenancy.yaml`, each naming its "
    "ref.** 16.7.35–37: `issueDeviceCredential` — *\"give the device an identity it can prove\"*, "
    "with `revokeDeviceCredential` and the `DeviceCredential` schema on "
    "`tenancy.device_credential`, per device and with an expiry, because **a device that "
    "authenticates with a shared key is a device that cannot be revoked alone** and one "
    "compromised scanner should not mean re-keying an estate. 16.7.38–39: "
    "`listDeviceAuditRecords` on `tenancy.device_audit`, administration and access interleaved "
    "*\"because an investigation needs the order\"*. 16.7.40: `listDeviceTamperEvents` and "
    "`recordDeviceTamperEvent` on `tenancy.device_tamper_event` — **a state, not a log line**, "
    "so a device that reported tampering is untrusted until somebody clears it.\n\n"
    "**Blocked on CF-64, which is retention and RPO and has nothing to do with device "
    "authentication.** Second instance today of a blocker naming an unrelated conflict, after "
    "BL-155 on CF-21 — the register was holding two entries shut against subjects they do not "
    "share. `offlineScope` on `RegisteredDevice` answers the entry's remaining question of what "
    "an unattended device may do without a connection; **`fullVenue` on a personal handset is a "
    "decision, not a default.**"
)

BL173_NARROWED = (
    "No leaderboard. **Challenges, streaks, milestones, badges and achievements are built** — "
    "`createChallenge`, `getMyChallenges`, `listBadges`, `setBadge`, `awardBadge`, "
    "`listCustomerBadges`, and `Challenge.kind` carries `streak` and `milestone`. **Ranking "
    "guests against each other is not.** `BO-831 Progress, Leaderboards & Hub` is served by "
    "`getLoyaltyPosition`, which returns a guest their own points and tier, and `Challenge` has "
    "no ranking field."
)
BL173_WHY = (
    "\n\n**Narrowed 20 September.** The traceability rows read `CONTRACTED` against `Challenge` "
    "and the entry stayed open — correctly, because it names leaderboards and `Challenge` does "
    "not address them. **Closing it on the strength of that schema resolving would repeat the "
    "BL-160 mistake**: a schema that exists is not evidence for a gap it does not answer. A "
    "leaderboard also asks a question the rest of gamification does not — **what one guest may "
    "see of another**, which is a privacy decision before it is an operation."
)

BL100_NARROWED = (
    "No dunning, no retry schedule and no billing statement. **Auto-renewal, grace periods, "
    "billing cycles, downgrade and mandates now exist** — `setRenewalAutoMembership`, "
    "`listRenewalAuto`, `autoRenewEligible`, `graceDays`, and mandates in `payments`. The "
    "three that remain appear nowhere in `contracts/`."
)
BL100_WHY = (
    "\n\n**Narrowed 20 September, and the entry's own argument has been overtaken.** It said "
    "*\"`subscription` looks like the answer and is not — it is the Control Plane, and a guest "
    "paying monthly for an annual pass is a different ledger, a different payer and a different "
    "failure mode.\"* `setRenewalAutoMembership` and `listMembershipRenewalRetention` are guest "
    "membership billing and **they are in `subscription.yaml`**. Either the boundary moved "
    "deliberately or guest billing landed in the control-plane contract; **that is a boundary "
    "decision and it is recorded rather than made.** Five of the eight capabilities this entry "
    "named are served; the stored-card and PCI scope it warned about arrived with them and has "
    "not been re-examined."
)

BL140_WHY = (
    "\n\n**Blocked on CF-133 from 20 September, which it always was.** This entry recorded no "
    "blocker while CF-133 — open with the client — opens *\"the platform cannot issue a tax "
    "invoice, and in the UAE that is a VAT obligation rather than a document feature. 5.7.93 "
    "requires tax invoices...\"* **5.7.93 is this entry's own first reference.** The inverse of "
    "BL-155, where a blocker outlived its conflict: here a conflict never reached its entry, and "
    "both leave the register wrong about what is ready to work."
)


def main():
    apply = "--apply" in sys.argv[1:]
    B = json.load(io.open(PATH, encoding="utf-8"))
    by_id = {e["id"]: e for e in B["entries"]}

    if by_id["BL-161"].get("status") == "done":
        print("  already applied")
        return 0

    e = by_id["BL-161"]
    if e.get("blockedOnConflicts") != ["CF-64"]:
        print("  !! BL-161 blockedOnConflicts is %r, expected ['CF-64']"
              % e.get("blockedOnConflicts"))
        return 1
    e["blockedOnConflicts"] = []
    e["status"], e["lane"], e["closed"] = "done", "settled", TODAY
    e["closedBy"] = BL161_CLOSED_BY
    print("    BL-161  open/decision -> done/settled · CF-64 blocker cleared (it is retention)")

    for bl, what, why in (("BL-173", BL173_NARROWED, BL173_WHY),
                          ("BL-100", BL100_NARROWED, BL100_WHY)):
        e = by_id[bl]
        e["narrowed"] = TODAY
        e["whatBefore"] = e["what"]
        e["what"] = what
        e["why"] = (e.get("why") or "") + why
        print("    %s  narrowed, stays open" % bl)

    e = by_id["BL-140"]
    if e.get("blockedOnConflicts"):
        print("  !! BL-140 already has a blocker: %r" % e.get("blockedOnConflicts"))
        return 1
    e["blockedOnConflicts"] = ["CF-133"]
    e["why"] = (e.get("why") or "") + BL140_WHY
    print("    BL-140  blocked on CF-133 · the conflict that names its own first reference")

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
