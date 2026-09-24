# Applied values with no configuration behind them

**`fnb.sub_bill.service_charge` is stored, recomputed per bill on a split, and no row in the
package holds the rate.** It was found by reading the contracts, not by any of the thirty checks
in `run-checks`, and that is the reason this document and `tools/audit-uncontrolled-values.py`
exist.

The tool pairs every applied value against the configuration that sets it, across four classes —
charge, threshold, rate and duration. `rental.settlement.late_fee` pairs with
`rental.fee_policy.late_fee_amount`, `late_fee_basis` and `grace_period_minutes`; that is the
shape when it is right. This file records the values that do not pair, and the verdict on each.

## The six verdicts

| Verdict | Meaning | Closes the row? |
|---|---|:---:|
| `setByAProvider` | A third party decided it. Nobody configures it and a control would be a fiction | yes |
| `enteredPerIncident` | A person assesses it against a real event. The control is an approval limit, not a rate | yes |
| `derivedFromAnother` | It falls out of a value that *is* controlled. The control is upstream | yes |
| `observedNotSet` | A reading, wearing a neutral word the `MEASUREMENT` list could not catch | yes |
| `fixedByLaw` | Statute sets it — **and it still needs a row**, because the law differs by jurisdiction and this platform is multi-region | **no** |
| `genuinelyMissing` | The platform applies a number that exists only in somebody's head | **no** |

**A verdict is not a dismissal.** The last two are findings: recording one triages the row and
the tool keeps reporting it as a CONFIRMED GAP until somebody builds the control. A ledger that
silenced its own gaps would be the place gaps go to be forgotten.

## Closed by building the control

**`fnb.sub_bill.service_charge` — the one this document was written for, and the first one shut.**
`fnb.service_charge_policy` now holds it: `basis` (`none`, `percentOfSubtotal`, `fixedPerCover`,
`fixedPerBill`), a rate or an amount, `minimumPartySize`, the `serviceTypes` it applies to,
`isTaxable`, `includedInDisplayPrice`, `shownSeparately`, `isDiscretionary` and `distribution`.
`getFnbServiceChargePolicy` and `setFnbServiceChargePolicy` read and write it at venue scope,
following `rental.fee_policy` and `setRentalFeePolicy`.

Three of those fields exist because the gap analysis asked questions the old column could not
answer. **`isDiscretionary` is the one a regulator reads first** — a charge a guest cannot decline
is a price, and a price belongs in the displayed total. **`distribution` carries `orders`' own
separation of a service charge from a tip** into payroll, rather than leaving it to whoever writes
the export. **`basis: none` is a real answer**: a venue that levies nothing should say so, rather
than leaving a null that reads as unconfigured.

**The screen is still missing.** No F&B service-charge configuration screen exists in P08, so
`audit-screenless-operations` will report both operations until one is drawn. That is a genuine
follow-up, not an exemption, and it is deliberately not recorded in
`handoff/operations-without-screens.md`.

**`orders.resale_listing.seller_fee_percent` and `buyer_fee_percent` — closed.**
`orders.resale_fee_policy` holds both, plus `priceCapPercent`, `minimumAskPrice`, effective dates
and an `eventId`/`productId` narrowest-match override, because a final and a Tuesday fixture do
not resell on the same terms. **The listing keeps its own columns as the snapshot** — the
rule-and-record split `payments.fee_rule` and `orders.order_fee` already use, since a commission
changed later must not restate a completed sale. The backlog had asked for exactly this and its
note that **anti-scalping caps are regulated in some jurisdictions and unresolved for the UAE and
Oman** is carried onto the field rather than settled.

**`fnb.temperature_log` — closed, and it was worse than the audit showed.** `check_point_id` was
`NOT NULL` and referenced **no table in the package**, so every HACCP reading was required to name
a definition nothing modelled, and `min_celsius`/`max_celsius` sat on each reading with no source.
`fnb.temperature_checkpoint` now holds the unit, its safe range, and `check_frequency_minutes` —
that last one because **an inspector's finding is usually not a bad reading but a missing one**,
and nothing said how often a unit must be read. The log keeps its range as the snapshot, for the
reason the log itself gives: *"deleting a bad reading is the one thing an inspector looks for"*,
and restating the range a past reading was judged against is that act by other means.

