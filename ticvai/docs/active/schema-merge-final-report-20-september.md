# Schema merge — final report

> **To:** the backend team · **From:** design · **20 September 2026**
> **Supersedes** `schema-merge-response-20-september.md`, which was written at 151 of 223 and
> before the criteria below were agreed.
>
> Every row: `handoff/TICVAI_Schema_Merge_Tasks.xlsx`. Every reason:
> `handoff/merge-verdicts.json`. The eleven structural decisions, scored:
> [schema-merge-decision-log.md](schema-merge-decision-log.md).

---

## How every call was made

**This was not our schema against yours.** Where your shape is better we took it, where ours is
better we kept it, and where each had half we combined. Nothing was decided on who authored it or
on how much a rename costs — **effort is a thing to plan around, not a thing to decide on.** Four
criteria, and nothing else:

| | the question |
|---|---|
| **Maintainability** | how many places a change has to be made, and how many ways to get it wrong |
| **Readability** | does the name tell a developer what the rows are, without the schema doc open |
| **Optimised access** | does the query a screen actually runs stay inside one schema, on narrow rows |
| **DB strain** | contention, row width, update churn, and what shares a hot table with what |

**The first pass of this review was argued on cost.** Re-reading all 223 against these criteria
moved **38 rows**, almost all of them in your favour.

## Where the 223 landed

| | tables | |
|---|---:|---|
| **we take yours** | **105** | your table, your name, or your columns |
| we keep ours | 105 | with the reason stated per row |
| **open** | **7** | payroll — a scope question, not a schema one |
| corrections | 6 | matches we had wrong |

**100 more of your tables already carry a name we use**, so the workbook agrees with us on 204 of
323 before any of this starts.

---

## 1 · What we are changing on our side

**Thirteen of these are ours to fix and would have been fixed whatever you had sent.** Your workbook
is how we found most of them.

### Things that are wrong today

| | |
|---|---|
| **`marketing.loyalty_programme` holds no rules.** It is a header — code, name, expiry months. The only rules table is **`marketing.loyalty_tier`, which is misnamed** (it holds earning triggers and multipliers, not tiers) and **referenced by nothing at all: 0 operations, 0 screens, 0 foreign keys.** The tier a guest is in is two denormalised strings on their balance row | **your split is right.** We take `points_earning_rule`, `points_redemption_rule` and `loyalty_rule`, retire `loyalty_tier`, and add a real tier table |
| **`marketing.loyalty_position` is a balance with no ledger behind it.** It cannot be audited or corrected | we take `marketing.loyalty_points` |
| **We hold `rental.agreement_rules` and `rental.agreement_signature` and no agreement.** The signature references a participant and a version *string*, so it signs a version number rather than a document, and `rental.participant` carries no booking reference at all | **we take `rental_agreement`**, and merge `rental_agreement_item` with our `equipment_assignment` |
| **`orders.payment_routing` and `payments.routing_rule` are the same table.** Both are "priority plus conditions decide which provider" | your single `payment_route` maps onto both. We collapse them |
| **`rental.category` is the asset-category master for the whole venue** — `maintenance.asset`, `maintenance_plan`, `inspection_template`, `resources.resource_category` and `resource_requirement` all point at it. A forklift that is never rented has its category defined in `rental` | it moves out of `rental` |

### Things that are inconsistent

- **Payments live in two of our schemas** — 6 tables in `orders`, 16 in `payments`. We move
  `payment_provider`, `payment_token` and `payment_routing` into `payments` **before** asking you
  to move anything.
- **Subscription lives in three places** — `control.subscription`, `control.subscription_plan` and
  a nine-table `subscription` schema. We consolidate into `subscription`.
- **`platform.org_unit` becomes `platform.scope`.** Your name is better and we are taking it:
  `scope` is the word **58 of our configuration profiles already address by**; `org_unit` is
  generic ERP vocabulary that appears nowhere else in our language.
- **We have no singular-or-plural rule** — `sla_policy`, `admission_rules`, `region_settings`,
  `seating_rules`. We will publish one and apply it to ourselves first. Until then we cannot argue
  yours, and `access.entry_rule` and `seating.seat_rule` are parked on it.
- **`fnb.fnb_order` repeats its schema** — the exact fault we are asking you to fix in
  `approvals.approval_matrix`. Taken: `fnb.order`, `fnb.order_line`, `orders.discount`.

### The one that is bigger than this merge

**140 of our 556 tables carry an array column that encodes a relationship.** Your workbook
normalised six of them and we took all six. `access.admission_rules.allowed_access_point_ids` is
the proof — your `entry_rule_point` *is* that array as a table.

**The other 134 are the same decision, unreviewed.** An `_ids` array cannot be joined, cannot
carry per-row state, needs a GIN index for a membership test, and is rewritten whole on every
change. That is our review to run, not yours, and it does not block anything here.

---

## 2 · What we are asking you to change

**Four schema renames, across 29 tables. No foreign key is repointed, no operation changes, no
screen changes** — your table names already carry the domain.

| | move | to | why |
|---|---|---|---|
| **rental** | 10 tables from `catalogue`, `resources`, `maintenance` | `rental` | **`catalogue.rental_rate` puts rental pricing inside the hottest table set in the system.** That is the flash-sale contention argument that gave F&B and Retail their own price tables, reintroduced. Your layout also splits rental across CatalogueService and VenueOpsService |
| **payments** | 5 tables from `orders` | `payments` | all five are **configuration**. `orders` is the highest-churn schema in the system, and config read on every checkout should not share a schema with rows written on every sale |
| **subscription** | 2 tables from `platform` | `subscription` | your placement puts billing in TenancyService and licensing in PlatformService. **A plan lookup becomes a cross-service call** |
| **accreditation** | 4 tables from `access` | `accreditation` | same principle |

