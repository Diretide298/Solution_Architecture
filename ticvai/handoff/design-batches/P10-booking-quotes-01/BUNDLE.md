# P10-booking-quotes-01 — P10 · Booking & Quotes

**4 screens · 28 operations · 44 schemas · 11 permissions**

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

- **Every control that can be refused must be gated.** 11 permissions apply here:
  `CAPACITY_CONFIGURE, ORDER_CREATE, ORDER_EXCHANGE, ORDER_MODIFY, ORDER_REPRINT, ORDER_RESCHEDULE, ORDER_VIEW, PARTNER_MANAGE, PARTNER_VIEW, PRICE_VIEW, PRODUCT_VIEW`. A control nobody can use must say so,
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

### Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management)

Platform Foundation is everything the apps stand on. Five apps each have one door: the guest app and website (WEB-016, GST-042: a six-digit code to email or mobile, a password, Apple or Google, UAE Pass; never enterprise SSO), the till (POS-000: employee number and PIN, recent operators as tiles; the kitchen display is the same app), the staff handheld and scanner (EMP-001, SCN-001), Venue Management (SUP-001, the single door for the back office P08, the CMS P13, analytics P16 and the support desk P12) and TICVAI Control (ADM-001 for TICVAI's own platform operators, PTR-001 for partner users; the developer portal P14 and the sign-up P17 belong to this app too). A second factor is required by permission, not by role or device: ROLE_MANAGE, LEDGER_APPROVE and every PLATFORM_* permission, plus any the tenant adds; so a cashier never sees it and a platform operator always does. The factor is an authenticator app with an emailed code as fallback; five wrong codes lock step-up for the lockout minutes, never permanently. Guests get two-step verification only at a venue that switched it on. One person holds one session per workstation: a second sign-in is refused and only a supervisor ends the other session. Several roles mean a role prompt; one role goes straight in. The workstation decides the Sale Board, hardware and till identity, never what a person may do. Sensitive actions (refund approval, journal approval, credential reset, partner credit, commission rules, opening a platform-staff grant and 17 more) demand a fresh step-up on the operation itself, asked in place in the action's confirmation; the tenant may raise the strength, never remove it. Permission outcomes are three, never one word: self-authorised (proceeds, audited), escalated (a supervisor PIN in place), refused (the denied state, naming the permission); a missing permission is never an empty table, and a record outside the person's venues is "not found", indistinguishable from absent. The hierarchy is binding (tenant, brand, region, venue, department, sub-department, workstation; outlet beside department for F&B and retail); region owns currency, decimals, time zone, date format and fiscal year; configuration resolves nearest-ancestor across tenant, region and venue (outlet for F&B and retail), venue is the floor and a workstation is assigned a profile, never configured; every configuration screen says which level it writes and what it inherits. Venue Management is one tenant-level surface filtering across the venues in the session's scope. TICVAI's Console runs outside every cell: a platform operator picks a tenant and opens a time-boxed, audited platform-staff grant (with step-up) before any tenant action, and the tenant sees every action in its audit log (ADM-412 is the reference implementation). Approval workflows record authorisations and never perform the action; the requester cannot approve their own request; a venue may tighten and never loosen a rule from above; in-flight …
*(source: screens/P12-support-agent-console.yaml#SUP-001; R135; R126; R167; DI-1072; ADR-0002; ADR-0003; ADR-0004; R184; contracts/spine/identity.yaml#createMfaChallenge; contracts/spine/approvals.yaml#setStepUpPolicy; ADR-0011; ADR-0018; ADR-0029; R098; contracts/spine/approvals.yaml#decideApprovalRequest …)*

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Sign in / Sign out | Entering and leaving any app, staff or guest. | Login, Log in, Logon, Logout | screens/P04-point-of-sale.yaml#POS-000 … |
| Authentication code | The staff second factor from the authenticator app (or the emailed fallback). | OTP, 2FA code, token | screens/P09-platform-admin-console.yaml#ADM-001 |
| One-time code | The six-digit code a guest receives to sign in or prove a contact. | OTP, PIN, password | DI-1034; R167 |
| Two-step verification | The guest's optional second factor, asked only at venues that switched it on. | MFA, 2FA | DI-1072 |
| Tenant / Brand / Region / Venue / Department / Outlet | The binding hierarchy levels; region owns currency and dates; outlet is F&B or retail inside a venue. | Client, Customer, Org (for tenant), Site, Park, Property (for venue), Area, Territory (for region) | ADR-0011; ADR-0018 |
| Workstation (back office) / till (operator copy) | A configured device; decides Sale Board, hardware and till identity, never authorisation. | Terminal, Station, POS (for the device), till (for the Deposit Box) | ADR-0002; R156 |
| Sale Board | The configured front end a workstation loads (ticketing, F&B or retail). | Screen, Layout, Menu | ADR-0003 |
| Role | A named, fully configurable grouping of permissions; the seeded five are editable starting points. | Group, Profile | R229 |
| Staff member / Partner user / Platform operator | A tenant's staff principal; a partner's user; a TICVAI employee in the Console. | User (alone), Account, Agent (for venue staff) | F104 step 1; F104 step 4; F104 step 5 |
| Platform-staff grant | The time-boxed, audited access a platform operator opens into one tenant before acting in it. | Impersonation, Support login | R098 |
| Escalate / Refused | Escalate is supervisor approval captured in place; Refused is the denied state that names the permission. | Denied (for an action that can be escalated) | R197 |
| Approve / Reject / Return / Request information | The four decisions on an approval request; Withdraw is the requester's own act and never a rejection. | Accept, Decline, Cancel (for withdraw) | contracts/spine/approvals.yaml#decideApprovalRequest … |
| Subscription / Plan / Module / Licence | TICVAI's commercial relationship with a tenant, its plan, the modules it licenses and the limits. | Membership (that is the guest's pass) | R214 |
| Membership / Annual pass | A guest's pass product and its holder (BO-284 to BO-303). | Subscription (that is the tenant's TICVAI plan) | screens/P08-venue-back-office.yaml#BO-284 |
| Sandbox client / Production client | A developer's own test credential; a TICVAI-issued live credential after certification. | Test key, Live key, API key (without environment) | DI-927 |
| Asset (DAM) / Media (ticket) | A digital file in the library; ticket media is a wristband or card carrying entitlements. Never mix them. | Media (for a library asset) | contracts/satellite/assets.yaml#searchMedia … |


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `PTR-008` | Booking Creation | B–D | 105 | 53 | 6 | 66 | 0 | 6 | — | notStarted (generated) |
| `PTR-009` | Group / Bulk Booking | B–D | 11 | 18 | 6 | 14 | 2 | 6 | — | notStarted (generated) |
| `PTR-010` | Cart & Quote | B–D | 46 | 51 | 6 | 30 | 0 | 6 | — | notStarted (generated) |
| `PTR-011` | Quote Management | B–D | 10 | 40 | 6 | 17 | 0 | 0 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `PTR-008` Booking Creation

**Add booking creation for this venue.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Booking & Quotes · wave 2 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner staff holding `ORDER_CREATE`, `ORDER_EXCHANGE`, `ORDER_MODIFY`, `ORDER_REPRINT`, `ORDER_RESCHEDULE`, `ORDER_VIEW` (5 operate, 1 read); in the flows as partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | listDetail (compact density): `listOrders` reads the population and `getOrder` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `orderId` (deepLink) · cold entry: **A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the … |
| Route | `/general/booking-creation` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Cross-platform navigation removed 24 August**: SCN-003. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-018): The partner creates a booking; refund, void and discount are venue-side (design-notes correction ticketing-guest PTR-008). Removed 2 October 2026 (CHG-WIR-018): The partner creates a booking; refund, void and discount are venue-side (design-notes correction ticketing-guest PTR-008). Removed 2 October 2026 (CHG-WIR-018): The partner creates a booking; refund, void and discount are venue-side (design-notes correction ticketing-guest PTR-008).

**From the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process.** Create a booking on credit and get the vouchers. After Block A. Credit is checked at booking; above the limit the booking is refused with the available amount.

**Fixed on main** (the package already carries these; draw what it says): Staff list filters and refund, void and discount actions on Booking Creation. (CHG-WIR-018).

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

**Form: Create order** (modal, opened by *Create order*; *Create order* calls `createOrder`, *Cancel* sends nothing)

