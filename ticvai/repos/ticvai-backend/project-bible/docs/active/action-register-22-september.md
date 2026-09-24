# Action register — 22 September 2026

> **Consolidated from two workstreams**: the board and dashboard requirements comparison
> (`handoff/board-dashboard-requirements.md`, 7,819 extracted requirements against the 3,184-row
> matrix) and the applied-values configuration audit
> (`handoff/values-without-configuration.md`, `tools/audit-uncontrolled-values.py`).
>
> **✓ marks a claim re-verified against source for this register**, independently of the report
> that raised it. Unmarked items are carried from their source document's own verification.
>
> **The dashboard question (B1) is decided** — see section I. It was the fork everything else hung
> on, and the answer changes what the other dashboard items mean.
>
> **Wave 2 landed 22–23 September** — I1, I2, F3, H2, H3 done, plus H4 (a deriver regression the
> wave caused and fixed). Configuration gaps 11 → 5; the checker now verifies the cold-chain fix
> itself; the command centre has its module binding and its read.

---

## A. Time-critical

| # | Action | Why |
|---|---|---|
| ~~A1~~ | ~~**Persist the intermediate extraction data**~~ — **CLOSED 22 September** ✓ | `handoff/board-dashboard-data/` now holds 37 MB — `extracted.jsonl`, `matrix.jsonl`, `candidates.jsonl`, `decision-register.jsonl`, `findings.jsonl`, `partial/`, scripts and agent specs, with a README. The comparison can be re-run without re-reading 48 board pages |

## B. Client and commercial decisions

**Numbers revised 22 September** after the sighted re-check superseded the blind pass:
pass 1 -> pass 2 -> pass 3. Covered 20.8% -> 30.8% -> **82% obliged or built**;
Absent 17.0% -> 2.4%; High-severity 268 -> 23 -> **1**; open rows -> **564**, resolved by
**222 decisions** (section J). 410 rows (5.8%) still carry unresolved Partial verdicts.

**B1 is resolved.** The platform goes to a **command centre**: a single dashboard shell showing
the module dashboards each login is entitled to see, plus drag-and-drop customisation and a
settings surface for building module-specific dashboards. Section I carries the work.

| # | Action | Why |
|---|---|---|
| B2 | **Rule on `1.4.4`** — "propagate changes to already-sold tickets" | Contradicts `1.4.15` and two independently recorded MoM decisions. Retroactive repricing is legal and commercial exposure |
| B3 | **`5.12.15` vs `5.12.8` / `5.12.119`** — recognise ticket revenue at sale, or defer to earned | Audit-relevant accounting policy, stated both ways in the matrix |
| B4 | **`5.9.2` vs `5.9.6`** — who receives the end-of-shift variance alert | `5.9.2` requires a *blind* cashier close-out. If the alert reaches the cashier, the blind control is defeated |
| B5 | **MoM 18 Aug vs `15.2.10`–`15.2.13`** | The team agreed **not** to implement picking, packing and dispatching statuses. The matrix requires picking lists, picking validation, partial picking and packing operations |
| B6 | **`7.6.8` vs `7.6.15`** — equipment serial scanning | `7.6.15` lists it as *"highly recommended and not currently covered"*, and is the only matrix row describing what the solution does **not** do while still counting toward the 3,184 |
| B7 | **Group discount threshold** — board says qty ≥ 10, matrix `3.6.28` says "15 people or more" | Straight conflict, cheap to settle before it reaches pricing |
| B8 | **UAE and Oman statutory values** — rest breaks by shift length, overtime thresholds and multipliers, minimum annual leave | Needs legal or HR. Blocks F1 |
| B9 | **Inter-entity transfer-pricing rate** | Tax consequences. **A transfer-pricing rate nobody configured is one nobody can defend to an auditor.** Blocks F2 |

## C. Matrix hygiene — cheap, high traceability impact

