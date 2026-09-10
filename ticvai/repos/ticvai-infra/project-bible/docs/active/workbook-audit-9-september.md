# Workbook audit — 9 September 2026

**Three spreadsheets carry the scope, the schedule and the outstanding actions.** Audited by
`tools/audit-workbooks.py` against the package and against themselves.

One is in good order, one contradicts itself by 1,869 person-days, and one is three weeks behind
the work it tracks.

---

## 1 · The requirement matrix is sound

`sources/requirements/Ticvai_matrix_20260621_2_2_2.xlsx` — **3,156 distinct requirement ids**,
against 3,184 verdicts in `handoff/traceability.json` from the 18 August walk.

| Verdict | Rows | |
|---|---|---|
| `CONTRACTED` | **2,647** | An operation or schema field demonstrably serves it |
| `PARKED` | 396 | AI-parked or workshop-blocked, reason named |
| `GAP_CONTRACT` | 93 | Needs an operation or schema that does not exist |
| `CONTRACTED_PARTIAL` | 43 | Served, but a field, operation or state is missing |
| `GAP_DECISION` | 5 | Undesignable without a client answer |

**Every requirement id in the matrix carries a verdict, and every verdict names a requirement the
matrix still has.** The 28-row excess is the known case recorded in the file's own `keyNote` —
twenty-eight references name two different requirements, so the walk keyed on `packageRef` and
`xlsxRow` together.

**This is the check that could not be run on 18 August**, when there was one version of the file.
There are now three in the package and **the walk has not drifted against any of them.** Nothing
to do here.

---

## 2 · The delivery plan states two different plans

`sources/planning/TAIS_Product_Planning_and_Delivery_Plan_4_1.xlsx` — 23 epics, 444 features,
**7,552 person-days**.

### The dependency matrix cannot answer the question CF-140 asks of it

CF-140 says the plan's *"priorities contradict the dependency order the walk found"*. **Sheet 7
cannot be read that way.** Its 18 rows name capability categories, vendors and infrastructure —
*"All functional modules"*, *"POS & Mobile features"*, *"Payments"*, *"Hardware"* — and **not one
epic, module or feature id.** Joining the epic register to it returns nothing, which is a null
result from a join the workbook does not support, not evidence of consistency.

### The question it *can* answer, and the answer is bad

Priority is stated twice — once per epic on sheet 2, once per feature on sheet 3. **The effort
totals reconcile to the person-day**, 7,552 on both. So any disagreement is purely about
sequencing.

| Read the plan at | P3 "Could" effort | Share |
|---|---|---|
| **Epic Register** | 2,302 pd | **30%** |
| **Feature Register** | 4,171 pd | **55%** |

**The same document, 1,869 person-days apart on what is optional.** A quarter of the whole plan
changes category depending on which sheet you read it from.

**16 of the 23 epics contain features priced below the epic's own priority:**

| Epic | Epic priority | Effort | Of which P3 |
|---|---|---|---|
| `E06` Retail Operations & POS | P2 – Should | 165 pd | **71%** |
| `E05` F&B Operations & POS | P2 – Should | 497 pd | **68%** |
| `E10` Events, Seating & Venue Mapping | P2 – Should | 625 pd | **59%** |
| `E12` Guest Mobile Experience | P2 – Should | 186 pd | 53% |
| `E01` Ticketing & Product Catalogue | **P1 – Must** | 572 pd | **49%** |
| `E03` Admission & Access Control | **P1 – Must** | 511 pd | **49%** |
| `E02` Sales Channels & Checkout | **P1 – Must** | 275 pd | 33% |
| `E04` Payments, Wallet & Financial | **P1 – Must** | 976 pd | 27% |

**`E03 Admission & Access Control` is the one to look at.** It is P1 – Must, gate entry is the
operational core, and **half its effort is marked Could-have.** A milestone plan built on the epic
row commits to it; a sprint built on the feature rows does not.

**70 of 150 modules are split across more than one priority.** CF-140 names four — Notifications,
Loyalty, Portfolio, Digital Waivers — and the real figure is seventy. *Accounting*, *Virtual
Queue*, *Profile Management*, *Ticket Types* and *Authentication and Login* each appear at P1, P2
and P3 at once. **A module that is partly must-have and partly could-have is not a schedulable
statement.**

### One CF-140 claim is wrong and should be corrected

CF-140 reads: *"Access Control System is also P3 at 114 requirements, which reads as a scoring
artefact rather than a judgement."* **It is not P3.** `E03` is **P1 – Must** at 259 requirements
and 511 person-days, and **35 of the 44 access-control features are P1.** The concern behind the
sentence is real and better stated the other way round: not that access control was scored too
low, but that **half of a P1 epic is priced as optional.**

---

## 3 · The task tracker is three weeks behind the work

`sources/planning/TICVAI_Task_Track_From_Workshops.xlsx` — 62 action items.

| Status column says | Items |
|---|---|
| pending | 47 |
| in progress | 11 |
| ongoing | 2 |
| **completed** | **2** |

**CF-143 assessed the same 62 tasks against the package on 18 August and found 37 done**, each
verdict naming its evidence — an ADR, a contract operation, a screen or a conflict. **The tracker
self-reports two.**

So the tracker is not wrong about what was asked for; it is **unmaintained about what has since
been delivered.** Its open list still carries *"Finalize multi-tenant architecture"* (ADR-0001,
ADR-0038, ADR-0039, ADR-0043), *"Evaluate separate database per tenant, schema isolation and
hybrid"* (ADR-0038 decided exactly this) and *"Prepare HLD & LLD architecture diagrams"*
(`diagrams/hld/` and `diagrams/lld/` exist and are derived).

**A tracker whose status column has said *pending* for three weeks against work that shipped is a
tracker nobody can use to find the things that genuinely have not moved** — and those are the ones
it exists for.

**Ownership of what remains open:** Softlabs Team 30, Chinmay 14, Softlabs Design Team 9, and one
each to five others.

---

## What to do

**Nothing on the matrix.** It is the healthiest artefact in the package.

**Take the delivery plan's priority contradiction to Qossai before it schedules anything.** The
question is not which sheet is right; it is **which of the two plans was priced**, because the
7,552 is the same either way and the delivery date is not. `E03` at 49% P3 is the sharpest single
instance.

**Correct CF-140** — the access-control claim is wrong, the module-split count is 70 rather than
four, and the dependency matrix does not support the join the entry assumes.

**Re-baseline the task tracker against CF-143's verdicts** rather than asking each owner. The
evidence is already written; the status column just never received it.
