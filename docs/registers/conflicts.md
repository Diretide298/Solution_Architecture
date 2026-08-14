# Conflict Register

> **CF-01 to CF-72**, plus one screen-level item. Every conflict raised since 30 July.
> **Blocking: 0 · Open: 25 · Closed: 41 · Withdrawn or absorbed: 6**

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
| **CF-57** | **AI configuration assistance is Wave 1 and is not in the phasing paper.** Qossai: "one of the most important item for the AI… it's supposed to be from beginning." An admin describes what they want and the assistant walks the configuration. Not among the fifteen Phase 1 applications. Two further data-independent candidates named: map layout generation and ticket artwork. **The phasing paper needs revising** | Chinmay | 14 Aug |
| **CF-53** | **73 back office screens are counted and never itemised.** The page inventory carries "POS · Scanner · Back office — 73" from v1 with no list behind it. Six are now written (P08 queue and parking); the remaining ~67 have no ids, no names and no owner, and were nonetheless in every estimate | Chinmay | 14 Aug |
| **CF-51** | **Location-aware ticket activation is not contracted.** 3.1.9 requires BLE beacon validation, geofencing, and entitlements that "shall only become active when the guest is physically located within authorized venues". Access control has geofencing for **staff handhelds**; there is nothing for guest-side activation. A dynamic QR that only works inside the venue is a real anti-fraud control and it does not exist. **Needs a decision on enforcement strength** — refusing activation outside a geofence will strand guests with poor GPS at an indoor gate | Chinmay + Qossai | 14 Aug |
| **CF-14** | AI concierge mechanism and token billing model. How AI usage is priced to tenants, and whether the concierge meters per interaction or per token | Both — workshop | 10 Aug |
| **CF-17** | Venue-map format and guidance standard. Which CAD or SVG conventions venues will supply, so the importer targets something real | Both | 10 Aug |
| **CF-35** | **Biometric data is sensitive under PDPL** — heightened protection, explicit consent, DPIA, stricter transfer rules. Affects Face Pass, facial readers and fingerprint enrolment. Not previously flagged; the current design treats biometrics as ordinary identity data | Allam + counsel | 13 Aug |
| **CF-40** | **Training & Knowledge Base and Employee Recognition have no provenance.** Both appear in the employee app design reference and in **neither the matrix nor any of the seven MoMs**. Recommendation: SOP repository in, LMS out, kudos out. The question that resolves it — does the tenant already have an LMS? If so the answer is an integration, not a build | Qossai / Allam | 12 Aug |
| **CF-41** | **AI is a primary navigation tab** in the employee app — Home, Tasks, Scan, **AI**, More. AI-06 sits in Wave 2, but the app shell cannot ship without the tab existing. Move AI-06 to Wave 1, ship a disabled tab, or reorder the navigation | Qossai + Chinmay | 12 Aug |
| **CF-48** | **Q2 Virtual Waiting Room.** ADR-0012 separated Q1 (ride queues, contracted) from Q2 (on-sale throttling). Q2 is edge infrastructure, not a product contract — it holds traffic before it reaches the application at all. **Build or buy.** Recommendation: buy. The vendors are mature, and a waiting room built badly fails on the one day it exists to protect | Dinesh + Qossai | 13 Aug |

## Open — Softlabs to resolve

