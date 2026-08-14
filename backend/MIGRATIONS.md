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

One migration per module, applied in order. Module boundaries match the contract tiers.

    V0001__baseline.sql              platform, RLS, partitioning, outbox, pii   [DONE]
    V0002__identity.sql              principals, roles, grants, sso, mfa
    V0003__tenancy.sql               workstations, sale boards, devices
    V0003a__scope-typing.sql         level-typed scope FKs, outlet, tenant projection
    V0004__catalogue.sql             products, pricing, events, capacity, entitlements
    V0005__orders.sql                order lines, payments, refunds, reservations
    V0006__shift.sql                 shifts, cash movements
    V0007__access.sql                access points, admission profiles, blacklist
    V0008__ledger.sql                accounts, journals, entries, settlement
    V0009__cross_cell.sql            guest links, redemption rights, DSAR
    V0010__seating.sql               seat maps, seats, holds, blocks
    V0011__fnb.sql                   menus, modifiers, visits, kitchen
    V0012__inventory.sql             items, movements, counts, procurement
    V0013__retail.sql                merchandise, returns, wallet, gift cards
    V0014__promotions.sql            promotions, coupons, vouchers, allocation
    V0015__marketing.sql             profiles, consent, segments, campaigns, cases
    V0016__maintenance.sql           assets, work orders, inspections, incidents
    V0017__queue.sql                 queues, entries, feeds
    V0018__white_label.sql           tenant config, content, versions
    V0019__assets.sql                media library, collections, rights
    V0020__games.sql                 cards, games, plays, prizes
    V0021__reporting.sql             definitions, executions, schedules

`subscription` has no migration here — it is Control Plane and lives in a separate database
outside any cell.

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
