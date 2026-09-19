# Schema merge — the decision log

> **What this is.** The eleven open decisions from
> [schema-merge-decisions-20-september.md](schema-merge-decisions-20-september.md), answered one
> at a time with the evidence that decided each. **This is the input to the final report** — the
> response document and the shared doc are written from here, not from memory.

## The rubric

**This is not ours against theirs.** Where their shape is better we take it, where ours is better
we keep it, and where each has half of it we combine. Every decision below is scored on four
things and nothing else:

| | the question it asks |
|---|---|
| **Maintainability** | how many places a change has to be made, and how many ways to get it wrong |
| **Readability** | does the name tell a developer what the rows are, without the schema doc open |
| **Optimised access** | does the query a screen actually runs stay inside one schema, on narrow rows |
| **DB strain** | contention, row width, update churn, and what shares a hot table with what |

**The fourth one carries more weight than it looks.** It is the same argument that gave F&B and
Retail their own product and price tables: a flash sale on retail stock must not contend with
ticket inventory. Anything that puts a second workload on `catalogue` or `orders` is paying that
cost again.

| # | Decision | Call | Date |
|---|---|---|---|
| 1 | Rental domain | **keep `rental.*` and take their agreement** | 20 Sep |
| 2 | Payments domain | **keep `payments` for config**, fix our own split first | 20 Sep |
| 3 | Subscription domain | **consolidate into `subscription`**, decline `platform` | 20 Sep |
| 4 | `venue` schema | **their name, our table** — `platform.scope`; decline all five | 20 Sep |
| 5 | `pricing` schema | **take all three**, and give the schema an owner | 20 Sep |
| 6 | Payroll and HR scope | **closed on their own sources** — decline payroll, take HR as a projection | 20 Sep |
| 7 | Where a customer lives | **keep the three-way split** | 20 Sep |
| 8 | Loyalty: one rules table or four | **take theirs** — ours has three faults | 20 Sep |
| 9 | Membership hierarchy | **take it** | 20 Sep |
| 10 | Cross-cell guest link | **reversed — keep it in `platform`** | 20 Sep |
| 11 | The DSAR duplicate | **drop theirs** | 20 Sep |

---

## 1 · Rental domain — **keep the schema, take their agreement**

**Their proposal:** ten tables across `catalogue` (4), `resources` (5) and `maintenance` (1).
**Ours:** one `rental` schema, 21 tables.

**The answer is neither side whole.** The schema boundary is ours; one of their tables is a
record we do not have and should.

### Scored

| | verdict | why |
|---|---|---|
| **Maintainability** | **ours** | a rental change touches one schema. Theirs touches `catalogue`, `resources` and `maintenance` — and `rental_rate` in `catalogue` means a pricing change lands in the ticket team's schema |
| **Readability** | **ours** | `rental.inspection` against `resources.rental_inspection`. Their prefix exists *because* of the placement — the name is carrying the schema's job |
| **Optimised access** | **ours** | a checkout reads booking, agreement, items, inspection, participant and pricing together. In ours that is one schema. In theirs it joins across three |
| **DB strain** | **ours, decisively** | **`catalogue.rental_rate` puts rental pricing inside the hottest table set in the system.** That is the flash-sale contention argument that gave F&B and Retail their own price tables, reintroduced |

**The fourth line is their own principle used against their own layout**, and it is the one to
lead with — not "the cost falls on you". The cost asymmetry is real (187 change points against a
schema rename) but it is an argument about effort, not about what is better.

### What is genuinely better on their side — **take it**

**We hold `agreement_rules` and `agreement_signature`, and no agreement.**

    rental.agreement_rules        agreement_required, e_signature_required, agreement_version, …
    rental.agreement_signature    participant_id, agreement_version, signatory_name, signed_at, …
    rental.participant            name, date_of_birth, has_signed_waiver, …   ← no booking reference

**The signature references a participant and a version string.** It signs a version *number*, not
a document instance, and the participant it names is attached to nothing — `rental.participant`
carries no booking or agreement column at all. Their `resources.rental_agreement` is exactly the
record both of ours are reaching for.

**Scored, taking it wins on all four:**

- **Maintainability** — a signature that points at a real row cannot be orphaned. Today it can
- **Readability** — `rental.agreement` beside `agreement_rules` and `agreement_signature` finally
  reads as a set
- **Optimised access** — a booking list does not need handover and return columns. Splitting
  narrows the row the busy query scans
