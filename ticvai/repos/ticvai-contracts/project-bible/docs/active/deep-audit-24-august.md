# Deep audit — ten invariants, run adversarially

**24 August 2026.** Not "does it validate" — **what would break in production that nothing here
would notice.**

Ten invariants, each checked across the whole package at once. **Three found real defects, one
found a structural gap that no checker can currently close, and six came back clean** — which is
itself a result worth stating, because a clean result on an invariant nobody had tested before is
new information.

---

## 🔴 Finding 1 — The offline model is prose on one side and a flag on the other

**Severity: high. This is the one that breaks a venue.**

| | |
|---|---:|
| Screens describing offline behaviour in prose | **190** of 481 |
| Operations declaring `x-ticvai-offline-capable` | **173** of 1,016 |
| **Screens claiming they keep working, with no offline-capable operation on load** | **37** |
| GET operations reachable from an offline platform, not flagged | **84** |

**Nothing joins the two.** A screen says *"Selling continues from the cached menu"* and every
operation it loads is flagged `offline: false`. **Both statements pass every check in the suite**,
because no check has ever compared them.

**What breaks:** a till goes offline on a Saturday, the screen renders empty, and the cashier reads
a design document that promised it would work.

**Three of the 37 are mine, written today.** `POS-021`, `POS-023` and the F&B counter screens — I
wrote the offline prose and wired operations that are not offline-capable, in the same hour.

**The fix is not to flip 84 flags.** It is to decide whether `x-ticvai-offline-capable` means *this
operation can be served from cache* or *this operation may be called while offline* — **they are
different properties and the package currently uses the flag for both.** Then a checker can compare
a screen's claim against its operations, and the 37 become a list rather than a surprise.

---

## 🔴 Finding 2 — 27 unbounded list operations over high-volume tables

**Severity: high. This is the one that takes the platform down.**

**94 of 183 `list*` operations declare no page size.** Most are over small tables and it does not
matter.

**27 are over `orders`, `marketing`, `access` or `ledger`** — and those are the tables that grow
without limit:

```
listMyCases            /my/cases
listGuestDevices       /guests/{subjectId}/devices
listGuestMemberships   /guest/memberships
listLoyaltyProgrammes  /loyalty/programmes
listJourneys           /journeys
```

**`marketing.guest_profile` is 37 tables' worth of the largest domain in the package**, and a
campaign send writes millions of `message_dispatch` rows. **An unpaged list over either is a query
that returns the whole table**, and the first venue to notice is the one whose season-ticket base
crossed a hundred thousand.

**`listMyCases` is mine, built today.** I wrote a guest-scoped operation and gave it no page size.

---

## 🔴 Finding 3 — 21 tables are written and never read

**Severity: medium. Each one is a feature that half-exists.**

```
fnb.kitchen_exception          chaseStation, logKitchenException write it
fnb.waitlist_entry             joinRestaurantWaitlist writes it
fnb.combo_slot                 createCombo, setComboSlots write it
maintenance.work_order_attachment  attachWorkOrderEvidence writes it
marketing.privacy_incident     recordPrivacyIncident writes it
control.api_quota              setApiQuota writes it
ai.suggestion_outcome          recordSuggestionOutcome writes it
```

**Every one is a write path with no read path.** A guest joins a restaurant waitlist and **no
operation lists the waitlist**. A steward attaches a photograph to a work order and **nothing
retrieves it**. `setApiQuota` was wired two days ago because the screen for the job could not do
the job — **and nothing reads the quota it sets.**

**`ai.suggestion_outcome` is the sharpest.** It is the label in the feedback loop — *a suggestion of
400 units, an order of 250* — and **the loop has no reader**, so the AI abstraction records outcomes
nothing learns from.

**This is the same defect class as `platform.audit_record` on 20 August**: written by nothing, read
by nothing, found by walking a journey rather than by any checker.

---

## Finding 4 — `signCorrectiveAction` transitions with no operation

**Severity: low, and it is a real one.**

`CorrectiveAction` has one transition — `signed → closed` — that names **no operation**. Every other
transition in 113 state models names one.

**A finding that cannot be closed by any operation is a finding that stays open forever**, which for
a food-safety corrective action means an inspector reads an open list that should be empty.

---

## What came back clean

**These were tested and passed, and none had been tested before.**

**State machines — 113 models.** Zero unreachable states, zero transitions out of a terminal state,
zero dead ends. **The one property I most expected to find broken.**

**Events — 29.** Every one published by something and consumed by something. No orphans in either
direction.

**Entry state — 481 screens.** Not one calls an operation needing a path parameter it never
declares. `check-screens` has enforced this and it holds.

**Idempotency.** 13 of 506 POSTs lack a key and only one touches money — `syncOrders`, which
**carries `deviceId` plus a monotonic `sequence` instead**, which is a stronger replay key than an
idempotency header for a batch. Correct as written.

**Scope escalation.** Five workstation-scoped operations write `platform.*` tables — a device
heartbeat, a redemption consumed, three wallet authorisations. **All five are a till acting on a
platform-owned row through a published path**, which is the append rule working.

**The AI boundary under 8 permissions.** `ai.interaction` is written by twelve operations under
eight permissions, which looked like ADR-0020 breaking. **Every writer is the `ai` contract or the
governed reporting pair** — the permission spread is roles, not services. **The boundary holds.**

---

## What I would fix first, and why

**1 — The 27 unbounded lists.** It is the only finding that takes a running system down, and the fix
is mechanical.

**2 — Decide what `offline-capable` means.** Until that word has one meaning, the 190 screens
describing offline behaviour are documentation nobody can verify — and offline is the property this
platform is sold on.

**3 — The 21 orphan writes**, as 21 separate questions. Each is either a missing read operation or a
table that should not exist, and **guessing which would be worse than leaving them.**

**4 — `signed → closed`.** One line.

---

## The pattern underneath all four

**Every defect here is a join that nothing checks.**

A screen's prose against its operations' flags. A list operation against the size of the table
behind it. A write against the existence of a read. A transition against an operation.

**The package validates each artefact against its own schema and each reference against its target.
It does not validate one artefact's claim against another artefact's fact** — and that is where all
four of these live, along with the 22 audience violations found an hour ago and the 121 bulk-attach
operations found yesterday.

**The checkers that have caught the most are the ones that compare two sources.** That is the shape
worth adding more of.
