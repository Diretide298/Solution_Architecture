# P01-ticketing-01 — P01 · Ticketing

**3 screens · 14 operations · 32 schemas · 6 permissions**

Platform P01 Guest Web · ships as **guest** ·
guest audience · web ·
online only

## Who this is for

**guest on web.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 6 permissions apply here:
  `LEDGER_VIEW, ORDER_CANCEL, ORDER_CREATE, ORDER_VIEW, PRODUCT_VIEW, RESOURCE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store. Offline, a screen shows what was already loaded, under the banner below.
- **Offline, every screen shows one banner, the same on web and app:** *"You're offline. Connect to the internet to book, pay, order or join a queue."* The moment the connection drops, on every screen, above the screen's own content. By itself as soon as the connection is back, with a short "Back online" confirmation. **It never** Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing. Each screen's `states.offline` says what stays on screen and what waits.
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


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `WEB-030` | Ticket Transfer | A | 8 | 6 | 6 | 5 | 3 | 0 | guest | review (client-verified) |
| `WEB-031` | My Reservations | A | 27 | 44 | 6 | 35 | 9 | 0 | guest | review (client-verified) |
| `WEB-035` | Multi-Currency & Pricing | A | 1 | 27 | 6 | 12 | 3 | 4 | guest | review (client-verified) |

## Thin screens in this batch

**WEB-030 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `WEB-030` Ticket Transfer

**Send a ticket to someone else, and see what you have sent.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Ticketing · wave 1 · needs the `ticketing` module |
| Block | Block A · ticket #17924 (APP-WEB-WEB-030) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025); in the flows as guest |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · the venue's theme |
| Pattern | listDetail (compact density): `listOrders` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **The offline banner shows.** Sending, claiming and listing for resale need the connection — a transfer nobody received is a ticket nobody holds. Tickets already loaded stay visible. |
| Opens with | `subjectId` (session), `orderId` (deepLink), `transferId` (deepLink) · cold entry: **A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the … |
| Route | `/ticket-transfer` |

**What the spec says about it.** Added 17 August for parity with GST-014. **Not on the wireframe board** — needs drawing. CF-93.

**Known gaps.** The staff-scoped order list; a guest screen lists the caller's own orders with `listMyOrders` (removed from guest screens on 24 August, back with the 31 August parity pass). The recipient claims from the link (GST-014 or a claim landing); the token is never typed on the sender's screen.

**From the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process.** Send tickets to someone else and see what you have sent. Block A. Per ticket, not per order (a family splitting tickets between phones is the normal case); ownership moves only when the friend claims the link, so a mistyped address expires rather than losing the ticket.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Not on the wireframe board. (CHG-SGU-026)

**Fixed on main** (the package already carries these; draw what it says): Staff list filters "Venue id", "Principal id", "Shift id", "Status", created from/to over listOrders. (CHG-GST-003); "Claim ticket transfer" sits on the sender's screen with a claimToken form. (CHG-GST-003).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Since | date picker | — | — | `listMyOrders` ?since |

**Form: Create resale listing** (modal, opened by *Create resale listing*; *Create resale listing* calls `createResaleListing`, *Cancel* sends nothing)

**Collects what `createResaleListing` sends before it is called.** Required: `entitlementId`, `askPrice`. Optional: `sellerSubjectId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Entitlement `entitlementId` | picker: choose an entitlement | required | — | — | shows names, sends the id | — | `createResaleListing` body |
| Ask price `askPrice` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createResaleListing` body |
| Seller subject `sellerSubjectId` | picker: choose a seller subject | optional | — | — | shows names, sends the id | The holder listing it. A guest caller is always the seller and may name only themselves; a member of staff listing on a guest's behalf names the guest. | `createResaleListing` body |

Errors to draw in the form: 409 Not resellable, and the reason says which — partly consumed (`partlyConsumed`), name-bound (`nameBound`), or outside the resale window (`outsideResaleWindow`) … (ResaleRefusedProblem)

**Form: Transfer tickets** (modal, opened by *Transfer tickets*; *Transfer tickets* calls `transferOrderTickets`, *Cancel* sends nothing)

**Pick the tickets on their cards, then the friend**: a channel (email, SMS or WhatsApp) and the address, with an optional message. `transferOrderTickets` moves ownership; the recipient claims from the link they receive.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Tickets `ticketIds` | multi-picker: choose tickets | required | — | at least 1 | — | The entitlements to hand over. A ticket is an entitlement, so each value is an `Entitlement.id` on this order — the ids in `OrderLine.entitlementIds`. | `transferOrderTickets` body |
| Recipient `recipient` | group | required | — | — | — | — | `transferOrderTickets` body |
| Channel `recipient.channel` | segmented control | required | — | Email · SMS · Whatsapp | — | — | `transferOrderTickets` body |
| Address `recipient.address` | text field | required | — | — | — | — | `transferOrderTickets` body |
| Message `message` | text area | optional | — | max length 500 | — | — | `transferOrderTickets` body |

Errors to draw in the form: 409 Ticket already redeemed (`alreadyRedeemed`), already offered (`alreadyOffered`), or the product forbids transfer (`transferNotAllowed`). (TicketTransferProblem)

**Rules for these inputs** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **tickets**: Tick the individual tickets of an order (guest type and date shown); used, name-bound or already-offered tickets are disabled with the reason. *(source: contracts/spine/orders.yaml#transferOrderTickets)*
- **recipient**: Channel (email, SMS, WhatsApp) and the address; a message up to 500 characters. *(source: contracts/spine/orders.yaml#transferOrderTickets)*

#### Outputs: what the screen shows and produces

**Shown**

**Your orders with tickets** (card list, from `listMyOrders`): Was the generated table 'Every order'; staff and plumbing columns removed (decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-3)).

| Shows | Format | Notes |
|---|---|---|
| Order number | text | The number a guest reads and a cashier types. Server-assigned: the venue prefix and a sequence per venue, for example `DXB1-000123` … |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Lines | list or chips (count when long) | — |
| Created at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Transfer tickets (primary button) | `transferOrderTickets` POST `/orders/{orderId}/transfer` | inline | TicketTransfer | 409 Ticket already redeemed (`alreadyRedeemed`), already offered (`alreadyOffered`), or the product forbids transfer (`transferNotAllowed`). (TicketTransferProblem) | opens modal first; produces a document or message: Transfer tickets to another guest |
| Create resale listing (secondary button) | `createResaleListing` POST `/resale-listings` | CreateResaleListingRequest | ResaleListing | 409 Not resellable, and the reason says which — partly consumed (`partlyConsumed`), name-bound (`nameBound`), or outside the resale window (`outsideResaleWindow`) … (ResaleRefusedProblem) | opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **sent transfers**: Each with tickets, masked recipient, status in guest words (Waiting to be claimed, Claimed, Expired and returned to you, Cancelled) and when an unclaimed offer expires. *(source: contracts/spine/orders.yaml#/components/schemas/TicketTransfer)*

**What each action does** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **Send**: The friend gets a claim link; the tickets show "Offered to s•••@example.com" until claimed. *(source: F55 step 4)*
- **Cancel transfer**: Allowed while unclaimed; the tickets come back at once. *(source: screens/P01-guest-web-storefront.yaml#WEB-030 wireframe.prototype.differences)*
- **Sell on resale**: Lists a ticket at an asking price within the venue's resale window; the ticket ID stays and the buyer gets new media, so the seller's QR stops working once sold. Refused for partly used or name-bound tickets. *(source: contracts/spine/orders.yaml#createResaleListing; TRACKER 30-September Old rows row 146 (A211))*

**Data it reads**: `listMyOrders` (onLoad, The orders this guest placed)

**Where the user goes next**

- → `WEB-031` My Reservations: *My Reservations*
- → `GST-014` Ticket Transfer: *The friend claims it in the app*; carries `orderId`, `transferId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The ticket transfer list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the ticket transfer untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No ticket transfer yet. Offers Create resale listing (`createResaleListing`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, principalId, shiftId, status, createdFrom, createdTo and the ticket transfer are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the … |
| Offline (`?state=offline`) | **The offline banner shows.** Sending, claiming and listing for resale need the connection — a transfer nobody received is a ticket nobody holds. Tickets already loaded stay visible. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Not resellable, and the reason says which — partly consumed (`partlyConsumed`), name-bound (`nameBound`), or outside the resale window (`outsideResaleWindow`) … (ResaleRefusedProblem); 409 Ticket already redeemed (`alreadyRedeemed`), already offered (`alreadyOffered`), or the product forbids transfer (`transferNotAllowed`). (TicketTransferProblem) |

#### Edge cases to draw

- **A dynamic-QR ticket bound to the sender's device**: The transfer moves the credential to the recipient's device and the sender's copy stops admitting; the copy says so before sending. *(source: DI-636)*

#### Consistency with other screens

- Match `GST-014`: The friend claims in the app (GST-014); the sender's view and statuses match.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
order: YAS1-000123
tickets:
- 2 park ticket · Adult · Fri 2 Oct (1 of 3)
- 2 park ticket · Adult · Fri 2 Oct (2 of 3)
recipient: WhatsApp +971 55 ••• 0198
message: Enjoy the day, see you at the gate!
```

#### Permissions

- `transferOrderTickets` → no permission · guest
- `listMyOrders` → no permission · guest
- `createResaleListing` → `ORDER_CREATE` (operate) · staff, guest

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the …

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.13 | Ticket Transfer - System shall support ticket transfers. | Guest Mobile App & Branding | CONTRACTED | `transferOrderTickets` |
| 1.1.27 | System shall support ticket ownership transfer between guests according to configurable policies, fees and approval workflows. | Ticketing Catalogue | CONTRACTED | `transferOrderTickets` |
| 1.6.17 | System shall expose marketplace functionality through APIs for websites, mobile applications, partner platforms, and third-party integrations. | Ticketing Catalogue | CONTRACTED | `transferOrderTickets` |
| 2.6.39 | Customer should have the ability to view the order transactions with all the details for the logged in users and should be able to resend the tickets / Transfer Tickets to Friend / Download tickets | Ticketing Sales | CONTRACTED | `transferOrderTickets` |
| 2.13.37 | Ticket Transfer & Reassignment | Ticketing Sales | CONTRACTED | `transferOrderTickets` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A purchased ticket can be transferred to another guest (e.g. a friend); the system keeps the original purchaser and full transfer history. *(client request · MoM 7 Sep 2026, 4.9 Ownership and transfer · DI-669)*
- Once activated in the app a digital ticket is bound to one approved device; moving to a new device requires deactivating the prior binding. Credential transfer moves a ticket to another person's device and invalidates the original holder's copy. *(client request · MoM 2 Sep 2026, 4.8 Device Binding, Credential Transfer & Revocation · DI-636)*
- Ticket transfer by email/SMS with optional message; either keep ownership and rename the holder, or transfer both ownership and holder. *(client request · MoM 10 Aug 2026, 4.3 B2C Guest App — End-to-End Booking Journey · DI-200)*

Also apply: 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-030` · status **review** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match partial): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html`, view *Account → 'Transfer & resale'; My tickets → Manage → 'Transfer ticket'; Confirmation → 'Transfer tickets'*. Differences: List pane with toast actions; no recipient form. Prototype adds cancel transfer and withdraw resale listing.
- Flow F55 *A guest buys on the web and transfers to a friend*, step 4: They transfer three tickets. → **Transferred, not forwarded.** A PDF sent by WhatsApp is a ticket sold four times.
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-030?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Transfer tickets, Create resale listing.
- [ ] Every transition is wired: `WEB-031`, `GST-014`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `WEB-031` My Reservations

**What you have booked and not yet paid for.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Ticketing · wave 2 · needs the `ticketing` module |
| Block | Block A · ticket #18162 (APP-WEB-WEB-031) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · the venue's theme |
| Pattern | listDetail (compact density): `listReservations` reads the population and `getReservation` reads one of them — list, select, act |
| Offline | **The offline banner shows.** Reservations already loaded stay visible with their age. Booking, changing and cancelling need the connection — a table held offline is a table two people think they have. |
| Opens with | `subjectId` (session), `reservationId` (deepLink), `groupBookingId` (navigation), `resourceId` (navigation), `productId` (navigation) · cold entry: **A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared ticket, a forwarded confirmation … |
| Route | `/my-reservations` |

**What the spec says about it.** Added 17 August for parity with GST-016. **Not on the wireframe board** — needs drawing. CF-93. **Rev 3 (decided 29 September).** **Table deposit (REV3-8b):** a dining deposit is a venue option, off unless the venue enables it in Venue Management (`DepositPolicy.dining`; amount and basis are the venue's), superseding audit R077 (a). A reservation holding a deposit shows its amount, when it stops being refundable (`refundableUntil`) and the late-cancel and no-show terms. Group booking on the web is this screen (`requestGroupBooking`; GAP-D3, already); school and party requests are unchanged (DG-4). **Two jobs, one id (GAP-D3, DI-1078; CHG-SGU-020).** This is My Reservations and the web's group-booking view. The group request form is a flow opened from here and from the booking listing, not a separate screen; the prototype labels that dialog WEB-031.

**From the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process.** The guest's reservations (booked, not yet paid: held bookings, table reservations with deposits, group requests) and, since 29 September, the web's Group Booking view. Block A. Get right the difference from My Tickets: a reservation holds capacity, expires and carries no money until paid.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- GroupBookingRequest.kind is general, school, corporate or party; the 30 September build shows Tour operator and Community as their own group types. (CHG-SGU-024)

**Fixed on main** (the package already carries these; draw what it says): The screen is named My Reservations but is also the web's Group Booking view (GAP-D3), and the prototype labels the group request dialog … (CHG-SGU-020); "Save table reservation" with a form exposing outletId, tables, status, tableVisitId, actualPartySize. (CHG-GST-003).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Are water-park groups booked into a session?** → Drawn default accepted: Group requests take a date and, for session products, a session. *(decided by Chinmay, 2026-10-02; DEC-121 / CHG-NOTE-007)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Kind | segmented control | optional | — | School · Party | — | Sends `?kind=` to `listGroupPackages`. | `listGroupPackages` ?kind |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Held · Converted · Expired · Cancelled | `listReservations` ?status |
| Expiring within minutes | number field (minutes) | — | min 1 | `listReservations` ?expiringWithinMinutes |

**Form: Request group booking** (modal, opened by *Request group booking*; *Request group booking* calls `requestGroupBooking`, *Cancel* sends nothing)

**Collects what `requestGroupBooking` sends before it is called.** Required: `kind`, `packageProductId`, `preferredDate`, `expectedSize`. Optional: `organisationName`, `yearGroup`, `accessAndDietaryNeeds`, `celebrantName`, `celebrantTurningAge`, `allergiesAndRequests`. Dismissing sends nothing; the screen behind is unchanged. **30 September (client feedback, CLIENT-RESPONSE-30SEP 1).** The group ticket is chosen first (`packageProductId`: cards with the per-person price and the minimum group size), then *How many people* (`expectedSize`) as a number box the guest types into or steps with − and + (+10 on the app); no Group size dropdown. The estimate reads *<ticket> · Guests × <n>*.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | radio group | required | — | General · School · Corporate · Party | — | — | `requestGroupBooking` body |
| Package product `packageProductId` | text field | required | — | — | — | — | `requestGroupBooking` body |
| Preferred date `preferredDate` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `requestGroupBooking` body |
| Expected size `expectedSize` | number field | required | — | min 2 | — | — | `requestGroupBooking` body |
| Organisation name `organisationName` | text field | optional | — | max length 200 | — | The school. | `requestGroupBooking` body |
| Year group `yearGroup` | text field | optional | — | max length 40 | — | — | `requestGroupBooking` body |
| Access and dietary needs `accessAndDietaryNeeds` | text area | optional | — | max length 1000 | — | — | `requestGroupBooking` body |
| Celebrant name `celebrantName` | text field | optional | — | max length 120 | — | The birthday child. | `requestGroupBooking` body |
| Celebrant turning age `celebrantTurningAge` | stepper or slider | optional | — | min 1; max 18 | — | — | `requestGroupBooking` body |
| Allergies and requests `allergiesAndRequests` | text area | optional | — | max length 1000 | — | — | `requestGroupBooking` body |

Errors to draw in the form: 409 The date is no longer available (`dateUnavailable`), or the package is not (`packageUnavailable`). (GroupBookingProblem); 422 More participants than the package allows (`aboveParticipantLimit`). (GroupBookingProblem)

**Form: Change reservation** (modal, opened by *Change reservation*; *Save* calls `updateTableReservation`, *Cancel* sends nothing)

**Party size and time, or cancel.** `updateTableReservation` with what the guest changed; the outlet, tables, status and visit are the venue's and never shown.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Outlet `outletId` | picker: choose an outlet | required | — | — | shows names, sends the id | — | `updateTableReservation` body |
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | — | `updateTableReservation` body |
| Guest name `guestName` | text field | optional | — | — | — | — | `updateTableReservation` body |
| Contact point `contactPoint` | text field | optional | — | — | — | — | `updateTableReservation` body |
| Party size `partySize` | number field | required | — | min 1 | — | — | `updateTableReservation` body |
| Starts at `startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateTableReservation` body |
| Duration minutes `durationMinutes` | number field (minutes) | optional | — | An outlet turning tables twice an evening needs this to be real, or the second sitting cannot be booked. | — | How long the cover is held. An outlet turning tables twice an evening needs this to be real, or the second sitting cannot be booked. | `updateTableReservation` body |
| Tables `tables` | repeatable rows | optional | — | — | — | The dining tables assigned to this reservation, one row each. Usually empty until seating. | `updateTableReservation` body |
| Reservation `tables[].reservationId` | picker: choose a reservation | required | — | — | shows names, sends the id | — | `updateTableReservation` body |
| Table `tables[].tableId` | picker: choose a table | required | — | — | shows names, sends the id | — | `updateTableReservation` body |
| Created at `tables[].createdAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateTableReservation` body |
| Status `status` | select | optional | — | Awaiting deposit · Booked · Confirmed · Seated · Completed · Cancelled · No show; `awaitingDeposit` only where the venue's dining deposit applies (decided 29 September, rev 3 REV3-8b); a booking with no deposit starts `booked`. | — | `awaitingDeposit` only where the venue's dining deposit applies (decided 29 September, rev 3 REV3-8b); a booking with no deposit starts `booked`. | `updateTableReservation` body |
| Group `groupId` | picker: choose a group | optional | — | — | shows names, sends the id | 5.1.2. Several bookings managed as one party across adjacent tables. | `updateTableReservation` body |
| Notes `notes` | text area | optional | — | — | — | Allergies, accessibility needs and other requests, as the guest wrote them. | `updateTableReservation` body |
| Seating preference `seatingPreference` | text field | optional | — | max length 64 | — | The seating area the guest asked for, e.g. indoor, terrace, majlis (Chinmay, 2 October, workbook Q204; DI-791; CHG-CSA-018). | `updateTableReservation` body |
| Occasion `occasion` | radio group | optional | — | Birthday · Anniversary · Business · Celebration · Other | — | The occasion the guest named (workbook Q204, DI-337; CHG-CSA-018). Shown to the host and the server; never a price. | `updateTableReservation` body |

Errors to draw in the form: 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

**Rules for these inputs** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **group request**: Choose the group ticket (School, Corporate, Tour operator, Community, each with per-person price and minimum), the date (and, for session products, a session), then How many people as a typed number box with minus and plus, supervisors separate and free. School adds the school name, year group, access and dietary needs; a party adds the child's name and turning age (1 to 18) and allergies. Headcount, child's name and age already entered are prefilled, never asked twice. *(source: DI-1104; DI-1105; DI-1117; contracts/spine/orders.yaml#/components/schemas/GroupBookingRequest; DI-1000)*

#### Outputs: what the screen shows and produces

**Shown**

**Your reservations** (card list, from `listReservations`): Was the generated table 'Every reservations'; staff and plumbing columns removed (decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-3)).

| Shows | Format | Notes |
|---|---|---|
| Status | chip: Held, Converted, Expired, Cancelled | — |
| Lines | list or chips (count when long) | — |
| Expires at | 1 Oct 2026, 14:30 | — |
| Converted order | the name it points at, never the id | — |

**Group packages** (card list, from `listGroupPackages`): School trips, parties and corporate days, as cards. Was the generated table 'Every group package definition'; staff and plumbing columns removed (decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-3)).

| Shows | Format | Notes |
|---|---|---|
| Product | text | — |
| Kind | chip: School, Party | — |
| Max participants | 1,234 | Pupils or children, e.g. 30 or 10. |
| Duration minutes | 1,234 | — |
| Host count | 1,234 | Party hosts included. |
| Pricing basis | chip: Per participant, Per package | — |
| Free leader ratio | 1,234 | Schools: one teacher or assistant enters free per this many pupils. |
| Payment mode | chip: Invoice, Deposit, Full | Schools are invoiced; parties take a deposit (see `DepositPolicy`). |
| Includes | list or chips (count when long) | — |

**The selected group package definition** (detail panel, from `getGroupPackageDefinition`)

| Shows | Format | Notes |
|---|---|---|
| Product | text | — |
| Kind | chip: School, Party | — |
| Max participants | 1,234 | Pupils or children, e.g. 30 or 10. |
| Duration minutes | 1,234 | — |
| Host count | 1,234 | Party hosts included. |
| Pricing basis | chip: Per participant, Per package | — |
| Free leader ratio | 1,234 | Schools: one teacher or assistant enters free per this many pupils. |
| Payment mode | chip: Invoice, Deposit, Full | Schools are invoiced; parties take a deposit (see `DepositPolicy`). |
| Includes | list or chips (count when long) | — |

**The group booking** (detail panel, from `getGroupBooking`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: General, School, Corporate, Party | — |
| Package product | text | The school-trip format or party package. |
| Year group | text | — |
| Access and dietary needs | text | — |
| Celebrant name | text | The birthday child. |
| Celebrant turning age | 1,234 | — |
| Allergies and requests | text | — |
| Final headcount due by | 1 Oct 2026, 14:30 | — |
| Quote sent at | 1 Oct 2026, 14:30 | — |
| Risk assessment sent at | 1 Oct 2026, 14:30 | — |
| Preferred date | 1 Oct 2026 | The date the guest asked for on `requestGroupBooking` — what its `409 dateUnavailable` is checked against. |
| Order | the name it points at, never the id | — |
| Leader subject | the name it points at, never the id | — |
| Organisation name | text | — |
| Expected size | 1,234 | — |

**The resource availability** (detail panel, from `getResourceAvailability`)

| Shows | Format | Notes |
|---|---|---|
| Resource | the name it points at, never the id | — |
| Free windows | list or chips (count when long) | — |
| Blocked windows | list or chips (count when long) | With a reason, because they are not the same. Booked and under repair need different responses from an operator looking for something free … |

**The reservation** (detail panel, from `getReservation`)

| Shows | Format | Notes |
|---|---|---|
| Status | chip: Held, Converted, Expired, Cancelled | — |
| Lines | list or chips (count when long) | — |
| Expires at | 1 Oct 2026, 14:30 | — |
| Converted order | the name it points at, never the id | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Cancel reservation (destructive button) | `cancelReservation` DELETE `/reservations/{reservationId}` | — | — | 409 Already converted (`alreadyConverted`), or no longer held — expired or already cancelled (`reservationNotHeld`). (ReservationProblem) | — |
| Request group booking (primary button) | `requestGroupBooking` POST `/group-booking-requests` | GroupBookingRequest | GroupBooking | 409 The date is no longer available (`dateUnavailable`), or the package is not (`packageUnavailable`). (GroupBookingProblem); 422 More participants than the package allows (`aboveParticipantLimit`). (GroupBookingProblem) | opens modal first |
| Change reservation (secondary button) | `updateTableReservation` PATCH `/table-reservations/{reservationId}` | TableReservation | TableReservation | 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **reservation row**: What, when, status in guest words (Awaiting payment, Confirmed, Expired, Cancelled), pay-by deadline as time remaining; a table deposit shows the amount, refundable until, and late-cancel and no-show terms. *(source: DI-612; screens/P01-guest-web-storefront.yaml#WEB-031 notes (REV3-8b))*
- **group request status**: Provisional with the held date; school "Quote and risk assessment within 2 working days, final headcount due 5 days before"; party "Deposit AED 100 per AED 400, refundable up to 24 hours before". *(source: contracts/spine/orders.yaml#requestGroupBooking; REV3 DG-4)*

**What each action does** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **Pay now**: Opens the payment for that reservation (WEB-014's payment component) before its deadline. *(source: screens/P01-guest-web-storefront.yaml#WEB-031 wireframe.prototype.differences)*
- **Cancel reservation**: The confirm names what is released and any deposit kept ("Cancel table for 4 on Fri 19:30? Your AED 100 deposit is not refundable after 24 hours."). *(source: screens/P01-guest-web-storefront.yaml#WEB-031 overlays.confirmCancelReservation)*

**Data it reads**: `listGroupPackages` (onLoad, School-trip formats and party packages); `listReservations` (onLoad, List reservations)

**Where the user goes next**

- → `WEB-030` Ticket Transfer: *Ticket Transfer*; carries `orderId`

**What opens over it**

- confirmDialog *Cancel reservation*: **Names what `cancelReservation` changes and what it leaves alone**, in the consequence rather than the verb. A reservations this affects should be identified in the dialog, not just counted.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reservations list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reservations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reservations yet. Offers Request group booking (`requestGroupBooking`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on kind and the reservations are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the … |
| Offline (`?state=offline`) | **The offline banner shows.** Reservations already loaded stay visible with their age. Booking, changing and cancelling need the connection — a table held offline is a table two people think they have. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Already converted (`alreadyConverted`), or no longer held — expired or already cancelled (`reservationNotHeld`). (ReservationProblem); 409 The date is no longer available (`dateUnavailable`), or the package is not (`packageUnavailable`). (GroupBookingProblem); 422 More participants than the package allows (`aboveParticipantLimit`). (GroupBookingProblem) |

#### Edge cases to draw

- **The headcount is over the package's cap, or the date has gone**: Over-cap and date-gone states with the nearest alternative date. *(source: REV3 DG-4)*

#### Consistency with other screens

- Match `GST-072`: Same group request and headcount box; the app adds a +10 step.
- Match `WEB-005`: The prototype draws the group request as a booking flow (group tickets, then headcount); it must be the same component here.
- Match `GST-016`: Same reservation statuses.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
reservations:
- what: Table for 4 · Saffron Table
  when: Fri 2 Oct 19:30
  status: Confirmed
  deposit: AED 100, refundable until Thu 19:30
- what: School group · Guests × 45 · Al Noor Private School
  when: Tue 21 Oct
  status: Provisional · quote within 2 working days
```