| ID | Issue | Owner | Since |
|---|---|---|---|
| **CF-21** | **Undiscussed domains — restated 14 Aug after an audit.** The original entry named four domains totalling ~276 requirements and was wrong on composition. **Rentals is not a domain.** Rentals and lockers are 30 requirements scattered across seven existing domains, mostly `catalogue` Resource Management (1.2.8–1.2.23), which **is contracted**. The real position: **three domains with no contract — Developer & API (94), Device Management (60), Accreditation (58) = 212 requirements.** Accreditation stays the urgent one: validation appears on the Wave 1 employee scanner. Two further domains have no owning contract for different reasons, tracked as CF-59 | Chinmay — schedule three workshops | 12 Aug |
| **CF-59** | **Two domains have no owning contract, and neither is workshop-blocked.** **Approval Workflows & Governance (80 reqs)** is genuinely cross-cutting — refund approval, shift variance, release promotion and manual discount all implement it, and no module owns it. **Employee Mobile App & AI Assistant (50 reqs)** is a surface, so it maps to screens rather than to a contract, and P06 has none written. Neither is a gap in capability; both are gaps in **traceability** — 130 requirements that cannot be shown as covered because nothing claims them | Chinmay | 14 Aug |
| **CF-62** | **`createReservation` had been silently absent from the contracts.** `/reservations` was declared twice in `orders.yaml`; YAML keeps the last block and drops the first, so a POST was lost to a GET. Every check passed on what survived, because there was nothing left to be inconsistent with. Found on 14 Aug by the state-model checker looking for something else. **Recovered — 624 operations.** A duplicate-path check now runs in `check-states.py`. One further duplicate found and removed in `seating.yaml`, where an operation had been added under a name that already existed | Chinmay | 14 Aug |
| **CF-61** | **On-premise deployment was never designed for.** Settled 14 Aug as the third client-facing model: the platform on the venue's own hardware, nothing leaving the site. Seven mechanisms assume TICVAI can reach the cell and cannot — the migration orchestrator cannot push, licensing cannot be Control-Plane enforced, support is blind, DR becomes the client's responsibility, and in-region AI inference has no endpoint. **Three decisions are needed before the first on-premise sale**, all commercial as much as technical: whether on-premise venues participate in cross-cell entitlements (honest default: no), what an expired licence does (recommendation: degrade, never stop — a gate refusing entry because a licence lapsed over a weekend is worse than running unlicensed until Monday), and who is contractually responsible for backups. ADR-0017 written | Chinmay + Qossai | 14 Aug |
| **CF-72** | **Twelve more lifecycle operations were missing, found the same way as CF-66.** Writing the remaining eighteen state models exposed `rejectRequisition`, `returnRequisition`, `cancelRequisition`, `closeTransferShort`, `recordInvoicePayment`, `disputeInvoice`, `resolveInvoiceDispute`, `cancelInvoice`, `rejectRelease`, `withdrawRelease`, `startRollout` and `rollbackTenantMigration` — every one an enum value nothing could reach. **The pattern is now confirmed rather than suspected:** the contracts were written for the happy path of each object and not its refusals, returns and reversals. `returnRequisition` is the clearest — without it every incomplete request is a rejection and the queue stops moving. Added — 654 operations, and **all 39 status enums now have a checked state model** | Chinmay | 14 Aug |
| **CF-71** | **A task has no contract, and the employee app is fifty screens built around them.** `listTasks`, `updateTask` and `createHandoverNote` appear in none of 642 operations. The Staff App board draws EMP-004, EMP-005, EMP-006 and EMP-007 — task list, task detail, raise a task, handover notes — and F08, the flow a venue runs its day on, names no operation for four of its eight steps. This is CF-59's traceability gap made concrete: Employee Mobile App is 50 requirements with no owning contract, and the assumption that it was "a surface, so it maps to screens" was wrong. **A task is an object, and it needs one** | Chinmay | 14 Aug |
| **CF-67** | **Virtual and hybrid events appear once and nowhere else.** 1.3.30 requires "physical, virtual and hybrid events with configurable attendance rules and access methods". Nothing else in 3,184 requirements mentions streaming, a virtual access method, or online attendance — no contract, no screen, no entitlement kind. Either a stray line, or a product capability nobody has costed. **A hybrid event changes admission fundamentally**: an entitlement with no gate to scan at needs a different validation path entirely | Qossai | 14 Aug |
| **CF-68** | **The contracts have no concept of a payment provider.** Two gateways are named in the integrations sheet — Stripe and Network International — and there is no `PaymentProvider` enum, no provider field on `Payment`, and no way to say which gateway a payment went through. **This breaks settlement reconciliation:** `ingestSettlementFile` matches an acquirer's file against payments, and with no provider there is nothing to match on but amount and time, which is how two transactions of the same value in the same minute get reconciled to each other. The platform runs two providers from day one, so this is not hypothetical | Chinmay | 14 Aug |
| **CF-69** | **Four named integrations have no trace in any contract.** **DET and DCT** — the Dubai and Abu Dhabi tourism authorities — are almost certainly mandatory visitor reporting rather than optional, and nobody has asked what the interface is. **Al Hosn** is the UAE health pass, likely dormant, worth confirming. **SIEM** has no contract because security events have no catalogue: `identity.authz_audit` exists and nothing ships it anywhere. All 16 hardware integrations resolve to a device kind and are covered by ADR-0015 | Qossai + Allam | 14 Aug |
| **CF-70** | **Three Postgres enums disagreed with their contract counterparts.** `platform.device_kind` held nine values the API did not and the API six the database did not — I wrote V0003 from the integrations list without checking the contract. `platform.scope_level` had `sub_department` against the contract's `subDepartment`, **a hierarchy level that would not resolve.** Both reconciled to a union of 20 device kinds and camelCase throughout. **Nothing had ever compared a Postgres enum to its contract**; `check-migrations.py` now does, and it was verified by breaking one deliberately | Chinmay | 14 Aug |
| **CF-64** | **89 retention requirements, two stated periods.** Only 4.3.4 (10 years, payment) and 6.1.78 (7 years) name a number. Combined with CF-60's 62 undesigned DR & BCP requirements, **there is no RPO and no RTO** — and recovery objectives determine the database topology. A one-hour RPO and a one-minute RPO are different replication architectures, and we are building without knowing which. Lands hardest on on-premise (ADR-0017), where backup is the client's responsibility and they will ask what good looks like | Dinesh + Qossai | 14 Aug |
| **CF-65** | **52 reports are named by title and nothing lists them.** 347 requirements mention reporting; the matrix names specific reports — Deferred Revenue, Commission, Cost Center Revenue, Access Control Override, Damage Fee — as a list rather than a capability. We hold a report *definition engine*, which is the right shape, and cannot show that any named report is covered because nothing maps title to definition. A register turns 347 requirements from unverifiable into countable | Chinmay | 14 Aug |
| **CF-60** | **113 requirements on three matrix sheets have never been counted.** Every figure quoted since 30 July — 3,184 across 21 domains — is the Functionality sheet alone. **Disaster Recovery & BCP (62)**, **Training & Knowledge Transfer (40)** and **Compliance & Security (11)** are separate sheets with their own requirements and no coverage analysis. DR & BCP is the one that matters: backup schedules, RPO and RTO are architectural and none of it has been designed. The Integrations sheet lists **19 software and 16 hardware integrations**, previously counted as "roughly 35" and never itemised against contracts | Chinmay | 14 Aug |
| **CF-24** | **9.2% actor coverage.** 292 of 3,184 requirements name a human actor. Assignment for the remaining ~91% is undetermined, which makes permission design partly inference | Chinmay | 12 Aug |
| **CF-42** | **RTL and dark theme are Sprint 1 scope**, not a later localisation pass. Arabic RTL means every layout mirrored, not translated, and the client's own hierarchy is emphatic that it is a core requirement. Roughly four days on `design-tokens` and `ui` | Chinmay / design | 12 Aug |
| **CF-49** | **Release-management scope skipped the matrix.** Thirteen Platform Admin screens raised 30 July, minuted, never written into a requirement — absent from the matrix, the capability register and every estimate. Contract now written (`platform-ops`, 24 ops). The scope needs reconciling into the matrix, because a workshop decision reaching a contract without passing through a requirement has skipped the step that would have caught it | Chinmay | 13 Aug |
| **CF-18** | Dynamic bundle auto-discounting design. How a dynamic bundle prices itself when its components change | Softlabs | 10 Aug |
| **CF-23** | 10 Aug §5.1 has a **lost subject** — "agreed this makes more sense and will be adopted" names nobody. No owner for a decision since partially reversed | Chitrangi | 10 Aug |

