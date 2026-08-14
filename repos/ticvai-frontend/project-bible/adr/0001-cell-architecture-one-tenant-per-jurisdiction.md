# ADR-0001: Cell architecture — one tenant per jurisdiction

**Status:** Accepted — split rule **superseded by [ADR-0014](0014-cell-per-region.md)**  
**Date:** 12 August 2026

## Context

70+ venues across multiple tenants. Client decision (10 Aug 2026): each tenant has its own isolated database, with all sales channels connecting to it. Client requirement: a venue operating in a jurisdiction expects its infrastructure in that jurisdiction. Oman and UAE are separate jurisdictions within a single tenant's portfolio.

## Superseded in part — 13 August 2026

**The split rule is now Cell = Tenant × Region ([ADR-0014](0014-cell-per-region.md)).**
Jurisdiction is no longer the split point; it is a *placement constraint* on regions.

Everything else in this ADR stands: cell isolation, tiering, the Control Plane registry,
and the reasons cells exist at all.

The amendment below is retained for the record and is no longer the operative rule.

---

### Withdrawn amendment

| Split | Status | Basis |
|---|---|---|
| **Across jurisdictions** | **Mandatory.** Regions in different countries are always different cells | Residency; client expectation that infrastructure sits in-country |
| **Within a jurisdiction** | **Available, not default.** Two regions in the same country share a cell unless placement says otherwise | Load, latency or client preference |

Region already carries a `placement` attribute, so splitting within a jurisdiction is a
configuration change rather than a redesign. ADR-0010 supplies the cross-cell machinery, so
a tenant split this way loses no capability.

**Default is one cell per tenant per jurisdiction**, because splitting within a jurisdiction
costs and buys little:

| Cost of splitting within a jurisdiction | |
|---|---|
| Cross-region features become cross-cell | A pass valid at two venues in the same country stops being a single order and becomes a delegated redemption |
| Guest identity fragments domestically | Two records plus a link, where one record would do |
| Cost floor multiplies | One per region rather than one per country |
| Migration and backup targets multiply | Same |

| Benefit | |
|---|---|
| Blast radius per region | Real, but a bad migration is already canary-gated |
| Independent scaling | Rarely needed — a single primary absorbs a tenant's aggregate write load with headroom |
| Latency | Only material where regions are geographically distant |

**Recommendation: split within a jurisdiction only when load or a client requirement forces
it.** Not as a default posture.

## Decision

**Cell = Tenant × Jurisdiction.** One isolated deployment — own cloud environment, cluster and database — per tenant per jurisdiction. Placement is a **Region** attribute: `shared` | `dedicated:{cloud}:{region}` | `client_hosted:{endpoint}`. A tenant may be mixed across regions.

## Consequences

- Noisy neighbour is structurally impossible across tenants
- Blast radius of a bad migration is one tenant
- Residency is satisfied by placement, not by filtering
- Client-hosted tenants use the same code path
- **Deployment fans out across N cells.** Progressive rollout, canary-first, is mandatory
- Cross-region reporting must come from a central warehouse, not from cells
- Per-cell cost floor requires a shared tier for small tenants

## Alternatives

| Rejected | Why |
|---|---|
| Shared multi-tenant cluster | Fails residency; noisy neighbour; connection exhaustion |
| Cell per tenant, ignoring jurisdiction | An Omani venue's data would sit in Dubai |
| Cell per venue | Breaks cross-venue passes, wallets, memberships and consolidated reporting |
