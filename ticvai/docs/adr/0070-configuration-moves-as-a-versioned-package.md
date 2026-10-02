# ADR-0070: Configuration moves to production as a versioned package; the schema only moves forward

**Status:** Accepted · 2 October 2026 · Chinmay Parab (sent as "the industry standard, default unless he objects"; no objection)
**Date:** 2026-10-02 · **Deciders:** Chinmay Parab
**Source:** decision DEC-168 (workbook question 168, screen ADM-122 Product Import / Export & Environment Transfer), in `docs/registers/decisions-2-october.md`; Chinmay's words in `docs/active/decisions/answers-2-october.md` (batch 5, set 1); change entry CHG-DOC-011
**Related:** ADR-0039 (the control plane and the tenant database lifecycle) · ADR-0056 (one id type, UUIDv7) · ADR-0038, amended by ADR-0040 (a database per tenant) · ADR-0035 (burst environments) · `tools/check-migration-freeze.py` · `tools/check-key-stability.py`

---

## Context

**The question came from a screen.** ADM-122, *Product Import / Export & Environment Transfer*, moves
product configuration between TICVAI environments, and its design notes asked: after go-live, is
configuration promoted from pre-production to production only as configuration? The drawn default was
"show transfers as configuration-only jobs with approval".

**Chinmay's answer widened it:** *"The biggest challenge is migration or changes in the DB… suggest a
better way, or the industry standard."* Two different things travel from one environment to another,
and they need different rules:

- **The schema** (tables, columns, indexes) changes with the code. From `r1` the baseline migrations are
  frozen (`check-migration-freeze`): a change is a new forward migration, and the platform kernel's
  migration fan-out already runs expand-then-contract changes across every tenant database
  (`PLATFORM-MIGRATE`, ADR-0039).
- **Configuration** (products, price lists, rules, menus, layouts, flows) is data a tenant authors. It is
  edited in pre-production, checked, and then has to reach production without anyone re-keying it, and
  without overwriting what production already holds.

What nobody should do is move a database: copy pre-production over production, merge two databases, or
run a migration backwards. Each of those destroys production data that pre-production never had (orders,
tickets, guests) or leaves a schema that no migration history describes.

---

## Decision

**Never merge or reverse-migrate a production database. The schema goes forward only; configuration
moves as a versioned package.**

### The schema

1. **Forward only.** Every schema change is a versioned forward migration, applied in order to every
   tenant database (ADR-0039's fan-out). No down-migrations in production; a mistake is corrected by the
   next forward migration.
2. **Expand, then contract.** A breaking change is split: add the new shape and write both (expand), move
   the readers, then remove the old shape in a later release (contract). Code of release N runs against
   the schema of N and N+1, so a rollback of the code never needs a rollback of the schema.

### Configuration

3. **A package, not a copy.** Configuration is exported from the source environment as a **versioned
   package**: each record carries its **stable key** (the business key or the UUIDv7 id it was created
   with, ADR-0056), never a database sequence, so the same record is recognised in every environment.
4. **Diff before apply.** The package is compared with the target: new, changed and removed records,
   field by field, and any record the target changed since the last package (a conflict, shown, never
   silently overwritten).
5. **Approval.** Applying to production needs an approver other than the person who prepared the package
   (the platform's approvals engine, step-up for the approver).
6. **Idempotent upsert by key.** Applying inserts or updates by stable key; applying the same package twice
   changes nothing. A record absent from the package is not deleted unless the package says so explicitly.
7. **Audited.** Every application records the package version, the diff, who approved it and when.
8. **Rollback re-applies the previous package**, through the same diff, approval and upsert. Nothing is
   restored from a backup to undo configuration.
9. **Secrets and environment settings never travel in a package.** Keys, credentials, endpoints, payment
   merchant ids and anything environment-specific stay in each environment's own settings (Key Vault and
   the environment configuration). The export refuses them.

---

## Options considered

| Option | Verdict |
|---|---|
| **A. Versioned configuration packages with diff, approval and idempotent upsert; forward-only schema (chosen)** | The industry pattern (configuration as data, migrations as code). Safe to repeat, reviewable, reversible by re-applying |
| B. Copy the pre-production database (or its configuration tables) over production | Destroys production-only data and history; ids collide; no review of what changed |
| C. Re-key configuration in production by hand | What the screen was meant to avoid: slow, error-prone, and nothing proves production matches what was tested |
| D. Two-way merge of environments | Needs conflict rules for every table and still cannot tell a deliberate production edit from drift |

---

## Consequences

**Easier:** a tested configuration reaches production exactly as tested; a bad change is undone by the
previous package; every change to production configuration has a diff, an approver and an audit record.

**Harder:** every configuration record needs a stable key that is the same in every environment, and the
export must know which fields are environment-specific. Records created in production (for example a
price list a venue edits live) can conflict with an incoming package; the diff shows the conflict and a
person decides.

**What it asks of the package:**

- **Contract.** Configuration export, diff and apply operations behind ADM-122 (for example
  `exportConfigPackage`, `diffConfigPackage`, `applyConfigPackage` in `contracts/satellite/platform-ops.yaml`),
  passing the new-operation gates (permission vocabulary, config noun, paging on lists). That contract
  change is the platform contracts' owner's, not this ADR's.
- **Checks.** `check-migration-freeze` already enforces the forward-only schema after `r1`. The keys a
  package carries must stay stable from release to release (`check-key-stability`); extending that check
  to the configuration package's keys is the prevention for this decision (CHG-DOC-011, open until it exists).
- **Runbook.** `docs/active/release-runbook.md` (section "Configuration promotion after go-live") points
  here.