| # | Action | Why |
|---|---|---|
| C1 | **Renumber 28 colliding requirement IDs (56 rows)** ✓ — blocks 22.3 (10), 5.6 (8), 8.1 (6), 5.5 (4). **Do 22.3 first** | `22.3.1` is ambiguous between case management and marketing journey automation. A numbering collision inside Marketing & CRM is where a scope argument starts |
| C2 | **Re-label sub-domains in matrix domains 6 and 7** (229 rows) | 7% of the matrix points the reader at the wrong subject. **Auditing coverage by sub-domain name returns the opposite of the truth.** 6.1 "Wallet" is 78 rows of Retail POS; 7.1 "Retail POS" is 62 rows of user rights; 7.4 "Table Reservation" is 52 rows of customer database; 7.5 "Kitchen Display" is 10 rows of invitation campaigns. **Corrected 22 September — "KDS has no requirements" was wrong.** Seven exist (4.6.22, 4.6.33, 4.8.3, 5.1.11, 5.2.1, 5.2.2, 10.1.1), scattered across four domains under labels like "Payment Methods". **The capability is not missing, it is unfindable** — which is the worse finding and the one C5 addresses |
| C3 | **Add matrix requirements obliging outlet master data** — the build already has it ✓ | **Corrected 22 September.** 33 matrix rows mention a store or outlet and zero create or configure one ✓ — but that is a fact about the *matrix*, and the earlier framing wrongly implied a build gap. `tenancy.yaml:2204` models `Outlet` fully (`platform.outlet`: code, name, venueId, kind, zone, stockLocationId, costCenterId, openingHours) with `createOutlet`, `updateOutlet` and `listOutlets` ✓. **The blind pass searched "store"; the project says "outlet"** — one word, roughly 20 false gaps. This is a register entry, not development |
| C4 | **Fix four sub-domain IDs carrying two names each** (5.4, 5.5, 8.1, 8.3) | Any count filtered by sub-domain silently merges them |
| C5 | **Split the matrix rows that defeat search** — `3.2.7` is 1,299 characters, opening on validity rules and burying anti-passback and exit-before-re-entry in its list; `7.1.10` reads as a concurrent-logins requirement and carries the entire facility-capacity and channel-allocation spec in its details column; **`6.1.78` holds a full reporting platform under the label "Retail POS / Wallet"** | **This is the single most valuable finding of the exercise, and three passes proved it the hard way.** Whole blocks never surfaced to a blind reader — the 80-row approval governance block, the entitlement block, all 60 device-management rows. The headline moved 79% not-covered → 17% → 2.4% Absent, **every correction in the same direction**, because the matrix is better than a search suggests and badly filed. **A matrix that defeats search defeats it for everyone** — estimators, testers, three separate automated passes, and the next person asked "is this covered?" |
| C6 | **Create register entries for the 1,039 requirements covered by the build and obliged by nothing in the matrix** | **Not a coverage gap — a traceability gap.** These need register entries, not development. Genuinely missing scope is 167 rows, of which 23 matter |

## D. Board pack defects

| # | Action | Why |
|---|---|---|
| D1 | **Confirm whether a Receiving & GRN board exists** | The Inventory nav lists two boards numbered 6 and no board 5. **Goods receipt — where stock enters the business and the three-way match happens — has no board.** If it does not exist this is a scope gap, not a labelling error |
| D2 | **Recover the missing frames** — Inventory Board 5 renders nine screens where its banner promises ten; the same skip appears on Retail p1 and F&B p2 and p6 | The complete Ticket Types pack carries exactly 10 frames on each of 12 boards, which establishes the intended shape |
| D3 | **Settle board names before the screen list is frozen** | Retail Board 1 is "Store Config", "Store & Ops Config" and "Store & POS Config" on three pages of one pack. The backlog will be named from these |
| D4 | **Transfer Summary gauge reads 99.1% where its own numbers give 69%** (29 of 42) | |
| D5 | Typo — Resource Management p11: "ANALYTICS, GOVERNANCE & RESOURCE **CONTIOL** CENTER" | |

## E. Delivery backlog

| # | Action | Why |
|---|---|---|
| E1 | **Settle the one remaining High: is F&B recipe depletion real-time or end-of-day?** ✓ | **268 → 23 → 1 across three passes.** This one decides **whether an outlet can sell while offline**, and the sources disagree. `fnb.yaml` states the real-time position twice and builds on it ✓ — the contract preamble says *"Stock depletion for recipe-linked items is real-time, so **F&B is blocked offline where inventory is tracked**"*, and `createFnbOrder` refuses offline orders containing a recipe-linked item. The minutes say end-of-day. **This is not a field edit**: the operation carries `x-ticvai-offline-capable: true` with a conditional refusal, and the offline model leans on ADR-0013's local bundle. Moving to end-of-day removes the block entirely |
| E2 | ~~**Resolve the 410 unresolved `Partial` rows**~~ — **DONE 22 September.** 410/410 adjudicated: **266 traceability (64.9%), 139 realWork (33.9%), 5 cannotTell.** Every traceability verdict cites a source; 264 of 266 machine-verified against `file:line`. **139 rows go to the backlog** — see section K | **The 80% prior did not hold, and the reason corrects this register.** These rows were *not* unexamined against the build: 345 of the 410 already carried a build path, from a sighted pass with full repository access. What they lacked was a build *verdict*, not a build *look* — so the easy traceability wins had already been harvested and 65% is the residue. **The "never checked against the build" framing in the earlier version of this row was wrong** |
| E3 | **Split two merged decision headings in the register** — procurement spend-category from business-unit taxonomy; till variance tolerance from cash variance reason codes | The register agent merged each pair under one heading. They need separate owners |

## F. Configuration gaps — 5 open in `audit-uncontrolled-values`

Three were closed by building the control: `fnb.service_charge_policy`,
`orders.resale_fee_policy`, `fnb.temperature_checkpoint`. See
`docs/active/uncontrolled-values-22-september.md`.

