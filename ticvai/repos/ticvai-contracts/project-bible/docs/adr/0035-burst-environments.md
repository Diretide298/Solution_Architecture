# ADR-0035: A flash sale gets its own environment, and it cannot be deleted until it has been reconciled

**Status:** Accepted · **amended 3 September 2026** — `synchronous_commit` moves from the server to
the statement ([below](#amendment--synchronous_commit-3-september-2026))
**Date:** 31 August 2026
**Related:** [ADR-0038](0038-cell-is-a-region-database-per-tenant.md), which supersedes [ADR-0014](0014-cell-per-region.md) and amends [ADR-0017](0017-deployment-models.md) · [ADR-0013](0013-local-first-point-of-sale.md) · [ADR-0031](0031-contention-and-locking.md) · [ADR-0033](0033-outbox-and-dead-letters.md) · CF-162

---

## Context

**Qossai described the failure on 31 July.** A ticketing platform his team installed for a theatre
in Bahrain went down when roughly thirty thousand people tried to buy at the same moment. *"The
outage took several days to resolve and ultimately cost the team the client relationship."*

**The client asked for three deployment scenarios on 24 August.** Two of them — an independent
tenant and a shared platform — are variations on the cell model and fit ADR-0014, which superseded ADR-0001 when a cell became able to hold many tenants. **The third,
dedicated infrastructure for large events and flash sales, is not a cell** and nothing in the
package modelled it. Recorded as CF-162 and open since.

### Why the traffic numbers do not describe the same system

**250,000 requests a day is 2.9 per second. Five thousand per second is 1,700 times that.**

**At 5,000 RPS the entire daily volume arrives in fifty seconds.** That is not a busy platform; it
is a queue of people buying one thing, and it touches **34 operations of 1,032 and 42 tables of
372.** Six services see no part of a ticket sale.

**Sizing the permanent platform for it means paying for the sale shape all year.** A stadium runs at
48 requests per second for 363 days and 6,000 for two.

---

## Decision

### A fifth cell kind

**`CellKind` gains `burst`**, alongside `shared`, `dedicated`, `onPremise` and `controlPlane`.

**The other four are places data lives. This one is a place data passes through.** That difference
is the whole ADR: it has a lifecycle the others do not, and a reconciliation obligation they do not
carry.

**It is not a jurisdiction.** It has no tenancy of its own, it reads a catalogue it does not own,
and it exists for one performance.

### The lifecycle, and the one edge that matters

```
requested -> provisioning -> warming -> live -> draining -> reconciling -> reconciled -> decommissioned
                    |            |                              ^______|
                    v            v                              resumable
                 failed       failed
```

**`decommissioned` is reachable only through `reconciled`.** `decommissionBurstEnvironment` returns
409 otherwise. **An environment torn down before its orders reach the permanent platform has lost
real money and real tickets**, and no path in the state model allows it.

**`failed` is reachable from `provisioning` and `warming` only.** Once an environment is `live` it
holds orders, and **there is no failure state that discards them** — a live environment in trouble
drains and reconciles whatever it has.

**Two transitions are time-driven.** `live -> draining` at `onSaleTo` plus a grace period, and
`reconciled -> decommissioned` when `autoDecommission` is set.

### Teardown is a mechanism, not a discipline

**$24 for a two-hour sale. $71 for six hours. $282 for a day. $8,587 for a month.**

**The risk is not the cost, it is forgetting**, and a month of forgetting costs more than the
platform the environment was protecting. **So teardown is tied to `catalogue.performance.onSaleTo`
rather than to somebody's calendar.**

**`catalogue.performance` already carries `onSaleFrom` and `onSaleTo`**, which is also what triggers
provisioning: **an environment requested when the load arrives is requested too late**, because
provisioning takes minutes and a sale takes seconds.

### Draining is not stopping

**A guest mid-checkout when the sale closes is allowed to finish.** A guest arriving after is told
the sale has ended. **`graceMinutes` exists because a queue does not empty at the instant the last
ticket sells.**

### Reconciliation, which is the half CF-162 left open

**The shape already exists one layer down.** `syncOrders` reconciles a till's offline journal: a
device id, a monotonic sequence, idempotent replay, and `sync.rejection` for what will not apply —
*kept, because a till that loses a rejected sale silently is worse than one that reports it.*

**Same three properties, one layer up**: an environment id in place of a device id, a sequence that
orders the replay, and the same rejection table. **Thirty thousand silently lost sales is worse than
thirty thousand reported ones.**

**Resumable, and the self-transition on `reconciling` is why.** A reconciliation interrupted at
order 18,000 of 30,000 continues from 18,000 rather than starting again.

### 🔴 The catalogue is a snapshot, and that is a policy question

**Not a replica.** The environment reads what was on sale at `snapshotTakenAt`.

**If the permanent platform changes a price during the sale, reconciliation has to decide which one
the guest paid.** `priceDivergencePolicy` names three answers and **has no default**:

**`honourSnapshot`** — what a guest expects, and it may undercharge.
**`honourCurrent`** — correct in the ledger, and it charges somebody a price they never saw.
**`reject`** — safe, and it turns a completed purchase into a support case.

**No default is deliberate.** Somebody chooses per sale, because the right answer depends on how
large the divergence is and who the venue would rather disappoint.

---

## Consequences

**Three services deployed, thirteen not.** **Identity is 1.8% of the weighted load and mandatory
anyway, because nothing sells without authentication** — a service can be small and still be
required.

**This ADR states a floor and no ceiling, and that is the decision.**

**A maximum is a cap on absorbing a peak nobody predicted**, and the peak is the entire reason this
environment exists. Sixty thousand seats over a two-hour window is 1,045 requests per second; the
same sale compressed into twenty minutes is 6,270. **A ceiling set from the first number fails the
second** — and failing at a ceiling is the Bahrain outage with a config value in front of it.

**Cost is bounded by duration rather than by a replica count.** The environment runs for the sale
and is torn down: $24 for two hours. **There is no runaway to protect against**, which is the usual
reason for a ceiling and does not apply here.

**`min` is the only replica number that is a decision** — traded against cold start, because under
five seconds to ready means the autoscaler can respond inside a burst and above it the floor has to
absorb what it cannot reach in time.

**`handoff/burst-scope.json` publishes `expectedAtTarget` as information, not as a limit.** It says
what 5,000 RPS implies at the declared triggers so a database and a connection pool can be sized;
it carries no authority to stop the autoscaler above it.

**An earlier draft named 20, 16 and 6 as maxima.** Nobody could show the workings, and the deeper
error was having a maximum at all: **the numbers were both unjustified and the wrong kind of
number.**

**`acquireInventoryHold` is the constraint and no amount of scaling relieves it.** Every buyer wants
the same rows; the lease path serialises under ADR-0031's `SKIP LOCKED`. **This is the number to
measure before anything else** — it is a property of the contention model, not of instance size.

**Which means the derived ceiling is an upper bound on throughput and not on usefulness.** Above
some replica count, more replicas are more waiters on one lock. `burst-scope.json` marks every
`max` as unverified for that reason, and it stays unverified until `tools/bench.py --pattern
hot-venue` runs against something.

**`synchronous_commit = off` on the burst database is a decision, not a setting.** A crash loses the
last few milliseconds of commits, which is a fair trade for fifty seconds of throughput and **a
data-loss bug if it is copied from a tuning guide.** *(Amended 3 September — the trade was right in
principle and this environment was not paying for it. See below.)*

**A new operational object somebody has to watch.** `listBurstEnvironments` exists because an
environment nobody is looking at is the one left running for a month.

---

## Alternatives considered

**Scale the shared cell for the peak.** Rejected: it pays for the sale shape for 363 days it is not
needed, and the spike is in one venue so the capacity would sit next to the tenant that needed it
rather than in it.

**A `dedicated` cell per large tenant, permanently sized for their worst day.** Rejected for the
same reason plus one more — **a stadium's worst day is 125 times its ordinary one**, and no
provisioning that survives the first also makes sense on the second.

**Queue-and-drain in the permanent platform: accept every request, process at a sustainable rate.**
Genuinely tempting, and rejected because **a guest waiting in a queue does not know whether they
have a ticket.** The Bahrain failure was not that the platform was slow; it was that nobody could
tell what they had bought.

**Let the CDN absorb it.** Handles the browse and does nothing for the buy — **`acquireInventoryHold`
cannot be cached**, and it is the operation that fails.

---

## Amendment — `synchronous_commit`, 3 September 2026

**The consequence above said `synchronous_commit = off` on the burst database was a decision rather
than a setting. It was, and the decision has been taken the other way.** All four configurations —
`deploy/c-flash-sale.yml` and the three variants — dropped it from the server on 31 August.

### What changed is the measurement, not the reasoning

**The trade is still a fair one where it is being paid for.** Fifty seconds of throughput against
the last few milliseconds of commits, in an environment that reconciles into the permanent platform
afterwards, is defensible.

**This environment was not paying for it.** It runs at a fraction of the statement ceiling — the
pooler's 80 server connections against a mean statement time put the wall far above what a sale
offers — so the flag was buying headroom that already existed, and the price was
acknowledged-commit durability **on the path where the commit is the seat allocation and the
payment capture.** A confirmed seat that vanishes in a crash is not a latency problem, and *"none
rejected, nothing lost"* is not a claim that survives the flag being set for those tables.

**A trade nobody is collecting on is not a trade.**

### The decision

**`synchronous_commit` stays ON at the server. It is turned off per statement, and only for
telemetry and analytics writes:**

```sql
SET LOCAL synchronous_commit = off;
```

**`SET LOCAL`, never `SET` — and this is the more important half.** Under pgbouncer's transaction
pooling a session-level `SET` leaks onto whichever connection the pooler hands out next. **The
order path then inherits a setting the analytics path chose, and nothing reports it.** That is the
production footgun rather than the durability trade, and [ADR-0032](0032-load-shedding-and-pooling.md)
already forbids session-scoped state for exactly this reason. **ADR-0032's pooling half is amended
by [ADR-0038](0038-cell-is-a-region-database-per-tenant.md)** — pools are per tenant database now —
but the rule being relied on here is its prohibition on session-scoped state, which the amendment
does not reach.

### Consequences

**🔴 The split is declared nowhere.** *"Telemetry and analytics writes"* is a sentence in one
compose header. No operation carries an annotation for it, nothing generates it, and no check
refuses a `SET` where a `SET LOCAL` belongs. **The next person who needs throughput has a comment
rather than a rule**, which is the shape of the original problem: this flag was set once without
being decided, and it read as a decision nobody remembered making.

**Turning it on tightens the lock, and [ADR-0037](0037-what-may-be-inside-a-lock.md) already
removed the collision.** An `fsync` costs 0.5–2 ms on SSD-backed WAL, and inside a row lock that
turns a 6 ms lease into 8 ms with the per-row ceiling falling to match. ADR-0037 forbids an `fsync`
inside a lock outright — acquire, release, then commit — so the durability comes back without the
lease paying for it. **Had these two been decided in the other order this would have been a
regression.**

**Every artefact that quoted the flag has been corrected**: `handoff/Burst Simulator.dc.html`,
`handoff/burst-simulator-README.md` and the viewer's burst map, which was asserting the setting in
prose while correctly reading its absence from the compose file two panels away.

### What this does not change

**Nothing else in this ADR.** The environment, its lifecycle, the reconciliation gate and the four
cost points stand as written.
