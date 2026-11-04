# backend/ — the versioned SQL

**The SQL files here are written by `tools/derive-ddl.py`: never hand-edit them.** This page is written by hand and
its figures are kept current by `tools/sync-counts.py`. Since r1 the baseline files (`000` to `930`) are frozen
at the tag and never regenerated; every later change is a forward migration, `V0100` and up, which derive-ddl
writes once and never rewrites (MIGRATIONS.md).

```
tenant/                      every tenant database
  000-schemas.sql            the schemas
  001-extensions.sql         ltree and the other extensions
  002-migration-register.sql platform.schema_version
  010-<schema>.sql           one file per schema
  900-foreign-keys.sql       constraints, applied after every table exists
  910-indexes.sql            conventions and scope paths
  920-row-level-security.sql the policies (backend/MIGRATIONS.md, "The connection context")
  930-*.sql                  partitioning
  V01nn__after_r1_*.sql      the forward migrations since the r1 freeze, one per release
control/                     the control database, the same layout, no row-level security
```

**Every statement is validated as Postgres** by `sqlglot` before it ships.

---

## 🔴 There is one generation of DDL here, plus its forward migrations, and there must stay one

The numbered files are the schema as it is now; the `V01nn` files are the forward migrations that take
a database built at the r1 freeze to it, in order. Nothing else may sit beside them.

**A consumer parsing `backend/*.sql` in sorted order will apply a later `CREATE TABLE` over an
earlier one for the same name.** Digits sort before letters, so a file named `V0002__identity.sql`
alongside `010-identity.sql` is parsed **last** and wins.

**That is not hypothetical.** On 31 August a consumer's tree held both this generation and a
`V0001`–`V0003b` series from August. **Thirty-three tables existed in both** and the August
definition won every time.

**The damage was in the ordering rather than the duplication.** `900-foreign-keys.sql` attaches all
580 keys by `ALTER TABLE` and runs *before* the V-series, because `900 < V`. The V-series then
re-created those 1178 tables and **815 foreign keys went with them.**

**And nothing reported a dangling reference**, because both generations' tables existed: the
surviving key on `identity.principal` pointed at `platform.scope_node`, a name this generation
renamed to `platform.org_unit` on 26 August. **Two tables, one per generation, and the graph quietly
wired itself to the dead half.**

**If you hold the August `V0001`-`V0003b` series, delete it.** It is no part of this folder. The history this
folder does carry is the forward-migration series after r1 (`V0100` and up, in each database's folder), applied
after the frozen baseline in name order; the August files are not in it.

---

## What a consumer should do

**Parse every file in sorted order and refuse a `CREATE TABLE` for a name already seen**, rather
than replacing it. That survives a stale file arriving in a future dump and costs one condition.

**Take the table count from `handoff/status.json` or `handoff/burst-scope.json`**, not from parsing.
Those come from the same pass that writes the DDL, so a disagreement between them and a parser means
the parser is reading something the generator did not write.

---

## Ordering, and why foreign keys are separate

**Tables first, constraints last, is the only ordering that terminates.** 26 schemas cannot be
sorted so that every reference precedes its use — `orders` reaches `catalogue`, `catalogue` reaches
`platform`, and something reaches back.

**`enforced: no` becomes an index and a comment, never a constraint.** 157 of the 3371 relationships
are naming conventions the contracts never asserted (ADR-0011), and **enforcing one fails on the
first row that legitimately points nowhere.**

---

## Still open

**CF-161 is closed** (ADR-0038, 3 September 2026): a cell is a region holding a database per tenant. The claim
that once stood here, that the `CREATE TABLE` statements are identical either way, was wrong, as ADR-0038 says:
the decision dropped `control.cell.tenant_id`, added tables, and took `control` out of the tenant template into
a database of its own (ADR-0039), which is why this folder has `tenant/` and `control/`.

**CF-64** — cloud provider. Affects the managed Postgres tier and nothing in these files.