- **DB strain** — **this is the real gain.** `rental.booking` carries the reservation *and* the
  fulfilment, so every row is updated at least twice more after creation: once at checkout, once
  at return, again on late accrual. Wide rows updated repeatedly means row versions and bloat on
  the table that every availability check reads. Move the churn to the agreement and `booking`
  goes stable-after-insert

**So: `rental.booking` keeps the commercial reservation, `rental.agreement` carries the
operational contract.** That is the split our own two tables already implied.

**And their `rental_agreement_item` merges with our `rental.equipment_assignment`** — their
per-item status and quantity path for things that are not serialised, our `asset_id`,
`serial_number`, `scanned_code` and `returned_at`. One table doing both jobs.

### What else we move — ours, not theirs

**`rental.category` leaves `rental`.** It is the asset-category master for the whole venue:

    maintenance.asset.category_id                    -> rental.category
    maintenance.maintenance_plan.asset_category_id   -> rental.category
    maintenance.inspection_template.applies_to_…     -> rental.category
    resources.resource_category.parent_category_id   -> rental.category
    resources.resource_requirement.category_id       -> rental.category

**A forklift that is never rented has its category defined in `rental`.** On maintainability and
readability alone it belongs in `maintenance` or `resources`. Their split is what surfaced it.

### The counter-argument, stated fairly

Rental equipment genuinely is a maintenance asset — seven real edges, against 14 that stay inside
rental. The domains interpenetrate and anyone arguing the other way is not being unreasonable.
It loses on **optimised access** and **DB strain**, not on ownership.

### A defect found on the way — evidence for nobody

**Five of the twelve `rental → maintenance` edges are wrong.**

    rental.category.icon_asset_id                    -> maintenance.asset    an icon
    rental.product.image_asset_id                    -> maintenance.asset    an image
    rental.agreement_rules.terms_document_asset_id   -> maintenance.asset    a PDF
    rental.agreement_signature.signature_asset_id    -> maintenance.asset    a signature scan
    rental.agreement_signature.document_asset_id     -> maintenance.asset    a signature scan

All five belong to `assets.media_asset`. **`derive-relationships` saw `*_asset_id` and reached for
`maintenance.asset`**, inflating the coupling by 70%.

**Open:** the same rule will have done this wherever a `*_asset_id` column names media. Not swept.

### Correction to carry into the report

**We do have dynamic pricing, on one table.** `rental.pricing_profile` holds `dynamic_enabled`,
`dynamic_max_increase_percent` and `dynamic_max_decrease_percent`. Those are **bounds, not an
engine** — there are no rules, no conditions, no actions, and nothing at all for tickets, F&B or
retail. The claim "no dynamic pricing at all" is stated in the response document and the shared
doc and is **overstated**; it has to read "guardrails on one table and no rules engine" before
decision 5 is argued.

---

## Re-score — what the rubric overturned in the 185 already closed

**The rubric arrived after 185 rows were closed**, so every one of them was re-read against it.
Most were decided on what the rows actually *are*, which the rubric does not disturb — the 21
prefix-repeat declines, the purpose-line matches, the stub replacements. **Two classes were
decided on something the rubric does not count.**

### Class one — decided on change points

Effort is not quality. Six rows carried a cost figure in their reason; five of those were
arguments about how much work a rename is, which is a thing to plan around, not a thing to
decide on.

| table | was | now | why it moved |
|---|---|---|---|
| `ai.activity` | DECLINE, 57 points | **TAKE THEIRS** | their purpose says *"any AI request, including non-chat calls"*. An `interaction` reads as a conversation and most of these rows are not one |
| `venuemap.route` | DECLINE, "not worth it" | **EITHER** | a cost dodge. Their purpose is *"a connection between two points"* — an edge. `route` and `path` both oversell it and neither is better |
| `access.entry_rule` | DECLINE, 37 points | **EITHER** | a coin toss held hostage by our own undecided singular/plural rule. Settle the convention and this answers itself |
| `platform.scope` | DECLINE, 91 FKs | **DECIDE** | their name is better — `scope` is the word 58 of our config profiles address by, `org_unit` is generic ERP. It is the venue decision in a second place, so it moves **into** §4 rather than being settled on effort |

**Held:** `orders.order` — 223 points, but `sales_order` also distinguishes it from an F&B order,
a purchase order and a kitchen order, so it wins on readability with the cost removed.
`inventory.wastage` — the ledger-path argument is optimised access and maintainability, not cost.

