# ADR

> **Purpose:** Architecture Decision Records  
> **Owner:** Chinmay  
> **Status:** Living

One file per decision: `NNNN-short-title.md`. Format: Context · Decision · Status · Consequences · Alternatives.

**A closed conflict becomes an ADR.** The [conflicts register](../registers/conflicts.md) tracks the question; the ADR records the answer and why — so that in a year nobody reconstructs the reasoning from seven MoM documents.

| # | Decision | Status | Closes |
|---|---|---|---|
| [0001](0001-cell-architecture-one-tenant-per-jurisdiction.md) | Cell architecture | **Superseded in part by 0014** | — |
| [0002](0002-authorisation-is-user-driven-not-workstation-driven.md) | Authorisation is user-driven, not workstation-driven | Accepted | CF-03 |
| [0003](0003-conditional-role-selection-at-login.md) | Conditional role selection at login | Accepted | CF-01 |
| [0004](0004-single-session-per-user.md) | Single session per user | Accepted | CF-02, CF-28 |
| [0005](0005-venue-isolation-by-partitioning-not-separate-databases.md) | Venue isolation by partitioning, not separate databases | Accepted | — |
| [0006](0006-tiered-guest-app-distribution.md) | Tiered guest-app app distribution | Accepted | CF-13 |
| [0007](0007-hybrid-repository-topology.md) | Hybrid repository topology | Accepted | — |
| [0008](0008-money-carries-per-region-scale.md) | Money carries per-region scale | Accepted | — |
| [0009](0009-ai-data-residency.md) | AI data residency — architectural, not storage-location | Accepted | **CF-20** |
| [0010](0010-cross-jurisdiction-entitlements.md) | Cross-jurisdiction entitlements — home-cell ownership with delegated redemption | Accepted | **CF-31** |
| [0011](0011-hierarchy-is-binding.md) | The hierarchy is binding — seven levels confirmed | Accepted | **CF-34, CF-27** |
| [0012](0012-queue-integration-adaptor-first.md) | Queue integration — adaptor-first, vendor deferred | Accepted (partial) | **CF-33** |
| [0013](0013-local-first-point-of-sale.md) | Local-first point of sale — one read path, leases, local journal | Accepted | **CF-15** |
| [0014](0014-cell-per-region.md) | **Cell per region** — supersedes the jurisdiction-only split | Accepted | **CF-32** |
| [0016](0016-read-write-separation.md) | Read and write paths are separated, routing declared per operation | Accepted |
| [0017](0017-deployment-models.md) | Deployment models — shared, dedicated, additional region, on-premise | Accepted |
| [0018](0018-configuration-scope.md) | Configuration scope — three levels, nearest ancestor wins, venue is the floor | Accepted |
| [0015](0015-standards-first-device-drivers.md) | Standards-first device drivers — ESC/POS, UnifiedPOS, OSDP | Accepted | — |

## Still needed

Decisions taken but not yet written up: contract-first delivery model · offline conflict policy per entity · PII separation from the append-only ledger · AI phasing.
