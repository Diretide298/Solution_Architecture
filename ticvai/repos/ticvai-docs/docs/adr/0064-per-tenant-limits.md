# ADR-0064: Every tenant has a request budget, and a busy tenant cannot starve the others

**Status:** Accepted · 1 October 2026 · Chinmay Parab
**Date:** 2026-10-01 (drafted 30 September from the system-design review) · **Deciders:** Chinmay Parab
**Finding:** SD-042 (medium), with SD-043
**Amends:** ADR-0032 (load shedding; pooling amended by ADR-0038, Redis product amended 30 September, amended by this ADR) — its deferred "global rate limit per tenant" is decided here
**Related:** ADR-0035, amended 3 September (burst environments) · ADR-0055 (deployables) · ADR-0066 (waiting room) · AI design 4.2

---

## Context

**ADR-0032 deferred the per-tenant limit on purpose.** Its alternatives section: *"Global rate limit per tenant.
Deferred rather than rejected — it protects other tenants from one, which is a real property of the
shared cell — but it needs a fairness model nobody has specified, and a wrong one throttles the
tenant having the good day."*

**Today nothing protects tenants from each other.**

- The deployables, Redis and the regional primary are shared. One tenant's on-sale or runaway integration can starve the rest.
- Per-tenant pgbouncer caps may sum above `max_connections` by design (ADR-0032's table: 10 tenants reach 89% in the worst case).
- AI already caps a tenant at 25% of `ai-interactive` (AI design 4.2). Nothing equivalent exists elsewhere.
- `429` was declared on 9 of 2,608 operations when the review ran (SD-043); a few more declare it today, still far from all.

---

## Decision

**The fairness model:** a tenant may use the whole platform when others are quiet, and at most a set
share of it when others need it.

1. **Token bucket per tenant and audience**, in the kernel middleware of every .NET host that serves requests (`commerce`, `access` and `operations`, ADR-0055), with counts shared through **Azure Managed Redis** (ADR-0032's product amendment) so all replicas agree.
   - Separate buckets for `guest`/`public`, `staff`, `service` and `partner` keys. A guest browse never spends a till's budget.
   - Sustained rate and burst (2× for 10 seconds) come from the tenant's plan, with a platform default. **Starting values:** twice the tenant's expected peak from its sizing tier (`sizing.json` venue tiers); recalibrated after the benchmark and after four weeks of production.
2. **Per-tenant share of in-flight work** on each replica: one tenant may hold at most 25% of a replica's request slots, **enforced only when the replica is above 70% of its limit.** A lone busy tenant on a quiet day gets the whole box. This answers ADR-0032's worry about throttling the tenant having a good day.
3. **Shedding order stays ADR-0032's:** `guest` and `public` first, `staff` and `service` last.
4. **Database:** keep the per-tenant pool cap. Alert when one tenant holds more than 60% of its pool for five minutes, and when the instance passes 80% of `max_connections`.
5. **On-sales belong in a burst environment** (ADR-0035, amended 3 September), behind the waiting room (ADR-0066). A tenant hitting its bucket because of an on-sale in the shared cell is the signal that the sale should have had one.
6. **Outer layer:** Front Door WAF rate rules per client IP, for abuse. They do not know tenants and are not the fairness model.
7. **Every operation declares `429` with `Retry-After`** (SD-043, a package fix).
8. **If Redis is unavailable**, each replica falls back to its own in-process buckets (the limit divided by the replica count). The request path never fails because the limiter's store did.

---

## Options Considered

### Option A: No per-tenant limit (status quo)

| Dimension | Assessment |
|---|---|
| Complexity | None |
| Cost | None |
| Scalability | One tenant can take the cell down |
| Team familiarity | n/a |
| Time to Block A | n/a |

**Pros:** Nothing to build. **Cons:** The shared cell's main risk stays open.

### Option B: Kernel middleware with Redis buckets and a load-aware share (decided)

| Dimension | Assessment |
|---|---|
| Complexity | Medium. A middleware and a Redis script |
| Cost | Negligible infrastructure |
| Scalability | Scales with the hosts; one Redis round trip per request |
| Team familiarity | High. ASP.NET Core has rate-limiting primitives; the distributed part is small |
| Time to Block A | Fits the kernel work in sprints 1–2 |

**Pros:** Knows tenant and audience. Load-aware, so it does not punish a good day.
**Cons:** Redis is on the request path (fail open to per-replica limits if Redis is down).

### Option C: Azure API Management in front, rate limit by key

| Dimension | Assessment |
|---|---|
| Complexity | Medium. Another hop and another product |
| Cost | Tiers with zone redundancy and private networking are expensive |
| Scalability | High |
| Team familiarity | Low to medium |
| Time to Block A | Slower |

**Pros:** Policies without code. **Cons:** Cost, latency, and it cannot see replica load for the share rule.

### Option D: WAF per-IP limits only

| Dimension | Assessment |
|---|---|
| Complexity | Low |
| Cost | Low |
| Scalability | Fine |
| Team familiarity | Medium |
| Time to Block A | Fast |

**Pros:** Stops abuse. **Cons:** Knows nothing about tenants; a venue's guests share few IPs on venue Wi-Fi.

---

## Trade-off Analysis

B is the only option that knows the tenant, the audience and the replica's load at once, which is
what ADR-0032 said a fair limit needs. C adds cost and a hop to get less. D is kept as the outer
layer for abuse.

---

## Consequences

**Easier:** one tenant's bad day stays that tenant's.
**Harder:** limits per plan must be set and explained to clients; 429 handling in every client, including the offline till's sync (ADR-0032 already requires it).
**Revisit:** starting values after the benchmark and after four weeks of production.

---

## Action Items

**Sprint 1**

1. [x] Chinmay: accepted 1 October 2026.
2. [x] Package: `429` with `Retry-After` on every operation (SD-043); a limits section on the subscription plan. Re-derive, mirrors, check. (2 pts) — **Authored 1 October**: every operation declares `429` (the shared `TooManyRequests`, now with the `RateLimit-*` headers; `tools/applied/adr-1-october.py` added it to 2,623); `Plan.requestLimits` (`PlanRequestLimits`, `RequestBudget`) in subscription. The four that declare their own `429` (three AI token ceilings, `verifyMfaChallenge`) now carry `Retry-After` too. Re-derive, mirrors and check at the next refresh.
3. [ ] Kernel: `429` and `Retry-After` are already in the kernel ticket (review 7.3).

**Sprint 2**

4. [ ] **KERNEL-TENANT-LIMITS**: Redis buckets per tenant and audience; load-aware share per replica; in-process fallback. (3 pts)
5. [ ] **OBS-TENANT-POOL**: alerts on pool share and `max_connections`. (1 pt)