### Class two — an array of ours against a join table of theirs

**This is the one worth knowing about, because the inconsistency was ours.**

We had already **accepted four** of their normalisations — `access.entry_rule_point`,
`fnb.menu_item_modifier`, `seating.seat_block_item`, `catalogue.plan_benefit` — each on the
grounds that we hold the relationship as an array and an array cannot carry per-row state. **Then
we declined two identical ones.**

| table | ours | why it flipped |
|---|---|---|
| `orders.payment_method_config` | `payments.method.currencies[]`, `channels[]`, `venue_ids[]` | **Access:** *"which methods are live at this venue, in AED, on web"* is an array containment scan, not an index lookup. **Strain:** enabling one method at one venue rewrites the whole row and every array on it. **Maintainability:** adding a venue to 40 methods is 40 row rewrites against 40 inserts |
| `platform.tier_module` | `subscription.module_listing.included_in_tiers[]` | *"which modules are in PRO"* scans every module row; the join table is one indexed read |

Both are now **TAKE THEIRS**. `payment_method_config` lands in `payments`, `tier_module` in
`subscription`.

### The larger thing this exposed — **open, not decided**

**140 of our 556 tables carry an array column that encodes a relationship.** Some are legitimate
value lists — `tags`, `allergens`, `blackout_dates`, `scopes`. Many are not:

    orders.order_line.seat_ids, entitlement_ids, cross_region_right_ids   18 ops, 49 screens
    access.entitlement.shared_with_subject_ids                            28 ops, 66 screens
    marketing.guest_profile.recent_order_ids, membership_ids              20 ops, 33 screens
    approvals.rule.approver_role_ids, escalate_to_role_ids                 6 ops, 34 screens
    access.admission_rules.allowed_access_point_ids                        7 ops, 18 screens
    whitelabel.tenant_config.enabled_payment_methods                      19 ops, 22 screens
    seating.seat.companion_seat_ids                                        5 ops, 26 screens

**Their workbook only happened to normalise six of them.** The rest are the same modelling
decision, unreviewed, and on this rubric most of them are wrong: an `_ids` array cannot be
joined, cannot carry per-row state, cannot be indexed for a membership test without a GIN index,
and is rewritten whole on every change.

**`access.admission_rules.allowed_access_point_ids` is the proof** — their `entry_rule_point` is
exactly that array as a table, and we accepted it. The same argument applies to the other 139 and
nobody has made it.

**This is a package-wide review, not a merge decision.** It does not block the eleven.

---

## 2 · Payments domain — **keep `payments` for configuration, and fix our own split first**

**The argument that carried §1 does not exist here.** `payments` and `orders` are **both
OrderService**. Nothing crosses a service boundary either way. Leading with the rental argument
would be noticed, and would cost us credibility on everything after it.

### Scored

| | verdict | why |
|---|---|---|
| **Maintainability** | **neither, today** | we hold payments in two schemas — **6 tables in `orders`, 16 in `payments`** — which is the worst of both |
| **Readability** | **ours** | `payments.method` against `orders.payment_method`; the prefix is doing the schema's job |
| **Optimised access** | **ours** | payment configuration is read on every checkout and changes monthly. It wants to be small, cacheable and apart |
| **DB strain** | **ours — lead with this** | `orders` is the highest-churn schema in the system. Config read constantly and written rarely should not share a schema with rows written on every sale; they compete for buffer cache, and every schema-wide operation treats them alike |

**The boundary that justifies it:** `payments.*` is configuration and policy — methods, providers,
routing, risk, terminals, merchant accounts. `orders.payment` is the **transaction**. That is why
`payments` has **zero inbound foreign keys**: nothing should depend on a config table.

### What we fix before asking them for anything

| table | cost | |
|---|---:|---|
| `orders.payment_provider` → `payments` | 12 | configuration on the wrong side of our own boundary |
| `orders.payment_token` → `payments` | 6 | same |
| `orders.payment_routing` → **collapse into `payments.routing_rule`** | 6 | **a real duplicate** — both are "priority plus conditions decide which provider" |

**Their single `orders.payment_route` maps onto both of ours.** They see one thing where we have
two, and they are right.

**`orders.payment` stays** — 12 inbound foreign keys, 63 screens, and it is the transaction, which
is the boundary we are arguing for.

