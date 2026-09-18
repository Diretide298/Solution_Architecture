# Schema merge audit — what the developer team's tables actually hold

> **18 September 2026.** Matching `TICVAI_16_Services_AND_Tables_UPDATED` against the package by
> column content rather than by name. **The change log's 743 rows describe the wrong thing.**

## Method

Names were the least reliable signal, so this compares what each table *holds*. Every column on
both sides was normalised — their table-name prefix stripped (`access_point_code` → `code`,
`access_point_id` → `id`), their five schema renames applied, `tenancy_scope_id` folded to
`scope_id` — and each of their 323 tables matched to the package table with the highest column
overlap.

Their 3,718 columns against the package's 3,983.

| | |
|---|---|
| matched to a package table (overlap ≥ .35) | **158** |
| no counterpart | **165** |

**A note on an earlier number.** A first pass reported 631 tables in their workbook. That was
wrong — it swept up `Purpose:` prose sitting in the table-name column. The figure is 323.

---

## The finding

**There are four architectural divergences, and everything else is detail.** The change log records
645 column renames as though the difference were naming. It is not. Four decisions were made
differently, and each one propagates across dozens of tables.

### 1. Scope is a path for us and a foreign key for them

| | |
|---|---|
| their tables carrying `scope_id` (uuid FK) | **63** |
| their tables carrying `scope_path` (ltree) | **4** |
| package tables carrying `scope_path` | **73** |

They dropped `scope_path` from **34** matched tables and added `scope_id` to **30**.

**This is the one that cannot be split down the middle.** The package's row-level security is a
predicate — `platform.in_scope(scope_path)` resolving `ltree <@` against the paths the connection
was granted. A uuid foreign key cannot answer *is this row at or beneath a scope I hold* inside a
policy without a recursive query per row, which is a policy nobody will keep enabled under load.

`V0001__baseline.sql`, ADR-0002 and the Sprint 1 Gate 0 criterion all rest on the path.

### 2. A venue is a tree node for us and an entity for them

They introduce `venue.venue` (19 columns: address, city, country, latitude, longitude, time zone,
status), plus `venue_department`, `venue_zone`, `venue_outlet`, `venue_space`. The package models
all of these as rows in `platform.org_unit`, typed by `platform.scope_level` and located by their
`ltree` path.

**The consequence is measurable: they dropped `venue_id` from 25 matched tables.** ADR-0044 — signed
off today — partitions exactly the tables whose `venue_id` is `NOT NULL`, and reads that rule from
the schema. Against their model the rule finds a fraction of what it should.

This is the same disagreement as §1 seen from the data side. Concrete entities are easier to query
and report on; a generic tree is what makes one policy cover every table.

### 3. Personal data is a separate schema for us and inline for them

Their `identity.customer` carries `first_name`, `middle_name`, `last_name`, `phone_number`,
`date_of_birth` directly.

The package keeps these in `pii.subject`. `MIGRATIONS.md` states why: *"the `pii` schema split — an
architectural boundary, not a naming convention."* It is what makes a subject-access export
enumerable and gives a retention rule somewhere to attach.

**Collapsing it is a compliance regression**, and it lands on CF-165 (retention and archival,
modelled nowhere) and ADR-0043 (the control plane splits on personal data).

### 4. The actor is a principal for us and a user-or-customer for them

Across matched tables they drop `principal_id` (8), `created_by_principal_id` (4) and
`approved_by_principal_id` (4), and add `user_id` (8) and `customer_id` (12).

ADR-0002 makes authorisation user-driven over a single `principal` — one actor type covering staff,
guest and system. Splitting it into user and customer means every permission check asks which table
to look in, and every audit row records one of two kinds of actor.

---

## What is worth taking from them

**Audit timestamps, and they are right.** They add `created_at` to **83** matched tables and
`updated_at` to **66**. The package largely lacks both. This is the single best change in the file
and it should be adopted wholesale rather than table by table.

**`is_active` on 39 tables** — a consistent soft-state convention where the package has none.

**165 tables with no counterpart**, and the clusters are real work rather than noise:

| area | tables | note |
|---|---|---|
| marketing | 28 | |
| orders | 24 | including an 11-table payment model — gateways, links, terminals, fee and eligibility rules, deposits |
| identity | 17 | |
| workforce | 14 | |
| catalogue | 12 | includes the four rental configuration tables |
| access | 8 | **7 of them accreditation** — `accreditation` alone carries 29 columns |

**The accreditation cluster matters most.** CF-21 calls accreditation *"the only blocked work left
on the project"* — 58 requirements, no contract, one workshop still owed. They appear to have
specified it. That is worth reading before the workshop rather than after.

**Membership** (`membership_plan`, `membership_program`, `membership_benefit`, `plan_benefit`) and
the **rental** cluster are likewise genuine additions, the latter matching the 9 September workshop
almost row for row.

---

## One naming clash worth settling once

The package uses `kind`; they use `type`. 22 `kind` columns dropped, 17 `type` columns added. Either
is fine. Both is not.

---

## What this changes about the plan

**The row-by-row reconciliation was the wrong shape.** Triaging 743 change-log entries would have
spent days on 645 column renames that are one style decision, and never reached the four choices
that actually matter.

**Settle the four, in this order:**

1. **Scope — path or foreign key.** Everything else waits on it. It decides whether `V0001` stands.
2. **Venue — tree node or entity.** Decides ADR-0044 and the partition rule signed off today.
3. **Personal data — separate schema or inline.** Compliance, and cheap to keep if decided now.
4. **Actor — one principal or user-plus-customer.** Decides ADR-0002's reach.

**Then adopt, without further debate:** `created_at`/`updated_at` everywhere, `is_active`, and the
165 new tables triaged by cluster — payments, accreditation, rentals, membership — rather than
individually.

**A merge that starts anywhere else will produce a schema that is neither model.**