| # | Action | Blocked on |
|---|---|---|
| F1 | **3 × `workforce`** — `rota_assignment.break_minutes`, `shift.break_minutes`, `leave_balance.entitled_days`. **Statute setting a value is the reason it needs a row, not the reason it does not** — the platform is multi-region. **Was 4 — `overtime_minutes` re-ruled in Wave 2**: `StaffingRules.overtime` already carries `afterHoursPerWeek`, `rateMultiplier` and `requiresApproval` under `scopePath`, so the per-region statutory threshold has a home. The *values* still need B8; the *schema* does not. `minimumRestHours` is rest between shifts, not an in-shift break, so `break_minutes` stays open | **B8** |
| F2 | **2 × `ledger.inter_entity_obligation`** — `settlement_rate`, `rate_applied` | **B9** |
| ~~F3~~ | **DONE — Wave 2, 22 September.** `rental.fee_policy` gains a damage-fee ceiling and approval threshold and a missing-item basis; `workforce.staffing_rules` gains incentive default, maximum and approval threshold; new `fnb.reservation_policy` holds turn times by party size, a seating buffer and a ceiling. **Four of five machine-verified by the checker**; `table_reservation.duration_minutes` is ruled by hand because `duration` is too generic a stem to pair. **`resources.venue_assignment.travel_buffer_minutes` was withdrawn** — the row is an effective-dated standing footprint and *is* the control; only its name ends in `assignment`. The checker now treats effective-dated rows as definitions | — |
| F4 | **Draw the F&B service-charge configuration screen** | No P08 screen exists, so `getFnbServiceChargePolicy` and `setFnbServiceChargePolicy` report as screenless until one is drawn |

## G. Package hygiene — pre-existing, not from this work

| # | Action | Why |
|---|---|---|
| G1 | **Two `check-package` errors** in `docs/active/build-readiness-21-september.md` — it names the accreditation platform by a different name than its screens file declares, and cites a two-digit platform code that no screen file defines | The only two gate errors standing. **Described rather than quoted on purpose**: `check-package` scans every `docs/` and `handoff/` markdown file for platform codes, so reproducing the offending strings here made *this register* fail the same check — which is what happened on the first write of it. `conflicts.md` and `conflict-status.md` are exempt for exactly this reason; a one-off register is not, and rewording is the right fix rather than widening the exemption |
| G2 | **Seven stale authored inputs** ✓, all written against `f236f872cf31`: `service-decomposition.json`, `contract-backlog.json`, `backlog-clusters.json`, `traceability.json`, `artefact-audit.md`, `schema-viewer-notes.md`, `rag-index-sources.md` | Nothing in `tools/` rebuilds them. See `docs/regenerating-authored-docs.md`, then `--bless` |

## H. Tooling follow-ups

| # | Action | Why |
|---|---|---|
| H1 | **Reword the report's claim that "the single 'graph' is SEO metadata (22.11.1)"** ✓ | `3.2.64` requires *"an access control points graphical map presenting statistics in real time"* and `1.3.8` requires a seating map *"in full graphical display"*. The substance holds — **no chart type is named anywhere in the matrix** ✓ — but the absolute as written is knockable in a client meeting. Use the stronger, verifiable form |
| ~~H2~~ | **DONE — Wave 2.** A unit bounded by `min`/`max`/`threshold`/`target` is a limit; alone it is a reading. **It now machine-verifies the cold-chain fix** that was ruled by hand the same morning, and surfaced the log's own range columns as snapshots. No false positives elsewhere. Was: *Build the unit-suffix rule in `tools/audit-uncontrolled-values.py`* | `celsius`, `kg`, `lux`, `psi` are in none of its four head-noun classes. This is how `fnb.temperature_log.min_celsius`/`max_celsius` and a `NOT NULL` foreign key to a table that existed nowhere were both missed. The detector is vocabulary-driven and the defect class is not |
| ~~H3~~ | **DONE — Wave 2.** Two entries in `docs/gotchas.md`: the derive cascade, and a document failing the check for the defect it quotes. Was: *Add the derive-cascade entry to `docs/gotchas.md`* | Any root edit — a contract, a file in `tools/`, even a count inside a JSON note — cascades through derived artefacts and ends at the six mirrors. One number changed in `service-decomposition.json` made all 198 diagrams stale |
| ~~H4~~ | **DONE — found and fixed in Wave 2: `derive-schema.py` let an alias shadow a definition.** Moving `ModuleKey` to `common.yaml` left `subscription.ModuleKey` as a bare `$ref`. The deriver registers schemas by name across every contract, **first-loaded wins**, and `satellite/` loads before `shared/` — so the pointer became *the* `ModuleKey`, every reference fell through to `jsonb`, and **`whitelabel.module_enablement.module_key` regressed from `text NOT NULL` without a line of `white-label.yaml` changing**. Caught by reading the derived DDL, not by a gate. An alias no longer claims a name over a definition, and the resolver follows one. It was the only alias in the package, so nothing else moved | — |

## I. Dashboard command centre — B1 resolved, build it

**The direction:** one command centre showing the module dashboards each login is entitled to,
with drag-and-drop customisation and a settings surface for building module-specific dashboards.