**Taken from them:** `payment_method_config` (the array flip), plus `payment_fee_rule`,
`payment_eligibility_rule`, `currency_rule` and `deposit_activity` as additive — all into
`payments`, not `orders`.

## 3 · Subscription domain — **consolidate into `subscription`, decline `platform`**

`control` and `subscription` are **both PlatformService**. `platform` is **TenancyService**.

### Scored

| | verdict | why |
|---|---|---|
| **Maintainability** | **a third option** | ours is split across `control.subscription`, `control.subscription_plan` and a nine-table `subscription` schema. Theirs moves it into `platform` |
| **Readability** | **against `control`** | **`control` holds 51 tables** — cells, migrations, releases, webhooks, invoices, and a subscription. It is a junk drawer and the name tells a developer nothing |
| **Optimised access** | **against theirs** | their placement puts billing in TenancyService and licensing in PlatformService. **A plan lookup becomes a cross-service call** |
| **DB strain** | tie | low-volume configuration either way |

**Call: move `control.subscription` and `control.subscription_plan` into `subscription`.** 86
change points, all ours, and it is the only option that puts one domain in one schema in one
service. Decline `platform.tenant_subscription` and `platform.subscription_tier` on the
cross-service split.

**Taken:** `tier_allowance` — a real gap, since what a tier *includes* is currently one column,
`subscription_plan.included_ai_tokens` — and `tier_module`, the array flip.

## 4 · The `venue` schema — **take their name, keep our table, take `department`**

The rubric changed this one most, because the old answer was "91 foreign keys" — which is effort,
and effort does not count.

### Scored

| | verdict | why |
|---|---|---|
| **Maintainability** | **ours** | `platform.org_unit` is **one self-referencing hierarchy** — `level`, `parent_id`, `path`, `child_count`. Their five typed tables flatten it, so **adding a level becomes a new table** rather than a row |
| **Readability** | **theirs** | `scope` is the word **58 of our configuration profiles already address by** (`scope_path`). `org_unit` is generic ERP vocabulary that appears nowhere else in our language |
| **Optimised access** | tie | same rows, same indexes, same queries |
| **DB strain** | tie | a rename moves nothing |

**Call: combine.** Keep the single-table hierarchy — that is the better model and it is not close.
**Take their name for it**: `platform.scope`, which is what every `scope_path` in the package has
been calling it all along. Decline `venue.venue`, `outlet`, `space` and `zone`, because each is a
level of the hierarchy we already hold as a row.

**Decline all five, including `department`.** *(Corrected — we had `department` down as a gap and
as a dangling reference. It is neither.)* `ScopeLevel` in `contracts/shared/common.yaml`
enumerates **tenant, brand, region, venue, department, subDepartment, workstation, outlet,
subject**, and **ADR-0011 makes the hierarchy binding**. `platform.org_unit` holds a department as
a row with `level: department`, and `platform.workstation.department_id` points at it. **Their
five tables are five of our nine levels flattened into tables** — which is the argument of this
whole decision, applied to the one table we had conceded.

## 5 · The `pricing` schema — **take it, and give it an owner**

`pricing.dynamic_price_rule`, `_condition`, `_action`.

**Correction carried from §1:** we do hold dynamic pricing — three guardrail columns on
`rental.pricing_profile`. **A ceiling and a floor with no engine under them**, and nothing at all
on `catalogue.price`, `games.pricing`, F&B or retail.

### Scored

| | verdict | why |
|---|---|---|
| **Maintainability** | **theirs** | a rule, its conditions and its actions as rows. Ours is three columns on one table, so a second pricing behaviour is a schema change |
| **Readability** | **theirs** | `pricing.dynamic_price_rule` says what it is. `rental.pricing_profile.dynamic_max_increase_percent` does not |
| **Optimised access** | **theirs** | rules are read-mostly and cacheable. Inside `catalogue` they would be read on every add-to-cart alongside ticket inventory |
| **DB strain** | **theirs** | the F&B and Retail argument again: an engine pricing tickets, F&B, retail and rental cannot live in `catalogue` |

**Call: take all three.** **`pricing` currently has no service owner** — assign it to
CatalogueService, which already owns `price`, `price_list` and `promotions`. Leaving a schema
unowned is how the last fifty unowned tables happened.

## 6 · Payroll and HR — superseded, see the closed entry at the end of this file

