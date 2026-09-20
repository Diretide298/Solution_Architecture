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
| we keep ours | 112 | with the reason stated per row |
| **open** | **0** | payroll closed on your own sources — §4 |
| corrections | 6 | matches we had wrong |

**100 more of your tables already carry a name we use**, so the workbook agrees with us on 204 of
323 before any of this starts.

---

## 1 · What we are changing on our side

**Fourteen of these are ours to fix and would have been fixed whatever you had sent.** Your workbook
is how we found most of them.

### The biggest thing you found — and we got it wrong twice before getting it right

**We first said we had reached this conclusion independently. We had not.** F&B and Retail have
their own schemas and their own services in our package, but not their own catalogue data:

    fnb.menu_item.product_variant_id   ->  catalogue.variant
    retail.merchandise.variant_id      ->  catalogue.variant
    retail.merchandise.price           ->  a column, not a price table

**Then we took all ten of your tables, and that was wrong too.** Here is the measurement that
settled it:

| | columns | operations |
|---|---|---|
| `catalogue.product` | 21 | **40**, across twelve contracts |
| `fnb.product` | 12 | 0 |
| `retail.product` | 11 | 0 |

The same holds for `product_category`, `variant`, `price` and `price_list`. **No retail operation
reads `catalogue.product` at all**, and `fnb` reads it exactly once.

**A split that relieves contention requires moving the reads, not adding the tables.** We added
ten tables and moved nothing — all of the maintenance cost, none of the isolation, and three
models to keep in step where a tax rule or an allergen flag now has three homes. The contention we
were protecting `catalogue` from is not in the contracts on either side.

So the ten come out, and `catalogue.*` stays the one product model. Where contention turns out to
be real we have `x-ticvai-read-routing: analytical`, which does not cost a second copy.

**Six of your columns stay, and one of them is the best single find in the workbook:**

| Column | Why |
|---|---|
| `catalogue.product.categoryId` | **`catalogue.product_category` has had two operations since 20 August and nothing could be filed under it.** A merchandise hierarchy with a tree and no leaves. Both your product tables carried this link and ours did not |
| `catalogue.product.isStockTracked` | whether a sale decrements stock — not what `isSellable` asks. A ticket does not, a bottle of water does |
| `catalogue.variant.name` | `axisValues` gives `{size: L}` and no string a guest can read |
| `catalogue.variant.barcode` | our `alternative_code` is a *partner's* code and requires `partnerId`, so a manufacturer's EAN had nowhere to live |
| `catalogue.variant.isDefault` | which variant a product page opens on |
| `catalogue.product_category.code` | a stable import key. Ours had a uuid and a localised name |

**`fnb.product_recommendation` and `retail.product_recommendation` are kept whole** — 17 columns
each, and we have nothing like them.

**How we caught it is worth more than the correction.** Our phase 3 tested *"already a table of
ours"* by name, so anything you sent under a name we did not use looked like a gap. That is also
what produced a duplicate `fnb.order` beside our `fnb.service_order`. There is now a check for it
that runs on every build, and it found all ten of these plus two in `whitelabel` on its first run.

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
| **rental** | 10 tables from `catalogue`, `resources`, `maintenance` | `rental` | **`catalogue.rental_rate` puts rental pricing inside the hottest table set in the system.** `catalogue.product` alone is read by twelve contracts across 40 operations, so a rental rate change takes write locks in the middle of that. (§1 explains why we are *not* splitting F&B and Retail off it — the fix for a hot table is routing, not a second copy of the model.) Your layout also splits rental across CatalogueService and VenueOpsService |
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

## 4 · Payroll, and why we are declining it on your own sources

**Nothing in this merge is still open.** We had payroll down as a question for the client. It did
not need to be one — the answer is in the client's reference pack and in the requirement matrix,
and we would rather cite those than tell you what we think.

### Your pack

`Resource_Management_Configuration_Reference.pdf`, **Board 3, page 45 — "Workforce Integration &
Synchronization Center"**:

> **Purpose.** Connect TICVAI Resource Management with **external** HR, workforce management,
> **payroll**, identity, and employee systems where applicable.
>
> **Integration Sources.** HRMS · Workforce Management · **Payroll** · Time & Attendance ·
> Identity Management · External staffing agencies

**Board 10** lists Payroll again — as an integration to **monitor**, beside HRMS, with sync
status, failed records and latency.

### The matrix

**Zero rows mention payroll, payslip, salary, wage, HRMS or HR system**, across all five sheets.
What it does require, at the rows Board 4 itself cites:

| | |
|---|---|
| 1.2.32–33 | staff scheduling, assignment, shifts |
| **1.2.37** | *"System shall **integrate** approved leave requests"* — integrate, not manage |
| 1.2.80–81 | shift swaps, check-in and check-out, lateness, no-shows, overtime |
| 1.2.83 | validate against working-hour limits, breaks, **certifications**, rest periods, union rules |
| **1.2.84** | *"calculate **labor costs**, staffing budgets, overtime costs… by venue, department, attraction"* |

**1.2.84 is labour costing, not payroll.** Costing a roster is not paying anybody, and it is the
closest the matrix comes.

### So

| | |
|---|---|
| **the seven payroll tables** | **declined.** `payroll_run`, `payroll_employee`, `payroll_line`, `payslip`, `salary`, `salary_component`, `pay_component` |
| **the seven HR tables** | **taken — as an externally mastered projection, not an HR master.** 1.2.83 needs certifications and job roles, 1.2.84 needs a cost rate per employee, and your Board 3 eligibility engine evaluates leave. The rows live with us; the system of record does not |

### And a gap this turned up in both of us

**Board 3 requires a field-ownership model** — *"for every field, administrators shall determine"*
which system is master, because that is what *"prevents conflicting updates"*. Board 10 specifies
a six-state integration monitor: connected systems, last synchronisation, successful records,
failed records, warnings, mapping errors, authentication status.

**We hold none of it. Neither does your workbook.** Your own conflict cases — *"employee exists
in HR but not TICVAI"*, *"employee terminated externally but has future TICVAI assignments"* — are
exactly what goes wrong without it. **Taking your employee tables without this layer takes the
data and leaves the governance behind**, so we are adding it and would rather build it with you
than beside you.

### Two smaller ones, where either answer works

- **Column prefixes** — §2. If you want them, we want the reason.
- **`platform.scope`** — we are taking your name. Confirm you are happy for the hierarchy to stay
  one table rather than five.

## 5 · One thing your workbook and ours disagree on, which neither of us would have found by comparing names

**Nine of the tables we accepted store `currency_code`.** Our checker failed all nine the moment
they landed, and it is right to: **ADR-0018 puts currency at region level** — *"currency and
decimal scale: OMR has three decimal places because Oman says so"* — so a currency resolves by
walking the scope tree rather than being stored on the row.

**Seven of the nine genuinely differ and we kept your column:**

| | why it stays |
|---|---|
| `payments.fee_rule`, `eligibility_rule`, `method_config` | the currency names **which** currency the rule applies to. That is a condition on the row, not a copy of the region's answer, and removing it would make the rule unconditional |
| `inventory.supplier_contract`, `orders.deposit` | an overseas supplier contracts in its own currency, and a deposit is money actually taken. Our `inventory.supplier` and `orders.payment` were already exempt for exactly this |
| `wallet.balance`, `wallet.hold` | a stored-value balance is denominated and a hold on it carries the same denomination |

**Two we changed.** `fnb.price_list` and `retail.price_list` now carry
`x-ticvai-persisted: false` on `currencyCode` — kept on the wire, removed from the table — which
is what our `catalogue.price_list` already does. A price list in a UAE region **is** AED and
cannot be anything else, so the column would hold millions of copies of one region-owned value
and would let a price list disagree with its own region.

**We mention it because it is the same shape as the payroll tables in §4.** A schema generated to
look like a schema puts a currency column on anything holding money, because that is what money
tables usually look like. **It cannot know that a region owns the answer here** — and that is not
a criticism, it is an argument for reading both workbooks against the decisions rather than
against each other.

## 6 · Corrections to things we told you earlier

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
