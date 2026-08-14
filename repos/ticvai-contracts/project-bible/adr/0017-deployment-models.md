# ADR-0017 — Deployment models

**Status:** Accepted
**Date:** 14 August 2026
**Consolidates:** the cell-kind material in [ADR-0001](0001-cell-architecture-one-tenant-per-jurisdiction.md)
and [ADR-0014](0014-cell-per-region.md), both of which have been amended twice. This ADR is
the operative statement; those two remain the record of how it got here.

---

## Context

Cell architecture has been settled in pieces since 12 August, and each piece arrived as an
amendment to an ADR written before it. Three separate documents now describe overlapping parts
of one model, and one of them is titled after a rule that no longer holds.

The 14 August discussion settled the remaining question and added one nobody had asked. This
ADR states the whole model once.

## Decision

**Four deployment models. One is the default; the others exist because a client asked or a law
requires it.**

| | Where it runs | Isolation | Who operates it |
|---|---|---|---|
| **Shared** | TICVAI infrastructure, UAE | Logical — RLS by scope | TICVAI |
| **Dedicated** | TICVAI infrastructure | Physical — own database and cluster | TICVAI |
| **Additional region** | TICVAI infrastructure, elsewhere | Physical, and in-jurisdiction | TICVAI |
| **On-premise** | The venue's own hardware | Complete. Nothing leaves the site | The client |

### 1. Shared — the default

**One TICVAI installation in the UAE serves every tenant that does not need otherwise.**
Isolation is `FORCE` row-level security on a scope path, and nothing else.

This is where a tenant starts unless something specific rules it out. It is the cheapest to
run and the cheapest to sell, and it is why the migration checker fails any table carrying
`scope_path` or `venue_id` without a policy: on a shared cell that policy is the only thing
between two paying customers.

### 2. Additional regions — demand-driven, not pre-built

**A second region is provisioned when a deployment requires it, not in anticipation.**

The trigger is residency: a venue whose jurisdiction requires its data to stay there. Not
latency, not capacity — capacity is answered by launching another cluster in the same region
(ADR-0016), which is cheaper and does not multiply the compliance surface.

This inverts what ADR-0001 assumed. It read the multi-jurisdiction case as the normal one and
sized the architecture for it. In practice the UAE installation covers the pipeline, and a
second region is a project with its own timeline, its own DESC-equivalent conversation and its
own cost. The machinery to do it exists and stays unused until something needs it.

### 3. Dedicated — what the extra cost buys

A client wanting physical isolation gets their own cell. **They can start shared and move
later** — `planTenantMigration` and `executeTenantMigration` — which is what makes the shared
tier sellable rather than a trap.

Worth saying plainly to a client asking why it costs more: **a dedicated cell survives an
application bug that a shared cell does not.** That is more honest than describing the shared
option as equivalently isolated, and it is the actual difference.

### 4. On-premise — the client's hardware, and the client's problem

**The platform installed on venue hardware. Nothing leaves the site.**

This is the model that changes the most, and none of it was designed for. Seven consequences,
each of which is a decision rather than a detail.

**The orchestrator cannot push.** Every migration mechanism written so far assumes TICVAI can
reach the cell. An on-premise installation may sit behind a firewall with no inbound route.
Updates are **pull-initiated by the site or physically delivered**, and the platform must
tolerate a site that has not called home for a month.

**Version skew is permanent, not transitional.** ADR-0016's skew report distinguishes
mid-rollout skew from unexplained skew. An on-premise cell is a third case: **legitimately
behind, indefinitely, because the client has not scheduled the window.** It should not appear
as a defect and should not be counted against a rollout.

**Licensing cannot be enforced by a Control Plane the site cannot reach.** A signed licence
file with an expiry, verified locally, is the only mechanism that works. It also means an
expired licence must **degrade rather than stop** — a venue whose gates refuse entry because a
licence lapsed over a weekend is a worse outcome than one running unlicensed until Monday.

**Cross-cell entitlements do not work both ways.** A pass sold elsewhere and redeemed at an
on-premise venue requires that venue to reach the issuing cell at the moment of redemption. It
may not be able to. Either the on-premise venue is excluded from cross-cell programmes, or
redemption is local-then-reconcile with the double-redemption risk that carries.
**This needs a decision before the first on-premise sale**, and the honest default is
exclusion.

**Support is blind.** Health reporting is outbound-only where it exists at all. A support
engineer cannot look at the cell, so diagnostics must be exportable by someone on site, and the
product needs to be diagnosable by a person who is not an engineer.

**Backup and disaster recovery become the client's responsibility**, and they must be told so
in writing. This is where the 62 uncounted DR requirements (CF-60) land hardest: an on-premise
client will ask what the RPO is, and the answer is whatever their own backup schedule achieves.

**AI is degraded or absent.** In-region inference (ADR-0009) assumed a cell in a cloud region
with a model endpoint. An on-premise site has neither unless the client buys hardware for it.
Conversational features either call out — which contradicts "nothing leaves the site" — or do
not run.

## Consequences

**`CellKind` gains `onPremise`.** Four values: `shared`, `dedicated`, `onPremise`,
`controlPlane`.

**The Control Plane holds a record it cannot reach.** An on-premise cell is registered for
licensing and support purposes with `isReachable: false`, and every operation that assumes
reachability must handle its absence rather than timing out.

**Three things must be decided before the first on-premise sale**, and all three are commercial
as much as technical: whether on-premise venues participate in cross-cell entitlements, what an
expired licence does, and who is contractually responsible for backups.

### Costs accepted

| | |
|---|---|
| Four models is four things to test | Real. Mitigated by the first three sharing one codebase and differing only in provisioning |
| On-premise is a different support product | Accepted. It should be priced as one |
| Cross-cell may exclude on-premise venues | Accepted as the default, revisited if a client needs otherwise |
| A second region is a project, not a setting | Accepted. The alternative is paying for capacity nobody uses |

## Alternatives considered

**Cloud only.** Cleanest, and unavailable — clients in this sector do ask for on-premise, and
some jurisdictions will require it before this platform is three years old.

**On-premise as a shipped appliance rather than an installation.** Genuinely better for support
and version control, and much more product than a first release should take on. Worth revisiting
once there is more than one on-premise client.

**Pre-provisioning a second region.** Rejected above. Capacity is answered by another cluster
in the same region; residency is answered by a project when residency is actually required.
