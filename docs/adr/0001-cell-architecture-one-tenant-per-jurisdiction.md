# ADR-0001: Cell architecture — one tenant per jurisdiction

**Status:** Accepted — split rule **superseded by [ADR-0014](0014-cell-per-region.md)**;
isolation claim **amended 14 August 2026**  
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

---

## Amendment — 14 August 2026

**"Each tenant has its own isolated database" is no longer universally true.**

This ADR recorded that as a client decision on 10 August. On 14 August the client confirmed a
second model alongside it: a **shared TICVAI database holding many small tenants**, isolated
logically by scope, sold as the cheaper package. A tenant wanting physical isolation pays for
a dedicated cell and **can be migrated to one later** — the shared start is not permanent.

See the amendment in [ADR-0014](0014-cell-per-region.md) for the operative model.

### Two claims in this ADR that the shared cell breaks

**"Blast radius of a bad migration is one tenant."** On a shared cell it is every tenant on
that cell. This does not change the migration strategy — canary first, halt on failure — but it
does change what a canary is worth. A canary that is itself a shared cell risks many tenants;
a canary should be a **dedicated cell or the smallest shared one**, and the orchestrator should
prefer that rather than picking by size alone.

**"Own cloud environment, cluster and database per tenant."** True for dedicated cells only.
On a shared cell, isolation is `FORCE` row-level security and nothing else, which is why the
migration checker fails any table carrying `scope_path` or `venue_id` without a policy, and why
`platform.tenant` gained one on 14 August.

### What still stands

Cells exist for residency, blast radius and tiering. Region is still a placement constraint.
Cross-cell entitlements still work by pseudonymous link. None of that depends on how many
tenants share a cell.

### Worth saying to a client

A dedicated cell survives an application bug that a shared cell does not. That is the concrete
answer to what the extra cost buys, and it is more honest than describing the shared option as
equivalently isolated.

> **Cell kinds are now stated in [ADR-0017](0017-deployment-models.md)**, which consolidates
> the material amended into this ADR and into ADR-0014. This document remains the record of
> how the model got here; ADR-0017 is what is true now.
