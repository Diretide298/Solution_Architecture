# Schema merge — our response to `TICVAI_16_Services_AND_Tables_UPDATED`

> **To:** the backend team · **From:** design · **20 September 2026**
>
> Read against your workbook's 323 tables and our 556. Row-level detail in
> `handoff/TICVAI_Schema_Merge_Tasks.xlsx`; the reasoning behind every verdict in
> `handoff/merge-verdicts.json`.

---

## Where we are

100 of your tables carry a name we already use. **223 do not**, and those are what this
document is about. We have been through **151 of them one at a time**, read against the
`Purpose:` line you put above each table — that line settled more cases than the Change Log did,
and we would ask you to keep writing it.

| | tables | |
|---|---:|---|
| **we accept** | 63 | your table, your name, or your columns |
| **we decline** | 46 | same table, we keep ours — mostly your redundant prefix |
| **needs a choice** | 42 | nobody can settle these alone; §4 and §6 |
| not yet reviewed | 72 | ambiguous matches on our side, in progress |

**Nothing here is a rejection of the workbook.** Two teams built the same system in the same
weeks, and the overlap is evidence that both readings of the requirement were sound.

---

## 1 · What we accept — 63 tables

### F&B and Retail carrying their own product and price tables — 15

You gave `fnb` and `retail` their own `product`, `product_category`, `variant`, `price` and
`price_list` rather than pointing them at `catalogue`. **We had reached the same conclusion
independently**, and for a reason worth writing down so it does not get undone later: a flash
sale on retail stock and a Friday-night F&B service must not contend on the same rows as ticket
inventory. Catalogue keeps tickets. **Agreed as designed — no discussion needed on these.**

### Gaps in ours that you found — 30

These are ours to fix, not preferences to argue:

| yours | what we had | |
|---|---|---|
| `marketing.loyalty_points` | `loyalty_position` — a balance | **a defect.** A balance with no ledger behind it cannot be audited or corrected |
| `identity.customer_membership`, `membership_history`, `benefit_usage` | `entitlement_template` only | we modelled the membership and never the holder |
| `marketing.waiver_signature` | `form_submission` | ours does not pin the waiver version a guest actually signed |
| `wallet.hold` | authorise, then settle | we authorise wallet money and never record the hold |
| `access.entry_rule_point` | implied | the join between admission rules and access point, which we imply and never store |
| `sync.cell_connection`, `cross_cell_request` | `sync.rejection` | we record refusals and not the requests |
| `inventory.supplier_contract` | — | purchasing terms with a supplier |
| `orders.deposit`, `membership_renewal` | — | |
| `whitelabel.redirect`, `seo_setting` | — | |
| `marketing.campaign_target`, `customer_badge`, `review_response`, `reward`, `reward_assignment`, `journey_step`, `loyalty_campaign` | partial | |
| `workforce.employee`, `employment`, `job_title`, `leave_type`, `leave_balance`, `work_assignment` | rostering only | **conditional — see §4 ①** |
| `identity.module`, `identity.permission` | contract files | ours live in `contracts/shared/permissions.yaml`, not in tables. Yours is the better answer if permissions are ever tenant-editable |

### Four of your names we prefer to ours

`fnb.dining_table` · `orders.pos_shift` · `maintenance.preventive_plan` ·
`marketing.journey_enrollment`

Each disambiguates something ours left vague — `fnb.table` sitting next to a reservation table,
`shift` next to `workforce.shift`. **`pos_shift` is worth calling out**: your Change Log records
it as an internal rename of `till_shift`, a name we never had, so it first read as your own
churn. It is in fact our `orders.shift`. Both readings were true at once.

### Two where we keep our name and take your columns

`approvals.approval_escalation` and `identity.otp` are two-column stubs on our side. Yours are
complete.

### Three coin-tosses we concede

`platform.cash_denomination` · `platform.region_setting` · `whitelabel.brand_version`

---

## 2 · The one position that answers 645 of your 743 change rows

**Column prefixes.** You prefix every column with its table name — `code` becomes
`access_point_code`, `id` becomes `<table>_id` on 193 tables. **We do not**, because
`access.access_point.code` is already unambiguous inside its own row.

This is one decision, not 645. Taken once, it also disposes of **21 of the table renames** we
decline, where the table name repeats its own schema —
`approvals.approval_matrix` → `approvals.matrix`, `inventory.stock_movement` →
`inventory.movement`, `reporting.report_schedule` → `reporting.schedule`.

