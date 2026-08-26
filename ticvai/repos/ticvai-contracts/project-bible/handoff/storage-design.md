# Storage design

**The 30% of a migration that does not derive from the contracts.**

The schema reference workbook holds tables, columns and types — roughly 70% of any migration,
derived mechanically from `x-ticvai-persistence` markers. This document holds the rest: the
part that makes it a database rather than a spreadsheet, and the part that protects the data.

Written down because the SQL that carried it has been removed from the delivery package while
the design settles. **When migrations resume, this is what they must contain beyond the
column list.**

---

## Row-level security

**Every table carrying `scope_path` or `venue_id` gets three statements, not one.**

    ALTER TABLE x ENABLE ROW LEVEL SECURITY;
    ALTER TABLE x FORCE  ROW LEVEL SECURITY;
    CREATE POLICY x_scope ON x USING (platform.in_scope(scope_path));

`FORCE` is the one people omit. Without it **the table owner bypasses every policy**, which
makes data-layer enforcement decorative for exactly the role most likely to run an ad-hoc query
at 2am.

This matters more since ADR-0017: on a shared cell, RLS is the only thing between two paying
customers.

Test it by proving it bites, not by reading it:

    SET ticvai.scope_paths = 'tenant.brand.region.venue_a';
    SELECT count(*) FROM orders.sales_order;   -- venue_a only
    RESET ticvai.scope_paths;
    SELECT count(*) FROM orders.sales_order;   -- 0, not everything

**Two exemptions, both deliberate.** `platform.outbox` is written inside the same transaction
as the state change it records, so a policy failure there would roll back a sale for a
bookkeeping reason; its `venue_id` is copied from an already-validated row. The relay reads it
through a named role holding `BYPASSRLS` — **a bypass granted to one auditable role beats an
absent policy.** Default partitions inherit their parent's policy and need none of their own.

## Level-typed scope references

`venue_id uuid` on 48 tables prevented nothing. The type said uuid, the intent said venue, and
nothing checked.

    venue_level platform.scope_level GENERATED ALWAYS AS ('venue') STORED,
    FOREIGN KEY (venue_id, venue_level) REFERENCES platform.scope_node (id, level)

`scope_node` carries `UNIQUE (id, level)` — redundant against its own primary key, and there
solely so this composite key is possible. Postgres then refuses a reference to anything that is
not a venue. No trigger, no application check.

Thirteen generated columns across the written tables. **Every future table with `venue_id`
needs the same two lines.**

## Partitioning

`orders.sales_order` and `access.scan_event` partition by list on `venue_id`.

Three rules that came out of getting it wrong:

**`venue_id` must be in the primary key.** Postgres requires it, and discovering that at
migration time is a rewrite.

**Every partitioned table needs a default partition.** `sales_order_unassigned` and
`scan_event_unassigned` catch rows whose venue matches no configured partition, so a
misconfiguration is loud rather than silently lossy.

**A partitioned table can still hold an outgoing foreign key** since Postgres 12, and the check
is a unique-index lookup. Worth the microseconds: a scan event pointing at a venue that does not
exist is an admission nobody can attribute afterwards.

## Indexes

53 across 40 tables, and **26 of them partial**.

`WHERE is_active` · `WHERE revoked_at IS NULL` · `WHERE status <> 'online'` ·
`WHERE expires_at > now()`. A partial index on the rows anyone actually queries is a fraction
of the size and stays in memory.

**10 GiST indexes**, one on every `ltree` path. `scope_path` is queried with `<@` and `@>` on
every scoped read; a btree does not serve those.

**174 tables still have no index strategy at all.** That is the largest single gap in the
storage design and the one that decides whether the read replicas in ADR-0016 help or merely
spread the problem.

## Constraints that encode a decision

28 checks. The ones worth keeping:

| | |
|---|---|
| `principal_deactivation_reason` | Deactivation always carries a reason. "Who disabled this and why" is the first question after an incident |
| `mfa_active_requires_verification` | A method cannot be active before it is verified — enrolling then enforcing locks the principal out of their own account |
| `subject_erasure_is_complete` | An erased subject cannot retain identifying fields. **A partial erasure that reports success is worse than a failure** |
| `sale_board_tile_product` | A product tile with no variant is a button that does nothing. Caught here rather than by a cashier during service |
| `drop_line_collected` | Collecting more than was dropped is not partial collection |
| `grant_unique_live` (partial unique) | One live grant per role per scope. A duplicate is a data defect, not a stronger grant |

**One anti-pattern to avoid repeating:** V0003 originally carried
`CONSTRAINT venue_settings_level CHECK (EXISTS (SELECT 1))` — a constraint that always passes,
standing in for a check a `CHECK` cannot do. **A constraint that reads like enforcement and
isn't is worse than none**, because it stops anyone looking.

## Functions and triggers

Seven functions. Three are load-bearing.

**`platform.in_scope(ltree)`** — the RLS predicate. Every policy calls it.

**`platform.cascade_scope_path()`** — when a venue moves region, every denormalised
`scope_path` beneath it updates in the same transaction. **The riskiest function in the
schema**: if it is wrong, RLS silently starts answering the wrong question and nothing fails
loudly.

**`pii.erase_subject(uuid, char)`** — erasure as one transaction. Written as a function rather
than left to the application because a partial erasure reports success while leaving an email
behind, and nobody checks again. It deletes contacts, documents and biometrics entirely and
leaves the subject row as a tombstone: **a sale cannot be unwritten because the buyer asked,
and it does not need to be — it never held a name.**

`assert_scope_level()` enforces what a `CHECK` cannot, since a check constraint cannot query
another table.

## Enum agreement

Every Postgres enum must hold the same values as its contract counterpart. Three disagreed on
14 August, including `scope_level` carrying `sub_department` against the contract's
`subDepartment` — **a hierarchy level that would not resolve**.

`check-migrations.py` now compares them.

---

## Conventions that survive the SQL being removed

**Forward-only.** No file is edited after merge. A mistake is a new migration.

**Every migration reversible**, with the rollback tested against a restored snapshot rather
than asserted. A rollback nobody has run is a comment.

**Additive first.** Add column, backfill, switch reads, drop old — four migrations, not one. A
cell mid-rollout runs two application versions against one schema.

**Migrations fan out per region, not per tenant** (ADR-0014), and on a shared cell a tenant
cannot defer an upgrade because many tenants share one schema version (ADR-0017).

**Nothing has ever been executed.** No `psql`, no restored snapshot, no rollback test. Every
statement above is structurally checked and syntactically unverified.
