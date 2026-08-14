# TICVAI — Base Project Direction

**Version:** 1.2
**Date:** 12 August 2026
**Status:** Living document — changes require sign-off per §9

---

## 1. Purpose

This document defines how the TICVAI platform project decides what is in scope, how source material is weighted, and which architectural positions are settled. It governs the requirement matrix, MoM decisions, reference material, design artefacts, and build.

Where any other artefact conflicts with this document, this document wins until amended.

---

## 2. Source of Truth Hierarchy

This is the governing rule of the project. Everything else follows from it.

| Rank | Source | Authority |
|---|---|---|
| 1 | **MoM decisions** (dated, in a Decisions section) | Scope + binding. Later decisions supersede earlier ones |
| 2 | **Requirement matrix** (`Ticvai_matrix_*.xlsx`, all 5 sheets) | Scope. The contracted requirement baseline |
| 3 | **Client-supplied design references** (PDFs, screen walkthroughs, page explanations) | Directional. Enhance, do not copy |
| 4 | **Reference system manuals** (VivaTicket BOS documentation) | **Inspiration and de-risking only. Never scope** |

### 2.1 Rules for reference system material

The reference system is a functional reference to learn from, not a design to copy
(07 Aug 2026 session close; 03 Aug 2026 §2).

Reference manuals may be used for exactly three purposes:

1. **Gap-hunting** — if the reference system needed a capability and the matrix is silent,
   raise it as a question. It becomes scope only once it appears in the matrix or a MoM decision.
2. **Edge-case discovery** — anti-passback, reentry rules, overshort thresholds, failure modes.
   Cheaper to learn from twenty years of someone else's production than to discover at UAT.
3. **Domain vocabulary** — glossary and entity definitions (see §6).

Reference manuals must **never** be used for:

- Determining scope or feature inclusion
- API, interface, or protocol design
- Architecture, session, or authorisation design
- Data model structure
- Justifying work that is not traceable to rank 1 or rank 2

**Documented exception.** Revenue recognition rules — Allam explicitly directed that the
reference manuals contain recognition rules beyond the requirement matrix and are to be
cross-checked (12 Aug 2026 §8). This exception is narrow and applies to revenue recognition only.
Any extension of it requires a new MoM decision.

### 2.2 Provenance tagging

Every entry in the capability catalogue, actor register, page inventory, and API specification
carries a provenance tag:

| Tag | Meaning | Build status |
|---|---|---|
| `MOM` | Traced to a dated MoM decision | Build |
| `MATRIX` | Traced to a matrix Requirement ID | Build |
| `REF` | Derived from reference system material | **Question for the client — not a build item** |
| `DESIGN` | Our own recommendation, not yet ratified | **Not a build item until accepted** |

Anything tagged `REF` or `DESIGN` is excluded from estimates, contracts, and sprint scope
until it is promoted to `MOM` or `MATRIX`.

---

## 3. Settled Architectural Positions

Positions below are decided. Reopening requires §9 change control.

### 3.1 Authorisation and session

| # | Position | Basis |
|---|---|---|
| 3.1.1 | Authorisation is **user/role-driven**. A user logs in from any device and carries their access | Client decision |
| 3.1.2 | Workstation determines **presentation, hardware binding, till identity, access-point inheritance, and reporting dimension** — never authorisation | Derived from 3.1.1 + 12 Aug §3 |
| 3.1.3 | **Single session per user.** A second login is rejected, not auto-terminating the first | Client decision |
| 3.1.4 | Supervisor-authorised force-logout exists for abandoned sessions | Derived from 3.1.3 |
| 3.1.5 | One user per workstation at a time; a user must log out or suspend shift before another logs in | 12 Aug 2026 §1 |
| 3.1.6 | Multi-role users are prompted to select a role at login; single-role users log in directly | 12 Aug 2026 §4 |
| 3.1.7 | Roles are fully configurable. No role or permission is predefined | 12 Aug 2026 §9 |
| 3.1.8 | Permission resolution across the org tree uses **deny-overrides-allow**, resolved at login, enforced at the data layer | `DESIGN` — pending sign-off |

### 3.2 Scope boundaries