**If you want the prefix, say so and say why.** There is a real argument for it if your ORM or
reporting layer flattens joins into a single namespace, and we would rather hear that argument
than assume there isn't one.

---

## 3 · What breaks the approach — three domains built twice

This is the expensive part of the file and it is **not a naming argument**. Three domains exist
on both sides, in different schemas, authored within the same week.

| domain | ours | yours |
|---|---|---|
| **rental** | `rental.*` — 21 tables, own schema | 10 tables across `catalogue`, `resources`, `maintenance` |
| **payments** | `payments.*` — 16 tables, own schema | 5 inside `orders`, plus 6 further payment tables |
| **subscription** | `control.subscription` plus a `subscription` schema | `platform.tenant_subscription` plus 3 tier tables |

The collisions are exact, which is why this cannot be deferred:

    maintenance.rental_damage_assessment   =  rental.damage_assessment
    resources.rental_inspection            =  rental.inspection
    orders.payment_method                  =  payments.method
    orders.payment_terminal                =  payments.terminal

**Your own naming is our argument.** Every one of those ten rental tables carries a `rental_`
prefix and every payment table a `payment_` prefix — *because each is sitting inside somebody
else's schema*. A table that has to announce its domain in its own name is telling you it wants
its own schema. It is the same principle you already applied when you moved `branding` →
`whitelabel`.

**We propose our placement, and the burden is on us to show the cost. §6 does that.**

### The fourth one, which we are not going to win and are not asking to

You propose a `venue` schema: `venue.venue`, `department`, `outlet`, `space`, `zone`. **It is the
better boundary and we are still going to decline it**, because `platform.org_unit` carries
**91 declared foreign keys** and `platform.outlet` 16 — the two most connected tables in the
package. Moving them is the single most expensive change available in this merge, and it buys a
tidier name.

**Counter-proposal: we take `venue.department`, which we genuinely lack, and leave the rest.**

---

## 4 · What needs clarification — questions we cannot answer from the workbook

**① Payroll — is it in scope at all?**
Your `workforce` is a full HR and payroll system; ours is rostering. Seven payroll tables
(`payroll_run`, `payroll_employee`, `payroll_line`, `payslip`, `salary`, `salary_component`,
`pay_component`) have **no requirement behind them in anything we hold**, and the six HR master
tables we accepted in §1 depend on the answer. *Are we building payroll, or rostering against an
external HR system?* Thirteen tables and a service contract follow from it. **This is the largest
open item in the file.**

**② Where a customer lives.** You put customer, address, contact and family in `identity`. We
split three ways on purpose:

    identity.principal        who can authenticate        staff, partner, device, service
    marketing.guest_profile   who the guest is
    pii.subject + _contact    the personal data itself    separately governed, 47 inbound FKs

The split exists so a subject-access export and a deletion request are answerable by walking one
subtree (ADR-0023). Collapsing it back into `identity` undoes that. **If you have a DSAR design
that works against a single `identity.customer`, we want to see it** — otherwise we ask you to
take our split.

**③ Loyalty — one rules table or four?** You split `points_earning_rule`,
`points_redemption_rule`, `loyalty_rule` and `reward`. Our `marketing.loyalty_programme` holds
all of it; its own description is "the rules of earning and burning". **Either shape works. We
need one.** The points ledger from §1 we take regardless of how this lands.

**④ Module enablement has three homes and two of them are ours.** Your
`identity.enabled_module`, our `whitelabel.module_enablement`, our `subscription.module_listing`.
Ours is arguably the wrong one — which modules a tenant has bought is a licensing fact, not a
white-label branding one. **We will collapse ours; tell us if yours should be the survivor.**

**⑤ A sales-channel master.** Your `control.channel` and `control.channel_item` have no
counterpart in ours — we hold `control.channel_listing` and `catalogue.channel_allocation`, that
is, listings with no channel behind them. **This looks like a real gap on our side. Confirm the
intent and we will take both.**

**⑥ Singular or plural — and this one is ours to fix first.** We hold `approvals.sla_policy`
singular, `access.admission_rules` plural, `platform.region_settings` plural,
`seating.recommendation_rules` plural. **We have no rule, so we cannot argue yours.** We will
publish one before the next pass and apply it to ourselves first.

