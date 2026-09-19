# The rename worklist — 42, not 3

> **Owner:** Chinmay · **Written:** 20 September 2026 · Supersedes the rename bullets in
> [current-work.md](current-work.md)
>
> Measured against **556 of our tables and 323 of theirs**. The 18 September pass ran against
> 374 of ours and is history.

## Why three was the wrong number

Their Change Log declares **12 table renames and we owe 3 of them** — but it only declares
renames **inside their own model**. `marketing.segment -> marketing.customer_segment` is there
because *they* changed their own mind, not because they were comparing to us.

**The renames between their names and ours are almost entirely undeclared.** 223 of their tables
have no name in common with ours and 456 of ours have none with theirs, and most of that is one
table under two names. Finding them is column work, and it recovers **42**.

## How they were found, and the two that work

**Band 0 — their redundant table-name prefix. 25 tables, certain.**
They repeat the schema or the subject in the table name: `approvals.approval_matrix`,
`inventory.stock_movement`, `reporting.report_schedule`. Strip the prefix and **our exact table is
there**. No scoring, no threshold — the stem matches or it does not.

**Band A — column overlap within the same schema. 17 more.**
Their columns carry the same habit one level down (`access_point_code` for `code`), so the columns
are normalised before comparing. Jaccard ≥ 0.50, at least four shared columns, **and both sides in
the same schema**. That last condition is what makes it trustworthy.

**Band C — cross-schema column matching. Discarded.**
It proposes `catalogue.membership_program ~ ledger.cost_center` and
`platform.cell ~ payments.provider_connection`. **Two tables that share four column names share
nothing else**, and the 18 September pass reached the same conclusion from the other direction:
step 3 must be human. Twenty-nine candidates dropped.

## What this corrects

**`orders.shift` is real after all.** The Change Log declares `orders.till_shift ->
orders.pos_shift`, which reads as their internal churn against a name we have never had — and on
that basis it was earlier marked *confirm before paying*. Band 0 shows `pos_shift` is our `shift`.
**Both are true**: they renamed `till_shift` to `pos_shift` internally, and `pos_shift` is our
`shift`. It is the third most expensive rename on the list.

**Yesterday's "seven the Change Log does not declare" are all here**, inside the 25 — the six
`approvals.*` and `resources.resource_booking`. So are eighteen more nobody had found.

## The worklist, cheapest first

Cost is `operations + 2×inbound FK + screens`. An inbound foreign key counts double: it is a
constraint in generated DDL, not just a reference to update.