**The specification already exists** — `sources/requirements/Ticketing_Platform_Native_Dashboard_Visualization_Requirements.pdf`,
12 pages, 18 visual types **all marked MVP**, 10 interaction capabilities, 9 builder panes, 4
modes, 6 roles, 10 architecture layers.

**The screens already exist and none is started** — `screens/P16-venue-analytics.yaml`: ANL-001
Executive Command Center, ANL-021 Dashboard Library, ANL-022 Creation Wizard, **ANL-023
Drag-and-Drop Dashboard Canvas**, ANL-024 Widget & Visualization Library, ANL-025 KPI Builder,
ANL-026 Targets & Thresholds, ANL-027 Data & Filter Configuration, ANL-028 Drill-Down &
Interaction Designer, ANL-029 Access, Publishing & Versioning, ANL-030 Preview, Validation &
Health. All `status: notStarted` ✓.

**More is modelled than the coverage report implies.** `SemanticModel` (version, domains,
relationships, publishedAt) and `KpiDefinition` (code, formula, unit, `higherIsBetter`,
`defaultPeriod`, owner) both persist, and `getSemanticModel`, `listKpis`, `createKpi` and
`getKpiValues` all exist ✓. The governed-definitions principle — *"Net Revenue has one definition
across POS, B2C, B2B and OTA"* — is already there.

| # | Action | Why |
|---|---|---|
| ~~I1~~ | **DONE — Wave 2.** `DashboardTile.visualisation` goes 8 → **20**: the nine genuinely missing (combo, matrix, funnel, waterfall, treemap, scatter, map, ribbon, decompositionTree) plus layout variants area, donut, stackedBar100. **`x-ticvai-refuses` states what the platform will not draw** — slicer is a `ReportParameter`, narrative belongs with `ai.Suggestion`, cohort is a usage not a mark. `screens/_components.yaml` now points at the contract instead of listing four marks — **three layers that disagreed now agree**. **The new marks cannot yet bind data**: `ReportColumn` has no encoding role, which is I3 | D-002 closes with it |
| ~~I2~~ | **DONE — Wave 2.** `ModuleKey` moved to `shared/common.yaml` — one list for subscriptions, screens and dashboards, guarded by `$ref` resolution rather than an unchecked copy. `Dashboard.module` is required (`core` for none). `createDashboard` and `updateDashboard` refuse with **409** when the caller is not entitled — on update too, or it would be the way round the create check. **`getCommandCentre`** resolves the caller's entitlement on the server, per request (licensed ∩ holds a permission in the module), and returns their dashboards grouped by module, with `canAuthor` per module for the drag-and-drop entry point. ANL-001 wired to it | — |
| I3 | **Type `DashboardTile.parameters`, and add `ReportColumn.role`** — the second is now urgent, because I1 added eleven marks that cannot bind data without it. A `scatter` needs x, y, size and colour; a `combo` needs a secondary axis with stated units. **Type `DashboardTile.parameters`** — it is `additionalProperties: true` ✓, so field wells (Axis, Legend, Values, Small Multiples, Tooltips, Filters), formatting and the analytics pane (constant, average, min, max, median, percentile, trend, target, forecast, anomaly) have nowhere defined to live. `position` is an untyped object, the only concession to a 12-column drag-resize canvas |
| I4 | **Model the interaction framework centrally** — cross-filtering, cross-highlighting, drill-down/up, drill-through, tooltips, visual/page/report filter scopes, bookmarks and reset, zoom/brush/select, navigation actions, and refresh state (as-of time, loading, stale, partial, error) | The spec is explicit that these are implemented once and shared by every visual, **not separately within each chart**. Only `refreshSeconds` exists, and that is cadence, not state |
| I5 | **Model the four modes** — view, edit, presentation, mobile layout | Presentation mode is not cosmetic: the spec calls out that the operations board must stay legible on a wall display |
| I6 | **Map the six spec roles onto the permission vocabulary** — Executive/Viewer, Operations Manager, Analyst, Dashboard Designer, Data Administrator, Platform Administrator | This is what makes "each login sees its entitled module dashboards" enforceable rather than cosmetic |
| I7 | **Dashboard versioning and a draft → review → publish workflow** | ANL-029 exists as a screen and `updateDashboard` is the only operation behind it |
| I8 | **Decide the engine / semantic split** — the spec names it the key design decision: the visualization engine separate from the semantic and query layer | `SemanticModel` exists. The query service (row and column security), calculation engine, cache and refresh coordinator, export and rendering service, and audit and telemetry layer do not. **Worth an ADR before any of I3–I7 is built** |
| I9 | **Give the command centre's module shell a pattern, and draw the screens the new configuration has no home for** | `screens/_patterns.yaml` describes one dashboard's tiles; the shell that switches between modules — what `getCommandCentre` feeds — has no pattern yet, and it is recorded there as an open question. Separately, `getFnbReservationPolicy` / `setFnbReservationPolicy` have no screen, alongside F4's service-charge pair |

**Two the package already flagged about itself**, confirmed here: ANL-025 KPI Builder and ANL-028
Drill-Down & Interaction Designer each *"declare no operation that writes anything — the name
promises authoring and the contract offers none."*

