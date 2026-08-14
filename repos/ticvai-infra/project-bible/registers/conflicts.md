# Conflict Register

> **CF-01 to CF-49**, plus one screen-level item. Every conflict raised since 30 July.
> **Blocking: 0 · Open: 14 · Closed: 30 · Withdrawn or absorbed: 6**

A conflict is any place where two sources disagree, or where a decision is required and
absent. It closes when a client decision, an ADR or a piece of research settles it — not when
someone stops mentioning it.

**Rebuilt 14 August.** The previous version had three defects: CF-27 appeared in both the open
and closed sections; CF-48 and CF-49 were filed under Closed while still open; and six items
raised in working sessions — CF-35, 37, 39, 40, 41, 42 — were never written in at all. One of
those was **CF-37**, which blocks roughly twelve finance operations. A register that loses its
most expensive open item is worse than no register, because it is trusted.

---

## Open — blocking

**None.** No conflict currently prevents contract, schema or build work from proceeding.

---

## Open — needs a client decision

Nothing here can be resolved by working harder.

| ID | Issue | Owner | Since |
|---|---|---|---|
| **CF-37** | **FX policy for cross-region revenue splits.** A pass sold in one region and redeemed in another splits revenue across legal entities in different currencies. At what rate, at what moment, and which entity carries the movement. A 100-unit pass split 60/40 books **400, 380 or 392** depending on the answer — same transaction, 5% spread. Recommendation drafted: daily published rate · convert at redemption · denominate in the consuming entity's currency · movement to the selling entity's FX gain and loss · revalue at close. **Blocks ~12 finance operations and period close.** The ledger is append-only, so a late change means posting corrections rather than restating | TICVAI Finance — email sent | 12 Aug |
| **CF-14** | AI concierge mechanism and token billing model. How AI usage is priced to tenants, and whether the concierge meters per interaction or per token | Both — workshop | 10 Aug |
| **CF-17** | Venue-map format and guidance standard. Which CAD or SVG conventions venues will supply, so the importer targets something real | Both | 10 Aug |
| **CF-35** | **Biometric data is sensitive under PDPL** — heightened protection, explicit consent, DPIA, stricter transfer rules. Affects Face Pass, facial readers and fingerprint enrolment. Not previously flagged; the current design treats biometrics as ordinary identity data | Allam + counsel | 13 Aug |
| **CF-40** | **Training & Knowledge Base and Employee Recognition have no provenance.** Both appear in the employee app design reference and in **neither the matrix nor any of the seven MoMs**. Recommendation: SOP repository in, LMS out, kudos out. The question that resolves it — does the tenant already have an LMS? If so the answer is an integration, not a build | Qossai / Allam | 12 Aug |
| **CF-41** | **AI is a primary navigation tab** in the employee app — Home, Tasks, Scan, **AI**, More. AI-06 sits in Wave 2, but the app shell cannot ship without the tab existing. Move AI-06 to Wave 1, ship a disabled tab, or reorder the navigation | Qossai + Chinmay | 12 Aug |
| **CF-48** | **Q2 Virtual Waiting Room.** ADR-0012 separated Q1 (ride queues, contracted) from Q2 (on-sale throttling). Q2 is edge infrastructure, not a product contract — it holds traffic before it reaches the application at all. **Build or buy.** Recommendation: buy. The vendors are mature, and a waiting room built badly fails on the one day it exists to protect | Dinesh + Qossai | 13 Aug |

## Open — Softlabs to resolve