| # | Position |
|---|---|
| 3.2.1 | Scope is the requirement matrix plus MoM decisions. Nothing else |
| 3.2.2 | Integration scope is the matrix Integrations sheet. Additional vendors are supported through driver extensibility, not pre-built |
| 3.2.3 | Kiosk attendant access is granted by a dedicated permission on a login page, assignable to any custom role |
| 3.2.4 | Flying/Mobile POS is a workstation profile with an offline-mandatory flag, not a separate application |
| 3.2.5 | Approval workflows include delegation, out-of-office rerouting, parallel, and consensus flows |

### 3.3 Platform architecture

| # | Position | Basis |
|---|---|---|
| 3.3.1 | **Cell = Tenant × Region** (ADR-0014). Every region is its own cell — not only where jurisdictions differ. Jurisdiction is a *placement constraint*, not the split rule. Cost is controlled by placement tier, not by varying the rule. Cells scale by replication, not decomposition | Client decision |
| 3.3.2 | Cells are **tiered**: Shared (small tenants, DB per tenant) · Dedicated (own cell) · Isolated (own region + key management) · Client-hosted. Tier is a Control Plane attribute, not a code fork | Derived from 3.3.1 + 12 Aug §3 (client-hosted option) |
| 3.3.3 | **One database per tenant.** All sales channels connect to it. Brand and venue isolation is achieved *within* that database | 10 Aug 2026 — Data architecture per tenant |
| 3.3.4 | **Venue isolation via Postgres list partitioning on `venue_id`** on high-volume tables. Not separate databases | `DESIGN` — see rationale below |
| 3.3.5 | **Region carries a placement attribute** — `shared` / `dedicated:{cloud}:{region}` / `client_hosted:{endpoint}`. A tenant may be mixed across regions. Brand is NOT a valid split boundary — it spans jurisdictions in the client's own example | Client decision |
| 3.3.6 | Repository topology is **hybrid**: separate repos per runtime (contracts, backend, frontend, AI, infra); monorepo *within* frontend only | `DESIGN` |
| 3.3.7 | Services split only where **availability domains** differ — venue edge (offline), AI (residency), reporting (analytical load). Target 6–8 services, not one per bounded context | `DESIGN` |
| 3.3.8 | Read scaling via replicas + CDN. Access validation reads the **primary unconditionally** to avoid replication lag refusing valid tickets at a turnstile | `DESIGN` |
| 3.3.9b | **ADR-0010 cross-cell machinery is Wave 1**, not an exception path. Every multi-region tenant exercises it continuously | Derived from ADR-0014 |
| 3.3.9 | Cross-tenant analytics uses a **central warehouse fed by per-cell event export**. Cells are never queried directly | `DESIGN` |

**Rationale for 3.3.4 (venue partitioning, not separate databases).** The following features
cross venue boundaries within a single transaction or query, and would require distributed
transactions or federation if venues were separate databases:

- Multi-venue passes with revenue split by percentage or fixed amount per venue (12 Aug §16)
- Memberships and annual passes valid across venues (matrix 2.14.x)
- Wallet balances spendable at any venue (matrix 6.1.x, 10.2.x)
- Consistent guest identity across channels — the stated reason for 3.3.3 (10 Aug)
- Consolidated brand and legal-entity reporting (12 Aug §14)

List partitioning delivers the same physical separation, partition pruning, and independent
archival as separate databases, while preserving single-transaction integrity and reducing
migration and backup targets from one-per-venue to one-per-tenant.

**Escape hatch.** A single venue that outgrows its tenant's cell may be *promoted* to its own
cell via logical replication and a registry update. Promotion is an exception path, not the
default topology.

### 3.35 Cross-jurisdiction and AI residency