## J. The 222-decision register

`handoff/board-dashboard-decisions.md` (222 decisions, readable) and the `Decision register`
sheet, ordered most-closing-first. **7,819 requirements → 82% already obliged or already built →
564 open rows → 222 decisions → 1 High.**

**The top eight close 98 rows between them.** Work these before anything further down the list.

| Decision | Rows | What it settles |
|---|---:|---|
| **D-001** | 21 | Agree one tab/section IA for the `configEditor` frames |
| **D-002** | 19 | Extend `DashboardTile.visualisation`, or state what the platform refuses to draw |
| **D-003** | 12 | Is a catalogue a first-class object, and how do channels bind to it |
| **D-004** | 10 | Extend `ApprovalKind` to the acts the screens actually gate |
| **D-005** | 10 | Type the stock location hierarchy — capacity, temperature class, bins |
| **D-006** | 9 | Are supplier compliance documents their own register |
| **D-007** | 9 | Define stock-health: inputs, formula, band thresholds |
| **D-008** | 8 | Express the staff-to-participant ratio once, so sale-time and roster agree |

**D-002 is I1 arriving from the other direction** — an independent pass reached the same
conclusion about the eight-value enum, which is the strongest evidence either has. Do them as one
piece of work, and take the second half of D-002 seriously: **stating what the platform refuses
to draw is as useful as extending the list**, and cheaper to defend.

**D-005 touches `fnb.temperature_checkpoint`**, built today — temperature class is exactly what
that table's `kind` and safe range express. Check before designing a second one.

## K. The 139 `realWork` rows — the actual remaining backlog

From the completed 410-row build check. Full detail in
`scratchpad/partial-build-check.jsonl` (410 rows, cited).

| n | Theme |
|---:|---|
| 23 | **BI dashboard authoring and visual library** — formatting pane, filter-pane types, cross-highlighting, interaction editor, presentation and mobile modes, calc functions, funnel and waterfall. *This is section I* |
| 18 | **F&B back-office boards** — Menu & Product Command Center tiles, PLU master nav, POS layout preview, pre-publish validation, KDS view selector |
| 16 | **Ticket-catalogue board chrome** — saved views, column chooser, freshness stamp with timezone, capability legend |
| 11 | **Procurement and spend analytics** — savings/cost-avoidance KPIs, budget-vs-actual, scenario planner. `Supplier` carries no country, category or rating |
| 10 | **Reporting NFRs and QA plan** — the 2s/2s/5s p95 targets, security-context-aware cache keys, and four *"QA test plan shall verify…"* rows. **The package holds no test-plan artefact at all** |
| 7 | **Offline-operations dashboard** — sync success/failure tiles, duration buckets, switch-event log |
| 6 | **Retail store management** — no Retail Command Center or Store Management screen exists; `listOutlets` takes only `venueId` and `kind` |
| 6 | **Alerts outside the closed `MetricSource` enum** — contract expiry, transfer overdue, coupon expiring, shift handover. **One fix, not six** |
| 4 | **Capacity hierarchy and precedence** — `effectiveLimit`/`bindingLevel`/`limitingLevel` return zero hits anywhere. Only single-level containment exists |
| 25 | Validity exceptions · publish-readiness detail · counted pagination · bulk assignment · warehouse capacity · atomicity · header controls · 7 singletons |

**Three are decision reversals, not tickets** — the build has already chosen the opposite and
someone must reverse a stated position first:

- **Counted pagination** (5 rows) — `_components.yaml:165`: *"Cursor pagination, never offset. Offset drifts under concurrent writes."* A visible range and total need a count the build refuses to produce.
- **Atomic bulk edit / rollback** (3 rows) — `inventory.yaml:352`: *"Partial failure is reported, not rolled back."*
- **Theme toggle** — themes are audience-driven by decision, per `rtl-and-theming.md:65`.

**Two counts are inflated by ingestion, not by shortfall.** 76 of the 410 come from one document
(the dashboard visualisation spec), and two packs were never carried into the build at all
(`Retail_Backend_Structure`, `F&B Dashboard Screens`). **Roughly half the F&B and Retail
`realWork` traces to those two missing ingestions** — so ingest them before sizing that work.

### Where the build is ahead of the matrix, commercially

| What | Why it matters |
|---|---|
| **`InventoryHold`** ✓ `catalogue.yaml:11405` | Per-workstation lease with TTL, `parentLeaseId` for edge sub-leasing, partial grants, auto-return on expiry. **This is the mechanism that prevents offline overselling, it is fully designed, and a prior pass scored it a High-severity gap on two rows** |
| `getWalletLiability` `wallet.yaml:1241` | Stored-value liability **and breakage** by venue, tenant, currency. Breakage is revenue recognition; the matrix asks only for after-the-fact reporting |
| `ChannelCapacity.oversellAllowance` / `oversellBasis` ✓ `catalogue.yaml:11153` | Deliberate oversell as a yield lever, explicitly separated from the admission gate |
| `SeatHoldType.releaseRule: onSelloutThreshold` `seating.yaml:2550` | Automatic inventory migration on sell-out — called a gap by the matrix-only pass |
| `ConfigurationProfile` `tenancy.yaml:367` | Fleet-wide POS configuration profiles; resolved nearly the whole POS-configuration block alone |