**Collects what `createOrder` sends before it is called.** Required: `id`, `venueId`, `channel`, `lines`, `recordedAt`. Optional: `shiftId`, `subjectId`, `guestLinkId`, `catalogueBundleVersion`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7. Also the idempotency key: it must equal the `Idempotency-Key` header, and a replay or a mismatch follows `IdempotencyKey` in `shared/common.yaml`. | `createOrder` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createOrder` body |
| Channel `channel` | select | required | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | — | — | `createOrder` body |
| Shift `shiftId` | picker: choose a shift | optional | — | — | shows names, sends the id | — | `createOrder` body |
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | Null for an anonymous sale. Identity and entitlement are separate. | `createOrder` body |
| Guest link `guestLinkId` | text field | optional | — | — | — | Present where the guest is linked across cells. | `createOrder` body |
| Catalogue bundle version `catalogueBundleVersion` | text field | optional | — | — | — | The bundle the client priced from. Lets the server explain a variance rather than merely report one. | `createOrder` body |
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `createOrder` body |
| ID `lines[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these. | `createOrder` body |
| Variant `lines[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `createOrder` body |
| Recommendation `lines[].recommendationId` | picker: choose a recommendation | optional | — | — | shows names, sends the id | The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation … | `createOrder` body |
| Performance `lines[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `createOrder` body |
| Booked window `lines[].bookedWindow` | group | optional | — | `endsAt` minus `startsAt` must equal the chosen variant's length (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. | — | The booked time window of an hourly product, such as a meeting room (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). | `createOrder` body |
| Starts at `lines[].bookedWindow.startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createOrder` body |
| Ends at `lines[].bookedWindow.endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | After `startsAt`, on the same venue day. | `createOrder` body |
| Inventory hold `lines[].inventoryHoldId` | text field | optional | — | — | — | Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products. | `createOrder` body |
| Seats `lines[].seatIds` | multi-picker: choose seats | optional | — | at most 50; At most `VenueSettings.; maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)), across all the … | — | Seated products only, as `seating.Seat.id`. Not available offline. | `createOrder` body |
| Resource hold `lines[].resourceHoldId` | picker: choose a resource hold | optional | — | — | shows names, sends the id | A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. | `createOrder` body |
| Attributes `lines[].attributes` | group | optional | — | — | — | Open attributes of a line, kept from the cart to the order line. `transport` is the one with a defined shape (decided 29 September, rev 3 REV3-21); other keys are free. | `createOrder` body |
| Transport `lines[].attributes.transport` | group | optional | — | — | — | What a transport line is for (decided 29 September, rev 3 REV3-21). Present on a one-way trip, a pass purchase, or a seat reserved with a pass already owned. | `createOrder` body |
| Quantity `lines[].quantity` | number field | required | — | min 1 | — | — | `createOrder` body |
| Eligibility declaration `lines[].eligibilityDeclaration` | repeatable rows | optional | — | — | — | What was declared for each guest on this line, kept as the record staff check at the gate. | `createOrder` body |
| Age band `lines[].eligibilityDeclaration[].ageBand` | radio group | optional | — | Infant · Child · Junior · Adult · Senior | — | Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+. | `createOrder` body |
| Age years `lines[].eligibilityDeclaration[].ageYears` | number field | optional | — | — | — | — | `createOrder` body |
| Height band index `lines[].eligibilityDeclaration[].heightBandIndex` | number field | optional | — | — | — | — | `createOrder` body |
| Confident swimmer `lines[].eligibilityDeclaration[].confidentSwimmer` | toggle | optional | — | — | — | Derived, kept for the gate check (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this … | `createOrder` body |
| Guardian signed `lines[].eligibilityDeclaration[].guardianSigned` | toggle | optional | — | — | — | — | `createOrder` body |
| Quoted unit price `lines[].quotedUnitPrice` | money field | required | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What the client charged, from its local bundle. | `createOrder` body |
| Holder name `lines[].holderName` | text field | optional | — | — | — | — | `createOrder` body |
| Data mask values `lines[].dataMaskValues` | key and value settings | optional | — | — | — | Deliberately open. Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the … | `createOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createOrder` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 A lease covering a line has expired (`leaseExpired`), capacity is exhausted (`capacityExhausted`), or the catalogue bundle the client priced from is beyond its … (OrderRefusedProblem); 422 More seats for one performance than the channel allows (`seatLimitExceeded`, decided 29 September, rev 3 REV3-7). (OrderRefusedProblem)

**Form: Exchange order lines** (modal, opened by *Exchange order lines*; *Exchange order lines* calls `exchangeOrderLines`, *Cancel* sends nothing)

**Collects what `exchangeOrderLines` sends before it is called.** Required: `id`, `outgoingLineIds`, `incomingLines`, `recordedAt`. Optional: `waiveFee`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of this exchange, and its idempotency key — it must equal the `Idempotency-Key` header. | `exchangeOrderLines` body |
| Outgoing lines `outgoingLineIds` | multi-picker: choose outgoing lines | required | — | at least 1 | — | — | `exchangeOrderLines` body |
| Incoming lines `incomingLines` | repeatable rows | required | — | at least 1 | — | — | `exchangeOrderLines` body |
| ID `incomingLines[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these. | `exchangeOrderLines` body |
| Variant `incomingLines[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `exchangeOrderLines` body |
| Recommendation `incomingLines[].recommendationId` | picker: choose a recommendation | optional | — | — | shows names, sends the id | The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation … | `exchangeOrderLines` body |
| Performance `incomingLines[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `exchangeOrderLines` body |
| Booked window `incomingLines[].bookedWindow` | group | optional | — | `endsAt` minus `startsAt` must equal the chosen variant's length (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. | — | The booked time window of an hourly product, such as a meeting room (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). | `exchangeOrderLines` body |
| Starts at `incomingLines[].bookedWindow.startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `exchangeOrderLines` body |
| Ends at `incomingLines[].bookedWindow.endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | After `startsAt`, on the same venue day. | `exchangeOrderLines` body |
| Inventory hold `incomingLines[].inventoryHoldId` | text field | optional | — | — | — | Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products. | `exchangeOrderLines` body |
| Seats `incomingLines[].seatIds` | multi-picker: choose seats | optional | — | at most 50; At most `VenueSettings.; maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)), across all the … | — | Seated products only, as `seating.Seat.id`. Not available offline. | `exchangeOrderLines` body |
| Resource hold `incomingLines[].resourceHoldId` | picker: choose a resource hold | optional | — | — | shows names, sends the id | A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. | `exchangeOrderLines` body |
| Attributes `incomingLines[].attributes` | group | optional | — | — | — | Open attributes of a line, kept from the cart to the order line. `transport` is the one with a defined shape (decided 29 September, rev 3 REV3-21); other keys are free. | `exchangeOrderLines` body |
| Transport `incomingLines[].attributes.transport` | group | optional | — | — | — | What a transport line is for (decided 29 September, rev 3 REV3-21). Present on a one-way trip, a pass purchase, or a seat reserved with a pass already owned. | `exchangeOrderLines` body |
| Quantity `incomingLines[].quantity` | number field | required | — | min 1 | — | — | `exchangeOrderLines` body |
| Eligibility declaration `incomingLines[].eligibilityDeclaration` | repeatable rows | optional | — | — | — | What was declared for each guest on this line, kept as the record staff check at the gate. | `exchangeOrderLines` body |
| Age band `incomingLines[].eligibilityDeclaration[].ageBand` | radio group | optional | — | Infant · Child · Junior · Adult · Senior | — | Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+. | `exchangeOrderLines` body |
| Age years `incomingLines[].eligibilityDeclaration[].ageYears` | number field | optional | — | — | — | — | `exchangeOrderLines` body |
| Height band index `incomingLines[].eligibilityDeclaration[].heightBandIndex` | number field | optional | — | — | — | — | `exchangeOrderLines` body |
| Confident swimmer `incomingLines[].eligibilityDeclaration[].confidentSwimmer` | toggle | optional | — | — | — | Derived, kept for the gate check (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this … | `exchangeOrderLines` body |
| Guardian signed `incomingLines[].eligibilityDeclaration[].guardianSigned` | toggle | optional | — | — | — | — | `exchangeOrderLines` body |
| Quoted unit price `incomingLines[].quotedUnitPrice` | money field | required | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What the client charged, from its local bundle. | `exchangeOrderLines` body |
| Holder name `incomingLines[].holderName` | text field | optional | — | — | — | — | `exchangeOrderLines` body |
| Data mask values `incomingLines[].dataMaskValues` | key and value settings | optional | — | — | — | Deliberately open. Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the … | `exchangeOrderLines` body |
| Waive fee `waiveFee` | toggle | optional | off | — | — | — | `exchangeOrderLines` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `exchangeOrderLines` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `exchangeOrderLines` body |

Errors to draw in the form: 409 Replacement unavailable (`replacementUnavailable`), outside the exchange window (`outsideExchangeWindow`), or the original is redeemed (`lineRedeemed`). (OrderRefusedProblem)

**Form: Hold order** (modal, opened by *Hold order*; *Hold order* calls `holdOrder`, *Cancel* sends nothing)

**Collects what `holdOrder` sends before it is called.** Required: `recordedAt`. Optional: `label`, `holdUntil`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Label `label` | text field | optional | — | max length 60 | — | How the cashier will find it again — a name, a description, a party size. A list of unlabelled parked sales is unusable at a busy counter. | `holdOrder` body |
| Hold until `holdUntil` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `holdOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `holdOrder` body |

Errors to draw in the form: 409 Order is already paid (`alreadyPaid`) or voided (`orderVoided`) — only a `pending` order is parked — or a seated line's lease ends before `holdUntil` … (OrderRefusedProblem)

**Form: Modify order** (modal, opened by *Modify order*; *Modify order* calls `modifyOrder`, *Cancel* sends nothing)

**Collects what `modifyOrder` sends before it is called.** Required: `id`, `recordedAt`. Optional: `addLines`, `removeLineIds`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of this modification, not of the order — the order is the path's `orderId`. | `modifyOrder` body |
| Add lines `addLines` | repeatable rows | optional | — | — | — | — | `modifyOrder` body |
| ID `addLines[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these. | `modifyOrder` body |
| Variant `addLines[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `modifyOrder` body |
| Recommendation `addLines[].recommendationId` | picker: choose a recommendation | optional | — | — | shows names, sends the id | The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation … | `modifyOrder` body |
| Performance `addLines[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `modifyOrder` body |
| Booked window `addLines[].bookedWindow` | group | optional | — | `endsAt` minus `startsAt` must equal the chosen variant's length (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. | — | The booked time window of an hourly product, such as a meeting room (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). | `modifyOrder` body |
| Starts at `addLines[].bookedWindow.startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `modifyOrder` body |
| Ends at `addLines[].bookedWindow.endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | After `startsAt`, on the same venue day. | `modifyOrder` body |
| Inventory hold `addLines[].inventoryHoldId` | text field | optional | — | — | — | Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products. | `modifyOrder` body |
| Seats `addLines[].seatIds` | multi-picker: choose seats | optional | — | at most 50; At most `VenueSettings.; maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)), across all the … | — | Seated products only, as `seating.Seat.id`. Not available offline. | `modifyOrder` body |
| Resource hold `addLines[].resourceHoldId` | picker: choose a resource hold | optional | — | — | shows names, sends the id | A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. | `modifyOrder` body |
| Attributes `addLines[].attributes` | group | optional | — | — | — | Open attributes of a line, kept from the cart to the order line. `transport` is the one with a defined shape (decided 29 September, rev 3 REV3-21); other keys are free. | `modifyOrder` body |
| Transport `addLines[].attributes.transport` | group | optional | — | — | — | What a transport line is for (decided 29 September, rev 3 REV3-21). Present on a one-way trip, a pass purchase, or a seat reserved with a pass already owned. | `modifyOrder` body |
| Quantity `addLines[].quantity` | number field | required | — | min 1 | — | — | `modifyOrder` body |
| Eligibility declaration `addLines[].eligibilityDeclaration` | repeatable rows | optional | — | — | — | What was declared for each guest on this line, kept as the record staff check at the gate. | `modifyOrder` body |
| Age band `addLines[].eligibilityDeclaration[].ageBand` | radio group | optional | — | Infant · Child · Junior · Adult · Senior | — | Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+. | `modifyOrder` body |
| Age years `addLines[].eligibilityDeclaration[].ageYears` | number field | optional | — | — | — | — | `modifyOrder` body |
| Height band index `addLines[].eligibilityDeclaration[].heightBandIndex` | number field | optional | — | — | — | — | `modifyOrder` body |
| Confident swimmer `addLines[].eligibilityDeclaration[].confidentSwimmer` | toggle | optional | — | — | — | Derived, kept for the gate check (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this … | `modifyOrder` body |
| Guardian signed `addLines[].eligibilityDeclaration[].guardianSigned` | toggle | optional | — | — | — | — | `modifyOrder` body |
| Quoted unit price `addLines[].quotedUnitPrice` | money field | required | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What the client charged, from its local bundle. | `modifyOrder` body |
| Holder name `addLines[].holderName` | text field | optional | — | — | — | — | `modifyOrder` body |
| Data mask values `addLines[].dataMaskValues` | key and value settings | optional | — | — | — | Deliberately open. Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the … | `modifyOrder` body |
| Remove lines `removeLineIds` | multi-picker: choose remove lines | optional | — | — | — | — | `modifyOrder` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `modifyOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `modifyOrder` body |

Errors to draw in the form: 409 A targeted line's entitlement has been redeemed (`lineRedeemed`, naming it in `lineIds`), or the order is voided (`orderVoided`). (OrderRefusedProblem)

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

**Form: Reschedule order** (modal, opened by *Reschedule order*; *Reschedule order* calls `rescheduleOrder`, *Cancel* sends nothing)

**Collects what `rescheduleOrder` sends before it is called.** Required: `targetPerformanceId`, `recordedAt`. Optional: `lineIds`, `waiveFee`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Target performance `targetPerformanceId` | picker: choose a target performance | required | — | — | shows names, sends the id | — | `rescheduleOrder` body |
| Lines `lineIds` | multi-picker: choose lines | optional | — | — | — | Omit to move the whole order. | `rescheduleOrder` body |
| Waive fee `waiveFee` | toggle | optional | off | — | — | — | `rescheduleOrder` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `rescheduleOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `rescheduleOrder` body |

Errors to draw in the form: 409 Target performance is unavailable (`targetUnavailable`) or outside the reschedule window (`outsideRescheduleWindow`). (OrderRefusedProblem)

#### Outputs: what the screen shows and produces

**Shown**

**Every order** (data table, from `listOrders`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order number | text | — |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunded amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | The same vocabulary as `Order.channel`, which this projects. |
| Line count | 1,234 | — |

**Every refund** (data table, from `listOrderRefunds`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order | the name it points at, never the id | — |
| Batch | the name it points at, never the id | The `RefundBatch` that raised this refund, where `createBulkRefund` did. Null for a refund raised on its own. |
| FX rate | text | The rate on the original payment, not today's (BL-087, CF-118). `Payment` records `tenderCurrency`, `fxRate` and `fxRateSource` at the … |
| Tax reversal entry | the name it points at, never the id | A refund reverses the tax entry it created, and this is where that is stated rather than implied. |
| Settle to | chip: Original tender, Advance balance, Wire transfer, Store credit | BL-086. A refund could only go back the way it came. |
| FX variance | AED 1,234.50 | Where the sale rate and the current rate differ, the difference is booked as an FX variance rather than hidden in the refund. |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Applied percentage | 1,234.5 | From the venue's time bands, or an approver override. |
| Status | chip: Pending approval, Pending gateway, Completed, Declined, Failed | — |
| Reason | text | — |
| Requested by principal | the name it points at, never the id | — |

**The selected order** (detail panel, from `listOrders`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order number | text | — |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunded amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | The same vocabulary as `Order.channel`, which this projects. |
| Line count | 1,234 | — |
| Principal | the name it points at, never the id | The cashier who raised it — what the held-orders list shows. |
| Hold label | text | As `Order.holdLabel`. |
| Held until | 1 Oct 2026, 14:30 | As `Order.heldUntil`, so a held-orders list can warn about the ones about to lapse. |

**The order statement** (detail panel, from `getOrderStatement`)

| Shows | Format | Notes |
|---|---|---|
| Order | the name it points at, never the id | — |
| Order number | text | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Entries | list or chips (count when long) | Sequential. What an agent reads to a guest asking about a charge. |
| Total paid | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total refunded | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Current balance | AED 1,234.50 | Positive means the guest owes; negative means a refund is outstanding. |

**The order** (detail panel, from `getOrder`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | The client UUIDv7 from `CreateOrderRequest.id`. |
| Order number | text | The number a guest reads and a cashier types. Server-assigned: the venue prefix and a sequence per venue, for example `DXB1-000123` … |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for … |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Net amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunded amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total price variance | AED 1,234.50 | Sum across lines. Zero on a normal order. |
| Lines | list or chips (count when long) | — |
| Payments | list or chips (count when long) | — |
| Principal | the name it points at, never the id | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create order (primary button) | `createOrder` POST `/orders` | CreateOrderRequest | Order | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 A lease covering a line has expired (`leaseExpired`), capacity is exhausted (`capacityExhausted`), or the catalogue bundle the … | opens modal first |
| Exchange order lines (secondary button) | `exchangeOrderLines` POST `/orders/{orderId}/exchanges` | ExchangeOrderRequest | OrderExchangeResult | 409 Replacement unavailable (`replacementUnavailable`), outside the exchange window (`outsideExchangeWindow`), or the original is redeemed (`lineRedeemed`). (OrderRefusedProblem) | opens modal first |
| Hold order (secondary button) | `holdOrder` POST `/orders/{orderId}/hold` | inline | Order | 409 Order is already paid (`alreadyPaid`) or voided (`orderVoided`) — only a `pending` order is parked — or a seated line's lease ends before `holdUntil` … (OrderRefusedProblem) | opens modal first |
| Modify order (secondary button) | `modifyOrder` POST `/orders/{orderId}/modify` | ModifyOrderRequest | OrderModificationResult | 409 A targeted line's entitlement has been redeemed (`lineRedeemed`, naming it in `lineIds`), or the order is voided (`orderVoided`). (OrderRefusedProblem) | opens modal first |
| Reprint order (secondary button) | `reprintOrder` POST `/orders/{orderId}/reprints` | inline | inline | 400 Validation failed | opens modal first; produces a document or message: Reprint or resend tickets |
| Reschedule order (secondary button) | `rescheduleOrder` POST `/orders/{orderId}/reschedule` | inline | OrderExchangeResult | 409 Target performance is unavailable (`targetUnavailable`) or outside the reschedule window (`outsideRescheduleWindow`). (OrderRefusedProblem) | opens modal first |
| Resume order (secondary button) | `resumeOrder` POST `/orders/{orderId}/resume` | — | OrderResumeResult | 409 Held order expired (`holdExpired`), or already resumed at another till (`alreadyResumed`). (OrderRefusedProblem) | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **confirmation**: Booking reference, vouchers to download or send, credit used. *(source: F03 step 3-4)*

**Data it reads**: `listOrders` (onLoad, From the flow it appears in)

**Where the user goes next**

- → `PTR-002` Partner Dashboard: *Partner Dashboard*; carries `orderId`
- → `PTR-003` Profile & Company Details: *Profile & Company Details*
- → `SCN-003` Ready to scan: *A customer arrives and is admitted*; calls `listOrders`
- → `PTR-016` Voucher / Ticket Download: *Downloads vouchers*; carries `orderId`; calls `createOrder`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The booking creation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the booking creation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No booking creation yet. Offers Create order (`createOrder`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, principalId, shiftId, status, createdFrom, createdTo and the booking creation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `listOrders` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A lease covering a line has expired (`leaseExpired`), capacity is exhausted (`capacityExhausted`), or the catalogue bundle the client priced from is beyond its … (OrderRefusedProblem); 409 A targeted line's entitlement has been redeemed (`lineRedeemed`, naming it in `lineIds`), or the order is voided (`orderVoided`). (OrderRefusedProblem); 409 Held order expired … |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
booking: DRT-2026-1042 · Day Pass Adult × 20 · AED 5,200 on credit
```

#### Permissions

- `createOrder` → `ORDER_CREATE` (operate) · staff, guest, partner
- `listOrders` → `ORDER_VIEW` (read) · staff, guest, partner
- `exchangeOrderLines` → `ORDER_EXCHANGE` (operate) · staff, partner
- `getOrder` → `ORDER_VIEW` (read) · staff, guest, partner
- `getOrderStatement` → `ORDER_VIEW` (read) · staff, partner
- `holdOrder` → `ORDER_MODIFY` (operate) · staff, partner
- `listOrderRefunds` → `ORDER_VIEW` (read) · staff, partner
- `modifyOrder` → `ORDER_MODIFY` (operate) · staff, partner
- `reprintOrder` → `ORDER_REPRINT` (operate) · staff, guest, partner
- `rescheduleOrder` → `ORDER_RESCHEDULE` (operate) · staff, partner
- `resumeOrder` → `ORDER_MODIFY` (operate) · staff, partner

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `listOrders` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

66 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.1.6 | This system should provide a Ticketing POS solution that enables the operator to sell all the tickets defined in the system including multi-day and combo tickets. The POS solution must also support … | Ticketing Sales | CONTRACTED | `createOrder` |
| 2.7.29 | The system should be able to offer ticket sales to various outside business entities through the use of the exposed APIs and dedicated modules. Examples of typical clients that would have discounts … | Ticketing Sales | CONTRACTED | `createOrder` |
| 2.7.30 | The system should cater to multiple ways of enabling B2B clients, resellers and partner distribution channels to resell tickets and services offered by the client: - Web-based solution for B2B … | Ticketing Sales | CONTRACTED | `createOrder` |
| 2.8.1 | The system should provide an application for call center agents to make new ticket purchases, modify existing ticket purchases and offer refunds for guests. Any modifications done should follow the … | Ticketing Sales | CONTRACTED | `createOrder` |
| 2.8.2 | The system should allow call center agents to: - Make ticket sales including individual seat selection. - Look up existing orders after guest verification. - Change demographic data on existing … | Ticketing Sales | CONTRACTED | `createOrder` |
| 2.12.25 | Each order has a unique number. | Ticketing Sales | CONTRACTED | `createOrder` |
| 2.11.11 | The system should correctly allocate the upgrade transaction to the sales channel it was processed on. Upgrade sales channel can be different from the purchase sales channel. | Ticketing Sales | CONTRACTED | `createOrder` |
| 2.13.5 | In addition to this, some B2B customers may have direct access via API. | Ticketing Sales | CONTRACTED | `createOrder` |
| 2.14.6 | The Annual pass can be bought at the Guest Service or at front gate. | Ticketing Sales | CONTRACTED | `createOrder` |
| 13.3.2 | APIs shall support ticket creation, modification, cancellation, exchange, upgrade, validation, inventory, availability and pricing operations. | Developer & API Management | CONTRACTED | `createOrder` |
| 5.3.7 | The system should allow access to their purchase history and ongoing orders and preferences. | F&B & Guest Management | CONTRACTED | `listOrders` |
| 5.9.4 | The system should be able to provide a detailed log of transactions for each till. Detailed log of transaction should be always accessible, searchable and printable at back office. | F&B & Guest Management | CONTRACTED | `listOrders` |
| … 54 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker · keyword 'ticket-booking ux')*
- **A46** Evaluate a dynamic bundle/package builder that auto-applies a discount when a guest adds multiple product types (ticket + F&B + retail) to cart, in addition to pre-defined packages *(Reshma Bandiwdekar · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'cart')*
- **A96** Build the journey library (abandoned cart with min-value/product filters, birthday, anniversary, cross-sell, survey — all consent-gated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'cart')*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'b2c checkout')*
- **A157** Keep F&B and retail online sale entirely within the platform (browse, cart, checkout, pickup or ship) with no redirect to a separate app *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 26 Aug 2026 · workshop tracker · keyword 'cart')*
- **A158** Obtain the resource-management reference documentation, review the hardware/ticketing docs, route follow-up questions to Qossai, and review the House of Wisdom booking flow as a UX reference *(Allam / Chinmay Parab / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 26 Aug 2026 · workshop tracker · keyword 'booking flow')*

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-008` · status **notStarted** · provenance generated
- Flow F03 *Partner books on credit*, step 3: Creates the booking → Order raised against the partner account
- Flow F10 *Partner books, uses and settles*, step 2: Books against the allocation → Held on credit, not paid
- Flow F10 *Partner books, uses and settles*, step 3: Receives vouchers → Distributes to their own customers
- Flow F03 branch at step 3 (requiresStaff): when The order exceeds available credit, Refused, with the shortfall stated. A supervisor may authorise a single-order override, which records who authorised it and expires — a partner past their limit is a decision someone owns.
- Flow F03 branch at step 3 (requiresStaff): when The partner account is suspended, Refused with the reason. Suspension is commercial and must not read as a system fault.
- Flow F10 branch at step 2 (requiresStaff): when Booking exceeds the credit limit, Refused, or requires an override. `overrideCreditLimit` exists and records who and why — a partner who can silently exceed their limit is a bad debt nobody saw.
- Flow F10 branch at step 2 (recoverable): when Allocation exhausted, Refused. **The partner may buy at retail instead**, which is a different price and must be shown as one.

#### Acceptance for the design

- [ ] Every input above is drawn (105), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (53 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-008?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create order, Exchange order lines, Hold order, Modify order, Reprint order, Reschedule order, Resume order.
- [ ] Every transition is wired: `PTR-002`, `PTR-003`, `SCN-003`, `PTR-016`.
- [ ] Every gated control is gated: `ORDER_CREATE`, `ORDER_EXCHANGE`, `ORDER_MODIFY`, `ORDER_REPRINT`, `ORDER_RESCHEDULE`, `ORDER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-009` Group / Bulk Booking

**Work with group / bulk booking for this venue.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Booking & Quotes · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner staff holding `CAPACITY_CONFIGURE`, `ORDER_CREATE`, `PRODUCT_VIEW` (1 configure, 1 operate, 1 read) |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | listDetail (compact density): `listSeatBlocks` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `blockId` (deepLink) · cold entry: **A partner link resolves within that partner's own scope and refuses outside it.** A forwarded link between partners must not open another partner's record. … |
| Route | `/general/group-bulk-booking` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Drawn 26 August** — `Seat Board 3.dc.html` frame `seat-3d`. **The frame names this screen on its own face**, which is the first pack to do that: the earlier F&B, POS and Retail boards had to be hand-assigned by purpose after three derivation attempts produced nonsense. **A board that says what it draws removes the guess entirely.**

**From the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process.** Group or bulk booking: seat blocks for a group, or a bulk batch of pre-generated QR tickets as CSV for partners without an integration. After Block A.

**Known correction pending (do not draw the wrong version)**

- **"Performance id" and "Reason" typed as text filters.** Why: The partner picks a performance by name and date. *(source: screens/P10-partner-reseller-portal.yaml#PTR-009 layout; Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Performance id | picker: choose a performance (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?performanceId=` to `listSeatBlocks`. | `listSeatBlocks` ?performanceId |
| Reason | select | optional | — | Production hold · House seats · Group allocation · Maintenance · Accessibility reserve · Distancing · Other | — | Sends `?reason=` to `listSeatBlocks`. | `listSeatBlocks` ?reason |

