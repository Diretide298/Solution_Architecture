# Conflict Register

> **Purpose:** Open and closed decisions, CF-01 to CF-47  
> **Owner:** Chinmay  
> **Status:** Living


A closed conflict becomes an [ADR](../adr/README.md). This register tracks the **question**; the ADR records the **answer and why**.

| | Count |
|---|---|
| **Open — blocking** | **0** |
| Open — non-blocking | **16** |
| Closed | **33** |
| Withdrawn / downgraded | **3** |

---

## Open — blocking

**None.**

Every remaining item is either a client decision that does not gate current work, a
scheduling task, or record hygiene. See below.

## Open — non-blocking

| ID | Issue | Owner | Since |
|---|---|---|---|
| CF-14 | AI concierge mechanism + token billing model | Both — workshop | 10 Aug |
| CF-17 | Venue-map format / guidance standard | Both | 10 Aug |
| CF-18 | Dynamic bundle auto-discounting design | Softlabs | 10 Aug |
| CF-21 | **Four undiscussed domains** — Developer/API (94), Device Mgmt (60), Accreditation (58), Rentals (~64). ~276 reqs, zero MoM coverage | Chinmay — schedule workshops | 12 Aug |
| CF-23 | 10 Aug §5.1 has a **lost subject** — "agreed this makes more sense" names nobody. No owner for a decision since partially reversed | Chitrangi | 10 Aug |
| CF-24 | **9.2% actor coverage** — 292 of 3,184 requirements name a human actor. Assignment for ~91% is undetermined | Chinmay | 12 Aug |
| CF-27 | **Hierarchy depth** — 7+ levels on a 3-level reference model. Rights cascade is original design work | Dinesh | 12 Aug |

## Closed

