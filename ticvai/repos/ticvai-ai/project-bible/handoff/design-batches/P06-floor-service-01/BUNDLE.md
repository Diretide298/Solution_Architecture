# P06-floor-service-01 — P06 · Floor Service

**10 screens · 39 operations · 46 schemas · 8 permissions**

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

- **Every control that can be refused must be gated.** 8 permissions apply here:
  `GUEST_MANAGE, GUEST_VIEW, ORDER_CREATE, ORDER_MODIFY, ORDER_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW, REPORT_VIEW_VENUE`. A control nobody can use must say so,
  not sit enabled and fail.
- **23 of these operations work offline**: addGuestNote, compItem, createFnbOrder, createPayment, fireCourse, getBill, getFnbReservationPolicy, getTableMap
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

### Food, Beverage & Retail

Food & beverage, retail, rentals, inventory and procurement across the till (P04), the kitchen display (P15), the staff app (P06), Venue Management (P08), the guest web and app (P01/P02), the kiosk (P05) and the CMS (P13). COUNTER SERVICE (F108): the cashier takes the order on the Food & Drink board from the outlet's menu in force (sections in the outlet's order, option groups attached to the item), sends it to the kitchen, and only then charges — send to kitchen, then charge, for every POS F&B order (R261, upheld against the v2 frame by POSV2-4). The kitchen ticket is on the rail while the card is in the guest's hand; an unpaid sent order is cancelled while ordered or accepted and voided with a reason after (R125(3), R091(5)); the guest gets an order number, and the customer-facing status board (numbers only) is the kitchen display's KIT-007, mirrored on the till's queue (POSV2-7). TABLE SERVICE (F29, F80, F94): a party is seated with its covers, orders across the visit, courses are fired by the pass (DI-333, DI-407), the bill is printed and settled at the end and split by amount, covers, category, item or seat (DI-106); the client's table statuses are Available → Ordered → Table closed → Reserved with no cleaning status (DI-336); moving and merging tables stay on the staff app until after r2 (POSV2-8). GUEST ORDERING (F11, F48): a guest inside the venue orders in the app or web for pickup or delivery to a seat or a scanned location (DI-288, DI-291); F&B and retail are optional licensed modules completed inside TICVAI (DI-505), kept simple (DI-1091); no food without an admission ticket (DI-292); table reservations and the waitlist do not go through the cart and a dining deposit is a venue option, off by default (DI-1048, DI-1049, R077). KITCHEN (P15, F83, F88): TICVAI's own display on commodity screens (19 September, replacing the 31 July "integration point only", DI-077); one kitchen ticket per preparation station from the outlet's routing rules with a fallback display (DI-323); a fired timer counts up and resets per course, not shown for quick service (DI-334); displays are assigned to stations and filter by course, with no station-load tile in r1 (R277). 86 takes an item off sale on every till and guest menu immediately (R110(c)); guests always see "Sold out", never a missing dish. RETAIL (F17, F34, F51): scan and sell through the same cart, charge and payment as tickets and food (DI-795), one cart, one receipt and one QR per guest (DI-293); system stock per venue gates the sale (DI-294); returns by receipt or order number only in r1 (R139(c)), refund to the original tender with a reason code and note (DI-796, DI-797); Shop & Drop is paid online and collected on the way out (R236), a merchandise reservation lasts to the end of the visit day (R169, R215). TILL MONEY (F32, F73, F74, F87): the float is counted by denomination with note images and typed quantities (DI-775, DI-776, R229) while the hardware checks itself (DI-778); the close is a …

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Send to kitchen | Put the order on the kitchen rail. On the till it always comes before Charge. | Fire, Fire order, Submit order, kitchen fires on payment | R261 / POSV2-4 / F108 step 3 |
| Charge | The till's single tender step (Payment, POS-005); the button reads "Charge AED 110.25". | Checkout (on staff screens), Pay now | F108 step 4 / screens/P04-point-of-sale.yaml#POS-021 |
| Fire / Hold (a course) | Kitchen-pass words for releasing or holding the next course of a table, and the "fired" timer. | using "fire" for sending an order from the till | DI-333 / DI-334 / DI-407 |
| Kitchen ticket | The slip on the kitchen display, one per preparation station. | Order (on the kitchen display), KOT | R210 |
| Ready · Served · Collected · Delivered | How an order reaches the guest; a server marks Served, a counter Collected, a runner Delivered (with the location). | Done, Complete, Bumped (as a status) | R125 / contracts/satellite/fnb.yaml#recordOrderHandover |
| Recall (kitchen) / Recall held sale (till) | Bring a mis-bumped kitchen ticket back to the rail; separately, bring a held cart back into a sale. Never "Recall" alone where both could apply. | Undo bump, Restore | contracts/satellite/fnb.yaml#recallKitchenTicket / POSV2-6 |
| Unavailable (86) / Sold out | Staff screens say "Unavailable" and may add "86"; guest screens say "Sold out". Immediate everywhere. | Out of stock (for food), Disabled, Hidden | R110 / contracts/satellite/fnb.yaml#getGuestMenu |
| Order type | Dine-in · Quick service · Takeaway · Delivery, chosen in the cart. | Service mode, Fulfilment source (on the till) | DI-789 / contracts/satellite/fnb.yaml#/components/schemas/ServiceMode |
| Covers | The number of guests at a table, entered when seating; drives split-by-covers. | Pax (except as a small suffix on the floor plan), Heads | DI-104 / contracts/satellite/fnb.yaml#openTableVisit |
| Vacant · Seated · Ordered · Bill requested · Table closed · … | Table statuses on every floor plan (till and staff app); "Table closed" is the client's word for after payment. | Cleaning, Needs clearing, Dirty | DI-336 / DI-792 |
| Till · Cash drawer | Staff copy may say "till" for the workstation; the cash drawer is the deposit box. | Terminal id as a heading, Deposit box (on staff screens) | R156 |
| Float · Count · Blind count · Variance | The opening float; the denomination count; the closing count made without seeing the expected cash; counted minus expected. | Expected in drawer, Discrepancy, Error | R080 / POSV2-3 |
| Cash out · Cash in · Safe drop | Taking cash out of the drawer mid-shift, adding change, and a supervisor moving cash to the safe with the cashier as witness. | Lift, Withdrawal (as button labels) | DI-274 / contracts/spine/shift.yaml#createCashMovement / … |
| Menu item · Merchandise item · Inventory item · SKU | The scoped product words; SKU is a variant's code, Product stays the sellable thing. | SKU as the item's name, Article | R131 |
| Stock on hand · Allocated · Available | Available is on hand minus allocated. | Inventory (as a number), Free stock | R171 / DI-361 |
| Requisition · Purchase order · Goods receipt · Transfer · … | The procurement and stock words, in that flow. | GRN as the only label, Indent | DI-341 / DI-348 / DI-362 / DI-363 |
| Shop & Drop | Bought and paid now, collected on the way out. | Click & collect | R236 |
| Check-out (rental) · Return (rental) | Handing equipment to the guest and taking it back. On the same screens payment is "Charge" or "Pay". | Checkout (for a handover), Check-in (for a return) | DI-758 / DI-765 |
| Deposit hold · Release · Capture | A refundable deposit held, given back in full, or partly kept for damage with the rest released. | Charge deposit, Refund deposit | DI-752 / R127 |
| Extension · Swap · Overdue · Late fee | The active-rental words; a quick swap restarts the clock, a late swap earns a free extension. | Renewal, Exchange (for a swap) | DI-761 / DI-762 / DI-764 |

### Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers)

Customer & marketing is how a venue knows its guests and talks to them. There is ONE guest profile per person across ticketing, F&B and retail, so a guest who books online and later dines is the same profile (DI-339). A profile needs at least an email or a mobile, never neither (DI-372). Profiles are created by registration, by guest checkout, or by staff at a till or desk. Repeat guest checkouts with the same verified email or phone attach to the same profile automatically (DI-941, R120 default). Two records that might be the same person are NEVER merged automatically: the guest is asked to confirm, and an admin review queue runs alongside (DI-377). Each candidate shows why it matched; the record that loses is superseded, not deleted; consent takes the narrower of the two positions (DI-808). Around the profile sit three things that must never be confused. CONSENT is what the law allows: per purpose and per channel, append-only, with the notice version and the source (recordConsent). It is Given, Withdrawn or Not asked. A SUBSCRIPTION is what the guest asked to receive, e.g. a newsletter list (MarketingSubscription). A PREFERENCE is what they like: table, dietary, accessibility (updateGuestPreferences). An anonymous visitor's cookie decision is recorded against a device key (recordDeviceConsent) and attaches to the guest when they sign in (claimDeviceConsent). Marketing consent at GUEST CHECKOUT is an open client question, and the design follows its default: an unticked opt-in beside the terms, one per channel and purpose. It is recorded with source "checkout" against the order and the verified contact, and nothing is sent without it. Whether that is sufficient consent under PDPL is the client DPO's call (M18-15 (audit R-M18-15), DI-954, DI-940). Marketing reads profiles through SEGMENTS (rules, evaluated when used) and static LISTS (imported). It reaches guests by CAMPAIGNS (one send to an audience) and JOURNEYS (automations started by an event, with waits and branches). Journeys may offer only pre-configured offers, never a free-typed discount (MoM 2026-08-20 4.6). Everything goes through ONE communications module that every other module uses (MoM 2026-08-31 4.6). Consent and suppression are applied at send time, and the number excluded, with the reasons, is reported before anything goes out (launchCampaign). Transactional messages (tickets, receipts, queue calls, case replies) do not need marketing consent and must never carry marketing. LOYALTY pays for spend: points, tiers, rewards and expiry. GAMIFICATION pays for behaviour: challenges, badges, streaks, referrals and leaderboards (createChallenge). A guest reads their own loyalty position (getLoyaltyPosition). A till, the back office or support reads a named guest's (getGuestLoyalty, or identifyGuest at a till). SERVICE: one Case object covers lost property, complaints, questions, accessibility and refund requests (CaseKind). A guest raises one with raiseMyCase, which needs the connection …

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Guest | The person the venue serves, signed in or not. In body copy on every surface. | Customer, User, Subject, Contact, Patron | contracts/satellite/marketing-crm.yaml#/components/schemas/GuestProfile |
| Guest profile | The CRM record of one person (details, consent, preferences, history). Distinct from the Account, which is how a guest signs in. | Customer record, Contact, Subject | contracts/satellite/marketing-crm.yaml#getGuestProfile |
| Consent - Given / Withdrawn / Not asked | What the law allows, per purpose (marketing, personalisation, profiling, third-party sharing, AI processing, transactional) and per channel. "Not asked" is not "Withdrawn" and must look different. | Opted in/out as a status, Accepted, Declined, Revoked, Unsubscribed (that is a subscription) | contracts/satellite/marketing-crm.yaml#/components/schemas/ConsentDecision |
| Subscription | A list the guest asked to receive (a newsletter, event news), per channel. Unsubscribing from a list is not withdrawing consent. | Consent, Opt-in | contracts/satellite/marketing-crm.yaml#/components/schemas/MarketingSubscription |
| Preferences | What the guest likes or needs (seating, drinks, dietary, accessibility, contact channel). Never grants permission. | Consents, Settings | contracts/satellite/marketing-crm.yaml#updateGuestPreferences |
| Send me offers and news | The marketing opt-in label beside the terms at checkout, unticked, one per channel and purpose. | I agree to marketing, Pre-ticked boxes, Keep me updated ticked by default | DI-954 |
| Points / Tier / Points to next tier / Expiring points | The loyalty position. Points are a liability earned per programme; tiers are ranked (Bronze, Silver, Gold, Platinum in the meetings). | Credits, Coins, Balance alone (wallet money is "credit"), Level | DI-382 |
| Pending points | Points earned on a purchase still inside its refund window; shown apart from spendable points. | Available points for pending ones | contracts/satellite/marketing-crm.yaml#getLoyaltyPosition |
| Reward | What points can be turned into (rewards catalogue). | Prize (games redemption uses prize), Voucher unless it is one | contracts/satellite/marketing-crm.yaml#listRewards |
| Challenge / Badge / Streak / Referral | Gamification - rewards for behaviour, not spend. Status badges such as Explorer, Adventurer, Legend. | Mission and Quest used interchangeably on one screen, Loyalty tier for a badge | DI-392 |
| Case | One service record - lost property, complaint, question, accessibility, refund request or other - with a number (venue prefix plus sequence), a status and an SLA. | Ticket (a ticket is an admission product), Issue, Incident (that is maintenance and safety) | contracts/satellite/marketing-crm.yaml#/components/schemas/CaseKind |
| Reply to guest / Internal note | The two kinds of case message. The agent always chooses one explicitly; there is no default. | Comment, Message (ambiguous) | F05 step 2 |
| Conversation | A live chat session (web chat, in-app, WhatsApp, SMS, email, kiosk, voice). With the assistant, then queued, then with an agent. It is not a case. | Ticket, Case (until one is raised from it) | contracts/satellite/marketing-crm.yaml#/components/schemas/ConversationState |
| Segment / List / Audience | A segment is rules evaluated when used. A list is static, imported or hand-picked. The audience is what a campaign or journey targets. | Group, Cohort, Target list for a segment | DI-381 |
| Campaign / Journey | A campaign is one send (one-off, scheduled, triggered or recurring) to an audience. A journey is an automation started by an event, with steps, waits and branches. | Flow (booking flows use it), Automation for a one-off send, Blast | R146 |
| Offer | A pre-configured, system-validated discount or benefit that a campaign or journey references. It is never typed into the builder. | Discount field, Coupon (unless the offer is a coupon code) | MoM 2026-08-20 4.6 |
| Reachable | How many guests in an audience can actually be sent to on a channel after consent and suppression. Always shown beside the matching count. | Audience size alone | contracts/satellite/marketing-crm.yaml#previewSegment |
| Possible duplicate / Merge | Two profiles that may be one person. Never called "Duplicate" as a verdict. Merging needs confirmation and stays reversible for 30 days. | Duplicate (as a status), Combine, Auto-merge | DI-808 |
| Data request | A guest's privacy request - a copy of my data, a correction, erasure, a restriction - with a legal clock. Statuses submitted, in progress, completed. | DSAR on guest screens, Subject data, Ticket | DI-379 |
| Waiver / Consent question | A waiver is a signed, versioned form. A consent question ("Are you able to swim?", "I accept the risk") is a single question asked per person or per booking and recorded as consent. | Contract, Disclaimer, Form for a waiver in guest copy | DI-1062 |
| Lost item / Found item / Possible match | The two directions of lost property and the suggested pairing between them. | Lost case, Claim before it is claimed | contracts/satellite/marketing-crm.yaml#/components/schemas/LostItem |
| Wishlist | Products and dates a guest saved to buy later, including F&B and retail to buy on site. | Favourites (used for transport routes), Saved for later on one surface and Wishlist on another | DI-202 |
| Notification / Message | A notification is an item in the guest's in-app feed. A message is one send on a channel (email, SMS, WhatsApp, push, in-app). | Alert for marketing content, Inbox for the guest feed | contracts/satellite/marketing-crm.yaml#/components/schemas/GuestNotification |
| Template | A reusable message body per channel and language with merge fields. Transactional and marketing templates are separate kinds. | Layout, Design | contracts/satellite/marketing-crm.yaml#createMessageTemplate |


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `EMP-051` | Restaurant Service Command Center | C | 3 | 16 | 6 | 1 | 0 | 0 | — | notStarted (generated) |
| `EMP-052` | Floor Plan & Table Map | C | 1 | 3 | 5 | 1 | 6 | 1 | — | notStarted (generated) |
| `EMP-053` | Table & Seating Configuration | C | 21 | 0 | 5 | 1 | 1 | 6 | — | notStarted (generated) |
| `EMP-054` | Reservation Calendar & Timeline | C | 3 | 36 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `EMP-055` | Create / Edit Reservation | C | 33 | 11 | 5 | 0 | 2 | 0 | — | notStarted (generated) |
| `EMP-056` | Walk-In & Waitlist Management | C | 23 | 0 | 5 | 7 | 1 | 0 | — | notStarted (generated) |
| `EMP-057` | Guest Profile & Dining History | D | 13 | 14 | 6 | 8 | 2 | 0 | — | notStarted (generated) |
| `EMP-058` | Live Table & Service Management | A | 51 | 5 | 5 | 10 | 4 | 1 | — | notStarted (generated) |
| `EMP-059` | Table Order, Bill & Payment Management | A | 51 | 5 | 5 | 16 | 2 | 1 | — | notStarted (generated) |
| `EMP-060` | Reservation & Table Performance | C | 3 | 26 | 6 | 1 | 0 | 1 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `EMP-051` Restaurant Service Command Center

**Restaurant Service Command Center — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Floor Service · wave 2 · needs the `fnb` module |
| Block | Block C · task APP-STAFF-EMP-051 |
| Who uses it | venue staff holding `ORDER_MODIFY`, `ORDER_VIEW` (1 operate, 1 read) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listTableReservations` reads the population and `getTableMap` reads one of them — list, select, act |
| Offline | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Opens with | `venueId` (session), `outletId` (EMP-003) · cold entry: **Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to. |
| Route | `/operations/restaurant-service-command-center` |

**What the spec says about it.** **Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Named in the board contents and not written up in it.** **Drawn 31 August** — `FnB Board 4.dc.html` frame `fnb-4a`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Restaurant Service Command Center* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

**From the Food, Beverage & Retail process.** The restaurant host's and floor manager's command centre for one service: how full the room is now, who arrives next, who is waiting, and what is stuck in the kitchen, at a glance on a handheld or tablet. Every tile drills into the screen that acts on it (floor plan, reservations, waitlist, table sheet). The one thing to get right: it compares what is booked with what is actually free, because those differ all evening.

**Known correction pending (do not draw the wrong version)**

- **"Outlet id" text field, a free Date picker, raw data tables "Every table reservation" and "Every F&B order" with id, subjectId, salesOrderId and kitchenTicketId columns, and a "Confirm" primary button with no operation.** Why: Plumbing on a user's screen. A command centre shows counts and the next things to act on. *(source: screens/P06-staff-app.yaml#EMP-051; Food, Beverage & Retail)*
- **The waiting-list tile has no source. There is no operation that lists an outlet's waitlist.** Why: The fnb contract has POST /waitlist and the quote, notify and leave actions, but no GET of the entries, so neither this tile nor EMP-056 can show who is waiting. *(source: contracts/satellite/fnb.yaml#joinRestaurantWaitlist / DI-337; Food, Beverage & Retail)*
- **listFnbOrders is not offline-capable while the screen's offline state says "works from cache".** Why: The kitchen tile must show "as of" when offline rather than imply live data. *(source: contracts/satellite/fnb.yaml#listFnbOrders / screens/P06-staff-app.yaml#EMP-051; Food, Beverage & Retail)*
- **Reading the reservations needs ORDER_MODIFY.** Why: A read gated on a modify permission keeps a view-only manager off the command centre. A view permission would fit. *(source: contracts/satellite/fnb.yaml#listTableReservations; Food, Beverage & Retail)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Outlet id | picker: choose an outlet (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?outletId=` to `listTableReservations`. | `listTableReservations` ?outletId |
| Date | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?date=` to `listTableReservations`. | `listTableReservations` ?date |
| Search restaurant service command center | search field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Outlet | picker: choose an outlet | — | — | `listFnbOrders` ?outletId |
| Table visit | picker: choose a table visit | — | — | `listFnbOrders` ?tableVisitId |
| Status | select | — | Ordered · Accepted · In preparation · Ready · Served · Collected · Delivered · Cancelled · Refunded | `listFnbOrders` ?status |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Outlet and service**: The outlet comes from the person's shift or role. A user who works several outlets gets a picker by outlet name (Oasis Bistro, Terrace Grill), never an "Outlet id" text field. The date defaults to today in the venue's time zone (GST), with no free date picker on the live view. *(source: contracts/satellite/fnb.yaml#listTableReservations / screens/P06-staff-app.yaml#EMP-051)*

#### Outputs: what the screen shows and produces

**Shown**

**Every table reservation** (data table, from `listTableReservations`)

| Shows | Format | Notes |
|---|---|---|
| Guest name | text | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Duration minutes | 1,234 | How long the cover is held. An outlet turning tables twice an evening needs this to be real, or the second sitting cannot be booked. |
| Status | chip: Awaiting deposit, Booked, Confirmed, Seated, Completed, Cancelled… | `awaitingDeposit` only where the venue's dining deposit applies (decided 29 September, rev 3 REV3-8b); a booking with no deposit starts … |

**Every F&B order** (data table, from `listFnbOrders`)

| Shows | Format | Notes |
|---|---|---|
| Order number | text | — |
| Status | chip: Ordered, Accepted, In preparation, Ready, Served, Collected… | The full lifecycle from 4.6.35. Nine states, not six — the earlier enum collapsed `accepted` into `placed` and had no `collected` or … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Estimated ready at | 1 Oct 2026, 14:30 | — |

**Card list** (card list): **Cards rather than a table.** One thumb, arm’s length, and a person who is walking.

**The selected table reservation** (detail panel, from `listTableReservations`)

| Shows | Format | Notes |
|---|---|---|
| Guest name | text | — |
| Contact point | text | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Duration minutes | 1,234 | How long the cover is held. An outlet turning tables twice an evening needs this to be real, or the second sitting cannot be booked. |
| Status | chip: Awaiting deposit, Booked, Confirmed, Seated, Completed, Cancelled… | `awaitingDeposit` only where the venue's dining deposit applies (decided 29 September, rev 3 REV3-8b); a booking with no deposit starts … |

**The table map** (detail panel, from `getTableMap`)

| Shows | Format | Notes |
|---|---|---|
| Outlet | the name it points at, never the id | — |
| Zones | list or chips (count when long) | — |
| Tables | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Room now**: Covers seated against capacity, and tables by status (Vacant, Occupied, Bill requested, Reserved) in the floor-plan colours, from the live table map. *(source: contracts/satellite/fnb.yaml#getTableMap / DI-792 / DI-336)*
- **Next arrivals**: Bookings in the next 60 minutes, ordered by time: name, party size, allergy marker from the booking notes, Confirmed or Booked, and a "Seat" shortcut into the table sheet. Late or no-show bookings are flagged once the grace period passes. *(source: contracts/satellite/fnb.yaml#listTableReservations / contracts/satellite/fnb.yaml#seatTableReservation)*
- **Kitchen**: A count of this outlet's table-service orders by kitchen state (In preparation, Ready and not yet served), with "Ready and not yet served" emphasised because food waiting goes out cold. Counts, not the "Every F&B order" table. *(source: contracts/satellite/fnb.yaml#listFnbOrders / contracts/satellite/fnb.yaml#notifyServer)*

**Data it reads**: `getTableMap` (onLoad, Table map with live state); `listTableReservations` (onLoad, Bookings for a service period); `listFnbOrders` (onLoad, List F&B orders)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The restaurant service list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the restaurant service untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No restaurant service yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on outletId, date and the restaurant service are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `getTableMap` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
outlet: Oasis Bistro · dinner service · Thu 15 Oct 2026
roomNow:
  coversSeated: 38
  capacity: 64
  vacant: 5
  occupied: 9
  billRequested: 2
  reserved: 1
nextArrivals:
- 19:30 Daniel Brooks · 2 · Confirmed
- 20:00 Fatima Al Suwaidi · 6 · Booked · nut allergy
- 20:15 Aisha Rahman · 4 · Confirmed
waiting: 3 parties · longest 22 min
kitchen:
  inPreparation: 7
  readyNotServed: 2
```

#### Permissions

- `getTableMap` → `ORDER_VIEW` (read) · staff
- `listTableReservations` → `ORDER_MODIFY` (operate) · staff
- `listFnbOrders` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `getTableMap` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.1.1 | The system should be able to allow table reservations view for the available tables in real-time, for the guests to choose/request. | F&B & Guest Management | CONTRACTED | `getTableMap` |

#### Client meeting inputs

None names this screen.

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-051` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/FnB Board 4.dc.html`
- Client design-board frames: `FnB Board 4.dc.html#fnb-4a`

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-051?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `ORDER_MODIFY`, `ORDER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-052` Floor Plan & Table Map

**Floor Plan & Table Map — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Floor Service · wave 2 · needs the `fnb` module |
| Block | Block C · task APP-STAFF-EMP-052 |
| Who uses it | venue staff holding `ORDER_VIEW` (1 read) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | statusTracker (comfortable density): `getTableMap` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Opens with | `venueId` (session), `outletId` (session) · cold entry: **Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to. |
| Route | `/operations/floor-plan-table-map` |

**What the spec says about it.** **Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Drawn 31 August** — `FnB Board 4.dc.html` frame `fnb-4b`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Floor Plan &amp; Table Map* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-008): "Save table layout" (setTableLayout, PRODUCT_CONFIGURE) is configuration on the live service map; layout editing is EMP-053, and F80 says configuration does not …

