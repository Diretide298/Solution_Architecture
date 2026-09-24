# Board and dashboard requirements, checked against the matrix and the build

**22 September 2026.** Every requirement the MoMs and the board/dashboard packs imply,
extracted blind, then checked three times — once blind against the matrix, once with the
whole matrix and repository open, and once more to settle what was left.

- Spreadsheet: `handoff/TICVAI_Board_Dashboard_Requirements.xlsx` (eleven sheets)
- Data, scripts and agent specs: `handoff/board-dashboard-data/`

---

## The headline

**7,819 requirements extracted. 7,019 carry board or dashboard bearing and were assessed.**

The useful question is not "is it covered" but **what does someone do with this row**:

| Action | Rows | Share | Meaning |
|---|---|---|---|
| **Covered** | 2,488 | 35.4% | The matrix already obliges it. Nothing to do. |
| **Traceability** | 3,262 | 46.5% | The build specifies it, the matrix does not. Needs a register entry, not development. |
| **Specification** | 564 | 8.0% | Neither settles it. A real decision is outstanding. |
| Partial, not yet resolved | 410 | 5.8% | Checked against the matrix, not against the build |
| **Absent** | 167 | 2.4% | Nothing covers it, after a search with everything open. |
| Not a requirement | 103 | 1.5% | Chrome, process notes, extraction artefacts |
| **Settled against** | 25 | 0.4% | The build deliberately **refused** this. |

**82% of the estate is either already obliged or already built.** Of the 564 genuine
decisions, **2 are High severity**, 347 Medium, 215 Low.

### How that differs from the first answer

The first pass reported 79% not covered and 268 High-severity gaps. That was wrong, and the
way it was wrong is itself the most useful finding in this document.

| | First pass (blind) | Final |
|---|---|---|
| Covered | 1,446 | **2,488** |
| Absent | 1,178 | **167** |
| High-severity | 268 | **2** |

Three passes, each correcting the last, **every single correction in the same direction.**

---

## Why the blind pass was wrong, and why that matters

The blind pass judged each requirement against five matrix rows chosen by lexical
similarity. It was not judging badly; it was judging on 5 rows out of 3,184, and **the
matrix's structure defeats search**. All three causes are verified:

**Long list rows.** `3.2.7` is 1,299 characters. Its opening sentence is about validity
rules; buried in the list are anti-passback, required-exit-before-re-entry and entry
quotas. A search that reads the first line finds none of it.

**Whole blocks never surfacing.** The 80-row `11.1.x` approval governance block, the
`5.5.x` entitlement block, and all 60 rows of domain 16 device management were invisible to
lexical retrieval. Each accounted for dozens of false gaps.

**Requirements filed under headings that describe something else.** This is the big one.
`7.1.10` reads as a concurrent-logins requirement and carries the entire facility-capacity
and channel-allocation specification in its details column. And `6.1.78` — a full reporting
platform, described below — is filed under **"Retail POS / Wallet"**.

**A vocabulary mismatch produced about twenty false gaps on its own.** The blind pass
searched for "store". The project calls it an `Outlet`.

**A matrix that defeats search defeats it for everyone** — estimators, testers, and the
next person asked whether something is covered. That is the finding, not the coverage
percentage.

---

## Findings

Each verified directly against the source files.

### 1. The reporting platform is obliged — in a row filed under Wallet

Matrix **6.1.78** (581 characters, domain 6, sub-domain "Wallet", inside Retail POS)
obliges: a self-service report builder, a dashboard designer, scheduled generation, report
subscriptions, role-based report access, multi-site reporting, **multi-language reporting in
English and Arabic**, exports to PDF/Excel/CSV/XML, API access, drill-down **and
drill-through**, interactive dashboards, KPI scorecards, trend analysis, forecasting,
comparative period analysis, **a minimum seven years of reporting history** with archival,
and real-time and historical reporting.

That one row resolved roughly thirty-five requirements the blind pass had called gaps.

**What is genuinely exposed is narrow: the visual vocabulary.**

- The dashboard specification names **17–18 distinct visual types**
- `contracts/satellite/reporting.yaml:3257` commits to **8**: number, line, bar, stackedBar,
  pie, table, gauge, heatmap
- The matrix names **one** — heat map, at `21.5.24` and `1.2.71`, neither on a dashboard.
  All six matrix mentions of "chart" are "Chart of Accounts".

Missing from the contract: combo, matrix/pivot, map, funnel, waterfall, treemap,
scatter/bubble, ribbon/rank, slicer, decomposition tree. **The Executive Performance board
is specified in terms of three marks that do not exist.**

This is one decision — extend the enum, or state what the platform refuses to draw.

*Note for accuracy:* two matrix rows use "graphical" (`3.2.64`, `1.3.8`). Neither names a
chart type. Quote the chart-type claim, which is verifiable; do not claim the word "graph"
is absent.

### 2. 229 matrix rows sit under sub-domain labels describing something else