| ID | Issue | Closed by | ADR |
|---|---|---|---|
| CF-01 | Multi-role login contradiction | 12 Aug §4 — conditional role prompt | [0003](../adr/0003-conditional-role-selection.md) |
| CF-02 | Session concurrency | Client — single session only | [0004](../adr/0004-single-session.md) |
| CF-03 | Role vs workstation authorisation | Client — user/role-driven, any device | [0002](../adr/0002-user-driven-authorisation.md) |
| CF-04 | Front-gate scanning surface | 2.13.6 + 3.2.17 | — |
| CF-05 | Four competing role taxonomies | 12 Aug §9 — no predefined roles; 7.1.12 is a seed list | — |
| CF-06 | `User` vs `StaffResource` | 1.2.17 / 1.2.23 — **`DESIGN`, not ratified** | — |
| CF-07 | Refund authorisation | 2.12.3 — dual-auth below threshold | — |
| CF-08 | Flying POS | Client — workstation profile, offline-mandatory | — |
| CF-09 | Kiosk operator model | Client — login page + assignable permission | — |
| CF-10 | Till handover on breaks | 12 Aug §1 — log out or suspend shift | — |
| CF-11 | Approval model depth | Client — add delegation, OOO, parallel, consensus | — |
| CF-12 | Universal Cashier landing screen | 12 Aug §3 — Sale Board per workstation | — |
| CF-13 | Guest app publishing | Client — Option C, tiered | [0006](../adr/0006-tiered-guest-app-distribution.md) |
| CF-16 | Reference manual undelivered | Received | — |
| CF-19 | KDS scope | 31 Jul §11 — integration point only | — |
| CF-22 | Accreditation vs entitlement | Precedent confirmed | — |
| CF-25 | Party inversion in 12 Aug MoM | Client — correcting the record | — |
| CF-28 | One user, two workstations | Absorbed into CF-02 | — |
| **CF-20** | AI data residency | **Research + ADR-0009.** No single AI residency rule; obligation derives from PDPL Art. 22/23. Residency is architectural — in-region inference, in-cell prompts, logs and vectors. Qdrant selected, deployed in-cell | [0009](../adr/0009-ai-data-residency.md) |
| **CF-31** | Do entitlements cross jurisdictions? | **Client: yes.** Home-cell ownership with delegated redemption | [0010](../adr/0010-cross-jurisdiction-entitlements.md) |
| **CF-33** | Queue management ownership | **Client: adaptor-first.** Q1 gets inbound API, adaptor framework, frontend and a venue-level integration toggle. Q2 is in-house infrastructure, Wave 1. Vendor selection deferred — a procurement question, not architecture | [0012](../adr/0012-queue-integration-adaptor-first.md) |
| **CF-36** | `ORDER_REFUND_APPROVE` threshold | **Client: venue policy, not permission scope.** The permission stays binary; thresholds, time bands and approval limits are venue configuration, because venues run different policies and the permission model should not encode commercial rules | — |
| **CF-38** | Price variance on re-pricing | **Client: variance account required, threshold custom per venue.** Quoted price is honoured, difference posted to a variance account, and a variance above the venue's threshold is an exception requiring review rather than a routine posting | — |
| **CF-32** | Hyperscaler presence in the second jurisdiction | **Dissolved by ADR-0014.** The jurisdiction in question came from an illustrative diagram, not a deployment. Cell = Tenant × Region makes availability a provisioning-time placement check per real deployment, not a design blocker | [0014](../adr/0014-cell-per-region.md) |
| **CF-43** | AI governance has no screens | **Closed.** Six screens and ten sub-screens added to the register as P08-111A→F — activity log, approval queue, explainability centre, AI audit trail, token analytics, consent and data controls | Hierarchy v2.1 |
| **CF-44** | Conversational coverage 3 of 8 | **Closed.** Four surfaces added as sub-screens — guest concierge (P02), kiosk (P03), employee voice (P06), financial (P08). Recorded as sub-screens because they are one framework rendered per surface, which is what the phasing paper means by "eight configurations of one framework" | Hierarchy v2.1 |
| **CF-45** | Two Phase 1 screens require operating history | **Closed.** Both annotated. They ship in Phase 1; the predictive source arrives in Phase 2. P08-066.1 renders live sensor data until AI-24 exists; P08-111 uses rule-based thresholds until AI-49 exists | Hierarchy v2.1 |
| **CF-48** | **Q2 Virtual Waiting Room** — WEB-015 in the storefront. ADR-0012 separated Q1 (ride queues, contracted) from Q2 (on-sale throttling). Q2 is edge infrastructure, not a product contract: it holds traffic before it reaches the application at all. **Decision needed — build or buy.** Recommendation: buy. It is a CDN and edge concern, the vendors are mature, and building one badly is worse than not having it | Dinesh + Qossai | 13 Aug |
| **CF-49** | **Release-management scope skipped the matrix.** Thirteen Platform Admin screens were raised on 30 July, minuted, and never written into a requirement — so they were absent from the matrix, the capability register and every estimate. Contract now written (`platform-ops`, 24 ops). **The scope should be reconciled into the matrix**, because a workshop decision reaching a contract without passing through a requirement has skipped the step that would have caught it earlier | Chinmay | 13 Aug |
| **CF-47** | ~102 screens absent from the page inventory | **Closed.** Five platforms added — Guest Web Storefront (29), Platform Admin Console (36), Partner Portal (21), Accreditation Portal (8), Support Console (8). Inventory 203 → **305**. Surfaced 28 screens with no contract behind them, 13 of which are the release-management scope from 30 Jul that never reached a requirement | Page inventory v3 |
| **CF-46** | 3,185/22 vs 3,184/21 | **Closed.** Read Me corrected to 3,184 across 21 domains, note 4 expanded to explain the earlier figure | Hierarchy v2.1 |
| **P08-047** | Channel-based offline inventory pooling — "design not yet agreed" (2 Aug) | **Closed by ADR-0013.** Channel allocation and leases are not competing designs: allocation is the commercial pool, a lease is the technical hold that draws from it. They compose. The screen stays; its note is stale | [0013](../adr/0013-local-first-point-of-sale.md) |
| **CF-15** | Online-first vs offline-first POS catalogue | **Case study complete. Local-first.** One read path, always local. Leases for contended inventory. Local journal, server re-prices on ingest. Three deployment profiles, one codebase | [0013](../adr/0013-local-first-point-of-sale.md) |
| **CF-34** | Is the hierarchy binding or illustrative? | **Client: binding.** Seven levels confirmed; only the populating example was illustrative | [0011](../adr/0011-hierarchy-is-binding.md) |
| **CF-27** | Hierarchy depth vs reference model | Absorbed into CF-34 | [0011](../adr/0011-hierarchy-is-binding.md) |

## Withdrawn / downgraded

| ID | Was | Now |
|---|---|---|
| CF-26 | SOAP/ISAPI incompatibility | **Downgraded** to one question: is migration from an existing BOS tenant in scope? |
| CF-29 | Reference modules absent from matrix | **Withdrawn.** The matrix is scope |
| CF-30 | Integration surface 3× the matrix | **Withdrawn as scope.** Tier 1 is the Integrations sheet |

---

## Raising a conflict

Two sources of equal authority disagree, or a decision is ambiguous enough that two teams would implement it differently. Record: the statement, the sources, the owner, blocking status, and a recommended resolution — so the meeting is a confirmation rather than a debate.
