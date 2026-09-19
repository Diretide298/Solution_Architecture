# Schema merge — everything that needs a decision

> **20 September 2026.** 151 of their 223 unmatched tables are answered; 46 of those answers
> are "somebody has to choose". Row-level detail in
> `handoff/TICVAI_Schema_Merge_Tasks.xlsx`, verdicts in `handoff/merge-verdicts.json`.
>
> **The 46 rows collapse into 14 decisions.** Most of them are one choice covering several
> tables.

---

## 1 · The rental domain — 4 tables · **biggest item in the file**

**Both teams built rental in the same week, in different schemas.**

| | |
|---|---|
| ours | `rental.*` — **21 tables**, its own schema, authored 19 September |
| theirs | `catalogue.rental_rate`, `rental_requirement`, `rental_rule`, `rental_product_config`; `resources.rental_agreement`, `rental_agreement_item`, `rental_inspection`, `rental_inspection_item`, `rental_product_mapping`; `maintenance.rental_damage_assessment` — **10 tables spread across four schemas** |

Their own names give it away: every one carries a `rental_` prefix **because it is sitting in
somebody else's schema**. `maintenance.rental_damage_assessment` is our
`rental.damage_assessment`; `resources.rental_inspection` is our `rental.inspection`.

**Recommend: our schema.** It is the same principle they already accepted when they moved
`branding` → `whitelabel`, and the prefix on every one of their ten names is the argument for it.

**The cost is theirs, not ours** — ten tables move schema on their side; nothing moves on ours.

## 2 · The payments domain — 5 tables

Same shape. Ours is `payments.*`, **16 tables**. Theirs is `orders.payment_method`,
`payment_gateway`, `payment_policy`, `payment_route`, `payment_terminal` — five tables carrying a
`payment_` prefix inside `orders`.

`orders.payment_method` is our `payments.method`. `orders.payment_terminal` is our
`payments.terminal`. **Recommend: our schema, same argument.**

## 3 · The subscription domain — 1 table, and we have two homes for it

`platform.tenant_subscription` is our `control.subscription`. **But we also hold a whole
`subscription` schema** — `licensing_model`, `enforcement_policy`, `capacity_pack`,
`vsi_assessment` and five more.

**Decide our own side first:** `control.subscription` and `subscription.*` are two homes for one
domain, and that is our inconsistency rather than theirs.

## 4 · A `venue` schema — 5 tables · **an open blocker**

They propose `venue.venue`, `venue.department`, `venue.outlet`, `venue.space`, `venue.zone`.

We hold **`platform.org_unit` as the venue** (77 inbound references), plus `platform.outlet`
(22 FKs), `catalogue.space`, `seating.zone`. We have no `department`.

| option | consequence |
|---|---|
| **keep ours** | `outlet` has 22 inbound FKs and `org_unit` 77 — the two most connected tables in the package. Moving them is the most expensive change available |
| adopt `venue` | a cleaner domain boundary, and `venue.department` is a table we genuinely lack |
| split | take `venue.department` as additive, decline the other four |

**Recommend: the split.** The cost is all in `outlet` and `org_unit`, and `department` is free.

## 5 · A `pricing` schema — 3 tables

`pricing.dynamic_price_rule`, `_condition`, `_action`.

We hold `catalogue.price`, `catalogue.price_list`, `rental.pricing_profile`, `games.pricing` —
**and no dynamic pricing engine at all.** These three are a genuine gap, not a rename.

**The decision is where they land**, not whether: a new `pricing` schema, or inside `catalogue`
beside `price_list`. **Recommend: their schema** — a rules engine that prices tickets, F&B, retail
and rental cannot sit inside `catalogue` once F&B and Retail stand alone.

## 6 · Payroll and HR — 7 + 6 tables · **flagged 18 September, still unanswered**

**Their `workforce` is a full HR system. Ours is rostering.**

| theirs, that we lack | |
|---|---|
| payroll (7) | `payroll_run`, `payroll_employee`, `payroll_line`, `payslip`, `salary`, `salary_component`, `pay_component` |
| HR master (6) | `employee`, `employment`, `job_title`, `leave_type`, `leave_balance`, `work_assignment` |

Ours: `rota_assignment`, `shift_template`, `open_shift`, `shift_swap`, `attendance`,
`leave_request`, `staffing_rules`, `training_record`, `announcement`.

