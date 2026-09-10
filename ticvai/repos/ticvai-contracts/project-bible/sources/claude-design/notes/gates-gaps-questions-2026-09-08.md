# Gates, gaps and open questions — complete report

> **Superseded in part by the source read later on 8 September — see §5 at the end.** Gates are
> now complete (34, all declared), BP-001 is 337, and 9 of the 74 questions are answered.

**8 September 2026.** Every figure below is measured from the patched package
(`sources/atlas-verify/`) and the frame anchors in this project's boards plus
`sources/old-boards/`. Re-run from `tracker-data.js` and `gaps-questions.json`.

---

## 1 · Gates — 35 real, 2 declared

`publishGate`'s `requiredWhen` keys off the declared operation, so this is machine-checkable:
a screen declares an operation matching `publish*`, `deploy*`, `promote*`, `activate*`, or
`releaseProductionPlan` — the one `release` that really is a publish.

| | |
|---|---|
| Real gates | **35** |
| Of those, declaring `publishGate` | **2** — `BO-094`, `BO-153` |
| **Missing the component** | **33** |
| `relinquish*` screens (renamed, no longer colliding) | **10** |

By platform: **P08 14 · P09 11 · P06 5 · P13 2 · P10 1.** Ten platforms declare none.

Frame state of the 35: 15 framed here, 11 client pack, 6 workshop, **1 drawn nowhere** —
`BO-066 Notification Settings`.

### The 33 that need the component

**P08 (13)** `BO-010` Promotions & Coupons · `BO-011` Packages & Bundles · `BO-013` Channel &
Distribution · `BO-014` Catalogue Publishing · `BO-036` Device Registry · `BO-037` Offline
Package Status · `BO-045` Menu Management · `BO-066` Notification Settings · `BO-124` Layout &
Journey Builder · `BO-126` Deployment, Preview & Audit · `BO-129` Software, Configuration &
Version Management · `BO-136` F&B Global Settings & Controls · `BO-163` Rule Simulation,
Conflict Check & Publication · `BO-183` Media Compatibility, Testing & Publication

**P09 (11)** `ADM-016` White-Label Branding · `ADM-022` Release & Version Management ·
`ADM-023` Staging Promotion & Approval · `ADM-024` Release Notification Composer · `ADM-026`
End-of-Support Notice · `ADM-035` Support & Escalation Console · `ADM-036` Platform Notification
Broadcast · `ADM-084` Pricing Publication & Effective-Date Scheduler · `ADM-124` Channel
Publication & Availability · `ADM-125` Publication & Activation Scheduler · `ADM-267` Channel
Publication, Readiness & AI Validation

**P06 (5)** `EMP-007` Handover notes · `EMP-037` Notifications · `EMP-038` Broadcast to team ·
`EMP-039` Announcements · `EMP-047` Emergency mode

**P13 (2)** `CMS-006` Component Preview · `CMS-014` Publishing Workflow
**P10 (1)** `PTR-010` Cart & Quote

**Two to check before applying.** `PTR-010 Cart & Quote` and `CMS-006 Component Preview` are
gates only because they declare an `activate*` or `promote*` operation. A quote being activated
and a component being previewed are not publications in the sense the component means. Confirm
or exclude them; the other 31 are unambiguous.

### `BO-136` closes the earlier disagreement

`releaseProductionPlan` is a publish — the board-panel map says a plan is edited before it is
released. So real gates are 35, not 34, and `BO-136` is the screen the earlier count missed.

---

## 2 · Contract gaps — 18, in four classes

The rule: the screen's **title** claims publication, deployment or launch, and its **declared
operations** cannot do it. Classing them by what they *can* do makes the remediation different
per class.

### A · Title-only — declares one `list*` and nothing else (11)

The title is the only evidence of a publish. Either the operation is missing or the title is
wrong; both are re-signature work.