**The audit did not find that one; reading the contract for a different reason did.** `celsius` is
in none of the four head-noun classes, so `min_celsius` and `max_celsius` were invisible to it and
`threshold_celsius` surfaced only because it happens to contain the word *threshold*. **The defect
class is vocabulary-independent and the detector is vocabulary-driven**, so any domain unit — kg,
lux, psi, decibels — slips through the same way. Extending the noun list indefinitely is not the
answer; a unit-suffix rule paired with the same transaction-versus-definition test is.

**Built 22 September, and it now verifies this fix by machine.** A unit bounded by `min`, `max`,
`threshold`, `target` and their kin is a limit; a unit on its own is a reading. The unit stays in
the stem, so `fnb.cold_chain_event.threshold_celsius` and both `fnb.temperature_log` range columns
now pair with `fnb.temperature_checkpoint` — **the hand ruling this row carried in the morning is
superseded by a derived one in the afternoon.** No other unit-bearing limit in 632 tables was
unpaired.

**Fixing it exposed a flaw in the checker.** `rental.fee_policy` pairs on a column name because it
holds several fee kinds and must say which is which — `late_fee_amount`, `late_fee_basis`.
`fnb.service_charge_policy` holds one, so its columns are `basis` and `rate_percent` and none
carries the word *service*. Reading only columns, the tool went on reporting a gap that had just
been filled. It now also reads the control table's own name, stripped of its `_policy` suffix.

**Wave 2, 22 September — three more closed by building the control, all verified by the tool:**

- **`rental.settlement.damage_fee`, `missing_item_fee`** → `rental.fee_policy` gains
  `damageFeeMaximum`, `damageFeeApprovalAbove`, `missingItemFeeBasis` (`replacementCost` |
  `fixedAmount`) and `missingItemFeeAmount`. **A dent is assessed, not tabulated**, so the damage
  control is a ceiling and a second signature, not a rate.
- **`workforce.open_shift.incentive_rate_multiplier`** → `workforce.staffing_rules` gains
  `defaultIncentiveRateMultiplier`, `maximumIncentiveRateMultiplier` and `incentiveApprovalAbove`,
  **top-level rather than inside `overtime`** so each is a column the tool can pair and a database
  can constrain, not a key inside a JSON blob.
- **`fnb.table_reservation.duration_minutes`** → `fnb.reservation_policy`: a default turn time,
  party-size bands, a seating buffer and a ceiling. **This one the tool cannot confirm** — see
  *Ruled* below.

## Withdrawn — a gap this document asserted and should not have

**`catalogue.channel_capacity.oversell_allowance` was listed here as `genuinelyMissing` and was
not a gap.** `catalogue.yaml:11153` places the allowance on the capacity envelope **on purpose**,
and says so: *"An allowance on the envelope rather than an admission policy, because the gate must
still refuse when actual capacity is reached — overselling is a sales decision and admission is a
safety one, and they must not share a number."* `oversellBasis` alongside it
(`fixedCount | historicNoShowRate | percentage`) names how the number is derived.

**The tool never reported this row.** `catalogue.channel_capacity` is not transaction-shaped, so
the checker classified it as a control and stayed silent — correctly. It was added to the table by
hand from an earlier, cruder probe and carried into the register from there.

**That is the second time in one day the same mistake was made**: noting that a value has no
separate control table without checking whether the design deliberately places it on the row. The
first was `outlet` master data, withdrawn for the same reason. **A hand-added row carries none of
the checker's reasoning and should be held to a higher standard than one the tool raised, not a
lower one.**

**`resources.venue_assignment.travel_buffer_minutes` — withdrawn, and the third instance.** This
one the tool *did* raise, and the triage agreed with it. The row is a resource's standing venue
footprint — `primaryVenueId`, `secondaryVenueIds`, `sharedPool`, `effectiveFrom`, `effectiveTo`,
`scopePath` — which makes it the control, not an outcome. **Only its name ends in `assignment`**,
and the checker's transaction list read the name. It now also treats an effective-dated row as a
definition; exactly two tables changed class, and the other carries no value columns.

**Three instances, one shape.** Each time, the absence of a *separate* control table was taken
for the absence of a control, without looking at what the row itself was. The check that would
have caught all three is the same: **read the columns before the name.**

## Ruled

