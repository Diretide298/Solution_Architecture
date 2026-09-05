# ADR-0039: The control plane is a database of its own, and a tenant database is the unit

**Status:** Accepted
**Date:** 3 September 2026
**Follows:** [ADR-0038](0038-cell-is-a-region-database-per-tenant.md), which said this home was the next ADR
**Amends:** [ADR-0028](0028-service-decomposition.md) — the tenant template is the schema set minus `control`
**Raises:** **CF-167** — where the control plane physically sits

---

## Context

**ADR-0038 put a database around each tenant and left 43 tables with nowhere to live.**
`control.*` is the cell registry, placement, licences, subscriptions, releases, rollouts,
migration plans and runs, onboarding applications, API clients and the tenant registry itself.
**Every one of them is *about* tenants rather than *inside* one.** A cell registry that exists two
hundred times is two hundred registries that can disagree, and the first thing that disagrees is
which of them is authoritative.

**Three tables count cells and mean tenants.** They were written while a cell had exactly one
tenant, so per-cell *was* per-tenant:

| Table | What it records | Under ADR-0038 |
|---|---|---|
| `control.migration_run_cell` | *"What happened in one cell during one run. Where a partial failure is named rather than counted"* | one row for two hundred outcomes |
| `control.migration_plan_cell` | which cells a plan targets | targets a cell, applies to N databases |
| `control.rollout_cell` | release progress, with `is_canary` and `wave` | a canary cell is now a canary of many tenants |

**Their own comment is the argument.** `migration_run_cell` exists so that a partial failure is
*named rather than counted*, and under the new topology it counts. A fan-out that succeeds for 180
tenants and fails for 20 currently has one row saying `failed`.

---

## Decision

### 1. `control` is a database, not a schema in a tenant database

**The tenant template is every schema except `control`.** `control` comes out of it and nothing
else moves: the rest are exactly what ADR-0028 decomposed, and no service gains or loses a
schema.

**Stated as a rule rather than a count, because the count moved four days later.** This read
*"the tenant template is 25 schemas"* when it was written on 3 September. On 4 September a
`subscription` schema arrived in the contracts carrying `subscription.partner_quote`, the
template became 26, and the ADR was wrong about an artefact it had not decided — the number
of schemas is an output of ADR-0028's decomposition, not of this decision. **A decision that
restates a derived number acquires a way to go stale that has nothing to do with the
decision.** The count lives in `backend/tenant/000-schemas.sql`, which is generated; this
says which schema is *excluded*, which is the part this ADR actually decided.

### 2. A tenant database is the unit of provisioning, migration, backup and destruction

**One name, one lifecycle, one restore.** The database is named from the tenant's stable slug in
`control.tenant` and **does not encode the region** — the instance already is the region, and a name
that repeats it is a name that can contradict it.

**Provisioning is triggered by verification, not by application.**
`control.onboarding_application` already says it: *"Nothing is provisioned until verification
passes — an unverified application that provisions a cell is a cell somebody has to clean up."*
This names the step that follows: apply the template, record the tenant's membership of the cell,
seed nothing.

**Destruction is a database drop and a row.** It is the first time in this architecture that
removing a tenant has been a bounded operation rather than a delete across 341 tables.

### 3. The fan-out unit is a tenant database, and the canary is a tenant

**`control.migration_run_tenant` is added**, one row per tenant per run, carrying what
`migration_run_cell` carries today — status, `from_version`, `to_version`, `error`, timings.
`migration_run_cell` stays as the rollup, because *"how is the UAE doing"* is a real question and
counting it from two hundred rows on every read is not.

**The canary is a tenant inside a canary cell, not the cell.** `migration_run.canary_cell_id`
selects a region; a canary that is two hundred databases is not a canary. The same applies to
`rollout_cell.is_canary` and `wave`: a wave is now a set of tenants, and it may be a subset of one
cell.

**`control.migration_plan_cell` keeps its name and gains an inclusion rule** — all tenants in the
cell, or a named set — because a plan that can only say *"this region"* cannot express the rollout
this decision makes normal.

### 4. `control.cell` loses `tenant_id`

It is a column today and it was correct while a cell had one tenant. **A relation replaces it**, one
row per tenant per cell. A tenant with venues in two regions has two rows, two cells and two
databases, which is the same fact ADR-0038 states and the schema should not have to be read against.

---

## Consequences

**The operational win is per-tenant restore, and it arrives for free.** Restoring one tenant to
yesterday no longer means restoring everybody. That was the strongest argument against a shared
database and nothing in the package had claimed it.

**The operational cost is 200 migrations where there was one, and it is a job rather than a
risk.** One template applied N times, recorded per tenant, canary-first, with a named partial
failure. The machinery exists — `control.release`, `release_component`, `rollout`, `rollout_cell`
— and what changes is the unit it iterates.

**`tenant_id` splits cleanly in two.** On a control-plane table it is the primary way rows are
addressed. Inside a tenant database it is redundant, and ADR-0038's 51 occurrences can now be read
against a rule rather than one at a time: **if the table is in `control`, keep it; if it is in the
tenant template, it is saying something the connection already said.**

**🔴 The control plane's own placement is not decided here.** `control.onboarding_application`
carries `contact_email`, `contact_phone` and `country_code` — **personal data, before a tenant
exists to own it** — while ADR-0010 puts the Guest Link Registry *"in the Control Plane,
pseudonymous only"* and fans out from it across regions. One of those wants a control plane in the
prospect's jurisdiction; the other wants one above all of them. **Raised as CF-167 with a
recommendation rather than settled by inference**, because the answer is a residency position and
not an engineering preference. Nothing in this ADR depends on it: the tables are the same shape
whether there is one control database or one per region.

**`control` has 43 tables in the generated DDL and 41 on the Modules sheet.** Two derivations of one
schema, disagreeing by two, and the provisioning script will be generated from one of them. It is
worth reconciling before that script exists rather than after.

---

## When this is reopened

**A tenant count where per-tenant migration recording becomes the slow part.** Two hundred tenants
across twelve releases a year is 2,400 rows; two thousand tenants is a different conversation about
retention, not about granularity.

**A schema change that cannot be applied tenant-by-tenant.** Everything in `backend/` today can. A
change requiring all databases to move together would make the fan-out a distributed transaction,
and that is a reason to re-argue the unit.

---

## Alternatives considered

**`control` as a schema in every tenant database.** Rejected. Two hundred cell registries, and the
question *"which tenants are in the UAE"* becomes a query against every tenant that might answer.

**`control` in one designated tenant's database.** Rejected. It creates a tenant that cannot be
deleted, cannot be migrated and cannot be restored independently — the three things this decision
exists to make possible.

**Reinterpret `migration_run_cell` rather than add a table.** Rejected. The row would mean *"one
cell"* in the plan and *"one tenant"* in the run, and a column whose referent changes between two
tables that join to each other is the defect this ADR is correcting.

**Leave the canary at cell granularity.** Rejected on the arithmetic: the point of a canary is that
its failure is cheap, and a first cell holding two hundred tenant databases is not a cheap failure.
