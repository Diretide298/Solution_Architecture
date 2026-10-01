# WS23 — B2B, Reseller & OTA Partner Management board 3

**10 screens · 0 operations · 0 schemas · 0 permissions**

Platform P10 Partner Web · ships as **ticvai-control** ·
partner audience · web ·
online only

## Who this is for

**partner on web.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 0 permissions apply here:
  ``. A control nobody can use must say so,
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

## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `PTR-042` | Partner Operations Command Center | B–D | 2 | 28 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `PTR-043` | Partner Orders & Booking Management | B–D | 2 | 32 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `PTR-044` | Reservations, Holds & Release Management | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `PTR-045` | Partner Cancellations, Refunds & Amendments | B–D | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `PTR-046` | Partner Statement & Account Activity | B–D | 0 | 18 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `PTR-047` | Partner Reconciliation & Exception Management | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `PTR-048` | Commission Calculation & Settlement Management | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `PTR-049` | Partner Disputes, Cases & Service Management | B–D | 0 | 8 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `PTR-050` | Partner Performance Scorecard & Risk Monitoring | B–D | 0 | 2 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `PTR-051` | Partner AI Intelligence & Relationship Optimization | B–D | 0 | 2 | 6 | 0 | 1 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**PTR-045, PTR-050, PTR-051 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `PTR-042` Partner Operations Command Center

