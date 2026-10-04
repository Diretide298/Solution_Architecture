# WS162 — Resource Management Configuration board 8

**10 screens · 16 operations · 21 schemas · 4 permissions**

Platform P08 Venue Management · ships as **venue-management** ·
staff audience · web ·
online only

## Who this is for

**staff on web.** Everything below is how you know what is
true. **None of it is the subject.** The subject is the person in front of the screen and the one
thing they came to do.

## What to build

**A working surface, not a drawing of one.** Two references, both built from these same sources:

- `sources/designs/TICVAI_Mobile.dc.html` — 54 screens in one navigable file, 133 animations,
  a live seat map, a five-stage payment flow. **This is the bar for finish.**
- `sources/designs/TICVAI_POS_Terminal_client_approved.html` — the client-approved POS build. **This is the bar for operator density.**

`sources/designs/ticvai-motion-and-interaction.md` names every mechanism in them. Open them and
match their depth. Do not describe them, read them.

## The one rule that outranks the rest

**Nothing in this bundle may appear as text a user can read.** Not an operation id, not a schema
field name, not a permission key, not a screen id, not a file path, not a finding reference.

A homepage that prints `getTenantAppStatus → listProducts` under its header, or labels a column
`venueId · scopePath`, has published its own homework. It happened on `WEB-001`: four products on
sale and not a single price on the page, because the build rendered what `listProducts` returns
instead of what a guest wants — a photo, a name, a price, and a way to book.

**The test: would the person this screen is for understand every word on it?** If a line would
confuse them, it is spec leakage, not design. `bindsTo` tells you what data to invent
convincingly. It is never a caption.

## What is in this folder

| file | what it is |
|---|---|
| `BUNDLE.md` | **The one file to hand a design session.** This brief; then **Screen by screen**, a full specification of each screen (what the user enters and picks, what it shows and produces, every state, who may do what, the requirements it meets, what the client said about it in the meetings, the tracker items, what the tenant configures, the references and an acceptance checklist); then what applies to the whole batch; then the raw data. |
| `screens.json` | Every field of every screen in the batch, as the package holds it. `machine` is what a screen is *in the middle of*; `overlays` is what opens over it and what closing it does; `navigation.transitions` is how you leave, with `carries` naming the state that travels. |
| `operations.json` | Method, path, parameters, request and response schema for every operation these screens call. Write fetches against these; do not invent endpoints. |
| `schemas.json` | The data those operations carry, resolved one level deep. **Seed from these.** The prototype hardcodes 57 models and every one corresponds to a schema here — a build that invents its own will disagree with the backend on day one. |

## Rules that are not style preferences

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `AI_CONFIGURE, AI_USE, RESOURCE_VIEW, WORKFORCE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.
- **How input should be, how output should be.** Each screen's block in `BUNDLE.md` says, field by
  field, the control, whether it is required, its default, its limits and allowed values, its format
  and its error; and, element by element, what is shown and in what format, what each action
  produces and where the user goes next. Draw exactly that.

## The processes these screens belong to

Written by the owner of each process (`handoff/design-notes/`). Read before any screen: it says how the process runs end to end and which words the screens must use.

### Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue)

Venue operations is everything that happens after a sale and inside the gates. A guest's ticket is one virtual ticket with interchangeable media (QR, dynamic QR, RFID wristband, NFC, Face Pass or Face Tag); at an access point a scanner (P07, or the scan function inside the Staff App P06) validates the media against the admission profile and the guest admission policy, offline if it must, and every deny carries a reason and a next action. The back office (Venue Management P08) configures that estate: the venue topology (venue, park, zone, attraction, access point, gate and lane, device placement), admission profiles and rules (entry, exit, re-entry, anti-passback, validity, crossover, companions), credential security (dynamic QR, device binding, beacons), biometrics, gate modes, and the live operations, fraud and monitoring views. Accreditation (P08 setup and review, P11 web portal for applicants, web first) takes an applicant from a configurable form through document checks, OCR, duplicate blocking and multi-level approval to a credential with zone rights. Resources and capacity manage bookable resources (rooms, vehicles, equipment, cabanas, instructors) that are booked as a consequence of selling a product, never sold directly. Workforce covers shift templates, rosters, attendance, swaps and breaks, mirrored on the Staff App. Maintenance and safety cover the asset register, preventive calendars, work orders with scored priority, inspections and incidents, with technicians working from the Staff App. Games and rides configure readers, credit types and consumption priority, play entitlements, game pricing, retry pricing, redemption and the card lifecycle. The virtual queue (Q1) gives a guest a live wait time and a return window for a ride; it is not the on-sale waiting room (Q2). Every calendar has day, week and month views. Configuration resolves tenant, region, venue (outlet only for F&B and retail), and a user's permissions, never the device, decide what they may do. The guest apps (P01, P02) show the guest's side of this: My Tickets, the scan code, Face Pass, wait times, the virtual queue, map booking of cabanas and the visit planner.
*(source: F06 step 1 / F112 step 1 / F111 step 1 / ADR-0002 / ADR-0012 / ADR-0018 / ADR-0041 / ADR-0066 / ADR-0067 / ADR-0068 / DI-652 / DI-627 / DI-640 / DI-654 / DI-666 / DI-482 / DI-483 / DI-907 / DI-919 / DI-923 / DI-865 / DI-678 / TRACKER Actions row 160 / MoM 2026-09-02 AccessControl / MoM 2026-09-07 …)*

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Ticket | The one virtual record a guest owns (ticket number, product, validity, entries). Its number never changes, whatever media carries it or whoever it is transferred or resold to. | Pass (unless the product is a pass), Booking, Order line | DI-652 / DI-620 / contracts/spine/access.yaml#/components/schemas/TicketStatus |
| Media | What the ticket is presented by at a gate (QR code, dynamic QR, wristband/RFID card, NFC, Face Pass, Face Tag). One ticket can carry several media as fallbacks; a media code can also cover several tickets scanned as one group. Show one … | Credential (for guest media; keep Credential for accreditation badges and staff), Ticket code | DI-180 / DI-608 / DI-652 |
| Access point | A place where a scan is judged, with a fixed direction (entry, exit, re-entry, crossover). Hierarchy shown to users is Venue > Park > Zone > Attraction > Access point > Gate/lane > Device. | Scanner (that is the device), Door | screens/P08-venue-back-office.yaml#BO-144 / … |
| Admission profile | The named set of rules an access point enforces (opening window, entries, exit scan, re-entry, validity, crossover). Products point at a profile; tiers such as Bronze/Silver/Gold are profiles with gate allow and deny lists. | Admission rules (as a screen title), Access rule set | DI-185 / contracts/spine/access.yaml#/components/schemas/AdmissionRules |
| Admitted / Denied / Overridden | The three scan outcomes. A denial is always shown with its reason in plain words and a next action; an override is a supervisor admitting despite a denial, and is always attributed and reasoned. | Valid/Invalid, Success/Fail, Error | contracts/spine/access.yaml#/components/schemas/ScanOutcome / … |
| Used | A ticket entry is used the moment a scan succeeds, whether or not the guest physically passed. Mistakes are resolved from the scan history, not by un-scanning. | Redeemed (for admission), Checked in (that is group check-in, a different step) | DI-627 / TRACKER Actions row 221 / TRACKER Actions row 189 |
| Gate mode | What a lane is doing now, set live by the podium or supervisor - Normal, Free flow (counts, does not validate), Drop arm (everybody through, evacuation), Closed (nobody through), Podium (staff validating by eye), Maintenance. Direction is … | Turnstile mode (as a label for direction), Open/Locked | contracts/spine/access.yaml#/components/schemas/AccessPointOperatingMode / R221 |
| Offline package | What a scanner holds to validate with no network - entitlements, blacklist, admission profiles and the active guest admission policy version - with its age always visible. | Cache, Local DB | F06 step 3 / ADR-0068 |
| Sync and reconciliation | Sending the offline scan journal to the server, and the duty manager's review of scans the server rejected after the device had already admitted the guest. | Upload, Retry | F06 step 6 / DI-065 |
| Face Pass / Face Tag | Face Pass is the long-lived face credential for members and season-pass holders (renewable); Face Tag is short-lived, for one day or event. Retention is set per tier by the venue. | Face ID, Biometric login | DI-640 / ADR-0063 |
| Accreditation / Credential (accreditation) | Accreditation is the application and approval of a person (media, contractor, corporate, staff of a partner) for an event or season; the credential is what is issued after approval (photo badge, QR or RFID) with zone access rights. | Registration (for the whole process), Ticket | DI-654 / DI-662 |
| Resource | A bookable thing or person a product needs (room, vehicle, cabana, equipment set, instructor). Guests buy products; resources are assigned to the booking, pre-assigned or dynamically. | Asset (that is maintenance), Inventory (that is stock) | DI-475 / DI-482 / TRACKER Actions row 160 |
| Asset | A physical item maintained by the venue (ride, turnstile, printer, pump) with a register record, documents, warranty and maintenance history. | Resource, Device (unless it is an IT device in the device register) | DI-910 / ADR-0067 |
| Work order | A unit of maintenance work, lifecycle Created > Assigned > In progress > Review > Closed, with a resolution timer. | Ticket (reserved for guest tickets), Job card | DI-231 |
| Game / attraction (games module) | In the games and rides module an attraction is an individual game or ride (roller coaster, racing game, bumper cars), not a venue. | Venue, Park | DI-863 |
| Virtual queue / Return window | A guest's place in a ride's queue held without standing in line, with a return window (for example 4:50 to 5:00 PM) that recalculates live. Distinct from the walk-in line and the VIP/express lane, and from the on-sale waiting room. | Waiting room, Fast pass (that is the express product), Booking | DI-675 / DI-678 / DI-679 / ADR-0066 |
| Wait time source | Where a ride's wait time comes from - Sensor, Throughput, Manual, or Unavailable - always shown beside the number. | Live (when the source is manual) | contracts/satellite/queue.yaml#/components/schemas/WaitTimeSource / DI-315 |

### AI & Intelligence

AI in TICVAI is one governed engine behind many screens. The guest meets it as Sahli, the concierge (WEB-044, GST-031, GST-033), as the planner agent that refines a rules-built day plan by chat (GST-054), and as upsell and cross-sell offers on a separate Extras step (WEB-008, GST-048). Staff meet it as the Staff App's AI tab (EMP-019/020, knowledge EMP-040/041), the kiosk assistant (KSK-015) and the support copilot (SUP-006, SUP-018). Venue managers meet it in Venue Management (BO-091 policy and spend, BO-919/BO-925..932 resource and staffing forecasts, BO-597/598 configuration drafts, BO-772/782 marketing optimisation, BO-793 translations, BO-970/975 seat-map generation, BO-1048 seat upsell, BO-1160 fraud cases) and in Analytics (ANL-010 suggestions, ANL-019 management insights, ANL-055 anomalies, ANL-057 forecasting studio, ANL-059 insight history, ANL-060 governance, ANL-071 AI maturity). The governance, configuration-assistant, forecasting, oversight, audit and monitoring boards sit on the TICVAI Console (P09: ADM-037 providers, ADM-469..498 configuration assistant, ADM-499..518 forecasting, ADM-519..558 governance, ADM-633/637 fraud, ADM-680..697 recommendation governance). Five rules hold on every one of these screens. (1) Baseline first, then it learns per tenant: every data-driven answer (forecast, suggestion, risk score, recommendation) exists from day one, from the venue AI profile, a starting pattern for the venue type, the UAE calendar and the weather, and shifts to the venue's own data as it trades; nothing says "comes later" or refuses for lack of history - a refusal only names a missing setting. (2) Every answer shows its basis and maturity: a "Based on" line, a stage badge (Starting, Learning, Established, Trained on your data), "Limited historical data" while the starting pattern carries more than half the weight, ranges or bands rather than a bare percentage, a confidence only where the producer really has one, a plain-words explanation always. (3) A trained model replaces the baseline only when it beats it in a shadow run of at least six weeks and an admin promotes it; the platform raises "Ready to promote" and never switches by itself. (4) The LLM never reads raw data: numbers come only from query results the platform runs (the answer shows the query), only the masked prompt and retrieved context leave the platform, and AI only drafts - the owning screen applies. (5) One autonomy scale, L0 Disabled to L4 Controlled auto, with first-release ceilings, separate from user permission and from the approval tier; impactful actions route to a person, who sees current against proposed, impact, risk and what is affected, and can approve within a limit, challenge, override or roll back; every decision is traceable (data, model, approver, time) and searchable by customer, venue and capability. In Block A (5 October to 20 November 2026) the guest concierge with retrieval, Help me choose, translations, the planner agent, the gateway and …
*(source: ADR-0051; ADR-0050; ADR-0020; ADR-0052; ADR-0053; ADR-0054; ADR-0059; ADR-0051 (AI-D01..AI-D20); ADR-0051 (AI functions review 30 Sep §2 §4 §9); MoM 18 Sep 4.1-4.10; MoM 21 Sep 4.1-4.14; MoM 30 Sep 4.1 4.7; ADR-0059 (Block A slice: tasks.csv))*

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Sahli | The guest concierge's name; the entry reads "Ask Sahli" and shows as mascot art when the venue's Concierge mascot setting is on (default), otherwise a plain button. | Chatbot, Bot, AI Concierge (as a visible label), Virtual agent | DI-1069 / screens/P01-guest-web-storefront.yaml#WEB-044 |
| Based on | The line on every AI answer that says what it was computed from, e.g. "Based on: your venue profile, UAE calendar, weather, 23 days of your sales". Always present. | Data sources, Model inputs, Powered by AI | ADR-0051 Maturity / contracts/satellite/ai.yaml#/components/schemas/AiMaturity |
| Starting / Learning / Established / Trained on your data | The four maturity stages (enum starting, learning, established, learned), shown as one badge. Moves by itself from Starting to Established as own data arrives; Trained on your data only after an admin promotion. | Beta, Experimental, Low confidence, Cold start (in UI), Not enough data | ADR-0051 / ADR-0051 (AI functions review 30 Sep §2) |
| Limited historical data | Shown while own data carries less than half the weight (AiMaturity.limitedHistory, ownDataShare < 0.5). An honest qualifier, never a refusal. | Insufficient data, Not available until, Comes later | ADR-0051 / contracts/satellite/ai.yaml#/components/schemas/AiMaturity |
| Range | The 10th-90th percentile band a forecast or estimate is shown with (e.g. "1,850-3,400 guests, most likely 2,600"). Never a bare accuracy percentage on an answer; measured accuracy (WAPE, bias, coverage) appears only on accuracy screens … | Accuracy 92%, Confidence 0.87 (on a heuristic), Exact | ADR-0051 / contracts/satellite/ai.yaml#getForecast / … |
| Running in the background | A trained model in shadow next to the live answer (AiRelease.stage shadow); it changes nothing a person sees. | Live, Active model, Testing in production | ADR-0051 Promotion / ADR-0051 (AI functions review 30 Sep §2) |
| Ready to promote / Promote | A shadow model passed its gate (governance alert promotionReady); an admin promotes it one stage at a time (canary, then production). The only way a model replaces the baseline. | Deploy, Go live, Auto-switch, Activate model, Upgrade AI | ADR-0051 (AI-D16) / contracts/satellite/ai.yaml#promoteAiRelease |
| L0 Disabled / L1 Advisory / L2 Prepare / L3 Execute with … | The one autonomy scale for every AI capability, shown as "L2 Prepare" etc. with the capability's ceiling beside it. Lower scopes tighten, never raise. | Autopilot, Copilot mode, Level 0-3 (CFG book), Approval level (for autonomy), Manual/Semi/Auto | ADR-0050 / ADR-0050 (AI-D04) / … |
| Approval tier | How many people must approve a proposed action (ProposedAction.approvalLevel, 1 or 2). Not an autonomy level. | Autonomy level, Approval level (ambiguous) | ADR-0050 |
| Suggestion / Draft | What AI produces. A suggestion advises; a draft is a ready-to-review change that a person applies in the owning screen. Copy says "Nothing is applied until you approve it." | AI changed, Auto-applied, AI updated your prices | ADR-0020 / ADR-0051 (AI functions review 30 Sep §4 Configuration assistant) / … |
| Why this? | The link or expander that opens an answer's explanation (Suggestion.explanation, recommendation template reason, decision trace). Plain words; for guests a template reason. | Explainability, SHAP, Feature importance (in operator copy) | ADR-0052 (AI-D09) / contracts/satellite/ai.yaml#/components/schemas/Suggestion |
| No thanks | The explicit decline on an offer. Only this counts as a decline and it is remembered across channels; scrolling past or closing the step is not a decline. | Dismiss (as a decline), Skip (as a decline), X (as a decline) | ADR-0052 (AI-D07) / DI-962 / … |
| Hold for review | What a high fraud or risk score does to a payment or order. The transaction goes through; it is held for a person. | Decline, Block, Reject (for a risk score), Fraud detected | ADR-0053 / ADR-0053 (AI-D06) |
| Hand over to a person | The concierge passes the whole conversation and its own summary to a live agent; the guest does not repeat themselves. | Escalate, Transfer, Contact bot | contracts/satellite/marketing-crm.yaml#handoverToAgent |
| Not available yet | The analytics assistant's answer to a question outside the semantic model; it records a knowledge gap and never improvises a number. | I cannot answer, Error, Unknown | ADR-0054 |


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `BO-923` | AI Resource Intelligence Command Center | D | 0 | 26 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-924` | Optimal Resource Recommendation Engine | D | 0 | 0 | 6 | 3 | 0 | 0 | — | notStarted (—) |
| `BO-925` | AI Staff Recommendation & Workforce Matching | D | 0 | 0 | 6 | 19 | 0 | 0 | — | notStarted (—) |
| `BO-926` | Resource Demand Forecasting | D | 0 | 6 | 6 | 46 | 0 | 0 | — | notStarted (—) |
| `BO-927` | AI Staffing Requirement Forecast | A | 17 | 16 | 6 | 47 | 1 | 0 | — | notStarted (—) |
| `BO-928` | AI Conflict Resolution Assistant | D | 0 | 0 | 6 | 15 | 0 | 0 | — | notStarted (—) |
| `BO-929` | Automatic Schedule Optimization | D | 0 | 0 | 6 | 12 | 0 | 0 | — | notStarted (—) |
| `BO-930` | Alternative & Replacement Resource | D | 0 | 0 | 6 | 3 | 1 | 0 | — | notStarted (—) |
| `BO-931` | Operational Scenario Simulator & Digital Twin | D | 0 | 0 | 6 | 1 | 0 | 0 | — | notStarted (—) |
| `BO-932` | Conversational AI Resource Copilot | D | 0 | 0 | 6 | 16 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-923, BO-924, BO-925, BO-926, BO-929, BO-930, BO-931, BO-932 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-923` AI Resource Intelligence Command Center

**Provide management with a centralized AI-generated overview of current and future resource conditions across the organization.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-923 |
| Who uses it | venue staff holding `RESOURCE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/ai-resource-intelligence-command-center-bo-923` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The AI view of resources for managers: readiness, today's and forecast utilisation, predicted shortages and excess, staffing and equipment gaps, conflicts, overtime and maintenance risk, and the recommendations awaiting a decision, over a chosen horizon (Live, Today, Tomorrow, 7 days, 30 days). Its centre is the daily brief. The one thing to get right: every recommendation shows its confidence, the factors and constraints behind it, and waits for a person.

**Known correction pending (do not draw the wrong version)**

- **The twelve KPIs and Time Horizons are drawn as columns of a table titled "Every resource intelligence"** Why: KPIs are tiles; time horizon is a control (VO-R02). *(source: screens/P08-venue-back-office.yaml#BO-923; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Only listResources is bound** Why: Forecasts, gaps, insights and recommendations need the AI reads (listOperationalRequirements, listAiInsights, listProposedActions) plus utilisation and the calendar's conflicts. *(source: contracts/satellite/ai.yaml#listOperationalRequirements / contracts/satellite/ai.yaml#listAiInsights / contracts/satellite/ai.yaml#listProposedActions / MATRIX 1.2.57; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Cabana · Lounger · Locker · Wheelchair · Stroller · Equipment · Room · Auditorium · Vehicle · Instructor · Staff · Table … | `listResources` ?kind |
| Available from | date and time picker | — | — | `listResources` ?availableFrom |
| Available to | date and time picker | — | — | `listResources` ?availableTo |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Time horizon**: Segmented Live / Today / Tomorrow / 7 days / 30 days / Custom; all tiles and the brief follow it. *(source: screens/P08-venue-back-office.yaml#BO-923 / screens/P08-venue-back-office.yaml#BO-924)*

#### Outputs: what the screen shows and produces

**Shown**

**Every resource intelligence** (data table)

| Shows | Format | Notes |
|---|---|---|
| Resource readiness | text | not in the schema: `Resource readiness` |
| Today's utilization | text | not in the schema: `Today's utilization` |
| Forecast utilization | text | not in the schema: `Forecast utilization` |
| Predicted shortages | text | not in the schema: `Predicted shortages` |
| Predicted excess capacity | text | not in the schema: `Predicted excess capacity` |
| Staffing gaps | text | not in the schema: `Staffing gaps` |
| Equipment gaps | text | not in the schema: `Equipment gaps` |
| Resource conflicts | text | not in the schema: `Resource conflicts` |
| Overtime risk | text | not in the schema: `Overtime risk` |
| Maintenance risk | text | not in the schema: `Maintenance risk` |
| AI recommendations awaiting action | text | not in the schema: `AI recommendations awaiting action` |
| Estimated optimization opportunity | text | not in the schema: `Estimated optimization opportunity` |
| Time horizons | text | not in the schema: `Time Horizons` |