### What to distrust in the 139

1. **A screen-cited `traceability` verdict is weaker than a contract-cited one.** `implementation.status` is information-free (all 2,427 screens read `notStarted`) and **859 of P08's 1,182 screens carry their own `gaps` block** saying the pack names actions the screen declares no operation for. The evidence string always says which kind of citation it is.
2. **Only 145 of the 410 are `decision_status: Agreed`** — 238 are `Noted`, 25 `Proposed`. A `realWork` verdict here is a candidate, not a commitment.
3. **Visualisation rows are the least reliable**, because three layers of the package disagree on chart types.
4. `screens/_patterns.yaml:117-124` is stale — it claims the four dashboard-authoring screens and `deleteDashboard` do not exist. ANL-021–030 were added on 19 September and `deleteDashboard` is at `reporting.yaml:1199`. **No verdict rests on that note**, but the note should be fixed.

---

## L. Delivery slice — tables the first release reads that nothing writes (23 September)

Found by `tools/derive-delivery-slice.py`. The slice covers the four first-release platforms plus their setup, 436 of 2,082 operations. A service cannot reach 1.0.0 while it reads a table no operation creates.

| # | Table | Read by | Missing | Service |
|---|---|---|---|---|
| L1 | ~~`identity.principal_credential`~~ | `login` | **Closed 23 Sep.** `changeOwnCredential` on POS-000 lets a new member of staff replace the temporary secret at first sign-in. `resetPrincipalCredential` (MFA step-up) is on BO-053. The lineage now records that `createPrincipal` writes the credential | Identity |
| L2 | ~~`orders.ticket_template`~~ | `printTicketProof`, `issueWalletPass` | **Closed 23 Sep.** `listTicketTemplates`, `createTicketTemplate` and `updateTicketTemplate`, plus `printTicketProof`, are on BO-346 | Order |
| L3 | ~~`platform.denomination`~~ | `listDenominations` | **Closed 23 Sep.** `setDenominations` is region-scoped, on BO-1065. It replaces one currency's list and deactivates rather than deletes. It also removed a stray `count` from `Denomination`, which had made every note definition demand a drawer count | Tenancy |
| L4 | ~~`orders.group_booking`~~ | `getGroupBooking` | **Closed 23 Sep.** `createGroupBooking` and `updateGroupBooking` are on BO-026. Group bookings are created by staff, so in the slice this table now counts as fed by Back Office trading | Order |
| L5 | 15 more | — | Mostly child lines written inside the parent operation, which the lineage omits (`retail.sale_line`), or totals derived from movements (`inventory.stock_level`). **Lineage fix, not contract fix.** `platform.tenant` is written by provisioning in the control plane | — |

| L6 | 20 setup operations (**7 White Labelling closed 23 Sep**: banners and promo blocks on CMS-008; content pages and the footer on CMS-007; 13 remain) | — | **A screen.** These make first-release data exist, but no screen calls them, so today they are reachable only through the API. **White Labelling, which is in scope:** `createBanner`, `updateBanner`, `createPromoBlock`, `updatePromoBlock`, `deletePromoBlock`, `updateContentPage`, `setFooter`. **Others:** `createModifierGroup` (F&B modifiers), `commitCatalogueImport`, `cloneProduct`, `bulkChangePrices`, `restoreProductVersion`, `createUpsellRule`/`deleteUpsellRule`, `updateBundle`, `setPromotionVariants`, `createInvitationCampaign`, `ingestKnowledgeDocument`, `setFxProvider`, `setSuggestionProvider`. Full list: the Gaps sheet of `handoff/service-docs/TICVAI_First_Release.xlsx` | several |
| L7 | Three White Labelling CMS screens wired to the wrong domain | — | **Rewire, including the layout.** CMS-004 Logo & Assets calls the **maintenance** equipment register (`listAssets`, `setAssetStatus`…) where its purpose is logos and icons: `getAppIcons`/`setAppIcons` exist. CMS-018 Consent & Legal calls **guest CRM** (profiles, loyalty, merge) where its purpose is consent notices: `listPolicies`/`setPolicy`/`setConsentPurposes` exist. CMS-001 Tenant Workspace calls subscription and billing where its purpose is "what is live": `getTenantAppStatus`, module enablement and feature toggles exist. The client Development Plan describes the intended screens. **Until rewired, the delivery slice wrongly counts 7 maintenance and 11 CRM operations as White Labelling work** | WhiteLabel |

In addition, 14 tables are **fed by other platforms' trading**: gate scans, work orders, gift-card issue and resource bookings. The first-release screens reading them ship with empty states until those platforms are built. This is known and expected, not a defect.

---

## M. Development Plan review, and the fixes it led to (23 September)

