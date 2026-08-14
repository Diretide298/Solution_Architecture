# Migrations

**No migrations are written. This is deliberate, as of 14 August.**

The schema reference workbook (`handoff/TICVAI_Schema_Reference.xlsx`) is the working artefact
while the design settles — 232 tables, 1,983 columns, derived from the contracts and regenerated
whenever they change. Writing DDL against a design that is still moving produces migrations that
have to be rewritten, and a forward-only migration cannot be rewritten.

Six migrations existed and were removed. What they contained beyond the column list —
row-level security, level-typed foreign keys, partitioning, 53 indexes, 28 constraints and
seven functions — is written up in **`handoff/storage-design.md`**. That is the 30% of a
migration that does not derive from the contracts, and it is the part worth keeping.

**When migrations resume**, the two documents together are the input: the workbook for tables
and columns, `storage-design.md` for everything that makes it a database.

---

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

The orchestrator that performs this fan-out is **not yet built and is unowned**. Until it
exists, migrations past V0001 can be written but not safely deployed.
