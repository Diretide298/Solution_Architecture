# WS63 — Ticket Resale Marketplace board 2

**10 screens · 13 operations · 12 schemas · 2 permissions**

Platform P09 TICVAI Web · ships as **ticvai-control** ·
platformAdmin audience · web ·
online only

## Who this is for

**platformAdmin on web.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 2 permissions apply here:
  `ORDER_VIEW, SETTLEMENT_RECONCILE`. A control nobody can use must say so,
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
| `ADM-288` | Resale Operations Command Center | B–D | 0 | 36 | 6 | 0 | 2 | 5 | — | notStarted (generated) |
| `ADM-289` | Buyer Purchase & Resale Order Management | B–D | 13 | 0 | 5 | 0 | 1 | 6 | — | notStarted (generated) |
| `ADM-290` | Ticket Ownership Transfer Management | B–D | 0 | 0 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `ADM-291` | Credential Revocation & Regeneration | B–D | 13 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-292` | Resale Fraud & Duplicate Sale Protection | B–D | 0 | 24 | 6 | 0 | 0 | 6 | — | notStarted (generated) |
| `ADM-293` | Capacity & Inventory Reconciliation | B–D | 0 | 20 | 6 | 0 | 0 | 4 | — | notStarted (generated) |
| `ADM-294` | Seller Settlement & Payout Management | B–D | 2 | 28 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-295` | Refunds, Disputes & Resale Exceptions | B–D | 2 | 0 | 6 | 0 | 0 | 6 | — | notStarted (generated) |
| `ADM-296` | Resale Audit & Ownership History | B–D | 19 | 0 | 6 | 0 | 1 | 5 | — | notStarted (generated) |
| `ADM-297` | Resale Analytics & AI Intelligence | B–D | 2 | 0 | 6 | 0 | 0 | 5 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-290, ADM-292 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-288` Resale Operations Command Center

**Provide operations teams with a real-time control center for all resale transactions after listings move into purchase/fulfillment.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `ORDER_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each resale transaction shall show) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/resale-operations-command-center-adm-288` |

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Venue | text field | — | — | `listResale2` ?venue |
| Event | text field | — | — | `listResale2` ?event |
| Product | text field | — | — | `listResale2` ?product |
| Ticket type | text field | — | — | `listResale2` ?ticketType |
| Section | text field | — | — | `listResale2` ?section |
| Seat category | text field | — | — | `listResale2` ?seatCategory |
| Seller segment | text field | — | — | `listResale2` ?sellerSegment |
| Buyer segment | text field | — | — | `listResale2` ?buyerSegment |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Resale Transactions Today** (metric tile)

**Gross Resale Value** (metric tile)

**Completed Transfers** (metric tile)

**Pending Transfers** (metric tile)

**Failed Transfers** (metric tile)

**Credential Reissues** (metric tile)

**Pending Seller Settlements** (metric tile)

**Settlement Value** (metric tile)

**Transactions Under Review** (metric tile)

**Fraud Alerts** (metric tile)

**Disputes** (metric tile)

**Refunds** (metric tile)

**Every resale operations** (data table, from `listResale`)

| Shows | Format | Notes |
|---|---|---|
| Resale transaction | text | Resale Transaction ID |
| Listing | text | Listing ID |
| Original order | text | Original Order ID |
| Original ticket | text | Original Ticket ID |
| Event | text | Event |
| Venue | text | Venue |
| Seller | text | Seller |
| Buyer | text | Buyer |
| Section row seat | text | Section / Row / Seat |
| Resale price | AED 1,234.50 | Resale Price |
| Buyer total | text | Buyer Total |
| Seller proceeds | text | Seller Proceeds |
| Purchase status | text | Purchase Status |
| Ownership status | text | Ownership Status |
| Credential status | text | Credential Status |
| Settlement status | text | Settlement Status |
| Risk score | 1,234.5 | Risk Score |
| Transaction date | 1 Oct 2026, 14:30 | Transaction Date |

**The selected resale operations** (detail panel): The pack groups this record's detail under its own headings: “Exception statuses”.

| Shows | Format | Notes |
|---|---|---|
| Resale transaction | text | Resale Transaction ID |
| Listing | text | Listing ID |
| Original order | text | Original Order ID |
| Original ticket | text | Original Ticket ID |
| Event | text | Event |
| Venue | text | Venue |
| Seller | text | Seller |
| Buyer | text | Buyer |
| Section row seat | text | Section / Row / Seat |
| Resale price | AED 1,234.50 | Resale Price |
| Buyer total | text | Buyer Total |
| Seller proceeds | text | Seller Proceeds |
| Purchase status | text | Purchase Status |
| Ownership status | text | Ownership Status |
| Credential status | text | Credential Status |
| Settlement status | text | Settlement Status |
| Risk score | 1,234.5 | Risk Score |
| Transaction date | 1 Oct 2026, 14:30 | Transaction Date |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Open transaction, Retry transfer, Hold transaction, Release transaction, Escalate, View credential, View settlement, View fraud assessment, View audit history. Each needs attaching to the control it gates, or the screen needs the control.

**Data it reads**: `listResale2` (onLoad, Resale Analytics & AI Intelligence); `listResale` (onLoad, Resale Operations Command Center)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-289` Buyer Purchase & Resale Order Management: *Works in Buyer Purchase & Resale Order Management*; calls `listResale`
- → `ADM-290` Ticket Ownership Transfer Management: *Works in Ticket Ownership Transfer Management*; calls `listResale`
- → `ADM-291` Credential Revocation & Regeneration: *Works in Credential Revocation & Regeneration*; calls `listResale`
- → `ADM-292` Resale Fraud & Duplicate Sale Protection: *Works in Resale Fraud & Duplicate Sale Protection*; calls `listResale`
- → `ADM-293` Capacity & Inventory Reconciliation: *Works in Capacity & Inventory Reconciliation*; calls `listResale`
- → `ADM-294` Seller Settlement & Payout Management: *Works in Seller Settlement & Payout Management*; calls `listResale`
- → `ADM-295` Refunds, Disputes & Resale Exceptions: *Works in Refunds, Disputes & Resale Exceptions*; calls `listResale`
- → `ADM-296` Resale Audit & Ownership History: *Works in Resale Audit & Ownership History*; calls `listResale`
- → `ADM-297` Resale Analytics & AI Intelligence: *Works in Resale Analytics & AI Intelligence*; calls `listResale`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resale operations list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resale operations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resale operations yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the resale operations are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listResale2` → `ORDER_VIEW` (read) · staff
- `listResale` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Resale listing dashboard with active / sold / expired / pending listings. Qossai: resale is expected almost exclusively for event tickets (concerts, sports), not open-dated admission tickets. *(client request · MoM 1 Sep 2026, 4.14 Resale Marketplace - Detailed Follow-Up · DI-622)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S5** Resale marketplace *(Chinmay Parab · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'resale')*
- **A210** Build the resale marketplace across three access models (client B2C site · TICVAI white-label portal · API into a client's own market) with eligibility, price range, commission, approval, ownership transfer, seller … *(Softlabs Team · High · Ongoing → 30 Sep: Closed, Rolled into S5 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **A211** Preserve the original virtual ticket ID through a resale, changing only owner and media, with a separate ownership change-log table *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S5 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **C36** Share the resale marketplace screens and documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **A213** Obtain the outstanding module documentation from Allam (pricing, upgrades, orders/reservations, resale, full access control boards) *(Allam · High · With client → 30 Sep: Closed, Rolled into S5 · 2 Sep 2026 · workshop tracker · keyword 'resale')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-288` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS169 Ticket Resale Marketplace Board 2.dc.html#adm-288`
- Workshop pack: Ticket Resale Marketplace_Reference.pdf board 2
- Flow F172 *Ticket Resale Marketplace board 2: Resale Operations Command Center*, step 1: Opens Resale Operations Command Center → Provide operations teams with a real-time control center for all resale transactions after listings move into purchase/fulfillment.
- Flow F172 *Ticket Resale Marketplace board 2: Resale Operations Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F172 *Ticket Resale Marketplace board 2: Resale Operations Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F172 *Ticket Resale Marketplace board 2: Resale Operations Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F172 *Ticket Resale Marketplace board 2: Resale Operations Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F172 *Ticket Resale Marketplace board 2: Resale Operations Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F172 *Ticket Resale Marketplace board 2: Resale Operations Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F172 *Ticket Resale Marketplace board 2: Resale Operations Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F172 branch at step 1 (expected): when Nothing has been set up on Resale Operations Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F172 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (36 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-288?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-002`, `ADM-289`, `ADM-290`, `ADM-291`, `ADM-292`, `ADM-293`, `ADM-294`, `ADM-295`, `ADM-296`, `ADM-297`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-289` Buyer Purchase & Resale Order Management

**Manage the buyer-side purchase transaction and ensure that a resale ticket is temporarily protected while checkout occurs.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `ORDER_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; Capture/reference) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/buyer-purchase-resale-order-management-adm-289` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Hold duration | select field | — | — | — | — | — | — |
| Hold extension rules | select field | — | — | — | — | — | — |
| Payment timeout | select field | — | — | — | — | — | — |
| Automatic release | select field | — | — | — | — | — | — |
| Concurrent buyer handling | select field | — | — | — | — | — | — |
| Customer ID | select field | — | — | — | — | — | — |
| Name | select field | — | — | — | — | — | — |
| Email | select field | — | — | — | — | — | — |
| Mobile | select field | — | — | — | — | — | — |
| Membership | select field | — | — | — | — | — | — |
| Loyalty profile | select field | — | — | — | — | — | — |
| Identity verification where required | text field | — | — | — | — | — | — |
| Billing information | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `listBuyerPurchaseResale` (onLoad, Buyer Purchase & Resale Order Management)

**Where the user goes next**

- → `ADM-288` Resale Operations Command Center: *Returns to the board's landing screen*; calls `listBuyerPurchaseResale`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The buyer purchase resale configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the buyer purchase resale untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No buyer purchase resale configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listBuyerPurchaseResale` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Board 1 resale rules: eligibility, allowed price range, venue/tenant fees and commission, optional approval step. Board 2 resale purchase: payment, ownership transfer and settlement to the seller. *(client request · MoM 1 Sep 2026, 4.14 Resale Marketplace - Board 1 / Board 2 · DI-619)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S5** Resale marketplace *(Chinmay Parab · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'resale')*
- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A210** Build the resale marketplace across three access models (client B2C site · TICVAI white-label portal · API into a client's own market) with eligibility, price range, commission, approval, ownership transfer, seller … *(Softlabs Team · High · Ongoing → 30 Sep: Closed, Rolled into S5 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **A211** Preserve the original virtual ticket ID through a resale, changing only owner and media, with a separate ownership change-log table *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S5 · 1 Sep 2026 · workshop tracker · keyword 'resale')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-289` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS169 Ticket Resale Marketplace Board 2.dc.html#adm-289`
- Workshop pack: Ticket Resale Marketplace_Reference.pdf board 2
- Flow F172 *Ticket Resale Marketplace board 2: Resale Operations Command Center*, step 2: Works in Buyer Purchase & Resale Order Management → Manage the buyer-side purchase transaction and ensure that a resale ticket is temporarily protected while checkout occurs.

#### Acceptance for the design

- [ ] Every input above is drawn (13), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-289?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-288`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-290` Ticket Ownership Transfer Management

**Securely transfer the ticket entitlement from the original seller to the resale buyer.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `ORDER_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/ticket-ownership-transfer-management-adm-290` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listTicketOwnershipTransfer` (onLoad, Ticket Ownership Transfer Management)

**Where the user goes next**

- → `ADM-288` Resale Operations Command Center: *Returns to the board's landing screen*; calls `listTicketOwnershipTransfer`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The ticket ownership transfer list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the ticket ownership transfer untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No ticket ownership transfer yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the ticket ownership transfer are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listTicketOwnershipTransfer` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Resale keeps the original virtual ticket ID; only owner name and media (QR) change. An ownership change log shows the history against one ID (e.g. VT0010: Qossai > Allam > Chinmay). *(agreed · MoM 1 Sep 2026, 4.14 Decision (ticket ID on resale) · DI-620)*
- Board 1 resale rules: eligibility, allowed price range, venue/tenant fees and commission, optional approval step. Board 2 resale purchase: payment, ownership transfer and settlement to the seller. *(client request · MoM 1 Sep 2026, 4.14 Resale Marketplace - Board 1 / Board 2 · DI-619)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-290` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS169 Ticket Resale Marketplace Board 2.dc.html#adm-290`
- Workshop pack: Ticket Resale Marketplace_Reference.pdf board 2
- Flow F172 *Ticket Resale Marketplace board 2: Resale Operations Command Center*, step 4: Works in Ticket Ownership Transfer Management → Securely transfer the ticket entitlement from the original seller to the resale buyer.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-290?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-288`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-291` Credential Revocation & Regeneration

**Ensure the seller's old ticket credential cannot continue to provide access after resale. This is one of the most important security functions in the module.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `ORDER_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Depending on TICVAI configuration; Deliver through configured channels) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/credential-revocation-regeneration-adm-291` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Static QR | select field | — | — | — | — | — | — |
| Dynamic QR | select field | — | — | — | — | — | — |
| Barcode | select field | — | — | — | — | — | — |
| NFC | select field | — | — | — | — | — | — |
| RFID | select field | — | — | — | — | — | — |
| Mobile Wallet pass | select field | — | — | — | — | — | — |
| Digital ticket | select field | — | — | — | — | — | — |
| Wearable credential | select field | — | — | — | — | — | — |
| TICVAI account | select field | — | — | — | — | — | — |
| Mobile app | select field | — | — | — | — | — | — |
| Email | select field | — | — | — | — | — | — |
| Wallet | select field | — | — | — | — | — | — |
| Other configured delivery methods | text field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `listCredentialRevocationRegeneration` (onLoad, Credential Revocation & Regeneration)

**Where the user goes next**

- → `ADM-288` Resale Operations Command Center: *Returns to the board's landing screen*; calls `listCredentialRevocationRegeneration`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The credential revocation regeneration configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the credential revocation regeneration untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No credential revocation regeneration configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listCredentialRevocationRegeneration` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-291` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS169 Ticket Resale Marketplace Board 2.dc.html#adm-291`
- Workshop pack: Ticket Resale Marketplace_Reference.pdf board 2
- Flow F172 *Ticket Resale Marketplace board 2: Resale Operations Command Center*, step 6: Works in Credential Revocation & Regeneration → Ensure the seller's old ticket credential cannot continue to provide access after resale. This is one of the most important security functions in the module.

#### Acceptance for the design

- [ ] Every input above is drawn (13), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-291?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-288`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-292` Resale Fraud & Duplicate Sale Protection

**Protect TICVAI, venues, sellers and buyers from resale abuse and fraudulent ticket activity.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `ORDER_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Monitor) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/resale-fraud-duplicate-sale-protection-adm-292` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every resale fraud duplicate** (data table, from `listResaleFraudDuplicate`)

| Shows | Format | Notes |
|---|---|---|
| Duplicate listings | text | not in the schema: `Duplicate listings` |
| Multiple resale attempts | 1,234 | Multiple resale attempts |
| Same ticket listed simultaneously | text | Same ticket listed simultaneously |
| Unusual seller volume | 1,234 | Unusual seller volume |
| High frequency resale | text | High-frequency resale |
| Suspicious pricing | text | Suspicious pricing |
| Multiple accounts | 1,234 | Multiple accounts |
| Payment anomalies | 1,234 | Payment anomalies |
| Identity mismatch | text | Identity mismatch |
| Credential reuse | text | Credential reuse |
| Repeated failed transactions | 1,234 | Repeated failed transactions |
| Account device anomalies | text | Account/device anomalies where permitted |

**The selected resale fraud duplicate** (detail panel): The pack groups this record's detail under its own headings: “Each transaction can receive”, “Detect attempted use of”, “Human Review”.

| Shows | Format | Notes |
|---|---|---|
| Duplicate listings | text | not in the schema: `Duplicate listings` |
| Multiple resale attempts | 1,234 | Multiple resale attempts |
| Same ticket listed simultaneously | text | Same ticket listed simultaneously |
| Unusual seller volume | 1,234 | Unusual seller volume |
| High frequency resale | text | High-frequency resale |
| Suspicious pricing | text | Suspicious pricing |
| Multiple accounts | 1,234 | Multiple accounts |
| Payment anomalies | 1,234 | Payment anomalies |
| Identity mismatch | text | Identity mismatch |
| Credential reuse | text | Credential reuse |
| Repeated failed transactions | 1,234 | Repeated failed transactions |
| Account device anomalies | text | Account/device anomalies where permitted |

**Data it reads**: `listResaleFraudDuplicate` (onLoad, Resale Fraud & Duplicate Sale Protection)

**Where the user goes next**

- → `ADM-288` Resale Operations Command Center: *Returns to the board's landing screen*; calls `listResaleFraudDuplicate`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resale fraud duplicate list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resale fraud duplicate untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resale fraud duplicate yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the resale fraud duplicate are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listResaleFraudDuplicate` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S5** Resale marketplace *(Chinmay Parab · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'resale')*
- **A69** Implement duplicate-account detection and profile-merge functionality (consolidating two profiles into one, carrying over the combined transaction history) *(Softlabs Backend Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Aug 2026 · workshop tracker · keyword 'duplicate-account')*
- **A90** Implement consent-gated duplicate merge (fuzzy name / exact mobile / exact email matching, customer confirmation required, admin review queue, login-of-record rule) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'duplicate merge')*
- **A210** Build the resale marketplace across three access models (client B2C site · TICVAI white-label portal · API into a client's own market) with eligibility, price range, commission, approval, ownership transfer, seller … *(Softlabs Team · High · Ongoing → 30 Sep: Closed, Rolled into S5 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **A211** Preserve the original virtual ticket ID through a resale, changing only owner and media, with a separate ownership change-log table *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S5 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **C36** Share the resale marketplace screens and documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 1 Sep 2026 · workshop tracker · keyword 'resale')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-292` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS169 Ticket Resale Marketplace Board 2.dc.html#adm-292`
- Workshop pack: Ticket Resale Marketplace_Reference.pdf board 2
- Flow F172 *Ticket Resale Marketplace board 2: Resale Operations Command Center*, step 8: Works in Resale Fraud & Duplicate Sale Protection → Protect TICVAI, venues, sellers and buyers from resale abuse and fraudulent ticket activity.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-292?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-288`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-293` Capacity & Inventory Reconciliation

**Ensure resale activity never creates additional venue capacity or corrupts primary ticket inventory.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `ORDER_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Detect) and a per-row directory (§For each event show) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/capacity-inventory-reconciliation-adm-293` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Duplicate active entitlement** (metric tile)

**Seat assigned to multiple active owners** (metric tile)

**Listing without ticket** (metric tile)

**Sold resale listing still active** (metric tile)

**Ownership mismatch** (metric tile)

**Credential mismatch** (metric tile)

**Capacity discrepancy** (metric tile)

**Every capacity inventory reconciliation** (data table, from `listCapacityInventoryReconciliation`)

| Shows | Format | Notes |
|---|---|---|
| Venue capacity | 1,234 | Venue capacity |
| Sellable capacity | 1,234 | Sellable capacity |
| Primary tickets sold | text | Primary tickets sold |
| Primary inventory remaining | text | Primary inventory remaining |
| Tickets listed for resale | text | Tickets listed for resale |
| Resale tickets sold | text | Resale tickets sold |
| Holds | text | Holds |
| Cancelled tickets | 1,234 | Cancelled tickets |
| Refunded tickets | text | Refunded tickets |
| Active entitlements | 1,234 | Active entitlements |

**The selected capacity inventory reconciliation** (detail panel): The pack groups this record's detail under its own headings: “A resale represents”, “Sold / New Owner”.

| Shows | Format | Notes |
|---|---|---|
| Venue capacity | 1,234 | Venue capacity |
| Sellable capacity | 1,234 | Sellable capacity |
| Primary tickets sold | text | Primary tickets sold |
| Primary inventory remaining | text | Primary inventory remaining |
| Tickets listed for resale | text | Tickets listed for resale |
| Resale tickets sold | text | Resale tickets sold |
| Holds | text | Holds |
| Cancelled tickets | 1,234 | Cancelled tickets |
| Refunded tickets | text | Refunded tickets |
| Active entitlements | 1,234 | Active entitlements |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Investigate, Re-sync, Correct mapping, Hold ticket, Escalate, Generate reconciliation report. Each needs attaching to the control it gates, or the screen needs the control.

**Data it reads**: `listCapacityInventoryReconciliation` (onLoad, Capacity & Inventory Reconciliation)

**Where the user goes next**

- → `ADM-288` Resale Operations Command Center: *Returns to the board's landing screen*; calls `listCapacityInventoryReconciliation`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The capacity inventory reconciliation list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the capacity inventory reconciliation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No capacity inventory reconciliation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the capacity inventory reconciliation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listCapacityInventoryReconciliation` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A301** Build maintenance vendor/procurement ops and analytics *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-293` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS169 Ticket Resale Marketplace Board 2.dc.html#adm-293`
- Workshop pack: Ticket Resale Marketplace_Reference.pdf board 2
- Flow F172 *Ticket Resale Marketplace board 2: Resale Operations Command Center*, step 10: Works in Capacity & Inventory Reconciliation → Ensure resale activity never creates additional venue capacity or corrupts primary ticket inventory.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-293?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-288`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-294` Seller Settlement & Payout Management

**Manage the financial amount owed to sellers following successful resale.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `ORDER_VIEW`, `SETTLEMENT_RECONCILE` (1 read, 1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | `resaleSettlementId` (navigation) |
| Route | `/commercial/seller-settlement-payout-management-adm-294` |

**Known gaps.** **The pack names 4 actions on this screen; 1 are served since the writers pass (29 September): Manual hold by `holdResaleSettlement`.** Still unserved: Payment account verification, Compliance hold …

#### Inputs: what the user enters or picks

**Form: Hold resale settlement** (modal, opened by *Hold resale settlement*; *Hold resale settlement* calls `holdResaleSettlement`, *Cancel* sends nothing)

**Collects what `holdResaleSettlement` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 1; max length 500 | — | — | `holdResaleSettlement` body |

Errors to draw in the form: 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The settlement is already `paid`, `failed` or `reversed` (`notHoldable`). (ResaleSettlementProblem)

**Form: Release resale settlement hold** (modal, opened by *Release resale settlement hold*; *Release resale settlement hold* calls `releaseResaleSettlementHold`, *Cancel* sends nothing)

**Collects what `releaseResaleSettlementHold` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 1; max length 500 | — | — | `releaseResaleSettlementHold` body |

Errors to draw in the form: 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The settlement is not `onHold` (`notOnHold`), or its hold is a `refundDisputeHold` that only the refund or dispute outcome releases (`holdNotReleasable`). (ResaleSettlementProblem)

#### Outputs: what the screen shows and produces

**Shown**

**Every seller settlement payout** (data table, from `listSellerSettlementPayout`)

| Shows | Format | Notes |
|---|---|---|
| Settlement | text | Settlement ID |
| Resale transaction | text | Resale Transaction |
| Seller | text | Seller |
| Listing price | AED 1,234.50 | Listing Price |
| Seller fee | AED 1,234.50 | Seller Fee |
| Commission | AED 1,234.50 | Commission |
| Processing fee | AED 1,234.50 | Processing fee |
| Applicable tax | text | Applicable tax |
| Adjustments | 1,234 | Adjustments |
| Seller proceeds | 1,234 | Seller Proceeds |
| Currency | text | Currency |
| Payout method | AED 1,234.50 | Payout method |
| Settlement status | 1,234 | Settlement status |
| Expected payout date | 1 Oct 2026, 14:30 | Expected payout date |

**The selected seller settlement payout** (detail panel): The pack groups this record's detail under its own headings: “Suggested”, “Exception statuses”, “A venue may prefer”, “Finance Integration”.

| Shows | Format | Notes |
|---|---|---|
| Settlement | text | Settlement ID |
| Resale transaction | text | Resale Transaction |
| Seller | text | Seller |
| Listing price | AED 1,234.50 | Listing Price |
| Seller fee | AED 1,234.50 | Seller Fee |
| Commission | AED 1,234.50 | Commission |
| Processing fee | AED 1,234.50 | Processing fee |
| Applicable tax | text | Applicable tax |
| Adjustments | 1,234 | Adjustments |
| Seller proceeds | 1,234 | Seller Proceeds |
| Currency | text | Currency |
| Payout method | AED 1,234.50 | Payout method |
| Settlement status | 1,234 | Settlement status |
| Expected payout date | 1 Oct 2026, 14:30 | Expected payout date |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Payment account verification (primary button) | navigation or local | — | — | — | — |
| Manual hold (secondary button) | navigation or local | — | — | — | — |
| Compliance hold (secondary button) | navigation or local | — | — | — | — |
| Refund/dispute hold (secondary button) | navigation or local | — | — | — | — |
| Hold resale settlement (secondary button) | `holdResaleSettlement` POST `/resale-settlements/{resaleSettlementId}/hold` | inline | ResaleSettlement | 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The settlement is already `paid`, `failed` or … | gated `SETTLEMENT_RECONCILE`; opens modal first |
| Release resale settlement hold (secondary button) | `releaseResaleSettlementHold` POST `/resale-settlements/{resaleSettlementId}/release` | inline | ResaleSettlement | 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The settlement is not `onHold` (`notOnHold`), or … | gated `SETTLEMENT_RECONCILE`; opens modal first |

**Data it reads**: `listSellerSettlementPayout` (onLoad, Seller Settlement & Payout Management)

**Where the user goes next**

- → `ADM-288` Resale Operations Command Center: *Returns to the board's landing screen*; calls `listSellerSettlementPayout`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The seller settlement payout list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the seller settlement payout untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No seller settlement payout yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the seller settlement payout are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The settlement is already `paid`, `failed` or `reversed` (`notHoldable`). (ResaleSettlementProblem); 409 The settlement is not `onHold` (`notOnHold`), or its hold is a `refundDisputeHold` that only the refund or dispute outcome releases (`holdNotReleasable`). (ResaleSettlementProblem) |

#### Permissions

- `listSellerSettlementPayout` → `ORDER_VIEW` (read) · staff
- `holdResaleSettlement` → `SETTLEMENT_RECONCILE` (operate) · staff
- `releaseResaleSettlementHold` → `SETTLEMENT_RECONCILE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Board 1 resale rules: eligibility, allowed price range, venue/tenant fees and commission, optional approval step. Board 2 resale purchase: payment, ownership transfer and settlement to the seller. *(client request · MoM 1 Sep 2026, 4.14 Resale Marketplace - Board 1 / Board 2 · DI-619)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-294` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS169 Ticket Resale Marketplace Board 2.dc.html#adm-294`
- Workshop pack: Ticket Resale Marketplace_Reference.pdf board 2
- Flow F172 *Ticket Resale Marketplace board 2: Resale Operations Command Center*, step 12: Works in Seller Settlement & Payout Management → Manage the financial amount owed to sellers following successful resale.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (403, 404, 409).
- [ ] Every output is drawn (28 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-294?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Payment account verification, Manual hold, Compliance hold, Refund/dispute hold, Hold resale settlement, Release resale settlement hold.
- [ ] Every transition is wired: `ADM-288`.
- [ ] Every gated control is gated: `ORDER_VIEW`, `SETTLEMENT_RECONCILE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-295` Refunds, Disputes & Resale Exceptions

**Handle exceptional scenarios that occur after a resale transaction.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `ORDER_VIEW`, `SETTLEMENT_RECONCILE` (1 read, 1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `resaleSettlementId` (navigation) |
| Route | `/commercial/refunds-disputes-resale-exceptions-adm-295` |

**Known gaps.** **The pack names 11 actions on this screen and the screen declares 1 operation.** Unserved: Event cancellation, Event postponement, Buyer refund, Payment chargeback, Failed ownership transfer, Failed … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Form: Hold resale settlement** (modal, opened by *Hold resale settlement*; *Hold resale settlement* calls `holdResaleSettlement`, *Cancel* sends nothing)

**Collects what `holdResaleSettlement` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 1; max length 500 | — | — | `holdResaleSettlement` body |

Errors to draw in the form: 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The settlement is already `paid`, `failed` or `reversed` (`notHoldable`). (ResaleSettlementProblem)

**Form: Release resale settlement hold** (modal, opened by *Release resale settlement hold*; *Release resale settlement hold* calls `releaseResaleSettlementHold`, *Cancel* sends nothing)

**Collects what `releaseResaleSettlementHold` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 1; max length 500 | — | — | `releaseResaleSettlementHold` body |

Errors to draw in the form: 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The settlement is not `onHold` (`notOnHold`), or its hold is a `refundDisputeHold` that only the refund or dispute outcome releases (`holdNotReleasable`). (ResaleSettlementProblem)

#### Outputs: what the screen shows and produces

**Shown**

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Refund buyer, Reverse settlement, Hold settlement, Reissue credential, Retry transfer, Cancel transaction, Return ownership, Provide replacement ticket, Escalate. Each needs attaching to the control it gates, or the screen needs the control.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Event cancellation (primary button) | navigation or local | — | — | — | — |
| Event postponement (secondary button) | navigation or local | — | — | — | — |
| Buyer refund (secondary button) | navigation or local | — | — | — | — |
| Payment chargeback (secondary button) | navigation or local | — | — | — | — |
| Failed ownership transfer (secondary button) | navigation or local | — | — | — | — |
| Failed credential issuance (secondary button) | navigation or local | — | — | — | — |
| Duplicate transaction (secondary button) | navigation or local | — | — | — | — |
| Ticket access issue (secondary button) | navigation or local | — | — | — | — |
| Hold resale settlement (secondary button) | `holdResaleSettlement` POST `/resale-settlements/{resaleSettlementId}/hold` | inline | ResaleSettlement | 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The settlement is already `paid`, `failed` or … | gated `SETTLEMENT_RECONCILE`; opens modal first |
| Release resale settlement hold (secondary button) | `releaseResaleSettlementHold` POST `/resale-settlements/{resaleSettlementId}/release` | inline | ResaleSettlement | 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The settlement is not `onHold` (`notOnHold`), or … | gated `SETTLEMENT_RECONCILE`; opens modal first |

**Data it reads**: `listRefundDisputeResale` (onLoad, Refunds, Disputes & Resale Exceptions)

**Where the user goes next**

- → `ADM-288` Resale Operations Command Center: *Returns to the board's landing screen*; calls `listRefundDisputeResale`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The refunds disputes resale list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the refunds disputes resale untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No refunds disputes resale yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the refunds disputes resale are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The settlement is already `paid`, `failed` or `reversed` (`notHoldable`). (ResaleSettlementProblem); 409 The settlement is not `onHold` (`notOnHold`), or its hold is a `refundDisputeHold` that only the refund or dispute outcome releases (`holdNotReleasable`). (ResaleSettlementProblem) |

#### Permissions

- `listRefundDisputeResale` → `ORDER_VIEW` (read) · staff
- `holdResaleSettlement` → `SETTLEMENT_RECONCILE` (operate) · staff
- `releaseResaleSettlementHold` → `SETTLEMENT_RECONCILE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S5** Resale marketplace *(Chinmay Parab · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'resale')*
- **A75** Design the refund engine: a six-step ledger-to-gateway refund flow with configurable time-banded percentages, an authorized-approver override, partial refunds, both operations- and customer-initiated requests, plus bulk … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 12 Aug 2026 · workshop tracker · keyword 'refund')*
- **A80** Implement a currency-locking rule for refunds/change: always issue in the local/base currency, locked at the value recorded at time of purchase; track foreign-currency activity only via a separate report *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 14 Aug 2026 · workshop tracker · keyword 'refund')*
- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'refund')*
- **A140** Centralise policy management (reschedule, exchange, refund, cancellation, upgrade, downgrade, ownership transfer, membership conversion) with each product mapped to pricing, GL code, promotions and channels *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'refund')*
- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'refund')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-295` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS169 Ticket Resale Marketplace Board 2.dc.html#adm-295`
- Workshop pack: Ticket Resale Marketplace_Reference.pdf board 2
- Flow F172 *Ticket Resale Marketplace board 2: Resale Operations Command Center*, step 14: Works in Refunds, Disputes & Resale Exceptions → Handle exceptional scenarios that occur after a resale transaction.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (403, 404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-295?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Event cancellation, Event postponement, Buyer refund, Payment chargeback, Failed ownership transfer, Failed credential issuance, Duplicate transaction, Ticket access issue, Hold resale settlement, Release resale settlement hold.
- [ ] Every transition is wired: `ADM-288`.
- [ ] Every gated control is gated: `ORDER_VIEW`, `SETTLEMENT_RECONCILE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-296` Resale Audit & Ownership History

**Provide complete end-to-end traceability of every ticket that enters the resale ecosystem.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `ORDER_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/resale-audit-ownership-history-adm-296` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search resale audit ownership | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by ticket id, credential, order, resale transaction, seller, buyer and 3 more — which are present is a decision the pack already made. | — |
| Timestamp | select field | — | — | — | — | — | — |
| User/system | select field | — | — | — | — | — | — |
| Action | select field | — | — | — | — | — | — |
| Original order | select field | — | — | — | — | — | — |
| Resale order | select field | — | — | — | — | — | — |
| Ticket | select field | — | — | — | — | — | — |
| Seller | select field | — | — | — | — | — | — |
| Buyer | select field | — | — | — | — | — | — |
| Listing | select field | — | — | — | — | — | — |
| Price | select field | — | — | — | — | — | — |
| Fee | select field | — | — | — | — | — | — |
| Credential | select field | — | — | — | — | — | — |
| Ownership | select field | — | — | — | — | — | — |
| Payment | select field | — | — | — | — | — | — |
| Settlement | select field | — | — | — | — | — | — |
| Approval | select field | — | — | — | — | — | — |
| Device/channel where applicable | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Ticket | text field | — | — | `listResaleOwnership` ?ticketId |
| Credential | text field | — | — | `listResaleOwnership` ?credential |
| Order | text field | — | — | `listResaleOwnership` ?order |
| Resale transaction | text field | — | — | `listResaleOwnership` ?resaleTransaction |
| Seller | text field | — | — | `listResaleOwnership` ?seller |
| Buyer | text field | — | — | `listResaleOwnership` ?buyer |
| Seat | text field | — | — | `listResaleOwnership` ?seat |
| Event | text field | — | — | `listResaleOwnership` ?event |
| Payment reference | text field | — | — | `listResaleOwnership` ?paymentReference |
| Export | radio group | — | Finance · Compliance · Fraud investigation · Customer dispute · Venue operations | `listResaleOwnership` ?export |

#### Outputs: what the screen shows and produces

**Data it reads**: `listResaleOwnership` (onLoad, Resale Audit & Ownership History); `listResaleConfirmationOwnership` (onLoad, Resale Confirmation, Ownership Transfer & Ticket Delivery)

**Where the user goes next**

- → `ADM-288` Resale Operations Command Center: *Returns to the board's landing screen*; calls `listResaleOwnership`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resale audit ownership configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resale audit ownership untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resale audit ownership configured yet. Carries the create action and says what the platform does in the meantime. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the resale audit ownership are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listResaleOwnership` → `ORDER_VIEW` (read) · staff
- `listResaleConfirmationOwnership` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Resale keeps the original virtual ticket ID; only owner name and media (QR) change. An ownership change log shows the history against one ID (e.g. VT0010: Qossai > Allam > Chinmay). *(agreed · MoM 1 Sep 2026, 4.14 Decision (ticket ID on resale) · DI-620)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S5** Resale marketplace *(Chinmay Parab · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'resale')*
- **A210** Build the resale marketplace across three access models (client B2C site · TICVAI white-label portal · API into a client's own market) with eligibility, price range, commission, approval, ownership transfer, seller … *(Softlabs Team · High · Ongoing → 30 Sep: Closed, Rolled into S5 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **A211** Preserve the original virtual ticket ID through a resale, changing only owner and media, with a separate ownership change-log table *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S5 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **C36** Share the resale marketplace screens and documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **A213** Obtain the outstanding module documentation from Allam (pricing, upgrades, orders/reservations, resale, full access control boards) *(Allam · High · With client → 30 Sep: Closed, Rolled into S5 · 2 Sep 2026 · workshop tracker · keyword 'resale')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-296` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS169 Ticket Resale Marketplace Board 2.dc.html#adm-296`
- Workshop pack: Ticket Resale Marketplace_Reference.pdf board 2
- Flow F172 *Ticket Resale Marketplace board 2: Resale Operations Command Center*, step 16: Works in Resale Audit & Ownership History → Provide complete end-to-end traceability of every ticket that enters the resale ecosystem.

#### Acceptance for the design

- [ ] Every input above is drawn (19), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-296?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-288`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-297` Resale Analytics & AI Intelligence

**Provide management with commercial, operational and predictive intelligence about the resale marketplace. Board 3 defines how the end customer actually accesses, uses, sells through, and buys from The existing resale architecture already defines the backend marketplace configuration and transaction processing across Boards 1 and 2. Board 3 closes the missing experience layer: Board 1 — Configure Marketplace Eligibility → Policy → Listings → Pricing → Fees → Approval → Inventory Board 2 — Execute Resale Transaction Buyer → Payment → Ownership Transfer → Credentials → Fraud → Settlement → Audit Board 3 — Customer Experience Seller Journey → Buyer Journey → White-Label Portal → Client B2C Integration → Hosted Marketplace → Headless/API**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `ORDER_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Display) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/resale-analytics-ai-intelligence-adm-297` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search resale analytics intelligence | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by venue, event, product, ticket type, section, seat category and 5 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Venue | text field | — | — | `listResale2` ?venue |
| Event | text field | — | — | `listResale2` ?event |
| Product | text field | — | — | `listResale2` ?product |
| Ticket type | text field | — | — | `listResale2` ?ticketType |
| Section | text field | — | — | `listResale2` ?section |
| Seat category | text field | — | — | `listResale2` ?seatCategory |
| Seller segment | text field | — | — | `listResale2` ?sellerSegment |
| Buyer segment | text field | — | — | `listResale2` ?buyerSegment |

#### Outputs: what the screen shows and produces

**Shown**

**Gross Resale Value** (metric tile)

**Resale Transactions** (metric tile)

**Resale Conversion Rate** (metric tile)

**Average Listing Price** (metric tile)

**Average Sale Price** (metric tile)

**Average Markup/Discount** (metric tile)

**Seller Proceeds** (metric tile)

**Marketplace Revenue** (metric tile)

**Average Time to Sell** (metric tile)

**Listings-to-Sales Ratio** (metric tile)

**Fraud Rate** (metric tile)

**Refund/Dispute Rate** (metric tile)

**Data it reads**: `listResale2` (onLoad, Resale Analytics & AI Intelligence); `listResale` (onLoad, Resale Operations Command Center)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resale analytics intelligence list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resale analytics intelligence untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resale analytics intelligence yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the resale analytics intelligence are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listResale2` → `ORDER_VIEW` (read) · staff
- `listResale` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S5** Resale marketplace *(Chinmay Parab · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'resale')*
- **A210** Build the resale marketplace across three access models (client B2C site · TICVAI white-label portal · API into a client's own market) with eligibility, price range, commission, approval, ownership transfer, seller … *(Softlabs Team · High · Ongoing → 30 Sep: Closed, Rolled into S5 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **A211** Preserve the original virtual ticket ID through a resale, changing only owner and media, with a separate ownership change-log table *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S5 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **C36** Share the resale marketplace screens and documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **A213** Obtain the outstanding module documentation from Allam (pricing, upgrades, orders/reservations, resale, full access control boards) *(Allam · High · With client → 30 Sep: Closed, Rolled into S5 · 2 Sep 2026 · workshop tracker · keyword 'resale')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-297` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS169 Ticket Resale Marketplace Board 2.dc.html#adm-297`
- Workshop pack: Ticket Resale Marketplace_Reference.pdf board 2
- Flow F172 *Ticket Resale Marketplace board 2: Resale Operations Command Center*, step 18: Works in Resale Analytics & AI Intelligence → Provide management with commercial, operational and predictive intelligence about the resale marketplace. Board 3 defines how the end customer actually accesses, uses, sells through, and buys from …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-297?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P09 reference designs** (from `handoff/design-batches/apps/6-ticvai-controller/README.md`)

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: the client-approved POS, for operator density and components.
- `sources/designs/TICVAI_Mobile.dc.html`: for finish and motion.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-028, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-039, DI-040, DI-041, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

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

### Across P09 TICVAI Web

- Portal access exposes TICVAI pricing, so prospects submit contact details and a trade license as proof of a real venue, reviewed and approved by TICVAI before access is granted. *(agreed · MoM 10 Sep 2026, 4.8 Customer Portal Access, Authentication & Verification · DI-827)*
- Simulation functionality stays embedded within each relevant configuration section rather than being consolidated, since it tests that section's own configuration. *(agreed · MoM 8 Sep 2026, 4.11 Dashboard & Reporting Module Consolidation Strategy · DI-722)*
- **Open question.** Proposed tenant hierarchy Tenant > Organization/Brand > Region > Branch > Venue > Department, under review against TICVAI's own organisational hierarchy before finalising. *(open · MoM 30 Jul 2026, 2. Proposed Multi-Tenant Hierarchy · DI-055)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Chart cards: title with period dropdown ("This Week"), headline metrics with deltas (Tickets Sold 12,840 +8.7%, Visitors, Conversion). Data visualisations must be easy to read. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Charts · DI-041)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Dynamic KPIs, forecasts and real-time insights; role-based dashboards, preferences and smart shortcuts for every user (e.g. greeting "Good morning, Ahmed" on the home screen, p2). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Smarter Data / Personalized Experience · DI-028)*

**7 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"holdResaleSettlement": {"method":"POST","path":"/resale-settlements/{resaleSettlementId}/hold","contract":"orders","summary":"Put a seller's resale payout on manual hold","permission":"SETTLEMENT_RECONCILE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ResaleSettlement"},
"listBuyerPurchaseResale": {"method":"GET","path":"/buyer-purchase-resale","contract":"orders","summary":"Buyer Purchase & Resale Order Management","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"BuyerPurchaseResaleOrderManagementView"},
"listCapacityInventoryReconciliation": {"method":"GET","path":"/capacity-inventory-reconciliation","contract":"orders","summary":"Capacity & Inventory Reconciliation","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CapacityInventoryReconciliationView"},
"listCredentialRevocationRegeneration": {"method":"GET","path":"/credential-revocation-regeneration","contract":"orders","summary":"Credential Revocation & Regeneration","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CredentialRevocationRegenerationView"},
"listRefundDisputeResale": {"method":"GET","path":"/refund-dispute-resale","contract":"orders","summary":"Refunds, Disputes & Resale Exceptions","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"RefundsDisputesResaleExceptionsView"},
"listResale": {"method":"GET","path":"/resale","contract":"orders","summary":"Resale Operations Command Center","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ResaleOperationsCommandCenterView"},
"listResale2": {"method":"GET","path":"/resale-2","contract":"orders","summary":"Resale Analytics & AI Intelligence","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"venue","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"ticketType","in":"query","required":false},{"name":"section","in":"query","required":false},{"name":"seatCategory","in":"query","required":false},{"name":"sellerSegment","in":"query","required":false},{"name":"buyerSegment","in":"query","required":false}],"requestBody":null,"responds":"ResaleAnalyticsAiIntelligenceView"},
"listResaleConfirmationOwnership": {"method":"GET","path":"/resale-confirmation-ownership","contract":"orders","summary":"Resale Confirmation, Ownership Transfer & Ticket Delivery","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ResaleConfirmationOwnershipTransferTicketDeliveryView"},
"listResaleFraudDuplicate": {"method":"GET","path":"/resale-fraud-duplicate","contract":"orders","summary":"Resale Fraud & Duplicate Sale Protection","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ResaleFraudDuplicateSaleProtectionView"},
"listResaleOwnership": {"method":"GET","path":"/resale-ownership","contract":"orders","summary":"Resale Audit & Ownership History","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"ticketId","in":"query","required":false},{"name":"credential","in":"query","required":false},{"name":"order","in":"query","required":false},{"name":"resaleTransaction","in":"query","required":false},{"name":"seller","in":"query","required":false},{"name":"buyer","in":"query","required":false},{"name":"seat","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"paymentReference","in":"query","required":false},{"name":"export","in":"query","required":false}],"requestBody":null,"responds":"ResaleAuditOwnershipHistoryView"},
"listSellerSettlementPayout": {"method":"GET","path":"/seller-settlement-payout","contract":"orders","summary":"Seller Settlement & Payout Management","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SellerSettlementPayoutManagementView"},
"listTicketOwnershipTransfer": {"method":"GET","path":"/ticket-ownership-transfer","contract":"orders","summary":"Ticket Ownership Transfer Management","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TicketOwnershipTransferManagementView"},
"releaseResaleSettlementHold": {"method":"POST","path":"/resale-settlements/{resaleSettlementId}/release","contract":"orders","summary":"Release a manual or compliance hold on a seller's resale payout","permission":"SETTLEMENT_RECONCILE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ResaleSettlement"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"BuyerPurchaseResaleOrderManagementView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Buyer Purchase & Resale Order Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"confirmationTransfer":{"type":"string","description":"Confirmation → Transfer"},"holdDuration":{"type":"string","format":"date-time","description":"Hold duration"},"holdExtensionRules":{"type":"string","description":"Hold extension rules"},"paymentTimeout":{"type":"string","description":"Payment timeout"},"automaticRelease":{"type":"string","description":"Automatic release"},"concurrentBuyerHandling":{"type":"string","description":"Concurrent buyer handling"},"customerId":{"type":"string","description":"Customer ID"},"name":{"type":"string","description":"Name"},"email":{"type":"string","description":"Email"},"mobile":{"type":"string","description":"Mobile"},"membership":{"type":"string","description":"Membership"},"loyaltyProfile":{"type":"string","description":"Loyalty profile"},"billingInformation":{"type":"string","description":"Billing information"},"resaleTicketPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Resale ticket price"},"buyerServiceFee":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Buyer service fee"},"taxes":{"type":"string","description":"Taxes"},"otherPermittedCharges":{"type":"string","description":"Other permitted charges"},"totalPayable":{"type":"integer","description":"Total payable"},"card":{"type":"string","description":"Card"},"wallet":{"type":"string","description":"Wallet"},"supportedAlternativePaymentMethods":{"type":"string","description":"Supported alternative payment methods"},"paymentAuthorization":{"type":"string","description":"Payment authorization"},"paymentCapture":{"type":"string","description":"Payment capture"},"failureHandling":{"type":"string","description":"Failure handling"},"identityVerification":{"type":"boolean","description":"Identity verification where required"}}},
"CapacityInventoryReconciliationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Capacity & Inventory Reconciliation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"venueCapacity":{"type":"integer","description":"Venue capacity"},"sellableCapacity":{"type":"integer","description":"Sellable capacity"},"primaryTicketsSold":{"type":"string","description":"Primary tickets sold"},"primaryInventoryRemaining":{"type":"string","description":"Primary inventory remaining"},"ticketsListedForResale":{"type":"string","description":"Tickets listed for resale"},"resaleTicketsSold":{"type":"string","description":"Resale tickets sold"},"holds":{"type":"string","description":"Holds"},"cancelledTickets":{"type":"integer","description":"Cancelled tickets"},"refundedTickets":{"type":"string","description":"Refunded tickets"},"activeEntitlements":{"type":"integer","description":"Active entitlements"},"soldResaleListingStillActive":{"type":"integer","description":"Sold resale listing still active"},"ownershipMismatch":{"type":"string","description":"Ownership mismatch"},"credentialMismatch":{"type":"string","description":"Credential mismatch"},"capacityDiscrepancy":{"type":"integer","description":"Capacity discrepancy"}}},
"CredentialRevocationRegenerationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Credential Revocation & Regeneration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"oldCredentialRevoke":{"type":"string","description":"Old Credential → Revoke"},"revokedResold":{"type":"string","description":"Revoked — Resold"},"newCredentialId":{"type":"string","description":"New credential ID"},"newQr":{"type":"integer","description":"New QR"},"newToken":{"type":"integer","description":"New token"},"buyerAssociation":{"type":"string","description":"Buyer association"},"originalTicketRelationship":{"type":"string","description":"Original ticket relationship"},"newSecurityKeys":{"type":"integer","description":"New security keys/token where applicable"},"newWalletPass":{"type":"integer","description":"New wallet pass where applicable"},"credentialMedia":{"type":"string","enum":["staticQr","dynamicQr","barcode","nfc","rfid","mobileWalletPass","digitalTicket","wearableCredential"],"description":"Credential media handled."},"deliveryMethod":{"type":"string","enum":["mobileApp","email","wallet","otherConfiguredDeliveryMethods"],"description":"How the new credential is delivered."}}},
"RefundsDisputesResaleExceptionsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Refunds, Disputes & Resale Exceptions displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"caseId":{"type":"string","description":"Case ID"},"resaleTransaction":{"type":"string","description":"Resale transaction"},"originalOrder":{"type":"string","description":"Original order"},"seller":{"type":"string","description":"Seller"},"buyer":{"type":"string","description":"Buyer"},"event":{"type":"string","description":"Event"},"financialAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Financial amount"},"credentialStatus":{"type":"string","description":"Credential status"},"settlementStatus":{"type":"string","description":"Settlement status"},"caseOwner":{"type":"string","description":"Case owner"},"sla":{"type":"string","description":"SLA"},"evidence":{"type":"string","description":"Evidence"},"notes":{"type":"string","description":"Notes"},"resolution":{"type":"string","description":"Resolution"},"issueType":{"type":"string","enum":["eventCancellation","eventPostponement","buyerRefund","sellerDispute","buyerDispute","paymentChargeback","failedOwnershipTransfer","failedCredentialIssuance","duplicateTransaction","ticketAccessIssue","sellerPayoutDispute","incorrectTicket","venueChange","seatChange"],"description":"Exception type."},"refundRecipient":{"type":"string","enum":["resaleBuyer","originalPurchaser","split"],"description":"Who is refunded when the event is cancelled after a resale; set by the resale policy the client names (make-or-break, see the operation)"}}},
"ResaleAnalyticsAiIntelligenceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Resale Analytics & AI Intelligence displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"grossResaleValue":{"type":"string","description":"Gross Resale Value"},"resaleTransactions":{"type":"integer","description":"Resale Transactions"},"resaleConversionRate":{"type":"number","description":"Resale Conversion Rate"},"averageListingPrice":{"type":"number","description":"Average Listing Price"},"averageSalePrice":{"type":"number","description":"Average Sale Price"},"averageMarkup":{"type":"number","description":"Average Markup"},"averageDiscount":{"type":"number","description":"Average discount, percent"},"sellerProceeds":{"type":"integer","description":"Seller Proceeds"},"marketplaceRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Marketplace Revenue"},"averageTimeToSell":{"type":"string","format":"date-time","description":"Average Time to Sell"},"listingsToSalesRatio":{"type":"number","description":"Listings-to-Sales Ratio"},"fraudRate":{"type":"number","description":"Fraud Rate"},"refundDisputeRate":{"type":"number","description":"Refund/Dispute Rate"},"primaryAvailability":{"type":"string","description":"Primary availability"},"resaleAvailability":{"type":"string","description":"Resale availability"},"primaryPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Primary price"},"averageResalePrice":{"type":"number","description":"Average resale price"},"demand":{"type":"string","description":"Demand"},"conversion":{"type":"number","description":"Conversion"},"sellThrough":{"type":"string","description":"Sell-through"},"expectedResaleDemand":{"type":"string","description":"Expected resale demand"},"expectedListingVolume":{"type":"integer","description":"Expected listing volume"},"expectedResalePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Expected resale price"},"expectedConversion":{"type":"number","description":"Expected conversion"},"expectedMarketplaceRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Expected marketplace revenue"}}},
"ResaleAuditOwnershipHistoryView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Resale Audit & Ownership History displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"timestamp":{"type":"string","format":"date-time","description":"Timestamp"},"userSystem":{"type":"string","description":"User/system"},"action":{"type":"string","description":"Action"},"originalOrder":{"type":"string","description":"Original order"},"resaleOrder":{"type":"string","description":"Resale order"},"ticket":{"type":"string","description":"Ticket"},"seller":{"type":"string","description":"Seller"},"buyer":{"type":"string","description":"Buyer"},"listing":{"type":"string","description":"Listing"},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Price"},"fee":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Fee"},"credential":{"type":"string","description":"Credential"},"ownership":{"type":"string","description":"Ownership"},"payment":{"type":"string","description":"Payment"},"settlement":{"type":"string","description":"Settlement"},"approval":{"type":"string","description":"Approval"},"ticketId":{"type":"string","description":"Ticket ID"},"order":{"type":"string","description":"Order"},"resaleTransaction":{"type":"string","description":"Resale transaction"},"paymentReference":{"type":"string","description":"Payment reference"},"deviceChannel":{"type":"string","description":"Device/channel where applicable"}}},
"ResaleConfirmationOwnershipTransferTicketDeliveryView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Resale Confirmation, Ownership Transfer & Ticket Delivery displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"dynamicQr":{"type":"string","description":"Dynamic QR"},"mobileTicket":{"type":"string","description":"Mobile Ticket"},"appleWallet":{"type":"string","description":"Apple Wallet"},"googleWallet":{"type":"string","description":"Google Wallet"},"otherSupportedCredentialMedia":{"type":"string","description":"Other supported credential media"},"rfidNfcAssignment":{"type":"string","description":"RFID/NFC assignment where applicable"},"ticketId":{"type":"string","description":"Ticket ID, unchanged through the resale (MoM 1 Sep)"},"currentOwner":{"type":"string","description":"Current owner"},"previousOwner":{"type":"string","description":"Previous owner"},"settlementStatus":{"type":"string","description":"Seller settlement status"}}},
"ResaleFraudDuplicateSaleProtectionView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Resale Fraud & Duplicate Sale Protection displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"multipleResaleAttempts":{"type":"integer","description":"Multiple resale attempts"},"sameTicketListedSimultaneously":{"type":"string","description":"Same ticket listed simultaneously"},"unusualSellerVolume":{"type":"integer","description":"Unusual seller volume"},"highFrequencyResale":{"type":"string","description":"High-frequency resale"},"suspiciousPricing":{"type":"string","description":"Suspicious pricing"},"multipleAccounts":{"type":"integer","description":"Multiple accounts"},"paymentAnomalies":{"type":"integer","description":"Payment anomalies"},"identityMismatch":{"type":"string","description":"Identity mismatch"},"credentialReuse":{"type":"string","description":"Credential reuse"},"repeatedFailedTransactions":{"type":"integer","description":"Repeated failed transactions"},"revokedSellerCredential":{"type":"string","description":"Revoked seller credential"},"duplicatedCredentials":{"type":"string","description":"Duplicated credentials"},"invalidatedTickets":{"type":"string","description":"Invalidated tickets"},"accountDeviceAnomalies":{"type":"string","description":"Account/device anomalies where permitted"},"response":{"type":"string","enum":["allow","requireVerification","holdTransaction","requireManualReview"],"description":"Configured response to the signal."}}},
"ResaleOperationsCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Resale Operations Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"resaleTransactionsToday":{"type":"string","description":"Resale Transactions Today"},"grossResaleValue":{"type":"string","description":"Gross Resale Value"},"completedTransfers":{"type":"integer","description":"Completed Transfers"},"pendingTransfers":{"type":"integer","description":"Pending Transfers"},"failedTransfers":{"type":"integer","description":"Failed Transfers"},"credentialReissues":{"type":"integer","description":"Credential Reissues"},"pendingSellerSettlements":{"type":"integer","description":"Pending Seller Settlements"},"settlementValue":{"type":"string","description":"Settlement Value"},"transactionsUnderReview":{"type":"string","description":"Transactions Under Review"},"fraudAlerts":{"type":"integer","description":"Fraud Alerts"},"disputes":{"type":"integer","description":"Disputes"},"refunds":{"type":"integer","description":"Refunds"},"resaleTransactionId":{"type":"string","description":"Resale Transaction ID"},"listingId":{"type":"string","description":"Listing ID"},"originalOrderId":{"type":"string","description":"Original Order ID"},"originalTicketId":{"type":"string","description":"Original Ticket ID"},"event":{"type":"string","description":"Event"},"venue":{"type":"string","description":"Venue"},"seller":{"type":"string","description":"Seller"},"buyer":{"type":"string","description":"Buyer"},"sectionRowSeat":{"type":"string","description":"Section / Row / Seat"},"resalePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Resale Price"},"buyerTotal":{"type":"string","description":"Buyer Total"},"sellerProceeds":{"type":"string","description":"Seller Proceeds"},"purchaseStatus":{"type":"string","description":"Purchase Status"},"ownershipStatus":{"type":"string","description":"Ownership Status"},"credentialStatus":{"type":"string","description":"Credential Status"},"settlementStatus":{"type":"string","description":"Settlement Status"},"riskScore":{"type":"number","description":"Risk Score"},"transactionDate":{"type":"string","format":"date-time","description":"Transaction Date"},"statusesType":{"type":"string","enum":["paymentFailed","transferFailed","underReview","suspended","refunded","disputed","cancelled"],"description":"Vocabulary listed under Exception statuses."}}},
"ResaleSettlement": {"type":"object","x-ticvai-persistence":"orders.resale_settlement","description":"**What one seller is owed for one sold listing, and when and how it is paid** (DM5, 29 September: data model for the agreed operations; MoM 1 Sep 4.14, Board 2: settlement to the original seller). The amounts are fixed from the listing's own fee snapshot at sale. `ResaleListing.payoutStatus` is the seller-facing summary of this row.\n**The seller is paid after the buyer is admitted, not after they pay**, so a dispute or a refund lands on a settlement that is still `pending` or `onHold`, never on money already paid out.","required":["id","resaleListingId","sellerSubjectId","listingPrice","sellerFee","sellerProceeds","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"resaleListingId":{"x-ticvai-references":"orders.resale_listing","type":"string","format":"uuid","description":"Unique; one settlement per sold listing."},"sellerSubjectId":{"type":"string","format":"uuid"},"listingPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"sellerFee":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"processingFee":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"tax":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"adjustments":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"sellerProceeds":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"payoutMethod":{"type":"string","nullable":true,"description":"Proposed values, client to correct (DM5).","enum":["originalPaymentMethod","bankTransfer","wallet"]},"settlementBatch":{"type":"string","maxLength":100,"nullable":true},"expectedPayoutDate":{"type":"string","format":"date","nullable":true},"status":{"type":"string","enum":["pending","scheduled","onHold","paid","failed","reversed"]},"holdReason":{"type":"string","nullable":true,"enum":["manualHold","complianceHold","refundDisputeHold"]},"paidAt":{"type":"string","format":"date-time","nullable":true},"failureReason":{"type":"string","maxLength":500,"nullable":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"SellerSettlementPayoutManagementView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Seller Settlement & Payout Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"settlementId":{"type":"string","description":"Settlement ID"},"resaleTransaction":{"type":"string","description":"Resale Transaction"},"seller":{"type":"string","description":"Seller"},"listingPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Listing Price"},"sellerFee":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Seller Fee"},"commission":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Commission"},"processingFee":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Processing fee"},"applicableTax":{"type":"string","description":"Applicable tax"},"adjustments":{"type":"integer","description":"Adjustments"},"sellerProceeds":{"type":"integer","description":"Seller Proceeds"},"currency":{"type":"string","description":"Currency"},"payoutMethod":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Payout method"},"settlementStatus":{"type":"integer","description":"Settlement status"},"expectedPayoutDate":{"type":"string","format":"date-time","description":"Expected payout date"},"statusesType":{"type":"string","enum":["onHold","failed","reversed","disputed"],"description":"Vocabulary listed under Exception statuses."},"minimumPayoutThreshold":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Minimum payout threshold"},"settlementBatches":{"type":"string","description":"Settlement batches"},"sellerVerification":{"type":"string","description":"Seller verification"},"paymentAccountVerification":{"type":"string","description":"Payment account verification"},"settlementTiming":{"type":"string","enum":["immediatelyAfterResale","xDaysAfterResale","afterEventCompletion","xDaysAfterEvent","afterAccessValidation","operatorDefinedSettlementCycle"],"description":"When sellers are paid (a venue may pay only after the event has taken place)."},"holdReason":{"type":"string","enum":["manualHold","complianceHold","refundDisputeHold"],"description":"Why a payout is on hold."}}},
"TicketOwnershipTransferManagementView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Ticket Ownership Transfer Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"customer":{"type":"string","description":"Customer"},"originalOrder":{"type":"string","description":"Original order"},"ticket":{"type":"string","description":"Ticket"},"ownershipStatus":{"type":"string","description":"Ownership status"},"newResaleOrder":{"type":"integer","description":"New resale order"},"identity":{"type":"string","description":"Identity"},"membershipAccount":{"type":"string","description":"Membership/account"},"event":{"type":"string","description":"Event"},"product":{"type":"string","description":"Product"},"seat":{"type":"string","description":"Seat"},"entitlements":{"type":"string","description":"Entitlements"},"validity":{"type":"string","description":"Validity"},"sellerOwnershipHistoricalTransferred":{"type":"string","description":"Seller Ownership: Historical / Transferred"},"buyerOwnershipActive":{"type":"integer","description":"Buyer Ownership: Active"},"admissionEntitlement":{"type":"string","description":"Admission entitlement"},"seatAssignment":{"type":"string","description":"Seat assignment"},"accessRights":{"type":"string","description":"Access rights"},"associatedBenefits":{"type":"string","description":"Associated benefits"},"addOns":{"type":"string","description":"Add-ons where permitted"}}}
}
```