A review of the client Development Plan raised five points. What was done, and what is still open:

| # | Item | State |
|---|---|---|
| M1 | ~~Module switching ignores the licence~~ | **Closed.** `white-label.yaml` says a module that is not licensed cannot be enabled, but `getModuleEnablement` and `setModuleEnablement` read only `whitelabel.module_enablement`. Both now also read `subscription.contract`, `subscription.plan` and `control.licence_add_on`, the tables `getTenantLicences` reads (hand-mapped lineage). The slice grew from 437 to 441 operations, and from 41 to 42 setup screens |
| M2 | ~~Two operations with no lineage~~ | **Closed.** `relinquishSeatHold` (POS Seat Map) and `relinquishCustomDomain` (White Labelling) are DELETEs, so derivation found no table. They are hand-mapped to `seating.seat_hold` and `whitelabel.custom_domain`. White Labelling is now 67 of 67 operations ready, POS 140 of 141 |
| M3 | ~~"Each service keeps its own data"~~ | **Closed.** The review read the migration order and cross-schema keys as contradicting that sentence, and took CF-161 to be open. **CF-161 closed on 3 September: one database per tenant, schemas inside it, not per service.** The sentence was the error. It now says each service owns its own area of the data |
| M4 | ~~Migration file names in a client document~~ | **Closed.** The table of 30 migrations is out of the Development Plan and Build Readiness. The client sees "30 reversible database changes, applied in dependency order". The list lives in `TICVAI - Backend Build Plan.xlsx`, which goes to developers only |
| M5 | ~~Readiness arithmetic and the unnamed "further screen"~~ | **Closed.** Readiness is shown as counts ("140 of 141 operations"), rounded down. Outstanding items are named from the data, never typed |
| M6 | ~~POS Reports relies on AI, and the plan did not say~~ | **Closed in the document.** `askReportingQuestion` reads `ai.policy` and `ai.provider`. Each platform now has an "Also relies on" line. **Still open:** team.json says Kalpita has "no AI work in the first release", but AiService has 9 operations in it, held by the backend developers |
| M7 | Wave 1 branding | **Needs Chinmay to confirm.** The plan now says Wave 1 venues are branded by Softlabs during setup, and self-service branding follows in Wave 2. That is a commitment to the client |
| M8 | Duplicate White Labelling screens | **Partly closed.** ADM-016 and ADM-017 are Softlabs' admin versions of venue screens, now labelled "(Softlabs administration)". **Open:** CMS-005 Theme Editor is a subset of CMS-003 Typography, and CMS-004 Logo & Assets overlaps CMS-002 Brand Kit. Merging them is a screen-spec change and needs a decision |
| M9 | Guest Web at 100% while wireframe feedback is out | **Closed in the document.** The web and mobile sections say the design review is open and that ready to build means specified, not signed off |

Also fixed the same day: the Client Questions workbook is regenerated on every refresh and flags the 9 of 32 questions the first release needs. Only one of the 577 provisional operations is in the first release: `setReaderScannerPeripheral` on Till Configuration.

---

## N. Block A in OpenProject, and what the first pull showed (23-24 September)

Block A is in OpenProject project 153 (`ticvai`): 24 epics, 133 features, 659 tasks and 2,000 sub-tasks, with every parent/child link checked against the task sheet. How to do it right next time is in `handoff/service-docs/OPENPROJECT-PUSH.md`.