| ours | theirs | rd | wr | FK | screens | cost |
|---|---|---:|---:|---:|---:|---:|
| `fnb.fnb_order_line` | `fnb.order_item` | 0 | 0 | 0 | 0 | **0** |
| `inventory.count_line` | `inventory.stock_count_line` | 0 | 0 | 0 | 0 | **0** |
| `inventory.transfer_line` | `inventory.stock_transfer_line` | 0 | 0 | 0 | 0 | **0** |
| `seating.section_row` | `seating.seat_section_row` | 0 | 0 | 0 | 0 | **0** |
| `whitelabel.faq_entry` | `whitelabel.faq` | 1 | 0 | 0 | 0 | 1 |
| `ai.suggestion_outcome` | `ai.suggestion_result` | 0 | 1 | 0 | 1 | 2 |
| `fnb.eighty_six_event` | `fnb.sold_out_item` | 1 | 0 | 0 | 1 | 2 |
| `fnb.recipe_ingredient` | `fnb.recipe_item` | 0 | 0 | 2 | 0 | 4 |
| `marketing.challenge_progress` | `marketing.customer_challenge_progress` | 1 | 0 | 0 | 3 | 4 |
| `marketing.suppression` | `marketing.do_not_contact` | 3 | 1 | 0 | 1 | 4 |
| `control.webhook_delivery` | `control.webhook_log` | 1 | 1 | 0 | 3 | 5 |
| `fnb.temperature_log` | `fnb.temperature_check` | 2 | 1 | 0 | 4 | 6 |
| `platform.denomination` | `platform.cash_denomination` | 1 | 0 | 1 | 5 | 8 |
| `seating.seating_rules` | `seating.seat_rule` | 4 | 1 | 0 | 5 | 9 |
| `reporting.schedule` | `reporting.report_schedule` | 4 | 3 | 2 | 3 | 11 |
| `inventory.count` | `inventory.stock_count` | 7 | 5 | 1 | 4 | 13 |
| `inventory.transfer` | `inventory.stock_transfer` | 4 | 3 | 2 | 6 | 14 |
| `whitelabel.feature_toggle` | `whitelabel.feature_setting` | 4 | 2 | 0 | 10 | 14 |
| `whitelabel.module_enablement` | `whitelabel.module_setting` | 4 | 2 | 0 | 10 | 14 |
| `approvals.escalation` | `approvals.approval_escalation` | 1 | 1 | 0 | 17 | 19 |
| `platform.region_settings` | `platform.region_setting` | 7 | 2 | 0 | 12 | 19 |
| `maintenance.maintenance_plan` | `maintenance.preventive_plan` | 6 | 2 | 0 | 14 | 20 |
| `approvals.delegation` | `approvals.approval_delegation` | 4 | 2 | 1 | 17 | 24 |
| `inventory.movement` | `inventory.stock_movement` | 6 | 6 | 0 | 16 | 27 |
| `marketing.segment` | `marketing.customer_segment` | 4 | 2 | 6 | 13 | 29 |
| `resources.booking` | `resources.resource_booking` | 9 | 3 | 1 | 18 | 29 |
| `venuemap.path` | `venuemap.route` | 6 | 3 | 0 | 21 | 29 |
| `approvals.matrix` | `approvals.approval_matrix` | 4 | 1 | 1 | 24 | 30 |
| **`fnb.table`** | **`fnb.dining_table` / `fnb.reservation_table`** | 13 | 6 | 3 | 13 | 33 |
| `marketing.campaign` | `marketing.loyalty_campaign` | 11 | 7 | 5 | 12 | 33 |
| `reporting.execution` | `reporting.report_execution` | 5 | 2 | 1 | 26 | 33 |
| `approvals.decision` | `approvals.approval_decision` | 2 | 1 | 0 | 31 | 34 |
| `access.admission_rules` | `access.entry_rule` | 7 | 2 | 6 | 18 | 37 |
| `marketing.case` | `marketing.support_case` | 11 | 8 | 3 | 20 | 39 |
| **`orders.shift`** | **`orders.pos_shift`** | 11 | 7 | 6 | 16 | 39 |
| `approvals.rule` | `approvals.approval_rule` | 5 | 1 | 1 | 34 | 42 |
| `fnb.fnb_order` | `fnb.order` | 18 | 11 | 1 | 24 | 45 |
| `ai.policy` | `ai.usage_policy` | 12 | 2 | 1 | 33 | 47 |
| `ai.interaction` | `ai.activity` | 4 | 12 | 2 | 37 | 57 |
| `catalogue.variant` | `catalogue.product_variant` | 5 | 2 | 11 | 29 | 57 |
| **`approvals.request`** | **`approvals.approval_request`** | 6 | 8 | **16** | 50 | **92** |

**42 renames · 207 reads · 117 writes · 76 inbound foreign keys · 564 screen references.**

## How to take it

**Four cost nothing** — no operation reads or writes them, no foreign key points at them, no
screen names them. Do those first and the list is 38.

**Fourteen cost ten or less.** Together they are most of the vocabulary argument and almost none
of the risk.

**Three need a decision before any work.**

- **`approvals.request` at 92, with 16 inbound foreign keys.** The most connected table in the
  list by a distance. Renaming it touches sixteen DDL constraints.
- **`fnb.table` matches two of theirs** — `fnb.dining_table` and `fnb.reservation_table`. Either
  they split one table into two or two of theirs collapse into one of ours. **A matcher cannot
  tell which**, and guessing produces a table nobody owns.
- **`catalogue.variant` at 57, 11 inbound FKs** — and it is the table
  `fnb.menu_item.product_variant_id` and `retail.merchandise.variant_id` both point at, so it is
  already the subject of the F&B/Retail isolation question. **Settle that first**; the rename is
  the smaller half of it.

## The position that resolves the rest

Their 645 column renames are one habit applied mechanically — prefix every column with its table
name, `code` becomes `access_point_code`. **We do not prefix**: `access.access_point.code` is
already unambiguous and `access_point_code` says the same thing three times.

**Stated once, that answers 645 of their 743 changes.** The 42 above are the part that needs
individual answers.