**The selected resource intelligence** (detail panel): The pack groups this record's detail under its own headings: “Users shall switch between”, “Underutilized”, “Overutilized”, “Shortage Risk”, “Resources affected by”.

| Shows | Format | Notes |
|---|---|---|
| Resource readiness | text | not in the schema: `Resource readiness` |
| Today's utilization | text | not in the schema: `Today's utilization` |
| Forecast utilization | text | not in the schema: `Forecast utilization` |
| Predicted shortages | text | not in the schema: `Predicted shortages` |
| Predicted excess capacity | text | not in the schema: `Predicted excess capacity` |
| Staffing gaps | text | not in the schema: `Staffing gaps` |
| Equipment gaps | text | not in the schema: `Equipment gaps` |
| Resource conflicts | text | not in the schema: `Resource conflicts` |
| Overtime risk | text | not in the schema: `Overtime risk` |
| Maintenance risk | text | not in the schema: `Maintenance risk` |
| AI recommendations awaiting action | text | not in the schema: `AI recommendations awaiting action` |
| Estimated optimization opportunity | text | not in the schema: `Estimated optimization opportunity` |
| Time horizons | text | not in the schema: `Time Horizons` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI tiles**: Resource readiness %, Today's utilisation, Forecast utilisation, Predicted shortages, Predicted excess capacity, Staffing gaps, Equipment gaps, Conflicts, Overtime risk (hours), Maintenance risk, Recommendations awaiting action, Optimisation opportunity (AED) - metric tiles with deltas (VO-R02). Forecast tiles carry a "Forecast" tag and data freshness. *(source: screens/P08-venue-back-office.yaml#BO-923)*
- **Resource health**: Donut - Fully resourced, At risk, Underutilised, Overutilised, Unavailable - each opening the list. *(source: screens/P08-venue-back-office.yaml#BO-923 / screens/P08-venue-back-office.yaml#BO-924)*
- **AI daily brief**: Expected attendance, readiness, staffing gaps, equipment shortages, overtime at risk, optimisation in AED, and the top recommendation with confidence, why (factors), constraints checked and expected impact ("Zone A coverage 87% to 100%"). *(source: screens/P08-venue-back-office.yaml#BO-924 / screens/P08-venue-back-office.yaml#BO-932)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Review / Accept / Reject a recommendation**: Accept goes through the autonomy level for that action type (user confirmation, approval required); executed actions are logged as AI-initiated (VO-R11). *(source: screens/P08-venue-back-office.yaml#BO-932)*
- **Board tiles**: Recommendation engine (BO-924), staff matching, demand forecast, staffing forecast, conflict assistant, schedule optimisation, alternatives (BO-930), scenario simulator, copilot. *(source: screens/P08-venue-back-office.yaml#BO-923)*

**Data it reads**: `listResources` (onLoad, Resources at this venue)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-924` Optimal Resource Recommendation Engine: *Optimal Resource Recommendation Engine*
- → `BO-925` AI Staff Recommendation & Workforce Matching: *AI Staff Recommendation & Workforce Matching*
- → `BO-926` Resource Demand Forecasting: *Resource Demand Forecasting*
- → `BO-927` AI Staffing Requirement Forecast: *AI Staffing Requirement Forecast*
- → `BO-928` AI Conflict Resolution Assistant: *AI Conflict Resolution Assistant*
- → `BO-929` Automatic Schedule Optimization: *Automatic Schedule Optimization*
- → `BO-930` Alternative & Replacement Resource: *Alternative & Replacement Resource*
- → `BO-931` Operational Scenario Simulator & Digital Twin: *Operational Scenario Simulator & Digital Twin*
- → `BO-932` Conversational AI Resource Copilot: *Conversational AI Resource Copilot*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource intelligence list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource intelligence untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource intelligence yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the resource intelligence are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Forecast not yet published for the horizon**: Forecast tiles show "No forecast for 30 days" and the brief covers only what is known. *(source: contracts/satellite/ai.yaml#listOperationalRequirements)*
- **AI capability paused by governance**: Banner "AI recommendations are paused at this venue"; live tiles still show. *(source: contracts/satellite/ai.yaml#pauseAiCapability)*

#### Consistency with other screens

- Match `BO-952`: The executive AI centre uses the same recommendation card (evidence, confidence, benefit, risk).
- Match `EMP-003`: The employee "AI Insight" line comes from the same insights.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
horizon: Tomorrow - Sun 11 Oct 2026
tiles:
  readiness: 94%
  predictedShortages: 5
  overtimeRisk: 18 h
  opportunity: AED 3,450
brief: 'Expected attendance 8,420; readiness 94%; 5 staffing gaps (14 people); 2 equipment shortages; 18 overtime
  hours at risk; AED 4,200 potential labour saving. Top: reallocate 4 instructors from Ski Zone B to Ski Zone A
  14:00-17:00 (confidence 96%).'
```

#### Permissions

- `listResources` → `RESOURCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-923` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS133 Resource Management Configuration Board 8.dc.html#bo-923`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 8
- Flow F271 *Resource Management Configuration board 8: AI Resource Intelligence Command …*, step 1: Opens AI Resource Intelligence Command Center → Provide management with a centralized AI-generated overview of current and future resource conditions across the organization.
- Flow F271 *Resource Management Configuration board 8: AI Resource Intelligence Command …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F271 *Resource Management Configuration board 8: AI Resource Intelligence Command …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F271 *Resource Management Configuration board 8: AI Resource Intelligence Command …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F271 *Resource Management Configuration board 8: AI Resource Intelligence Command …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F271 *Resource Management Configuration board 8: AI Resource Intelligence Command …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F271 *Resource Management Configuration board 8: AI Resource Intelligence Command …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F271 *Resource Management Configuration board 8: AI Resource Intelligence Command …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F271 branch at step 1 (expected): when Nothing has been set up on AI Resource Intelligence Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F271 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-923?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-924`, `BO-925`, `BO-926`, `BO-927`, `BO-928`, `BO-929`, `BO-930`, `BO-931`, `BO-932`.
- [ ] Every gated control is gated: `RESOURCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-924` Optimal Resource Recommendation Engine

**Recommend the best available resource for any operational requirement.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-924 |
| Who uses it | venue staff holding `RESOURCE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/optimal-resource-recommendation-engine-bo-924` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Given a requirement (Private ski instructor, 11 Oct 14:00-15:00, Arabic-speaking, Level 3+), the ranked candidates with the facts behind each (available, Level 3, Arabic, same venue, certification valid, no overtime), a recommended one and alternatives, and "Why this resource?". The one thing to get right: recommendations come from rules (attribute match and the venue's scoring policy), so the explanation is a list of checked facts and weights, never "the AI thinks".

**Known correction pending (do not draw the wrong version)**

- **The screen has no components at all and the gap note says nothing is drawable** Why: The pack gives request inputs, fourteen evaluation factors, a worked recommendation and an explanation panel. *(source: screens/P08-venue-back-office.yaml#BO-924; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **suggestResources returns resources with no score or reason, and takes no venue, capacity or certification parameter** Why: The ranking and "Why this resource?" have no source; the screen's name promises AI while 26 August chose attribute matching. *(source: contracts/satellite/resources.yaml#suggestResources / DI-495 / MATRIX 1.2.53; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Requirement**: Resource type, date and time or duration, venue, capacity, skill and level, certification, equipment specification, customer preference, operational priority - shown as a requirement chip line once set. *(source: screens/P08-venue-back-office.yaml#BO-924)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Recommended and alternatives**: Tabs Recommended / Alternatives; cards with photo, name, level, languages, fact ticks and a score from the scoring policy; Select on each. *(source: screens/P08-venue-back-office.yaml#BO-924 / contracts/satellite/resources.yaml#getResourceAllocationPolicy)*
- **Why this resource**: Expands to the evaluated factors (availability, skills, certifications, capacity, venue and transfer time, utilisation, current assignments, cost, maintenance status, dependencies, preference) with the weight each contributed. *(source: screens/P08-venue-back-office.yaml#BO-924 / screens/P08-venue-back-office.yaml#BO-925)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Select**: Returns the resource to the calling flow (booking, assignment); nothing is booked from this screen alone. *(source: designer default)*

**Where the user goes next**

- → `BO-923` AI Resource Intelligence Command Center: *Back to AI Resource Intelligence Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The optimal resource recommendation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the optimal resource recommendation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No optimal resource recommendation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the optimal resource recommendation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Only candidates that fail a mandatory rule**: "No eligible resource" with the rule that excludes each, never a low-scored ineligible suggestion. *(source: screens/P08-venue-back-office.yaml#BO-902)*

#### Consistency with other screens

- Match `BO-898`: Same card; this screen adds the scoring explanation.
- Match `BO-901`: Scores come from that policy.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
requirement: Private ski instructor - Sun 11 Oct 2026 14:00-15:00 - Arabic - Level 3+ - Summit Peaks
recommended:
  name: Maria Santos
  score: 97
  facts: Available, Level 3, Arabic, same venue, certification valid, no overtime
alternatives:
- Ahmed Al Mansoori 91 - 6 h worked today
- Omar Haddad 82 - other venue, 40 min transfer
```

#### Permissions

- `suggestResources` → `RESOURCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.53 | AI shall recommend optimal resources. | Ticketing Catalogue | CONTRACTED | `suggestResources` |
| 1.2.54 | AI shall recommend suitable staff based on skills and availability. | Ticketing Catalogue | CONTRACTED | `suggestResources` |
| 1.2.56 | AI shall propose alternatives for scheduling conflicts. | Ticketing Catalogue | CONTRACTED | `suggestResources` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-924` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS133 Resource Management Configuration Board 8.dc.html#bo-924`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 8
- Flow F271 *Resource Management Configuration board 8: AI Resource Intelligence Command …*, step 2: Works in Optimal Resource Recommendation Engine → Recommend the best available resource for any operational requirement.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-924?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-923`.
- [ ] Every gated control is gated: `RESOURCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-925` AI Staff Recommendation & Workforce Matching

**Provide advanced AI-assisted selection specifically for human resources. This screen consumes the staff rules established in Boards 3 and 4.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-925 |
| Who uses it | venue staff holding `AI_USE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/ai-staff-recommendation-workforce-matching-bo-925` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-014): No operation proposes named staff for a requirement.

**From the AI & Intelligence process.** Staff recommendation and matching: for a requirement or an open shift, the suggested people ranked by qualification, availability, cost and fairness rules from the resource boards. The one thing to get right: the client confirmed matching is keyword and rule matching on attributes and qualifications, not full AI - show the rules that matched, and a person assigns.

**Known correction pending (do not draw the wrong version)**

- **Declares requestSuggestion, whose kinds have no staff-matching kind (staffing is a headcount).** Why: Matching needs a workforce candidate operation; the suggestion kind staffing returns numbers, not people. *(source: contracts/satellite/ai.yaml#/components/schemas/SuggestionKind / TRACKER Actions row 156; AI & Intelligence)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Staff · POS · Kiosk · Gates · Fnb · Retail · Stock · Resource · Equipment · Facility | `listOperationalRequirements` ?kind |
| Status | select | — | Issued · Accepted · Modified · Rejected · Handed over · Expired | `listOperationalRequirements` ?status |
| From | date and time picker | — | — | `listOperationalRequirements` ?from |
| To | date and time picker | — | — | `listOperationalRequirements` ?to |
| Version | picker: choose a version | — | — | `listOperationalRequirements` ?versionId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **candidate list**: Each candidate with the qualifications matched, availability, hours this week and why ranked here; unqualified people never appear (a filled position by an unqualified person is still a gap). *(source: TRACKER Actions row 156 / contracts/satellite/workforce.yaml#getStaffingCoverage)*

**What each action does** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Assign**: Opens the assignment in Workforce; nothing is assigned here. *(source: ADR-0050 (L2 Prepare))*

**Data it reads**: `listOperationalRequirements` (onLoad, Requirements derived from the forecast)

**Where the user goes next**

- → `BO-923` AI Resource Intelligence Command Center: *Back to AI Resource Intelligence Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The staff recommendation workforce list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the staff recommendation workforce untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No staff recommendation workforce yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the staff recommendation workforce are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 A setting the answer cannot do without is missing (29 September, AI functions review). (AiMissingSettingProblem) |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
requirement: Lifeguard, Sat 17 Oct 10:00-14:00
candidates:
- name: Ahmed Al Zaabi
  matched:
  - Lifeguard L2
  - Wave pool
  hoursThisWeek: 32
- name: Priya Nair
  matched:
  - Lifeguard L2
  hoursThisWeek: 24
```

#### Permissions

- `listOperationalRequirements` → `AI_USE` (operate) · staff
- `requestSuggestion` → `AI_USE` (operate) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

19 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.6.38 | The system shall provide operational recommendations to reduce queue congestion based on forecasted demand. | F&B & Guest Management | CONTRACTED | `listOperationalRequirements` |
| 8.2.43 | System shall forecast staffing requirements by venue. | Unified Operations Dashboard | CONTRACTED | `listOperationalRequirements` |
| 8.2.44 | System shall forecast staffing requirements by department. | Unified Operations Dashboard | CONTRACTED | `listOperationalRequirements` |
| 8.2.45 | System shall forecast staffing requirements by shift. | Unified Operations Dashboard | CONTRACTED | `listOperationalRequirements` |
| 8.2.46 | System shall forecast staffing requirements by attraction. | Unified Operations Dashboard | CONTRACTED | `listOperationalRequirements` |
| 8.2.47 | System shall forecast staffing requirements based on attendance forecasts. | Unified Operations Dashboard | CONTRACTED | `listOperationalRequirements` |
| 8.2.48 | System shall forecast staffing requirements based on operational demand. | Unified Operations Dashboard | CONTRACTED | `listOperationalRequirements` |
| 8.2.50 | System shall provide staffing forecasting dashboards. | Unified Operations Dashboard | CONTRACTED | `listOperationalRequirements` |
| 2.1.28 | Kiosks shall provide an AI assistant to guide guests through ticket selection, promotions, FAQs, recommendations, and checkout. | Ticketing Sales | CONTRACTED | `requestSuggestion` |
| 4.1.16 | Analyze menu performance and profitability. | Bundles and Promotions | CONTRACTED | `requestSuggestion` |
| 4.1.19 | Recommend actions to reduce waste and spoilage. | Bundles and Promotions | CONTRACTED | `requestSuggestion` |
| 4.1.20 | Recommend pricing and promotion strategies. | Bundles and Promotions | CONTRACTED | `requestSuggestion` |
| … 7 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-925` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS133 Resource Management Configuration Board 8.dc.html#bo-925`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 8
- Flow F271 *Resource Management Configuration board 8: AI Resource Intelligence Command …*, step 4: Works in AI Staff Recommendation & Workforce Matching → Provide advanced AI-assisted selection specifically for human resources. This screen consumes the staff rules established in Boards 3 and 4.
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-925?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-923`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-926` Resource Demand Forecasting

**Predict future demand for resources before shortages occur.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-926 |
| Who uses it | venue staff holding `AI_USE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/resource-demand-forecasting-bo-926` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the AI & Intelligence process.** Resource demand forecast for the resources team: how many of each resource (carts, lockers, cabanas, equipment, staff roles) will be needed per period, from the published forecast, against what exists - before a shortage happens. The one thing to get right: historical, forecast and actual are three distinct series, and the forecast is a range from a named version with its stage.

**Known correction pending (do not draw the wrong version)**

- **DI-280 is attached.** Why: Superseded by ADR-0051. *(source: DI-280 / ADR-0051; AI & Intelligence)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Definition key | text field | — | — | `getForecast` ?definitionKey |
| Version | picker: choose a version | — | — | `getForecast` ?versionId |
| From | date and time picker | — | — | `getForecast` ?from |
| To | date and time picker | — | — | `getForecast` ?to |
| Dimension key | text field | — | — | `getForecast` ?dimensionKey |
| Scenario | picker: choose a scenario | — | — | `getForecast` ?scenarioId |
| Kind | select | — | Staff · POS · Kiosk · Gates · Fnb · Retail · Stock · Resource · Equipment · Facility | `listOperationalRequirements` ?kind |
| Status | select | — | Issued · Accepted · Modified · Rejected · Handed over · Expired | `listOperationalRequirements` ?status |
| From | date and time picker | — | — | `listOperationalRequirements` ?from |
| To | date and time picker | — | — | `listOperationalRequirements` ?to |
| Version | picker: choose a version | — | — | `listOperationalRequirements` ?versionId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every resource demand forecasting** (data table)

| Shows | Format | Notes |
|---|---|---|
| Historical | text | not in the schema: `Historical` |
| Forecast | text | not in the schema: `Forecast` |
| Actual | text | not in the schema: `Actual` |

**The selected resource demand forecasting** (detail panel): The pack groups this record's detail under its own headings: “Expected Visitors”, “Expected Lesson Participants”, “Available”, “Confidence”.

| Shows | Format | Notes |
|---|---|---|
| Historical | text | not in the schema: `Historical` |
| Forecast | text | not in the schema: `Forecast` |
| Actual | text | not in the schema: `Actual` |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **resource rows**: Resource, period, forecast need (with busy case), available, shortfall highlighted; actuals once the period has passed. *(source: contracts/satellite/ai.yaml#listOperationalRequirements / contracts/satellite/ai.yaml#getForecast)*

**Data it reads**: `getForecast` (onLoad, Forecast values); `listOperationalRequirements` (onLoad, Requirements derived from the forecast)

**Where the user goes next**

- → `BO-923` AI Resource Intelligence Command Center: *Back to AI Resource Intelligence Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource demand forecasting list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource demand forecasting untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource demand forecasting yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the resource demand forecasting are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- resource: Family cabanas
  period: Sat 17 Oct
  need: 38 (busy case 44)
  available: 40
  shortfall: up to 4
```

#### Permissions

- `getForecast` → `AI_USE` (operate) · staff
- `listOperationalRequirements` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

46 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.55 | AI shall forecast future resource demand. | Ticketing Catalogue | CONTRACTED | `getForecast` |
| 4.1.17 | Forecast demand based on historical and operational data. | Bundles and Promotions | CONTRACTED | `getForecast` |
| 5.6.26 | Predict queue lengths, wait times, peak demand, and capacity shortages. | F&B & Guest Management | CONTRACTED | `getForecast` |
| 8.2.1 | System shall forecast attendance based on historical attendance patterns. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.2 | System shall forecast attendance by venue. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.3 | System shall forecast attendance by attraction. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.4 | System shall forecast attendance by event. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.5 | System shall forecast attendance by session. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.6 | System shall forecast attendance by date range. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.7 | System shall forecast attendance by day of week. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.8 | System shall forecast attendance by month. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.9 | System shall forecast attendance by season. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| … 34 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-926` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS133 Resource Management Configuration Board 8.dc.html#bo-926`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 8
- Flow F271 *Resource Management Configuration board 8: AI Resource Intelligence Command …*, step 6: Works in Resource Demand Forecasting → Predict future demand for resources before shortages occur.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-926?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-923`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-927` AI Staffing Requirement Forecast

**Translate forecast operational demand into specific workforce requirements.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 1 · needs the `resources` module |
| Block | Block A · ticket #28941 (APP-SETUP-BO-927) |
| Who uses it | venue staff holding `AI_CONFIGURE`, `AI_USE`, `WORKFORCE_VIEW` (1 configure, 1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a configuration directory (§Configured rule) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `requirementId` (navigation), `venueId` (session) |
| Route | `/rentals/ai-staffing-requirement-forecast-bo-927` |

**From the AI & Intelligence process.** Staffing requirements from the forecast: per role and period, how many people the forecast says are needed (with the busy case), how that was worked out (forecast divided by a productivity standard), and where the rota is short. The manager accepts, modifies or rejects each requirement; accepting hands it to Workforce as a recommendation - nothing is rostered here (autonomy L2 Prepare). The one thing to get right: the standard used is visible and editable in the venue profile, because day-one standards are defaults from the venue-type pattern.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- In Block A only decideOperationalRequirement is in the slice; listOperationalRequirements and getForecast are not. (CHG-SBO-006)
- The form's example field "1 Lifeguard / 250 guests" is a concurrent ratio, while AiVenueSettings.staffProductivity is "units per staff hour". (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): The layout has an unbound dataTable, a primaryButton with no label and an inline productivity textField; no operation sets a standard here. (CHG-SBO-007).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Does an accepted requirement create draft shifts in Workforce, or only a coverage target the rota manager works to?** → Drawn default stands (answer: "Default / recommended accepted"): A coverage target (recommendation) shown on the rota; shifts are created by a person in Workforce. *(decided by Chinmay, 2026-10-02; DEC-010 / CHG-NOTE-001)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Definition key | text field | — | — | `getForecast` ?definitionKey |
| Version | picker: choose a version | — | — | `getForecast` ?versionId |
| From | date and time picker | — | — | `getForecast` ?from |
| To | date and time picker | — | — | `getForecast` ?to |
| Dimension key | text field | — | — | `getForecast` ?dimensionKey |
| Scenario | picker: choose a scenario | — | — | `getForecast` ?scenarioId |
| Kind | select | — | Staff · POS · Kiosk · Gates · Fnb · Retail · Stock · Resource · Equipment · Facility | `listOperationalRequirements` ?kind |
| Status | select | — | Issued · Accepted · Modified · Rejected · Handed over · Expired | `listOperationalRequirements` ?status |
| From | date and time picker | — | — | `listOperationalRequirements` ?from |
| To | date and time picker | — | — | `listOperationalRequirements` ?to |
| Version | picker: choose a version | — | — | `listOperationalRequirements` ?versionId |
| From | date picker | — | — | `getStaffingCoverage` ?from |
| To | date picker | — | — | `getStaffingCoverage` ?to |
| Basis | segmented control | Minimum | Minimum · Forecast requirement · Higher of both | `getStaffingCoverage` ?basis |

**Form: Decide requirement** (modal, opened by *Decide requirement*; *Decide requirement* calls `decideOperationalRequirement`, *Cancel* sends nothing)

**Collects what `decideOperationalRequirement` sends before it is called.** Required: `decision`. Optional: `quantity`, `note`. `decision` is accept, modify (with `quantity`) or reject; a person then creates the shifts (coverage target only, DEC default for BO-927). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Decision `decision` | segmented control | required | — | Accept · Modify · Reject | — | — | `decideOperationalRequirement` body |
| Quantity `quantity` | number field | optional | — | — | — | — | `decideOperationalRequirement` body |
| Note `note` | text area | optional | — | max length 1000 | — | — | `decideOperationalRequirement` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The requirement is no longer `issued` (`requirement-not-open`).

**Form: Save productivity standards** (modal, opened by *Save productivity standards*; *Save productivity standards* calls `setAiVenueSettings`, *Cancel* sends nothing)

**Collects what `setAiVenueSettings` sends before it is called.** Required: `venueId`, `venueType`. Optional: `isOutdoor`, `capacity`, `openingHours`, `typicalWeekdayAttendance`, `typicalWeekendAttendance`, `peakMonths`, `averageSpend`, `fnbAttachRate`, `staffProductivity`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `setAiVenueSettings` body |
| Venue type `venueType` | select | required | — | Water park · Theme park · Family entertainment centre · Museum · Arena · Zoo aquarium · Other | — | — | `setAiVenueSettings` body |
| Is outdoor `isOutdoor` | toggle | optional | on | — | — | Outdoor venues take the summer-heat and weather effects. | `setAiVenueSettings` body |
| Capacity `capacity` | number field | optional | — | min 1 | — | — | `setAiVenueSettings` body |
| Opening hours `openingHours` | repeatable rows | optional | — | — | — | The usual week. Exceptions come from the venue calendar. | `setAiVenueSettings` body |
| Day of week `openingHours[].dayOfWeek` | stepper or slider | optional | — | min 1; max 7 | — | — | `setAiVenueSettings` body |
| Opens at `openingHours[].opensAt` | text field | optional | — | — | — | — | `setAiVenueSettings` body |
| Closes at `openingHours[].closesAt` | text field | optional | — | — | — | — | `setAiVenueSettings` body |
| Typical weekday attendance `typicalWeekdayAttendance` | number field | optional | — | min 0 | — | — | `setAiVenueSettings` body |
| Typical weekend attendance `typicalWeekendAttendance` | number field | optional | — | min 0 | — | — | `setAiVenueSettings` body |
| Peak months `peakMonths` | list of values (chips) | optional | — | — | — | — | `setAiVenueSettings` body |
| Average spend `averageSpend` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setAiVenueSettings` body |
| Fnb attach rate `fnbAttachRate` | stepper or slider (%) | optional | — | min 0; max 1 | — | — | `setAiVenueSettings` body |
| Staff productivity `staffProductivity` | key and value settings | optional | — | — | — | Per role, units per staff hour, e.g. `{"cashier": 40, "gate": 300}`. | `setAiVenueSettings` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Rules for these inputs** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **decision (accept / modify / reject)**: Per row. Modify needs a quantity (whole people, ≥ 0) and offers a note; reject offers a reason note. Bulk accept for a day is allowed; bulk reject is not. *(source: contracts/satellite/ai.yaml#decideOperationalRequirement / designer default)*
- **productivity standard (e.g. "1 lifeguard per 250 guests", "40 transactions per cashier hour")**: Shown per role with where it came from (venue-type default, your edit, or measured from your shifts after about 4 weeks). Editing it opens the AI venue profile; it is not edited inline on each requirement. *(source: ADR-0051 (AI functions review 30 Sep §4 Operational requirements) / contracts/satellite/ai.yaml#/components/schemas/AiVenueSettings (staffProductivity))*

#### Outputs: what the screen shows and produces

**Shown**

**Staffing requirements** (data table, from `listOperationalRequirements`)

| Shows | Format | Notes |
|---|---|---|
| Subject ref | text | A role, outlet, gate, item or resource type. |
| Period start | 1 Oct 2026, 14:30 | — |
| Period end | 1 Oct 2026, 14:30 | — |
| Quantity | 1,234.5 | — |
| Quantity P90 | 1,234.5 | The requirement at the forecast's 90th percentile, for planning to the busy case. |
| Unit | text | — |
| Productivity standard | grouped details | The standard used, e.g. covers per staff hour, scans per gate per hour. |
| Status | chip: Issued, Accepted, Modified, Rejected, Handed over, Expired | — |

**The selected requirement** (detail panel, from `listOperationalRequirements`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Staff, POS, Kiosk, Gates, Fnb, Retail… | — |
| Target contract | text | The owning module that applies it: `workforce`, `fnb`, `inventory`, `resources`, `access`. |
| Decision note | text | — |
| Decided at | 1 Oct 2026, 14:30 | — |
| Handover ref | text | The owning module's record once handed over. |

**Productivity standards** (detail panel, from `getAiVenueSettings`): Standards live on the venue AI profile, not on this screen. A lifeguard ratio ("1 per 250 guests present") is a concurrent ratio, not units per staff hour; the ratio kind is a logged contract gap (CHG-SBO-005).

| Shows | Format | Notes |
|---|---|---|
| Staff productivity | grouped details | Per role, units per staff hour, e.g. `{"cashier": 40, "gate": 300}`. |
| Capacity | 1,234 | — |
| Updated at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Decide requirement (primary button) | `decideOperationalRequirement` POST `/operational-requirements/{requirementId}/decide` | inline | AiOperationalRequirement | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The requirement is no longer `issued` (`requirement-not-open`). | opens modal first |
| Save productivity standards (secondary button) | `setAiVenueSettings` PUT `/venues/{venueId}/ai-settings` | AiVenueSettings | AiVenueSettings | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **requirement rows**: Role, period (e.g. Sat 17 Oct 10:00-14:00), required quantity and busy case (quantityP90), rota coverage from Workforce and the gap ("2 short"), status (issued, accepted, modified, rejected, handed over, expired). *(source: contracts/satellite/ai.yaml#/components/schemas/AiOperationalRequirement / contracts/satellite/workforce.yaml#getStaffingCoverage)*
- **how it was worked out**: Expandable: "Forecast 2,600 guests (range 1,850-3,400) ÷ 1 lifeguard per 250 guests in the water = 11; busy case 14", with the forecast version, its stage and "Based on" line. *(source: contracts/satellite/ai.yaml#/components/schemas/AiOperationalRequirement (productivityStandard, versionId) / ADR-0051)*

**What each action does** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Accept**: Status accepted then handed over; Workforce receives a recommendation bound to the forecast version; a link opens the rota there. *(source: contracts/satellite/ai.yaml#decideOperationalRequirement)*
- **Modify / Reject**: Records the person's figure or rejection with the note; 409 if the requirement already expired or was superseded by a newer forecast. *(source: contracts/satellite/ai.yaml#decideOperationalRequirement)*

**Data it reads**: `getForecast` (onLoad, Forecast values); `listOperationalRequirements` (onLoad, Requirements derived from the forecast); `getStaffingCoverage` (onLoad, AI staffing requirement against the rota …); `getAiVenueSettings` (onLoad, The venue AI profile, where productivity standards are kept)

**Where the user goes next**

- → `BO-923` AI Resource Intelligence Command Center: *Back to AI Resource Intelligence Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The staffing requirement forecast configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the staffing requirement forecast untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No staffing requirement issued for this period yet; they appear when a forecast version is published. Offers no create action: requirements come from the forecast. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The requirement is no longer `issued` (`requirement-not-open`). |

#### Edge cases to draw

- **A newer forecast version is published after the requirement was issued**: The old requirement shows "Superseded by the forecast of <time>" and cannot be accepted; the new one appears. *(source: contracts/satellite/ai.yaml#publishForecastVersion ("operational requirements are derived from the new one"))*
- **No productivity standard for a role**: The row names the missing standard and links to the venue profile instead of a number. *(source: ADR-0051 (422 only for a missing setting))*

#### Consistency with other screens

- Match `BO-919`: Same requirement rows and forecast basis.
- Match `ADM-513`: The console's workforce forecast uses the same rows and labels.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
venue: Coastal Aqua
rows:
- role: Lifeguard
  period: Sat 17 Oct 10:00-14:00
  required: 11
  busyCase: 14
  rota: 9
  gap: 2 short
  status: issued
- role: Cashier (F&B)
  period: Sat 17 Oct 12:00-15:00
  required: 5
  busyCase: 6
  rota: 5
  gap: '0'
  status: issued
standard:
  role: Lifeguard
  value: 1 per 250 guests in the water
  from: Water-park default (edit in venue profile)
forecast:
  stage: Learning
  basedOn: your venue profile, UAE calendar, weather, 5 weeks of your sales
```

#### Permissions

- `getForecast` → `AI_USE` (operate) · staff
- `listOperationalRequirements` → `AI_USE` (operate) · staff
- `decideOperationalRequirement` → `AI_USE` (operate) · staff
- `getStaffingCoverage` → `WORKFORCE_VIEW` (read) · staff
- `getAiVenueSettings` → `AI_USE` (operate) · staff
- `setAiVenueSettings` → `AI_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

47 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.55 | AI shall forecast future resource demand. | Ticketing Catalogue | CONTRACTED | `getForecast` |
| 4.1.17 | Forecast demand based on historical and operational data. | Bundles and Promotions | CONTRACTED | `getForecast` |
| 5.6.26 | Predict queue lengths, wait times, peak demand, and capacity shortages. | F&B & Guest Management | CONTRACTED | `getForecast` |
| 8.2.1 | System shall forecast attendance based on historical attendance patterns. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.2 | System shall forecast attendance by venue. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.3 | System shall forecast attendance by attraction. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.4 | System shall forecast attendance by event. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.5 | System shall forecast attendance by session. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.6 | System shall forecast attendance by date range. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.7 | System shall forecast attendance by day of week. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.8 | System shall forecast attendance by month. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.9 | System shall forecast attendance by season. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| … 35 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- AI forecasting from historical bookings recommends staffing levels for upcoming periods (e.g. "you will need this many resources over the next week") so leave and availability can be planned. Analytics show total cost and revenue by resource and by event. *(client request · MoM 26 Aug 2026, 4.9 AI Optimization, Mobile App & Analytics · DI-501)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-927` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS133 Resource Management Configuration Board 8.dc.html#bo-927`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 8
- Flow F271 *Resource Management Configuration board 8: AI Resource Intelligence Command …*, step 8: Works in AI Staffing Requirement Forecast → Translate forecast operational demand into specific workforce requirements.

#### Acceptance for the design

- [ ] Every input above is drawn (17), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-927?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Decide requirement, Save productivity standards.
- [ ] Every transition is wired: `BO-923`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `AI_USE`, `WORKFORCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-928` AI Conflict Resolution Assistant

**Automatically analyze resource conflicts and recommend the most operationally appropriate resolution.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-928 |
| Who uses it | venue staff holding `AI_USE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `actionId` (navigation), `conversationId` (navigation) |
| Route | `/rentals/ai-conflict-resolution-assistant-bo-928` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the AI & Intelligence process.** Resource conflict assistant: double bookings, expired certifications, equipment in maintenance, venue, capacity, dependency, travel-time and setup conflicts - each with the assistant's proposed resolution as a draft a person approves. The one thing to get right: proposals are listed with what they would change and expire if not decided; approving still applies through the owning module.

**Known correction pending (do not draw the wrong version)**

- **Conflict types are action buttons.** Why: They are filter chips. *(source: screens/P08-venue-back-office.yaml#BO-928; AI & Intelligence)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Double booking (primary button) | navigation or local | — | — | — | — |
| Certification expiry (secondary button) | navigation or local | — | — | — | — |
| Equipment maintenance (secondary button) | navigation or local | — | — | — | — |
| Venue conflict (secondary button) | navigation or local | — | — | — | — |
| Capacity conflict (secondary button) | navigation or local | — | — | — | — |
| Dependency conflict (secondary button) | navigation or local | — | — | — | — |
| Travel-time conflict (secondary button) | navigation or local | — | — | — | — |
| Setup conflict (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **conflicts and proposals**: Conflict type as a filter chip; each proposal with summary, what changes (before/after), target module, status and expiry (proposed expires after 7 days). *(source: contracts/satellite/ai.yaml#listProposedActions / contracts/satellite/ai.yaml#/components/schemas/ProposedAction (expiresAt) / R213)*

**What each action does** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Approve / Reject**: Reject needs a reason; approve records the decision and, for an operational action, routes to the owner to apply within 24 hours or it expires. *(source: contracts/satellite/ai.yaml#decideProposedAction / contracts/satellite/ai.yaml#/components/schemas/ProposedAction)*

**Data it reads**: `listProposedActions` (onLoad, What the assistant has proposed and nobody has decided)

**Where the user goes next**

- → `BO-923` AI Resource Intelligence Command Center: *Back to AI Resource Intelligence Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The conflict resolution assistant list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the conflict resolution assistant untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No conflict resolution assistant yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the conflict resolution assistant are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The action is no longer `proposed` — already decided, or expired (7 days after it was proposed, audit R213).; 422 The guard (the provider''s content-safety service, CHG-R1S-002) blocked the message or the reply (`guard-refused`, CHG-CSA-003). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
conflict:
  type: Certification expiry
  detail: Omar Haddad assigned to lifeguard shift Sat; certificate expired 30 Sep
  proposal: Swap with Ahmed Al Zaabi (qualified, available)
```

#### Permissions

- `createAiConversation` → `AI_USE` (operate) · staff, guest
- `sendAiMessage` → `AI_USE` (operate) · staff, guest
- `listProposedActions` → `AI_USE` (operate) · staff
- `decideProposedAction` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

15 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.4.1 | System shall provide a conversational AI assistant across all platform modules. | Unified Operations Dashboard | CONTRACTED | `createAiConversation` |
| 8.4.2 | System shall support natural language interaction. | Unified Operations Dashboard | CONTRACTED | `createAiConversation` |
| 8.4.3 | System shall support multilingual AI interactions. | Unified Operations Dashboard | CONTRACTED | `createAiConversation` |
| 8.1.5 | Explainability System shall provide reasoning and confidence indicators where available. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 8.4.19 | System shall support AI-powered ticketing assistance. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 8.4.20 | System shall support AI-powered support assistance. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 18.10.1 | AI Assistant - System shall provide an AI assistant for employees. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.3 | Operational Queries - Users shall retrieve operational information through AI. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.4 | Work Order Assistance - AI shall assist users with work order activities. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.5 | Knowledge Base Assistance - AI shall provide access to operational knowledge and procedures. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 22.8.4 | AI Chatbot Assistant | Marketing & CRM | CONTRACTED | `sendAiMessage` |
| 22.8.13 | AI Intent Recognition | Marketing & CRM | CONTRACTED | `sendAiMessage` |
| … 3 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-928` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS133 Resource Management Configuration Board 8.dc.html#bo-928`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 8
- Flow F271 *Resource Management Configuration board 8: AI Resource Intelligence Command …*, step 10: Works in AI Conflict Resolution Assistant → Automatically analyze resource conflicts and recommend the most operationally appropriate resolution.
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-928?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Double booking, Certification expiry, Equipment maintenance, Venue conflict, Capacity conflict, Dependency conflict, Travel-time conflict, Setup conflict.
- [ ] Every transition is wired: `BO-923`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-929` Automatic Schedule Optimization

**Optimize resource schedules across multiple assignments while respecting operational constraints.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-929 |
| Who uses it | venue staff holding `AI_USE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `actionId` (navigation), `conversationId` (navigation) |
| Route | `/rentals/automatic-schedule-optimization-bo-929` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the AI & Intelligence process.** Schedule optimisation: the assistant proposes a re-arranged schedule across assignments that respects constraints (qualifications, hours, breaks, travel time), shown as a diff a manager approves or rejects. The one thing to get right: the proposal shows what moves for whom and why it is better (gaps closed, overtime avoided), and nothing changes until approved.

**Known correction pending (do not draw the wrong version)**

- **"Automatic" in the name, while the operations only propose.** Why: Autonomy for operational requirements is L2 Prepare; label it "Schedule optimisation (proposal)". *(source: ADR-0050; AI & Intelligence)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Send AI message (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **proposal diff**: Before/after per person with the improvement in plain numbers (gaps 6 → 1, overtime 14 h → 4 h). *(source: contracts/satellite/ai.yaml#listProposedActions / ADR-0050)*

**Data it reads**: `listProposedActions` (onLoad, What the assistant has proposed and nobody has decided)

**Where the user goes next**

- → `BO-923` AI Resource Intelligence Command Center: *Back to AI Resource Intelligence Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The automatic schedule optimization list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the automatic schedule optimization untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No automatic schedule optimization yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the automatic schedule optimization are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The action is no longer `proposed` — already decided, or expired (7 days after it was proposed, audit R213).; 422 The guard (the provider''s content-safety service, CHG-R1S-002) blocked the message or the reply (`guard-refused`, CHG-CSA-003). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
proposal: Move 3 lifeguards from Sun AM to Sat PM; gaps 6 → 1, overtime 14 h → 4 h
```

#### Permissions

- `sendAiMessage` → `AI_USE` (operate) · staff, guest
- `listProposedActions` → `AI_USE` (operate) · staff
- `decideProposedAction` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

12 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.1.5 | Explainability System shall provide reasoning and confidence indicators where available. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 8.4.19 | System shall support AI-powered ticketing assistance. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 8.4.20 | System shall support AI-powered support assistance. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 18.10.1 | AI Assistant - System shall provide an AI assistant for employees. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.3 | Operational Queries - Users shall retrieve operational information through AI. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.4 | Work Order Assistance - AI shall assist users with work order activities. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.5 | Knowledge Base Assistance - AI shall provide access to operational knowledge and procedures. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 22.8.4 | AI Chatbot Assistant | Marketing & CRM | CONTRACTED | `sendAiMessage` |
| 22.8.13 | AI Intent Recognition | Marketing & CRM | CONTRACTED | `sendAiMessage` |
| 22.8.14 | AI Knowledge Base Integration | Marketing & CRM | CONTRACTED | `sendAiMessage` |
| 22.8.15 | AI Product Recommendations | Marketing & CRM | CONTRACTED | `sendAiMessage` |
| 8.1.4 | Approval Before Execution AI recommendations affecting pricing or financial operations shall require approval before execution | Unified Operations Dashboard | CONTRACTED | `decideProposedAction` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-929` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS133 Resource Management Configuration Board 8.dc.html#bo-929`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 8
- Flow F271 *Resource Management Configuration board 8: AI Resource Intelligence Command …*, step 12: Works in Automatic Schedule Optimization → Optimize resource schedules across multiple assignments while respecting operational constraints.
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-929?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Send AI message, Cancel.
- [ ] Every transition is wired: `BO-923`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-930` Alternative & Replacement Resource

**Provide intelligent alternatives when the preferred resource cannot be used.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-930 |
| Who uses it | venue staff holding `RESOURCE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/alternative-replacement-resource-bo-930` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** When the preferred resource cannot be used (under maintenance, absent, failed, certification expired, the guest's chosen instructor unavailable), the compatible alternatives ranked by how alike they are and what the swap costs the guest: Projector P-24 same specification same venue, P-31 compatible but 30 minutes' transfer. The one thing to get right: say whether the guest must be told or must approve.

**Known correction pending (do not draw the wrong version)**

- **The screen has no components and the gap note says nothing is drawable** Why: The pack lists triggers, two similarity sets, a worked example and the customer-impact classification. *(source: screens/P08-venue-back-office.yaml#BO-930; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Customer impact classification and similarity ranking have no source** Why: suggestResources returns matching free resources only. *(source: contracts/satellite/resources.yaml#suggestResources; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Requested resource and window**: The unavailable resource (from the trigger) with its status and the booking window. *(source: screens/P08-venue-back-office.yaml#BO-930)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Alternatives**: Ranked rows - for equipment by type, specification, capacity, features, location, dependencies, availability; for staff by role, skill, certification, language, experience, availability, venue. Each row shows "Same spec / Same venue / Available" or "Compatible / Different venue / 30 min transfer", with View. *(source: screens/P08-venue-back-office.yaml#BO-930 / contracts/satellite/resources.yaml#suggestResources)*
- **Customer impact**: One of No notification required, Customer notification recommended, Customer approval required - shown per alternative. *(source: screens/P08-venue-back-office.yaml#BO-930)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Use this alternative**: Replaces the resource on the affected booking (keeps the guest and order); a guest-chosen resource first asks for the guest's approval. *(source: contracts/satellite/resources.yaml#replaceResourceAllocation / contracts/satellite/resources.yaml#setResourceSelectionPolicy)*

**Where the user goes next**

- → `BO-923` AI Resource Intelligence Command Center: *Back to AI Resource Intelligence Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The alternative replacement resource list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the alternative replacement resource untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No alternative replacement resource yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the alternative replacement resource are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Instructor did not check in for a shift**: Trigger "Not checked in 10 min after start"; alternatives listed and operations alerted. *(source: DI-490)*

#### Consistency with other screens

- Match `BO-902`: Same alternatives list and facts; BO-930 is the reusable alternatives panel used inside recovery (BO-902) and drag-and-drop (BO-872) (VO-R14).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
requested: Projector P-17 - Under maintenance
alternatives:
- name: Projector P-24
  facts: Same specification, same venue, available
  impact: No notification required
- name: Projector P-31
  facts: Compatible, Summit Peaks, 30 min transfer
  impact: Customer notification recommended
- name: Projector P-11
  facts: Full HD, lower spec
  impact: Customer approval required
```

#### Permissions

- `suggestResources` → `RESOURCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.53 | AI shall recommend optimal resources. | Ticketing Catalogue | CONTRACTED | `suggestResources` |
| 1.2.54 | AI shall recommend suitable staff based on skills and availability. | Ticketing Catalogue | CONTRACTED | `suggestResources` |
| 1.2.56 | AI shall propose alternatives for scheduling conflicts. | Ticketing Catalogue | CONTRACTED | `suggestResources` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- If a scheduled resource fails to check in, the shortfall is flagged for operations and AI can recommend reassigning that resource's bookings. A compliance/validation centre flags events where required staffing is not met, with labour cost tracked. *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering, Attendance & Staffing Control · DI-490)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-930` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS133 Resource Management Configuration Board 8.dc.html#bo-930`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 8
- Flow F271 *Resource Management Configuration board 8: AI Resource Intelligence Command …*, step 14: Works in Alternative & Replacement Resource → Provide intelligent alternatives when the preferred resource cannot be used.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-930?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-923`.
- [ ] Every gated control is gated: `RESOURCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-931` Operational Scenario Simulator & Digital Twin

**Allow managers to test operational scenarios before changing the live resource plan. This should be one of Board 8's signature AI capabilities.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-931 |
| Who uses it | venue staff holding `AI_USE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/operational-scenario-simulator-digital-twin-bo-931` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the AI & Intelligence process.** Operational scenario simulator for the resources team: test "what if 20% more guests", "close the north gate", "two lifeguards off sick" before changing the live resource plan, and compare scenarios. The one thing to get right: a scenario never changes the plan; any change goes through the owning screen.

**Known correction pending (do not draw the wrong version)**

- **"Digital twin" in the name; only forecast scenarios exist.** Why: No twin model exists in the contracts; label it "Scenario simulator" to avoid promising one. *(source: contracts/satellite/ai.yaml#createForecastScenario; AI & Intelligence)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **changes**: Levers as on ADM-507 (capacity, opening hours, staffing, closure, event, weather) with plain-language labels. *(source: contracts/satellite/ai.yaml#createForecastScenario)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create forecast scenario (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **comparison**: Requirement deltas per resource for each scenario side by side. *(source: contracts/satellite/ai.yaml#compareForecastScenarios)*

**Where the user goes next**

- → `BO-923` AI Resource Intelligence Command Center: *Back to AI Resource Intelligence Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The operational scenario simulator list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the operational scenario simulator untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No operational scenario simulator yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the operational scenario simulator are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `ADM-507`: Same simulator component and lever labels.
- Match `ADM-517`: Operational readiness simulator on the console.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
scenarios:
- 'Eid Day 1: +25% guests'
- North gate closed 10:00-12:00
```

#### Permissions

- `createForecastScenario` → `AI_USE` (operate) · staff
- `compareForecastScenarios` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.58 | AI shall simulate future operational scenarios. | Ticketing Catalogue | CONTRACTED | `createForecastScenario` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-931` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS133 Resource Management Configuration Board 8.dc.html#bo-931`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 8
- Flow F271 *Resource Management Configuration board 8: AI Resource Intelligence Command …*, step 16: Works in Operational Scenario Simulator & Digital Twin → Allow managers to test operational scenarios before changing the live resource plan. This should be one of Board 8's signature AI capabilities.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-931?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create forecast scenario, Cancel.
- [ ] Every transition is wired: `BO-923`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-932` Conversational AI Resource Copilot

**Ask the Resource Management module questions and give it commands in plain language, from the back office.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-932 |
| Who uses it | venue staff holding `AI_USE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `conversationId` (navigation) |
| Route | `/rentals/conversational-ai-resource-copilot-bo-932` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the AI & Intelligence process.** Conversational resource copilot: managers ask about and command the resource module in natural language ("who is free to cover gate 2 at 14:00?", "move the cabana cleaning to 18:00"); answers come from the resource services within the person's rights, and commands become drafts to approve. The one thing to get right: a command is never executed from the chat - it returns a proposal card.

**Known correction pending (do not draw the wrong version)**

- **Conversation history shown as a table.** Why: Own conversations as a list, as on the other assistants. *(source: contracts/satellite/ai.yaml#listAiConversations; AI & Intelligence)*

**Fixed on main** (the package already carries these; draw what it says): purpose is a pasted board text describing the Employee App workspace. (CHG-WIR-013).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create AI conversation (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **answer / proposal**: Answers cite the record they came from; command results show as a proposal card (approve in place or open the owning screen). *(source: contracts/satellite/ai.yaml#sendAiMessage (proposedAction) / ADR-0020)*

**Data it reads**: `listAiConversations` (onLoad, Conversation history)

**Where the user goes next**

- → `BO-923` AI Resource Intelligence Command Center: *Back to AI Resource Intelligence Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The conversational resource copilot list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the conversational resource copilot untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No conversational resource copilot yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the conversational resource copilot are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 The guard (the provider''s content-safety service, CHG-R1S-002) blocked the message or the reply (`guard-refused`, CHG-CSA-003). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
exchange:
- Who is free to cover Gate 2 at 14:00 today?
- Ahmed Al Zaabi and Sara Khan are free and qualified for gates.
```

#### Permissions

- `listAiConversations` → `AI_USE` (operate) · staff, guest
- `createAiConversation` → `AI_USE` (operate) · staff, guest
- `sendAiMessage` → `AI_USE` (operate) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

16 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.4.29 | System shall expose AI services through APIs. | Unified Operations Dashboard | CONTRACTED | `listAiConversations` |
| 8.4.30 | System shall maintain AI interaction history. | Unified Operations Dashboard | CONTRACTED | `listAiConversations` |
| 8.4.1 | System shall provide a conversational AI assistant across all platform modules. | Unified Operations Dashboard | CONTRACTED | `createAiConversation` |
| 8.4.2 | System shall support natural language interaction. | Unified Operations Dashboard | CONTRACTED | `createAiConversation` |
| 8.4.3 | System shall support multilingual AI interactions. | Unified Operations Dashboard | CONTRACTED | `createAiConversation` |
| 8.1.5 | Explainability System shall provide reasoning and confidence indicators where available. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 8.4.19 | System shall support AI-powered ticketing assistance. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 8.4.20 | System shall support AI-powered support assistance. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 18.10.1 | AI Assistant - System shall provide an AI assistant for employees. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.3 | Operational Queries - Users shall retrieve operational information through AI. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.4 | Work Order Assistance - AI shall assist users with work order activities. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.5 | Knowledge Base Assistance - AI shall provide access to operational knowledge and procedures. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| … 4 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-932` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS133 Resource Management Configuration Board 8.dc.html#bo-932`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 8
- Flow F271 *Resource Management Configuration board 8: AI Resource Intelligence Command …*, step 18: Works in Conversational AI Resource Copilot → Allow managers to interact with the complete Resource Management module using natural- language questions and commands.
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-932?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create AI conversation, Cancel.
- [ ] Every transition is wired: `BO-923`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P08 reference designs** (from `handoff/design-batches/apps/5-venue-management/README.md`)

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: the client-approved POS, for operator density and components.
- `sources/designs/TICVAI_Mobile.dc.html`: for finish and motion.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-028, DI-029, DI-030, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-039, DI-040, DI-041, DI-042, DI-043, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051, DI-052 (each is in the design inputs below).

**Workshop tracker rows about P08 as a whole** (1: 1 open, 0 closed). Open first; a closed row says where it went on 30 September.

- **S8** Venue Management back-end configuration wireframes *(Chinmay Parab · In progress · due Fri 2 Oct · 30 Sep 2026 · 30 Sep tracker)*

## Design inputs from the client meetings

**What the client asked for in the meetings and design reviews, for these screens.** Apply every item. They are the client's own requirements and they are later than the reference files: where a reference design or a screen's fields disagree with an item here, the item wins. Newest first; where two items disagree, the newer one wins (anything a later meeting replaced is already left out). An **Open question** is not settled: build the default it states and keep it easy to change. The text in brackets is for traceability and, like everything else in this bundle, never appears on a screen.

### Everywhere, on every app

- Allam (platform-wide requirement): every calendar throughout the platform, not just maintenance, must support day, week and month views, with the day view further broken down by hour from a defined start hour through the day. *(agreed · MoM 17 Sep 2026, 4.2 Preventive Maintenance Planning · DI-907)*
- Minimise the number of separate screens an end user navigates: consolidate related information wherever it can reasonably be shown together, rather than mirroring every workshop board as its own screen. *(agreed · MoM 7 Sep 2026, 4.10 Screen consolidation / 5. Key Decisions · DI-671)*
- Region-configurable tax on pre-discount price (e.g. Egypt: AED 100 ticket with 20% off is paid at AED 80 but taxed on AED 100). Rounding must support up to three decimal places without dropping the third decimal where the currency requires it. *(agreed · MoM 1 Sep 2026, 4.5 Taxes, Fees & Price Calculation · DI-598)*
- "Powered by TICVAI" is shown consistently across staff and guest-facing surfaces. *(agreed · MoM 14 Aug 2026, 8. POS / Kiosk Branding · DI-297)*
- Full multi-language support (Arabic and others such as Chinese) consistent with the agreed i18n/RTL architecture. *(agreed · MoM 10 Aug 2026, 4.7 Account Creation, Localisation & Multi-Currency · DI-210)*
- The reference system is a functional reference only: its dated UI/UX is not to be replicated; TICVAI delivers equivalent depth with a modern, AI-friendly, easy-to-configure experience. *(agreed · MoM 7 Aug 2026, 23. Reference System Access & Documentation · DI-186)*
- Direction: modern, minimalistic, spacious, cross-device designs that still convey a sense of place (venue or park); Softlabs proposes two to three enhanced visual concepts for TICVAI to steer. *(agreed · MoM 3 Aug 2026, 11. Design Alignment & Team Input · DI-126)*
- Languages: English and Arabic at minimum, with Russian, Spanish and Mandarin. *(agreed · MoM 31 Jul 2026, 13. Internationalization & Localization · DI-080)*
- Clarity first; reduce cognitive load (simple layouts, familiar patterns); consistency ("Use the system. Do not recreate."); accessibility; hierarchy (guide attention with contrast, spacing and visual weight); feedback (every action has a clear response). *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - Design Principles in Action · DI-051)*
- Standard components: search bar with Cmd+K; tabs (Overview, Events, Sales, Reports); pagination; badges (New, Pending, Sold Out, Completed); toggle (Off/On); dropdown; removable chip ("VIP x"). *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - Example UI Components · DI-050)*
- Spacing on an 8px base grid: 4, 8, 12, 16, 24, 32, 40, 48, 64, 80. Border radius scale 4, 8, 12, 16, 24px, consistent across the platform. Soft shadows: sm 0 1px 2px rgba(0,0,0,.05); md 0 4px 6px rgba(0,0,0,.08); lg 0 10px 15px rgba(0,0,0,.10); xl 0 20px 40px rgba(0,0,0,.14). *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 6. Spacing / 7. Border Radius / 8. Shadows · DI-049)*
- Icons: line style, outline, 2px stroke, round corners, clean and consistent. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 5. Icons · DI-048)*
- Component principles: clarity first; consistent spacing on an 8px grid; meaningful colour (colours communicate status and guide the user); accessible by design; mobile ready (components adapt across all screen sizes). Components are consistent, flexible, accessible and composable. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Component principles · DI-045)*
- Empty states have a title, one explanatory line and one action: "No events yet / Create your first event to get started / Create Event"; "No data available / We couldn't find anything to show here / Refresh". *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Empty States · DI-044)*
- Notification list: status icon, title, one-line detail and relative time (e.g. "Payment received ... 2m ago", "High demand detected ... 10m ago"), with "View all notifications". *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Notifications · DI-042)*
- Forms: label above field; text input, select ("Choose an option"), date picker, toggle, checkbox. Input states: Default, Focused, Filled, Disabled and Error with inline message (e.g. "This field is required"). *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Forms; 08 Design System (p8) - 4. Inputs · DI-040)*
- Card types: event card (title, date and time, venue, "From 120.00 AED"); KPI card (label, value, delta, "vs last 7 days"); onboarding checklist card ("3 of 6 completed": Create Event, Add Staff, Configure Seating, Connect Payment). *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Cards · DI-038)*
- Button hierarchy Primary, Secondary, Tertiary (text) and Icon buttons, each with Default, Hover, Pressed and Disabled states. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Buttons; 08 Design System (p8) - 3. Buttons · DI-036)*
- Regardless of the module a user is working in, the experience should feel like one product, not a collection of separate applications. *(agreed · Design Vision Book 29 Jul 2026, 07 Modules Overview (p7) · DI-034)*
- DO: focus on clarity and hierarchy, use clear simple interactive elements, give relevant information at a glance (card example: "Annual Membership / All Venues / 4.4 (388) / BESTSELLER"). DON'T: clutter and overload (e.g. "-10% NEW PROMO AED 450.00 !!! BOOK NOW!!!"), complex forms and flows, hard-to-read data visualisations. *(agreed · Design Vision Book 29 Jul 2026, 05 Design Principles (p5) - DO / DON'T · DI-033)*
- Eight principles on every screen: User-Centric, AI-First, Simple & Clear (clean layouts, clear hierarchy, minimal noise), Fast & Efficient (optimised for quick actions), Reliable & Secure (permissions, data protection), Data-Driven (data visual, actionable, easy to understand), Scalable, Consistent (same patterns, components and interactions across the ecosystem). *(agreed · Design Vision Book 29 Jul 2026, 05 Design Principles (p5) - Our Design Principles · DI-032)*
- Accessibility: high contrast, readable text, keyboard navigation and inclusive components throughout; WCAG AA standards minimum ("Design for everyone"). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Better Accessibility; 06 Component principles (p6); 08 Design principles in action (p8) · DI-029)*
- AI everywhere: AI insights, recommendations and smart assistance are embedded across the platform, not hidden. AI is not an add-on: it assists, predicts, recommends and automates. *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - How TICVAI improves this concept; 05 Design Principles (p5) - 2. AI-First · DI-027)*
- Global Search: prominent, AI-powered search that finds anything, in the top bar with a Cmd+K shortcut (placeholder e.g. "Search events, customers, orders, venues or ask AI..."). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - UI inspiration reference, item 1; 08 Design System (p8) - Search Bar · DI-025)*
- Visual direction: Purposeful (every element has a clear purpose), Consistent (one visual system across all modules and devices), Clear (easy to scan, understand and act on), Modern. Key takeaway: clean, modern, product-first layout with clear hierarchy and minimal visual noise; deep, modern, trustworthy; built for enterprise scale. *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) · DI-024)*
- The brand is presented consistently across Web Platform, Mobile App and Admin Portal (and print). Ticvai identity, colours and typography are applied consistently across all screens and devices. *(agreed · Design Vision Book 29 Jul 2026, 02 Brand Identity (p2) - Brand in action; 03 Visual Direction (p3) - Consistent Branding · DI-023)*
- Copy is Professional, Friendly, Clear, Confident, Concise and Helpful. Avoid jargon, overly technical language, clutter, outdated language and complexity. *(agreed · Design Vision Book 29 Jul 2026, 02 Brand Identity (p2) - Brand voice · DI-022)*
- Brand personality: Modern, AI-First, Enterprise, Premium, Reliable, Minimal, Scalable, Human-Centred. Visual essence: intelligent and forward-thinking, clean and minimal, trustworthy and secure, modern and timeless, scalable and flexible. *(agreed · Design Vision Book 29 Jul 2026, 02 Brand Identity (p2) - Brand personality / Visual essence · DI-021)*
- Arabic is a core requirement, not later localisation: full Arabic RTL across web, mobile, POS, reports, emails, WhatsApp, SMS, notifications, tickets and receipts, and administrative interfaces. *(agreed · MoM 28 Jul 2026, 27. Internationalisation and Arabic Support · DI-019)*