| # | Item | State |
|---|---|---|
| N1 | ~~"Follows" links through the API take a day~~ | **Closed.** OpenProject 10 stores every derived connection (its typed_dag closure), so each API link re-walked the graph: ~40 s a link and rising. Implied links (A>C when A>B>C) are dropped, giving 1,770 links with exactly the same 9,865 ordering pairs. Feature-level links were rejected: 49,807 waits not in the plan, and one loop. The last 1,474 went in on the server through `tools/op-bulk-links.rb` in 94 s |
| N2 | ~~Pulled tickets said "nothing is linked"~~ | **Closed.** ADAM keeps ticket links in its own `artefact_link` table, and the push never wrote any. `tools/adam-links.py` builds 17,124 from the package (operations, services, tables, screens) and `viewer/api/load_links.py` loads them on the ADAM server. #20354 now pulls its contract, two tables, service and two screens. Loaded on the ADAM server on 24 September |
| N3 | ~~One-line ticket descriptions~~ | **Closed.** All 2,816 written on the server on 24 September (3.6 s), then `updated_at` moved so the API stops serving its cached copy. `tools/op-descriptions.py` writes a full brief per ticket: contract details, tables, screens, a "Done when" list and the plan. `tools/op-descriptions.rb` writes them on the server without 2,816 notification emails. The push script now uses the same builder, so new tickets are created with them |
| N4 | ~~Features looked empty in the list~~ | **Closed.** `per_page_options` is now 20, 100, 500, 3000. The list pages 20 or 100 rows and only nests children on the same page. Shared views 396 "Hierarchy (all levels)" and 397 "Hierarchy (to tasks)" exist; `per_page_options` needs 500 and 3000 added on the server |
| N5 | ~~`listPurchaseOrders` defines no error responses~~ | **Closed 24 September by rule:** shared errors are implicit (api-conventions 5); 1,609 of 2,113 operations list none, correctly. Only `200`. Worth a sweep: list operations across the contracts with no 4xx responses |
| N6 | ~~Venue-scoped lists and tenant-level orders~~ | **Closed 24 September:** a venue sees its own rows, not tenant-level ones; head office sees all (naming-and-style 5.3). The ltree RLS already enforces it. **Side finding, fixed the same day:** on tables that carry `venue_id` instead of `scope_path`, `venue_in_scope` hid tenant-level rows from everyone. A null `venue_id` is now visible only to a grant equal to the tenant root (`platform.scope` row with `level = 'tenant'`); venue, region and brand grants still do not see it, and no grant sees nothing (tools/derive-ddl.py) |
| N9 | ~~Control database's `venue_in_scope` reads a table it does not have~~ | **Closed 24 September.** The control database has no scope tree, so its RLS file now carries no venue functions or policies; `control.usage_record` (the cross-tenant billing log) is listed there as operator data, guarded by who may connect. `check-migrations` exempts control tables scoped only by `venue_id` |
| N10 | ~~One database holding several tenants~~ | **Closed 24 September by failing closed.** `venue_in_scope` shows a null-venue row only while the database holds exactly one tenant root; with two or more it hides such rows rather than show them to every head office |
| N7 | ~~DDL drifts from `naming-and-style.md`~~ | **Closed 24 September.** `scope_path` and every `*_scope_path` is `ltree` (266 columns) with GiST indexes, and `in_scope` no longer casts (tools/derive-ddl.py). Currency: the standard now says amounts resolve their currency (ADR-0018); no columns added. Names: 27 money columns renamed to say gross, net or list price, via `x-ticvai-column`, API names unchanged (`handoff/money-column-names.md`). N5 and N6 are written into `api-conventions.md` section 5 and `naming-and-style.md` 5.3 in all seven copies |
| N8 | ADAM's contract lookup hid parameters and responses, and the agent took it as the truth | **Fixed; needs the ADAM deploy, then /update-adam.** The agent on #20354 reported "no parameters apart from status, no item schema"; the contract has `supplierId`, `PageSize`, `PageCursor` and `Page` of `PurchaseOrder`. It also claimed the table has no RLS; `920-row-level-security.sql:208` applies it. Cause: an operation's index node kept only the schemas it points at. `viewer/lib/indexer.mjs` now adds its parameters, responses and request body (in the detail layer). And every pulled ticket's README now has "Before you report a gap": check the source with adam_contract / adam_file and say what was checked. Connector build `d36a4effe13a` |

---

## Why `Partial` was 66.8% — and what is left of it

**The movement.** Absent −1,011, Covered +685, Partial +301. A third of what left Absent did not
reach Covered; it landed here. Partial is the destination for *"found the area, not the specific
thing"*, which is precisely what the sighted pass produces when it locates a capability inside a
1,299-character row without reaching the clause that settles it.

**It is arithmetically expected, not a finding.** The two documents are written at different
altitudes. A matrix row is a contractual obligation at capability level — *"provide procurement
dashboards"*. An extracted requirement is a UI atom: a column, a tile, a filter, a button, at
roughly 92 per board page. One matrix row legitimately spans dozens of board requirements, and
every one of those scores Partial. **A high Partial rate is what comparing a contract to a design
looks like when both are correct.**

**It is a residual bucket doing two incompatible jobs**, which is why the number alone is
useless — see E2.

**The defect that collapsed Absent is still operating inside Partial.** An adjudicator who finds
the row but not the buried clause scores Partial — correct on their evidence, wrong in fact. The
same rows that defeated the blind pass (C5) are still depressing verdicts here, just less
visibly.

**That prediction held.** The third pass re-checked Partial at scale and it collapsed as expected:
**82% of all 7,819 requirements are now obliged or built, 564 rows are open, and 410 (5.8%) still
carry unresolved Partial verdicts** — checked against the matrix, never against the build. On the
observed rate roughly 80% of those would land as traceability too.

**The trajectory is the finding, not the final number.** Three passes, each overturning the last,
every correction in the same direction: 79% not-covered → 17% → 2.4% Absent. Not because the
passes were careless but because **the matrix is better than a search suggests and badly filed**.
A number that has moved three times in one direction has not finished moving — which is why E2
stays open and why C5 is the item that stops this recurring.

---

## If only three things get done

**E1** — the one remaining High, and it decides whether an outlet can sell offline. The contract
and the minutes say opposite things, and the contract has built on its answer twice.

**D-001 to D-008** — 98 rows closed by eight decisions, and D-002 is I1 reached independently.

**C5** — the matrix that defeats search. Unlike everything else on this list it compounds: every
estimate, test plan and coverage question asked against that matrix inherits the error, and
re-running the analysis does not fix it. Three passes have now demonstrated that.
