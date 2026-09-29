# AI functions review: build every AI function now, then let it learn

> **For:** the product owner and the project manager
> **Date:** 29 September 2026
> **Question (product owner):** "The thing about data driven AI. We still have to build it right. Just it starts getting more accurate with time. The thing is this does not fit well for customers. Think of a way we can sort this. Check each AI functionality again which is not part of current build and why and how can it be done."
> **Data:** `ai-functions-review.json` in this folder, one entry per capability.
> **Status:** A proposal. Nothing in the package has been changed.

## The answer in brief

- **Every AI function can ship inside the six months and be useful on day one.** Each one starts from a baseline: the venue's own settings, the UAE calendar, the weather, and starting patterns that TICVAI ships for each venue type. As the venue trades, the answer shifts to the venue's own data. Later, a model trained on that data runs in the background. It goes live only when it proves better and an admin approves it.
- **No customer sees "this comes later".** They see "Learning your venue", and each answer shows what it is based on.
- **Extra work against the 29 September plan: about 2,220 points.**
  - About 445 points of developer work: operations, screens and back-end engineering. That is about 4.5% of Block B.
  - About 37 AI-engineer weeks of engine work, about 1,780 points at the plan's pace.
- **People: add one AI engineer from 7 December (S4).** Two AI engineers have about 35 weeks in Block B. The new approach needs about 50.
- **Move the configuration assistant and the analytics assistant back into the six months.** Neither needs any history. The configuration assistant was also the client's first AI priority (14 and 17 August).
- **What still cannot happen by 2 April:** a trained model *live* for any tenant. The code for every model ships. But promoting a model needs about a season of that tenant's own data, and a model must never be switched on without that proof.

## 1. The problem, in the package today

Most of the "data-driven AI" is already specified as rules-first. The trouble is that the rules themselves need history. The contract says so plainly:

- `requestSuggestion` answers **422 InsufficientDataProblem** when a venue has less than the minimum history for that kind of question. The minimums run from 8 weeks (demand forecast, staffing, anomaly) to 90 days (upsell, segmentation, menu engineering, send time). Only `price` needs no history.
- `requestSuggestion` is **already in Block A**. It is bound to Block A screens: BO-005 (queue balancing), GST-031 (prep plan and upsell), BO-115, BO-117 and WEB-044. So a new tenant would get refusals on Block A screens for weeks. That is exactly the message the product owner wants gone.
- The design's first-week forecast uses "the same weekday over 8 weeks, or a sister venue". A new venue with a single site has neither.
- There is **no operation to import a venue's own historical sales or attendance**. The forecast definition has **no cold-start setting**.

The client's own books already ask for the answer. The forecasting book (p.27, "New Venue / New Product Problem") asks for similar-venue, category, business-provided and rules baselines, with reduced confidence, and for the screen to say "Limited historical data". The fraud book's "Cold Start" section, the recommendation book's "Cold Start" screen and the upsell book's four-phase cold-start strategy all say the same thing.

## 2. The pattern: baseline, then learn

One shared layer is built once and used by every data-driven function.