| Column | Verdict | Why |
|---|---|---|
| `orders.chargeback.fee_amount` | setByAProvider | What the acquirer took to process the dispute. The backlog entry behind `Chargeback` reasons about *"a 40 AED case with a 30 AED fee"* as something to concede deliberately — only sensible if the fee arrived rather than being set here |
| `orders.payment.fx_rate`, `orders.refund.fx_rate` | setByAProvider | A rate off the feed, snapshotted at the moment of payment. `ledger.fx_rate` owns the feed and `finance` already argues the daily-versus-intraday choice is per purpose. The stem does not pair because the control column is bare `rate`, which is a limit of the matcher, not a gap |
| `rental.settlement.chargeable_late_minutes` | derivedFromAnother | Return time minus expected return minus `grace_period_minutes`, and the grace period is controlled by `rental.fee_policy` |
| `workforce.rota_assignment.overtime_minutes` | derivedFromAnother | **Re-ruled 22 September — this was `fixedByLaw` and the control already existed.** `workforce.yaml` `StaffingRules.overtime` carries `afterHoursPerWeek`, `rateMultiplier` and `requiresApproval`, under `scopePath` — so the per-region statutory threshold has a home and the per-assignment minutes are computed from it. **Recorded by hand**: `overtime` is a nested object, a JSON column the matcher cannot read into. The statutory *values* still need legal input (register B8); the *schema* does not |
| `fnb.table_reservation.duration_minutes` | derivedFromAnother | Defaulted from `fnb.reservation_policy` — `getFnbReservationPolicy` / `setFnbReservationPolicy` in `fnb.yaml` — and kept on the booking as its snapshot. **Recorded by hand**: `duration` is a generic stem and the matcher refuses to pair on one, deliberately, after it once proposed an audio clip's length as the control for a kitchen delay |
| `fnb.kitchen_exception.duration_minutes` | observedNotSet | How long the exception lasted. `duration_minutes` is `elapsed_minutes` wearing a neutral word |
| `workforce.leave_balance.available_days`, `workforce.leave_balance.pending_days` | derivedFromAnother | A balance and a pending total, both computed from `entitled_days` and bookings against it. `entitled_days` is the one that needs a control, and it is listed below |
| `fnb.waitlist_entry.quoted_wait_minutes` | derivedFromAnother | The quote given to a guest, computed from the queue's own `cycle_minutes` and party position. `queue.queue` holds the inputs |
| `subscription.module_listing.provisioning_minutes` | observedNotSet | How long provisioning took for that listing. The table is a catalogue entry the matcher read as transactional because of the word *listing* |

## Confirmed gaps — triaged, still open

These stay in the report. Each is a control somebody has to decide on and build.

| Column | Verdict | Why |
|---|---|---|
| `workforce.rota_assignment.break_minutes`, `workforce.shift.break_minutes` | fixedByLaw | UAE labour law sets minimum rest breaks by shift length, and Oman's differ. **Statute setting it is the reason it needs a row, not the reason it does not** — a multi-region platform cannot hard-code one jurisdiction's number |
| `workforce.leave_balance.entitled_days` | fixedByLaw | Statutory minimum annual leave, varying by region and tenure, with the employer free to exceed it. Needs an entitlement policy, not a column |
| `ledger.inter_entity_obligation.settlement_rate`, `ledger.inter_entity_obligation.rate_applied` | genuinelyMissing | Inter-entity settlement between legal entities. `rate_applied` is plausibly the snapshot of `settlement_rate`, but nothing configures the latter, and **a transfer-pricing rate nobody configured is a transfer-pricing rate nobody can defend to an auditor** |
| `orders.invitation_allowance.allowance`, `wallet.shared_wallet_member.allowance_amount` | genuinelyMissing | Per-row allowances with no scheme defining them |

## What this does not yet cover

The tool reads four classes of value. **Counts were deliberately left out** — `quantity`,
`*_count` and their kin are overwhelmingly transactional facts, and including them put 164 rows
into the report to find nothing. If a count ever needs configuring it will be a `max_*` or
`reorder_*`, which the threshold class already reads.

The matcher pairs on a stem within one schema. `orders.payment.fx_rate` against
`ledger.fx_rate.rate` is the case it cannot see, because the control column is bare `rate` and a
bare stem pairs with anything. That is a limit worth knowing when reading a row as open.