### Across P08 Venue Management

- Qossai: configuration screens should consolidate related functionality, potentially merging 3-4 previously separate screens into one, rather than the repetitive one-screen-per-concept pattern of the AI-built reference system. *(agreed · MoM 24 Sep 2026, 4.5 Screen Consolidation Philosophy · DI-987)*
- **Open question.** Open: should AI monitoring live in one centralised AI command dashboard or be distributed as widgets in each functional module's own dashboard? Allam: Softlabs' call; the current proposal is illustrative and Softlabs may propose a better structure. *(open · MoM 18 Sep 2026, 4.4 AI Governance — Risk, Compliance & Continuous Monitoring · DI-936)*
- Simulation functionality stays embedded within each relevant configuration section rather than being consolidated, since it tests that section's own configuration. *(agreed · MoM 8 Sep 2026, 4.11 Dashboard & Reporting Module Consolidation Strategy · DI-722)*
- Client boards (POS Frontline, F&B, Retail, Inventory & Procurement) share one architecture: six boards of ten screens per domain, a command centre first and an AI/analytics board last, under the hierarchy Company > Venue > Department > Workstation > Operator/Shift > Transaction > Exception > Reconciliation > Analytics. *(agreed · client-design-boards-audit 20 Aug 2026, Opening / What the boards give us · DI-400)*
- Decision: RBAC per role, per module, three levels — edit/view, view-only, hidden (e.g. a marketing officer does not see Finance at all) — plus sub-permissions within a module (a CRM role may get Campaigns and Communications but not Journeys). Default role templates, admin-customisable. *(agreed · MoM 20 Aug 2026, 4.7 Role-Based Access Control (RBAC); 5. Key Decisions · DI-387)*
- **Open question.** Allam: a user's visibility must be restrictable to specific outlets (an F&B manager of one outlet should not see other outlets' items); also relevant for ticketing/event-specific access. Implementation approach still open. *(open · MoM 18 Aug 2026, 4.6 Role-Based & Outlet-Level Access Control — Open Item · DI-331)*
- Access loads automatically at login on POS and web/admin. A user with one role logs straight in; a user with several roles (e.g. admin, cashier, supervisor, manager) is prompted to choose which role to use. *(agreed · MoM 12 Aug 2026, 4. Multiple Roles per User and Role Switching · DI-249)*
- Back office is role-driven from any device: a finance user signing in from a workstation, laptop or home sees only finance reports and related information. *(agreed · MoM 12 Aug 2026, 3. Role-Based Access and Workstation-Linked Front-End · DI-248)*
- Built-in help menu with step-by-step tutorials with screenshots for common tasks (e.g. how to sell a ticket at the POS). *(client request · MoM 7 Aug 2026, 8. Legacy POS Layout Designer & System Logging · DI-160)*
- Custom data-capture fields ("data mask") at account, event, extended-ticket and product level: field types text, dropdown, radio, true/false; multi-language labels; validation (min/max length, required/optional); reusable value lists (e.g. country list). Standard fields come out of the box. *(agreed · MoM 7 Aug 2026, 6. Data Mask: Flexible Custom Data Capture · DI-155)*
- Load/traffic dashboards respect the tenancy model: a venue manager sees traffic for their own venue only. *(agreed · MoM 31 Jul 2026, 4. Non-Functional Requirements: Scalability & Availability · DI-061)*
- Allam: queue management is built into the system (not third-party) so traffic entering the site can be throttled from the back office itself. *(agreed · MoM 31 Jul 2026, 4. Non-Functional Requirements: Scalability & Availability · DI-060)*
- **Open question.** Proposed tenant hierarchy Tenant > Organization/Brand > Region > Branch > Venue > Department, under review against TICVAI's own organisational hierarchy before finalising. *(open · MoM 30 Jul 2026, 2. Proposed Multi-Tenant Hierarchy · DI-055)*
- Documentation deliverable includes user guides and help content; the preview shows a TICVAI Help Center with categories (Getting Started, Events, Tickets, Orders, Payments, Memberships, Access Control, Reports, Integrations), a "Welcome to TICVAI" getting-started article and Quick Links (Create an Event, Set Pricing, Manage Access, View Reports). *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - What We Deliver / Key Deliverables Preview · DI-052)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- AI Assistant panel: a short framing ("Based on last 30 days, here are 3 actions that can improve your revenue") then actionable recommendations, each with its potential impact (e.g. "Increase pricing for VIP seats, +12%") and a chevron, plus "View all recommendations". *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - AI Panels · DI-043)*
- Chart cards: title with period dropdown ("This Week"), headline metrics with deltas (Tickets Sold 12,840 +8.7%, Visitors, Conversion). Data visualisations must be easy to read. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Charts · DI-041)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Back-office shell: collapsible left sidebar with Overview, Events, Tickets, Orders, Customers, Memberships, Access Control, POS, Reports, Analytics, AI Assistant, Settings, and the signed-in user (name, role) at the bottom; top bar with global search (Cmd+K), current time and date, Notifications with unread dot, and user menu. *(agreed · Design Vision Book 29 Jul 2026, 04 Dashboard Vision (p4) - navigation shell · DI-030)*
- Dynamic KPIs, forecasts and real-time insights; role-based dashboards, preferences and smart shortcuts for every user (e.g. greeting "Good morning, Ahmed" on the home screen, p2). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Smarter Data / Personalized Experience · DI-028)*
- Reports and historical searches must still retrieve archived transactions when required; the retention period (e.g. keep 3 of 5+ years live) is configurable per customer, archival manual or automated. *(agreed · MoM 28 Jul 2026, 23. Database Optimisation and Archiving · DI-018)*
- Back-office controls for the waiting room: configurable maximum active users and admission intervals, set per customer and venue. *(agreed · MoM 28 Jul 2026, 19. Auto-scaling and Virtual Waiting Room · DI-017)*

