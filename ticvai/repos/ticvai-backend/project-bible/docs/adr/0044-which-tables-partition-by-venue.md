# ADR-0044: Which tables partition by venue

**Status:** Accepted — signed off by Chinmay, 18 September 2026. **The full rule, not the six-table
subset**: `venue_id NOT NULL` implies `PARTITION BY LIST (venue_id)`, a leading `venue_id` in the
primary key, and composite foreign keys into it. The 74 columns are in scope. `backend/tenant/930-partitioning.sql`
is written against this.
**Date:** 8 September 2026
**Amends:** [ADR-0005](0005-venue-isolation-by-partitioning-not-separate-databases.md) — it decided *that* venues are isolated by list partitioning and never said which tables
**Depends on:** [ADR-0038](0038-cell-is-a-region-database-per-tenant.md), amended by ADR-0040 on instance count, which does not touch what a tenant database is — partitioning happens inside it, which ADR-0038 settled

---

## Context

**ADR-0005 has been Accepted since 12 August and unimplemented since.** Its own status line says so:
*"`backend/` contains no `PARTITION BY`, so `venue_id` is an ordinary column and this decision is
owed its DDL."* It decided that venues are isolated by list partitioning on `venue_id` and **never
said which tables partition**, which is the whole of the remaining work.

**The reason it has not been written is visible once the columns are counted.** 69 tables carry a
`venue_id`. **32 have it `NOT NULL` and 37 have it nullable** — and those two groups are different
kinds of thing. A nullable `venue_id` is the schema saying *this row may belong to the tenant rather
than to a venue*: a campaign across every venue, a product shared between them. **Partitioning by a
column that is sometimes absent is partitioning on a question the data does not answer.**

**The cost is not in the 32; it is in what points at them.** Postgres requires a partitioned table's
unique constraint to include the partition key, so a partitioned table's primary key becomes
`(venue_id, id)` — and every foreign key referencing it becomes composite.

| | |
|---|---|
| tables with `venue_id NOT NULL` | **32** |
| of those, referenced by something | **26** |
| referenced by nothing — free to partition today | **6** |
| tables holding a foreign key into the 32 | **99** |
| of those, already carrying `venue_id` | 25 |
| **would have to gain a `venue_id` column** | **74** |

---

## Decision

**Partition exactly the tables whose `venue_id` is `NOT NULL`, make `venue_id` the leading column of
their primary key, and make every foreign key into them composite.**

**The rule reads a property the schema already carries.** `NOT NULL` on `venue_id` *is* the
assertion that a row belongs to exactly one venue — it is already written down, on every table, by
whoever added the column. A hand-maintained list of partitioned tables would need updating every
time a table is added and would be wrong the first time somebody forgot; **this rule cannot drift
from the schema because it is read from it.**

### The 74 columns are the mechanism, not the cost

This is the part that looks like a price and is not.

**Nothing today prevents a cross-venue reference.** `orders.order_line` points at
`orders.sales_order` by `sales_order_id` alone, and carries no `venue_id` of its own. A line in venue A referencing an order in venue B
satisfies every constraint in the database. **ADR-0005 claims venue isolation and the schema does
not currently enforce it** — partition pruning makes cross-venue queries *unlikely*, and a foreign
key makes them *impossible*.

**A composite foreign key is the isolation ADR-0005 said it was buying.**
`(venue_id, sales_order_id)` referencing `(venue_id, id)` cannot resolve across venues, because the venue is part of the match.
The 74 columns are what turns a performance property into a correctness one.

---

## Consequences

**🔴 74 tables gain a `venue_id` column, and it is denormalisation with a purpose.** A line item's
venue is derivable from its order; storing it again is redundancy, and the redundancy is what the
constraint is made of. **This is the reason the decision needs a person**: it is a schema-wide
change made once, and it is expensive to reverse after data exists.

**Six tables can be partitioned today with no ripple at all** — `lost_item`, `price_variance`,
`published_bundle`, `refund_policy`, `reservation`, `scan_event`. Nothing references them. **If the
full rule is not signed off, these six are still worth doing** and would prove the mechanism against
`scan_event`, which is the highest-volume table in the set.

**The 37 nullable-`venue_id` tables stay unpartitioned, and that is a decision rather than an
omission.** They are tenant-scoped rows with an optional venue. Forcing them into the rule would
mean either a `DEFAULT` partition holding every shared row — a partition that grows without bound
and prunes nothing — or making `venue_id` mandatory on a campaign that deliberately spans venues.

**Migration and backup targets are unchanged.** ADR-0005 already settled that: one per tenant, not
one per venue. Partitioning is inside the database.

**`derive-ddl.py` becomes the place the rule lives.** The DDL is generated, so the rule is code —
`venue_id NOT NULL` implies `PARTITION BY LIST (venue_id)` and a composite key — rather than a
list in a document that the generator does not read.

---

## When this is reopened

**A partitioned table needs a unique constraint that cannot include `venue_id`.** A globally unique
code on a venue-scoped table is the case, and it is the one that breaks the rule rather than bending
it. It would need either a separate global lookup table or an exception, and an exception should be
argued rather than assumed.

**Venue counts per tenant reach a number where list partitions become unwieldy.** Postgres handles
hundreds of partitions comfortably and thousands poorly. **A tenant with 2,000 venues is a different
decision**, and it is the same shape as ADR-0042's *ten instances wants a scheduler*.

---

## Alternatives considered

**Partition every table with a `venue_id`, nullable included.** Rejected. It needs a `DEFAULT`
partition for the shared rows, which is an unbounded partition that prunes nothing — the opposite of
the property being bought — and it would make `venue_id` mandatory on rows that are deliberately
tenant-wide.

**Partition only the six unreferenced tables.** Rejected as the answer, kept as the first step. It
costs nothing and buys almost nothing: the tables worth pruning are the large referenced ones —
`sales_order`, `product`, `outlet` — and a rule that partitions only what nothing points at
partitions only the leaves.

**Partition without composite foreign keys, using plain single-column keys where Postgres allows.**
Rejected, and it is the tempting shortcut because it skips all 74 columns. It gives partition
pruning and no enforcement, which leaves ADR-0005's isolation claim exactly as unbacked as it is
today — **a performance optimisation wearing the language of a correctness guarantee.**

**Row-level security instead of partitioning.** Rejected here as a substitute and worth having
alongside. RLS enforces who may read a venue's rows; it does not give pruning, per-venue archival or
independent vacuum, which are three of ADR-0005's four stated consequences.