| Label | Rows | Actual contents |
|---|---|---|
| 6.1 "Wallet" (all of Retail POS) | 78 | Receipts, e-invoicing, tender balancing, **and the reporting platform** |
| 7.1 "Retail POS" (inside F&B POS) | 62 | User groups, rights, logins, password policy |
| 7.4 "Table Reservation" | 52 | The customer database |
| 7.5 "Kitchen Display" | 10 | Invitation campaigns, VIP quotas, event-entry QR codes |

The real requirements exist elsewhere. Kitchen display is obliged by `4.6.22`, `4.6.33`,
`4.8.3`, `5.1.11`, `5.2.1`, `5.2.2` and `10.1.1` — seven rows across four domains. Table
reservation by `4.9.13`, `5.1.1`, `5.1.2`. The F&B POS requirements are in domain 4,
"Bundles and Promotions".

**The capability is not missing — it is unfindable.**

### 3. Withdrawn scope is still obliged, and still drawn

The client decided against a warehouse execution layer at the 18 August workshop.
`docs/registers/contract-backlog.md` records it verbatim: **BL-158 — "No warehouse
execution layer — putaway, picking, packing, dispatch or warehouse tasks. Withdrawn — the
client decided against a warehouse execution layer at the 18 August workshop."**

The matrix still requires `15.2.10` Picking Lists, `15.2.11` Picking Validation, `15.2.12`
Partial Picking, `15.2.13` Packing Operations. And a board page was drawn for it anyway —
**INVPROC page 2, Warehouse Operations, sixteen requirements with nothing to build
against.**

This is the clearest failure of propagation in the exercise. It will not be the only one.

### 4. Matrix 1.4.4 contradicts a matrix row, two decisions and the build

`1.4.4` requires changes to propagate "to the already sold tickets as well". `1.4.15`
requires retirement "without impacting previously sold tickets". The minutes record twice
that a price change must never alter a sold ticket. The build protects them —
`catalogue.yaml` carries
`DynamicPricingGuardrailsCommercialProtectionView.alreadyPurchasedTickets`.

Everything disagrees with `1.4.4`. Retroactive repricing is commercial and legal exposure.

### 5. The matrix contradicts the build on rollback

`8.5.26` — "System shall support rollback of pricing changes."
`states/catalogue-import-job.yaml` — "**Partial application is recorded rather than rolled
back** — three thousand products half-created is a state somebody has to see to repair."

A tester holding `8.5.26` will raise a defect against a design working as intended.

### 6. Twenty-five requirements were settled against, not left open

These are not awaiting a register entry. The build considered and refused them:

- **ADR-0018** refuses workstation as a configuration level — "Rejected by the client on
  14 August… **Still rejected**" — against boards showing workstation-level overrides.
- **ADR-0002** refuses workstation as a permission source.
- `payments.yaml` refuses auto-revoking entry on failed payment: *"Ending somebody's access
  stays a staff decision with a name attached to it."*
- `fnb.yaml` refuses offline F&B where stock is tracked, against a minute asking for
  end-of-day depletion **so that F&B can keep selling offline**.

**These go back to whoever drew the boards.** Filing them as traceability would record
agreement that does not exist.

### 7. Time semantics are undecided platform-wide

A grep for "daylight" or "DST" across every contract returns **nothing**. Nothing states
whether `validTo` is inclusive. `validTimeWindows` is a pair of times of day, so an
overnight window (22:00→02:00) cannot be expressed. And `daysOfWeek`, `validTimeWindows`
and `blackoutDates` carry no evaluation order, although the package states precedence
explicitly everywhere else ("the first match wins", "most-specific first").

A ticket valid "until 22:00" on the night the clocks change either admits a guest or
refuses them depending on an answer nobody has given.

### 8. A staff-to-participant ratio cannot be expressed

`capacityModel`, `staffRatio`, `onePer`, `minParticipants` return nothing across all
contracts. `StaffingRules.minimumCover` carries a flat headcount.

Sale-time capacity and roster-time cover must evaluate the same expression or a session
sells more places than can be staffed. Because the ratio has no home, **the two are free to
diverge by construction.**

### 9. Other verified contradictions

| Where | What |
|---|---|
| `7.6.8` vs `7.6.15` | One requires scanning equipment serials; the other lists it under *"highly recommended and not currently covered"*. `7.6.15` is the only row describing what the solution does **not** do while counting toward the 3,184. |
| `5.9.2` vs `5.9.6` | A *blind* cashier close-out, and a variance alert at end of shift. Neither says who receives the alert. If it reaches the cashier, the control is defeated. |
| Board vs `3.6.28` | Group discount at qty ≥ 10; matrix says 15 or more. |
| `5.12.15` vs `5.12.8`/`5.12.119` | Recognise ticket revenue at sale, versus defer to earned. |
| MOM-0833 vs `rental.yaml` | A fast swap restarts the rental timer; `swapRentalEquipment` says "the deposit, the agreement and **the clock stay where they are**". |
| `states/entitlement-status.yaml` | "Refunded with entries already taken. The consumed entries stand" — against a pack showing `Refund +1`. |