Unchanged: seven payroll tables with **no requirement behind them**, and seven HR master tables
already accepted *conditionally* on the answer.

**What the rubric adds:** `workforce` is **TenancyService**. Payroll is a finance function, and
putting payslips and salary components inside the service that manages tenants and staff rostering
is wrong on maintainability whatever the scope answer turns out to be. **If the answer is yes,
payroll wants its own schema and its own owner** — not thirteen more tables in `workforce`.

## 7 · Where a customer lives — **keep ours; the strongest position in the file**

### Scored

| | verdict | why |
|---|---|---|
| **Maintainability** | **ours** | a subject-access export and a deletion request walk one subtree. Collapsed into `identity.customer` they walk everything |
| **Readability** | **ours** | `identity.principal` is who can authenticate, `marketing.guest_profile` is who the guest is, `pii.subject` is the regulated data. Each name states its own governance |
| **Optimised access** | **ours** | a marketing segment query never touches PII; an authentication check never touches marketing |
| **DB strain** | **ours, decisively** | **`identity.principal` carries 134 inbound foreign keys — the most connected table in the package.** Their proposal adds every guest row to the table every authentication already reads |

**Call: keep the three-way split.** If they have a DSAR design that works against a single
`identity.customer` we want to see it — but the 134-foreign-key figure is what to put in front of
them first.

## 8 · Loyalty — **take their split, and correct ourselves while doing it**

**We said `marketing.loyalty_programme` holds the rules of earning and burning. It does not.**

    marketing.loyalty_programme   code, name, venue_id, points_liability_account_id,
                                  points_expire_after_months, is_active        <- a header
    marketing.loyalty_tier        trigger, points, product_kinds[], multiplier <- the rules
                                  0 operations · 0 screens · 0 foreign keys    <- unwired
    marketing.loyalty_position    ..., tier_code, tier_name                    <- tiers as strings

**Three faults in one domain.** The programme is a header with no rules on it. The only rules
table is **misnamed** — `loyalty_tier` holds earning triggers and multipliers, not tiers — and is
**referenced by nothing at all**. And the tier a guest is in is two denormalised strings on their
balance row, because there is no tier table.

### Scored

| | verdict |
|---|---|
| **Maintainability** | **theirs** — a new earning rule is an insert. Ours is a `product_kinds[]` array on an unused table |
| **Readability** | **theirs** — `points_earning_rule` and `points_redemption_rule` say what they hold. `loyalty_tier` actively misleads |
| **Optimised access** | **theirs** — earning rules are read on every transaction, redemption rules only on redeem. One table for both is read more often than it needs to be |
| **DB strain** | theirs, marginally |

**Call: take `points_earning_rule`, `points_redemption_rule` and `loyalty_rule`.** Retire
`marketing.loyalty_tier` or rename it to what it is, and add a real tier table so
`loyalty_position.tier_code` points at something. **`marketing.loyalty_points`, the ledger, was
already accepted and remains the most serious gap here** — a balance with no history behind it.

## 9 · The membership hierarchy — **take it; the array argument in its purest form**

They hold `membership_program` → `membership_plan` → `membership_benefit`, joined by
`plan_benefit`. We hold one table, `catalogue.entitlement_template`, **with the benefits as
columns**: `fast_track_tier`, `can_claim_shop_and_drop`, `included_value`.

### Scored

| | verdict | why |
|---|---|---|
| **Maintainability** | **theirs** | **a new benefit is currently a schema change** |
| **Readability** | **theirs** | three levels named for what they are, against one 34-column table doing all three jobs |
| **Optimised access** | **theirs** | "which plans include fast track" is a column scan today |
| **DB strain** | **theirs** | `entitlement_template` is read by 15 operations and 34 screens, and every one of them reads 34 columns to get three |

**Call: take `membership_benefit` and `plan_benefit`, and `membership_program` as the level above.**
`membership_plan` stays as our `entitlement_template` — already resolved — plus their renewal rules.

## 10 · Cross-cell guest linking — **reversed: keep it in `platform`**

**The earlier recommendation was to move `platform.guest_link` into `sync`.** On the rubric that is
wrong.

    platform.dsar_request.guest_link_id  ->  platform.guest_link

Both are **TenancyService**. `sync` is **CrossRegionService**. Moving the link alone puts a DSAR
fan-out — which walks `guest_link` to find every cell holding a guest — **across a service boundary
on its hottest path**. On optimised access and maintainability that is worse, and readability is
the only thing it buys.