| Screen | Declares |
|---|---|
| `BO-173` Credential Security Simulation, Audit & Publication | `listCredentialSecurity` |
| `BO-193` Biometric Simulation, Audit & Publication | `listBiometric` |
| `BO-203` Hardware Compatibility, Health, Testing & Deployment | `listHardwareCompatibilityHealth` |
| `BO-213` Edge Security, Audit & Deployment | `listEdgeSecurityDeployment` |
| `BO-223` Journey Simulation, Audit & Publication | `listJourneys` |
| `BO-233` Operations Audit, Shift Handover & Control Summary | `listShiftHandoverSummary` |
| `ADM-085` Pricing Distribution, Synchronization & Publication Monitor | `listPricingDistributionSynchronization` |
| `ADM-143` Promotion Channel & Publication Monitor | `listPromotionChannel` |
| `ADM-227` Governance Audit, AI Risk & Launch Readiness | `listGovernanceRiskLaunch` |
| `ADM-307` White-Label Marketplace Deployment & Experience Architecture | `listWhiteLabelMarketplace` |
| `CMS-033` Consent Evidence, History & Withdrawal Management | `listConsentEvidenceWithdrawal` |

Six of these — `BO-173`, `BO-193`, `BO-213`, `BO-223`, `ADM-227` and `BO-343` — were the screens
§2.2 of the handoff wanted to give `publishGate`. They were correctly held.

### B · Can approve, cannot publish (5)

A different and more interesting defect: the approval step exists and the publication it
approves does not.

`BO-293` Membership Product Validation, Approval, Publication → `approveMembershipProductValidation`
`BO-353` Multi-Media Preview, Testing, Approval & Publication → `approveMultiMediaPreview`
`ADM-247` Versioning, Governance, Approval & Publication → `approveVersioningGovernance`
`CMS-030` Privacy Configuration Testing, Approval & Publication → `approvePrivacyTesting`
`CMS-050` Waiver Approval, Testing & Publication Workspace → `approveWaiverTesting`

**An approval with nothing to release is a dead end in the workflow, not a naming problem.**
These five are the ones worth raising first.

### C · Monitors something it creates (1)

`ADM-115 Live Dynamic Price Execution & Deployment Monitor` declares
`createLiveDynamicPrice` — it creates prices and calls itself a deployment monitor.

### D · False positive — exclude (1)

`ADM-029 Deployment Monitor` declares twelve operations including `startRollout`,
`pauseRollout`, `rollbackRollout` and `decommissionCell`. It is a real deployment actor; the
title rule caught it because rollout control is not named `publish*`. **Not a gap.** It is,
separately, one of the eight cell-block screens that can decommission a cell.

**So: 17 real gaps, 1 false positive.** The earlier figure of nine came from reading only the
§2.2 patch list; extended package-wide the rule adds `BO-203`, `BO-293`, `BO-353`, `ADM-085`,
`ADM-115`, `ADM-143`, `ADM-247`, `ADM-307`, `CMS-030`, `CMS-050`.

---

## 3 · Open questions — 74 screens, and four of them are one question each

74 screens carry exactly one `openQuestions` entry. But they are **19 distinct questions**, and
the top five account for 60 of the 74.

| Screens | Question |
|---|---|
| **41** | *Inventory cites `<REST path>` — no matching operation. Written before the contracts existed.* — all P02 |
| **8** | *Blocked on the Accreditation workshop. 58 requirements, zero MoM coverage.* — all of P11 |
| **5** | *No contract — new scope, 30 Jul* — `ADM-022`–`ADM-026` |
| **4** | *No contract — not specified* — `ADM-017`, `ADM-028`, `ADM-031`, `ADM-036` |
| **2** | *Blocked — Developer & API workshop* — `ADM-015`, `PTR-019` |

By platform: **P02 41 · P09 18 · P11 8 · P10 3 · P01 2 · P08 1 · P12 1.**

### The 41 are one systemic issue

Every P02 question is the same sentence with a different REST path: `GET /catalogue`,
`GET /wallet`, `POST /tickets/{id}/transfer`, `POST /ai/concierge`, and so on. **The P02
inventory was written against REST paths before the contracts existed**, so none of its screens
resolve to a declared operation. That is one decision — re-map P02's inventory onto the 689
declared operations — not 41 questions. It is also why P02 holds 17 of the 100 screens drawn
nowhere.

### The 8 are one blocked workshop

All of P11 Accreditation. 58 requirements, no MoM coverage, no capability or API mapping until
the domain is discussed. **P11 is 100% framed here** — eight frames drawn against a domain
nobody has specified.

### The 18 P09 questions are almost all the same shape

Thirteen are `No contract — …` with a reason: Control Plane audit not specified, infrastructure
(Terraform not API), platform defaults, the unowned orchestrator, retention, overlaps P12. These
are scope boundaries, not screen defects — several say the screen should not have a contract at
all.

### Five singletons that name a person or a decision