| # | Position | Basis |
|---|---|---|
| 3.35.1 | **Entitlements, wallets, memberships and guest identity cross jurisdictions.** Home-cell ownership with delegated redemption | Client decision · [ADR-0010](adr/0010-cross-jurisdiction-entitlements.md) |
| 3.35.2 | **Only a pseudonymous `guestLinkId` crosses a border.** No PII, ever | Derived |
| 3.35.3 | Cross-cell linkage requires **explicit recorded consent** — the PDPL Article 23 basis | Derived |
| 3.35.4 | **Orders never span cells.** The selling cell owns the order; redemption rights propagate | Derived |
| 3.35.5 | **Wallet balance is single and authoritative** in the home cell. Cross-cell spend is synchronous authorisation with a bounded allocation fallback | Derived |
| 3.35.6 | **AI residency is architectural, not a storage location.** In-region inference; prompts, logs and vector stores in-cell | [ADR-0009](adr/0009-ai-data-residency.md) |
| 3.35.7 | Cross-border AI inference is permitted **only** with a documented Article 22/23 mechanism and a transfer risk assessment, per tenant | [ADR-0009](adr/0009-ai-data-residency.md) |
| 3.35.8 | Qdrant selected, deployed in-cell. `pgvector` remains the shared-tier default | [ADR-0009](adr/0009-ai-data-residency.md) |

### 3.36 Point of sale

| # | Position | Basis |
|---|---|---|
| 3.36.1 | **Local-first. One read path.** Catalogue, prices, tax and rules read from local SQLite on every transaction, online or offline | [ADR-0013](adr/0013-local-first-point-of-sale.md) |
| 3.36.2 | Server publishes **signed, versioned bundles**; terminals apply deltas atomically | Derived |
| 3.36.3 | **Contended inventory uses leases**, not replication — TTL, automatic return, refusal on exhaustion | Derived |
| 3.36.4 | Seated inventory stays **blocked offline** | Ratified |
| 3.36.5 | Transactions written to a local journal and **committed before the cashier is acknowledged** | Derived |
| 3.36.6 | **Server re-prices every line on ingest.** Local price is the guest answer; the server is authoritative for the ledger | Derived |
| 3.36.7 | Three deployment profiles — **terminal-local, venue edge, thin** — one codebase | Derived |
| 3.36.8 | Venue edge node for mid and large venues. Turns WAN-down-LAN-up into a fully working venue | Derived |

### 3.37 Device drivers

| # | Position | Basis |
|---|---|---|
| 3.37.1 | **Build to open standards where they exist** — ESC/POS, UnifiedPOS, OSDP/IEC 60839-11-5. Not provisional work | [ADR-0015](adr/0015-standards-first-device-drivers.md) |
| 3.37.2 | Where no standard exists, define our interface **modelled on the nearest standard's command shape** and ship a mock adaptor | Derived |
| 3.37.3 | Vendor adaptors are bespoke work, quoted separately | ADR-0012 |
| 3.37.4 | The hardware model list is a **verification and procurement input**, not a design input | Derived |
| 3.37.5 | Cash drawer is not a separate driver — ESC/POS kick pulse through the printer | Derived |

### 3.4 Guest application distribution

| # | Position | Basis |
|---|---|---|
| 3.4.1 | **Tiered distribution.** Dedicated/Isolated tenants get branded native apps; Shared tenants get a branded PWA; a universal TICVAI app exists as a discovery surface only, deep-linking outward | Client decision |
| 3.4.2 | Branded apps are published under the **tenant's own** Apple Developer and Google Play accounts. TICVAI is granted App Manager access | App Store Review Guideline 4.2.6 — template apps must be submitted by the content provider |
| 3.4.3 | **Managed build pipeline.** TICVAI builds, signs and submits. Tenants do not export or self-publish | Version fragmentation, signing key custody, toolchain burden |
| 3.4.4 | Build-time set is minimised to: bundle ID, app name, icon, splash, signing identity, **tenant ID**, push certificates, deep-link domains. Everything else is runtime config | Every build-time item costs a store review cycle |
| 3.4.5 | Theming, imagery, copy, module visibility and feature flags are delivered via config API + OTA. A rebrand is a config publish, not a release | Derived from 3.4.4 |
| 3.4.6 | Upload validation enforces size/pixel limits (banner ≤ 1024px), font metrics and contrast ratios, with guidance shown to the tenant admin | 10 Aug 2026 §31 |
| 3.4.7 | **TICVAI attribution** appears in Settings → About and in the store listing description, non-configurable. Not on splash | 12 Aug 2026 §5 |
| 3.4.8 | **Tenant ID is baked at build time.** The app resolves tenant → cell endpoint once and caches it. A branded app never crosses a jurisdiction boundary | Derived from 3.3.1 |
| 3.4.9 | API contracts support **N-3 minor versions**. Control Plane tracks contract version per tenant per platform. Force-upgrade below the supported floor | Store review latency + tenant update adoption |
| 3.4.10 | Publishing, build status, review state and per-tenant version are **Control Plane** functions | Co-located with tenant registry, licensing, cell routing |

