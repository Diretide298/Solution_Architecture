# P06-operations-02 — P06 · Operations (2 of 5)

**10 screens · 26 operations · 44 schemas · 10 permissions**

Platform P06 Venue Staff App · ships as **venue-staff-mobile** ·
staff audience · mobileApp ·
offline-capable

## Who this is for

**staff on mobileApp.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 10 permissions apply here:
  `ACCESS_OVERRIDE, ACCESS_VALIDATE, AI_USE, ATTENDANCE_RECORD, ORDER_REPRINT, ORDER_VIEW, PRODUCT_VIEW, REPORT_VIEW_VENUE, TICKET_LOOKUP, WORKFORCE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **11 of these operations work offline**: getOrder, listCatalogueBundles, listOrderRefunds, listOrders, listRotaAssignments, lookupTicket, overrideAccess, recordAttendance
  — and the rest do not. A surface that looks the same online and off is lying.
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
| `EMP-014` | Ticket lookup | C | 11 | 23 | 6 | 27 | 2 | 0 | — | notStarted (generated) |
| `EMP-015` | Group scan | C | 37 | 12 | 6 | 60 | 1 | 0 | — | notStarted (generated) |
| `EMP-017` | Sync & reconciliation | C | 35 | 16 | 6 | 60 | 2 | 0 | — | notStarted (generated) |
| `EMP-018` | Offline package | B | 3 | 14 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `EMP-019` | AI assistant — home | D | 4 | 9 | 6 | 16 | 1 | 0 | — | notStarted (generated) |
| `EMP-020` | AI assistant — answer | D | 7 | 9 | 6 | 17 | 1 | 0 | — | notStarted (generated) |
| `EMP-021` | Roster | D | 6 | 9 | 6 | 15 | 1 | 0 | — | notStarted (generated) |
| `EMP-022` | My rota | D | 6 | 9 | 6 | 15 | 2 | 0 | — | notStarted (generated) |
| `EMP-023` | Swap request | B–D | 6 | 12 | 6 | 15 | 2 | 0 | — | notStarted (generated) |
| `EMP-024` | Clock in / out | D | 9 | 14 | 6 | 4 | 3 | 0 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `EMP-014` Ticket lookup

**Answer a question without admitting anybody.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `ticketing` module |
| Block | Block C · task APP-STAFF-EMP-014 |
| Who uses it | venue staff holding `ORDER_REPRINT`, `ORDER_VIEW` (1 operate, 1 read) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listOrders` reads the population and `getOrder` reads one of them — list, select, act |
| Offline | Searches the bundle only. A ticket issued after the last sync will not be found, and the screen says so |
| Opens with | `orderId` (deepLink) · cold entry: **A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the … |
| Route | `/operations/ticket-lookup` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-018): Ten order-changing actions on a lookup screen whose purpose is to answer a question without acting; the employee app has a basic validity lookup, not sales … Removed 2 October 2026 (CHG-WIR-018): Ten order-changing actions on a lookup screen whose purpose is to answer a question without acting; the employee app has a basic validity lookup, not sales … Removed 2 October 2026 (CHG-WIR-018): Ten order-changing actions on a lookup screen whose purpose is to answer a question without acting; the employee app has a basic validity lookup, not sales …

**From the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process.** Ticket lookup on the staff handheld: answer a guest's question about a ticket without admitting anybody. After Block A. Shows the full consumption and scan history; any override is logged.