#### Permissions

- `listGroupPackages` → `PRODUCT_VIEW` (read) · guest, staff
- `getGroupPackageDefinition` → `PRODUCT_VIEW` (read) · staff, guest
- `requestGroupBooking` → no permission · guest
- `listReservations` → `ORDER_VIEW` (read) · staff, guest
- `getReservation` → `ORDER_VIEW` (read) · staff, guest
- `cancelReservation` → `ORDER_CANCEL` (operate) · staff, guest
- `getGroupBooking` → `ORDER_VIEW` (read) · staff, guest
- `getResourceAvailability` → `RESOURCE_VIEW` (read) · staff, guest
- `updateTableReservation` → no permission · guest

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the …

#### Requirements it meets

35 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.31 | Reservation Cancellation - System shall support reservation cancellations. | Guest Mobile App & Branding | CONTRACTED | `cancelReservation` |
| 1.2.6 | The system should provide a calendar view for all the resources (e.g. instructors) and associated time slots (e.g. ski school session by an instructor). The calendar should support application of … | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.7 | The system should show the booked capacity of different time-slots to provide their availability. The capacity can be color-coded to indicate if not busy, moderately busy, or crowded within each … | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.13 | Using the calendar view, system should provide an drag and drop interface to reassign the resources from one resource to another available resources. System should automatically assign the next … | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.18 | Resource Calendar: Centralized calendar view (daily/weekly/monthly). | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.19 | Availability Management: Check conflicts before assigning resources. | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.20 | Recurring Reservations: Block resources for repeated sessions/shows. | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.21 | Time Slot Management: Allocate setup, event, teardown, and maintenance times. | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.22 | Multi-event Handling: Manage shared resources across parallel events. | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.27 | System shall provide centralized resource calendars. | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.28 | System shall manage resource time slots and availability. | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.29 | System shall manage availability and conflict detection. | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| … 23 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- **Open question.** Are water-park groups booked into a session (the build picks a session first)? Default built: group requests take a date and, for session-based products, a session. *(open · Decisions Register 1 Oct 2026, Questions for the client — Group booking / Water-park groups by session · DI-1117)*
- **Open question.** Each group ticket card shows a minimum group size; is it set per group ticket, and what values? Default built: each group ticket carries its own minimum, default 10. *(open · Decisions Register 1 Oct 2026, Questions for the client — Group booking / Minimum group size · DI-1116)*
- **Open question.** Do Tour operator and Community become their own group types or map to general? Default built: School, Corporate, Tour operator and Community shown as their own group types (platform also has general and party). *(open · Decisions Register 1 Oct 2026, Questions for the client — Group booking / Group types · DI-1115)*
- **Open question.** How many supervisors come free per group (per N guests), and is it per group ticket? Default built: supervisors are a separate, free guest type, up to 1 per 10 guests, counted on the group request. *(open · Decisions Register 1 Oct 2026, Questions for the client — Group booking / Supervisors · DI-1114)*
- Supervisors are listed separately and are free; the enquiry panel shows the estimate as e.g. "School group · Guests × 45". Water park group booking: pick a session, then enter the number of swimmers and supervisors. On mobile the headcount stepper has a +10 button. *(client request · design review 30 Sep 2026, 1. Group booking: product missing, enter the number of people · DI-1105)*
- Group / school booking starts with group ticket cards (School, Corporate, Tour operator, Community), each showing a per-person price and minimum group size. Then "How many people" is a number box the guest can type (e.g. 45) or step with − / +; no Group size dropdown. *(client request · design review 30 Sep 2026, 1. Group booking: product missing, enter the number of people · DI-1104)*
- Duplicate screens become one implementation covering several screen IDs (mobile Transfer + Delivery & Sharing; web Wishlist / Devices & Consent; Help Centre + Help & Accessibility as one Help view with FAQ, cases, policies, accessibility tabs). Ticket-selection functions belong on GST-008. Web gets a Group Booking view. *(agreed · design review 29 Sep 2026, GAP-D3 · D. Duplicate screens merged; group booking on web · DI-1078)*
- Booking statuses: draft > reserved (awaiting payment) > completed, with cancelled or expired paths. Hold policy sets how long a capacity booking is held pending payment before release to inventory. *(client request · MoM 1 Sep 2026, 4.11 Order & Reservation Management · DI-612)*
- Guest profile shows gift vouchers and a stored-value "money card"/wallet; "My Tickets" (all tickets) is separate from "My Reservations" (bookings holding one or more tickets) with reservation details and date modification. *(client request · MoM 10 Aug 2026, 4.3 B2C Guest App — End-to-End Booking Journey · DI-199)*