### 3.5 Known deviations from the requirement matrix

Deviations are deliberate and must be surfaced at acceptance testing.

| Requirement | Deviation | Reason |
|---|---|---|
| 2.7.x — sales permission restricted by workstation | Not implemented as a workstation-level permission | Superseded by 3.1.1 |
| 7.1.10 — configurable concurrent logins across terminals | Not implemented | Superseded by 3.1.3 |

---

## 4. Working Model

### 4.1 Unit of work

Flows, endpoints, and pages are built against **capabilities**, not job titles.
Actors are compositions of capabilities, validated against a matrix — they are not
a source of diagrams or endpoints.

### 4.2 Artefact naming

| Artefact | Convention |
|---|---|
| Capability | `Cnn` |
| Actor | `Ann` |
| Open issue | `CF-nn` |
| User flow | `UF-<Ann>-<DOMAIN>-<NNN>` |

Every user flow carries its source Requirement ID range in the footer.

### 4.3 Traceability

No artefact ships without provenance. A capability, page, or endpoint that cannot be traced
to a Requirement ID or a dated MoM decision is not scope.

---

## 5. Extensibility Principle

The platform targets 70+ venues. Every new venue arrives with hardware and third-party systems
not previously seen. Therefore:

- Payment terminals and access-control devices sit behind a **driver abstraction layer**
- Adding a vendor is configuration plus a driver, never a core change or a platform release
- Modules are independently licensable and toggleable per tenant

---

## 6. Glossary

The canonical glossary is maintained separately and derived from client-supplied definitions.
Terms carrying platform-specific meaning that must not drift between schema, API, and UI labels:

Event · Performance · Media · Entitlement · Component · Attribute · Envelope ·
Data Mask · Operating Area · Metric Sheet · Admission Profile · Access Point ·
Capacity Allocation · Sale Board · Workstation · Site

Schema field names, API resource names, and screen labels must use these terms consistently.

---

## 7. Open Issues

Open issues are tracked in the conflict register (`CF-nn`). Rules:

- An issue is **blocking** if it shapes schema, authorisation, or flow structure
- Blocking issues gate the artefacts they affect — work does not proceed around them
- Issues are closed by a dated MoM decision or an accepted `DESIGN` position, never by inference
- Conflicts between MoM decisions are escalated, not silently resolved by recency

---

## 8. Record Quality Standards

MoM decisions are the highest-authority artefact in the project. They must therefore state:

- **Who** decided (named, not "agreed")
- **What** was decided, in one unambiguous sentence
- **Which** prior decision it supersedes, if any

Decisions that contradict each other within the same record, or that omit the deciding party,
are returned for correction before being treated as binding.

---

## 9. Change Control

| Change type | Requires |
|---|---|
| Amend §2 source hierarchy | Joint sign-off, both sides |
| Amend §3 settled positions | Dated MoM decision |
| Promote `REF` or `DESIGN` to scope | Matrix entry or MoM decision |
| Add a §3.3 deviation | Architecture lead, logged and surfaced at UAT |

---

## 10. Revision History

| Version | Date | Change |
|---|---|---|
| 1.0 | 12 Aug 2026 | Initial. Source-of-truth hierarchy, settled authorisation and session positions, deviation log |
| 1.1 | 12 Aug 2026 | Added §3.3 Platform architecture — cell-per-tenant model, cell tiering, venue partitioning, repository topology, service-split criteria |
| 1.2 | 12 Aug 2026 | Cell redefined as Tenant × Jurisdiction; Region placement attribute; large multi-region set as design baseline; added §3.4 Guest application distribution (Option C, tiered) |
