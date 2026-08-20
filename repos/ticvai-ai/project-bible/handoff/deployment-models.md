# Deployment models

**Four. One is the default; the others exist because a client asked or a law requires it.**
Full reasoning in [ADR-0017](../docs/adr/0017-deployment-models.md).

| | Where | Isolation | Operated by | When |
|---|---|---|---|---|
| **Shared** | TICVAI, UAE | Logical — RLS by scope | TICVAI | **Default** |
| **Dedicated** | TICVAI | Own database and cluster | TICVAI | Client pays for it |
| **Additional region** | TICVAI, elsewhere | Physical, in-jurisdiction | TICVAI | Residency requires it |
| **On-premise** | Venue hardware | Complete | **The client** | Client requires it |

## The rules that follow

**One UAE installation covers the pipeline.** A second region is provisioned when a deployment
requires it, not in anticipation. The trigger is residency — not latency, not capacity.
Capacity is answered by launching another cluster in the same region, which is cheaper and does
not multiply the compliance surface.

**A tenant can move up.** Shared to dedicated is `planTenantMigration` and
`executeTenantMigration`. The cheap start is not a trap, and saying so is what makes it
sellable.

**What the extra cost buys, stated plainly:** a dedicated cell survives an application bug that
a shared cell does not. On a shared cell, `FORCE` row-level security is the only thing between
two paying customers.

## On-premise — what changes

Everything below was designed assuming TICVAI can reach the cell.

| | |
|---|---|
| **Migrations** | The orchestrator cannot push. Updates are pull-initiated or physically delivered |
| **Version skew** | Permanent and legitimate, not transitional. Must not read as a defect |
| **Licensing** | A signed file verified locally. **An expired licence degrades, never stops** |
| **Cross-cell** | Requires reaching the issuing cell at redemption. May not be possible |
| **Support** | Blind. Diagnostics must be exportable by a non-engineer on site |
| **Backup and DR** | The client's responsibility, and they must be told in writing |
| **AI** | In-region inference has no endpoint unless the client buys hardware for it |

## Three decisions before the first on-premise sale

All three are commercial as much as technical. **CF-61.**

**Do on-premise venues participate in cross-cell entitlements?** Redeeming a pass issued
elsewhere needs the issuing cell reachable at that moment. Honest default: no.
Local-then-reconcile carries a double-redemption risk that needs a decision rather than an
assumption.

**What does an expired licence do?** Recommendation: degrade. A venue whose gates refuse entry
because a licence lapsed over a weekend is a worse outcome than one running unlicensed until
Monday.

**Who is contractually responsible for backups?** An on-premise client will ask what the RPO
is, and the answer is whatever their own schedule achieves. This is where the 62 uncounted
DR requirements (CF-60) land hardest.
