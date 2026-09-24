# Values the platform applies with nothing configuring them

> **22 September 2026 · a new checker, a ledger, and three controls built**
>
> **Started from one question — "do we have settings for extra fees like a processing or service
> charge?"** The answer was partly yes, and the part that was no turned out to be a class of
> defect no checker in the package could see.
>
> Contracts, DDL, one checker and one tool were edited. `tools/run-checks.py` is back to its
> entry baseline: two pre-existing errors in `check-package`, seven pre-existing stale authored
> inputs, nothing else.

---

## 1. What was wrong, and why thirty checkers passed on it

`fnb.sub_bill.service_charge` was a stored `numeric(18,4)`. `F29` recomputes tax and service
charge per bill on a split, so a rate was being applied at least twice over a single visit — and
**no row in 628 tables held that rate**. It was found by reading, not by any gate.

Every existing check passes on it, and each for its own reason:

| Checker | Why it stayed quiet |
|---|---|
| `audit-unwired-tables` | `fnb.sub_bill` is reached, so the table never enters the report |
| `check-config-scope` | validates the scope of config operations that exist. There was no operation |
| `audit-screenless-operations` | walks operations. Again — none |
| `check-spec-coverage`, `check-rfp-coverage` | lexical, against capability names. A service charge is a field inside a capability, not a row |

**The reason is structural.** Every check walks a structure and asks whether its *edges* are
present — table to operation, operation to screen, screen to pack citation. A value with no
configuration has no missing edge. It has a missing **node**, one nobody drew, and walking edges
will never find a node that was never there.

## 2. `tools/audit-uncontrolled-values.py`

Asks the inverse question: for every column carrying a value somebody ought to have set, **is
there anywhere a person sets it?** Four classes — `charge`, `threshold`, `rate`, `duration`.

A value on a *definition* is already configured; a value on a *transaction* is not. So the table
is classified first, and only transactional rows are asked. Measurements are excluded outright.

**Report-only, not a gate** — whether an outcome needs a control is a judgement, which is the
argument `run-checks` already records for `audit-unwired-tables`.

**`handoff/values-without-configuration.md` holds the verdicts and is read back**, so a question
answered once stops being asked. Six verdicts; four close a row, two do not:

> `genuinelyMissing` and `fixedByLaw` are **findings**. Recording one triages the row and the tool
> keeps reporting it as a CONFIRMED GAP until somebody builds the control. **A ledger that
> silenced its own gaps would be the place gaps go to be forgotten.**

## 3. Where it stands

    27 applied values · 6 controlled · 10 answered · 11 confirmed gaps · 0 untriaged

**Three closed by building the control:**

| Table | What it fixes |
|---|---|
| `fnb.service_charge_policy` | basis, rate or amount, minimum party size, service types, taxability, `is_discretionary`, `distribution`. **`is_discretionary` is the field a regulator reads first** — a charge a guest cannot decline is a price, and a price belongs in the displayed total. `distribution` carries `orders`' own separation of a service charge from a tip into payroll |
| `orders.resale_fee_policy` | seller and buyer commission, `price_cap_percent`, effective dates, `event_id`/`product_id` narrowest-match override. The listing keeps its columns as the **snapshot** — the rule-and-record split `payments.fee_rule` and `orders.order_fee` already use, because a commission changed later must not restate a completed sale |
| `fnb.temperature_checkpoint` | the unit, its safe range, and `check_frequency_minutes`. **`temperature_log.check_point_id` was `NOT NULL` and referenced no table in the package** — every HACCP reading was required to name a definition nothing modelled. The frequency field exists because an inspector's finding is usually not a bad reading but a **missing** one |

**Eleven remain, and two of them are not ours to decide:**

- **`workforce`** — `break_minutes` (×2), `overtime_minutes`, `entitled_days` are `fixedByLaw`.
  UAE and Oman set different statutory minima. **Statute setting a value is the reason it needs a
  row, not the reason it does not** — a multi-region platform cannot hard-code one jurisdiction.
  Needs legal or HR input before a policy table means anything.
- **`ledger.inter_entity_obligation.settlement_rate` / `rate_applied`** — transfer pricing between
  legal entities, with tax consequences. **A transfer-pricing rate nobody configured is one nobody
  can defend to an auditor.** Escalate rather than build.
- The other five — `rental` damage and missing-item fees, `fnb.table_reservation.duration_minutes`,
  `resources.venue_assignment.travel_buffer_minutes`,
  `workforce.open_shift.incentive_rate_multiplier` — are buildable on the same pattern.

## 4. What this does not cover

**The detector is vocabulary-driven and the defect class is not.** `fnb.temperature_log`'s
`min_celsius` / `max_celsius` were invisible to it — `celsius` is in none of the four head-noun
classes, and `threshold_celsius` surfaced only because it happens to contain the word *threshold*.
**That gap was found by reading the contract for another reason, not by the audit.** Any domain
unit — kg, lux, psi, decibels — slips through identically.

The fix is a unit-suffix rule paired with the existing transaction-versus-definition test, not an
ever-growing noun list. **It is not built.**

Counts were left out deliberately: `quantity` and `*_count` are transactional facts, and including
them put 164 rows in the report to find nothing.

**The F&B service-charge screen does not exist.** `audit-screenless-operations` will report both
new operations until one is drawn. That is a real follow-up and is deliberately *not* recorded in
`handoff/operations-without-screens.md` as an exemption.

## 5. Verification

`check-config-scope`, `check-lineage`, `check-migrations` and `check-screens` all pass.
`check-package` is at its two pre-existing errors; `check-authored-inputs` at its seven
pre-existing stale files. Neither is in this work's diff.

**Four defects in the contract work here were caught by the package's own gates rather than by the
author** — a permission invented outside the vocabulary, a config operation whose scope tag the
naming rules could not reach (*"an unexamined tag is worse than an absent one"*), an unbounded list
over a growing table, and a table count in an authored note left stale. See
[`gotchas.md`](../gotchas.md) for the dependency that caused most of the rework.