---

## Closed

### Resolved in the 14 August working session

| ID | Issue | Resolution |
|---|---|---|
| **CF-56** | **ADR-0014 contradicted by the shared-tenant hosting model.** 14 Aug confirmed two models: dedicated infrastructure per tenant, and a shared TICVAI database hosting many small tenants with logical isolation by site id. ADR-0014 states a cell holds exactly one tenant, and `platform.tenant` was written as a single-row projection **with no RLS on that basis** — on a shared cell that is a cross-tenant leak. Also affects orchestrator fan-out: a shared cell has many tenants on one schema version. **Closed 14 Aug.** ADR-0014 amended with a third cell kind. `platform.tenant` RLS added the same day. Two further points settled by the client: **a tenant can be migrated from shared to dedicated** — the shared start is not a decision they are stuck with, and that is what makes the cheaper package sellable — and **capacity is driven by traffic and concurrent users, not tenant count**, so scaling out means launching another identical cluster rather than growing one. Six operations added: `getCellCapacity`, `listCellClusters`, `launchCellCluster`, `listTenantMigrations`, `planTenantMigration`, `executeTenantMigration`. `Cell.tenantId` is now nullable |
| **CF-55** | **Four POS operations existed in the delivered design and in no contract.** The Park POS mockups show Hold Order, Discount, Add Tip and a cash drawer, none of which had an operation. Now added: `holdOrder`, `resumeOrder`, `applyManualDiscount`, `addTip`, `recordNoSale`, plus a `held` order status and the `ORDER_DISCOUNT` permission. **A design is a requirements source and had not been read as one** — the mockups arrived and were treated as visual reference rather than as a specification with buttons that must do something | Chinmay | 14 Aug |
| **CF-54** | **The `pii` schema was declared and empty.** V0001 created the schema, the V0001 rollback dropped two tables in it, and four foreign keys in V0003b referenced `pii.subject` — which no migration created. `psql` would have failed on the first FK; the structural checker reported PASS, because it verified conventions and never verified that a referenced table exists. **Both fixed:** `V0001a` writes the four PII tables and an erasure function, and the checker now fails any FK whose target no migration creates. Closed on the day it was found | Chinmay | 14 Aug |
| **CF-50** | **Guest self-ordering had no contract.** `diningAndFnb` is a module a tenant can switch on in the guest app, and nothing was reachable behind it — `listOutlets` needed `SCOPE_VIEW`, menus needed `PRODUCT_VIEW`, and `createFnbOrder` needed `ORDER_CREATE`, all staff permissions on `bearerAuth`. Six guest operations now added. **The same failure as push notifications: a feature toggle wired to nothing.** Worth auditing the remaining twelve module keys for the same gap | Chinmay | 14 Aug |
| **CF-66** | **Seventeen enum values existed that nothing could reach.** Writing state models for twenty entities found that the contracts could start and finish things but not manage them mid-flight: `paused` on campaigns and promotions, `sent` and `acknowledged` and `closedShort` on purchase orders, `assigned` on coupons, `variancePending` recount, `decommissioning` on cells, journal `reject`, period `reopen`, case `reopen`. **All seventeen were declared states with no operation reaching them.** Added — 642 operations. Also corrected: twenty-three transitions named operations that exist under different names, including `transitionProductLifecycle`, which handles every product move in one operation rather than six | Chinmay | 14 Aug |

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
| **CF-33a** | Queue vendor selection | **Closed 14 Aug. Client: integrate with the on-site systems already installed, and allow manual entry alongside.** `manual` is now a first-class adaptor rather than the absence of one — a venue with a supervisor and a clipboard is configured, not unconfigured, and the health view must not report it as broken. A `testQueueFeed` operation was added: configuring an integration without a test is configuring it blind. Venue Back Office gains a Queue Integration Setup screen (BO-003) and a Manual Wait Time Entry screen (BO-004) |
| **CF-37** | **FX policy for cross-region revenue splits** | **Closed 14 Aug.** Allam settled the principle: **every transaction is stored in the base currency of the region it was transacted in.** A guest paying USD 100 in a UAE venue has the dirham equivalent stored; change and refunds are always in base currency; a foreign-tender report shows what each cashier took in which currency. Most of the questions FX usually raises then do not arise — there is no rate to lock at redemption, expiry or refund, because the stored amount was never foreign. **The cross-region split follows from the same principle rather than extending it:** the obligation between two legal entities arises **at redemption**, denominated in the **consuming** entity's base currency at that date's rate; movement between arising and settling is FX gain or loss on the **selling** entity, which holds the balance; revalued at close. Neither entity ever holds a currency that is not its own. Four operations added — `listFxRates`, `setFxRate`, `getForeignTenderReport`, `listInterEntityObligations`, `runFxRevaluation` |
| **CF-58** | Entitlements could not be appended to an existing ticket | **Closed 14 Aug.** `getMediaEntitlements` and `appendEntitlementToMedia` added, keyed on **media code rather than order id** — the guest has the wristband in their hand and does not know which order issued it. Appending creates a **new order**; the original is untouched, because editing a paid and reported order moves yesterday's revenue. Entitlement templates gain `canShareMedia`, false for anything surrendered at use — a single-entry ticket taken at the gate is not a claim token for a locker bought afterwards |
| **CF-63** | 263 of 273 "configurable" requirements did not say at what level | **Closed 14 Aug by rule rather than by 263 answers.** ADR-0018: configuration resolves up the scope tree, nearest ancestor wins, **three levels — tenant, region, venue.** Client correction that made it work: **venue is the floor.** A workstation is assigned a profile the venue defined; an outlet is assigned a menu the venue defined. Nothing below venue configures anything, because forty workstations configured individually is forty things that drift. Region holds law and money; tenant holds brand, identity, consent and one-scheme concerns. `x-ticvai-config-scope` now on 28 operations, checked by `check-config-scope.py`, which found two real defects — `createMessageTemplate` and `createLoyaltyProgramme` were callable by a venue manager while setting tenant-wide values |
| **CF-52** | Parking scope | **Closed 14 Aug.** Three modes: no integration (we issue a QR, security scans it) · plate number pushed to the vendor's ANPR whitelist, the expected path · QR pushed to the barrier where there is no ANPR. Hourly parking charged on exit is **out of scope** — the parking POS handles it without us. **Direction settled: we consume the vendor's API and push to it**, rather than publishing one for them to call |
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
| Open — needs a client decision | **9** |
| Open — Softlabs to resolve | **16** |
| **Closed** | **41** |
| Withdrawn or absorbed | **6** |
| **Total raised** | **72** |

| **Closed** | **31** |
| Withdrawn or absorbed | 6 |
| **Total raised** | **71** |

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