**Form: Allocate blocked seats** (modal, opened by *Allocate blocked seats*; *Allocate blocked seats* calls `allocateBlockedSeats`, *Cancel* sends nothing)

**Collects what `allocateBlockedSeats` sends before it is called.** Required: `seatIds`. Optional: `subjectId`, `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Seats `seatIds` | list of values (chips) | required | — | at least 1 | — | — | `allocateBlockedSeats` body |
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | — | `allocateBlockedSeats` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `allocateBlockedSeats` body |

**Form: Create seat block** (modal, opened by *Create seat block*; *Create seat block* calls `createSeatBlock`, *Cancel* sends nothing)

**Collects what `createSeatBlock` sends before it is called.** Required: `performanceId`, `seatIds`, `reason`, `note`. Optional: `releaseAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Performance `performanceId` | picker: choose a performance | required | — | — | shows names, sends the id | — | `createSeatBlock` body |
| Seats `seatIds` | list of values (chips) | required | — | at least 1 | — | — | `createSeatBlock` body |
| Reason `reason` | select | required | — | Production hold · House seats · Group allocation · Maintenance · Accessibility reserve · Distancing · Other | — | `other` is allowed only with a note (decided 28 September, audit R222). Every block already requires `note`, so an `other` block always says why; the notes are reviewed quarterly … | `createSeatBlock` body |
| Note `note` | text area | required | — | min length 3; max length 500 | — | — | `createSeatBlock` body |
| Release at `releaseAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Automatic release, for production holds freed close to performance. | `createSeatBlock` body |

Errors to draw in the form: 409 One or more seats already sold. (SeatConflictProblem)

**Form: Release seat block** (modal, opened by *Release seat block*; *Release seat block* calls `relinquishSeatBlock`, *Cancel* sends nothing)

**Collects what `relinquishSeatBlock` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `relinquishSeatBlock` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

#### Outputs: what the screen shows and produces

**Shown**

**Every seat block** (data table, from `listSeatBlocks`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Performance | the name it points at, never the id | — |
| Seats | list or chips (count when long) | — |
| Reason | chip: Production hold, House seats, Group allocation, Maintenance, Accessibility reserve … | `other` is allowed only with a note (decided 28 September, audit R222). Every block already requires `note`, so an `other` block always … |
| Note | text | — |
| Created by principal | the name it points at, never the id | — |
| Release at | 1 Oct 2026, 14:30 | — |
| Released at | 1 Oct 2026, 14:30 | — |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

**The selected seat block** (detail panel, from `listSeatBlocks`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Performance | the name it points at, never the id | — |
| Seats | list or chips (count when long) | — |
| Reason | chip: Production hold, House seats, Group allocation, Maintenance, Accessibility reserve … | `other` is allowed only with a note (decided 28 September, audit R222). Every block already requires `note`, so an `other` block always … |
| Note | text | — |
| Created by principal | the name it points at, never the id | — |
| Release at | 1 Oct 2026, 14:30 | — |
| Released at | 1 Oct 2026, 14:30 | — |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Allocate blocked seats (primary button) | `allocateBlockedSeats` POST `/seat-blocks/{blockId}/allocate` | inline | SeatHold | — | opens modal first |
| Create seat block (secondary button) | `createSeatBlock` POST `/seat-blocks` | CreateSeatBlockRequest | SeatBlock | 409 One or more seats already sold. (SeatConflictProblem) | opens modal first |
| Release seat block (secondary button) | `relinquishSeatBlock` DELETE `/seat-blocks/{blockId}` | inline | — | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **bulk batch**: Quantity, validity window, agreed rate, CSV download. *(source: DI-135; DI-553)*

**Data it reads**: `listSeatBlocks` (onLoad, List seat blocks)

**Where the user goes next**

- → `PTR-003` Profile & Company Details: *Profile & Company Details*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The group bulk booking list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the group bulk booking untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No group bulk booking yet. Offers Create seat block (`createSeatBlock`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on performanceId, reason and the group bulk booking are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listSeatBlocks` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 One or more seats already sold. (SeatConflictProblem) |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
batch: 5,000 × Day Pass · valid 1 Oct-31 Dec · AED 240 each · CSV
```

#### Permissions

- `allocateBlockedSeats` → `ORDER_CREATE` (operate) · staff, partner
- `createSeatBlock` → `CAPACITY_CONFIGURE` (configure) · staff, partner
- `listSeatBlocks` → `PRODUCT_VIEW` (read) · staff, partner
- `relinquishSeatBlock` → `CAPACITY_CONFIGURE` (configure) · staff, partner

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listSeatBlocks` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

14 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 21.9.1 | Group Reservations | Seat Management & Venue Mapping | CONTRACTED | `allocateBlockedSeats` |
| 21.9.2 | Corporate Seat Blocks | Seat Management & Venue Mapping | CONTRACTED | `allocateBlockedSeats` |
| 21.9.5 | Bulk Seat Allocation | Seat Management & Venue Mapping | CONTRACTED | `allocateBlockedSeats` |
| 21.3.5 | Temporary Seat Blocking | Seat Management & Venue Mapping | CONTRACTED | `createSeatBlock` |
| 21.3.6 | Temporary Seat Release | Seat Management & Venue Mapping | CONTRACTED | `createSeatBlock` |
| 21.4.6 | Seat Maintenance Status | Seat Management & Venue Mapping | CONTRACTED | `createSeatBlock` |
| 21.6.1 | VIP Seat Holds | Seat Management & Venue Mapping | CONTRACTED | `createSeatBlock` |
| 21.6.2 | Sponsor Seat Holds | Seat Management & Venue Mapping | CONTRACTED | `createSeatBlock` |
| 21.6.3 | Artist Seat Holds | Seat Management & Venue Mapping | CONTRACTED | `createSeatBlock` |
| 21.6.4 | Media Seat Holds | Seat Management & Venue Mapping | CONTRACTED | `createSeatBlock` |
| 21.6.5 | Corporate Seat Holds | Seat Management & Venue Mapping | CONTRACTED | `createSeatBlock` |
| 21.6.6 | Internal Seat Holds | Seat Management & Venue Mapping | CONTRACTED | `createSeatBlock` |
| … 2 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Amendments/cancellations/reschedules are checked against the applicable policy before being allowed. A booking's financial status (deposit required, partial payment, full payment) is tracked; schools and corporates can pay a 20-30% deposit with the balance due on or before arrival. *(agreed · MoM 1 Sep 2026, 4.12 Amendment, Cancellation & Booking Status · DI-615)*
- Allam: Bulk QR option — for partners with no technical capability, the platform generates a bulk batch of tickets (e.g. 5,000) with a validity window, delivered as QR codes (e.g. CSV) for the partner to import and resell. *(client request · MoM 5 Aug 2026, 2. B2B Ticket Distribution Models · DI-135)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker · keyword 'ticket-booking ux')*
- **A46** Evaluate a dynamic bundle/package builder that auto-applies a discount when a guest adds multiple product types (ticket + F&B + retail) to cart, in addition to pre-defined packages *(Reshma Bandiwdekar · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'cart')*
- **A96** Build the journey library (abandoned cart with min-value/product filters, birthday, anniversary, cross-sell, survey — all consent-gated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'cart')*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'b2c checkout')*
- **A157** Keep F&B and retail online sale entirely within the platform (browse, cart, checkout, pickup or ship) with no redirect to a separate app *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 26 Aug 2026 · workshop tracker · keyword 'cart')*
- **A158** Obtain the resource-management reference documentation, review the hardware/ticketing docs, route follow-up questions to Qossai, and review the House of Wisdom booking flow as a UX reference *(Allam / Chinmay Parab / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 26 Aug 2026 · workshop tracker · keyword 'booking flow')*

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-009` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Seat Board 3.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/Seat Board 3.dc.html`
- Client design-board frames: `Seat Board 3.dc.html#seat-3d`

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-009?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Allocate blocked seats, Create seat block, Release seat block.
- [ ] Every transition is wired: `PTR-003`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`, `ORDER_CREATE`, `PRODUCT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-010` Cart & Quote

**Work with cart & quote for this venue.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Booking & Quotes · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner staff holding `PRICE_VIEW` (1 read) |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | listDetail (compact density): `listPromotions` reads the population and `getPromotion` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `cartId` (session), `lineId` (deepLink), `promotionId` (deepLink) · cold entry: **A partner link resolves within that partner's own scope and refuses outside it.** A forwarded link between partners must not open another partner's record. … |
| Route | `/general/cart-and-quote` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-018): Promotion analysis (analysePromotionConflicts) is a venue tool, not a partner's cart action (design-notes correction ticketing-guest PTR-010).

**From the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process.** The partner's cart and quote: lines at partner prices, a quote to send to the end customer, then checkout on credit. After Block A.

**Fixed on main** (the package already carries these; draw what it says): Promotion list filters and "Analyse promotion conflicts" on the partner's cart. (CHG-WIR-018).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listPromotions`. | `listPromotions` ?venueId |
| Status | select | optional | — | Draft · Scheduled · Live · Paused · Expired · Ended | — | Sends `?status=` to `listPromotions`. | `listPromotions` ?status |
| Active at | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?activeAt=` to `listPromotions`. | `listPromotions` ?activeAt |

**Form: Evaluate promotions** (modal, opened by *Evaluate promotions*; *Evaluate promotions* calls `evaluatePromotions`, *Cancel* sends nothing)

**Collects what `evaluatePromotions` sends before it is called.** Required: `venueId`, `channel`, `lines`. Optional: `subjectId`, `membershipTierId`, `couponCodes`, `evaluateAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `evaluatePromotions` body |
| Channel `channel` | select | required | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | — | Where the sale is being made. Matched against `PromotionConditions.channels`, so both sides use the one shared vocabulary. | `evaluatePromotions` body |
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | — | `evaluatePromotions` body |
| Membership tier `membershipTierId` | picker: choose a membership tier | optional | — | — | shows names, sends the id | — | `evaluatePromotions` body |
| Coupon codes `couponCodes` | list of values (chips) | optional | — | — | — | — | `evaluatePromotions` body |
| Evaluate at `evaluateAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | For back-office testing of a rule before publishing. | `evaluatePromotions` body |
| Order `orderId` | picker: choose an order | optional | — | — | shows names, sends the id | The order (`orders.sales_order`) being priced for payment. Sent only by the order service when it confirms an order; when present the evaluation writes one … | `evaluatePromotions` body |
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `evaluatePromotions` body |
| Line `lines[].lineId` | text field | required | — | — | — | — | `evaluatePromotions` body |
| Variant `lines[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `evaluatePromotions` body |
| Performance `lines[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `evaluatePromotions` body |
| Quantity `lines[].quantity` | number field | required | — | min 1 | — | — | `evaluatePromotions` body |
| Unit price `lines[].unitPrice` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `evaluatePromotions` body |

Errors to draw in the form: 400 Validation failed

**Form: Add cart line** (modal, opened by *Add cart line*; *Add cart line* calls `addCartLine`, *Cancel* sends nothing)

**Collects what `addCartLine` sends before it is called.** Required: `variantId`, `quantity`. Optional: `performanceId`, `seatIds`, `parentLineId`, `attributes`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Variant `variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `addCartLine` body |
| Quantity `quantity` | number field | required | — | min 1 | — | — | `addCartLine` body |
| Performance `performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `addCartLine` body |
| Booked window `bookedWindow` | group | optional | — | `endsAt` minus `startsAt` must equal the chosen variant's length (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. | — | The booked time window of an hourly product, such as a meeting room (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). | `addCartLine` body |
| Starts at `bookedWindow.startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `addCartLine` body |
| Ends at `bookedWindow.endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | After `startsAt`, on the same venue day. | `addCartLine` body |
| Recommendation `recommendationId` | picker: choose a recommendation | optional | — | — | shows names, sends the id | The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation … | `addCartLine` body |
| Table reservation `tableReservationId` | picker: choose a table reservation | optional | — | A booking that is not awaiting a deposit is refused 422 `depositNotDue`. | shows names, sends the id | A table deposit line (decided 29 September, rev 3 REV3-8b): the `fnb.TableReservation` in `awaitingDeposit` this pays for, sent with `variantId` set to the booking's … | `addCartLine` body |
| Seats `seatIds` | multi-picker: choose seats | optional | — | at most 50; At most `VenueSettings.; maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)). | — | At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on … | `addCartLine` body |
| Resource hold `resourceHoldId` | picker: choose a resource hold | optional | — | — | shows names, sends the id | A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant and … | `addCartLine` body |
| Parent line `parentLineId` | picker: choose a parent line | optional | — | — | shows names, sends the id | For an add-on attaching to a ticket already in the cart. Removing the parent removes the child — a locker with no admission is not a sale. | `addCartLine` body |
| Attributes `attributes` | group | optional | — | — | — | Open attributes of a line, kept from the cart to the order line. `transport` is the one with a defined shape (decided 29 September, rev 3 REV3-21); other keys are free. | `addCartLine` body |
| Transport `attributes.transport` | group | optional | — | — | — | What a transport line is for (decided 29 September, rev 3 REV3-21). Present on a one-way trip, a pass purchase, or a seat reserved with a pass already owned. | `addCartLine` body |
| Route `attributes.transport.routeId` | picker: choose a route | required | — | — | shows names, sends the id | The `transport.TransportRoute`. | `addCartLine` body |
| From station `attributes.transport.fromStationId` | picker: choose a from station | required | — | — | shows names, sends the id | Boarding station, a stop of the route. | `addCartLine` body |
| To station `attributes.transport.toStationId` | picker: choose a to station | required | — | — | shows names, sends the id | Alighting station, a later stop of the route. | `addCartLine` body |
| Passenger type code `attributes.transport.passengerTypeCode` | text field | optional | — | pattern `^[a-z][a-zA-Z0-9]{0,31}$` | — | The fare table's passenger type (`adult`, `child`, ...). Required on a one-way trip. | `addCartLine` body |
| Pass type `attributes.transport.passTypeId` | picker: choose a pass type | optional | — | — | shows names, sends the id | Pass purchase only. The `transport.PassType` bought for this station pair. | `addCartLine` body |
| Pass entitlement `attributes.transport.passEntitlementId` | picker: choose a pass entitlement | optional | — | — | shows names, sends the id | A seat reserved with a pass already owned. The line is zero-priced and validated against the pass (stations covered, an entry left, within validity). | `addCartLine` body |

Errors to draw in the form: 403 The performance's on-sale waiting room is on and the request has no valid admission token (ADR-0066).; 409 No capacity, or the product is not sellable on this channel (`notSellableOnChannel`). (CartProblem); 422 The booked window is missing, not allowed or the wrong length for the variant (`windowRequired`, `windowNotAllowed`, `windowLengthMismatch`; rev 3 REV3-13), or … (CartProblem)

**Form: Save cart line** (modal, opened by *Save cart line*; *Save cart line* calls `updateCartLine`, *Cancel* sends nothing)

**Collects what `updateCartLine` sends before it is called.** Required: `quantity`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Quantity `quantity` | number field | required | — | min 0 | — | The new quantity. 0 removes the line (audit R123 (1)). | `updateCartLine` body |

Errors to draw in the form: 409 Not enough capacity to increase (`noCapacity`). (CartProblem); 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

**Form: Checkout cart** (modal, opened by *Checkout cart*; *Checkout cart* calls `checkoutCart`, *Cancel* sends nothing)

