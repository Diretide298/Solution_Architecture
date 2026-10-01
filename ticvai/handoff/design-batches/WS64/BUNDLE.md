# WS64 — Ticket Resale Marketplace board 3

**10 screens · 10 operations · 10 schemas · 1 permissions**

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

- **Every control that can be refused must be gated.** 1 permissions apply here:
  `ORDER_VIEW`. A control nobody can use must say so,
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
| `ADM-298` | My Tickets & Resale Marketplace Entry | B–D | 7 | 0 | 5 | 0 | 2 | 5 | — | notStarted (generated) |
| `ADM-299` | Resale Eligibility & Ticket Selection | B–D | 0 | 16 | 6 | 0 | 1 | 5 | — | notStarted (generated) |
| `ADM-300` | Create Listing & Resale Price Selection | B–D | 0 | 0 | 6 | 0 | 2 | 5 | — | notStarted (generated) |
| `ADM-301` | Fees, Seller Proceeds & Listing Confirmation | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-302` | My Resale Listings & Seller Dashboard | B–D | 0 | 22 | 6 | 0 | 1 | 5 | — | notStarted (generated) |
| `ADM-303` | Official Resale Marketplace & Buyer Discovery | B–D | 0 | 0 | 6 | 0 | 2 | 5 | — | notStarted (generated) |
| `ADM-304` | Resale Ticket Detail, Seat Selection & Primary-vs-Resale Experience | B–D | 0 | 24 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `ADM-305` | Buyer Checkout, Inventory Hold & Secure Payment | B–D | 1 | 0 | 5 | 0 | 1 | 6 | — | notStarted (generated) |
| `ADM-306` | Resale Confirmation, Ownership Transfer & Ticket Delivery | B–D | 0 | 0 | 6 | 0 | 1 | 5 | — | notStarted (generated) |
| `ADM-307` | White-Label Marketplace Deployment & Experience Architecture | B–D | 19 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-299, ADM-300, ADM-301, ADM-304, ADM-305, ADM-306 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-298` My Tickets & Resale Marketplace Entry

