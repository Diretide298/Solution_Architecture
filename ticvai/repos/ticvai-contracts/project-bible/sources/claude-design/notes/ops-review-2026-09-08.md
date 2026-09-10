# Operations review, re-run

**8 September 2026.** Phase B. The 7 September review covered ADM-001–037 of a platform that
declares 318, and P08's review plan was written when P08 was 143 screens. Both re-run here
against the current YAMLs, plus the whole package where the question needed it.

Method: parse every screen block in `screens/P*.yaml`, take `apis[].operationId` as declared,
compare declared operation sets across screens. 1,091 screens, 15 platform files.

---

## 1 · The cell block holds, and it is not a pattern

The original finding: six screens declare an identical seven-operation cell block, so a WAF
policy view, a backup status page and an archival monitor can each decommission a cell. It
could not be called a pattern until tested against the other 281.

**Tested. It is eight screens, and it is not a pattern — it is one stamped base.**

| Screen | Ops | Beyond the seven |
|---|---|---|
| ADM-003 Cross-Tenant Health Dashboard | 10 | cross-region propagate, get, reconcileRedemptions |
| ADM-013 Tenant Performance Monitor | 7 | — |
| ADM-014 Auto-Scaling Configuration | 8 | getScalingPolicy |
| ADM-029 Deployment Monitor | 12 | rollout list, get, start, pause, rollback |
| ADM-030 Infrastructure Sizing & Scaling Policy | 9 | get + setScalingPolicy |
| ADM-032 WAF & Security Policy View | 9 | listWafRules, setWafPolicy |
| ADM-033 Backup & DR Status | 8 | listBackupRuns |
| ADM-034 Archival Job Monitor | 8 | listArchivalJobs |

All eight declare `getCell`, `getCellHealth`, `getCellCapacity`, `listCellJobs`,
`updateCellTier`, `decommissionCell`, `cancelDecommission`. **All eight can decommission a
cell** — including the WAF view, the backup page and the archival monitor, which was the
original point and is now two screens worse.

What changed is the diagnosis. Only ADM-013 declares the seven and nothing else; the other
seven add their own operations on top. So this is a **base applied to anything infrastructure-
shaped**, not a duplicated screen. And across all 318 screens there is exactly **one** other
identical repeated operation set in the entire platform:

- **ADM-022 Release & Version Management** and **ADM-023 Staging Promotion & Approval** —
  the same seven release operations, `listReleases` through `withdrawRelease`. One is a `form`,
  one is a `wizard`, and they declare the same capability.

Two repeats in 318 screens means the cell block is not a generator habit that will keep
recurring. It is a specific eight-screen defect, fixable by removing `decommissionCell` and
`cancelDecommission` from the six screens that only observe.

---

## 2 · P09 as it now stands · 318 screens

541 operation declarations, 402 distinct operations. No screen declares zero.

**Templates:** `split` 212 · `dashboard` 75 · `form` 15 · `detail` 9 · `list` 6 · `wizard` 1.
Two thirds of the platform is one template.

**Read-only:** 216 of 318 screens declare only `list…` and `get…` operations. **279 of 318
declare exactly one operation.**

**Contracts**, by declaration count: `catalogue` 110 · `promotions` 100 · `orders` 40 ·
`approvals` 21 · `subscription` 19 · `platform-ops` 16 · `identity` 13 · `marketing-crm` 10 ·
the rest in single figures. The 281 screens the first review never reached are almost entirely
catalogue and promotions — which is why it found the cell block and nothing like it. **The
reviewed 37 and the unreviewed 281 are different populations**, and the first review's findings
should not be read as a sample of the platform.

**46 read-only screens carry a verb in their title.** ADM-081 Pricing Version *Management*
declares `listPricingVersionBaseline` and nothing else. ADM-132 Rollback & Recovery
*Management* declares `listRollbackRecovery`. ADM-160 Unique Code *Generation* & Batch
*Manager* declares `listUniqueCodeGeneration`. None can do what its name says.

---

## 3 · P08 as it now stands · 363 screens

1,114 operation declarations, 666 distinct. No screen declares zero.

**Templates:** `split` 172 · `list` 68 · `detail` 65 · `dashboard` 50 · `form` 4 ·
`calendar` 1 · **absent 3** — BO-092, BO-093, BO-094, confirming §2.4 of the handoff has not
been applied.

**227 of 363 declare exactly one operation.** 166 are read-only; 28 of those carry a verb in
the title (BO-319 Void, Reversal & Same-Day Correction *Management* → `listVoidReversalSame`).

**Five repeated identical operation sets, 14 screens** — and unlike P09's, these are the
*authored* screens duplicating each other:

| Screens | Ops | Shared block |
|---|---|---|
| BO-039 BO-040 BO-041 BO-042 | 13 | the full shift block — open, close, cash movements, variance |
| BO-022 BO-026 BO-047 | 14 | the full order block — create, modify, refund, exchange, discount |
| BO-029 BO-059 BO-061 | 9 | the report block — create, run, save NL query, delete |
| BO-015 BO-016 | 11 | event and performance CRUD + seat availability |
| BO-051 BO-070 | 13 | the order block minus refunds |