**Provide commercial, operations and finance teams with one real-time view of active B2B, reseller and OTA business.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner; in the flows as partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each partner should show) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/partners/partner-operations-command-center-ptr-042` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search partner operations | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by partner, partner type, venue, event, market, account manager and 4 more — which are present is a decision the pack already made. | — |

#### Outputs: what the screen shows and produces

**Shown**

**Partner Sales Today** (metric tile)

**Partner Sales MTD** (metric tile)

**Active Partner Orders** (metric tile)

**Active Reservations/Holds** (metric tile)

**Tickets Sold** (metric tile)

**Cancellations** (metric tile)

**Refunds** (metric tile)

**Outstanding Receivables** (metric tile)

**Commission Payable** (metric tile)

**Pending Settlements** (metric tile)

**Operational Exceptions** (metric tile)

**Partners Requiring Attention** (metric tile)

**Every partner operations** (data table, from `listPartner2`)

| Shows | Format | Notes |
|---|---|---|
| Partner | text | not in the schema: `PartnerOperationsCommandCenterView.partner` |
| Partner type | text | not in the schema: `PartnerOperationsCommandCenterView.partnerType` |
| Account manager | text | not in the schema: `PartnerOperationsCommandCenterView.accountManager` |
| Orders | text | not in the schema: `PartnerOperationsCommandCenterView.orders` |
| Tickets | text | not in the schema: `PartnerOperationsCommandCenterView.tickets` |
| Gross sales | text | not in the schema: `PartnerOperationsCommandCenterView.grossSales` |
| Net sales | text | not in the schema: `PartnerOperationsCommandCenterView.netSales` |
| Commission | text | not in the schema: `PartnerOperationsCommandCenterView.commission` |
| Outstanding balance | text | not in the schema: `PartnerOperationsCommandCenterView.outstandingBalance` |
| Credit utilization | text | not in the schema: `PartnerOperationsCommandCenterView.creditUtilization` |
| Allocation utilization | text | not in the schema: `PartnerOperationsCommandCenterView.allocationUtilization` |
| Cancellation rate | text | not in the schema: `PartnerOperationsCommandCenterView.cancellationRate` |
| Operational status | text | not in the schema: `PartnerOperationsCommandCenterView.operationalStatus` |
| Risk | text | not in the schema: `PartnerOperationsCommandCenterView.risk` |

**The selected partner operations** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Partner | text | not in the schema: `PartnerOperationsCommandCenterView.partner` |
| Partner type | text | not in the schema: `PartnerOperationsCommandCenterView.partnerType` |
| Account manager | text | not in the schema: `PartnerOperationsCommandCenterView.accountManager` |
| Orders | text | not in the schema: `PartnerOperationsCommandCenterView.orders` |
| Tickets | text | not in the schema: `PartnerOperationsCommandCenterView.tickets` |
| Gross sales | text | not in the schema: `PartnerOperationsCommandCenterView.grossSales` |
| Net sales | text | not in the schema: `PartnerOperationsCommandCenterView.netSales` |
| Commission | text | not in the schema: `PartnerOperationsCommandCenterView.commission` |
| Outstanding balance | text | not in the schema: `PartnerOperationsCommandCenterView.outstandingBalance` |
| Credit utilization | text | not in the schema: `PartnerOperationsCommandCenterView.creditUtilization` |
| Allocation utilization | text | not in the schema: `PartnerOperationsCommandCenterView.allocationUtilization` |
| Cancellation rate | text | not in the schema: `PartnerOperationsCommandCenterView.cancellationRate` |
| Operational status | text | not in the schema: `PartnerOperationsCommandCenterView.operationalStatus` |
| Risk | text | not in the schema: `PartnerOperationsCommandCenterView.risk` |

**Data it reads**: `listPartner2` (onLoad, Partner Operations Command Center); `listPartner` (onLoad, Partner Management Command Center)

**Where the user goes next**

- → `PTR-043` Partner Orders & Booking Management: *Works in Partner Orders & Booking Management*; calls `listPartner2`
- → `PTR-044` Reservations, Holds & Release Management: *Works in Reservations, Holds & Release Management*; calls `listPartner2`
- → `PTR-045` Partner Cancellations, Refunds & Amendments: *Works in Partner Cancellations, Refunds & Amendments*; calls `listPartner2`
- → `PTR-046` Partner Statement & Account Activity: *Works in Partner Statement & Account Activity*; calls `listPartner2`
- → `PTR-047` Partner Reconciliation & Exception Management: *Works in Partner Reconciliation & Exception Management*; calls `listPartner2`
- → `PTR-048` Commission Calculation & Settlement Management: *Works in Commission Calculation & Settlement Management*; calls `listPartner2`
- → `PTR-049` Partner Disputes, Cases & Service Management: *Works in Partner Disputes, Cases & Service Management*; calls `listPartner2`
- → `PTR-050` Partner Performance Scorecard & Risk Monitoring: *Works in Partner Performance Scorecard & Risk Monitoring*; calls `listPartner2`
- → `PTR-051` Partner AI Intelligence & Relationship Optimization: *Works in Partner AI Intelligence & Relationship Optimization*; calls `listPartner2`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The partner operations list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partner operations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No partner operations yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the partner operations are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Operations dashboard per partner: order volume, revenue, reservations and tickets on hold (booked but not yet issued). Cancellations/refund requests, statement of account (opening/closing balance, activity), reconciliation exceptions and disputes are tracked from this view. *(client request · MoM 31 Aug 2026, 4.5 B2B Day-to-Day Operations & Settlement · DI-557)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-042` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS40 B2B, Reseller & OTA Partner Management Board 3.dc.html#ptr-042`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 3
- Flow F132 *B2B, Reseller & OTA Partner Management board 3: Partner Operations Command …*, step 1: Opens Partner Operations Command Center → Provide commercial, operations and finance teams with one real-time view of active B2B, reseller and OTA business.
- Flow F132 *B2B, Reseller & OTA Partner Management board 3: Partner Operations Command …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F132 *B2B, Reseller & OTA Partner Management board 3: Partner Operations Command …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F132 *B2B, Reseller & OTA Partner Management board 3: Partner Operations Command …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F132 *B2B, Reseller & OTA Partner Management board 3: Partner Operations Command …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F132 *B2B, Reseller & OTA Partner Management board 3: Partner Operations Command …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F132 *B2B, Reseller & OTA Partner Management board 3: Partner Operations Command …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F132 *B2B, Reseller & OTA Partner Management board 3: Partner Operations Command …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F132 branch at step 1 (expected): when Nothing has been set up on Partner Operations Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F132 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (28 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-042?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `PTR-043`, `PTR-044`, `PTR-045`, `PTR-046`, `PTR-047`, `PTR-048`, `PTR-049`, `PTR-050`, `PTR-051`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-043` Partner Orders & Booking Management

**Provide a consolidated operational view of orders created by each partner.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner; in the flows as partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/partners/partner-orders-booking-management-ptr-043` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search partner orders booking | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by partner, partner order reference, ticvai order id, event, venue, product and 5 more — which are present is a decision the pack already made. | — |

#### Outputs: what the screen shows and produces

**Shown**

**Every partner orders booking** (data table, from `listPartnerOrderBooking`)

| Shows | Format | Notes |
|---|---|---|
| TICVAI order ID | text | not in the schema: `TICVAI Order ID` |
| Partner reference | text | not in the schema: `PartnerOrdersBookingManagementView.partnerReference` |
| Partner | text | not in the schema: `Partner` |
| Agent user | text | not in the schema: `PartnerOrdersBookingManagementView.agentUser` |
| Customer name | text | not in the schema: `PartnerOrdersBookingManagementView.customerName` |
| Booking date | text | not in the schema: `Booking Date` |
| Event | text | not in the schema: `Event` |
| Products | text | not in the schema: `PartnerOrdersBookingManagementView.products` |
| Quantity | text | not in the schema: `PartnerOrdersBookingManagementView.quantity` |
| Gross value | text | not in the schema: `PartnerOrdersBookingManagementView.grossValue` |
| Partner rate | text | not in the schema: `PartnerOrdersBookingManagementView.partnerRate` |
| Commission | text | not in the schema: `PartnerOrdersBookingManagementView.commission` |
| Net amount | text | not in the schema: `PartnerOrdersBookingManagementView.netAmount` |
| Payment method | text | not in the schema: `PartnerOrdersBookingManagementView.paymentMethod` |
| Billing status | text | not in the schema: `PartnerOrdersBookingManagementView.billingStatus` |
| Fulfillment status | text | not in the schema: `PartnerOrdersBookingManagementView.fulfillmentStatus` |

**The selected partner orders booking** (detail panel): The pack groups this record's detail under its own headings: “Important Architecture”.

| Shows | Format | Notes |
|---|---|---|
| TICVAI order ID | text | not in the schema: `TICVAI Order ID` |
| Partner reference | text | not in the schema: `PartnerOrdersBookingManagementView.partnerReference` |
| Partner | text | not in the schema: `Partner` |
| Agent user | text | not in the schema: `PartnerOrdersBookingManagementView.agentUser` |
| Customer name | text | not in the schema: `PartnerOrdersBookingManagementView.customerName` |
| Booking date | text | not in the schema: `Booking Date` |
| Event | text | not in the schema: `Event` |
| Products | text | not in the schema: `PartnerOrdersBookingManagementView.products` |
| Quantity | text | not in the schema: `PartnerOrdersBookingManagementView.quantity` |
| Gross value | text | not in the schema: `PartnerOrdersBookingManagementView.grossValue` |
| Partner rate | text | not in the schema: `PartnerOrdersBookingManagementView.partnerRate` |
| Commission | text | not in the schema: `PartnerOrdersBookingManagementView.commission` |
| Net amount | text | not in the schema: `PartnerOrdersBookingManagementView.netAmount` |
| Payment method | text | not in the schema: `PartnerOrdersBookingManagementView.paymentMethod` |
| Billing status | text | not in the schema: `PartnerOrdersBookingManagementView.billingStatus` |
| Fulfillment status | text | not in the schema: `PartnerOrdersBookingManagementView.fulfillmentStatus` |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** View, Modify, Cancel, Rebook, Resend Tickets, Reissue, Add Internal Note, Escalate, Open Financial Record. Each needs attaching to the control it gates, or the screen needs the control.

**Data it reads**: `listPartnerOrderBooking` (onLoad, Partner Orders & Booking Management)

**Where the user goes next**

- → `PTR-042` Partner Operations Command Center: *Returns to the board's landing screen*; calls `listPartnerOrderBooking`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The partner orders booking list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partner orders booking untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No partner orders booking yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the partner orders booking are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- For partners not integrating by API, TICVAI can issue a bulk batch of pre-generated tickets (QR codes, agreed rates, defined validity) as a CSV export for the partner to import and resell. *(agreed · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-553)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker · keyword 'ticket-booking ux')*
- **A46** Evaluate a dynamic bundle/package builder that auto-applies a discount when a guest adds multiple product types (ticket + F&B + retail) to cart, in addition to pre-defined packages *(Reshma Bandiwdekar · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'cart')*
- **A96** Build the journey library (abandoned cart with min-value/product filters, birthday, anniversary, cross-sell, survey — all consent-gated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'cart')*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'b2c checkout')*
- **A157** Keep F&B and retail online sale entirely within the platform (browse, cart, checkout, pickup or ship) with no redirect to a separate app *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 26 Aug 2026 · workshop tracker · keyword 'cart')*
- **A158** Obtain the resource-management reference documentation, review the hardware/ticketing docs, route follow-up questions to Qossai, and review the House of Wisdom booking flow as a UX reference *(Allam / Chinmay Parab / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 26 Aug 2026 · workshop tracker · keyword 'booking flow')*

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-043` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS40 B2B, Reseller & OTA Partner Management Board 3.dc.html#ptr-043`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 3
- Flow F132 *B2B, Reseller & OTA Partner Management board 3: Partner Operations Command …*, step 2: Works in Partner Orders & Booking Management → Provide a consolidated operational view of orders created by each partner.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (32 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-043?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `PTR-042`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-044` Reservations, Holds & Release Management

**Manage inventory temporarily reserved by B2B partners before final confirmation. This is particularly important for tour operators, corporate groups and travel-trade partners.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner; in the flows as partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/partners/reservations-holds-release-management-ptr-044` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Active Holds** (metric tile, from `listReservationHoldRelease`)

**Held Tickets** (metric tile, from `listReservationHoldRelease`)

**Held Value** (metric tile, from `listReservationHoldRelease`)

**Expiring Today** (metric tile, from `listReservationHoldRelease`)

**Expired Holds** (metric tile, from `listReservationHoldRelease`)

**Converted Holds** (metric tile, from `listReservationHoldRelease`)

**Released Inventory, tickets** (metric tile, from `listReservationHoldRelease`)

**Every reservations holds release** (data table, from `listReservationHoldRelease`)

**The selected reservations holds release** (detail panel): The pack groups this record's detail under its own headings: “When a hold expires”.

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Extend Hold, Reduce Hold, Release Hold, Convert to Booking, Reassign where permitted, Escalate. Each needs attaching to the control it gates, or the screen needs the control.

**Data it reads**: `listReservationHoldRelease` (onLoad, Reservations, Holds & Release Management)

**Where the user goes next**

- → `PTR-042` Partner Operations Command Center: *Returns to the board's landing screen*; calls `listReservationHoldRelease`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reservations holds release list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reservations holds release untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reservations holds release yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the reservations holds release are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-044` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS40 B2B, Reseller & OTA Partner Management Board 3.dc.html#ptr-044`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 3
- Flow F132 *B2B, Reseller & OTA Partner Management board 3: Partner Operations Command …*, step 4: Works in Reservations, Holds & Release Management → Manage inventory temporarily reserved by B2B partners before final confirmation. This is particularly important for tour operators, corporate groups and travel-trade partners.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-044?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `PTR-042`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-045` Partner Cancellations, Refunds & Amendments

**Manage post-booking changes according to the partner's commercial agreement and product policies.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner; in the flows as partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/partners/partner-cancellations-refunds-amendments-ptr-045` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Form: Create partner change request** (modal, opened by *Create partner change request*; *Create partner change request* calls `createPartnerChangeRequest`, *Cancel* sends nothing)

**Collects what `createPartnerChangeRequest` sends before it is called.** Required: `orderId`, `requestType`. Optional: `quantity`, `targetPerformanceId`, `targetProductId`, `newCustomerName`, `feeWaiverRequested`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

`createPartnerChangeRequest` is not in any contract: draw the form greyed and list it in FINDINGS.md.

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create partner change request (primary button) | `createPartnerChangeRequest` (not in any contract) | — | — | — | — |

**Data it reads**: `listPartnerCancellationRefund` (onLoad, Partner Cancellations, Refunds & Amendments)

**Where the user goes next**

- → `PTR-042` Partner Operations Command Center: *Returns to the board's landing screen*; calls `listPartnerCancellationRefund`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The partner cancellations refunds list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partner cancellations refunds untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No partner cancellations refunds yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the partner cancellations refunds are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Operations dashboard per partner: order volume, revenue, reservations and tickets on hold (booked but not yet issued). Cancellations/refund requests, statement of account (opening/closing balance, activity), reconciliation exceptions and disputes are tracked from this view. *(client request · MoM 31 Aug 2026, 4.5 B2B Day-to-Day Operations & Settlement · DI-557)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A75** Design the refund engine: a six-step ledger-to-gateway refund flow with configurable time-banded percentages, an authorized-approver override, partial refunds, both operations- and customer-initiated requests, plus bulk … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 12 Aug 2026 · workshop tracker · keyword 'refund')*
- **A80** Implement a currency-locking rule for refunds/change: always issue in the local/base currency, locked at the value recorded at time of purchase; track foreign-currency activity only via a separate report *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 14 Aug 2026 · workshop tracker · keyword 'refund')*
- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'refund')*
- **A140** Centralise policy management (reschedule, exchange, refund, cancellation, upgrade, downgrade, ownership transfer, membership conversion) with each product mapped to pricing, GL code, promotions and channels *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'refund')*
- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'refund')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'refund')*

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-045` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS40 B2B, Reseller & OTA Partner Management Board 3.dc.html#ptr-045`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 3
- Flow F132 *B2B, Reseller & OTA Partner Management board 3: Partner Operations Command …*, step 6: Works in Partner Cancellations, Refunds & Amendments → Manage post-booking changes according to the partner's commercial agreement and product policies.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-045?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create partner change request.
- [ ] Every transition is wired: `PTR-042`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-046` Partner Statement & Account Activity

**Give finance and commercial teams a complete financial statement for each partner account.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner; in the flows as partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each line should show) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/partners/partner-statement-account-activity-ptr-046` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Opening Balance** (metric tile)

