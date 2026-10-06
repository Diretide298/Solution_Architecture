# Migrations

**DDL lives here as versioned SQL. Not in the OpenAPI contracts, and not in a schema DSL.**

## Why SQL rather than YAML

The contracts describe the wire. Storage needs things OpenAPI has no way to express, and a
generic schema DSL expresses badly:

| Needed | Why a DSL loses it |
|---|---|
| `PARTITION BY LIST (venue_id)` | Partitioning strategy is not a field property |
| `FORCE ROW LEVEL SECURITY` | Policies are predicates, not annotations. `FORCE` is the whole point — without it the owner bypasses every policy |
| `ltree` + GiST | Extension types with their own operators |
| Partial indexes | `WHERE is_active` is a query-shape decision |
| `GENERATED ALWAYS AS` | Derived columns |
| The `pii` schema split | An architectural boundary, not a naming convention |

Generating SQL from YAML would mean either a DSL that reaches every one of these — at which
point it is SQL with extra steps — or a DDL nobody can read at the exact moment production
is broken.

## Where the mapping is recorded

Each API schema in the contracts carries `x-ticvai-persistence`:

```yaml
JournalEntry:
  x-ticvai-persistence: "ledger.journal_entry + ledger.journal_line"
TrialBalance:
  x-ticvai-persistence: "none — computed"
```

Documentation of the mapping, not a generator input. It answers "where does this live" without
pretending the contract defines storage. **19 of the 71 mapped spine schemas have no table at
all** — they are computed responses, and that is worth stating explicitly rather than leaving
someone to search for a table that was never meant to exist.

## File layout

**What is in `backend/` (3 October 2026, CHG-TBF-002).** Two databases, `backend/tenant/` and
`backend/control/`, each with the same layout. The numbered files are derived by `tools/derive-ddl.py`
and **frozen at the git tag `r1`** (`tools/check-migration-freeze.py`): a baseline file is never edited
again, and a later table change is a forward migration of its own.

    000-schemas.sql                  the schemas                                  [DERIVED, frozen at r1]
    001-extensions.sql               ltree, btree_gist, pgcrypto, vector (tenant) [DERIVED, frozen at r1]
    002-migration-register.sql       platform.schema_version                      [DERIVED, frozen at r1]
    010-<schema>.sql                 one file per schema: its tables              [DERIVED, frozen at r1]
    900-foreign-keys.sql             the declared references                      [DERIVED, frozen at r1]
    910-indexes.sql                  conventions and scope paths                  [DERIVED, frozen at r1]
    920-row-level-security.sql       one policy per table, FORCE on every one     [DERIVED, frozen at r1]
    930-partitioning.sql             monthly range partitions (ADR-0056)          [DERIVED, frozen at r1]
    V01nn__after_r1_<yyyymmdd>.sql   what changed after r1, additive only         [DERIVED, then frozen]

Each file's header gives its own counts; they are not repeated here, where they went stale.

**The migration files the developers write** are numbered by the plan, not here.
`tools/build-service-docs.py` gives every migration ticket its file, and writes the same names, in the
same run, into `handoff/service-docs/backend/MIGRATIONS.md` (generated), so a ticket and that list cannot
disagree. Until 3 October this section listed twenty files numbered V0002 to V0021, a hand-written
plan from before the DDL was derived: none of those files exists, and the tickets named other numbers
for the same schemas (access was V0026 on its ticket and V0007 here; retail had two numbers).
The numbering:

| Range | What | Who numbers it |
|---|---|---|
| V0001 | the baseline: schemas, extensions, the register, the RLS and partition helpers (MIG-BASELINE) | the plan |
| V0002 to V0099 | the first release, one migration per schema in key order, cross-schema keys last (MIG-<SCHEMA>, MIG-FOREIGN-KEYS) | the plan, in schema order |
| V0100 to V0999 | derive-ddl's frozen-mode files in `backend/<db>/` (`V<nnnn>__after_r1_<yyyymmdd>.sql`). The three written against the old r1 (V0100-V0102, 2-3 Oct) were deleted on 6 Oct (CHG-SQL-001): the fresh r1 baseline already holds them | derive-ddl, one number per run |
| V1000 upwards | every later forward migration (VM-MIG-*, MIG-<SCHEMA>-<n>), in build order | the plan, kept once planned |

**A number is never reused and never renumbered.** A forward migration keeps the number it was first
planned with on every later refresh (`build-service-docs.py --renumber-migrations` drops that only
before a first push); the frozen V01nn files are never renumbered. A V01nn change to a table that no
migration has created yet is folded into that table's own migration ticket rather than applied to a
table that does not exist. `tools/check-migration-tickets.py` fails on a ticket with no file, a number
used twice or outside its range, a migration that runs before one it depends on, and any file name here
or in the generated list that the tickets do not carry.

**Every table is in a migration or says why not** (CHG-TBF-003). The tables no operation reads or writes
and no task names are listed, with that reason, under "Tables no migration creates" in the generated
`handoff/service-docs/backend/MIGRATIONS.md`; a table there that an operation does reach fails the check.
The kernel's own tables (`kernel.inbox`, `ai.inbox`, `control.outbox_relay`, ADR-0058) go with the first
release, and `platform.schema_version` with the baseline.

`subscription` is a tenant schema with a first-release migration of its own; the Control Plane is the
`control` database (ADR-0039), migrated as its own series and holding its own `platform.schema_version`.

## Tenant-level row-level security

**A table under `platform.apply_tenant_rls` has no `tenant_id` column, by design.** A tenant database
holds one tenant (ADR-0038, a cell is a region with a database per tenant), so there is nothing to filter
by tenant inside it. The policy is `platform.tenant_root_in_scope()`: the caller's scope must include the
tenant root, which is how a table with no scope column, venue or owning row is still under FORCE row-level
security rather than open. ADAM's table view calls this policy `tenant_isolation`; it is not a missing
column, and the DDL is right as it stands. A table gets this policy only when it has no `scope_path`,
no `venue_id`, no subject and no NOT NULL owning reference (the comment beside each call in
`920-row-level-security.sql` says which).

## Rules

**Forward-only.** No file is ever edited after merge. A mistake is a new migration.

**Every migration is reversible.** A `-- ROLLBACK` section is mandatory and is tested in CI
against a restored snapshot, not asserted.

**Additive first.** Add column, backfill, switch reads, drop old — four migrations, not one.
A cell mid-rollout runs two application versions against one schema.

**Every venue-partitioned table needs a default partition.** Misconfiguration should be loud,
not silently lossy.

**Every table with a `scope_path` needs RLS with `FORCE`.** API-layer enforcement alone fails
the first time somebody writes a report query directly against the database.

## Applying

Migrations fan out **per region**, not per tenant (ADR-0014). A tenant in three regions is
three cells and three applications, and they may legitimately sit at different versions during
a rollout — `platform.schema_version` records where each one is.

The orchestrator that performs this fan-out is the Block A task PLATFORM-MIGRATE (migration fan-out
across tenant databases, with progress and resume). Until it exists, migrations past V0001 can be
written but not safely deployed.