Four screens that can each close a shift and record a cash movement is the same class of
finding as the cell block, in the module where money is counted. **This is the P08 equivalent
and it was not in any earlier note.**

**Contracts:** `access` 156 · `orders` 69 · `tenancy` 39 · `fnb` 24 · `subscription` 21 ·
`catalogue` 19 · `inventory` 16 · `finance` 15 · `reporting` 14 · rest in single figures.
Access is 43% of the platform's declarations, which matches the assembly board's 175-screen
Access & Venue section.

---

## 4 · The generator default, measured

The 7 September note asserted that operation names are titles camel-cased, so the API and the
layout agreeing proves nothing. That is now a number.

**360 of 1,091 screens declare exactly one operation, and that operation is `list` + the
screen's own title camel-cased.** 637 screens declare exactly one operation at all.

| | Screens | 1-op | stamped | |
|---|---|---|---|---|
| P09 | 318 | 279 | **175** | 55% |
| P08 | 363 | 227 | **137** | 38% |
| P10 | 51 | 31 | 19 | 37% |
| P13 | 60 | 44 | 21 | 35% |
| P12 | 28 | 21 | 8 | 29% |
| P01 P02 P04 P05 P06 P07 P11 P14 P15 P16 | 271 | 35 | **0** | 0% |

Ten platforms produce zero. The five generated ones produce all 360. **The stamp is not a
package-wide property, it is a property of five files** — which makes the first CI check
shippable now: enforce it on the ten clean platforms today, warn on the five until
re-signature. A check that can only warn everywhere is a check nobody fixes.

---

## 5 · `publishGate` scope — the blocking decision, with numbers

The handoff asks whether `requiredWhen` ships enforcing or warning, noting it fires on more
than the eight screens named. It fires on **45**.

**34 are real gates**: something goes live. `publishAnnouncement` (7 screens, mostly P06 staff
broadcast), `publishBundle` (4), `deployConfigurationProfile` (4), `publishSupportNotice` (4),
`publishTenantConfig` (3), `promoteRelease` (2), `publishPromotion` (2), plus eleven
one-of-a-kind publish operations. **None of the 34 currently declares `publishGate`.**

**11 are a naming collision.** `release` there means *let go of a hold*, the opposite of
publishing: `releaseInventoryHold` (POS-003, BO-018), `releaseSeatHold` (POS-004),
`releaseSeatBlock` (PTR-009), `releaseStoredValue` (BO-097), `releaseChannelAllocation`
(EMP-033, BO-017, PTR-005), `releaseCustomDomain` (ADM-017, CMS-017),
`releaseProductionPlan` (BO-136). A gate on any of these would ask an operator to confirm the
publication of a seat hold being dropped.

### The patch's own list does not survive this

Of the seven screens §2.2 names, **six declare no publish-shaped operation at all**:

| Screen | Declares | |
|---|---|---|
| BO-153 Topology Validation & Publication | `publishTopologyValidation` | real gate |
| BO-173 Credential Security Simulation, Audit & Publication | `listCredentialSecurity` | title only |
| BO-193 Biometric Simulation, Audit & Publication | `listBiometric` | title only |
| BO-213 Edge Security, Audit & Deployment | `listEdgeSecurityDeployment` | title only |
| BO-223 Journey Simulation, Audit & Publication | `listJourneys` | title only |
| BO-343 Virtual Ticket Architecture Testing, Governance & Audit | `listVirtualTicketArchitecture` | title only |
| ADM-227 Governance Audit, AI Risk & Launch Readiness | `listGovernanceRiskLaunch` | title only |

All seven are BP-006 screens — `dashboard` · `timeline` · `searchField`. **The publish list was
read off their titles**, which is the same evidence CI check 1 exists to reject. Either those
six publish and are missing an operation — a contract gap, like BO-233 and CMS-033 — or they do
not and their titles are wrong. Both are re-signature work, not a component addition.

### Recommendation

1. **Reword `requiredWhen` to key off the declared operation**, not the screen's subject:
   *"the screen declares an operation that publishes, deploys, promotes or activates"*. That is
   machine-checkable and returns the 34. Exclude `release*` explicitly, or rename the eleven
   hold-releasing operations — the collision will keep costing.
2. **Ship it warning.** Enforcing on day one fails 34 screens that do not declare the component
   and would reject six of the seven screens the patch itself is adding it to. Warning lands the
   vocabulary now and makes the 34 a work list.
3. **Apply `publishGate` to BO-153 and BO-094 only**, both of which declare a real publish
   operation. Hold the other six pending re-signature.
4. Flip to enforcing when the 34 are declared and the six are resolved.

---

## 6 · What this changes in the plan

- Phase A's decision is answerable: **warn, operation-keyed, two screens not eight.**
- Phase A gains a step: the six title-only publish screens go on the contract-gap list with
  BO-233 and CMS-033 — nine screens now, not two.
- Phase C's first check is shippable enforcing on ten platforms immediately.
- New, not previously recorded: **the P08 shift and order blocks** (§3), four screens that can
  each close a shift, three that can each refund an order. Same shape as the cell block.
