# ADR-0042: When a region grows, and where a tenant lands

**Status:** Accepted — one number pending sign-off, marked below
**Date:** 8 September 2026
**Decides:** **CF-168**, raised by [ADR-0040](0040-a-cell-may-hold-more-than-one-instance.md)
**Amends:** [ADR-0039](0039-control-plane-and-tenant-database-lifecycle.md) — provisioning now picks an instance as well as applying the template

---

## Context

**ADR-0040 removed the ceiling on a region and left two questions only a person can answer.** A cell
is a region; a region may be served by more than one Postgres instance. It said when that is
*possible* and deliberately did not say **when it should happen** or **which instance a new tenant
goes on** — and it named the schema gap underneath both rather than closing it.

**Nothing routes today.** `control.cell_tenant` carries `cell_id`, `tenant_id` and `database_name`,
which was a complete address for exactly as long as a cell had one instance. **A database name
without a host is not an address.** Until that is fixed, a second instance cannot be added — not
because it would be slow, but because no service could find a tenant on it.

**The signal was already agreed and the threshold was not.** ADR-0032 — amended by ADR-0040, which
made its pool cap a limit rather than a reservation — and ADR-0040 itself both land on concurrent
server connections against the primary's own `max_connections`, and both refuse tenant count as a
proxy: a client with fifty venues and a client with two both get a pool of forty.

---

## Decision

### 1 · The address is `cellId` + `instanceId`

`control.cell_instance` holds one row per Postgres instance serving a cell. `control.cell_tenant`
gains a **required, non-nullable** `instance_id`.

**Required from the first row, while every region still has one instance.** A column that is only
populated once there are two is a column every reader has to guess about, and the guess is wrong
exactly once — on the first region that grows, which is the first region under load.

`status` on an instance walks `provisioning · live · draining · retired`. **`draining` takes no new
tenants and still serves the ones it has**, because placement and liveness are different questions:
an instance being emptied is not an instance being down.

### 2 · Placement is emptiest-first, with a pin

**A new tenant goes to the `live` instance in its cell with the most headroom.** Pinned tenants are
placed by hand and the balancer leaves them alone.

**Headroom is measured as peak concurrent server connections over the trailing 7 days, as a
fraction of that instance's own `max_connections`** — not as a count of databases. This is the whole
argument of ADR-0040 applied one level down: capacity is a function of load, not of how many tenants
exist. Counting databases would place a tenant onto the instance holding ten quiet ones and away
from the one holding three busy ones, which is backwards on the only day it matters.

**Trailing 7 days, and peak rather than mean.** A week covers one Saturday, and Saturday evening is
when every venue trades at once. A mean would hide it — the mean of a week containing one Saturday
is a Tuesday.

**`maxConnections` is read per instance, not assumed.** Instances in one region need not be the same
size, and headroom expressed as a fraction survives that; headroom expressed as a raw number does
not.

**The pin is what a dedicated client is actually buying.** A rule that can silently rebalance a
pinned tenant has sold something it does not deliver, so a pin survives migration: moving a pinned
tenant is an operator decision and never a placement one.

### 3 · The growth trigger

**Add an instance when peak concurrent server connections on a region's busiest instance hold at or
above 70% of its `max_connections` on three days within a rolling seven, at least two of them not
consecutive.**

> **🟡 The 70% needs Chinmay's sign-off.** The signal, the window and the shape are derived below;
> the number is a judgement about how much runway the team wants and is the one thing here that
> cannot be read off the arithmetic.

**Why a fraction and not 440.** ADR-0032's table is arithmetic on `default_pool_size = 40` and
`max_connections = 500`: eleven databases is 440, or 89%. That figure is a worst case where every
tenant peaks at full depth simultaneously, and it is specific to one configuration. **A fraction
survives a config change; a constant becomes wrong silently** — which is precisely how the
`backend/900-foreign-keys.sql` path outlived the file it pointed at.

**Why 70% and not 89%.** 89% is one busy tenant from exhaustion, and adding an instance is not
instantaneous: it is a host, a template, a migration fan-out and a tenant move. **The trigger has to
fire early enough for the work to finish before the ceiling arrives**, and the gap between 70% and
89% is that runway. Growing a region that did not need it costs a machine; not growing one that did
costs a Saturday evening.

**Why three days in seven, two non-consecutive.** This is what separates growth from an event. One
peak is a concert. Two consecutive peaks are a weekend. **Three across a week, with a gap, is a
level that has moved** — the shape the register asked for when it said *"sustained"*, made
countable.

**A single five-minute period above 90% is an incident, not a growth signal.** It pages, and it does
not add a host. **Autoscaling a database on a spike is how one bad query becomes an estate**, and
the two responses are genuinely different: one is investigated, the other is planned.

---

## Consequences

**Provisioning gains a step and a failure mode.** ADR-0039's *apply the template, record the
membership, seed nothing* becomes *choose an instance, apply the template, record the membership
with its instance, seed nothing.* **A cell with no `live` instance now fails provisioning loudly**,
which is correct and is new: previously there was nothing to fail on.

**The router reads two columns where it read one.** Every service resolving a tenant already goes
through `cell_tenant` before opening a connection (ADR-0038, amended by ADR-0040 on instance count);
it now takes the host from the same row. No new lookup, no new round trip.

**Rebalancing is deliberately not automatic.** Emptiest-first applies at provisioning. **An existing
tenant moves only by `planTenantMigration` and `executeTenantMigration`**, which are specified,
audited and operator-initiated. A balancer that moves live databases on its own is a component
nobody has designed and the failure mode is a tenant offline for a reason no human chose.

**`migration_run_cell` gets a second meaning and keeps its first.** *"How is the UAE doing"* may now
need per-instance detail, as ADR-0040 anticipated. The rollup is still per cell.

**One more thing to monitor per region, and it is the thing already being monitored.** Concurrent
server connections against `max_connections` is what ADR-0032 said to watch; this makes a threshold
out of it rather than adding a metric.

---

## When this is reopened

**Instances per region reach a number where placement wants a scheduler.** ADR-0040 put that at
around ten and it is unchanged. Emptiest-first over a trailing week is a query; at ten instances it
is a component, and the decision should be re-argued rather than extended.

**The pin population grows past a handful.** A pin is an exception. **If most tenants in a region
are pinned, the rule is not emptiest-first with an override — it is manual placement with a default**,
and it should be written down as what it actually is.

**`default_pool_size` or `max_connections` changes.** The 70% is a fraction and survives, but the
runway between 70% and exhaustion is a function of both, and a large change to either is a reason to
re-derive the number rather than carry it.

---

## Alternatives considered

**Fullest-first.** Rejected. It packs tenants onto one instance and leaves the newest underused,
which is efficient in cost and wrong in risk: **it concentrates the busiest tenants on the host with
the least headroom**, and the first symptom of getting it wrong is the failure this ADR exists to
prevent. It is the right rule for bin-packing stateless workloads and the wrong one for databases
that cannot be moved quickly.

**Pinned-only, no automatic rule.** Rejected as a default, kept as the override. It makes every
provisioning a decision, and a step that always needs a human is a step that gets skipped under
load — which is when it is being done.

**Round-robin.** Rejected. It is emptiest-first with the measurement removed, and it is
indistinguishable from it while instances are equal and wrong the moment they are not.

**Trigger on tenant count.** Rejected, and it is the rejection ADR-0040 already argued: eleven
tenants was called a ceiling when it is a monitoring threshold, and **tenant count says nothing
about load.** It is named here because it is the number that will be reached for in a meeting.