**⑦ Two matches we had wrong, corrected here so they do not propagate:**

| yours | we first matched | actually |
|---|---|---|
| `wallet.account` | `ledger.account` | **`wallet.wallet`** — a stored-value master, not a chart of accounts |
| `whitelabel.menu_item` | `fnb.menu_item` | **`whitelabel.navigation_item`** — a navigation menu, not food |

**⑧ `marketing.data_subject_request` duplicates our `platform.dsar_request`.** One of the two
has to go. The platform one is what the DSAR fan-out walks, so we propose dropping yours — but
if yours carries state ours lacks, say so and we will take the body.

---

## 5 · Pros and cons of the three ways to settle this

| | pros | cons |
|---|---|---|
| **A · we adopt your schema wholesale** | one migration, on our side only; your DDL ships unchanged; no negotiation at all | costs us roughly 940 change points (§6); loses the PII split and the F&B/catalogue isolation; we would be re-arguing both within a month |
| **B · you adopt ours wholesale** | our contracts, screens and lineage stay valid; the F&B isolation and the DSAR split survive | your 28 new tables move schema; ignores that four of your names and 30 of your tables are genuinely better than ours |
| **C · domain by domain — what this document proposes** | each domain settled on cost and on who has the stronger argument; both sides concede in writing | slowest; needs the §4 answers before it can finish; two working sessions, not one email |

**We propose C**, and §1 is our half of it paid up front: 63 tables accepted, four of your names
taken over ours, two of our stubs replaced by your columns, and one real defect in our loyalty
model that your workbook is the reason we found.

---

## 6 · Scope compromise costing

Cost is `operations + 2 × inbound foreign keys + screens`. A foreign key counts double because it
is a constraint in generated DDL as well as a reference to repoint. The figures are from the
package's own relationship graph, not estimates.

### If we move our domains into your schemas

| domain | our tables | inbound FKs | operations | screens | **cost** |
|---|---:|---:|---:|---:|---:|
| rental → `catalogue`/`resources`/`maintenance` | 21 | 27 | 34 | 99 | **187** |
| payments → `orders` | 16 | 4 | 25 | 45 | **78** |
| subscription → `platform` | 9 | 0 | 14 | 61 | **75** |
| `platform.org_unit` + `outlet` → `venue` | 2 | 107 | 27 | 57 | **298** |
| accreditation → `access` | 13 | 14 | 26 | 60 | **114** |
| wallet → `retail`, reversing 19 September | 23 | 18 | 45 | 110 | **191** |
| | | | | | **943** |

### If you move your tables into ours

| domain | your tables | what changes |
|---|---:|---|
| rental | 10 | the schema name — the table names already read `rental_*` |
| payments | 11 | the schema name — already `payment_*` |
| subscription | 4 | the schema name |
| accreditation | 4 | the schema name — already `accreditation_*` |
| | **29** | **no foreign key repointed, no operation changed, no screen changed** |

**That asymmetry is the whole argument.** Your tables carry their domain in their own names, so
moving them is a schema rename and nothing else. Ours carry 170 inbound foreign keys, 171
operation references and 432 screen references between them, every one of which we would have to
rewrite to arrive at the same place.

### What we put on the table against it

| we concede | what it costs us |
|---|---|
| your `pricing` schema for the dynamic-pricing engine | 3 tables and none of ours move — **we have no dynamic pricing at all**, so this is a gap you closed |
| `venue.department` | additive |
| the 63 tables in §1, including 15 we had already built your way | our workbook grows; nothing of ours breaks |
| four of your table names over ours | 4 renames, two of them with no references at all |
| our own three homes for module enablement, and our singular/plural inconsistency | ours to fix either way, and we are fixing them |

**Net:** we ask you to rename four schemas across 29 tables. We take 63 tables, four names, one
new schema and two corrections of our own — and we absorb the ~940-point cost of *not* moving
`org_unit` into `venue`, which is the largest single compromise in this merge and appears in no
column of either sheet.

---

## 7 · Still open on our side

**72 of the 223 are not yet reviewed** — 44 where your table matches two or more of ours and a
matcher cannot choose between them, 11 additive, 17 stragglers. **None of them is structural**;
each needs your `Purpose:` line read against our candidates, which is a day of work and not a
negotiation.

We will send those, our naming convention, and the module-enablement collapse in the next pass.
**The eight questions in §4 are what we need back from you.**