**Fixed on main** (the package already carries these; draw what it says): Ten order-changing actions (create, discount, refund, exchange, hold, modify, reschedule, resume, void) on a lookup screen. (CHG-WIR-018).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listOrders`. | `listOrders` ?venueId |
| Principal id | picker: choose a principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?principalId=` to `listOrders`. | `listOrders` ?principalId |
| Shift id | picker: choose a shift (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?shiftId=` to `listOrders`. | `listOrders` ?shiftId |
| Status | select | optional | — | Pending · Held · Paid · Partially paid · Completed · Voided · Refunded · Partially refunded · Failed; It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed. | — | Sends `?status=` to `listOrders`. | `listOrders` ?status |
| Created from | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?createdFrom=` to `listOrders`. | `listOrders` ?createdFrom |
| Created to | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?createdTo=` to `listOrders`. | `listOrders` ?createdTo |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Workstation | picker: choose a workstation | — | — | `listOrders` ?workstationId |
| Subject | picker: choose a subject | — | — | `listOrders` ?subjectId |
| Tender | select | — | Cash · Card · Wallet · Voucher · Bank transfer · Hotel charge · Installment · Gift card · Complimentary | `listOrders` ?tender |

**Form: Reprint order** (modal, opened by *Reprint order*; *Reprint order* calls `reprintOrder`, *Cancel* sends nothing)

**Collects what `reprintOrder` sends before it is called.** Required: `delivery`, `recordedAt`. Optional: `destination`, `lineIds`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Delivery `delivery` | radio group | required | — | Print · Email · SMS · Whatsapp · Wallet | — | — | `reprintOrder` body |
| Destination `destination` | text field | optional | — | — | — | — | `reprintOrder` body |
| Lines `lineIds` | multi-picker: choose lines | optional | — | — | — | Omit to reprint every line. | `reprintOrder` body |
| Reason `reason` | radio group | optional | — | Printer fault · Guest request · Lost ticket · Not received · Other | — | — | `reprintOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | When the till reprinted — device time, as for every offline-capable write. | `reprintOrder` body |

Errors to draw in the form: 400 Validation failed

#### Outputs: what the screen shows and produces

**Shown**

**Every order** (data table, from `listOrders`)

| Shows | Format | Notes |
|---|---|---|
| Order number | text | — |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | The same vocabulary as `Order.channel`, which this projects. |
| Line count | 1,234 | — |

**Every refund** (data table, from `listOrderRefunds`)

| Shows | Format | Notes |
|---|---|---|
| FX rate | text | The rate on the original payment, not today's (BL-087, CF-118). `Payment` records `tenderCurrency`, `fxRate` and `fxRateSource` at the … |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Applied percentage | 1,234.5 | From the venue's time bands, or an approver override. |
| Status | chip: Pending approval, Pending gateway, Completed, Declined, Failed | — |

**The selected order** (detail panel, from `listOrders`)

| Shows | Format | Notes |
|---|---|---|
| Order number | text | — |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunded amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Hold label | text | As `Order.holdLabel`. |

**The order statement** (detail panel, from `getOrderStatement`)

| Shows | Format | Notes |
|---|---|---|
| Order number | text | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Total paid | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total refunded | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Current balance | AED 1,234.50 | Positive means the guest owes; negative means a refund is outstanding. |

**The order** (detail panel, from `getOrder`)

| Shows | Format | Notes |
|---|---|---|
| Order number | text | The number a guest reads and a cashier types. Server-assigned: the venue prefix and a sequence per venue, for example `DXB1-000123` … |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Net amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Reprint order (secondary button) | `reprintOrder` POST `/orders/{orderId}/reprints` | inline | inline | 400 Validation failed | works offline; opens modal first; produces a document or message: Reprint or resend tickets |

**Rules for what is shown** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **ticket history**: Purchaser, validity, every scan (gate, time, result), entries left, wallet balance and F&B or retail spend against it. *(source: DI-462; DI-649)*

**Data it reads**: `listOrders` (onLoad, List orders)

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The ticket lookup list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the ticket lookup untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No ticket lookup yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, principalId, shiftId, status, createdFrom, createdTo and the ticket lookup are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `listOrders` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ORDER_REPRINT` for `reprintOrder`. |
| Offline (`?state=offline`) | Searches the bundle only. A ticket issued after the last sync will not be found, and the screen says so |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **Offline**: Searches the device bundle only and says a ticket issued after the last sync will not be found. *(source: screens/P06-staff-app.yaml#EMP-014 states.offline)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
ticket: YAS1-000123-02 · Day Pass Adult · Fri 2 Oct · scanned Main Gate 09:41 (admitted), Gate 3 10:12 (re-entry)
```

#### Permissions

- `listOrders` → `ORDER_VIEW` (read) · staff, guest, partner
- `getOrder` → `ORDER_VIEW` (read) · staff, guest, partner
- `getOrderStatement` → `ORDER_VIEW` (read) · staff, partner
- `listOrderRefunds` → `ORDER_VIEW` (read) · staff, partner
- `reprintOrder` → `ORDER_REPRINT` (operate) · staff, guest, partner, device

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `listOrders` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ORDER_REPRINT` for `reprintOrder`.

#### Requirements it meets

27 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.3.7 | The system should allow access to their purchase history and ongoing orders and preferences. | F&B & Guest Management | CONTRACTED | `listOrders` |
| 5.9.4 | The system should be able to provide a detailed log of transactions for each till. Detailed log of transaction should be always accessible, searchable and printable at back office. | F&B & Guest Management | CONTRACTED | `listOrders` |
| 22.2.11 | Ticketing History | Marketing & CRM | CONTRACTED | `listOrders` |
| 22.2.12 | Membership History | Marketing & CRM | CONTRACTED | `listOrders` |
| 22.2.15 | Reservation History | Marketing & CRM | CONTRACTED | `listOrders` |
| 19.2.12 | Ticket Viewing - System shall display ticket details. | Guest Mobile App & Branding | CONTRACTED | `getOrder` |
| 2.6.2 | Post-order service 1) On the order details page, users can view the order number, amount, time, payment method, user information, refund/change policies, and the QR code of the e-ticket 2) During the … | Ticketing Sales | CONTRACTED | `getOrder` |
| 2.12.27 | All orders can be finalized for payment registration or modified or even cancelled at the Guest Service or any reservation PC. | Ticketing Sales | CONTRACTED | `getOrder` |
| 5.7.8 | The system should be able to use of a unique Order or Reference number (PNR) for each transaction, which can be communicated to the Payment Gateway, Acquiring Bank and the ERP system for … | F&B & Guest Management | CONTRACTED | `getOrder` |
| 1.6.16 | System shall maintain immutable audit logs for listings, approvals, purchases, ownership transfers, cancellations, and administrative actions. | Ticketing Catalogue | CONTRACTED | `getOrderStatement` |
| 2.7.40 | The system should provide: - Management and display/communication of payments due and balance. - Management of the possibility to cancel or refund an order. - Alerts to B2B clients for credit limit … | Ticketing Sales | CONTRACTED | `getOrderStatement` |
| 2.12.32 | System shall maintain a complete audit history showing all order activities including creation, modifications, upgrades, refunds, cancellations, transfers, communications, redemptions, and user … | Ticketing Sales | CONTRACTED | `getOrderStatement` |
| … 15 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Ticket lookup shows the complete scan history: purchaser, gate and timestamp for every attempt. Security can manually override to admit a guest despite a scan issue; every override is logged against the visitor's record. *(client request · MoM 2 Sep 2026, 4.16 Ticket Lookup & Manual Override · DI-649)*
- Ticket look-up shows the ticket's full consumption history: transaction date/time, number of scans, expiry, and (if applicable) wallet balance and F&B/retail spend against that ticket. *(client request · MoM 25 Aug 2026, 4.7 Entitlements & Access Control · DI-462)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-014` · status **notStarted** · provenance generated
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (23 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-014?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Reprint order.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`.
- [ ] Every gated control is gated: `ORDER_REPRINT`, `ORDER_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-015` Group scan

**Admit a party on one credential.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 2 · needs the `access` module |
| Block | Block C · task APP-STAFF-EMP-015 |
| Who uses it | venue staff holding `ACCESS_OVERRIDE`, `ACCESS_VALIDATE`, `REPORT_VIEW_VENUE`, `TICKET_LOOKUP` (4 operate) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listScans` reads the population and `getOfflinePackage` reads one of them — list, select, act |
| Offline | Fully offline. Admits what is valid and states the shortfall |
| Opens with | nothing: it opens on its own |
| Route | `/operations/group-scan` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Group admission on the Staff App: one credential, counted admissions, partial entry normal. The one thing to get right: the same counter and stepper as SCN-007.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Access point id | picker: choose an access point (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?accessPointId=` to `listScans`. | `listScans` ?accessPointId |
| Ticket id | picker: choose a ticket (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?ticketId=` to `listScans`. | `listScans` ?ticketId |
| Outcome | segmented control | optional | — | Admitted · Denied · Overridden | — | Sends `?outcome=` to `listScans`. | `listScans` ?outcome |
| Recorded from | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?recordedFrom=` to `listScans`. | `listScans` ?recordedFrom |
| Recorded to | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?recordedTo=` to `listScans`. | `listScans` ?recordedTo |
|  | text area | optional | — | max length 256 | — | **A screen that validates a credential needs somewhere to point the camera.** `denied` and `hardwareError` look different because an operator facing a guest needs to know whether to try again or … | `ValidateRequest.mediaCode` |
| Search | text area | optional | — | max length 256 | — | Sends `?mediaCode=` to `lookupTicket` (a code typed when the camera cannot read it) (CHG-RFM-012). A search that returns nothing must say so differently from a search not yet run. | `lookupTicket` ?mediaCode |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Since version | number field | — | — | `getOfflinePackage` ?sinceVersion |
| Valid from | date and time picker | — | — | `getOfflinePackage` ?validFrom |
| Valid to | date and time picker | — | — | `getOfflinePackage` ?validTo |

**Form: Sync scans** (modal, opened by *Sync scans*; *Sync scans* calls `syncScans`, *Cancel* sends nothing)

**Collects what `syncScans` sends before it is called.** Required: `deviceId`, `scans`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Device `deviceId` | picker: choose a device | required | — | — | shows names, sends the id | Sequence numbers are monotonic per device, not globally. | `syncScans` body |
| Scans `scans` | repeatable rows | required | — | at least 1; at most 500 | — | — | `syncScans` body |
| ID `scans[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7. Also the idempotency key and dedupe key. | `syncScans` body |
| Media code `scans[].mediaCode` | text area | required | — | max length 256 | — | What was read from the media. NOT the ticket id — media can be re-linked over a ticket's life. | `syncScans` body |
| Media kind `scans[].mediaKind` | select | required | — | Image · Video · Audio · Document · Vector · Font · Archive · Model3d; glb`) venue model, at most 40 MB. | — | `model3d` added 3 October 2026 (r1 additions; ADR-0069 action item 4): a glTF binary (`model/gltf-binary`, `.glb`) venue model, at most 40 MB. | `syncScans` body |
| Direction `scans[].direction` | radio group | required | — | Entry · Exit · Reentry · Crossover | — | — | `syncScans` body |
| Group size `scans[].groupSize` | number field | optional | — | min 1 | — | For group media admitting several holders on one read. | `syncScans` body |
| Proximity token `scans[].proximityToken` | text field | optional | — | — | — | BLE proximity assertion where the venue requires the operator to be physically at the gate. | `syncScans` body |
| Recorded at `scans[].recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the read. Authoritative for ordering, not for validity. | `syncScans` body |
| Sequence `scans[].sequence` | number field | required | — | min 1 | — | Monotonic per device. The server processes in this order. | `syncScans` body |
| Local outcome `scans[].localOutcome` | segmented control | required | — | Admitted · Denied · Overridden | — | What the device decided offline. The server is authoritative and may disagree; disagreements are returned for reconciliation, not discarded. | `syncScans` body |
| Local deny reason `scans[].localDenyReason` | select | optional | — | Not found · Not yet valid · Expired · Already used · Reentry limit reached · Exit required before reentry · Wrong access point · Wrong performance · Outside admission window · Entitlement suspended · Blacklisted · Capacity reached … | — | Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a boolean. | `syncScans` body |
| Overridden by principal `scans[].overriddenByPrincipalId` | picker: choose an overridden by principal | optional | — | — | shows names, sends the id | — | `syncScans` body |
| Override reason `scans[].overrideReason` | text field | optional | — | — | — | — | `syncScans` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Form: Validate access** (modal, opened by *Validate access*; *Validate access* calls `validateAccess`, *Cancel* sends nothing)

**Collects what `validateAccess` sends before it is called.** Required: `id`, `mediaCode`, `mediaKind`, `direction`, `recordedAt`. Optional: `groupSize`, `proximityToken`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7. Also the idempotency key and dedupe key. | `validateAccess` body |
| Media code `mediaCode` | text area | required | — | max length 256 | — | What was read from the media. NOT the ticket id — media can be re-linked over a ticket's life. | `validateAccess` body |
| Media kind `mediaKind` | select | required | — | Image · Video · Audio · Document · Vector · Font · Archive · Model3d; glb`) venue model, at most 40 MB. | — | `model3d` added 3 October 2026 (r1 additions; ADR-0069 action item 4): a glTF binary (`model/gltf-binary`, `.glb`) venue model, at most 40 MB. | `validateAccess` body |
| Direction `direction` | radio group | required | — | Entry · Exit · Reentry · Crossover | — | — | `validateAccess` body |
| Group size `groupSize` | number field | optional | — | min 1 | — | For group media admitting several holders on one read. | `validateAccess` body |
| Proximity token `proximityToken` | text field | optional | — | — | — | BLE proximity assertion where the venue requires the operator to be physically at the gate. | `validateAccess` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the read. Authoritative for ordering, not for validity. | `validateAccess` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 Media not recognised in this cell

**Form: Validate group access** (modal, opened by *Validate group access*; *Validate group access* calls `validateGroupAccess`, *Cancel* sends nothing)

**Collects what `validateGroupAccess` sends before it is called.** Required: `id`, `mediaCode`, `admitCount`, `recordedAt`. Optional: `direction`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `validateGroupAccess` body |
| Media code `mediaCode` | text area | required | — | max length 256 | — | — | `validateGroupAccess` body |
| Admit count `admitCount` | number field | required | — | min 1 | — | — | `validateGroupAccess` body |
| Direction `direction` | radio group | optional | — | Entry · Exit · Reentry · Crossover | — | — | `validateGroupAccess` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `validateGroupAccess` body |

Errors to draw in the form: 403 Authenticated but not permitted at the requested scope; 409 Requested count exceeds the remaining group allowance

**Sent by *Override access*** (`overrideAccess`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `overrideAccess` body |
| Scan `scanId` | picker: choose a scan | required | — | — | shows names, sends the id | The denied scan being overridden. | `overrideAccess` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `overrideAccess` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `overrideAccess` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every scan event** (data table, from `listScans`)

| Shows | Format | Notes |
|---|---|---|
| Media code | text | — |
| Outcome | chip: Admitted, Denied, Overridden | — |

**The selected scan event** (detail panel, from `listScans`)

| Shows | Format | Notes |
|---|---|---|
| Media code | text | — |
| Outcome | chip: Admitted, Denied, Overridden | — |
| Deny reason | chip: Not found, Not yet valid, Expired, Already used, Reentry limit reached, Exit … | Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a … |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Synced at | 1 Oct 2026, 14:30 | Null while pending. Differs from recordedAt for offline scans. |

**The offline package** (detail panel, from `getOfflinePackage`)

| Shows | Format | Notes |
|---|---|---|
| Generated at | 1 Oct 2026, 14:30 | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |
| Entitlements | list or chips (count when long) | Read from `access.entitlement` (SD-052). With `sinceVersion`, only the rows changed after it, including ones now void or used, so a device … |
| Delegated rights | list or chips (count when long) | Redemption rights issued by other cells and valid at this access point. Included in the package so a cross-region entitlement still admits … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Sync scans (primary button) | `syncScans` POST `/access/scans` | inline | ScanSyncResult | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | opens modal first |
| Lookup ticket (secondary button) | `lookupTicket` GET `/access/lookup` | — | TicketStatus | 400 Neither mediaCode nor ticketId supplied; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | works offline; produces a document or message: Read-only validity check without admitting |
| Override access (destructive button) | `overrideAccess` POST `/access/override` | inline | ValidationResult | 403 Authenticated but not permitted at the requested scope; 409 The scan was not a denial, or has already been overridden | works offline |
| Validate access (secondary button) | `validateAccess` POST `/access/validate` | ValidateRequest | ValidationResult | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 Media not recognised in this cell | works offline; opens modal first |
| Validate group access (secondary button) | `validateGroupAccess` POST `/access/group-validate` | inline | ValidationResult | 403 Authenticated but not permitted at the requested scope; 409 Requested count exceeds the remaining group allowance | works offline; opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Group counter**: As SCN-007. *(source: contracts/spine/access.yaml#validateGroupAccess / DI-137)*

**Data it reads**: `listScans` (onLoad, List scan events); `getOfflinePackage` (onLoad, Entitlement and rule set for offline validation)

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*

**What opens over it**

- confirmDialog *Override access*: **Names what `overrideAccess` changes and what it leaves alone**, in the consequence rather than the verb. A group scan this affects should be identified in the dialog, not just counted. **Collects what `overrideAccess` sends before it is called.** Required: `id`, `scanId`, `reason`, `recordedAt`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The group scan list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the group scan untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No group scan yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on accessPointId, ticketId, outcome, recordedFrom, recordedTo and the group scan are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listScans` requires to show this screen, and names that permission (the screen's other reads need `ACCESS_VALIDATE` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ACCESS_OVERRIDE` for `overrideAccess`; `TICKET_LOOKUP` for … |
| Offline (`?state=offline`) | Fully offline. Admits what is valid and states the shortfall |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Neither mediaCode nor ticketId supplied; 400 Validation failed; 409 Requested count exceeds the remaining group allowance; 409 The scan was not a denial, or has already been overridden |

#### Consistency with other screens

- Match `SCN-007`: Same component.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
group:
  booking: Yas Tours - 12 pax
  admitted: 10
  remaining: 2
```

#### Permissions

- `listScans` → `REPORT_VIEW_VENUE` (operate) · staff
- `syncScans` → `ACCESS_VALIDATE` (operate) · staff
- `getOfflinePackage` → `ACCESS_VALIDATE` (operate) · staff
- `lookupTicket` → `TICKET_LOOKUP` (operate) · staff
- `overrideAccess` → `ACCESS_OVERRIDE` (operate) · staff
- `validateAccess` → `ACCESS_VALIDATE` (operate) · staff
- `validateGroupAccess` → `ACCESS_VALIDATE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listScans` requires to show this screen, and names that permission (the screen's other reads need `ACCESS_VALIDATE` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ACCESS_OVERRIDE` for `overrideAccess`; `TICKET_LOOKUP` for …

#### Requirements it meets

60 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.63 | Entitlement audit reporting | Ticketing Catalogue | CONTRACTED | `listScans` |
| 3.1.6 | The system shall maintain complete scan history including gate, location, timestamp, device ID, operator, validation result, and entry attempts. | Admission and Access | CONTRACTED | `listScans` |
| 3.2.21 | The system should keep track of the count of people passing through an access control device. Multiple Access Control System can be grouped together to give the capacity count of a specific … | Admission and Access | CONTRACTED | `listScans` |
| 3.2.54 | If access control reading is valid, the attendance counter is increased by the number or Guests associated to the ticket. | Admission and Access | CONTRACTED | `listScans` |
| 3.2.55 | All Guests are invited use the turnstiles when leaving the park. It is expected that the system counts the number of exits. Scan can be required at exit. | Admission and Access | CONTRACTED | `listScans` |
| 3.2.58 | In park attendance figure per ticket time is calculated in real time. | Admission and Access | CONTRACTED | `listScans` |
| 5.3.28 | Maintain detailed access validation history including gate entries, exits, attraction validations, RFID scans, QR scans, and turnstile events. | F&B & Guest Management | CONTRACTED | `listScans` |
| 18.1.4 | Synchronization - System shall synchronize data when connectivity is restored. | Employee Mobile App & AI Assistant | CONTRACTED | `syncScans` |
| 2.13.38 | Offline Access Validation | Ticketing Sales | CONTRACTED | `getOfflinePackage` |
| 3.1.5 | Access control devices shall validate dynamic QR codes using secure offline cryptographic validation without requiring continuous connectivity to the central platform. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.1.10 | System shall support embedding entitlement information within secure QR, RFID, NFC, mobile wallet, and digital credential tokens. Embedded information may include ticket type, seat assignment, event … | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.2.49 | The validity check logic allows offline validity check. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| … 48 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Group tickets can carry one shared QR code or individual QR codes, with partial check-in tracking; family tickets bundle adult/child pricing. *(agreed · MoM 5 Aug 2026, 4. Ticket Catalogue & Product Types · DI-137)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-015` · status **notStarted** · provenance generated
- ADR-0068 *Guest admission policy lives in Access only, and the offline package carries it* (`docs/adr/0068-guest-admission-policy-lives-in-access-only.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (37), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-015?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Sync scans, Lookup ticket, Override access, Validate access, Validate group access.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`.
- [ ] Every gated control is gated: `ACCESS_OVERRIDE`, `ACCESS_VALIDATE`, `REPORT_VIEW_VENUE`, `TICKET_LOOKUP`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-017` Sync & reconciliation

**Learn that the server disagreed with you.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `access` module |
| Block | Block C · task APP-STAFF-EMP-017 |
| Who uses it | venue staff holding `ACCESS_OVERRIDE`, `ACCESS_VALIDATE`, `ORDER_VIEW`, `REPORT_VIEW_VENUE`, `TICKET_LOOKUP` (4 operate, 1 read); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listSyncRejections` reads the population and `getOfflinePackage` reads one of them — list, select, act |
| Offline | Not applicable; this screen ends the offline period |
| Opens with | nothing: it opens on its own |
| Route | `/operations/sync-reconciliation` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): syncOrders replays till sales; a staff phone replays scans, and till order sync is POS work (design-notes correction venue-operations EMP-017).

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Staff App sync and reconciliation: what was journalled offline (scans, and other offline work such as attendance and work orders) is posted, and the person learns which items the server rejected so a supervisor can close them. The one thing to get right: unresolved rejections stay visible with a count on the home screen until resolved.

**Fixed on main** (the package already carries these; draw what it says): Workstation id text filter and Sync orders on a staff phone screen (CHG-WIR-001).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Workstation id | picker: choose a workstation (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?workstationId=` to `listSyncRejections`. | `listSyncRejections` ?workstationId |
| Kind | radio group | optional | — | Order · Payment · Refund · Void · Scan | — | Sends `?kind=` to `listSyncRejections`. | `listSyncRejections` ?kind |
| Resolved | toggle | optional | — | — | — | Sends `?resolved=` to `listSyncRejections`. | `listSyncRejections` ?resolved |
|  | text area | optional | — | max length 256 | — | **A screen that validates a credential needs somewhere to point the camera.** `denied` and `hardwareError` look different because an operator facing a guest needs to know whether to try again or … | `ValidateRequest.mediaCode` |
| Search | text area | optional | — | max length 256 | — | Sends `?mediaCode=` to `lookupTicket` (a code typed when the camera cannot read it) (CHG-RFM-012). A search that returns nothing must say so differently from a search not yet run. | `lookupTicket` ?mediaCode |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Since version | number field | — | — | `getOfflinePackage` ?sinceVersion |
| Valid from | date and time picker | — | — | `getOfflinePackage` ?validFrom |
| Valid to | date and time picker | — | — | `getOfflinePackage` ?validTo |
| Access point | picker: choose an access point | — | — | `listScans` ?accessPointId |
| Ticket | picker: choose a ticket | — | — | `listScans` ?ticketId |
| Outcome | segmented control | — | Admitted · Denied · Overridden | `listScans` ?outcome |
| Recorded from | date and time picker | — | — | `listScans` ?recordedFrom |
| Recorded to | date and time picker | — | — | `listScans` ?recordedTo |

**Form: Sync scans** (modal, opened by *Sync scans*; *Sync scans* calls `syncScans`, *Cancel* sends nothing)

**Collects what `syncScans` sends before it is called.** Required: `deviceId`, `scans`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Device `deviceId` | picker: choose a device | required | — | — | shows names, sends the id | Sequence numbers are monotonic per device, not globally. | `syncScans` body |
| Scans `scans` | repeatable rows | required | — | at least 1; at most 500 | — | — | `syncScans` body |
| ID `scans[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7. Also the idempotency key and dedupe key. | `syncScans` body |
| Media code `scans[].mediaCode` | text area | required | — | max length 256 | — | What was read from the media. NOT the ticket id — media can be re-linked over a ticket's life. | `syncScans` body |
| Media kind `scans[].mediaKind` | select | required | — | Image · Video · Audio · Document · Vector · Font · Archive · Model3d; glb`) venue model, at most 40 MB. | — | `model3d` added 3 October 2026 (r1 additions; ADR-0069 action item 4): a glTF binary (`model/gltf-binary`, `.glb`) venue model, at most 40 MB. | `syncScans` body |
| Direction `scans[].direction` | radio group | required | — | Entry · Exit · Reentry · Crossover | — | — | `syncScans` body |
| Group size `scans[].groupSize` | number field | optional | — | min 1 | — | For group media admitting several holders on one read. | `syncScans` body |
| Proximity token `scans[].proximityToken` | text field | optional | — | — | — | BLE proximity assertion where the venue requires the operator to be physically at the gate. | `syncScans` body |
| Recorded at `scans[].recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the read. Authoritative for ordering, not for validity. | `syncScans` body |
| Sequence `scans[].sequence` | number field | required | — | min 1 | — | Monotonic per device. The server processes in this order. | `syncScans` body |
| Local outcome `scans[].localOutcome` | segmented control | required | — | Admitted · Denied · Overridden | — | What the device decided offline. The server is authoritative and may disagree; disagreements are returned for reconciliation, not discarded. | `syncScans` body |
| Local deny reason `scans[].localDenyReason` | select | optional | — | Not found · Not yet valid · Expired · Already used · Reentry limit reached · Exit required before reentry · Wrong access point · Wrong performance · Outside admission window · Entitlement suspended · Blacklisted · Capacity reached … | — | Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a boolean. | `syncScans` body |
| Overridden by principal `scans[].overriddenByPrincipalId` | picker: choose an overridden by principal | optional | — | — | shows names, sends the id | — | `syncScans` body |
| Override reason `scans[].overrideReason` | text field | optional | — | — | — | — | `syncScans` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Form: Validate access** (modal, opened by *Validate access*; *Validate access* calls `validateAccess`, *Cancel* sends nothing)

**Collects what `validateAccess` sends before it is called.** Required: `id`, `mediaCode`, `mediaKind`, `direction`, `recordedAt`. Optional: `groupSize`, `proximityToken`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7. Also the idempotency key and dedupe key. | `validateAccess` body |
| Media code `mediaCode` | text area | required | — | max length 256 | — | What was read from the media. NOT the ticket id — media can be re-linked over a ticket's life. | `validateAccess` body |
| Media kind `mediaKind` | select | required | — | Image · Video · Audio · Document · Vector · Font · Archive · Model3d; glb`) venue model, at most 40 MB. | — | `model3d` added 3 October 2026 (r1 additions; ADR-0069 action item 4): a glTF binary (`model/gltf-binary`, `.glb`) venue model, at most 40 MB. | `validateAccess` body |
| Direction `direction` | radio group | required | — | Entry · Exit · Reentry · Crossover | — | — | `validateAccess` body |
| Group size `groupSize` | number field | optional | — | min 1 | — | For group media admitting several holders on one read. | `validateAccess` body |
| Proximity token `proximityToken` | text field | optional | — | — | — | BLE proximity assertion where the venue requires the operator to be physically at the gate. | `validateAccess` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the read. Authoritative for ordering, not for validity. | `validateAccess` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 Media not recognised in this cell

**Form: Validate group access** (modal, opened by *Validate group access*; *Validate group access* calls `validateGroupAccess`, *Cancel* sends nothing)

**Collects what `validateGroupAccess` sends before it is called.** Required: `id`, `mediaCode`, `admitCount`, `recordedAt`. Optional: `direction`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `validateGroupAccess` body |
| Media code `mediaCode` | text area | required | — | max length 256 | — | — | `validateGroupAccess` body |
| Admit count `admitCount` | number field | required | — | min 1 | — | — | `validateGroupAccess` body |
| Direction `direction` | radio group | optional | — | Entry · Exit · Reentry · Crossover | — | — | `validateGroupAccess` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `validateGroupAccess` body |

Errors to draw in the form: 403 Authenticated but not permitted at the requested scope; 409 Requested count exceeds the remaining group allowance

**Sent by *Override access*** (`overrideAccess`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `overrideAccess` body |
| Scan `scanId` | picker: choose a scan | required | — | — | shows names, sends the id | The denied scan being overridden. | `overrideAccess` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `overrideAccess` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `overrideAccess` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every sync rejection** (data table, from `listSyncRejections`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Order, Payment, Refund, Void, Scan | — |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Rejected at | 1 Oct 2026, 14:30 | — |
| Resolved at | 1 Oct 2026, 14:30 | — |

**Every scan event** (data table, from `listScans`)

| Shows | Format | Notes |
|---|---|---|
| Media code | text | — |
| Outcome | chip: Admitted, Denied, Overridden | — |

**The selected sync rejection** (detail panel, from `listSyncRejections`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Order, Payment, Refund, Void, Scan | — |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Rejected at | 1 Oct 2026, 14:30 | — |
| Problem | grouped details | RFC 9457 problem details. Every error response uses this shape. |
| Resolved at | 1 Oct 2026, 14:30 | — |

**The offline package** (detail panel, from `getOfflinePackage`)

| Shows | Format | Notes |
|---|---|---|
| Generated at | 1 Oct 2026, 14:30 | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |
| Entitlements | list or chips (count when long) | Read from `access.entitlement` (SD-052). With `sinceVersion`, only the rows changed after it, including ones now void or used, so a device … |
| Delegated rights | list or chips (count when long) | Redemption rights issued by other cells and valid at this access point. Included in the package so a cross-region entitlement still admits … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Sync scans (primary button) | `syncScans` POST `/access/scans` | inline | ScanSyncResult | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | opens modal first |
| Lookup ticket (secondary button) | `lookupTicket` GET `/access/lookup` | — | TicketStatus | 400 Neither mediaCode nor ticketId supplied; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | works offline; produces a document or message: Read-only validity check without admitting |
| Override access (destructive button) | `overrideAccess` POST `/access/override` | inline | ValidationResult | 403 Authenticated but not permitted at the requested scope; 409 The scan was not a denial, or has already been overridden | works offline |
| Validate access (secondary button) | `validateAccess` POST `/access/validate` | ValidateRequest | ValidationResult | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 Media not recognised in this cell | works offline; opens modal first |
| Validate group access (secondary button) | `validateGroupAccess` POST `/access/group-validate` | inline | ValidationResult | 403 Authenticated but not permitted at the requested scope; 409 Requested count exceeds the remaining group allowance | works offline; opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Rejections**: Kind (scan, order, other), recorded and rejected times, problem in words, resolved or not. *(source: contracts/spine/orders.yaml#listSyncRejections / F08 step 4)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Sync now**: Posts queued work in sequence; required before closing the shift. *(source: F72 step 2 / contracts/spine/access.yaml#syncScans)*

**Data it reads**: `listSyncRejections` (onLoad, Entries the server refused); `getOfflinePackage` (onLoad, Entitlement and rule set for offline validation); `listScans` (onLoad, List scan events)

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*
- → `EMP-018` Offline package: *Offline package*
- → `EMP-009` End shift: *The cashier submits a blind count;*

**What opens over it**

- confirmDialog *Override access*: **Names what `overrideAccess` changes and what it leaves alone**, in the consequence rather than the verb. A sync reconciliation this affects should be identified in the dialog, not just counted. **Collects what `overrideAccess` sends before it is called.** Required: `id`, `scanId`, `reason` …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The sync reconciliation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the sync reconciliation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No sync reconciliation yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on workstationId, kind, resolved and the sync reconciliation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `listSyncRejections` requires to show this screen, and names that permission (the screen's other reads need `ACCESS_VALIDATE`, `REPORT_VIEW_VENUE` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ACCESS_OVERRIDE` for `overrideAccess` … |
| Offline (`?state=offline`) | Not applicable; this screen ends the offline period |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Neither mediaCode nor ticketId supplied; 400 Validation failed; 409 Requested count exceeds the remaining group allowance; 409 The scan was not a denial, or has already been overridden |

#### Consistency with other screens

- Match `SCN-014`: Same rows and wording.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rejections:
- kind: Scan
  ticket: VT0933
  problem: Already used at 09:58 Gate 1
  state: Unresolved
```

#### Permissions

- `syncScans` → `ACCESS_VALIDATE` (operate) · staff
- `listSyncRejections` → `ORDER_VIEW` (read) · staff
- `getOfflinePackage` → `ACCESS_VALIDATE` (operate) · staff
- `listScans` → `REPORT_VIEW_VENUE` (operate) · staff
- `lookupTicket` → `TICKET_LOOKUP` (operate) · staff
- `overrideAccess` → `ACCESS_OVERRIDE` (operate) · staff
- `validateAccess` → `ACCESS_VALIDATE` (operate) · staff
- `validateGroupAccess` → `ACCESS_VALIDATE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `listSyncRejections` requires to show this screen, and names that permission (the screen's other reads need `ACCESS_VALIDATE`, `REPORT_VIEW_VENUE` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ACCESS_OVERRIDE` for `overrideAccess` …

#### Requirements it meets

60 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 18.1.4 | Synchronization - System shall synchronize data when connectivity is restored. | Employee Mobile App & AI Assistant | CONTRACTED | `syncScans` |
| 2.13.38 | Offline Access Validation | Ticketing Sales | CONTRACTED | `getOfflinePackage` |
| 3.1.5 | Access control devices shall validate dynamic QR codes using secure offline cryptographic validation without requiring continuous connectivity to the central platform. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.1.10 | System shall support embedding entitlement information within secure QR, RFID, NFC, mobile wallet, and digital credential tokens. Embedded information may include ticket type, seat assignment, event … | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.2.49 | The validity check logic allows offline validity check. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.2.75 | The access control can be operated in offline mode. Turnstiles can perform access control in absence of database access (database unavailable or not reachable). Key access control criteria can be … | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.3.30 | Distributed Policy Evaluation - System shall support local policy evaluation when offline. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 18.1.3 | Offline Mode - System shall support offline operation. | Employee Mobile App & AI Assistant | CONTRACTED | `getOfflinePackage` |
| 1.1.63 | Entitlement audit reporting | Ticketing Catalogue | CONTRACTED | `listScans` |
| 3.1.6 | The system shall maintain complete scan history including gate, location, timestamp, device ID, operator, validation result, and entry attempts. | Admission and Access | CONTRACTED | `listScans` |
| 3.2.21 | The system should keep track of the count of people passing through an access control device. Multiple Access Control System can be grouped together to give the capacity count of a specific … | Admission and Access | CONTRACTED | `listScans` |
| 3.2.54 | If access control reading is valid, the attendance counter is increased by the number or Guests associated to the ticket. | Admission and Access | CONTRACTED | `listScans` |
| … 48 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Scanning must be native/installable and work fully offline, storing scans locally and syncing when connectivity returns. *(agreed · MoM 10 Aug 2026, 5.7 Ticket Scanning / Access Control App · DI-240)*
- After reconnection, offline records sync in batches in the order events occurred, tagged with both the original recorded time and the sync time; syncing must not slow gate entry. *(agreed · MoM 31 Jul 2026, 7. Ticket Validation & Offline Architecture · DI-065)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-017` · status **notStarted** · provenance generated
- Flow F72 *A shift ends and the summary is read*, step 2: Anything unsynced is pushed first. → **Sync before close, always.** F33 exits at `openWithUnsynced` for exactly this.
- Flow F72 branch at step 2 (high): when Transactions are still rejected after sync., **The shift stays open.** F33 step 8 resolves them, and a shift closed over rejections has settled against a number that will change.
- ADR-0068 *Guest admission policy lives in Access only, and the offline package carries it* (`docs/adr/0068-guest-admission-policy-lives-in-access-only.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (35), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-017?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Sync scans, Lookup ticket, Override access, Validate access, Validate group access.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`, `EMP-018`, `EMP-009`.
- [ ] Every gated control is gated: `ACCESS_OVERRIDE`, `ACCESS_VALIDATE`, `ORDER_VIEW`, `REPORT_VIEW_VENUE`, `TICKET_LOOKUP`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-018` Offline package

**Know which rules this device is enforcing.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `ticketing` module |
| Block | Block B · task APP-STAFF-EMP-018 |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as technician |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listCatalogueBundles` reads the population and `getLatestBundle` reads one of them — list, select, act |
| Offline | Cannot refresh. The existing bundle continues and its age is shown |
| Opens with | `version` (deepLink) · cold entry: **A version link is expected to point at something superseded — that is what versions are for.** The screen opens the requested version read-only, says it is … |
| Route | `/operations/offline-package` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Removed 24 August**: publishBundle. **Bulk-attach residue, found by walking a journey.** A device-settings screen does not read guest loyalty, a venue map does not set a refund policy, a shift summary does not close the shift, and **a rota a steward can rewrite is not a rota.**

**From the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process.** Which offline package (catalogue bundle and rules) this device enforces, and how old it is. After Block A.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Since | text field | — | — | `getLatestBundle` ?since |

**Form: Report bundle applied** (modal, opened by *Report bundle applied*; *Report bundle applied* calls `reportBundleApplied`, *Cancel* sends nothing)

**Collects what `reportBundleApplied` sends before it is called.** Required: `appliedAt`, `outcome`. Optional: `error`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Applied at `appliedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `reportBundleApplied` body |
| Outcome `outcome` | segmented control | required | — | Applied · Rolled back · Signature invalid | — | — | `reportBundleApplied` body |
| Error `error` | text field | optional | — | — | — | — | `reportBundleApplied` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every bundle** (data table, from `listCatalogueBundles`)

| Shows | Format | Notes |
|---|---|---|
| Published at | 1 Oct 2026, 14:30 | — |
| Published by | the name it points at, never the id | — |
| Stale after | 1 Oct 2026, 14:30 | — |
| Size bytes | 1,234 | — |

**The selected bundle** (detail panel, from `listCatalogueBundles`)

| Shows | Format | Notes |
|---|---|---|
| Published at | 1 Oct 2026, 14:30 | — |
| Published by | the name it points at, never the id | — |
| Stale after | 1 Oct 2026, 14:30 | — |
| Size bytes | 1,234 | — |
| Note | text | — |

**The catalogue bundle** (detail panel, from `getLatestBundle`)

| Shows | Format | Notes |
|---|---|---|
| Is delta | yes / no (icon or chip) | — |
| Base version | text | Present when `isDelta`. The version this delta applies to. |
| Signature | text | Detached signature over `contentHash`. The terminal verifies before applying and rolls back on failure — a half-applied catalogue is never … |
| Stale after | 1 Oct 2026, 14:30 | — |
| Payload | grouped details | Products, variants, price lists, prices, tax codes, events, performances, envelope definitions, data mask field definitions and the venue's … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Report bundle applied (primary button) | `reportBundleApplied` POST `/catalogue/bundles/{version}/applied` | inline | — | — | opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **package**: Version, built at, applied at, age ("3 h old"), and what it covers. *(source: contracts/spine/catalogue.yaml#getLatestBundle)*

**Data it reads**: `listCatalogueBundles` (onLoad, List published bundles); `getLatestBundle` (onLoad, Pull the current bundle for this workstation's venue)

**Where the user goes next**

- → `EMP-049` Hand over the journal: *At the end of the session the journal is handed over*
- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The offline package list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the offline package untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No offline package yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listCatalogueBundles` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listCatalogueBundles` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Cannot refresh. The existing bundle continues and its age is shown |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
bundle: v214 · built 06:00 · applied 06:04 · 3 h old
```

#### Permissions

- `listCatalogueBundles` → `PRODUCT_VIEW` (read) · staff, guest
- `getLatestBundle` → `PRODUCT_VIEW` (read) · staff
- `reportBundleApplied` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listCatalogueBundles` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Scanning must be native/installable and work fully offline, storing scans locally and syncing when connectivity returns. *(agreed · MoM 10 Aug 2026, 5.7 Ticket Scanning / Access Control App · DI-240)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-018` · status **notStarted** · provenance generated
- Flow F71 *A device is prepared, used and handed over*, step 2: It pulls its offline package. → **`reportBundleApplied` closes the loop.** A device that pulled a bundle and never confirmed it is a device the fleet view believes is current.
- Flow F71 branch at step 2 (high): when The bundle is stale and the network is gone., **The device is not issued.** ADR-0013 makes the till and the scanner local-first, and local-first with a stale catalogue is worse than no device.
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-018?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Report bundle applied.
- [ ] Every transition is wired: `EMP-049`, `EMP-001`, `EMP-002`, `EMP-003`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-019` AI assistant — home

**Ask and be answered within your role, with the source.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `ai` module |
| Block | Block D · task APP-STAFF-EMP-019 |
| Who uses it | venue staff holding `AI_USE` (1 operate); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listAiConversations` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **Not available.** Retrieval needs the index |
| Opens with | `conversationId` (deepLink) · cold entry: A conversation link an agent opens from a notification. Resolves, or says it was closed and by whom. |
| Route | `/operations/ai-assistant-home` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. Pulled to Wave 1 (CF-101). CF-57: the client named AI configuration assistance as a Wave 1 priority, and F20 is Wave 1.

**From the AI & Intelligence process.** The AI tab of the Staff App (a primary tab, CF-41): a staff member asks in their own words - "what was yesterday's ticketing revenue?", "what is today's promo code?", "how do I process a refund?" - and gets an answer within their role, with its source. The home lists their recent conversations and suggested questions for their role. The one thing to get right: the assistant answers as that person - a cashier cannot get the CEO's revenue by asking nicely - and says so plainly when something is outside their access.

**Known correction pending (do not draw the wrong version)**

- **Layout is a dataTable "Every AI conversation" with id, principalId, scopePath, module columns and a Create AI conversation modal asking for module.** Why: A staff phone tab needs an ask box and the person's recent conversations; module comes from the session. *(source: screens/P06-staff-app.yaml#EMP-019 / contracts/satellite/ai.yaml#createAiConversation; AI & Intelligence)*

**Fixed on main** (the package already carries these; draw what it says): purpose "The tab that is already in the shell." (CHG-WIR-013).

#### Inputs: what the user enters or picks

**Form: Create AI conversation** (modal, opened by *Create AI conversation*; *Create AI conversation* calls `createAiConversation`, *Cancel* sends nothing)

**Collects what `createAiConversation` sends before it is called.** Required: `module`. Optional: `locale`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Module `module` | field | required | — | — | — | Which part of the platform the conversation is about (8.4.1). | `createAiConversation` body |
| Locale `locale` | text field | optional | — | — | — | 8.4.3. Multilingual, and Arabic is not an afterthought here. | `createAiConversation` body |

**Form: Send AI message** (modal, opened by *Send AI message*; *Send AI message* calls `sendAiMessage`, *Cancel* sends nothing)

**Collects what `sendAiMessage` sends before it is called.** Required: `content`. Optional: `collectionIds`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Content `content` | text area | required | — | min length 1; max length 8000 | — | — | `sendAiMessage` body |
| Collections `collectionIds` | multi-picker: choose collections | optional | — | — | — | Restrict retrieval to named collections. Absent means every collection the principal may read. | `sendAiMessage` body |

Errors to draw in the form: 422 The guard (the provider''s content-safety service, CHG-R1S-002) blocked the message or the reply (`guard-refused`, CHG-CSA-003).

**Rules for these inputs** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **question**: Text and starter chips per role (cashier, supervisor, manager). module and locale are not asked; they come from the session and app. *(source: contracts/satellite/ai.yaml#createAiConversation / DI-964)*

#### Outputs: what the screen shows and produces

**Shown**

**Every AI conversation** (data table, from `listAiConversations`)

| Shows | Format | Notes |
|---|---|---|
| Locale | text | — |
| Message count | 1,234 | — |
| Started at | 1 Oct 2026, 14:30 | — |
| Last message at | 1 Oct 2026, 14:30 | — |

**The selected AI conversation** (detail panel, from `listAiConversations`)

| Shows | Format | Notes |
|---|---|---|
| Module | text | — |
| Locale | text | — |
| Message count | 1,234 | — |
| Started at | 1 Oct 2026, 14:30 | — |
| Last message at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create AI conversation (primary button) | `createAiConversation` POST `/conversations` | inline | AiConversation | — | opens modal first |
| Send AI message (secondary button) | `sendAiMessage` POST `/conversations/{conversationId}/messages` | inline | AiMessage | 422 The guard (the provider''s content-safety service, CHG-R1S-002) blocked the message or the reply (`guard-refused`, CHG-CSA-003). | opens modal first |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **recent conversations**: The person's own, newest first, first question as title; not a table with principal and scope columns. *(source: contracts/satellite/ai.yaml#listAiConversations)*

**What each action does** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Ask**: Opens EMP-020 with the answer streaming. *(source: F101 step 1)*

**Data it reads**: `listAiConversations` (onLoad, A principal's conversation history)

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*
- → `EMP-020` AI assistant — answer: *AI assistant — answer*; carries `conversationId`, `messageId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The assistant home list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the assistant home untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No assistant home yet. Offers Create AI conversation (`createAiConversation`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listAiConversations` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `AI_USE`, which `listAiConversations` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Not available.** Retrieval needs the index |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 The guard (the provider''s content-safety service, CHG-R1S-002) blocked the message or the reply (`guard-refused`, CHG-CSA-003). |

#### Edge cases to draw

- **Offline**: The tab says the assistant needs the connection; recent conversations stay readable. *(source: screens/P06-staff-app.yaml#EMP-019 (states.offline))*
- **Assistant paused or the staff profile inactive**: The tab shows the knowledge base search (EMP-040) instead, with a note. *(source: contracts/satellite/ai.yaml#pauseAiCapability (degradationMode searchOnly))*

#### Consistency with other screens

- Match `EMP-020`: Question and answer are one screen pair.
- Match `POS-008`: The till's embedded assistant uses the same staff assistant and answer component.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
role: Supervisor, Coastal Aqua
chips:
- What was yesterday's ticketing revenue?
- Today's promo codes
- How do I refund a cabana?
- Who is on shift at Gate 2?
```

#### Permissions

- `listAiConversations` → `AI_USE` (operate) · staff, guest
- `createAiConversation` → `AI_USE` (operate) · staff, guest
- `sendAiMessage` → `AI_USE` (operate) · staff, guest

**A refused user sees:** Shown when the caller lacks `AI_USE`, which `listAiConversations` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

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

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The AI assistant answers natural-language business queries (e.g. "what was yesterday's ticketing revenue?") only within the user's role (a CEO sees full revenue, a cashier does not), shows grounded citations naming the policy or document an answer came from, and keeps conversation context ("compare that to this week"). *(client request · MoM 21 Sep 2026, 4.8 Core AI Platform — AI Assistant (Query & Knowledge) · DI-964)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-019` · status **notStarted** · provenance generated
- Flow F101 *A staff member asks the assistant and it answers from the venue*, step 1: AI assistant — home. → 2 operations, 2 of them previously unwalked.
- Flow F101 branch at step 1 (medium): when The acting principal lacks the permission at this scope., **Refused at the first step, not the last.** ADR-0002 makes authorisation user-driven — a person who gets three steps in and then cannot finish has been told the wrong thing.
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (422).
- [ ] Every output is drawn (9 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-019?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create AI conversation, Send AI message.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`, `EMP-020`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-020` AI assistant — answer

**Answer with the operation behind it visible.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `ai` module |
| Block | Block D · task APP-STAFF-EMP-020 |
| Who uses it | venue staff holding `AI_USE`, `REPORT_VIEW_VENUE` (2 operate); in the flows as supervisor, venue manager |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listAiConversations` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | Not available |
| Opens with | `conversationId` (deepLink), `messageId` (navigation) · cold entry: A conversation link an agent opens from a notification. Resolves, or says it was closed and by whom. |
| Route | `/operations/ai-assistant-answer` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. Pulled to Wave 1 (CF-101) with EMP-019 — **the question and the answer are one screen pair** and splitting them across waves ships half a feature. **Cross-platform navigation removed 24 August**: BO-058. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link.

**From the AI & Intelligence process.** The answer: what the assistant said, what it is based on (the policy, document or report it came from) and, for numbers, the query that produced them. Follow-ups keep context ("compare that to this week"). The one thing to get right: a figure is only ever shown from a query result with its "Data as of" time; a policy answer cites the policy; nothing is invented.

**Known correction pending (do not draw the wrong version)**

- **Layout repeats EMP-019's conversation table.** Why: This is the answer view - message thread, citations, query link, feedback. *(source: screens/P06-staff-app.yaml#EMP-020 (purpose "Answer with the operation behind it visible"); AI & Intelligence)*

**Fixed on main** (the package already carries these; draw what it says): Staff numeric questions go through sendAiMessage only; askReportingQuestion is not declared. (CHG-WIR-012).

#### Inputs: what the user enters or picks

**Form: Send AI message** (modal, opened by *Send AI message*; *Send AI message* calls `sendAiMessage`, *Cancel* sends nothing)

**Collects what `sendAiMessage` sends before it is called.** Required: `content`. Optional: `collectionIds`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Content `content` | text area | required | — | min length 1; max length 8000 | — | — | `sendAiMessage` body |
| Collections `collectionIds` | multi-picker: choose collections | optional | — | — | — | Restrict retrieval to named collections. Absent means every collection the principal may read. | `sendAiMessage` body |

Errors to draw in the form: 422 The guard (the provider''s content-safety service, CHG-R1S-002) blocked the message or the reply (`guard-refused`, CHG-CSA-003).

**Form: Create AI conversation** (modal, opened by *Create AI conversation*; *Create AI conversation* calls `createAiConversation`, *Cancel* sends nothing)

**Collects what `createAiConversation` sends before it is called.** Required: `module`. Optional: `locale`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Module `module` | field | required | — | — | — | Which part of the platform the conversation is about (8.4.1). | `createAiConversation` body |
| Locale `locale` | text field | optional | — | — | — | 8.4.3. Multilingual, and Arabic is not an afterthought here. | `createAiConversation` body |

**Form: Ask a number** (modal, opened by *Ask a number*; *Ask a number* calls `askReportingQuestion`, *Cancel* sends nothing)

**Collects what `askReportingQuestion` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Question `question` | text area | required | — | min length 3; max length 1000 | — | — | `askReportingQuestion` body |
| Conversation `conversationId` | text field | optional | — | — | — | Continue a prior exchange for follow-up questions. | `askReportingQuestion` body |
| Venue `venueId` | picker: choose a venue | optional | — | Omitting it answers over everything the caller's scope permits — it cannot be used to reach beyond that. | shows names, sends the id | Narrows the answer to one venue. Omitting it answers over everything the caller's scope permits — it cannot be used to reach beyond that. | `askReportingQuestion` body |

Errors to draw in the form: 400 Question could not be interpreted. (ReportQuestionProblem); 403 Authenticated but not permitted at the requested scope

#### Outputs: what the screen shows and produces

**Shown**

**Every AI conversation** (data table, from `listAiConversations`)

| Shows | Format | Notes |
|---|---|---|
| Locale | text | — |
| Message count | 1,234 | — |
| Started at | 1 Oct 2026, 14:30 | — |
| Last message at | 1 Oct 2026, 14:30 | — |

**The selected AI conversation** (detail panel, from `listAiConversations`)

| Shows | Format | Notes |
|---|---|---|
| Module | text | — |
| Locale | text | — |
| Message count | 1,234 | — |
| Started at | 1 Oct 2026, 14:30 | — |
| Last message at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Send AI message (primary button) | `sendAiMessage` POST `/conversations/{conversationId}/messages` | inline | AiMessage | 422 The guard (the provider''s content-safety service, CHG-R1S-002) blocked the message or the reply (`guard-refused`, CHG-CSA-003). | opens modal first |
| Create AI conversation (secondary button) | `createAiConversation` POST `/conversations` | inline | AiConversation | — | opens modal first |
| Ask a number (secondary button) | `askReportingQuestion` POST `/reports/ask` | inline | NaturalLanguageAnswer | 400 Question could not be interpreted. (ReportQuestionProblem); 403 Authenticated but not permitted at the requested scope | opens modal first |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **answer and sources**: Answer text, then citations (document title and section); confidence shown only when the provider reports one, as a band, never a number with decimals. *(source: contracts/satellite/ai.yaml#/components/schemas/AiMessage / DI-964)*
- **numbers**: A numeric answer shows "Data as of <time>" and a "Show query" link (metric, filters, period). Outside the semantic model the answer is "Not available yet" and the gap is recorded. *(source: ADR-0054 / contracts/satellite/reporting.yaml#askReportingQuestion)*
- **proposed action**: When the answer suggests a change (e.g. a refund), it shows as a draft card with "Open in <screen>"; it is never applied from here. *(source: contracts/satellite/ai.yaml#/components/schemas/AiMessage (proposedAction))*

**What each action does** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Helpful / Not helpful**: Once per answer, optional reason; feeds the golden set and knowledge gaps. *(source: contracts/satellite/ai.yaml#recordAnswerFeedback)*
- **Follow-up**: Same conversation; the answer uses the earlier context. *(source: DI-964 / MoM 21 Sep 4.8)*

**Data it reads**: `listAiConversations` (onLoad, A principal's conversation history)

**Where the user goes next**

- → `EMP-040` Knowledge base: *Knowledge base*
- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*
- → `BO-058` Reporting Home: *Saves it as a report*; carries `conversationId`; calls `sendAiMessage`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The assistant answer list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the assistant answer untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No assistant answer yet. Offers Create AI conversation (`createAiConversation`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listAiConversations` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `AI_USE`, which `listAiConversations` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `REPORT_VIEW_VENUE` for `askReportingQuestion`. |
| Offline (`?state=offline`) | Not available |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Question could not be interpreted. (ReportQuestionProblem); 422 The guard (the provider''s content-safety service, CHG-R1S-002) blocked the message or the reply (`guard-refused`, CHG-CSA-003). |

#### Edge cases to draw

- **The question needs data the person may not see**: "You don't have access to finance figures" - not an empty or zero answer. *(source: contracts/satellite/ai.yaml#sendAiMessage ("retrieval runs as the calling principal") / MoM 21 Sep 4.8)*
- **Usage limit reached (429)**: Says which limit and that the manager has been told. *(source: contracts/satellite/ai.yaml#sendAiMessage (429))*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
question: What was yesterday's ticketing revenue?
answer: AED 84,320.00 from 1,912 tickets on Wed 30 Sep (online AED 51,200.00, POS AED 33,120.00).
dataAsOf: Thu 1 Oct 06:00
followUp: Compare that to the same day last week
```

#### Permissions

- `sendAiMessage` → `AI_USE` (operate) · staff, guest
- `createAiConversation` → `AI_USE` (operate) · staff, guest
- `listAiConversations` → `AI_USE` (operate) · staff, guest
- `recordAnswerFeedback` → `AI_USE` (operate) · staff, guest
- `askReportingQuestion` → `REPORT_VIEW_VENUE` (operate) · staff, partner

**A refused user sees:** Shown when the caller lacks `AI_USE`, which `listAiConversations` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `REPORT_VIEW_VENUE` for `askReportingQuestion`.

#### Requirements it meets

17 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| 8.4.1 | System shall provide a conversational AI assistant across all platform modules. | Unified Operations Dashboard | CONTRACTED | `createAiConversation` |
| … 5 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The AI assistant answers natural-language business queries (e.g. "what was yesterday's ticketing revenue?") only within the user's role (a CEO sees full revenue, a cashier does not), shows grounded citations naming the policy or document an answer came from, and keeps conversation context ("compare that to this week"). *(client request · MoM 21 Sep 2026, 4.8 Core AI Platform — AI Assistant (Query & Knowledge) · DI-964)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-020` · status **notStarted** · provenance generated
- Flow F101 *A staff member asks the assistant and it answers from the venue*, step 2: AI assistant — answer. → 2 operations, 2 of them previously unwalked.
- Flow F20 *A manager asks a question and gets an answer*, step 2: The answer arrives with its sources → **An answer with no sources is a guess**, and the interface shows it as one
- Flow F20 branch at step 2 (recoverable): when Nothing relevant was retrieved, **Says so rather than answering from general knowledge.** A confident answer about a venue the model has never seen is the failure that stops people trusting it.
- Flow F20 branch at step 2 (requiresStaff): when The answer proposes a change, A `proposedAction`, not an applied one. Pricing and financial proposals need approval before execution.
- Flow F20 branch at step 2 (recoverable): when Every provider is unavailable, Reported rather than retried indefinitely. **An assistant that hangs is worse than one that says no.**
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)
- ADR-0054 *Natural-language analytics goes through the semantic layer* (`docs/adr/0054-natural-language-analytics-goes-through-the-semantic-layer.md`)
- ADR-0059 *AI phasing against the six-month plan* (`docs/adr/0059-ai-phasing-against-the-six-month-plan.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (400, 403, 404, 422).
- [ ] Every output is drawn (9 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-020?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Send AI message, Create AI conversation, Ask a number.
- [ ] Every transition is wired: `EMP-040`, `EMP-001`, `EMP-002`, `EMP-003`, `BO-058`.
- [ ] Every gated control is gated: `AI_USE`, `REPORT_VIEW_VENUE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-021` Roster

**See who is on, and where.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `core` module |
| Block | Block D · task APP-STAFF-EMP-021 |
| Who uses it | venue staff holding `WORKFORCE_VIEW` (1 read); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listRotaAssignments` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | Cached roster with its age |
| Opens with | `assignmentId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/operations/roster` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Removed 24 August**: createRotaAssignment, updateRotaAssignment. **Bulk-attach residue.** A device-settings screen does not merge guest profiles, a rota view does not author the rota, a shift summary does not open a shift, and **authority notification belongs where the incident is raised, not where it is read.**

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The team roster on the Staff App: a supervisor on the floor sees who is on, where and when - today by hour, the week, the month - and who is late or missing. It reads the rota the back office published; it never writes it. The one thing to get right: it is a calendar with Day, Week and Month (Day by default, split into hours from the venue's day start), people as rows, with the gaps visible, not a table of assignment ids.

**Known correction pending (do not draw the wrong version)**

- **No calendar component; From and To date pickers over a table** Why: Every rota is a calendar with Day, Week and Month (VO-R01); the client's mobile render shows Day/Week/Month tabs. *(source: screens/P06-staff-app.yaml#EMP-021 / DI-919; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Filters "Principal id" and "Department id" are free-text id fields; the table shows id, principalId, venueId, departmentId, requiredRoleId, workstationId** Why: Pickers and names (VO-R12); ids are plumbing. *(source: screens/P08-venue-back-office.yaml#BO-156 / DI-039; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **labourCost and overtimeMinutes of colleagues are columns on a handheld** Why: Pay-derived figures are sensitive staff data and belong on the back office (BO-891), not on a shared phone. *(source: screens/P08-venue-back-office.yaml#BO-882 / contracts/satellite/workforce.yaml#/components/schemas/RotaAssignment; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Request shift swap is the primary action on the team roster** Why: A person can only ask to swap their own assignment; on someone else's row the action makes no sense. Keep it on EMP-022 and EMP-023. *(source: contracts/satellite/workforce.yaml#requestShiftSwap / F68 step 3; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should the phone roster show live attendance (checked in, not in yet), which needs listAttendance and a connection?** → Drawn default accepted: Draw the overlay as above, greyed offline. *(decided by Chinmay, 2026-10-02; DEC-523 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| From | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?from=` to `listRotaAssignments`. | `listRotaAssignments` ?from |
| To | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?to=` to `listRotaAssignments`. | `listRotaAssignments` ?to |
| Principal id | picker: choose a principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?principalId=` to `listRotaAssignments`. | `listRotaAssignments` ?principalId |
| Department id | picker: choose a department (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?departmentId=` to `listRotaAssignments`. | `listRotaAssignments` ?departmentId |

**Form: Request shift swap** (modal, opened by *Request shift swap*; *Request shift swap* calls `requestShiftSwap`, *Cancel* sends nothing)

**Collects what `requestShiftSwap` sends before it is called.** Required: `toPrincipalId`. Optional: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| To principal `toPrincipalId` | picker: choose a to principal | required | — | — | shows names, sends the id | — | `requestShiftSwap` body |
| Reason `reason` | text area | optional | — | max length 300 | — | — | `requestShiftSwap` body |

Errors to draw in the form: 409 The swap is not like for like (audit R129 (6)): the other person does not hold the assignment's role (`swap-role-mismatch`), or is not staff at the …

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **View**: Segmented Day / Week / Month (plus Agenda), per VO-R01. Day opens on today, hours from calendarDayStartHour (e.g. 06:00) to close; Week starts on the venue's first day; swipe changes period; "Today" returns. *(source: screens/P06-staff-app.yaml#EMP-021 / DI-919)*
- **Team filter**: Department and position chips (Gate stewards, Cashiers, Lifeguards, Ride operators) and a person search by name; no id text fields. Defaults to the supervisor's own department. *(source: contracts/satellite/workforce.yaml#listRotaAssignments)*

#### Outputs: what the screen shows and produces

**Shown**

**Every rota assignment** (data table, from `listRotaAssignments`)

| Shows | Format | Notes |
|---|---|---|
| Overtime minutes | 1,234 | BL-044, 1.2.83. UAE labour law limits working hours and mandates rest periods, and nothing in the package counted either. |
| Rest period before | 1,234 | Minutes since the previous shift ended. The check that stops a closing shift followed by an opening one, which is legal in most places and … |
| Labour cost | AED 1,234.50 | Cost at the point of scheduling. A manager building a rota without seeing its cost is a manager who finds out from finance. |
| Display name | text | — |

**The selected rota assignment** (detail panel, from `listRotaAssignments`)

| Shows | Format | Notes |
|---|---|---|
| Overtime minutes | 1,234 | BL-044, 1.2.83. UAE labour law limits working hours and mandates rest periods, and nothing in the package counted either. |
| Labour cost | AED 1,234.50 | Cost at the point of scheduling. A manager building a rota without seeing its cost is a manager who finds out from finance. |
| Display name | text | — |
| Status | chip: Planned, Published, Confirmed, Swap pending, Cancelled, Completed… | — |
| Break minutes | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Request shift swap (primary button) | `requestShiftSwap` POST `/rota-assignments/{assignmentId}/swap` | inline | ShiftSwap | 409 The swap is not like for like (audit R129 (6)): the other person does not hold the assignment's role (`swap-role-mismatch`), or is not staff at the … | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Day timeline**: One row per person (photo, name, position), a bar per assignment from start to end in venue time with the post ("Main Plaza Gate 2") on the bar, the break as a hatched segment, and a status pill (Published, Confirmed, Swap pending, No show). A now-line across the day. Live attendance overlays the bar: checked in (solid), not yet arrived after start (amber outline "Not in yet"), on break. *(source: screens/P08-venue-back-office.yaml#BO-883 / contracts/satellite/workforce.yaml#/components/schemas/RotaAssignment / contracts/satellite/workforce.yaml#listAttendance)*
- **Week and Month**: Week shows each person's shift times per day ("07:00-15:00"); Month shows headcount per day with a red count where short. Tapping a day opens Day. *(source: contracts/satellite/workforce.yaml#getStaffingCoverage)*
- **Shift detail sheet**: Person, position, post, start-end, break minutes, note, status, and for the supervisor only the flags "Rest 9 h before (minimum 11 h)" and "Over weekly limit". Never labourCost, workstationId or requiredRoleId as raw values; show the role name. *(source: contracts/satellite/workforce.yaml#/components/schemas/RotaAssignment)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Open my shifts**: Goes to EMP-022 with the person's own assignment selected. *(source: screens/P06-staff-app.yaml#EMP-021)*
- **Message**: From the shift sheet, messages that colleague directly (on-shift dot shown). *(source: contracts/satellite/workforce.yaml#sendStaffMessage)*

**Data it reads**: `listRotaAssignments` (onLoad, The rota)

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*
- → `EMP-022` My rota: *A steward reads their own shifts*; carries `assignmentId`; calls `listRotaAssignments`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The roster list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the roster untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No roster yet. Offers Request shift swap (`requestShiftSwap`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on from, to, principalId, departmentId and the roster are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `WORKFORCE_VIEW`, which `listRotaAssignments` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Cached roster with its age |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The swap is not like for like (audit R129 (6)): the other person does not hold the assignment's role (`swap-role-mismatch`), or is not staff at the … |

#### Edge cases to draw

- **Offline**: Cached roster with "Roster as of 06:40"; attendance overlay greyed with "Live status needs a connection". *(source: screens/P06-staff-app.yaml#EMP-021)*
- **Signed-in person lacks WORKFORCE_VIEW**: The screen is not offered; EMP-022 (own shifts) is. If deep-linked, "You can see your own shifts only" with a link to EMP-022. *(source: contracts/satellite/workforce.yaml#listRotaAssignments)*
- **Shift crosses midnight**: Bar runs to the edge with "+1" on the end time ("22:00-06:00 +1"). *(source: contracts/satellite/workforce.yaml#listShiftPatterns)*
- **Long team list**: Cursor paging with "Load more"; the Day view loads people in pages of 50. *(source: contracts/satellite/workforce.yaml#listRotaAssignments)*

#### Consistency with other screens

- Match `BO-055`: Same rota, same statuses and the same calendar component, read-only here.
- Match `BO-883`: The supervisor's phone view of the back-office roster timeline; same status words.
- Match `EMP-022`: Own-shift view of the same data; same bar and pill design.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
day: Sat 10 Oct 2026, Aqua Park, day starts 06:00
rows:
- person: Rahul Menon
  position: Gate steward
  post: Main Plaza Gate 2
  time: 07:00-15:00
  break: 11:00-11:30
  status: Checked in 06:52
- person: Omar Haddad
  position: Gate steward
  post: Main Plaza Gate 3
  time: 07:00-15:00
  status: Not in yet
- person: Maria Santos
  position: Cashier
  post: North Entry ticket office
  time: 09:00-17:00
  status: Late 18 min
- person: Fatima Al Hashimi
  position: Duty supervisor
  post: Aqua Park
  time: 14:00-23:00
  status: Published
  flag: Rest 9 h before (minimum 11 h)
```

#### Permissions

- `listRotaAssignments` → `WORKFORCE_VIEW` (read) · staff
- `requestShiftSwap` → `WORKFORCE_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `WORKFORCE_VIEW`, which `listRotaAssignments` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

15 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.11 | The system should be able to generate operational rosters for staff resources. The rosters should provide information on the staff resources associated with an attraction, their availability, booked … | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.32 | System shall support staff scheduling and assignment. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.33 | System shall manage employee shifts. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.60 | Employees shall receive assignments on mobile devices. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.61 | Employees shall check into assigned resources. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.62 | Employees shall check out assigned resources. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.63 | Employees shall view schedules via mobile app. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 18.1.1 | iOS Mobile Application - System shall provide a native iOS application. | Employee Mobile App & AI Assistant | CONTRACTED | `listRotaAssignments` |
| 18.1.2 | Android Mobile Application - System shall provide a native Android application. | Employee Mobile App & AI Assistant | CONTRACTED | `listRotaAssignments` |
| 1.2.80 | System shall allow employees to request shift swaps, shift transfers, shift pickups, and shift releases. Approval workflows, qualification validation, staffing rules, and manager approvals shall be … | Ticketing Catalogue | CONTRACTED | `requestShiftSwap` |
| 1.2.37 | System shall integrate approved leave requests. | Ticketing Catalogue | CONTRACTED | data `RotaAssignment` |
| 1.2.38 | System shall manage overtime allocation and monitoring. | Ticketing Catalogue | CONTRACTED | data `RotaAssignment` |
| … 3 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Staff see shift timings and upcoming shifts, clock in/out, and submit leave requests in the app. *(client request · MoM 10 Aug 2026, 5.6 Roster, Leave & Break Management, Resources · DI-236)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-021` · status **notStarted** · provenance generated
- Flow F68 *A rota is published, worked and swapped*, step 1: The steward reads the published rota. → **Read, not authored.** `createRotaAssignment` and `updateRotaAssignment` were on this screen until 24 August — **a handheld that could write the rota it is showing.** The rota is published from the …

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (9 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-021?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Request shift swap.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`, `EMP-022`.
- [ ] Every gated control is gated: `WORKFORCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 4 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-022` My rota

**Know when to turn up next.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `core` module |
| Block | Block D · task APP-STAFF-EMP-022 |
| Who uses it | venue staff holding `WORKFORCE_VIEW` (1 read); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listRotaAssignments` reads the population and `getCurrentShift` reads one of them — list, select, act |
| Offline | Cached |
| Opens with | `assignmentId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/operations/my-rota` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Removed 24 August**: createRotaAssignment, updateRotaAssignment. **Bulk-attach residue, found by walking a journey.** A device-settings screen does not read guest loyalty, a venue map does not set a refund policy, a shift summary does not close the shift, and **a rota a steward can rewrite is not a rota.**

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): getCurrentShift reads the till session (SHIFT_OPEN, workstation scope); a rota assignment is not a cash shift and most positions never touch a till (design-notes …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** My rota: a steward's own shifts - today, the next shift, the week and the month - so they know when and where to turn up and see at once when a manager moves them. Read-only by design. The one thing to get right: the next shift is the first thing on screen ("Tomorrow 07:00-15:00, Main Plaza Gate 2"), changes are announced on the shift itself, and the calendar has Day, Week and Month.

**Known correction pending (do not draw the wrong version)**

- **No calendar; From/To pickers, "Principal id" and "Department id" filters** Why: VO-R01 calendar; own shifts need no person or department filter. *(source: contracts/satellite/workforce.yaml#listRotaAssignments; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **listRotaAssignments requires WORKFORCE_VIEW, yet its description says a steward without WORKFORCE_VIEW gets their own assignments** Why: The permission and the described scoping contradict each other; a steward without the permission would get a 403, not their rota. *(source: contracts/satellite/workforce.yaml#listRotaAssignments; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Detail panel "The shift" bound to getCurrentShift (the till session, SHIFT_OPEN, workstation scope) (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Does a steward confirm a published shift (RotaStatus has "confirmed" but no operation sets it from the app)?** → Drawn default accepted: Draw a "Confirm" button on Published shifts, greyed with "Not available yet". *(decided by Chinmay, 2026-10-02; DEC-524 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.
- **Where does a steward request leave from the app (DI-236)? requestLeave is bound only to BO-880.** → Drawn default accepted: Draw "Request leave" on the agenda header opening a short form (type, from, to, half day, reason). *(decided by Chinmay, 2026-10-02; DEC-525 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| From | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?from=` to `listRotaAssignments`. | `listRotaAssignments` ?from |
| To | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?to=` to `listRotaAssignments`. | `listRotaAssignments` ?to |
| Principal id | picker: choose a principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?principalId=` to `listRotaAssignments`. | `listRotaAssignments` ?principalId |
| Department id | picker: choose a department (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?departmentId=` to `listRotaAssignments`. | `listRotaAssignments` ?departmentId |

**Form: Request shift swap** (modal, opened by *Request shift swap*; *Request shift swap* calls `requestShiftSwap`, *Cancel* sends nothing)

**Collects what `requestShiftSwap` sends before it is called.** Required: `toPrincipalId`. Optional: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| To principal `toPrincipalId` | picker: choose a to principal | required | — | — | shows names, sends the id | — | `requestShiftSwap` body |
| Reason `reason` | text area | optional | — | max length 300 | — | — | `requestShiftSwap` body |

Errors to draw in the form: 409 The swap is not like for like (audit R129 (6)): the other person does not hold the assignment's role (`swap-role-mismatch`), or is not staff at the …

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **View**: Day / Week / Month and Agenda (per VO-R01); Agenda is the default on a phone (pack "Today, Tomorrow, Week, Agenda"). No principal or department filters: the list is always the signed-in person's. *(source: screens/P08-venue-back-office.yaml#BO-934 / contracts/satellite/workforce.yaml#listRotaAssignments)*

#### Outputs: what the screen shows and produces

**Shown**

**Every rota assignment** (data table, from `listRotaAssignments`)

| Shows | Format | Notes |
|---|---|---|
| Overtime minutes | 1,234 | BL-044, 1.2.83. UAE labour law limits working hours and mandates rest periods, and nothing in the package counted either. |
| Rest period before | 1,234 | Minutes since the previous shift ended. The check that stops a closing shift followed by an opening one, which is legal in most places and … |
| Labour cost | AED 1,234.50 | Cost at the point of scheduling. A manager building a rota without seeing its cost is a manager who finds out from finance. |
| Display name | text | — |

**The selected rota assignment** (detail panel, from `listRotaAssignments`)

| Shows | Format | Notes |
|---|---|---|
| Overtime minutes | 1,234 | BL-044, 1.2.83. UAE labour law limits working hours and mandates rest periods, and nothing in the package counted either. |
| Labour cost | AED 1,234.50 | Cost at the point of scheduling. A manager building a rota without seeing its cost is a manager who finds out from finance. |
| Display name | text | — |
| Status | chip: Planned, Published, Confirmed, Swap pending, Cancelled, Completed… | — |
| Break minutes | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Request shift swap (primary button) | `requestShiftSwap` POST `/rota-assignments/{assignmentId}/swap` | inline | ShiftSwap | 409 The swap is not like for like (audit R129 (6)): the other person does not hold the assignment's role (`swap-role-mismatch`), or is not staff at the … | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Next shift card**: Top card: date, start-end in venue time, post and position, break planned, supervisor, and a countdown ("Starts in 12 h"). On the day it becomes "Clock in" (EMP-024) from 30 minutes before start. *(source: screens/P08-venue-back-office.yaml#BO-933 / contracts/satellite/workforce.yaml#/components/schemas/RotaAssignment)*
- **Agenda and calendar**: Each shift as a block with status in words: Upcoming (published), Confirmed, Swap pending (with "Awaiting Rahul" or "Awaiting supervisor"), Changed (with old and new post or time), Cancelled (struck through), Completed. Days off shown as "Off", approved leave as "Annual leave". *(source: screens/P08-venue-back-office.yaml#BO-935 / contracts/satellite/workforce.yaml#/components/schemas/RotaStatus)*
- **Hours this week**: Total rostered hours this week against the standard ("38 of 48 h"); no cost figures. *(source: contracts/satellite/workforce.yaml#/components/schemas/StaffingRules / designer default)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Ask to swap**: On a Published or Confirmed shift only, opens EMP-023 with the assignment carried. On other statuses it is disabled with the reason ("Swaps open once the rota is published"). *(source: contracts/satellite/workforce.yaml#requestShiftSwap / F68 step 3)*
- **Add to phone calendar**: Exports the shift as a calendar event; designer may omit. *(source: designer default)*

**Data it reads**: `listRotaAssignments` (onLoad, The rota)

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*
- → `EMP-023` Swap request: *They ask to swap one*; carries `assignmentId`; calls `listRotaAssignments`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rota list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rota untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rota yet. Offers Request shift swap (`requestShiftSwap`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on from, to, principalId, departmentId and the rota are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `WORKFORCE_VIEW`, which `listRotaAssignments` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Cached |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The swap is not like for like (audit R129 (6)): the other person does not hold the assignment's role (`swap-role-mismatch`), or is not staff at the … |

#### Edge cases to draw

- **Assignment changed by a manager**: Push notification and a "Changed" banner on the shift ("Moved from Gate 2 to North Entry, 07:00 unchanged") until opened. *(source: screens/P08-venue-back-office.yaml#BO-935 / MATRIX 1.2.66)*
- **Offline**: Cached rota with its age; swap greyed with "Needs a connection" (requestShiftSwap is online only). *(source: contracts/satellite/workforce.yaml#requestShiftSwap)*
- **No shifts in range**: "No shifts between 12 and 18 Oct" with the next published shift date if one exists; never an empty table. *(source: ADR-0002 / DI-387)*

#### Consistency with other screens

- Match `EMP-021`: Same shift block and status pills.
- Match `BO-934`: The pack's mobile "My Schedule & Assignment Calendar" is this screen; draw once (per VO-R14).
- Match `BO-055`: The back-office rota writes what this screen reads; status labels identical.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
next:
  date: Sat 10 Oct 2026
  time: 07:00-15:00
  post: Main Plaza Gate 2
  position: Gate steward
  break: 11:00-11:30 (30 min, unpaid)
  supervisor: Fatima Al Hashimi
week:
- day: Sun 11 Oct
  shift: 07:00-15:00 Main Plaza Gate 2
  status: Swap pending - awaiting Omar Haddad
- day: Mon 12 Oct
  shift: 'Off'
- day: Tue 13 Oct
  shift: 14:00-22:00 North Entry
  status: Changed - was Gate 3
hours: 38 of 48 h this week
```

#### Permissions

- `listRotaAssignments` → `WORKFORCE_VIEW` (read) · staff
- `requestShiftSwap` → `WORKFORCE_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `WORKFORCE_VIEW`, which `listRotaAssignments` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

15 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.11 | The system should be able to generate operational rosters for staff resources. The rosters should provide information on the staff resources associated with an attraction, their availability, booked … | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.32 | System shall support staff scheduling and assignment. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.33 | System shall manage employee shifts. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.60 | Employees shall receive assignments on mobile devices. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.61 | Employees shall check into assigned resources. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.62 | Employees shall check out assigned resources. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.63 | Employees shall view schedules via mobile app. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 18.1.1 | iOS Mobile Application - System shall provide a native iOS application. | Employee Mobile App & AI Assistant | CONTRACTED | `listRotaAssignments` |
| 18.1.2 | Android Mobile Application - System shall provide a native Android application. | Employee Mobile App & AI Assistant | CONTRACTED | `listRotaAssignments` |
| 1.2.80 | System shall allow employees to request shift swaps, shift transfers, shift pickups, and shift releases. Approval workflows, qualification validation, staffing rules, and manager approvals shall be … | Ticketing Catalogue | CONTRACTED | `requestShiftSwap` |
| 1.2.37 | System shall integrate approved leave requests. | Ticketing Catalogue | CONTRACTED | data `RotaAssignment` |
| 1.2.38 | System shall manage overtime allocation and monitoring. | Ticketing Catalogue | CONTRACTED | data `RotaAssignment` |
| … 3 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Employee mobile app: staff see their assigned bookings and tasks for the day, perform check-in/check-out and shift closing, and request swaps directly from the app — mirroring the booking info on their back-office profile. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel; 4.9 AI Optimization, Mobile App & Analytics · DI-492)*
- Staff see shift timings and upcoming shifts, clock in/out, and submit leave requests in the app. *(client request · MoM 10 Aug 2026, 5.6 Roster, Leave & Break Management, Resources · DI-236)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-022` · status **notStarted** · provenance generated
- Flow F68 *A rota is published, worked and swapped*, step 2: A steward reads their own shifts. → **Read-only, deliberately.** `createRotaAssignment` was on this screen until 24 August — **a rota a steward can rewrite is not a rota.**

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (9 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-022?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Request shift swap.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`, `EMP-023`.
- [ ] Every gated control is gated: `WORKFORCE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-023` Swap request

**Ask somebody to take a shift.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 2 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WORKFORCE_VIEW` (1 read); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listRotaAssignments` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | Queues locally |
| Opens with | `assignmentId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/operations/swap-request` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Removed 24 August**: createRotaAssignment, updateRotaAssignment. **Bulk-attach residue, found by walking a journey.** A device-settings screen does not read guest loyalty, a venue map does not set a refund policy, a shift summary does not close the shift, and **a rota a steward can rewrite is not a rota.**

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Swap request: a steward asks a named colleague to take one of their published shifts, and follows it through the colleague's acceptance and the supervisor's approval. The one thing to get right: it is a request, not a swap - the shift stays theirs until both the colleague and a supervisor have agreed, and the screen says at every step who it is waiting for.

**Known correction pending (do not draw the wrong version)**

- **requestShiftSwap asks someone to take my shift; the client's swap is an exchange of two shifts, plus transfer, pickup and release** Why: The pack's example is Maria's Tuesday for David's Wednesday; the contract has no second assignment, so an exchange cannot be requested. *(source: screens/P08-venue-back-office.yaml#BO-887 / screens/P08-venue-back-office.yaml#BO-940 / contracts/satellite/workforce.yaml#requestShiftSwap; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No operation lets the colleague accept or decline, or the requester withdraw** Why: ShiftSwap has statuses awaitingPeer and withdrawn but nothing writes them, so a request can never leave awaitingPeer. *(source: contracts/satellite/workforce.yaml#/components/schemas/ShiftSwap; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Offline state "Queues locally" while requestShiftSwap is not offline-capable** Why: The state contradicts the contract; draw Send disabled offline. *(source: contracts/satellite/workforce.yaml#requestShiftSwap; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The screen repeats the roster's From/To pickers, id filters and "Every rota assignment" table** Why: Generic residue; the screen is one form and a request list. *(source: screens/P06-staff-app.yaml#EMP-023; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **listShiftSwapRequests has no filters (mine, incoming, status) and returns an unpaged array** Why: A steward needs only their own and incoming requests; a venue-wide array is both too much and a privacy leak. *(source: contracts/satellite/workforce.yaml#listShiftSwapRequests; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is the swap pre-check (hours, rest, overtime, minimum staffing) done before submission as the pack asks, or only at supervisor approval?** → Drawn default accepted: Show role and venue as checked and the rest as "Supervisor will check". *(decided by Chinmay, 2026-10-02; DEC-526 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| From | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?from=` to `listRotaAssignments`. | `listRotaAssignments` ?from |
| To | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?to=` to `listRotaAssignments`. | `listRotaAssignments` ?to |
| Principal id | picker: choose a principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?principalId=` to `listRotaAssignments`. | `listRotaAssignments` ?principalId |
| Department id | picker: choose a department (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?departmentId=` to `listRotaAssignments`. | `listRotaAssignments` ?departmentId |

**Form: Request shift swap** (modal, opened by *Request shift swap*; *Request shift swap* calls `requestShiftSwap`, *Cancel* sends nothing)

**Collects what `requestShiftSwap` sends before it is called.** Required: `toPrincipalId`. Optional: `reason`. **The colleague picker lists only staff with the same role at the same venue**; anyone else is refused 409 `swap-role-mismatch` or `swap-venue-mismatch`. After the request the assignment shows `swapPending` until a supervisor approves (decided 28 September, audit R129 (6)). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| To principal `toPrincipalId` | picker: choose a to principal | required | — | — | shows names, sends the id | — | `requestShiftSwap` body |
| Reason `reason` | text area | optional | — | max length 300 | — | — | `requestShiftSwap` body |

Errors to draw in the form: 409 The swap is not like for like (audit R129 (6)): the other person does not hold the assignment's role (`swap-role-mismatch`), or is not staff at the …

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **My shift**: Carried from EMP-022 (read-only card with date, time, post); only Published or Confirmed shifts can start a swap. *(source: contracts/satellite/workforce.yaml#requestShiftSwap / F68 step 3)*
- **Colleague**: A picker of people who hold the same role at the same venue (the server refuses others with swap-role-mismatch or swap-venue-mismatch). Each candidate shows whether they are free at that time and their hours that week; people already rostered at that time are listed below, disabled with "On shift then". *(source: contracts/satellite/workforce.yaml#requestShiftSwap)*
- **Reason**: Optional, max 300 characters, with chips "Family", "Medical appointment", "Study", "Break cover". *(source: contracts/satellite/workforce.yaml#requestShiftSwap / DI-491)*

#### Outputs: what the screen shows and produces

**Shown**

**Every rota assignment** (data table, from `listRotaAssignments`)

| Shows | Format | Notes |
|---|---|---|
| Overtime minutes | 1,234 | BL-044, 1.2.83. UAE labour law limits working hours and mandates rest periods, and nothing in the package counted either. |
| Rest period before | 1,234 | Minutes since the previous shift ended. The check that stops a closing shift followed by an opening one, which is legal in most places and … |
| Labour cost | AED 1,234.50 | Cost at the point of scheduling. A manager building a rota without seeing its cost is a manager who finds out from finance. |
| Display name | text | — |

**Every shift swap** (data table, from `listShiftSwapRequests`)

| Shows | Format | Notes |
|---|---|---|
| Status | chip: Awaiting peer, Awaiting approval, Approved, Rejected, Withdrawn | Both parties before the supervisor. A swap approved against someone who never agreed is a gap in the rota nobody notices until the shift … |
| Reason | text | — |
| Requested at | 1 Oct 2026, 14:30 | — |

**The selected rota assignment** (detail panel, from `listRotaAssignments`)

| Shows | Format | Notes |
|---|---|---|
| Overtime minutes | 1,234 | BL-044, 1.2.83. UAE labour law limits working hours and mandates rest periods, and nothing in the package counted either. |
| Labour cost | AED 1,234.50 | Cost at the point of scheduling. A manager building a rota without seeing its cost is a manager who finds out from finance. |
| Display name | text | — |
| Status | chip: Planned, Published, Confirmed, Swap pending, Cancelled, Completed… | — |
| Break minutes | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Request shift swap (primary button) | `requestShiftSwap` POST `/rota-assignments/{assignmentId}/swap` | inline | ShiftSwap | 409 The swap is not like for like (audit R129 (6)): the other person does not hold the assignment's role (`swap-role-mismatch`), or is not staff at the … | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **My requests**: Outgoing and incoming requests, newest first, each with both people, the shift, and a step tracker: Sent > Awaiting Omar Haddad > Awaiting supervisor > Approved (or Declined / Rejected / Withdrawn) with times. Status words map awaitingPeer, awaitingApproval, approved, rejected, withdrawn. *(source: screens/P08-venue-back-office.yaml#BO-940 / contracts/satellite/workforce.yaml#listShiftSwapRequests / contracts/satellite/workforce.yaml#/components/schemas/ShiftSwap)*
- **Pre-check before sending**: A short checklist the person sees before Send: same role, same venue, colleague free, colleague stays within weekly hours and rest. Items the server does not check yet are shown as "Supervisor will check". *(source: screens/P08-venue-back-office.yaml#BO-940 / contracts/satellite/workforce.yaml#requestShiftSwap)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Send request**: Assignment becomes Swap pending; confirmation "Request sent to Omar Haddad. Your shift stays yours until approved." A 409 names the failed condition in words ("Omar is not a Gate steward at Aqua Park"; "This shift is not published yet"). *(source: contracts/satellite/workforce.yaml#requestShiftSwap)*
- **Accept / Decline (incoming)**: The colleague's answer moves the request to Awaiting supervisor or Declined; shown on the incoming card. *(source: contracts/satellite/workforce.yaml#/components/schemas/ShiftSwap / F68 step 3)*
- **Withdraw**: Available until approved; the shift returns to its previous status. *(source: contracts/satellite/workforce.yaml#/components/schemas/ShiftSwap)*

**Data it reads**: `listRotaAssignments` (onLoad, The rota); `listShiftSwapRequests` (onLoad, Swap requests and their state)

**Where the user goes next**

- → `EMP-024` Clock in / out: *On the day, they clock in*; calls `requestShiftSwap`
- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The swap request list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the swap request untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No swap request yet. Offers Request shift swap (`requestShiftSwap`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on from, to, principalId, departmentId and the swap request are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `WORKFORCE_VIEW`, which `listRotaAssignments` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Queues locally |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The swap is not like for like (audit R129 (6)): the other person does not hold the assignment's role (`swap-role-mismatch`), or is not staff at the … |

#### Edge cases to draw

- **Nobody accepts before the shift starts**: The original assignment stands; the card says "Not accepted - you are still on this shift" 2 hours before start. *(source: F68 step 3)*
- **Offline**: Send is disabled with "Needs a connection"; the list shows its age. *(source: contracts/satellite/workforce.yaml#requestShiftSwap)*
- **Requester is a supervisor**: They still cannot approve their own swap; the approval goes to another supervisor. *(source: contracts/satellite/workforce.yaml#requestShiftSwap)*

#### Consistency with other screens

- Match `BO-939`: The pack's mobile shift change screen is this screen; one design (per VO-R14).
- Match `BO-887`: The supervisor approves on the back-office marketplace queue (or the mobile approval card); same status words.
- Match `EMP-037`: Incoming requests also appear in the inbox as Action required.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
outgoing:
  shift: Sun 11 Oct 2026, 07:00-15:00, Main Plaza Gate 2, Gate steward
  to: Omar Haddad
  reason: Medical appointment
  status: Awaiting Omar Haddad (sent 09:14)
incoming:
- from: Maria Santos
  shift: Tue 13 Oct 09:00-17:00, North Entry ticket office
  status: Awaiting you
```

#### Permissions

- `requestShiftSwap` → `WORKFORCE_VIEW` (read) · staff
- `listRotaAssignments` → `WORKFORCE_VIEW` (read) · staff
- `listShiftSwapRequests` → `WORKFORCE_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `WORKFORCE_VIEW`, which `listRotaAssignments` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

15 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.80 | System shall allow employees to request shift swaps, shift transfers, shift pickups, and shift releases. Approval workflows, qualification validation, staffing rules, and manager approvals shall be … | Ticketing Catalogue | CONTRACTED | `requestShiftSwap` |
| 1.2.11 | The system should be able to generate operational rosters for staff resources. The rosters should provide information on the staff resources associated with an attraction, their availability, booked … | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.32 | System shall support staff scheduling and assignment. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.33 | System shall manage employee shifts. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.60 | Employees shall receive assignments on mobile devices. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.61 | Employees shall check into assigned resources. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.62 | Employees shall check out assigned resources. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.63 | Employees shall view schedules via mobile app. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 18.1.1 | iOS Mobile Application - System shall provide a native iOS application. | Employee Mobile App & AI Assistant | CONTRACTED | `listRotaAssignments` |
| 18.1.2 | Android Mobile Application - System shall provide a native Android application. | Employee Mobile App & AI Assistant | CONTRACTED | `listRotaAssignments` |
| 1.2.37 | System shall integrate approved leave requests. | Ticketing Catalogue | CONTRACTED | data `RotaAssignment` |
| 1.2.38 | System shall manage overtime allocation and monitoring. | Ticketing Catalogue | CONTRACTED | data `RotaAssignment` |
| … 3 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Employee mobile app: staff see their assigned bookings and tasks for the day, perform check-in/check-out and shift closing, and request swaps directly from the app — mirroring the booking info on their back-office profile. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel; 4.9 AI Optimization, Mobile App & Analytics · DI-492)*
- Staff can request a swap (e.g. break coverage) from another resource; attendance exceptions are marked manually (active, not active, absent, other). *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering; 4.9 AI Optimization, Mobile App & Analytics · DI-491)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-023` · status **notStarted** · provenance generated
- Flow F68 *A rota is published, worked and swapped*, step 3: They ask to swap one. → **A request, not a swap.** The other person has to agree and a supervisor has to allow it — two consents, and the approval path is the one mechanism CF-132 settled.
- Flow F68 branch at step 3 (high): when Nobody accepts the swap., **The original assignment stands.** An unaccepted swap that silently vacates a shift leaves a lane unstaffed.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-023?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Request shift swap.
- [ ] Every transition is wired: `EMP-024`, `EMP-001`, `EMP-002`, `EMP-003`.
- [ ] Every gated control is gated: `WORKFORCE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 5 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-024` Clock in / out

**Record attendance from the device already in hand.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `core` module |
| Block | Block D · task APP-STAFF-EMP-024 |
| Who uses it | venue staff holding `ATTENDANCE_RECORD`, `WORKFORCE_VIEW` (1 operate, 1 read); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listAttendance` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **Device time is recorded and both are kept.** A steward clocking in at a gate with no signal is not late because the sync was |
| Opens with | `recordId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/operations/clock-in-out` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): Amending attendance is a supervisor act (WORKFORCE_MANAGE); it was removed from EMP-025 for that reason and goes from the staff member's own clock screen too … Contract gap recorded 2 October 2026 (CHG-WIR-004): No read returns the caller's own attendance records without WORKFORCE_VIEW.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Clock in and out from the phone already in hand: one big button that knows which shift the person is on, records the device time, and works with no signal. The one thing to get right: a steward at a gate with no signal is not late because the sync was - the screen records the device time, says it is waiting to send, and never asks the person to type a time.

**Known correction pending (do not draw the wrong version)**

- **The screen is a venue attendance list (listAttendance needs WORKFORCE_VIEW) with "Principal id" filter and latitude/longitude columns** Why: The purpose is "record attendance from the device in hand"; the person's own clock card is the screen. Coordinates are shown as a place name. *(source: screens/P06-staff-app.yaml#EMP-024; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **F68 says a clock-in at the wrong venue is refused against the rota, but recordAttendance refuses only out-of-sequence events** Why: The flow and the contract disagree; the contract records it and computes outOfGeofence or unscheduled instead. *(source: F68 step 4 / contracts/satellite/workforce.yaml#recordAttendance; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **listAttendance returns an unpaged array of records** Why: Attendance is live data that pages by cursor (VO-R12). *(source: contracts/satellite/workforce.yaml#listAttendance; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Amend attendance is an action on the staff member's own clock screen (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which verification methods does each venue require (checkpoint QR, NFC, geofence, manager validation), and is there an allowed check-in window?** → Drawn default accepted: Draw checkpoint QR as primary, "Clock in manually" as secondary, and no window enforcement. *(decided by Chinmay, 2026-10-02; DEC-527 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Date | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?date=` to `listAttendance`. | `listAttendance` ?date |
| Principal id | picker: choose a principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?principalId=` to `listAttendance`. | `listAttendance` ?principalId |
| Exceptions only | toggle | optional | — | — | — | Sends `?exceptionsOnly=` to `listAttendance`. | `listAttendance` ?exceptionsOnly |

**Form: Record attendance** (modal, opened by *Record attendance*; *Record attendance* calls `recordAttendance`, *Cancel* sends nothing)

**Collects what `recordAttendance` sends before it is called.** Required: `kind`, `occurredAt`. Optional: `assignmentId`, `accessPointId`, `latitude`, `longitude`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | radio group | required | — | Clock in · Clock out · Break start · Break end | — | — | `recordAttendance` body |
| Occurred at `occurredAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time. The server records both this and when it arrived. | `recordAttendance` body |
| Assignment `assignmentId` | picker: choose an assignment | optional | — | — | shows names, sends the id | — | `recordAttendance` body |
| Access point `accessPointId` | picker: choose an access point | optional | — | — | shows names, sends the id | — | `recordAttendance` body |
| Latitude `latitude` | number field | optional | — | — | — | — | `recordAttendance` body |
| Longitude `longitude` | number field | optional | — | — | — | — | `recordAttendance` body |

Errors to draw in the form: 409 Out of sequence — a clock-out with no clock-in, or a second clock-in. Reported rather than silently corrected.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Shift**: Defaulted to the rota assignment overlapping now (or starting within the check-in window); if several, a choice. With no assignment the button reads "Clock in (not on the rota)" and the record is flagged Unscheduled. *(source: DI-487 / contracts/satellite/workforce.yaml#recordAttendance / contracts/satellite/workforce.yaml#/components/schemas/AttendanceRecord)*
- **Where**: Captured, not typed: scanning the checkpoint QR or tapping the NFC tag at the staff entrance fills the access point; device location is attached where the venue requires it. "Clock in manually" is a secondary link when no checkpoint is available. *(source: screens/P08-venue-back-office.yaml#BO-936 / screens/P06-staff-app.yaml#EMP-024 / contracts/satellite/workforce.yaml#recordAttendance)*
- **occurredAt**: Device time, set automatically at the tap; never editable by the person. *(source: contracts/satellite/workforce.yaml#recordAttendance)*

#### Outputs: what the screen shows and produces

**Shown**

**Every attendance** (data table, from `listAttendance`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Clock in, Clock out, Break start, Break end | — |
| Occurred at | 1 Oct 2026, 14:30 | Device time — when it happened. |
| Recorded at | 1 Oct 2026, 14:30 | When the server received it. Both are kept: a steward clocking in offline at a gate is not late because the sync was. |
| Latitude | 1,234.5 | — |

**The selected attendance** (detail panel, from `listAttendance`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Clock in, Clock out, Break start, Break end | — |
| Occurred at | 1 Oct 2026, 14:30 | Device time — when it happened. |
| Recorded at | 1 Oct 2026, 14:30 | When the server received it. Both are kept: a steward clocking in offline at a gate is not late because the sync was. |
| Original occurred at | 1 Oct 2026, 14:30 | The original is never overwritten. Attendance feeds pay, and a record that can be quietly rewritten is not evidence. |
| Original occurred at | 1 Oct 2026, 14:30 | The original is never overwritten. Attendance feeds pay, and a record that can be quietly rewritten is not evidence. |

**Corrections** (timeline, from `listAttendance`): **Every correction, oldest first** — who, when, the time before and after, and why — rather than only the last amender and reason (decided 28 September, audit R129 (7)).

| Shows | Format | Notes |
|---|---|---|
| Amended at | 1 Oct 2026, 14:30 | — |
| Amended by principal | the name it points at, never the id | — |
| Occurred at before | 1 Oct 2026, 14:30 | The record's time before this correction. |
| Occurred at after | 1 Oct 2026, 14:30 | The time this correction set (`correctedAt` on the request). |
| Reason | text | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Record attendance (primary button) | `recordAttendance` POST `/attendance/clock` | inline | AttendanceRecord | 409 Out of sequence — a clock-out with no clock-in, or a second clock-in. Reported rather than silently corrected. | works offline; opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Clock card**: Person, shift ("08:00-16:00, Ski School" style: "07:00-15:00, Main Plaza Gate 2"), current time large, status "Ready to clock in" / "On shift since 06:52" / "On break since 11:02", and one primary button. *(source: screens/P08-venue-back-office.yaml#BO-936 / screens/P06-staff-app.yaml#EMP-024)*
- **Clock-out summary**: Worked time, breaks taken, overtime if any, and exceptions ("Left 25 min early") after clocking out. *(source: screens/P08-venue-back-office.yaml#BO-936 / contracts/satellite/workforce.yaml#/components/schemas/AttendanceRecord)*
- **Today's record**: The person's own events today, oldest first (Clock in 06:52 at Staff Entrance, Break 11:02-11:31, Clock out 15:04), each marked "Sent" or "Waiting to send", and "Corrected by Fatima Al Hashimi" where amended, with the original time kept. *(source: contracts/satellite/workforce.yaml#/components/schemas/AttendanceRecord / contracts/satellite/workforce.yaml#/components/schemas/AttendanceAmendment)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Clock in / Clock out**: Immediate confirmation with a haptic and the time ("Clocked in 06:52"); offline the same plus "Saved on this phone, will send". A 409 out of sequence ("You are already clocked in since 06:52") is shown as a message, never silently corrected. *(source: contracts/satellite/workforce.yaml#recordAttendance)*
- **Take a break**: Goes to EMP-025. *(source: screens/P06-staff-app.yaml#EMP-024)*

**Data it reads**: `listAttendance` (onLoad, Who was here)

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*
- → `EMP-025` Break management: *They take a break and come back*; carries `recordId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The clock out list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the clock out untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No clock out yet. Offers Record attendance (`recordAttendance`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on date, principalId, exceptionsOnly and the clock out are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `WORKFORCE_VIEW`, which `listAttendance` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ATTENDANCE_RECORD` for `recordAttendance`. |
| Offline (`?state=offline`) | **Device time is recorded and both are kept.** A steward clocking in at a gate with no signal is not late because the sync was |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Out of sequence — a clock-out with no clock-in, or a second clock-in. Reported rather than silently corrected. |

#### Edge cases to draw

- **Clock-in recorded offline and synced later**: Shows device time and arrival time ("06:52, sent 07:40"); not marked late or absent because of the delay. *(source: contracts/satellite/workforce.yaml#/components/schemas/AttendanceRecord / DI-065)*
- **Clock-in outside the venue area**: Recorded and flagged "Outside the venue area"; the person sees "Your supervisor will see this was outside the venue." *(source: contracts/satellite/workforce.yaml#/components/schemas/AttendanceRecord)*
- **Forgot to clock out yesterday**: "No clock-out on Fri 9 Oct. Ask your supervisor to correct it." Not auto-filled. *(source: contracts/satellite/workforce.yaml#recordAttendance)*
- **Shared device, another person still clocked in on it**: Clock events belong to the signed-in person, not the device; the screen shows only the signed-in person's state. *(source: ADR-0002)*

#### Consistency with other screens

- Match `BO-056`: Every tap here is a row there; exception words identical (Late, Left early, No clock-out, No show, Outside the venue area, Not on the rota).
- Match `BO-936`: The pack's mobile check-in screen is this screen; one design (per VO-R14).
- Match `BO-889`: Corrections are made there (or BO-056) by a supervisor, never here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
card:
  person: Rahul Menon
  shift: Sat 10 Oct 2026, 07:00-15:00
  post: Main Plaza Gate 2
  now: 06:52
  status: Ready to clock in
  checkpoint: Staff Entrance North
today:
- Clock in 06:52 - Staff Entrance North - Sent
- Break 11:02-11:31 - Sent
- Clock out 15:04 - Waiting to send
```

#### Permissions

- `recordAttendance` → `ATTENDANCE_RECORD` (operate) · staff
- `listAttendance` → `WORKFORCE_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `WORKFORCE_VIEW`, which `listAttendance` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ATTENDANCE_RECORD` for `recordAttendance`.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.81 | System shall record planned shifts, actual check-in times, actual check-out times, attendance status, lateness, early departures, no-shows, overtime hours, attendance exceptions, and workforce … | Ticketing Catalogue | CONTRACTED | `recordAttendance` |
| 18.9.1 | Attendance Management - Users shall clock in and clock out. | Employee Mobile App & AI Assistant | CONTRACTED | `recordAttendance` |
| 18.9.2 | Shift Management - Users shall view assigned shifts. | Employee Mobile App & AI Assistant | CONTRACTED | `recordAttendance` |
| 8.9.7 | System shall display staffing levels, shift attendance, assignments, absences, overtime, and workforce utilization. | Unified Operations Dashboard | CONTRACTED | `listAttendance` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Employee mobile app: staff see their assigned bookings and tasks for the day, perform check-in/check-out and shift closing, and request swaps directly from the app — mirroring the booking info on their back-office profile. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel; 4.9 AI Optimization, Mobile App & Analytics · DI-492)*
- Shift templates (morning/afternoon/evening) define working patterns; the system recognises which shift a staff member has logged into from the configured shift timings. Leave/absence types and quotas work as a lightweight HR module, optionally integrated with an external HR/time-and-attendance system. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel Resource Management · DI-487)*
- Staff see shift timings and upcoming shifts, clock in/out, and submit leave requests in the app. *(client request · MoM 10 Aug 2026, 5.6 Roster, Leave & Break Management, Resources · DI-236)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-024` · status **notStarted** · provenance generated
- Flow F68 *A rota is published, worked and swapped*, step 4: On the day, they clock in. → **Attendance is not the shift.** A rota says who should be there; attendance says who was, and the gap is the number a venue manages.
- Flow F68 branch at step 4 (medium): when They clock in at the wrong venue., Refused against the rota. **A steward at the wrong site is a steward the right site is waiting for.**

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-024?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Record attendance.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`, `EMP-025`.
- [ ] Every gated control is gated: `ATTENDANCE_RECORD`, `WORKFORCE_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 4 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P06 reference designs** (from `handoff/design-batches/apps/4-staff-app/README.md`)

- `sources/designs/TICVAI_Employee_App_UI_Reference_1.pdf`: the client's employee app reference: dark theme, Home, Tasks, Scan, AI, More.
- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: the client-approved POS, for operator density and components.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-040, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

**Workshop tracker rows about P06 as a whole** (3: 0 open, 3 closed). Open first; a closed row says where it went on 30 September.

- **A48** Update Employee App wireframe: remove the manual role-selection screen — role and home dashboard should be determined automatically from backend RBAC configuration immediately after login *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A49** Confirm scope: deliver a lightweight standalone ticket-validation app for dedicated scanner devices, in addition to the scan/validate function embedded in the full Staff Operations App *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A71** Design an offline-first, native ticket-scanning/access-control capability (local scan storage with sync-on-reconnect) for both the dedicated scanner app and the scanning function embedded in the Employee App *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 10 Aug 2026 · workshop tracker)*

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

### Across P06 Venue Staff App

- From the case screen agents act on the customer's bookings/tickets (date change, reschedule, resend tickets), initiate refunds/compensation, route for internal approval, or escalate to another department, which sees it on that department's mobile app. *(client request · MoM 31 Aug 2026, 4.1 Customer Service & Contact Center (Case Management) · DI-542)*
- Client boards (POS Frontline, F&B, Retail, Inventory & Procurement) share one architecture: six boards of ten screens per domain, a command centre first and an AI/analytics board last, under the hierarchy Company > Venue > Department > Workstation > Operator/Shift > Transaction > Exception > Reconciliation > Analytics. *(agreed · client-design-boards-audit 20 Aug 2026, Opening / What the boards give us · DI-400)*
- Staff-facing POS and tablet UIs always carry TICVAI branding, not client branding. *(agreed · MoM 14 Aug 2026, 8. POS / Kiosk Branding · DI-296)*
- Approval screens offer Approve, Reject, Return and Request More Information, show an AI-generated approval summary beside the request, and a visible trail of who approved at each stage (e.g. IT → Ops Manager → Finance → CEO → IT publishes). *(client request · MoM 10 Aug 2026, 5.5 Multi-Stage Approval Workflow · DI-235)*
- Two separate apps: an access-control app (handhelds or fixed terminals) scoped purely to entry validation/scanning, and an employee app (approvals, alerts/messages, matrix features) that may include a basic ticket-validity lookup but not full scanning. *(agreed · MoM 3 Aug 2026, 12. Mobile Application Strategy · DI-128)*
- Offline state must be clearly visible in the UI, e.g. a visible mode indicator or greyed-out unavailable functions; exact visual treatment to be settled in the UI/UX session. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-072)*
- Allam: the app detects loss of connectivity and switches to offline mode automatically, without cashier action, then restores online mode and syncs pending transactions automatically. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-071)*
- Offline capability applies to POS terminals, handheld/validation devices (turnstiles, scanners), and staff and customer mobile apps. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-070)*
- Allam: the platform is device-agnostic (Android, iOS and web) so sales can continue on any available device. *(agreed · MoM 31 Jul 2026, 8. Point-of-Sale Data Sync Strategy · DI-068)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*

### In P06 · Operations

- Employee app navigation: Work Orders, Task & Assets, Inventory/Safety/Inspections, Attendance, Approvals/Requests, Incidents, Communications, Venue Map; plus employee ID/profile and preferences. *(client request · MoM 10 Aug 2026, 5.2 Core Navigation & Modules · DI-228)*

**16 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"askReportingQuestion": {"method":"POST","path":"/reports/ask","contract":"reporting","summary":"Natural-language reporting query","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"NaturalLanguageAnswer"},
"createAiConversation": {"method":"POST","path":"/conversations","contract":"ai","summary":"Open a conversation","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiConversation"},
"getLatestBundle": {"method":"GET","path":"/catalogue/bundles/latest","contract":"catalogue","summary":"Pull the current bundle for this workstation's venue","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":"since","in":"query","required":null},{"name":"If-None-Match","in":"header","required":null}],"requestBody":null,"responds":"CatalogueBundle"},
"getOfflinePackage": {"method":"GET","path":"/access/offline-package","contract":"access","summary":"Entitlement and rule set for offline validation","permission":"ACCESS_VALIDATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":"sinceVersion","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":"validFrom","in":"query","required":true},{"name":"validTo","in":"query","required":true},{"name":"If-None-Match","in":"header","required":null}],"requestBody":null,"responds":"OfflinePackage"},
"getOrder": {"method":"GET","path":"/orders/{orderId}","contract":"orders","summary":"Read an order","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Order"},
"getOrderStatement": {"method":"GET","path":"/orders/{orderId}/statement","contract":"orders","summary":"Full financial history of an order","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"OrderStatement"},
"listAiConversations": {"method":"GET","path":"/conversations","contract":"ai","summary":"A principal's conversation history","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAttendance": {"method":"GET","path":"/attendance","contract":"workforce","summary":"Who was here","permission":"WORKFORCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"date","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"exceptionsOnly","in":"query","required":null}],"requestBody":null,"responds":"AttendanceRecord"},
"listCatalogueBundles": {"method":"GET","path":"/catalogue/bundles","contract":"catalogue","summary":"List published catalogue bundles","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"BundleSummary"},
"listOrderRefunds": {"method":"GET","path":"/orders/{orderId}/refunds","contract":"orders","summary":"List refunds against an order","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOrders": {"method":"GET","path":"/orders","contract":"orders","summary":"List orders","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"shiftId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"createdFrom","in":"query","required":null},{"name":"createdTo","in":"query","required":null},{"name":"workstationId","in":"query","required":null},{"name":"subjectId","in":"query","required":null},{"name":"tender","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listRotaAssignments": {"method":"GET","path":"/rota-assignments","contract":"workforce","summary":"The rota","permission":"WORKFORCE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"departmentId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listScans": {"method":"GET","path":"/access/scans","contract":"access","summary":"List scan events","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"accessPointId","in":"query","required":null},{"name":"ticketId","in":"query","required":null},{"name":"outcome","in":"query","required":null},{"name":"recordedFrom","in":"query","required":null},{"name":"recordedTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listShiftSwapRequests": {"method":"GET","path":"/shift-swaps","contract":"workforce","summary":"Swap requests and their state","permission":"WORKFORCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ShiftSwap"},
"listSyncRejections": {"method":"GET","path":"/sync/rejections","contract":"orders","summary":"Entries the server refused","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"workstationId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"resolved","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"lookupTicket": {"method":"GET","path":"/access/lookup","contract":"access","summary":"Read-only validity check without admitting","permission":"TICKET_LOOKUP","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"mediaCode","in":"query","required":null},{"name":"ticketId","in":"query","required":null}],"requestBody":null,"responds":"TicketStatus"},
"overrideAccess": {"method":"POST","path":"/access/override","contract":"access","summary":"Admit against a failed validation","permission":"ACCESS_OVERRIDE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ValidationResult"},
"recordAnswerFeedback": {"method":"POST","path":"/messages/{messageId}/feedback","contract":"ai","summary":"Say whether an answer helped","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiAnswerFeedback"},
"recordAttendance": {"method":"POST","path":"/attendance/clock","contract":"workforce","summary":"Clock in, clock out, or take a break","permission":"ATTENDANCE_RECORD","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AttendanceRecord"},
"reportBundleApplied": {"method":"POST","path":"/catalogue/bundles/{version}/applied","contract":"catalogue","summary":"Report that a workstation applied a bundle","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"reprintOrder": {"method":"POST","path":"/orders/{orderId}/reprints","contract":"orders","summary":"Reprint or resend tickets","permission":"ORDER_REPRINT","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"requestShiftSwap": {"method":"POST","path":"/rota-assignments/{assignmentId}/swap","contract":"workforce","summary":"Ask someone to take your shift","permission":"WORKFORCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"sendAiMessage": {"method":"POST","path":"/conversations/{conversationId}/messages","contract":"ai","summary":"Ask","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiMessage"},
"syncScans": {"method":"POST","path":"/access/scans","contract":"access","summary":"Replay scans recorded offline","permission":"ACCESS_VALIDATE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ScanSyncResult"},
"validateAccess": {"method":"POST","path":"/access/validate","contract":"access","summary":"Validate media at an access point and admit or deny","permission":"ACCESS_VALIDATE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ValidateRequest","responds":"ValidationResult"},
"validateGroupAccess": {"method":"POST","path":"/access/group-validate","contract":"access","summary":"Admit a group on one read","permission":"ACCESS_VALIDATE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ValidationResult"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessAccreditationCredential": {"type":"object","x-ticvai-persistence":"access.accreditation_credential","x-ticvai-agreed":"29 September: build pass (group OWN, from group RA's handoff; BL-181); the events accreditation.credentialIssued and accreditation.holderStatusChanged name access as their critical consumer","description":"**What a gate needs to admit an accredited person, kept by `access`** (29 September, build). Written only by the consumers of `accreditation.credentialIssued` (a row per credential; a replacement sets the replaced row's `admits` false) and `accreditation.holderStatusChanged` (every credential of the holder: `admits` false unless the holder is `active`, validity taken from the event). Read by `validateAccess` and shipped in the offline package. The record of truth stays in `accreditation`; this is a copy shaped for the gate, never edited by a person.","required":["id","holderId","encodedIdentifier","admits","scopePath"],"properties":{"id":{"type":"string","format":"uuid","description":"The accreditation credential's id (`credentialId` on the events)."},"holderId":{"type":"string","format":"uuid"},"programmeId":{"type":"string","format":"uuid","nullable":true},"kind":{"type":"string","description":"printedBadge, mobileCredential, qr, nfcCard, rfidCard or wristband, as issued."},"encodedIdentifier":{"type":"string","x-ticvai-unique":"tenant","description":"What the gate reads from the credential. Never sent to webhook subscribers."},"validFrom":{"type":"string","format":"date","nullable":true},"validTo":{"type":"string","format":"date","nullable":true},"zoneIds":{"type":"array","description":"The holder's effective zones, from the event (`effectiveZones`).","items":{"type":"string","format":"uuid"}},"holderStatus":{"type":"string","enum":["active","suspended","revoked","expired","archived"],"description":"The holder's status as last published; only `active` admits."},"admits":{"type":"boolean","description":"False once the credential is replaced or the holder is not active."},"sourceChangedAt":{"type":"string","format":"date-time","description":"The `issuedAt` or `changedAt` of the event last applied; an older event arriving late is ignored."},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005), the accreditation programme's scope."}}},
"AccessDynamicPolicy": {"type":"object","x-ticvai-persistence":"access.dynamic_policy","description":"One guest-admission dynamic (attribute-based) policy with its current content - type, context or identity it tests, condition expression, result, priority, zones, validity, status and current version. Not identity.authorisation_policy, which is staff permission (declared 29 September, data-model close-out DM1).\n\n**Guest admission lives here and nowhere else** (ADR-0068, accepted 1 October). `validateAccess` online and the gate offline evaluate the same active version: `getOfflinePackage` carries it, and every `scan_event` records the policy and version that decided it (`dynamicPolicyId`, `dynamicPolicyVersion`) and the set it was decided under (`policySetVersion`). The condition is `conditionRule`, a closed JSON format (`AdmissionRule`), not free text. Identity's staff-permission engine was renamed `AuthorisationPolicy` on the same day, so \"access policy\" means this.\n\n**Which of the two policy engines this is** (stated 29 September, build pass). **This one governs who may pass which gate**: admission of a guest, pass holder, accreditation holder or employee at an access point, decided in validation with results a gate acts on (allow, deny, review, requireId, requireBiometric, requireCompanion, requireSupervisor). **identity `AuthorisationPolicy` governs who may do what in the software**: a principal's permissions on operations and screens, decided by identity `evaluateAccess`. An employee's badge opening a staff door is decided here; the same employee approving a refund is decided in identity. Effectiveness is reported per engine: `listDynamicPolicyEffectiveness` here, `listAuthorisationPolicyEffectiveness` in identity.","required":["id","scopePath","name","policyType","conditionRule","result","status","currentVersion"],"properties":{"id":{"type":"string","format":"uuid","description":"The policyId"},"venueId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string","description":"ltree of the owning scope node; where it applies further is access.policy_scope_assignment"},"name":{"type":"string","maxLength":200},"policyType":{"type":"string","enum":["guestAttribute","accreditation","occupancy","employee","risk","membership","timeEvent"]},"contextType":{"type":"string","enum":["date","day","time","season","event","performance","specialEvent","holiday","operatingCalendar","occupancy","attractionStatus"],"nullable":true,"description":"Context/time/event policies (setContextTimeEvent)"},"identityType":{"type":"string","enum":["guest","member","annualPassHolder","employee","contractor","vendor","performer","media","vip","security","emergencyServices","eventStaff"],"nullable":true,"description":"Identity-based policies (listIdentityMembershipAccreditation)"},"conditionRule":{"$ref":"#/components/schemas/AdmissionRule","description":"The condition, in the closed JSON rule format evaluated the same way online and at the gate (ADR-0068; replaces the free-text `conditionExpression`)."},"result":{"type":"string","enum":["allow","deny","review","requireId","requireBiometric","requireCompanion","requireSupervisor"]},"priority":{"type":"integer","nullable":true},"allowedZoneIds":{"type":"array","items":{"type":"string","format":"uuid"}},"deniedZoneIds":{"type":"array","items":{"type":"string","format":"uuid"}},"monitorThresholdPercent":{"type":"integer","minimum":0,"maximum":100,"nullable":true,"description":"Occupancy policies. Percent at which the band becomes Monitor"},"restrictThresholdPercent":{"type":"integer","minimum":0,"maximum":100,"nullable":true,"description":"Occupancy policies. Percent at which the band becomes Restrict"},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true,"description":"The grant expires automatically at validTo"},"status":{"type":"string","enum":["draft","pendingApproval","active","inactive","expired"],"default":"draft"},"currentVersion":{"type":"integer","minimum":1,"description":"The version in force (access.dynamic_policy_version)"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AiAnswerFeedback": {"type":"object","x-ticvai-persistence":"ai.answer_feedback","description":"**What a person thought of an answer** (AIC-062). One label per message per person; it feeds the golden sets and the knowledge-gap list, never an online update (design 3.5).","required":["messageId","rating"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"messageId":{"type":"string","format":"uuid","x-ticvai-references":"ai.message"},"conversationId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.conversation"},"rating":{"type":"string","enum":["helpful","notHelpful"]},"reason":{"type":"string","enum":["wrong","outdated","incomplete","notGrounded","unsafe","other"],"nullable":true},"comment":{"type":"string","nullable":true,"maxLength":1000},"audience":{"type":"string","enum":["staff","guest"],"readOnly":true},"principalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"subjectId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The guest, where the audience is `guest`."},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiConversation": {"type":"object","x-ticvai-persistence":"ai.conversation","required":["id","principalId","module","startedAt"],"properties":{"id":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"module":{"$ref":"../shared/common.yaml#/components/schemas/ModuleKey"},"locale":{"type":"string"},"messageCount":{"type":"integer"},"startedAt":{"type":"string","format":"date-time"},"lastMessageAt":{"type":"string","format":"date-time"}}},
"AiMessage": {"type":"object","x-ticvai-persistence":"ai.message","required":["id","conversationId","role","content","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"conversationId":{"type":"string","format":"uuid"},"role":{"type":"string","enum":["user","assistant","system"]},"content":{"type":"string"},"sources":{"$ref":"#/components/schemas/AiSourceList"},"confidence":{"type":"number","nullable":true,"description":"8.1.5, 8.3.67. **Nullable on purpose** — a provider that does not report confidence must yield null rather than an invented number, and an interface showing 0.9 because the code defaulted it is worse than showing nothing.\n"},"rationale":{"type":"string","nullable":true,"description":"8.3.68, 8.3.69."},"proposedAction":{"allOf":[{"$ref":"#/components/schemas/ProposedAction"}],"nullable":true,"description":"Present where the answer suggests a change. **A draft, never applied here.**"},"traceId":{"type":"string"},"provider":{"$ref":"#/components/schemas/AiProviderKind"},"model":{"type":"string"},"promptTokens":{"type":"integer"},"completionTokens":{"type":"integer"},"latencyMs":{"type":"integer"},"createdAt":{"type":"string","format":"date-time"}}},
"AiProviderKind": {"type":"string","enum":["openai","gemini","anthropic","azureOpenai","localLlm","openaiCompatible"],"description":"`openaiCompatible` (added 29 September, AI design 3.3): a customer endpoint that speaks the OpenAI API, taken with no custom development (AIC-009). Any other protocol needs an adapter.\n**Core42 Compass is reached through `openaiCompatible`** (Chinmay, 2 October: the AI residency decision, amending AI-D02; CHG-CSA-002). Compass is the provider of the `uaeOnly` residency class (common `AiResidencyClass`): Small tier Compass GPT-4.1 mini (or Seraj), Strong tier Compass GPT-5, with OpenAI UAE as the fallback. OpenAI UAE is `openai` with a UAE `endpoint`: OpenAI's UAE-region API project, `ae.api.openai.com` (in-country processing, on OpenAI sales approval), allowed under `uaeOnly` and the only endpoint a `uaeOnly` BYOK OpenAI key may use (CHG-R1S-016). **We host no model** (Chinmay, 3 October, CHG-R1S-002): there is no in-cell open-weights fallback; `localLlm` is used only where a client asks for self-hosting and runs the model on the client's estate (`onPrem`).\n**A kind is a protocol, not a vendor** (Chinmay, 2 October, contract follow-ups: BYOK accepts any provider; CHG-FUP-008). Any vendor is accepted, named in `AiProvider.vendor`: Mistral, Cohere or any other is reached through `openaiCompatible` where its API speaks it, which the compatibility test confirms before activation (`AiProviderCompatibility`). A new native adapter is a new value here, a breaking change for a client built earlier that goes out with an approval (`docs/active/breaking-changes.yaml`); until then a vendor without either protocol is refused `422 provider-protocol-unsupported`.\n"},
"AiSourceList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**The sources an answer was grounded in, stored with the answer** (8.3.70). One `jsonb` column on the row that carries it — `ai.message.sources` and `ai.activity.sources` — because the grounding audit reads the list as it was when the answer was given, and a source is never queried on its own.\n","items":{"$ref":"#/components/schemas/AiSource"}},
"AttendanceAmendment": {"type":"object","x-ticvai-persistence":"workforce.attendance_amendment","description":"One correction to an attendance record, appended by `amendAttendance` and never updated (decided 28 September, audit R129 (7)).\n","required":["id","attendanceRecordId","amendedByPrincipalId","amendedAt","occurredAtBefore","occurredAtAfter","reason"],"properties":{"id":{"type":"string","format":"uuid"},"attendanceRecordId":{"type":"string","format":"uuid"},"amendedByPrincipalId":{"type":"string","format":"uuid"},"amendedAt":{"type":"string","format":"date-time"},"occurredAtBefore":{"type":"string","format":"date-time","description":"The record's time before this correction."},"occurredAtAfter":{"type":"string","format":"date-time","description":"The time this correction set (`correctedAt` on the request)."},"reason":{"type":"string","maxLength":300}}},
"AttendanceRecord": {"type":"object","x-ticvai-persistence":"workforce.attendance","required":["id","principalId","kind","occurredAt"],"properties":{"id":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid"},"assignmentId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["clockIn","clockOut","breakStart","breakEnd"]},"occurredAt":{"type":"string","format":"date-time","description":"Device time — when it happened."},"recordedAt":{"type":"string","format":"date-time","description":"When the server received it. **Both are kept**: a steward clocking in offline at a gate is not late because the sync was.\n"},"accessPointId":{"type":"string","format":"uuid","nullable":true},"latitude":{"type":"number","nullable":true},"longitude":{"type":"number","nullable":true},"isAmended":{"type":"boolean","readOnly":true},"amendedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Who made the latest amendment. The full history is `amendments` (audit R129 (7))."},"amendmentReason":{"type":"string","nullable":true,"readOnly":true,"description":"The latest amendment's reason. The full history is `amendments` (audit R129 (7))."},"originalOccurredAt":{"type":"string","format":"date-time","nullable":true,"description":"**The original is never overwritten.** Attendance feeds pay, and a record that can be quietly rewritten is not evidence.\n"},"amendments":{"type":"array","readOnly":true,"description":"**Every correction, oldest first, one row each** (decided 28 September, audit R129 (7)). A single set of amendment columns holds only the last one, and the second correction to a record would erase the evidence of the first.\n","items":{"$ref":"#/components/schemas/AttendanceAmendment"}},"exception":{"type":"string","nullable":true,"enum":["late","earlyLeave","missingClockOut","noShow","outOfGeofence","unscheduled"],"description":"Computed against the rota. Null where the record matches what was expected."}}},
"BundleSummary": {"x-ticvai-persistence":"none — projection over bundle","type":"object","description":"One published catalogue bundle — the signed snapshot terminals pull (ADR-0013). Not `promotions.Bundle`, which is a sellable product made of other products.","required":["version","venueId","publishedAt","publishedBy","contentHash","staleAfter","sizeBytes"],"properties":{"version":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"publishedAt":{"type":"string","format":"date-time"},"publishedBy":{"type":"string","format":"uuid"},"contentHash":{"type":"string"},"signatureKeyId":{"type":"string","description":"Key that signed this bundle. A terminal offline across a key rotation needs a grace window, or it cannot verify the next bundle.\n"},"staleAfter":{"type":"string","format":"date-time"},"sizeBytes":{"type":"integer"},"note":{"type":"string"},"appliedByWorkstations":{"type":"integer"}}},
"CatalogueBundle": {"x-ticvai-persistence":"catalogue.published_bundle","type":"object","required":["version","venueId","isDelta","signature","signatureKeyId","contentHash","staleAfter","payload"],"properties":{"version":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"isDelta":{"type":"boolean"},"baseVersion":{"type":"string","nullable":true,"description":"Present when `isDelta`. The version this delta applies to."},"signature":{"type":"string","description":"Detached signature over `contentHash`. The terminal verifies before applying and rolls back on failure — a half-applied catalogue is never traded against.\n"},"signatureKeyId":{"type":"string"},"contentHash":{"type":"string"},"staleAfter":{"type":"string","format":"date-time"},"payload":{"type":"object","description":"Products, variants, price lists, prices, tax codes, events, performances, envelope definitions, data mask field definitions and the venue's sale boards. Shape is versioned with the bundle format, not with this API.\n","additionalProperties":true,"properties":{"saleBoards":{"type":"array","description":"**The venue's sale boards as `tenancy.listSaleBoards` returns them**, read from `platform.sale_board` when the bundle is snapshotted (decided 28 September, audit R129 (4)). A board changed by `updateSaleBoard` reaches terminals here, with the next bundle, and never mid-transaction.\n","items":{"type":"object","additionalProperties":true}}}}}},
"DenyReason": {"type":"string","description":"Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a boolean.\n","enum":["notFound","notYetValid","expired","alreadyUsed","reentryLimitReached","exitRequiredBeforeReentry","wrongAccessPoint","wrongPerformance","outsideAdmissionWindow","entitlementSuspended","blacklisted","capacityReached","waiverRequired","accompanimentRequired","mediaDeactivated","unpaid","delegatedRightExhausted","delegatedRightRevoked","journeyNotCovered"]},
"Direction": {"type":"string","enum":["entry","exit","reentry","crossover"]},
"ExchangeRateDecimal": {"type":"string","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,6)","description":"**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one — a JavaScript client must not round a rate in transit. **Six decimal places**, the precision `finance.FxRate.rate` asks for, and stored at that precision.\n","pattern":"^\\d+(\\.\\d{1,6})?$"},
"GeneratedQuery": {"x-ticvai-persistence":"none — embedded; stored whole in `reporting.natural_language_query`","type":"object","description":"The structured query a natural-language question produced — data source, columns, filters, grouping. Named on 26 September so the answer and the kept copy are one shape.\n","properties":{"dataSource":{"$ref":"#/components/schemas/DataSource"},"columns":{"type":"array","items":{"$ref":"#/components/schemas/ReportColumn"}},"filters":{"type":"array","items":{"$ref":"#/components/schemas/ReportFilter"}},"groupBy":{"type":"array","items":{"type":"string"}},"compiledSql":{"type":"string","nullable":true,"description":"The SQL the semantic spec compiled to, exactly as run on the analytical replica (29 September, design 5.7). The replica's row-level security applies beneath it, so it does not need to carry the caller's scope. Null on queries kept before the semantic compile.\n"}}},
"MediaKind": {"type":"string","enum":["image","video","audio","document","vector","font","archive","model3d"],"description":"`model3d` added 3 October 2026 (r1 additions; ADR-0069 action item 4): a glTF binary (`model/gltf-binary`, `.glb`) venue model, at most 40 MB. No rendition or derivative is generated for it; the guest app downloads the file as uploaded.\n"},
"ModuleKey": {"$ref":"../shared/common.yaml#/components/schemas/ModuleKey"},
"NaturalLanguageAnswer": {"x-ticvai-persistence":"none — computed","type":"object","required":["conversationId","question","interpretation","result","reliability"],"properties":{"conversationId":{"type":"string"},"question":{"type":"string"},"interpretation":{"type":"string","description":"What the question was understood to mean, in plain language. When the question is outside the semantic model, the \"not available yet\" sentence."},"semanticSpec":{"allOf":[{"$ref":"#/components/schemas/ReportingSemanticQuerySpec"}],"nullable":true,"description":"What the model returned instead of SQL (design 2.2 E, 5.7): metric, dimensions, filters, period, comparison, as validated against the semantic model. Null when the question is outside it. **Also kept**, on `NaturalLanguageQuery`, so a follow-up edits it.\n"},"generatedQuery":{"allOf":[{"$ref":"#/components/schemas/GeneratedQuery"}],"nullable":true,"description":"The query the spec compiled to: data source, columns, filters, grouping, and the compiled SQL in `compiledSql`. Returned so the answer can be checked. An answer nobody can verify is worse than no answer. **Also kept, as `NaturalLanguageQuery`**, for `saveNaturalLanguageQuery`. Null when the question is outside the semantic model.\n"},"result":{"allOf":[{"$ref":"#/components/schemas/ReportResult"}],"nullable":true,"description":"Null when the question is outside the semantic model."},"dataAsOf":{"type":"string","format":"date-time","nullable":true,"description":"Replica position the answer was read at, the result's `dataAsOf`, stated beside the answer so a figure that moved is not argued about. Null when nothing was run."},"reliability":{"$ref":"#/components/schemas/ReportingAnswerReliability"},"unavailableReason":{"allOf":[{"$ref":"#/components/schemas/ReportingUnavailableReason"}],"nullable":true,"description":"Set only when `reliability` is `insufficientEvidence` because the question is outside the semantic model (\"not available yet\"); names which part is not modelled."},"confidence":{"type":"number","minimum":0,"maximum":1,"deprecated":true,"description":"Superseded by `reliability` on 29 September (design 5.6, never a bare percentage for analytics). Returned for one release, then removed."},"suggestedFollowUps":{"type":"array","items":{"type":"string"}},"modelVersion":{"type":"string"},"tokensUsed":{"type":"integer"}}},
"OfflinePackage": {"x-ticvai-persistence":"none — generated artefact in object storage","type":"object","required":["etag","generatedAt","validFrom","validTo","accessPointId","entitlements"],"properties":{"etag":{"type":"string"},"generatedAt":{"type":"string","format":"date-time"},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"accessPointId":{"type":"string","format":"uuid"},"entitlementsVersion":{"type":"integer","description":"The highest `access.entitlement` change included (SD-052, 29 September). A refresh sends it as `sinceVersion` and receives only what changed after it, so a 60,000-guest venue is not re-sent whole."},"policySetVersion":{"type":"string","description":"**The active admission policy version the package carries** (ADR-0068, 1 October): a fingerprint of the `(id, currentVersion)` of every policy in `dynamicPolicies`, computed the same way by `validateAccess` online. Every scan the gate records carries it (`ScanEvent.policySetVersion`), so a scan decided offline under a set that has since changed is visible at sync rather than assumed equal."},"dynamicPolicies":{"type":"array","description":"The active guest-admission dynamic policies for this access point's zones (SD-052), each at its active version with its `conditionRule` (ADR-0068), so an offline gate applies the same rules as an online one.","items":{"$ref":"#/components/schemas/AccessDynamicPolicy"}},"entitlements":{"type":"array","description":"Read from `access.entitlement` (SD-052). With `sinceVersion`, only the rows changed after it, including ones now void or used, so a device removes them.","items":{"type":"object","required":["ticketId","mediaCodes","validFrom","validTo","entriesAllowed","reentryAllowed"],"properties":{"ticketId":{"type":"string","format":"uuid","description":"The `Entitlement.id`."},"mediaCodes":{"type":"array","items":{"type":"string"},"description":"A ticket may carry several media over its life."},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"performanceId":{"type":"string","format":"uuid","nullable":true},"entriesAllowed":{"type":"integer","nullable":true},"entriesUsed":{"type":"integer"},"reentryAllowed":{"type":"boolean"},"admissionRulesId":{"type":"string","format":"uuid"}}}},"delegatedRights":{"type":"array","description":"Redemption rights issued by other cells and valid at this access point. Included in the package so a cross-region entitlement still admits when the inter-cell link is down — the same reason locally issued entitlements are included.\n","items":{"type":"object","required":["rightId","ticketId","issuingCellId","validFrom","validTo","entriesAllowed","entriesConsumed"],"properties":{"rightId":{"type":"string"},"ticketId":{"type":"string","format":"uuid","description":"The `Entitlement.id` in the issuing cell."},"issuingCellId":{"type":"string"},"guestLinkId":{"type":"string","nullable":true},"mediaCodes":{"type":"array","items":{"type":"string"}},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"entriesAllowed":{"type":"integer","nullable":true},"entriesConsumed":{"type":"integer"},"admissionRulesId":{"type":"string","format":"uuid"}}}},"blacklist":{"type":"array","items":{"type":"string"},"description":"Media codes to deny outright regardless of entitlement state."},"admissionRules":{"type":"array","items":{"type":"object","required":["id","openMinutesBefore","closeMinutesAfter"],"properties":{"id":{"type":"string","format":"uuid"},"openMinutesBefore":{"type":"integer"},"closeMinutesAfter":{"type":"integer"},"maxDurationMinutes":{"type":"integer","nullable":true},"requiresExitBeforeReentry":{"type":"boolean"}}}},"accreditationCredentials":{"type":"array","description":"Accreditation credentials that admit at this access point, from access.accreditation_credential (29 September, build; BL-181). Only rows that admit are included; a credential dropped from one package to the next no longer admits.","items":{"$ref":"#/components/schemas/AccessAccreditationCredential"}}}},
"OfflineScan": {"x-ticvai-persistence":"none — client-side journal","allOf":[{"$ref":"#/components/schemas/ValidateRequest"},{"type":"object","required":["sequence","localOutcome"],"properties":{"sequence":{"type":"integer","minimum":1,"description":"Monotonic per device. The server processes in this order."},"localOutcome":{"allOf":[{"$ref":"#/components/schemas/ScanOutcome"}],"description":"What the device decided offline. The server is authoritative and may disagree; disagreements are returned for reconciliation, not discarded.\n"},"localDenyReason":{"$ref":"#/components/schemas/DenyReason"},"overriddenByPrincipalId":{"type":"string","format":"uuid","nullable":true},"overrideReason":{"type":"string","nullable":true}}}]},
"Order": {"x-ticvai-persistence":"orders.sales_order + orders.order_line","type":"object","required":["id","venueId","scopePath","channel","status","currency","currencyScale","grossAmount","taxAmount","netAmount","lines","createdAt","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The client UUIDv7 from `CreateOrderRequest.id`."},"orderNumber":{"type":"string","readOnly":true,"description":"The number a guest reads and a cashier types. **Server-assigned: the venue prefix and a sequence per venue**, for example `DXB1-000123` (decided 28 September, audit R152). A till holds a reserved range of the venue sequence, so an order taken offline gets its number on the till and keeps it through `syncOrders`. **Not gapless**: an unused reserved range leaves a gap, and that is allowed. Only tax invoices are gapless, per legal entity. The receipt carries this number.\n"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for within a month of launch.\n"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"chargeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**The currency the guest selected and is charged in** (CHG-FIN-001, 2 October 2026). Null or equal to `currency` for a sale in the base currency. Everything else on the order, and every ledger posting, stays in the base currency `currency`."},"chargeFxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"readOnly":true,"description":"Units of `chargeCurrency` per one unit of the base currency, from the region's `tender` rate in force at checkout (`finance.FxRate`), stored on the order so the payment, the receipt, the tax invoice and any refund use the same rate (CHG-FIN-001)."},"chargeFxRateId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `finance.FxRate` row the rate was taken from, for audit."},"chargeTotal":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"`grossAmount` converted at `chargeFxRate` and rounded to the charge currency's scale: what the guest pays and what the payment request to the provider asks for (CHG-FIN-001)."},"chargeRateLockedUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"The quote holds until then (the cart lease). After it, the next payment attempt re-quotes at the rate then in force and the guest confirms the new amount (CHG-FIN-001)."},"droppedPromotions":{"type":"array","readOnly":true,"x-ticvai-persisted":false,"description":"**Promotions left off this order at checkout because their budget cap would have been exceeded** (decided 28 September, audit R101 (8)). Empty when none was dropped. Returned by `checkoutCart` and `createOrder`, not stored.\n","items":{"type":"object","required":["promotionId"],"properties":{"promotionId":{"type":"string","format":"uuid"},"name":{"type":"string"},"reason":{"type":"string","enum":["budgetCapReached"]}}}},"totalPriceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Sum across lines. Zero on a normal order."},"lines":{"type":"array","items":{"$ref":"#/components/schemas/OrderLine"}},"payments":{"type":"array","items":{"$ref":"#/components/schemas/Payment"}},"principalId":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid"},"shiftId":{"type":"string","format":"uuid","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"holdLabel":{"type":"string","maxLength":60,"nullable":true,"readOnly":true,"description":"The `label` a cashier gave when parking it with `holdOrder` — how they find it again. Null on an order never held."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When a held order expires and is voided (states/order.yaml), from `holdOrder`'s `holdUntil`. Null on an order not currently held."},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"OrderChannel": {"type":"string","description":"Where the order originated. Added when guest self-ordering was contracted — an order a guest placed on their own phone is commercially and operationally different from one a cashier typed, and reporting that cannot separate them cannot answer whether self-ordering is working.\n","enum":["pos","kiosk","guestApp","guestWeb","callCentre","partner","api","backOffice"]},
"OrderLine": {"x-ticvai-persistence":"orders.order_line + orders.order_line_eligibility + orders.order_line_discount","x-ticvai-retired-columns":["promotion_id","name","reason"],"allOf":[{"$ref":"#/components/schemas/CreateOrderLine"},{"type":"object","required":["serverUnitPrice","taxAmount","netAmount","grossAmount"],"properties":{"serverUnitPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the server computed on ingest."},"priceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Server minus quoted. Non-zero means the quoted price was honoured and the difference posted to the variance account.\n"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"entitlementIds":{"type":"array","description":"The entitlements this line issued. **These are the ticket ids** — `transferOrderTickets.ticketIds` and `reprintOrder.reissuedTicketIds` take and return them.","items":{"type":"string","format":"uuid"}},"crossRegionRightIds":{"type":"array","items":{"type":"string"},"description":"Redemption rights propagated to other cells for this line."},"reprintCount":{"type":"integer","minimum":0,"default":0,"readOnly":true,"description":"How many times this line's tickets were reprinted or resent. `reprintOrder` increments it; repeated reprints are the signal worth surfacing."},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"The order's venue, copied onto the line (ADR-0044's own example; system-design review SD-008, 29 September) so a line is scoped and partitionable without its order."},"discounts":{"type":"array","readOnly":true,"description":"**The discounts applied to this line, one row each** (system-design review SD-008, 29 September). Until then a discount object was flattened into the line as `promotion_id NOT NULL`, so a line with no promotion could not be inserted. A line with no discount has none.","items":{"$ref":"#/components/schemas/OrderLineDiscount"}}}}]},
"OrderStatement": {"x-ticvai-persistence":"none — computed from order, payment, refund and ledger","type":"object","required":["orderId","orderNumber","currency","entries","currentBalance"],"properties":{"orderId":{"type":"string","format":"uuid"},"orderNumber":{"type":"string"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"entries":{"type":"array","description":"Sequential. What an agent reads to a guest asking about a charge.","items":{"type":"object","required":["kind","amount","runningBalance","occurredAt"],"properties":{"kind":{"type":"string","enum":["sale","payment","refund","void","modification","exchange","fee","variance","chargeback"]},"description":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"runningBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"referenceId":{"type":"string","nullable":true},"principalId":{"type":"string","format":"uuid","nullable":true},"occurredAt":{"type":"string","format":"date-time"}}}},"totalPaid":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"totalRefunded":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"currentBalance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Positive means the guest owes; negative means a refund is outstanding."}}},
"OrderStatus": {"type":"string","enum":["pending","held","paid","partiallyPaid","completed","voided","refunded","partiallyRefunded","failed"],"description":"`held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed.\n"},
"OrderSummary": {"x-ticvai-persistence":"none — projection","type":"object","required":["id","orderNumber","status","grossAmount","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderNumber":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"The same vocabulary as `Order.channel`, which this projects."},"lineCount":{"type":"integer"},"principalId":{"type":"string","format":"uuid","description":"The cashier who raised it — what the held-orders list shows."},"holdLabel":{"type":"string","nullable":true,"description":"As `Order.holdLabel`."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"description":"As `Order.heldUntil`, so a held-orders list can warn about the ones about to lapse."},"createdAt":{"type":"string","format":"date-time"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Payment": {"x-ticvai-persistence":"orders.payment","type":"object","required":["id","orderId","tender","amount","status","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid"},"tender":{"$ref":"#/components/schemas/TenderKind"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","description":"4.6.11. **What the guest actually handed over**, which is not always what the venue books. A tourist paying USD cash at a till is a foreign tender; the sale is still recorded in base currency.\nEqual to the base currency for almost every payment. **Present on all of them so the foreign-tender report has a source** — `getForeignTenderReport` promised *what was taken in which currency* and nothing recorded it until 18 August.\n"},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"The amount in `tenderCurrency`, at that currency's own scale."},"fxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"description":"The rate applied, **stored on the payment rather than looked up later** (CF-37). A payment reconciled next month is reconciled at the rate of the day it was taken.\n"},"fxRateSource":{"type":"string","nullable":true,"enum":["manual","feed","cardScheme"],"description":"4.2.8. Manual or fed on a schedule. **`cardScheme` is where the terminal did the conversion and told us** — dynamic currency conversion, the scheme's rate rather than ours.\n"},"changeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"description":"4.6.11 is deliberately asymmetric: **accept foreign currency, refund in local.** A till giving change in five currencies needs five floats and five counts, and the variance becomes unattributable.\n**Cash at a till only** (CHG-FIN-001, 2 October 2026). A card or wallet payment the guest made in a currency they selected is refunded in that currency (`Refund.tenderCurrency`).\n"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"changeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["authorised","captured","pendingConfirmation","declined","failed","voided","refunded"]},"providerName":{"type":"string","nullable":true},"providerReference":{"type":"string","nullable":true,"description":"The provider's own id for the charge (Stripe PaymentIntent, NI order reference). What `payments.receivePaymentProviderWebhook` matches an incoming event on (SD-034)."},"providerIdempotencyKey":{"type":"string","nullable":true,"readOnly":true,"description":"The idempotency key sent to the provider, which is this payment's `id` (SD-034, 29 September). A retried provider call cannot charge twice."},"terminalId":{"type":"string","format":"uuid","nullable":true,"description":"The card terminal a till payment ran on (ECR flow, SD-034)."},"nextAction":{"type":"object","nullable":true,"x-ticvai-persisted":false,"description":"**What the caller does while the payment is `pendingConfirmation`** (SD-034, 29 September). `redirect`: send the browser to `url` (3-D Secure challenge or hosted page); the provider returns the guest to `returnUrl` and the result arrives by webhook. `terminal`: the card terminal has been instructed; wait for its result. Null once the payment has an outcome.","properties":{"kind":{"type":"string","enum":["redirect","terminal"]},"url":{"type":"string","format":"uri","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true}}},"lastInquiryAt":{"type":"string","format":"date-time","nullable":true},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"ProposedAction": {"type":"object","x-ticvai-persistence":"ai.proposed_action","required":["id","kind","targetContract","targetOperation","payload","status"],"properties":{"id":{"type":"string","format":"uuid"},"interactionId":{"type":"string","format":"uuid"},"translationJobId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `proposeTranslations` job that drafted this proposal; `getTranslationProposals` reads a job's rows by it. Null on every other proposal (CHG-RFM-004)."},"kind":{"type":"string","enum":["pricing","promotion","operational","financial","configuration","content","audience"],"description":"`content` (a marketing or storefront draft from `proposeMarketingContent`) and `audience` (a lookalike segment from `proposeLookalikeSegment`) added 29 September (build); both are applied by a person in the owning screen."},"targetContract":{"type":"string","description":"Which contract would perform it. The assistant never performs it itself."},"targetOperation":{"type":"string"},"payload":{"type":"object","additionalProperties":true,"description":"The request body a person would submit, ready to review. **Open on purpose: its shape is the request body of `targetOperation` in `targetContract`**, and it is validated against that operation, not restated here.\n"},"summary":{"type":"string"},"status":{"type":"string","description":"**Expiry (decided 28 September, audit R213)**: a `proposed` action expires 7 days after `proposedAt`; an `approved` action not applied expires 24 hours after `decidedAt`. Both are proposed values, client to correct, and `expiresAt` carries the one that applies.\n","enum":["proposed","approved","rejected","applied","expired"]},"expiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"When the expiry timer moves this action to `expired` — `proposedAt` plus 7 days while `proposed`, `decidedAt` plus 24 hours once `approved`, null once `rejected`, `applied` or `expired` (audit R213)."},"approvalLevel":{"type":"integer","minimum":1,"maximum":2,"description":"8.3.65. Multi-level, because a discount and a pricing change differ in authority. **Two levels (decided 28 September, audit R213)**: `2` for anything touching prices or permissions (every `pricing` and `promotion` action, and any other whose payload sets a price, a discount, a role or a permission grant), which needs a manager other than the requester; `1` for everything else, which the requester approves themselves.\n"},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"decisionReason":{"type":"string","nullable":true,"description":"Required on rejection. **The only signal the assistant is proposing badly**, and without it a poor model degrades silently.\n"},"proposedAt":{"type":"string","format":"date-time"},"decidedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","readOnly":true,"description":"**Added 29 September (AI design 3.1):** `ai.proposed_action` had no policy — its only references were nullable. The scope it was proposed at, and the partition key row-level security reads.\n"},"planId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.action_plan","description":"The plan this action presents for a decision (AI design 2.2 D, 3.8)."},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `approvals` request deciding a tier 2 or matrix-caught action (AI design 2.3)."},"changeSetHash":{"type":"string","nullable":true,"readOnly":true,"description":"Hash of the change set approved; execution refuses a plan whose hash differs (AIC-181)."}}},
"Refund": {"x-ticvai-persistence":"orders.refund","type":"object","required":["id","orderId","amount","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid"},"batchId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `RefundBatch` that raised this refund, where `createBulkRefund` did. Null for a refund raised on its own."},"fxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"readOnly":true,"description":"**The rate on the original payment, not today's** (BL-087, CF-118).\n`Payment` records `tenderCurrency`, `fxRate` and `fxRateSource` at the moment of sale, so the sale rate is always retrievable. **Refunding at today's rate repays a different amount of money than was taken** — a guest who paid 100 USD at 3.67 and is refunded at 3.72 gets back more AED than they gave, and the venue carries the difference on every refund.\nThe exposure runs both ways and neither direction is defensible: a guest short-changed by a moving rate has a complaint the venue cannot answer, because **the guest did nothing but wait.**\n"},"taxReversalEntryId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**A refund reverses the tax entry it created, and this is where that is stated rather than implied.** `reverseJournalEntry` and `calculateTax` both exist, so both halves were present and the obligation was assumed — **an implied obligation is one a developer can miss without failing anything.**\nNull only where the original sale carried no tax.\n"},"settleTo":{"type":"string","enum":["originalTender","advanceBalance","wireTransfer","storeCredit"],"default":"originalTender","description":"BL-086. **A refund could only go back the way it came.** A guest whose card has expired, a partner settling by wire, a guest who would rather have the credit — three real cases with one answer.\n**`originalTender` stays the default** because refunding elsewhere is how money laundering works, and anything else needs a reason.\n\n**`storeCredit` is a gift card issued for the refund amount** (decided 2 October 2026, Chinmay, batch 1, POS-011; DEC-061; CHG-CSP-037; DI-796), never a voucher or a wallet top-up.\n"},"fxVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Where the sale rate and the current rate differ, **the difference is booked as an FX variance rather than hidden in the refund**. `runFxRevaluation` already handles this class of movement and this is the same act at a smaller scale.\n"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**A refund goes back in the currency the guest paid** (decided 2 October 2026, Chinmay; CHG-FIN-001). For a card or wallet payment taken in a guest-selected currency, the refund request to the provider is in that currency, and `tenderAmount` is the refunded share of the original `Payment.tenderAmount` at the sale rate (`fxRate`), so a full refund returns exactly what was charged. `amount` stays in base currency for the ledger. Null for a refund in the base currency. Foreign cash refunded at a till is paid in base currency (DI-282)."},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"The refund in `tenderCurrency`, at that currency's own scale (CHG-FIN-001)."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"appliedPercentage":{"type":"number","description":"From the venue's time bands, or an approver override."},"status":{"type":"string","enum":["pendingApproval","pendingGateway","completed","declined","failed"]},"reason":{"type":"string"},"requestedByPrincipalId":{"type":"string","format":"uuid"},"secondaryPrincipalId":{"type":"string","format":"uuid","nullable":true},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"ledgerEntryId":{"type":"string","format":"uuid","nullable":true,"description":"Written before the gateway is called."},"gatewayReference":{"type":"string","nullable":true},"createdAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true}}},
"ReportResult": {"x-ticvai-persistence":"none — result set, cached in object storage","type":"object","required":["executionId","columns","rows"],"properties":{"executionId":{"type":"string"},"columns":{"type":"array","items":{"type":"object","properties":{"key":{"type":"string"},"label":{"type":"string"},"type":{"$ref":"#/components/schemas/FieldType"}}}},"rows":{"type":"array","description":"**Open on purpose; the shape is `columns`.** Each row is keyed by `columns[].key`, and each value is of that column's `type` — money as a `Money`, dates, date-times and uuids as strings. A report's columns are chosen at run time, so no fixed schema can name them.\n","items":{"type":"object","additionalProperties":true}},"totals":{"type":"object","additionalProperties":true,"description":"Aggregated columns only, keyed and typed as a row is."},"rowCount":{"type":"integer"},"nextCursor":{"type":"string","nullable":true},"generatedAt":{"type":"string","format":"date-time"},"dataAsOf":{"type":"string","format":"date-time","description":"Replica position the result was read at. Reporting reads a lag-tolerant replica, so this may trail the primary by seconds — stating it prevents an argument about a figure that moved.\n"}}},
"ReportingAnswerReliability": {"type":"string","description":"**How far an analytics answer can be relied on** (decided 29 September, AI system design 5.6): a category, never a bare percentage. `grounded`: every figure comes from a result of the compiled spec. `partial`: part of the question was answered and the rest was not modelled. `conflictingSources`: the result and a cited source disagree. `insufficientEvidence`: the question could not be answered, including \"not available yet\" outside the semantic model. The same four values as `ai.yaml`'s assistant answers.\n","enum":["grounded","partial","conflictingSources","insufficientEvidence"]},
"ReportingSemanticQuerySpec": {"x-ticvai-persistence":"none — embedded; stored whole in `reporting.natural_language_query`","type":"object","description":"**A question in the semantic model's own vocabulary** (decided 29 September, AI system design 2.2 E and 5.7). What the model returns for a live-number question instead of SQL, and what `runSemanticQuery` takes. Every code is a `SemanticModel` field code or a KPI code; Reporting validates the spec against the published model and compiles it deterministically, so the same spec compiles to the same SQL for the same model version.\n","required":["metric","period"],"properties":{"metric":{"type":"string","description":"A measure field code in the `SemanticModel`, or a `KpiDefinition.code`. The governed definition the dashboards use, so the number matches them."},"dimensions":{"type":"array","maxItems":5,"description":"Field codes to group by. Each must be reachable from the metric's dataset through a relationship the semantic model declares.","items":{"type":"string"}},"filters":{"type":"array","items":{"type":"object","required":["field","operator"],"properties":{"field":{"type":"string","description":"A `SemanticModel` field code."},"operator":{"type":"string","enum":["equals","notEquals","greaterThan","lessThan","between","in","notIn","isNull","isNotNull"]},"values":{"type":"array","description":"**Open on purpose; typed by the field.** One value for the comparison operators, exactly two (from, to) for `between`, any number for `in` and `notIn`, none for `isNull` and `isNotNull`.\n","items":{}}}}},"period":{"type":"string","description":"ISO 8601 interval in the venue's time zone, e.g. `2026-09-21/2026-09-27`, the form `explainMetricChange` takes."},"comparison":{"type":"string","nullable":true,"description":"As `getKpiValues` `compareTo`. With one, each row carries the metric for the comparison beside the current value.","enum":["previousPeriod","samePeriodLastYear","target","benchmark"]},"semanticModelVersion":{"type":"integer","readOnly":true,"description":"The `SemanticModel.version` the spec was validated and compiled against. Set by Reporting."}}},
"ReportingUnavailableReason": {"type":"string","description":"Which part of a question is outside the semantic model, so the answer is \"not available yet\" (design 5.7). A metric or field the caller may not see is reported as not modelled, so the reason does not reveal that it exists.","enum":["metricNotModelled","dimensionNotModelled","filterNotModelled","comparisonNotAvailable","periodOutsideHistory"]},
"RotaAssignment": {"type":"object","x-ticvai-persistence":"workforce.rota_assignment","required":["principalId","venueId","startsAt","endsAt","position"],"properties":{"overtimeMinutes":{"type":"integer","nullable":true,"readOnly":true,"description":"BL-044, 1.2.83. **UAE labour law limits working hours and mandates rest periods**, and nothing in the package counted either. Derived from attendance against the shift.\n"},"restPeriodBefore":{"type":"integer","nullable":true,"description":"Minutes since the previous shift ended. **The check that stops a closing shift followed by an opening one**, which is legal in most places and unsafe in all of them.\n"},"breachesWorkingHourLimit":{"type":"boolean","default":false,"readOnly":true,"description":"**Flagged at assignment, not discovered at payroll.** A rota that breaches a statutory limit is a rota somebody has to redo, and finding out a month later means it was worked.\n"},"labourCost":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"**Cost at the point of scheduling.** A manager building a rota without seeing its cost is a manager who finds out from finance.\n"},"id":{"type":"string","format":"uuid","readOnly":true},"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string","readOnly":true},"venueId":{"type":"string","format":"uuid"},"departmentId":{"type":"string","format":"uuid","nullable":true},"position":{"type":"string","description":"What they are rostered to do — gate steward, cashier, lifeguard, technician. **Most positions never touch a till**, which is why a rota assignment is not a shift.\n**A position code, not a label.** It is the same value as `StaffingRules.minimumCover[].positionCode`, `OpenShift.positionCode` and `StaffingCoverage.positionCode`: coverage counts rostered people per position, so an assignment spelled differently from the rule it fills is counted against nothing and the gap stays open. Tenant-defined, which is why it is not an enum here.\n"},"requiredRoleId":{"type":"string","format":"uuid","nullable":true,"description":"Checked on assignment. A rota naming someone unqualified is a rota that gets overridden."},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"Where the position needs a till. **The link between a rota and a cash session**, without merging the two.\n"},"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time"},"status":{"$ref":"#/components/schemas/RotaStatus"},"breakMinutes":{"type":"integer","nullable":true},"note":{"type":"string","nullable":true}}},
"RotaStatus": {"type":"string","enum":["planned","published","confirmed","swapPending","cancelled","completed","noShow"]},
"ScanEvent": {"x-ticvai-append-only":"recordedAt","x-ticvai-persistence":"access.scan_event","type":"object","required":["id","accessPointId","venueId","outcome","direction","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The scan's client-generated UUIDv7, the key offline replay deduplicates on."},"accessPointId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"ticketId":{"type":"string","format":"uuid","nullable":true,"description":"The `Entitlement.id` scanned; null where the media resolved to nothing."},"mediaCode":{"type":"string","nullable":true},"outcome":{"$ref":"#/components/schemas/ScanOutcome"},"denyReason":{"$ref":"#/components/schemas/DenyReason"},"direction":{"$ref":"#/components/schemas/Direction"},"operatorPrincipalId":{"type":"string","format":"uuid","nullable":true},"deviceId":{"type":"string","format":"uuid","nullable":true},"overridesScanId":{"type":"string","format":"uuid","nullable":true,"description":"**Set only on an override row**, naming the denied scan it admits against (decided 28 September, audit R228). The denied scan itself is never updated: the denial and the override are two rows, and at most one override row names any scan. Null on every other scan.\n"},"overrideReason":{"type":"string","nullable":true,"description":"The supervisor's justification, on the override row only. The overriding principal is that row's `operatorPrincipalId`."},"dynamicPolicyId":{"type":"string","format":"uuid","nullable":true,"description":"The dynamic access policy (`access.dynamic_policy`) whose result decided this scan; null when no dynamic policy matched and the entitlement alone decided (added 29 September, build pass, 3.3.48). `listDynamicPolicyEffectiveness` counts from it."},"dynamicPolicyVersion":{"type":"integer","minimum":1,"nullable":true,"description":"The version of that policy in force at the scan, so a report spanning a change counts each version apart."},"dynamicPolicyResult":{"type":"string","enum":["allow","deny","review","requireId","requireBiometric","requireCompanion","requireSupervisor"],"nullable":true,"description":"What the policy decided, which for a step-up is not the same as the scan's outcome."},"quantity":{"type":"integer","minimum":1,"default":1,"description":"Admissions this scan counted. More than one only for a group wave (`validateGroupAccess`) or a quantity entitlement consumed in one pass (added 29 September, data-model close-out DM1)."},"localSequence":{"type":"integer","nullable":true,"description":"The device-local sequence number of a scan recorded offline; null for an online scan (added 29 September, data-model close-out DM1)."},"policySetVersion":{"type":"string","nullable":true,"description":"The admission policy set the scan was decided under (`OfflinePackage.policySetVersion`, or the same fingerprint computed online by `validateAccess`), beside the one policy and version that decided it (`dynamicPolicyId`, `dynamicPolicyVersion`). ADR-0068, 1 October."},"packageVersion":{"type":"string","nullable":true,"description":"The offline package (`access.edge_package`) the device validated against; null for an online scan (added 29 September, data-model close-out DM1)."},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true,"description":"Null while pending. Differs from recordedAt for offline scans."}}},
"ScanOutcome": {"type":"string","enum":["admitted","denied","overridden"]},
"ScanSyncResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["accepted","results"],"properties":{"accepted":{"type":"integer","description":"Entries processed before any stop."},"stoppedAtSequence":{"type":"integer","nullable":true,"description":"Sequence of the first entry that could not be processed. Null when the whole batch succeeded. The client retries from here — never past it.\n"},"results":{"type":"array","items":{"type":"object","required":["id","sequence","status"],"properties":{"id":{"type":"string"},"sequence":{"type":"integer"},"status":{"type":"string","enum":["accepted","duplicate","reconciled","rejected"]},"serverOutcome":{"$ref":"#/components/schemas/ScanOutcome"},"divergence":{"type":"string","nullable":true,"description":"Present when `reconciled` — the device admitted and the server would have denied, or vice versa. Surfaced to the operator, not swallowed.\n"},"error":{"$ref":"../shared/common.yaml#/components/schemas/Problem"}}}}}},
"ShiftSwap": {"type":"object","x-ticvai-persistence":"workforce.shift_swap","required":["id","assignmentId","fromPrincipalId","toPrincipalId","status"],"properties":{"id":{"type":"string","format":"uuid"},"assignmentId":{"type":"string","format":"uuid"},"fromPrincipalId":{"type":"string","format":"uuid"},"toPrincipalId":{"type":"string","format":"uuid"},"status":{"type":"string","enum":["awaitingPeer","awaitingApproval","approved","rejected","withdrawn"],"description":"**Both parties before the supervisor.** A swap approved against someone who never agreed is a gap in the rota nobody notices until the shift starts.\n"},"approvalRequestId":{"type":"string","nullable":true,"description":"Routed through `approvals` rather than a second mechanism here."},"reason":{"type":"string","nullable":true},"requestedAt":{"type":"string","format":"date-time"}}},
"SyncRejection": {"x-ticvai-persistence":"sync.rejection","type":"object","required":["id","workstationId","kind","rejectedAt","problem"],"properties":{"id":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["order","payment","refund","void","scan"]},"recordedAt":{"type":"string","format":"date-time"},"rejectedAt":{"type":"string","format":"date-time"},"problem":{"$ref":"../shared/common.yaml#/components/schemas/Problem"},"payload":{"type":"object","additionalProperties":true,"description":"**Deliberately open: the journal entry exactly as the till sent it.** Its shape is the request schema for `kind` — an `OfflineOrder` for `order`, a `CreatePaymentRequest` for `payment` — kept verbatim so the supervisor resolves what was actually recorded, not a re-typed copy.\n"},"resolvedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"resolvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"resolution":{"type":"string","nullable":true,"readOnly":true,"enum":["posted","voided","refunded"],"description":"What `resolveSyncRejection` recorded. Null while the rejection waits."},"resolvedRecordId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The order, void or refund the resolution produced — what stops the entry being posted twice."}}},
"TicketStatus": {"x-ticvai-persistence":"none — computed from entitlement and scans","description":"**A validation result, not a lifecycle**, despite the name. Computed at scan time from the entitlement and its scan history — `isValid`, `entriesUsed`, `isInsideVenue`.\n**The name misled a state model into anchoring on it** (`states/entitlement.yaml`, removed 18 August): six lifecycle states were checked against an object with no values, and `check-states` warned about it for a day before anyone read the schema.\nThe entitlement's lifecycle is `orders.EntitlementStatus`. **This is what a gate learns when it scans**, which is a different question with a similar name.\n","type":"object","required":["ticketId","isValid"],"properties":{"ticketId":{"type":"string","format":"uuid","description":"Stable for the life of the ticket, independent of the media carrying it."},"mediaCode":{"type":"string","nullable":true},"productName":{"type":"string"},"holderName":{"type":"string","nullable":true,"description":"Present only where the entitlement is name-bound. Identity and entitlement are separate concerns; most entitlements carry no holder.\n"},"isValid":{"type":"boolean"},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true},"performanceId":{"type":"string","format":"uuid","nullable":true},"entriesUsed":{"type":"integer"},"entriesAllowed":{"type":"integer","nullable":true,"description":"Null means unlimited."},"reentryAllowed":{"type":"boolean"},"isInsideVenue":{"type":"boolean","description":"Derived from the last scan. Drives anti-passback evaluation."},"issuingCellId":{"type":"string","nullable":true,"description":"Present when this entitlement was issued in a different cell and is being redeemed here as a delegated right (ADR-0010). Null for locally issued tickets.\n"},"guestLinkId":{"type":"string","nullable":true,"description":"Pseudonymous cross-region guest reference. Present only on delegated rights. Carries no personal data.\n"},"admissionRulesId":{"type":"string","format":"uuid"},"denyReason":{"$ref":"#/components/schemas/DenyReason"}}},
"ValidateRequest": {"type":"object","required":["id","mediaCode","mediaKind","direction","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7. Also the idempotency key and dedupe key."},"mediaCode":{"type":"string","maxLength":256,"description":"What was read from the media. NOT the ticket id — media can be re-linked over a ticket's life.\n"},"mediaKind":{"$ref":"#/components/schemas/MediaKind"},"direction":{"$ref":"#/components/schemas/Direction"},"groupSize":{"type":"integer","minimum":1,"description":"For group media admitting several holders on one read."},"proximityToken":{"type":"string","description":"BLE proximity assertion where the venue requires the operator to be physically at the gate. Absent where not configured.\n"},"recordedAt":{"type":"string","format":"date-time","description":"Device time of the read. Authoritative for ordering, not for validity."}}},
"ValidationResult": {"x-ticvai-persistence":"none — computed, persisted as scan_event","type":"object","required":["scanId","outcome","accessPointId","recordedAt"],"properties":{"scanId":{"type":"string","format":"uuid"},"outcome":{"$ref":"#/components/schemas/ScanOutcome"},"denyReason":{"$ref":"#/components/schemas/DenyReason"},"denyDetail":{"type":"string","description":"Human-readable, localised. For operator display, never for logic."},"denyCause":{"type":"string","nullable":true,"enum":["attractionTemporarilyClosed","timeBoundWindowElapsed","offlineLimitExceeded"],"description":"**The finer cause of three denials decided on 2 October 2026**, beside the r1 `denyReason` a client already switches on (a new `DenyReason` value would be a breaking change against r1; CHG-CSP-026, CHG-CSP-030, CHG-CSP-035). `attractionTemporarilyClosed` (DEC-228): `denyReason` `outsideAdmissionWindow`, with `reopensAt` and `queueReturnOffer`. `timeBoundWindowElapsed` (DEC-232): a time-bound entitlement scanned after its window from first scan, `denyReason` `expired`. `offlineLimitExceeded` (DEC-426): a reader offline longer than the venue's `AccessOfflinePolicy.maxOfflineDurationHours` refusing a tap it cannot check, `denyReason` `outsideAdmissionWindow`. Null for every other denial."},"reopensAt":{"type":"string","format":"date-time","nullable":true,"description":"When a temporarily closed attraction expects to reopen, where known (DEC-228; CHG-CSP-026)."},"queueReturnOffer":{"type":"object","nullable":true,"description":"A virtual-queue return window offered at a denied scan of a temporarily closed attraction, where the venue enables it (DEC-228; CHG-CSP-026). Taking it is `queue.joinQueue`.","properties":{"queueId":{"type":"string","format":"uuid"},"returnWindowStart":{"type":"string","format":"date-time"},"returnWindowEnd":{"type":"string","format":"date-time"}}},"accessPointId":{"type":"string","format":"uuid"},"ticket":{"$ref":"#/components/schemas/TicketStatus"},"admittedCount":{"type":"integer","description":"Holders admitted on this read. Differs from groupSize on partial admission."},"recordedAt":{"type":"string","format":"date-time"},"serverEvaluatedAt":{"type":"string","format":"date-time"},"advisory":{"type":"object","nullable":true,"description":"BL-179, CF-130. **What a device observed, for the steward, never for the gate.** Present only where an access point's device reports the matching `DeviceCapability` and the venue has turned the corresponding setting on.\n**Never persisted.** This schema is computed and stored as `access.scan_event`, and the advisory is deliberately not part of what is stored: an inferred classification kept against a guest is sensitive personal data with no consent behind it. **A guest agreed to be admitted, not to be classified** — Face Pass and Face Tag carry `consent_purpose_id` and `consent_given_at` because somebody enrolled, and nobody enrols in being looked at by a turnstile. `scan_event` records that an override happened and never what the device thought, which keeps `overrideRateAlertThreshold` working without building a register nobody agreed to.\n**It cannot reach `outcome` or `denyReason`.** Those are decisive and `entitlementGated` is `true` and read-only: the gate admits on the entitlement, and everything here sits on top of that without replacing any of it.\n","properties":{"genderClassification":{"type":"string","enum":["women","men","undetermined"],"description":"**`undetermined` is a real answer and the most common one to design for.** A classifier that never returns it is one that has been tuned to look confident.\n"},"confidence":{"type":"number","minimum":0,"maximum":1,"description":"**Required reading for the steward, not decoration.** An advisory with no confidence is read as a fact, and `overrideRateAlertThreshold` exists to catch exactly the failure that produces — *an override rate near zero means the steward has stopped deciding.* That number only means anything if the steward could see how sure the device was.\n"},"reportedByDeviceId":{"type":"string","format":"uuid","description":"**Which device said it.** A classifier that degrades is one camera, not a venue, and an advisory nobody can trace to hardware cannot be investigated or switched off alone.\n"}}}}}
}
```