**From the Food, Beverage & Retail process.** The live floor plan a host and the servers work from: a graphical, to-scale picture of each dining hall, with every table drawn in its real shape and seat count, coloured by status, and tagged when the guest is a VIP. Tapping a table opens its table sheet. The one thing to get right: the client's four-status flow and nothing else on the map. No cleaning or "needs clearing" colour.

**Known correction pending (do not draw the wrong version)**

- **TableStatus has needsClearing. closeTableVisit moves the table to needsClearing ("clearing is a separate act by a separate person"), getTableMap describes "needs clearing", and states/table.yaml says needsClearing exists so a paid table is not immediately sellable.** Why: The client decided that the flow is Available, Ordered, Table Closed and Reserved, with no cleaning status, because cleaning is a manual task deliberately left out. Rename it to the client's "Table closed" (or return the table to free on close) and drop the clearing wording, including clearTable's "Mark a table cleared". *(source: DI-336 / TRACKER Workshops/Actions row 89 / contracts/satellite/fnb.yaml#closeTableVisit / contracts/satellite/fnb.yaml#/components/schemas/TableStatus; Food, Beverage & Retail)*
- **TableStatus also has outOfService and seated, which are not in the client's four statuses.** Why: outOfService is a configuration flag (isOutOfService: damaged, or the section is closed), not a service status. Draw it as "Not in use", outside the status colours and filters, and confirm with the client. seated is drawn under Occupied. *(source: DI-336 / DI-792 / contracts/satellite/fnb.yaml#/components/schemas/TableDefinition; Food, Beverage & Retail)*
- **TableDefinition has only position x and y. There is no size, rotation or hall outline (walls, pillars, bar counter), so the plan cannot be drawn to scale.** Why: The client asked for a realistic, to-scale floor plan of the actual halls. *(source: DI-793 / contracts/satellite/fnb.yaml#/components/schemas/TableDefinition; Food, Beverage & Retail)*
- **No customer-category or VIP tag on the table, the visit or the reservation.** Why: The client asked for tables tagged with a customer category so staff prioritise service. Only the kitchen SLA weights carry a VIP signal. *(source: DI-335 / contracts/satellite/fnb.yaml#/components/schemas/TableState; Food, Beverage & Retail)*
- **TableState carries no service stage and no server display name (only serverPrincipalId).** Why: setServiceStage calls itself "the floor plan colour that tells a manager everything", and the map cannot show it without a field. The tile needs the server's name or initials, not an id. *(source: contracts/satellite/fnb.yaml#setServiceStage / contracts/satellite/fnb.yaml#/components/schemas/TableState; Food, Beverage & Retail)*
- **The pattern statusTracker ("reads one record") and an empty state that offers nothing.** Why: The floor plan is a spatial board of many tables. With no tables configured, the empty state points a manager to Table & seating configuration. *(source: screens/P06-staff-app.yaml#EMP-052; Food, Beverage & Retail)*

**Fixed on main** (the package already carries these; draw what it says): "Save table layout" (setTableLayout, PRODUCT_CONFIGURE) with a modal collecting tables, plus the leftover search field, card list and … (CHG-WIR-008).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Does "Table closed" persist after payment until someone resets the table (which acts like the cleaning status DI-336 excluded), or does a paid table go straight back to Vacant?** → Drawn default stands (answer: "A short 'Table closed' state, then 'Make available'"): Draw "Table closed" as a short-lived state with a one-tap "Make available" on the tile. Avoid "clean", "clear" and "reset" wording. *(decided by Chinmay, 2026-10-02; DEC-201 / CHG-NOTE-004)*
- **When does a table show Reserved, given the host normally allocates the table at seating (DI-689)? Options: only when the booking names a table, or from N minutes before a pre-allocated booking.** → A table shows Reserved when the booking names it, or N minutes (venue-set) before a pre-allocated booking. *(decided by Chinmay, 2026-10-02; DEC-202 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search floor plan | search field | — | — | — | — | — | — |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Hall**: Tabs per dining area (Main Hall, Terrace, Majlis), from the table zones, in the outlet's order. Swipe between halls on a handheld. *(source: DI-793 / DI-335 / contracts/satellite/fnb.yaml#/components/schemas/TableMap)*
- **Status filter**: Chips Vacant, Occupied, Bill requested and Reserved, combinable. Filtering dims the other tables rather than removing them, so the room keeps its shape. *(source: DI-792 / screens/P04-point-of-sale.yaml#POS-028)*
- **My tables**: A toggle that dims every table not assigned to the signed-in server. On by default for the server role, off for the host. *(source: contracts/satellite/fnb.yaml#/components/schemas/TableState / DI-227)*

#### Outputs: what the screen shows and produces

**Shown**

**The table map** (detail panel, from `getTableMap`): **Table states** (DI-336; CHG-CSA-012): Available, Ordered, Table closed (a short state after payment, ended by Make available; DEC-201, default) and Reserved, shown when a booking names the table or from N minutes (the venue's lead time) before a pre-allocated booking (decided 2 October 2026, Chinmay, batch 6; DEC-202).

| Shows | Format | Notes |
|---|---|---|
| Outlet | the name it points at, never the id | — |
| Zones | list or chips (count when long) | — |
| Tables | list or chips (count when long) | — |

**Card list** (card list): **Cards rather than a table.** One thumb, arm’s length, and a person who is walking.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Table shape**: Drawn from the table's shape (round, square, rectangle, booth, bar) and position, to scale, with one chair mark per seat, so a 2-seat and a 4-seat table are visibly different. The table code (T12) is unique in the venue and always readable. *(source: DI-104 / DI-793 / R108 / contracts/satellite/fnb.yaml#/components/schemas/TableDefinition)*
- **Status colour**: Vacant, Occupied (seated or ordered), Bill requested and Reserved, plus Table closed (paid) per the client's flow. The colour is always paired with a label or icon, never colour alone. A table out of service is hatched grey with "Not in use", outside the status colours. *(source: DI-336 / DI-792 / contracts/satellite/fnb.yaml#/components/schemas/TableStatus)*
- **Table detail on the tile**: Covers against seats ("3/4"), minutes since seated, the server's initials, and on Bill requested the bill total in AED with 2 decimals. The VIP tag shows as a small badge. *(source: contracts/satellite/fnb.yaml#/components/schemas/TableState / DI-335)*
- **Combined tables**: Tables seated together for one party (a combination or a merged visit) are drawn with one outline around them and one status. *(source: contracts/satellite/fnb.yaml#setTableCombinations / contracts/satellite/fnb.yaml#mergeTableVisits)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Tap a table**: Opens the table sheet (EMP-058). On a vacant table the sheet opens on "Seat" with the covers stepper (cashier picks the table, then enters covers). On an occupied table it opens on the visit. *(source: DI-104 / F29 step 1)*

**Data it reads**: `getTableMap` (onLoad, Table map with live state)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The floor plan table, read by `getTableMap`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the floor plan table untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No floor plan table yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `getTableMap` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |

#### Edge cases to draw

- **Offline on the terrace**: The map stays usable from the cache with an "Offline, as of 20:31" strip. Seating and orders queue, and statuses changed by others are not seen until sync. *(source: contracts/satellite/fnb.yaml#getTableMap / DI-071 / DI-072)*
- **A booking with no table assigned**: A table shows Reserved when the booking names it, or from N minutes (the venue's setting) before a pre-allocated booking. Otherwise the next arrivals show in a side strip ("Next: 20:00 Al Suwaidi · 6"). *(source: contracts/satellite/fnb.yaml#createTableReservation / DI-689 / decided 2 October 2026 by Chinmay (CHG-NOTE-004))*

#### Consistency with other screens

- Match `POS-028`: Same halls, same table glyphs, same status names, colours and filter chips (the v2 till has Main Hall, Terrace and Majlis rooms with vacant, occupied, bill requested and reserved). The two must read as one floor plan.
- Match `EMP-053`: Draws exactly what the configuration saved, the same shapes and positions.
- Match `EMP-058`: The tap target. Move and merge stay there (off POS-028 until after r2).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
halls:
- Main Hall
- Terrace
- Majlis
tables:
- code: T1
  shape: square
  seats: 2
  status: Vacant
- code: T4
  shape: rectangle
  seats: 4
  status: Occupied
  covers: 3
  seatedMin: 42
  server: PN
- code: T7
  shape: square
  seats: 4
  status: Bill requested
  covers: 4
  bill: AED 620.24
  server: KM
- code: T9
  shape: round
  seats: 6
  status: Reserved
  booking: 20:00 Al Suwaidi · 6
- code: M2
  shape: booth
  seats: 8
  status: Occupied
  covers: 7
  vip: true
  hall: Majlis
- code: T15
  shape: square
  seats: 2
  state: Not in use (damaged leg)
```

#### Permissions

- `getTableMap` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `getTableMap` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.1.1 | The system should be able to allow table reservations view for the available tables in real-time, for the guests to choose/request. | F&B & Guest Management | CONTRACTED | `getTableMap` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Allam: a realistic, to-scale visual floor plan reflecting the actual hall layout and table shapes (square, rectangular) across multiple dining areas/halls, instead of a generic list. *(client request · MoM 9 Sep 2026, 4.15 POS Prototype Review - Food & Beverage, Tables & Kitchen Display · DI-793)*
- Tables are colour-coded by status (vacant, occupied, reserved) and filterable by status. *(client request · MoM 9 Sep 2026, 4.15 POS Prototype Review - Food & Beverage, Tables & Kitchen Display · DI-792)*
- Qossai asked if guests pick a specific table; Allam: table choice can be an option, but the default is the guest gives party size and the system/host allocates a table. *(agreed · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Dining) · DI-689)*
- Decision: table status flow is Available → Ordered → Table Closed (after payment) → Reserved (booked in advance). No "Cleaning" status — cleaning is a manual staff task, deliberately excluded to avoid complexity. *(agreed · MoM 18 Aug 2026, 4.8 Table Management (Fine Dining); 5. Key Decisions · DI-336)*
- A visual floor/table map (main hall, terrace, VIP lounge, etc.) shows table status, and tables can be tagged with a customer category (e.g. VIP) so staff prioritise service. *(client request · MoM 18 Aug 2026, 4.8 Table Management (Fine Dining) · DI-335)*
- Allam: replace the dated table layout with a modern, graphical table map where two-seat and four-seat tables look visually distinct; the cashier selects a table then enters the number of covers. *(agreed · MoM 3 Aug 2026, 5. Table Management & Dining Service Models · DI-104)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A85** Design the table management module for fine dining: visual floor/table map with VIP tagging, table status flow (Available → Ordered → Table Closed → Reserved), reservations with deposit and waitlist, a per-table … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'table management')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-052` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/FnB Board 4.dc.html`
- Client design-board frames: `FnB Board 4.dc.html#fnb-4b`

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (3 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-052?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 6 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 6 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-053` Table & Seating Configuration

**Table & Seating Configuration — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Floor Service · wave 2 · needs the `fnb` module |
| Block | Block C · task APP-STAFF-EMP-053 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | configEditor (comfortable density): the screen declares only writes (`setTableLayout`) and no read of a population — it is settings, not a list |
| Offline | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Opens with | `venueId` (session), `outletId` (session) · cold entry: **Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to. |
| Route | `/operations/table-seating-configuration` |

**What the spec says about it.** **Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Named in the board contents and not written up in it.** **Drawn 31 August** — `FnB Board 4.dc.html` frame `fnb-4c`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Table &amp; Seating Configuration* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-008): Three ways to write the same table (setTableLayout for the whole outlet, createTable and updateTable for one) mean two conflict behaviours on one screen; the … Removed 2 October 2026 (CHG-WIR-008): Three ways to write the same table (setTableLayout for the whole outlet, createTable and updateTable for one) mean two conflict behaviours on one screen; the …

**From the Food, Beverage & Retail process.** Where a restaurant manager lays out the room: tables drawn on each hall in their real shape, seats and position, grouped into sections with a server each, with the pairs of tables that can be pushed together. It is configuration done before service, not during it. The one thing to get right: a drag-and-drop floor-plan editor whose output is the same picture the live map (EMP-052) and the till (POS-028) draw, not a form of x and y numbers.

**Known correction pending (do not draw the wrong version)**

- **Text fields labelled "id", "label", "capacity", "zone", "position" and "shape", bound to raw schema fields.** Why: Plumbing on a user's screen. The id is generated, position and shape are set on the canvas, and the labels must be Table code, Seats and Hall. *(source: screens/P06-staff-app.yaml#EMP-053; Food, Beverage & Retail)*
- **The board frame fnb-4c is claimed by both EMP-053 and EMP-060.** Why: A frame drawn once cannot be the design of two screens. One of the two mappings is wrong. *(source: screens/P06-staff-app.yaml#EMP-053 / screens/P06-staff-app.yaml#EMP-060; Food, Beverage & Retail)*
- **TableDefinition lacks table size and rotation, and the hall has no outline, so the editor cannot place tables to scale.** Why: DI-793 asks for a to-scale plan of the actual hall layout. *(source: DI-793 / contracts/satellite/fnb.yaml#/components/schemas/TableDefinition; Food, Beverage & Retail)*

**Fixed on main** (the package already carries these; draw what it says): Three ways to write the same table: setTableLayout (the whole outlet, matching on id) and createTable or updateTable (one table). (CHG-WIR-008); setTableCombinations (PRODUCT_CONFIGURE) sits on the live service screen EMP-058 and not here, even though it is configuration. (CHG-WIR-008).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is the floor-plan editor meant for a phone at all, or a tablet or back office only?** → Drawn default stands (answer: "Tablet (landscape) + back office; read-only on a phone"): Draw it for a tablet in landscape. On a phone, show the plan read-only with an "Edit on a tablet or in Back Office" note. *(decided by Chinmay, 2026-10-02; DEC-203 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| id | picker: choose an id (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | — | `TableDefinition.id` |
| label | text field | optional | — | max length 32 | — | The table code, unique per venue (decided 28 September, audit R108). Two tables in one venue never share a label, across all its outlets, so *T12* names one table wherever it is read. | `TableDefinition.label` |
| capacity | number field | optional | — | min 1 | — | — | `TableDefinition.capacity` |
| zone | text field | optional | — | — | — | — | `TableDefinition.zone` |
| position | group | optional | — | — | — | — | `TableDefinition.position` |
| shape | radio group | optional | — | Round · Square · Rectangle · Booth · Bar | — | — | `TableDefinition.shape` |
| Search table | search field | — | — | — | — | — | — |

**Form: Save table combinations** (modal, opened by *Save table combinations*; *Save table combinations* calls `setTableCombinations`, *Cancel* sends nothing)

**Collects what `setTableCombinations` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Combinations `combinations` | repeatable rows | required | — | — | — | — | `setTableCombinations` body |
| Tables `combinations[].tableIds` | multi-picker: choose tables | required | — | at least 2 | — | — | `setTableCombinations` body |
| Combined covers `combinations[].combinedCovers` | number field | required | — | min 1 | — | — | `setTableCombinations` body |
| Setup minutes `combinations[].setupMinutes` | number field (minutes) | optional | 5 | — | — | — | `setTableCombinations` body |

Errors to draw in the form: 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

**Sent by *Save table layout*** (`setTableLayout`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Tables `tables` | repeatable rows | required | — | — | — | — | `setTableLayout` body |
| ID `tables[].id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setTableLayout` body |
| Label `tables[].label` | text field | required | — | max length 32 | — | The table code, unique per venue (decided 28 September, audit R108). Two tables in one venue never share a label, across all its outlets, so *T12* names one table wherever it is … | `setTableLayout` body |
| Capacity `tables[].capacity` | number field | required | — | min 1 | — | — | `setTableLayout` body |
| Zone `tables[].zone` | text field | optional | — | — | — | — | `setTableLayout` body |
| Position `tables[].position` | group | optional | — | — | — | — | `setTableLayout` body |
| X `tables[].position.x` | number field | optional | — | — | — | — | `setTableLayout` body |
| Y `tables[].position.y` | number field | optional | — | — | — | — | `setTableLayout` body |
| Shape `tables[].shape` | radio group | optional | — | Round · Square · Rectangle · Booth · Bar | — | — | `setTableLayout` body |
| Is out of service `tables[].isOutOfService` | toggle | optional | off | `getTableMap` shows it as `outOfService` and a claim on it is refused with `tableOutOfService`. | — | Damaged, or its section closed. `getTableMap` shows it as `outOfService` and a claim on it is refused with `tableOutOfService`. | `setTableLayout` body |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Table code**: Short code such as T12, up to 32 characters, unique across the whole venue (all outlets). A duplicate is refused at once with "T12 is already used in Lagoon Bar". *(source: R108 / contracts/satellite/fnb.yaml#createTable)*
- **Seats**: Whole number of at least 1, set with a stepper. The glyph redraws with that many chairs. A change is refused while a party is seated at the table, with "Table T12 has an open table now. Change it after they leave." *(source: contracts/satellite/fnb.yaml#updateTable / contracts/satellite/fnb.yaml#setTableLayout / DI-104)*
- **Shape**: Picked visually, not typed, from Round, Square, Rectangle, Booth and Bar seat. *(source: contracts/satellite/fnb.yaml#/components/schemas/TableDefinition / DI-793)*
- **Hall**: The dining area the table sits in (Main Hall, Terrace, Majlis). Drag the table between hall tabs or pick the hall. *(source: contracts/satellite/fnb.yaml#/components/schemas/TableDefinition / DI-793)*
- **Position**: Set by dragging on the canvas with a snap grid. Never typed coordinates. *(source: DI-793 / contracts/satellite/fnb.yaml#/components/schemas/TableDefinition)*
- **Out of service**: Toggle "Not in use (damaged or section closed)". The table stays on the plan, greyed, and cannot be seated. *(source: contracts/satellite/fnb.yaml#/components/schemas/TableDefinition)*
- **Sections**: Lasso tables into a named section and assign a server, per service period (lunch with three sections, Friday dinner with five). Every table belongs to at most one section in a period. *(source: contracts/satellite/fnb.yaml#setSectionLayout / F94 step 1)*
- **Combinations**: Pick two or more tables and give the covers they seat together and the set-up minutes (default 5). Declared by the manager, not inferred from adjacency, because a pillar or a step can stop two neighbours combining. *(source: contracts/satellite/fnb.yaml#setTableCombinations / F29 step 2)*

#### Outputs: what the screen shows and produces

**Shown**

**Card list** (card list): **Cards rather than a table.** One thumb, arm’s length, and a person who is walking.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (primary button) | navigation or local | — | — | — | — |
| Save table layout (primary button) | `setTableLayout` PUT `/outlets/{outletId}/tables` | inline | TableMap | 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | — |
| Save table combinations (secondary button) | `setTableCombinations` PUT `/outlets/{outletId}/table-combinations` | inline | inline | 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | opens modal first |

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Save layout**: Saves the whole outlet in one write. If someone else saved meanwhile (412), say "The layout changed on another device. Reload to see it before saving." and keep the edits on screen. Online only; offline the editor is read-only. *(source: contracts/satellite/fnb.yaml#setTableLayout / F94 step 1)*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The saved table seating. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the table seating untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No table seating configured. The form opens empty and `setTableLayout` saves the first one; it says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_CONFIGURE`, which `setTableLayout` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |

#### Consistency with other screens

- Match `BO-729`: The back-office Create / Edit Outlet edits the same tables and sections. One editor component, one vocabulary.
- Match `POS-024`: The till's Outlet Setup writes the same layout and combinations.
- Match `EMP-052`: Renders exactly what is saved here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
outlet: Oasis Bistro
halls:
- Main Hall
- Terrace
- Majlis
tables:
- code: T6
  seats: 4
  shape: Square
  hall: Main Hall
- code: T7
  seats: 4
  shape: Square
  hall: Main Hall
- code: T9
  seats: 6
  shape: Round
  hall: Main Hall
- code: M2
  seats: 8
  shape: Booth
  hall: Majlis
- code: TR3
  seats: 2
  shape: Square
  hall: Terrace
  outOfService: true
sections:
- Dinner · Section A (T1 to T6) · Priya Nair
- Dinner · Section B (T7 to T12) · Khalid Al Mansoori
combinations:
- T6 + T7 seat 9 · 5 min set-up
```

#### Permissions

- `setTableLayout` → `PRODUCT_CONFIGURE` (configure) · staff
- `setSectionLayout` → `PRODUCT_CONFIGURE` (configure) · staff
- `setTableCombinations` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_CONFIGURE`, which `setTableLayout` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.9.6 | The system should be able to create, modify, delete a restaurant floor plan. | Bundles and Promotions | CONTRACTED | `setTableLayout` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Allam: a realistic, to-scale visual floor plan reflecting the actual hall layout and table shapes (square, rectangular) across multiple dining areas/halls, instead of a generic list. *(client request · MoM 9 Sep 2026, 4.15 POS Prototype Review - Food & Beverage, Tables & Kitchen Display · DI-793)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **C18** Locate and share the AutoCAD/PDF seating drawing from the Bahrain project (also to be shared with 3D vendor "3DDV") *(Allam · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'seating')*
- **A85** Design the table management module for fine dining: visual floor/table map with VIP tagging, table status flow (Available → Ordered → Table Closed → Reserved), reservations with deposit and waitlist, a per-table … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'table management')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **A102** Build a single unified seat map builder screen (section type as a section-level attribute — seated / zone / standing / suite — mixed types in one map, suites sold bulk or by seat) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'seat map')*
- **A104** Make best-seat ranking configurable per map/event and implement section-wise holds rather than freeform polygon selection *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'best-seat')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-053` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/FnB Board 4.dc.html`
- Client design-board frames: `FnB Board 4.dc.html#fnb-4c`

#### Acceptance for the design

- [ ] Every input above is drawn (21), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-053?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Save table layout, Save table combinations.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-054` Reservation Calendar & Timeline

**Reservation Calendar & Timeline — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Floor Service · wave 2 · needs the `fnb` module |
| Block | Block C · task APP-STAFF-EMP-054 |
| Who uses it | venue staff holding `ORDER_MODIFY`, `ORDER_VIEW` (1 operate, 1 read) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listTableReservations` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Opens with | `venueId` (session) · cold entry: **Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to. |
| Route | `/operations/reservation-calendar-timeline` |

**What the spec says about it.** **Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Drawn 31 August** — `FnB Board 4.dc.html` frame `fnb-4d`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Reservation Calendar &amp; Timeline* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

**From the Food, Beverage & Retail process.** The host's book for the restaurant: who is coming, when, how many, and for how long, as a day timeline on a tablet and an agenda list on a phone, with week and month views for looking ahead. The one thing to get right: bookings are mostly not on a table until the party is seated, so the timeline shows covers over time and unassigned bookings, not a grid of tables that looks falsely full or empty.

**Known correction pending (do not draw the wrong version)**

- **listTableReservations takes a single date. Week and month views would need one call per day, and there is no status filter.** Why: DI-919 requires day, week, month and agenda views for every calendar. The read needs a date range. *(source: DI-919 / contracts/satellite/fnb.yaml#listTableReservations; Food, Beverage & Retail)*
- **"Outlet id" text field, a free date picker, and the raw "Every table reservation" data table with id, outletId, subjectId and groupId columns.** Why: Plumbing on a user's screen. The calendar view replaces the table. *(source: screens/P06-staff-app.yaml#EMP-054; Food, Beverage & Retail)*
- **The host cannot cancel, move or change a booking from the calendar.** Why: updateTableReservation is guest-only and self-scoped (guestAuth). There is no staff operation to change or cancel a booking taken by phone. *(source: contracts/satellite/fnb.yaml#updateTableReservation / MATRIX 4.9.10; Food, Beverage & Retail)*

**Fixed on main** (the package already carries these; draw what it says): The double-booking read (resolveBookingConflict, "Board 4D") is consumed by no screen, though this screen is the client's frame fnb-4d. (CHG-WIR-008).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Outlet id | picker: choose an outlet (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?outletId=` to `listTableReservations`. | `listTableReservations` ?outletId |
| Date | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?date=` to `listTableReservations`. | `listTableReservations` ?date |
| Search reservation calendar | search field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Date | date picker | — | — | `resolveBookingConflict` ?date |
| Outlet | picker: choose an outlet | — | — | `resolveBookingConflict` ?outletId |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **View and date**: Day (default today), week, month and agenda. The day view runs in hours from the venue's day start hour, in GST. A phone opens on the agenda. *(source: DI-919 / contracts/satellite/fnb.yaml#listTableReservations)*
- **Outlet**: From the shift. A picker by name only for users with several outlets. *(source: contracts/satellite/fnb.yaml#listTableReservations)*
- **Status filter**: Chips for Booked, Confirmed, Awaiting deposit (only where the venue's deposit is on), Seated, No-show and Cancelled. Cancelled is off by default. *(source: contracts/satellite/fnb.yaml#/components/schemas/TableReservationStatus / DI-1049)*

#### Outputs: what the screen shows and produces

**Shown**

**Calendar** (calendar view, from `listTableReservations`): Reservations by hour; agenda view on the handheld. Day, week, month and agenda views; the day starts at the venue's `calendarDayStartHour`. Filters the category on what it read.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Outlet | the name it points at, never the id | — |
| Subject | the name it points at, never the id | — |
| Guest name | text | — |
| Contact point | text | — |
| Party size | 1,234 | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Duration minutes | 1,234 | How long the cover is held. An outlet turning tables twice an evening needs this to be real, or the second sitting cannot be booked. |
| Tables | list or chips (count when long) | The dining tables assigned to this reservation, one row each. Usually empty until seating. |
| Reservation | the name it points at, never the id | — |
| Table | the name it points at, never the id | — |
| Status | chip: Awaiting deposit, Booked, Confirmed, Seated, Completed, Cancelled… | `awaitingDeposit` only where the venue's dining deposit applies (decided 29 September, rev 3 REV3-8b); a booking with no deposit starts … |
| Group | the name it points at, never the id | 5.1.2. Several bookings managed as one party across adjacent tables. |
| Notes | text | Allergies, accessibility needs and other requests, as the guest wrote them. |
| Seating preference | text | The seating area the guest asked for, e.g. indoor, terrace, majlis (Chinmay, 2 October, workbook Q204; DI-791; CHG-CSA-018). |
| Occasion | chip: Birthday, Anniversary, Business, Celebration, Other | The occasion the guest named (workbook Q204, DI-337; CHG-CSA-018). Shown to the host and the server; never a price. |
| Taken by principal | the name it points at, never the id | The staff member who took the booking (`createTableReservationForGuest`); null for a guest's own booking (CHG-CSA-045). |
| Actual party size | 1,234 | — |
| Table visit | the name it points at, never the id | — |

**Every table reservation** (data table, from `listTableReservations`)

| Shows | Format | Notes |
|---|---|---|
| Guest name | text | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Duration minutes | 1,234 | How long the cover is held. An outlet turning tables twice an evening needs this to be real, or the second sitting cannot be booked. |
| Status | chip: Awaiting deposit, Booked, Confirmed, Seated, Completed, Cancelled… | `awaitingDeposit` only where the venue's dining deposit applies (decided 29 September, rev 3 REV3-8b); a booking with no deposit starts … |

**Card list** (card list): **Cards rather than a table.** One thumb, arm’s length, and a person who is walking.

**Conflicts** (data table, from `resolveBookingConflict`)

| Shows | Format | Notes |
|---|---|---|
| Table | the name it points at, never the id | — |
| Reservations | list or chips (count when long) | — |
| Overlap minutes | 1,234 | — |
| Options | list or chips (count when long) | — |
| Kind | chip: Alternative table, Earlier slot, Later slot, Combine tables, Contact guest | — |
| Detail | text | — |
| Disruption score | 1,234 | Lower is easier to move. A party of two at 6pm has options; a party of twelve at 8pm on a Saturday does not. |

**The selected table reservation** (detail panel, from `listTableReservations`)

| Shows | Format | Notes |
|---|---|---|
| Guest name | text | — |
| Contact point | text | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Duration minutes | 1,234 | How long the cover is held. An outlet turning tables twice an evening needs this to be real, or the second sitting cannot be booked. |
| Status | chip: Awaiting deposit, Booked, Confirmed, Seated, Completed, Cancelled… | `awaitingDeposit` only where the venue's dining deposit applies (decided 29 September, rev 3 REV3-8b); a booking with no deposit starts … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Booking bar or row**: Time, then name, party size (with the actual party size once seated, "6 → 4"), duration as bar length, status chip, an allergy icon when the notes carry one, and a link icon when the booking is one of a group across tables. Contact number on tap only. *(source: contracts/satellite/fnb.yaml#/components/schemas/TableReservation / F29 step 1)*
- **Covers per slot**: A small histogram of booked covers per 15-minute slot against the outlet's seats, so the host sees where the evening is tight. *(source: contracts/satellite/fnb.yaml#listTableReservations / contracts/satellite/fnb.yaml#getFnbReservationPolicy)*
- **No-show**: Set by the system after the grace period, not by the host. Shown as "No-show" with a "Seat anyway" action if they turn up late. *(source: contracts/satellite/fnb.yaml#seatTableReservation / contracts/satellite/fnb.yaml#/components/schemas/TableReservationStatus)*

**Data it reads**: `listTableReservations` (onLoad, Bookings for a service period); `resolveBookingConflict` (onLoad, Double bookings to resolve)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reservation calendar timeline list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reservation calendar timeline untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reservation calendar timeline yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on outletId, date and the reservation calendar timeline are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_MODIFY`, which `listTableReservations` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |

#### Edge cases to draw

- **Two bookings on one table for the same hour**: Flag the clash on both bookings with the options ranked by which party is easier to move (another table, earlier or later, combine, call the guest). The system never resolves it silently. *(source: contracts/satellite/fnb.yaml#resolveBookingConflict)*

#### Consistency with other screens

- Match `EMP-055`: Tapping a slot opens New reservation prefilled with that time. Tapping a booking opens it for change.
- Match `EMP-058`: Seat on a booking opens the table sheet's seat step with the booking attached.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
date: Thu 15 Oct 2026 · Oasis Bistro
bookings:
- time: '19:30'
  name: Daniel Brooks
  party: 2
  mins: 90
  status: Confirmed
- time: '20:00'
  name: Fatima Al Suwaidi
  party: 6
  mins: 120
  status: Booked
  notes: Nut allergy (1 guest) · anniversary
- time: '20:15'
  name: Aisha Rahman
  party: 4
  mins: 90
  status: Confirmed
- time: '21:00'
  name: Khalid Al Mansoori
  party: 9
  mins: 150
  status: Booked
  tables: T6 + T7
- time: '18:00'
  name: Omar Ziad
  party: 3
  status: No-show
```

#### Permissions

- `listTableReservations` → `ORDER_MODIFY` (operate) · staff
- `resolveBookingConflict` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `ORDER_MODIFY`, which `listTableReservations` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Every calendar has day, week and month (and agenda) views, and the day view is broken into hours from the venue's day start hour (calendarDayStartHour). *(agreed · MoM 17 Sep 2026, M17-03 · DI-919)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-054` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/FnB Board 4.dc.html`
- Client design-board frames: `FnB Board 4.dc.html#fnb-4d`

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state.
- [ ] Every output is drawn (36 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-054?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `ORDER_MODIFY`, `ORDER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-055` Create / Edit Reservation

**Create / Edit Reservation — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Floor Service · wave 2 · needs the `fnb` module |
| Block | Block C · task APP-STAFF-EMP-055 |
| Who uses it | venue staff holding `GUEST_VIEW`, `ORDER_CREATE`, `ORDER_MODIFY`, `PRODUCT_VIEW` (2 read, 2 operate) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | configEditor (comfortable density): the screen declares only writes (`createTableReservation`) and no read of a population — it is settings, not a list |
| Offline | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Opens with | `venueId` (session), `reservationId` (navigation), `outletId` (navigation) · cold entry: **Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to. |
| Route | `/operations/create-edit-reservation` |

**What the spec says about it.** **Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Named in the board contents and not written up in it.** **Drawn 31 August** — `FnB Board 4.dc.html` frame `fnb-4e`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Create / Edit Reservation* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-008): createTableReservation is a guest operation (guestAuth, self-scoped, no permission); a host booking for a caller is not the caller, so it comes off the staff app … Contract gap recorded 2 October 2026 (CHG-WIR-011): No staff-audience create, amend or cancel of a table reservation. 2 October 2026 (CHG-SPO-010): the staff create now exists (`createTableReservationForGuest`, CHG-CSA-045), so a host books from here; amending or cancelling a booking from staff still has no …

**From the Food, Beverage & Retail process.** A host takes a booking, usually on the phone or at the podium: date and time, party size, guest name and contact, allergies and requests, and only optionally a table. While the name and number are typed, possible existing guests are proposed, so the restaurant does not create a second record for the same person. The one thing to get right: no table is committed by default and no deposit is asked for unless the venue has switched it on.

**Known correction pending (do not draw the wrong version)**

- **"Edit" has no operation: updateTableReservation is guest-only.** Why: The screen is Create / Edit, and the matrix asks for amendment and cancellation. *(source: contracts/satellite/fnb.yaml#updateTableReservation / MATRIX 4.9.10 / MATRIX 13.3.11; Food, Beverage & Retail)*
- **The form exposes id, outletId, subjectId, status, groupId, tableVisitId and actualPartySize as text fields, and the duplicate-match component is listed three times.** Why: Read-only and system fields on a user's form. One duplicate-match panel under the guest fields. *(source: screens/P06-staff-app.yaml#EMP-055; Food, Beverage & Retail)*
- **The deposit note says the deposit is adjusted against the final bill, and the Bill has no line for a deposit applied.** Why: DI-337 asks for the deposit to be adjusted against the final bill. See EMP-059. *(source: DI-337 / contracts/satellite/fnb.yaml#/components/schemas/Bill; Food, Beverage & Retail)*

**Fixed on main** (the package already carries these; draw what it says): createTableReservation is a guest operation (guestAuth, self-scoped to the subject, no permission). It is listed as unpermissioned on the … (CHG-WIR-008); Neither sendBookingConfirmation ("Board 4E") nor getFnbReservationPolicy (the default duration) is wired to this screen, though this screen … (CHG-WIR-008).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should a booking capture seating-area preference (indoor, terrace, majlis) and the occasion? The waitlist has seatingPreference and the reservation does not.** → Seating preference and occasion are fields on a table booking. *(decided by Chinmay, 2026-10-02; DEC-204 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| guestName | text field | optional | — | — | — | — | `TableReservation.guestName` |
| contactPoint | text field | optional | — | — | — | — | `TableReservation.contactPoint` |
| partySize | number field | optional | — | min 1 | — | — | `TableReservation.partySize` |
| startsAt | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `TableReservation.startsAt` |
| durationMinutes | number field (minutes) | optional | — | An outlet turning tables twice an evening needs this to be real, or the second sitting cannot be booked. | — | How long the cover is held. An outlet turning tables twice an evening needs this to be real, or the second sitting cannot be booked. | `TableReservation.durationMinutes` |
| tableIds | picker: choose a table (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | — | `TableReservation.tables[].tableId` |
| notes | text area | optional | — | — | — | Allergies, accessibility needs and other requests, as the guest wrote them. | `TableReservation.notes` |
| Search create / edit reservation | search field | — | — | — | — | — | — |
| Seating preference | text field | optional | — | max length 64 | — | Indoor, terrace, majlis: a preference, not a table (decided 2 October 2026, Chinmay, batch 6; DEC-204; CHG-CSA-018). | `TableReservation.seatingPreference` |
| Occasion | radio group | optional | — | Birthday · Anniversary · Business · Celebration · Other | — | Birthday, anniversary, business and so on; shown to the host and the server (DEC-204). | `TableReservation.occasion` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Outlet | picker: choose an outlet | — | — | `getFnbReservationPolicy` ?outletId |

**Form: Find matches for guest** (modal, opened by *Find matches for guest*; *Find matches for guest* calls `matchGuest`, *Cancel* sends nothing)

**Collects what `matchGuest` sends before it is called.** Nothing in the body is required. Optional: `name`, `phone`, `email`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | — | — | — | `matchGuest` body |
| Phone `phone` | phone field | optional | — | — | +971 5X XXX XXXX (E.164) | — | `matchGuest` body |
| Email `email` | text field | optional | — | — | — | — | `matchGuest` body |

**Sent by *Send confirmation*** (`sendBookingConfirmation`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Channel `channel` | segmented control | optional | — | Email · SMS · Whatsapp | — | — | `sendBookingConfirmation` body |
| Kind `kind` | radio group | optional | Confirmation | Confirmation · Reminder · Reconfirmation request · Cancellation | — | — | `sendBookingConfirmation` body |
| Requires reconfirmation `requiresReconfirmation` | toggle | optional | off | — | — | — | `sendBookingConfirmation` body |
| Release if unconfirmed hours `releaseIfUnconfirmedHours` | number field (hours) | optional | — | — | — | — | `sendBookingConfirmation` body |

**Sent by *Save booking*** (`createTableReservationForGuest`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Outlet `outletId` | picker: choose an outlet | required | — | — | shows names, sends the id | — | `createTableReservationForGuest` body |
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | — | `createTableReservationForGuest` body |
| Guest name `guestName` | text field | optional | — | — | — | — | `createTableReservationForGuest` body |
| Contact point `contactPoint` | text field | optional | — | — | — | — | `createTableReservationForGuest` body |
| Party size `partySize` | number field | required | — | min 1 | — | — | `createTableReservationForGuest` body |
| Starts at `startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createTableReservationForGuest` body |
| Duration minutes `durationMinutes` | number field (minutes) | optional | — | An outlet turning tables twice an evening needs this to be real, or the second sitting cannot be booked. | — | How long the cover is held. An outlet turning tables twice an evening needs this to be real, or the second sitting cannot be booked. | `createTableReservationForGuest` body |
| Tables `tables` | repeatable rows | optional | — | — | — | The dining tables assigned to this reservation, one row each. Usually empty until seating. | `createTableReservationForGuest` body |
| Reservation `tables[].reservationId` | picker: choose a reservation | required | — | — | shows names, sends the id | — | `createTableReservationForGuest` body |
| Table `tables[].tableId` | picker: choose a table | required | — | — | shows names, sends the id | — | `createTableReservationForGuest` body |
| Created at `tables[].createdAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createTableReservationForGuest` body |
| Status `status` | select | optional | — | Awaiting deposit · Booked · Confirmed · Seated · Completed · Cancelled · No show; `awaitingDeposit` only where the venue's dining deposit applies (decided 29 September, rev 3 REV3-8b); a booking with no deposit starts `booked`. | — | `awaitingDeposit` only where the venue's dining deposit applies (decided 29 September, rev 3 REV3-8b); a booking with no deposit starts `booked`. | `createTableReservationForGuest` body |
| Group `groupId` | picker: choose a group | optional | — | — | shows names, sends the id | 5.1.2. Several bookings managed as one party across adjacent tables. | `createTableReservationForGuest` body |
| Notes `notes` | text area | optional | — | — | — | Allergies, accessibility needs and other requests, as the guest wrote them. | `createTableReservationForGuest` body |
| Seating preference `seatingPreference` | text field | optional | — | max length 64 | — | The seating area the guest asked for, e.g. indoor, terrace, majlis (Chinmay, 2 October, workbook Q204; DI-791; CHG-CSA-018). | `createTableReservationForGuest` body |
| Occasion `occasion` | radio group | optional | — | Birthday · Anniversary · Business · Celebration · Other | — | The occasion the guest named (workbook Q204, DI-337; CHG-CSA-018). Shown to the host and the server; never a price. | `createTableReservationForGuest` body |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Date and time**: In the venue's time zone (GST), in slots of the outlet's interval. A time outside opening hours is refused with the hours shown. *(source: contracts/satellite/fnb.yaml#createTableReservation / DI-919)*
- **Party size**: Whole number of at least 1. A refusal names the constraint: no table for this party size (offer combinations or another time) is a different message from the outlet being full at that time. *(source: contracts/satellite/fnb.yaml#createTableReservation)*
- **Duration**: Prefilled from the outlet's turn time for the party size. Editable by the host. It is what makes the second sitting bookable. *(source: contracts/satellite/fnb.yaml#getFnbReservationPolicy / contracts/satellite/fnb.yaml#/components/schemas/TableReservation)*
- **Guest name, mobile, email**: Mobile in international format (+971 50 123 4567). As soon as a name plus a mobile or email is entered, matches appear under the fields: "Same mobile" ranks above "Similar name". Choosing one links the booking to that guest. Merging two records is not done here; it is done on the guest profile. *(source: DI-808 / contracts/satellite/marketing-crm.yaml#matchGuest / contracts/satellite/marketing-crm.yaml#mergeGuests)*
- **Allergies and requests**: Free text, shown on every later screen with an allergy icon. Prompt the host to ask about allergies. *(source: contracts/satellite/fnb.yaml#/components/schemas/TableReservation)*
- **Table (optional)**: Hidden behind "Request a specific table". By default the host allocates the table at seating. Where shown, recommend tables that fit the party, including declared combinations. *(source: DI-689 / DI-337 / contracts/satellite/fnb.yaml#createTableReservation / contracts/satellite/fnb.yaml#setTableCombinations)*
- **Deposit**: Not shown at all while the venue's dining deposit is off (the default) or the party is below its threshold, and the confirmation then says no card is needed. When it applies, the booking is created "Awaiting deposit" with the amount, basis (per guest, per table or % of minimum spend), hold expiry (15 minutes), refund cut-off and late-cancel terms. It is paid through the till cart. Unpaid at expiry, the booking is cancelled. *(source: DI-1049 / REV3-8b / DI-1048 / R169 / contracts/satellite/fnb.yaml#/components/schemas/TableReservationDeposit)*
- **Seating preference and occasion**: Seating area (indoor, terrace, majlis) and occasion (birthday, anniversary, business) are fields on the booking, not folded into the requests text. *(source: decided 2 October 2026 by Chinmay (CHG-NOTE-004))*

#### Outputs: what the screen shows and produces

**Shown**

**Possible existing guest** (duplicate match): **Runs while the booking is being typed, not after it is saved.** A duplicate created at the podium is one somebody has to find later. Proposes only — `matchGuest` never merges, and the reason each candidate matched is shown beside it.

**Card list** (card list): **Cards rather than a table.** One thumb, arm’s length, and a person who is walking.

**Possible existing guest** (duplicate match): **Runs while the booking is being typed, not after it is saved.** A duplicate created at the podium is one somebody has to find later. Proposes only — `matchGuest` never merges, and the reason each candidate matched is shown beside it.

**Reservation policy** (detail panel, from `getFnbReservationPolicy`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Outlet | the name it points at, never the id | Null is the venue default; an outlet's own policy overrides it. |
| Default turn minutes | 1,234 | The turn time when no party-size band matches. |
| Turn time bands | list or chips (count when long) | Turn time by party size — a two-top and a table of eight do not turn at the same speed, and a single default is how a restaurant ends up … |
| From party size | 1,234 | — |
| To party size | 1,234 | Null means no upper bound. |
| Turn minutes | 1,234 | — |
| Seating buffer minutes | 1,234 | The reset between seatings — clearing, laying and a moment for the floor. Zero is a legitimate answer and a stated one. |
| Maximum duration minutes | 1,234 | The ceiling on a single booking. A reservation extended by hand past this needs the manager, because the table after it is somebody else's … |
| Reserved lead minutes | 1,234 | When a table shows Reserved (Chinmay, 2 October, workbook Q202; DI-689; CHG-CSA-012). |
| Is active | yes / no (icon or chip) | — |

**Possible existing guest** (duplicate match): **Runs while the booking is being typed, not after it is saved.** A duplicate created at the podium is one somebody has to find later. Proposes only — `matchGuest` never merges, and the reason each candidate matched is shown beside it.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (primary button) | navigation or local | — | — | — | — |
| Find matches for guest (secondary button) | `matchGuest` POST `/guests/match` | inline | inline | — | opens modal first |
| Send confirmation (secondary button) | `sendBookingConfirmation` POST `/table-reservations/{reservationId}/confirm` | inline | BookingMessageReceipt | — | — |
| Save booking (primary button) | `createTableReservationForGuest` POST `/outlets/{outletId}/table-reservations` | TableReservation | TableReservation | 400 Validation failed; 409 No cover is free at that time for that party size (`no-availability`). | — |

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Book table**: Creates the booking as Booked (or Awaiting deposit) and offers "Send confirmation" by SMS, WhatsApp or email, with an optional reconfirmation request. *(source: contracts/satellite/fnb.yaml#createTableReservation / contracts/satellite/fnb.yaml#sendBookingConfirmation)*

**Data it reads**: `getFnbReservationPolicy` (onLoad, The default duration and turn times)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The saved create edit reservation. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the create edit reservation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No create edit reservation configured. The form opens empty; it says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `getFnbReservationPolicy` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `GUEST_VIEW` for `matchGuest`; `ORDER_CREATE` for `createTableReservationForGuest`; `ORDER_MODIFY` for `sendBookingConfirmation`. |
| Offline (`?state=offline`) | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 No cover is free at that time for that party size (`no-availability`). |

#### Edge cases to draw

- **Offline at the podium**: Booking is online only. Disable "Book table" with "Needs a connection" and keep the typed details. *(source: contracts/satellite/fnb.yaml#createTableReservation / DI-072)*

#### Consistency with other screens

- Match `GST-070`: The guest-side Reserve a Table uses the same booking. Same status names and the same "no card needed" rule.
- Match `EMP-057`: The duplicate-match candidates look the same as on the guest profile, where the merge happens.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
outlet: Oasis Bistro
when: Thu 15 Oct 2026 · 20:00 GST · 120 min
party: 6
guest:
  name: Fatima Al Suwaidi
  mobile: +971 50 123 4567
  email: fatima.s@example.ae
notes: Nut allergy (1 guest) · anniversary, quiet table if possible
matches:
- Fatima Al Suwaidi · same mobile · 4 visits
- Fatima Alsuwaidi · similar name, same email
depositWhenOn:
  amount: AED 50.00 per guest = AED 300.00
  holdUntil: 19:57 GST
  refundableUntil: Wed 14 Oct 20:00
```

#### Permissions

- `matchGuest` → `GUEST_VIEW` (read) · staff
- `getFnbReservationPolicy` → `PRODUCT_VIEW` (read) · staff
- `sendBookingConfirmation` → `ORDER_MODIFY` (operate) · staff
- `createTableReservationForGuest` → `ORDER_CREATE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `getFnbReservationPolicy` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `GUEST_VIEW` for `matchGuest`; `ORDER_CREATE` for `createTableReservationForGuest`; `ORDER_MODIFY` for `sendBookingConfirmation`.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The client's FnB Board 4 draws a guest duplicate-match and merge process on reservation create/edit and the guest profile: proposed matches shown as candidates, and the merge confirmed by the user. *(agreed · design-brief-9-september 9 Sep 2026, 2 (f) duplicateMatch · DI-808)*
- Table reservation captures table selection (with system recommendations), customer details, guest count, location/outlet and an optional deposit adjusted against the final bill; walk-in and waitlist management are also supported. *(client request · MoM 18 Aug 2026, 4.8 Table Management (Fine Dining) · DI-337)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-055` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/FnB Board 4.dc.html`
- Client design-board frames: `FnB Board 4.dc.html#fnb-4e`

#### Acceptance for the design

- [ ] Every input above is drawn (33), with its required mark, default, format and its error state (400, 409).
- [ ] Every output is drawn (11 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-055?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Find matches for guest, Send confirmation, Save booking.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `GUEST_VIEW`, `ORDER_CREATE`, `ORDER_MODIFY`, `PRODUCT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-056` Walk-In & Waitlist Management

**Walk-In & Waitlist Management — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Floor Service · wave 2 · needs the `fnb` module |
| Block | Block C · task APP-STAFF-EMP-056 |
| Who uses it | venue staff holding `ORDER_MODIFY` (1 operate) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | configEditor (comfortable density): the screen declares only writes (`joinRestaurantWaitlist`) and no read of a population — it is settings, not a list |
| Offline | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Opens with | `venueId` (session), `entryId` (navigation) · cold entry: **Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to. |
| Route | `/operations/walk-in-waitlist-management` |

**What the spec says about it.** **Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Drawn 31 August** — `FnB Board 4.dc.html` frame `fnb-4f`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Walk-In &amp; Waitlist Management* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-011): No read of an outlet's waitlist entries; no operation seats a waiting party or records walked away.

**From the Food, Beverage & Retail process.** The host's list of walk-in parties waiting for a table: add a party in a few taps, tell them a wait the system computed, message them when the table is ready, and take them off when they leave. A walk-in with a free table is seated straight away from the floor plan, not put on the list. The one thing to get right: a live, ordered list of who is waiting and for how long. Today the screen is a form that can only add one entry.

**Known correction pending (do not draw the wrong version)**

- **There is no operation that lists an outlet's waitlist.** Why: The screen cannot show who is waiting, and the pattern was set to configEditor because no read existed. *(source: contracts/satellite/fnb.yaml#joinRestaurantWaitlist / DI-337 / screens/P06-staff-app.yaml#EMP-056; Food, Beverage & Retail)*

**Fixed on main** (the package already carries these; draw what it says): No operation seats a waiting party (links the entry to a table visit) or records "walked away". The state model uses joinRestaurantWaitlist … (CHG-WIR-008); RestaurantWaitlist has no guest name or contact, only subjectId. (CHG-WIR-008); quoteWaitTime and notifyWaitlistParty are on EMP-058, not on the waitlist screen. The form exposes id, outletId, status, notifiedAt and … (CHG-WIR-008).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| id | picker: choose an id (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | — | `RestaurantWaitlist.id` |
| outletId | picker: choose an outlet (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | — | `RestaurantWaitlist.outletId` |
| subjectId | picker: choose a subject (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | — | `RestaurantWaitlist.subjectId` |
| partySize | number field | optional | — | — | — | — | `RestaurantWaitlist.partySize` |
| quotedWaitMinutes | number field (minutes) | optional | — | — | — | — | `RestaurantWaitlist.quotedWaitMinutes` |
| seatingPreference | select | optional | — | Any · Indoor · Outdoor · Bar · Booth · High chair | — | — | `RestaurantWaitlist.seatingPreference` |
| status | select | optional | — | Waiting · Notified · Seated · Walked away · No show · Cancelled | — | — | `RestaurantWaitlist.status` |
| notifiedAt | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `RestaurantWaitlist.notifiedAt` |
| holdExpiresAt | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | How long a table waits for somebody who was called. Too short and a guest returning from the bathroom loses it; too long and the table sits empty at peak — which is why it is a setting rather than a … | `RestaurantWaitlist.holdExpiresAt` |
| Search walk-in | search field | — | — | — | — | — | — |

**Form: Leave waitlist** (confirmDialog, opened by *Leave waitlist*; *Take them off the list* calls `leaveRestaurantWaitlist`, *Keep them* sends nothing)

**Names the party and its place in the list.** `leaveRestaurantWaitlist` ends the entry `cancelled`; a party already called releases its held table at once. Optional: `note`, why the party left (audit R073 (d)).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Note `note` | text area | optional | — | max length 300 | — | Why, where the guest or host gave a reason. Optional. | `leaveRestaurantWaitlist` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The party is already `seated`, `walkedAway` or `noShow`. Names the entry's current status.

**Sent by *Join restaurant waitlist*** (`joinRestaurantWaitlist`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `joinRestaurantWaitlist` body |
| Outlet `outletId` | picker: choose an outlet | required | — | — | shows names, sends the id | — | `joinRestaurantWaitlist` body |
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | — | `joinRestaurantWaitlist` body |
| Party size `partySize` | number field | required | — | — | — | — | `joinRestaurantWaitlist` body |
| Quoted wait minutes `quotedWaitMinutes` | number field (minutes) | optional | — | — | — | — | `joinRestaurantWaitlist` body |
| Seating preference `seatingPreference` | select | optional | — | Any · Indoor · Outdoor · Bar · Booth · High chair | — | — | `joinRestaurantWaitlist` body |
| Status `status` | select | required | — | Waiting · Notified · Seated · Walked away · No show · Cancelled | — | — | `joinRestaurantWaitlist` body |
| Notified at `notifiedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `joinRestaurantWaitlist` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | When the party joined, on the device. The wait a party had is measured from here to `notifiedAt` or to seating, which is the report `walkedAway` exists for. | `joinRestaurantWaitlist` body |
| Hold expires at `holdExpiresAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | How long a table waits for somebody who was called. Too short and a guest returning from the bathroom loses it; too long and the table sits empty at peak — which is why it is a … | `joinRestaurantWaitlist` body |

**Sent by *Notify party*** (`notifyWaitlistParty`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Channel `channel` | radio group | optional | — | SMS · Whatsapp · Push · Pager · Called in person | — | — | `notifyWaitlistParty` body |
| Hold minutes `holdMinutes` | number field (minutes) | optional | 10 | — | — | — | `notifyWaitlistParty` body |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Party size**: Stepper starting at 2, minimum 1. *(source: contracts/satellite/fnb.yaml#joinRestaurantWaitlist)*
- **Seating preference**: Chips Any (default), Indoors, Outdoors, Bar, Booth and High chair needed. *(source: contracts/satellite/fnb.yaml#/components/schemas/RestaurantWaitlist)*
- **Name and mobile**: Needed to call the party by SMS or WhatsApp. Run the same duplicate match as reservations. *(source: contracts/satellite/fnb.yaml#notifyWaitlistParty / DI-808)*
- **Quoted wait**: Computed from turn times and the parties ahead, and shown with its basis ("3 parties ahead · based on tonight's turn times"). The host does not type it. A host override is possible and recorded as such. *(source: contracts/satellite/fnb.yaml#quoteWaitTime / F29 step 1)*

#### Outputs: what the screen shows and produces

**Shown**

**Card list** (card list): **Cards rather than a table.** One thumb, arm’s length, and a person who is walking.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (primary button) | navigation or local | — | — | — | — |
| Join restaurant waitlist (primary button) | `joinRestaurantWaitlist` POST `/waitlist` | RestaurantWaitlist | RestaurantWaitlist | — | works offline |
| Leave waitlist (destructive button) | `leaveRestaurantWaitlist` POST `/waitlist/{entryId}/leave` | inline | RestaurantWaitlist | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The party is already `seated`, `walkedAway` or `noShow`. Names the entry's current status. | opens confirmDialog first |
| Quote wait (secondary button) | `quoteWaitTime` POST `/waitlist/{entryId}/quote` | — | inline | — | — |
| Notify party (secondary button) | `notifyWaitlistParty` POST `/waitlist/{entryId}/notify` | inline | RestaurantWaitlist | — | — |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Waiting list**: Ordered by time joined: name, party, preference, minutes waited against minutes quoted (red once past the quote), and status Waiting or Called. A called party shows a countdown to the hold expiry (default 10 minutes). *(source: contracts/satellite/fnb.yaml#/components/schemas/RestaurantWaitlist / contracts/satellite/fnb.yaml#notifyWaitlistParty)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Call party**: Sends "Your table is ready" by SMS, WhatsApp or push, or records "Called in person". Starts the hold. A party can be called again, and each call is recorded. *(source: contracts/satellite/fnb.yaml#notifyWaitlistParty)*
- **Take off list**: Confirm names the party and their place ("Omar Ziad, party of 4, 2nd"), with an optional reason. It ends Cancelled, and a party already called releases its table at once. This is distinct from "Walked away" (left without telling us). *(source: contracts/satellite/fnb.yaml#leaveRestaurantWaitlist / R073)*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The saved walk-in waitlist. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the walk-in waitlist untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No walk-in waitlist configured. The form opens empty and `joinRestaurantWaitlist` saves the first one; it says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_MODIFY`, which `joinRestaurantWaitlist` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The party is already `seated`, `walkedAway` or `noShow`. Names the entry's current status. |

#### Edge cases to draw

- **Offline at the door**: Adding a party works offline and keeps the time on the device. Quoting, calling and taking off need a connection and show as disabled. *(source: contracts/satellite/fnb.yaml#joinRestaurantWaitlist / contracts/satellite/fnb.yaml#quoteWaitTime / contracts/satellite/fnb.yaml#leaveRestaurantWaitlist)*
- **Guest asks about a deposit**: The waitlist never takes a deposit, even when the venue's dining deposit is on, and never goes into a cart. *(source: contracts/satellite/fnb.yaml#joinRestaurantWaitlist / DI-1048 / REV3-8)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
waiting:
- name: Omar Ziad
  party: 4
  pref: Outdoors
  joined: '19:42'
  quoted: 25 min
  waited: 18 min
  status: Waiting
- name: Priya Nair
  party: 2
  pref: Any
  joined: '19:51'
  quoted: 15 min
  status: Called via SMS
  holdUntil: '20:15'
- name: Daniel Brooks
  party: 5
  pref: High chair needed
  joined: '20:02'
  quoted: 35 min
  status: Waiting
```

#### Permissions

- `joinRestaurantWaitlist` → `ORDER_MODIFY` (operate) · staff, guest
- `leaveRestaurantWaitlist` → `ORDER_MODIFY` (operate) · staff, guest
- `quoteWaitTime` → `ORDER_MODIFY` (operate) · staff
- `notifyWaitlistParty` → `ORDER_MODIFY` (operate) · staff

**A refused user sees:** Shown when the caller lacks `ORDER_MODIFY`, which `joinRestaurantWaitlist` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.9.11 | The system should be able to create,modify, delete a new/old guest to the wait list | Bundles and Promotions | CONTRACTED | data `RestaurantWaitlist` |
| 4.9.14 | Allow guests to make reservations via website, mobile app, kiosk, QR code, call center, and third-party reservation channels with real-time availability. | Bundles and Promotions | CONTRACTED | data `RestaurantWaitlist` |
| 4.9.15 | Prevent overbooking by managing seating capacities, combined tables, reservation duration, occupancy rules, and operating schedules. | Bundles and Promotions | CONTRACTED | data `RestaurantWaitlist` |
| 4.9.16 | Support no-show tracking, deposits, cancellation policies, penalties, blacklists, and automated guest communications. | Bundles and Promotions | CONTRACTED | data `RestaurantWaitlist` |
| 4.9.17 | Provide automated waitlist management with SMS, email, WhatsApp, push notification, and mobile app alerts when tables become available. | Bundles and Promotions | CONTRACTED | data `RestaurantWaitlist` |
| 5.1.4 | The system should be able to provide a way for central reservations where the guest should be able to place a booking from various touchpoints. The system should provide APIs to facilitate … | F&B & Guest Management | CONTRACTED | data `RestaurantWaitlist` |
| 5.6.13 | Track no-shows and support warnings, restrictions, penalties, and future reservation controls. | F&B & Guest Management | CONTRACTED | data `RestaurantWaitlist` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Table reservation captures table selection (with system recommendations), customer details, guest count, location/outlet and an optional deposit adjusted against the final bill; walk-in and waitlist management are also supported. *(client request · MoM 18 Aug 2026, 4.8 Table Management (Fine Dining) · DI-337)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-056` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/FnB Board 4.dc.html`
- Client design-board frames: `FnB Board 4.dc.html#fnb-4f`

#### Acceptance for the design

- [ ] Every input above is drawn (23), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-056?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Join restaurant waitlist, Leave waitlist, Quote wait, Notify party.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `ORDER_MODIFY`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-057` Guest Profile & Dining History

**Guest Profile & Dining History — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Floor Service · wave 2 · needs the `marketing` module |
| Block | Block D · task APP-STAFF-EMP-057 |
| Who uses it | venue staff holding `GUEST_MANAGE`, `GUEST_VIEW`, `ORDER_VIEW` (1 configure, 2 read) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listOrders` reads the population and `getGuestProfile` reads one of them — list, select, act |
| Offline | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Opens with | `venueId` (session), `subjectId` (EMP-003) · cold entry: **Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to. |
| Route | `/operations/guest-profile-dining-history` |

**What the spec says about it.** **Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Named in the board contents and not written up in it.** **Drawn 31 August** — `FnB Board 4.dc.html` frame `fnb-4g`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Guest Profile &amp; Dining History* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** A server sees who is at the table: profile, allergies and notes, dining history, and possible duplicates. A restaurant creates a duplicate every time someone books by phone with a different number, so the floor is where the match is proposed. The merge is always the server's confirmed decision, never automatic.

**Known correction pending (do not draw the wrong version)**

- **The order list exposes staff filters (Venue id, Principal id, Shift id, Status) as text fields.** Why: On a guest profile the list is this guest's orders; those filters belong to the order screens. *(source: screens/P06-staff-app.yaml#EMP-057; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

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
| Search guest profile | search field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Workstation | picker: choose a workstation | — | — | `listOrders` ?workstationId |
| Subject | picker: choose a subject | — | — | `listOrders` ?subjectId |
| Tender | select | — | Cash · Card · Wallet · Voucher · Bank transfer · Hotel charge · Installment · Gift card · Complimentary | `listOrders` ?tender |

**Form: Find matches for guest** (modal, opened by *Find matches for guest*; *Find matches for guest* calls `matchGuest`, *Cancel* sends nothing)

**Collects what `matchGuest` sends before it is called.** Nothing in the body is required. Optional: `name`, `phone`, `email`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | — | — | — | `matchGuest` body |
| Phone `phone` | phone field | optional | — | — | +971 5X XXX XXXX (E.164) | — | `matchGuest` body |
| Email `email` | text field | optional | — | — | — | — | `matchGuest` body |

**Sent by *Merge guests*** (`mergeGuests`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Keep subject `keepSubjectId` | picker: choose a keep subject | required | — | — | shows names, sends the id | — | `mergeGuests` body |
| Merge subjects `mergeSubjectIds` | multi-picker: choose merge subjects | required | — | — | — | — | `mergeGuests` body |
| Reason `reason` | text area | optional | — | — | — | — | `mergeGuests` body |

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Note**: Allergy (flagged prominently), seating preference, last-visit complaint, the regular's usual. *(source: contracts/satellite/marketing-crm.yaml#addGuestNote)*

#### Outputs: what the screen shows and produces

**Shown**

**Every order** (data table, from `listOrders`)

| Shows | Format | Notes |
|---|---|---|
| Order number | text | — |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | The same vocabulary as `Order.channel`, which this projects. |
| Line count | 1,234 | — |

**Possible duplicates of this guest** (duplicate match): Candidates from `matchGuest`, each with the rule that matched it.

**Card list** (card list): **Cards rather than a table.** One thumb, arm’s length, and a person who is walking.

**Possible duplicates of this guest** (duplicate match): Candidates from `matchGuest`, each with the rule that matched it.

**The selected order** (detail panel, from `listOrders`)

| Shows | Format | Notes |
|---|---|---|
| Order number | text | — |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunded amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Hold label | text | As `Order.holdLabel`. |

**Possible duplicates of this guest** (duplicate match): Candidates from `matchGuest`, each with the rule that matched it.

**The guest profile** (detail panel, from `getGuestProfile`)

| Shows | Format | Notes |
|---|---|---|
| Display name | text | — |
| Preferred channel | chip: Email, SMS, Whatsapp, Push, In app, Post | — |
| Engagement score | 1,234 | 22.2.20 and 22.2.21. `lifetimeValue` and `visitCount` existed, so value was a stored figure and engagement was not. |
| Lifetime value | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Visit count | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Merge these two records (confirm dialog) | navigation or local | — | — | — | — |
| Confirm (primary button) | navigation or local | — | — | — | — |
| Merge these two records (confirm dialog) | navigation or local | — | — | — | — |
| Merge these two records (confirm dialog) | navigation or local | — | — | — | — |
| Find matches for guest (primary button) | `matchGuest` POST `/guests/match` | inline | inline | — | opens modal first |
| Merge guests (destructive button) | `mergeGuests` POST `/guests/merge` | inline | MergeResult[] | 409 A record in `mergeSubjectIds` is already merged (`alreadyMerged`), or `keepSubjectId` is among them (`sameProfile`) (MergeRefusedProblem) | — |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Possible duplicates**: Each candidate with its match reason (same mobile, similar name), never a bare score. *(source: DI-808; contracts/satellite/marketing-crm.yaml#matchGuest)*
- **Dining history**: This guest's orders, newest first (this guest's orders only; never a staff filter screen). *(source: contracts/spine/orders.yaml#listOrders)*

**What each action does** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Merge these two records**: Confirmation states the losing record is superseded not deleted, reversible for 30 days, and consent takes the narrower position. *(source: DI-808; contracts/satellite/marketing-crm.yaml#mergeGuests)*

**Data it reads**: `getGuestProfile` (onLoad, Read a guest profile); `listOrders` (onLoad, List orders)

**What opens over it**

- confirmDialog *Merge guests*: **Names what `mergeGuests` changes and what it leaves alone**, in the consequence rather than the verb. A guest profile dining this affects should be identified in the dialog, not just counted. **Collects what `mergeGuests` sends before it is called.** Required: `keepSubjectId`, `mergeSubjectIds`. …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The guest profile dining list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the guest profile dining untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No guest profile dining yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, principalId, shiftId, status, createdFrom, createdTo and the guest profile dining are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `GUEST_VIEW`, which `getGuestProfile` requires to show this screen, and names that permission (the screen's other reads need `ORDER_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `GUEST_MANAGE` for `mergeGuests`, `addGuestNote`. |
| Offline (`?state=offline`) | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A record in `mergeSubjectIds` is already merged (`alreadyMerged`), or `keepSubjectId` is among them (`sameProfile`) (MergeRefusedProblem) |

#### Consistency with other screens

- Match `BO-746`: Same match reasons and merge confirmation.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
guest:
  name: Priya Nair
  notes:
  - ALLERGY - shellfish
  - Prefers terrace
  - Complained about slow service 12 Sep
duplicate: Priya N. - +971 55 210 9981 - same email
```

#### Permissions

- `getGuestProfile` → `GUEST_VIEW` (read) · staff, guest
- `listOrders` → `ORDER_VIEW` (read) · staff, guest, partner
- `matchGuest` → `GUEST_VIEW` (read) · staff
- `mergeGuests` → `GUEST_MANAGE` (configure) · staff
- `addGuestNote` → `GUEST_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `GUEST_VIEW`, which `getGuestProfile` requires to show this screen, and names that permission (the screen's other reads need `ORDER_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `GUEST_MANAGE` for `mergeGuests`, `addGuestNote`.

#### Requirements it meets

8 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 13.3.8 | APIs shall support guest profile creation, updates, segmentation, communication preferences and activity history retrieval. | Developer & API Management | CONTRACTED | `getGuestProfile` |
| 22.2.27 | CRM APIs | Marketing & CRM | CONTRACTED | `getGuestProfile` |
| 22.2.28 | CRM Audit Trail | Marketing & CRM | CONTRACTED | `getGuestProfile` |
| 5.3.7 | The system should allow access to their purchase history and ongoing orders and preferences. | F&B & Guest Management | CONTRACTED | `listOrders` |
| 5.9.4 | The system should be able to provide a detailed log of transactions for each till. Detailed log of transaction should be always accessible, searchable and printable at back office. | F&B & Guest Management | CONTRACTED | `listOrders` |
| 22.2.11 | Ticketing History | Marketing & CRM | CONTRACTED | `listOrders` |
| 22.2.12 | Membership History | Marketing & CRM | CONTRACTED | `listOrders` |
| 22.2.15 | Reservation History | Marketing & CRM | CONTRACTED | `listOrders` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The client's FnB Board 4 draws a guest duplicate-match and merge process on reservation create/edit and the guest profile: proposed matches shown as candidates, and the merge confirmed by the user. *(agreed · design-brief-9-september 9 Sep 2026, 2 (f) duplicateMatch · DI-808)*
- Decision: one unified customer profile across ticketing, F&B and retail gives a 360° view of guest activity and avoids duplicates; e.g. a guest who buys tickets online and later dines is matched by name/mobile to the same profile. *(agreed · MoM 18 Aug 2026, 4.9 Unified Customer Profile · DI-339)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-057` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/FnB Board 4.dc.html`
- Client design-board frames: `FnB Board 4.dc.html#fnb-4g`

#### Acceptance for the design

- [ ] Every input above is drawn (13), with its required mark, default, format and its error state (403, 404, 409).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-057?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Merge these two records, Confirm, Merge these two records, Merge these two records, Find matches for guest, Merge guests.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `GUEST_MANAGE`, `GUEST_VIEW`, `ORDER_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-058` Live Table & Service Management

**Live Table & Service Management — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Floor Service · wave 1 · needs the `fnb` module |
| Block | Block A · task APP-STAFF-EMP-058 |
| Who uses it | venue staff holding `ORDER_CREATE`, `ORDER_MODIFY`, `ORDER_VIEW` (2 operate, 1 read); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | configEditor (comfortable density): the screen declares only writes (`openTableVisit`, `updateTableVisit`, `mergeTableVisits`) and no read of a population — it is settings, not a list |
| Offline | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Opens with | `venueId` (session), `visitId` (EMP-003), `reservationId` (deepLink), `outletId` (session), `ticketId` (deepLink) · cold entry: **Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to. A booking opened from the timeline. **The … |
| Route | `/operations/live-table-service-management` |

**What the spec says about it.** **Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Operations from the 24 August F&B build wired here** — the contract grew and the screens had not caught up, which is how 92 operations reached 49% of screens. **Cross-platform navigation removed 24 August**: KIT-002. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-008): Combinations are pre-service configuration (EMP-053) and the waitlist actions belong to EMP-056; R254 re-derives operations from purpose (F94 step 1, F29 step 1 … Removed 2 October 2026 (CHG-WIR-008): Combinations are pre-service configuration (EMP-053) and the waitlist actions belong to EMP-056; R254 re-derives operations from purpose (F94 step 1, F29 step 1 … Removed 2 October 2026 (CHG-WIR-008): Combinations are pre-service configuration (EMP-053) and the waitlist actions belong to EMP-056; R254 re-derives operations from purpose (F94 step 1, F29 step 1 …

**From the Food, Beverage & Retail process.** The table sheet for one table during service, opened by tapping it on the floor plan: seat the party (walk-in or booking), see where the table is in its meal, order, add a guest, change the server, move the party to another table or merge two tables, and follow the table's activity. The one thing to get right: the client's three named actions (Add guest, Change server, Transfer table) and an activity log, each as one clear action, instead of the 16 buttons the operations produced.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Three operations change the server (updateTableVisit.serverPrincipalId, transferTableVisit, reassignServer), and two move the table (updateTableVisit.tableId, moveTableVisit). (CHG-SPO-019)
- No operation or field gives a table's activity log. (CHG-SPO-019)
- "Fire course" and "Hold course" on the server's handheld (F29 step 5), while the agreed decision says the kitchen pass fires courses and the vocabulary keeps "Fire" on the kitchen side. (CHG-SPO-020)
- F29 step 1 seats with seatTableReservation and openTableVisit, but the table state model moves a table from free to seated only by claimTableSession (the guest's claim). (CHG-SPO-019)

**Fixed on main** (the package already carries these; draw what it says): Naming collision. The client's "Transfer table" means move the party to another table (moveTableVisit). The contract's transferTableVisit … (CHG-SPO-018); "Notify server" as a button on the server's own table sheet. (CHG-SPO-018); "Save table combinations" (setTableCombinations, PRODUCT_CONFIGURE) and the waitlist actions (join, quote wait, notify party) on the table … (CHG-WIR-008); The pattern configEditor with text fields for id, tableId, covers, serverPrincipalId, subjectId and recordedAt, and a "Create F&B order" … (CHG-SPO-018).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **May a server release the next course from the handheld (F29 step 5), or does only the kitchen pass fire (DI-407)?** → Drawn default stands (answer: "Default / recommended accepted"): Show the course strip read-only, plus a "Ready for mains" action that is drawn but marked pending the decision. Never label it "Fire" on the floor. *(decided by Chinmay, 2026-10-02; DEC-050 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search live table | search field | — | — | — | — | — | — |

**Form: Save table visit** (modal, opened by *Save table visit*; *Save table visit* calls `updateTableVisit`, *Cancel* sends nothing)

**Collects what `updateTableVisit` sends before it is called.** Required: `recordedAt`. Optional: `covers`, `tableId`, `serverPrincipalId`, `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Covers `covers` | number field | optional | — | min 1 | — | — | `updateTableVisit` body |
| Table `tableId` | picker: choose a table | optional | — | — | shows names, sends the id | — | `updateTableVisit` body |
| Server principal `serverPrincipalId` | picker: choose a server principal | optional | — | — | shows names, sends the id | — | `updateTableVisit` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `updateTableVisit` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `updateTableVisit` body |

Errors to draw in the form: 409 Target table is occupied.

**Form: Transfer table visit** (modal, opened by *Transfer table visit*; *Transfer table visit* calls `transferTableVisit`, *Cancel* sends nothing)

**Collects what `transferTableVisit` sends before it is called.** Required: `toPrincipalId`, `reason`, `recordedAt`. **`note` is collected too, and required when the reason is Other** — the operation refuses 400 without it (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| To principal `toPrincipalId` | picker: choose a to principal | required | — | — | shows names, sends the id | — | `transferTableVisit` body |
| Reason `reason` | radio group | required | — | Shift change · Break · Section change · Escalation · Other; A reason of `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real reasons. | — | `other` is allowed only with a `note`, which it then requires (decided 28 September, audit R222). | `transferTableVisit` body |
| Note `note` | text area | optional | — | max length 500 | — | Free text. Required where the reason is `other` (audit R222). | `transferTableVisit` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `transferTableVisit` body |

Errors to draw in the form: 400 Validation failed

**Form: Seat table reservation** (modal, opened by *Seat table reservation*; *Seat table reservation* calls `seatTableReservation`, *Cancel* sends nothing)

**Collects what `seatTableReservation` sends before it is called.** Required: `tableIds`, `recordedAt`. Optional: `actualPartySize`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Tables `tableIds` | multi-picker: choose tables | required | — | at least 1 | — | — | `seatTableReservation` body |
| Actual party size `actualPartySize` | number field | optional | — | — | — | — | `seatTableReservation` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `seatTableReservation` body |

Errors to draw in the form: 409 The booking is not in a seatable state. Names its current status.

**Form: Save service stage** (modal, opened by *Save service stage*; *Save service stage* calls `setServiceStage`, *Cancel* sends nothing)

**Collects what `setServiceStage` sends before it is called.** Required: `recordedAt`, `stage`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `setServiceStage` body |
| Stage `stage` | select | required | — | Seated · Drinks ordered · Food ordered · Starters away · Mains away · Dessert · Coffee · Bill requested · Paying · Cleared | — | — | `setServiceStage` body |

**Form: Move table visit** (modal, opened by *Move table visit*; *Move table visit* calls `moveTableVisit`, *Cancel* sends nothing)

**Collects what `moveTableVisit` sends before it is called.** Required: `toTableId`, `recordedAt`. Optional: `reason`. **`note` is collected too, and required when the reason is Other** — the operation refuses 400 without it (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| To table `toTableId` | picker: choose a to table | required | — | — | shows names, sends the id | — | `moveTableVisit` body |
| Reason `reason` | radio group | optional | — | Guest request · Table fault · Party size change · Service recovery · Other; A reason of `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real reasons. | — | `other` is allowed only with a `note`, which it then requires (decided 28 September, audit R222). | `moveTableVisit` body |
| Note `note` | text area | optional | — | max length 500 | — | Free text. Required where the reason is `other` (audit R222). | `moveTableVisit` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `moveTableVisit` body |

Errors to draw in the form: 400 Validation failed; 409 The target table is occupied. Names the visit occupying it in `occupyingVisitId`, because the next thing the server asks is *by whom*, and `suggestedOperation` …

**Form: Reassign server** (modal, opened by *Reassign server*; *Reassign server* calls `reassignServer`, *Cancel* sends nothing)

**Collects what `reassignServer` sends before it is called.** Required: `recordedAt`, `serverPrincipalId`. Optional: `splitGratuity`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `reassignServer` body |
| Server principal `serverPrincipalId` | picker: choose a server principal | required | — | — | shows names, sends the id | — | `reassignServer` body |
| Split gratuity `splitGratuity` | toggle | optional | on | — | — | — | `reassignServer` body |

**Form: Create F&B order** (modal, opened by *Create F&B order*; *Create F&B order* calls `createFnbOrder`, *Cancel* sends nothing)

**Ordering is a menu, like the till's order pad**: dishes and options are tapped, not typed; ids, outlet and device time are set by the app (design-notes correction fnb-retail EMP-058).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createFnbOrder` body |
| Outlet `outletId` | picker: choose an outlet | required | — | — | shows names, sends the id | — | `createFnbOrder` body |
| Service mode `serviceMode` | radio group | required | — | Quick service · Table service · Room service · Collection · Delivery | — | — | `createFnbOrder` body |
| Table visit `tableVisitId` | picker: choose a table visit | optional | — | — | shows names, sends the id | Required for table service. Absent for quick service. | `createFnbOrder` body |
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `createFnbOrder` body |
| ID `lines[].id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createFnbOrder` body |
| Menu item `lines[].menuItemId` | picker: choose a menu item | required | — | — | shows names, sends the id | — | `createFnbOrder` body |
| Quantity `lines[].quantity` | number field | required | — | min 1 | — | — | `createFnbOrder` body |
| Modifier options `lines[].modifierOptionIds` | multi-picker: choose modifier options | optional | — | — | — | — | `createFnbOrder` body |
| Note `lines[].note` | text area | optional | — | max length 200 | — | Free text to the kitchen. Allergy notes belong here and are surfaced prominently. | `createFnbOrder` body |
| Seat number `lines[].seatNumber` | number field | optional | — | — | — | Which cover ordered it. Drives split-by-covers accurately. | `createFnbOrder` body |
| Course `lines[].course` | number field | optional | — | — | — | Course grouping, so the kitchen fires in sequence. | `createFnbOrder` body |
| Redeem entitlement `lines[].redeemEntitlementId` | text field | optional | — | An entitlement already used, for another item or outlet, or not yet valid is refused 409 `entitlementNotRedeemable`; a till that is offline queues the redemption like any sale and the replay is … | — | A meal combo redeemed at the till or by a scan (29 September, MOB-4; applied 30 September). | `createFnbOrder` body |
| Sales order `salesOrderId` | picker: choose a sales order | optional | — | — | shows names, sends the id | The `orders.sales_order` this F&B order fulfils (SD-046, 29 September). A POS sale sends the order it took payment on; the commercial order is the sales order and this is its … | `createFnbOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createFnbOrder` body |

Errors to draw in the form: 400 Validation failed; 409 An item is unavailable, modifier constraints are unmet, a tracked item was ordered offline, or a line's `redeemEntitlementId` cannot be redeemed here …

**Form: Fire course** (modal, opened by *Fire course*; *Fire course* calls `fireCourse`, *Cancel* sends nothing)

**Collects what `fireCourse` sends before it is called.** Required: `recordedAt`, `course`. Optional: `fireAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `fireCourse` body |
| Course `course` | number field | required | — | min 1 | — | — | `fireCourse` body |
| Fire at `fireAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | For `timed` coursing. Absent means now — a server standing at the pass is not scheduling, they are calling it. | `fireCourse` body |

**Form: Hold course** (modal, opened by *Hold course*; *Hold course* calls `holdCourse`, *Cancel* sends nothing)

**Collects what `holdCourse` sends before it is called.** Required: `recordedAt`, `course`. Optional: `reason`. **`note` is collected too, and required when the reason is Other** — the operation refuses 400 without it (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `holdCourse` body |
| Course `course` | number field | required | — | min 1 | — | — | `holdCourse` body |
| Reason `reason` | radio group | optional | — | Table not ready · Guest request · Kitchen backed up · Awaiting previous · Other; A reason of `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real reasons. | — | `other` is allowed only with a `note`, which it then requires (decided 28 September, audit R222). | `holdCourse` body |
| Note `note` | text area | optional | — | max length 500 | — | Free text. Required where the reason is `other` (audit R222). | `holdCourse` body |

Errors to draw in the form: 400 Validation failed

**Sent by *Open table visit*** (`openTableVisit`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `openTableVisit` body |
| Table `tableId` | picker: choose a table | required | — | — | shows names, sends the id | — | `openTableVisit` body |
| Covers `covers` | number field | required | — | min 1 | — | Captured at seating because it drives split-by-covers at close. | `openTableVisit` body |
| Server principal `serverPrincipalId` | picker: choose a server principal | optional | — | — | shows names, sends the id | — | `openTableVisit` body |
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | — | `openTableVisit` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `openTableVisit` body |

**Sent by *Merge table visits*** (`mergeTableVisits`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Source visit `sourceVisitId` | picker: choose a source visit | required | — | — | shows names, sends the id | — | `mergeTableVisits` body |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Covers (seat step)**: Picked after the table, with a stepper defaulting to the booking's party size (or the table's seats for a walk-in). It drives split by covers at the end. For a booking, record the actual party when it differs ("Booked 6, arrived 4"). *(source: DI-104 / contracts/satellite/fnb.yaml#openTableVisit / contracts/satellite/fnb.yaml#seatTableReservation)*
- **Table(s) for a booking**: At least one. The host picks on the mini floor plan, and a declared combination can be chosen as one choice. Seats from Booked, Confirmed or No-show (late arrival) only. *(source: contracts/satellite/fnb.yaml#seatTableReservation / DI-689 / contracts/satellite/fnb.yaml#setTableCombinations)*
- **Move reason**: Guest request, Table fault, Party size changed, Service recovery, or Other. Other needs a note. *(source: contracts/satellite/fnb.yaml#moveTableVisit / R222)*

#### Outputs: what the screen shows and produces

**Shown**

**The table visit** (detail panel, from `getTableVisit`)

| Shows | Format | Notes |
|---|---|---|
| Table label | text | — |
| Status | chip: Open, Bill requested, Settled, Merged, Cancelled | — |
| Running total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Opened at | 1 Oct 2026, 14:30 | — |
| Closed at | 1 Oct 2026, 14:30 | — |

**Card list** (card list): **Cards rather than a table.** One thumb, arm’s length, and a person who is walking.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (primary button) | navigation or local | — | — | — | — |
| Open table visit (primary button) | `openTableVisit` POST `/table-visits` | OpenTableVisitRequest | TableVisit | 409 Table already occupied. | works offline |
| Change covers (secondary button) | `updateTableVisit` PATCH `/table-visits/{visitId}` | inline | TableVisit | 409 Target table is occupied. | works offline; opens modal first |
| Merge table visits (destructive button) | `mergeTableVisits` POST `/table-visits/{visitId}/merge` | inline | TableVisit | 409 Either visit is already closed | — |
| Change server (secondary button) | `transferTableVisit` POST `/table-visits/{visitId}/transfer` | inline | TableVisit | 400 Validation failed | works offline; opens modal first |
| Seat table reservation (secondary button) | `seatTableReservation` POST `/table-reservations/{reservationId}/seat` | inline | TableReservation | 409 The booking is not in a seatable state. Names its current status. | works offline; opens modal first |
| Save service stage (secondary button) | `setServiceStage` PUT `/table-visits/{visitId}/stage` | inline | TableVisit | — | works offline; opens modal first |
| Transfer table (secondary button) | `moveTableVisit` POST `/table-visits/{visitId}/move` | inline | TableVisit | 400 Validation failed; 409 The target table is occupied. Names the visit occupying it in `occupyingVisitId`, because the next thing the server asks is *by whom*, and `suggestedOperation` … | works offline; opens modal first |
| Reassign server (secondary button) | `reassignServer` PUT `/table-visits/{visitId}/server` | inline | TableVisit | — | works offline; opens modal first |
| Create F&B order (secondary button) | `createFnbOrder` POST `/fnb-orders` | CreateFnbOrderRequest | FnbOrder | 400 Validation failed; 409 An item is unavailable, modifier constraints are unmet, a tracked item was ordered offline, or a line's `redeemEntitlementId` cannot be redeemed here … | emits `fnb.kitchenTicketCreated`; works offline; opens modal first |
| Fire course (secondary button) | `fireCourse` POST `/kitchen-tickets/{ticketId}/fire` | inline | KitchenTicket | — | works offline; opens modal first |
| Hold course (secondary button) | `holdCourse` POST `/kitchen-tickets/{ticketId}/hold` | inline | KitchenTicket | 400 Validation failed | works offline; opens modal first |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Service stage**: A stepper from Seated through Drinks ordered, Food ordered, Starters away, Mains away, Dessert, Coffee, Bill requested and Paying, with minutes in the current stage. Stages are set by the act wherever an act exists (an order, a course). The server sets by hand only the ones nothing else observes. *(source: contracts/satellite/fnb.yaml#setServiceStage / F29 step 2)*
- **Activity log**: Newest first, each line with the time and the person: seated, drinks ordered, food ordered, sent to kitchen, course served, guest added, server changed, moved from T4. The course lines show the kitchen's fired time. *(source: DI-338 / DI-334)*
- **Orders and running total**: Orders on this visit grouped by course, with the running total in AED (2 decimals). *(source: contracts/satellite/fnb.yaml#getTableVisit)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Add guest**: Adds covers to the visit (the client's term). Allowed offline. *(source: DI-338 / contracts/satellite/fnb.yaml#updateTableVisit)*
- **Change server**: Pick the incoming server with reason (Shift change, Break, Section change, Escalation, or Other with a note). Gratuity splits between the two servers by default. The change is recorded, not silent. *(source: DI-338 / contracts/satellite/fnb.yaml#reassignServer / contracts/satellite/fnb.yaml#transferTableVisit / R222)*
- **Transfer table**: The client's "Transfer table" is moving the party to another table: the bill, the kitchen tickets and the server follow. If the target is occupied, the refusal names who is there and offers "Merge with T9 instead". *(source: DI-338 / contracts/satellite/fnb.yaml#moveTableVisit / POSV2-8)*
- **Merge tables**: Confirm names both tables and their covers and bills ("T6 (4, AED 212.00) joins T7 (5, AED 318.50) into one bill"). Online only. Refused if either visit is already closed. *(source: contracts/satellite/fnb.yaml#mergeTableVisits / POSV2-8)*
- **Order**: Opens the menu for this table (same order pad as the till), with the table and table service already set. *(source: contracts/satellite/fnb.yaml#createFnbOrder / F29 step 2)*

**Where the user goes next**

- → `EMP-059` Table Order, Bill & Payment Management: *Food is ordered with courses*; carries `visitId`
- → `EMP-060` Reservation & Table Performance: *Reservation & Table Performance*; carries `outletId`
- → `KIT-002` Kitchen Display System (KDS): *One main comes back wrong*; carries `ticketId`, `visitId`

**What opens over it**

- confirmDialog *Merge table visits*: **Names what `mergeTableVisits` changes and what it leaves alone**, in the consequence rather than the verb. A live table service this affects should be identified in the dialog, not just counted. **Collects what `mergeTableVisits` sends before it is called.** Required: `sourceVisitId`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The saved live table service. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the live table service untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No live table service configured. The form opens empty and `openTableVisit` saves the first one; it says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `getTableVisit` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 An item is unavailable, modifier constraints are unmet, a tracked item was ordered offline, or a line's `redeemEntitlementId` cannot be redeemed here …; 409 Either visit is already closed; 409 Table already occupied. |

#### Edge cases to draw

- **Seat on a table someone else just seated**: The 409 names the visit at that table ("T9 was seated by Khalid at 20:02") and offers another table. *(source: contracts/satellite/fnb.yaml#openTableVisit)*
- **Order with a recipe-linked item while offline**: Refused with "Can't order this offline; stock is tracked". Untracked items queue normally. *(source: contracts/satellite/fnb.yaml#createFnbOrder)*

#### Consistency with other screens

- Match `POS-028`: Move and merge exist here and are off the till until after r2. The till's table list actions (Seat & order, Recall check, Settle bill, Seat booking) use the same words.
- Match `KIT-003`: The course state shown here is the kitchen pass's. The fired timer and course names match.
- Match `EMP-059`: The bill and payment live on EMP-059. This sheet links to it ("Bill").

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
table: T12 · Main Hall · 4 seats
visit:
  covers: 4
  server: Priya Nair
  seatedAt: '19:58'
  stage: Starters away · 14 min
  runningTotal: AED 448.00
log:
- 20:31 Starters served · kitchen
- 20:12 Food ordered · Priya
- 20:03 Drinks ordered · Priya
- 19:58 Seated, booking Al Suwaidi (6 → 4) · Aisha (host)
```

#### Permissions

- `openTableVisit` → `ORDER_CREATE` (operate) · staff
- `updateTableVisit` → `ORDER_MODIFY` (operate) · staff
- `mergeTableVisits` → `ORDER_MODIFY` (operate) · staff
- `transferTableVisit` → `ORDER_MODIFY` (operate) · staff
- `seatTableReservation` → `ORDER_MODIFY` (operate) · staff
- `setServiceStage` → `ORDER_MODIFY` (operate) · staff
- `moveTableVisit` → `ORDER_MODIFY` (operate) · staff
- `reassignServer` → `ORDER_MODIFY` (operate) · staff
- `createFnbOrder` → `ORDER_CREATE` (operate) · staff
- `fireCourse` → `ORDER_MODIFY` (operate) · staff
- `holdCourse` → `ORDER_MODIFY` (operate) · staff
- `getTableVisit` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `getTableVisit` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

10 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.6.19 | The system should be able to ensure table number and number of guests can be updated. | Bundles and Promotions | CONTRACTED | `updateTableVisit` |
| 5.1.2 | The system should be able to allow grouping of table reservations for easier order management and billing as per the guest to choice/request. | F&B & Guest Management | CONTRACTED | `mergeTableVisits` |
| 4.6.15 | The system should be able to transfer one/multiple/all checks to a different operator. | Bundles and Promotions | CONTRACTED | `transferTableVisit` |
| 4.9.7 | The system should be able to assign waiters to a table | Bundles and Promotions | CONTRACTED | `transferTableVisit` |
| 4.9.8 | The system should be able to modify waiters assignment to tables | Bundles and Promotions | CONTRACTED | `transferTableVisit` |
| 4.9.9 | The system should be able to delete waiter assignment to a table | Bundles and Promotions | CONTRACTED | `transferTableVisit` |
| 4.6.1 | The system should be able to record a sale to guests from the POS register using menu screens/buttons. | Bundles and Promotions | CONTRACTED | `createFnbOrder` |
| 4.6.2 | The system should be able to record a sale to guests from the POS register using manual product sale option | Bundles and Promotions | CONTRACTED | `createFnbOrder` |
| 4.9.2 | The system should have a notes section to capture special requests that modifiers don't cover, such as bespoke guest requirements. | Bundles and Promotions | CONTRACTED | `createFnbOrder` |
| 10.1.1 | The system should allow send special request comments/directions on the kitchen display/printers for the kitchen preparation guest requests/inputs. | Games & F&B Integration | CONTRACTED | `createFnbOrder` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Each table has an activity log (seated, drinks ordered, food ordered, sent to kitchen, course served, etc.) and actions Add Guest, Change Server and Transfer Table. *(client request · MoM 18 Aug 2026, 4.8 Table Management (Fine Dining) · DI-338)*
- Decision: table status flow is Available → Ordered → Table Closed (after payment) → Reserved (booked in advance). No "Cleaning" status — cleaning is a manual staff task, deliberately excluded to avoid complexity. *(agreed · MoM 18 Aug 2026, 4.8 Table Management (Fine Dining); 5. Key Decisions · DI-336)*
- A visual floor/table map (main hall, terrace, VIP lounge, etc.) shows table status, and tables can be tagged with a customer category (e.g. VIP) so staff prioritise service. *(client request · MoM 18 Aug 2026, 4.8 Table Management (Fine Dining) · DI-335)*
- Support both service models: quick-service (order and pay at the counter before food is served) and fine dining (table opened, items added over the visit, bill printed and paid at the end). *(agreed · MoM 3 Aug 2026, 5. Table Management & Dining Service Models · DI-105)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A85** Design the table management module for fine dining: visual floor/table map with VIP tagging, table status flow (Available → Ordered → Table Closed → Reserved), reservations with deposit and waitlist, a per-table … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'table management')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-058` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/FnB Board 4.dc.html`
- Drawn by: Claude Design F&B pack, 24 August
- Client design-board frames: `FnB Board 4.dc.html#fnb-4a`, `FnB Board 4.dc.html#fnb-4b`, `FnB Board 4.dc.html#fnb-4h`
- Flow F29 *A table is seated, coursed and split*, step 1: The host seats the booking against a table. → A visit opens on the table. **The reservation becomes a visit rather than staying a reservation** — a booking that is still a booking while people are sitting at it is a table the system thinks is …
- Flow F29 *A table is seated, coursed and split*, step 2: The server marks them seated and takes drinks. → Stage `seated`, then `drinksOrdered`. **The stage is what makes a turn time real** — a table `seated` fifty minutes and not ordered is a service problem, and open/closed cannot say so.
- Flow F29 *A table is seated, coursed and split*, step 5: Starters cleared. The server judges the table is ready and fires the mains. → **The act this whole flow exists to prove.** `KitchenTicket.coursing` carried the policy until 24 August and nothing fired anything — a venue could configure coursing and never course a table.
- Flow F80 *A table is configured, reserved, seated and billed*, step 2: Live Table & Service Management. → **Drawn by the client as FNB-4B.** 10 operations on this step.
- Flow F94 *A restaurant floor is set up before service*, step 1: Live Table & Service Management. → **Drawn by the client as FNB-4A.**
- Flow F29 branch at step 1 (low): when There is no booking — four people walk in., Enters through the waitlist instead: `joinRestaurantWaitlist`, then `quoteWaitTime`, then `notifyWaitlistParty` when a table frees. **The quote is computed, not typed** — a host guesses low under …
- Flow F29 branch at step 2 (medium): when The party is larger than the table., `setTableCombinations` says which tables push together and to what capacity. **Declared rather than inferred** — a pillar or a step means two adjacent tables do not always combine, and a host knows …
- Flow F29 branch at step 5 (low): when The table has gone quiet and is not ready for mains., `holdCourse`. **A held course keeps its place in the rail** so the kitchen can see how long it has waited — a held course nobody fires becomes a cold course nobody wants.
- Flow F94 branch at step 1 (medium): when A step is not licensed for this tenant., **The chain stops at the module boundary.** `requiresModule` decides — the journey is shorter, not broken.

#### Acceptance for the design

- [ ] Every input above is drawn (51), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (5 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-058?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Open table visit, Change covers, Merge table visits, Change server, Seat table reservation, Save service stage, Transfer table, Reassign server, Create F&B order, Fire course, Hold course.
- [ ] Every transition is wired: `EMP-059`, `EMP-060`, `KIT-002`.
- [ ] Every gated control is gated: `ORDER_CREATE`, `ORDER_MODIFY`, `ORDER_VIEW`.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-059` Table Order, Bill & Payment Management

**Table Order, Bill & Payment Management — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Floor Service · wave 1 · needs the `fnb` module |
| Block | Block A · task APP-STAFF-EMP-059 |
| Who uses it | venue staff holding `ORDER_CREATE`, `ORDER_MODIFY`, `ORDER_VIEW` (2 operate, 1 read); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | statusTracker (comfortable density): `getBill` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Opens with | `venueId` (session), `visitId` (EMP-003) · cold entry: **Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to. |
| Route | `/operations/table-order-bill-payment-management` |

**What the spec says about it.** **Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Named in the board contents and not written up in it.** **Operations from the 24 August F&B build wired here** — the contract grew and the screens had not caught up, which is how 92 operations reached 49% of screens.

**From the Food, Beverage & Retail process.** The table's bill at the end of the visit: every line across every order, service charge and VAT, the split the party asks for, comps for service recovery, payment, and closing the table. The one thing to get right: the split is done at close and each part recomputes its own tax and service charge, so the parts always sum to the bill to the fils. A comp is never shown as a discount.

**Known correction pending (do not draw the wrong version)**

- **Two ways to pay. closeTableVisit takes the payments inline (sub-bill, tender, amount), and the screen also offers "Create payment" (createPayment), which needs an orderId. The sales orders exist only after the visit is closed.** Why: F29 step 9 lists both, and the table state model moves the table on createPayment. Which act takes the money for a sub-bill is undefined. *(source: contracts/satellite/fnb.yaml#closeTableVisit / contracts/spine/orders.yaml#createPayment / F29 step 9; Food, Beverage & Retail)*
- **The Bill has no deposit line.** Why: DI-337 says a deposit is adjusted against the final bill, and REV3-8b applies a held deposit to the bill. *(source: DI-337 / REV3-8b / contracts/satellite/fnb.yaml#/components/schemas/Bill; Food, Beverage & Retail)*
- **closeTableVisit moves the table to needsClearing.** Why: The client's flow is Ordered, then Table Closed, with no cleaning status. See EMP-052. *(source: DI-336 / contracts/satellite/fnb.yaml#closeTableVisit; Food, Beverage & Retail)*
- **requestBill is described as reversible, but no operation reverses it. The state model returns from billRequested to open via openTableVisit, which refuses an occupied table.** Why: The design needs "Add more" to work. *(source: contracts/satellite/fnb.yaml#requestBill; Food, Beverage & Retail)*
- **splitBill, compItem and transferOrderItems are marked offline-capable while F29 says splitting and payment need the network.** Why: A split computed offline against a changed bill makes two guests pay for one item. *(source: F29 step 8 / contracts/satellite/fnb.yaml#splitBill; Food, Beverage & Retail)*
- **The "Create F&B order" modal collecting raw ids, a "Create payment" modal collecting id, orderId, tender and deviceId, and the transition to EMP-058 on transferOrderItems.** Why: Plumbing on a user's screen. Moving items keeps the server on the bill and does not navigate. *(source: screens/P06-staff-app.yaml#EMP-059; Food, Beverage & Retail)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search table order, bill | search field | — | — | — | — | — | — |

**Form: Request bill** (modal, opened by *Request bill*; *Request bill* calls `requestBill`, *Cancel* sends nothing)

**Collects what `requestBill` sends before it is called.** Required: `recordedAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `requestBill` body |

**Form: Create payment** (modal, opened by *Create payment*; *Create payment* calls `createPayment`, *Cancel* sends nothing)

**Card, contactless, wallet or room charge; never cash.** A handheld takes no cash payment: cash goes to a till (decided 2 October 2026, Chinmay, batch 6, EMP-009: "No cash on handhelds; cash goes to a till"; DEC-200; CHG-CSP-039), and `createPayment` refuses cash from a session with no till (409 `cashNotOnHandheld`). Required: `orderId`, `tender`, `amount`; `id` and `recordedAt` are set by the app. Dismissing sends nothing.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the payment, and its idempotency key — it must equal the `Idempotency-Key` header. | `createPayment` body |
| Order `orderId` | picker: choose an order | required | — | — | shows names, sends the id | — | `createPayment` body |
| Tender `tender` | select | required | — | Cash · Card · Wallet · Voucher · Bank transfer · Hotel charge · Installment · Gift card · Complimentary | — | `wallet` is a digital wallet (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 … | `createPayment` body |
| Amount `amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createPayment` body |
| Tender currency `tenderCurrency` | text field | optional | — | pattern `^[A-Z]{3}$` | — | The currency the guest handed over, where it is not the venue's — becomes `Payment.tenderCurrency`. | `createPayment` body |
| Tender amount `tenderAmount` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What the guest handed over, in `tenderCurrency` — becomes `Payment.tenderAmount`, one name for one concept (renamed from `tenderedAmount` on 26 September). | `createPayment` body |
| Wallet authorisation `walletAuthorisationId` | text field | optional | — | — | — | Cross-cell wallet hold, where the guest's home cell is elsewhere. | `createPayment` body |
| Wallet hold `walletHoldId` | picker: choose a wallet hold | optional | — | — | shows names, sends the id | For a `wallet` tender, the hold `wallet.holdWalletFunds` placed (SD-027). Capture debits it; the order service writes no wallet table. | `createPayment` body |
| Return URL `returnUrl` | URL field | optional | — | — | https:// | Where the provider returns the guest after a 3-D Secure challenge or hosted page (SD-034). | `createPayment` body |
| Terminal `terminalId` | picker: choose a terminal | optional | — | — | shows names, sends the id | The card terminal to instruct, for a card payment at a till (ECR flow, SD-034). | `createPayment` body |
| Device `deviceId` | picker: choose a device | optional | — | — | shows names, sends the id | — | `createPayment` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createPayment` body |

Errors to draw in the form: 402 Declined by the provider (`providerDeclined`). (PaymentProblem); 409 Tender unavailable offline (`tenderUnavailableOffline`), amount exceeds the balance due (`exceedsBalanceDue`), or a guest channel sent a tender other than card … (PaymentProblem)

**Form: Create F&B order** (modal, opened by *Create F&B order*; *Create F&B order* calls `createFnbOrder`, *Cancel* sends nothing)

**Collects what `createFnbOrder` sends before it is called.** Required: `id`, `outletId`, `serviceMode`, `lines`, `recordedAt`. Optional: `tableVisitId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createFnbOrder` body |
| Outlet `outletId` | picker: choose an outlet | required | — | — | shows names, sends the id | — | `createFnbOrder` body |
| Service mode `serviceMode` | radio group | required | — | Quick service · Table service · Room service · Collection · Delivery | — | — | `createFnbOrder` body |
| Table visit `tableVisitId` | picker: choose a table visit | optional | — | — | shows names, sends the id | Required for table service. Absent for quick service. | `createFnbOrder` body |
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `createFnbOrder` body |
| ID `lines[].id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createFnbOrder` body |
| Menu item `lines[].menuItemId` | picker: choose a menu item | required | — | — | shows names, sends the id | — | `createFnbOrder` body |
| Quantity `lines[].quantity` | number field | required | — | min 1 | — | — | `createFnbOrder` body |
| Modifier options `lines[].modifierOptionIds` | multi-picker: choose modifier options | optional | — | — | — | — | `createFnbOrder` body |
| Note `lines[].note` | text area | optional | — | max length 200 | — | Free text to the kitchen. Allergy notes belong here and are surfaced prominently. | `createFnbOrder` body |
| Seat number `lines[].seatNumber` | number field | optional | — | — | — | Which cover ordered it. Drives split-by-covers accurately. | `createFnbOrder` body |
| Course `lines[].course` | number field | optional | — | — | — | Course grouping, so the kitchen fires in sequence. | `createFnbOrder` body |
| Redeem entitlement `lines[].redeemEntitlementId` | text field | optional | — | An entitlement already used, for another item or outlet, or not yet valid is refused 409 `entitlementNotRedeemable`; a till that is offline queues the redemption like any sale and the replay is … | — | A meal combo redeemed at the till or by a scan (29 September, MOB-4; applied 30 September). | `createFnbOrder` body |
| Sales order `salesOrderId` | picker: choose a sales order | optional | — | — | shows names, sends the id | The `orders.sales_order` this F&B order fulfils (SD-046, 29 September). A POS sale sends the order it took payment on; the commercial order is the sales order and this is its … | `createFnbOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createFnbOrder` body |

Errors to draw in the form: 400 Validation failed; 409 An item is unavailable, modifier constraints are unmet, a tracked item was ordered offline, or a line's `redeemEntitlementId` cannot be redeemed here …

**Form: Split bill** (modal, opened by *Split bill*; *Split bill* calls `splitBill`, *Cancel* sends nothing)

**Collects what `splitBill` sends before it is called.** Required: `recordedAt`, `method`. Optional: `parts`, `amounts`, `lineAssignments`, `categoryAssignments`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the split (offline-capable). | `splitBill` body |
| Method `method` | radio group | required | — | By amount · By covers · By category · By line · By seat | — | — | `splitBill` body |
| Parts `parts` | number field | optional | — | min 2 | — | For `byCovers` — defaults to the visit's cover count. | `splitBill` body |
| Amounts `amounts` | repeatable rows | optional | — | — | — | For `byAmount`. Must sum to the bill total. | `splitBill` body |
| Line assignments `lineAssignments` | repeatable rows | optional | — | — | — | For `byLine` or `bySeat`. Every line must be assigned exactly once. | `splitBill` body |
| Line `lineAssignments[].lineId` | text field | required | — | — | — | — | `splitBill` body |
| Part index `lineAssignments[].partIndex` | number field | required | — | min 0 | — | — | `splitBill` body |
| Category assignments `categoryAssignments` | repeatable rows | optional | — | — | — | For `byCategory` — food to one part, beverage to another. | `splitBill` body |
| Category code `categoryAssignments[].categoryCode` | text field | required | — | — | — | — | `splitBill` body |
| Part index `categoryAssignments[].partIndex` | number field | required | — | min 0 | — | — | `splitBill` body |

Errors to draw in the form: 400 Split does not sum to the bill total, or a line is assigned twice.; 409 Visit already settled

**Form: Comp item** (modal, opened by *Comp item*; *Comp item* calls `compItem`, *Cancel* sends nothing)

**Collects what `compItem` sends before it is called.** Required: `orderLineId`, `recordedAt`, `reason`. Optional: `note`. **When the reason is Other, `note` is required** — the operation refuses 400 without it (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Order line `orderLineId` | picker: choose an order line | required | — | — | shows names, sends the id | An order line (`FnbOrder.lines[].id`). | `compItem` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `compItem` body |
| Reason `reason` | select | required | — | Quality issue · Wait · Wrong item · Allergy incident · Goodwill · Staff meal · Wastage · Other; A reason of `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real reasons. | — | `other` is allowed only with a `note`, which it then requires (decided 28 September, audit R222). | `compItem` body |
| Note `note` | text area | optional | — | — | — | Free text. Required where the reason is `other` (audit R222). | `compItem` body |

Errors to draw in the form: 400 Validation failed

**Form: Transfer order items** (modal, opened by *Transfer order items*; *Transfer order items* calls `transferOrderItems`, *Cancel* sends nothing)

**Collects what `transferOrderItems` sends before it is called.** Required: `toVisitId`, `lineIds`, `recordedAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| To visit `toVisitId` | picker: choose a to visit | required | — | — | shows names, sends the id | — | `transferOrderItems` body |
| Lines `lineIds` | multi-picker: choose lines | required | — | — | — | — | `transferOrderItems` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `transferOrderItems` body |

**Sent by *Close table visit*** (`closeTableVisit`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Payments `payments` | repeatable rows | required | — | at least 0 | — | Empty only at a `payFirst` outlet with nothing left to pay (CHG-RUL-001). | `closeTableVisit` body |
| Sub bill `payments[].subBillId` | text field | optional | — | — | — | The sub-bill this payment settles. Omitted on a bill that was never split, which closes as one sub-bill (CHG-RUL-001); required once the bill is split. | `closeTableVisit` body |
| Tender `payments[].tender` | text field | required | — | — | — | — | `closeTableVisit` body |
| Amount `payments[].amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `closeTableVisit` body |
| Gratuity `gratuity` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `closeTableVisit` body |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Split**: Methods in the client's order: By amount, By covers (defaults to the table's covers), By category (food to one guest, drinks to another), then By item and By seat. Every line goes to exactly one part. Amounts must sum to the total. A split that does not sum is refused, never rounded away. Remainders go to the minor unit, and 3-decimal currencies keep the third decimal. *(source: DI-106 / contracts/satellite/fnb.yaml#splitBill / F29 step 8 / DI-306)*
- **Comp reason**: Quality issue, Long wait, Wrong item, Allergy incident, Goodwill, Staff meal, Wastage, or Other (with a note). A comp on a line above the venue's comp limit (proposed AED 100.00) needs a manager with discount authority, by PIN on this device. *(source: contracts/satellite/fnb.yaml#compItem / R197 / R222)*
- **Tip**: The guest's gratuity, entered at payment, separate from the service charge (which is revenue, not a tip). *(source: contracts/satellite/fnb.yaml#closeTableVisit / contracts/satellite/fnb.yaml#/components/schemas/TableVisit)*

#### Outputs: what the screen shows and produces

**Shown**

**The bill** (detail panel, from `getBill`)

| Shows | Format | Notes |
|---|---|---|
| Covers | 1,234 | — |
| Subtotal | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Discount amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Card list** (card list): **Cards rather than a table.** One thumb, arm’s length, and a person who is walking.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (primary button) | navigation or local | — | — | — | — |
| Close table visit (destructive button) | `closeTableVisit` POST `/table-visits/{visitId}/close` | inline | inline | 409 Payments do not cover the bill, or lines remain unserved (named in `lineIds`). | — |
| Create payment (secondary button) | `createPayment` POST `/payments` | CreatePaymentRequest | Payment | 402 Declined by the provider (`providerDeclined`). (PaymentProblem); 409 Tender unavailable offline (`tenderUnavailableOffline`), amount exceeds the balance due (`exceedsBalanceDue`), or a guest channel sent a tender … | emits `payment.captured`, `order.paid`; works offline; opens modal first |
| Create F&B order (secondary button) | `createFnbOrder` POST `/fnb-orders` | CreateFnbOrderRequest | FnbOrder | 400 Validation failed; 409 An item is unavailable, modifier constraints are unmet, a tracked item was ordered offline, or a line's `redeemEntitlementId` cannot be redeemed here … | emits `fnb.kitchenTicketCreated`; works offline; opens modal first |
| Split bill (secondary button) | `splitBill` POST `/table-visits/{visitId}/bill/split` | SplitBillRequest | BillSplit | 400 Split does not sum to the bill total, or a line is assigned twice.; 409 Visit already settled | works offline; opens modal first |
| Comp item (secondary button) | `compItem` POST `/table-visits/{visitId}/comp` | inline | TableVisit | 400 Validation failed | works offline; opens modal first |
| Transfer order items (secondary button) | `transferOrderItems` POST `/table-visits/{visitId}/transfer-items` | inline | TableVisit | — | works offline; opens modal first |
| Request bill (primary button) | `requestBill` POST `/table-visits/{visitId}/request-bill` | inline | TableVisit | — | works offline; opens modal first |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Bill**: Lines grouped by course (or by seat when split by seat), each with quantity and line total. Comped lines are struck through with "Comp · Long wait · Priya". Then subtotal, service charge, VAT 5%, total in AED with 2 decimals. A deposit paid on the booking is shown as a deduction above the amount to pay. *(source: contracts/satellite/fnb.yaml#getBill / DI-337 / contracts/satellite/fnb.yaml#compItem)*
- **Sub-bills**: One card per part with its own subtotal, VAT, total and a Paid or To pay state. The table closes when every part is paid. *(source: contracts/satellite/fnb.yaml#/components/schemas/BillSplit / F29 step 9)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Request bill**: Marks the table "Bill requested" on the floor plan. The kitchen stops accepting additions for this table. Reversible: "Add more" puts the table back to ordering when the party orders another round. *(source: contracts/satellite/fnb.yaml#requestBill / F29 step 8)*
- **Move items to another table**: Moves selected lines to another table's bill (a guest who moves from the bar). The kitchen is not asked to make them again. *(source: contracts/satellite/fnb.yaml#transferOrderItems / F29 step 8)*
- **Close table**: Takes the payments per part and closes. The 409 says why, either "AED 155.06 still to pay on part 3" or "2 items not yet served: Umm Ali ×2". The table then goes to Table closed and the next waiting party can be called. *(source: contracts/satellite/fnb.yaml#closeTableVisit / F29 step 9 / DI-336)*

**Data it reads**: `getBill` (onLoad, Bill for a visit)

**Where the user goes next**

- → `EMP-058` Live Table & Service Management: *Live Table & Service Management*; carries `ticketId`, `visitId`; calls `transferOrderItems`
- → `KIT-002` Kitchen Display System (KDS): *The kitchen makes the starters and bumps them*; carries `ticketId`, `visitId`; calls `createFnbOrder`

**What opens over it**

- confirmDialog *Close table visit*: **Names what `closeTableVisit` changes and what it leaves alone**, in the consequence rather than the verb. A table order bill this affects should be identified in the dialog, not just counted. **Collects what `closeTableVisit` sends before it is called.** Required: `payments`. Optional: `gratuity`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The table order bill, read by `getBill`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the table order bill untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No table order bill yet. Offers Create payment (`createPayment`). |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `getBill` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ORDER_CREATE` for `closeTableVisit`, `createPayment`, `createFnbOrder`; `ORDER_MODIFY` for `splitBill`, `compItem`, `transferOrderItems`, `requestBill`. |
| Offline (`?state=offline`) | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Split does not sum to the bill total, or a line is assigned twice.; 400 Validation failed; 409 An item is unavailable, modifier constraints are unmet, a tracked item was ordered offline, or a line's `redeemEntitlementId` cannot be redeemed here …; 409 Payments do not cover the bill, or lines remain unserved (named in `lineIds`). |

#### Edge cases to draw

- **Card payment with no answer from the terminal**: Show "Waiting for the card terminal" and check the payment's status. Never assume it failed or take the card again. *(source: contracts/spine/orders.yaml#createPayment)*
- **Offline at the table**: Ordering continues. Split, payment by card and close need a connection and show as disabled with that reason. *(source: F29 step 8 / contracts/satellite/fnb.yaml#closeTableVisit)*

#### Consistency with other screens

- Match `POS-005`: Payment tenders and wording ("Charge AED x") match the till's single tender step.
- Match `POS-028`: The till's "Settle bill" on a table is the same bill, split and close.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
table: T12 · 4 covers · Priya Nair
lines:
- item: Mezze platter
  qty: 1
  total: '62.00'
  course: Starters
- item: Grilled hammour
  qty: 2
  total: '196.00'
  course: Mains
- item: Lamb ouzi
  qty: 1
  total: '115.00'
  course: Mains
- item: Fresh lemon mint
  qty: 4
  total: '88.00'
  course: Drinks
- item: Umm Ali
  qty: 2
  total: '76.00'
  course: Dessert
subtotal: AED 537.00
serviceCharge: AED 53.70
vat5: AED 29.54
total: AED 620.24
splitByCovers:
- AED 155.06
- AED 155.06
- AED 155.06
- AED 155.06
comp: Grilled hammour ×1 · AED 98.00 · Long wait (under the AED 100.00 limit, no manager needed)
orderNumbers:
- OAS-104582
- OAS-104590
```

#### Permissions

- `closeTableVisit` → `ORDER_CREATE` (operate) · staff
- `createPayment` → `ORDER_CREATE` (operate) · staff, guest, partner
- `createFnbOrder` → `ORDER_CREATE` (operate) · staff
- `splitBill` → `ORDER_MODIFY` (operate) · staff
- `getBill` → `ORDER_VIEW` (read) · staff
- `compItem` → `ORDER_MODIFY` (operate) · staff
- `transferOrderItems` → `ORDER_MODIFY` (operate) · staff
- `requestBill` → `ORDER_MODIFY` (operate) · staff

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `getBill` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ORDER_CREATE` for `closeTableVisit`, `createPayment`, `createFnbOrder`; `ORDER_MODIFY` for `splitBill`, `compItem`, `transferOrderItems`, `requestBill`.

#### Requirements it meets

16 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.23 | Payment can be done online. | Ticketing Sales | CONTRACTED | `createPayment` |
| 2.12.35 | System shall support multiple payment methods within a single transaction including cash, credit card, wallet, loyalty points, vouchers, gift cards, bank transfers, and credit balances. | Ticketing Sales | CONTRACTED | `createPayment` |
| 2.13.2 | The operator can register the payment. | Ticketing Sales | CONTRACTED | `createPayment` |
| 2.15.3 | The operator can register the payment and print the pass. | Ticketing Sales | CONTRACTED | `createPayment` |
| 4.2.6 | The system should be able to accept several currencies in one transaction (a guest pays in USD and gets the change in AED). | Bundles and Promotions | CONTRACTED | `createPayment` |
| 4.2.7 | The system should be accept multiple payments in one transaction. For example, there must be an option to split the payment within a group of guests | Bundles and Promotions | CONTRACTED | `createPayment` |
| 4.2.13 | The system should be able to support payment of one transaction with multiple payment methods. | Bundles and Promotions | CONTRACTED | `createPayment` |
| 4.2.22 | The system shall support mixed payment scenarios using any combination of loyalty points, wallet balances, gift cards, vouchers, cash, and payment cards within the same transaction. | Bundles and Promotions | CONTRACTED | `createPayment` |
| 4.6.27 | Support mobile payment for F&B and retail orders. | Bundles and Promotions | CONTRACTED | `createPayment` |
| 4.6.1 | The system should be able to record a sale to guests from the POS register using menu screens/buttons. | Bundles and Promotions | CONTRACTED | `createFnbOrder` |
| 4.6.2 | The system should be able to record a sale to guests from the POS register using manual product sale option | Bundles and Promotions | CONTRACTED | `createFnbOrder` |
| 4.9.2 | The system should have a notes section to capture special requests that modifiers don't cover, such as bespoke guest requirements. | Bundles and Promotions | CONTRACTED | `createFnbOrder` |
| … 4 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Table/seat-level structure supports flexible bill-splitting: by amount, by number of covers, or by category (e.g. one guest pays food, another drinks). *(agreed · MoM 3 Aug 2026, 5. Table Management & Dining Service Models · DI-106)*
- Support both service models: quick-service (order and pay at the counter before food is served) and fine dining (table opened, items added over the visit, bill printed and paid at the end). *(agreed · MoM 3 Aug 2026, 5. Table Management & Dining Service Models · DI-105)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A85** Design the table management module for fine dining: visual floor/table map with VIP tagging, table status flow (Available → Ordered → Table Closed → Reserved), reservations with deposit and waitlist, a per-table … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'table management')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-059` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/FnB Board 4.dc.html`
- Drawn by: Claude Design F&B pack, 24 August
- Client design-board frames: `FnB Board 4.dc.html#fnb-4j`
- Flow F29 *A table is seated, coursed and split*, step 3: Food is ordered with courses. → A kitchen ticket with `coursing` set from the outlet's default. **Starters fire; mains hold.**
- Flow F29 *A table is seated, coursed and split*, step 7: The server comps the delayed dish. → **A comp is not a discount.** Different budget, and a venue that cannot tell them apart cannot tell a generous manager from a leaking till.
- Flow F29 *A table is seated, coursed and split*, step 8: The table asks to split four ways. → Four bills. **Tax and service charge recompute per bill** — a split that apportions VAT by percentage produces bills that do not sum, and the difference is a fils somebody explains.
- Flow F29 *A table is seated, coursed and split*, step 9: Each guest pays their own. → The visit closes. **Stage `cleared` releases the table to the floor plan**, and the waitlist picks it up.
- Flow F80 *A table is configured, reserved, seated and billed*, step 1: Table Order, Bill & Payment Management. → **Drawn by the client as FNB-4J.** 1 operations on this step.
- Flow F29 branch at step 8 (low): when A guest moves from the bar and their drinks should follow., `transferOrderItems` moves lines between bills. **The kitchen is not re-fired** — food already made does not get made again because the bill moved.
- Flow F80 branch at step 1 (medium): when A step in the chain is not licensed for this tenant., **The chain stops at the module boundary.** `requiresModule` on each screen decides — a tenant without the retail licence does not see the retail half, and the journey is shorter rather than broken.
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (51), with its required mark, default, format and its error state (400, 402, 404, 409).
- [ ] Every output is drawn (5 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-059?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Close table visit, Create payment, Create F&B order, Split bill, Comp item, Transfer order items, Request bill.
- [ ] Every transition is wired: `EMP-058`, `KIT-002`.
- [ ] Every gated control is gated: `ORDER_CREATE`, `ORDER_MODIFY`, `ORDER_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 6 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-060` Reservation & Table Performance

**Reservation & Table Performance — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Floor Service · wave 2 · needs the `fnb` module |
| Block | Block C · task APP-STAFF-EMP-060 |
| Who uses it | venue staff holding `ORDER_MODIFY`, `ORDER_VIEW`, `REPORT_VIEW_VENUE` (2 operate, 1 read); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listTableReservations` reads the population and `getTableMap` reads one of them — list, select, act |
| Offline | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Opens with | `venueId` (session), `outletId` (EMP-003) · cold entry: **Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to. |
| Route | `/operations/reservation-table-performance` |

**What the spec says about it.** **Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Named in the board contents and not written up in it.**

**From the Food, Beverage & Retail process.** How the restaurant's bookings and tables performed, for the floor manager during and after a service: booked against seated covers, no-shows, parties that arrived smaller than booked, and how long tables turned. The one thing to get right: show only what the data can support. Today only the bookings and the live table map are read, so turn times and quoted-against-actual waits have no source yet.

**Known correction pending (do not draw the wrong version)**

- **No source for table performance (turn time, time per service stage, quoted against actual wait, revenue per cover).** Why: setServiceStage says the stage "is what makes a turn time real", and quoteWaitTime records quotes so the venue can compare them with actual waits, but no read returns these. A list of bookings is not a performance view. *(source: contracts/satellite/fnb.yaml#setServiceStage / contracts/satellite/fnb.yaml#quoteWaitTime / screens/P06-staff-app.yaml#EMP-060; Food, Beverage & Retail)*
- **The board frame fnb-4c is the same as EMP-053's.** Why: One frame cannot be the design of two screens. *(source: screens/P06-staff-app.yaml#EMP-060 / screens/P06-staff-app.yaml#EMP-053; Food, Beverage & Retail)*
- **"Outlet id" text field, a free date picker, the raw reservations table and detail panel, a "Confirm" button with no operation, and a read gated on ORDER_MODIFY.** Why: Plumbing on a user's screen, and a manager who only views is refused. *(source: screens/P06-staff-app.yaml#EMP-060 / contracts/satellite/fnb.yaml#listTableReservations; Food, Beverage & Retail)*

**Fixed on main** (the package already carries these; draw what it says): The exit to EMP-061 Retail Inventory Command Center (F80 step 3 to 4, F94 step 2 to 3), and the flow labels "drawn by the client as FNB-4B … (CHG-WIR-009).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which restaurant measures does the client want on the staff app (turn time, no-show rate, covers, wait accuracy), and are they computed by reporting or on the device?** → Turn time, no-show rate, covers and wait accuracy, all from reporting. *(decided by Chinmay, 2026-10-02; DEC-205 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Outlet id | picker: choose an outlet (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?outletId=` to `listTableReservations`. | `listTableReservations` ?outletId |
| Date | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?date=` to `listTableReservations`. | `listTableReservations` ?date |
| Search reservation | search field | — | — | — | — | — | — |

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

#### Outputs: what the screen shows and produces

**Shown**

**Turn time, no-shows, covers, wait accuracy** (metric tile, from `getKpiValues`): All four from reporting, never computed on the device (decided 2 October 2026, Chinmay, batch 6, EMP-060; DEC-205; CHG-CSA-020): `tableTurnTime`, `noShowRate`, `covers`, `waitQuoteAccuracy`, for this outlet and today.

| Shows | Format | Notes |
|---|---|---|
| Kpi | the name it points at, never the id | — |
| Code | text | — |
| Bucket start | 1 Oct 2026, 14:30 | The start of the bucket this value covers, when `getKpiValues` was asked for an `interval`; null otherwise. |
| Group key | text | The value of the `groupBy` dimension this row is for (a status, a category code, a tier); null when no `groupBy` was asked. |
| Name | text | — |
| Period | text | — |
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Target | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Variance percent | 1,234.5 | — |
| Direction | chip: Up, Down, Flat | — |
| Status | chip: Green, Amber, Red, No target | — |
| As of | 1 Oct 2026, 14:30 | — |
| Stale | yes / no (icon or chip) | True when the pipeline behind it has not refreshed. A number nobody flagged as stale is a number somebody will act on. |

**Every table reservation** (data table, from `listTableReservations`)

| Shows | Format | Notes |
|---|---|---|
| Guest name | text | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Duration minutes | 1,234 | How long the cover is held. An outlet turning tables twice an evening needs this to be real, or the second sitting cannot be booked. |
| Status | chip: Awaiting deposit, Booked, Confirmed, Seated, Completed, Cancelled… | `awaitingDeposit` only where the venue's dining deposit applies (decided 29 September, rev 3 REV3-8b); a booking with no deposit starts … |

**Card list** (card list): **Cards rather than a table.** One thumb, arm’s length, and a person who is walking.

**The selected table reservation** (detail panel, from `listTableReservations`)

| Shows | Format | Notes |
|---|---|---|
| Guest name | text | — |
| Contact point | text | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Duration minutes | 1,234 | How long the cover is held. An outlet turning tables twice an evening needs this to be real, or the second sitting cannot be booked. |
| Status | chip: Awaiting deposit, Booked, Confirmed, Seated, Completed, Cancelled… | `awaitingDeposit` only where the venue's dining deposit applies (decided 29 September, rev 3 REV3-8b); a booking with no deposit starts … |

**The table map** (detail panel, from `getTableMap`)

| Shows | Format | Notes |
|---|---|---|
| Outlet | the name it points at, never the id | — |
| Zones | list or chips (count when long) | — |
| Tables | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Bookings performance**: From the day's bookings: booked, seated, no-show and cancelled counts and covers, and covers lost to smaller arrivals (booked 6, arrived 4 is two covers the restaurant could have sold). Compared with the same weekday last week only if a source exists. *(source: contracts/satellite/fnb.yaml#listTableReservations / contracts/satellite/fnb.yaml#seatTableReservation)*
- **Tables now**: Occupancy by hall from the live map, in the floor-plan colours. *(source: contracts/satellite/fnb.yaml#getTableMap / DI-792)*
- **Restaurant measures**: Turn time, no-show rate, covers and wait accuracy, all from reporting (never computed on the device). *(source: decided 2 October 2026 by Chinmay (CHG-NOTE-004))*

**Data it reads**: `listTableReservations` (onLoad, Bookings for a service period); `getTableMap` (onLoad, Table map with live state); `getKpiValues` (onLoad, Turn time, no-show rate, covers and wait-quote accuracy …)

**Where the user goes next**

- → `EMP-061` Retail Inventory Command Center: *Retail Inventory Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reservation table performance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reservation table performance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reservation table performance yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on outletId, date and the reservation table performance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_MODIFY`, which `listTableReservations` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
service: Oasis Bistro dinner · Thu 15 Oct 2026
bookings:
  booked: 24
  seated: 19
  noShow: 3
  cancelled: 2
covers:
  booked: 92
  seated: 81
  lostToSmallerParties: 6
occupancyNow:
  mainHall: 78%
  terrace: 50%
  majlis: 100%
```

#### Permissions

- `listTableReservations` → `ORDER_MODIFY` (operate) · staff
- `getTableMap` → `ORDER_VIEW` (read) · staff
- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `ORDER_MODIFY`, which `listTableReservations` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.1.1 | The system should be able to allow table reservations view for the available tables in real-time, for the guests to choose/request. | F&B & Guest Management | CONTRACTED | `getTableMap` |

#### Client meeting inputs

None names this screen.

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A85** Design the table management module for fine dining: visual floor/table map with VIP tagging, table status flow (Available → Ordered → Table Closed → Reserved), reservations with deposit and waitlist, a per-table … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'table management')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-060` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/FnB Board 4.dc.html`
- Drawn by: Claude Design F&B pack, 24 August
- Client design-board frames: `FnB Board 4.dc.html#fnb-4c`
- Flow F80 *A table is configured, reserved, seated and billed*, step 3: Reservation & Table Performance. → **Drawn by the client as FNB-4C.** 2 operations on this step.
- Flow F94 *A restaurant floor is set up before service*, step 2: Reservation & Table Performance. → **Drawn by the client as FNB-4B.**

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (400, 404).
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-060?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm.
- [ ] Every transition is wired: `EMP-061`.
- [ ] Every gated control is gated: `ORDER_MODIFY`, `ORDER_VIEW`, `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
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

**19 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"addGuestNote": {"method":"POST","path":"/guests/{subjectId}/notes","contract":"marketing-crm","summary":"What the floor needs to know about this table","permission":"GUEST_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GuestNote"},
"closeTableVisit": {"method":"POST","path":"/table-visits/{visitId}/close","contract":"fnb","summary":"Settle and close a visit","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"compItem": {"method":"POST","path":"/table-visits/{visitId}/comp","contract":"fnb","summary":"Take a line off the bill, with a reason and a name","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TableVisit"},
"createFnbOrder": {"method":"POST","path":"/fnb-orders","contract":"fnb","summary":"Place an F&B order","permission":"ORDER_CREATE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateFnbOrderRequest","responds":"FnbOrder"},
"createPayment": {"method":"POST","path":"/payments","contract":"orders","summary":"Take a payment against an order","permission":"ORDER_CREATE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreatePaymentRequest","responds":"Payment"},
"createTableReservationForGuest": {"method":"POST","path":"/outlets/{outletId}/table-reservations","contract":"fnb","summary":"Book a table for a guest (staff)","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"TableReservation","responds":"TableReservation"},
"fireCourse": {"method":"POST","path":"/kitchen-tickets/{ticketId}/fire","contract":"fnb","summary":"Send a held course to the pass","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"KitchenTicket"},
"getBill": {"method":"GET","path":"/table-visits/{visitId}/bill","contract":"fnb","summary":"Bill for a visit","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Bill"},
"getFnbReservationPolicy": {"method":"GET","path":"/reservation-policy","contract":"fnb","summary":"How long a table is held, by party size","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"outletId","in":"query","required":false}],"requestBody":null,"responds":"FnbReservationPolicy"},
"getGuestProfile": {"method":"GET","path":"/guests/{subjectId}","contract":"marketing-crm","summary":"Read a guest profile","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GuestProfileDetail"},
"getKpiValues": {"method":"GET","path":"/kpi-values","contract":"reporting","summary":"Current values, against target, with movement","permission":"REPORT_VIEW_VENUE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"kpiIds","in":"query","required":null},{"name":"kpiCodes","in":"query","required":null},{"name":"scopePath","in":"query","required":null},{"name":"period","in":"query","required":null},{"name":"compareTo","in":"query","required":null},{"name":"interval","in":"query","required":null},{"name":"groupBy","in":"query","required":null},{"name":"module","in":"query","required":null}],"requestBody":null,"responds":"KpiValue"},
"getTableMap": {"method":"GET","path":"/outlets/{outletId}/tables","contract":"fnb","summary":"Table map with live state","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"TableMap"},
"getTableVisit": {"method":"GET","path":"/table-visits/{visitId}","contract":"fnb","summary":"Read a visit with all its orders","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"TableVisit"},
"holdCourse": {"method":"POST","path":"/kitchen-tickets/{ticketId}/hold","contract":"fnb","summary":"Stop a course going out","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"KitchenTicket"},
"joinRestaurantWaitlist": {"method":"POST","path":"/waitlist","contract":"fnb","summary":"Add a party to an outlet's waitlist","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RestaurantWaitlist","responds":"RestaurantWaitlist"},
"leaveRestaurantWaitlist": {"method":"POST","path":"/waitlist/{entryId}/leave","contract":"fnb","summary":"Take a party off an outlet's waitlist","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"RestaurantWaitlist"},
"listFnbOrders": {"method":"GET","path":"/fnb-orders","contract":"fnb","summary":"List F&B orders","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"outletId","in":"query","required":null},{"name":"tableVisitId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOrders": {"method":"GET","path":"/orders","contract":"orders","summary":"List orders","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"shiftId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"createdFrom","in":"query","required":null},{"name":"createdTo","in":"query","required":null},{"name":"workstationId","in":"query","required":null},{"name":"subjectId","in":"query","required":null},{"name":"tender","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTableReservations": {"method":"GET","path":"/table-reservations","contract":"fnb","summary":"Bookings for a service period","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"outletId","in":"query","required":null},{"name":"date","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"matchGuest": {"method":"POST","path":"/guests/match","contract":"marketing-crm","summary":"Is this the same person we already have?","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"mergeGuests": {"method":"POST","path":"/guests/merge","contract":"marketing-crm","summary":"Two records, one person","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MergeResult"},
"mergeTableVisits": {"method":"POST","path":"/table-visits/{visitId}/merge","contract":"fnb","summary":"Merge another visit into this one","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TableVisit"},
"moveTableVisit": {"method":"POST","path":"/table-visits/{visitId}/move","contract":"fnb","summary":"Move a party to a different table, mid-service","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TableVisit"},
"notifyWaitlistParty": {"method":"POST","path":"/waitlist/{entryId}/notify","contract":"fnb","summary":"Their table is ready","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"RestaurantWaitlist"},
"openTableVisit": {"method":"POST","path":"/table-visits","contract":"fnb","summary":"Seat a party and open a visit","permission":"ORDER_CREATE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"OpenTableVisitRequest","responds":"TableVisit"},
"quoteWaitTime": {"method":"POST","path":"/waitlist/{entryId}/quote","contract":"fnb","summary":"Tell a party how long, and mean it","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"reassignServer": {"method":"PUT","path":"/table-visits/{visitId}/server","contract":"fnb","summary":"Hand a table to another server","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TableVisit"},
"requestBill": {"method":"POST","path":"/table-visits/{visitId}/request-bill","contract":"fnb","summary":"The party asked to pay","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TableVisit"},
"resolveBookingConflict": {"method":"GET","path":"/table-reservations/conflicts","contract":"fnb","summary":"Two bookings, one table — and what to do about it","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"date","in":"query","required":null},{"name":"outletId","in":"query","required":null}],"requestBody":null,"responds":null},
"seatTableReservation": {"method":"POST","path":"/table-reservations/{reservationId}/seat","contract":"fnb","summary":"The party arrived and has been sat down","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TableReservation"},
"sendBookingConfirmation": {"method":"POST","path":"/table-reservations/{reservationId}/confirm","contract":"fnb","summary":"Confirm a booking, and ask them to confirm back","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"setSectionLayout": {"method":"PUT","path":"/outlets/{outletId}/sections","contract":"fnb","summary":"Divide the floor into sections and give each a server","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"SectionLayout","responds":"SectionLayout"},
"setServiceStage": {"method":"PUT","path":"/table-visits/{visitId}/stage","contract":"fnb","summary":"Where this table is in its meal","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TableVisit"},
"setTableCombinations": {"method":"PUT","path":"/outlets/{outletId}/table-combinations","contract":"fnb","summary":"Which tables can be pushed together, and to what capacity","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"setTableLayout": {"method":"PUT","path":"/outlets/{outletId}/tables","contract":"fnb","summary":"Configure the table layout","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TableMap"},
"splitBill": {"method":"POST","path":"/table-visits/{visitId}/bill/split","contract":"fnb","summary":"Split a bill","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SplitBillRequest","responds":"BillSplit"},
"transferOrderItems": {"method":"POST","path":"/table-visits/{visitId}/transfer-items","contract":"fnb","summary":"Move items to another table's bill","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TableVisit"},
"transferTableVisit": {"method":"POST","path":"/table-visits/{visitId}/transfer","contract":"fnb","summary":"Move a check to another server","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TableVisit"},
"updateTableVisit": {"method":"PATCH","path":"/table-visits/{visitId}","contract":"fnb","summary":"Amend covers, move table, or reassign server","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TableVisit"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AllergenCode": {"type":"string","description":"**The fourteen declarable allergens, as one closed list.** Every allergen field in this contract uses it — the menu claim, the ticket line, a substitution's delta, a modifier option, the label on a bag — so a declared set and an actual set compare without anybody normalising case or synonyms. It was the `Allergen.contains` enum; the other fields were free text.\n","enum":["gluten","crustaceans","eggs","fish","peanuts","soybeans","milk","nuts","celery","mustard","sesame","sulphites","lupin","molluscs"]},
"Bill": {"x-ticvai-persistence":"none — computed from visit orders","type":"object","required":["visitId","lines","subtotal","taxAmount","total"],"properties":{"visitId":{"type":"string"},"covers":{"type":"integer"},"lines":{"type":"array","items":{"type":"object","required":["lineId","name","quantity","lineTotal"],"properties":{"lineId":{"type":"string"},"orderId":{"type":"string"},"name":{"type":"string"},"quantity":{"type":"integer"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lineTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"categoryCode":{"type":"string","nullable":true},"seatNumber":{"type":"integer","nullable":true}}}},"subtotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"serviceCharge":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"discountAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"total":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},
"BillSplit": {"x-ticvai-persistence":"fnb.bill_split + fnb.sub_bill","type":"object","required":["visitId","method","subBills"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"visitId":{"type":"string"},"method":{"$ref":"#/components/schemas/SplitMethod"},"subBills":{"type":"array","items":{"type":"object","required":["subBillId","total","status"],"properties":{"subBillId":{"type":"string"},"lineIds":{"type":"array","items":{"type":"string"}},"subtotal":{"x-ticvai-column":"net_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"total":{"x-ticvai-column":"gross_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["unpaid","paid"]}}}}}},
"ConsentDecision": {"type":"string","enum":["granted","withdrawn","notAsked"]},
"ConsentPurpose": {"type":"string","enum":["marketing","personalisation","profiling","thirdPartySharing","aiProcessing","transactional"]},
"ConsentState": {"x-ticvai-persistence":"none — projection over consent_record","type":"object","required":["subjectId","purposes"],"properties":{"subjectId":{"type":"string","format":"uuid"},"purposes":{"type":"array","items":{"type":"object","required":["purpose","decision","requiresRenewal"],"properties":{"purpose":{"$ref":"#/components/schemas/ConsentPurpose"},"decision":{"$ref":"#/components/schemas/ConsentDecision"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/MessageChannel"}},"noticeVersion":{"type":"string","nullable":true},"requiresRenewal":{"type":"boolean","description":"True where the notice has been superseded since consent was given."},"decidedAt":{"type":"string","format":"date-time","nullable":true}}}}}},
"CoursingPolicy": {"type":"string","description":"How a ticket's courses are fired. `fireAndForget` sends every course at once, which is no coursing; `holdAndFire` waits for a server to call each course; `timed` fires on a clock; `phased` staggers by course. **One vocabulary for the ticket (`KitchenTicket.coursing`) and the outlet default (`CourseRules.defaultCoursing`)** — the default said `none` for `fireAndForget` and had no `delayed` until 26 September, so a default could not be copied onto the field it defaults.\n","enum":["fireAndForget","holdAndFire","phased","timed","delayed"]},
"CreateFnbOrderLine": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","menuItemId","quantity"],"properties":{"id":{"type":"string","format":"uuid"},"menuItemId":{"type":"string","format":"uuid"},"quantity":{"type":"integer","minimum":1},"modifierOptionIds":{"type":"array","items":{"type":"string","format":"uuid"}},"note":{"type":"string","maxLength":200,"description":"Free text to the kitchen. Allergy notes belong here and are surfaced prominently."},"seatNumber":{"type":"integer","nullable":true,"description":"Which cover ordered it. Drives split-by-covers accurately."},"course":{"type":"integer","nullable":true,"description":"Course grouping, so the kitchen fires in sequence."},"redeemEntitlementId":{"type":"string","nullable":true,"x-ticvai-references":"access.entitlement","description":"**A meal combo redeemed at the till or by a scan** (29 September, MOB-4; applied 30 September). The entitlement a bundle's `fnbMenuItem` component issued (promotions `BundleComponent.componentKind: fnbMenuItem`, `menuItemId`, `redeemAtOutletIds`). The line is priced at zero against it, `menuItemId` must be the component's menu item and the outlet one of `redeemAtOutletIds` (or any outlet with the item on a live menu when that list is empty), and the entitlement is marked used in the same step through access `validateAccess` at the outlet. An entitlement already used, for another item or outlet, or not yet valid is refused 409 `entitlementNotRedeemable`; a till that is offline queues the redemption like any sale and the replay is refused the same way if it was used meanwhile."}}},
"CreateFnbOrderRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","outletId","serviceMode","lines","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"outletId":{"type":"string","format":"uuid"},"serviceMode":{"$ref":"#/components/schemas/ServiceMode"},"tableVisitId":{"type":"string","format":"uuid","nullable":true,"description":"Required for table service. Absent for quick service."},"lines":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/CreateFnbOrderLine"}},"salesOrderId":{"type":"string","format":"uuid","nullable":true,"description":"The `orders.sales_order` this F&B order fulfils (SD-046, 29 September). A POS sale sends the order it took payment on; the commercial order is the sales order and this is its fulfilment."},"recordedAt":{"type":"string","format":"date-time"}}},
"CreatePaymentRequest": {"type":"object","required":["id","orderId","tender","amount","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of the payment, and its idempotency key — it must equal the `Idempotency-Key` header."},"orderId":{"type":"string","format":"uuid"},"tender":{"$ref":"#/components/schemas/TenderKind"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"description":"The currency the guest handed over, where it is not the venue's — becomes `Payment.tenderCurrency`. Omit for a payment in the venue's own currency. For a guest-channel card or wallet payment on an order with a `chargeCurrency`, the server sets it from the order (CHG-FIN-001)."},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"**What the guest handed over**, in `tenderCurrency` — becomes `Payment.tenderAmount`, one name for one concept (renamed from `tenderedAmount` on 26 September). For cash, change is the difference.\n"},"walletAuthorisationId":{"type":"string","nullable":true,"description":"Cross-cell wallet hold, where the guest's home cell is elsewhere."},"walletHoldId":{"type":"string","format":"uuid","nullable":true,"description":"For a `wallet` tender, the hold `wallet.holdWalletFunds` placed (SD-027). Capture debits it; the order service writes no wallet table."},"returnUrl":{"type":"string","format":"uri","nullable":true,"description":"Where the provider returns the guest after a 3-D Secure challenge or hosted page (SD-034). Required for a card payment from the guest web or app."},"terminalId":{"type":"string","format":"uuid","nullable":true,"description":"The card terminal to instruct, for a card payment at a till (ECR flow, SD-034)."},"deviceId":{"type":"string","format":"uuid","nullable":true},"recordedAt":{"type":"string","format":"date-time"}}},
"ExchangeRateDecimal": {"type":"string","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,6)","description":"**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one — a JavaScript client must not round a rate in transit. **Six decimal places**, the precision `finance.FxRate.rate` asks for, and stored at that precision.\n","pattern":"^\\d+(\\.\\d{1,6})?$"},
"FnbOrder": {"x-ticvai-persistence":"fnb.service_order + fnb.service_order_line","type":"object","required":["id","orderNumber","outletId","serviceMode","status","lines","grossAmount","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderNumber":{"type":"string"},"outletId":{"type":"string","format":"uuid"},"paymentTiming":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/OutletPaymentTiming"}],"readOnly":true,"description":"The outlet's payment timing when the order was placed (CHG-CSA-010), kept as a snapshot."},"sentToKitchenAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When the order's kitchen tickets were created. Null on a `payFirst` order not yet paid (CHG-CSA-010)."},"serviceMode":{"$ref":"#/components/schemas/ServiceMode"},"tableVisitId":{"type":"string","format":"uuid","nullable":true},"status":{"$ref":"#/components/schemas/FnbOrderStatus"},"lines":{"type":"array","items":{"allOf":[{"$ref":"#/components/schemas/CreateFnbOrderLine"},{"type":"object","properties":{"status":{"$ref":"#/components/schemas/FnbOrderStatus"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lineTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}]}},"salesOrderId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"orders.sales_order","description":"**Retyped 29 September (SD-046)**, and `format: uuid` since ADR-0056 (30 September): every id is a uuid, so this joins `orders.sales_order.id`. **Taken from their `fnb.order`, 20 September.** We carried outlet, table visit and kitchen ticket on an F&B order and nothing joining it to what was actually sold, so an F&B line could not be reconciled to the order that paid for it.\n"},"updatedAt":{"type":"string","format":"date-time","nullable":true,"description":"Taken from their `fnb.order`. Ours had `recordedAt` and `syncedAt`, which are both offline-sync fields, and no plain updated timestamp.\n"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"kitchenTicketId":{"type":"string","format":"uuid","nullable":true},"kitchenTickets":{"type":"array","readOnly":true,"x-ticvai-persisted":false,"description":"The kitchen tickets this order created, one per station (SD-046). Returned, not stored here; they are `fnb.kitchen_ticket` rows.","items":{"$ref":"#/components/schemas/KitchenTicket"}},"estimatedReadyAt":{"type":"string","format":"date-time","nullable":true},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"FnbOrderStatus": {"type":"string","description":"The full lifecycle from 4.6.35. Nine states, not six — the earlier enum collapsed `accepted` into `placed` and had no `collected` or `delivered` at all, which made collection and delivery indistinguishable from a server putting a plate down.\n`accepted` matters because an outlet may refuse: past last orders, out of a key ingredient, or simply too far behind. A guest whose order sat in `placed` for ten minutes and was then rejected has a worse experience than one refused immediately.\n","enum":["ordered","accepted","inPreparation","ready","served","collected","delivered","cancelled","refunded"]},
"FnbReservationPolicy": {"type":"object","x-ticvai-persistence":"fnb.reservation_policy","description":"**How long a table is held, and what sits between one seating and the next.** The source of `TableReservation.durationMinutes`, which keeps its own value as the snapshot.","required":["defaultTurnMinutes","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"outletId":{"type":"string","format":"uuid","nullable":true,"description":"Null is the venue default; an outlet's own policy overrides it."},"defaultTurnMinutes":{"type":"integer","minimum":15,"description":"The turn time when no party-size band matches."},"turnTimeBands":{"type":"array","description":"**Turn time by party size** — a two-top and a table of eight do not turn at the same speed, and a single default is how a restaurant ends up double-booking its large tables. The first band whose range contains the party size wins.","items":{"type":"object","required":["fromPartySize","turnMinutes"],"properties":{"fromPartySize":{"type":"integer","minimum":1},"toPartySize":{"type":"integer","nullable":true,"description":"Null means no upper bound."},"turnMinutes":{"type":"integer","minimum":15}}}},"seatingBufferMinutes":{"type":"integer","minimum":0,"default":0,"description":"**The reset between seatings** — clearing, laying and a moment for the floor. Zero is a legitimate answer and a stated one."},"maximumDurationMinutes":{"type":"integer","nullable":true,"description":"**The ceiling on a single booking.** A reservation extended by hand past this needs the manager, because the table after it is somebody else's booking."},"reservedLeadMinutes":{"type":"integer","minimum":0,"nullable":true,"description":"**When a table shows Reserved** (Chinmay, 2 October, workbook Q202; DI-689; CHG-CSA-012). **The canonical setting** (CHG-CLN-009): tenancy `VenueSettings.fnb.tableReservedLeadMinutes` is deprecated in its favour. A table shows Reserved when a booking names it; with this set, it also shows Reserved this many minutes before a booking pre-allocated to it starts. Null, the default, means only a named table shows Reserved and other arrivals show in the next-arrivals strip. Set by the venue, per outlet where the outlet has its own policy."},"isActive":{"type":"boolean"},"scopePath":{"type":"string"}}},
"FnbReservationTable": {"type":"object","x-ticvai-persistence":"fnb.reservation_table","description":"**Taken from the backend workbook, 20 September.** Maps one or more dining tables assigned to a reservation.","required":["reservationId","tableId","createdAt"],"properties":{"reservationId":{"type":"string","format":"uuid"},"tableId":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"}}},
"GuestNote": {"type":"object","x-ticvai-persistence":"marketing.guest_note","description":"A note on a guest, written by staff (`addGuestNote`). **Attributed and personal data**, and `isAllergy` keeps an allergy apart from every other kind so it surfaces on the order screen.\n","required":["id","subjectId","kind","text","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["allergy","dietary","seatingPreference","occasion","serviceRecovery","vip","general"]},"text":{"type":"string"},"isAllergy":{"type":"boolean","default":false},"visibleToServer":{"type":"boolean","default":true},"authorPrincipalId":{"type":"string","format":"uuid","readOnly":true},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","readOnly":true}}},
"GuestProfile": {"x-ticvai-persistence":"marketing.guest_profile","type":"object","required":["subjectId","isActive"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"subjectId":{"type":"string","format":"uuid","description":"Opaque reference. Personal data lives in the separately erasable store, which is what makes erasure possible against an append-only ledger.\n"},"displayName":{"type":"string","nullable":true},"email":{"type":"string","nullable":true},"phone":{"type":"string","nullable":true},"preferredLanguage":{"type":"string","nullable":true},"preferredChannel":{"$ref":"#/components/schemas/MessageChannel"},"guestLinkId":{"type":"string","nullable":true,"description":"Present where the guest is linked across cells. Marketing acts locally."},"tags":{"type":"array","items":{"type":"string"}},"engagementScore":{"type":"integer","nullable":true,"minimum":0,"maximum":100,"description":"22.2.20 and 22.2.21. **`lifetimeValue` and `visitCount` existed, so value was a stored figure and engagement was not.** They are different questions: a guest who spent a lot once and a guest who visits monthly have the same LTV and need opposite treatment.\n**Recency, frequency and breadth, not spend** — spend is already `lifetimeValue`, and folding it in here would make one number twice.\n"},"engagementTier":{"type":"string","nullable":true,"enum":["new","active","occasional","lapsing","lapsed","dormant"],"description":"5.3.19. **Automatic classification, computed rather than assigned.** `lapsing` is the tier the whole field exists for — **a guest who has not been for a while and still might is the only one marketing can change**, and lumping them with `lapsed` wastes the window.\n"},"lifetimeValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"visitCount":{"type":"integer"},"lastVisitAt":{"type":"string","format":"date-time","nullable":true},"isActive":{"type":"boolean"},"mergedIntoSubjectId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Set on the absorbed profile by `mergeGuestProfiles` and `mergeGuests`**, which retain it as a redirect rather than deleting it. A read that lands here follows it; a second merge of a profile that has one is refused as `alreadyMerged`.\n"},"mergedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"GuestProfileDetail": {"x-ticvai-persistence":"marketing.guest_profile","allOf":[{"$ref":"#/components/schemas/GuestProfile"},{"type":"object","properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"consents":{"$ref":"#/components/schemas/ConsentState"},"loyalty":{"$ref":"#/components/schemas/LoyaltyPosition"},"openCaseCount":{"type":"integer"},"recentOrderIds":{"type":"array","items":{"type":"string"}},"membershipIds":{"type":"array","items":{"type":"string","format":"uuid"}},"notes":{"type":"string","nullable":true}}}]},
"KitchenTicket": {"x-ticvai-persistence":"fnb.kitchen_ticket + fnb.kitchen_ticket_line","type":"object","required":["id","orderId","outletId","status","lines","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid","description":"The F&B order the ticket was created from on acceptance (`FnbOrder.id`)."},"orderNumber":{"type":"string"},"outletId":{"type":"string","format":"uuid"},"tableLabel":{"type":"string","nullable":true},"serviceMode":{"$ref":"#/components/schemas/ServiceMode"},"coursing":{"allOf":[{"$ref":"#/components/schemas/CoursingPolicy"}],"nullable":true,"description":"BL-131. **Starters before mains is the entire job of a kitchen pass**, and the model fired everything at once.\n`holdAndFire` waits for a server to call it; `timed` fires on a clock; `phased` staggers by course. **Without this a table gets its dessert while eating its starter.**\n"},"buzzerCode":{"type":"string","nullable":true,"description":"BL-128. **The pager number handed to a guest at a counter.** Recorded against the order so a lost buzzer is a lookup rather than an argument.\n"},"status":{"$ref":"#/components/schemas/KitchenTicketStatus"},"priority":{"type":"integer","description":"Higher fires sooner. Raised by Fast Pass or supervisor override."},"prioritisedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"prioritiseReason":{"type":"string","nullable":true},"lines":{"type":"array","items":{"type":"object","required":["lineId","name","quantity","status"],"properties":{"lineId":{"type":"string","format":"uuid"},"name":{"type":"string"},"quantity":{"type":"integer"},"modifiers":{"type":"array","items":{"type":"string"}},"note":{"type":"string","nullable":true},"allergens":{"type":"array","items":{"$ref":"#/components/schemas/AllergenCode"}},"refireOfLineId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Set on a refire.** The line it remakes, which stays — food cost counts both, the bill counts one (`refireItem`)."},"refireReason":{"allOf":[{"$ref":"#/components/schemas/RefireReason"}],"nullable":true,"readOnly":true},"isChargeable":{"type":"boolean","nullable":true,"readOnly":true,"description":"A refire's `chargeable` flag. Null on a line that is not a refire."},"course":{"type":"integer","nullable":true},"stationId":{"type":"string","format":"uuid","nullable":true},"status":{"$ref":"#/components/schemas/KitchenTicketStatus"}}}},"createdAt":{"type":"string","format":"date-time"},"targetReadyAt":{"type":"string","format":"date-time","nullable":true},"elapsedSeconds":{"type":"integer"}}},
"KitchenTicketStatus": {"type":"string","enum":["received","preparing","ready","served","recalled","cancelled"]},
"KpiValue": {"type":"object","description":"BI board 10.3. **Value, target, variance, direction and freshness in one read.**","properties":{"kpiId":{"type":"string","format":"uuid"},"code":{"type":"string"},"bucketStart":{"type":"string","format":"date-time","nullable":true,"description":"The start of the bucket this value covers, when `getKpiValues` was asked for an `interval`; null otherwise."},"groupKey":{"type":"string","nullable":true,"description":"The value of the `groupBy` dimension this row is for (a status, a category code, a tier); null when no `groupBy` was asked."},"name":{"type":"string"},"scopePath":{"type":"string"},"period":{"type":"string"},"value":{"$ref":"#/components/schemas/MetricValue"},"target":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"comparison":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"variancePercent":{"type":"number","nullable":true},"direction":{"type":"string","enum":["up","down","flat"]},"status":{"type":"string","enum":["green","amber","red","noTarget"]},"asOf":{"type":"string","format":"date-time"},"stale":{"type":"boolean","description":"**True when the pipeline behind it has not refreshed.** A number nobody flagged as stale is a number somebody will act on.\n"}}},
"LoyaltyPosition": {"x-ticvai-persistence":"marketing.loyalty_position","type":"object","required":["subjectId","programmeId","pointsBalance","tierCode"],"properties":{"leaderboardNickname":{"type":"string","nullable":true,"maxLength":24,"description":"BL-173. **The name shown on a leaderboard, chosen by the guest.** Offered whenever they reach the board and changeable afterwards; `setLeaderboardNickname` is the only thing that writes it.\n**Null means the guest has not chosen one yet, and the board shows a generated `Player-4821` in its place** — never `pii.subject.display_name`, which would disclose silently on the day a guest first placed and is the case this field exists to prevent.\n**The generated name is computed at read time and not stored here.** Writing it would make *\"has this guest chosen a name\"* unanswerable, and that flag is what the prompt-on-reaching-the-board depends on.\n"},"subjectId":{"type":"string","format":"uuid"},"programmeId":{"type":"string","format":"uuid"},"pointsBalance":{"type":"integer"},"lifetimePoints":{"type":"integer"},"tierId":{"type":"string","format":"uuid","nullable":true,"description":"**The tier this row's `tierCode` and `tierName` are a copy of.** Added 20 September with `marketing.programme_tier`: the two strings were a cache of something that did not exist, and a cache with no source cannot be rebuilt or audited.\n"},"tierCode":{"type":"string"},"tierName":{"type":"string"},"pointsToNextTier":{"type":"integer","nullable":true},"nextExpiryPoints":{"type":"integer","nullable":true},"nextExpiryAt":{"type":"string","format":"date-time","nullable":true}}},
"MergeResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["survivingSubjectId","absorbedSubjectId","transferred"],"properties":{"survivingSubjectId":{"type":"string","format":"uuid"},"absorbedSubjectId":{"type":"string","format":"uuid"},"transferred":{"type":"object","properties":{"orders":{"type":"integer"},"cases":{"type":"integer"},"loyaltyPoints":{"type":"integer","description":"The total points moved across every programme. The per-programme outcome is `loyaltyProgrammes`."}}},"loyaltyProgrammes":{"type":"array","description":"**One entry per loyalty programme either record belonged to (decided 28 September, audit R149).** Points are added and the higher tier is kept, per programme — a single points number cannot say which programme it belongs to.\n","items":{"type":"object","required":["programmeId","pointsAdded","resultingPoints"],"properties":{"programmeId":{"type":"string","format":"uuid"},"pointsAdded":{"type":"integer","description":"The absorbed record's balance in this programme, added to the survivor's."},"resultingPoints":{"type":"integer"},"tierKept":{"type":"string","nullable":true,"description":"The higher of the two records' tiers in this programme."}}}},"consentOutcome":{"type":"array","description":"Per purpose, the resulting position. Where the two profiles disagreed, the more restrictive position won.\n","items":{"type":"object","properties":{"purpose":{"$ref":"#/components/schemas/ConsentPurpose"},"result":{"$ref":"#/components/schemas/ConsentDecision"},"wasRestricted":{"type":"boolean"}}}}}},
"MetricValue": {"x-ticvai-persistence-column":"numeric(18,4)","description":"**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n","oneOf":[{"type":"number"},{"$ref":"../shared/common.yaml#/components/schemas/Money"}]},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"OpenTableVisitRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","tableId","covers","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"tableId":{"type":"string","format":"uuid"},"covers":{"type":"integer","minimum":1,"description":"Captured at seating because it drives split-by-covers at close."},"serverPrincipalId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid"},"recordedAt":{"type":"string","format":"date-time"}}},
"OrderChannel": {"type":"string","description":"Where the order originated. Added when guest self-ordering was contracted — an order a guest placed on their own phone is commercially and operationally different from one a cashier typed, and reporting that cannot separate them cannot answer whether self-ordering is working.\n","enum":["pos","kiosk","guestApp","guestWeb","callCentre","partner","api","backOffice"]},
"OrderStatus": {"type":"string","enum":["pending","held","paid","partiallyPaid","completed","voided","refunded","partiallyRefunded","failed"],"description":"`held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed.\n"},
"OrderSummary": {"x-ticvai-persistence":"none — projection","type":"object","required":["id","orderNumber","status","grossAmount","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderNumber":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"The same vocabulary as `Order.channel`, which this projects."},"lineCount":{"type":"integer"},"principalId":{"type":"string","format":"uuid","description":"The cashier who raised it — what the held-orders list shows."},"holdLabel":{"type":"string","nullable":true,"description":"As `Order.holdLabel`."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"description":"As `Order.heldUntil`, so a held-orders list can warn about the ones about to lapse."},"createdAt":{"type":"string","format":"date-time"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Payment": {"x-ticvai-persistence":"orders.payment","type":"object","required":["id","orderId","tender","amount","status","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid"},"tender":{"$ref":"#/components/schemas/TenderKind"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","description":"4.6.11. **What the guest actually handed over**, which is not always what the venue books. A tourist paying USD cash at a till is a foreign tender; the sale is still recorded in base currency.\nEqual to the base currency for almost every payment. **Present on all of them so the foreign-tender report has a source** — `getForeignTenderReport` promised *what was taken in which currency* and nothing recorded it until 18 August.\n"},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"The amount in `tenderCurrency`, at that currency's own scale."},"fxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"description":"The rate applied, **stored on the payment rather than looked up later** (CF-37). A payment reconciled next month is reconciled at the rate of the day it was taken.\n"},"fxRateSource":{"type":"string","nullable":true,"enum":["manual","feed","cardScheme"],"description":"4.2.8. Manual or fed on a schedule. **`cardScheme` is where the terminal did the conversion and told us** — dynamic currency conversion, the scheme's rate rather than ours.\n"},"changeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"description":"4.6.11 is deliberately asymmetric: **accept foreign currency, refund in local.** A till giving change in five currencies needs five floats and five counts, and the variance becomes unattributable.\n**Cash at a till only** (CHG-FIN-001, 2 October 2026). A card or wallet payment the guest made in a currency they selected is refunded in that currency (`Refund.tenderCurrency`).\n"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"changeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["authorised","captured","pendingConfirmation","declined","failed","voided","refunded"]},"providerName":{"type":"string","nullable":true},"providerReference":{"type":"string","nullable":true,"description":"The provider's own id for the charge (Stripe PaymentIntent, NI order reference). What `payments.receivePaymentProviderWebhook` matches an incoming event on (SD-034)."},"providerIdempotencyKey":{"type":"string","nullable":true,"readOnly":true,"description":"The idempotency key sent to the provider, which is this payment's `id` (SD-034, 29 September). A retried provider call cannot charge twice."},"terminalId":{"type":"string","format":"uuid","nullable":true,"description":"The card terminal a till payment ran on (ECR flow, SD-034)."},"nextAction":{"type":"object","nullable":true,"x-ticvai-persisted":false,"description":"**What the caller does while the payment is `pendingConfirmation`** (SD-034, 29 September). `redirect`: send the browser to `url` (3-D Secure challenge or hosted page); the provider returns the guest to `returnUrl` and the result arrives by webhook. `terminal`: the card terminal has been instructed; wait for its result. Null once the payment has an outcome.","properties":{"kind":{"type":"string","enum":["redirect","terminal"]},"url":{"type":"string","format":"uri","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true}}},"lastInquiryAt":{"type":"string","format":"date-time","nullable":true},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"RefireReason": {"type":"string","description":"Why a line was made again (`refireItem`). The reasons are the data.","enum":["overcooked","undercooked","wrongItem","dropped","cold","allergyRisk","guestChangedMind","lateAdd"]},
"RestaurantWaitlist": {"type":"object","x-ticvai-persistence":"fnb.waitlist_entry","description":"BL-130. **Distinct from `queue`, which is for rides.** A restaurant waitlist has a party size, a table preference and a walk-away point, and a guest who leaves is not the same as a guest who was served.\n","required":["id","outletId","partySize","status","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"outletId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true},"partySize":{"type":"integer"},"quotedWaitMinutes":{"type":"integer","nullable":true},"seatingPreference":{"type":"string","enum":["any","indoor","outdoor","bar","booth","highChair"],"nullable":true},"status":{"type":"string","enum":["waiting","notified","seated","walkedAway","noShow","cancelled"]},"notifiedAt":{"type":"string","format":"date-time","nullable":true},"recordedAt":{"type":"string","format":"date-time","description":"**When the party joined, on the device.** The wait a party had is measured from here to `notifiedAt` or to seating, which is the report `walkedAway` exists for. Required on a join — the operation is offline-capable."},"syncedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"holdExpiresAt":{"type":"string","format":"date-time","nullable":true,"description":"**How long a table waits for somebody who was called.** Too short and a guest returning from the bathroom loses it; too long and the table sits empty at peak — which is why it is a setting rather than a constant.\n"}}},
"SectionLayout": {"type":"object","description":"An outlet's floor divided into sections, each with its server (`setSectionLayout`).","required":["sections"],"properties":{"sections":{"type":"array","items":{"type":"object","required":["name","tableIds"],"properties":{"name":{"type":"string"},"tableIds":{"type":"array","items":{"type":"string","format":"uuid"}},"serverPrincipalId":{"type":"string","format":"uuid","nullable":true},"servicePeriod":{"type":"string","nullable":true}}}}}},
"ServiceMode": {"type":"string","enum":["quickService","tableService","roomService","collection","delivery"]},
"SplitBillRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["method","recordedAt"],"properties":{"recordedAt":{"type":"string","format":"date-time","description":"Device time of the split (offline-capable)."},"method":{"$ref":"#/components/schemas/SplitMethod"},"parts":{"type":"integer","minimum":2,"description":"For `byCovers` — defaults to the visit's cover count."},"amounts":{"type":"array","description":"For `byAmount`. Must sum to the bill total.","items":{"$ref":"../shared/common.yaml#/components/schemas/Money"}},"lineAssignments":{"type":"array","description":"For `byLine` or `bySeat`. Every line must be assigned exactly once.","items":{"type":"object","required":["lineId","partIndex"],"properties":{"lineId":{"type":"string"},"partIndex":{"type":"integer","minimum":0}}}},"categoryAssignments":{"type":"array","description":"For `byCategory` — food to one part, beverage to another.","items":{"type":"object","required":["categoryCode","partIndex"],"properties":{"categoryCode":{"type":"string"},"partIndex":{"type":"integer","minimum":0}}}}}},
"SplitMethod": {"type":"string","enum":["byAmount","byCovers","byCategory","byLine","bySeat"]},
"TableCombination": {"type":"object","x-ticvai-persistence":"fnb.table_combination","description":"**Tables that can be pushed together, and what they seat together.** Declared by a host rather than inferred from a floor plan — a pillar, a step or a service run stops two adjacent tables combining. `setTableCombinations` writes the outlet's set.\n","required":["tableIds","combinedCovers"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"outletId":{"type":"string","format":"uuid","readOnly":true,"description":"The outlet in the path."},"tableIds":{"type":"array","minItems":2,"items":{"type":"string","format":"uuid"}},"combinedCovers":{"type":"integer","minimum":1},"setupMinutes":{"type":"integer","default":5},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `outlet` scope."}}},
"TableDefinition": {"x-ticvai-persistence":"fnb.dining_table","type":"object","description":"A restaurant (dining) table, reserved with `createTableReservation`. Not a map-bookable `resources` table, which is a non-dining spot sold like a cabana (decided 29 September, rev 3 GAP-C2).","required":["id","label","capacity"],"properties":{"id":{"type":"string","format":"uuid"},"label":{"type":"string","maxLength":32,"x-ticvai-unique":"venue","description":"**The table code, unique per venue** (decided 28 September, audit R108). Two tables in one venue never share a label, across all its outlets, so *T12* names one table wherever it is read. `createTable` and `updateTable` refuse a duplicate with `409` `duplicate-code`.\n"},"capacity":{"type":"integer","minimum":1},"zone":{"type":"string","nullable":true},"position":{"type":"object","properties":{"x":{"type":"number"},"y":{"type":"number"}}},"shape":{"type":"string","enum":["round","square","rectangle","booth","bar"]},"isOutOfService":{"type":"boolean","default":false,"description":"**Damaged, or its section closed.** `getTableMap` shows it as `outOfService` and a claim on it is refused with `tableOutOfService`."}}},
"TableMap": {"x-ticvai-persistence":"none — projection","type":"object","required":["outletId","tables"],"properties":{"outletId":{"type":"string","format":"uuid"},"zones":{"type":"array","items":{"type":"string"}},"tables":{"type":"array","items":{"$ref":"#/components/schemas/TableState"}}}},
"TableReservation": {"type":"object","x-ticvai-persistence":"fnb.table_reservation","x-ticvai-retired-columns":["table_ids"],"required":["outletId","startsAt","partySize"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"outletId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true},"guestName":{"type":"string"},"contactPoint":{"type":"string"},"partySize":{"type":"integer","minimum":1},"startsAt":{"type":"string","format":"date-time"},"durationMinutes":{"type":"integer","description":"**How long the cover is held.** An outlet turning tables twice an evening needs this to be real, or the second sitting cannot be booked.\n"},"tables":{"type":"array","description":"The dining tables assigned to this reservation, one row each.\n**Usually empty until seating.** Committing a specific table at booking time refuses later bookings against a constraint that did not need to exist — that was true of the `tableIds` array this replaces and it is still true, because it is about *when* a table is assigned rather than how the assignment is stored.\n**Replaces `tableIds`, retired 20 September.** An array cannot carry per-row state, which is the same reason this merge took `entry_rule_point`, `menu_item_modifier`, `seat_block_item`, `plan_benefit`, `payment_method_config` and `tier_module` from the backend workbook. A party seated across three tables that releases one early has nowhere to say so in an array, and *\"which reservations are on table 7 tonight\"* is a GIN scan over every reservation instead of an index seek.\n","items":{"$ref":"#/components/schemas/FnbReservationTable"}},"status":{"$ref":"#/components/schemas/TableReservationStatus"},"groupId":{"type":"string","format":"uuid","nullable":true,"description":"5.1.2. Several bookings managed as one party across adjacent tables."},"notes":{"type":"string","description":"Allergies, accessibility needs and other requests, as the guest wrote them."},"seatingPreference":{"type":"string","maxLength":64,"nullable":true,"description":"**The seating area the guest asked for**, e.g. indoor, terrace, majlis (Chinmay, 2 October, workbook Q204; DI-791; CHG-CSA-018). The outlet's own area names, as the waitlist's `RestaurantWaitlist.seatingPreference` takes them. A preference, not a table: the host seats the party on the night."},"occasion":{"type":"string","nullable":true,"enum":["birthday","anniversary","business","celebration","other"],"description":"The occasion the guest named (workbook Q204, DI-337; CHG-CSA-018). Shown to the host and the server; never a price."},"takenByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The staff member who took the booking (`createTableReservationForGuest`); null for a guest's own booking (CHG-CSA-045)."},"actualPartySize":{"type":"integer","nullable":true,"readOnly":true},"tableVisitId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"deposit":{"$ref":"#/components/schemas/TableReservationDeposit"},"createdAt":{"type":"string","format":"date-time","readOnly":true}}},
"TableReservationDeposit": {"type":"object","nullable":true,"readOnly":true,"x-ticvai-persistence":"fnb.table_reservation","description":"**The deposit this booking holds, snapshotted from `orders.DepositPolicy.dining` when it was made** (decided 29 September, rev 3 REV3-8b). Null where no deposit applied, which is every booking while the venue leaves `dining.enabled` false (the default). A later change to the policy does not re-price a booking already made.\n","required":["amount","basis"],"properties":{"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"basis":{"type":"string","enum":["fixedPerGuest","fixedPerTable","percentOfMinimumSpend"]},"holdExpiresAt":{"type":"string","format":"date-time","nullable":true,"description":"While `awaitingDeposit`, when the held cover is released if the deposit has not been authorised. The cart lease of the deposit line (15 minutes, audit R169)."},"refundableUntil":{"type":"string","format":"date-time","nullable":true,"description":"`startsAt` less `dining.refundableUntilHours`. Cancelling before it releases the deposit in full."},"variantId":{"type":"string","format":"uuid","description":"The venue's table-deposit variant, `DepositPolicy.dining.depositVariantId`, which the client sends to `addCartLine` with this booking's id."},"cartLineId":{"type":"string","format":"uuid","nullable":true,"description":"The `orders.CartLine` carrying the deposit, once added."},"depositId":{"type":"string","format":"uuid","nullable":true,"description":"The `orders.deposit` row, once the payment is authorised."}}},
"TableReservationStatus": {"type":"string","description":"`awaitingDeposit` only where the venue's dining deposit applies (decided 29 September, rev 3 REV3-8b); a booking with no deposit starts `booked`.","enum":["awaitingDeposit","booked","confirmed","seated","completed","cancelled","noShow"]},
"TableState": {"x-ticvai-persistence":"none — projection over table and visit","allOf":[{"$ref":"#/components/schemas/TableDefinition"},{"type":"object","required":["status"],"properties":{"status":{"$ref":"#/components/schemas/TableStatus"},"visitId":{"type":"string","format":"uuid","nullable":true},"covers":{"type":"integer","nullable":true},"seatedAt":{"type":"string","format":"date-time","nullable":true},"serverPrincipalId":{"type":"string","format":"uuid","nullable":true},"billTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}]},
"TableVisit": {"x-ticvai-persistence":"fnb.table_visit","type":"object","required":["id","tableId","outletId","covers","status","orders","openedAt"],"properties":{"id":{"type":"string","format":"uuid"},"tableId":{"type":"string","format":"uuid"},"tableLabel":{"type":"string"},"outletId":{"type":"string","format":"uuid"},"covers":{"type":"integer"},"status":{"type":"string","enum":["open","billRequested","settled","merged","cancelled"]},"serverPrincipalId":{"type":"string","format":"uuid","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"orders":{"type":"array","items":{"$ref":"#/components/schemas/FnbOrder"}},"mergedIntoVisitId":{"type":"string","format":"uuid","nullable":true},"mergedFromVisitIds":{"type":"array","items":{"type":"string","format":"uuid"}},"runningTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"gratuity":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"readOnly":true,"description":"The gratuity taken at `closeTableVisit`. **Not the service charge**, which is revenue (`FnbServiceChargePolicy`); this is the guest's tip, and `reassignServer` decides who shares it."},"openedAt":{"type":"string","format":"date-time"},"closedAt":{"type":"string","format":"date-time","nullable":true}}},
"TenderKind": {"type":"string","description":"`wallet` is a **digital wallet** (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 (a)). **The stored-value TICVAI wallet is a separate tender**: it is spent through `authoriseStoredValue` and `captureStoredValue` (`StoredValueKind` `wallet`), never as this value, so the client can see which of the two the decision meant.\n","enum":["cash","card","wallet","voucher","bankTransfer","hotelCharge","installment","giftCard","complimentary"]}
}
```
