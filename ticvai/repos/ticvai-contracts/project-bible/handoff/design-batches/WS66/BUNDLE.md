# WS66 — Unified BI Reporting and AI Analytics Platform board 1

**9 screens · 10 operations · 23 schemas · 4 permissions**

Platform P16 Venue Analytics · ships as **venue-management** ·
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
  `AI_USE, PRICE_VIEW, REPORT_VIEW_TENANT, REPORT_VIEW_VENUE`. A control nobody can use must say so,
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

### Finance, Ledger & Tax · Reporting & Analytics

Finance and insights run underneath every sale. A sale at a till (P04), kiosk, web storefront (P01) or guest app (P02) is priced and taxed per line at the moment of sale, recorded in the venue's base currency (AED in the UAE; 2 decimals, or 3 for BHD, KWD and OMR, never rounded away), and posted to an append-only dual ledger through account mappings per money event; anything unmapped lands in suspense. Tax follows the jurisdiction's tax profile: inclusive or exclusive, compound where a tax applies on another, zero-rated or exempt with verified evidence, and computed on the discounted price by default or on the price before discount where the region requires it (Egypt). A guest may select a currency the venue charges and pay in it: the rate is locked on the order, the payment partner is asked in that currency, the ledger keeps the base amount with the rate, and a refund goes back in the currency paid (decided 2 October 2026, Chinmay); a currency shown but not charged is an approximate price. Foreign cash at a till is recorded at its base equivalent and change is given in base currency. A paid order can carry a VAT receipt (simplified tax invoice), a full tax invoice with the buyer's TRN, or a consolidated invoice for a company, each numbered without gaps and never edited; corrections are credit memos. Revenue is recognised by rule: POS-style immediate, tickets on the visit, gift cards and wallet on use, annual passes straight-line or per visit, breakage on expiry; deferred revenue is a balance that ages. Each venue's day is reconciled (POS cash, gateways, bank, wallet against the ledger, provider files matched automatically, only genuine mismatches to a person); chargebacks are defended against the bank's deadline; month end runs seven close checks and goes to a finance approver. Nothing posted is deleted: a correction is a reversal, an approver is never the preparer, and ledger approval needs a second factor. Back-office finance lives in Venue Management (P08: chart of accounts, mapping, FX, journals, recognition, reconciliation, period close, chargebacks); tax profiles, calculation validation and platform reconciliation in the TICVAI Console (P09); partner settlement in P10. Reporting is one consolidated, permission-based area (Analytics, P16): seeded standard dashboards and reports plus no-code builders over a governed business catalogue; the P08 report screens, the POS terminal day view and the kitchen performance view are scoped windows onto the same definitions and must show the same numbers. Every figure is read from a lag-tolerant reporting copy and shows its "as of" time; scope comes from the person's rights, never from a filter; AI explains and recommends but never acts, answers only within the person's role, labels forecasts, and is phase two for finance ledgers.

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Base currency | The venue's region currency; the currency every record and ledger posting is in. A guest may pay in a currency they select (where the venue charges it); the books still hold the base amount and the rate. | Home currency, Local price, Default currency | DI-211 / DI-282 / contracts/spine/orders.yaml#/components/schemas/Order |
| Pay in USD (a currency the venue charges) | The guest's selected payment currency; the card is charged in it at the rate locked on the order, and refunds go back in it. | Converted price, Approx. (for a charged currency) | contracts/spine/orders.yaml#checkoutCart / … |
| ≈ (approx.) price in USD / SAR / … | A conversion of a base-currency price for a currency the venue shows but does not charge, always next to the base price. | Converted price, USD price | DI-211 / screens/P02-guest-mobile-app.yaml#GST-044 |
| Takings | Money received in the period less refunds (cash-basis); the seeded KPI on hubs. | Revenue, Sales, Income | contracts/satellite/reporting.yaml#/components/schemas/ReportingSystemKpi / R283 |
| Gross sales | Issued sales before discounts and refunds; whether tax is included must be stated on the tile. | Revenue, Turnover | MATRIX 6.1.78 |
| Net revenue | Gross sales less discounts less refunds, adjusted per finance policy. | Net sales, Revenue, Income | MATRIX 6.1.78 |
| Recognised revenue / Deferred revenue | Earned under the recognition rules / paid for but not yet earned. Kept distinct from sales. | Realised revenue, Unearned income, Wallet revenue | MATRIX 5.12.6 / DI-260 / contracts/spine/finance.yaml#getDeferredRevenue |
| VAT receipt | The simplified tax invoice issued on a paid order. | Receipt (when it is a tax document), Bill | contracts/spine/finance.yaml#issueTaxInvoice |
| Tax invoice / Combined tax invoice | A full invoice with the buyer's details / one invoice for several paid orders of one buyer. | Bill, Statement | contracts/spine/finance.yaml#/components/schemas/FinTaxInvoiceType |
| Credit memo | The document that corrects an issued invoice after a refund; the invoice itself is never edited. | Credit note (until the client's tax adviser chooses "Tax credit note"), Edit invoice | contracts/spine/finance.yaml#/components/schemas/FinTaxInvoice |
| VAT (or the jurisdiction's tax name) | Use the tax profile's own name on every surface; "Tax" only where several kinds are summed. | GST in UAE, Service charge for a tax | contracts/spine/catalogue.yaml#setTaxProfileJurisdiction |
| Price before discount | The taxable base where the jurisdiction taxes the undiscounted price. | Gross price, List tax | DI-598 |
| Post / Reverse | A journal reaches the ledger when approved and posted; a correction is a reversal, never an edit or delete. | Edit entry, Delete entry, Undo | contracts/spine/finance.yaml#reverseJournalEntry |
| Period (Open / Closing / Closed) | A fiscal period's state; closing stops postings, closed locks them. | Month locked, Frozen | contracts/spine/finance.yaml#/components/schemas/PeriodStatus |
| Variance (Over / Short) | The difference between expected and counted or recorded, always saying between which two figures. | Discrepancy, Error, Loss | DI-275 / contracts/spine/finance.yaml#/components/schemas/UnifiedReconciliation |
| Settlement / Exception / Resolve | A provider's file for a day / a line that did not match / the recorded explanation. | Payout file, Error, Close | contracts/spine/finance.yaml#/components/schemas/SettlementException |
| Chargeback | A bank-initiated reversal with an evidence deadline; not a refund. | Dispute refund, Reversal | contracts/spine/orders.yaml#/components/schemas/Chargeback |
| Report / Dashboard / Tile / KPI | A runnable, exportable, schedulable definition / a page of tiles / one visual bound to a report / a company-wide measure defined once. | Widget (outside the builder's library), Board (for a user-facing dashboard) | contracts/satellite/reporting.yaml#/components/schemas/DashboardTile / … |
| Warning / Critical | KPI status bands set by a target's amber and red thresholds; always words plus colour. | Amber, Red (alone), Bad | contracts/satellite/reporting.yaml#/components/schemas/KpiTarget |
| As of HH:MM / Updated N sec ago | The freshness of every figure read from the reporting copy; stale shows a warning. | Live (unless refreshed), Real-time | MATRIX 8.7.22 |
| Forecast | Any projected figure, with its range; never shown as a fact. | Expected, Will be | DI-973 |
| Outlet / Workstation (till) | A sales point / the device; staff copy may say "till" for the workstation. | Store, POS (in copy), Drawer (for the device) | R156 |
| Channel | POS, Web, App, Kiosk, B2B, OTA, from one closed list. | Source, Platform | MoM 2026-08-18 4.2 Recipes, Operating Hours & Service Channels / MATRIX 1.4.7 |

### Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale)

A guest finds something to do, picks when and how many, holds capacity, pays, and receives a ticket they can show at the gate, transfer or resell. The same booking engine serves the guest website (P01, WEB-), the guest app (P02, GST-) and, through the same catalogue, cart and order operations, the kiosk (P05), the cashier at the till (P04) and the staff handheld (P06); partners book on credit through the partner portal (P10). Guest surfaces are white-label (venue logo, colours, fonts, card layouts, step indicator style, cart placement) with "Powered by TICVAI" kept; the till and handheld stay TICVAI-branded. The booking runs in a fixed order that the client set on 29 September and confirmed on 30 September: for a dated product, the date first, then the time (hidden until a date), then the tickets (hidden until a time); undated products go straight to the tickets; product-first flows (workshops) pick the product, then the date; seated events with one performance open on the seat map, sections first, zoom into a section, pinch out to compare. Choosing a date, time or session commits nothing; capacity is held only when a quantity is set (a 15-minute basket window, 8 minutes for seats and cabanas, one extension). The guest counters (adult, child, senior, infant, person of determination) belong to the chosen ticket and take its prices, so a basket line is "<ticket> · <guest type> × <n>"; group and school products start from group ticket cards and a typed headcount (minus, plus, and +10 on the app), supervisors free. Help me choose filters the catalogue on the server (never a consent step) with Show everything; consent questions such as "Are you able to swim?" are asked once after the session is picked and never again where the page already asked. Sign-in or the six-digit guest code is asked when the guest leaves Add-ons (or at payment, per venue), only the fields the venue configured; after the code, only the T&Cs tick remains (W1). Payment creates the order first and treats an unknown outcome as "checking with your bank", never a second charge; tickets issue on payment, go to Apple or Google Wallet, and a dynamic-QR event's ticket lives in the app. The guest app is deliberately not a copy of the website (30 September): its structure is Home, Explore, Plan and Tickets tabs with a persistent Buy tickets button, item pages that propose the right product (a restaurant's meal combo that includes admission), ride videos that play with no loader, a visit planner that plans each day at one park from that park's rides, dining and shops only, and in-park walking navigation; the booking flow inside it is functionally identical to the web. Vocabulary in guest copy follows the glossary's recorded exceptions (Booking, Session, QR). source: [F01, F02, F03, F07, F49, F52, F55, F57, F58, F59, MoM 29 Sep 1 (W1-W12), MoM 29 Sep 2, MoM 29 Sep 3, MoM 30 Sep 4.4-4.8, CLIENT-RESPONSE-30SEP 1-6, CLIENT-RESPONSE-REV3-25SEP, REV3-1, REV3-2, REV3-3, REV3-4, REV3-26, DI-1086 …

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Booking | An order or reservation as the guest reads it (Booking Confirmation, Group Booking, My bookings). Code says Order or Reservation. | Order (in guest copy), Purchase record, Transaction | docs/glossary.md (Recorded exceptions, Booking, audit R145) |
| Session | A dated, timed performance as the guest reads it (Pick a session, Surf sessions). Staff screens (POS, back office) keep Performance. | Slot, Showtime, Performance (in guest copy) | docs/glossary.md (Recorded exceptions, Session, rev 3 CFG-10); DI-1064 |
| Basket | The guest's unpaid selection with its held capacity (Add to basket, Your basket). Never a paid order. The till and staff screens say Cart. | Cart (in guest copy), Bag, Order (for an unpaid selection) | CLIENT-RESPONSE-REV3-25SEP (Basket, 10) … |
| Ticket | The issued instrument a guest shows at the gate. Product names from the catalogue keep their own words (Day Pass, Annual pass, 2 park ticket); the interface around them says ticket. | Admission, Voucher (for a ticket), Pass (in interface copy) | docs/glossary.md (Ticket) |
| Adult, Child, Senior, Infant, Person of determination | The guest types of a ticket, each with its age or height band shown under it (Child 3-12, Under 1.20 m). A companion of a person of determination is its own free type where the product has one. | Disabled, Handicapped, Kid, Pax | DI-686; screens/P01-guest-web-storefront.yaml#WEB-049 (Passengers notes) … |
| Held for | The countdown on held capacity ("Your seats are held for 7:42"); the release is Release hold. | Lease, Reserved for (a reservation is a different thing), Locked | contracts/spine/orders.yaml#/components/schemas/CartLine (leaseExpiresAt) … |
| Reservation | Booked and not yet paid; holds capacity and expires (My Reservations). Paid tickets are in Tickets or My Tickets. | Booking (for an unpaid hold in lists), Pending order | docs/glossary.md (Reservation); DI-199 |
| Help me choose | The venue's questions whose answers filter the products; Show everything clears them. | Quiz, Wizard, Experience builder, Consent | MoM 29 Sep W4; REV3-11 |
| Info only / Not bookable online | A product listed with full details that cannot be booked online; it shows Contact sales to book with Call sales and Email sales. | Unavailable, Sold out, Coming soon | REV3-14; MoM 29 Sep W3 |
| Guest code | The six-digit code sent to the guest's email or mobile to prove the contact at guest checkout; the copy says six digits. | OTP, PIN, Token, Verification key | DI-1034; MoM 29 Sep W1 |
| How many people | The typed headcount of a group or school booking (number box with minus and plus; +10 on the app), with Supervisors listed separately and free. | Group size (the removed dropdown), Pax | DI-1104; DI-1105; CLIENT-RESPONSE-30SEP 1 |
| Waiting room | The on-sale queue in front of a high-demand performance's sale (WEB-015, GST-046). | Virtual queue (that is the ride queue), Lobby | screens/P01-guest-web-storefront.yaml#WEB-015 notes (ADR-0066) |
| QR | The code a guest shows, in guest copy only (Dynamic QR). Staff screens say Media code. | Barcode, Serial, Media code (in guest copy) | docs/glossary.md (Recorded exceptions, QR, audit R210) |
| Not at this park | The planner's per-day notice that the day's park cannot meet a preference, naming the park that can. | Unavailable, No results | DI-1113 |
| Book this plan | Turns the whole visit plan (tickets, Fast Track, meal combos) into basket lines. | Checkout plan, Buy itinerary | screens/P02-guest-mobile-app.yaml#GST-053 (Book this plan) |

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
| `ANL-012` | Live Operations Dashboard | D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ANL-013` | Revenue Pulse | D | 0 | 36 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ANL-014` | Attendance & Footfall Intelligence | D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ANL-015` | Capacity & Utilization Monitor | D | 0 | 0 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `ANL-016` | Sales & Channel Performance | D | 0 | 0 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `ANL-017` | Customer, Membership & Loyalty Pulse | D | 2 | 30 | 6 | 0 | 2 | 2 | — | notStarted (—) |
| `ANL-018` | Alerts & Exception Center | C | 0 | 22 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ANL-019` | AI Management Insights | D | 11 | 41 | 6 | 3 | 2 | 0 | — | notStarted (—) |
| `ANL-020` | Multi-Site & Performance Comparison | D | 3 | 6 | 6 | 0 | 1 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ANL-018 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ANL-012` Live Operations Dashboard

**Provide a real-time view of what is happening across all operating locations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-012 |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Display) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/live-operations-dashboard-anl-012` |

**From the Finance, Ledger & Tax · Reporting & Analytics process.** The operations control room: what is happening right now across every venue the user may see — people on site, entries and exits, occupancy, gate status, active tills, queues, incidents and device exceptions. It implements the client's Operations Control Room board and DI-699, and must stay legible on a wall display. The one thing to get right: freshness — every tile says how old it is, and a stalled feed is shown as stale, not as a low number.

**Known correction pending (do not draw the wrong version)**

- **Gate status, active gates, active POS terminals, queues and device exceptions have no declared source.** Why: The screen reads only getKpiValues (seeded takings and admissions) and listAlerts; gate and occupancy sources exist in access (listLiveAccess, listLiveVenueOccupancy), devices in tenancy (listDevices), queues in queue (getWaitTimes). *(source: screens/P16-venue-analytics.yaml#ANL-012 / contracts/spine/access.yaml#listLiveAccess / contracts/spine/access.yaml#listLiveVenueOccupancy / contracts/satellite/queue.yaml#getWaitTimes; Finance, Ledger & Tax · Reporting & Analytics)*
- **The states describe "the live operations list" with "Carries the create action".** Why: A live dashboard has no list and nothing to create; first run is "No live data yet — gates and tills will appear once they report". *(source: screens/P16-venue-analytics.yaml#ANL-012; Finance, Ledger & Tax · Reporting & Analytics)*
- **The Operations preset bookmark (today, all venues, live) is absent.** Why: The client asks for it for the control room; the screen should open in it. *(source: MATRIX 6.1.78; Finance, Ledger & Tax · Reporting & Analytics)*
- **"Map or venue layout" is asked for on this board.** Why: The map mark cannot bind yet; use the gate status grid meanwhile. *(source: MATRIX 8.7.33 / MATRIX 8.9.1 / contracts/satellite/reporting.yaml#/components/schemas/DashboardTile; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **What is the stale threshold for live tiles (60 s, 2 min)?** → Drawn default accepted: Stale after 2 minutes without a refresh. *(decided by Chinmay, 2026-10-02; DEC-319 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kpis | text field | — | — | `getKpiValues` ?kpiIds |
| Kpi codes | text field | — | — | `getKpiValues` ?kpiCodes |
| Scope path | text field | — | — | `getKpiValues` ?scopePath |
| Period | text field | — | — | `getKpiValues` ?period |
| Compare to | radio group | — | Previous period · Same period last year · Target · Benchmark | `getKpiValues` ?compareTo |
| Interval | radio group | — | Hour · Day · Week · Month | `getKpiValues` ?interval |
| Group by | text field | — | — | `getKpiValues` ?groupBy |
| Module | field | — | — | `getKpiValues` ?module |
| Status | radio group | — | Raised · Acknowledged · Resolved · Expired | `listAlerts` ?status |
| Severity | segmented control | — | Info · Warning · Critical | `listAlerts` ?severity |
| Workstation | picker: choose a workstation | — | — | `listAlerts` ?workstationId |
| Shift | picker: choose a shift | — | — | `listAlerts` ?shiftId |
| Item | picker: choose an item | — | — | `listAlerts` ?itemId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **venue**: All venues in scope by default (multi-tenant/multi-venue grid); one venue on a wall display preset. *(source: DI-699)*

#### Outputs: what the screen shows and produces

**Shown**

**Visitors currently on-site** (metric tile)

**Entries today** (metric tile)

**Exits today** (metric tile)

**Current occupancy** (metric tile)

**Capacity remaining** (metric tile)

**Occupancy %** (metric tile)

**Active gates** (metric tile)

**Gate status** (metric tile)

**Active POS terminals** (metric tile)

**Active sessions/timeslots** (metric tile)

**Current queues** (metric tile)

**Resource utilization** (metric tile)

**Operational incidents** (metric tile)

**System/device exceptions** (metric tile)

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **people on site**: On site = entries minus exits today; Occupancy % = on site over configured capacity; Capacity remaining = capacity minus on site. Bands Normal below 80%, Warning from 80%, Critical from 95%. *(source: MATRIX 3.2.65 / MATRIX 8.2.36 / MATRIX 1.1.40 / DI-704 / DI-698)*
- **gate status**: Status grid per gate — Open, Closed, Offline — with counts; Offline sorts first and is red with an icon and text. *(source: DI-699 / MATRIX 8.7.33 / MATRIX 8.9.1)*
- **live sales**: Gross sales today and per venue, plus Active POS terminals; same Gross sales definition as the executive board. *(source: DI-699)*
- **queues and incidents**: Current wait per queue (minutes), open incidents and device exceptions as counts that drill through. *(source: MATRIX 8.9.1 / MATRIX 16.4.18 / contracts/satellite/reporting.yaml#/components/schemas/MetricSource)*
- **freshness**: "Updated 40 sec ago" per tile; refresh no faster than every 30 seconds; stale warning past the dataset threshold. *(source: contracts/satellite/reporting.yaml#/components/schemas/DashboardTile / MATRIX 8.7.22 / DI-711)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **open a gate, occupancy or device tile**: Drill-through to the live access, occupancy or device screen with the venue carried; incidents open the alert centre. *(source: MATRIX 2.12.1 / MATRIX 16.9.58 / MATRIX 8.9.10 / MATRIX 8.7.28)*
- **Presentation mode**: Full screen, large type, simplified controls, auto-refresh; for the control-room wall. *(source: MATRIX 8.7.23)*

**Data it reads**: `getKpiValues` (onLoad, Live operational KPIs); `listAlerts` (onLoad, What needs attention)

**Where the user goes next**

- → `ANL-020` Multi-Site & Performance Comparison: *Back to Multi-Site & Performance Comparison*
- → `ANL-001` Executive Command Center: *Executive Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The live operations list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the live operations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No live operations yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the live operations are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **A venue does not scan exits**: On site and visit duration show "Exit scanning not configured" instead of treating entries as people on site. *(source: MATRIX 3.2.65)*
- **Occupancy is between 90% and 95%**: Warning (amber); DI-704's example leaves this band undefined, the 80/95 rule applies. *(source: MATRIX 8.2.36 / MATRIX 1.1.40 / DI-704)*
- **The replica lags by minutes during a spike**: Tiles keep their last values with the stale warning; nothing reads the live transactional database. *(source: MoM 2026-09-08 4.6 Real-Time Reporting Architecture / DI-711)*

#### Consistency with other screens

- Match `ANL-014`: ANL-012 is today and now; ANL-014 is history and trends of the same counts with the same definitions.
- Match `BO-224`: Gate status words and colours identical to Live Access Operations.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
asOf: Updated 35 sec ago · 14:32
venues:
- Aquaventure Waterpark · on site 7,140 of 10,000 (71.4%, Normal) · entries 8,876 · exits 1,736 · gates 11 open,
  1 offline
- Dubai Parks — Motiongate · on site 12,050 of 14,000 (86.1%, Warning) · entries 13,402 · exits 1,352
- House of Wisdom, Sharjah · on site 640 of 1,200 (53.3%) · gates 3 open
queues: Slither's Slides 35 min · Poseidon's Revenge 20 min
incidents: 2 open · 1 device exception (Kiosk 4 printer)
```

#### Permissions

- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff
- `listAlerts` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Live operations view shows sales, entries and exits per tenant/venue for multi-tenant setups, with a quick-glance access-control gate status (open / closed / offline gates). *(client request · MoM 8 Sep 2026, 4.2 Command Center Overview (Board 1) · DI-699)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-012` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS172 Unified BI Reporting and AI Analytics Platform Board 1.dc.html#anl-012`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 1
- Flow F175 *Unified BI Reporting and AI Analytics Platform board 1: Multi-Site & …*, step 2: Works in Live Operations Dashboard → Provide a real-time view of what is happening across all operating locations.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-012?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-020`, `ANL-001`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-013` Revenue Pulse

**Provide real-time visibility into revenue generation across TICVAI.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-013 |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Display) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/revenue-pulse-anl-013` |

**What the spec says about it.** **Measure names, not "Revenue"** (decided 2 October 2026, Chinmay; CHG-FIN-002; BOARDREQ MOM-2758..2761). Takings (money taken less money paid back, a cash-control figure), Gross sales (before discounts, excluding VAT), Net revenue (gross sales less discounts and refunds), Recognised revenue and Deferred revenue are different numbers and never share a label; a tile takes its label from the seeded KPI it is bound to (`ReportingSystemKpi`). Intraday figures are Gross sales (before discounts, excluding VAT) because refunds and recognition settle later; by payment method the figure is Takings, the money taken by tender. Net revenue is shown against target.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Revenue pulse: intraday revenue tempo with its comparisons and breakdowns, drillable from consolidated revenue to site, business unit, channel, product and transaction. The one thing to get right: every "Revenue" tile the pack draws is relabelled with its real measure — this is an operational sales view (Gross sales / Net revenue), not recognised revenue — and breakdowns are charts, not single-number tiles.

**Known correction pending (do not draw the wrong version)**

- **"Revenue by Site / Attraction / Product / Channel / Business Unit / Payment Method" are drawn as single metric tiles.** Why: They are breakdowns; draw them as bar or donut marks. *(source: screens/P16-venue-analytics.yaml#ANL-013 / MATRIX 8.7.4; Finance, Ledger & Tax · Reporting & Analytics)*
- **"Revenue vs Same Day Last Week" has no comparison in the KPI read.** Why: compareTo offers previousPeriod, samePeriodLastYear, target and benchmark only; same weekday last week needs a value or a period convention. *(source: contracts/satellite/reporting.yaml#getKpiValues; Finance, Ledger & Tax · Reporting & Analytics)*
- **No revenue KPI is seeded; only "takings" (payments less refunds).** Why: Binding the revenue tiles to takings would show cash received as revenue; Gross sales and Net revenue KPIs must be defined. *(source: contracts/satellite/reporting.yaml#/components/schemas/ReportingSystemKpi / MoM 2026-08-12 14. Finance Module Walkthrough — Dashboards, Chart of Accounts & Entities; Finance, Ledger & Tax · Reporting & Analytics)*

**Fixed on main** (the package already carries these; draw what it says): Twelve tiles are labelled bare "Revenue ...". (CHG-FIN-002).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **What is a "business unit" in the drill path — department, a tenancy scope node, or a cost centre?** → Drawn default accepted: Treat business unit as department. *(decided by Chinmay, 2026-10-02; DEC-320 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.
- **Should a multi-country tenant see a converted group total, and at what rate?** → Drawn default accepted: Per-currency subtotals only. *(decided by Chinmay, 2026-10-02; DEC-321 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kpis | text field | — | — | `getKpiValues` ?kpiIds |
| Kpi codes | text field | — | — | `getKpiValues` ?kpiCodes |
| Scope path | text field | — | — | `getKpiValues` ?scopePath |
| Period | text field | — | — | `getKpiValues` ?period |
| Compare to | radio group | — | Previous period · Same period last year · Target · Benchmark | `getKpiValues` ?compareTo |
| Interval | radio group | — | Hour · Day · Week · Month | `getKpiValues` ?interval |
| Group by | text field | — | — | `getKpiValues` ?groupBy |
| Module | field | — | — | `getKpiValues` ?module |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **comparison**: Yesterday, Same day last week, Same period last year, Target — one at a time beside the headline. *(source: screens/P16-venue-analytics.yaml#ANL-013 / contracts/satellite/reporting.yaml#getKpiValues)*

#### Outputs: what the screen shows and produces

**Shown**

**Gross sales today** (metric tile, from `getKpiValues`): `getKpiValues?kpiCodes=grossSales`, today; shows its as-of time (CHG-FIN-002, CHG-FIN-007).

| Shows | Format | Notes |
|---|---|---|
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Gross sales this hour** (metric tile, from `getKpiValues`): `getKpiValues?kpiCodes=grossSales`, this hour, interval=hour; shows its as-of time (CHG-FIN-002, CHG-FIN-007).

| Shows | Format | Notes |
|---|---|---|
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Net revenue vs target** (metric tile, from `getKpiValues`): `getKpiValues?kpiCodes=netRevenue`, today, with its target; shows its as-of time (CHG-FIN-002, CHG-FIN-007).

| Shows | Format | Notes |
|---|---|---|
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Gross sales vs yesterday** (metric tile, from `getKpiValues`): `getKpiValues?kpiCodes=grossSales`, today against yesterday; shows its as-of time (CHG-FIN-002, CHG-FIN-007).

| Shows | Format | Notes |
|---|---|---|
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Gross sales vs same day last week** (metric tile, from `getKpiValues`): `getKpiValues?kpiCodes=grossSales`, today against the same day last week; shows its as-of time (CHG-FIN-002, CHG-FIN-007).

| Shows | Format | Notes |
|---|---|---|
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Gross sales vs same period last year** (metric tile, from `getKpiValues`): `getKpiValues?kpiCodes=grossSales`, the period against the same period last year; shows its as-of time (CHG-FIN-002, CHG-FIN-007).

| Shows | Format | Notes |
|---|---|---|
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Gross sales by site** (metric tile, from `getKpiValues`): `getKpiValues?kpiCodes=grossSales`, groupBy=venue; shows its as-of time (CHG-FIN-002, CHG-FIN-007).

| Shows | Format | Notes |
|---|---|---|
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Gross sales by attraction** (metric tile, from `getKpiValues`): `getKpiValues?kpiCodes=grossSales`, groupBy=attraction; shows its as-of time (CHG-FIN-002, CHG-FIN-007).

| Shows | Format | Notes |
|---|---|---|
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Gross sales by product** (metric tile, from `getKpiValues`): `getKpiValues?kpiCodes=grossSales`, groupBy=product; shows its as-of time (CHG-FIN-002, CHG-FIN-007).

| Shows | Format | Notes |
|---|---|---|
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Gross sales by channel** (metric tile, from `getKpiValues`): `getKpiValues?kpiCodes=grossSales`, groupBy=channel; shows its as-of time (CHG-FIN-002, CHG-FIN-007).

| Shows | Format | Notes |
|---|---|---|
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Gross sales by business unit** (metric tile, from `getKpiValues`): `getKpiValues?kpiCodes=grossSales`, groupBy=businessUnit; shows its as-of time (CHG-FIN-002, CHG-FIN-007).

| Shows | Format | Notes |
|---|---|---|
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Takings by payment method** (metric tile, from `getKpiValues`): `getKpiValues?kpiCodes=takings`, groupBy=tender; shows its as-of time (CHG-FIN-002, CHG-FIN-007).

| Shows | Format | Notes |
|---|---|---|
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **headline**: "Net revenue today" and "Net revenue this hour" as number marks with sparkline; Gross sales shown beneath in smaller type. *(source: MATRIX 5.12.6 / MATRIX 8.7.21)*
- **breakdowns**: By site, attraction, product, business unit: sorted bar (top 10 + Other). By channel: donut with at most six slices plus Other. By payment method: donut labelled "Takings by payment method" (payments, not sales). *(source: MATRIX 8.7.4 / MATRIX 8.7.1 / contracts/satellite/reporting.yaml#/components/schemas/ReportingSystemKpi)*
- **hourly tempo**: Line of net revenue per hour today against the comparison day's curve (dashed), venue time zone. *(source: MATRIX 8.7.4 / MATRIX 8.7.8 / MATRIX 8.7.25)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **drill**: Consolidated → site → business unit → channel → product → transaction, each level only where a real hierarchy exists; transaction detail respects the viewer's permissions. *(source: DI-709 / screens/P16-venue-analytics.yaml#ANL-013)*

**Data it reads**: `getKpiValues` (onLoad, Revenue against target)

**Where the user goes next**

- → `ANL-020` Multi-Site & Performance Comparison: *Back to Multi-Site & Performance Comparison*
- → `ANL-001` Executive Command Center: *Executive Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The revenue pulse list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the revenue pulse untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No revenue pulse yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the revenue pulse are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **Tenant spans AED and BHD venues**: Consolidated revenue is shown per base currency; never summed across currencies. *(source: contracts/shared/common.yaml#/components/schemas/Money)*
- **Today is a partial day being compared to a full day**: "vs yesterday" compares to yesterday up to the same time, labelled "to 14:32". *(source: designer default)*

#### Consistency with other screens

- Match `ANL-001`: Same Net revenue and Gross sales numbers as the executive tiles at the same moment; ANL-013 is their drill target.
- Match `ANL-016`: Channel split here must equal ANL-016's for the same period.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
venue: All venues in scope (AED)
headline: Net revenue today AED 2,904,180.25 (vs same day last week AED 2,711,930.00, +7.1%) · this hour AED 312,450.00
bySite: Aquaventure AED 1,169,690.00 · Motiongate AED 1,402,300.25 · House of Wisdom AED 332,190.00
byChannel: Web 44% · POS 27% · OTA 18% · B2B 7% · Kiosk 4%
byPayment: Card AED 1,986,400.00 · Cash AED 402,115.50 · Wallet AED 210,300.00
```

#### Permissions

- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-013` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS172 Unified BI Reporting and AI Analytics Platform Board 1.dc.html#anl-013`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 1
- Flow F175 *Unified BI Reporting and AI Analytics Platform board 1: Multi-Site & …*, step 4: Works in Revenue Pulse → Provide real-time visibility into revenue generation across TICVAI.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (36 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-013?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-020`, `ANL-001`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-014` Attendance & Footfall Intelligence

**Monitor visitor movement and attendance across venues.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-014 |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Display) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/attendance-footfall-intelligence-anl-014` |

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Attendance and footfall: how many people came, when, through which gates, on what tickets, and how that compares with what was sold and with the forecast. It implements the admissions half of the client's Admissions & Capacity board and the access-control part of the Operations board. The one thing to get right: attendance is counted by visit date (scans), not by sale date, and ticketed vs actual uses the same visit date.

**Known correction pending (do not draw the wrong version)**

- **The forecast attendance the purpose promises has no declared read.** Why: Forecast visitors come from ai.getForecast (subject attendance); only getKpiValues is declared. *(source: screens/P16-venue-analytics.yaml#ANL-014 / contracts/satellite/ai.yaml#getForecast; Finance, Ledger & Tax · Reporting & Analytics)*
- **Per-gate (turnstile) breakdown is not among the tiles.** Why: DI-717 asks for per-turnstile breakdowns explicitly. *(source: DI-717; Finance, Ledger & Tax · Reporting & Analytics)*
- **"Attendance by Site / Attraction / Ticket Type / Product / Timeslot" are single metric tiles.** Why: They are breakdowns; bar or table marks. *(source: screens/P16-venue-analytics.yaml#ANL-014; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kpis | text field | — | — | `getKpiValues` ?kpiIds |
| Kpi codes | text field | — | — | `getKpiValues` ?kpiCodes |
| Scope path | text field | — | — | `getKpiValues` ?scopePath |
| Period | text field | — | — | `getKpiValues` ?period |
| Compare to | radio group | — | Previous period · Same period last year · Target · Benchmark | `getKpiValues` ?compareTo |
| Interval | radio group | — | Hour · Day · Week · Month | `getKpiValues` ?interval |
| Group by | text field | — | — | `getKpiValues` ?groupBy |
| Module | field | — | — | `getKpiValues` ?module |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **period**: Visit date range, default Last 7 days; labelled "Visit date" so it is not confused with sale date. *(source: MATRIX 1.1.40 / MATRIX 8.8.3)*

#### Outputs: what the screen shows and produces

**Shown**

**Total Visitors** (metric tile)

**Current Visitors On-Site** (metric tile)

**Entry Count** (metric tile)

**Exit Count** (metric tile)

**Hourly Footfall** (metric tile)

**Peak Entry Time** (metric tile)

**Average Visit Duration** (metric tile)

**Attendance by Site** (metric tile)

**Attendance by Attraction** (metric tile)

**Attendance by Ticket Type** (metric tile)

**Attendance by Product** (metric tile)

**Attendance by Timeslot** (metric tile)

**Repeat Visits** (metric tile)

**No-Show %** (metric tile)

**Ticketed vs Actual Attendance** (metric tile)

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **counts**: Total visitors (admitted entries), Entries, Exits, Current visitors on site, Repeat visits, No-show %. *(source: MATRIX 1.1.40 / MATRIX 6.1.69 / MATRIX 8.1.2 / MATRIX 3.2.65 / contracts/satellite/reporting.yaml#/components/schemas/ReportingSystemKpi)*
- **admission conversion**: "Ticketed vs actual" = admitted tickets over valid issued tickets for the visit period, as a %, with both counts shown. *(source: MATRIX 1.1.40 / MATRIX 8.7.21)*
- **hourly footfall**: Heatmap hour × weekday of entries; Peak entry time stated in words ("Peak 10:00–11:00, 1,912 entries"). *(source: MATRIX 6.1.69 / MATRIX 6.1.70)*
- **by gate**: Entries by gate/turnstile as a sorted bar. *(source: DI-717)*
- **forecast**: Next 7 days attendance as a dashed Forecast line with its range, after the actuals. *(source: screens/P16-venue-analytics.yaml#ANL-014 / DI-973 / MATRIX 8.2.1)*
- **average visit duration**: From the time between entry and exit scans; shown only where exits are scanned. *(source: MATRIX 3.2.65)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **drill**: Venue → attraction → ticket type → time slot → scan detail. *(source: MATRIX 8.7.28 / DI-709)*

**Data it reads**: `getKpiValues` (onLoad, Attendance and footfall)

**Where the user goes next**

- → `ANL-020` Multi-Site & Performance Comparison: *Back to Multi-Site & Performance Comparison*
- → `ANL-001` Executive Command Center: *Executive Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The attendance footfall intelligence list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the attendance footfall intelligence untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No attendance footfall intelligence yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the attendance footfall intelligence are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **Complimentary tickets**: Counted in attendance; excluded from average ticket value where policy says so; the exclusion is stated. *(source: MATRIX 8.1.3 / MATRIX 6.1.66)*
- **Daylight-saving or time-zone boundary venue (multi-country tenant)**: Hours are local to each venue; the heatmap never mixes time zones. *(source: MATRIX 6.1.78)*

#### Consistency with other screens

- Match `ANL-012`: Same entry/exit/on-site definitions; ANL-012 is live, ANL-014 is the period view.
- Match `ANL-015`: ANL-014 owns people counts; ANL-015 owns capacity and utilisation. No-show % appears on both and must match.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
venue: Aquaventure Waterpark
period: Visit date 23–29 Sep 2026
counts: Visitors 58,214 · Exits 55,902 · Repeat visits 9,840 · No-show 4.1%
ticketedVsActual: Admitted 58,214 of 60,705 valid tickets (95.9%)
peak: Peak 10:00–11:00 Fri, 1,912 entries
byGate: 'Main Gate 1: 22,410 · Main Gate 2: 19,880 · Beach Gate: 15,924'
forecast: Forecast Thu 01 Oct 8,900 (likely 8,100 – 9,650)
```

#### Permissions

- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Operations board: access-control metrics - total entries, attendance, exits, per-turnstile breakdowns, and park capacity utilisation. *(client request · MoM 8 Sep 2026, 4.9 Sales, Finance, Operations & CRM Boards · DI-717)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-014` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS172 Unified BI Reporting and AI Analytics Platform Board 1.dc.html#anl-014`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 1
- Flow F175 *Unified BI Reporting and AI Analytics Platform board 1: Multi-Site & …*, step 6: Works in Attendance & Footfall Intelligence → Monitor visitor movement and attendance across venues.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-014?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-020`, `ANL-001`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-015` Capacity & Utilization Monitor

**Provide centralized monitoring of available and consumed capacity.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-015 |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/capacity-utilization-monitor-anl-015` |

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Capacity and utilisation: where capacity is under-used, filling up or full, by attraction, time slot and inventory item, and what is still available to sell. It implements the capacity half of the Admissions & Capacity board and DI-700's capacity section. The one thing to get right: utilisation's definition (consumed or reserved over sellable) and how holds and blocked inventory are treated must be visible on the screen.

**Known correction pending (do not draw the wrong version)**

- **Two utilisation-like metrics exist (occupancy = sold + leased vs capacity; capacityUtilisation = remaining over the window) and the screen does not say which "Utilization %" is.** Why: Two definitions under one label is the drift the KPI register exists to prevent. *(source: contracts/satellite/reporting.yaml#/components/schemas/MetricSource / MATRIX 8.2.36 / MATRIX 1.1.40 / MATRIX 8.9.2; Finance, Ledger & Tax · Reporting & Analytics)*
- **Forecast utilisation has no declared read.** Why: It comes from ai.getForecast (subject attractionUtilisation / occupancy). *(source: contracts/satellite/ai.yaml#getForecast / MATRIX 8.2.35 / MATRIX 8.2.36; Finance, Ledger & Tax · Reporting & Analytics)*
- **DI-704's example leaves 90–95% undefined (80–90 warning, above 95 critical).** Why: The board spec's 80/95 rule closes the gap; DI-704's example should be corrected. *(source: DI-704 / MATRIX 8.2.36 / MATRIX 1.1.40; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Do holds and blocked inventory count as consumed in utilisation?** → Drawn default accepted: Count holds as reserved (in utilisation), exclude blocked from sellable. *(decided by Chinmay, 2026-10-02; DEC-322 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kpis | text field | — | — | `getKpiValues` ?kpiIds |
| Kpi codes | text field | — | — | `getKpiValues` ?kpiCodes |
| Scope path | text field | — | — | `getKpiValues` ?scopePath |
| Period | text field | — | — | `getKpiValues` ?period |
| Compare to | radio group | — | Previous period · Same period last year · Target · Benchmark | `getKpiValues` ?compareTo |
| Interval | radio group | — | Hour · Day · Week · Month | `getKpiValues` ?interval |
| Group by | text field | — | — | `getKpiValues` ?groupBy |
| Module | field | — | — | `getKpiValues` ?module |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Available Capacity** (metric tile)

**Booked Capacity** (metric tile)

**Used Capacity** (metric tile)

**Remaining Capacity** (metric tile)

**Utilization %** (metric tile)

**No-Show %** (metric tile)

**Peak Utilization** (metric tile)

**Forecast Utilization** (metric tile)

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **capacity cards**: Sellable capacity, Booked, Held, Used (admitted), Remaining (available to sell), Utilisation %, No-show %, Peak utilisation. *(source: MATRIX 6.1.70 / MATRIX 8.2.36 / MATRIX 1.1.40 / MATRIX 8.9.2 / contracts/satellite/reporting.yaml#/components/schemas/MetricSource)*
- **utilisation by attraction / slot**: Gauge only for the headline (a target range exists); per attraction a sorted bar with the 80% and 95% reference lines; per time slot a heatmap. *(source: MATRIX 1.1.40 / MATRIX 8.2.36 / MATRIX 8.7.21 / MATRIX 6.1.69)*
- **status bands**: Normal under 80%, Warning 80–95%, Critical 95% and above; tenant-configurable via KPI targets. *(source: MATRIX 8.2.36 / MATRIX 1.1.40 / contracts/satellite/reporting.yaml#/components/schemas/KpiTarget / DI-704)*
- **forecast utilisation**: Labelled "Forecast", dashed, with range. *(source: DI-973 / MATRIX 8.2.36)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **open a time slot**: Drill-through to capacity configuration for that product and slot (an authorised workflow link, permission-checked). *(source: MATRIX 2.12.1 / MATRIX 16.9.58 / MATRIX 8.9.10)*

**Data it reads**: `getKpiValues` (onLoad, Capacity and utilisation)

**Where the user goes next**

- → `ANL-020` Multi-Site & Performance Comparison: *Back to Multi-Site & Performance Comparison*
- → `ANL-001` Executive Command Center: *Executive Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The capacity utilization list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the capacity utilization untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No capacity utilization yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the capacity utilization are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **Capacity reduced mid-day (a ride closes)**: Utilisation recomputes against the new sellable capacity; the change is marked on the chart. *(source: designer default)*
- **Holds exceed 10% of capacity**: Held shown as its own segment so utilisation is not overstated. *(source: MATRIX 8.2.36 / MATRIX 1.1.40)*

#### Consistency with other screens

- Match `ANL-012`: ANL-012's occupancy (people on site now) is not ANL-015's utilisation (sold or reserved over sellable); different labels.
- Match `ANL-014`: No-show % identical.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
venue: Dubai Parks — Motiongate, Sat 03 Oct 2026
cards: Sellable 14,000 · Booked 11,620 · Held 480 · Remaining 1,900 · Utilisation 86.4% (Warning)
slots:
- 10:00 Dreamworks Tour · 98% · Critical
- 14:00 Hunger Games Mockingjay · 72% · Normal
forecast: Forecast utilisation Sat 89% (likely 84% – 93%)
```

#### Permissions

- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Operations board: access-control metrics - total entries, attendance, exits, per-turnstile breakdowns, and park capacity utilisation. *(client request · MoM 8 Sep 2026, 4.9 Sales, Finance, Operations & CRM Boards · DI-717)*
- Further command-centre sections: revenue by sales channel; capacity utilisation by attraction/inventory item; top products by channel; conversion rate (site visits to completed purchase, cart abandonment, via Google Analytics); customer, membership and loyalty information. *(client request · MoM 8 Sep 2026, 4.2 Command Center Overview (Board 1) · DI-700)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-015` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS172 Unified BI Reporting and AI Analytics Platform Board 1.dc.html#anl-015`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 1
- Flow F175 *Unified BI Reporting and AI Analytics Platform board 1: Multi-Site & …*, step 8: Works in Capacity & Utilization Monitor → Provide centralized monitoring of available and consumed capacity.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-015?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-020`, `ANL-001`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-016` Sales & Channel Performance

**Provide management with consolidated commercial performance across every sales channel.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-016 |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/sales-channel-performance-anl-016` |

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Sales and channel performance: one scorecard of commercial performance across POS, B2C (web, app, kiosk), B2B and OTA, with conversion, basket size, discount use and channel mix. It implements the client's Sales & Channel board and DI-700's channel section. The one thing to get right: Net revenue (not "Net Sales") is the headline, commission and discounts are deductions, and clicking a channel filters every visual.

**Known correction pending (do not draw the wrong version)**

- **The tile is labelled "Net Sales".** Why: The agreed measure is Net revenue (gross minus discounts minus refunds); "Sales" must not stand for net. *(source: screens/P16-venue-analytics.yaml#ANL-016; Finance, Ledger & Tax · Reporting & Analytics)*
- **The board is specified with a funnel and slicers.** Why: Funnel cannot bind yet; slicer is refused as a mark (it is a report parameter). *(source: MATRIX 8.7.4 / MATRIX 8.7.25 / contracts/satellite/reporting.yaml#/components/schemas/DashboardTile; Finance, Ledger & Tax · Reporting & Analytics)*
- **Gross sales, Net revenue, Discounts, Refunds, Average order value and channel sales have no metric source; only conversion is a named metric.** Why: The scorecard's money tiles cannot bind until these are defined as KPIs (takings is payments, not sales). *(source: contracts/satellite/reporting.yaml#/components/schemas/MetricSource / MoM 2026-08-12 14. Finance Module Walkthrough — Dashboards, Chart of Accounts & Entities; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is commission shown as a deduction from net revenue or as a separate cost line?** → Drawn default accepted: Separate line, not deducted from Net revenue. *(decided by Chinmay, 2026-10-02; DEC-323 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kpis | text field | — | — | `getKpiValues` ?kpiIds |
| Kpi codes | text field | — | — | `getKpiValues` ?kpiCodes |
| Scope path | text field | — | — | `getKpiValues` ?scopePath |
| Period | text field | — | — | `getKpiValues` ?period |
| Compare to | radio group | — | Previous period · Same period last year · Target · Benchmark | `getKpiValues` ?compareTo |
| Interval | radio group | — | Hour · Day · Week · Month | `getKpiValues` ?interval |
| Group by | text field | — | — | `getKpiValues` ?groupBy |
| Module | field | — | — | `getKpiValues` ?module |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **filter bar**: Venue, channel, product, performance date, customer segment — rendered as filter controls bound to report parameters (a slicer is a control, not a mark); active filters as breadcrumbs with Clear and Reset. *(source: MATRIX 8.7.28 / MATRIX 6.1.50 / MATRIX 6.1.66 / contracts/satellite/reporting.yaml#/components/schemas/DashboardTile)*

#### Outputs: what the screen shows and produces

**Shown**

**Gross Sales** (metric tile)

**Net Sales** (metric tile)

**Transactions** (metric tile)

**Tickets Sold** (metric tile)

**Average Order Value** (metric tile)

**Conversion Rate** (metric tile)

**Discount Value** (metric tile)

**Refunds** (metric tile)

**Cancellations** (metric tile)

**Commission** (metric tile)

**Upsell Revenue** (metric tile)

**Cross-Sell Revenue** (metric tile)

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **scorecard**: Gross sales, Discounts, Refunds, Net revenue, Transactions, Tickets sold, Average order value, Conversion, Cancellations, Commission (B2B/OTA), Attributed to upsell, Attributed to cross-sell. Discounts, refunds and commission shown as negatives in brackets. *(source: screens/P16-venue-analytics.yaml#ANL-016 / MATRIX 8.7.4)*
- **channel mix over time**: Stacked bar of Net revenue by channel by day; trend line for conversion. *(source: MATRIX 8.7.4 / MATRIX 8.7.25)*
- **channel table**: Per channel Net revenue, transactions, AOV, conversion, discount %, commission; totals row server-side. *(source: MATRIX 8.7.4 / MATRIX 8.7.25)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **click B2C in any visual**: KPI tiles and the order table filter to B2C; other visuals highlight its contribution while keeping totals. *(source: MATRIX 8.7.28 / MATRIX 8.9.10)*

**Data it reads**: `getKpiValues` (onLoad, Sales by channel)

**Where the user goes next**

- → `ANL-020` Multi-Site & Performance Comparison: *Back to Multi-Site & Performance Comparison*
- → `ANL-001` Executive Command Center: *Executive Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The sales channel performance list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the sales channel performance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No sales channel performance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the sales channel performance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **An OTA booking cancelled after the period**: Counted in the period it was cancelled; the cancellation tile links to the bookings. *(source: MATRIX 6.1.78)*

#### Consistency with other screens

- Match `ANL-002`: ANL-016 owns the channel scorecard; ANL-002 the product-by-channel detail and recognition. Same definitions.
- Match `PTR-002`: Partner commission must match the partner's own dashboard for the same period.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
venue: All venues in scope (AED)
period: Last 7 days
scorecard: Gross sales AED 19,840,200.00 · Discounts (AED 1,284,600.00) · Refunds (AED 212,450.00) · Net revenue
  AED 18,343,150.00 · Commission (AED 611,300.00)
channels:
- Web · AED 8,071,000.00 · 18,410 orders · AOV AED 438.40 · conversion 3.4%
- OTA · AED 3,301,770.00 · 7,120 orders · commission (AED 495,265.50)
- POS · AED 4,952,650.00 · 21,800 transactions
```

#### Permissions

- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Sales board: product/attraction performance by sales channel, discounts, upsell/cross-sell results, deferred vs realised revenue, and sales forecast vs target. *(client request · MoM 8 Sep 2026, 4.9 Sales, Finance, Operations & CRM Boards · DI-715)*
- Further command-centre sections: revenue by sales channel; capacity utilisation by attraction/inventory item; top products by channel; conversion rate (site visits to completed purchase, cart abandonment, via Google Analytics); customer, membership and loyalty information. *(client request · MoM 8 Sep 2026, 4.2 Command Center Overview (Board 1) · DI-700)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-016` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS172 Unified BI Reporting and AI Analytics Platform Board 1.dc.html#anl-016`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 1
- Flow F175 *Unified BI Reporting and AI Analytics Platform board 1: Multi-Site & …*, step 10: Works in Sales & Channel Performance → Provide management with consolidated commercial performance across every sales channel.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-016?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-020`, `ANL-001`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-017` Customer, Membership & Loyalty Pulse

**Provide a consolidated view of customer health and engagement.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-017 |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `dashboardId` (navigation) |
| Route | `/analytics/customer-membership-loyalty-pulse-anl-017` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Customer, membership and loyalty pulse: acquisition, renewals, retention, member visits, loyalty activity and points liability, with inactive members flagged for follow-up. It implements the client's Customer & Membership board and the 8 Sep CRM board. The one thing to get right: it is an aggregate view; any list of named customers is permission-gated and masked, and points liability is a finance figure from the ledger.

**Known correction pending (do not draw the wrong version)**

- **The layout is a 15-column table of "Every customer membership loyalty" with no operation and a detail panel per customer.** Why: The board is a pulse of aggregates; a customer-level list is a PII surface that belongs to CRM with permission and masking. *(source: screens/P16-venue-analytics.yaml#ANL-017 / MATRIX 8.3.73; Finance, Ledger & Tax · Reporting & Analytics)*
- **emptyFirstRun says "Carries the create action".** Why: There is nothing to create on a pulse dashboard; first run is "No members yet". *(source: screens/P16-venue-analytics.yaml#ANL-017; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is points liability shown to non-finance roles?** → Drawn default accepted: Shown only with finance or tenant report scope. *(decided by Chinmay, 2026-10-02; DEC-324 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search customer membership loyalty | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by customer segment, membership type, geography, demographic group, acquisition source, visit frequency and 1 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kpis | text field | — | — | `getKpiValues` ?kpiIds |
| Kpi codes | text field | — | — | `getKpiValues` ?kpiCodes |
| Scope path | text field | — | — | `getKpiValues` ?scopePath |
| Period | text field | — | — | `getKpiValues` ?period |
| Compare to | radio group | — | Previous period · Same period last year · Target · Benchmark | `getKpiValues` ?compareTo |
| Interval | radio group | — | Hour · Day · Week · Month | `getKpiValues` ?interval |
| Group by | text field | — | — | `getKpiValues` ?groupBy |
| Module | field | — | — | `getKpiValues` ?module |
| Refresh | toggle | off | — | `getDashboard` ?refresh |

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **filters**: Customer segment, membership type, geography (country/emirate), acquisition source, visit frequency. *(source: screens/P16-venue-analytics.yaml#ANL-017)*

#### Outputs: what the screen shows and produces

**Shown**

**Every customer membership loyalty** (data table)

| Shows | Format | Notes |
|---|---|---|
| Unique customers | text | not in the schema: `Unique Customers` |
| New customers | text | not in the schema: `New Customers` |
| Returning customers | text | not in the schema: `Returning Customers` |
| Repeat visit % | text | not in the schema: `Repeat Visit %` |
| Average customer spend | text | not in the schema: `Average Customer Spend` |
| Customer lifetime value | text | not in the schema: `Customer Lifetime Value` |
| Active members | text | not in the schema: `Active Members` |
| New memberships | text | not in the schema: `New Memberships` |
| Membership renewals | text | not in the schema: `Membership Renewals` |
| Membership expiring | text | not in the schema: `Membership Expiring` |
| Loyalty members | text | not in the schema: `Loyalty Members` |
| Loyalty earn | text | not in the schema: `Loyalty Earn` |
| Loyalty burn | text | not in the schema: `Loyalty Burn` |
| Outstanding loyalty liability | text | not in the schema: `Outstanding Loyalty Liability` |
| Customer satisfaction score | text | not in the schema: `Customer Satisfaction Score` |

**The selected customer membership loyalty** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Unique customers | text | not in the schema: `Unique Customers` |
| New customers | text | not in the schema: `New Customers` |
| Returning customers | text | not in the schema: `Returning Customers` |
| Repeat visit % | text | not in the schema: `Repeat Visit %` |
| Average customer spend | text | not in the schema: `Average Customer Spend` |
| Customer lifetime value | text | not in the schema: `Customer Lifetime Value` |
| Active members | text | not in the schema: `Active Members` |
| New memberships | text | not in the schema: `New Memberships` |
| Membership renewals | text | not in the schema: `Membership Renewals` |
| Membership expiring | text | not in the schema: `Membership Expiring` |
| Loyalty members | text | not in the schema: `Loyalty Members` |
| Loyalty earn | text | not in the schema: `Loyalty Earn` |
| Loyalty burn | text | not in the schema: `Loyalty Burn` |
| Outstanding loyalty liability | text | not in the schema: `Outstanding Loyalty Liability` |
| Customer satisfaction score | text | not in the schema: `Customer Satisfaction Score` |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **membership**: New, Renewed, Expired members (period), Renewal rate, Churn, Member visits; trend line by month. *(source: MATRIX 2.14.17 / MATRIX 6.1.72 / contracts/satellite/reporting.yaml#/components/schemas/MetricSource)*
- **loyalty**: Active members, Tier distribution (stacked bar), Member retention, Breakage rate, Points liability (AED, from the ledger). *(source: contracts/satellite/reporting.yaml#/components/schemas/MetricSource)*
- **inactive members**: "No visit last quarter" count per membership type, with Follow up opening the CRM segment. *(source: DI-718)*
- **retention cohort**: Cohort is refused as a mark; draw a heatmap (join month × months since) of retention %. *(source: contracts/satellite/reporting.yaml#/components/schemas/DashboardTile / MATRIX 8.7.25 / MATRIX 8.7.8)*
- **customer origin**: Bar by country / emirate (map cannot bind yet; never plot individual addresses). *(source: MATRIX 8.7.8)*

**Data it reads**: `getKpiValues` (onLoad, Membership and loyalty); `getDashboard` (onLoad, Loyalty dashboard (active members, tiers, liability …)

**Where the user goes next**

- → `ANL-020` Multi-Site & Performance Comparison: *Back to Multi-Site & Performance Comparison*
- → `ANL-001` Executive Command Center: *Executive Command Center*; carries `dashboardId`, `reportId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The customer membership loyalty list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the customer membership loyalty untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No customer membership loyalty yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the customer membership loyalty are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **A user without personal-data permission drills to members**: Aggregates only; names and contacts masked; export of personal data requires the audited permission. *(source: MATRIX 8.3.73 / contracts/shared/permissions.yaml#/components/schemas/Permission)*

#### Consistency with other screens

- Match `ANL-007`: Same segment names; ANL-007 owns purchase behaviour.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
venue: Aquaventure Waterpark (AED)
period: September 2026
membership: New 1,240 · Renewed 2,815 · Expired 612 · Renewal rate 82.1%
loyalty: Active members 38,450 · Gold 6% / Silver 21% / Blue 73% · Points liability AED 1,842,300.00
inactive: 'Annual pass holders with no visit last quarter: 1,906'
```

#### Permissions

- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff
- `getDashboard` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- CRM board: membership/loyalty visit history; retention/churn section flagging inactive customers (e.g. an annual pass holder with no visit last quarter flagged for follow-up); campaign performance and customer behaviour analytics. *(client request · MoM 8 Sep 2026, 4.9 Sales, Finance, Operations & CRM Boards · DI-718)*
- Further command-centre sections: revenue by sales channel; capacity utilisation by attraction/inventory item; top products by channel; conversion rate (site visits to completed purchase, cart abandonment, via Google Analytics); customer, membership and loyalty information. *(client request · MoM 8 Sep 2026, 4.2 Command Center Overview (Board 1) · DI-700)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A94** Hold the loyalty workshop and define the full programme configuration (tiers, point accrual, redemption, expiry, benefit unlocks) *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'loyalty')*
- **A134** Build the eligibility rules engine (residency/nationality with ID capture, minimum age by DOB, VIP-only profiles, loyalty-points thresholds, purchase limits per order/guest/category/channel) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'loyalty')*

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-017` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS172 Unified BI Reporting and AI Analytics Platform Board 1.dc.html#anl-017`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 1
- Flow F175 *Unified BI Reporting and AI Analytics Platform board 1: Multi-Site & …*, step 12: Works in Customer, Membership & Loyalty Pulse → Provide a consolidated view of customer health and engagement.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (400, 404).
- [ ] Every output is drawn (30 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-017?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-020`, `ANL-001`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-018` Alerts & Exception Center

**Create one centralized location for management-level KPI and operational exceptions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block C · task APP-ANALYTICS-ANL-018 |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Each Alert Shall Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/alerts-exception-center-anl-018` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process.** The management alerts and exceptions queue; from the ticketing angle, sales exceptions (sold-out sessions, unusual refunds, payment gateway mismatches) belong here. After Block A.

**Known correction pending (do not draw the wrong version)**

- **The screen's operations return no schema, so no column can be bound.** Why: Recorded gap. *(source: screens/P16-venue-analytics.yaml#ANL-018 gaps; Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every alerts exception** (data table)

| Shows | Format | Notes |
|---|---|---|
| Severity | text | not in the schema: `Severity` |
| KPI | text | not in the schema: `KPI` |
| Current value | text | not in the schema: `Current value` |
| Expected/target value | text | not in the schema: `Expected/target value` |
| Variance | text | not in the schema: `Variance` |
| Site | text | not in the schema: `Site` |
| Detection time | text | not in the schema: `Detection time` |
| Source system | text | not in the schema: `Source system` |
| Owner | text | not in the schema: `Owner` |
| Status | text | not in the schema: `Status` |
| Recommended action | text | not in the schema: `Recommended action` |

**The selected alerts exception** (detail panel): The pack groups this record's detail under its own headings: “Alert Categories”, “Alert Workflow”.

| Shows | Format | Notes |
|---|---|---|
| Severity | text | not in the schema: `Severity` |
| KPI | text | not in the schema: `KPI` |
| Current value | text | not in the schema: `Current value` |
| Expected/target value | text | not in the schema: `Expected/target value` |
| Variance | text | not in the schema: `Variance` |
| Site | text | not in the schema: `Site` |
| Detection time | text | not in the schema: `Detection time` |
| Source system | text | not in the schema: `Source system` |
| Owner | text | not in the schema: `Owner` |
| Status | text | not in the schema: `Status` |
| Recommended action | text | not in the schema: `Recommended action` |

**Data it reads**: `listPromotionAlertException` (onLoad, Promotion Alerts & Exception Center)

**Where the user goes next**

- → `ANL-020` Multi-Site & Performance Comparison: *Back to Multi-Site & Performance Comparison*
- → `ANL-001` Executive Command Center: *Executive Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The alerts exception list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the alerts exception untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No alerts exception yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the alerts exception are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
alert: Refunds at Main Gate till 3 are 4× the daily average · Fri 2 Oct
```

#### Permissions

- `listPromotionAlertException` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-018` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS172 Unified BI Reporting and AI Analytics Platform Board 1.dc.html#anl-018`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 1
- Flow F175 *Unified BI Reporting and AI Analytics Platform board 1: Multi-Site & …*, step 14: Works in Alerts & Exception Center → Create one centralized location for management-level KPI and operational exceptions.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-018?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-020`, `ANL-001`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-019` AI Management Insights

**Provide management with proactive AI-generated business intelligence rather than requiring users to manually analyze every dashboard.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-SETUP-ANL-019 |
| Who uses it | venue staff holding `AI_USE`, `REPORT_VIEW_VENUE` (2 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listAiInsights` reads the population and the selected insight is decided or explained — list, select, act (CHG-SOT-011). |
| Offline | online only |
| Opens with | `insightId` (navigation) |
| Route | `/analytics/ai-management-insights-anl-019` |

**Known gaps.** Removed 2 October 2026 (CHG-WIR-012): Two sources of anomalies on one card list show the same situation twice; ADR-0053 and the insight layer make ai.listAiInsights (kind anomaly) the one list … **The explanation carries no query or semantic spec** (design-notes correction ai ANL-019). ADR-0054 says an answer shows the query it ran; `NaturalLanguageAnswer` has `semanticSpec` and …

**From the AI & Intelligence process.** AI management insights: proactive findings for managers - a drop, a spike, a forecast miss, an opportunity - each with why it happened, broken down by channel, product and time, and what to do about it. Every number comes from a query the platform ran, never from the model; the model only words the result. The one thing to get right: an insight is a reviewable item with a lifecycle (new, reviewed, accepted or rejected, actioned, measured), and rejecting one with a reason is how the detector learns what is a false alarm.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- In Block A only decideAiInsight and explainMetricChange are in the slice; listAiInsights is not. (CHG-SOT-016)
- AiMetricChangeExplanation carries no query or semantic spec. (CHG-SOT-016)

**Fixed on main** (the package already carries these; draw what it says): The screen declares both reporting.listAnalyticsAnomalies and ai.listAiInsights. (CHG-WIR-012); Layout is an unbound primary button, table and Cancel. (CHG-SOT-011).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Kind | select field | — | — | — | — | Sends `?kind=`: anomaly, forecast deviation, trend, opportunity, executive summary, root cause. | — |
| Priority | select field | — | — | — | — | Sends `?priority=`. | — |
| Status | select field | — | — | — | — | Sends `?status=`; new and reviewed first by default. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | select | — | New · Reviewed · Accepted · Rejected · Actioned · Measured | `listAiInsights` ?status |
| Kind | select | — | Anomaly · Forecast deviation · Trend · Opportunity · Executive summary · Root cause · Forecast threshold · Marketing recommendation | `listAiInsights` ?kind |
| Priority | radio group | — | Low · Medium · High · Critical | `listAiInsights` ?priority |
| From | date and time picker | — | — | `listAiInsights` ?from |

**Form: Accept, Mark actioned or Reject** (modal, opened by *Accept, Mark actioned or Reject*; *Record decision* calls `decideAiInsight`, *Cancel* sends nothing)

**Collects what `decideAiInsight` sends.** Required: `decision` (set by the button: accept, actioned or reject). Optional: `reason` (asked for on Reject), `actionRef` (the work the insight led to, on Mark actioned). Dismissing sends nothing.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Decision `decision` | radio group | required | — | Review · Accept · Reject · Actioned | — | — | `decideAiInsight` body |
| Reason `reason` | text area | optional | — | max length 1000 | — | — | `decideAiInsight` body |
| Action ref `actionRef` | text field | optional | — | — | — | — | `decideAiInsight` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The move is not allowed from the insight's state.

**Form: Why did this change?** (drawer, opened by *Why did this change?*; *Explain* calls `explainMetricChange`, *Cancel* sends nothing)

**Filled from the selected insight**: `metricKey` and `period` come from it; the person picks the `comparison` (previous period or same period last year) and may add dimensions. Dismissing sends nothing.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Metric key `metricKey` | text field | required | — | — | — | — | `explainMetricChange` body |
| Period `period` | text field | required | — | — | — | ISO period, e.g. `2026-09-21/2026-09-27`. | `explainMetricChange` body |
| Comparison `comparison` | segmented control | optional | Previous period | Previous period · Same period last year · Forecast | — | — | `explainMetricChange` body |
| Dimensions `dimensions` | list of values (chips) | optional | — | — | — | — | `explainMetricChange` body |
| Keep `keep` | toggle | optional | off | — | — | — | `explainMetricChange` body |

**Rules for these inputs** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **decision (review / accept / reject / actioned)**: Reject asks a reason (the false-alarm signal); Actioned asks what was done (link to the action, e.g. a promotion or a rota change). *(source: contracts/satellite/ai.yaml#decideAiInsight)*
- **explain a metric (metric, period, comparison)**: Comparison previous period (default), same period last year, or forecast; year-on-year is offered only when history (own or imported) covers it. *(source: contracts/satellite/ai.yaml#explainMetricChange / ADR-0051 (AI functions review 30 Sep §4 Analytics assistant))*
- **Ask (askReportingQuestion)**: The free-text question box is behind a flag until Sprint 7 (8-26 February 2027); in Block A the screen shows saved insights and KPI explanations only. *(source: ADR-0054 / ADR-0059)*

#### Outputs: what the screen shows and produces

**Shown**

**Insights** (card list, from `listAiInsights`): **One list** (ADR-0053): anomalies are insights of kind anomaly, not a second source. Newest first; each card says what moved, by how much and how sure.

| Shows | Format | Notes |
|---|---|---|
| Title | text | — |
| Kind | chip: Anomaly, Forecast deviation, Trend, Opportunity, Executive summary, Root cause… | — |
| Priority | chip: Low, Medium, High, Critical | — |
| Status | chip: New, Reviewed, Accepted, Rejected, Actioned, Measured | — |
| Detected at | 1 Oct 2026, 14:30 | — |

**Ask about what moved** (assistant panel, from `askReportingQuestion`): Answers through the semantic layer and shows the query it ran (ADR-0054).

| Shows | Format | Notes |
|---|---|---|
| Conversation | text | — |
| Question | text | — |
| Interpretation | text | What the question was understood to mean, in plain language. When the question is outside the semantic model, the "not available yet" … |
| Semantic spec | grouped details | What the model returned instead of SQL (design 2.2 E, 5.7): metric, dimensions, filters, period, comparison, as validated against the … |
| Metric | text | A measure field code in the `SemanticModel`, or a `KpiDefinition.code`. The governed definition the dashboards use, so the number matches … |
| Dimensions | list or chips (count when long) | Field codes to group by. Each must be reachable from the metric's dataset through a relationship the semantic model declares. |
| Filters | list or chips (count when long) | — |
| Field | text | A `SemanticModel` field code. |
| Operator | chip: Equals, Not equals, Greater than, Less than, Between, In… | — |
| Values | list or chips (count when long) | Open on purpose; typed by the field. One value for the comparison operators, exactly two (from, to) for `between`, any number for `in` and … |
| Period | text | ISO 8601 interval in the venue's time zone, e.g. `2026-09-21/2026-09-27`, the form `explainMetricChange` takes. |
| Comparison | chip: Previous period, Same period last year, Target, Benchmark | As `getKpiValues` `compareTo`. With one, each row carries the metric for the comparison beside the current value. |
| Semantic model version | 1,234 | The `SemanticModel.version` the spec was validated and compiled against. Set by Reporting. |
| Generated query | grouped details | The query the spec compiled to: data source, columns, filters, grouping, and the compiled SQL in `compiledSql`. |
| Data source | chip: Orders, Order lines, Payments, Refunds, Shifts, Scan events… | What a report may be built over. A closed set, and that is the point — a builder that accepts any table will happily produce a report over … |
| Columns | list or chips (count when long) | — |
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Field | text | — |
| Label | text | — |
| Aggregation | chip: None, Count, Count distinct, Sum, Average, Min… | — |

**The selected insight** (detail panel, from `listAiInsights`): **Explainable and traceable**: the evidence items link to the data behind them.

| Shows | Format | Notes |
|---|---|---|
| Title | text | — |
| Narrative | text | — |
| Evidence | list or chips (count when long) | The evidence of one decision record, stored with it. |
| Recommended action | grouped details | For `marketingRecommendation`: `{recommendation, parameters}` as `AiMarketingRecommendation`. |
| Expected impact | grouped details | A range on a named metric (`metric`, `low`, `high`), never a single number (design 5.6). |
| Status | chip: New, Reviewed, Accepted, Rejected, Actioned, Measured | — |
| Decided at | 1 Oct 2026, 14:30 | — |
| Measured impact | grouped details | — |

**Why it changed** (detail panel, from `explainMetricChange`): The drivers in order of contribution and how reliable the explanation is (grounded, partial, conflicting sources, insufficient evidence).

| Shows | Format | Notes |
|---|---|---|
| Metric key | text | — |
| Period | text | — |
| Comparison | text | — |
| Change | 1,234.5 | — |
| Change percent | 1,234.5 | — |
| Drivers | list or chips (count when long) | — |
| Narrative | text | — |
| Reliability | chip: Grounded, Partial, Conflicting sources, Insufficient evidence | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Accept (primary button) | `decideAiInsight` POST `/insights/{insightId}/decide` | inline | AiInsight | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The move is not allowed from the insight's state. | opens modal first |
| Mark actioned (secondary button) | `decideAiInsight` POST `/insights/{insightId}/decide` | inline | AiInsight | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The move is not allowed from the insight's state. | opens modal first |
| Reject (destructive button) | `decideAiInsight` POST `/insights/{insightId}/decide` | inline | AiInsight | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The move is not allowed from the insight's state. | opens modal first |
| Why did this change? (secondary button) | `explainMetricChange` POST `/insights/explain-metric-change` | inline | AiMetricChangeExplanation | — | opens drawer first |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **insight card**: Title, kind (anomaly, forecast deviation, trend, opportunity, executive summary), priority, expected impact as a range on a named metric (never a single number), status, detected at. Evidence items labelled "From your data", "Calculated" or "AI inferred". *(source: contracts/satellite/ai.yaml#/components/schemas/AiInsight / contracts/satellite/ai.yaml#/components/schemas/AiEvidenceItem)*
- **why it changed**: The change and % for the period, drivers as a ranked contribution bar (e.g. Online -AED 18,400, POS +AED 2,100), the narrative, a reliability label (grounded, partial, conflicting sources, insufficient evidence) and "Data as of". No confidence percentage. *(source: contracts/satellite/ai.yaml#explainMetricChange / ADR-0054 / DI-719)*
- **basis**: For anomalies, the baseline's stage, e.g. "Learning - compared with the same weekday over 5 weeks"; in the first weeks against default thresholds and the forecast's low end. *(source: ADR-0051 (AI functions review 30 Sep §4 Anomaly detection) / ADR-0051)*

**What each action does** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Explain**: Runs the decomposition and shows drivers; "Keep" saves it as an insight. *(source: contracts/satellite/ai.yaml#explainMetricChange)*
- **Accept / Reject / Mark actioned**: Moves the insight along its lifecycle; measured is set later by the job that measures the effect. *(source: contracts/satellite/ai.yaml#decideAiInsight)*

**Data it reads**: `listAiInsights` (onLoad, Insights and anomalies)

**Where the user goes next**

- → `ANL-020` Multi-Site & Performance Comparison: *Back to Multi-Site & Performance Comparison*
- → `ANL-001` Executive Command Center: *Executive Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The insights list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the insights untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No insights yet: nothing has moved enough to report. Good news, not a failure; the ask panel stays available. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the kind, priority or status filter, and the insights are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `AI_USE`, which `listAiInsights` requires, and names that permission. **Never an empty list.** A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `REPORT_VIEW_VENUE` for `askReportingQuestion`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Question could not be interpreted. (ReportQuestionProblem); 409 The move is not allowed from the insight's state. |

#### Edge cases to draw

- **Question or metric outside the semantic model**: "Not available yet" naming what is not modelled; a knowledge gap is recorded; no improvised number. *(source: ADR-0054)*
- **Only a few weeks of data**: Comparison against the last 7 days, said explicitly; year-on-year appears once imported or own history covers it. *(source: ADR-0051 (AI functions review 30 Sep §4 Analytics assistant))*
- **The same situation detected by two detectors**: One insight (one correlation key), not two cards. *(source: contracts/satellite/ai.yaml#listAiInsights)*

#### Consistency with other screens

- Match `ANL-059`: History, evidence and explainability of the same insights.
- Match `ANL-055`: Anomalies appear here as insights of kind anomaly; same card.
- Match `ADM-506`: Same driver decomposition component.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
insight:
  title: Online revenue down 14% last weekend at Coastal Aqua
  kind: anomaly
  priority: high
  expectedImpact: AED 15,000-22,000 below forecast for the next weekend
  drivers:
  - Online -AED 18,400 (Family Day Pass)
  - POS +AED 2,100
  - 'Weather: 41°C Saturday (outdoor venue)'
  reliability: grounded
  dataAsOf: Mon 28 Sep 06:00
  basis: Learning - compared with the same weekday over 6 weeks
```

#### Permissions

- `askReportingQuestion` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `listAiInsights` → `AI_USE` (operate) · staff
- `decideAiInsight` → `AI_USE` (operate) · staff
- `explainMetricChange` → `AI_USE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `AI_USE`, which `listAiInsights` requires, and names that permission. **Never an empty list.** A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `REPORT_VIEW_VENUE` for `askReportingQuestion`.

Screen guard: `AI_USE`

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.7.30 | System shall support natural language reporting. | Unified Operations Dashboard | CONTRACTED | `askReportingQuestion` |
| 8.4.17 | System shall support AI-powered anomaly explanations. | Unified Operations Dashboard | CONTRACTED | `listAiInsights` |
| 8.4.18 | System shall support AI-powered root cause analysis. | Unified Operations Dashboard | CONTRACTED | `explainMetricChange` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- An AI layer across all dashboards explains why a metric changed (e.g. why revenue dropped on a given day) and recommends management actions from sales, revenue and attendance trends. *(client request · MoM 8 Sep 2026, 4.10 AI Intelligence Layer & KPI/Benchmarking Administration · DI-719)*
- Multi-site performance comparison (this month vs last month, or vs the same period last year), and AI management insights that surface possible reasons behind a change (e.g. a drop in attendance or revenue). *(client request · MoM 8 Sep 2026, 4.2 Command Center Overview (Board 1) · DI-701)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-019` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS172 Unified BI Reporting and AI Analytics Platform Board 1.dc.html#anl-019`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 1
- Flow F175 *Unified BI Reporting and AI Analytics Platform board 1: Multi-Site & …*, step 16: Works in AI Management Insights → Provide management with proactive AI-generated business intelligence rather than requiring users to manually analyze every dashboard.
- ADR-0054 *Natural-language analytics goes through the semantic layer* (`docs/adr/0054-natural-language-analytics-goes-through-the-semantic-layer.md`)
- ADR-0053 *Owners keep their deterministic rules; AI owns cross-entity risk, alerts and cases* (`docs/adr/0053-risk-layer-ownership.md`)
- ADR-0059 *AI phasing against the six-month plan* (`docs/adr/0059-ai-phasing-against-the-six-month-plan.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (41 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-019?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Accept, Mark actioned, Reject, Why did this change?.
- [ ] Every transition is wired: `ANL-020`, `ANL-001`.
- [ ] Every gated control is gated: `AI_USE`, `REPORT_VIEW_VENUE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-020` Multi-Site & Performance Comparison

**Allow enterprise management to compare sites, venues, attractions and business units.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-020 |
| Who uses it | venue staff holding `REPORT_VIEW_TENANT` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Comparison KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/multi-site-performance-comparison-anl-020` |

**What the spec says about it.** **Measure names, not "Revenue"** (decided 2 October 2026, Chinmay; CHG-FIN-002; BOARDREQ MOM-2758..2761). Takings (money taken less money paid back, a cash-control figure), Gross sales (before discounts, excluding VAT), Net revenue (gross sales less discounts and refunds), Recognised revenue and Deferred revenue are different numbers and never share a label; a tile takes its label from the seeded KPI it is bound to (`ReportingSystemKpi`).

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Multi-site comparison for enterprise management: compare sites, venues, attractions or business units on like-for-like KPIs, this month against last month or the same period last year, and drill into why they differ. It is also the landing of the client's Board 1. The one thing to get right: the normalisation basis (per visitor, per operating hour, per staffed position, per m²) travels with every comparison.

**Known correction pending (do not draw the wrong version)**

- **The benchmark read has no period or comparison parameter.** Why: DI-701 asks for this month vs last month / same period last year; getAnalyticsBenchmark takes only kpiId, scopePaths and normaliseBy. *(source: contracts/satellite/reporting.yaml#getAnalyticsBenchmark / DI-701; Finance, Ledger & Tax · Reporting & Analytics)*
- **The board's flow names a venue manager as the actor, but the benchmark needs tenant scope.** Why: A venue manager can never open the comparison; either the actor or the scope is wrong. *(source: F175 step 1 / contracts/satellite/reporting.yaml#getAnalyticsBenchmark; Finance, Ledger & Tax · Reporting & Analytics)*
- **Filters are "Scope path", "Period from", "Period to" and a normalisation-basis table is listed.** Why: A scope path is a spec leak; the basis table is configuration data owned by ANL-064. *(source: screens/P16-venue-analytics.yaml#ANL-020; Finance, Ledger & Tax · Reporting & Analytics)*
- **"Customer Satisfaction", "Operational Exceptions", "Revenue", "Revenue Growth", "Refund %" and "Average Transaction Value" have no metric source (only revenuePerVisitor exists).** Why: Draw them only once defined as KPIs; "outlet performance score" is also undefined; bare "Revenue" must become Net revenue. *(source: contracts/satellite/reporting.yaml#/components/schemas/MetricSource / MATRIX 4.5.25 / MATRIX 8.7.1; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Group comparison across currencies — converted at what rate, or kept per currency?** → Drawn default accepted: Per-currency groups. *(decided by Chinmay, 2026-10-02; DEC-325 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Scope path | text field | optional | — | — | — | Sends `?scopePath=` to `listSiteNormalisationBases`. | `listSiteNormalisationBases` ?scopePath |
| Period from | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?periodFrom=` to `listSiteNormalisationBases`. | `listSiteNormalisationBases` ?periodFrom |
| Period to | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?periodTo=` to `listSiteNormalisationBases`. | `listSiteNormalisationBases` ?periodTo |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kpi | picker: choose a kpi | — | — | `getAnalyticsBenchmark` ?kpiId |
| Scope paths | text field | — | — | `getAnalyticsBenchmark` ?scopePaths |
| Normalise by | radio group | — | None · Per visitor · Per operating hour · Per staffed position · Per square metre | `getAnalyticsBenchmark` ?normaliseBy |

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **sites**: Multi-select of sites in scope (labelled by name; never a scope path). *(source: contracts/satellite/reporting.yaml#getAnalyticsBenchmark)*
- **normalise by**: None, Per visitor, Per operating hour, Per staffed position, Per square metre; default Per visitor for money KPIs. *(source: contracts/satellite/reporting.yaml#/components/schemas/BenchmarkNormalisation)*
- **period and comparison**: This month vs last month (default) or vs same period last year. *(source: DI-701)*

#### Outputs: what the screen shows and produces

**Shown**

**Net revenue** (metric tile): (CHG-FIN-002: never a bare "Revenue")

**Revenue Growth** (metric tile)

**Attendance** (metric tile)

**Capacity Utilization** (metric tile)

**Revenue per Visitor** (metric tile)

**Average Transaction Value** (metric tile)

**Conversion** (metric tile)

**Refund %** (metric tile)

**Membership Conversion** (metric tile)

**Repeat Visitor %** (metric tile)

**Customer Satisfaction** (metric tile)

**F&B Spend** (metric tile)

**Retail Spend** (metric tile)

**Operational Exceptions** (metric tile)

**Every site normalisation basis** (data table, from `listSiteNormalisationBases`)

| Shows | Format | Notes |
|---|---|---|
| Period start | 1 Oct 2026 | — |
| Period end | 1 Oct 2026 | — |
| Visitors | 1,234 | `perVisitor`. |
| Operating hours | 1,234.5 | `perOperatingHour`. |
| Staffed positions | 1,234.5 | `perStaffedPosition`. Average positions staffed over the period. |
| Area square metres | 1,234.5 | `perSquareMetre`. Operated area. |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **comparison table**: Rows = sites, columns = KPIs; each cell shows the normalised value with the raw value beneath, the rank and the change vs the comparison period; the basis is in the column header ("Net revenue per visitor"). *(source: contracts/satellite/reporting.yaml#/components/schemas/BenchmarkRow)*
- **ranking chart**: Sorted bar per KPI; ribbon (rank over time) cannot bind yet. *(source: MATRIX 8.7.25 / contracts/satellite/reporting.yaml#/components/schemas/DashboardTile)*
- **AI reasons**: "Possible reasons" panel for the selected gap, opening root-cause analysis. *(source: DI-701)*

**Data it reads**: `getAnalyticsBenchmark` (onLoad, Site against site, normalised); `listSiteNormalisationBases` (onLoad, The denominators each site is benchmarked by)

**Where the user goes next**

- → `ANL-001` Executive Command Center: *Back to Executive Command Center*
- → `ANL-012` Live Operations Dashboard: *Live Operations Dashboard*
- → `ANL-013` Revenue Pulse: *Revenue Pulse*
- → `ANL-014` Attendance & Footfall Intelligence: *Attendance & Footfall Intelligence*
- → `ANL-015` Capacity & Utilization Monitor: *Capacity & Utilization Monitor*
- → `ANL-016` Sales & Channel Performance: *Sales & Channel Performance*
- → `ANL-017` Customer, Membership & Loyalty Pulse: *Customer, Membership & Loyalty Pulse*
- → `ANL-018` Alerts & Exception Center: *Alerts & Exception Center*
- → `ANL-019` AI Management Insights: *AI Management Insights*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The multi-site performance comparison list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the multi-site performance comparison untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No multi-site performance comparison yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the multi-site performance comparison are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A site has no basis for the period (visitors not recorded)**: "No basis for this period" in its cells; it is not ranked. *(source: contracts/satellite/reporting.yaml#/components/schemas/SiteNormalisationBasis)*
- **Sites in different base currencies**: Money KPIs are not ranked across currencies unless converted; shown per currency group. *(source: contracts/shared/common.yaml#/components/schemas/Money)*
- **A venue manager opens the board**: The comparison needs tenant scope; the screen says "Site comparison needs group access" rather than showing one site against itself. *(source: contracts/satellite/reporting.yaml#getAnalyticsBenchmark)*

#### Consistency with other screens

- Match `ANL-001`: The single-scope numbers on ANL-001 must equal the same site's raw value here.
- Match `ANL-064`: Normalisation bases are maintained on ANL-064; ANL-020 only shows them as footnotes per site.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
period: September 2026 vs August 2026
rows:
- Aquaventure Waterpark · Net revenue per visitor AED 131.80 (rank 1, +4.2%) · F&B spend per visitor AED 34.20
- Dubai Parks — Motiongate · AED 97.45 (rank 2, −1.8%) · AED 22.10
- House of Wisdom, Sharjah · AED 42.10 (rank 3, +0.6%) · AED 8.90
basis: 'Visitors: Aquaventure 284,100 · Motiongate 402,560 · House of Wisdom 31,780'
```

#### Permissions

- `getAnalyticsBenchmark` → `REPORT_VIEW_TENANT` (operate) · staff
- `listSiteNormalisationBases` → `REPORT_VIEW_TENANT` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Multi-site performance comparison (this month vs last month, or vs the same period last year), and AI management insights that surface possible reasons behind a change (e.g. a drop in attendance or revenue). *(client request · MoM 8 Sep 2026, 4.2 Command Center Overview (Board 1) · DI-701)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-020` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS172 Unified BI Reporting and AI Analytics Platform Board 1.dc.html#anl-020`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 1
- Flow F175 *Unified BI Reporting and AI Analytics Platform board 1: Multi-Site & …*, step 1: Opens Multi-Site & Performance Comparison → Allow enterprise management to compare sites, venues, attractions and business units.
- Flow F175 *Unified BI Reporting and AI Analytics Platform board 1: Multi-Site & …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F175 *Unified BI Reporting and AI Analytics Platform board 1: Multi-Site & …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F175 *Unified BI Reporting and AI Analytics Platform board 1: Multi-Site & …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F175 *Unified BI Reporting and AI Analytics Platform board 1: Multi-Site & …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F175 *Unified BI Reporting and AI Analytics Platform board 1: Multi-Site & …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F175 *Unified BI Reporting and AI Analytics Platform board 1: Multi-Site & …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F175 *Unified BI Reporting and AI Analytics Platform board 1: Multi-Site & …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F175 branch at step 1 (expected): when Nothing has been set up on Multi-Site & Performance Comparison yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F175 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-020?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-001`, `ANL-012`, `ANL-013`, `ANL-014`, `ANL-015`, `ANL-016`, `ANL-017`, `ANL-018`, `ANL-019`.
- [ ] Every gated control is gated: `REPORT_VIEW_TENANT`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P16 reference designs** (from `handoff/design-batches/apps/5-venue-management/README.md`)

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: for density and components.
- `sources/designs/TICVAI_Mobile.dc.html`: for finish and motion.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-028, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-039, DI-040, DI-041, DI-042, DI-043, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

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

### Across P16 Venue Analytics

- One consolidated, permission-based reporting/dashboard area: a user opens "dashboards" once and sees all dashboards their access allows (finance sees finance; a CEO sees sales, admissions, access control), with dashboard settings there too - not duplicated dashboard screens inside each functional module. *(agreed · MoM 8 Sep 2026, 4.11 Dashboard & Reporting Module Consolidation Strategy · DI-721)*
- Dashboards should refresh near-real-time (seconds) so management can monitor sales continuously rather than wait for periodic or end-of-day refreshes. *(agreed · MoM 8 Sep 2026, 4.6 Real-Time Reporting Architecture · DI-711)*
- Dashboards must be mobile-responsive so management (e.g. a CEO outside the venue) can log in from a smartphone via a URL rather than needing a laptop. *(agreed · MoM 8 Sep 2026, 4.1 Rationale for a Native BI/Reporting Platform · DI-696)*
- Decision: RBAC per role, per module, three levels — edit/view, view-only, hidden (e.g. a marketing officer does not see Finance at all) — plus sub-permissions within a module (a CRM role may get Campaigns and Communications but not Journeys). Default role templates, admin-customisable. *(agreed · MoM 20 Aug 2026, 4.7 Role-Based Access Control (RBAC); 5. Key Decisions · DI-387)*
- Back office is role-driven from any device: a finance user signing in from a workstation, laptop or home sees only finance reports and related information. *(agreed · MoM 12 Aug 2026, 3. Role-Based Access and Workstation-Linked Front-End · DI-248)*
- Load/traffic dashboards respect the tenancy model: a venue manager sees traffic for their own venue only. *(agreed · MoM 31 Jul 2026, 4. Non-Functional Requirements: Scalability & Availability · DI-061)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- AI Assistant panel: a short framing ("Based on last 30 days, here are 3 actions that can improve your revenue") then actionable recommendations, each with its potential impact (e.g. "Increase pricing for VIP seats, +12%") and a chevron, plus "View all recommendations". *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - AI Panels · DI-043)*
- Chart cards: title with period dropdown ("This Week"), headline metrics with deltas (Tickets Sold 12,840 +8.7%, Visitors, Conversion). Data visualisations must be easy to read. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Charts · DI-041)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Dynamic KPIs, forecasts and real-time insights; role-based dashboards, preferences and smart shortcuts for every user (e.g. greeting "Good morning, Ahmed" on the home screen, p2). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Smarter Data / Personalized Experience · DI-028)*
- Reports and historical searches must still retrieve archived transactions when required; the retention period (e.g. keep 3 of 5+ years live) is configurable per customer, archival manual or automated. *(agreed · MoM 28 Jul 2026, 23. Database Optimisation and Archiving · DI-018)*

### In P16 · Analytics

- Finance board: revenue by department and cost centre, shift-closing details, and payment gateway reconciliation, shown as bar and pie charts. *(client request · MoM 8 Sep 2026, 4.9 Sales, Finance, Operations & CRM Boards · DI-716)*

**11 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"askReportingQuestion": {"method":"POST","path":"/reports/ask","contract":"reporting","summary":"Natural-language reporting query","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"NaturalLanguageAnswer"},
"decideAiInsight": {"method":"POST","path":"/insights/{insightId}/decide","contract":"ai","summary":"Review, accept, reject or mark an insight actioned","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiInsight"},
"explainMetricChange": {"method":"POST","path":"/insights/explain-metric-change","contract":"ai","summary":"Why did this metric change","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiMetricChangeExplanation"},
"getAnalyticsBenchmark": {"method":"GET","path":"/analytics-benchmarks","contract":"reporting","summary":"One site against another, on a like-for-like basis","permission":"REPORT_VIEW_TENANT","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"kpiId","in":"query","required":true},{"name":"scopePaths","in":"query","required":null},{"name":"normaliseBy","in":"query","required":null}],"requestBody":null,"responds":"BenchmarkRow"},
"getDashboard": {"method":"GET","path":"/dashboards/{dashboardId}","contract":"reporting","summary":"Read a dashboard with tile data","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"refresh","in":"query","required":null}],"requestBody":null,"responds":"DashboardData"},
"getKpiValues": {"method":"GET","path":"/kpi-values","contract":"reporting","summary":"Current values, against target, with movement","permission":"REPORT_VIEW_VENUE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"kpiIds","in":"query","required":null},{"name":"kpiCodes","in":"query","required":null},{"name":"scopePath","in":"query","required":null},{"name":"period","in":"query","required":null},{"name":"compareTo","in":"query","required":null},{"name":"interval","in":"query","required":null},{"name":"groupBy","in":"query","required":null},{"name":"module","in":"query","required":null}],"requestBody":null,"responds":"KpiValue"},
"listAiInsights": {"method":"GET","path":"/insights","contract":"ai","summary":"Insights and anomalies","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"priority","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAlerts": {"method":"GET","path":"/alerts","contract":"reporting","summary":"What is currently wrong","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"severity","in":"query","required":null},{"name":"workstationId","in":"query","required":null},{"name":"shiftId","in":"query","required":null},{"name":"itemId","in":"query","required":null}],"requestBody":null,"responds":"Alert"},
"listPromotionAlertException": {"method":"GET","path":"/promotion-alert-exception","contract":"promotions","summary":"Promotion Alerts & Exception Center","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"PromotionAlertsExceptionCenterView"},
"listSiteNormalisationBases": {"method":"GET","path":"/site-normalisation-bases","contract":"reporting","summary":"The denominators each site is benchmarked by","permission":"REPORT_VIEW_TENANT","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"scopePath","in":"query","required":null},{"name":"periodFrom","in":"query","required":null},{"name":"periodTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiEvidenceItem": {"type":"object","x-ticvai-persistence":"none — held in jsonb on ai.decision_record.evidence, through AiEvidenceItemList","description":"One piece of evidence behind a decision, **labelled by origin** (AIC-197): read from a source system, derived by a rule or feature, or inferred by a model. An explanation is built from these, never from a model's chain of thought (AIC-192).","required":["label","kind"],"properties":{"label":{"type":"string","enum":["source","derived","modelInferred"]},"kind":{"type":"string","description":"What it is: `feature`, `rule`, `document`, `metric`, `transaction`, `candidateSet`."},"ref":{"type":"string","nullable":true,"description":"Where it came from: a table and id, a document chunk, a metric key."},"name":{"type":"string"},"value":{"type":"object","additionalProperties":true,"nullable":true},"observedAt":{"type":"string","format":"date-time","nullable":true}}},
"AiEvidenceItemList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"The evidence of one decision record, stored with it.","items":{"$ref":"#/components/schemas/AiEvidenceItem"}},
"AiInsight": {"type":"object","x-ticvai-persistence":"ai.insight","description":"**An insight with a lifecycle** (AIP-181): new, reviewed, accepted or rejected, actioned, measured. Anomalies, forecast deviations, trends and opportunities land here; the narrative binds numbers to results, so a figure can only come from a query (design 8, 5.10).","required":["kind","title","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"type":"string","enum":["anomaly","forecastDeviation","trend","opportunity","executiveSummary","rootCause","forecastThreshold","marketingRecommendation"]},"detectorId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.anomaly_detector"},"metricKey":{"type":"string","nullable":true},"subjectKind":{"type":"string","nullable":true,"enum":["campaign","journey","forecastDefinition","venue"],"description":"What the insight is about where it is not a KPI (29 September, build): a marketing-crm campaign or journey for `marketingRecommendation`, a forecast definition for `forecastThreshold`."},"subjectRef":{"type":"string","nullable":true},"recommendedAction":{"type":"object","additionalProperties":true,"nullable":true,"description":"For `marketingRecommendation`: `{recommendation, parameters}` as `AiMarketingRecommendation`. Applied by a person in the owning module, never here."},"expectedImpact":{"type":"object","additionalProperties":true,"nullable":true,"description":"A range on a named metric (`metric`, `low`, `high`), never a single number (design 5.6)."},"title":{"type":"string"},"narrative":{"type":"string","nullable":true},"evidence":{"$ref":"#/components/schemas/AiEvidenceItemList"},"magnitude":{"type":"number","nullable":true},"priority":{"type":"string","enum":["low","medium","high","critical"]},"correlationKey":{"type":"string","nullable":true},"status":{"type":"string","enum":["new","reviewed","accepted","rejected","actioned","measured"],"readOnly":true},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"decidedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"actionRef":{"type":"string","nullable":true},"measuredImpact":{"type":"object","additionalProperties":true,"nullable":true,"readOnly":true},"decisionRecordId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"detectedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiMetricChangeExplanation": {"type":"object","x-ticvai-persistence":"none — computed; written as an ai.insight of kind rootCause when kept","description":"**Why a metric changed** (AIP-176..180, ANL-056): drivers with their contribution, computed from the semantic layer. The narrative binds every figure to a result placeholder (design 8, 5.10).","required":["metricKey","change","drivers"],"properties":{"metricKey":{"type":"string"},"period":{"type":"string"},"comparison":{"type":"string"},"change":{"type":"number"},"changePercent":{"type":"number","nullable":true},"drivers":{"type":"array","items":{"type":"object","properties":{"dimension":{"type":"string"},"member":{"type":"string"},"contribution":{"type":"number"},"evidence":{"$ref":"#/components/schemas/AiEvidenceItem"}}}},"narrative":{"type":"string","nullable":true},"reliability":{"type":"string","enum":["grounded","partial","conflictingSources","insufficientEvidence"]},"dataAsOf":{"type":"string","format":"date-time"}}},
"Alert": {"type":"object","x-ticvai-persistence":"reporting.alert","description":"A raised alert. **Acknowledged rather than dismissed** — CF-134 asked for it markable, and the difference is that an acknowledgement records who saw it.\n","required":["id","ruleId","raisedAt","severity","status"],"properties":{"id":{"type":"string","format":"uuid"},"ruleId":{"type":"string","format":"uuid"},"ruleName":{"type":"string","description":"`AlertRule.name` as it stood when the alert was raised. **The line a person reads** — a list of rule ids is not an alert panel, and a screen should not need `listAlertRules` to label one.\n"},"metric":{"allOf":[{"$ref":"#/components/schemas/MetricSource"}],"description":"The rule's metric, carried so the alert says what went out of range."},"raisedAt":{"type":"string","format":"date-time"},"severity":{"$ref":"#/components/schemas/AlertSeverity"},"status":{"$ref":"#/components/schemas/AlertStatus"},"observedValue":{"$ref":"#/components/schemas/MetricValue"},"threshold":{"$ref":"#/components/schemas/MetricValue"},"scopePath":{"type":"string"},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"The workstation the reading was taken for, where the metric is measured per workstation (`salesByWorkstation`). Null otherwise. `listAlerts` filters on it."},"shiftId":{"type":"string","format":"uuid","nullable":true,"description":"The till shift (`orders.pos_shift`) the reading belongs to, where it was taken for a workstation with a shift open. Null otherwise. `listAlerts` filters on it."},"itemId":{"type":"string","format":"uuid","nullable":true,"description":"The inventory item the reading is about, where the metric is measured per item (`stockAgeing`, `stockTurnover`, `wastageRate`, `inventoryValuation`). Null otherwise. **What a replenishment screen prefills a requisition from.**\n"},"acknowledgedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"acknowledgedAt":{"type":"string","format":"date-time","nullable":true},"acknowledgementNote":{"type":"string","maxLength":300,"nullable":true,"description":"The `note` given to `acknowledgeAlert`. Kept, because an acknowledgement that says what is being done about it is the one escalation can skip."},"resolvedAt":{"type":"string","format":"date-time","nullable":true,"description":"**Set when the metric returns to range, automatically.** An alert that only a person can close is an alert list that only grows.\n"},"escalatedAt":{"type":"string","format":"date-time","nullable":true,"description":"Where `VenueSettings.alerting.escalateAfterMinutes` passed with no acknowledgement. **A critical alert nobody acknowledged is the case escalation exists for.**\n"}}},
"AlertSeverity": {"type":"string","description":"How urgent an alert rule's breach is. Shared by `AlertRule`, `Alert` and the `listAlerts` filter.","enum":["info","warning","critical"]},
"AlertStatus": {"type":"string","description":"Where a raised alert is. Shared by `Alert` and the `listAlerts` filter.","enum":["raised","acknowledged","resolved","expired"]},
"BenchmarkNormalisation": {"type":"string","description":"The basis a benchmark is compared on. Shared by `getAnalyticsBenchmark` and `BenchmarkRow`.","enum":["none","perVisitor","perOperatingHour","perStaffedPosition","perSquareMetre"]},
"BenchmarkRow": {"type":"object","description":"BI board 10.4. **The normalisation travels with the comparison.**","properties":{"scopePath":{"type":"string"},"label":{"type":"string"},"value":{"$ref":"#/components/schemas/MetricValue"},"normalisedValue":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"normaliseBy":{"$ref":"#/components/schemas/BenchmarkNormalisation"},"rank":{"type":"integer"},"percentile":{"type":"number","nullable":true}}},
"Dashboard": {"x-ticvai-persistence":"reporting.dashboard + reporting.dashboard_tile","allOf":[{"$ref":"#/components/schemas/CreateDashboardRequest"},{"type":"object","required":["id","ownerPrincipalId","aggregateCost","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"ownerPrincipalId":{"type":"string","format":"uuid"},"aggregateCost":{"type":"string","enum":["low","medium","high"],"description":"Combined refresh load of every tile."},"archivedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Set by `deleteDashboard`, which archives rather than removes.** A dashboard's tiles carry `visualisation`, `parameters` and `refresh_seconds` that somebody configured, and `reporting.dashboard_tile` cascades — so a hard delete takes an afternoon's work with it and leaves nothing to say what was there.\nArchived dashboards are excluded from `listDashboards` unless asked for with `includeArchived=true`.\n"},"createdAt":{"type":"string","format":"date-time"}}}]},
"DashboardData": {"x-ticvai-persistence":"none — computed","allOf":[{"$ref":"#/components/schemas/Dashboard"},{"type":"object","properties":{"tileData":{"type":"array","items":{"type":"object","properties":{"tileId":{"type":"string","format":"uuid"},"result":{"$ref":"#/components/schemas/ReportResult"},"isCached":{"type":"boolean"},"error":{"type":"string","nullable":true}}}}}}]},
"GeneratedQuery": {"x-ticvai-persistence":"none — embedded; stored whole in `reporting.natural_language_query`","type":"object","description":"The structured query a natural-language question produced — data source, columns, filters, grouping. Named on 26 September so the answer and the kept copy are one shape.\n","properties":{"dataSource":{"$ref":"#/components/schemas/DataSource"},"columns":{"type":"array","items":{"$ref":"#/components/schemas/ReportColumn"}},"filters":{"type":"array","items":{"$ref":"#/components/schemas/ReportFilter"}},"groupBy":{"type":"array","items":{"type":"string"}},"compiledSql":{"type":"string","nullable":true,"description":"The SQL the semantic spec compiled to, exactly as run on the analytical replica (29 September, design 5.7). The replica's row-level security applies beneath it, so it does not need to carry the caller's scope. Null on queries kept before the semantic compile.\n"}}},
"KpiValue": {"type":"object","description":"BI board 10.3. **Value, target, variance, direction and freshness in one read.**","properties":{"kpiId":{"type":"string","format":"uuid"},"code":{"type":"string"},"bucketStart":{"type":"string","format":"date-time","nullable":true,"description":"The start of the bucket this value covers, when `getKpiValues` was asked for an `interval`; null otherwise."},"groupKey":{"type":"string","nullable":true,"description":"The value of the `groupBy` dimension this row is for (a status, a category code, a tier); null when no `groupBy` was asked."},"name":{"type":"string"},"scopePath":{"type":"string"},"period":{"type":"string"},"value":{"$ref":"#/components/schemas/MetricValue"},"target":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"comparison":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"variancePercent":{"type":"number","nullable":true},"direction":{"type":"string","enum":["up","down","flat"]},"status":{"type":"string","enum":["green","amber","red","noTarget"]},"asOf":{"type":"string","format":"date-time"},"stale":{"type":"boolean","description":"**True when the pipeline behind it has not refreshed.** A number nobody flagged as stale is a number somebody will act on.\n"}}},
"MetricSource": {"type":"string","description":"**A named metric with a verified source.** BL-053, 75 requirement rows.\n`reporting` is a generic builder, and **a generic builder makes every reporting requirement look covered** — it will happily assemble a report over data nobody produces. That is the shape to watch across the whole walk, and this enum is the answer to it: each value below was checked against the schema before being named.\n| Metric | Source | |---|---| | `occupancy` | `catalogue.channel_capacity.sold` and `leased` against `capacity` | | `capacityUtilisation` | `catalogue.channel_capacity.remaining` over the same window | | `admissionRate` | `access.scan_event.outcome`, in-direction | | `noShowRate` | Entitlements issued against scans that never arrived | | `conversion` | `orders.cart` against `orders.sales_order` | | `salesByOperator` | `orders.sales_order.principal_id` | | `salesByWorkstation` | The workstation on the shift that took it | | `waitTime` | `queue.waiting_guest.estimated_call_at` against `called_at` | | `throughput` | `queue.waiting_guest` completions per hour | | `abandonmentRate` | Queue entries that left before being called |\n**`salesByInstructor` was deliberately absent from the first cut** because it needed the staff-assignment link CL-01 covers. It was added on 18 August once `resources.Resource` produced it — see `x-ticvai-extension-note` below. Naming a metric with no source is still the defect this enum exists to prevent.\n**Money-valued metrics are listed in `x-ticvai-money-valued`.** A reading or threshold on one of them is a `Money`, never a float (`MetricValue`).\n","enum":["occupancy","capacityUtilisation","admissionRate","noShowRate","conversion","salesByOperator","salesByWorkstation","waitTime","throughput","abandonmentRate","inventoryValuation","stockTurnover","stockAgeing","wastageRate","resaleVolume","resaleCommission","salesByInstructor","resourceUtilisation","allocationUtilisation","channelAllocationBurn","membershipChurn","membershipRenewalRate","supplierDeliveryPerformance","revenuePerEntitlement","revenuePerVisitor","assetDowntime","meanTimeToRepair","challengeCompletionRate","attributedRevenue","loyaltyActiveMembers","loyaltyTierDistribution","loyaltyPointsLiability","loyaltyBreakageRate","loyaltyMemberRetention","challengeParticipationRate","gamificationLoyaltyImpact","gamificationMembershipImpact","gamificationRetention","accreditationApplications","accreditationTimeToDecision","accreditationCredentialsIssued","accreditationActiveHolders","accreditationRenewalsDue","staffingShortfall","grossSales","discounts","refunds","netRevenue","recognisedRevenue","deferredRevenue","taxCollected","takings"],"x-ticvai-money-valued":["grossSales","discounts","refunds","netRevenue","recognisedRevenue","deferredRevenue","taxCollected","takings","inventoryValuation","resaleCommission","revenuePerEntitlement","revenuePerVisitor","attributedRevenue","loyaltyPointsLiability"],"x-ticvai-extended-29-september":"**Fourteen metrics added 29 September (build pass)**, each checked against the schema of the contract that produces it.\n\n| Metric | Source | Requirement | |---|---|---| | `loyaltyActiveMembers` | `marketing.loyalty_position` members with a `marketing.loyalty_points` movement in the period | 5.4.27 | | `loyaltyTierDistribution` | `marketing.loyalty_position.tier_id` against `marketing.programme_tier`, members per tier | 5.4.27 | | `loyaltyPointsLiability` | the balance of `ledger.journal_line` on each programme's `pointsLiabilityAccountId`, where points post on accrual and release on redemption or expiry | 5.4.27 | | `loyaltyBreakageRate` | `marketing.loyalty_points` expiry movements over points earned, in the period | 5.4.27 | | `loyaltyMemberRetention` | members with a movement in the previous period who also have one in this period | 5.4.27 | | `challengeParticipationRate` | distinct `marketing.challenge_progress.subject_id` over active loyalty members | 22.6.20 | | `gamificationLoyaltyImpact` | points earned per member, challenge participants against non-participants (`marketing.loyalty_points` split by `marketing.challenge_progress`) | 22.6.20 | | `gamificationMembershipImpact` | joins and renewals in `identity.customer_membership`, participants against non-participants | 22.6.20 | | `gamificationRetention` | return visits (`access.scan_event`, in-direction) of participants against non-participants | 22.6.20 | | `accreditationApplications` | `accreditation.application` by `status` | 12.1.50 | | `accreditationTimeToDecision` | `accreditation.application.decided_at` minus `submitted_at` | 12.1.50 | | `accreditationCredentialsIssued` | `accreditation.credential.issued_at` | 12.1.50 | | `accreditationActiveHolders` | `accreditation.holder` `active`, by `category_code` | 12.1.50 | | `accreditationRenewalsDue` | `accreditation.holder.valid_to` inside `accreditation.validity.renewal_window_days` | 12.1.50 |\n\n**`staffingShortfall` added the same evening (build pass, group G2; 8.2.49)**: the largest gap in the window between the staff rostered and the staff the forecast requires, per venue and position, from `workforce.forecast_requirement` (the handed-over AI staff requirement) against `workforce.rota_assignment` and `workforce.open_shift`, computed as `workforce.getStaffingCoverage` with `basis` `forecastRequirement`. An `AlertRule` on it with `comparator` `above` and `threshold` 0 is the staffing shortage alert; `windowMinutes` looks ahead rather than back for this metric (the rota for the coming window), and `cooldownMinutes` stops one short shift alerting every quarter hour.\n\n**Points issued, points redeemed, campaign performance and reward redemption were already served** by the `loyalty` and `campaigns` sources, and challenge completion and revenue attribution by `challengeCompletionRate` and `attributedRevenue`.\n","x-ticvai-extended-2-october":"**Eight finance measures added 2 October 2026** (Chinmay; CHG-FIN-007, CHG-FIN-010), each with the source and formula of the seeded KPI of the same code in `ReportingSystemKpi`: `grossSales`, `discounts`, `refunds`, `netRevenue`, `recognisedRevenue`, `deferredRevenue`, `taxCollected` and `takings`, so an alert rule can watch them (a refund spike, takings below a target). Formulas are the D-185 default; client finance sign-off is pending.","x-ticvai-money-valued-note":"**`salesByOperator`, `salesByWorkstation` and `resaleVolume` are not listed because the package does not say whether they count sales or sum their value.** Until that is decided, a rule on them carries a plain number.\n","x-ticvai-extended":"18 August 2026","x-ticvai-extension-note":"**Nineteen metrics added when their upstream models landed**, which is how BL-053 was always going to close — not by changing `reporting` but by building the things it wanted to report on.\n`inventoryValuation`, `stockTurnover`, `stockAgeing` and `wastageRate` came from `inventory.StockBatch`; `resaleVolume` and `resaleCommission` from `orders.ResaleListing`; **`salesByInstructor` from `resources.Resource`, which was the one metric this enum deliberately refused to name in the morning** because nothing produced it. `allocationUtilisation` from `PartnerUser` and `ChannelListing`, `membershipChurn` from `Journey`, `supplierDeliveryPerformance` from `ProductionRun`, `assetDowntime` and `meanTimeToRepair` from `WorkOrder.downtimeMinutes`, `challengeCompletionRate` from `ChallengeProgress`, `attributedRevenue` from `AttributionTouch`.\n**Each was checked against the schema before being named.** That rule has not changed — naming a metric with no source is the defect this enum exists to prevent.\n"},
"MetricValue": {"x-ticvai-persistence-column":"numeric(18,4)","description":"**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n","oneOf":[{"type":"number"},{"$ref":"../shared/common.yaml#/components/schemas/Money"}]},
"NaturalLanguageAnswer": {"x-ticvai-persistence":"none — computed","type":"object","required":["conversationId","question","interpretation","result","reliability"],"properties":{"conversationId":{"type":"string"},"question":{"type":"string"},"interpretation":{"type":"string","description":"What the question was understood to mean, in plain language. When the question is outside the semantic model, the \"not available yet\" sentence."},"semanticSpec":{"allOf":[{"$ref":"#/components/schemas/ReportingSemanticQuerySpec"}],"nullable":true,"description":"What the model returned instead of SQL (design 2.2 E, 5.7): metric, dimensions, filters, period, comparison, as validated against the semantic model. Null when the question is outside it. **Also kept**, on `NaturalLanguageQuery`, so a follow-up edits it.\n"},"generatedQuery":{"allOf":[{"$ref":"#/components/schemas/GeneratedQuery"}],"nullable":true,"description":"The query the spec compiled to: data source, columns, filters, grouping, and the compiled SQL in `compiledSql`. Returned so the answer can be checked. An answer nobody can verify is worse than no answer. **Also kept, as `NaturalLanguageQuery`**, for `saveNaturalLanguageQuery`. Null when the question is outside the semantic model.\n"},"result":{"allOf":[{"$ref":"#/components/schemas/ReportResult"}],"nullable":true,"description":"Null when the question is outside the semantic model."},"dataAsOf":{"type":"string","format":"date-time","nullable":true,"description":"Replica position the answer was read at, the result's `dataAsOf`, stated beside the answer so a figure that moved is not argued about. Null when nothing was run."},"reliability":{"$ref":"#/components/schemas/ReportingAnswerReliability"},"unavailableReason":{"allOf":[{"$ref":"#/components/schemas/ReportingUnavailableReason"}],"nullable":true,"description":"Set only when `reliability` is `insufficientEvidence` because the question is outside the semantic model (\"not available yet\"); names which part is not modelled."},"confidence":{"type":"number","minimum":0,"maximum":1,"deprecated":true,"description":"Superseded by `reliability` on 29 September (design 5.6, never a bare percentage for analytics). Returned for one release, then removed."},"suggestedFollowUps":{"type":"array","items":{"type":"string"}},"modelVersion":{"type":"string"},"tokensUsed":{"type":"integer"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PromotionAlertsExceptionCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Promotion Alerts & Exception Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"alertType":{"type":"string","enum":["missingProduct","missingEligibility","invalidDates","invalidDiscount","invalidCode","missingApproval","budgetNearLimit","budgetExceeded","marginBelowThreshold","excessiveDiscountExposure","promotionFailedToPublish","productUnavailable","bundleComponentUnavailable","channelSynchronizationFailure","lowConversion","lowRedemption","unexpectedHighRedemption","campaignUnderperforming","abnormalCouponUsage","excessiveRepeatRedemption","suspiciousCustomerBehavior","promoCodeLeakage"],"description":"What the alert is about."},"severity":{"type":"string","enum":["information","warning","critical"],"description":"Alert severity."},"alertId":{"type":"string","description":"Alert ID"},"promotionId":{"type":"string","description":"Promotion ID"},"alertCategory":{"type":"string","enum":["configuration","financial","operational","commercial","fraudRisk"],"description":"The pack's alert group."},"raisedAt":{"type":"string","format":"date-time","description":"When the alert was raised"}}},
"ReportResult": {"x-ticvai-persistence":"none — result set, cached in object storage","type":"object","required":["executionId","columns","rows"],"properties":{"executionId":{"type":"string"},"columns":{"type":"array","items":{"type":"object","properties":{"key":{"type":"string"},"label":{"type":"string"},"type":{"$ref":"#/components/schemas/FieldType"}}}},"rows":{"type":"array","description":"**Open on purpose; the shape is `columns`.** Each row is keyed by `columns[].key`, and each value is of that column's `type` — money as a `Money`, dates, date-times and uuids as strings. A report's columns are chosen at run time, so no fixed schema can name them.\n","items":{"type":"object","additionalProperties":true}},"totals":{"type":"object","additionalProperties":true,"description":"Aggregated columns only, keyed and typed as a row is."},"rowCount":{"type":"integer"},"nextCursor":{"type":"string","nullable":true},"generatedAt":{"type":"string","format":"date-time"},"dataAsOf":{"type":"string","format":"date-time","description":"Replica position the result was read at. Reporting reads a lag-tolerant replica, so this may trail the primary by seconds — stating it prevents an argument about a figure that moved.\n"}}},
"ReportingAnswerReliability": {"type":"string","description":"**How far an analytics answer can be relied on** (decided 29 September, AI system design 5.6): a category, never a bare percentage. `grounded`: every figure comes from a result of the compiled spec. `partial`: part of the question was answered and the rest was not modelled. `conflictingSources`: the result and a cited source disagree. `insufficientEvidence`: the question could not be answered, including \"not available yet\" outside the semantic model. The same four values as `ai.yaml`'s assistant answers.\n","enum":["grounded","partial","conflictingSources","insufficientEvidence"]},
"ReportingSemanticQuerySpec": {"x-ticvai-persistence":"none — embedded; stored whole in `reporting.natural_language_query`","type":"object","description":"**A question in the semantic model's own vocabulary** (decided 29 September, AI system design 2.2 E and 5.7). What the model returns for a live-number question instead of SQL, and what `runSemanticQuery` takes. Every code is a `SemanticModel` field code or a KPI code; Reporting validates the spec against the published model and compiles it deterministically, so the same spec compiles to the same SQL for the same model version.\n","required":["metric","period"],"properties":{"metric":{"type":"string","description":"A measure field code in the `SemanticModel`, or a `KpiDefinition.code`. The governed definition the dashboards use, so the number matches them."},"dimensions":{"type":"array","maxItems":5,"description":"Field codes to group by. Each must be reachable from the metric's dataset through a relationship the semantic model declares.","items":{"type":"string"}},"filters":{"type":"array","items":{"type":"object","required":["field","operator"],"properties":{"field":{"type":"string","description":"A `SemanticModel` field code."},"operator":{"type":"string","enum":["equals","notEquals","greaterThan","lessThan","between","in","notIn","isNull","isNotNull"]},"values":{"type":"array","description":"**Open on purpose; typed by the field.** One value for the comparison operators, exactly two (from, to) for `between`, any number for `in` and `notIn`, none for `isNull` and `isNotNull`.\n","items":{}}}}},"period":{"type":"string","description":"ISO 8601 interval in the venue's time zone, e.g. `2026-09-21/2026-09-27`, the form `explainMetricChange` takes."},"comparison":{"type":"string","nullable":true,"description":"As `getKpiValues` `compareTo`. With one, each row carries the metric for the comparison beside the current value.","enum":["previousPeriod","samePeriodLastYear","target","benchmark"]},"semanticModelVersion":{"type":"integer","readOnly":true,"description":"The `SemanticModel.version` the spec was validated and compiled against. Set by Reporting."}}},
"ReportingUnavailableReason": {"type":"string","description":"Which part of a question is outside the semantic model, so the answer is \"not available yet\" (design 5.7). A metric or field the caller may not see is reported as not modelled, so the reason does not reveal that it exists.","enum":["metricNotModelled","dimensionNotModelled","filterNotModelled","comparisonNotAvailable","periodOutsideHistory"]},
"SiteNormalisationBasis": {"type":"object","x-ticvai-persistence":"reporting.site_normalisation_basis","description":"BI boards 7.9 and 10.4. **The denominators a benchmark divides by**, per site and period: visitors, operating hours, staffed positions and area, one for each `BenchmarkNormalisation` other than `none`. Read by `getAnalyticsBenchmark` for the period that covers the benchmark (data model, 29 September).\n","required":["scopePath","periodStart","periodEnd"],"properties":{"id":{"type":"string","format":"uuid"},"scopePath":{"type":"string","description":"The site (venue scope) the basis applies to."},"periodStart":{"type":"string","format":"date"},"periodEnd":{"type":"string","format":"date"},"visitors":{"type":"integer","nullable":true,"minimum":0,"description":"`perVisitor`."},"operatingHours":{"type":"number","nullable":true,"minimum":0,"description":"`perOperatingHour`."},"staffedPositions":{"type":"number","nullable":true,"minimum":0,"description":"`perStaffedPosition`. Average positions staffed over the period."},"areaSquareMetres":{"type":"number","nullable":true,"minimum":0,"description":"`perSquareMetre`. Operated area."}}}
}
```
