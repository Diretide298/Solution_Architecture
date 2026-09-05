# ADR-0037: A lock holds one statement, not a transaction

**Status:** Accepted
**Date:** 31 August 2026
**Related:** [ADR-0031](0031-contention-and-locking.md) · [ADR-0032](0032-load-shedding-and-pooling.md), whose pooling half is amended by [ADR-0038](0038-cell-is-a-region-database-per-tenant.md) · [ADR-0035](0035-burst-environments.md), amended 3 September to move `synchronous_commit` from the server to the statement — **which this ADR is the reason it is safe to do**, since an `fsync` inside a lock is one of the things forbidden here · CF-115

---

## Context

**A Postgres row lock costs microseconds. `acquireInventoryHold` was measured at six milliseconds**,
which is a factor of roughly five hundred, and the difference is what the transaction does while
holding it.

**Inside the lock**: a Redis read for the idempotency key, a `platform.workstation` read, a
`catalogue.channel_capacity` read, then the write.

**Two of those have nothing to do with the capacity decision.** `platform.workstation` is *who is
holding*, resolvable from the session. The idempotency check is *have I seen this request*, which
is answerable before a transaction exists.

**The third is the network.** A Redis round trip inside a Postgres transaction means the row lock
is held across a hop to another process on another host.

### Why this was not visible

**ADR-0031 established that contended rows take a lock and that the lease duration is the
ceiling.** It did not say what may be inside one — so the contention model was correct and the
number was five hundred times worse than it needed to be.

**And the mitigation being designed made it invisible.** A sharding variant widens the wall by
sixteen; **shrinking the lease widens it by twelve without shards, fragmentation or
reconciliation.** The arithmetic:

```
6.0 ms lease   ->     167 holds/s per row
16 shards      ->   2,667 holds/s   (the wall, widened)
0.5 ms lease   ->   2,000 holds/s   per row, unsharded
```

**Nobody asked whether the wall needed to be that thick before proposing to widen it.**

---

## Decision

**A transaction holding a row lock does exactly three things: read the row, decide, write the row.**

**Nothing else may be inside it.** Specifically:

**No network call to another store.** Redis, an HTTP call, a queue publish — **a lock held across a
hop is a lock held for the latency of the slowest thing on the path**, and the path is not under
the transaction's control.

**No read the decision does not use.** `platform.workstation` identifies the holder and is resolved
from the session before the transaction opens. **A read that could have happened earlier and did
not is lock time somebody is paying for.**

**No fsync.** ADR-0032 covers this from the other side: an `fsync` inside the lock adds 0.5–2 ms and
**turns a 6 ms lease into 8 ms.** Commit outside the lock — acquire, release, then commit the
order.

**No idempotency check.** It answers *have I seen this request*, which is true or false before any
row is touched. **Checking it inside the lock means every duplicate request pays the contention
cost of a real one.**

### The four operations this applies to

**All four declaring `x-ticvai-lock` under ADR-0031**, and all four had the same shape:

```
acquireInventoryHold    cache:idempotency + workstation + channel_capacity, inside
createSeatHold          cache:idempotency, inside
authoriseWalletSpend    cache:idempotency, inside
captureStoredValue      two-table write, one of them not contended
```

**`captureStoredValue` is the interesting one**: it writes `orders.stored_value_authorisation` and
`retail.wallet_transaction` in one transaction. **The second is an append to an uncontended table
and does not need the lock** — it needs the same transaction, which is not the same requirement.

### What this does not decide

**Whether the lock is needed at all.** A guarded decrement —
`UPDATE ... SET remaining = remaining - $1 WHERE remaining >= $1` — is one statement with no
explicit lock and **a ceiling around 91,000 per second.**

**It is the better answer and it is not free.** It commits the reservation immediately, so
`expires_at` stops being a safety net and becomes load-bearing: **a browser closed mid-checkout has
taken a seat, and a sweeper has to give it back.** CF-115 chose leases over reservations for
exactly that property, and a guarded decrement keeps it while moving it from *the lock expires* to
*something reverses the decrement*.

**Deferred until the sweeper is designed**, not rejected.

---

## Consequences

**The lease measurement becomes the acceptance criterion.** `tools/bench.py` reports
`holdContentionMs`; **under this ADR it should read under one millisecond**, and a figure above that
means something is inside the lock that this decision forbids.

**Variant C stops being interesting.** It widens a wall that shrinking the lease shows did not need
to be that thick — **and it carries fragmentation the lease change does not.** It stays in
`deploy/variants/` as a measurement, not a candidate.

**🔴 The idempotency check moving outside the transaction has a real edge.** Two concurrent
duplicates can both pass the check before either writes. **The write must still be idempotent** —
`cache:idempotency` is a fast path, not the guarantee, and 660 operations already carry a key for
this reason.

**And a lock this short changes what the pooler is for.** At 0.5 ms a connection is returned almost
immediately, so transaction pooling stops being a mitigation for lock waits and goes back to being
what ADR-0032 describes: connection multiplexing — **amended by ADR-0038, which puts the pool per tenant database**, so the multiplexing is the same mechanism against a smaller ceiling.

---

## Alternatives considered

**Shard the contended row** (variant C). Rejected as a first move: **it widens the wall by sixteen
where this widens it by twelve**, and it costs sub-pool fragmentation — fifteen shards empty and one
holding four is a performance that looks sold out to most buyers.

**Move the lease to Redis.** Genuinely faster and it **moves the authoritative answer to "who holds
this seat" out of the transactional store**, buying throughput with a correctness obligation. Worth
measuring; not worth taking before the cheap change.

**Optimistic retry on the counter.** Rejected under ADR-0031 for the reason that still holds: at
5,000 RPS the retry storm is the failure, and **a retry that loses still consumed a connection.**
