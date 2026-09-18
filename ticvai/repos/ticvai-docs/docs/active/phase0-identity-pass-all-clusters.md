# Phase 0 — identity pass, all clusters

> **18 September 2026.** Which of their tables are actually new, read cluster by cluster.
> Continues [phase0-orders-cluster.md](phase0-orders-cluster.md), which covered orders only.

---

## The count, three passes deep

| pass | method | "new" |
|---|---|---|
| 1 | no name match in ours | **165** |
| 2 | minus those whose name does exist | **138** |
| 3 | minus renames, read by a person | **~110** |

**Fourteen tables were renames of tables we already have.** Creating them would have produced
fourteen duplicate pairs holding the same rows, and **no check in the package would have caught it** —
a table nothing references is not an error.

### The fourteen

| theirs | ours | note |
|---|---|---|
| `orders.order` | `orders.sales_order` | keep ours — `ORDER` is a reserved word |
| `orders.pos_shift` | `orders.shift` | take theirs |
| `orders.payment_gateway` | `orders.payment_provider` | take theirs — industry term |
| `orders.payment_route` | `orders.payment_routing` | take theirs — a row is one route |
| `orders.discount` | `orders.order_discount` | **take theirs wholesale, ours is a stub** |
| `catalogue.product_variant` | `catalogue.variant` | keep ours — pairs with `variant_dimension` |
| `marketing.journey_enrollment` | `marketing.journey_entrant` | take theirs |
| `reporting.report_execution` | `reporting.execution` | take theirs — their change log declares it |
| `reporting.report_input` | `reporting.report_parameter` | keep ours — "parameter" is the domain word |
| `whitelabel.brand_version` | `whitelabel.config_version` | either |
| `ai.usage_policy` | `ai.policy` | keep ours — 28 columns against their 17 |
| `approvals.approval_request` | `approvals.request` | merge, both rich |
| `approvals.approval_rule` | `approvals.rule` | merge, ours richer |
| `approvals.approval_escalation` | `approvals.escalation` | **take theirs wholesale, ours is a stub** |

**The approvals trio is their table-name prefix convention**, which the change log recorded for
columns and not for tables. Any future cluster should expect the same.

### Two of our tables are stubs and theirs are real

`orders.order_discount` holds `id` and `order_id`. `approvals.escalation` holds `id` and
`request_id`. **Nothing else.** Their versions carry the actual domain — applied amount, coupon code,
promotion, reason, type, value; escalated_at, from_level, to_level, from_principal, to_principal,
reason. **Take both wholesale.** These are the same defect as the four book tables that yield no
columns, found from the other side.

---

## Five things that need a decision

### 1. Five payroll tables with no requirement behind them

Their `workforce` schema adds 13 tables. **The matrix supports eight of them and is silent on five.**

- **In scope** — `roster`, `work_assignment`, `work_time`, `leave_balance`, `shift`, `employee`,
  `employment`. Matrix 1.2.3, 1.2.32, 1.2.37, 1.2.81, 1.2.82, 1.2.83 require staff scheduling,
  leave, attendance history, staffing thresholds and compliance validation. **Our `workforce` schema
  has six tables and does not cover this properly** — we have `rota_assignment` but no roster, no
  work time, no leave balance. This is a genuine gap they have filled.
- **Not in scope** — `payroll_run`, `payroll_line`, `payslip`, `salary`, `salary_component`.
  **A search of the requirement matrix for payroll, payslip and salary returns nothing.**

And matrix **1.2.3 is explicit about the boundary**: staff schedule data *"can be captured via manual
entry or through integration with another workforce management system."* The matrix contemplates
**integrating** with a workforce system, not becoming one. Payroll means tax tables, statutory
deductions and a jurisdiction-by-jurisdiction compliance surface.

**Recommendation: take the eight, and ask what the five are for before taking them.**

### 2. Per-domain product catalogues, against one cart

They add `product`, `product_category`, `price` and `product_recommendation` to **both `fnb` and
`retail`**, alongside the ones in `catalogue`.

Our model is one `catalogue` that F&B and retail extend. Theirs duplicates the catalogue three times.

**This sits awkwardly against their own `orders.order_line.item_source`** — `CATALOGUE`, `FNB`,
`RETAIL` — which is *one cart, one order, one receipt* made explicit, and which we are taking
gratefully. A line can say which domain it came from precisely because there is one line shape;
three product catalogues pull the other way.

**This is a fifth architectural divergence** and belongs with the four in the response document.

### 3. `marketing.data_subject_request` duplicates `platform.dsar_request`

We have DSAR in `platform`. They have it in `marketing`. **One has to go**, and the choice is not
cosmetic: a subject-access request has to reach every schema, so it belongs with the platform
boundary rather than inside the marketing domain.

### 4. Waivers — a real gap, filled

`marketing.waiver_template` and `marketing.waiver_signature`.

**We have no waiver table anywhere**, despite 321 mentions of waivers across the contracts, a client
design pack devoted to *Waiver, Consent & Digital Form Management*, and a workshop board. **Take
both.** This is one of the clearest wins in their file.

### 5. Accreditation — seven tables against a blocked conflict

`accreditation`, `_access`, `_credential`, `_document`, `_status_history`, `_type`, plus
`access_change`. We hold one table, `approvals.accreditation_badge`.

**CF-21 calls accreditation the only blocked work left on the project** — 58 requirements, no
contract, one workshop still owed. If these were modelled from a source rather than inferred, they
may close it without the workshop. **That question is already in the response document.**

---

## Genuinely new, by cluster

| cluster | new | character |
|---|---|---|
| marketing | ~19 | loyalty points engine, support cases with SLA, surveys, waivers, badges |
| identity | ~15 | membership instances, family/household, customer extra fields, OTP |
| orders | 14 | payments — the strongest material in the file |
| workforce | 13 | **8 rostering (take) + 5 payroll (ask)** |
| catalogue | 9 | rentals, membership benefits, product media, recommendations, upgrade rules |
| access | 8 | **7 accreditation** |
| platform | 5 | subscription tiers, allowances, modules, cell endpoint |
| fnb / retail | 10 | **per-domain catalogues — see finding 2** |
| resources | 5 | rental agreements and inspections |
| sync | 4 | cross-cell requests, rejections, guest link, cell connection |
| reporting, whitelabel, inventory, maintenance, control, seating | ~8 | tail |

---

## Method, confirmed across sixteen schemas

1. **Exact name match** → column merge. Mechanical.
2. **Name absent** → find our best candidate by column overlap, then **read both column lists.**
3. **Only what survives both** is new.

Step 2's arithmetic is a shortlist, never a verdict. It scored their `payment_link` as a 0.29 match
for `reservation` while our own `payment_link` sat unmatched, and it paired `sla_policy` with
`loyalty_programme` on nothing but `code`, `id`, `name` and `is_active`.

**Roughly half an hour per cluster, and it removed fourteen duplicate tables before they were
written.**
