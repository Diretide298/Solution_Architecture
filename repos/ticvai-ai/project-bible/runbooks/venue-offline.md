# Venue Offline

> **Purpose:** A site loses connectivity  
> **Owner:** Dinesh  
> **Status:** **Week 2**


## Expected behaviour

The venue keeps trading. This is designed for, not an incident in itself.

| Component | Behaviour |
|---|---|
| POS | Switches automatically. Cash only. Capacity products blocked. Offline indicator visible |
| Scanner | Validates against local SQLite. Queues scans |
| Venue edge node | Serves access rules locally |
| Retail | **Blocked** — real-time inventory depletion required |
| Employee app | Read-only lookup |

## On detection

1. Confirm the alert is a venue-level outage, not a single device.
2. Verify the edge node is serving locally — check gate throughput, not connectivity.
3. Notify the venue's duty supervisor. They may need to switch to cash-only signage.
4. Do **not** force a sync. The orchestrator flushes automatically on restore, with jittered backoff so terminals do not retry in lockstep.

## On restore

1. Watch outbox backlog drain per device.
2. Check for `rejected` entries — these need operator attention and will not retry.
3. Reconcile capacity counters against Postgres.
4. Verify no duplicate orders — deduplication is by ULID, so duplicates indicate a client-side ID generation fault.

## Escalate if

Backlog does not drain · rejected entries appear in volume · capacity counters diverge · the edge node did not serve locally during the outage.