| Piece | What it is | Size |
|---|---|---|
| **Estimator interface** | Each question has three producers behind the same contract: **prior** (settings + starting patterns + calendar + weather), **statistical** (own data, pulled toward the prior until there is enough), **learned** (a per-tenant model, background first). The routing already exists (`setSuggestionProvider`, the forecast `producer`, the release pointer). | 1.5 AI-weeks |
| **Maturity on every answer** | Stage (Starting, Learning, Established, Trained on your data), what it is based on, how much of it is own data, what the next stage needs | in the above |
| **Venue AI profile** | Entered at onboarding: capacity, opening hours, typical weekday and weekend attendance, peak months, average spend, F&B attach rate, staff productivity. The configuration assistant can ask for it in conversation. | 0.5 AI-weeks, 2 ops, 1 screen |
| **Historical import** | The venue's own CSV, POS and ticketing exports (12–36 months if it has them), mapped and checked, then loaded into the AI data only. It is never written into the ledger. | 1.5 back-end weeks, 3 ops, 1 screen |
| **Starting-pattern packs** | One pack per venue type: water park, theme park, family entertainment centre, museum, arena, zoo/aquarium. Each has month curves, day-of-week shape, the UAE calendar (Sat–Sun weekend, public holidays, Ramadan and Eid by Hijri date, school holidays, summer heat for outdoor venues), default fraud rules and default staff productivity. **Written by TICVAI from published sources and made-up example curves. No other tenant's data is used**, because models are per tenant (AI-D01, AIP-149). | 1.5 AI-weeks |
| **Weather and calendar signals** | The weather API is already agreed with its cost (AI-D10) | in the plan |
| **Per-tenant training and backtest job** | Retrains weekly, checks the model against past data, runs it in the background next to the live answer | 2.5 AI-weeks |
| **Promotion rule** | When the background model passes its test, the system raises a "ready to promote" governance alert and the admin promotes it. It never switches itself (AI-D16). | 0.5 AI-weeks |
| **Basis and maturity display** | One shared UI component for every AI screen, plus an "AI maturity" page | about 40 + 11 points |

**How the weight moves from the starting pattern to own data.** The statistical producer blends the two: estimate = (k × starting value + n × own average) / (k + n). Here n is the number of own observations and k is how much the starting value is trusted, for example 4 same weekdays. It is re-estimated every night and each run is recorded as a new version. This is not the "online learning" the design rules out (design 3.5), because no model ever switches itself. The design already allows it: "the statistical producers improve on their own" (design 3.12).

**What the customer sees on every AI answer:**

- a "Based on" chip, for example *"Based on: your venue profile, UAE calendar, weather, 23 days of your sales"*;
- a stage badge: Starting, Learning, Established, or Trained on your data;
- a range or band where it applies, never a bare percentage (design 5.6);
- "Limited historical data" while the starting pattern still carries more than half the weight.

**The maturity ladder**, the same shape everywhere:

| When | Behaviour | Switch |
|---|---|---|
| **Day 1** | Answers from the starting pattern; wide range; "Starting" | — |
| **~4 weeks** | Weekly patterns and short-range answers come mostly from own data; accuracy is measured and shown; "Learning" | Automatic, recorded |
| **~3 months** | Own level and trend lead; the starting pattern only fills gaps, such as a holiday not yet seen; "Established" | Automatic, recorded |
| **A season** | The trained model runs in the background for at least 6 weeks. If it beats the current answer (forecast: at least 10% smaller error at 7 days, bias within ±3%, range covers 70–90% of actuals; fraud: at least as many frauds caught with 20% fewer false alarms; recommendations: wins a controlled experiment), the admin is asked to promote it | **Admin decides** (AI-D16) |

Importing 12 months or more of a venue's own history moves day one straight to "Established".

## 3. Every AI function outside Block A

