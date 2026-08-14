# Migration Rollout

> **Purpose:** Every schema change, across every cell  
> **Owner:** Dinesh  
> **Status:** **Week 1**


Every migration runs **once per cell**. Errors multiply by tenant count.

1. Merge only after **rollback is tested**, not assumed.
2. Apply to the **canary cell**. Verify schema version register updated.
3. Smoke test: the vertical slice runs end to end on canary.
4. Roll out to 10% of cells. Hold. Watch error rate, latency, replication lag.
5. Remainder, batched.
6. Update per-cell version in the Control Plane.

## Rules

- **No long-held lock on a hot table during trading hours.** A lock on `sales_order` is an outage across every venue in the cell
- `CREATE INDEX CONCURRENTLY` where available
- Resumable — a migration interrupted halfway must be safe to re-run
- Version skew between cells is expected. Contracts tolerate N-3 minor versions

## Failure

Stop the rollout. Do not proceed to the next batch. A migration that failed on one cell will fail on the rest.