Also apply: 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-031` · status **review** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match partial): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html`, view *Account → 'Reservations'*. Differences: The prototype uses the WEB-031 label for the group booking request dialog (deposit / invoice quote) inside Kids Club → 'Birthday party / group' and 'School trip', which the YAML covers only through requestGroupBooking. 'Pay now' on a held reservation has no YAML route (WEB-014 is pay-by-link).
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (27), with its required mark, default, format and its error state (403, 404, 409, 412, 422).
- [ ] Every output is drawn (44 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-031?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Cancel reservation, Request group booking, Change reservation.
- [ ] Every transition is wired: `WEB-030`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 9 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `WEB-035` Multi-Currency & Pricing

**Choose the currency you see prices in and pay in.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Ticketing · wave 1 · needs the `ticketing` module |
| Block | Block A · ticket #17871 (APP-WEB-WEB-035) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · the venue's theme |
| Pattern | listDetail (compact density): `listFxRates` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **The offline banner shows. Last known rates stay, with their age.** A rate is a number a guest may act on, and an undated one they cannot judge. |
| Opens with | nothing: it opens on its own |
| Route | `/multi-currency-pricing` |

**What the spec says about it.** Added 17 August. **The surface the matrix names** — 2.6.33 *"website should be able to display multi currency"* and 2.9.1 *"in the B2C portal for guests comparison"*. Wave 1 against the app's Wave 2, because **the website is where an overseas guest compares before booking** and the app is where they check after. **Display only — the sale settles in base currency** (CF-37). Not on the wireframe board; needs drawing. **`getRegionSettings` deliberately not called** — a guest does not need the venue's scope configuration to pick a currency. `listFxRates` is the currency list: a rate exists only for a currency the venue enabled, so the two questions have one answer. **Rev 3 (decided 29 September, rev 3 GAP-D2).** The web and app waves of this capability differ; they are aligned to one wave once the client picks it (open, client to choose). Rates carry `fetchedAt` (`listFxRates`; GAP-B3, already); the prototype's fixed demo rate is prototype-only (CFG-7, no change). **The guest selects the currency and pays in it** (decided 2 October 2026, Chinmay; CHG-FIN-001; reverses the display-only rule, CF-37 and "payment will be processed in AED", in favour of option (b) of MoM 10 Aug 2026 4.7, DI-211). The venue lists the currencies a guest may pay in (`VenueSettings.chargeCurrencies`, a subset of the currencies it shows); `listFxRates` with `chargeable=true` returns them, each marked `chargeable`. The selected currency is sent at checkout (`checkoutCart.chargeCurrency`), the rate is locked on the order (`Order.chargeFxRate`, `chargeTotal`, until `chargeRateLockedUntil`), and the payment …

**From the Finance, Ledger & Tax · Reporting & Analytics process.** An overseas guest picks their currency before booking. Where the venue charges that currency the guest pays in it: the rate is locked at checkout, the card is charged in that currency, refunds come back in it, and the venue's books stay in AED with the rate recorded (decided 2 October 2026, Chinmay). Where the venue only shows a currency, prices in it are approximate and the guest pays in AED. The one thing to get right: the guest always knows which currency the card will be charged in, and an approximate figure never looks like a charge.

**Fixed on main** (the package already carries these; draw what it says): Venue, As at and Purpose are drawn as guest controls. (CHG-FIN-001); The rate table and detail panel bind every FX rate field. (CHG-FIN-001); The empty first-run state ("No multi-currency pricing yet… offers no create action"). (CHG-FIN-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is gateway-level currency conversion (the guest is charged in their own currency) in scope?** → The guest selects the currency and is charged in it. *(decided by Chinmay, 2026-10-02; DEC-092 / CHG-FIN-001 / CHG-NOTE-003)*
- **Which wave do web and app multi-currency ship in together?** → Web and app multi-currency are built now. *(decided by Chinmay, 2026-10-02; DEC-093 / CHG-FIN-001 / CHG-NOTE-003)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Pay in | select field | — | — | — | — | Sends `?venueId=&chargeable=true` to `listFxRates`: the currencies this venue lets a guest pay in, base currency first. The choice is kept for the session and sent at checkout as `chargeCurrency` … | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| As at | date and time picker | — | — | `listFxRates` ?asAt |
| Purpose | radio group | — | Tender · Inter entity · Reporting · Revaluation | `listFxRates` ?purpose |
| Chargeable | toggle | — | — | `listFxRates` ?chargeable |
| Kind | select | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | `listProducts` ?kind |
| Is sellable | toggle | — | — | `listProducts` ?isSellable |
| Category | picker: choose a category | — | — | `listProducts` ?categoryId |
| Segment tag | text field | — | max length 120 | `listProducts` ?segmentTag |
| Guided answers | multi-picker: choose guided answers | — | at most 10 | `listProducts` ?guidedAnswerIds |

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Currency (the only guest control)**: Options are the currencies this venue shows; the region sets the rates and the venue picks which appear and which of them a guest can pay in (`chargeable`). Base currency first, then in the order returned. The choice changes every displayed price (DI-1071) and, for a chargeable currency, becomes the payment currency sent at checkout (`chargeCurrency`); for a shown-only currency it stays a display preference. *(source: contracts/spine/finance.yaml#listFxRates / contracts/spine/orders.yaml#checkoutCart / R120 / DI-1071 / DI-211)*
- **Venue**: Not a guest control. The venue is the one the guest already picked on the home screen and is sent silently. Remove the venue picker from the drawing. *(source: screens/P01-guest-web-storefront.yaml#WEB-035)*
- **As at / Purpose**: Not guest controls. "As at" is always now. "Purpose" is always the guest-facing rate (tender: "what a guest pays at"). Interbank, reporting, revaluation and inter-entity rates are internal treasury figures a guest must never see. *(source: contracts/spine/finance.yaml#ingestFxRates / contracts/spine/finance.yaml#/components/schemas/FxRatePurpose)*

#### Outputs: what the screen shows and produces

**Shown**

**How you pay** (banner, from `listFxRates`): "You pay in USD. Your card is charged USD 81.72; the venue records AED 300.00 at 3.6710." For a currency shown but not chargeable: "Prices in EUR are approximate. You pay in AED." (CHG-FIN-001). The purpose filter is fixed to `tender`, never typed by a guest.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| From currency | text | — |
| To currency | text | — |
| Rate | text | Units of `toCurrency` per one `fromCurrency`. Six decimal places — a two-place rate on a three-place currency loses money on every … |
| Purpose | chip: Tender, Inter entity, Reporting, Revaluation | A venue does not accept dollars at the rate it books an intercompany balance at. |
| Source | chip: Manual, Uae central bank, Ecb, Open exchange rates, Card scheme, Provider | Where the rate came from, and which provider specifically. `source: provider` said a feed set it and not which one — two tenants on … |
| Effective from | 1 Oct 2026, 14:30 | — |
| Effective to | 1 Oct 2026, 14:30 | A rate change is a new row. The old one is never edited — a transaction posted last Tuesday must still reconcile at last Tuesday's rate. |
| Set by principal | the name it points at, never the id | — |
| Note | text | Why this rate, and from where. Required when `source` is `manual` (decided 28 September, audit R127 (4)); null on a rate `ingestFxRates` … |
| Provider reference | text | The provider's own identifier for this quote. What makes a rate reproducible — an auditor asking why a payment converted at 3.6725 gets an … |
| Fetched at | 1 Oct 2026, 14:30 | When the rate was pulled. Distinct from `effectiveFrom`, which is when it applies — a rate fetched at 06:00 for a business day starting at … |
| Chargeable | yes / no (icon or chip) | With `venueId`, true where a guest may select this currency and pay in it at that venue (`tenancy.VenueSettings.chargeCurrencies`), false … |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Currencies** (card list, from `listFxRates`): Fixed by the screen: the venue from Home, as at now, purpose tender. A guest never chooses a purpose: that would let them browse internal treasury rates. Was the generated table 'Every FX rate'; staff and plumbing columns removed (decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-3)).

| Shows | Format | Notes |
|---|---|---|
| To currency | text | — |
| Rate | text | Units of `toCurrency` per one `fromCurrency`. Six decimal places — a two-place rate on a three-place currency loses money on every … |
| Fetched at | 1 Oct 2026, 14:30 | When the rate was pulled. Distinct from `effectiveFrom`, which is when it applies — a rate fetched at 06:00 for a business day starting at … |
| Chargeable | yes / no (icon or chip) | With `venueId`, true where a guest may select this currency and pay in it at that venue (`tenancy.VenueSettings.chargeCurrencies`), false … |

**Prices in your currency** (card list, from `listProducts`): The venue's products with the price converted at the rate above; the venue's own currency stays the price charged. The venue is the one the guest picked on Home (`venueId` from the session, audit R267), never typed. Was the generated table 'Every product'; staff and plumbing columns removed (decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-3)).

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Description | text | — |

**The selected currency** (detail panel, from `listFxRates`)

| Shows | Format | Notes |
|---|---|---|
| From currency | text | — |
| To currency | text | — |
| Rate | text | Units of `toCurrency` per one `fromCurrency`. Six decimal places — a two-place rate on a three-place currency loses money on every … |
| Fetched at | 1 Oct 2026, 14:30 | When the rate was pulled. Distinct from `effectiveFrom`, which is when it applies — a rate fetched at 06:00 for a business day starting at … |
| Chargeable | yes / no (icon or chip) | With `venueId`, true where a guest may select this currency and pay in it at that venue (`tenancy.VenueSettings.chargeCurrencies`), false … |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Converted price**: Shown as "≈ USD 81.42" under or beside "AED 299.00". Computed as base price ÷ the rate, rounded to the shown currency's own decimals (2 for USD/GBP/SAR/INR, 3 for KWD/BHD/OMR). Never larger or bolder than the AED price. *(source: DI-211 / DI-306 / DI-598 / contracts/spine/finance.yaml#/components/schemas/FxRateValue)*
- **Rate line**: "1 USD = 3.6725 AED · updated 06:00 today". Use the time the rate was fetched where the provider supplied it, otherwise the time it took effect. A rate more than a day old shows its date, not "today". *(source: DI-1074 / contracts/spine/finance.yaml#/components/schemas/FxRate)*
- **"You pay in" statement**: In the body next to the selector, never a footnote. Chargeable currency: "You pay in USD. Refunds go back in USD." Shown-only currency: "Prices in EUR are a guide. You pay in AED." *(source: contracts/spine/orders.yaml#/components/schemas/Refund / contracts/spine/finance.yaml#listFxRates)*
- **Products**: Photo, name and the "from" price in AED with its approximate conversion. Show none of the rate table's internal columns (who set it, provider reference, the rate note, which can state the venue's margin over market). *(source: contracts/spine/finance.yaml#/components/schemas/FxRate / DI-026)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Change currency**: Re-renders every price instantly from the rates already loaded. Nothing is saved to the server and nothing is added to the order. *(source: contracts/spine/finance.yaml#listFxRates)*
- **Book (any product)**: The selected currency carries through the cart to checkout. A chargeable currency is locked at checkout and charged; a shown-only currency stays approximate and checkout charges AED. *(source: contracts/spine/orders.yaml#checkoutCart / contracts/spine/orders.yaml#/components/schemas/Order / DI-211)*

**Data it reads**: `listFxRates` (onLoad, The currencies the venue shows, each marked chargeable or …); `listProducts` (onLoad, List products)

**Where the user goes next**

- → `WEB-030` Ticket Transfer: *Ticket Transfer*
- → `WEB-031` My Reservations: *My Reservations*; carries `productId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The multi-currency pricing list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the multi-currency pricing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | Not reachable: with no other currency at the venue the screen is not linked, and prices stay in the venue's currency. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: the screen sends no filter a guest chose. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the … |
| Offline (`?state=offline`) | **The offline banner shows. Last known rates stay, with their age.** A rate is a number a guest may act on, and an undated one they cannot judge. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A `categoryId` that names no category of the venue, or a `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 … |

#### Edge cases to draw

- **The venue shows no other currency**: The entry point to this screen is not offered and no selector is drawn. Never an empty table titled "No multi-currency pricing yet". *(source: contracts/spine/finance.yaml#listFxRates / screens/P01-guest-web-storefront.yaml#WEB-035)*
- **Offline or the rates could not be refreshed**: Keep the last rates with their age ("Rates from 06:00, may have changed"). An undated rate is never shown. *(source: screens/P01-guest-web-storefront.yaml#WEB-035)*
- **The provider feed failed this morning**: The previous rate is still in force; show its date plainly. The platform refuses a feed that cannot be reached rather than reusing a stale rate silently, so the date is the warning. *(source: contracts/spine/finance.yaml#ingestFxRates)*
- **Arabic (right-to-left)**: Layout mirrors; currency codes and figures stay left-to-right inside the line ("AED 299.00"). *(source: DI-019)*

#### Consistency with other screens

- Match `GST-044`: Same component, rules and wording on web and app (one product, two renderings). Web is wave 1 and app wave 2 until the client aligns them (REV3 GAP-D2).
- Match `WEB-012`: Checkout shows the total in the selected chargeable currency with the AED amount and the locked rate beneath; for a shown-only currency it shows AED with the approximate figure under it.
- Match `POS-005`: The till applies the same display rule for foreign-currency guests and records the base equivalent (DI-213).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
venue: Aquaventure Waterpark, Dubai (base AED, 2 decimals)
currencies:
- AED
- USD
- SAR
- GBP
- INR
rates:
- 1 USD = 3.6725 AED · updated 06:00 today
- 1 SAR = 0.9793 AED
- 1 GBP = 4.6610 AED
- 1 INR = 0.0440 AED
products:
- Day Pass Adult · AED 299.00 · ≈ USD 81.42 · ≈ SAR 305.32
- Day Pass Child · AED 249.00 · ≈ USD 67.80
- Cabana for 4 · AED 1,250.00 · ≈ GBP 268.18
threeDecimalExample: 'A Kuwait-facing venue showing KWD: AED 299.00 ≈ KWD 25.032'
```

#### Permissions

- `listFxRates` → `LEDGER_VIEW` (read) · staff, guest
- `listProducts` → `PRODUCT_VIEW` (read) · staff, guest, partner

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the …

#### Requirements it meets

12 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.7 | For BtoC online sales, the following points shall be available online: | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.6.8 | - All PLUs | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.13.21 | All PLUs can be sold on the POS (ticketing and non-ticketing) including Packages. | Ticketing Sales | CONTRACTED | `listProducts` |
| 8.8.1 | A price for a PLU is changing depending on the date of visit. I can sell today a product to be used after a price change at the new price defined in the sales calendar. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.2 | System shall support future-dated pricing schedules. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.3 | System shall support pricing by visit date. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.4 | System shall support pricing by booking date. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.5 | System shall support pricing calendar management. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.6 | System shall support automatic activation of future pricing. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.7 | System shall support overlapping pricing schedules with priority rules. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.8 | System shall maintain pricing schedule history. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.9 | System shall provide pricing schedule audit trails. | Unified Operations Dashboard | CONTRACTED | data `Product` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Web screens carry: cart promo code (valid/invalid/expired) and empty basket with confirm; interrupted-payment recovery ("we are checking with your bank" → success/failed/unknown); reprint/resend tickets; UAE Pass sign-in, link guest checkout, sign out; support cases and Sahli handoff; FX rates with timestamp; remaining entitlements. *(agreed · design review 29 Sep 2026, GAP-B3 · B. Web — missing functions on existing screens · DI-1074)*
- A currency selector (AED, SAR, USD, INR, GBP) converts every displayed price. *(agreed · design review 29 Sep 2026, CFG-7 · Currency (AED/SAR/USD/INR/GBP) · DI-1071)*
- Foreign-currency display: an approximate conversion at a back-office rate so the guest sees roughly what they pay while settling in base currency, and/or full DCC at the gateway where the guest is charged in their own currency; records always in the venue base currency. *(agreed · MoM 10 Aug 2026, 4.7 Account Creation, Localisation & Multi-Currency · DI-211)*

Also apply: 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A43** Design multi-currency display to support both manual FX-rate entry (with configurable margin) and an optional real-time third-party FX-rate API; confirm which payment gateway(s) support Dynamic Currency Conversion (DCC) *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · names this screen)*
- **A44** Add a foreign-currency collection report (transactions collected broken down by foreign currency) to the Finance reporting suite *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'foreign currency')*
- **C23** Confirm foreign-currency display approach (manual FX-rate entry with margin vs. live third-party FX-rate API) and confirm the payment gateway that will support Dynamic Currency Conversion *(Qossai / Allam · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'fx-rate')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'multi-currency')*

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-035` · status **review** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match exact): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html`, view *Discover → 'Prices in your currency'*. Differences: Matches the YAML's charged-vs-shown rule. Separately, Config → Currency switches the whole storefront currency, which contradicts 'always charged in AED'. **Resolved 2 October 2026 (CHG-FIN-001):** the guest may pay in the selected currency, so a storefront currency switch is right where the venue charges that currency.
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (27 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-035?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `WEB-030`, `WEB-031`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 4 edge case(s) from the process notes are drawn.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

## Tenant configuration on every guest screen

Every guest screen in this batch is white-label. These elements are set by the tenant in the CMS and apply to every screen of the guest app (each screen's block lists the ones particular to it). **Draw with the default theme; on the key screens add one alternate tenant theme** (below), so a reviewer sees the brand is configuration, not paint. The full map, with the input-to-output examples: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Element | Configured in | Allowed values | Default | What it changes |
|---|---|---|---|---|
| Logo (`brand.logoAssetRef`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the logo in the header or nav bar, the splash and the footer |
| Logo dark image (`brand.logoDarkAssetRef`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the logo on dark backgrounds (falls back to the primary logo) |
| Logo variant (`brand.logoVariant`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | Light · Dark · Duotone | Light | which logo lockup sits in the nav bar, and whose colours drive the theme |
| Favicon (`brand.faviconAssetRef`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the browser tab icon (website only) |
| Splash image (`brand.splashImageAssetRefs`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | PNG, JPG, SVG or MP4 from the media library | — | Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish (audit R163). |
| Splash duration seconds (`brand.splashDurationSeconds`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | min 0; max 10 | 3 | — |
| Splash background colour (`brand.splashBackgroundColour`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | #RRGGBB | — | — |
| Show loading indicator (`brand.showLoadingIndicator`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | — | on | — |
| Intro video (`brand.introVideoAssetRef`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | The optional intro video (decided 29 September, MOB-5). A video `MediaAsset` from the media library (CMS-010). |
| Intro video mode (`brand.introVideoMode`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | Off · First launch · Every launch; Anything but `off` needs `introVideoAssetRef`, or 400. | Off | When GST-001 plays it full screen. "Skip introduction" is always shown. |
| Powered by TICVAI credit (`brand.showPoweredBy`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | — | on | the *Powered by TICVAI* credit on the launch screen, at the foot of Account and in the web footer; on by default, and switching it off needs the licence add-on (403 … |
| Primary colour (`theme.primaryColour`) | `CMS-005`, `ADM-016` | #RRGGBB | — | the brand colour (the `accentSolid` token): primary buttons (Book, Continue, Add to cart, Pay), the active step of the step indicator, selected date and time chips, focus rings |
| Secondary colour (`theme.secondaryColour`) | `CMS-005`, `ADM-016` | #RRGGBB | — | secondary buttons and secondary emphasis: unselected chips, secondary tabs |
| Accent colour (`theme.accentColour`) | `CMS-005`, `ADM-016` | #RRGGBB | — | highlights: badges (LIMITED, NEW, BESTSELLER), availability counts, sale prices |
| Background colour (`theme.backgroundColour`) | `CMS-005`, `ADM-016` | #RRGGBB | — | the page background behind every screen (the `ground` token) |
| Text colour (`theme.textColour`) | `CMS-005`, `ADM-016` | #RRGGBB | — | body text on the background |
| Corner radius (`theme.cornerRadius`) | `CMS-005`, `ADM-016` | min 0; max 32 | — | the corners of cards, buttons, inputs, sheets and the cart (0 square to 22 the prototype's roundest) |
| Surface style (`theme.surfaceStyle`) | `CMS-005`, `ADM-016` | Glass · Solid | Glass | cards and panels: frosted glass (default) or opaque (the `surfaceRaised` token) |
| Button style (`theme.buttonStyle`) | `CMS-005`, `ADM-016` | Solid · Outline · Pill | Solid | every button's shape: solid fill, outline, or pill |
| Component colours (`theme.componentColours`) | `CMS-005`, `ADM-016` | — | — | Colours for single interactive elements (decided 17 September, M17-11). Each is optional and falls back to the theme colours. |
| Primary latin (`fonts.primaryLatin`) | `CMS-003` | — | — | headings and body text in English |
| Primary arabic (`fonts.primaryArabic`) | `CMS-003` | Required when `ar` is among the tenant's languages (audit R163). | — | headings and body text in Arabic |
| Secondary latin (`fonts.secondaryLatin`) | `CMS-003` | — | — | the secondary face (eyebrows, numbers) in English |
| Secondary arabic (`fonts.secondaryArabic`) | `CMS-003` | Required whenever `secondaryLatin` is set and `ar` is among the tenant's languages (decided 28 September, audit R163). | — | the secondary face in Arabic |
| Custom font images (`fonts.customFontAssetRefs`) | `CMS-003` | PNG, JPG, SVG or MP4 from the media library | — | Uploaded font files, as `MediaAsset` ids. |
| Header layout (`header.layout`) | `CMS-009` | Logo left · Logo centre · Logo with menu | — | the header: logo left, logo centred, or logo with the menu |
| Show logo (`header.showLogo`) | `CMS-009` | — | on | — |
| Show menu (`header.showMenu`) | `CMS-009` | — | on | — |
| Show notifications (`header.showNotifications`) | `CMS-009` | — | on | — |
| Background colour (`header.backgroundColour`) | `CMS-009` | #RRGGBB | — | — |
| Navigation kind (`navigation.kind`) | `CMS-009` | Bottom navigation · Drawer · Tabs | — | the main navigation: bottom tab bar, drawer, or tabs |
| Navigation items (`navigation.items`) | `CMS-009` | at most 12 | — | — |
| Buy button (`navigation.buyButton`) | `CMS-009` | — | — | The persistent Buy tickets button (decided 29 September, MOB-2). On every screen of the mobile app except the booking and checkout steps; it opens GST-003. |
| Footer columns (`footer.columns`) | `CMS-009` | — | — | — |
| Legal links (`footer.legalLinks`) | `CMS-009` | — | — | Required links, held separately from the free-form columns — a tenant reorganising their footer must not be able to remove the privacy notice by accident. |
| Copyright text (`footer.copyrightText`) | `CMS-009` | — | — | — |
| Social links (`footer.socialLinks`) | `CMS-009` | — | — | — |
| Languages (`languages.languages`) | `CMS-011`, `ADM-018` | at least 1 | — | the language button in the header; Arabic flips every screen right to left |
| Default language (`languages.defaultLanguage`) | `CMS-011`, `ADM-018` | ISO 639-1 code, shown as the language name | — | the language a first visit opens in |
| Modules (`modules.modules`) | `CMS-001`, `ADM-424` | — | — | — |
| Features (`features.features`) | `CMS-001` | — | — | — |
| Custom domain hostname (`domains.hostname`) | `CMS-017`, `ADM-017` | — | — | — |
| Custom domain kind (`domains.kind`) | `CMS-017`, `ADM-017` | Guest web · Guest app · Partner portal · Developer portal | — | — |
| Verification method (`domains.verificationMethod`) | `CMS-017`, `ADM-017` | Dns txt · Cname · Http file | Dns txt | — |
| Entity kind (`seo.entityKind`) | `CMS-013` | Content page · Product · Event · Performance · Membership · Promotion · Venue | — | — |
| Entity (`seo.entityId`) | `CMS-013` | shows names, sends the id | — | — |
| Locale (`seo.locale`) | `CMS-013` | — | — | — |
| SEO metadata title (`seo.title`) | `CMS-013` | — | — | — |
| Meta description (`seo.metaDescription`) | `CMS-013` | — | — | — |
| Keywords (`seo.keywords`) | `CMS-013` | — | — | — |
| Canonical URL (`seo.canonicalUrl`) | `CMS-013` | — | — | — |
| Slug (`seo.slug`) | `CMS-013` | — | — | 22.11.6. Human-readable, and changing one is a redirect rather than an edit — a slug that changes without a 301 is a page that was ranking and now is not. |
| Hreflang (`seo.hreflang`) | `CMS-013` | — | — | 22.11.11. Which URL serves which language, and getting this wrong on a bilingual venue site splits its own ranking between two versions of the same page. |
| Schema org type (`seo.schemaOrgType`) | `CMS-013` | — | — | — |
| Open graph (`seo.openGraph`) | `CMS-013` | — | — | — |
| Is auto generated (`seo.isAutoGenerated`) | `CMS-013` | — | on | 22.11.2. Generated by default and overridable. |
| No index (`seo.noIndex`) | `CMS-013` | — | off | — |
| Favicon (`brand.faviconAssetRef`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the browser tab icon (website only) |
| Component colours: primary CTA (`theme.componentColours.primaryCta`) | `CMS-005`, `ADM-016` | — | — | the one main call to action on each screen, when it should differ from the brand colour |
| Component colours: pay button (`theme.componentColours.payButton`) | `CMS-005`, `ADM-016` | — | — | the Pay button at checkout |
| Buy button: style (`navigation.buyButton.style`) | `CMS-009` | Raised · Floating · Flat · Hidden | Raised | the Buy tickets button in the tab bar: raised (default), floating, flat, or hidden |

**The alternate tenant theme (Coastal Aqua)**: Primary colour #0077B6; Secondary colour #023E8A; Accent colour #FFB703; Background colour #F5FAFC; Text colour #0B1324; Corner radius 18; Surface style Solid; Button style Pill; Logo variant Duotone; Header layout Logo centre; Step indicator Dots; Card layout Cards across; Card size Standard; Cart layout Floating icon; Fonts Poppins / Tajawal.
**Key screens to show in it:** `WEB-001`, `WEB-005`, `WEB-006`, `WEB-010`, `WEB-012`, `GST-001`, `GST-007`, `GST-041`, `KSK-002`, `KSK-003`.

**Decided for every guest screen:** **No dark or light mode.** The venue's chosen theme applies on every device setting; `Theme.darkMode` is deprecated and ignored, never drawn, and the guest app has no Light/Dark switch (Chinmay, 2 October, Q150; CHG-CSA-035). ***Powered by TICVAI* is a tenant toggle, on by default** (`brand.showPoweredBy`): shown on the launch screen, at the foot of Account and in the web footer; switching it off needs the licence add-on, or 403 `powered-by-locked` (Chinmay, 2 October, Q160; DI-297; CHG-CSA-036). **Each homepage section sets its card count and its scroll animation** (`maxItems`; `scrollAnimation` rise, scale, slide, blur or none, default rise): every customisation option of the approved wireframe (Chinmay, 2 October, Q152 and Q153; DI-1088; CHG-CSA-040). **Landing-page templates.** A tenant with no landing page of its own starts from a TICVAI template (`listLandingPageTemplates`, kept as `HomepageLayout.templateKey`); one with its own site links in with deep links (`landingSource` ownSite) (Chinmay, 2 October, batch 2 #41; CHG-CSA-037).

**Never configurable:** A dark or light mode: the guest surfaces have one theme, the venue's (Chinmay, 2 October; CHG-CSA-035). Semantic colour pairs (success, warning, danger, neutral) are not overridable: a tenant who recolours danger to their brand green has made a destructive confirmation look like a success (`screens/_design-tokens.yaml` whiteLabel). Site structure and the navigation flow are fixed and adapt to the product configuration (MoM 3 Aug, DI-119); a guest always books a product or package, never a resource (DI-502). A colour pair that fails 4.5:1 contrast is refused by the CMS, not warned (setTheme 400 ContrastProblem, audit R139).

## Reference designs and the trackers for this platform

**P01 reference designs** (from `handoff/design-batches/apps/1-guest-app/README.md`)

- `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`: the website. Rev 3 with the 29 September fixes and the 30 September feedback (group booking with a headcount, multi-park counters, surf session tickets, the swim-ability answer, transport stations and departures, popular route cards; `CLIENT-RESPONSE-30SEP.md` beside it). The client approved it for development once W1 to W10 are in.
- `sources/designs/guest-rev3-30-september/TICVAI Visit Planner.dc.html`: the visit planner. WEB-050 Plan Your Visit is this file.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-026, DI-027, DI-029, DI-032, DI-033, DI-034, DI-036, DI-038, DI-040, DI-042, DI-044, DI-045, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

**Workshop tracker rows about P01 as a whole** (23: 3 open, 20 closed). Open first; a closed row says where it went on 30 September.

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker)*
- **S9** Final UI/UX for the website and the mobile app *(Chinmay Parab · In progress · due Fri 2 Oct · 30 Sep 2026 · 30 Sep tracker)*
- **T1** Feedback on the revised website and mobile wireframes *(Allam / Qossai · Open · due 1 Oct · 30 Sep 2026 · 30 Sep tracker)*
- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker)*
- **A28** Review the 'Viva Ticket' website as a reference for ticket-flow variations *(Softlabs Design Team · Low · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker)*
- **A29** Collate design references/inspiration and share with TICVAI, organized by mobile app, website, and admin/back-office pages *(Softlabs (Sahil & Aishwarya) · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A55** Implement per-tenant module visibility toggles (e.g., hide Dining, Retail, or other services) configurable independently for the guest website and mobile app *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker)*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker)*
- **A115** Apply HA selectively to revenue-critical components (ticketing, POS, B2C) same-region, with multi-region DR as an optional add-on *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 24 Aug 2026 · workshop tracker)*
- **A118** Commission the third-party penetration test before go-live (ticketing, B2C, B2B, mobile apps) and resolve all severities *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 24 Aug 2026 · workshop tracker)*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker)*
- **A174** Cross-check the six previously-scoped wallet types against Allam's documentation and deliver the three wireframe flows (ticketing, F&B, retail) plus the revised B2C flow *(Chinmay Parab / Pradnya Yeram / Allam · High · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 9 Sep 2026 · workshop tracker)*
- … 9 more in `handoff/design-inputs/task-tracker-index.json`

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

### Across P01 Guest Web

- Step-indicator style is configurable, the same as on the web: bars, dots, counters or step names. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1093)*
- **Open question.** Real venue photos, clips and logos are still to come from the client; designs use stand-ins. Slots expected: a photo per ticket card and clip per card, a square shot per extra/shop item, one landscape poster per venue for the single-event page. Photos ≥1600 px, clips mp4 6–12 s, no audio. *(open · design review 29 Sep 2026, Asset list — TICVAI Guest Booking · DI-1080)*
- The tenant picks which logo lockup sits in the nav bar and a logo variant (Light, Dark, Duotone) whose colours drive the theme. *(agreed · design review 29 Sep 2026, CFG-4 · Brand logo + Logo palette (Light/Dark/Duotone) · DI-1068)*
- Theme settings: surface style Glass (default) or Solid cards; button style Solid (default), Outline or Pill. *(agreed · design review 29 Sep 2026, CFG-3 · Surfaces (Glass/Solid) and Buttons (Solid/Outline/Pill) · DI-1067)*
- Venue branding offers named palettes, font pairs, background tones and a 0–22 px corner radius. *(agreed · design review 29 Sep 2026, CFG-2 · Brand: Palette, Typeface; Shape: Background, Corner radius · DI-1066)*
- Guest-facing copy may say "session" (surf sessions, timed sessions) as a glossary exception, like "Booking". *(agreed · design review 29 Sep 2026, CFG-10 · 'Sessions can be added, edited or closed from Config -> Sessions' · DI-1064)*
- Never ask the same thing twice: table zone is picked on the table map (no zone step before it); height is asked once (height bands on the water-park day pass are the eligibility check); party/school summaries prefill headcount, child's name and age from the earlier form. *(agreed · rev 3 design review 28 Sep 2026, Flow review (28 Sep): repeated steps removed · DI-1000)*
- Confirmed final: cart sliding in from the right or bottom, card size options, and cart-sidebar placement left or right; Qossai specifically liked the compact card size. No further changes requested. *(agreed · MoM 24 Sep 2026, 4.10 Guest Web App — Card Layout & Cart Configuration Confirmed · DI-991)*
- Headers are reserved for standard elements only (venue image, category tabs, language bar, profile icon), applied consistently; date/availability selection belongs in the main content below the header, never in the header. Header/layout patterns must be adapted for mobile, which looks and behaves differently. *(agreed · MoM 24 Sep 2026, 4.9 Guest Web App — Specific UX Feedback (Header/Date Placement Standardization) · DI-990)*
- A language button (EN / العربية) sits in the header next to the profile icon, web and mobile. Arabic flips the whole layout right-to-left and switches interface text (navigation, buttons, booking steps, ticket names and tags, cart, seat map, checkout, account). Venue, show and dish names stay as written. *(client request · design review 23 Sep 2026, Header 2. Language icon in the header · DI-975)*
- Replace "Sign in / Create account" in the header with a single profile icon. It opens one screen with Log in and Register tabs; signed-in guests get their account menu from the same icon. *(client request · design review 23 Sep 2026, Header 1. One profile icon in the header that opens login / register · DI-974)*
- Allam's model reference: a simple card-based family-entertainment-centre site with minimal clicks, a right-side cart drawer, "help me choose", clear categories, video that autoplays when a guest taps "read more", adapting seamlessly between desktop and mobile. Allam and Qossai want this simplicity to guide the guest experience. *(client request · MoM 18 Sep 2026, 4.14 Guest Website UX Review — Upsell/Cross-Sell Placement & Reference Sites · DI-952)*
- **Open question.** Allam expects a large volume of feedback on the guest web/mobile prototype; detailed feedback goes to a separate dedicated session with Qossai and Allam. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-888)*
- The reviewed prototype is the actual guest-facing B2C site customers browse and book from, not a CMS tool. A separate, more limited white-label interface lets a client adjust colours, fonts and layout from a menu of options; not yet built in the prototype. *(agreed · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-887)*
- **Open question.** Product card-layout options shown in the prototype: stacked, staggered, horizontal. Choice/feedback pending the dedicated review. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-886)*
- **Open question.** Prototype's white-label panel previews the guest site under theme presets (e.g. "stadium", "theatre"), alternative layouts and brand colour palettes. Shown by Chinmay; client feedback deferred to a dedicated session. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-885)*
- Qossai is dissatisfied with the current B2C guest platform build and wants a separate vision session; references: the "Little Explorer" site and Six Flags. Six Flags cues: single-page flow. *(client request · MoM 8 Sep 2026, 4.20 Planning & Next Steps · DI-736)*
- Allam: most guests book from a smartphone, so the mobile version of the booking flows is the higher priority to validate (only desktop shown). *(client request · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough · DI-684)*
- Face enrollment via mobile app, website, POS, self-service kiosk, or at the turnstile itself (scan the ticket, then look at the reader on first use), covering e.g. B2B/reseller tickets. Re-enrollment and fallback to QR/RFID if face fails at the gate. *(agreed · MoM 2 Sep 2026, 4.10 Facial Recognition - Face Pass, Face Tag & Enrollment · DI-641)*
- Configurable cookie consent banner (accept/reject) per website; some cookies flagged mandatory (non-rejectable), others optional; templated and configurable in the system. *(client request · MoM 1 Sep 2026, 4.13 Privacy Consent & Cookie Policy · DI-617)*
- Waiver versioning, a mobile-optimised guest waiver view, approval/testing/publication flow, and access to the form via a QR code that opens it directly. *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-575)*
- Confirmed: a guest always books a product or package — never a resource (a specific room, vehicle or instructor by itself) directly — on every sales channel, including the guest/mobile app; the product's configuration determines which resources are booked behind the scenes. *(agreed · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 5. Key Decisions · DI-502)*
- Six Flags Kidiya reference: fixed header with configurable navigation (logo, Explore/Tickets/Passes, sub-menus), every item toggleable via the CMS. *(client request · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review — Six Flags Kidiya Reference Walkthrough · DI-424)*
- Allam: the venue's main website is fully venue-managed; after "Book Now" the white-label B2C flow keeps the venue's header/footer branding while product selection, cart and checkout are TICVAI-managed. Header/footer links to non-checkout pages redirect to the main venue site. *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-397)*
- Ticketing, F&B and retail share one cart and checkout, one unified receipt and one QR/wristband per customer — no separate receipts or wristbands per product line. *(agreed · MoM 14 Aug 2026, 7. Retail — Cart and Inventory · DI-293)*
- Guest website and app share one CMS/publishing and the same branding, look and feel, but differ in function: the app is the full tenant experience (venue info, services, profile, purchase); a client's own website usually just links ("Buy Tickets") to a TICVAI-hosted checkout. *(agreed · MoM 14 Aug 2026, 3. Guest Website vs. Guest Mobile App · DI-284)*
- Qossai: the TICVAI name must always remain visible to end users of a client-branded guest app (e.g. a "Made by TICVAI" credit) and cannot be removed by the client. *(agreed · MoM 12 Aug 2026, 5. Guest Application Publishing and White-Labelling · DI-250)*
- Qossai: present products with video rather than static images (as Talabat-style apps do); see benchmark app "222" for further inspiration. *(client request · MoM 10 Aug 2026, 4.10 Bundle Packages · DI-222)*
- Qossai shared reference apps (Al Qadiya / Six Flags Saudi Arabia, and "The District" by Zomato) and cited their use of video over static images as design inspiration. *(client request · MoM 5 Aug 2026, 13. Mobile / POS App Design References · DI-146)*
- A single cart/order must take mixed purchases (e.g. family tickets plus gift vouchers) with one unified checkout and identity capture. *(agreed · MoM 5 Aug 2026, 7. Sales Channels, Pricing & Cart · DI-141)*
- Base ticket-booking UX (web and mobile) on current market best practice rather than the demoed references as-is; Allam recommends the "Viva Ticket" website as a reference for the flow variations. *(agreed · MoM 3 Aug 2026, 10. Reference Material & Design Research · DI-125)*
- A multi-language toggle switches the entire site's content. *(agreed · MoM 3 Aug 2026, 9. Website Structure, Localization & Authentication · DI-120)*
- Allam: banner, header, footer and background color are CMS-configurable per client, but site structure and navigation flow are fixed and adapt automatically to product configuration (dated, non-dated, seated, membership products surface the right fields). *(agreed · MoM 3 Aug 2026, 9. Website Structure, Localization & Authentication · DI-119)*
- All sites are fully mobile-responsive; e.g. the desktop calendar view collapses into a mobile-optimized layout. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-113)*
- A "powered by [platform]" footer credit is fixed and not client-editable. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-111)*
- One client can run multiple branded sites from the same setup, e.g. two brands sharing a footer but with distinct headers and hero banners. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-110)*
- White-label sites share one platform/template but each is configured independently: header, footer, logo, colors, fonts and hero banner are client-editable from the backend. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-108)*
- Selling reference layout: clean top navigation; category tabs with counts (All Events 32, Exhibitions, Guided Tours ...); sort and type chips (Price, Rating, Popular; General, Seated, Multipass, Scheduled, Rental); content cards with large image, type badge, rating, tags (LIMITED, NEW, BESTSELLER), availability ("180 available", "11 left") and "from" price; persistent cart on the right with member discount, totals and "Checkout Securely". *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - UI inspiration reference, items 2-5 · DI-026)*
- Preliminary perceived-performance targets: web pages load in under about 3 seconds, mobile app loads in under about 2 seconds, ticket validation responds in under 500 milliseconds. *(agreed · MoM 28 Jul 2026, 18. Performance and Scalability · DI-015)*

**15 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"cancelReservation": {"method":"DELETE","path":"/reservations/{reservationId}","contract":"orders","summary":"Cancel a reservation","permission":"ORDER_CANCEL","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"createResaleListing": {"method":"POST","path":"/resale-listings","contract":"orders","summary":"List an entitlement for resale","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateResaleListingRequest","responds":"ResaleListing"},
"getGroupBooking": {"method":"GET","path":"/group-bookings/{groupBookingId}","contract":"orders","summary":"A group, its leader and its name-capture duty","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GroupBooking"},
"getGroupPackageDefinition": {"method":"GET","path":"/products/{productId}/group-package","contract":"catalogue","summary":"A school-trip format or party package","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"productId","in":"path","required":true}],"requestBody":null,"responds":"GroupPackageDefinition"},
"getReservation": {"method":"GET","path":"/reservations/{reservationId}","contract":"orders","summary":"Read a reservation","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Reservation"},
"getResourceAvailability": {"method":"GET","path":"/resources/{resourceId}/availability","contract":"resources","summary":"When it is free, with conflicts already resolved","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true}],"requestBody":null,"responds":"ResourceAvailability"},
"listFxRates": {"method":"GET","path":"/fx-rates","contract":"finance","summary":"The rates in force","permission":"LEDGER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"asAt","in":"query","required":null},{"name":"purpose","in":"query","required":null},{"name":"venueId","in":"query","required":null},{"name":"chargeable","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listGroupPackages": {"method":"GET","path":"/group-packages","contract":"catalogue","summary":"The school-trip formats or party packages on offer","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMyOrders": {"method":"GET","path":"/my/orders","contract":"orders","summary":"The orders this guest placed","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":"since","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProducts": {"method":"GET","path":"/products","contract":"catalogue","summary":"List products","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"isSellable","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"segmentTag","in":"query","required":null},{"name":"guidedAnswerIds","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listReservations": {"method":"GET","path":"/reservations","contract":"orders","summary":"List reservations","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"expiringWithinMinutes","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"requestGroupBooking": {"method":"POST","path":"/group-booking-requests","contract":"orders","summary":"Ask for a school trip or a birthday party","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GroupBookingRequest","responds":"GroupBooking"},
"transferOrderTickets": {"method":"POST","path":"/orders/{orderId}/transfer","contract":"orders","summary":"Transfer tickets to another guest","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"updateTableReservation": {"method":"PATCH","path":"/table-reservations/{reservationId}","contract":"fnb","summary":"Change or cancel a booking","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"TableReservation","responds":"TableReservation"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"CreateOrderLine": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","variantId","quantity","quotedUnitPrice"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these."},"variantId":{"type":"string","format":"uuid"},"recommendationId":{"type":"string","format":"uuid","nullable":true,"description":"The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Carried from the cart line at checkout; stored on `orders.order_line` and sent in `order.completed` lines.\n"},"performanceId":{"type":"string","format":"uuid"},"bookedWindow":{"$ref":"#/components/schemas/BookedWindow"},"inventoryHoldId":{"type":"string","nullable":true,"description":"Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products."},"seatIds":{"type":"array","maxItems":50,"items":{"type":"string","format":"uuid"},"description":"Seated products only, as `seating.Seat.id`. Not available offline. **At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel** (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); **at most 10 per sale on staff and POS** (audit R080 (c)), across all the lines of one order for one performance. `createOrder` refuses more with 422 `seatLimitExceeded` (problem type `seat-limit-exceeded`)."},"resourceHoldId":{"type":"string","format":"uuid","nullable":true,"description":"A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. `createOrder` converts the hold into a `ResourceBooking` without releasing it. Not available offline."},"attributes":{"$ref":"#/components/schemas/OrderLineAttributes"},"quantity":{"type":"integer","minimum":1},"eligibilityDeclaration":{"type":"array","nullable":true,"x-ticvai-note":"One row per declared guest in `orders.order_line_eligibility` (named on `OrderLine`), because an array of objects is a child table's rows, not a column.\n","items":{"type":"object","properties":{"ageBand":{"type":"string","enum":["infant","child","junior","adult","senior"],"description":"Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+."},"ageYears":{"type":"integer","nullable":true},"heightBandIndex":{"type":"integer","nullable":true},"confidentSwimmer":{"type":"boolean","nullable":true,"description":"**Derived, kept for the gate check** (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this is filled from it (true for a `yes` covering this person, whether answered for them or once for the booking). A value sent that contradicts the record is ignored and the record wins. No longer the place a swim answer is captured.\n"},"guardianSigned":{"type":"boolean"}}},"description":"What was declared for each guest on this line, kept as the record staff check at the gate."},"quotedUnitPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the client charged, from its local bundle."},"holderName":{"type":"string","nullable":true},"dataMaskValues":{"type":"object","additionalProperties":true,"description":"**Deliberately open.** Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the venue's to define, as on `catalogue`'s own `dataMaskValues`.\n"}}},
"CreateResaleListingRequest": {"type":"object","x-ticvai-persistence":"none — request only","description":"Request only; persisted as `ResaleListing`. **What a seller decides**: which entitlement, and at what price. The id, the status, the fee snapshot and the partition key are the server's, which is why `createResaleListing` no longer takes the whole listing.\n","required":["entitlementId","askPrice"],"properties":{"entitlementId":{"type":"string","format":"uuid"},"askPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"sellerSubjectId":{"type":"string","format":"uuid","nullable":true,"description":"The holder listing it. A guest caller is always the seller and may name only themselves; a member of staff listing on a guest's behalf names the guest."}}},
"ExchangeRateDecimal": {"type":"string","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,6)","description":"**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one — a JavaScript client must not round a rate in transit. **Six decimal places**, the precision `finance.FxRate.rate` asks for, and stored at that precision.\n","pattern":"^\\d+(\\.\\d{1,6})?$"},
"FnbReservationTable": {"type":"object","x-ticvai-persistence":"fnb.reservation_table","description":"**Taken from the backend workbook, 20 September.** Maps one or more dining tables assigned to a reservation.","required":["reservationId","tableId","createdAt"],"properties":{"reservationId":{"type":"string","format":"uuid"},"tableId":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"}}},
"FxRate": {"type":"object","x-ticvai-persistence":"ledger.fx_rate","description":"Also the `setFxRate` body. **Server-owned fields are `readOnly`** and ignored if sent: `id`, `setByPrincipalId`, and the provenance `ingestFxRates` writes (`source`, `providerReference`, `fetchedAt`). A rate set through `setFxRate` has `source` `manual`.\n","required":["fromCurrency","toCurrency","rate","purpose","effectiveFrom"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"fromCurrency":{"type":"string","pattern":"^[A-Z]{3}$"},"toCurrency":{"type":"string","pattern":"^[A-Z]{3}$"},"rate":{"allOf":[{"$ref":"#/components/schemas/FxRateValue"}],"description":"Units of `toCurrency` per one `fromCurrency`. Six decimal places — a two-place rate on a three-place currency loses money on every transaction, quietly.\n"},"purpose":{"$ref":"#/components/schemas/FxRatePurpose"},"source":{"allOf":[{"$ref":"#/components/schemas/FxRateSource"}],"readOnly":true},"effectiveFrom":{"type":"string","format":"date-time"},"effectiveTo":{"type":"string","format":"date-time","nullable":true,"description":"A rate change is a new row. The old one is never edited — a transaction posted last Tuesday must still reconcile at last Tuesday's rate.\n"},"setByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"note":{"type":"string","maxLength":500,"nullable":true,"description":"Why this rate, and from where. **Required when `source` is `manual`** (decided 28 September, audit R127 (4)); null on a rate `ingestFxRates` fetched."},"providerReference":{"type":"string","nullable":true,"readOnly":true,"description":"The provider's own identifier for this quote. **What makes a rate reproducible** — an auditor asking why a payment converted at 3.6725 gets an answer that is checkable against the source rather than a number somebody typed."},"fetchedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When the rate was pulled. **Distinct from `effectiveFrom`**, which is when it applies — a rate fetched at 06:00 for a business day starting at 00:00 has two different times and conflating them makes a late feed look like a backdated rate."},"chargeable":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"description":"With `venueId`, true where a guest may select this currency and pay in it at that venue (`tenancy.VenueSettings.chargeCurrencies`), false where it is shown as an approximate price only (CHG-FIN-001)."}}},
"FxRatePurpose": {"type":"string","description":"A venue does not accept dollars at the rate it books an intercompany balance at. Separating them is what stops a spread on the counter appearing as a loss in the accounts.\n","enum":["tender","interEntity","reporting","revaluation"]},
"FxRateSource": {"type":"string","description":"**Where the rate came from, and which provider specifically.** `source: provider` said a feed set it and not which one — two tenants on different feeds were indistinguishable in the ledger, and a rate cannot be defended in an audit without naming its origin.\n\n**`uaeCentralBank` is the default for AED pairs.** The UAE Central Bank publishes an official daily rate and it is what a UAE auditor expects to see — a commercial feed is defensible for tender and awkward for statutory reporting.\n\n**`openExchangeRates` and `ecb` are the commercial and reference options.** ECB publishes daily reference rates free and is the usual fallback for non-AED pairs; Open Exchange Rates is the common commercial feed with intraday granularity. **The choice is per purpose, not per platform** — a tender rate wants intraday, a reporting rate wants the official daily close.","enum":["manual","uaeCentralBank","ecb","openExchangeRates","cardScheme","provider"]},
"FxRateValue": {"x-ticvai-persistence-column":"numeric(18,6)","type":"string","pattern":"^\\d+(\\.\\d{1,6})?$","description":"**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one (naming-and-style 5.1). Up to six decimal places — a two-place rate on a three-place currency loses money on every transaction, quietly — and stored as `numeric(18,6)` so the six places the wire carries survive the database.\n"},
"GroupBooking": {"type":"object","x-ticvai-persistence":"orders.group_booking","description":"BL-028. **`BO-026 Group Bookings` ran on generic order operations** — no group size, no quota, no leader, no per-attendee capture.\n**The leader is the point.** A school booking forty places has one person who pays, one who is called if the coach is late, and forty who need names collecting — and a generic order has one guest.\n","required":["id","orderId","leaderSubjectId","expectedSize","status"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["general","school","corporate","party"],"default":"general"},"packageProductId":{"type":"string","nullable":true,"description":"The school-trip format or party package."},"yearGroup":{"type":"string","maxLength":40,"nullable":true},"accessAndDietaryNeeds":{"type":"string","maxLength":1000,"nullable":true},"celebrantName":{"type":"string","maxLength":120,"nullable":true,"description":"The birthday child."},"celebrantTurningAge":{"type":"integer","minimum":1,"maximum":18,"nullable":true},"allergiesAndRequests":{"type":"string","maxLength":1000,"nullable":true},"finalHeadcountDueBy":{"type":"string","format":"date-time","nullable":true},"quoteSentAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"riskAssessmentSentAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"preferredDate":{"type":"string","format":"date","nullable":true,"description":"The date the guest asked for on `requestGroupBooking` — what its `409 dateUnavailable` is checked against. Null for a group a member of staff built from an order."},"orderId":{"type":"string","format":"uuid"},"leaderSubjectId":{"type":"string","format":"uuid"},"organisationName":{"type":"string","nullable":true},"expectedSize":{"type":"integer"},"confirmedSize":{"type":"integer","nullable":true},"minimumSize":{"type":"integer","nullable":true,"description":"**Below which the group rate does not apply.** A booking for forty that arrives as twelve is a pricing question somebody has to answer at the gate, and stating the threshold means answering it at booking instead.\n"},"attendeeCaptureRequired":{"type":"boolean","default":false,"description":"**Whether names are needed before admission.** A school trip usually needs them and a corporate day out usually does not, and the difference is a safeguarding requirement rather than a preference.\n"},"attendeeCaptureDueBy":{"type":"string","format":"date-time","nullable":true},"status":{"type":"string","enum":["provisional","confirmed","namesPending","complete","cancelled"]}}},
"GroupBookingRequest": {"type":"object","description":"Request only. The caller is the leader. `kind` is the same vocabulary as `GroupBooking.kind`, so a request the guest makes can be any group the venue books.","required":["kind","packageProductId","preferredDate","expectedSize"],"properties":{"kind":{"type":"string","enum":["general","school","corporate","party"]},"packageProductId":{"type":"string"},"preferredDate":{"type":"string","format":"date"},"expectedSize":{"type":"integer","minimum":2},"organisationName":{"type":"string","maxLength":200,"nullable":true,"description":"The school."},"yearGroup":{"type":"string","maxLength":40,"nullable":true},"accessAndDietaryNeeds":{"type":"string","maxLength":1000,"nullable":true},"celebrantName":{"type":"string","maxLength":120,"nullable":true,"description":"The birthday child."},"celebrantTurningAge":{"type":"integer","minimum":1,"maximum":18,"nullable":true},"allergiesAndRequests":{"type":"string","maxLength":1000,"nullable":true}}},
"GroupPackageDefinition": {"type":"object","x-ticvai-persistence":"catalogue.group_package","required":["kind","maxParticipants","durationMinutes"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"productId":{"type":"string","readOnly":true},"kind":{"type":"string","enum":["school","party"]},"maxParticipants":{"type":"integer","minimum":1,"description":"Pupils or children, e.g. 30 or 10."},"durationMinutes":{"type":"integer","minimum":15},"hostCount":{"type":"integer","minimum":0,"default":1,"description":"Party hosts included."},"pricingBasis":{"type":"string","enum":["perParticipant","perPackage"]},"freeLeaderRatio":{"type":"integer","nullable":true,"default":10,"description":"Schools: one teacher or assistant enters free per this many pupils."},"paymentMode":{"type":"string","enum":["invoice","deposit","full"],"description":"Schools are invoiced; parties take a deposit (see `DepositPolicy`)."},"includes":{"type":"array","items":{"type":"string","maxLength":120}},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."}}},
"GuestListing": {"type":"string","enum":["bookable","infoOnly","hidden"],"default":"bookable","description":"**How a product appears to a guest** (decided 29 September, rev 3 REV3-14). `bookable`: listed and searched while it is on sale, and added to the basket. `infoOnly`: listed and searched with its details, photo and `notBookableLabel` whether or not it is on sale, and **never added to a basket** (`addCartLine` refuses it with `409`); the screen opens its details instead. `hidden`: never listed or searched for a guest, and reachable only where a staff channel sells it. Independent of `isSellable`, which says whether a channel may sell it at all.\n"},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"Order": {"x-ticvai-persistence":"orders.sales_order + orders.order_line","type":"object","required":["id","venueId","scopePath","channel","status","currency","currencyScale","grossAmount","taxAmount","netAmount","lines","createdAt","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The client UUIDv7 from `CreateOrderRequest.id`."},"orderNumber":{"type":"string","readOnly":true,"description":"The number a guest reads and a cashier types. **Server-assigned: the venue prefix and a sequence per venue**, for example `DXB1-000123` (decided 28 September, audit R152). A till holds a reserved range of the venue sequence, so an order taken offline gets its number on the till and keeps it through `syncOrders`. **Not gapless**: an unused reserved range leaves a gap, and that is allowed. Only tax invoices are gapless, per legal entity. The receipt carries this number.\n"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for within a month of launch.\n"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"chargeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**The currency the guest selected and is charged in** (CHG-FIN-001, 2 October 2026). Null or equal to `currency` for a sale in the base currency. Everything else on the order, and every ledger posting, stays in the base currency `currency`."},"chargeFxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"readOnly":true,"description":"Units of `chargeCurrency` per one unit of the base currency, from the region's `tender` rate in force at checkout (`finance.FxRate`), stored on the order so the payment, the receipt, the tax invoice and any refund use the same rate (CHG-FIN-001)."},"chargeFxRateId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `finance.FxRate` row the rate was taken from, for audit."},"chargeTotal":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"`grossAmount` converted at `chargeFxRate` and rounded to the charge currency's scale: what the guest pays and what the payment request to the provider asks for (CHG-FIN-001)."},"chargeRateLockedUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"The quote holds until then (the cart lease). After it, the next payment attempt re-quotes at the rate then in force and the guest confirms the new amount (CHG-FIN-001)."},"droppedPromotions":{"type":"array","readOnly":true,"x-ticvai-persisted":false,"description":"**Promotions left off this order at checkout because their budget cap would have been exceeded** (decided 28 September, audit R101 (8)). Empty when none was dropped. Returned by `checkoutCart` and `createOrder`, not stored.\n","items":{"type":"object","required":["promotionId"],"properties":{"promotionId":{"type":"string","format":"uuid"},"name":{"type":"string"},"reason":{"type":"string","enum":["budgetCapReached"]}}}},"totalPriceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Sum across lines. Zero on a normal order."},"lines":{"type":"array","items":{"$ref":"#/components/schemas/OrderLine"}},"payments":{"type":"array","items":{"$ref":"#/components/schemas/Payment"}},"principalId":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid"},"shiftId":{"type":"string","format":"uuid","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"holdLabel":{"type":"string","maxLength":60,"nullable":true,"readOnly":true,"description":"The `label` a cashier gave when parking it with `holdOrder` — how they find it again. Null on an order never held."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When a held order expires and is voided (states/order.yaml), from `holdOrder`'s `holdUntil`. Null on an order not currently held."},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"OrderChannel": {"type":"string","description":"Where the order originated. Added when guest self-ordering was contracted — an order a guest placed on their own phone is commercially and operationally different from one a cashier typed, and reporting that cannot separate them cannot answer whether self-ordering is working.\n","enum":["pos","kiosk","guestApp","guestWeb","callCentre","partner","api","backOffice"]},
"OrderLine": {"x-ticvai-persistence":"orders.order_line + orders.order_line_eligibility + orders.order_line_discount","x-ticvai-retired-columns":["promotion_id","name","reason"],"allOf":[{"$ref":"#/components/schemas/CreateOrderLine"},{"type":"object","required":["serverUnitPrice","taxAmount","netAmount","grossAmount"],"properties":{"serverUnitPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the server computed on ingest."},"priceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Server minus quoted. Non-zero means the quoted price was honoured and the difference posted to the variance account.\n"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"entitlementIds":{"type":"array","description":"The entitlements this line issued. **These are the ticket ids** — `transferOrderTickets.ticketIds` and `reprintOrder.reissuedTicketIds` take and return them.","items":{"type":"string","format":"uuid"}},"crossRegionRightIds":{"type":"array","items":{"type":"string"},"description":"Redemption rights propagated to other cells for this line."},"reprintCount":{"type":"integer","minimum":0,"default":0,"readOnly":true,"description":"How many times this line's tickets were reprinted or resent. `reprintOrder` increments it; repeated reprints are the signal worth surfacing."},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"The order's venue, copied onto the line (ADR-0044's own example; system-design review SD-008, 29 September) so a line is scoped and partitionable without its order."},"discounts":{"type":"array","readOnly":true,"description":"**The discounts applied to this line, one row each** (system-design review SD-008, 29 September). Until then a discount object was flattened into the line as `promotion_id NOT NULL`, so a line with no promotion could not be inserted. A line with no discount has none.","items":{"$ref":"#/components/schemas/OrderLineDiscount"}}}}]},
"OrderStatus": {"type":"string","enum":["pending","held","paid","partiallyPaid","completed","voided","refunded","partiallyRefunded","failed"],"description":"`held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed.\n"},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Payment": {"x-ticvai-persistence":"orders.payment","type":"object","required":["id","orderId","tender","amount","status","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid"},"tender":{"$ref":"#/components/schemas/TenderKind"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","description":"4.6.11. **What the guest actually handed over**, which is not always what the venue books. A tourist paying USD cash at a till is a foreign tender; the sale is still recorded in base currency.\nEqual to the base currency for almost every payment. **Present on all of them so the foreign-tender report has a source** — `getForeignTenderReport` promised *what was taken in which currency* and nothing recorded it until 18 August.\n"},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"The amount in `tenderCurrency`, at that currency's own scale."},"fxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"description":"The rate applied, **stored on the payment rather than looked up later** (CF-37). A payment reconciled next month is reconciled at the rate of the day it was taken.\n"},"fxRateSource":{"type":"string","nullable":true,"enum":["manual","feed","cardScheme"],"description":"4.2.8. Manual or fed on a schedule. **`cardScheme` is where the terminal did the conversion and told us** — dynamic currency conversion, the scheme's rate rather than ours.\n"},"changeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"description":"4.6.11 is deliberately asymmetric: **accept foreign currency, refund in local.** A till giving change in five currencies needs five floats and five counts, and the variance becomes unattributable.\n**Cash at a till only** (CHG-FIN-001, 2 October 2026). A card or wallet payment the guest made in a currency they selected is refunded in that currency (`Refund.tenderCurrency`).\n"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"changeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["authorised","captured","pendingConfirmation","declined","failed","voided","refunded"]},"providerName":{"type":"string","nullable":true},"providerReference":{"type":"string","nullable":true,"description":"The provider's own id for the charge (Stripe PaymentIntent, NI order reference). What `payments.receivePaymentProviderWebhook` matches an incoming event on (SD-034)."},"providerIdempotencyKey":{"type":"string","nullable":true,"readOnly":true,"description":"The idempotency key sent to the provider, which is this payment's `id` (SD-034, 29 September). A retried provider call cannot charge twice."},"terminalId":{"type":"string","format":"uuid","nullable":true,"description":"The card terminal a till payment ran on (ECR flow, SD-034)."},"nextAction":{"type":"object","nullable":true,"x-ticvai-persisted":false,"description":"**What the caller does while the payment is `pendingConfirmation`** (SD-034, 29 September). `redirect`: send the browser to `url` (3-D Secure challenge or hosted page); the provider returns the guest to `returnUrl` and the result arrives by webhook. `terminal`: the card terminal has been instructed; wait for its result. Null once the payment has an outcome.","properties":{"kind":{"type":"string","enum":["redirect","terminal"]},"url":{"type":"string","format":"uri","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true}}},"lastInquiryAt":{"type":"string","format":"date-time","nullable":true},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"Product": {"x-ticvai-persistence":"catalogue.product","type":"object","required":["id","code","name","kind","venueId","scopePath","isSellable","hasVariants"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"familyKey":{"type":"string","maxLength":64,"pattern":"^[A-Za-z0-9_-]+$","nullable":true,"x-ticvai-unique":"venue","description":"**The same product at another location** (decided 29 September, rev 3 REV3-18). Optional. A tenant that sells one attraction at several venues gives each venue's product the same key, e.g. `aquarium-entry`; the key names the family across the tenant and each venue has at most one product in it, so a second product at the same venue with the key is refused with `409 duplicate-code`. **What it is for:** when a guest changes location on the booking screen (the 'Booking at' switcher, `BookingFlowConfig.locationSwitcher`), lines whose product shares a `familyKey` with a product at the new venue are carried over to that product, with times and prices refreshed; every other line is cleared. Null means the product belongs to no family and its lines always clear on a switch. Compared case-insensitively, like `code`.\n"},"name":{"type":"string","maxLength":200},"description":{"type":"string"},"kind":{"$ref":"#/components/schemas/ProductKind"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"createdByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"1.4.18. **The approval gate refuses an approver who is the author, and nothing recorded either.** `SeatBlock`, `DelegatedAccess` and `ManualDiscountRequest` all carry this and the product passing through approval did not.\n"},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"responsibleDepartmentId":{"type":"string","format":"uuid","nullable":true,"description":"Who owns this product commercially. A scope node at `department` level."},"onSaleFrom":{"type":"string","format":"date-time","nullable":true,"description":"1.4.8. **A seasonal product should not need somebody awake at midnight.** Archiving already runs on a timer in this contract, so the machinery exists; `effectiveFrom` appears on tax codes, FX rates and white-label policies and not here.\n"},"onSaleTo":{"type":"string","format":"date-time","nullable":true,"description":"Retires the product automatically. **Retirement is not deletion** — the product stops selling and every order that referenced it still resolves.\n"},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"**Taken from their `fnb.product` and `retail.product`, 20 September.** `catalogue.product_category` has existed since 20 August with two operations and nothing could be filed under it — a merchandise hierarchy with a tree and no leaves. Their per-domain product tables both carried this column and ours did not.\n"},"lifecycleState":{"$ref":"#/components/schemas/ProductLifecycleState"},"isSellable":{"type":"boolean","readOnly":true,"description":"True only when live **and** carried by a published bundle. Approval and publication are different acts.\n**Derived, never set.** It changes when `transitionProductLifecycle` moves the product and when `publishBundle` carries it, so `updateProduct` does not take it — `withdraw` is how a product stops selling.\n"},"isStockTracked":{"type":"boolean","default":false,"description":"**Taken from their `fnb.product`, 20 September.** Whether a sale decrements stock, which is not what `isSellable` asks. A ticket is sellable and tracks no stock; a bottle of water is both. Without it, an F&B sale cannot tell inventory whether to move.\n"},"hasVariants":{"type":"boolean"},"variantCount":{"type":"integer"},"segmentTags":{"type":"array","description":"7.3.5. **A channel and a segment tag are mandatory and nothing required either.** A catalogue that cannot be filtered by segment is a catalogue nobody can report on.\n**Hierarchical, not flat** — `family/with-toddlers` narrows `family` without duplicating it, which is how the promotions engine already treats scope.\n**A level is a tag under `level/`** (decided 29 September, rev 3 REV3-19): `level/beginner`, `level/intermediate`, `level/advanced`, `level/expert` (proposed codes, client to correct). A guest screen filters on it with `listProducts` `segmentTag`, and the words a guest reads beside each option come from `ProductCategory.description`, not from the tag.\n","items":{"type":"string"}},"codeSchema":{"type":"string","readOnly":true,"description":"7.3.4 specifies `[ParkCode]-[ProductType]-[Variant]`. **`Product.code` existed and nothing required a format**, so a venue with three thousand products had three thousand conventions.\nThe tenant sets the pattern and the platform generates against it. **Validation is the point, not the string** — a code typed by hand is a code that will not sort.\n"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/Channel"}},"entitlementTemplateId":{"type":"string","format":"uuid","nullable":true,"description":"What the buyer receives. Null for products that grant nothing — F&B and retail. Identity and entitlement are separate concerns.\n"},"blockedOffline":{"type":"boolean","description":"True for seated and retail. Seated because a seat map is not a count; retail because stock depletes in real time.\n"},"dataMaskValues":{"type":"object","additionalProperties":true,"description":"Custom fields. JSONB-backed, defined by the venue's data mask."},"guestListing":{"$ref":"#/components/schemas/GuestListing"},"notBookableLabel":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"The label a guest reads on an `infoOnly` product, e.g. *Info only* or *Not bookable online; ask at the desk* (decided 29 September, rev 3 REV3-14). Each value at most 60 characters. Null means the guest screen shows its default wording. Ignored unless `guestListing` is `infoOnly`.\n"},"salesContact":{"allOf":[{"$ref":"#/components/schemas/ProductSalesContact"}],"nullable":true,"description":"**Who a guest contacts to book a view-only product** (decided 29 September, W3), e.g. a training course listed with full details and no Book button. Shown as *Call sales* and *Email sales* on an `infoOnly` product. Null means the venue's own contact (white-label `getTenantAppStatus.contact`). Ignored unless `guestListing` is `infoOnly`.\n"},"bookingFlowId":{"type":"string","format":"uuid","nullable":true,"description":"**The booking flow this product is sold through** (decided 29 September, W8 and W12): a white-label `BookingFlow` of the venue, which orders the guest's steps (for a workshop, the product first and then the date and time). Null means the category's flow (`ProductCategory.bookingFlowId`), and failing that the venue's flow for the product's `kind`. Written by `createProduct` and `updateProduct`, which refuse an id that is not a flow of the venue with `422`.\n"},"displayTags":{"type":"array","maxItems":6,"items":{"$ref":"#/components/schemas/ProductDisplayTag"},"description":"**Short facts a guest reads on the ticket card and under *Read more***: *2 Hours*, *Min 1.10 m*, *Free adult entry*, *Valid 90 days*, *Emirates ID* (decided 29 September, 23SEP-3). Not `segmentTags`, which are for reporting and segmentation and which a guest never reads.\n**Derived on read when none are set.** When the venue has written no tags, a read returns tags derived from the product's duration (`clock`), entitlement validity (`calendar`) and the eligibility rule's `minHeightCm` (`height`), each marked `derived: true`; they are never stored. Once the venue writes any tag, only what it wrote is returned. Whether the guest screen shows them is `BookingFlowConfig.ticketTags` (white-label).\n"},"media":{"type":"array","maxItems":20,"items":{"$ref":"#/components/schemas/ProductMedia"},"description":"**The product's own photos and video** (decided 29 September, 23SEP-4). *Read more* opens on the `isPrimary` item, and a listing shows each product's primary image, so two tickets in one category no longer share the category's picture (`ProductCategory.imageAssetId`).\nEvery `assetId` names an asset of the asset library (`assets.yaml` `MediaAsset`) in status `ready` whose kind matches `kind`; anything else is a `422`. **Exactly one item is `isPrimary`** when the list is not empty, and an `assetId` appears once; otherwise `400`. Setting the list records each reference as asset usage (`MediaUsage` with `surface: product`, `referenceId` the product id, `isLive` true while the product is listed to guests), which is what stops a used asset being archived from under the product.\n"},"consentQuestionIds":{"type":"array","maxItems":10,"uniqueItems":true,"items":{"type":"string","format":"uuid"},"description":"**The consent questions a guest answers when booking this product**, in the order they are asked (decided 29 September, rev 3 REV3-26): *Are you able to swim?*, *Do you hold a scuba certification?*, *I accept the risk*. Each id names a consent question defined in marketing-crm (`ConsentQuestion`), which owns the text, its version and whether it is asked per person or once per booking; the answer is stored there as a consent record (question version, answer, who answered, when). **One question or several, as the venue chooses.** A flow can carry its own list too (`white-label.BookingFlow.settings.consentQuestionIds`, on the product's published booking flow as `getPublishedBookingFlow` resolves it: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig` 29 September, W12); a booking asks the union of the flow's questions and those of every product in the cart, each question once (`orders.Cart.consentQuestions`). An id that names no active consent question of the tenant is a `422`.\n"},"requiresTimeWindow":{"type":"boolean","default":false,"description":"**True for a space sold by the hour**, e.g. a meeting room type (decided 29 September, rev 3 REV3-13). The product is the room type (*focus pod*, *majlis*, *boardroom*, *auditorium*), never a named room; its lengths are a `length` axis (`setProductAttributes`) whose values carry `durationMinutes`, and each length is a variant priced on its own in the price list, so price is the room rate for that length. The cart line carries the booked start and end (orders), the end being the start plus the chosen variant's `durationMinutes`; `resources.listProductStartTimes` supplies the start times for a variant and a date and `allocateResources` picks the room from the product's resource requirements (`setExperienceResourceRequirements`) at checkout. True requires every active variant to have a `durationMinutes`; otherwise `422`.\n"},"productOwnerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The product owner (29 September, data model DM3), set with `setProductContextOwnership`. `responsibleDepartmentId` is the owning department."},"operationalContact":{"type":"string","maxLength":200,"nullable":true,"description":"A principal id or a name, as the context screen takes it."},"businessUnitId":{"type":"string","format":"uuid","nullable":true},"legalEntityId":{"type":"string","format":"uuid","nullable":true,"description":"A `ledger.legal_entity`, read through finance."},"attractionId":{"type":"string","format":"uuid","nullable":true},"siteId":{"type":"string","format":"uuid","nullable":true},"locationId":{"type":"string","format":"uuid","nullable":true},"brandId":{"type":"string","format":"uuid","nullable":true,"description":"The brand, as the context screen names it (a catalogue brand category)."},"marketCode":{"type":"string","maxLength":40,"nullable":true},"salesTerritory":{"type":"string","maxLength":100,"nullable":true}}},
"ProductDisplayTag": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","required":["kind","label"],"description":"One short fact on a ticket card (decided 29 September, 23SEP-3). `kind` picks the icon.","properties":{"kind":{"type":"string","enum":["clock","height","free","calendar","id"],"description":"`clock` a duration, `height` a height rule, `free` something included free, `calendar` a validity, `id` a document the guest must bring."},"label":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"What the guest reads, e.g. *2 Hours*. Each language value at most 40 characters."},"derived":{"type":"boolean","readOnly":true,"default":false,"description":"True on a tag the server derived on read because the venue set none. Never sent."}}},
"ProductKind": {"type":"string","description":"**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n","enum":["admission","timedAdmission","datedAdmission","openDated","seated","membership","bundle","fnb","retail","rental","addOn","giftCard"]},
"ProductLifecycleState": {"type":"string","enum":["draft","inReview","approved","live","withdrawn","archived"]},
"ProductMedia": {"x-ticvai-persistence":"catalogue.product_media","type":"object","required":["assetId","kind","isPrimary"],"description":"One photo or video of a product, referencing the asset library (decided 29 September, 23SEP-4). One row per product and asset, so the asset library can answer which products use an asset.\n","properties":{"assetId":{"type":"string","format":"uuid","description":"A `MediaAsset` of `assets.yaml`, in status `ready`."},"kind":{"type":"string","enum":["image","video"]},"isPrimary":{"type":"boolean","default":false,"description":"The item *Read more* opens on and a listing shows. Exactly one per product."},"displayOrder":{"type":"integer","default":100},"altText":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true}}},
"ProductSalesContact": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","description":"Who to contact to book a view-only product (decided 29 September, W3). At least one of `phone` or `email`.\n","minProperties":1,"properties":{"phone":{"type":"string","maxLength":32,"nullable":true},"email":{"type":"string","format":"email","maxLength":254,"nullable":true},"note":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"A line shown under the contact, e.g. *Group courses are booked by phone*. At most 200 characters per language."}}},
"ResaleListing": {"type":"object","x-ticvai-persistence":"orders.resale_listing","description":"BL-060. **Smaller than it first looked** — most of the machinery exists. An entitlement can already be transferred, an order can already be created, and payment already routes. What was missing is the listing itself and a cart line that can point at one.\n**A resale is a transfer with money attached**, and the venue is in the middle: the buyer becomes the owner of the same entitlement (the virtual ticket ID is preserved, MoM 1 Sep 4.14), its media is re-issued and the transfer is logged, so **the media that admits is always one the venue issued.** That is what stops a screenshot at the gate.\n","required":["id","entitlementId","sellerSubjectId","askPrice","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"entitlementId":{"type":"string","format":"uuid"},"sellerSubjectId":{"type":"string","format":"uuid"},"askPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"priceCapPercent":{"type":"number","nullable":true,"readOnly":true,"description":"**A ceiling as a percentage of face value**, because uncapped resale is a venue watching its own tickets sold at four times the price with its name on them. Null means uncapped, which is a venue decision rather than a default. Snapshotted from `ResaleFeePolicy` at listing.\n"},"sellerFeePercent":{"type":"number","readOnly":true,"description":"Snapshotted from `ResaleFeePolicy` at listing."},"buyerFeePercent":{"type":"number","readOnly":true,"description":"Snapshotted from `ResaleFeePolicy` at listing."},"status":{"type":"string","readOnly":true,"enum":["pendingReview","listed","reserved","sold","withdrawn","expired","rejected"],"description":"`pendingReview` and `rejected` added 29 September (DM5): a listing the marketplace's `moderationMode` sends to review waits there until `approveListingModeration` lists or rejects it."},"listedAt":{"type":"string","format":"date-time","readOnly":true},"soldToSubjectId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"reviewReasons":{"type":"array","readOnly":true,"description":"Why the listing was sent to review (DM5, 29 September).","items":{"type":"string","enum":["highResalePrice","unusualDiscount","highValueTicket","vipTicket","sellerRisk","newSeller","multipleListings","identityIssue","paymentIssue","ticketOwnershipConcern","fraudIndicator"]}},"moderatedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"moderatedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"moderationReason":{"type":"string","maxLength":1000,"nullable":true,"readOnly":true},"payoutStatus":{"type":"string","readOnly":true,"enum":["pending","held","paid","failed"],"description":"**The seller is paid after the buyer is admitted, not after they pay.** A resale refunded at the gate for a void ticket cannot be clawed back from a seller who has already been paid.\n"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"Reservation": {"x-ticvai-persistence":"orders.reservation + orders.reservation_line","type":"object","description":"**An unpaid hold, not a booking.** It holds capacity, expires, issues no entitlement and carries no media — a paid booking is an order (naming-and-style §3.1).\n","required":["id","venueId","status","expiresAt","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"The guest it is held for, from `CreateReservationRequest.subjectId`. A guest caller sees only reservations carrying their own."},"status":{"type":"string","enum":["held","converted","expired","cancelled"]},"lines":{"type":"array","items":{"$ref":"#/components/schemas/CreateOrderLine"}},"expiresAt":{"type":"string","format":"date-time"},"createdAt":{"type":"string","format":"date-time"},"convertedOrderId":{"type":"string","format":"uuid","nullable":true}}},
"ResourceAvailability": {"type":"object","description":"**Free windows, with setup and teardown already subtracted.** A client computing this from bookings will forget the turnaround.\n","properties":{"resourceId":{"type":"string","format":"uuid"},"freeWindows":{"type":"array","items":{"type":"object","properties":{"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"}}}},"blockedWindows":{"type":"array","description":"**With a reason, because they are not the same.** Booked and under repair need different responses from an operator looking for something free — wait, or look elsewhere.\n","items":{"type":"object","properties":{"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"reason":{"type":"string","enum":["booked","held","setup","teardown","maintenance","blackout","closed","cleaning"],"description":"`held` is a live `ResourceHold` (rev 3 REV3-15): taken now, free again if it expires. `cleaning` is a cleaning the resource's `cleaningPolicy` places (W10, 29 September).\n"}}}}}},
"TableReservation": {"type":"object","x-ticvai-persistence":"fnb.table_reservation","x-ticvai-retired-columns":["table_ids"],"required":["outletId","startsAt","partySize"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"outletId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true},"guestName":{"type":"string"},"contactPoint":{"type":"string"},"partySize":{"type":"integer","minimum":1},"startsAt":{"type":"string","format":"date-time"},"durationMinutes":{"type":"integer","description":"**How long the cover is held.** An outlet turning tables twice an evening needs this to be real, or the second sitting cannot be booked.\n"},"tables":{"type":"array","description":"The dining tables assigned to this reservation, one row each.\n**Usually empty until seating.** Committing a specific table at booking time refuses later bookings against a constraint that did not need to exist — that was true of the `tableIds` array this replaces and it is still true, because it is about *when* a table is assigned rather than how the assignment is stored.\n**Replaces `tableIds`, retired 20 September.** An array cannot carry per-row state, which is the same reason this merge took `entry_rule_point`, `menu_item_modifier`, `seat_block_item`, `plan_benefit`, `payment_method_config` and `tier_module` from the backend workbook. A party seated across three tables that releases one early has nowhere to say so in an array, and *\"which reservations are on table 7 tonight\"* is a GIN scan over every reservation instead of an index seek.\n","items":{"$ref":"#/components/schemas/FnbReservationTable"}},"status":{"$ref":"#/components/schemas/TableReservationStatus"},"groupId":{"type":"string","format":"uuid","nullable":true,"description":"5.1.2. Several bookings managed as one party across adjacent tables."},"notes":{"type":"string","description":"Allergies, accessibility needs and other requests, as the guest wrote them."},"seatingPreference":{"type":"string","maxLength":64,"nullable":true,"description":"**The seating area the guest asked for**, e.g. indoor, terrace, majlis (Chinmay, 2 October, workbook Q204; DI-791; CHG-CSA-018). The outlet's own area names, as the waitlist's `RestaurantWaitlist.seatingPreference` takes them. A preference, not a table: the host seats the party on the night."},"occasion":{"type":"string","nullable":true,"enum":["birthday","anniversary","business","celebration","other"],"description":"The occasion the guest named (workbook Q204, DI-337; CHG-CSA-018). Shown to the host and the server; never a price."},"takenByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The staff member who took the booking (`createTableReservationForGuest`); null for a guest's own booking (CHG-CSA-045)."},"actualPartySize":{"type":"integer","nullable":true,"readOnly":true},"tableVisitId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"deposit":{"$ref":"#/components/schemas/TableReservationDeposit"},"createdAt":{"type":"string","format":"date-time","readOnly":true}}},
"TableReservationDeposit": {"type":"object","nullable":true,"readOnly":true,"x-ticvai-persistence":"fnb.table_reservation","description":"**The deposit this booking holds, snapshotted from `orders.DepositPolicy.dining` when it was made** (decided 29 September, rev 3 REV3-8b). Null where no deposit applied, which is every booking while the venue leaves `dining.enabled` false (the default). A later change to the policy does not re-price a booking already made.\n","required":["amount","basis"],"properties":{"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"basis":{"type":"string","enum":["fixedPerGuest","fixedPerTable","percentOfMinimumSpend"]},"holdExpiresAt":{"type":"string","format":"date-time","nullable":true,"description":"While `awaitingDeposit`, when the held cover is released if the deposit has not been authorised. The cart lease of the deposit line (15 minutes, audit R169)."},"refundableUntil":{"type":"string","format":"date-time","nullable":true,"description":"`startsAt` less `dining.refundableUntilHours`. Cancelling before it releases the deposit in full."},"variantId":{"type":"string","format":"uuid","description":"The venue's table-deposit variant, `DepositPolicy.dining.depositVariantId`, which the client sends to `addCartLine` with this booking's id."},"cartLineId":{"type":"string","format":"uuid","nullable":true,"description":"The `orders.CartLine` carrying the deposit, once added."},"depositId":{"type":"string","format":"uuid","nullable":true,"description":"The `orders.deposit` row, once the payment is authorised."}}},
"TableReservationStatus": {"type":"string","description":"`awaitingDeposit` only where the venue's dining deposit applies (decided 29 September, rev 3 REV3-8b); a booking with no deposit starts `booked`.","enum":["awaitingDeposit","booked","confirmed","seated","completed","cancelled","noShow"]}
}
```