**Sales** (metric tile)

**Payments** (metric tile)

**Credits** (metric tile)

**Refunds** (metric tile)

**Commission** (metric tile)

**Adjustments** (metric tile)

**Closing Balance** (metric tile)

**Overdue Balance** (metric tile)

**Available Credit** (metric tile)

**Current** (metric tile)

**1–30 Days** (metric tile)

**31–60 Days** (metric tile)

**61–90 Days** (metric tile)

**90+ Days** (metric tile)

**Every partner statement account** (data table, from `listPartnerStatementAccount`)

| Shows | Format | Notes |
|---|---|---|
| Date | text | not in the schema: `PartnerStatementAccountActivityView.date` |
| Transaction type | text | not in the schema: `PartnerStatementAccountActivityView.transactionType` |
| Reference | text | not in the schema: `PartnerStatementAccountActivityView.reference` |
| Order invoice | text | not in the schema: `PartnerStatementAccountActivityView.orderInvoice` |
| Debit | text | not in the schema: `PartnerStatementAccountActivityView.debit` |
| Credit | text | not in the schema: `PartnerStatementAccountActivityView.credit` |
| Running balance | text | not in the schema: `PartnerStatementAccountActivityView.runningBalance` |
| Due date | text | not in the schema: `PartnerStatementAccountActivityView.dueDate` |
| Status | text | not in the schema: `PartnerStatementAccountActivityView.status` |

