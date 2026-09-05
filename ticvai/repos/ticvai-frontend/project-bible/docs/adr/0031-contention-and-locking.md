# ADR-0031: Contention is leased, not locked — and where a lock is unavoidable it is named

**Status:** Accepted
**Date:** 31 August 2026
**Related:** [ADR-0013](0013-local-first-point-of-sale.md) · [ADR-0016](0016-read-write-separation.md) · CF-115

---

## Context

**A flash sale fails at one operation.** `acquireInventoryHold` is where thirty thousand people
want the same rows, and the 31 July minute records what that costs: a Bahrain theatre where the
platform went down and the outage cost the client relationship.

**The package already decided the shape.** CF-115 settled that contended inventory is leased rather
than reserved, and `catalogue.inventory_hold` and `seating.seat_hold` are the tables. **What it
never said is how the lease is taken.**

**Nothing in 1,025 operations declares a locking strategy.** Every write carries an idempotency key
and a conflict policy — `serverWins` on 926, `lastWriterWins` on 33, `append` on 66 — and those
resolve a *collision after the fact*. **They do not stop two callers reading the same free seat.**

---

## Decision

### Optimistic by default, and it already is

**`serverWins` on 926 operations is optimistic concurrency**: read, act, and let the server refuse
if the row moved. **That is correct for almost everything**, because almost nothing is contended.

**A booking screen edited by two managers is a rare collision.** Paying for a lock on every write
to prevent it is the wrong trade.

### Pessimistic where the row is contended, and only there

**Four operations take a row lock**, declared as `x-ticvai-lock: rowExclusive`:

```
acquireInventoryHold      catalogue.inventory_hold
createSeatHold            seating.seat_hold
captureStoredValue        orders.stored_value_authorisation
authoriseWalletSpend      platform.wallet_authorisation
```

**These are the operations where two callers want the same row and both cannot have it.** Optimistic
retry under contention is worse than a lock: at 5,000 RPS every retry is another read, and the
retry storm is the outage.

**`SELECT ... FOR UPDATE SKIP LOCKED` on the lease path.** A buyer who cannot get seat 14 should get
seat 15 in the same query rather than fail and retry — **`SKIP LOCKED` turns contention into
throughput** where the caller does not care which row it gets.

**Plain `FOR UPDATE` where they do care.** Somebody choosing seat 14 specifically waits or is told
no; they must not silently receive seat 15.

### A lease expires; a lock does not

**This is the property that matters and CF-115 chose it.** A held seat whose holder closes the
browser is free again in ten minutes. **A locked row whose holder crashes is locked until somebody
notices.**

**So the lock is held for the duration of the statement, not the duration of the decision.** The
lease row is the long-lived thing and the lock only protects writing it.

### Distributed locks, and where they are actually needed

**Not for rows.** Postgres already serialises those and a Redis lock over a database row is two
sources of truth.

**For scheduled work.** `ingestFxRates` at 06:00, `runFxRevaluation` at close, retention sweeps —
**with three replicas of a service, three instances wake up.**

**`x-ticvai-singleton: true`** on those operations. Implementation is a Postgres advisory lock
rather than Redis: **the work is transactional against the same database, so the lock belongs
there.** A Redis lock that expires mid-transaction leaves two writers and no error.

---

## Consequences

**`acquireInventoryHold` becomes the number the benchmark exists to find.** Lease throughput on one
hot performance is a property of the contention model, not of instance size, and **no amount of
horizontal scaling helps a contended row.**

**Four operations get slower under contention and correct.** That is the trade and it is worth
saying to whoever reads the p99.

**`check-package` enforces the declaration**: an operation writing `inventory_hold`, `seat_hold`,
`stored_value_authorisation` or `wallet_authorisation` must declare a lock, and an operation
declaring one must write one of those.

---

## Alternatives considered

**Optimistic everywhere with retry.** Rejected: at 5k RPS the retry storm is the failure mode, and
the first Bahrain-shaped incident would be caused by the mitigation.

**Pessimistic everywhere.** Rejected: 926 operations paying for a lock to protect a collision that
happens weekly.

**Serialisable isolation on the lease path.** Rejected as a first move — it pushes the problem into
serialisation failures the caller has to retry, which is the retry storm again with a different
error code. **Worth revisiting if `SKIP LOCKED` measures badly.**
