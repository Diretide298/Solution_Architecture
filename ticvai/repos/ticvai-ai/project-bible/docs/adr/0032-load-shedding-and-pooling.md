# ADR-0032: A service refuses early or fails late — pooling, backpressure and breakers

**Status:** Accepted — pooling amended by [ADR-0038](0038-cell-is-a-region-database-per-tenant.md).
Shedding, backpressure and breakers stand as written. **The connection arithmetic below is per
database, and there is now one database per tenant** — *"four hundred client connections share forty
server ones"* is a statement about one tenant. **The cap is a per-tenant limit, not a reservation,
and the primary's connections are a shared budget** — amended again by
[ADR-0040](0040-a-cell-may-hold-more-than-one-instance.md), which also gives the region a second
instance when one is not enough.
**Date:** 31 August 2026
**Related:** [ADR-0016](0016-read-write-separation.md) · [ADR-0028](0028-service-decomposition.md) · [ADR-0031](0031-contention-and-locking.md) · CF-161

---

## Context

**A service under load queues until it dies.** Nothing in the package declares a limit, a shed
policy or a breaker, so the default behaviour of every service is to accept work it cannot do and
discover that fact at the timeout.

**Three specific gaps, all runtime rather than schema**, which is why a contracts-first package did
not surface them:

**Connections.** Twenty Catalogue replicas at twenty connections each is four hundred against a
primary configured for five hundred — **and Catalogue is one of sixteen services.** The shared tier
stops scaling around six replicas and the bottleneck looks like the database.

**Cache expiry.** `cache:resolution` is read on every authorised call. **When it expires at 5,000
RPS, every request goes to the database at the same instant.**

**Provider outages.** BL-151 already names it: *a provider outage with no fallback is every AI
surface going dark at once.* Named, not built.

---

## Decision

### Connection pooling is infrastructure, not a service concern

**pgbouncer in transaction mode, in front of every Postgres.** Services connect to the pooler and
never to the primary.

**Transaction mode, not session mode.** Session mode holds a server connection for the life of a
client connection and buys nothing; transaction mode returns it at commit, which is what lets four
hundred client connections share forty server ones.

**What this forbids**: session-scoped state — prepared statements across transactions, `SET`
outside one, advisory locks held between statements. **ADR-0031's singleton lock is taken and
released inside one transaction for exactly this reason.**

**`PG_POOL_MAX` per service is sized against the pooler, not the primary.** A service may hold
twenty; the pooler decides how many reach Postgres.

**The pooler's budget is per database, and ADR-0038 made the number of databases grow with
sales.** `default_pool_size` is a cap on server connections for one database, so what reaches
Postgres is that figure times the number of tenant databases, plus one for `control`. Amended 5
September against the figure that was missing when ADR-0038 raised this: **ten tenants at go-live,
growing.**

| tenants | databases | server connections | of `max_connections = 500` |
|---:|---:|---:|---:|
| 3 | 4 | 160 | 32% |
| **10** | **11** | **440** | **89%** |
| 11 | 12 | 480 | 97% |
| 12 | 13 | 520 | **over** |

**Read that as a worst case, not a ceiling.** It is the column where every tenant peaks at full
pool depth in the same moment. **`MIN_POOL_SIZE` is unset in every configuration**, so pgbouncer's
default of zero applies: a provisioned tenant holds no server connection until it transacts and
gives it back at idle timeout. Ten tenants at three in the morning hold nothing.

**So the sum of the caps is deliberately allowed to exceed `max_connections`.** A cap is what one
tenant may take, not what it has taken, and sizing the sum to fit would give each tenant less on the
day a single one is busy — which is the day it matters. **What is monitored is concurrent server
connections against the primary's limit**, because tenant count says nothing about load.

**Idle tenants are free, and that is what makes this sizeable.** `min_pool_size` is unset, so
pgbouncer opens server connections on demand and returns them at `server_idle_timeout`. A
provisioned tenant that is not transacting holds nothing. **So the figure to size against is
concurrent busy tenants, not provisioned ones** — and 440 is the Saturday-evening worst case where
every venue is trading at once, which is exactly when they do.