### And one position that answers 645 of your 743 change rows

**Column prefixes.** You prefix every column with its table name — `code` becomes
`access_point_code`, `id` becomes `<table>_id` on 193 tables. **We do not**, because
`access.access_point.code` is unambiguous inside its own row. One decision, not 645 — and it also
disposes of **21 table renames** where the name repeats its own schema.

**The bound on that rule**, so it is not applied blindly: strip a repeated prefix only where what
is left still names the thing. `approvals.approval_matrix` → `matrix`, yes.
`orders.order_line` → `orders.line`, no.

**If you want the prefix, say so and say why.** There is a real argument for it if your ORM or
reporting layer flattens joins into one namespace, and we would rather hear it.

---

## 3 · Where we are keeping ours, and the reason in one line each

| | our table | the reason |
|---|---|---|
| `identity.customer`, `_address`, `family`, `family_member` | `marketing.guest_profile` + `pii.subject` + `guest_relationship` | **`identity.principal` carries 134 inbound foreign keys — the most connected table in the package.** Your proposal adds every guest row to the table every authentication already reads. The split is also what lets a DSAR walk one subtree |
| `marketing.data_subject_request` | `platform.dsar_request` | a DSAR spans every service. Ours is TenancyService and walks `guest_link`; yours would be MarketingService, which owns one of the dozen schemas a DSAR must reach |
| `sync.guest_link` | `platform.guest_link` | **we reversed ourselves on this one.** `dsar_request.guest_link_id` points at it and both are TenancyService. Moving the link alone puts a DSAR fan-out across a service boundary on its hottest path |
| `venue.venue`, `department`, `outlet`, `space`, `zone` | `platform.scope` | **each of the five is a *level* of a hierarchy we hold as rows.** `ScopeLevel` enumerates tenant, brand, region, venue, department, subDepartment, workstation, outlet and subject, and ADR-0011 makes it binding. Five typed tables make adding a level a new table |
| `orders.order` | `orders.sales_order` | `sales_order` distinguishes it from an F&B order, a purchase order and a kitchen order |
| `inventory.wastage` | `inventory.movement` | ours carries `unit_cost`, `cost_center_id` and `journal_entry_id`, so wastage posts to the ledger by the same path as every other movement. A separate table splits the stock ledger in two |
| `marketing.survey`, `waiver_template` | `marketing.form_definition` | it holds `kind`, `score_scale`, `requires_signature`, `signature_kind`, `legal_reviewed_by` and `version` — NPS and a waiver are shapes of one form |
| `whitelabel.module_setting` | `whitelabel.module_enablement` | and **your workbook settled a question we had open**: yours is what is *visible*, `identity.enabled_module` is what the tenant *bought*. Three facts, not one duplicated three times |

---

## 4 · What we need back

**One question, and it is the only thing still open.**

**Is payroll in scope?** Your `workforce` is a full HR and payroll system; ours is rostering.
Seven payroll tables — `payroll_run`, `payroll_employee`, `payroll_line`, `payslip`, `salary`,
`salary_component`, `pay_component` — have **no requirement behind them in anything we hold**, and
**seven HR master tables we have already accepted are conditional on the answer**.

*Are we building payroll, or rostering against an external HR system?*

**One thing to note whichever way it goes:** `workforce` is TenancyService. Payroll is a finance
function, and putting payslips and salary components inside the service that manages tenants and
staff rosters is wrong on maintainability regardless of scope. **If the answer is yes, payroll
wants its own schema and its own owner** — not thirteen more tables in `workforce`.

### Two smaller ones, where either answer works

- **Column prefixes** — §2. If you want them, we want the reason.
- **`platform.scope`** — we are taking your name. Confirm you are happy for the hierarchy to stay
  one table rather than five.

---

## 5 · Corrections to things we told you earlier

**We said we had no dynamic pricing at all.** We do — three guardrail columns on
`rental.pricing_profile`: `dynamic_enabled`, and a maximum increase and decrease percent. **A
ceiling and a floor with no engine under them**, and nothing at all on tickets, F&B or retail.
Your three `pricing` tables are still a genuine gap; the claim was overstated.

**We said `venue.department` was a gap and that `platform.workstation.department_id` pointed at nothing. Both were wrong** — `department` is one of nine `ScopeLevel` values, the column points at `platform.org_unit` with `level: department`, and ADR-0011 makes that hierarchy binding. We are declining all five `venue` tables, not four.

**Two matches we had wrong**, corrected so they do not propagate:

| yours | we first matched | actually |
|---|---|---|
| `wallet.account` | `ledger.account` | **`wallet.wallet`** — a stored-value master, not a chart of accounts |
| `whitelabel.menu_item` | `fnb.menu_item` | **`whitelabel.navigation_item`** — a navigation menu, not food |

**And one about your own workbook**, in your favour: `orders.pos_shift` appears in your Change Log
as an internal rename of `till_shift`, a name we never had, so it first read as your churn. **It
is our `orders.shift`.** Both readings were true at once.

---

## What would help most next time

**The `Purpose:` line above each table settled more cases than the Change Log did.** It is one
sentence in your own words and it resolved things columns could not — `queue.entry` *"stores a
customer or party currently waiting"* told us in nine words that our `waiting_guest` misnames a
party of six. **Please keep writing it.**