**The selected partner statement account** (detail panel): The pack groups this record's detail under its own headings: “Generate by”, “Partner Access”, “Architecture”.

| Shows | Format | Notes |
|---|---|---|
| Date | text | not in the schema: `PartnerStatementAccountActivityView.date` |
| Transaction type | text | not in the schema: `PartnerStatementAccountActivityView.transactionType` |
| Reference | text | not in the schema: `PartnerStatementAccountActivityView.reference` |
| Order invoice | text | not in the schema: `PartnerStatementAccountActivityView.orderInvoice` |
| Debit | text | not in the schema: `PartnerStatementAccountActivityView.debit` |
| Credit | text | not in the schema: `PartnerStatementAccountActivityView.credit` |
| Running balance | text | not in the schema: `PartnerStatementAccountActivityView.runningBalance` |
| Due date | text | not in the schema: `PartnerStatementAccountActivityView.dueDate` |
| Status | text | not in the schema: `PartnerStatementAccountActivityView.status` |

**Data it reads**: `listPartnerStatementAccount` (onLoad, Partner Statement & Account Activity)

**Where the user goes next**

- → `PTR-042` Partner Operations Command Center: *Returns to the board's landing screen*; calls `listPartnerStatementAccount`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The partner statement account list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partner statement account untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No partner statement account yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the partner statement account are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Operations dashboard per partner: order volume, revenue, reservations and tickets on hold (booked but not yet issued). Cancellations/refund requests, statement of account (opening/closing balance, activity), reconciliation exceptions and disputes are tracked from this view. *(client request · MoM 31 Aug 2026, 4.5 B2B Day-to-Day Operations & Settlement · DI-557)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-046` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS40 B2B, Reseller & OTA Partner Management Board 3.dc.html#ptr-046`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 3
- Flow F132 *B2B, Reseller & OTA Partner Management board 3: Partner Operations Command …*, step 8: Works in Partner Statement & Account Activity → Give finance and commercial teams a complete financial statement for each partner account.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-046?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `PTR-042`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-047` Partner Reconciliation & Exception Management

**Reconcile operational bookings against financial and channel records and identify discrepancies.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner; in the flows as partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `exceptionId` (navigation) |
| Route | `/partners/partner-reconciliation-exception-management-ptr-047` |

#### Inputs: what the user enters or picks

**Form: Act on partner reconciliation exception** (modal, opened by *Act on partner reconciliation exception*; *Act on partner reconciliation exception* calls `actOnPartnerReconciliationException`, *Cancel* sends nothing)

**Collects what `actOnPartnerReconciliationException` sends before it is called.** Required: `action`. Optional: `assigneePrincipalId`, `adjustmentRef`, `note`. Dismissing sends nothing; the screen behind is unchanged.

`actOnPartnerReconciliationException` is not in any contract: draw the form greyed and list it in FINDINGS.md.

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Records Reconciled** (metric tile, from `listPartnerReconciliationException`)

**Unmatched Orders** (metric tile, from `listPartnerReconciliationException`)

**Amount Mismatches** (metric tile, from `listPartnerReconciliationException`)

**Missing Tickets** (metric tile, from `listPartnerReconciliationException`)

**Pricing Differences** (metric tile, from `listPartnerReconciliationException`)

**Commission Differences** (metric tile, from `listPartnerReconciliationException`)

**Payment Differences** (metric tile, from `listPartnerReconciliationException`)

**Pending Investigation** (metric tile, from `listPartnerReconciliationException`)

**Every partner reconciliation exception** (data table, from `listPartnerReconciliationException`)

**The selected partner reconciliation exception** (detail panel): The pack groups this record's detail under its own headings: “Partner Orders”, “Partner Reference OTA-82714”, “Exception Types”.

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Match, Correct, Accept Difference, Create Adjustment, Assign, Escalate, Dispute. Each needs attaching to the control it gates, or the screen needs the control.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Act on partner reconciliation exception (primary button) | `actOnPartnerReconciliationException` (not in any contract) | — | — | — | — |

**Data it reads**: `listPartnerReconciliationException` (onLoad, Partner Reconciliation & Exception Management)

**Where the user goes next**

- → `PTR-042` Partner Operations Command Center: *Returns to the board's landing screen*; calls `listPartnerReconciliationException`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The partner reconciliation exception list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partner reconciliation exception untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No partner reconciliation exception yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the partner reconciliation exception are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Operations dashboard per partner: order volume, revenue, reservations and tickets on hold (booked but not yet issued). Cancellations/refund requests, statement of account (opening/closing balance, activity), reconciliation exceptions and disputes are tracked from this view. *(client request · MoM 31 Aug 2026, 4.5 B2B Day-to-Day Operations & Settlement · DI-557)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-047` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS40 B2B, Reseller & OTA Partner Management Board 3.dc.html#ptr-047`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 3
- Flow F132 *B2B, Reseller & OTA Partner Management board 3: Partner Operations Command …*, step 10: Works in Partner Reconciliation & Exception Management → Reconcile operational bookings against financial and channel records and identify discrepancies.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-047?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Act on partner reconciliation exception.
- [ ] Every transition is wired: `PTR-042`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-048` Commission Calculation & Settlement Management

**Calculate, approve and settle commission or incentive amounts owed under partner commercial agreements.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner; in the flows as partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `lineId` (navigation), `batchId` (navigation) |
| Route | `/partners/commission-calculation-settlement-management-ptr-048` |

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Per Transaction. Each needs an operation, or needs removing from the screen; this is the Phase 3 …

#### Inputs: what the user enters or picks

**Form: Act on partner commission line** (modal, opened by *Act on partner commission line*; *Act on partner commission line* calls `actOnPartnerCommissionLine`, *Cancel* sends nothing)

**Collects what `actOnPartnerCommissionLine` sends before it is called.** Required: `action`. Optional: `reason`, `caseId`. Dismissing sends nothing; the screen behind is unchanged.

`actOnPartnerCommissionLine` is not in any contract: draw the form greyed and list it in FINDINGS.md.

**Form: Act on partner settlement batch** (modal, opened by *Act on partner settlement batch*; *Act on partner settlement batch* calls `actOnPartnerSettlementBatch`, *Cancel* sends nothing)

**Collects what `actOnPartnerSettlementBatch` sends before it is called.** Required: `action`. Optional: `scheduledDate`, `reason`, `caseId`. Dismissing sends nothing; the screen behind is unchanged.

`actOnPartnerSettlementBatch` is not in any contract: draw the form greyed and list it in FINDINGS.md.

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Commission Earned** (metric tile, from `listCommissionCalculationSettlement`)

**Commission Pending** (metric tile, from `listCommissionCalculationSettlement`)

**Approved** (metric tile, from `listCommissionCalculationSettlement`)

**On Hold** (metric tile, from `listCommissionCalculationSettlement`)

**Paid** (metric tile, from `listCommissionCalculationSettlement`)

**Reversed** (metric tile, from `listCommissionCalculationSettlement`)

**Incentives Earned** (metric tile, from `listCommissionCalculationSettlement`)

**Next Settlement date** (metric tile, from `listCommissionCalculationSettlement`)

**Every commission calculation settlement** (data table, from `listCommissionCalculationSettlement`)

**The selected commission calculation settlement** (detail panel): The pack groups this record's detail under its own headings: “For each transaction”, “Automatically account for”, “Exception states”, “Settlement Batch”, “Important Boundary”.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Per Transaction (primary button) | navigation or local | — | — | — | — |
| Act on partner commission line (secondary button) | `actOnPartnerCommissionLine` (not in any contract) | — | — | — | — |
| Act on partner settlement batch (secondary button) | `actOnPartnerSettlementBatch` (not in any contract) | — | — | — | — |

**Data it reads**: `listCommissionCalculationSettlement` (onLoad, Commission Calculation & Settlement Management)

**Where the user goes next**

- → `PTR-042` Partner Operations Command Center: *Returns to the board's landing screen*; calls `listCommissionCalculationSettlement`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The commission calculation settlement list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the commission calculation settlement untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No commission calculation settlement yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the commission calculation settlement are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-048` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS40 B2B, Reseller & OTA Partner Management Board 3.dc.html#ptr-048`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 3
- Flow F132 *B2B, Reseller & OTA Partner Management board 3: Partner Operations Command …*, step 12: Works in Commission Calculation & Settlement Management → Calculate, approve and settle commission or incentive amounts owed under partner commercial agreements.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-048?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Per Transaction, Act on partner commission line, Act on partner settlement batch.
- [ ] Every transition is wired: `PTR-042`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-049` Partner Disputes, Cases & Service Management

**Provide a structured case-management environment for partner operational and commercial disputes.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner; in the flows as partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Monitor) and no metric row |
| Offline | online only |
| Opens with | `caseId` (navigation) |
| Route | `/partners/partner-disputes-cases-service-management-ptr-049` |

**Known gaps.** **The pack names 8 actions on this screen; 6 are served since the writers pass (29 September): Booking Dispute, Pricing Dispute, Credit Dispute, Ticket Issue, Allocation Issue, API Issue by …

#### Inputs: what the user enters or picks

**Form: Create partner case** (modal, opened by *Create partner case*; *Create partner case* calls `createPartnerCase`, *Cancel* sends nothing)

**Collects what `createPartnerCase` sends before it is called.** Required: `id`, `partnerId`, `category`, `priority`, `description`, `status`, `resolutionTargetAt`. Optional: `contactId`, `orderId`, `invoiceReference`, `settlementBatchId`, `amountInDispute`, `evidence`, `ownerPrincipalId`, `slaPolicyId`, `firstResponseAt`, `resolvedAt`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.

`createPartnerCase` is not in any contract: draw the form greyed and list it in FINDINGS.md.

**Form: Act on partner case** (modal, opened by *Act on partner case*; *Act on partner case* calls `actOnPartnerCase`, *Cancel* sends nothing)

**Collects what `actOnPartnerCase` sends before it is called.** Required: `action`. Optional: `ownerPrincipalId`, `resolution`, `reason`, `note`. Dismissing sends nothing; the screen behind is unchanged.

`actOnPartnerCase` is not in any contract: draw the form greyed and list it in FINDINGS.md.

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every partner disputes cases** (data table, from `listPartnerDisputeCase`)

| Shows | Format | Notes |
|---|---|---|
| First response | text | not in the schema: `PartnerDisputesCasesServiceManagementView.firstResponse` |
| Resolution target | text | not in the schema: `PartnerDisputesCasesServiceManagementView.resolutionTarget` |
| Time open | text | not in the schema: `PartnerDisputesCasesServiceManagementView.timeOpen` |
| Sla breach | text | not in the schema: `PartnerDisputesCasesServiceManagementView.slaBreach` |

**The selected partner disputes cases** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| First response | text | not in the schema: `PartnerDisputesCasesServiceManagementView.firstResponse` |
| Resolution target | text | not in the schema: `PartnerDisputesCasesServiceManagementView.resolutionTarget` |
| Time open | text | not in the schema: `PartnerDisputesCasesServiceManagementView.timeOpen` |
| Sla breach | text | not in the schema: `PartnerDisputesCasesServiceManagementView.slaBreach` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Booking Dispute (primary button) | navigation or local | — | — | — | — |
| Pricing Dispute (secondary button) | navigation or local | — | — | — | — |
| Credit Dispute (secondary button) | navigation or local | — | — | — | — |
| Ticket Issue (secondary button) | navigation or local | — | — | — | — |
| Allocation Issue (secondary button) | navigation or local | — | — | — | — |
| API Issue (secondary button) | navigation or local | — | — | — | — |
| Finance review (secondary button) | navigation or local | — | — | — | — |
| Technical review (secondary button) | navigation or local | — | — | — | — |
| Create partner case (secondary button) | `createPartnerCase` (not in any contract) | — | — | — | — |
| Act on partner case (secondary button) | `actOnPartnerCase` (not in any contract) | — | — | — | — |

**Data it reads**: `listPartnerDisputeCase` (onLoad, Partner Disputes, Cases & Service Management)

**Where the user goes next**

- → `PTR-042` Partner Operations Command Center: *Returns to the board's landing screen*; calls `listPartnerDisputeCase`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The partner disputes cases list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partner disputes cases untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No partner disputes cases yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the partner disputes cases are still there. The pack's own statuses are Proposed → Resolved → Closed — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Operations dashboard per partner: order volume, revenue, reservations and tickets on hold (booked but not yet issued). Cancellations/refund requests, statement of account (opening/closing balance, activity), reconciliation exceptions and disputes are tracked from this view. *(client request · MoM 31 Aug 2026, 4.5 B2B Day-to-Day Operations & Settlement · DI-557)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-049` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS40 B2B, Reseller & OTA Partner Management Board 3.dc.html#ptr-049`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 3
- Flow F132 *B2B, Reseller & OTA Partner Management board 3: Partner Operations Command …*, step 14: Works in Partner Disputes, Cases & Service Management → Provide a structured case-management environment for partner operational and commercial disputes.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (8 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-049?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Booking Dispute, Pricing Dispute, Credit Dispute, Ticket Issue, Allocation Issue, API Issue, Finance review, Technical review, Create partner case, Act on partner case.
- [ ] Every transition is wired: `PTR-042`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-050` Partner Performance Scorecard & Risk Monitoring

**Create a consistent scorecard for evaluating the quality and commercial value of every partner relationship.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner; in the flows as partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/partners/partner-performance-scorecard-risk-monitoring-ptr-050` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every partner performance scorecard** (data table, from `listPartnerPerformanceScorecard`)

| Shows | Format | Notes |
|---|---|---|
| Trend | text | not in the schema: `PartnerPerformanceScorecardRiskMonitoringView.trend` |

**The selected partner performance scorecard** (detail panel): The pack groups this record's detail under its own headings: “Commercial”, “Allocation”, “Financial”, “Operational”, “Technical”, “Compliance”.

| Shows | Format | Notes |
|---|---|---|
| Trend | text | not in the schema: `PartnerPerformanceScorecardRiskMonitoringView.trend` |

**Data it reads**: `listPartnerPerformanceScorecard` (onLoad, Partner Performance Scorecard & Risk Monitoring)

**Where the user goes next**

- → `PTR-042` Partner Operations Command Center: *Returns to the board's landing screen*; calls `listPartnerPerformanceScorecard`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The partner performance scorecard list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partner performance scorecard untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No partner performance scorecard yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the partner performance scorecard are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- AI partner performance view surfaces trends, risks and opportunities across the partner base for account-management decisions. *(client request · MoM 31 Aug 2026, 4.5 B2B Day-to-Day Operations & Settlement · DI-558)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-050` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS40 B2B, Reseller & OTA Partner Management Board 3.dc.html#ptr-050`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 3
- Flow F132 *B2B, Reseller & OTA Partner Management board 3: Partner Operations Command …*, step 16: Works in Partner Performance Scorecard & Risk Monitoring → Create a consistent scorecard for evaluating the quality and commercial value of every partner relationship.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-050?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `PTR-042`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-051` Partner AI Intelligence & Relationship Optimization

**Provide TICVAI's AI decision-support layer across the complete partner lifecycle. This screen should combine information from Boards 1, 2 and 3.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner; in the flows as partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Analyze) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/partners/partner-ai-intelligence-relationship-optimization-ptr-051` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every partner intelligence relationship** (data table, from `listPartnerRelationship`)

| Shows | Format | Notes |
|---|---|---|
| Inputs considered | text | not in the schema: `PartnerAiIntelligenceRelationshipOptimizationView.inputsConsidered` |

**The selected partner intelligence relationship** (detail panel): The pack groups this record's detail under its own headings: “Commercial”, “Allocation”, “Credit”, “Risk”, “Growth”, “Natural-Language Analysis”.

| Shows | Format | Notes |
|---|---|---|
| Inputs considered | text | not in the schema: `PartnerAiIntelligenceRelationshipOptimizationView.inputsConsidered` |

**Data it reads**: `listPartnerRelationship` (onLoad, Partner AI Intelligence & Relationship Optimization)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The partner intelligence relationship list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partner intelligence relationship untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No partner intelligence relationship yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the partner intelligence relationship are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- AI partner performance view surfaces trends, risks and opportunities across the partner base for account-management decisions. *(client request · MoM 31 Aug 2026, 4.5 B2B Day-to-Day Operations & Settlement · DI-558)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-051` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS40 B2B, Reseller & OTA Partner Management Board 3.dc.html#ptr-051`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 3
- Flow F132 *B2B, Reseller & OTA Partner Management board 3: Partner Operations Command …*, step 18: Works in Partner AI Intelligence & Relationship Optimization → Provide TICVAI's AI decision-support layer across the complete partner lifecycle. This screen should combine information from Boards 1, 2 and 3.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-051?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-028, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-039, DI-040, DI-041, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

**Workshop tracker rows about P10 as a whole** (12: 0 open, 12 closed). Open first; a closed row says where it went on 30 September.

- **A89** Build corporate/B2B self-service onboarding (trade licence & VAT upload → approve/reject → rate setup → credential issuance) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker)*
- **A135** Manage group, family and corporate/allocation ticket types inside the unified product screen rather than separate screens *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 25 Aug 2026 · workshop tracker)*
- **A170** Build family and corporate wallets (parent-funded child wristbands, per-member allowances, parent-only top-up, guest self-service family setup, department-segregated corporate funds, bidirectional transfer as a venue … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker)*
- **A178** Build B2B partner management (configurable profiles, onboarding workflow, sub-agents, territory and distribution rights, venue association with per-venue pricing, document compliance repository, action permissions … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker)*
- **A179** Support all three B2B/OTA routes (direct portal · bidirectional API with external OTAs · bulk pre-generated QR CSV for non-integrating partners), with an existing OTA integration reusable by configuration *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker)*
- **A180** Build B2B agreements & payment models (tiered volume discounts, commission rates, credit limit vs. prepaid wallet vs. card, partner-reserved inventory, booking limits) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker)*
- **A181** Build B2B settlement & reconciliation (per-partner operations dashboard, statements of account, exception management for unsettled transfers, dispute handling, AI partner performance view) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker)*
- **A184** Build group, school and corporate sales (inquiry dashboard, configurable customer categories, package builder against live inventory and resources, versioned quotations with discount approval, conversion to confirmed … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker)*
- **A208** Check amendments and cancellations against policy before allowing refund, cancellation or reschedule, track booking financial status, and support deposits for school and corporate bookings *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 1 Sep 2026 · workshop tracker)*
- **A231** Build the live operations dashboard and group/B2B admission profile (real-time attendance by venue and gate, gate status, turnstile mode reconfigurable through the day, entry stats by category) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker)*
- **C35** Share the wallet-configuration reference documentation (foundation, funding, stored value, family/corporate, gift cards, payments, fraud/risk, API) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 27 Aug 2026 · workshop tracker)*
- **C44** Confirm how B2B/reseller-issued tickets are handled under a fully-dynamic-QR event policy *(Qossai · Pending → 30 Sep: Closed, Moved to T10 · 2 Sep 2026 · workshop tracker)*

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

