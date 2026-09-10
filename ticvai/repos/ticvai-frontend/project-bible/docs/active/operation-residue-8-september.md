# Operation residue — 8 September 2026

**Operations attached to a screen by module resemblance rather than by what the screen does.**
The pattern was named in `notes/atlas-handoff.md` §2.9 after `BO-003` was cleaned on 24 August —
fifteen order operations removed, *"attached by module resemblance, not by what this screen does"* —
and the check was never re-run. This records the fourth instance and leaves the other three open.

---

## Cleaned — `PTR-010 Cart & Quote`

**A partner reseller's cart screen could create, publish, pause, end and unschedule promotions.**

Found while resolving the `publishGate` gap. Claude Design's 8 September report listed `PTR-010`
among the 33 screens needing the component, flagging it as uncertain on the grounds that it was
*"a gate only because it declares an `activate*` or `promote*` operation."* **That reading was
wrong** — it declared `publishPromotion` outright, which is the least ambiguous kind of match.

The real defect was underneath, and it is §2.9's:

| | |
|---|---|
| Operations declared | **16** |
| P10 median operations per screen | **1** |
| Promotion operations on `PTR-010` | 11 |
| Other P10 screens declaring any | **0** |
| P10 screens named for promotions | **0** |

**Six removed** — `createPromotion`, `updatePromotion`, `publishPromotion`, `pausePromotion`,
`endPromotion`, `unschedulePromotion`. Every one is `trigger: onAction`, and every one is
authoring. **A reseller building a quote evaluates promotions; it does not write them**, and a
partner surface that can publish a venue's promotion is a permission question as much as a
layout one.

**Five kept** — `evaluatePromotions`, `analysePromotionConflicts`, `getPromotion`,
`getPromotionUsage`, `listPromotions`. All `onLoad`, all reads. A cart that cannot say which
promotion applied to it is a quote nobody can check.

**Consequence: the gate rule went enforcing.** `PTR-010` was the last of 35 publishing screens
without `publishGate`, and it was resolved by deleting the operation rather than declaring the
component — which is the right direction when the operation should not have been there. All
remaining screens that publish declare the gate, so `check-screens` now fails on a new one.

---

## Still open — the three from §2.9, unchanged

The 24 August clean-up of `BO-003` was never extended to its neighbours.

| Screen | Declared | Foreign |
|---|---|---|
| `BO-001` Queue Directory | 19 | 6 catalogue, including `createEvent`, `createPerformances` |
| `BO-002` Queue Configuration | 14 | 4 catalogue + 2 seating, including `recommendSeats` |
| `BO-005` Queue Monitor | 19 | 12 marketing-crm, including `launchCampaign`, `stopCampaign` |

**`BO-005` is the one that matters most**, and not only as residue: its declaration is 63%
campaign management, and `CF-33a` is the open question of whether the screen exists at all. Cleaning
it and deciding it are the same conversation.

`BO-003`'s `entryState` also still declares an `orderId` from `deepLink` and a `coldEntry` about
refunded orders — residue of the fifteen operations removed from it in August.

---

## Why this keeps happening

**Every one of these screens passes every checker.** The operations exist, they resolve to real
contracts, and they resolve to real tables. Nothing in the package asks whether an operation has
any business being on the screen that declares it — which is the same shape as the four other
defects found this week: a component derived from an operation that happened to be attached, a
state derived from a screen name, a layout the generator wrote, an operation named after a title.

**A cheap check exists and is not written**: an operation whose contract is not the screen's own
module, on a screen that declares no other operation from that contract, is worth a warning. It
would have caught all four of these.

---

## Found 9 September — the merge process had no screen, and its residue had two

**`matchGuest` and `mergeGuests` were declared by no screen in the package.** The process is fully
decided — drawn on `FnB Board 4`, specified in `marketing-crm` down to the consent rule — and a
designer reading `screens/` could not know it existed.

| | |
|---|---|
| `matchGuest` — *"Is this the same person we already have?"* | cites **Board 4E** = `fnb-4e` = `EMP-055 Create / Edit Reservation` |
| `mergeGuests` — *"Two records, one person"* | cites **Board 4G** = `fnb-4g` = `EMP-057 Guest Profile & Dining History` |

Both screens already declared those exact frames in `wireframe.board`. **The drawing and the
contract agreed all along and the screen sat between them declaring neither.** Wired 9 September,
with a new `duplicateMatch` component and a `confirmDialog` carrying the consequence.

**The residue is `mergeGuestProfiles`, on two screens that have no business with it** —
`BO-036 Device Registry` and `CMS-018 Consent & Legal`. A device registry that can merge guest
records is §2.9's pattern exactly: attached by module resemblance, not by what the screen does.
`BO-036` declares 20 operations of which 8 are guest management.

**And it is a second operation for the same act.** `mergeGuestProfiles` and `mergeGuests` both
merge a duplicate guest, both state the same consent rule in different words — *"the more
restrictive position wins"* against *"produces the narrower of the two"* — and they live in the
same contract. **Two endpoints for one decision is two places to change when the rule moves**, and
the rule here is a regulatory one. One of them should go; which is a contract decision, not a
screen one.

**One warning was accepted rather than suppressed.** `EMP-055` requires the `fnb` module and
`matchGuest` belongs to `marketing`, so `check-screens` now warns that a venue licensing F&B and
not marketing gets a reservation screen that cannot deduplicate. **That is a real licensing
question** — guest deduplication is arguably `core` — and it is better visible as a warning than
hidden by moving the operation without deciding.
