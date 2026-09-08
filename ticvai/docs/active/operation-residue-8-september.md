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