**Call: decline the move.** Either both tables go to `sync` or neither does, and a DSAR is a
tenancy obligation rather than a synchronisation mechanism. Neither goes. `sync` keeps cell
plumbing — `cell_connection`, `cross_cell_request`, `rejection` — which is what it says.

## 11 · The DSAR duplicate — **drop theirs**

`marketing.data_subject_request` against our `platform.dsar_request`.

**A subject-access request spans every service.** Ours sits in TenancyService and walks
`guest_link`; theirs would sit in **MarketingService**, which owns one of the dozen schemas a DSAR
has to reach. On maintainability and optimised access that is not close.

**Call: drop theirs.** If it carries state ours lacks, take the body.

---

## 6 · Payroll and HR — **closed on their own sources, not by asking**

**We had this down as a client question. It did not need to be one.** The answer is in the
client's own reference pack and in the requirement matrix, and citing those rather than arguing
preference is what makes the decline stick.

### What their pack says

`Resource_Management_Configuration_Reference.pdf`, **Board 3, page 45 — "Workforce Integration &
Synchronization Center"**:

> **Purpose.** Connect TICVAI Resource Management with **external** HR, workforce management,
> **payroll**, identity, and employee systems where applicable.
>
> **Integration Sources.** HRMS · Workforce Management · **Payroll** · Time & Attendance ·
> Identity Management · External staffing agencies
>
> **External System Master.** *"This prevents conflicting updates."*
>
> **Conflict handling.** *"Employee exists in HR but not TICVAI."* · *"Employee terminated
> externally but has future TICVAI assignments."*

**Board 10** lists Payroll again — as an integration to **monitor**, with sync status, failed
records and latency beside HRMS.

### What the matrix says

**Zero rows mention payroll, payslip, salary, wage, HRMS or HR system.** Not one, across all five
sheets. What it requires at the rows Board 4 itself cites:

| | |
|---|---|
| 1.2.32–33 | staff scheduling, assignment, shifts |
| **1.2.37** | *"System shall **integrate** approved leave requests"* — integrate, not manage |
| 1.2.80–81 | shift swaps, check-in and check-out, lateness, no-shows, overtime hours |
| 1.2.83 | validate against working-hour limits, breaks, **certifications**, rest periods, union rules |
| **1.2.84** | *"calculate **labor costs**, staffing budgets, overtime costs… by venue, department, attraction"* |

**1.2.84 is labour costing, not payroll.** Costing a roster is not paying anybody, and it is the
closest the matrix comes.

### The call

| | |
|---|---|
| **the seven payroll tables** | **decline.** `payroll_run`, `payroll_employee`, `payroll_line`, `payslip`, `salary`, `salary_component`, `pay_component`. No requirement, and their own pack names payroll as an external system to integrate with and monitor |
| **the seven HR tables** | **take — as an externally mastered projection, not an HR master.** 1.2.83 needs certifications and job roles, 1.2.84 needs a cost rate per employee, and Board 3's eligibility engine evaluates leave. The rows live here; the system of record does not |

### The gap this exposes, which is in neither workbook

**Board 3 requires a field-ownership model** — *"for every field, administrators shall
determine"* which system is master, because that is what *"prevents conflicting updates"*. Board
10 specifies a six-state integration monitor: connected systems, last synchronisation, successful
records, failed records, warnings, mapping errors, authentication status.

**We hold none of it. Neither do they.** Taking their employee tables without it takes the data
and leaves the governance behind — and their own conflict cases, *"employee terminated externally
but has future TICVAI assignments"*, are exactly what goes wrong without it.

### A note on where their seven payroll tables came from

`payroll_run` → `payroll_employee` → `payroll_line` → `payslip`, with `salary`,
`salary_component` and `pay_component` beside them, **is a standard payroll schema completed to
its usual shape.** It is what you get when a model is asked to finish a `workforce` schema rather
than to satisfy a requirement. **That is worth saying plainly and without accusation**, because it
also means the reverse may be true elsewhere in the workbook: a generated schema fills in what is
conventional and omits what is specific — which is consistent with the field-ownership and sync
layer above being missing from both sides, since nothing conventional would have supplied it.

**It is also the reason to cite their sources rather than our judgement.** A decline backed by
their own Board 3 and by an empty search of the matrix is checkable. A decline backed by "we did
not think it was in scope" is not.