### 10. 28 requirement IDs are used twice

56 rows, across blocks 22.3, 5.6, 8.1 and 5.5. `22.3.1`–`22.3.10`: rows 2901–2910 are case
management, 2911–2920 are marketing journey automation. A traceability entry citing
"22.3.1" is ambiguous between two unrelated capabilities. Four sub-domain IDs also carry
two different names each.

### 11. Defects in the board packs

- **Frames are missing.** Inventory Board 5 renders frames 1–7, 9, 10 — nine screens where
  its banner promises ten. Retail p1 and F&B p2/p6 skip a badge the same way.
- **The Inventory nav advertises a board that does not exist** — two boards numbered 6, no
  board 5, and a "Receiving & GRN" entry no page delivers.
- A Transfer Summary gauge reads **99.1% where its own numbers give 69%** (29 of 42).
- Resource Management p11: "ANALYTICS, GOVERNANCE & RESOURCE **CONTIOL** CENTER".
- The word **"dock"** appears nowhere in the matrix, in `inventory.yaml`, or in any screen,
  though the Inventory pack specifies dock appointments and utilisation.

---

## The workbook

| Sheet | Rows | Contents |
|---|---|---|
| Read me | — | Method, counts, and what each action means |
| Requirements | 7,819 | Every requirement, with evidence, verdict, **ACTION**, the build path, and which pass produced it |
| **Decision register** | **222** | The 564 rows deduplicated into the decisions behind them, most-closing first. **Start here.** |
| Decisions outstanding | 564 | The individual rows behind those decisions, severity first |
| **Traceability register** | 3,287 | The build specifies it; needs a register entry. "Settled against" rows sorted to the top. |
| Gaps | 4,428 | Partial and Absent, High first |
| Matrix coverage | 3,184 | Reverse view — every matrix row and whether anything evidences it |
| Boards and screens | 1,058 | Every named board, dashboard and screen |
| Pack coverage claims | 12 | The packs' own claims, checked — all 158 cited IDs exist |
| Source and matrix issues | 30 | The findings above, each with an action |
| Summary / Sources | — | By module and source; provenance |

**Read the ACTION column, not the verdict.** A verdict needs interpreting; an action does
not. And "How this verdict was reached" says whether a row was judged blind or with
everything open — only the latter is fully trustworthy.

---

## What to do next

1. **Reconcile the visual-type lists** — 17–18 specified, 8 contracted, 1 in the matrix.
   One decision. This is the commercial item.
2. **Book the 3,262 traceability rows** as register entries, not development. Twelve
   artefacts carry most of the weight — `tenancy.yaml` alone accounts for 228.
3. **Return the 25 "settled against" rows to the board designers.**
4. **Resolve BL-158** — delete or except matrix `15.2.10`–`15.2.13` and withdraw INVPROC
   page 2. Then check whether other withdrawn backlog items still have matrix rows and
   boards behind them.
5. **Fix `1.4.4`** and **decide `8.5.26` versus the import-job design.**
6. **Re-file the mislabelled sub-domains**, starting with `6.1.78` — a reporting platform
   filed under Wallet will keep being missed.
7. **Settle time semantics** — inclusivity, DST, and rule precedence.
8. **Decide where a staff-to-participant ratio lives**, and make the sell path and the
   roster path read the same expression.
9. **Work the Decision register.** The 564 rows reduce to **222 decisions** — 119 close more
   than one row, 103 are genuinely single questions. The top eight close 98 rows between
   them. Only one is High severity: whether F&B recipe depletion is real-time or end-of-day,
   which decides whether an outlet can sell while offline.

---

## Method and reproduction

Three passes, each auditable:

| Pass | Scope | Access | Result |
|---|---|---|---|
| Blind extraction | 27 MoMs, 2 specs, 48 board pages | Assigned documents only | 7,819 requirements |
| Blind adjudication | 7,019 rows | 5 lexical candidates | Superseded |
| Truncation re-judgement | 1,000 rows | Full matrix text | 52 changed, all upward |
| Sighted re-check | 1,287 Absent/High rows | Whole matrix + repository | 1,088 changed, all upward |
| Partial resolution | 4,208 rows | Whole matrix + repository | 80% traceability |

**The blind extraction remains the durable asset** — each agent saw its documents and
nothing else, so the 7,819 requirements are an independent statement of what the sources
ask for. The blind *adjudication* is what proved unreliable, and it has been superseded.

`board-dashboard-data/` holds the extracted requirements, all three verdict sets, the
matrix, the findings, the scripts, and the agent specs in `specs/` — which are more of the
method than the scripts are.

Counts to check a rebuild against: **7,819** extracted, **7,019** assessed, **3,184** matrix
rows, **1,000** re-judged (52 changed), **1,287** sighted (1,088 changed), **4,208** partial
resolutions.

Total: **75 agent runs** — 13 extraction, 24 adjudication, 6 re-judgement, 8 sighted,
24 partial resolution.