- `WEB-012` — Stripe and Network International sandbox credentials outstanding; recovery paths
  cannot be tested.
- `WEB-015` — CF-48 Q2 Virtual Waiting Room, build-or-buy outstanding with Dinesh and Qossai.
- `BO-006` — awaiting the 14 August MoM; whether parking is barrier integration, space counting
  or pre-booking is unknown. Deliberately undrawn.
- `PTR-011` — quotes are procurement-side only. `PTR-017` — commission not modelled.
- `SUP-003` — agent routing not modelled.

---

## 4 · What to do, in order

1. **Five approve-without-publish screens** (§2B) — a workflow that cannot complete.
2. **Confirm or exclude `PTR-010` and `CMS-006`**, then apply `publishGate` to the other 31.
3. **Re-map P02's inventory** onto declared operations — one decision, 41 questions closed.
4. **Schedule the Accreditation workshop** — one decision, 8 questions closed, 8 drawn frames
   validated or redrawn.
5. **`BO-066`** is a gate drawn nowhere. Draw it or route it to a pattern.
6. Eleven title-only screens (§2A) go on the re-signature list, not the component list.

---

## 5 · Re-read of the source, later on 8 September

Six files changed. **Every item this report flagged has been actioned**, and one was resolved
better than recommended.

### Gates are complete — and the count is 34, not 35

`publishGate` is declared on **34 screens**, and **no screen with a publish-shaped operation is
without it**. Each carries `impliedBy` naming the operation that required it.

**`PTR-010 Cart & Quote` was not excluded — it was fixed at the cause.** Five write operations
were *removed* from it: `createPromotion`, `publishPromotion`, `pausePromotion`,
`endPromotion`, `unschedulePromotion`. It now declares `evaluatePromotions`,
`analysePromotionConflicts`, `getPromotion`, `getPromotionUsage`, `listPromotions` — read and
evaluate only. **A partner cart could publish a promotion; now it cannot.** So it is no longer a
gate at all, which is why 35 became 34. That is the better answer to the question this report
asked, and it is the same class of finding as the cell block: the defect was the operation list,
not the missing component.

`CMS-006 Component Preview` was kept as a gate.

### BP-001 is 337

`searchField` was added to the last two screens carrying the signature without it —
**`ADM-240`** ("Find a rule") and **`CMS-044`** ("Find a field"), the two §2.5 re-signatures
`pattern-data.js` said would match BP-001 once BP-010 folded. **Zero screens now carry
`split` + `dataTable` + `detailPanel` without a `searchField`.** The signature is finally
uniform, and the count the regeneration must produce is **337**.

### The schema id pattern is fixed

`^[A-Z]{3}-[0-9]{3}$` → **`^[A-Z]{2,3}-[0-9]{3}$`**, widened rather than renaming 363 screens,
because the id is what `board-data.js`, the traceability map and every board anchor join on.

### Nine questions answered — but in the `openQuestions` field

- **`BO-006` Parking** answered by the 14 August MoM §10: barrier integration in three models
  (none, ANPR whitelist push, QR handoff), **not** space counting, pay-per-hour out of scope. One
  configuration screen binding a vendor adaptor, not the three screens the question feared.
- **All eight P11 `ACC-` screens** unblocked by the 7 September Accreditation workshop: identity
  documents OCR'd into structured fields rather than images so expiry and renewal can be read,
  uniqueness enforced on passport and Emirates ID, web portal primary and mobile secondary. One
  decision **removes** screens — accreditation-holder monitoring becomes a filtered view inside
  general entitlement monitoring rather than a separate system.

**So 65 questions are open, not 74.** The nine answers are recorded as `openQuestions` entries
beginning *"Answered by…"* / *"Unblocked by…"*, which means **the field now holds both questions
and their resolutions** — the same defect as `wireframe.status` carrying intent and fact, one
field with two meanings. Worth splitting before the count is quoted anywhere: as it stands,
"74 open questions" is wrong and only reading each entry reveals it.

### Unchanged

`wireframe.origin` is still not renamed; `wireframe.provenance` still collides with the
screen-level `provenance` on 128 screens.

### Gaps: no change

Still 17 real plus `ADM-029` as a false positive. The five approve-without-publish screens
(`BO-293`, `BO-353`, `ADM-247`, `CMS-030`, `CMS-050`) are now the only class untouched, and with
gates complete they are the top of the list.