| ID | Issue | Owner | Since |
|---|---|---|---|
| **CF-21** | **Four undiscussed domains** — Developer & API (94), Device Management (60), Accreditation (58), Rentals (~64). **~276 requirements, zero MoM coverage.** Accreditation is the urgent one: accreditation validation appears on the employee scanner in Wave 1, so it cannot defer with the other three | Chinmay — schedule workshops | 12 Aug |
| **CF-24** | **9.2% actor coverage.** 292 of 3,184 requirements name a human actor. Assignment for the remaining ~91% is undetermined, which makes permission design partly inference | Chinmay | 12 Aug |
| **CF-42** | **RTL and dark theme are Sprint 1 scope**, not a later localisation pass. Arabic RTL means every layout mirrored, not translated, and the client's own hierarchy is emphatic that it is a core requirement. Roughly four days on `design-tokens` and `ui` | Chinmay / design | 12 Aug |
| **CF-49** | **Release-management scope skipped the matrix.** Thirteen Platform Admin screens raised 30 July, minuted, never written into a requirement — absent from the matrix, the capability register and every estimate. Contract now written (`platform-ops`, 24 ops). The scope needs reconciling into the matrix, because a workshop decision reaching a contract without passing through a requirement has skipped the step that would have caught it | Chinmay | 13 Aug |
| **CF-18** | Dynamic bundle auto-discounting design. How a dynamic bundle prices itself when its components change | Softlabs | 10 Aug |
| **CF-23** | 10 Aug §5.1 has a **lost subject** — "agreed this makes more sense and will be adopted" names nobody. No owner for a decision since partially reversed | Chitrangi | 10 Aug |
| **CF-33a** | Queue vendor selection. Parked deliberately — procurement, not architecture. The adaptor framework makes it a late decision | Parked | 12 Aug |

---

## Closed

### By client decision

| ID | Issue | Closed by | ADR |
|---|---|---|---|
| CF-01 | Multi-role login contradiction | 12 Aug §4 — conditional role prompt | [0003](../adr/0003-conditional-role-selection-at-login.md) |
| CF-02 | Session concurrency | Client — single session only | [0004](../adr/0004-single-session-per-user.md) |
| CF-03 | Role vs workstation authorisation | Client — user and role driven, any device | [0002](../adr/0002-authorisation-is-user-driven-not-workstation-driven.md) |
| CF-05 | Four competing role taxonomies | 12 Aug §9 — no predefined roles; 7.1.12 is a seed list | — |
| CF-07 | Refund authorisation | 2.12.3 — dual-auth below threshold | — |
| CF-08 | Flying POS | Client — workstation profile, offline-mandatory | — |
| CF-09 | Kiosk operator model | Client — login page plus assignable permission | — |
| CF-10 | Till handover on breaks | 12 Aug §1 — log out or suspend shift | — |
| CF-11 | Approval model depth | Client — add delegation, out-of-office, parallel, consensus | — |
| CF-12 | Universal Cashier landing screen | 12 Aug §3 — sale board per workstation | — |
| CF-13 | Guest app publishing | Client — Option C, tiered | [0006](../adr/0006-tiered-guest-app-distribution.md) |
| **CF-31** | Do entitlements cross jurisdictions? | **Client: yes.** Home-cell ownership with delegated redemption. Only a pseudonymous `guestLinkId` crosses | [0010](../adr/0010-cross-jurisdiction-entitlements.md) |
| **CF-33** | Queue management ownership | **Client: adaptor-first.** Q1 gets the inbound API, adaptor framework and a venue toggle. Q2 is infrastructure | [0012](../adr/0012-queue-integration-adaptor-first.md) |
| **CF-34** | Is the hierarchy binding or illustrative? | **Client: binding.** Seven levels confirmed; only the populating example was illustrative | [0011](../adr/0011-hierarchy-is-binding.md) |
| **CF-36** | `ORDER_REFUND_APPROVE` threshold | **Client: venue policy, not permission scope.** The permission stays binary; thresholds are venue configuration, because venues run different policies and the permission model should not encode commercial rules | — |
| **CF-38** | Price variance on re-pricing | **Client: variance account required, threshold per venue.** Quoted price honoured, difference posted, above threshold becomes a reviewable exception | — |

### By research or architecture