### Across P10 Partner Web

- **Open question.** Qossai proposes a POS-style interface for high-volume resellers (hotels, travel agents) instead of a B2C-style site with login: assigned tickets and partner prices after login, optional cash drawer, sent-ticket history and resend, balance view. Chinmay wireframes both options; decide after review. *(open · MoM 29 Sep 2026, 3. B2B / reseller portal · DI-1023)*
- Qossai: partners may use the TICVAI B2B portal directly with a white-label-style B2B credential (similar to B2C), or integrate via API (preferred for OTAs such as Ticketmaster, Platinum List, BookMyShow). *(agreed · MoM 31 Aug 2026, 4.3 Clarified (integration models) · DI-552)*
- Partner access controls define which actions a partner may perform (e.g. refund, reschedule); the partner portal should only offer the actions granted. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-551)*
- Allam: B2B Portal option — partners without their own platform use a TICVAI B2B portal structured like the B2C store but behind login credentials, showing pre-configured partner pricing and products, with commission tracked the same way. *(client request · MoM 5 Aug 2026, 2. B2B Ticket Distribution Models · DI-134)*
- The POS/tablet application carries TICVAI's own branding and UI direction; the B2C and B2B mobile applications are white-label by design. *(agreed · MoM 31 Jul 2026, 15. Monday UI/UX Session Planning · DI-084)*
- Qossai: the target product is a white-label application supporting both B2C and B2B mobile use cases, built around three to four distinct flows (e.g. admission ticket flow, seat assignment flow). *(client request · MoM 31 Jul 2026, 4. Application Flow & White-Label Requirements · DI-056)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Chart cards: title with period dropdown ("This Week"), headline metrics with deltas (Tickets Sold 12,840 +8.7%, Visitors, Conversion). Data visualisations must be easy to read. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Charts · DI-041)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Dynamic KPIs, forecasts and real-time insights; role-based dashboards, preferences and smart shortcuts for every user (e.g. greeting "Good morning, Ahmed" on the home screen, p2). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Smarter Data / Personalized Experience · DI-028)*

**9 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{

}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{

}
```