**Collects what `checkoutCart` sends before it is called.** Nothing in the body is required. Optional: `subjectId`, `attendees`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | The guest the order is for. A guest caller may name only themselves (`guestAuth` never widens to another subject); omitted, the cart's own `subjectId` is used. | `checkoutCart` body |
| Charge currency `chargeCurrency` | text field | optional | — | pattern `^[A-Z]{3}$`; A currency the venue does not take is refused 400 `currency-not-chargeable`. | — | The currency the guest selected to pay in (decided 2 October 2026, Chinmay; CHG-FIN-001). | `checkoutCart` body |
| Marketing consents `marketingConsents` | repeatable rows | optional | — | — | — | Marketing opt-ins given at checkout (29 September, M18-15). Shown unticked beside the terms; one entry per channel and purpose the guest ticked. | `checkoutCart` body |
| Channel `marketingConsents[].channel` | radio group | required | — | Email · SMS · Whatsapp · Push | — | — | `checkoutCart` body |
| Purpose `marketingConsents[].purpose` | text field | required | — | max length 60 | — | The consent purpose code (marketing ConsentPurpose), for example `marketing`. | `checkoutCart` body |
| Granted `marketingConsents[].granted` | toggle | required | — | True only when the guest ticked it. | — | True only when the guest ticked it. Never pre-ticked. | `checkoutCart` body |
| Notice version `marketingConsents[].noticeVersion` | text field | optional | — | max length 40 | — | The version of the consent notice shown. | `checkoutCart` body |
| Attendees `attendees` | repeatable rows | optional | — | — | — | The named holder for each cart line that needs one. Becomes `CreateOrderLine.holderName` on the order's matching line. | `checkoutCart` body |
| Line `attendees[].lineId` | picker: choose a line | required | — | — | shows names, sends the id | A `CartLine.id` in this cart. | `checkoutCart` body |
| Holder name `attendees[].holderName` | text field | required | — | — | — | — | `checkoutCart` body |