**Provide the authenticated ticket holder with a simple and secure entry point into the official resale journey. The preferred starting point should be the customer's existing: My Account → My Tickets rather than asking customers to manually enter ticket numbers or upload ticket PDFs.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `ORDER_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Depending on ticket configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/my-tickets-resale-marketplace-entry-adm-298` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| View Ticket | select field | — | — | — | — | — | — |
| Add to Wallet | select field | — | — | — | — | — | — |
| Transfer | select field | — | — | — | — | — | — |
| Exchange | select field | — | — | — | — | — | — |
| Upgrade | select field | — | — | — | — | — | — |
| Resell Ticket | select field | — | — | — | — | — | — |
| Request Refund | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `listTicketResaleMarketplace` (onLoad, My Tickets & Resale Marketplace Entry)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-299` Resale Eligibility & Ticket Selection: *Works in Resale Eligibility & Ticket Selection*; calls `listTicketResaleMarketplace`
- → `ADM-300` Create Listing & Resale Price Selection: *Works in Create Listing & Resale Price Selection*; calls `listTicketResaleMarketplace`
- → `ADM-301` Fees, Seller Proceeds & Listing Confirmation: *Works in Fees, Seller Proceeds & Listing Confirmation*; calls `listTicketResaleMarketplace`
- → `ADM-302` My Resale Listings & Seller Dashboard: *Works in My Resale Listings & Seller Dashboard*; calls `listTicketResaleMarketplace`
- → `ADM-303` Official Resale Marketplace & Buyer Discovery: *Works in Official Resale Marketplace & Buyer Discovery*; calls `listTicketResaleMarketplace`
- → `ADM-304` Resale Ticket Detail, Seat Selection & Primary-vs-Resale Experience: *Works in Resale Ticket Detail, Seat Selection & Primary-vs-Resale Experience*; calls `listTicketResaleMarketplace`
- → `ADM-305` Buyer Checkout, Inventory Hold & Secure Payment: *Works in Buyer Checkout, Inventory Hold & Secure Payment*; calls `listTicketResaleMarketplace`
- → `ADM-306` Resale Confirmation, Ownership Transfer & Ticket Delivery: *Works in Resale Confirmation, Ownership Transfer & Ticket Delivery*; calls `listTicketResaleMarketplace`
- → `ADM-307` White-Label Marketplace Deployment & Experience Architecture: *Works in White-Label Marketplace Deployment & Experience Architecture*; calls `listTicketResaleMarketplace`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The tickets resale marketplace configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the tickets resale marketplace untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No tickets resale marketplace configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listTicketResaleMarketplace` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Three resale access models: (1) the client's own B2C site, where a guest requests resale within an admin-set price range (e.g. 10-20% below original); (2) a TICVAI-hosted white-label resale portal (e.g. museum.tickvai.com) for clients without B2C; (3) API for clients' own resale markets. *(agreed · MoM 1 Sep 2026, 4.14 Resale Marketplace - Detailed Follow-Up · DI-618)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S5** Resale marketplace *(Chinmay Parab · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'resale')*
- **A210** Build the resale marketplace across three access models (client B2C site · TICVAI white-label portal · API into a client's own market) with eligibility, price range, commission, approval, ownership transfer, seller … *(Softlabs Team · High · Ongoing → 30 Sep: Closed, Rolled into S5 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **A211** Preserve the original virtual ticket ID through a resale, changing only owner and media, with a separate ownership change-log table *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S5 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **C36** Share the resale marketplace screens and documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **A213** Obtain the outstanding module documentation from Allam (pricing, upgrades, orders/reservations, resale, full access control boards) *(Allam · High · With client → 30 Sep: Closed, Rolled into S5 · 2 Sep 2026 · workshop tracker · keyword 'resale')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-298` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS170 Ticket Resale Marketplace Board 3.dc.html#adm-298`
- Workshop pack: Ticket Resale Marketplace_Reference.pdf board 3
- Flow F173 *Ticket Resale Marketplace board 3: My Tickets & Resale Marketplace Entry*, step 1: Opens My Tickets & Resale Marketplace Entry → Provide the authenticated ticket holder with a simple and secure entry point into the official resale journey. The preferred starting point should be the customer's existing: My Account → My Tickets …
- Flow F173 *Ticket Resale Marketplace board 3: My Tickets & Resale Marketplace Entry*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F173 *Ticket Resale Marketplace board 3: My Tickets & Resale Marketplace Entry*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F173 *Ticket Resale Marketplace board 3: My Tickets & Resale Marketplace Entry*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F173 *Ticket Resale Marketplace board 3: My Tickets & Resale Marketplace Entry*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F173 *Ticket Resale Marketplace board 3: My Tickets & Resale Marketplace Entry*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F173 *Ticket Resale Marketplace board 3: My Tickets & Resale Marketplace Entry*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F173 *Ticket Resale Marketplace board 3: My Tickets & Resale Marketplace Entry*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F173 branch at step 1 (expected): when Nothing has been set up on My Tickets & Resale Marketplace Entry yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F173 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-298?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-002`, `ADM-299`, `ADM-300`, `ADM-301`, `ADM-302`, `ADM-303`, `ADM-304`, `ADM-305`, `ADM-306`, `ADM-307`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-299` Resale Eligibility & Ticket Selection

**Explain whether the selected ticket can be resold before allowing a listing to be created.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `ORDER_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/resale-eligibility-ticket-selection-adm-299` |

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Sell selected tickets. Each needs an operation, or needs removing from the screen; this is the Phase 3 …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every resale eligibility ticket** (data table, from `listResaleEligibilityTicket`)

| Shows | Format | Notes |
|---|---|---|
| ✓ your ticket is eligible for resale | text | not in the schema: `✓ Your ticket is eligible for resale` |
| Event | text | Event |
| Date | 1 Oct 2026, 14:30 | Date |
| Venue | text | Venue |
| Seat | text | Seat |
| Original price | AED 1,234.50 | Original price |
| Resale closing time | 1 Oct 2026, 14:30 | Resale closing time |
| Applicable marketplace conditions | 1,234 | Applicable marketplace conditions |

**The selected resale eligibility ticket** (detail panel): The pack groups this record's detail under its own headings: “Eligibility Check”, “Check applicable conditions such as”, “Do not simply display”, “Multiple Tickets”, “Backend Boundary”.

| Shows | Format | Notes |
|---|---|---|
| ✓ your ticket is eligible for resale | text | not in the schema: `✓ Your ticket is eligible for resale` |
| Event | text | Event |
| Date | 1 Oct 2026, 14:30 | Date |
| Venue | text | Venue |
| Seat | text | Seat |
| Original price | AED 1,234.50 | Original price |
| Resale closing time | 1 Oct 2026, 14:30 | Resale closing time |
| Applicable marketplace conditions | 1,234 | Applicable marketplace conditions |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Sell selected tickets (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `listResaleEligibilityTicket` (onLoad, Resale Eligibility & Ticket Selection)

**Where the user goes next**

- → `ADM-298` My Tickets & Resale Marketplace Entry: *Returns to the board's landing screen*; calls `listResaleEligibilityTicket`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resale eligibility ticket list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resale eligibility ticket untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resale eligibility ticket yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the resale eligibility ticket are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listResaleEligibilityTicket` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- White-label resale page: guest lists a ticket and sets a price within the allowed range; buyer searches, browses and receives the new ticket after purchase; the resale summary shows the market fee TICVAI retains. *(client request · MoM 1 Sep 2026, 4.14 Resale Marketplace - Board 3 · DI-621)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S5** Resale marketplace *(Chinmay Parab · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'resale')*
- **A210** Build the resale marketplace across three access models (client B2C site · TICVAI white-label portal · API into a client's own market) with eligibility, price range, commission, approval, ownership transfer, seller … *(Softlabs Team · High · Ongoing → 30 Sep: Closed, Rolled into S5 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **A211** Preserve the original virtual ticket ID through a resale, changing only owner and media, with a separate ownership change-log table *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S5 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **C36** Share the resale marketplace screens and documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **A213** Obtain the outstanding module documentation from Allam (pricing, upgrades, orders/reservations, resale, full access control boards) *(Allam · High · With client → 30 Sep: Closed, Rolled into S5 · 2 Sep 2026 · workshop tracker · keyword 'resale')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-299` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS170 Ticket Resale Marketplace Board 3.dc.html#adm-299`
- Workshop pack: Ticket Resale Marketplace_Reference.pdf board 3
- Flow F173 *Ticket Resale Marketplace board 3: My Tickets & Resale Marketplace Entry*, step 2: Works in Resale Eligibility & Ticket Selection → Explain whether the selected ticket can be resold before allowing a listing to be created.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-299?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Sell selected tickets.
- [ ] Every transition is wired: `ADM-298`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-300` Create Listing & Resale Price Selection

**Allow an eligible seller to select a resale price within the client's approved marketplace rules.**

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
| Route | `/commercial/create-listing-resale-price-selection-adm-300` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listCreateListingResale` (onLoad, Create Listing & Resale Price Selection)

**Where the user goes next**

- → `ADM-298` My Tickets & Resale Marketplace Entry: *Returns to the board's landing screen*; calls `listCreateListingResale`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The create listing resale list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the create listing resale untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No create listing resale yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the create listing resale are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listCreateListingResale` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- White-label resale page: guest lists a ticket and sets a price within the allowed range; buyer searches, browses and receives the new ticket after purchase; the resale summary shows the market fee TICVAI retains. *(client request · MoM 1 Sep 2026, 4.14 Resale Marketplace - Board 3 · DI-621)*
- Three resale access models: (1) the client's own B2C site, where a guest requests resale within an admin-set price range (e.g. 10-20% below original); (2) a TICVAI-hosted white-label resale portal (e.g. museum.tickvai.com) for clients without B2C; (3) API for clients' own resale markets. *(agreed · MoM 1 Sep 2026, 4.14 Resale Marketplace - Detailed Follow-Up · DI-618)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S5** Resale marketplace *(Chinmay Parab · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'resale')*
- **A210** Build the resale marketplace across three access models (client B2C site · TICVAI white-label portal · API into a client's own market) with eligibility, price range, commission, approval, ownership transfer, seller … *(Softlabs Team · High · Ongoing → 30 Sep: Closed, Rolled into S5 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **A211** Preserve the original virtual ticket ID through a resale, changing only owner and media, with a separate ownership change-log table *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S5 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **C36** Share the resale marketplace screens and documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **A213** Obtain the outstanding module documentation from Allam (pricing, upgrades, orders/reservations, resale, full access control boards) *(Allam · High · With client → 30 Sep: Closed, Rolled into S5 · 2 Sep 2026 · workshop tracker · keyword 'resale')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-300` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS170 Ticket Resale Marketplace Board 3.dc.html#adm-300`
- Workshop pack: Ticket Resale Marketplace_Reference.pdf board 3
- Flow F173 *Ticket Resale Marketplace board 3: My Tickets & Resale Marketplace Entry*, step 4: Works in Create Listing & Resale Price Selection → Allow an eligible seller to select a resale price within the client's approved marketplace rules.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-300?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-298`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-301` Fees, Seller Proceeds & Listing Confirmation

**Provide complete financial transparency before the seller commits to publishing the listing. This is essential to prevent later disputes.**

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
| Route | `/commercial/fees-seller-proceeds-listing-confirmation-adm-301` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listFeeSellerProceed` (onLoad, Fees, Seller Proceeds & Listing Confirmation)

**Where the user goes next**

- → `ADM-298` My Tickets & Resale Marketplace Entry: *Returns to the board's landing screen*; calls `listFeeSellerProceed`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The fees seller proceeds list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the fees seller proceeds untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No fees seller proceeds yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the fees seller proceeds are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listFeeSellerProceed` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- White-label resale page: guest lists a ticket and sets a price within the allowed range; buyer searches, browses and receives the new ticket after purchase; the resale summary shows the market fee TICVAI retains. *(client request · MoM 1 Sep 2026, 4.14 Resale Marketplace - Board 3 · DI-621)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-301` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS170 Ticket Resale Marketplace Board 3.dc.html#adm-301`
- Workshop pack: Ticket Resale Marketplace_Reference.pdf board 3
- Flow F173 *Ticket Resale Marketplace board 3: My Tickets & Resale Marketplace Entry*, step 6: Works in Fees, Seller Proceeds & Listing Confirmation → Provide complete financial transparency before the seller commits to publishing the listing. This is essential to prevent later disputes.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-301?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-298`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-302` My Resale Listings & Seller Dashboard

**Give sellers a dedicated self-service workspace to manage their resale activity after publishing.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `ORDER_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Display; Show) and a per-row directory (§Each listing shows) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/my-resale-listings-seller-dashboard-adm-302` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Active Listings** (metric tile)

**Pending Approval** (metric tile)

**Sold** (metric tile)

**Expiring Soon** (metric tile)

**Seller Proceeds** (metric tile)

**Pending Settlement** (metric tile)

**Paid Settlements** (metric tile)

**SOLD ✓** (metric tile)

**Selling Price: AED 220** (metric tile)

**Estimated Proceeds: AED 198** (metric tile)

**Settlement: Scheduled after event** (metric tile)

**Every resale listings seller** (data table, from `listResaleListingSeller`)

| Shows | Format | Notes |
|---|---|---|
| Event | text | Event |
| Date | 1 Oct 2026, 14:30 | Date |
| Seat | text | Seat |
| Listing price | AED 1,234.50 | Listing Price |
| Original price | AED 1,234.50 | Original Price |
| Marketplace status | text | Marketplace Status |
| Views | text | Views where applicable |
| Listing date | 1 Oct 2026, 14:30 | Listing Date |
| Expiry | 1 Oct 2026, 14:30 | Expiry |
| Seller proceeds | 1,234 | Seller Proceeds |
| Settlement status | text | Settlement Status |

**The selected resale listings seller** (detail panel): The pack groups this record's detail under its own headings: “Reserved by Buyer”.

| Shows | Format | Notes |
|---|---|---|
| Event | text | Event |
| Date | 1 Oct 2026, 14:30 | Date |
| Seat | text | Seat |
| Listing price | AED 1,234.50 | Listing Price |
| Original price | AED 1,234.50 | Original Price |
| Marketplace status | text | Marketplace Status |
| Views | text | Views where applicable |
| Listing date | 1 Oct 2026, 14:30 | Listing Date |
| Expiry | 1 Oct 2026, 14:30 | Expiry |
| Seller proceeds | 1,234 | Seller Proceeds |
| Settlement status | text | Settlement Status |

**Data it reads**: `listResaleListingSeller` (onLoad, My Resale Listings & Seller Dashboard)

**Where the user goes next**

- → `ADM-298` My Tickets & Resale Marketplace Entry: *Returns to the board's landing screen*; calls `listResaleListingSeller`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resale listings seller list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resale listings seller untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resale listings seller yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the resale listings seller are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listResaleListingSeller` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Resale listing dashboard with active / sold / expired / pending listings. Qossai: resale is expected almost exclusively for event tickets (concerts, sports), not open-dated admission tickets. *(client request · MoM 1 Sep 2026, 4.14 Resale Marketplace - Detailed Follow-Up · DI-622)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S5** Resale marketplace *(Chinmay Parab · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'resale')*
- **A210** Build the resale marketplace across three access models (client B2C site · TICVAI white-label portal · API into a client's own market) with eligibility, price range, commission, approval, ownership transfer, seller … *(Softlabs Team · High · Ongoing → 30 Sep: Closed, Rolled into S5 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **A211** Preserve the original virtual ticket ID through a resale, changing only owner and media, with a separate ownership change-log table *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S5 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **C36** Share the resale marketplace screens and documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **A213** Obtain the outstanding module documentation from Allam (pricing, upgrades, orders/reservations, resale, full access control boards) *(Allam · High · With client → 30 Sep: Closed, Rolled into S5 · 2 Sep 2026 · workshop tracker · keyword 'resale')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-302` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS170 Ticket Resale Marketplace Board 3.dc.html#adm-302`
- Workshop pack: Ticket Resale Marketplace_Reference.pdf board 3
- Flow F173 *Ticket Resale Marketplace board 3: My Tickets & Resale Marketplace Entry*, step 8: Works in My Resale Listings & Seller Dashboard → Give sellers a dedicated self-service workspace to manage their resale activity after publishing.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-302?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-298`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-303` Official Resale Marketplace & Buyer Discovery

**Provide buyers with a trusted client-branded marketplace for discovering authentic resale inventory.**

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
| Route | `/commercial/official-resale-marketplace-buyer-discovery-adm-303` |

**Known gaps.** **The pack names 7 actions on this screen and the screen declares 1 operation.** Unserved: Event, Venue, Ticket Type, Price, Quantity, Primary only. Each needs an operation, or needs removing from … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Event (primary button) | navigation or local | — | — | — | — |
| Venue (secondary button) | navigation or local | — | — | — | — |
| Ticket Type (secondary button) | navigation or local | — | — | — | — |
| Price (secondary button) | navigation or local | — | — | — | — |
| Quantity (secondary button) | navigation or local | — | — | — | — |
| Resale only (secondary button) | navigation or local | — | — | — | — |
| Primary only (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listOfficialResaleMarketplace` (onLoad, Official Resale Marketplace & Buyer Discovery)

**Where the user goes next**

- → `ADM-298` My Tickets & Resale Marketplace Entry: *Returns to the board's landing screen*; calls `listOfficialResaleMarketplace`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The official resale marketplace list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the official resale marketplace untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No official resale marketplace yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the official resale marketplace are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listOfficialResaleMarketplace` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- White-label resale page: guest lists a ticket and sets a price within the allowed range; buyer searches, browses and receives the new ticket after purchase; the resale summary shows the market fee TICVAI retains. *(client request · MoM 1 Sep 2026, 4.14 Resale Marketplace - Board 3 · DI-621)*
- Three resale access models: (1) the client's own B2C site, where a guest requests resale within an admin-set price range (e.g. 10-20% below original); (2) a TICVAI-hosted white-label resale portal (e.g. museum.tickvai.com) for clients without B2C; (3) API for clients' own resale markets. *(agreed · MoM 1 Sep 2026, 4.14 Resale Marketplace - Detailed Follow-Up · DI-618)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S5** Resale marketplace *(Chinmay Parab · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'resale')*
- **A210** Build the resale marketplace across three access models (client B2C site · TICVAI white-label portal · API into a client's own market) with eligibility, price range, commission, approval, ownership transfer, seller … *(Softlabs Team · High · Ongoing → 30 Sep: Closed, Rolled into S5 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **A211** Preserve the original virtual ticket ID through a resale, changing only owner and media, with a separate ownership change-log table *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S5 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **C36** Share the resale marketplace screens and documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **A213** Obtain the outstanding module documentation from Allam (pricing, upgrades, orders/reservations, resale, full access control boards) *(Allam · High · With client → 30 Sep: Closed, Rolled into S5 · 2 Sep 2026 · workshop tracker · keyword 'resale')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-303` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS170 Ticket Resale Marketplace Board 3.dc.html#adm-303`
- Workshop pack: Ticket Resale Marketplace_Reference.pdf board 3
- Flow F173 *Ticket Resale Marketplace board 3: My Tickets & Resale Marketplace Entry*, step 10: Works in Official Resale Marketplace & Buyer Discovery → Provide buyers with a trusted client-branded marketplace for discovering authentic resale inventory.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-303?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Event, Venue, Ticket Type, Price, Quantity, Resale only, Primary only.
- [ ] Every transition is wired: `ADM-298`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-304` Resale Ticket Detail, Seat Selection & Primary-vs-Resale Experience

**Allow customers to understand exactly what they are purchasing and distinguish resale inventory from primary inventory.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `ORDER_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/resale-ticket-detail-seat-selection-primary-vs-resale-ex-adm-304` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every resale ticket detail** (data table, from `listResaleTicketDetail`)

| Shows | Format | Notes |
|---|---|---|
| Event | text | Event |
| Venue | text | Venue |
| Performance | text | Performance |
| Ticket type | text | Ticket Type |
| Section | text | Section |
| Row | text | Row |
| Seat | text | Seat |
| Accessibility attributes | 1,234 | Accessibility attributes |
| Applicable benefits | 1,234 | Applicable benefits |
| Resale price | AED 1,234.50 | Resale Price |
| Fees | 1,234 | Fees |
| Applicable restrictions | 1,234 | Applicable restrictions |

**The selected resale ticket detail** (detail panel): The pack groups this record's detail under its own headings: “Reserved Seating”, “Unavailable”, “AED 195”, “Important Commercial Benefit”, “Listing Availability”.

| Shows | Format | Notes |
|---|---|---|
| Event | text | Event |
| Venue | text | Venue |
| Performance | text | Performance |
| Ticket type | text | Ticket Type |
| Section | text | Section |
| Row | text | Row |
| Seat | text | Seat |
| Accessibility attributes | 1,234 | Accessibility attributes |
| Applicable benefits | 1,234 | Applicable benefits |
| Resale price | AED 1,234.50 | Resale Price |
| Fees | 1,234 | Fees |
| Applicable restrictions | 1,234 | Applicable restrictions |

**Data it reads**: `listResaleTicketDetail` (onLoad, Resale Ticket Detail, Seat Selection & Primary-vs-Resale …)

**Where the user goes next**

- → `ADM-298` My Tickets & Resale Marketplace Entry: *Returns to the board's landing screen*; calls `listResaleTicketDetail`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resale ticket detail list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resale ticket detail untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resale ticket detail yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the resale ticket detail are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listResaleTicketDetail` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- White-label resale page: guest lists a ticket and sets a price within the allowed range; buyer searches, browses and receives the new ticket after purchase; the resale summary shows the market fee TICVAI retains. *(client request · MoM 1 Sep 2026, 4.14 Resale Marketplace - Board 3 · DI-621)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S5** Resale marketplace *(Chinmay Parab · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'resale')*
- **C18** Locate and share the AutoCAD/PDF seating drawing from the Bahrain project (also to be shared with 3D vendor "3DDV") *(Allam · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'seating')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **A102** Build a single unified seat map builder screen (section type as a section-level attribute — seated / zone / standing / suite — mixed types in one map, suites sold bulk or by seat) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'seat map')*
- **A104** Make best-seat ranking configurable per map/event and implement section-wise holds rather than freeform polygon selection *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'best-seat')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-304` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS170 Ticket Resale Marketplace Board 3.dc.html#adm-304`
- Workshop pack: Ticket Resale Marketplace_Reference.pdf board 3
- Flow F173 *Ticket Resale Marketplace board 3: My Tickets & Resale Marketplace Entry*, step 12: Works in Resale Ticket Detail, Seat Selection & Primary-vs-Resale Experience → Allow customers to understand exactly what they are purchasing and distinguish resale inventory from primary inventory.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-304?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-298`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-305` Buyer Checkout, Inventory Hold & Secure Payment

**Provide a normal, secure TICVAI checkout while protecting the resale listing from simultaneous purchase.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `ORDER_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Select Resale Ticket) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/buyer-checkout-inventory-hold-secure-payment-adm-305` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| ↓ | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listBuyerCheckoutInventory` (onLoad, Buyer Checkout, Inventory Hold & Secure Payment)

**Where the user goes next**

- → `ADM-298` My Tickets & Resale Marketplace Entry: *Returns to the board's landing screen*; calls `listBuyerCheckoutInventory`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The buyer checkout inventory configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the buyer checkout inventory untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No buyer checkout inventory configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listBuyerCheckoutInventory` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- White-label resale page: guest lists a ticket and sets a price within the allowed range; buyer searches, browses and receives the new ticket after purchase; the resale summary shows the market fee TICVAI retains. *(client request · MoM 1 Sep 2026, 4.14 Resale Marketplace - Board 3 · DI-621)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker · keyword 'ticket-booking ux')*
- **A46** Evaluate a dynamic bundle/package builder that auto-applies a discount when a guest adds multiple product types (ticket + F&B + retail) to cart, in addition to pre-defined packages *(Reshma Bandiwdekar · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'cart')*
- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A96** Build the journey library (abandoned cart with min-value/product filters, birthday, anniversary, cross-sell, survey — all consent-gated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'cart')*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'b2c checkout')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-305` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS170 Ticket Resale Marketplace Board 3.dc.html#adm-305`
- Workshop pack: Ticket Resale Marketplace_Reference.pdf board 3
- Flow F173 *Ticket Resale Marketplace board 3: My Tickets & Resale Marketplace Entry*, step 14: Works in Buyer Checkout, Inventory Hold & Secure Payment → Provide a normal, secure TICVAI checkout while protecting the resale listing from simultaneous purchase.

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-305?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-298`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-306` Resale Confirmation, Ownership Transfer & Ticket Delivery

**Provide the customer-facing completion experience after successful payment while the backend performs the secure entitlement transfer.**

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
| Route | `/commercial/resale-confirmation-ownership-transfer-ticket-delivery-adm-306` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listResaleConfirmationOwnership` (onLoad, Resale Confirmation, Ownership Transfer & Ticket Delivery)

**Where the user goes next**

- → `ADM-298` My Tickets & Resale Marketplace Entry: *Returns to the board's landing screen*; calls `listResaleConfirmationOwnership`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resale confirmation ownership list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resale confirmation ownership untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resale confirmation ownership yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the resale confirmation ownership are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listResaleConfirmationOwnership` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- White-label resale page: guest lists a ticket and sets a price within the allowed range; buyer searches, browses and receives the new ticket after purchase; the resale summary shows the market fee TICVAI retains. *(client request · MoM 1 Sep 2026, 4.14 Resale Marketplace - Board 3 · DI-621)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S5** Resale marketplace *(Chinmay Parab · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'resale')*
- **A210** Build the resale marketplace across three access models (client B2C site · TICVAI white-label portal · API into a client's own market) with eligibility, price range, commission, approval, ownership transfer, seller … *(Softlabs Team · High · Ongoing → 30 Sep: Closed, Rolled into S5 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **A211** Preserve the original virtual ticket ID through a resale, changing only owner and media, with a separate ownership change-log table *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S5 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **C36** Share the resale marketplace screens and documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 1 Sep 2026 · workshop tracker · keyword 'resale')*
- **A213** Obtain the outstanding module documentation from Allam (pricing, upgrades, orders/reservations, resale, full access control boards) *(Allam · High · With client → 30 Sep: Closed, Rolled into S5 · 2 Sep 2026 · workshop tracker · keyword 'resale')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-306` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS170 Ticket Resale Marketplace Board 3.dc.html#adm-306`
- Workshop pack: Ticket Resale Marketplace_Reference.pdf board 3
- Flow F173 *Ticket Resale Marketplace board 3: My Tickets & Resale Marketplace Entry*, step 16: Works in Resale Confirmation, Ownership Transfer & Ticket Delivery → Provide the customer-facing completion experience after successful payment while the backend performs the secure entitlement transfer.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-306?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-298`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-307` White-Label Marketplace Deployment & Experience Architecture

**This is the key architecture/configuration screen It defines how each TICVAI client chooses to expose the resale marketplace to its customers. Deployment Model A — Embedded White-Label**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `ORDER_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/white-label-marketplace-deployment-experience-architectu-adm-307` |

**Known gaps.** **The pack names 8 actions on this screen and the screen declares 1 operation.** Unserved: Domain configuration, Analytics, Additional client languages, Secure sessions, Fraud integration, Data …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Marketplace Name | select field | — | — | — | — | — | — |
| Client Logo | select field | — | — | — | — | — | — |
| Brand Colors | select field | — | — | — | — | — | — |
| Typography | select field | — | — | — | — | — | — |
| Domain/Subdomain | select field | — | — | — | — | — | — |
| Support Contact | select field | — | — | — | — | — | — |
| Legal Links | select field | — | — | — | — | — | — |
| Seller Terms | select field | — | — | — | — | — | — |
| Buyer Terms | select field | — | — | — | — | — | — |
| Privacy | select field | — | — | — | — | — | — |
| Languages | select field | — | — | — | — | — | — |
| Authentication method | select field | — | — | — | — | — | — |
| My Tickets | select field | — | — | — | — | — | — |
| Sell | select field | — | — | — | — | — | — |
| Buy | select field | — | — | — | — | — | — |
| My Listings | select field | — | — | — | — | — | — |
| Transactions | select field | — | — | — | — | — | — |
| Settlements | select field | — | — | — | — | — | — |
| Help | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Domain configuration (primary button) | navigation or local | — | — | — | — |
| Analytics (secondary button) | navigation or local | — | — | — | — |
| Additional client languages (secondary button) | navigation or local | — | — | — | — |
| Secure sessions (secondary button) | navigation or local | — | — | — | — |
| Fraud integration (secondary button) | navigation or local | — | — | — | — |
| Data protection (secondary button) | navigation or local | — | — | — | — |
| Session expiry (secondary button) | navigation or local | — | — | — | — |
| Audit logging (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listWhiteLabelMarketplace` (onLoad, White-Label Marketplace Deployment & Experience Architecture)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The white-label marketplace deployment configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the white-label marketplace deployment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No white-label marketplace deployment configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listWhiteLabelMarketplace` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Three resale access models: (1) the client's own B2C site, where a guest requests resale within an admin-set price range (e.g. 10-20% below original); (2) a TICVAI-hosted white-label resale portal (e.g. museum.tickvai.com) for clients without B2C; (3) API for clients' own resale markets. *(agreed · MoM 1 Sep 2026, 4.14 Resale Marketplace - Detailed Follow-Up · DI-618)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-307` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS170 Ticket Resale Marketplace Board 3.dc.html#adm-307`
- Workshop pack: Ticket Resale Marketplace_Reference.pdf board 3
- Flow F173 *Ticket Resale Marketplace board 3: My Tickets & Resale Marketplace Entry*, step 18: Works in White-Label Marketplace Deployment & Experience Architecture → This is the key architecture/configuration screen It defines how each TICVAI client chooses to expose the resale marketplace to its customers. Deployment Model A — Embedded White-Label

#### Acceptance for the design

- [ ] Every input above is drawn (19), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-307?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Domain configuration, Analytics, Additional client languages, Secure sessions, Fraud integration, Data protection, Session expiry, Audit logging.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
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

**13 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"listBuyerCheckoutInventory": {"method":"GET","path":"/buyer-checkout-inventory","contract":"orders","summary":"Buyer Checkout, Inventory Hold & Secure Payment","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"BuyerCheckoutInventoryHoldSecurePaymentView"},
"listCreateListingResale": {"method":"GET","path":"/create-listing-resale","contract":"orders","summary":"Create Listing & Resale Price Selection","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CreateListingResalePriceSelectionView"},
"listFeeSellerProceed": {"method":"GET","path":"/fee-seller-proceed","contract":"orders","summary":"Fees, Seller Proceeds & Listing Confirmation","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"FeesSellerProceedsListingConfirmationView"},
"listOfficialResaleMarketplace": {"method":"GET","path":"/official-resale-marketplace","contract":"orders","summary":"Official Resale Marketplace & Buyer Discovery","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"OfficialResaleMarketplaceBuyerDiscoveryView"},
"listResaleConfirmationOwnership": {"method":"GET","path":"/resale-confirmation-ownership","contract":"orders","summary":"Resale Confirmation, Ownership Transfer & Ticket Delivery","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ResaleConfirmationOwnershipTransferTicketDeliveryView"},
"listResaleEligibilityTicket": {"method":"GET","path":"/resale-eligibility-ticket","contract":"orders","summary":"Resale Eligibility & Ticket Selection","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ResaleEligibilityTicketSelectionView"},
"listResaleListingSeller": {"method":"GET","path":"/resale-listing-seller","contract":"orders","summary":"My Resale Listings & Seller Dashboard","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MyResaleListingsSellerDashboardView"},
"listResaleTicketDetail": {"method":"GET","path":"/resale-ticket-detail","contract":"orders","summary":"Resale Ticket Detail, Seat Selection & Primary-vs-Resale Experience","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ResaleTicketDetailSeatSelectionPrimaryVsResaleExperiView"},
"listTicketResaleMarketplace": {"method":"GET","path":"/ticket-resale-marketplace","contract":"orders","summary":"My Tickets & Resale Marketplace Entry","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MyTicketsResaleMarketplaceEntryView"},
"listWhiteLabelMarketplace": {"method":"GET","path":"/white-label-marketplace","contract":"orders","summary":"White-Label Marketplace Deployment & Experience Architecture","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WhiteLabelMarketplaceDeploymentExperienceArchitecturView"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"BuyerCheckoutInventoryHoldSecurePaymentView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Buyer Checkout, Inventory Hold & Secure Payment displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"name":{"type":"string","description":"Name"},"email":{"type":"string","description":"Email"},"mobile":{"type":"string","description":"Mobile"},"billingDetails":{"type":"string","description":"Billing details"},"requiredParticipantInformation":{"type":"string","description":"Required participant information"},"holdExpiresAt":{"type":"string","format":"date-time","description":"When the inventory hold ends"},"total":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Total payable"}}},
"CreateListingResalePriceSelectionView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Create Listing & Resale Price Selection displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"pricingMode":{"type":"string","enum":["faceValueOnly","fixedPrice","sellerSelectedPrice","cappedPrice","operatorControlled","aiRecommendedPrice"],"description":"How the seller prices the listing."},"recommendedPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Recommended price"},"minimumPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Permitted minimum"},"maximumPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Permitted maximum"}}},
"FeesSellerProceedsListingConfirmationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Fees, Seller Proceeds & Listing Confirmation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"marketplaceTerms":{"type":"integer","description":"Marketplace Terms"},"sellerTerms":{"type":"integer","description":"Seller Terms"},"cancellationPolicy":{"type":"string","description":"Cancellation Policy"},"settlementConditions":{"type":"integer","description":"Settlement Conditions"},"eventCancellationTreatment":{"type":"string","description":"Event Cancellation Treatment"},"applicablePrivacyNotice":{"type":"string","description":"Applicable privacy notice"},"sellingPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Selling price"},"fee":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Fee"},"estimatedProceeds":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Estimated seller proceeds"},"termsVersion":{"type":"string","description":"Terms version the seller accepts; stored with the acceptance"}}},
"MyResaleListingsSellerDashboardView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What My Resale Listings & Seller Dashboard displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"activeListings":{"type":"integer","description":"Active Listings"},"pendingApproval":{"type":"integer","description":"Pending Approval"},"sold":{"type":"string","description":"Sold"},"expiringSoon":{"type":"string","description":"Expiring Soon"},"sellerProceeds":{"type":"integer","description":"Seller Proceeds"},"pendingSettlement":{"type":"integer","description":"Pending Settlement"},"paidSettlements":{"type":"integer","description":"Paid Settlements"},"event":{"type":"string","description":"Event"},"date":{"type":"string","format":"date-time","description":"Date"},"seat":{"type":"string","description":"Seat"},"listingPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Listing Price"},"originalPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Original Price"},"marketplaceStatus":{"type":"string","description":"Marketplace Status"},"listingDate":{"type":"string","format":"date-time","description":"Listing Date"},"expiry":{"type":"string","format":"date-time","description":"Expiry"},"settlementStatus":{"type":"string","description":"Settlement Status"},"settlementScheduledAfterEvent":{"type":"string","format":"date-time","description":"Settlement: Scheduled after event"},"views":{"type":"string","description":"Views where applicable"}}},
"MyTicketsResaleMarketplaceEntryView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What My Tickets & Resale Marketplace Entry displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"eventProduct":{"type":"string","description":"Event/Product"},"venue":{"type":"string","description":"Venue"},"dateTime":{"type":"string","format":"date-time","description":"Date/Time"},"ticketType":{"type":"string","description":"Ticket Type"},"sectionRowSeat":{"type":"string","description":"Section/Row/Seat"},"ticketHolder":{"type":"string","description":"Ticket Holder"},"virtualTicketIdReference":{"type":"string","description":"Virtual Ticket ID reference"},"ticketStatus":{"type":"string","description":"Ticket Status"},"resaleStatus":{"type":"string","description":"Resale Status"},"availableActions":{"type":"string","description":"Available Actions"},"clientLogo":{"type":"string","description":"Client logo"},"brand":{"type":"string","description":"Brand"},"colors":{"type":"string","description":"Colors"},"typography":{"type":"string","description":"Typography"},"language":{"type":"string","description":"Language"},"supportDetails":{"type":"string","description":"Support details"},"marketplaceName":{"type":"string","description":"Marketplace name"},"authenticationMethod":{"type":"string","enum":["customerAccount","sso","passwordlessLogin","otp","appAuthentication"],"description":"How the guest signs in to the marketplace"}}},
"OfficialResaleMarketplaceBuyerDiscoveryView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Official Resale Marketplace & Buyer Discovery displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"event":{"type":"string","description":"Event"},"venue":{"type":"string","description":"Venue"},"date":{"type":"string","format":"date-time","description":"Date"},"performance":{"type":"string","description":"Performance"},"ticketType":{"type":"string","description":"Ticket Type"},"section":{"type":"string","description":"Section"},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Price"},"quantity":{"type":"integer","description":"Quantity"},"accessibility":{"type":"string","description":"Accessibility"},"name":{"type":"string","description":"Name"},"email":{"type":"string","description":"Email"},"mobile":{"type":"string","description":"Mobile"},"address":{"type":"string","description":"Address"},"paymentInformation":{"type":"string","description":"Payment information"},"inventoryFilter":{"type":"string","enum":["officialTicketsOfficialResale","resaleOnly","primaryOnly"],"description":"Which inventory the buyer sees."}}},
"ResaleConfirmationOwnershipTransferTicketDeliveryView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Resale Confirmation, Ownership Transfer & Ticket Delivery displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"dynamicQr":{"type":"string","description":"Dynamic QR"},"mobileTicket":{"type":"string","description":"Mobile Ticket"},"appleWallet":{"type":"string","description":"Apple Wallet"},"googleWallet":{"type":"string","description":"Google Wallet"},"otherSupportedCredentialMedia":{"type":"string","description":"Other supported credential media"},"rfidNfcAssignment":{"type":"string","description":"RFID/NFC assignment where applicable"},"ticketId":{"type":"string","description":"Ticket ID, unchanged through the resale (MoM 1 Sep)"},"currentOwner":{"type":"string","description":"Current owner"},"previousOwner":{"type":"string","description":"Previous owner"},"settlementStatus":{"type":"string","description":"Seller settlement status"}}},
"ResaleEligibilityTicketSelectionView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Resale Eligibility & Ticket Selection displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ticketOwnership":{"type":"string","description":"Ticket ownership"},"paymentStatus":{"type":"string","description":"Payment status"},"ticketValidity":{"type":"string","description":"Ticket validity"},"scanUseStatus":{"type":"string","description":"Scan/use status"},"eventStatus":{"type":"string","description":"Event status"},"resaleWindow":{"type":"string","format":"date-time","description":"Resale window"},"ticketType":{"type":"string","description":"Ticket type"},"product":{"type":"string","description":"Product"},"promotionRestrictions":{"type":"string","description":"Promotion restrictions"},"membershipRestrictions":{"type":"string","description":"Membership restrictions"},"existingListing":{"type":"string","description":"Existing listing"},"fraudSecurityHold":{"type":"string","description":"Fraud/security hold"},"event":{"type":"string","description":"Event"},"date":{"type":"string","format":"date-time","description":"Date"},"venue":{"type":"string","description":"Venue"},"seat":{"type":"string","description":"Seat"},"originalPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Original price"},"resaleClosingTime":{"type":"string","format":"date-time","description":"Resale closing time"},"applicableMarketplaceConditions":{"type":"integer","description":"Applicable marketplace conditions"},"sellingMode":{"type":"string","enum":["sellIndividually","sellSelectedTickets","sellTogetherOnly","adjacentSeatGroup"],"description":"How the tickets may be sold."}}},
"ResaleTicketDetailSeatSelectionPrimaryVsResaleExperiView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Resale Ticket Detail, Seat Selection & Primary-vs-Resale Experience displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"event":{"type":"string","description":"Event"},"venue":{"type":"string","description":"Venue"},"performance":{"type":"string","description":"Performance"},"ticketType":{"type":"string","description":"Ticket Type"},"section":{"type":"string","description":"Section"},"row":{"type":"string","description":"Row"},"seat":{"type":"string","description":"Seat"},"accessibilityAttributes":{"type":"integer","description":"Accessibility attributes"},"applicableBenefits":{"type":"integer","description":"Applicable benefits"},"resalePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Resale Price"},"fees":{"type":"integer","description":"Fees"},"applicableRestrictions":{"type":"integer","description":"Applicable restrictions"},"primaryInventoryResaleInventory":{"type":"string","description":"Primary Inventory + Resale Inventory"},"originalFaceValue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Original face value"},"listingSource":{"type":"string","enum":["primary","resale"],"description":"Primary or resale inventory, shown distinctly"}}},
"WhiteLabelMarketplaceDeploymentExperienceArchitecturView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What White-Label Marketplace Deployment & Experience Architecture displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"embeddedPages":{"type":"string","description":"Embedded pages"},"embeddedComponents":{"type":"string","description":"Embedded components"},"clientNavigation":{"type":"string","description":"Client navigation"},"clientAuthentication":{"type":"string","description":"Client authentication"},"ssoSessionPassing":{"type":"string","description":"SSO/session passing"},"clientBranding":{"type":"string","description":"Client branding"},"domainConfiguration":{"type":"string","description":"Domain configuration"},"analytics":{"type":"string","description":"Analytics"},"localization":{"type":"string","description":"Localization"},"deepLinking":{"type":"string","description":"Deep linking"},"mobileResponsiveBehavior":{"type":"string","description":"Mobile responsive behavior"},"marketplaceName":{"type":"string","description":"Marketplace Name"},"clientLogo":{"type":"string","description":"Client Logo"},"brandColors":{"type":"string","description":"Brand Colors"},"typography":{"type":"string","description":"Typography"},"domainSubdomain":{"type":"string","description":"Domain/Subdomain"},"supportContact":{"type":"string","description":"Support Contact"},"legalLinks":{"type":"string","description":"Legal Links"},"sellerTerms":{"type":"string","description":"Seller Terms"},"buyerTerms":{"type":"string","description":"Buyer Terms"},"privacy":{"type":"string","description":"Privacy"},"languages":{"type":"string","description":"Languages"},"authenticationMethod":{"type":"string","description":"Authentication method"},"deploymentModel":{"type":"string","enum":["embeddedWhiteLabel","ticvaiHostedWhiteLabel","headlessApi"],"description":"Deployment model (MoM 1 Sep: own B2C site, TICVAI-hosted portal, API)"},"navigation":{"type":"array","items":{"type":"string","enum":["myTickets","sell","buy","myListings","transactions"]},"description":"Marketplace navigation"}}}
}
```