**A sustained approach to that limit is the signal, and there are three answers to it.** Raise
`max_connections`, which is bounded — every backend is a process costing memory used or not. Lower
`default_pool_size`, which is bounded differently and worse: it trades a platform limit for a
per-tenant one. Or **add an instance to the region**, which is unbounded and is what
[ADR-0040](0040-a-cell-may-hold-more-than-one-instance.md) decides. The first two are tuning; only
the third changes the shape of the limit.

**Connections size against load, not tenancy — and the package already knows this.**
`derive-burst-scope.py` computes `connectionsAtFloor = floor × POOL_MAX_PER_REPLICA` with the floor
derived from RPS. **The tenant pools are the only place capacity is a function of how many tenants
exist rather than how much work they do**, and that asymmetry is the thing to remove, not the
number.

### Backpressure: refuse early with a number the caller can use

**Every service declares a concurrency limit and returns `429` with `Retry-After` when it is
exceeded.** Not a queue that grows until memory does.

**`Retry-After` is a real number, jittered.** A fixed value synchronises every client into the same
retry instant, which is the thundering herd wearing a different hat.

**Shed by audience, not uniformly.** A staff till completing a sale outranks a guest browsing a
catalogue. `x-ticvai-audience` already says which is which, so **the shed policy reads a field that
exists**: `guest` and `public` shed first, `staff` and `service` last.

### Thundering herd: three mechanisms, all on the read path

**Jittered TTL.** A cache entry written at the same moment as ten thousand others must not expire
with them. **±10% on every TTL.**

**Single-flight.** One request per key recomputes; the rest wait on it. **Two hundred people asking
the same question when a ride breaks is one database read, not two hundred.**

**Stale-while-revalidate on `cache:resolution`.** Permission resolution reads five tables. **Serving
a two-second-old scope resolution while refreshing behind it is correct** — permissions change on
the order of days and the alternative is a stampede on every expiry.

### Circuit breakers on every external call

**Payment providers, AI providers, queue adaptors, access-control vendors.** Open after five
consecutive failures or a 50% error rate over twenty calls; half-open after thirty seconds.

**An open breaker is a fast, specific error.** `AiProviderError` already has `unreachable` and
`quotaExceeded` as first-class outcomes — **the breaker makes them arrive in ten milliseconds
instead of at a thirty-second timeout.**

### Bulkheads: one pool per dependency, not one per service

**A slow catalogue query must not starve the payment path inside OrderService.** Separate pools per
downstream, sized independently.

**Without this, `x-ticvai-lock` on `acquireInventoryHold` becomes a service-wide outage**: contended
lease waits consume the shared pool and every other operation in OrderService blocks behind them.

---

## Consequences

**pgbouncer becomes a component with its own failure mode.** It is a single point in front of the
database and must be run as a pair. **The benchmark question it raises**: the replica count at which
the pooler becomes the bottleneck instead of Postgres.

**429 is now a normal response** and every client has to handle it — including the offline till,
whose sync must treat it as *retry later* rather than *rejected*. **`sync.rejection` is for records
the server refused on their merits; a 429 is not one.**

**Shedding guests before staff is a commercial decision made in an architecture document**, and it
should be checked with Qossai rather than assumed. It is the right default and it is not obviously
the client's.

---

## Alternatives considered

**Application-side pooling only.** Rejected: it cannot see across replicas, which is where the
arithmetic fails.

**Unbounded queue with a long timeout.** Rejected: a request nobody is waiting for anymore still
costs a connection, and the queue is where an outage hides until it is total.

**Global rate limit per tenant.** Deferred rather than rejected — **it protects other tenants from
one, which is a real property of the shared cell** — but it needs a fairness model nobody has
specified, and a wrong one throttles the tenant having the good day.