**2 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"compareForecastScenarios": {"method":"POST","path":"/forecast-scenarios/compare","contract":"ai","summary":"Compare scenarios","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiScenarioComparison"},
"createAiConversation": {"method":"POST","path":"/conversations","contract":"ai","summary":"Open a conversation","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiConversation"},
"createForecastScenario": {"method":"POST","path":"/forecast-scenarios","contract":"ai","summary":"Run a what-if","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AiForecastScenario","responds":null},
"decideOperationalRequirement": {"method":"POST","path":"/operational-requirements/{requirementId}/decide","contract":"ai","summary":"Accept, modify or reject a requirement","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiOperationalRequirement"},
"decideProposedAction": {"method":"POST","path":"/proposed-actions/{actionId}/decide","contract":"ai","summary":"Approve or reject a proposal","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ProposedAction"},
"getAiVenueSettings": {"method":"GET","path":"/venues/{venueId}/ai-settings","contract":"ai","summary":"The venue AI profile the baselines stand on","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AiVenueSettings"},
"getForecast": {"method":"GET","path":"/forecasts","contract":"ai","summary":"Forecast values","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"definitionKey","in":"query","required":true},{"name":"versionId","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"dimensionKey","in":"query","required":null},{"name":"scenarioId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"getStaffingCoverage": {"method":"GET","path":"/staffing-coverage","contract":"workforce","summary":"Where the rota is short, and by how much","permission":"WORKFORCE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true},{"name":"venueId","in":"query","required":null},{"name":"basis","in":"query","required":null}],"requestBody":null,"responds":"StaffingCoverage"},
"listAiConversations": {"method":"GET","path":"/conversations","contract":"ai","summary":"A principal's conversation history","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOperationalRequirements": {"method":"GET","path":"/operational-requirements","contract":"ai","summary":"Requirements derived from the forecast","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"versionId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProposedActions": {"method":"GET","path":"/proposed-actions","contract":"ai","summary":"What the assistant has proposed and nobody has decided","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ProposedAction"},
"listResources": {"method":"GET","path":"/resources","contract":"resources","summary":"Resources at this venue","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":"availableFrom","in":"query","required":null},{"name":"availableTo","in":"query","required":null}],"requestBody":null,"responds":"Resource"},
"requestSuggestion": {"method":"POST","path":"/ai/suggestions","contract":"ai","summary":"Ask for an answer, however it is currently produced","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Suggestion"},
"sendAiMessage": {"method":"POST","path":"/conversations/{conversationId}/messages","contract":"ai","summary":"Ask","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiMessage"},
"setAiVenueSettings": {"method":"PUT","path":"/venues/{venueId}/ai-settings","contract":"ai","summary":"Set the venue AI profile","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AiVenueSettings","responds":"AiVenueSettings"},
"suggestResources": {"method":"GET","path":"/resource-suggestions","contract":"resources","summary":"Resources matching a requirement, by attribute","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"resourceTypeId","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"attributes","in":"query","required":null}],"requestBody":null,"responds":"Resource"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiConversation": {"type":"object","x-ticvai-persistence":"ai.conversation","required":["id","principalId","module","startedAt"],"properties":{"id":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"module":{"$ref":"../shared/common.yaml#/components/schemas/ModuleKey"},"locale":{"type":"string"},"messageCount":{"type":"integer"},"startedAt":{"type":"string","format":"date-time"},"lastMessageAt":{"type":"string","format":"date-time"}}},
"AiForecastPoint": {"type":"object","x-ticvai-persistence":"ai.forecast_point","description":"One forecast value with its interval: 10th, 50th and 90th percentile (design 5.6: a range, never a bare percentage). Partitioned by target month. **AI log database** (design 2.4): append-only, partitioned by month, one Postgres database per tenant on the regional AI log server. The table name stays `ai.<table>`; which server holds it is a deployment matter, not a contract one.","required":["versionId","targetStart","p50"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"versionId":{"type":"string","format":"uuid","x-ticvai-references":"ai.forecast_version"},"scenarioId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.forecast_scenario","description":"Set where the point belongs to a what-if scenario rather than the version itself."},"targetStart":{"type":"string","format":"date-time"},"targetEnd":{"type":"string","format":"date-time"},"dimensionKey":{"type":"string","nullable":true,"description":"Canonical key of the breakdown, e.g. `product=…;channel=web`."},"p10":{"type":"number","nullable":true},"p50":{"type":"number"},"p90":{"type":"number","nullable":true},"unit":{"type":"string"},"drivers":{"type":"object","additionalProperties":true,"nullable":true,"description":"Component decomposition or SHAP contributions, largest first (ADM-506)."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiForecastScenario": {"type":"object","x-ticvai-persistence":"ai.forecast_scenario","description":"**A what-if against a published version** (ADM-507, ADM-517, BO-931). Changes nothing in production; its points are written with `scenarioId`.","required":["baseVersionId","changes"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"name":{"type":"string"},"baseVersionId":{"type":"string","format":"uuid","x-ticvai-references":"ai.forecast_version"},"changes":{"type":"array","items":{"type":"object","required":["lever"],"properties":{"lever":{"type":"string","enum":["price","capacity","openingHours","weather","event","marketing","staffing","closure"]},"target":{"type":"string","nullable":true},"value":{"type":"object","additionalProperties":true,"nullable":true}}},"minItems":1},"status":{"type":"string","enum":["computing","ready","failed"],"readOnly":true},"result":{"type":"object","additionalProperties":true,"nullable":true,"readOnly":true,"description":"Deltas against the base version by subject and period."},"createdByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiForecastVersion": {"type":"object","x-ticvai-persistence":"ai.forecast_version","description":"**An immutable forecast version** (AIP-032): producer, model version, data cut-off, horizon and status. Nothing is overwritten; yesterday's actuals are scored against every earlier version.","required":["definitionId","versionNumber","status","basis"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"definitionId":{"type":"string","format":"uuid","x-ticvai-references":"ai.forecast_definition"},"versionNumber":{"type":"integer","minimum":1},"module":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/ModuleKey"}],"readOnly":true,"description":"The module of the version's definition (`AiForecastDefinition.module`), copied when the version is produced; the module whose AI publish permission `publishForecastVersion` requires (CHG-FUP-004)."},"status":{"type":"string","enum":["running","draft","awaitingApproval","published","superseded","rejected","failed"],"readOnly":true},"basis":{"$ref":"#/components/schemas/SuggestionBasis"},"maturity":{"$ref":"#/components/schemas/AiMaturity"},"producerRef":{"type":"string"},"modelVersion":{"type":"string","nullable":true},"dataCutoffAt":{"type":"string","format":"date-time","description":"The analytical replica watermark the snapshot was taken at."},"horizonStart":{"type":"string","format":"date-time"},"horizonEnd":{"type":"string","format":"date-time"},"qualityChecks":{"type":"object","additionalProperties":true,"readOnly":true,"description":"Each gate and whether it passed."},"publishedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal","description":"Null where the definition auto-published."},"publishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"decisionRecordId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiMaturity": {"type":"object","x-ticvai-persistence":"none — embedded as jsonb on ai.suggestion and ai.forecast_version","description":"**Where an answer stands, on every answer** (29 September, AI functions review; baseline then learn). The customer sees a stage badge and a \"Based on\" chip, never a bare percentage (design 5.6), and \"Limited historical data\" while the starting pattern carries more than half the weight.","required":["stage","basedOn"],"properties":{"stage":{"type":"string","enum":["starting","learning","established","learned"],"description":"`starting`: the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, weather). `learning`: own data carries short-range patterns (about 4 weeks). `established`: own level and trend lead, the baseline fills gaps such as a holiday not yet seen (about 3 months, or at once with 12+ months imported). `learned`: a model trained on this tenant's data, promoted by an admin (AI-D16)."},"basedOn":{"type":"string","description":"The \"Based on\" line, in words, e.g. *Based on: your venue profile, UAE calendar, weather, 23 days of your sales*. Always present."},"sources":{"type":"array","items":{"type":"object","required":["source"],"properties":{"source":{"type":"string","enum":["venueSettings","startingPattern","calendar","weather","bookingsOnHand","ownHistory","importedHistory","configuration","trainedModel"]},"detail":{"type":"string","nullable":true,"description":"e.g. *23 days*, *water park pattern v3*, *Eid al-Adha 2027*."},"observations":{"type":"integer","nullable":true}}}},"ownDataShare":{"type":"number","minimum":0,"maximum":1,"description":"The weight own data carries, `n / (k + n)`. Below 0.5 the answer is marked \"Limited historical data\"."},"limitedHistory":{"type":"boolean"},"nextStage":{"type":"object","nullable":true,"description":"What the next stage needs, e.g. *8 more Saturdays of sales*, or *an admin promotion*.","properties":{"stage":{"type":"string","enum":["learning","established","learned"]},"needs":{"type":"string"},"expectedBy":{"type":"string","format":"date","nullable":true}}}}},
"AiMessage": {"type":"object","x-ticvai-persistence":"ai.message","required":["id","conversationId","role","content","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"conversationId":{"type":"string","format":"uuid"},"role":{"type":"string","enum":["user","assistant","system"]},"content":{"type":"string"},"sources":{"$ref":"#/components/schemas/AiSourceList"},"confidence":{"type":"number","nullable":true,"description":"8.1.5, 8.3.67. **Nullable on purpose** — a provider that does not report confidence must yield null rather than an invented number, and an interface showing 0.9 because the code defaulted it is worse than showing nothing.\n"},"rationale":{"type":"string","nullable":true,"description":"8.3.68, 8.3.69."},"proposedAction":{"allOf":[{"$ref":"#/components/schemas/ProposedAction"}],"nullable":true,"description":"Present where the answer suggests a change. **A draft, never applied here.**"},"traceId":{"type":"string"},"provider":{"$ref":"#/components/schemas/AiProviderKind"},"model":{"type":"string"},"promptTokens":{"type":"integer"},"completionTokens":{"type":"integer"},"latencyMs":{"type":"integer"},"createdAt":{"type":"string","format":"date-time"}}},
"AiOperationalRequirement": {"type":"object","x-ticvai-persistence":"ai.operational_requirement","description":"**A requirement derived from a forecast version** (design 2.2 C step 6, AIP-067): staff, POS, gates, F&B, stock or resources, computed with the tenant's productivity standards. **Autonomy L2 (prepare)**: it is sent to the owning module as a recommendation bound to that version, and a person applies it there.\n**Every kind, from release 1** (Chinmay, 2 October, workbook Q9: \"all kinds\"; CHG-CSA-005). The event forecast derives requirements of every `kind` below, filtered to what the venue has configured (a venue with no kiosks gets no `kiosk` rows); the models in place improve with the venue's data.","required":["versionId","kind","periodStart","quantity"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"versionId":{"type":"string","format":"uuid","x-ticvai-references":"ai.forecast_version"},"kind":{"type":"string","enum":["staff","pos","kiosk","gates","fnb","retail","stock","resource","equipment","facility"]},"targetContract":{"type":"string","description":"The owning module that applies it: `workforce`, `fnb`, `inventory`, `resources`, `access`."},"subjectRef":{"type":"string","nullable":true,"description":"A role, outlet, gate, item or resource type."},"periodStart":{"type":"string","format":"date-time"},"periodEnd":{"type":"string","format":"date-time"},"quantity":{"type":"number"},"quantityP90":{"type":"number","nullable":true,"description":"The requirement at the forecast's 90th percentile, for planning to the busy case."},"unit":{"type":"string"},"productivityStandard":{"type":"object","additionalProperties":true,"nullable":true,"description":"The standard used, e.g. covers per staff hour, scans per gate per hour."},"status":{"type":"string","enum":["issued","accepted","modified","rejected","handedOver","expired"],"readOnly":true},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"decidedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"decisionNote":{"type":"string","nullable":true},"handoverRef":{"type":"string","nullable":true,"readOnly":true,"description":"The owning module's record once handed over."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiProviderKind": {"type":"string","enum":["openai","gemini","anthropic","azureOpenai","localLlm","openaiCompatible"],"description":"`openaiCompatible` (added 29 September, AI design 3.3): a customer endpoint that speaks the OpenAI API, taken with no custom development (AIC-009). Any other protocol needs an adapter.\n**Core42 Compass is reached through `openaiCompatible`** (Chinmay, 2 October: the AI residency decision, amending AI-D02; CHG-CSA-002). Compass is the provider of the `uaeOnly` residency class (common `AiResidencyClass`): Small tier Compass GPT-4.1 mini (or Seraj), Strong tier Compass GPT-5, with OpenAI UAE as the fallback. OpenAI UAE is `openai` with a UAE `endpoint`: OpenAI's UAE-region API project, `ae.api.openai.com` (in-country processing, on OpenAI sales approval), allowed under `uaeOnly` and the only endpoint a `uaeOnly` BYOK OpenAI key may use (CHG-R1S-016). **We host no model** (Chinmay, 3 October, CHG-R1S-002): there is no in-cell open-weights fallback; `localLlm` is used only where a client asks for self-hosting and runs the model on the client's estate (`onPrem`).\n**A kind is a protocol, not a vendor** (Chinmay, 2 October, contract follow-ups: BYOK accepts any provider; CHG-FUP-008). Any vendor is accepted, named in `AiProvider.vendor`: Mistral, Cohere or any other is reached through `openaiCompatible` where its API speaks it, which the compatibility test confirms before activation (`AiProviderCompatibility`). A new native adapter is a new value here, a breaking change for a client built earlier that goes out with an approval (`docs/active/breaking-changes.yaml`); until then a vendor without either protocol is refused `422 provider-protocol-unsupported`.\n"},
"AiScenarioComparison": {"type":"object","x-ticvai-persistence":"none — computed from ai.forecast_point","description":"Scenarios side by side against their base version.","required":["scenarios"],"properties":{"scenarios":{"type":"array","items":{"$ref":"#/components/schemas/AiForecastScenario"}},"rows":{"type":"array","items":{"type":"object","properties":{"subject":{"type":"string"},"periodStart":{"type":"string","format":"date-time"},"base":{"type":"number"},"values":{"type":"object","additionalProperties":true,"description":"Scenario id to value."}}}}}},
"AiSourceList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**The sources an answer was grounded in, stored with the answer** (8.3.70). One `jsonb` column on the row that carries it — `ai.message.sources` and `ai.activity.sources` — because the grounding audit reads the list as it was when the answer was given, and a source is never queried on its own.\n","items":{"$ref":"#/components/schemas/AiSource"}},
"AiVenueSettings": {"type":"object","x-ticvai-persistence":"ai.venue_settings","description":"**The venue AI profile** (29 September, AI functions review): the figures a venue gives at onboarding so every data-driven answer is useful before it has history. One row per venue; configuration, not history. Defaults come from the starting pattern for `venueType`, which TICVAI writes from published sources and made-up example curves, **never from another tenant's data** (AI-D01, AIP-149).","required":["venueId","venueType"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid"},"venueType":{"type":"string","enum":["waterPark","themePark","familyEntertainmentCentre","museum","arena","zooAquarium","other"]},"isOutdoor":{"type":"boolean","default":true,"description":"Outdoor venues take the summer-heat and weather effects."},"capacity":{"type":"integer","minimum":1,"nullable":true},"openingHours":{"type":"array","description":"The usual week. Exceptions come from the venue calendar.","items":{"type":"object","properties":{"dayOfWeek":{"type":"integer","minimum":1,"maximum":7},"opensAt":{"type":"string"},"closesAt":{"type":"string"}}}},"typicalWeekdayAttendance":{"type":"integer","minimum":0,"nullable":true},"typicalWeekendAttendance":{"type":"integer","minimum":0,"nullable":true},"peakMonths":{"type":"array","items":{"type":"integer","minimum":1,"maximum":12}},"averageSpend":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"fnbAttachRate":{"type":"number","minimum":0,"maximum":1,"nullable":true},"staffProductivity":{"type":"object","additionalProperties":{"type":"number"},"description":"Per role, units per staff hour, e.g. `{\"cashier\": 40, \"gate\": 300}`. Defaults from the pattern."},"startingPatternKey":{"type":"string","readOnly":true,"description":"The pattern and version in use, e.g. `waterPark@3`."},"updatedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"ModuleKey": {"$ref":"../shared/common.yaml#/components/schemas/ModuleKey"},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ProposedAction": {"type":"object","x-ticvai-persistence":"ai.proposed_action","required":["id","kind","targetContract","targetOperation","payload","status"],"properties":{"id":{"type":"string","format":"uuid"},"interactionId":{"type":"string","format":"uuid"},"translationJobId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `proposeTranslations` job that drafted this proposal; `getTranslationProposals` reads a job's rows by it. Null on every other proposal (CHG-RFM-004)."},"kind":{"type":"string","enum":["pricing","promotion","operational","financial","configuration","content","audience"],"description":"`content` (a marketing or storefront draft from `proposeMarketingContent`) and `audience` (a lookalike segment from `proposeLookalikeSegment`) added 29 September (build); both are applied by a person in the owning screen."},"targetContract":{"type":"string","description":"Which contract would perform it. The assistant never performs it itself."},"targetOperation":{"type":"string"},"payload":{"type":"object","additionalProperties":true,"description":"The request body a person would submit, ready to review. **Open on purpose: its shape is the request body of `targetOperation` in `targetContract`**, and it is validated against that operation, not restated here.\n"},"summary":{"type":"string"},"status":{"type":"string","description":"**Expiry (decided 28 September, audit R213)**: a `proposed` action expires 7 days after `proposedAt`; an `approved` action not applied expires 24 hours after `decidedAt`. Both are proposed values, client to correct, and `expiresAt` carries the one that applies.\n","enum":["proposed","approved","rejected","applied","expired"]},"expiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"When the expiry timer moves this action to `expired` — `proposedAt` plus 7 days while `proposed`, `decidedAt` plus 24 hours once `approved`, null once `rejected`, `applied` or `expired` (audit R213)."},"approvalLevel":{"type":"integer","minimum":1,"maximum":2,"description":"8.3.65. Multi-level, because a discount and a pricing change differ in authority. **Two levels (decided 28 September, audit R213)**: `2` for anything touching prices or permissions (every `pricing` and `promotion` action, and any other whose payload sets a price, a discount, a role or a permission grant), which needs a manager other than the requester; `1` for everything else, which the requester approves themselves.\n"},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"decisionReason":{"type":"string","nullable":true,"description":"Required on rejection. **The only signal the assistant is proposing badly**, and without it a poor model degrades silently.\n"},"proposedAt":{"type":"string","format":"date-time"},"decidedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","readOnly":true,"description":"**Added 29 September (AI design 3.1):** `ai.proposed_action` had no policy — its only references were nullable. The scope it was proposed at, and the partition key row-level security reads.\n"},"planId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.action_plan","description":"The plan this action presents for a decision (AI design 2.2 D, 3.8)."},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `approvals` request deciding a tier 2 or matrix-caught action (AI design 2.3)."},"changeSetHash":{"type":"string","nullable":true,"readOnly":true,"description":"Hash of the change set approved; execution refuses a plan whose hash differs (AIC-181)."}}},
"Resource": {"type":"object","x-ticvai-persistence":"resources.resource","description":"**A specific object, not a quantity of interchangeable ones.** A venue with forty identical strollers has forty resources, because guest number twelve returned stroller number twelve.\n","required":["id","code","name","kind","venueId"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"kind":{"$ref":"#/components/schemas/ResourceKind"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"parentResourceId":{"type":"string","format":"uuid","nullable":true,"description":"**A pool cabana belongs to the pool area; a seat belongs to an auditorium.** Booking a parent takes its children with it, which is the behaviour a venue expects and would otherwise have to enforce by hand.\n"},"principalId":{"type":"string","format":"uuid","nullable":true,"description":"For a resource of kind `instructor` or `staff`. **`workforce` still owns their rota** — this says whether they are qualified and whether they are already committed.\n"},"attributes":{"type":"object","additionalProperties":true,"description":"Configurable per kind — capacity, size, shade, power, poolside."},"setupMinutes":{"type":"integer","default":0,"description":"**Before the booking, not inside it.** An auditorium booked 14:00–16:00 is unavailable from 13:30 with a 30-minute setup, and a calendar that cannot express that double-books every time.\n"},"teardownMinutes":{"type":"integer","default":0,"description":"After the booking. **Kept as it is** (decided 29 September, W10): with a `cleaningPolicy` of `afterEveryBooking` the cleaning buffer is added after the teardown, so a room with no teardown and a 15-minute clean is free 15 minutes after each booking ends.\n"},"cleaningPolicy":{"allOf":[{"$ref":"#/components/schemas/ResourceCleaningPolicy"}],"nullable":true,"description":"How the resource is cleaned between uses (decided 29 September, W10). Null means no cleaning is scheduled beyond `teardownMinutes`."},"requiresQualification":{"type":"array","items":{"type":"string"},"description":"Qualification codes a person must hold to be assigned to this."},"depositAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["available","booked","checkedOut","maintenance","retired"]},"isActive":{"type":"boolean","default":true},"resourceTypeId":{"type":"string","format":"uuid","nullable":true,"description":"**The configurable resource type** (`resources.resource_type`, 4 October 2026, CHG-FXC-003). `kind` is the fixed family a type belongs to; this is the tenant's own type within it, and the `resourceTypeId` filter of `suggestResources` and `ResourceRequirement.resourceTypeId` match on it."}}},
"ResourceCleaningPolicy": {"x-ticvai-persistence":"none — columns on resources.resource","type":"object","description":"**When the resource is cleaned, and what that takes out of availability** (decided 29 September, W10; the meeting-room case from the 29 September website review).\n- `afterEveryBooking` (option A): `bufferMinutes` blocked after every booking, after its teardown. - `timesPerDay` (option B): `cleaningsPerDay` cleanings of `bufferMinutes` each, between `windowStart` and `windowEnd`, **placed by the system**. The targets are spread evenly across the window; each is put in the free gap nearest its target that is long enough, and never on a booking, a hold or a block. **A confirmed booking is never moved for a cleaning.** Placement is computed on read from the day's bookings, so it moves when bookings change, and a start time is offered only if every cleaning of that day can still be placed after it is booked.\n`createResource` and `updateResource` refuse a policy with `timesPerDay` and no `cleaningsPerDay`, or a window that ends before it starts, with `422`.\n","required":["mode","bufferMinutes"],"properties":{"mode":{"type":"string","enum":["afterEveryBooking","timesPerDay"]},"bufferMinutes":{"type":"integer","minimum":5,"maximum":240,"description":"Minutes one cleaning takes. The prototype uses 15 (proposed default, client to correct)."},"cleaningsPerDay":{"type":"integer","minimum":1,"maximum":24,"nullable":true,"description":"Required for `timesPerDay`; ignored for `afterEveryBooking`."},"windowStart":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","nullable":true,"description":"Venue-local time the cleaning window opens. Null means the resource's opening time."},"windowEnd":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","nullable":true,"description":"Venue-local time the cleaning window closes. Null means the resource's closing time."}}},
"ResourceKind": {"type":"string","description":"BL-135. **`locker` was an entitlement kind in `orders` and nothing issued, assigned or released one.** A locker is a specific object checked out to a named guest and returned — which is this context exactly, and modelling it as an entitlement would have needed a second check-out mechanism.\nA seed for `ResourceType` rather than the law (board 1.02): a customer adding a class does it with `createResourceType`, not by waiting for this list to grow.\n**`table` is a non-dining spot** (decided 29 September, rev 3 GAP-C2, confirmed by Chinmay): a beach or event table placed on a venue map, picked and sold like a cabana (`createResourceHold`, then the order). **A dining table is not this**: restaurant tables stay `fnb` tables, booked with `fnb.createTableReservation` and the waitlist (audit R073 (d)).\n","enum":["cabana","lounger","locker","wheelchair","stroller","equipment","room","auditorium","vehicle","instructor","staff","table","pitch","studio","other"],"x-ticvai-refuses":{"mealPlan":"**Listed by 5.5.8b and deliberately not a kind.** 5.5.8b groups meal plans with lockers and parking, but a meal plan is a balance rather than an object. It resolves to `retail.Wallet` with a `mealPlan` credit kind (CF-126), not to a resource — so it is not offered here, and a form built from this enum cannot offer it either."}},
"StaffingCoverage": {"type":"object","description":"Resource board 4.4. **The gap is the product.**","properties":{"date":{"type":"string","format":"date"},"venueId":{"type":"string","format":"uuid"},"positionCode":{"type":"string"},"label":{"type":"string"},"from":{"type":"string"},"to":{"type":"string"},"required":{"type":"integer"},"rostered":{"type":"integer"},"qualified":{"type":"integer","description":"**A position filled by somebody not qualified for it is still a gap.**"},"gap":{"type":"integer"},"severity":{"type":"string","enum":["covered","tight","short","blocking"]},"openShiftIds":{"type":"array","items":{"type":"string","format":"uuid"}},"basisApplied":{"type":"string","enum":["minimum","forecastRequirement"],"description":"Which figure `required` is for this row. With `higherOfBoth`, the larger; with `forecastRequirement` and no handed-over requirement for the period, `minimum`."},"minimumRequired":{"type":"integer","nullable":true,"description":"The configured minimum for the position and window."},"forecastRequired":{"type":"number","nullable":true,"description":"The forecast staff requirement (p50) for the position and window, from `workforce.forecast_requirement`. Null where none was handed over."},"forecastRequiredP90":{"type":"number","nullable":true,"description":"The busy-case requirement, for planning to the busy case."},"forecastVersionId":{"type":"string","format":"uuid","nullable":true,"description":"The AI forecast version the requirement is bound to (AIP-067), so a manager can open the forecast behind it."}}},
"Suggestion": {"type":"object","x-ticvai-persistence":"ai.suggestion","description":"One answer to one question, with its reasoning and its confidence. **Built 24 August so that machine learning can be swapped in without touching a screen.**\n**A suggestion is never an action.** It proposes; `ProposedAction` and its approval path decide. A model that can order stock is a model that will order stock wrongly at three in the morning.\n**`inputs` is recorded, not just referenced.** A suggestion that cannot be reproduced cannot be defended to a finance controller asking why the system said to order four hundred.\n","required":["id","kind","basis","maturity","producedAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/SuggestionKind"},"basis":{"$ref":"#/components/schemas/SuggestionBasis"},"scopePath":{"type":"string"},"subjectRef":{"type":"string","nullable":true,"description":"What it is about — a product, an outlet, an item, a party."},"value":{"type":"object","additionalProperties":true,"description":"The suggestion itself. Shape depends on `kind`."},"confidence":{"type":"number","nullable":true,"minimum":0,"maximum":1,"description":"**Null for a heuristic and that is honest.** A rule has no confidence — dressing one up with 0.85 is the fastest way to make a manager trust a number that means nothing.\n"},"explanation":{"type":"string","description":"**Plain words, always present, whatever the basis.** *Because covers are up 12% on this day last year* — a suggestion a manager cannot explain to their own boss is a suggestion they will not action.\n"},"inputs":{"type":"object","additionalProperties":true,"description":"What went in. **Recorded so the answer can be reproduced** — and so that when a model replaces the rule, the two can be run against the same inputs and compared.\n"},"producerRef":{"type":"string","description":"The rule name or the model id and version. **A model version is part of the record**: *the model said so* is not an answer to *which model, when*.\n"},"maturity":{"$ref":"#/components/schemas/AiMaturity"},"producedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time","nullable":true,"description":"**A demand forecast for Saturday is worthless on Sunday.** An expired suggestion is hidden rather than shown stale.\n"}}},
"SuggestionBasis": {"type":"string","description":"**How the answer was reached, and this is the field the whole design exists for.**\nA venue must be able to see that today's price suggestion is a margin rule and next quarter's is a trained model — **the same operation, the same screen, a different basis** — and a screen that cannot say which is a screen that asks a manager to trust arithmetic it will not show.\n**Swapping a heuristic for a model is a provider change, not a contract change.** That is the point of the abstraction: the frontend, the audit record and the outcome capture all stay exactly as they are.\n","enum":["heuristic","statistical","model","hybrid","manual"]},
"SuggestionKind": {"type":"string","description":"What is being suggested. **A closed set, and the reason it is closed is the swap.** Every entry here is a question a venue asks that a model could answer better than a rule — and each one starts as a heuristic and becomes a model when there is data.\n**Six of these were drawn as their own endpoints on the client F&B boards** — `suggestPrice`, `simulateScenario`, `simulateSlaPolicy`, `suggestRequisition`, `suggestReplenishment`, `publishDemandPlan`. **Building six endpoints means six places to change when a model changes**, and the model will change more often than the venue's question does.\n**What each kind is based on, and when the venue's own data takes over. Proposed, client to correct (decided 28 September, audit R213; re-read 29 September, AI functions review).** The figure after each rule is **the point where own data takes over from the baseline, not a refusal**: below it the kind answers from the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, the weather) with `maturity.stage` `starting`, and between it and about three months it blends the two (`learning`). The day-one baseline per kind: `replenishment`, `requisition`, `prepPlan`, `staffing`, `demandForecast` and `scenario` from the baseline forecast (typical attendance from the venue AI settings x the venue-type month curve x the calendar x weather, bookings on hand as a floor); `menuEngineering` ranked by margin with popularity marked learning; `slaTarget` a standard default; `waitTime` people ahead / configured capacity; `upsell` the relationship map and business priority; `segmentation` known guest attributes; `anomaly` the venue's configured thresholds and actual against the forecast's low end; `sendTime` the channel's typical hour; `wasteRisk` shelf life and par against the forecast; `queueBalancing` configured capacity per queue. Only a missing setting refuses (422 `AiMissingSettingProblem`).\n- `price`: unit cost plus the category's target margin, held inside the price band. Minimum: a current cost, no history.\n- `replenishment`: par level minus on-hand plus expected use over the supplier lead time. Minimum: 14 days of stock movements.\n- `requisition`: the next service's prep-plan ingredient needs minus kitchen stock. Minimum: 14 days of sales.\n- `demandForecast`: the average of the same weekday over the last 8 weeks, adjusted by admissions already booked. Minimum: 8 weeks of sales.\n- `prepPlan`: forecast covers for the service times each item's share of the last 4 same weekdays. Minimum: 4 weeks of sales.\n- `menuEngineering`: each item placed by popularity against margin, over 90 days. Minimum: 90 days of sales.\n- `staffing`: forecast demand divided by the role's standard covers per staff hour. Minimum: 8 weeks of sales (the forecast it rests on).\n- `slaTarget`: the 80th percentile of actual times over the last 30 days. Minimum: 30 days of timed events.\n- `waitTime`: people ahead divided by the throughput of the last 30 minutes. Minimum: 30 minutes of throughput today.\n- `upsell`: the item most often bought with the basket's items over 90 days. Minimum: 90 days of orders.\n- `segmentation`: recency, frequency and spend scores over 12 months. Minimum: 90 days of orders.\n- `anomaly`: a value outside three standard deviations of the same weekday over 8 weeks. Minimum: 8 weeks of the measure.\n- `scenario`: the demand forecast re-run with the stated changes. Minimum: as `demandForecast`.\n- `sendTime` (added 29 September): per recipient, the hour inside `context.sendWindow` in which they have most often opened or clicked over the last 90 days (marketing-crm attribution touches), and where `context.channel` is `best`, the consented channel with the highest engagement. A recipient with fewer than three touches gets their segment's modal hour, and one with none the window's start. Asked with `subjectRef` a segment id or `context.subjectIds` (at most 10,000). `value` is `{recommendations: [{subjectId, sendAt, channel, basisTouches}]}`. Minimum: 90 days of message touches at the scope.\n- `wasteRisk` (added 29 September): per item at an outlet or store location, planned production and stock on hand minus forecast demand over the item's shelf life, plus batches expiring inside the horizon (`inventory.listExpiringBatches`). `value` is `{items: [{itemRef, quantityAtRisk, valueAtCost, expiresAt, recommendedAction (reducePrep, promote, transfer, useInRecipe), transferTo}]}`. Minimum: 14 days of recorded waste and of sales.\n- `queueBalancing` (added 29 September): per queue or attraction at `subjectRef` (a venue) over `horizon`, the forecast wait (the `queue` forecast definition) against throughput capacity, a recommended virtual-queue return-slot allocation by queue type, and guest redirection from over-used to under-used attractions. `value` is `{queues: [{queueId, forecastWaitMinutes, capacityPerHour, returnSlotsPerInterval, redirectTo}]}`. Minimum: 14 days of queue readings.\n- `itinerary` (added 29 September, MOB-6, guest-allowed): refines a `venue-map` visit plan the guest owns. `subjectRef` is the plan id; `value` is `{planId, baseVersion, changes, rationale}`, applied with `updateVisitPlan` as the guest. Minimum: none; the rules plan is the baseline. Every change names a point or performance of that day's venue only, rides, dining and retail alike (30 September client meeting, MoM 4.7).\n","enum":["price","replenishment","requisition","demandForecast","prepPlan","menuEngineering","staffing","slaTarget","waitTime","upsell","segmentation","anomaly","scenario","sendTime","wasteRisk","queueBalancing","itinerary"]}
}
```