| ID | Issue | Closed by | ADR |
|---|---|---|---|
| CF-04 | Front-gate scanning surface | 2.13.6 plus 3.2.17 | — |
| CF-19 | KDS scope | 31 Jul §11 — integration point only, not a build | — |
| CF-22 | Accreditation vs entitlement | Precedent confirmed | — |
| **CF-15** | Online-first vs offline-first POS catalogue | **Case study. Local-first.** One read path, always local. Leases for contended inventory, local journal, server re-prices on ingest. The framing was a false binary — data classes need distinct strategies, not one architectural choice | [0013](../adr/0013-local-first-point-of-sale.md) |
| **CF-20** | AI data residency | **Research plus ADR-0009.** No single UAE AI residency rule; the obligation derives from PDPL Art. 22/23. Residency is architectural — in-region inference, in-cell prompts, logs and vectors | [0009](../adr/0009-ai-data-residency.md) |
| **CF-32** | Hyperscaler presence in the second jurisdiction | **Dissolved by ADR-0014.** The jurisdiction came from an illustrative diagram, not a deployment. Cell = Tenant × Region makes availability a provisioning-time placement check | [0014](../adr/0014-cell-per-region.md) |
| **CF-39** | White Label Builder had no owning context | **Closed.** Promoted to its own satellite contract — `white-label`, 41 operations. It is a CMS plus an app builder, not a settings page, and 20 screens in the client boards confirm it | — |
| **P08-047** | Channel-based offline inventory pooling — "design not yet agreed" (2 Aug) | **Closed by ADR-0013.** Allocation and leases are not competing designs: allocation is the commercial pool, a lease is the technical hold drawing from it. They compose | [0013](../adr/0013-local-first-point-of-sale.md) |

### By correcting an artefact

| ID | Issue | Closed by |
|---|---|---|
| CF-16 | Reference manual undelivered | Received |
| CF-25 | Party inversion in the 12 Aug MoM | Client correcting the record |
| **CF-43** | AI governance has no screens | Six screens and ten sub-screens added as P08-111A→F — activity log, approval queue, explainability centre, AI audit trail, token analytics, consent controls. Hierarchy v2.1 |
| **CF-44** | Conversational coverage 3 of 8 | Four surfaces added as sub-screens — guest concierge, kiosk, employee voice, financial. Sub-screens because they are one framework rendered per surface, which is what "eight configurations of one framework" means. Hierarchy v2.1 |
| **CF-45** | Two Phase 1 screens require operating history | Both annotated. They ship in Phase 1; the predictive source arrives in Phase 2. Hierarchy v2.1 |
| **CF-46** | 3,185 / 22 domains vs 3,184 / 21 | Read Me corrected; note 4 expanded to explain the earlier figure. Hierarchy v2.1 |
| **CF-47** | ~102 screens absent from the page inventory | Five platforms added — Guest Web (29), Platform Admin (36), Partner Portal (21), Accreditation (8), Support Console (8). Inventory 203 → **305**. Surfaced 28 screens with no contract behind them |

---

## Withdrawn or absorbed

| ID | Was | Now |
|---|---|---|
| CF-06 | `User` vs `StaffResource` | **Downgraded.** 1.2.17 / 1.2.23 are `DESIGN`, not ratified. Not a conflict until one is |
| CF-26 | SOAP / ISAPI incompatibility | **Downgraded** to one question: is migration from an existing BOS tenant in scope? |
| CF-27 | Hierarchy depth vs reference model | **Absorbed into CF-34.** Previously listed as both open and closed — a register defect, now corrected |
| CF-28 | One user, two workstations | **Absorbed into CF-02** |
| CF-29 | Reference modules absent from the matrix | **Withdrawn.** The matrix is scope |
| CF-30 | Integration surface 3× the matrix | **Withdrawn as scope.** Tier 1 is the Integrations sheet, roughly 35 systems |

---

## Summary

| State | Count |
|---|---|
| **Blocking** | **0** |
| Open — needs a client decision | **7** |
| Open — Softlabs to resolve | **6** |
| Parked | 1 |
| **Closed** | **30** |
| Withdrawn or absorbed | 6 |
| **Total raised** | **50** |

**The three that cost most if they slip:**

**CF-37** blocks twelve finance operations against an append-only ledger. A late answer means
posting corrections rather than restating.

**CF-21** is four workshops covering ~276 requirements, and Accreditation sits on a Wave 1
surface while the other three genuinely can wait.

**CF-48** is a build-or-buy decision on infrastructure that only matters on the day it is
needed — which is also the day it is too late to procure.

---

## Raising a conflict

A conflict needs three things: the two sources that disagree, quoted; what a decision would
unblock; and a recommendation. A conflict raised without a recommendation is a question, and
questions accumulate faster than they get answered.