**The 18 September note says there is no requirement behind the payroll tables.** That is the
question: **are we building HR and payroll, or rostering against an external HR system?** Six
more tables and a contract follow from the answer, and nothing else in this list is as large.

**Recommend: ask the client before answering them.** It is a scope question, not a schema one.

## 7 · Where a customer lives — 5 tables

Theirs puts customer, family and login in `identity`. Ours splits three ways:

    identity.principal        who can authenticate      staff, partner, device, service
    marketing.guest_profile   who the guest is
    pii.subject + _contact    the personal data itself   separately governed

Their `identity.customer` is our `guest_profile` + `pii.subject`; `identity.customer_address` and
`_contact` are `pii.subject_contact`; `identity.family` and `_member` are
`marketing.guest_relationship`.

**Recommend: keep ours and say why.** The split exists so a subject-access export and a deletion
request are answerable — ADR-0023. Collapsing personal data back into `identity` undoes that.

## 8 · Loyalty — one table or four

They split `points_earning_rule`, `points_redemption_rule`, `loyalty_rule`, `reward`. Our
`marketing.loyalty_programme` holds all of it; its own description is *"the rules of earning and
burning"*.

**Separately, we have a real gap**: `marketing.loyalty_points`, the points ledger. We hold
`loyalty_position` — a balance — **and no transaction history behind it.** A balance with no
ledger cannot be audited or corrected.

**Recommend: take the ledger regardless; decide the rule split on its own.**

## 9 · Cross-cell guest linking — 1 table

`sync.guest_link` against our `platform.guest_link` (5 FKs). Theirs is arguably better placed —
it **is** a cross-cell concern, and we already own a `sync` schema for exactly that.

**Recommend: move ours to `sync`.** Small, and it makes the schema mean what it says.

## 10 · `data_subject_request` is in two places — 1 table

`marketing.data_subject_request` duplicates our `platform.dsar_request`. **Flagged 18 September,
still true.** One of the two has to go, and the platform one is the one the DSAR fan-out uses.

## 11 · Module enablement — 1 table

`identity.enabled_module` against our `whitelabel.module_enablement`. **Ours is arguably wrong**:
which modules a tenant has bought is a licensing fact, not a white-label branding one, and we hold
`subscription.module_listing` as well. **Three homes for one idea on our side.**

## 12 · Two matches to correct — 2 tables

| | matched | actually |
|---|---|---|
| `wallet.account` | `ledger.account` | **our `wallet.wallet`** — a stored-value master, not a chart of accounts |
| `whitelabel.menu_item` | `fnb.menu_item` | **our `whitelabel.navigation_item`** — a nav menu, not food |

Both were bare-name matches. No decision needed, only the correction.

## 13 · Four that needed their own check — resolved

| theirs | ours | verdict |
|---|---|---|
| `catalogue.product_recommendation` | `promotions.upsell_rule`, `recommendation_strategy` | **ours, different schema** — placement |
| `catalogue.upgrade_rule` | nothing (`control.upgrade_schedule` is platform releases) | **additive** |
| `control.channel` | `control.channel_listing`, `catalogue.channel_allocation` | **additive** — we have listings and no channel master |
| `control.channel_item` | `control.channel_listing` | probably ours |

## 14 · Naming, ours and theirs — 4 tables and one convention

`platform.cash_denomination` · `platform.region_setting` · `whitelabel.brand_version` ·
`ai.knowledge_group` — each is a coin-toss worth conceding.

**But settle our own convention first.** We hold `approvals.sla_policy` singular,
`access.admission_rules` plural, `platform.region_settings` plural, `seating.recommendation_rules`
plural. **We have no rule**, and we cannot argue theirs until we have ours.

---

## The one position that is not on this list

**Column prefixes.** They prefix every column with its table name — `code` becomes
`access_point_code`, `id` becomes `<table>_id` on 193 tables. **645 of their 743 changes are that
one habit.**

It needs stating once, and it is not a per-table decision. The same answer also disposes of 21
table renames already marked DECLINE, where the table name repeats its schema.

## What is not yet looked at

**72 rows** — 44 `rename-ambiguous`, 11 `additive-declared`, 17 stragglers. The ambiguous ones
each have two or more candidates and need the purpose read against them; none is structural.