In total, 94 of the 133 `ai.yaml` operations are outside the Block A slice. Points use the package measure: 2.1 per back-end operation, screens by the package formula, and engine work in engineer-weeks at 48 points a week (Block A's pace of 9.6 points per developer-day). "Extra" means extra against the 29 September plan.

| Capability | Ops outside Block A | Screens outside Block A (points) | Why it was left out | Really no data? | How day one works | Extra points | Sprint |
|---|---:|---|---|---|---|---:|---|
| **Shared baseline-then-learn layer** | 7 new | 3 new + UI component (51) | Not in the plan | — | See section 2 | 450 | S2, S3, S6, S7 |
| **Forecasting** | 9 | 13 (34) | "Data-dependent AI waits" | Partly: only the trained model needs data | Venue profile × venue-type month curve × UAE calendar × weather, with bookings on hand as a floor; wide range | 196 | S3–S6; model S8 |
| **Operational requirements, staffing** | 1 | 11 (27) | Follows forecasting | No | Forecast ÷ default productivity per role (editable) | 24 | S5 |
| **Operational suggestions** (16 kinds) | 2 | 2 (6) | 422 below the minimum history | Partly | A starting answer for every kind; 422 only when a setting is missing | 74 | S2 (Block A kinds), S5 |
| **Queue and wait time** | 1 | 0 | Needs 30 minutes to 14 days of readings | No | People ahead ÷ configured ride capacity | 24 | S5 |
| **Anomaly detection** | 4 | 3 (6) | Moved past month 6 | Partly | Default thresholds, plus "actual against forecast" | 134 | S6 |
| **Analytics assistant, metric explanation** | 0 (already in Block A) | 6 (16) | Moved past month 6 for capacity | **No** | Full function over whatever data exists | 208 | S7 |
| **Fraud and risk** | 12 | 4 (14) | "Trained fraud models wait" | Partly: only the classifier needs data | Fraud-rule template per venue type, speed-of-activity limits, payment-provider signals; lets payments through and puts suspect ones on hold | 168 | S4, S6; model S8 |
| **Approval-request scoring** | 2 | 1 (2) | Not stated | No | Rules on the amount, limits and separation of duties | 24 | S7 |
| **Recommendations and personalisation** | 3 | 60 (135, already in the plan) | "Trained recommendation models wait" | Partly | Relationship map, business priority and context (party, time, weather, capacity) | 168 | S5–S7; model S8 |
| **Marketing recommendations, lookalikes, send time** | 2 | 5 (13, already in the plan) | Needs 90 days | Partly | Rule playbooks, lookalikes by guest attributes, a typical send hour per channel | 72 | S7 |
| **Dynamic pricing suggestions** | 0 (+1 new kind) | 2 (4, already in the plan) | "AI part depends on forecasting" (19 Aug) | Partly | Bookings against the forecast suggest a step within the venue's price bands; a person approves | 50 | S7 |
| **Configuration assistant** | 9 | 32 (77) | Moved past month 6 for capacity | **No** | Full function | 432 | S3–S5, S8 |
| **Seat-map and layout generation** | 4 | 4 (9) | Grouped with the configuration assistant | **No** | Full function; a person approves every map | 161 | S6 |
| **Translations** | 1 | 1 (2) | Block A in the plan, but missing from the slice | No | Full function | 28 | S2 |
| **Planner agent** | 0 (no operation exists) | 1 (3; GST-054 is deferred) | Block A in the plan, but missing from the package | No | Full function | 7 | S2 |
| Action pipeline | 11 | 11 (28) | Sequencing (B1) | No | Full function | 0 | S3–S4 |
| Knowledge administration | 7 | 3 (6) | Sequencing | No | Full function | 0 | S5 |
| Governance and gateway remainder | 13 | 7 (21) | Sequencing (B3) | No | Full function | 0 | S2 for 3 ops, then B3 |
| Models and evaluation | 3 | 0 | Sequencing (B3) | No | Full function | 0 | S6 |
| Monitoring (incl. "ready to promote" alerts) | 9 | 8 (23) | Sequencing (B3) | No | Full function | 0 | S6–S7 |
| Decision records and audit | 4 | 10 (21) | Sequencing (B3) | No | Full function | 0 | S6 |
| **Total** | **97** (94 ai + 3 in other contracts) | | | | | **≈ 2,220** | |

**The pattern in the "Why" column.** The only reason that is truly about data is the *trained model*. Every "waits for data" item also has a useful day-one version. The two assistants, the seat-map generation and the platform pieces were left out for capacity or sequencing, not for lack of data.

## 4. Each capability in short

Each entry gives what it does, how day one works, how it grows, and the one sentence the customer is told. Operation lists, screen ids, owners and risks are in the JSON.

**Forecasting (C8).** Tells managers how many guests, sales and how much revenue to expect, with a range and a what-if simulator. Screens: ADM-499..507, ANL-008, ANL-057, BO-926, BO-931. ADM-508, BO-919 and BO-927 are already in Block A.
- *Day 1:* the venue profile × the venue-type month curve × UAE calendar effects × weather. Bookings on hand act as a floor. The range is about ±40%.
- *Growth:* by week 4 its own weekly shape and booking pace take over, and accuracy is shown as "measured". By month 3 it uses seasonal smoothing on its own data. After a season, a trained model runs in the background and is promoted by the admin.
- *Build:* the starting-pattern producer and a cold-start setting (1 week, extra), the statistical producer (6 weeks, in the plan), the trained model (3 weeks, extra).
- *Who:* the second AI engineer; Pranay for the operations.
- *Customer:* "Forecasts are available from day one based on your venue profile, the calendar and the weather; they tighten as your own sales come in, and the screen always shows the range and what it is based on."

**Operational requirements and staffing.** Forecast ÷ a productivity standard per role (covers per staff hour, sales per till hour, scans per lane per hour). The defaults come from the starting-pattern pack and the venue can edit them. Measured productivity takes over after about 4 weeks of recorded shifts. It is a recommendation a person accepts.
- *Customer:* "Staffing and resource suggestions start from standard productivity figures you can edit, and switch to your measured figures as shifts are recorded."

**Operational suggestions (the 16 `requestSuggestion` kinds).** Every kind gets a starting answer:
- replenishment = par level − stock on hand + forecast use over the supplier lead time;
- prep plan = forecast covers × menu mix;
- menu engineering = ranked by margin, with popularity marked "learning";
- SLA target = a standard default;
- send time = the typical hour for the channel;
- waste risk = shelf life and par level against the forecast.

The existing minimum-history figures become the point where own data takes over, not a refusal. **Fix this in S2**, because the queue-balancing, prep-plan and upsell kinds sit on Block A screens.
- *Customer:* "Suggestions work from the first day using your settings and standard figures, and say so; they switch to your own history as it builds."

**Queue and wait time.** Wait = people ahead ÷ throughput. Until 30 minutes of throughput have been measured, it uses the ride capacity the venue configured. The queue forecast rides on forecasting.
- *Customer:* "Wait times show from opening on your first day using each attraction's capacity, and become more exact as the day's real throughput is measured."

**Anomaly detection (C9).** Screens ANL-055, 058, 059.
- *Day 1:* default thresholds the venue can edit (refund rate, void rate, cash variance), plus "attendance below the forecast's low end".
- *Growth:* a per-weekday baseline from week 4, and a seasonal baseline and comparison across the tenant's own venues by month 3. A model only where a KPI raises too many false alarms.
- *Customer:* "Unusual movements are flagged from the first week against the limits you set and against the forecast; the system learns what is normal for your venue over the following weeks."

**Analytics assistant and metric explanation (C6).** Screens ANL-009, 051, 052, 053, 054, 056.
- *Day 1:* full function. The model writes a query specification. Reporting compiles and runs it, so the model never sees raw data (AI-D15).
- `explainMetricChange` breaks a change down by channel, product and time with plain arithmetic, and the model only words the result.
- With little history it compares with the last 7 days and says so. Imported history makes year-on-year possible.
- *Customer:* "You can ask questions about your venue's numbers in plain language from the first day; every figure comes from your own reports, with the query shown."

**Fraud and risk (C10).** Screens ADM-633, 637, 638, BO-1160.
- *Day 1:* a fraud-rule template per venue type, written by TICVAI. It covers the signals in the 21 September minutes: attempts, success ratio, cards per identity, refunds, reuse of expired tickets. It adds payment-provider signals and speed-of-activity counts. Payments go through and suspect ones are held (AI-D06).
- *Growth:* each customer's, device's and cashier's normal behaviour from about week 4. Linked devices, cards and accounts by month 3. A classifier trained on the analysts' confirmed cases runs in the background. Many tenants will never have enough confirmed cases, and staying on rules is fine.
- *Needs:* the five new owner events (design 3.2).
- *Customer:* "Payments are risk-scored from the first transaction using proven fraud rules for venues like yours; the scoring learns what normal looks like for your customers, and a model is only switched on when your administrator approves it."

**Approval-request scoring.** Rules on the amount against limits, separation of duties and time of day. It informs the approver and never blocks.
- *Customer:* "Approvers see why a request looks unusual from the first request, based on your approval rules."

**Recommendations and personalisation (C11).**
- *Day 1:* the relationship map, eligibility rules and business priority, plus context. For example, 2 adults and 2 children in the cart leads to a family ticket (21 September minutes). Business rules always win.
- *Growth:* take-up rates start from the configured relationship strength and learn from every offer shown. Popularity by time of day from week 4. "Bought together" patterns once the minimum-support thresholds are met, around month 3. After a season, a ranking model is tested in a controlled experiment and the admin promotes it.
- *Customer:* "Offers at checkout follow your own product rules from day one and learn which add-ons your guests actually take."

**Marketing recommendations, lookalikes, send time.**
- *Day 1:* rule playbooks (abandoned cart, membership expiring, a slow forecast day) and lookalikes on known guest attributes. Send time uses the channel's typical hour until a guest has three touches. A propensity model comes after a season.
- *Consent:* marketing to guests who checked out without an account is still open (18 September).
- *Customer:* "Campaign and audience suggestions start from proven playbooks and your guests' known attributes, and sharpen as campaign results come in."

**Dynamic pricing suggestions.**
- *Day 1:* if bookings run ahead of the forecast's high end, the assistant suggests a price step inside the venue's price band. If they run behind the low end, it suggests a promotion. A person approves every price change (18 September minutes).
- Price sensitivity cannot be learned until prices have actually varied. Automatic pricing stays off by governance.
- *Customer:* "Price suggestions start from day one by comparing bookings with the forecast, always inside your price bands and always approved by a person."

**Configuration assistant (C7).** 9 operations and 32 screens (ADM-469..498, BO-597, BO-598).
- *Day 1:* full function. It needs no history.
- It is also the natural place to collect the venue AI profile during onboarding.
- *Needs:* the action pipeline (B1) before its execute step, and "validate-only" on the first 15 tool operations in the owning services.
- *Customer:* "You can set up venues and products by describing what you want; the assistant asks what is missing and nothing is applied until you approve it."

**Seat-map and layout generation.** `generateVenueLayout`, `proposeSeatMapChanges`, `proposeVenueLabels`, `proposeWalkways`.
- *Day 1:* full function. A person always previews and approves the map (21 August decision).
- BO-093 is in Block A without its labelling operation.
- *Customer:* "Upload your venue plan and get a proposed seat map to correct and approve, instead of drawing it by hand."

**Translations and the planner agent.** Both are Block A in the plan but missing from the package. `proposeTranslations` is not in the slice. `ai.yaml` has no planner operation, and GST-054 is on the deferred list. Add both in S2.

**Platform pieces** (action pipeline, knowledge administration, the rest of governance, models, monitoring, audit). None of them needs data. Three need to come earlier:
- the decision point and spend (`evaluateAiGovernance`, `getAiUsage`, `getAiPolicy`) belong in Block A;
- the "ready to promote" alerts, the release path and the decision records must work by S6–S7, or no model can be promoted and no stage can be shown before 2 April.

## 5. Sprint plan and people

| Sprint | Kalpita Mejari (AI) | Second AI engineer (from 2 Nov) | Proposed third AI engineer (from 7 Dec) | Back-end |
|---|---|---|---|---|
| S1 5–23 Oct | Gateway, governance, concierge (Block A) | — | — | Block A slice |
| S2 26 Oct–13 Nov | Help me choose, translations, planner agent | Estimator interface, maturity block, first starting answers for the Block A suggestion kinds | — | Hrushikant: contract change (no 422, maturity); decision point and spend into Block A |
| S3 16 Nov–4 Dec | Block A close-out; configuration assistant discovery | Starting-pattern packs, venue profile, forecast starting producer, weather and holidays | — | Deep: historical import; Hrushikant, Pranay: action pipeline (B1) |
| S4 7–25 Dec | Configuration assistant blueprint | Forecast statistical producer | Fraud scoring and rule templates | Tanmay: Orders scoring call; Deep: owner events |
| S5 28 Dec–15 Jan | Configuration assistant plan and execute | Staffing, suggestion kinds, queue | Recommendation runtime | Hrushikant, Deep: validate-only on 15 tools |
| S6 18 Jan–5 Feb | Seat-map and layout generation | Anomaly; training, backtest and background-run job | Fraud: normal-behaviour baselines, links between devices and cards, alerts, cases; "bought together" patterns | Monitoring alerts, releases, decision records |
| S7 8–26 Feb | Analytics assistant, metric explanation | Promotion rule; marketing AI | Pricing suggestions, approval scoring, recommendation experiments | Hrushikant: Reporting compile |
| S8 1–19 Mar | Configuration assistant for the other modules | Trained forecast model, in the background | Trained fraud classifier and ranking model, in the background | — |
| S9 22 Mar–2 Apr | Tests, hardening; stretch: AI dashboard and report generation | Backtests on imported pilot history | Tests, hardening | — |

**Capacity.**

- Two AI engineers have about 35 weeks in Block B, after the holidays (about 7 working days).
- The new approach needs about 50. The plan as it stands needs about 15 for these capabilities.
- **A third AI engineer from S4 closes the gap, with no slack.**
- Block A's own AI list is already about 13 AI-weeks against about 10 available. If Block A overruns, S3 slips a sprint.
- The developers' extra (about 445 points) is about 4.5% of Block B's 9,850. That is about half a developer over Block B. Re-check it at the 23 October pace measurement.

**Without a third AI engineer**, the least harmful slip is the trained models: forecast, fraud and ranking, 9 AI-weeks together. They would finish, running in the background, around May–June 2027. No customer would notice, because no tenant can pass a promotion test before then anyway. But this breaks the product owner's rule that everything is built within the six months, so it is the fallback, not the plan.

## 6. The two assistants: bring them back?

**For bringing them back into the six months:**
- Neither needs any history. The design says both work fully in week one (design 3.12). They were moved for capacity, not data.
- The configuration assistant was the client's **first** AI priority: "the priority AI use case for phase one is a configuration assistant" (14 August minutes). Qossai on 17 August: "seating maps and the ticket configuration". Also CF-57.
- It collects the venue profile that makes every other AI function useful on day one. It is part of the fix, not an extra.
- `askReportingQuestion` and `explainMetricChange` are **already in the Block A slice** (POS-008, BO-029, KIT-010, ANL-019). The analytics assistant mostly wraps what is already being built.
- The plan marks the phase-2 message "to be told to the client". Taking it back costs nothing with the client.

**For keeping them deferred:**
- About 640 points: configuration about 432, analytics about 208. Seat-map (161) and anomaly (134) usually travel with them.
- "Validate-only" in the owning services is work across teams.
- AI engineer capacity is short even without them.

**Recommendation: bring both back.** The configuration assistant goes in S3–S5, seating and ticketing first, as the scope paper proposed. Seat-map generation goes in S6 and the analytics assistant in S7. The only S9 stretch is AI dashboard and report generation (AIP-186/187). It does not need data; it needs the assistant proven first.

## 7. What still cannot ship by 2 April, and why

1. **A trained model live for any tenant.** Promotion needs about a season of that tenant's data and a 6-week background run, or 12 months or more of imported history. The code for every model ships. Promotion then happens tenant by tenant.
2. **The fraud classifier going live.** It needs analyst-confirmed cases. Many tenants never reach enough and stay on rules.
3. **The ranking model going live.** It needs a controlled experiment with enough traffic.
4. **Price sensitivity and AI-set prices.** They need prices that have actually varied. Automatic pricing is off by governance until there are six months of evidence at the approval level.
5. **Not data questions, unchanged:**
   - external knowledge connectors (data residency);
   - partner cross-sell (the integrations do not exist);
   - in-venue location triggers (the signals are not governed);
   - OTA and reseller recommendations (AI-D08);
   - models pooled across tenants (AIP-149).

None of these shows the customer a missing feature. Each one sits behind something that already works.

## 8. Package gaps to fix before tickets

Fix these in the pre-ticket re-audit (plan decision 9):

1. `requestSuggestion` refuses without history on Block A screens (BO-005, GST-031). Narrow the 422 to missing *settings* and add the maturity block.
2. Six operations in the Block A slice have no producer behind them in the plan: `runForecast`, `publishForecastVersion`, `createForecastScenario`, `decideOperationalRequirement`, `explainMetricChange`, `decideAiInsight`. With the starting-pattern producer they work; without it those screens show nothing.
3. Translations and the planner agent are Block A in the plan, but missing from the slice and from `ai.yaml`. GST-054 is deferred.
4. BO-093 (Block A) has no `proposeVenueLabels`.
5. `evaluateAiGovernance`, `getAiUsage` and `getAiPolicy` are not in the slice.
6. `team.json` still says Kalpita has "no AI work in the first release", and the AI operations sit with Hrushikant and Sanket.
7. There is no historical import operation, and `AiForecastDefinition` has no cold-start setting.

Changing `ai.yaml` means re-deriving the derived files and the mirrors (derive before check).

## 9. What the customer is told

> Every AI feature is on from your first day. It starts from your venue profile, the UAE calendar, the weather and patterns for venues like yours, and it learns your venue as you trade. Every answer tells you what it is based on. When a model trained on your own data does better than the starting method, your administrator is asked whether to switch it on.

**The honest risk.** In the first weeks the starting pattern can be wrong for an unusual venue. That is why:
- the range is wide and shown;
- the basis is always visible;
- the venue can correct its profile;
- nothing that changes money, prices or configuration happens without a person.

## Sources read

- `ticvai/docs/active/six-month-plan-29-september.md`
- `ticvai/docs/architecture/ai-system-design.md` (sections 3.5, 3.10, 3.12, 5.1, 7, 8)
- `ticvai/handoff/ai-decisions.json`
- `ticvai/contracts/satellite/ai.yaml` (133 operations; SuggestionKind, SuggestionBasis, AiForecastDefinition)
- `ticvai/handoff/delivery-slice.json` (39 ai operations in the slice)
- `ticvai/handoff/service-docs/tasks.csv`
- `ticvai/screens/P*.yaml` (screen points by the formula in `tools/build-service-docs.py`)
- `ticvai/docs/active/ai-scope-for-confirmation.md` and `team.json`
- `ticvai/sources/mom-decisions.json`
- The minutes of 14 August, 18 September and 21 September
- The design books: AI Forecasting (p.27), AI Fraud & Risk ("Cold Start"), Recommendation & Personalization ("Cold Start"), Upsell/Cross-Sell (the cold-start strategy, "Minimum Data Threshold"), Core AI Platform, AI Configuration Assistant

**How the points were worked out.**
- Back-end operations: 2.1 points each.
- Screens: the package formula.
- Engine work: rough engineer-weeks from the design's section 7, adjusted, then converted at 48 points a week. The per-operation measure prices endpoints, not engines.
- All figures are rough and should be re-based on the 23 October pace measurement.