Errors to draw in the form: 400 `chargeCurrency` is not one the venue takes (problem type `currency-not-chargeable`, CHG-FIN-001).; 403 The contact the tickets would go to is not proven — an unverified session (`sessionNotVerified`), or a guest checkout with no confirmed one-time code … (CartProblem); 409 A lease expired between the last read and checkout (`leaseExpired`), or a resource hold did (`resourceHoldInvalid`, rev 3 REV3-15). (CartProblem); 422 A required consent question is unanswered (`consentRequired`), or an answer blocks the booking (`consentAnswerBlocks`), with the lines in `lineIds` (decided 29 … (CartProblem)

#### Outputs: what the screen shows and produces

**Shown**

**Every promotion** (data table, from `listPromotions`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Venue | the name it points at, never the id | — |
| Discount | grouped details | — |
| Conditions | grouped details | All conditions must hold. An empty object matches everything. |
| Stacking mode | chip: Exclusive, Stackable, Best only, Stack with group | How this promotion combines with others. Declared, never inferred from creation order — two reasonable promotions can otherwise combine … |
| Stacking group | text | — |
| Precedence | 1,234 | Higher evaluates first where several could apply. |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |
| Max redemptions | 1,234 | — |

**The selected promotion** (detail panel, from `getPromotion`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Venue | the name it points at, never the id | — |
| Discount | grouped details | — |
| Conditions | grouped details | All conditions must hold. An empty object matches everything. |
| Stacking mode | chip: Exclusive, Stackable, Best only, Stack with group | How this promotion combines with others. Declared, never inferred from creation order — two reasonable promotions can otherwise combine … |
| Stacking group | text | — |
| Precedence | 1,234 | Higher evaluates first where several could apply. |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |
| Max redemptions | 1,234 | — |
| Max redemptions per guest | 1,234 | — |
| Budget cap | AED 1,234.50 | Total discount value after which the promotion stops automatically. Enforced at checkout, where an order whose discount would take the … |
| ID | the name it points at, never the id | — |
| Status | chip: Draft, Scheduled, Live, Paused, Expired, Ended | — |

**The promotion usage** (detail panel, from `getPromotionUsage`)

| Shows | Format | Notes |
|---|---|---|
| Promotion | the name it points at, never the id | — |
| Redemption count | 1,234 | — |
| Discount given | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Budget cap | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Budget remaining | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Is budget exhausted | yes / no (icon or chip) | — |
| By channel | list or chips (count when long) | — |

**The cart** (detail panel, from `getCart`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Token | text | How an anonymous guest returns to their cart, including from a recovery email. Rotated on claim, so a link shared before signing in does … |
| Venue | the name it points at, never the id | — |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | Where a sale came from. Restored 24 August — this was lost in the `Money` rewrite and nine references across four contracts were pointing … |
| Subject | the name it points at, never the id | Null while anonymous. Set by `claimCart`. |
| Status | chip: Active, Expiring, Expired, Abandoned, Checked out | — |
| Lines | list or chips (count when long) | — |
| Conflicts | list or chips (count when long) | — |
| Subtotal | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Discount total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Applied promotions | list or chips (count when long) | Re-evaluated on every read. A promotion that expired while the cart sat must not still be applied at checkout, and a promotion that became … |
| Expires at | 1 Oct 2026, 14:30 | The earliest lease expiry in the cart, or the cart's own window where it holds none. |
| Extensions used | 1,234 | — |
| Max extensions | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Evaluate promotions (primary button) | `evaluatePromotions` POST `/promotions/evaluate` | EvaluatePromotionsRequest | PromotionEvaluation | 400 Validation failed | opens modal first |
| Add cart line (secondary button) | `addCartLine` POST `/carts/{cartId}/lines` | AddCartLineRequest | Cart | 403 The performance's on-sale waiting room is on and the request has no valid admission token (ADR-0066).; 409 No capacity, or the product is not sellable on this channel (`notSellableOnChannel`). (CartProblem); 422 The … | opens modal first |
| Save cart line (secondary button) | `updateCartLine` PATCH `/carts/{cartId}/lines/{lineId}` | inline | Cart | 409 Not enough capacity to increase (`noCapacity`). (CartProblem); 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | opens modal first |
| Remove cart line (destructive button) | `removeCartLine` DELETE `/carts/{cartId}/lines/{lineId}` | — | Cart | — | — |
| Checkout cart (secondary button) | `checkoutCart` POST `/carts/{cartId}/checkout` | inline | Order | 400 `chargeCurrency` is not one the venue takes (problem type `currency-not-chargeable`, CHG-FIN-001).; 403 The contact the tickets would go to is not proven — an unverified session (`sessionNotVerified`), or a guest … | emits `order.created`; opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **quote**: Lines, partner net and the selling price the partner chooses, validity of the quote. *(source: screens/P10-partner-reseller-portal.yaml#PTR-010 purpose)*

**Data it reads**: `evaluatePromotions` (onLoad, from page inventory); `listPromotions` (onLoad, List promotions); `getCart` (onLoad, The cart, priced and checked, right now)

**Where the user goes next**

- → `PTR-002` Partner Dashboard: *Partner Dashboard*; carries `orderId`
- → `PTR-003` Profile & Company Details: *Profile & Company Details*

**What opens over it**

- confirmDialog *Remove cart line*: **Names what `removeCartLine` changes and what it leaves alone**, in the consequence rather than the verb. A cart quote this affects should be identified in the dialog, not just counted.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The cart quote list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the cart quote untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No cart quote yet. Offers Add cart line (`addCartLine`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, status, activeAt and the cart quote are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRICE_VIEW`, which `getPromotion` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 400 `chargeCurrency` is not one the venue takes (problem type `currency-not-chargeable`, CHG-FIN-001).; 409 A lease expired between the last read and checkout (`leaseExpired`), or a resource hold did (`resourceHoldInvalid`, rev 3 REV3-15). (CartProblem); 409 No capacity, or the product is not sellable on this channel (`notSellableOnChannel`). (CartProblem) |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
quote: Q-1042 · 20 × Day Pass · net AED 5,200 · valid 48 h
```

#### Permissions

- `evaluatePromotions` → `PRICE_VIEW` (read) · staff, guest, partner
- `getPromotion` → `PRICE_VIEW` (read) · staff, guest, partner
- `getPromotionUsage` → `PRICE_VIEW` (read) · staff, partner
- `listPromotions` → `PRICE_VIEW` (read) · staff, guest, partner
- `getCart` → no permission · guest, partner, staff
- `addCartLine` → no permission · guest, partner, staff
- `updateCartLine` → no permission · guest, partner
- `removeCartLine` → no permission · guest, partner
- `checkoutCart` → no permission · guest, partner

**A refused user sees:** Shown when the caller lacks `PRICE_VIEW`, which `getPromotion` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

30 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.11 | - Discounts | Ticketing Sales | CONTRACTED | `evaluatePromotions` |
| 2.6.12 | - Dynamic promotions | Ticketing Sales | CONTRACTED | `evaluatePromotions` |
| 2.6.13 | - Coupons | Ticketing Sales | CONTRACTED | `evaluatePromotions` |
| 2.8.5 | The system should allow call center agents to apply promotions, discounts, up-sales and offers configured in the system. Application of discount coupons via a code supplied (on the phone) by the … | Ticketing Sales | CONTRACTED | `evaluatePromotions` |
| 3.5.9 | System shall automatically present bundle offers based on configurable conditions such as number of tickets purchased, guest type, loyalty tier, membership status, sales channel, season, location, or … | Admission and Access | CONTRACTED | `evaluatePromotions` |
| 3.6.16 | The system should allow creation of promotion on a bundle: “buy x, get x free”, or “buy a ticket and a catalogue and get 10% off or get AED 10 discount” | Admission and Access | CONTRACTED | `evaluatePromotions` |
| 3.6.17 | The system should allow creation of added value: “Buy for more than 200 AED and get a free pencil” | Admission and Access | CONTRACTED | `evaluatePromotions` |
| 3.6.32 | Discounts can be under conditions (dynamic discounts): - early birds, - subject to volume (buy one get one, 4 for 3 …), - subject to the type of tickets or - subject to the customer segment. | Admission and Access | CONTRACTED | `evaluatePromotions` |
| 3.6.34 | Cart-level promotions & bundle logic (e.g., “Buy 4 Pay 3”, multi-park family packs) applied automatically at checkout, without new SKUs | Admission and Access | CONTRACTED | `evaluatePromotions` |
| 4.1.7 | The system should be able to accept promotions linked with admission tickets and/or vouchers. | Bundles and Promotions | CONTRACTED | `evaluatePromotions` |
| 4.1.9 | The system should be able to apply BOGO based promotion offers based on purchased product types and/or product count | Bundles and Promotions | CONTRACTED | `evaluatePromotions` |
| 4.1.10 | The system should be able to allow: - Buy X product and get X product for free. - Buy X product and get Y product for free. - Buy N number of products and Get X product for free. - Buy N number of … | Bundles and Promotions | CONTRACTED | `evaluatePromotions` |
| … 18 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker · keyword 'ticket-booking ux')*
- **A46** Evaluate a dynamic bundle/package builder that auto-applies a discount when a guest adds multiple product types (ticket + F&B + retail) to cart, in addition to pre-defined packages *(Reshma Bandiwdekar · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'cart')*
- **A96** Build the journey library (abandoned cart with min-value/product filters, birthday, anniversary, cross-sell, survey — all consent-gated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'cart')*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'b2c checkout')*
- **A157** Keep F&B and retail online sale entirely within the platform (browse, cart, checkout, pickup or ship) with no redirect to a separate app *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 26 Aug 2026 · workshop tracker · keyword 'cart')*
- **A158** Obtain the resource-management reference documentation, review the hardware/ticketing docs, route follow-up questions to Qossai, and review the House of Wisdom booking flow as a UX reference *(Allam / Chinmay Parab / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 26 Aug 2026 · workshop tracker · keyword 'booking flow')*

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-010` · status **notStarted** · provenance generated
- ADR-0037 *A lock holds one statement, not a transaction* (`docs/adr/0037-what-may-be-inside-a-lock.md`)
- ADR-0045 *Every order carries a proven contact, and the gate is the checkout page* (`docs/adr/0045-every-order-carries-a-proven-contact.md`)
- ADR-0066 *The on-sale waiting room sits at the edge, apart from the ride queue* (`docs/adr/0066-the-on-sale-waiting-room-is-separate-from-the-ride-queue.md`)
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (46), with its required mark, default, format and its error state (400, 403, 404, 409, 410, 412, 422).
- [ ] Every output is drawn (51 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-010?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Evaluate promotions, Add cart line, Save cart line, Remove cart line, Checkout cart.
- [ ] Every transition is wired: `PTR-002`, `PTR-003`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-011` Quote Management

**Raise quotes and follow the ones offered to this partner.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Booking & Quotes · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner staff holding `PARTNER_MANAGE`, `PARTNER_VIEW` (1 configure, 1 read) |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | listDetail (compact density): `listPartnerAgreements` reads the population and `getCommissionStatement` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `agreementId` (deepLink) · cold entry: **A partner link resolves within that partner's own scope and refuses outside it.** A forwarded link between partners must not open another partner's record. … |
| Route | `/general/quote-management` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement.

**Known gaps.**  Open: No contract — quotes are procurement-side only

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** A partner's quotes for group or trade bookings against its agreement: create, see validity and state. Prices shown are the partner's net prices from the agreement; the partner never sets a price.

**Fixed on main** (the package already carries these; draw what it says): Purpose "for this venue". (CHG-WIR-023); formCreatePartnerQuote asks the person for id. (CHG-SOT-015); Tables show every schema field, plumbing included: 'Every partner agreement' drop id, partnerId, brandingAssetId; 'Every partner quote' … (CHG-SOT-015).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Expiring within days | number field (days) | optional | — | — | — | Sends `?expiringWithinDays=` to `listPartnerAgreements`. | `listPartnerAgreements` ?expiringWithinDays |
| Status | select | optional | — | Pending approval · Active · Expiring soon · Expired · Suspended · Terminated | — | Sends `?status=` to `listPartnerAgreements`. | `listPartnerAgreements` ?status |

**Form: Create partner quote** (modal, opened by *Create partner quote*; *Create partner quote* calls `createPartnerQuote`, *Cancel* sends nothing)

**Collects what `createPartnerQuote` sends before it is called.** The person picks the agreement and enters the amount, currency and validity; `partnerId` comes from the session. Never `id` or `status`: an id is a client UUIDv7 generated silently and the status and timestamps are the server's (design-notes correction, CHG-SOT-015). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createPartnerQuote` body |
| Partner `partnerId` | picker: choose a partner | optional | — | — | shows names, sends the id | — | `createPartnerQuote` body |
| Agreement `agreementId` | picker: choose an agreement | optional | — | — | shows names, sends the id | — | `createPartnerQuote` body |
| Currency `currency` | text field | optional | — | — | — | Not stored on the row. Currency is region-scoped and resolves from the scope walk (ADR-0018); a quote that carries its own copy is a quote that disagrees with the region the … | `createPartnerQuote` body |
| Total minor `totalMinor` | number field | optional | — | — | — | — | `createPartnerQuote` body |
| State `state` | radio group | optional | — | Draft · Sent · Accepted · Declined · Expired | — | — | `createPartnerQuote` body |
| Valid until `validUntil` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Stored, not calculated - an offer whose expiry moves when you read it is not an offer. | `createPartnerQuote` body |
| Created at `createdAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createPartnerQuote` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every partner agreement** (data table, from `listPartnerAgreements`): The partner and agreement are shown by name; ids stay in the detail panel with a copy action.

| Shows | Format | Notes |
|---|---|---|
| Partner name | text | The partner's trading name, read from control.partner.trading_name (Partner.tradingName) when the agreement is returned and never stored on … |
| Status | chip: Pending approval, Active, Expiring soon, Expired, Suspended, Terminated | — |
| Rate mode | chip: Net rate, Commission | Alternatives, not both. A partner buys at a net rate and keeps the margin, or sells at face value and is paid commission. |
| Commission percent | 1,234.5 | — |
| Volume tiers | list or chips (count when long) | Retired: the tiers are rows of control.partner_rate_volume_band (`PartnerRate.volumeBands`, written by setPartnerRateNet), one set per rate … |
| Volume window | chip: Calendar month, Calendar quarter, Calendar year, Agreement year, Rolling12 months | — |
| Seasonal rates | list or chips (count when long) | Retired: a seasonal rate is a control.partner_rate row with `seasonalRate: true` and its own `effectiveFrom`/`effectiveTo` (`PartnerRate` … |
| Segment tier | text | — |
| Storefront subdomain | text | — |

**Every partner quote** (data table, from `listPartnerQuotes`): The partner and agreement are shown by name; ids stay in the detail panel with a copy action.

| Shows | Format | Notes |
|---|---|---|
| Currency | text | Not stored on the row. Currency is region-scoped and resolves from the scope walk (ADR-0018); a quote that carries its own copy is a quote … |
| Total minor | 1,234 | — |
| State | chip: Draft, Sent, Accepted, Declined, Expired | — |
| Valid until | 1 Oct 2026, 14:30 | Stored, not calculated - an offer whose expiry moves when you read it is not an offer. |

**The selected partner agreement** (detail panel, from `listPartnerAgreements`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Partner | the name it points at, never the id | The partner (control.partner) this agreement is with. The agreement carries the terms; control.partner carries who the partner is and … |
| Partner name | text | The partner's trading name, read from control.partner.trading_name (Partner.tradingName) when the agreement is returned and never stored on … |
| Status | chip: Pending approval, Active, Expiring soon, Expired, Suspended, Terminated | — |
| Rate mode | chip: Net rate, Commission | Alternatives, not both. A partner buys at a net rate and keeps the margin, or sells at face value and is paid commission. |
| Commission percent | 1,234.5 | — |
| Volume tiers | list or chips (count when long) | Retired: the tiers are rows of control.partner_rate_volume_band (`PartnerRate.volumeBands`, written by setPartnerRateNet), one set per rate … |
| Volume window | chip: Calendar month, Calendar quarter, Calendar year, Agreement year, Rolling12 months | — |
| Seasonal rates | list or chips (count when long) | Retired: a seasonal rate is a control.partner_rate row with `seasonalRate: true` and its own `effectiveFrom`/`effectiveTo` (`PartnerRate` … |
| Segment tier | text | — |
| Branding image | the image or video | 2.7.x, BL-078. A reseller selling a venue's tickets under their own brand is a second scope level white-label does not have — … |
| Storefront subdomain | text | — |
| Sponsorship | grouped details | BL-050. Sponsorship inventory is sellable capacity of a different kind — logo placements, hospitality allocations, naming rights. |
| Net rates | list or chips (count when long) | Retired: net rates are rows of control.partner_rate (`PartnerRate` with `pricingModel: netRate`, `netRate` and the `maxDiscountPercent` … |
| Credit term days | 1,234 | 2.7.36. Net 30, net 60. |
| Accepted by principal | the name it points at, never the id | BL-079. Electronic acceptance against a version, following the `signatureRef` precedent. |

**The commission statement** (detail panel, from `getCommissionStatement`)

| Shows | Format | Notes |
|---|---|---|
| Agreement | the name it points at, never the id | — |
| Partner name | text | — |
| From | 1 Oct 2026 | — |
| To | 1 Oct 2026 | — |
| Currency | text | — |
| Gross sales | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunds | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Net sales | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Commission earned | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Amount due | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Lines | list or chips (count when long) | Reconcilable order by order. A statement a partner cannot check line by line is a statement they will dispute, and the dispute costs more … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create partner quote (primary button) | `createPartnerQuote` POST `/partner-quotes` | PartnerQuote | PartnerQuote | — | opens modal first |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Quote total**: Money in the agreement's currency; valid-until date prominent; an expired quote cannot be booked. *(source: contracts/satellite/subscription.yaml#listPartnerQuotes; DI-930)*

**Data it reads**: `listPartnerAgreements` (onLoad, Commercial agreements with B2B partners); `listPartnerQuotes` (onLoad, Quotes offered to this partner)

**Where the user goes next**

- → `PTR-003` Profile & Company Details: *Profile & Company Details*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The quote list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the quote untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No quote yet. Offers Create partner quote (`createPartnerQuote`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on expiringWithinDays, status and the quote are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PARTNER_MANAGE`, which `listPartnerAgreements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
quotes:
- ref: Q-DGT-0098
  agreement: Desert Gate Tours 2026 trade
  total: AED 12,600.00
  state: issued
  validUntil: 15/10/2026
```

#### Permissions

- `listPartnerAgreements` → `PARTNER_MANAGE` (configure) · staff, partner
- `getCommissionStatement` → `PARTNER_VIEW` (read) · staff, partner
- `listPartnerQuotes` → `PARTNER_VIEW` (read) · partner
- `createPartnerQuote` → `PARTNER_MANAGE` (configure) · partner

**A refused user sees:** Shown when the caller lacks `PARTNER_MANAGE`, which `listPartnerAgreements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

17 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.7.12 | - Discounts | Ticketing Sales | CONTRACTED | `listPartnerAgreements` |
| 2.7.13 | - Commissions | Ticketing Sales | CONTRACTED | `listPartnerAgreements` |
| 2.7.56 | System shall automatically calculate commissions, incentives, bonuses, overrides, deductions, refunds, and settlement amounts based on partner agreements and sales performance. | Ticketing Sales | CONTRACTED | `getCommissionStatement` |
| 1.1.30 | System shall support corporate ticket allocations, corporate pricing, quotas, approval workflows and corporate account management. | Ticketing Catalogue | CONTRACTED | data `PartnerAgreement` |
| 1.1.102 | Corporate memberships | Ticketing Catalogue | CONTRACTED | data `PartnerAgreement` |
| 1.3.24 | System shall support sponsor packages, sponsor entitlements, sponsorship inventory and sponsor reporting. | Ticketing Catalogue | CONTRACTED | data `PartnerAgreement` |
| 2.7.44 | The system should have the ability to adapt branding and logos on emails and tickets according to B2B client (e.g. co-branded Partner logos to be used on sales through their channels). | Ticketing Sales | CONTRACTED | data `PartnerAgreement` |
| 2.7.48 | The system should offer white label e-commerce engine for B2B sales (internal CMS). The interface of e-commerce engine should have configurable theming: - Color scheme can be updated - Background … | Ticketing Sales | CONTRACTED | data `PartnerAgreement` |
| 2.7.50 | System shall support electronic approval and digital signature workflows for B2B agreements, including approval routing, partner acceptance, version history, timestamping, and document storage. | Ticketing Sales | CONTRACTED | data `PartnerAgreement` |
| 2.7.57 | System shall support partner-specific pricing based on contract terms, tiers, volume thresholds, seasonality, event type, customer segment, product category, negotiated rates, and promotional rules. | Ticketing Sales | CONTRACTED | data `PartnerAgreement` |
| 2.9.15 | System shall support dedicated pricing structures for memberships, annual passes, member-exclusive products, and member-only promotions. | Ticketing Sales | CONTRACTED | data `PartnerAgreement` |
| 2.9.16 | System shall support pricing variations and exclusive pricing benefits based on loyalty tier, status level, and guest segmentation. | Ticketing Sales | CONTRACTED | data `PartnerAgreement` |
| … 5 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-011` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state.
- [ ] Every output is drawn (40 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-011?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create partner quote.
- [ ] Every transition is wired: `PTR-003`.
- [ ] Every gated control is gated: `PARTNER_MANAGE`, `PARTNER_VIEW`.
- [ ] The module and platform inputs below are applied.
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

**2 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"addCartLine": {"method":"POST","path":"/carts/{cartId}/lines","contract":"orders","summary":"Add something","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"AddCartLineRequest","responds":"Cart"},
"allocateBlockedSeats": {"method":"POST","path":"/seat-blocks/{blockId}/allocate","contract":"seating","summary":"Issue seats from a block to a group","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SeatHold"},
"checkoutCart": {"method":"POST","path":"/carts/{cartId}/checkout","contract":"orders","summary":"Turn the cart into an order","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Order"},
"createOrder": {"method":"POST","path":"/orders","contract":"orders","summary":"Create an order","permission":"ORDER_CREATE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateOrderRequest","responds":"Order"},
"createPartnerQuote": {"method":"POST","path":"/partner-quotes","contract":"subscription","summary":"Raise a quote","permission":"PARTNER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PartnerQuote","responds":"PartnerQuote"},
"createSeatBlock": {"method":"POST","path":"/seat-blocks","contract":"seating","summary":"Block seats from sale","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateSeatBlockRequest","responds":"SeatBlock"},
"evaluatePromotions": {"method":"POST","path":"/promotions/evaluate","contract":"promotions","summary":"Evaluate promotions against a cart","permission":"PRICE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"EvaluatePromotionsRequest","responds":"PromotionEvaluation"},
"exchangeOrderLines": {"method":"POST","path":"/orders/{orderId}/exchanges","contract":"orders","summary":"Exchange lines for different products or dates","permission":"ORDER_EXCHANGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ExchangeOrderRequest","responds":"OrderExchangeResult"},
"getCart": {"method":"GET","path":"/carts/{cartId}","contract":"orders","summary":"The cart, priced and checked, right now","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Cart"},
"getCommissionStatement": {"method":"GET","path":"/partner-agreements/{agreementId}/commission-statement","contract":"subscription","summary":"What the partner earned and what is owed","permission":"PARTNER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null}],"requestBody":null,"responds":"CommissionStatement"},
"getOrder": {"method":"GET","path":"/orders/{orderId}","contract":"orders","summary":"Read an order","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Order"},
"getOrderStatement": {"method":"GET","path":"/orders/{orderId}/statement","contract":"orders","summary":"Full financial history of an order","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"OrderStatement"},
"getPromotion": {"method":"GET","path":"/promotions/{promotionId}","contract":"promotions","summary":"Read a promotion","permission":"PRICE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Promotion"},
"getPromotionUsage": {"method":"GET","path":"/promotions/{promotionId}/usage","contract":"promotions","summary":"Redemption count and discount given","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"PromotionUsage"},
"holdOrder": {"method":"POST","path":"/orders/{orderId}/hold","contract":"orders","summary":"Park a sale and free the till","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Order"},
"listOrderRefunds": {"method":"GET","path":"/orders/{orderId}/refunds","contract":"orders","summary":"List refunds against an order","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOrders": {"method":"GET","path":"/orders","contract":"orders","summary":"List orders","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"shiftId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"createdFrom","in":"query","required":null},{"name":"createdTo","in":"query","required":null},{"name":"workstationId","in":"query","required":null},{"name":"subjectId","in":"query","required":null},{"name":"tender","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPartnerAgreements": {"method":"GET","path":"/partner-agreements","contract":"subscription","summary":"Commercial agreements with B2B partners","permission":"PARTNER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"expiringWithinDays","in":"query","required":null},{"name":"status","in":"query","required":null}],"requestBody":null,"responds":"PartnerAgreement"},
"listPartnerQuotes": {"method":"GET","path":"/partner-quotes","contract":"subscription","summary":"Quotes offered to this partner","permission":"PARTNER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"PartnerQuote"},
"listPromotions": {"method":"GET","path":"/promotions","contract":"promotions","summary":"List promotions","permission":"PRICE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"activeAt","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSeatBlocks": {"method":"GET","path":"/seat-blocks","contract":"seating","summary":"List seat blocks","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"performanceId","in":"query","required":null},{"name":"reason","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"modifyOrder": {"method":"POST","path":"/orders/{orderId}/modify","contract":"orders","summary":"Add or remove lines on an existing order","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ModifyOrderRequest","responds":"OrderModificationResult"},
"relinquishSeatBlock": {"method":"DELETE","path":"/seat-blocks/{blockId}","contract":"seating","summary":"Release a block back to sale","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"removeCartLine": {"method":"DELETE","path":"/carts/{cartId}/lines/{lineId}","contract":"orders","summary":"Take something out","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Cart"},
"reprintOrder": {"method":"POST","path":"/orders/{orderId}/reprints","contract":"orders","summary":"Reprint or resend tickets","permission":"ORDER_REPRINT","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"rescheduleOrder": {"method":"POST","path":"/orders/{orderId}/reschedule","contract":"orders","summary":"Move an order to another performance","permission":"ORDER_RESCHEDULE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"OrderExchangeResult"},
"resumeOrder": {"method":"POST","path":"/orders/{orderId}/resume","contract":"orders","summary":"Bring a parked sale back to a till","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"OrderResumeResult"},
"updateCartLine": {"method":"PATCH","path":"/carts/{cartId}/lines/{lineId}","contract":"orders","summary":"Change a quantity","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Cart"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AddCartLineRequest": {"type":"object","x-ticvai-persistence":"none — request only","required":["variantId","quantity"],"properties":{"variantId":{"type":"string","format":"uuid"},"quantity":{"type":"integer","minimum":1},"performanceId":{"type":"string","format":"uuid"},"bookedWindow":{"$ref":"#/components/schemas/BookedWindow"},"recommendationId":{"type":"string","format":"uuid","nullable":true,"description":"The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Optional; sent by a page or till that shows the engine's recommendations. Not validated against the engine: an unknown id only fails to attribute.\n"},"tableReservationId":{"type":"string","format":"uuid","nullable":true,"description":"A table deposit line (decided 29 September, rev 3 REV3-8b): the `fnb.TableReservation` in `awaitingDeposit` this pays for, sent with `variantId` set to the booking's `deposit.variantId` and `quantity` 1. The price is the booking's `deposit.amount`. A booking that is not awaiting a deposit is refused 422 `depositNotDue`.\n"},"seatIds":{"type":"array","maxItems":50,"description":"At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)). Over the limit is 422 `seatLimitExceeded`.","items":{"type":"string","format":"uuid"}},"resourceHoldId":{"type":"string","format":"uuid","nullable":true,"description":"A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant and `quantity` is 1. The hold is the line's capacity; no inventory lease is taken."},"parentLineId":{"type":"string","format":"uuid","nullable":true,"description":"For an add-on attaching to a ticket already in the cart. **Removing the parent removes the child** — a locker with no admission is not a sale.\n"},"attributes":{"$ref":"#/components/schemas/OrderLineAttributes"}}},
"BlockReason": {"type":"string","description":"`other` is allowed only with a note (decided 28 September, audit R222). Every block already requires `note`, so an `other` block always says why; the notes are reviewed quarterly to add the real reasons they reveal.\n","enum":["productionHold","houseSeats","groupAllocation","maintenance","accessibilityReserve","distancing","other"]},
"BookedWindow": {"type":"object","nullable":true,"x-ticvai-persistence":"none — embedded as window_starts_at and window_ends_at on orders.cart_line and orders.order_line","description":"**The booked time window of an hourly product, such as a meeting room** (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). The guest picks a date, a length and a start time from `resources.listProductStartTimes`; the length is the product's `length` variant (1 hour, 2 hours, half day, full day), priced per variant, so the price is the variant's. **`endsAt` minus `startsAt` must equal the chosen variant's length** (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. Required on a product with `catalogue.Product.requiresTimeWindow` true and refused on any other (`windowRequired`, `windowNotAllowed`). The room itself is not named here: the window holds capacity of the room type, and `resources.allocateResources` picks the room at checkout (26 August minute: a guest books a meeting room product, never a raw room).\n","required":["startsAt","endsAt"],"properties":{"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time","description":"After `startsAt`, on the same venue day."}}},
"Cart": {"type":"object","x-ticvai-persistence":"orders.cart","required":["id","venueId","channel","status","lines"],"properties":{"id":{"type":"string","format":"uuid"},"token":{"type":"string","readOnly":true,"description":"**How an anonymous guest returns to their cart**, including from a recovery email. Rotated on claim, so a link shared before signing in does not reach the account after.\n"},"venueId":{"type":"string","format":"uuid"},"channel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"Null while anonymous. Set by `claimCart`."},"status":{"$ref":"#/components/schemas/CartStatus"},"lines":{"type":"array","items":{"$ref":"#/components/schemas/CartLine"}},"conflicts":{"type":"array","items":{"$ref":"#/components/schemas/CartConflict"}},"consentQuestions":{"type":"array","readOnly":true,"description":"**The consent questions this cart's products and flow ask** (decided 29 September, rev 3 REV3-26), computed on read at their current version as **the union of each line's published booking flow's `white-label.BookingFlow.settings.consentQuestionIds`** (the flow `getPublishedBookingFlow` resolves for the line's product: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig`, 29 September W12) **and every line's `catalogue.Product.consentQuestionIds`, each question once**: the flow's first, in its order, then each product's in cart-line order, a question already listed not repeated (its `lineIds` gain the line). The client asks them, in the order given, and sends the answers to `marketing.recordConsentAnswers`; `answered` then turns true. One or several, as the venue chose. `checkoutCart` refuses while a required one is unanswered.\n","items":{"allOf":[{"$ref":"../satellite/marketing-crm.yaml#/components/schemas/ConsentQuestion"},{"type":"object","properties":{"lineIds":{"type":"array","description":"The cart lines that ask it. Empty for a question the flow asks.","items":{"type":"string","format":"uuid"}},"answered":{"type":"boolean","description":"Every person (for `perPerson`) or the booking (for `perBooking`) has an answer."}}}]}},"subtotal":{"x-ticvai-column":"net_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"discountTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"total":{"x-ticvai-column":"gross_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"appliedPromotionIds":{"type":"array","description":"**Re-evaluated on every read.** A promotion that expired while the cart sat must not still be applied at checkout, and a promotion that became applicable should be.\n","items":{"type":"string","format":"uuid"}},"couponCodes":{"type":"array","readOnly":true,"description":"The promo codes the guest entered through `applyCartPromoCode` (decided 28 September, audit R073 (e)). **Sent as `couponCodes` on every promotions evaluation of this cart**, so a code is re-checked on each read like any promotion; a code that stops qualifying stays listed here and its promotion drops out of `appliedPromotionIds`.\n","items":{"type":"string","maxLength":100}},"expiresAt":{"type":"string","format":"date-time","description":"The earliest lease expiry in the cart, or the cart's own window where it holds none."},"extensionsUsed":{"type":"integer","readOnly":true},"maxExtensions":{"type":"integer","readOnly":true},"locale":{"type":"string"},"createdAt":{"type":"string","format":"date-time"},"updatedAt":{"type":"string","format":"date-time"}}},
"CartConflict": {"type":"object","x-ticvai-persistence":"none — computed on read","description":"2.9.5. Golf at 13:00 and karting at 13:00 for the same guest. **A prompt, not a refusal** — a party of four may legitimately split, and refusing would be wrong more often than right.\n","properties":{"kind":{"type":"string","enum":["overlappingTime","sameSessionDifferentVenue","exceedsPartySize","requiresPrerequisite","consentBlocksBooking"]},"lineIds":{"type":"array","items":{"type":"string","format":"uuid"}},"message":{"type":"string"},"isBlocking":{"type":"boolean","description":"Most are not. `requiresPrerequisite` is — an add-on with no ticket to attach to cannot be sold. So is `consentBlocksBooking`: a consent question answered with the answer the venue set to block the booking (decided 29 September, rev 3 REV3-26).\n"}}},
"CartLine": {"type":"object","x-ticvai-persistence":"orders.cart_line","required":["id","variantId","quantity"],"properties":{"id":{"type":"string","format":"uuid"},"variantId":{"type":"string","format":"uuid"},"productName":{"type":"string","readOnly":true},"quantity":{"type":"integer","minimum":1},"performanceId":{"type":"string","format":"uuid","nullable":true},"bookedWindow":{"$ref":"#/components/schemas/BookedWindow"},"recommendationId":{"type":"string","format":"uuid","nullable":true,"description":"The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Set from `addCartLine`; checkout copies it to the order line.\n"},"tableReservationId":{"type":"string","format":"uuid","nullable":true,"description":"Set on a table deposit line only (decided 29 September, rev 3 REV3-8b): the `fnb.TableReservation` this line secures. Priced from the deposit the booking snapshotted, not from the variant. Becomes an `orders.deposit` row at checkout, not revenue. A table booking with no deposit never has a line (rev 3 REV3-8).\n"},"seatIds":{"type":"array","maxItems":50,"items":{"type":"string","format":"uuid"}},"resourceHoldId":{"type":"string","format":"uuid","nullable":true,"description":"The `resources.ResourceHold` this line buys (decided 29 September, rev 3 REV3-15). While set, `leaseExpiresAt` is the hold's `expiresAt` and `inventoryHoldId` is null."},"attributes":{"$ref":"#/components/schemas/OrderLineAttributes"},"parentLineId":{"type":"string","format":"uuid","nullable":true,"description":"The line this add-on is attached to, from `AddCartLineRequest.parentLineId`. Kept on the line because **removing the parent removes the child**, and `removeCartLine` has to be able to find the children.\n"},"overridePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"overrideReason":{"type":"string","nullable":true,"enum":["priceMatch","serviceRecovery","negotiated","damagedGoods","staffSale","error"],"description":"BL-085. **An operator could apply an approved discount and not enter a price.** A price match against a competitor and a service-recovery gesture are not discounts off a list — they are a number somebody decided.\n**Escalated above a configured threshold, and the reason is a closed set**: a free-text override reason is an override nobody can report on, and this is the field an auditor reads first.\n"},"feeKind":{"type":"string","nullable":true,"enum":["booking","transaction","service","delivery","convenience","cancellation"],"description":"**A fee is a line, not an adjustment.** `orders` already separates a service charge from a tip for the reason that applies here: **a guest is entitled to see what they are being charged for**, and a fee folded into the ticket price is a fee nobody can question.\nItemised at checkout, taxed on its own code, and refundable separately — **a cancellation fee is usually the one thing not refunded**, which only works if it is its own line.\n"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lineTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"inventoryHoldId":{"type":"string","nullable":true,"description":"The capacity held for this line — a `catalogue.InventoryHold.id`, typed as that id is. **Null for a product with no capacity** — a t-shirt needs stock, not a lease.\n"},"leaseExpiresAt":{"type":"string","format":"date-time","nullable":true,"description":"Shown to the guest. *\"Your seats are held for 6 minutes\"* is better than discovering it at checkout.\n"},"isAvailable":{"type":"boolean","readOnly":true,"description":"Re-checked on every read. **A line can become unavailable while the cart sits** — a lease expiring is not the same as the product selling out, and both land here.\n"}}},
"CartStatus": {"type":"string","enum":["active","expiring","expired","abandoned","checkedOut"]},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"CommissionStatement": {"type":"object","x-ticvai-persistence":"none — aggregated from orders and control.partner_agreement","properties":{"agreementId":{"type":"string","format":"uuid"},"partnerName":{"type":"string"},"from":{"type":"string","format":"date"},"to":{"type":"string","format":"date"},"currency":{"type":"string"},"grossSales":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refunds":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netSales":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"commissionEarned":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"amountDue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lines":{"type":"array","description":"**Reconcilable order by order.** A statement a partner cannot check line by line is a statement they will dispute, and the dispute costs more than the detail.\n","items":{"type":"object","properties":{"orderId":{"type":"string","format":"uuid"},"orderNumber":{"type":"string"},"soldAt":{"type":"string","format":"date-time"},"agreementVersion":{"type":"integer","description":"The version in force at the time of that sale, not the current one."},"gross":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"commission":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"isRefunded":{"type":"boolean"}}}}}},
"CreateOrderLine": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","variantId","quantity","quotedUnitPrice"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these."},"variantId":{"type":"string","format":"uuid"},"recommendationId":{"type":"string","format":"uuid","nullable":true,"description":"The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Carried from the cart line at checkout; stored on `orders.order_line` and sent in `order.completed` lines.\n"},"performanceId":{"type":"string","format":"uuid"},"bookedWindow":{"$ref":"#/components/schemas/BookedWindow"},"inventoryHoldId":{"type":"string","nullable":true,"description":"Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products."},"seatIds":{"type":"array","maxItems":50,"items":{"type":"string","format":"uuid"},"description":"Seated products only, as `seating.Seat.id`. Not available offline. **At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel** (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); **at most 10 per sale on staff and POS** (audit R080 (c)), across all the lines of one order for one performance. `createOrder` refuses more with 422 `seatLimitExceeded` (problem type `seat-limit-exceeded`)."},"resourceHoldId":{"type":"string","format":"uuid","nullable":true,"description":"A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. `createOrder` converts the hold into a `ResourceBooking` without releasing it. Not available offline."},"attributes":{"$ref":"#/components/schemas/OrderLineAttributes"},"quantity":{"type":"integer","minimum":1},"eligibilityDeclaration":{"type":"array","nullable":true,"x-ticvai-note":"One row per declared guest in `orders.order_line_eligibility` (named on `OrderLine`), because an array of objects is a child table's rows, not a column.\n","items":{"type":"object","properties":{"ageBand":{"type":"string","enum":["infant","child","junior","adult","senior"],"description":"Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+."},"ageYears":{"type":"integer","nullable":true},"heightBandIndex":{"type":"integer","nullable":true},"confidentSwimmer":{"type":"boolean","nullable":true,"description":"**Derived, kept for the gate check** (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this is filled from it (true for a `yes` covering this person, whether answered for them or once for the booking). A value sent that contradicts the record is ignored and the record wins. No longer the place a swim answer is captured.\n"},"guardianSigned":{"type":"boolean"}}},"description":"What was declared for each guest on this line, kept as the record staff check at the gate."},"quotedUnitPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the client charged, from its local bundle."},"holderName":{"type":"string","nullable":true},"dataMaskValues":{"type":"object","additionalProperties":true,"description":"**Deliberately open.** Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the venue's to define, as on `catalogue`'s own `dataMaskValues`.\n"}}},
"CreateOrderRequest": {"type":"object","required":["id","venueId","channel","lines","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7. Also the idempotency key: it must equal the `Idempotency-Key` header, and a replay or a mismatch follows `IdempotencyKey` in `shared/common.yaml`. Offline replay through `syncOrders` carries no header, and this id alone deduplicates there.\n"},"venueId":{"type":"string","format":"uuid"},"channel":{"$ref":"#/components/schemas/Channel"},"shiftId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"Null for an anonymous sale. Identity and entitlement are separate."},"guestLinkId":{"type":"string","nullable":true,"description":"Present where the guest is linked across cells."},"catalogueBundleVersion":{"type":"string","description":"The bundle the client priced from. Lets the server explain a variance rather than merely report one.\n"},"lines":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/CreateOrderLine"}},"recordedAt":{"type":"string","format":"date-time"}}},
"CreatePromotionRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["code","name","venueId","discount","validFrom"],"properties":{"code":{"type":"string","maxLength":64,"pattern":"^[A-Za-z0-9_-]+$"},"name":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":1000},"venueId":{"type":"string","format":"uuid"},"discount":{"$ref":"#/components/schemas/Discount"},"conditions":{"$ref":"#/components/schemas/PromotionConditions"},"stackingMode":{"allOf":[{"$ref":"#/components/schemas/StackingMode"}],"default":"bestOnly"},"stackingGroup":{"type":"string","maxLength":64},"precedence":{"type":"integer","default":0,"description":"Higher evaluates first where several could apply."},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"maxRedemptions":{"type":"integer","nullable":true},"maxRedemptionsPerGuest":{"type":"integer","nullable":true},"budgetCap":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Total discount value after which the promotion stops automatically. **Enforced at checkout**, where an order whose discount would take the total past the cap does not receive the promotion (decided 28 September, audit R101)."},"campaignId":{"type":"string","format":"uuid","nullable":true,"description":"The commercial campaign (`promotions.campaign`) this promotion belongs to; null for a promotion run on its own. The directory, calendar and campaign budget screens group by it. (DM5, 29 September: data model for the agreed operations)"},"recommendable":{"type":"boolean","default":false,"description":"**May the recommendation engine show this offer to a guest** (8.6.30 to 8.6.36; 29 September, build pass, group G2, from group G1's handoff). False keeps a promotion to the basket, where `evaluatePromotions` applies it as before. True makes a live promotion a candidate item of kind `offer` in `ai.decideRecommendations` for the guests its conditions and `recommendableSegmentIds` admit: while it is live, `promotions.recommendationStrategyPublished` (kind `offers`) keeps the engine's candidate cache current, and it leaves the cache when it is paused, ends or expires. **The engine shows the offer; the discount is still computed here at the basket**, never by ai."},"recommendableSegmentIds":{"type":"array","nullable":true,"description":"The marketing-crm segments the offer may be recommended to; null means every guest its own conditions admit.","items":{"type":"string","format":"uuid"}}}},
"CreateSeatBlockRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["performanceId","seatIds","reason","note"],"properties":{"performanceId":{"type":"string","format":"uuid"},"seatIds":{"type":"array","minItems":1,"items":{"type":"string"}},"reason":{"$ref":"#/components/schemas/BlockReason"},"note":{"type":"string","minLength":3,"maxLength":500},"releaseAt":{"type":"string","format":"date-time","description":"Automatic release, for production holds freed close to performance."}}},
"Discount": {"x-ticvai-persistence":"none — embedded in promotion","type":"object","required":["kind"],"properties":{"kind":{"$ref":"#/components/schemas/DiscountKind"},"percentage":{"type":"number","minimum":0,"maximum":100},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"fixedPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"buyQuantity":{"type":"integer","minimum":1},"getQuantity":{"type":"integer","minimum":1},"getDiscountPercentage":{"type":"number","minimum":0,"maximum":100,"description":"100 makes the free items actually free; lower values give a partial discount."},"tiers":{"type":"array","description":"For `tieredPercentage` — more units, larger discount.","items":{"type":"object","required":["minQuantity","percentage"],"properties":{"minQuantity":{"type":"integer","minimum":1},"percentage":{"type":"number","minimum":0,"maximum":100}}}},"maxDiscountAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Cap on a percentage discount. Prevents an unbounded discount on a large basket."},"rewardVariantIds":{"type":"array","nullable":true,"items":{"type":"string","format":"uuid"},"description":"The reward products, where the reward is not the qualifying product: the free gift of `freeItem`, the \"different product\" of a `buyXGetY` (createPromotion; the builders setGiftFreeProduct and setBuyGetBogo were retired in r2, CHG-CLN-001). Absent means the reward is taken from the qualifying lines. (DM5, 29 September: data model for the agreed operations)"},"maxApplicationsPerBasket":{"type":"integer","minimum":1,"nullable":true,"description":"How many times the offer repeats in one basket: the \"maximum repetitions\" of an N-for-X offer (createPromotion; setFixedPriceOffer was retired in r2, CHG-CLN-001). Null repeats for every complete set. (DM5, 29 September: data model for the agreed operations)"}}},
"EvaluatePromotionsRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["venueId","channel","lines"],"properties":{"venueId":{"type":"string","format":"uuid"},"channel":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"}],"description":"Where the sale is being made. Matched against `PromotionConditions.channels`, so both sides use the one shared vocabulary.\n"},"subjectId":{"type":"string","format":"uuid"},"membershipTierId":{"type":"string","format":"uuid"},"couponCodes":{"type":"array","items":{"type":"string"}},"evaluateAt":{"type":"string","format":"date-time","description":"For back-office testing of a rule before publishing."},"orderId":{"type":"string","format":"uuid","nullable":true,"description":"The order (`orders.sales_order`) being priced for payment. Sent only by the order service when it confirms an order; when present the evaluation writes one `promotions.promotion_evaluation_trace` row for it. (decided 29 September, writers pass)"},"lines":{"type":"array","minItems":1,"items":{"type":"object","required":["lineId","variantId","quantity","unitPrice"],"properties":{"lineId":{"type":"string"},"variantId":{"type":"string","format":"uuid"},"performanceId":{"type":"string","format":"uuid"},"quantity":{"type":"integer","minimum":1},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}}}},
"ExchangeOrderRequest": {"type":"object","required":["id","outgoingLineIds","incomingLines","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of this exchange, and its idempotency key — it must equal the `Idempotency-Key` header."},"outgoingLineIds":{"type":"array","minItems":1,"items":{"type":"string","format":"uuid"}},"incomingLines":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/CreateOrderLine"}},"waiveFee":{"type":"boolean","default":false},"reason":{"type":"string","maxLength":500},"recordedAt":{"type":"string","format":"date-time"}}},
"ExchangeRateDecimal": {"type":"string","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,6)","description":"**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one — a JavaScript client must not round a rate in transit. **Six decimal places**, the precision `finance.FxRate.rate` asks for, and stored at that precision.\n","pattern":"^\\d+(\\.\\d{1,6})?$"},
"GuestPromotion": {"x-ticvai-persistence":"none — guest projection of promotions.promotion","type":"object","description":"**What a guest may see of a promotion.** `Promotion` carries the commercial internals (`budgetCap`, `maxRedemptions`, `redemptionCount`, `discountGiven`, `precedence`, `stackingGroup`), and `listPromotions` and `getPromotion` are guest-audience. A guest caller receives this shape instead. `additionalProperties: false` is the point: a server that adds an internal field to it fails validation instead of publishing the field.\n","additionalProperties":false,"required":["id","code","name","discount","validFrom"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"description":{"type":"string"},"discount":{"$ref":"#/components/schemas/Discount"},"conditions":{"$ref":"#/components/schemas/PromotionConditions"},"stackingMode":{"$ref":"#/components/schemas/StackingMode"},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"maxRedemptionsPerGuest":{"type":"integer","nullable":true}}},
"ModifyOrderRequest": {"type":"object","required":["id","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 **of this modification, not of the order** — the order is the path's `orderId`. It is the modification's idempotency key and must equal the `Idempotency-Key` header.\n"},"addLines":{"type":"array","items":{"$ref":"#/components/schemas/CreateOrderLine"}},"removeLineIds":{"type":"array","items":{"type":"string","format":"uuid"}},"reason":{"type":"string","maxLength":500},"recordedAt":{"type":"string","format":"date-time"}}},
"Order": {"x-ticvai-persistence":"orders.sales_order + orders.order_line","type":"object","required":["id","venueId","scopePath","channel","status","currency","currencyScale","grossAmount","taxAmount","netAmount","lines","createdAt","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The client UUIDv7 from `CreateOrderRequest.id`."},"orderNumber":{"type":"string","readOnly":true,"description":"The number a guest reads and a cashier types. **Server-assigned: the venue prefix and a sequence per venue**, for example `DXB1-000123` (decided 28 September, audit R152). A till holds a reserved range of the venue sequence, so an order taken offline gets its number on the till and keeps it through `syncOrders`. **Not gapless**: an unused reserved range leaves a gap, and that is allowed. Only tax invoices are gapless, per legal entity. The receipt carries this number.\n"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for within a month of launch.\n"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"chargeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**The currency the guest selected and is charged in** (CHG-FIN-001, 2 October 2026). Null or equal to `currency` for a sale in the base currency. Everything else on the order, and every ledger posting, stays in the base currency `currency`."},"chargeFxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"readOnly":true,"description":"Units of `chargeCurrency` per one unit of the base currency, from the region's `tender` rate in force at checkout (`finance.FxRate`), stored on the order so the payment, the receipt, the tax invoice and any refund use the same rate (CHG-FIN-001)."},"chargeFxRateId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `finance.FxRate` row the rate was taken from, for audit."},"chargeTotal":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"`grossAmount` converted at `chargeFxRate` and rounded to the charge currency's scale: what the guest pays and what the payment request to the provider asks for (CHG-FIN-001)."},"chargeRateLockedUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"The quote holds until then (the cart lease). After it, the next payment attempt re-quotes at the rate then in force and the guest confirms the new amount (CHG-FIN-001)."},"droppedPromotions":{"type":"array","readOnly":true,"x-ticvai-persisted":false,"description":"**Promotions left off this order at checkout because their budget cap would have been exceeded** (decided 28 September, audit R101 (8)). Empty when none was dropped. Returned by `checkoutCart` and `createOrder`, not stored.\n","items":{"type":"object","required":["promotionId"],"properties":{"promotionId":{"type":"string","format":"uuid"},"name":{"type":"string"},"reason":{"type":"string","enum":["budgetCapReached"]}}}},"totalPriceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Sum across lines. Zero on a normal order."},"lines":{"type":"array","items":{"$ref":"#/components/schemas/OrderLine"}},"payments":{"type":"array","items":{"$ref":"#/components/schemas/Payment"}},"principalId":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid"},"shiftId":{"type":"string","format":"uuid","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"holdLabel":{"type":"string","maxLength":60,"nullable":true,"readOnly":true,"description":"The `label` a cashier gave when parking it with `holdOrder` — how they find it again. Null on an order never held."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When a held order expires and is voided (states/order.yaml), from `holdOrder`'s `holdUntil`. Null on an order not currently held."},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"OrderChannel": {"type":"string","description":"Where the order originated. Added when guest self-ordering was contracted — an order a guest placed on their own phone is commercially and operationally different from one a cashier typed, and reporting that cannot separate them cannot answer whether self-ordering is working.\n","enum":["pos","kiosk","guestApp","guestWeb","callCentre","partner","api","backOffice"]},
"OrderExchangeResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["orderId","outgoingValue","incomingValue","difference"],"properties":{"orderId":{"type":"string","format":"uuid"},"outgoingValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"incomingValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"exchangeFee":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"difference":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Only the difference settles. The replacement is held before the original is released, never the other way round.\n"},"newLineIds":{"type":"array","items":{"type":"string","format":"uuid"}},"revokedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}},"issuedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"OrderLine": {"x-ticvai-persistence":"orders.order_line + orders.order_line_eligibility + orders.order_line_discount","x-ticvai-retired-columns":["promotion_id","name","reason"],"allOf":[{"$ref":"#/components/schemas/CreateOrderLine"},{"type":"object","required":["serverUnitPrice","taxAmount","netAmount","grossAmount"],"properties":{"serverUnitPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the server computed on ingest."},"priceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Server minus quoted. Non-zero means the quoted price was honoured and the difference posted to the variance account.\n"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"entitlementIds":{"type":"array","description":"The entitlements this line issued. **These are the ticket ids** — `transferOrderTickets.ticketIds` and `reprintOrder.reissuedTicketIds` take and return them.","items":{"type":"string","format":"uuid"}},"crossRegionRightIds":{"type":"array","items":{"type":"string"},"description":"Redemption rights propagated to other cells for this line."},"reprintCount":{"type":"integer","minimum":0,"default":0,"readOnly":true,"description":"How many times this line's tickets were reprinted or resent. `reprintOrder` increments it; repeated reprints are the signal worth surfacing."},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"The order's venue, copied onto the line (ADR-0044's own example; system-design review SD-008, 29 September) so a line is scoped and partitionable without its order."},"discounts":{"type":"array","readOnly":true,"description":"**The discounts applied to this line, one row each** (system-design review SD-008, 29 September). Until then a discount object was flattened into the line as `promotion_id NOT NULL`, so a line with no promotion could not be inserted. A line with no discount has none.","items":{"$ref":"#/components/schemas/OrderLineDiscount"}}}}]},
"OrderLineAttributes": {"type":"object","nullable":true,"additionalProperties":true,"x-ticvai-persistence":"none — embedded as attributes (jsonb) on orders.cart_line and orders.order_line","description":"Open attributes of a line, kept from the cart to the order line. **`transport` is the one with a defined shape** (decided 29 September, rev 3 REV3-21); other keys are free.\n","properties":{"transport":{"$ref":"#/components/schemas/TransportLineAttributes"}}},
"OrderModificationResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["order","balanceDue"],"properties":{"order":{"$ref":"#/components/schemas/Order"},"addedValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"removedValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"balanceDue":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Positive means the guest pays; negative means a refund is due."},"refundId":{"type":"string","format":"uuid","nullable":true},"revokedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}},"issuedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"OrderResumeResult": {"type":"object","x-ticvai-persistence":"none — computed","required":["order","hasChanged"],"properties":{"order":{"$ref":"#/components/schemas/Order"},"hasChanged":{"type":"boolean","description":"True where anything moved while the sale was parked. The cashier decides — silently charging the old price loses money, silently charging the new one loses the guest.\n"},"changes":{"type":"array","items":{"type":"object","properties":{"kind":{"type":"string","enum":["priceChanged","promotionExpired","promotionNowApplies","soldOut","seatHoldExpired","productWithdrawn"]},"lineId":{"type":"string","format":"uuid"},"detail":{"type":"string"},"wasAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"nowAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}}}},
"OrderStatement": {"x-ticvai-persistence":"none — computed from order, payment, refund and ledger","type":"object","required":["orderId","orderNumber","currency","entries","currentBalance"],"properties":{"orderId":{"type":"string","format":"uuid"},"orderNumber":{"type":"string"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"entries":{"type":"array","description":"Sequential. What an agent reads to a guest asking about a charge.","items":{"type":"object","required":["kind","amount","runningBalance","occurredAt"],"properties":{"kind":{"type":"string","enum":["sale","payment","refund","void","modification","exchange","fee","variance","chargeback"]},"description":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"runningBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"referenceId":{"type":"string","nullable":true},"principalId":{"type":"string","format":"uuid","nullable":true},"occurredAt":{"type":"string","format":"date-time"}}}},"totalPaid":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"totalRefunded":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"currentBalance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Positive means the guest owes; negative means a refund is outstanding."}}},
"OrderStatus": {"type":"string","enum":["pending","held","paid","partiallyPaid","completed","voided","refunded","partiallyRefunded","failed"],"description":"`held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed.\n"},
"OrderSummary": {"x-ticvai-persistence":"none — projection","type":"object","required":["id","orderNumber","status","grossAmount","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderNumber":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"The same vocabulary as `Order.channel`, which this projects."},"lineCount":{"type":"integer"},"principalId":{"type":"string","format":"uuid","description":"The cashier who raised it — what the held-orders list shows."},"holdLabel":{"type":"string","nullable":true,"description":"As `Order.holdLabel`."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"description":"As `Order.heldUntil`, so a held-orders list can warn about the ones about to lapse."},"createdAt":{"type":"string","format":"date-time"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PartnerAgreement": {"type":"object","x-ticvai-persistence":"control.partner_agreement","x-ticvai-retired-columns":["partner_name"],"required":["partnerId","rateMode","validFrom"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"partnerId":{"x-ticvai-references":"control.partner","type":"string","format":"uuid","description":"The partner (control.partner) this agreement is with. The agreement carries the terms; control.partner carries who the partner is and whether it may trade. **Resolves to control.partner**, not to platform.tenant as the naming convention guessed before the partner master existed (decided 29 September, writers pass; DM4)"},"partnerName":{"type":"string","readOnly":true,"x-ticvai-persisted":false,"description":"The partner's trading name, **read from control.partner.trading_name** (Partner.tradingName) when the agreement is returned and never stored on the agreement, so a renamed partner cannot show two names (decided 29 September, writers pass; DM4)"},"version":{"type":"integer","readOnly":true,"description":"**Amending creates a version.** An order placed last week was placed under last week's rate, and settlement must be able to say which.\n"},"status":{"$ref":"#/components/schemas/PartnerAgreementStatus"},"rateMode":{"$ref":"#/components/schemas/PartnerRateMode"},"commissionPercent":{"type":"number","nullable":true},"volumeTiers":{"type":"array","deprecated":true,"x-ticvai-persisted":false,"description":"**Retired: the tiers are rows of control.partner_rate_volume_band** (`PartnerRate.volumeBands`, written by setPartnerRateNet), one set per rate row, so a tier can differ by product, venue or channel. Accepted and ignored on write; not returned once the bands exist. `volumeWindow` below still says over which window the bands count (decided 29 September, writers pass; DM4).\n\n2.7.57. **A tier that changes at a threshold needs the sale to look back at cumulative volume, and nothing did.** Flat net rates and per-channel price lists cover the simple case and stop there.\n**The window is the argument, not the tier.** A partner who sells 400 in January and 400 in February is either a 400-tier partner twice or an 800-tier partner once, and the two are different money. `volumeWindow` says which.\n","items":{"type":"object","required":["fromUnits","commissionPercent"],"properties":{"fromUnits":{"type":"integer"},"commissionPercent":{"type":"number"},"appliesRetrospectively":{"type":"boolean","default":false,"description":"**Whether crossing a tier reprices what came before it.** Retrospective is what a partner assumes and prospective is what a venue budgets for — it has to be stated.\n"}}}},"volumeWindow":{"type":"string","nullable":true,"enum":["calendarMonth","calendarQuarter","calendarYear","agreementYear","rolling12Months"]},"seasonalRates":{"type":"array","deprecated":true,"x-ticvai-persisted":false,"description":"**Retired: a seasonal rate is a control.partner_rate row** with `seasonalRate: true` and its own `effectiveFrom`/`effectiveTo` (`PartnerRate`, written by setPartnerRateNet); the most specific row in force wins. Accepted and ignored on write (decided 29 September, writers pass; DM4).\n\nRates that change by date range. **Separate from the volume tier because they compound** — a peak-season rate at a high volume tier is both, and a single rate table cannot say so.\n","items":{"type":"object","properties":{"from":{"type":"string","format":"date"},"to":{"type":"string","format":"date"},"commissionPercent":{"type":"number"}}}},"segmentTier":{"type":"string","nullable":true},"brandingAssetId":{"type":"string","format":"uuid","nullable":true,"description":"2.7.x, BL-078. **A reseller selling a venue's tickets under their own brand is a second scope level white-label does not have** — `BrandIdentity` and `setTheme` are tenant-scoped throughout.\n**Co-branding rather than replacement.** The venue's identity stays on the ticket because the ticket admits to the venue; the partner's sits beside it.\n"},"storefrontSubdomain":{"type":"string","nullable":true},"sponsorship":{"type":"object","nullable":true,"description":"BL-050. **Sponsorship inventory is sellable capacity of a different kind** — logo placements, hospitality allocations, naming rights. It is closer to a partner agreement than to a product: **a sponsor buys a relationship for a season, not a ticket for a date.**\nModelled here rather than as a `ProductKind` because the commercial terms — the term, the exclusivity, the settlement — are the agreement's, and duplicating them onto a product would mean two places to disagree.\n","properties":{"placements":{"type":"array","items":{"type":"object","properties":{"surface":{"type":"string","enum":["signage","ticketFace","appBanner","emailFooter","venueNaming","zoneNaming","uniform","printedMap"]},"quantity":{"type":"integer"},"exclusive":{"type":"boolean","default":false,"description":"**Exclusivity is the expensive word.** A sponsor paying for category exclusivity has bought the absence of a competitor, and a second agreement breaching it is a legal problem rather than a scheduling one.\n"}}}},"hospitalityAllocation":{"type":"integer","nullable":true,"description":"Tickets or cabanas included. **Issued as invitations, not sales** — no revenue attaches."},"categoryExclusivity":{"type":"string","nullable":true}}},"netRates":{"type":"array","deprecated":true,"x-ticvai-persisted":false,"description":"**Retired: net rates are rows of control.partner_rate** (`PartnerRate` with `pricingModel: netRate`, `netRate` and the `maxDiscountPercent` guardrail), written by setPartnerRateNet. Per product or category; absent means the commission applies across the catalogue. Accepted and ignored on write (decided 29 September, writers pass; DM4)","items":{"type":"object","properties":{"productId":{"type":"string","format":"uuid","nullable":true},"categoryId":{"type":"string","format":"uuid","nullable":true},"netPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"maxDiscountPercent":{"type":"number","nullable":true,"description":"1.6.10. **What the partner may not undercut.** A reseller selling below the venue's own price damages the direct channel, and the venue usually cares more about that than the margin.\n"}}}},"creditTermDays":{"type":"integer","description":"2.7.36. Net 30, net 60. Drives when an invoice becomes overdue."},"acceptedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"BL-079. **Electronic acceptance against a version**, following the `signatureRef` precedent. An agreement accepted with no version recorded is an agreement nobody can produce in a dispute.\n"},"acceptedVersion":{"type":"integer","nullable":true},"acceptedAt":{"type":"string","format":"date-time","nullable":true},"signatureRef":{"type":"string","nullable":true},"corporateAllocations":{"type":"array","deprecated":true,"x-ticvai-persisted":false,"description":"**Retired: allocations are rows of control.partner_allocation** (`PartnerAllocation`, written by setPartnerAllocations and read by listCommercialAllocationQuota); used quantity is counted from orders against the row, not stored. Accepted and ignored on write (decided 29 September, writers pass; DM4).\n\nBL-035. **`PartnerAgreement` covered commercial terms and not allocations.** A corporate account with fifty places for its staff is the same structure as a reseller with fifty to sell, and **the difference is that a corporate member does not pay.**\n","items":{"type":"object","properties":{"productId":{"type":"string","format":"uuid"},"quantity":{"type":"integer"},"usedQuantity":{"type":"integer","readOnly":true},"perMemberLimit":{"type":"integer","nullable":true},"validTo":{"type":"string","format":"date","nullable":true}}}},"settlementCurrency":{"type":"string","pattern":"^[A-Z]{3}$","description":"**The currency this partner is billed and settles in**, which is often not the venue's. A UK tour operator selling a Dubai attraction is invoiced in GBP against sales booked in AED, and the difference is somebody's exposure.\n**`creditLimit` and `netRates` are expressed in this currency**, not the venue's — a limit in the wrong currency is a limit that moves with the exchange rate.\n"},"fxPolicy":{"type":"string","enum":["rateAtSale","rateAtInvoice","fixedRate"],"default":"rateAtSale","description":"**Which rate converts a sale into the settlement currency, and it is a commercial term.** `rateAtSale` puts the movement on the partner; `rateAtInvoice` puts it on the venue; `fixedRate` puts it on whoever guessed wrong when the agreement was signed.\n**Not a default to leave alone** — on a monthly statement across a moving rate the three produce materially different numbers, and the partner will have assumed one of them.\n"},"fixedRate":{"type":"number","nullable":true,"description":"Where `fxPolicy` is `fixedRate`. **An amendment creates a version** so an old statement stays readable."},"creditLimit":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"allowedChannels":{"type":"array","items":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"}},"allowedVenueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"requiresApprovalAboveValue":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"2.7.39. Routes through `approvals` rather than a second mechanism here."},"validFrom":{"type":"string","format":"date"},"validTo":{"type":"string","format":"date","nullable":true,"description":"2.7.37. **An agreement that lapses silently keeps selling at rates nobody agreed to**, discovered at settlement rather than at sale. Null means open-ended, which should be rare and deliberate.\n"},"expiryAlertDays":{"type":"integer","default":30},"approvalRequestId":{"type":"string","nullable":true,"readOnly":true},"notes":{"type":"string"},"agreementName":{"type":"string","nullable":true,"description":"Agreement name (decided 29 September, data model DM4)"},"agreementType":{"type":"string","nullable":true,"description":"Agreement type code, seeded with reseller, ota, travelTrade, corporate, wholesale, affiliate, distribution, apiCommercial (pack p.26) (decided 29 September, data model DM4)"},"contractReference":{"type":"string","nullable":true,"description":"Contract reference (decided 29 September, data model DM4)"},"legalEntityId":{"type":"string","format":"uuid","nullable":true,"description":"The contracting legal entity (ledger.legal_entity) (decided 29 September, data model DM4)"},"brandId":{"type":"string","format":"uuid","nullable":true,"description":"Brand the agreement covers; empty for every brand of the tenant (decided 29 September, data model DM4)"},"territory":{"type":"string","nullable":true,"description":"Territory (decided 29 September, data model DM4)"},"commercialOwnerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Commercial owner, a staff principal (decided 29 September, data model DM4)"},"financeOwnerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Finance owner, a staff principal (decided 29 September, data model DM4)"},"pricingBasis":{"type":"string","enum":["retailPrice","netRate","discountFromRetail","markup","derivedRate"],"nullable":true,"description":"Pricing basis (pack p.27 pricing models); the rows are `control.partner_rate` (decided 29 September, data model DM4)"},"paymentModel":{"type":"string","enum":["creditAccount","prepaid","payPerTransaction"],"nullable":true,"description":"Payment model, the three confirmed at MoM 5 Aug and MoM 31 Aug 4.4: creditAccount (sells to an approved credit ceiling, invoiced periodically), prepaid (pre-funded wallet drawn down per sale) or payPerTransaction (card at each sale). Held here once; the billing screen reads and sets this column (decided 29 September, data model DM4)"},"renewalType":{"type":"string","enum":["manual","auto"],"nullable":true,"description":"Renewal type (decided 29 September, data model DM4)"},"renewalNoticeDays":{"type":"integer","minimum":0,"nullable":true,"description":"Renewal notice period in days (decided 29 September, data model DM4)"},"renegotiationRequired":{"type":"boolean","default":false,"description":"Renegotiation required before renewal (decided 29 September, data model DM4)"},"renewalRequiresApproval":{"type":"boolean","description":"Renewal needs approval (decided 29 September, data model DM4)"},"minimumCommitment":{"type":"integer","minimum":0,"nullable":true,"description":"Minimum commitment: tickets over the agreement term (decided 29 September, data model DM4)"},"salesTarget":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Sales target over the agreement term (decided 29 September, data model DM4)"},"agreementValue":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Agreement value (MoM 31 Aug 4.4: each agreement captures term/value) (decided 29 September, data model DM4)"},"commissionTerms":{"type":"string","nullable":true,"description":"Commission terms as written in the contract; the rules that compute it are `control.partner_commission_rule` (decided 29 September, data model DM4)"},"creditTerms":{"type":"string","nullable":true,"description":"Credit terms as written in the contract (decided 29 September, data model DM4)"},"allocationTerms":{"type":"string","nullable":true,"description":"Allocation terms as written in the contract; the allocations are `control.partner_allocation` (decided 29 September, data model DM4)"},"cancellationConditions":{"type":"string","nullable":true,"description":"Cancellation conditions (decided 29 September, data model DM4)"},"refundConditions":{"type":"string","nullable":true,"description":"Refund conditions (pack p.26) (decided 29 September, data model DM4)"},"bookingRestrictions":{"type":"string","nullable":true,"description":"Booking restrictions as written in the contract; the enforced limits are `control.partner_booking_limit` (decided 29 September, data model DM4)"},"settlementTerms":{"type":"string","nullable":true,"description":"Settlement terms (decided 29 September, data model DM4)"},"scopePath":{"type":"string","description":"The partition key (ADR-0005), written at `tenant` scope, as every control.partner_* row carries it, so row-level security scopes the agreement the same way (decided 29 September, writers pass; DM4)"}}},
"PartnerAgreementStatus": {"type":"string","enum":["pendingApproval","active","expiringSoon","expired","suspended","terminated"]},
"PartnerQuote": {"type":"object","x-ticvai-persistence":"subscription.partner_quote","description":"**Drafted 4 September.** A priced offer to a partner, with an expiry. **Not the same as a procurement quotation** - `inventory.quotation` is what a supplier offers this venue, and this is what this venue offers a reseller.","required":["id"],"properties":{"id":{"type":"string","format":"uuid"},"partnerId":{"type":"string","format":"uuid"},"agreementId":{"type":"string","format":"uuid"},"currency":{"type":"string","x-ticvai-persisted":false,"description":"**Not stored on the row.** Currency is region-scoped and resolves from the scope walk (ADR-0018); a quote that carries its own copy is a quote that disagrees with the region the moment one of them changes."},"totalMinor":{"type":"integer"},"state":{"type":"string","enum":["draft","sent","accepted","declined","expired"]},"validUntil":{"type":"string","format":"date-time","description":"**Stored, not calculated** - an offer whose expiry moves when you read it is not an offer."},"createdAt":{"type":"string","format":"date-time"}}},
"PartnerRateMode": {"type":"string","description":"**Alternatives, not both.** A partner buys at a net rate and keeps the margin, or sells at face value and is paid commission. Both is being paid twice for the same sale.\n","enum":["netRate","commission"]},
"Payment": {"x-ticvai-persistence":"orders.payment","type":"object","required":["id","orderId","tender","amount","status","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid"},"tender":{"$ref":"#/components/schemas/TenderKind"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","description":"4.6.11. **What the guest actually handed over**, which is not always what the venue books. A tourist paying USD cash at a till is a foreign tender; the sale is still recorded in base currency.\nEqual to the base currency for almost every payment. **Present on all of them so the foreign-tender report has a source** — `getForeignTenderReport` promised *what was taken in which currency* and nothing recorded it until 18 August.\n"},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"The amount in `tenderCurrency`, at that currency's own scale."},"fxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"description":"The rate applied, **stored on the payment rather than looked up later** (CF-37). A payment reconciled next month is reconciled at the rate of the day it was taken.\n"},"fxRateSource":{"type":"string","nullable":true,"enum":["manual","feed","cardScheme"],"description":"4.2.8. Manual or fed on a schedule. **`cardScheme` is where the terminal did the conversion and told us** — dynamic currency conversion, the scheme's rate rather than ours.\n"},"changeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"description":"4.6.11 is deliberately asymmetric: **accept foreign currency, refund in local.** A till giving change in five currencies needs five floats and five counts, and the variance becomes unattributable.\n**Cash at a till only** (CHG-FIN-001, 2 October 2026). A card or wallet payment the guest made in a currency they selected is refunded in that currency (`Refund.tenderCurrency`).\n"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"changeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["authorised","captured","pendingConfirmation","declined","failed","voided","refunded"]},"providerName":{"type":"string","nullable":true},"providerReference":{"type":"string","nullable":true,"description":"The provider's own id for the charge (Stripe PaymentIntent, NI order reference). What `payments.receivePaymentProviderWebhook` matches an incoming event on (SD-034)."},"providerIdempotencyKey":{"type":"string","nullable":true,"readOnly":true,"description":"The idempotency key sent to the provider, which is this payment's `id` (SD-034, 29 September). A retried provider call cannot charge twice."},"terminalId":{"type":"string","format":"uuid","nullable":true,"description":"The card terminal a till payment ran on (ECR flow, SD-034)."},"nextAction":{"type":"object","nullable":true,"x-ticvai-persisted":false,"description":"**What the caller does while the payment is `pendingConfirmation`** (SD-034, 29 September). `redirect`: send the browser to `url` (3-D Secure challenge or hosted page); the provider returns the guest to `returnUrl` and the result arrives by webhook. `terminal`: the card terminal has been instructed; wait for its result. Null once the payment has an outcome.","properties":{"kind":{"type":"string","enum":["redirect","terminal"]},"url":{"type":"string","format":"uri","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true}}},"lastInquiryAt":{"type":"string","format":"date-time","nullable":true},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"Promotion": {"x-ticvai-persistence":"promotions.promotion","allOf":[{"$ref":"#/components/schemas/CreatePromotionRequest"},{"type":"object","required":["id","status"],"properties":{"id":{"type":"string","format":"uuid"},"status":{"$ref":"#/components/schemas/PromotionStatus"},"isPaused":{"type":"boolean"},"redemptionCount":{"type":"integer"},"discountGiven":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"publishedAt":{"type":"string","format":"date-time","nullable":true},"version":{"type":"integer","minimum":1,"readOnly":true,"description":"Starts at 1 and goes up by one on every saved change. The version the directory, the audit history (`promotions.promotion_audit`) and the channel publication monitor (`promotions.promotion_channel_publication`) name. (DM5, 29 September: data model for the agreed operations)"}}}]},
"PromotionConditions": {"x-ticvai-persistence":"none — embedded in promotion","type":"object","description":"All conditions must hold. An empty object matches everything.","properties":{"variantIds":{"type":"array","items":{"type":"string","format":"uuid"}},"productKinds":{"type":"array","items":{"type":"string"}},"categoryIds":{"type":"array","items":{"type":"string","format":"uuid"}},"minQuantity":{"type":"integer","minimum":1},"minBasketValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"channels":{"type":"array","description":"Empty or absent matches every channel.","items":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"}},"purchaseGate":{"type":"boolean","default":false,"description":"BL-037. **`evaluatePromotions` gates a price and nothing gated a sale.** A non-member could buy a member-only product at the member price refused, which is a discount failure rather than an eligibility one.\nTrue makes these conditions a **precondition of purchase**: fail them and the line cannot be added, not merely charged more. **Evaluated at add-to-cart**, because a guest told at payment has already entered a card.\n"},"paymentMethod":{"type":"array","nullable":true,"description":"BL-113. **Card-issuer and payment-type promotions** — *10% with a Network International card* is a real campaign a bank co-funds, and it was unexpressible.\n**Evaluated at payment, not at cart**, which is the awkward part: the discount appears after the tender is chosen, and the basket total must be allowed to move at that point.\n","items":{"type":"string"}},"issuerBins":{"type":"array","nullable":true,"description":"Card BIN ranges, where the campaign is issuer-specific rather than scheme-specific. **The bank supplies these and they change**, so they are data rather than configuration.\n","items":{"type":"string"}},"componentRedemption":{"type":"string","nullable":true,"enum":["allTogether","independently","sequenced"],"description":"BL-112. **Per-component redemption inside a bundle was unstated.** A park-plus-lunch bundle where lunch may be used another day behaves differently from one where both must be used on the same visit, and **the difference is revenue recognition, not just convenience.**\n"},"daysOfWeek":{"type":"array","items":{"type":"integer","minimum":0,"maximum":6}},"startTime":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$"},"endTime":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$"},"membershipTierIds":{"type":"array","items":{"type":"string","format":"uuid"}},"requiresCoupon":{"type":"boolean","default":false},"firstPurchaseOnly":{"type":"boolean","default":false},"performanceIds":{"type":"array","items":{"type":"string","format":"uuid"}},"advanceDaysMin":{"type":"integer","description":"Early-bird — booked at least this many days ahead."},"advanceDaysMax":{"type":"integer","description":"Last-minute — booked no more than this many days ahead."},"eligibilityRuleIds":{"type":"array","nullable":true,"items":{"type":"string","format":"uuid"},"description":"Reusable eligibility rules (`promotions.promotion_rule` rows of `ruleType: eligibility` with no promotion of their own) that must also hold. **Deprecated in r2** (CHG-CLN-001): setEligibilityRule, which saved library rules, was retired (BC-017), so no operation creates one; send the conditions inline. Rules already saved still apply. Each is evaluated with its own `effect`. (DM5, 29 September: data model for the agreed operations)"}}},
"PromotionEvaluation": {"x-ticvai-persistence":"none — computed","type":"object","required":["totalDiscount","lines","applied","rejected"],"properties":{"totalDiscount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lines":{"type":"array","items":{"type":"object","required":["lineId","originalPrice","discountedPrice","discount"],"properties":{"lineId":{"type":"string"},"originalPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"discountedPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"discount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"appliedPromotionIds":{"type":"array","items":{"type":"string","format":"uuid"}}}}},"applied":{"type":"array","items":{"type":"object","required":["promotionId","promotionCode","discount"],"properties":{"promotionId":{"type":"string","format":"uuid"},"promotionCode":{"type":"string"},"promotionName":{"type":"string"},"discount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"couponCode":{"type":"string","nullable":true}}}},"rejected":{"type":"array","description":"Promotions that matched the products but did not apply, with the reason. This is what a cashier reads to a guest who expected a discount.\n","items":{"type":"object","required":["promotionCode","reason"],"properties":{"promotionCode":{"type":"string"},"promotionName":{"type":"string"},"reason":{"type":"string","enum":["conditionsNotMet","supersededByBetterOffer","exclusivePromotionApplied","redemptionLimitReached","budgetExhausted","outsideValidPeriod","wrongChannel","membershipRequired","couponRequired"]},"detail":{"type":"string"}}}}}},
"PromotionStatus": {"type":"string","enum":["draft","scheduled","live","paused","expired","ended"]},
"PromotionUsage": {"x-ticvai-persistence":"none — aggregated from ledger and orders","type":"object","required":["promotionId","redemptionCount","discountGiven"],"properties":{"promotionId":{"type":"string","format":"uuid"},"redemptionCount":{"type":"integer"},"discountGiven":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"budgetCap":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"budgetRemaining":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"isBudgetExhausted":{"type":"boolean"},"byChannel":{"type":"array","items":{"type":"object","properties":{"channel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"},"redemptionCount":{"type":"integer"},"discountGiven":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}}}},
"Refund": {"x-ticvai-persistence":"orders.refund","type":"object","required":["id","orderId","amount","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid"},"batchId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `RefundBatch` that raised this refund, where `createBulkRefund` did. Null for a refund raised on its own."},"fxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"readOnly":true,"description":"**The rate on the original payment, not today's** (BL-087, CF-118).\n`Payment` records `tenderCurrency`, `fxRate` and `fxRateSource` at the moment of sale, so the sale rate is always retrievable. **Refunding at today's rate repays a different amount of money than was taken** — a guest who paid 100 USD at 3.67 and is refunded at 3.72 gets back more AED than they gave, and the venue carries the difference on every refund.\nThe exposure runs both ways and neither direction is defensible: a guest short-changed by a moving rate has a complaint the venue cannot answer, because **the guest did nothing but wait.**\n"},"taxReversalEntryId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**A refund reverses the tax entry it created, and this is where that is stated rather than implied.** `reverseJournalEntry` and `calculateTax` both exist, so both halves were present and the obligation was assumed — **an implied obligation is one a developer can miss without failing anything.**\nNull only where the original sale carried no tax.\n"},"settleTo":{"type":"string","enum":["originalTender","advanceBalance","wireTransfer","storeCredit"],"default":"originalTender","description":"BL-086. **A refund could only go back the way it came.** A guest whose card has expired, a partner settling by wire, a guest who would rather have the credit — three real cases with one answer.\n**`originalTender` stays the default** because refunding elsewhere is how money laundering works, and anything else needs a reason.\n\n**`storeCredit` is a gift card issued for the refund amount** (decided 2 October 2026, Chinmay, batch 1, POS-011; DEC-061; CHG-CSP-037; DI-796), never a voucher or a wallet top-up.\n"},"fxVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Where the sale rate and the current rate differ, **the difference is booked as an FX variance rather than hidden in the refund**. `runFxRevaluation` already handles this class of movement and this is the same act at a smaller scale.\n"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**A refund goes back in the currency the guest paid** (decided 2 October 2026, Chinmay; CHG-FIN-001). For a card or wallet payment taken in a guest-selected currency, the refund request to the provider is in that currency, and `tenderAmount` is the refunded share of the original `Payment.tenderAmount` at the sale rate (`fxRate`), so a full refund returns exactly what was charged. `amount` stays in base currency for the ledger. Null for a refund in the base currency. Foreign cash refunded at a till is paid in base currency (DI-282)."},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"The refund in `tenderCurrency`, at that currency's own scale (CHG-FIN-001)."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"appliedPercentage":{"type":"number","description":"From the venue's time bands, or an approver override."},"status":{"type":"string","enum":["pendingApproval","pendingGateway","completed","declined","failed"]},"reason":{"type":"string"},"requestedByPrincipalId":{"type":"string","format":"uuid"},"secondaryPrincipalId":{"type":"string","format":"uuid","nullable":true},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"ledgerEntryId":{"type":"string","format":"uuid","nullable":true,"description":"Written before the gateway is called."},"gatewayReference":{"type":"string","nullable":true},"createdAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true}}},
"SeatBlock": {"x-ticvai-persistence":"seating.seat_block","type":"object","required":["id","performanceId","seatIds","reason","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"performanceId":{"type":"string","format":"uuid"},"seatIds":{"type":"array","items":{"type":"string"}},"reason":{"$ref":"#/components/schemas/BlockReason"},"note":{"type":"string"},"createdByPrincipalId":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"},"releaseAt":{"type":"string","format":"date-time","nullable":true},"releasedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"SeatHold": {"x-ticvai-persistence":"seating.seat_hold","type":"object","required":["id","performanceId","seatIds","status","createdAt","expiresAt"],"properties":{"id":{"type":"string"},"performanceId":{"type":"string","format":"uuid"},"seatIds":{"type":"array","items":{"type":"string"}},"bufferedSeatIds":{"type":"array","items":{"type":"string"},"description":"Neighbours implicitly held by a seating rule."},"status":{"type":"string","enum":["held","converted","released","expired"]},"totalPrice":{"x-ticvai-column":"gross_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"heldByPrincipalId":{"type":"string","format":"uuid","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"extensionCount":{"type":"integer"},"createdAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time"}}},
"StackingMode": {"type":"string","description":"How this promotion combines with others. Declared, never inferred from creation order — two reasonable promotions can otherwise combine into a free ticket.\n","enum":["exclusive","stackable","bestOnly","stackWithGroup"]}
}
```
