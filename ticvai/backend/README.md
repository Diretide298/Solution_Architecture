# backend/ — the versioned SQL

**The SQL files are generated: `tools/derive-ddl.py` rebuilds them on `refresh.sh`. Do not hand-edit
them.** Two databases, one folder each (ADR-0038: a cell holds many tenants, each in its own tenant
database; ADR-0039: the control database is its own):

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
re-created those 1173 tables and **815 foreign keys went with them.**

**And nothing reported a dangling reference**, because both generations' tables existed: the
surviving key on `identity.principal` pointed at `platform.scope_node`, a name this generation
renamed to `platform.org_unit` on 26 August. **Two tables, one per generation, and the graph quietly
wired itself to the dead half.**

**If you hold an older series, delete it.** This folder is regenerated in full and carries no
history; the history is in the contracts.

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

**`enforced: no` becomes an index and a comment, never a constraint.** 157 of the 3329 relationships
are naming conventions the contracts never asserted (ADR-0011), and **enforcing one fails on the
first row that legitimately points nowhere.**

---

## Still open

**CF-161** is settled: ADR-0038 puts each tenant in its own database inside a cell (a region holding many
tenants), and ADR-0039 keeps the control database apart.

**CF-64** — cloud provider. Affects the managed Postgres tier and nothing in these files.
