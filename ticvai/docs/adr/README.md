# ADR

> **Purpose:** Architecture Decision Records  
> **Owner:** Chinmay  
> **Status:** Living

One file per decision: `NNNN-short-title.md`. Format: Context · Decision · Status · Consequences · Alternatives.

**A closed conflict becomes an ADR.** The [conflicts register](../registers/conflicts.md) tracks the question; the ADR records the answer and why — so that in a year nobody reconstructs the reasoning from seven MoM documents.


**The principles beneath these are in [../principles.md](../principles.md)**, which is shorter
and usually enough to predict what an ADR says.
| # | Decision | Status | Closes |
|---|---|---|---|
| [0001](0001-cell-architecture-one-tenant-per-jurisdiction.md) | Cell architecture — one tenant per jurisdiction | **Superseded** by 0014 and 0017 | — |
| [0002](0002-authorisation-is-user-driven-not-workstation-driven.md) | Authorisation is user-driven, not workstation-driven | Accepted | CF-03 |
| [0003](0003-conditional-role-selection-at-login.md) | Conditional role selection at login | Accepted | CF-01 |
| [0004](0004-single-session-per-user.md) | Single session per user | Accepted | CF-02, CF-28 |
| [0005](0005-venue-isolation-by-partitioning-not-separate-databases.md) | Venue isolation by partitioning, not separate databases | Accepted — confirmed by 0038, **not yet implemented** | — |
| [0006](0006-tiered-guest-app-distribution.md) | Tiered guest-app app distribution | Accepted | CF-13 |
| [0007](0007-hybrid-repository-topology.md) | Hybrid repository topology | Accepted | — |
| [0008](0008-money-carries-per-region-scale.md) | Money carries per-region scale | Accepted | — |
| [0009](0009-ai-data-residency.md) | AI data residency — architectural, not storage-location | Accepted | **CF-20** |
| [0010](0010-cross-jurisdiction-entitlements.md) | Cross-jurisdiction entitlements — home-cell ownership with delegated redemption | Accepted | **CF-31** |
| [0011](0011-hierarchy-is-binding.md) | The hierarchy is binding — seven levels confirmed | Accepted | **CF-34, CF-27** |
| [0012](0012-queue-integration-adaptor-first.md) | Queue integration — adaptor-first, vendor deferred | Accepted (partial) | **CF-33** |
| [0013](0013-local-first-point-of-sale.md) | Local-first point of sale — one read path, leases, local journal | Accepted | **CF-15** |
| [0014](0014-cell-per-region.md) | **Cell per region** — supersedes the jurisdiction-only split | **Superseded** by 0038 | **CF-32** |
| [0016](0016-read-write-separation.md) | Read and write paths are separated, routing declared per operation | Accepted |
| [0017](0017-deployment-models.md) | Deployment models — shared, dedicated, additional region, on-premise | Accepted — amended by 0038 |
| [0018](0018-configuration-scope.md) | Configuration scope — three levels, nearest ancestor wins, venue is the floor | Accepted |
| [0019](0019-dynamic-bundle-pricing.md) | A dynamic bundle has a fixed price and a variable allocation | Proposed |
| [0020](0020-ai-isolation-boundary.md) | Where AI runs, and what it is isolated from | Proposed |
| [0021](0021-qdrant-partitioning.md) | Qdrant — one collection per embedding model, tenant is the shard, scope is the filter | Proposed |
| [0022](0022-conflict-policy.md) | Conflict policy is declared per operation, from a closed set of four | Accepted |
| [0023](0023-pii-separation.md) | Personal data lives apart from the append-only ledger | Accepted |
| [0024](0024-contract-first-delivery.md) | The contract is the deliverable, written before anything else | Accepted |
| [0025](0025-one-audience-field.md) | One field says who may call an operation | Accepted |
| [0015](0015-standards-first-device-drivers.md) | Standards-first device drivers — ESC/POS, UnifiedPOS, OSDP | Accepted | — |
| [0038](0038-cell-is-a-region-database-per-tenant.md) | **A cell is a region, and a database per tenant inside it** | Accepted | **CF-161** |
| [0039](0039-control-plane-and-tenant-database-lifecycle.md) | The control plane is a database of its own, and a tenant database is the unit | Accepted | — raises **CF-167** |
| [0040](0040-a-cell-may-hold-more-than-one-instance.md) | A cell is a region; a region may need more than one instance | Accepted | — amends 0038 |
| [0041](0041-a-command-centre-is-a-saved-dashboard.md) | A command centre is a saved dashboard, not a screen | Accepted | — raises **CF-169** |
| [0042](0042-when-a-region-grows-and-where-a-tenant-lands.md) | When a region grows, and where a tenant lands | Accepted — one number pending sign-off | **CF-168** |
| [0043](0043-the-control-plane-splits-on-personal-data.md) | The control plane splits on personal data | Accepted | **CF-167** |
| [0044](0044-which-tables-partition-by-venue.md) | Which tables partition by venue | **Proposed** — needs sign-off before any DDL | — completes 0005 |
| [0045](0045-every-order-carries-a-proven-contact.md) | **Every order carries a proven contact, and the gate is the checkout page** | Accepted | **CF-172** |
| [0046](0046-on-premise-has-two-configurations.md) | **On-premise has two configurations, and the difference is a control channel** | Accepted | **CF-61** — amends 0017, closes the AI question in 0020 |
| [0047](0047-how-long-data-is-kept-and-where-it-goes-next.md) | **How long data is kept, and where it goes next** | Accepted — one number pending | **CF-64** (closed), **CF-165** — amends 0042 |
| [0048](0048-guest-recurring-billing-is-commerce.md) | **Guest recurring billing is commerce, not the Control Plane** | Accepted | **BL-100** — relates to 0039, 0043, 0028 |

> **This table is twelve entries short.** 0026 to 0037 are on disk and were never added to it —
> the index has not kept up since 24 August. 0038 is here because it supersedes two of the rows
> above it, and a supersession that is not visible in the index is a superseded ADR somebody
> still reads as current. **0040 to 0045 were added 18 September**, **0046 on 19 September**,
> **0047 and 0048 on 21 September** — 0047 was written the day before and added a day late, which
> is the same lapse this note has been describing since August. The gap is now 0026–0037 only.

## Still needed

Two remain, and both are blocked rather than unwritten:

**AI phasing** — CF-57 and CF-14 are open on what is in Wave 1 and whether the guest concierge is
in it at all. Writing this before the client answers would record an assumption as a decision.

**The embedding model** — gated on the benchmark run in ADR-0021's addendum, then on real tenant
content. The architecture does not wait on it.

## Status vocabulary

Four values, and a status must **lead** with its state rather than bury it.

| | |
|---|---|
| **Accepted** | In force |
| **Accepted in part** | In force with a named carve-out, and the carve-out says which |
| **Proposed** | Written and not yet reviewed by anyone but its author |
| **Superseded** | Replaced. **Do not cite its Decision section** |

`check-package.py` enforces the set, and fails any ADR citing a superseded one without naming
the supersession. **Both rules exist because of CF-97**: ADR-0001 (retired — see ADR-0014 and ADR-0017)'s status read
*"Accepted — split rule superseded by ADR-0014"*, and a careful reader took the first word and
built a cross-tenant isolation defect on it.
