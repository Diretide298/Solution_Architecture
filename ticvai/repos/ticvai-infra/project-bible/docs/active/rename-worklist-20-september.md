# Their workbook, every change in it, and what it means for us — 20 September

> **Owner:** Chinmay · Supersedes the rename bullets in [current-work.md](current-work.md) and the
> first cut of this file, which said 42 and was wrong.
>
> Measured against **556 of our tables and 323 of theirs**. The 18 September pass ran against 374
> of ours.

---

## Every change they declare

`TICVAI_16_Services_AND_Tables_UPDATED (1).xlsx` carries two independent records of change, and
both had to be read.

**The Change Log sheet — 743 rows.**

| change type | rows |
|---|---:|
| Column Renamed | 645 |
| Table Added | 28 |
| Column Attributes Changed | 23 |
| Column Added | 17 |
| Table Renamed | 12 |
| Column Renamed & Attributes Changed | 9 |
| Schema Prefix Renamed | 5 (covering 43 tables) |
| Proposed then Rejected | 3 |
| Column Removed | 1 |

**A `Purpose:` line above every one of the 323 tables** — the functionality, in their words. It
flags **28 NEW TABLE** and **15 MODIFIED** outright. This is the record that matters most and it
is not in the Change Log at all.

---

## The 28 new tables are three whole domains, and we built all three

| their new tables | n | ours |
|---|---:|---|
| **payment / deposit / fee** — `orders.payment_method`, `payment_method_config`, `payment_policy`, `payment_terminal`, `payment_link`, `payment_eligibility_rule`, `payment_fee_rule`, `currency_rule`, `order_fee`, `deposit`, `deposit_activity` | 11 | **`payments.*` — 16 tables** |
| **rental** — `catalogue.rental_product_config`, `rental_rate`, `rental_requirement`, `rental_rule`; `resources.rental_agreement`, `rental_agreement_item`, `rental_inspection`, `rental_inspection_item`, `rental_product_mapping`; `maintenance.rental_damage_assessment` | 10 | **`rental.*` — 21 tables** |
| **subscription / tier** — `platform.subscription_tier`, `tenant_subscription`, `tier_allowance`, `tier_module` | 4 | `control.subscription*` |
| customer extra fields — `identity.customer_extra_field`, `_option`, `_value` | 3 | — genuinely new |

**Both teams built rental and payment orchestration inside the same week, in different schemas.**
Ours went into `rental` and `payments` as their own schemas on 19 September; theirs went into
`catalogue`, `resources`, `maintenance` and `orders`.

The exact-name collisions make the overlap unarguable:

    maintenance.rental_damage_assessment   ->  rental.damage_assessment
    orders.payment_method                  ->  payments.method
    orders.payment_terminal                ->  payments.terminal
    resources.rental_inspection            ->  rental.inspection

**This is the most expensive thing in the file and it is not a rename argument.** It is two
schemas for one domain, decided independently, and it needs settling before either side writes
migrations.

## The 15 modified tables say what changed and why

Their `Purpose` prose is explicit where a Change Log row is not — `orders.cart_line` *"makes the
cart support items recommended from Catalogue, FnB and Retail"*, `marketing.campaign` *"adds
optional journey_id so the same campaign model serves journeys"*, `access.scan` *"keeps the
existing common scan history while allowing the same scanner to validate more"*.

`orders.payment_gateway` and `orders.payment_route` are in this list, **not in Table Added** —
they are modifications of tables they already had, which is why the 18 September pass read them as
renames of our `payment_provider` and `payment_routing`.

---

## Renames: the matcher gets part of the way and stops

**The first cut of this file said 42 and used Jaccard similarity. That was the wrong measure.**
A real rename has genuinely different column sets — they added columns, we added others — so
Jaccard collapses while containment stays high. Scored the old way, **every one of the fourteen
renames found by hand on 18 September falls below the threshold**; the highest is 0.36.

Re-run on containment within the same schema:

| band | n | what it is |
|---|---:|---|
| **0 — certain** | 25 | their redundant table prefix, our exact table exists. No scoring: `approvals.approval_matrix` → `approvals.matrix`, `inventory.stock_movement` → `inventory.movement`, `reporting.report_schedule` → `reporting.schedule` |
| **1 — strong** | 20 | one candidate, containment ≥ 0.60 — `ai.knowledge_item` → `ai.knowledge_document`, `queue.entry` → `queue.waiting_guest`, `access.scan` → `access.scan_event`, `ledger.settlement_issue` → `ledger.settlement_exception` |
| **2 — review** | 37 | one candidate, 0.40–0.60 |
| **3 — ambiguous** | 46 | several candidates; a matcher cannot choose |
| **no candidate** | 95 | nothing in the same schema shares two columns |

**128 of their 223 unmatched tables have a candidate.** Full detail in
`handoff/rename-candidates.json`; every table's stated purpose in
`handoff/their-table-purpose.json`.

### It still cannot finish, and this is the third time that has been demonstrated

Containment recovers **12 of the 18 September fourteen**. The two it misses are the proof:

    orders.payment_gateway  ->  orders.payment_provider     containment 0.29
    orders.payment_route    ->  orders.payment_routing      2 shared columns

**Those are semantic, not columnar.** Somebody read the words and knew a gateway is a provider and
a route is a routing. No threshold recovers them without admitting the noise that cross-schema
matching produced — `catalogue.membership_program` against `ledger.cost_center`,
`platform.cell` against `payments.provider_connection`.

**Use the `Purpose` line for the last mile.** It is one sentence per table in their own words, and
it settles cases columns cannot: `queue.entry` *"stores a guest waiting in a virtual queue"*
against our `queue.waiting_guest` is obvious in prose and a coin-toss in columns.

---

## Cost, for the renames that are certain

Cost is `operations + 2×inbound FK + screens`; a foreign key counts double because it is a
constraint in generated DDL.

**Four cost nothing** — `fnb.fnb_order_line`, `inventory.count_line`, `inventory.transfer_line`,
`seating.section_row`. No operation, no FK, no screen.

**Fourteen cost ten or less**, and together they are most of the vocabulary argument.

**Three need a decision before any work:**

- **`approvals.request` — 16 inbound foreign keys**, the most connected table in the list
- **`catalogue.variant` — 11 inbound FKs**, and it is what `fnb.menu_item.product_variant_id` and
  `retail.merchandise.variant_id` both point at. **The F&B isolation question settles this one**
- **`fnb.table` matches two of theirs** — `dining_table` and `reservation_table`. Either they split
  one or two collapse into one, and a matcher cannot tell which

**`orders.shift` is real.** The Change Log declares `till_shift → pos_shift`, a name we never had,
so it read as their internal churn. Band 0 shows `pos_shift` is our `shift`. Both are true.

---

## The one position that resolves most of the file

Their 645 column renames are a single habit applied mechanically: prefix every column with its
table name, so `code` becomes `access_point_code` and `id` becomes `<table>_id` on 193 tables.
**We do not prefix** — `access.access_point.code` is already unambiguous.

**Stated once, that answers 645 of 743 rows.** What is left needs individual answers: the 28 new
tables, the 15 modified, and the banded renames above.
