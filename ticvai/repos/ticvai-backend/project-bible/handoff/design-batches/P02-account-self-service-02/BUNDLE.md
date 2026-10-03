# P02-account-self-service-02 — P02 · Account & Self-Service (2 of 2)

**4 screens · 24 operations · 27 schemas · 7 permissions**

Platform P02 Guest App · ships as **guest** ·
guest audience · mobileApp ·
offline-capable

## Who this is for

**guest on mobileApp.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 7 permissions apply here:
  `GUEST_MANAGE, GUEST_VIEW, LOYALTY_REDEEM, ORDER_CREATE, ORDER_VIEW, WALLET_OPERATE, WALLET_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **2 of these operations work offline**: getGuestSession, getOrder
  — and the rest do not. A surface that looks the same online and off is lying.
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
| `GST-067` | Refunds & Resale | A | 6 | 5 | 6 | 14 | 7 | 6 | guest | notStarted (client-verified) |
| `GST-069` | Face Pass | A | 14 | 5 | 7 | 36 | 5 | 6 | guest | notStarted (client-verified) |
| `GST-071` | Payment Methods | A | 9 | 9 | 6 | 7 | 1 | 0 | guest | notStarted (client-verified) |
| `GST-073` | Security & Sign-in | A | 5 | 15 | 5 | 3 | 2 | 0 | guest | notStarted (designed) |

## Thin screens in this batch

**GST-067 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `GST-067` Refunds & Resale

****A guest could buy a ticket and not ask for their money back.** `createRefundRequest` and `createResaleListing` were back-office only, so every refund began as a phone call.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | Account & Self-Service · wave 1 · needs the `core` module |
| Block | Block A · task APP-MOB-GST-067 |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · the venue's theme |
| Pattern | statusTracker (comfortable density): Refund and resale of one order: its state and what happens next (CHG-SGU-020) |
| Offline | **Not available, and the offline banner says why.** Refunds and resale listings need the server — a queued refund request is a promise nobody made. |
| Opens with | `subjectId` (session), `orderId` (navigation) · cold entry: **Resolves from the session.** A guest arriving cold is asked to sign in and returned here afterwards — never a 404, and never a screen that silently shows … |
| Route | `/account/refunds-resale` |

**What the spec says about it.** **A guest could buy a ticket and not ask for their money back.** `createRefundRequest` and `createResaleListing` were back-office only, so every refund began as a phone call. **The refund policy decides what is offered, not this screen.** `orders.refund_policy` is scoped, so a venue may be stricter than its tenant — the screen shows the answer rather than arguing with it.

**From the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process.** Ask for a refund or list a ticket for resale from the app. Block A. The venue's refund policy decides what is offered; the screen shows the answer (e.g. 100% more than 48 hours before, 50% 24 to 48 hours, none within 24) and a refund is always a request until operations approve it.

**Fixed on main** (the package already carries these; draw what it says): A Waiver status panel bound to getWaiverStatus, whose response has no named schema. (CHG-SGU-020).

#### Inputs: what the user enters or picks

**Form: Create refund request** (modal, opened by *Create refund request*; *Create refund request* calls `createRefundRequest`, *Cancel* sends nothing)

**Collects what `createRefundRequest` sends before it is called.** Required: `orderId`, `reason`. Optional: `lineIds`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Order `orderId` | picker: choose an order | required | — | — | shows names, sends the id | — | `createRefundRequest` body |
| Lines `lineIds` | multi-picker: choose lines | optional | — | — | — | — | `createRefundRequest` body |
| Reason `reason` | text area | required | — | min length 3; max length 1000 | — | — | `createRefundRequest` body |

Errors to draw in the form: 403 Authenticated but not permitted at the requested scope

**Form: Create resale listing** (modal, opened by *Create resale listing*; *Create resale listing* calls `createResaleListing`, *Cancel* sends nothing)

**Collects what `createResaleListing` sends before it is called.** Required: `entitlementId`, `askPrice`. Optional: `sellerSubjectId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Entitlement `entitlementId` | picker: choose an entitlement | required | — | — | shows names, sends the id | — | `createResaleListing` body |
| Ask price `askPrice` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createResaleListing` body |
| Seller subject `sellerSubjectId` | picker: choose a seller subject | optional | — | — | shows names, sends the id | The holder listing it. A guest caller is always the seller and may name only themselves; a member of staff listing on a guest's behalf names the guest. | `createResaleListing` body |

Errors to draw in the form: 409 Not resellable, and the reason says which — partly consumed (`partlyConsumed`), name-bound (`nameBound`), or outside the resale window (`outsideResaleWindow`) … (ResaleRefusedProblem)

#### Outputs: what the screen shows and produces

**Shown**

**Load the order a refund or resale is asked for** (detail panel, from `getOrder`)

| Shows | Format | Notes |
|---|---|---|
| Order number | text | The number a guest reads and a cashier types. Server-assigned: the venue prefix and a sequence per venue, for example `DXB1-000123` … |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Hold label | text | The `label` a cashier gave when parking it with `holdOrder` — how they find it again. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create refund request (primary button) | `createRefundRequest` POST `/refund-requests` | inline | inline | 403 Authenticated but not permitted at the requested scope | opens modal first |
| Create resale listing (secondary button) | `createResaleListing` POST `/resale-listings` | CreateResaleListingRequest | ResaleListing | 409 Not resellable, and the reason says which — partly consumed (`partlyConsumed`), name-bound (`nameBound`), or outside the resale window (`outsideResaleWindow`) … (ResaleRefusedProblem) | opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **refund policy line**: The tier that applies now, before the guest asks ("You'll get 50% back, your visit is in 30 hours"). *(source: DI-192; contracts/spine/orders.yaml#getRefundPolicy)*
- **where the money goes**: Original payment method or wallet credit, as the venue allows; the guest picks when both are offered. *(source: DI-673)*
- **resale listing**: Price within the venue's allowed range (e.g. 10 to 20% below the original), the market fee and what the guest receives; the ticket stays usable until sold, then the guest's QR stops working. *(source: DI-618; DI-621; contracts/spine/orders.yaml#createResaleListing)*

**Data it reads**: `getOrder` (onLoad, Load the order a refund or resale is asked for)

**Where the user goes next**

- → `GST-039` Profile: *Profile*; carries `subjectId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Content loads. |
| Error (`?state=error`) | Could not load. **Says what failed and offers one way onward**, never a bare failure. |
| Empty, first run (`?state=emptyFirstRun`) | **No refunds or listings yet.** The venue's policy is shown regardless, so a guest knows the answer before they need it. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing here yet.** The scope is what narrowed it — naming the scope is what stops somebody concluding the record does not exist. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that … |
| Offline (`?state=offline`) | **Not available, and the offline banner says why.** Refunds and resale listings need the server — a queued refund request is a promise nobody made. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Not resellable, and the reason says which — partly consumed (`partlyConsumed`), name-bound (`nameBound`), or outside the resale window (`outsideResaleWindow`) … (ResaleRefusedProblem) |

#### Edge cases to draw

- **Ticket partly used, name-bound or past the resale window**: Resale is not offered, with the reason. *(source: contracts/spine/orders.yaml#createResaleListing)*

#### Consistency with other screens

- Match `WEB-019`: Same refund request on the web.
- Match `WEB-030`: Same resale rules.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
refund: 2 park ticket × 3 · Fri 2 Oct · 50% back = AED 712.50 to Visa •••• 4242
resale: List at AED 400 (range AED 380-427) · fee AED 20 · you receive AED 380
```

#### Permissions

- `createRefundRequest` → no permission · guest
- `createResaleListing` → `ORDER_CREATE` (operate) · staff, guest
- `getOrder` → `ORDER_VIEW` (read) · staff, guest, partner

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that …

#### Requirements it meets

14 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.15 | Ticket Cancellation - System shall support ticket cancellation. | Guest Mobile App & Branding | CONTRACTED | `createRefundRequest` |
| 19.2.82 | Self-Service Refund Requests - System shall support self-service refund requests. | Guest Mobile App & Branding | CONTRACTED | `createRefundRequest` |
| 2.6.42 | Customer should be able to intiate refund tickets from the online portal | Ticketing Sales | CONTRACTED | `createRefundRequest` |
| 2.12.12 | The system should allow amendment and refunds (full or partial) based on ticket status (available, expired, etc.). This should be configurable. | Ticketing Sales | CONTRACTED | `createRefundRequest` |
| 2.12.15 | The system should be able to refund in different and multiple payment methods (example: System to allow refunds in cash for the tickets/bookings purchased through credit card). | Ticketing Sales | CONTRACTED | `createRefundRequest` |
| 2.12.18 | The system should provide the option to issue refund in the original mode of payment used by the guest or a different method of payment with supervisor override. Refund can also be offered as credits … | Ticketing Sales | CONTRACTED | `createRefundRequest` |
| 4.2.2 | The system should be able to refund transactions that contain promotions and ensure discounted amount is not refunded | Bundles and Promotions | CONTRACTED | `createRefundRequest` |
| 4.6.10 | The system to be able to refund in different and multiple payment methods. For example, system to allow refunds in cash or original payment methods. | Bundles and Promotions | CONTRACTED | `createRefundRequest` |
| 4.6.11 | The system should be able to accept foreign currency and offer refunds/negative sales in local currencies. | Bundles and Promotions | CONTRACTED | `createRefundRequest` |
| 5.5.24 | Support partial and full refunds while maintaining financial reconciliation. | F&B & Guest Management | CONTRACTED | `createRefundRequest` |
| 19.2.12 | Ticket Viewing - System shall display ticket details. | Guest Mobile App & Branding | CONTRACTED | `getOrder` |
| 2.6.2 | Post-order service 1) On the order details page, users can view the order number, amount, time, payment method, user information, refund/change policies, and the QR code of the e-ticket 2) During the … | Ticketing Sales | CONTRACTED | `getOrder` |
| … 2 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Approved refunds go back to the original payment method or are credited to the guest's wallet for future purchases. *(client request · MoM 7 Sep 2026, 4.11 Entitlements Usage, Upgrades & Refund/Credit Recovery · DI-673)*
- White-label resale page: guest lists a ticket and sets a price within the allowed range; buyer searches, browses and receives the new ticket after purchase; the resale summary shows the market fee TICVAI retains. *(client request · MoM 1 Sep 2026, 4.14 Resale Marketplace - Board 3 · DI-621)*
- Three resale access models: (1) the client's own B2C site, where a guest requests resale within an admin-set price range (e.g. 10-20% below original); (2) a TICVAI-hosted white-label resale portal (e.g. museum.tickvai.com) for clients without B2C; (3) API for clients' own resale markets. *(agreed · MoM 1 Sep 2026, 4.14 Resale Marketplace - Detailed Follow-Up · DI-618)*
- **Open question.** Resale lets a guest resell a ticket through a secured channel with configurable commission and eligibility (e.g. minimum time before validity date, no expired tickets). Open: TICVAI-owned secure portal vs inside each client's own B2C site/app. *(open · MoM 31 Aug 2026, 4.12 Resale Marketplace · DI-584)*
- Online/app returns: customer submits a return request with a reason (and photo if applicable) → approval team → courier pickup → refund after verified receipt. Confirmed: an item bought at the POS can also be returned via the web portal, subject to approval. *(agreed · MoM 19 Aug 2026, 4.7 Returns, Refunds & Exchanges — In-Store and Online; 5. Key Decisions · DI-367)*
- Guests can request a refund from their account/profile; operations are notified and can approve, reject or ask for more information. *(agreed · MoM 12 Aug 2026, 9. Refund Ledger Sequencing and Refund Policy · DI-254)*
- Refund policy shown to guests is tiered and driven by back-office rules per business, e.g. no refund <24h, 50% between 24–48h, 100% >48h. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-192)*

Also apply: 1 for P02 · Account & Self-Service, 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S5** Resale marketplace *(Chinmay Parab · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'resale')*
- **A75** Design the refund engine: a six-step ledger-to-gateway refund flow with configurable time-banded percentages, an authorized-approver override, partial refunds, both operations- and customer-initiated requests, plus bulk … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 12 Aug 2026 · workshop tracker · keyword 'refund')*
- **A80** Implement a currency-locking rule for refunds/change: always issue in the local/base currency, locked at the value recorded at time of purchase; track foreign-currency activity only via a separate report *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 14 Aug 2026 · workshop tracker · keyword 'refund')*
- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'refund')*
- **A140** Centralise policy management (reschedule, exchange, refund, cancellation, upgrade, downgrade, ownership transfer, membership conversion) with each product mapped to pricing, GL code, promotions and channels *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'refund')*
- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'refund')*

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-067` · status **notStarted** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match exact): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html`, view *Account → All screens → Wave 2 → Refunds & resale*
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0030 *A deep link is a pointer, not authorisation* (`docs/adr/0030-deep-link-cold-entry.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (403, 404, 409).
- [ ] Every output is drawn (5 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-067?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create refund request, Create resale listing.
- [ ] Every transition is wired: `GST-039`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 7 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-069` Face Pass

**Register or remove my face for gate entry on my pass, or a linked child's with my consent as guardian.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | Account & Self-Service · wave 1 · needs the `core` module |
| Block | Block A · task APP-MOB-GST-069 |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · the venue's theme |
| Pattern | statusTracker (comfortable density): `getFacePassEnrolment` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | **Not available, and the offline banner says why.** Biometric enrolment never happens offline — a face captured and queued is a face the guest cannot withdraw until it uploads. |
| Opens with | `enrolmentId` (deepLink), `subjectId` (session) · cold entry: **Resolves from the session.** A guest arriving cold is asked to sign in and returned here afterwards — never a 404, and never a screen that silently shows … |
| Route | `/account/face-pass` |

**What the spec says about it.** 🔴 **Biometric enrolment had no guest-facing consent step.** `enrolFacePass` was callable by a guest and reachable from nowhere, which means enrolment was happening at a desk with somebody else operating the screen. **`pii.subject_biometric` is separate from contact and document precisely so consent and erasure differ per kind.** Revocation sits beside enrolment for the same reason — a face a guest cannot withdraw is a face they did not really consent to. **Who is this for** (decided 28 September, audit R205): the signed-in adult enrols themselves or a linked child, and is recorded as guardian by the server. The age below which a subject is a minor is an open value client counsel sets.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Face Pass enrolment and withdrawal by the guest for themselves (and, if allowed, a linked child): who it is for, what is captured and why, explicit consent, capture, and the active state with a Remove button that destroys the face record. The one thing to get right: consent is a deliberate, separate step, and removing the face never removes the pass.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- enrolFacePass sends the face template to TICVAI (CHG-SGU-025)

**Fixed on main** (the package already carries these; draw what it says): Enrolment channels disagree (CHG-SGU-021); Purpose field holds a review note (red flag text) instead of a purpose (CHG-SGU-021).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **May children be enrolled with guardian consent, or are under-18s excluded?** → Superseded: children MAY be enrolled with guardian consent on the venue's form; the minor age is per country and the venue can switch minors off (Critical set 1, BO-187). The batch-4 default ('not available for under-18s') no longer applies. *(decided by Chinmay, 2026-10-02; DEC-138 / CHG-NOTE-008 / CHG-SGU-004)*
- **Where are face templates held (vendor only, or TICVAI) and what is the legal retention floor?** → Drawn default accepted: Copy says "held by our face recognition provider" and shows the venue's configured retention. *(decided by Chinmay, 2026-10-02; DEC-139 / CHG-NOTE-008)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Who is this for | select field | — | — | — | — | **The first step of enrolment** (decided 28 September, audit R205): the signed-in guest, then each child linked to them — the `heldByThisGuest` grants whose `delegationKind` is `familyMember` or … | — |

**Form: Enrol face pass** (modal, opened by *Enrol face pass*; *Enrol face pass* calls `enrolFacePass`, *Cancel* sends nothing)

**Collects what `enrolFacePass` sends before it is called.** Required: `subjectId`, `entitlementId`, `template`, `capturedAt`, `source`, `consent`. `subjectId` is the person picked in **Who is this for** (the guest or a linked child), not typed; **no guardian is asked for** — the server sets `consent.guardianSubjectId` to the signed-in guest (decided 28 September, audit R205). Dismissing sends nothing; the screen behind is unchanged. **Consent is the venue's own consent form** (`VenueSettings.biometrics.consentFormId`), shown before the camera opens; for a child the signed-in guest consents as guardian, and the form version is recorded with the enrolment (CHG-SGU-004). **Where:** in this …

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Subject `subjectId` | picker: choose a subject | required | — | — | shows names, sends the id | — | `enrolFacePass` body |
| Entitlement `entitlementId` | picker: choose an entitlement | required | — | — | shows names, sends the id | An `Entitlement.id`, which is a UUIDv7. | `enrolFacePass` body |
| Template `template` | text field | required | — | — | — | Write-only, never returned. A template, not an image — the derived vector a matcher compares against, from which no face can be reconstructed. | `enrolFacePass` body |
| Captured at `capturedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `enrolFacePass` body |
| Source `source` | radio group | required | — | Guest app · Ticket counter · Annual pass counter · Self service kiosk; 43 allows, and the self-service kiosk since 2 October 2026 (Chinmay, BO-186; DEC-236; CHG-CSP-021): a kiosk shows the venue's consent form on its screen and enrols only where the venue's … | — | The three surfaces 3.2.43 allows, and the self-service kiosk since 2 October 2026 (Chinmay, BO-186; DEC-236; CHG-CSP-021): a kiosk shows the venue's consent form on its screen and … | `enrolFacePass` body |
| Consent `consent` | group | required | — | — | — | — | `enrolFacePass` body |
| Purpose `consent.purposeId` | picker: choose a purpose | required | — | — | shows names, sends the id | — | `enrolFacePass` body |
| Given at `consent.givenAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `enrolFacePass` body |
| Consent form `consent.consentFormId` | picker: choose a consent form | optional | — | — | shows names, sends the id | The venue's consent form accepted (DEC-128; CHG-CSP-018). | `enrolFacePass` body |
| Consent form version `consent.consentFormVersion` | number field | optional | — | min 1 | — | The version of that form shown (CHG-CSP-018). | `enrolFacePass` body |
| Guardian subject `consent.guardianSubjectId` | picker: choose a guardian subject | optional | — | — | shows names, sends the id | Required where the subject is a minor. On a guest surface the server sets it to the signed-in adult enrolling their linked child (audit R205). | `enrolFacePass` body |
| Guardian relationship `consent.guardianRelationship` | text field | optional | — | — | — | — | `enrolFacePass` body |
| Reason for re enrollment `reasonForReEnrollment` | select | optional | — | Appearance change · Poor original capture · Technical issue · Guest request · Recovery · Other | — | Required when the subject already has a Face Pass: why the face is being enrolled again (decided 29 September, writers pass) | `enrolFacePass` body |

Errors to draw in the form: 403 A guest enrolling a subject who is neither themselves nor a child linked to them by a `familyMember` or `primaryHolder` delegation (audit R205).; 409 This face is already on another annual pass. Returned with the reason and without naming the other pass — a counter agent needs to know it is a duplicate, not …; 422 Capture quality too low to enrol. Retake rather than store something that will not match.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Who is this for**: The signed-in guest first, then children linked by a family or primary-holder delegation. A child can be enrolled with guardian consent on the venue's form; the minor age is set per country, and where the venue has switched minors off, children are listed but disabled with "Not offered for children here". *(source: contracts/spine/identity.yaml#listDelegations / ADR-0063 / DI-1085 / decided 2 October 2026 by Chinmay (CHG-NOTE-008))*
- **Pass to attach to**: Only memberships and season or annual passes that allow Face Pass; one face per annual pass, so a pass that already has one shows "Face already registered". *(source: contracts/spine/access.yaml#enrolFacePass / DI-640)*
- **Consent**: A separate screen in plain language modelled on the venue group's published policy: what is stored, for how long (the venue's retention for Face Pass), where, how to withdraw; an unticked checkbox and "I agree"; a guardian confirms for a child. *(source: DI-642 / contracts/spine/access.yaml#enrolFacePass / ADR-0063)*
- **Reason for re-enrolment**: Shown only when a Face Pass already exists; choices Appearance changed, Poor original photo, Technical issue, My request, Recovery, Other. *(source: contracts/spine/access.yaml#enrolFacePass)*

#### Outputs: what the screen shows and produces

**Shown**

**The face pass enrolment** (detail panel, from `getFacePassEnrolment`)

| Shows | Format | Notes |
|---|---|---|
| Source | chip: Guest app, Ticket counter, Annual pass counter, Entry gate | `entryGate` is valid for `faceTag` only, and 3.2.43's omission of it from Face Pass is deliberate: an enduring enrolment is a considered … |
| Captured at | 1 Oct 2026, 14:30 | — |
| Consent given at | 1 Oct 2026, 14:30 | — |
| Is active | yes / no (icon or chip) | — |
| Expires at | 1 Oct 2026, 14:30 | Bounded by whatever `retentionAnchor` names, and a face outliving it is a biometric held for no stated purpose. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Enrol face pass (primary button) | `enrolFacePass` POST `/face-pass/enrolments` | inline | FacePassEnrolment | 403 A guest enrolling a subject who is neither themselves nor a child linked to them by a `familyMember` or `primaryHolder` delegation (audit R205).; 409 This face is already on another annual pass. Returned with the … | opens modal first |
| Revoke face pass (destructive button) | `revokeFacePass` DELETE `/face-pass/enrolments/{enrolmentId}` | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Status**: "Face Pass active on Summit Peaks Annual Pass since 3 Sep 2026, kept until your pass ends" with source (App, Ticket counter) and consent date; never a photo of the stored face. *(source: contracts/spine/access.yaml#getFacePassEnrolment)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Capture**: Live camera with an oval guide, liveness prompt, retake; on success "Face Pass ready - use any face gate". *(source: designer default / DI-641)*
- **Remove Face Pass**: Confirm "Your face data will be deleted. Your annual pass stays valid; use your QR or wristband at the gate." then destroyed. *(source: contracts/spine/access.yaml#revokeFacePass)*

**Data it reads**: `listDelegations` (onLoad, Who this guest may enrol — themselves and the children …); `getFacePassEnrolment` (onLoad, Whether a pass has a face registered, and when)

**Where the user goes next**

- → `GST-039` Profile: *Profile*; carries `subjectId`

**What opens over it**

- confirmDialog *Revoke face pass*: **Names what `revokeFacePass` changes and what it leaves alone**, in the consequence rather than the verb. A face pass this affects should be identified in the dialog, not just counted.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Content loads. |
| Error (`?state=error`) | Could not load. **Says what failed and offers one way onward**, never a bare failure. |
| Empty, first run (`?state=emptyFirstRun`) | **Not enrolled.** What a face pass is for, where it works, and what withdrawing it does — **before** the camera opens. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing here yet.** The scope is what narrowed it — naming the scope is what stops somebody concluding the record does not exist. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that … |
| Offline (`?state=offline`) | **Not available, and the offline banner says why.** Biometric enrolment never happens offline — a face captured and queued is a face the guest cannot withdraw until it uploads. |
| Subject not linked (`?state=subjectNotLinked`) | **Refused: that person is not linked to you** (403 `subject-not-linked`). A guest may enrol only themselves or a child linked to them by a family-member or primary-holder delegation; the screen says so and returns to **Who is this for**, which is refreshed in case the link was just removed (decided 28 September, audit R205). |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 This face is already on another annual pass. Returned with the reason and without naming the other pass — a counter agent needs to know it is a duplicate, not …; 422 Capture quality too low to enrol. Retake rather than store something that will not match. |

#### Edge cases to draw

- **Offline**: Enrolment unavailable with the reason; status can still be read from cache. *(source: screens/P02-guest-mobile-app.yaml#GST-069)*
- **Person not linked**: "You can only enrol yourself or a child linked to your account" and back to the list. *(source: screens/P02-guest-mobile-app.yaml#GST-069)*
- **Face fails at the gate later**: The status screen explains the fallback (QR or wristband) so the guest is not stuck. *(source: DI-641)*

#### Consistency with other screens

- Match `BO-184`: Retention period and enrolment channels shown to the guest come from the biometric settings on BO-184 to BO-189.
- Match `BO-188`: Face Tag (single visit) is a staff/gate flow and never offered here; this screen is Face Pass only.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
enrolment:
  for: Sara Al Nuaimi
  pass: Summit Peaks Annual Pass
  since: 3 Sep 2026
  source: App
  retention: Until the pass ends, then 30 days
```

#### Permissions

- `listDelegations` → `GUEST_VIEW` (read) · staff, guest
- `enrolFacePass` → `GUEST_MANAGE` (configure) · staff, guest
- `getFacePassEnrolment` → `GUEST_VIEW` (read) · staff, guest
- `revokeFacePass` → `GUEST_MANAGE` (configure) · staff, guest

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that …

#### Requirements it meets

36 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.2.43 | Face Pass Enrollment | Admission and Access | CONTRACTED | `enrolFacePass` |
| 19.2.8 | Family Profiles - System shall support family profile management. | Guest Mobile App & Branding | CONTRACTED | data `DelegatedAccess` |
| 1.1.29 | System shall support family ticket products with configurable family composition rules, age restrictions and entitlement management. | Ticketing Catalogue | CONTRACTED | data `DelegatedAccess` |
| 1.1.101 | Family memberships | Ticketing Catalogue | CONTRACTED | data `DelegatedAccess` |
| 1.1.116 | Family ticket management | Ticketing Catalogue | CONTRACTED | data `DelegatedAccess` |
| 2.6.47 | System shall allow one guest account to manage multiple family members or friends. The main account holder shall be able to assign tickets, memberships, annual passes, wallets, benefits, and … | Ticketing Sales | CONTRACTED | data `DelegatedAccess` |
| 2.13.42 | Family & Group Sales | Ticketing Sales | CONTRACTED | data `DelegatedAccess` |
| 2.14.8 | Support annual, season, family, corporate and VIP membership products. | Ticketing Sales | CONTRACTED | data `DelegatedAccess` |
| 2.14.14 | Support primary member and dependent relationships. | Ticketing Sales | CONTRACTED | data `DelegatedAccess` |
| 2.16.7 | The system should be able to create group tickets. The group ticket can be configured in multiple ways: - 1 ticket with N continuous entries - 1 ticket with N non-continuous entries - N tickets with … | Ticketing Sales | CONTRACTED | data `DelegatedAccess` |
| 3.2.72 | The access control can support group tickets: -definition of a specific product for group access, -group ticket is configured to allow n admissions, -one ticket scan unlocks the access control device … | Admission and Access | CONTRACTED | data `DelegatedAccess` |
| 4.3.11 | The system should allow guests to use B2C website to register themselves either as an individual or as a family (group) to be able to use the digital wallet. In case of family wallet, more than 1 … | Bundles and Promotions | CONTRACTED | data `DelegatedAccess` |
| … 24 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- **Open question.** Open: biometric data for children. Adults with consent is compliant; for minors, either exclude biometric storage entirely or allow it with a parent/guardian-signed consent form. TICVAI to answer by email. *(open · MoM 30 Sep 2026, 4.3 Open Questions Flagged by Chinmay — Invoicing/Taxation & Biometric Consent for Minors · DI-1085)*
- Web account gets device management and "sign out a lost device" (WEB-024). Face Pass stays mobile-only until the facial-reader vendor SDK supports web capture. *(agreed · design review 29 Sep 2026, GAP-D1 · D. Mobile-only features get web equivalents · DI-1077)*
- Qossai: use an existing major venue-group client's live app and published privacy policy as the model for how facial-recognition consent, data use and retention are explained to guests. *(client request · MoM 2 Sep 2026, 4.11 Privacy & Biometric Data Retention · DI-642)*
- Face enrollment via mobile app, website, POS, self-service kiosk, or at the turnstile itself (scan the ticket, then look at the reader on first use), covering e.g. B2B/reseller tickets. Re-enrollment and fallback to QR/RFID if face fails at the gate. *(agreed · MoM 2 Sep 2026, 4.10 Facial Recognition - Face Pass, Face Tag & Enrollment · DI-641)*
- Two face credentials: Face Pass (long-term, renewable, for memberships/season passes) and Face Tag (short-lived, single day or event). Retention is venue-configurable per tier. *(agreed · MoM 2 Sep 2026, 4.10 Facial Recognition - Face Pass, Face Tag & Enrollment · DI-640)*

Also apply: 1 for P02 · Account & Self-Service, 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S11** Email: invoicing and taxation questions; biometrics, including children (exclude, or guardian consent) *(Chinmay Parab · Open · due 30 Sep · 30 Sep 2026 · 30 Sep tracker · keyword 'biometric')*
- **A119** Share the selected access control / facial recognition vendor (HID vs. Suprema) so integration scope can be confirmed *(Qossai Alqawasmi · High · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 24 Aug 2026 · workshop tracker · keyword 'facial recognition')*
- **A224** Build the media types board and verification configuration (QR, RFID, NFC, biometric against one virtual ticket; issuance/encoding profiles; on-site media swap as a zero-value transaction; compatibility testing per gate) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **A226** Build facial recognition in two tiers (Face Pass for memberships, Face Tag for single visits) with enrolment via app, web, POS, kiosk or turnstile, plus re-enrolment and fallback media *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **C41** Confirm the access control / facial recognition vendor selection (HID vs. Suprema) and share the vendor details *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-069` · status **notStarted** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match exact): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html`, view *Account → All screens → Wave 2 → Face Pass (also Account → Face Pass)*
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0030 *A deep link is a pointer, not authorisation* (`docs/adr/0030-deep-link-cold-entry.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state (403, 404, 409, 422).
- [ ] Every output is drawn (5 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-069?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline, subjectNotLinked.
- [ ] Every action is wired with its success and its failure: Enrol face pass, Revoke face pass.
- [ ] Every transition is wired: `GST-039`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 5 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-071` Payment Methods

****A stored card a guest cannot see is a stored card they cannot remove.** `listPaymentTokens` and `storePaymentToken` were guest-callable with no guest screen.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | Account & Self-Service · wave 1 · needs the `core` module |
| Block | Block A · task APP-MOB-GST-071 |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · the venue's theme |
| Pattern | listDetail (comfortable density): `listPaymentTokens` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **The offline banner shows.** Balances and stored cards already loaded stay visible with their age, cards masked. Storing a card and transferring value need the server. |
| Opens with | `subjectId` (session), `walletId` (deepLink), `cardCode` (navigation) · cold entry: **Resolves from the session.** A guest arriving cold is asked to sign in and returned here afterwards — never a 404, and never a screen that silently shows … |
| Route | `/account/payment-methods` |

**What the spec says about it.** **A stored card a guest cannot see is a stored card they cannot remove.** `listPaymentTokens` and `storePaymentToken` were guest-callable with no guest screen. **Wallet transfer and loyalty redemption sit here** because to a guest they are all *how I pay*, whatever the contracts call them.

**From the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process.** Payment methods: saved cards (masked), gift cards, wallet transfer and loyalty points, because to a guest they are all how I pay. Block A. The screen exists so a guest can see and remove a stored card.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No operation removes a saved card, yet the screen's purpose is that a guest can remove one. (CHG-SGU-024)

**Fixed on main** (the package already carries these; draw what it says): The redeem form asks for subjectId and programmeId; the transfer is bound to retail.yaml. (CHG-SGU-020); The prototype's Account → Payment methods row opens Engine settings. (CHG-SGU-020).

#### Inputs: what the user enters or picks

**Form: Add a card** (modal, opened by *Add a card*; *Save card* calls `storePaymentToken`, *Cancel* sends nothing)

**The gateway's own card form**, hosted by the provider; it returns the token that `storePaymentToken` saves with the guest's consent. No token, provider or consent id is ever a field.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Provider `providerId` | picker: choose a provider | required | — | — | shows names, sends the id | — | `storePaymentToken` body |
| Provider token `providerToken` | text field | required | — | — | — | — | `storePaymentToken` body |
| Consent purpose `consentPurposeId` | picker: choose a consent purpose | required | — | — | shows names, sends the id | — | `storePaymentToken` body |
| Set default `setDefault` | toggle | optional | off | — | — | — | `storePaymentToken` body |

Errors to draw in the form: 409 The provider cannot hold a stored credential (`tokenisationNotSupported`, `PaymentProvider.supportsTokenisation` false), or the guest has not consented to the … (PaymentProblem)

**Form: Transfer wallet balance** (modal, opened by *Transfer wallet balance*; *Transfer wallet balance* calls `transferWalletBalance`, *Cancel* sends nothing)

**Collects what `transferWalletBalance` sends before it is called.** Required: `amount`. Optional: `toSubjectId`, `toWalletId`, `message`. Dismissing sends nothing; the screen behind is unchanged.

Errors to draw in the form: 409 Insufficient cash credit, distinct from insufficient balance — a guest with 200 of bonus credit and 10 of cash can transfer 10, and telling them they have 200 … (WalletTransferProblem)

**Form: Redeem loyalty points** (modal, opened by *Redeem loyalty points*; *Redeem loyalty points* calls `redeemLoyaltyPoints`, *Cancel* sends nothing)

The reward and the points to spend; the guest is the caller, so no subject or programme is asked.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Subject `subjectId` | picker: choose a subject | required | — | — | shows names, sends the id | — | `redeemLoyaltyPoints` body |
| Programme `programmeId` | picker: choose a programme | required | — | — | shows names, sends the id | — | `redeemLoyaltyPoints` body |
| Points `points` | number field | required | — | — | — | — | `redeemLoyaltyPoints` body |
| Reward `rewardId` | picker: choose a reward | optional | — | — | shows names, sends the id | — | `redeemLoyaltyPoints` body |
| Order `orderId` | picker: choose an order | optional | — | — | shows names, sends the id | Where points are being used against a sale rather than for a catalogue reward. | `redeemLoyaltyPoints` body |

Errors to draw in the form: 409 The balance does not cover `points` (`insufficientPoints`). Nothing is held. (LoyaltyRefusedProblem)

#### Outputs: what the screen shows and produces

**Shown**

**Saved cards** (card list, from `listPaymentTokens`): Was the generated table 'Every payment token'; staff and plumbing columns removed (decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-3)).

| Shows | Format | Notes |
|---|---|---|
| Method | text | — |
| Masked identifier | text | What a guest sees — the last four digits, the card brand. Enough to choose between two saved cards and not enough to use one. |
| Expires at | 1 Oct 2026 | — |
| Is default | yes / no (icon or chip) | — |

**The gift card** (detail panel, from `getGiftCard`)

| Shows | Format | Notes |
|---|---|---|
| Card code | text | — |
| Kind | text | — |
| Face value | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Balance | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Status | chip: Issued, Active, Partially redeemed, Redeemed, Expired, Blocked | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Add a card (primary button) | `storePaymentToken` POST `/payment-tokens` | inline | PaymentToken | 409 The provider cannot hold a stored credential (`tokenisationNotSupported`, `PaymentProvider.supportsTokenisation` false), or the guest has not consented to the … (PaymentProblem) | opens modal first |
| Transfer wallet balance (secondary button) | `transferWalletBalance` POST `/wallets/{walletId}/transfer` | inline | WalletTransaction | 409 Insufficient cash credit, distinct from insufficient balance — a guest with 200 of bonus credit and 10 of cash can transfer 10, and telling them they have 200 … (WalletTransferProblem) | opens modal first |
| Redeem loyalty points (secondary button) | `redeemLoyaltyPoints` POST `/loyalty/redemptions` | inline | LoyaltyPosition | 409 The balance does not cover `points` (`insufficientPoints`). Nothing is held. (LoyaltyRefusedProblem) | opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **saved card**: Brand and last four ("Visa •••• 4242, expires 08/28"), default marked; never the full number. *(source: DI-069)*

**What each action does** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **Add a card**: Through the gateway's card form with consent to store it. *(source: contracts/spine/orders.yaml#storePaymentToken)*
- **Redeem points**: Shows points, the rewards they buy and the value; redeeming confirms what is spent. *(source: contracts/satellite/marketing-crm.yaml#redeemLoyaltyPoints)*

**Data it reads**: `listPaymentTokens` (onLoad, A guest's saved payment methods)

**Where the user goes next**

- → `GST-039` Profile: *Profile*; carries `subjectId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Content loads. |
| Error (`?state=error`) | Could not load. **Says what failed and offers one way onward**, never a bare failure. |
| Empty, first run (`?state=emptyFirstRun`) | **No stored cards.** A guest arrives here after a first purchase, so the empty state is the common one. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing here yet.** The scope is what narrowed it — naming the scope is what stops somebody concluding the record does not exist. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that … |
| Offline (`?state=offline`) | **The offline banner shows.** Balances and stored cards already loaded stay visible with their age, cards masked. Storing a card and transferring value need the server. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Insufficient cash credit, distinct from insufficient balance — a guest with 200 of bonus credit and 10 of cash can transfer 10, and telling them they have 200 … (WalletTransferProblem); 409 The balance does not cover `points` (`insufficientPoints`). Nothing is held. (LoyaltyRefusedProblem); 409 The provider cannot hold a stored credential (`tokenisationNotSupported` … |

#### Consistency with other screens

- Match `WEB-021`: Same saved cards and gift card balance.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
cards:
- Visa •••• 4242 · default
- Mastercard •••• 8810
points: 2,450 points · worth AED 24.50
```

#### Permissions

- `listPaymentTokens` → `ORDER_VIEW` (read) · staff, guest
- `storePaymentToken` → `ORDER_CREATE` (operate) · staff, guest
- `transferWalletBalance` → `WALLET_OPERATE` (operate) · staff, guest
- `redeemLoyaltyPoints` → `LOYALTY_REDEEM` (operate) · staff, guest
- `getGiftCard` → `WALLET_VIEW` (read) · staff, guest

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that …

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.3.16 | The system should support peer to peer transaction for digital wallets using which a guests should be able to transfer money from their wallet to another guest's wallet. | Bundles and Promotions | CONTRACTED | `transferWalletBalance` |
| 5.5.3 | The system should provide the ability to move stored credit between portfolios linked to different accounts. For Example: each family member have their own portfolio with the possibility to transfer … | F&B & Guest Management | CONTRACTED | `transferWalletBalance` |
| 5.5.3 | Allow configurable transfer of stored value, wallet balances, promotional credits, and vouchers between linked portfolios with full audit tracking. | F&B & Guest Management | CONTRACTED | `transferWalletBalance` |
| 5.5.6 | Support shared family wallets while maintaining individual transaction tracking. | F&B & Guest Management | CONTRACTED | `transferWalletBalance` |
| 19.2.44 | Points Redemption - System shall support loyalty redemption. | Guest Mobile App & Branding | CONTRACTED | `redeemLoyaltyPoints` |
| 19.2.45 | Rewards Catalog - System shall provide rewards catalog access. | Guest Mobile App & Branding | CONTRACTED | `redeemLoyaltyPoints` |
| 19.2.40 | Gift Card Wallet - System shall support gift card storage. | Guest Mobile App & Branding | CONTRACTED | `getGiftCard` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Full card numbers are never stored or shown; only a masked representation (e.g. last four digits) so the user can identify which card was used. *(agreed · MoM 31 Jul 2026, 10. Compliance & Data Protection · DI-069)*

Also apply: 1 for P02 · Account & Self-Service, 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-071` · status **notStarted** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match exact): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html`, view *Account → All screens → Wave 2 → Payment methods*. Differences: The Account → "Payment methods" row opens Engine settings instead of this screen. **The frame must open this screen** from Account → Payment methods; the prototype's link to Engine settings is a wiring slip (CHG-SGU-020).
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0030 *A deep link is a pointer, not authorisation* (`docs/adr/0030-deep-link-cold-entry.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (9 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-071?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Add a card, Transfer wallet balance, Redeem loyalty points.
- [ ] Every transition is wired: `GST-039`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-073` Security & Sign-in

****How this guest signs in, and where.** The sign-in methods linked to the account, the email that recovers it, and the devices signed in, with a way to sign a lost phone out. Small screen, and it is the one a guest reaches after losing a phone. Two-step verification where a venue of the tenant enabled it (decided 29 September, rev 3 GAP-B1, per venue).**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | Account & Self-Service · wave 1 · needs the `core` module |
| Block | Block A · task APP-MOB-GST-073 |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · the venue's theme |
| Pattern | configEditor (comfortable density): settings for the guest's own sign-in — the linked sign-in methods (`getGuestSession`) and the devices that hold the account (`listGuestDevices`), each with one act; not a list to browse |
| Offline | **Nothing here is offered offline, and the banner says so.** An erasure request or a device change queued and never sent is worse than one that could not be made — the legal clock starts when the platform receives it, and a device signed out offline is still signed in. |
| Opens with | `subjectId` (session), `deviceId` (session), `challengeId` (navigation), `methodId` (navigation) · cold entry: **Resolves from the session.** A guest arriving cold is asked to sign in and returned here afterwards — never a 404, and never a screen that silently shows … |
| Route | `/account/security-sign-in` |

**What the spec says about it.** **A guest could enrol a second factor and not manage it.** Small screen, and it is the one a guest reaches after losing a phone. **Two-step verification, per venue** (decided 29 September, rev 3 GAP-B1, per venue, superseding the second part of audit R167, which had removed it on 28 September): a guest may enrol a method on their account (`listMfaMethods`, `enrolMfaMethod`, `verifyMfaEnrolment`, `removeMfaMethod`; an authenticator, with an email code as fallback), **offered only when at least one venue of the tenant has `VenueSettings.identity.guestTwoStep.enabled` on** — when none has, the section is not shown. The code is then asked only when signing in or acting at a venue that has it on (step-up before that venue's `guestTwoStep.stepUpActions`: `createMfaChallenge`, `verifyMfaChallenge`). No enterprise SSO for guests (R167, first part, stands). What the screen offers instead: the sign-in methods linked to the account (`GuestSession.identityProviders`), confirming the email that recovers it (`verifyGuestEmail`), the devices that hold its credentials and signing a lost one out (`listGuestDevices`, `revokeGuestDevice`), and signing out here (`guestLogout`). The contract has no guest operation that lists sessions, so "your sessions" is the device list.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The guest's own security page in the app: how they sign in (linked methods and whether the contact is verified), the devices signed into the account with "sign a lost phone out", and two-step verification only when at least one venue of the tenant switched it on. It is the screen a guest reaches after losing a phone, so the lost-device action must be obvious and work from another device.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The offline state text speaks of "an erasure request", copied from a privacy screen. (CHG-SGU-025)

**Fixed on main** (the package already carries these; draw what it says): emptyNoAccess says the caller lacks GUEST_VIEW (because verifyGuestEmail declares it). (CHG-GST-004); "Register guest device" is a button with a form asking platform and token. (CHG-SGU-019); getMyIdentityVerification and submitGuestIdentityDocument are declared but no component uses them. (CHG-SGU-019); Tables show every schema field, plumbing included: 'Every guest device' drop id, subjectId, tokenFingerprint, tokenRef. (CHG-SGU-019).

#### Inputs: what the user enters or picks

**Form: Verify guest email** (modal, opened by *Verify guest email*; *Verify guest email* calls `verifyGuestEmail`, *Cancel* sends nothing)

**Collects what `verifyGuestEmail` sends before it is called.** Required: `mode`. Optional: `token`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Mode `mode` | segmented control | required | — | Send · Confirm | — | — | `verifyGuestEmail` body |
| Token `token` | text field | optional | — | — | — | For `confirm`. Single use and short-lived — a verification link that works forever is a verification link in an old inbox. | `verifyGuestEmail` body |

Errors to draw in the form: 410 The token expired or was already used. Distinct from an invalid one — a guest who clicked an old link should be offered a new one rather than told they are …

**Form: Set up two-step verification** (modal, opened by *Set up two-step verification*; *Turn on* calls `verifyMfaEnrolment`, *Cancel* sends nothing)

**Collects what `enrolMfaMethod` sends**, then asks for the first code (`verifyMfaEnrolment`). The guest is told the code will be asked only at venues that turned it on. Dismissing enrols nothing.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | — | — | — | `verifyMfaEnrolment` body |

**Sent by *Set up two-step verification*** (`enrolMfaMethod`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | radio group | required | — | Totp · SMS OTP · Email OTP · Biometric · Hardware token | — | — | `enrolMfaMethod` body |
| Target `target` | text field | optional | — | — | — | Phone or email for OTP methods. | `enrolMfaMethod` body |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Set up two-step verification**: Offered only when a venue of the tenant has guest two-step verification on. Kinds: an authenticator app, with an emailed code as fallback; the first code confirms it. The copy says the code will be asked only at venues that turned it on. A guest who signs in by email code is not offered email as the second factor. *(source: DI-1072; contracts/spine/identity.yaml#enrolMfaMethod; contracts/spine/identity.yaml#createMfaChallenge)*
- **Verify email**: The recovery email must be verified before it can recover the account; the link lasts 24 hours and is sent by email. *(source: contracts/spine/identity.yaml#verifyGuestEmail; R126)*
- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: registerGuestDevice, revokeGuestDevice: the guest's own setting, no scope selector. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/satellite/marketing-crm.yaml#registerGuestDevice)*

#### Outputs: what the screen shows and produces

**Shown**

**My devices** (data table, from `listGuestDevices`)

| Shows | Format | Notes |
|---|---|---|
| Platform | chip: Ios, Android, Web | — |
| Status | chip: Active, Revoked, Failed | — |
| Failure count | 1,234 | Consecutive delivery failures. Past the threshold the device is marked failed and stops being targeted — a dead token retried forever is … |
| Registered at | 1 Oct 2026, 14:30 | — |

**How you sign in** (detail panel, from `getGuestSession`): The sign-in methods linked to this account (code, password, Apple, Google, UAE Pass) and whether its contact is verified. A second factor is listed only when a venue of the tenant enabled guest two-step verification (decided 29 September, rev 3 GAP-B1, per venue).

| Shows | Format | Notes |
|---|---|---|
| Display name | text | — |
| Is verified | yes / no (icon or chip) | False until an OTP or a verified provider identity confirms ownership. An unverified account may browse and fill a cart but not transact … |
| Identity providers | list or chips (count when long) | Linked providers. Several may resolve to one account. |

**Two-step verification** (card list, from `listMfaMethods`): Enrol, verify, remove. **Shown only when a venue of the tenant has guest two-step verification on.**

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | chip: Totp, SMS OTP, Email OTP, Biometric, Hardware token | — |
| Label | text | — |
| Masked target | text | Partially masked destination, so a person can tell two methods apart. |
| Is active | yes / no (icon or chip) | — |
| Is primary | yes / no (icon or chip) | — |
| Enrolled at | 1 Oct 2026, 14:30 | — |
| Last used at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Sign out on this device (secondary button) | `guestLogout` DELETE `/auth/guest/session` | — | — | — | — |
| Stop notifications on this device (destructive button) | `revokeGuestDevice` DELETE `/guests/{subjectId}/devices/{deviceId}` | — | — | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Verify guest email (secondary button) | `verifyGuestEmail` POST `/auth/guest/verify-email` | inline | inline | 410 The token expired or was already used. Distinct from an invalid one — a guest who clicked an old link should be offered a new one rather than told they are … | opens modal first; produces a document or message: Send a verification link, or consume one |
| Set up two-step verification (secondary button) | `enrolMfaMethod` POST `/auth/mfa/methods` | inline | MfaEnrolment | 403 A guest caller while no venue of the tenant has guest two-step verification on (rev 3 GAP-B1, per venue).; 422 A kind the caller may not enrol. Staff use `totp`, with `emailOtp` as the fallback (audit R126); a guest … | — |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Devices signed in**: One row per device: model, platform, app version, last active and "This device" on the current one. No token fingerprints, token refs or failure counts. Sorted with this device first, then by last active. *(source: contracts/satellite/marketing-crm.yaml#listGuestDevices; DI-1077)*
- **How you sign in**: The linked methods as readable names (One-time code, Password, Apple, Google, UAE Pass) and a Verified badge on the contact; UAE Pass shows "verified identity". *(source: contracts/spine/identity.yaml#getGuestSession)*

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Sign out this device (lost device)**: Confirmation names the device ("Sign out iPhone 15 last used 28/09 in Abu Dhabi?"); the device's session and push token are revoked at once; tickets stay on the account. *(source: contracts/satellite/marketing-crm.yaml#revokeGuestDevice)*
- **Remove a two-step method**: Removing the last method turns two-step off for this guest; the confirmation says the venues that ask for it will then refuse step-up actions until a method is enrolled. *(source: contracts/spine/identity.yaml#removeMfaMethod; DI-1072)*

**Data it reads**: `getGuestSession` (onLoad, The sign-in methods linked to the account and whether it is …); `listGuestDevices` (onLoad, Which devices hold this guest's credentials); `registerGuestDevice` (background, The app registers its push token silently at launch; never …); `listMfaMethods` (onLoad, The guest's enrolled methods)

**Where the user goes next**

- → `GST-039` Profile: *Profile*; carries `subjectId`

**What opens over it**

- confirmDialog *Stop notifications on this device*: **Names what `revokeGuestDevice` changes and what it leaves alone**, in the consequence rather than the verb. A security sign-in this affects should be identified in the dialog, not just counted.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Content loads. |
| Error (`?state=error`) | Could not load. **Says what failed and offers one way onward**, never a bare failure. |
| Empty, first run (`?state=emptyFirstRun`) | **Only this device is signed in.** The device list holds one row, this one, and the screen says that signing in elsewhere will add a row here. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that … |
| Offline (`?state=offline`) | **Nothing here is offered offline, and the banner says so.** An erasure request or a device change queued and never sent is worse than one that could not be made — the legal clock starts when the platform receives it, and a device signed out offline is still signed in. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Last remaining method of a principal who holds a permission that requires MFA (audit R135); 422 A kind the caller may not enrol. Staff use `totp`, with `emailOtp` as the fallback (audit R126); a guest the same (rev 3 GAP-B1).; 422 A wrong code, attempts one to four (CHG-R1S-025; the r1 gate found only the fifth failure specified). |

#### Edge cases to draw

- **Offline**: Nothing is offered offline and the banner says so; a device sign-out queued offline would leave the lost phone signed in. *(source: screens/P02-guest-mobile-app.yaml#GST-073)*
- **No venue of the tenant has two-step on**: The two-step card is absent, not disabled. *(source: DI-1072)*
- **verifyGuestEmail answers 410**: Show it as something the person can act on, not a failure: **The token expired or was already used.** Distinct from an invalid one — a guest who clicked an old link should be offered a new one rather than told they are wrong. *(source: contracts/spine/identity.yaml#verifyGuestEmail)*
- **enrolMfaMethod answers 403**: Show it as something the person can act on, not a failure: A guest caller while no venue of the tenant has guest two-step verification on (rev 3 GAP-B1, per venue). *(source: contracts/spine/identity.yaml#enrolMfaMethod)*
- **enrolMfaMethod answers 422**: Show it as something the person can act on, not a failure: A kind the caller may not enrol. Staff use `totp`, with `emailOtp` as the fallback (audit R126); a guest the same (rev 3 GAP-B1). *(source: contracts/spine/identity.yaml#enrolMfaMethod)*
- **removeMfaMethod answers 409**: Show it as something the person can act on, not a failure: Last remaining method of a principal who holds a permission that requires MFA (audit R135) *(source: contracts/spine/identity.yaml#removeMfaMethod)*

#### Consistency with other screens

- Match `WEB-024`: The web account carries the same device list and sign-out-lost-device function (GAP-D1).
- Match `GST-042`: Methods listed here are the ones offered at sign-in.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
devices:
- model: iPhone 15
  platform: iOS
  appVersion: 3.4.1
  lastActive: 01/10/2026 09:14
  current: true
- model: Samsung Galaxy S23
  platform: Android
  appVersion: 3.3.0
  lastActive: 28/09/2026 21:40
signInMethods:
- One-time code
- Apple
- UAE Pass
email: aisha.nuaimi@outlook.com (verified)
```

#### Permissions

- `getGuestSession` → no permission · guest
- `guestLogout` → no permission · guest
- `listGuestDevices` → no permission · guest
- `registerGuestDevice` → no permission · guest
- `revokeGuestDevice` → no permission · guest
- `verifyGuestEmail` → `GUEST_VIEW` (read) · guest, anonymous
- `listMfaMethods` → no permission · staff, partner, guest
- `enrolMfaMethod` → no permission · staff, partner, guest
- `verifyMfaEnrolment` → no permission · staff, partner, guest
- `removeMfaMethod` → no permission · staff, partner, guest
- `createMfaChallenge` → no permission · staff, partner, guest
- `verifyMfaChallenge` → no permission · staff, partner, guest

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that …

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.2 | User Login - System shall support user login. | Guest Mobile App & Branding | CONTRACTED | `getGuestSession` |
| 2.6.29 | If the customers require to have access to this account, this account shall have a login and password in order to recall previous transactions. | Ticketing Sales | CONTRACTED | `getGuestSession` |
| 7.1.16 | The system shall support MFA using Email OTP, SMS OTP, Authenticator Apps, and future supported authentication mechanisms. | F&B POS | CONTRACTED | `enrolMfaMethod` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Web account gets device management and "sign out a lost device" (WEB-024). Face Pass stays mobile-only until the facial-reader vendor SDK supports web capture. *(agreed · design review 29 Sep 2026, GAP-D1 · D. Mobile-only features get web equivalents · DI-1077)*
- Guest two-step verification is a per-venue setting, off by default. Enrolment lives on the guest's tenant-wide account; the second factor is asked only when signing in or acting at a venue that enables it. Guests never see enterprise SSO. *(agreed · design review 29 Sep 2026, GAP-B1 · B. Login: set up two-step verification; C. Security & Sign-in (step-up auth) · DI-1072)*

Also apply: 1 for P02 · Account & Self-Service, 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-073` · status **notStarted** · provenance designed · **Drawn by Claude Code on 30 September 2026 in the Mobile App v4 look; not client-verified, awaiting the client's design reviewer.** `provenance: designed` because the accepted vocabulary has no …
- Prototype (Mobile App v4, 29 September 2026, verified —, match none): `sources/designs/guest-rev3-30-september/TICVAI Mobile App v4.dc.html`, view **
- Drawn by: Claude Code, 30 September 2026, drawn in the Mobile App v4 look
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0030 *A deep link is a pointer, not authorisation* (`docs/adr/0030-deep-link-cold-entry.md`)
- ADR-0045 *Every order carries a proven contact, and the gate is the checkout page* (`docs/adr/0045-every-order-carries-a-proven-contact.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state (403, 404, 409, 410, 422).
- [ ] Every output is drawn (15 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-073?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Sign out on this device, Stop notifications on this device, Verify guest email, Set up two-step verification.
- [ ] Every transition is wired: `GST-039`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 6 edge case(s) from the process notes are drawn.
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
| Powered by TICVAI credit (`brand.showPoweredBy`) | `CMS-104`, `ADM-016` | — | on | the *Powered by TICVAI* credit on the launch screen, at the foot of Account and in the web footer; on by default, and switching it off needs the licence add-on (403 … |
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

**P02 reference designs** (from `handoff/design-batches/apps/1-guest-app/README.md`)

- `sources/designs/guest-rev3-30-september/TICVAI Mobile App v4.dc.html`: Mobile App v4, the newest guest look (29 September, with the 30 September feedback in the booking flows). It replaces the 28 September Mobile v2 build.
- `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`: the booking engine that runs inside the app. Keep both files in the same folder.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-026, DI-027, DI-029, DI-032, DI-033, DI-034, DI-036, DI-038, DI-040, DI-042, DI-044, DI-045, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

**Workshop tracker rows about P02 as a whole** (30: 3 open, 27 closed). Open first; a closed row says where it went on 30 September.

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker)*
- **S9** Final UI/UX for the website and the mobile app *(Chinmay Parab · In progress · due Fri 2 Oct · 30 Sep 2026 · 30 Sep tracker)*
- **T1** Feedback on the revised website and mobile wireframes *(Allam / Qossai · Open · due 1 Oct · 30 Sep 2026 · 30 Sep tracker)*
- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker)*
- **A28** Review the 'Viva Ticket' website as a reference for ticket-flow variations *(Softlabs Design Team · Low · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker)*
- **A29** Collate design references/inspiration and share with TICVAI, organized by mobile app, website, and admin/back-office pages *(Softlabs (Sahil & Aishwarya) · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A45** Design the "Plan Your Adventure" itinerary-planner feature for the guest app, including group-sharing / invite-to-itinerary functionality *(Softlabs Design Team · High · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A55** Implement per-tenant module visibility toggles (e.g., hide Dining, Retail, or other services) configurable independently for the guest website and mobile app *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker)*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker)*
- **A115** Apply HA selectively to revenue-critical components (ticketing, POS, B2C) same-region, with multi-region DR as an optional add-on *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 24 Aug 2026 · workshop tracker)*
- **A118** Commission the third-party penetration test before go-live (ticketing, B2C, B2B, mobile apps) and resolve all severities *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 24 Aug 2026 · workshop tracker)*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker)*
- … 16 more in `handoff/design-inputs/task-tracker-index.json`

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

### Across P02 Guest App

- Font, header/footer (not yet in the current wireframe build), card size and layout are configurable in the mobile app, consistent with the web app's white-labelling approach. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1097)*
- Step-indicator style is configurable, the same as on the web: bars, dots, counters or step names. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1093)*
- Products can be presented in multiple card layout styles: carousel, video poster, split, etc. *(agreed · MoM 30 Sep 2026, 4.5 Mobile App — Configuration Flexibility · DI-1089)*
- The home-screen navigation bar layout is configurable: home/explore/map/buy-tickets in different arrangements. *(agreed · MoM 30 Sep 2026, 4.5 Mobile App — Configuration Flexibility · DI-1087)*
- The revised mobile app design is approved in direction: Qossai liked the opening video and visual polish, Allam the UI/graphics quality. Its flow is deliberately different from the web application (after front-end team input), not a reused structure. Detailed feedback to follow. *(agreed · MoM 30 Sep 2026, 4.4 Guest Mobile App — Revised Design Walkthrough · DI-1086)*
- Every web product and flow stays bookable in the mobile app (incl. cabanas, surf, 2D/3D stadium, theatre plan, bus route map), each with its own step order; a toggle switches back to one decision per screen. *(agreed · design review 29 Sep 2026, Mobile app (v4) — All web products and flows available · DI-1084)*
- Mobile app must not open straight into booking (client found it unclear). Tabs: Home · Explore · Plan · Tickets (Yas Island / Six Flags references), with a persistent "Buy tickets" button on every screen (raised centre button, or floating / flat per venue). *(agreed · design review 29 Sep 2026, Mobile app (v4) — Tabs Home · Explore · Plan · Tickets, persistent Buy tickets · DI-1081)*
- **Open question.** Real venue photos, clips and logos are still to come from the client; designs use stand-ins. Slots expected: a photo per ticket card and clip per card, a square shot per extra/shop item, one landscape poster per venue for the single-event page. Photos ≥1600 px, clips mp4 6–12 s, no audio. *(open · design review 29 Sep 2026, Asset list — TICVAI Guest Booking · DI-1080)*
- The tenant picks which logo lockup sits in the nav bar and a logo variant (Light, Dark, Duotone) whose colours drive the theme. *(agreed · design review 29 Sep 2026, CFG-4 · Brand logo + Logo palette (Light/Dark/Duotone) · DI-1068)*
- Theme settings: surface style Glass (default) or Solid cards; button style Solid (default), Outline or Pill. *(agreed · design review 29 Sep 2026, CFG-3 · Surfaces (Glass/Solid) and Buttons (Solid/Outline/Pill) · DI-1067)*
- Venue branding offers named palettes, font pairs, background tones and a 0–22 px corner radius. *(agreed · design review 29 Sep 2026, CFG-2 · Brand: Palette, Typeface; Shape: Background, Corner radius · DI-1066)*
- Guest-facing copy may say "session" (surf sessions, timed sessions) as a glossary exception, like "Booking". *(agreed · design review 29 Sep 2026, CFG-10 · 'Sessions can be added, edited or closed from Config -> Sessions' · DI-1064)*
- Optional intro video on opening the app, with a "Skip introduction" control. *(agreed · MoM 29 Sep 2026, 2. Mobile app · DI-1020)*
- A persistent "Buy tickets" button appears on every screen of the mobile app. *(agreed · MoM 29 Sep 2026, 2. Mobile app · DI-1017)*
- Mobile tabs: Home, Explore, Plan, Tickets (Yas Island / Six Flags references). *(agreed · MoM 29 Sep 2026, 2. Mobile app · DI-1016)*
- The current mobile build goes straight into the booking journey and the client finds it unclear: redesign the UI. All web products and flows, including cabanas and surf, must remain available. *(agreed · MoM 29 Sep 2026, 2. Mobile app · DI-1015)*
- Never ask the same thing twice: table zone is picked on the table map (no zone step before it); height is asked once (height bands on the water-park day pass are the eligibility check); party/school summaries prefill headcount, child's name and age from the earlier form. *(agreed · rev 3 design review 28 Sep 2026, Flow review (28 Sep): repeated steps removed · DI-1000)*
- Headers are reserved for standard elements only (venue image, category tabs, language bar, profile icon), applied consistently; date/availability selection belongs in the main content below the header, never in the header. Header/layout patterns must be adapted for mobile, which looks and behaves differently. *(agreed · MoM 24 Sep 2026, 4.9 Guest Web App — Specific UX Feedback (Header/Date Placement Standardization) · DI-990)*
- A language button (EN / العربية) sits in the header next to the profile icon, web and mobile. Arabic flips the whole layout right-to-left and switches interface text (navigation, buttons, booking steps, ticket names and tags, cart, seat map, checkout, account). Venue, show and dish names stay as written. *(client request · design review 23 Sep 2026, Header 2. Language icon in the header · DI-975)*
- Replace "Sign in / Create account" in the header with a single profile icon. It opens one screen with Log in and Register tabs; signed-in guests get their account menu from the same icon. *(client request · design review 23 Sep 2026, Header 1. One profile icon in the header that opens login / register · DI-974)*
- Allam's model reference: a simple card-based family-entertainment-centre site with minimal clicks, a right-side cart drawer, "help me choose", clear categories, video that autoplays when a guest taps "read more", adapting seamlessly between desktop and mobile. Allam and Qossai want this simplicity to guide the guest experience. *(client request · MoM 18 Sep 2026, 4.14 Guest Website UX Review — Upsell/Cross-Sell Placement & Reference Sites · DI-952)*
- **Open question.** Allam expects a large volume of feedback on the guest web/mobile prototype; detailed feedback goes to a separate dedicated session with Qossai and Allam. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-888)*
- **Open question.** Product card-layout options shown in the prototype: stacked, staggered, horizontal. Choice/feedback pending the dedicated review. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-886)*
- **Open question.** Prototype's white-label panel previews the guest site under theme presets (e.g. "stadium", "theatre"), alternative layouts and brand colour palettes. Shown by Chinmay; client feedback deferred to a dedicated session. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-885)*
- Allam: most guests book from a smartphone, so the mobile version of the booking flows is the higher priority to validate (only desktop shown). *(client request · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough · DI-684)*
- Accreditation is primarily completed in the web portal (document upload and photo checks suit a larger screen); the same submission is also available in the guest mobile app as a secondary option for individuals. *(agreed · MoM 7 Sep 2026, 4.8 Accreditation Channel Placement & API Access · DI-666)*
- Waiver versioning, a mobile-optimised guest waiver view, approval/testing/publication flow, and access to the form via a QR code that opens it directly. *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-575)*
- Confirmed: a guest always books a product or package — never a resource (a specific room, vehicle or instructor by itself) directly — on every sales channel, including the guest/mobile app; the product's configuration determines which resources are booked behind the scenes. *(agreed · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 5. Key Decisions · DI-502)*
- Ticketing, F&B and retail share one cart and checkout, one unified receipt and one QR/wristband per customer — no separate receipts or wristbands per product line. *(agreed · MoM 14 Aug 2026, 7. Retail — Cart and Inventory · DI-293)*
- Guest website and app share one CMS/publishing and the same branding, look and feel, but differ in function: the app is the full tenant experience (venue info, services, profile, purchase); a client's own website usually just links ("Buy Tickets") to a TICVAI-hosted checkout. *(agreed · MoM 14 Aug 2026, 3. Guest Website vs. Guest Mobile App · DI-284)*
- **Open question.** Open: publishing model — each client's own App/Play Store listing vs one universal TICVAI app where the user selects the venue; and a client module with customisation screens plus a CI/CD-linked publish action vs a canvas the client exports and publishes. Softlabs to present pros/cons. *(open · MoM 12 Aug 2026, 5. Guest Application Publishing and White-Labelling · DI-251)*
- Qossai: the TICVAI name must always remain visible to end users of a client-branded guest app (e.g. a "Made by TICVAI" credit) and cannot be removed by the client. *(agreed · MoM 12 Aug 2026, 5. Guest Application Publishing and White-Labelling · DI-250)*
- Qossai: present products with video rather than static images (as Talabat-style apps do); see benchmark app "222" for further inspiration. *(client request · MoM 10 Aug 2026, 4.10 Bundle Packages · DI-222)*
- Qossai shared reference apps (Al Qadiya / Six Flags Saudi Arabia, and "The District" by Zomato) and cited their use of video over static images as design inspiration. *(client request · MoM 5 Aug 2026, 13. Mobile / POS App Design References · DI-146)*
- A single cart/order must take mixed purchases (e.g. family tickets plus gift vouchers) with one unified checkout and identity capture. *(agreed · MoM 5 Aug 2026, 7. Sales Channels, Pricing & Cart · DI-141)*
- Base ticket-booking UX (web and mobile) on current market best practice rather than the demoed references as-is; Allam recommends the "Viva Ticket" website as a reference for the flow variations. *(agreed · MoM 3 Aug 2026, 10. Reference Material & Design Research · DI-125)*
- The POS/tablet application carries TICVAI's own branding and UI direction; the B2C and B2B mobile applications are white-label by design. *(agreed · MoM 31 Jul 2026, 15. Monday UI/UX Session Planning · DI-084)*
- Offline capability applies to POS terminals, handheld/validation devices (turnstiles, scanners), and staff and customer mobile apps. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-070)*
- Qossai: the target product is a white-label application supporting both B2C and B2B mobile use cases, built around three to four distinct flows (e.g. admission ticket flow, seat assignment flow). *(client request · MoM 31 Jul 2026, 4. Application Flow & White-Label Requirements · DI-056)*
- Selling reference layout: clean top navigation; category tabs with counts (All Events 32, Exhibitions, Guided Tours ...); sort and type chips (Price, Rating, Popular; General, Seated, Multipass, Scheduled, Rental); content cards with large image, type badge, rating, tags (LIMITED, NEW, BESTSELLER), availability ("180 available", "11 left") and "from" price; persistent cart on the right with member discount, totals and "Checkout Securely". *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - UI inspiration reference, items 2-5 · DI-026)*
- Preliminary perceived-performance targets: web pages load in under about 3 seconds, mobile app loads in under about 2 seconds, ticket validation responds in under 500 milliseconds. *(agreed · MoM 28 Jul 2026, 18. Performance and Scalability · DI-015)*

### In P02 · Account & Self-Service

- Decision: profiles are never merged automatically. Likely duplicates are notified to the customer (push or e-mail) and merge only on the customer's confirmation; an admin review queue tracks flagged duplicates independently of the customer's response. *(agreed · MoM 20 Aug 2026, 4.2 Duplicate Detection; 5. Key Decisions · DI-377)*

**15 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createMfaChallenge": {"method":"POST","path":"/auth/mfa/challenge","contract":"identity","summary":"Second factor at staff sign-in, and step-up for a sensitive action","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"createRefundRequest": {"method":"POST","path":"/refund-requests","contract":"orders","summary":"Guest-initiated refund request","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"createResaleListing": {"method":"POST","path":"/resale-listings","contract":"orders","summary":"List an entitlement for resale","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateResaleListingRequest","responds":"ResaleListing"},
"enrolFacePass": {"method":"POST","path":"/face-pass/enrolments","contract":"access","summary":"Register a facial profile against an entitlement","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"FacePassEnrolment"},
"enrolMfaMethod": {"method":"POST","path":"/auth/mfa/methods","contract":"identity","summary":"Enrol an MFA method","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MfaEnrolment"},
"getFacePassEnrolment": {"method":"GET","path":"/face-pass/enrolments/{enrolmentId}","contract":"access","summary":"Whether a pass has a face registered, and when","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"FacePassEnrolment"},
"getGiftCard": {"method":"GET","path":"/gift-cards/{cardCode}","contract":"wallet","summary":"Check a gift card balance","permission":"WALLET_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GiftCard"},
"getGuestSession": {"method":"GET","path":"/auth/guest/session","contract":"identity","summary":"Read the current guest session","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"GuestSession"},
"getOrder": {"method":"GET","path":"/orders/{orderId}","contract":"orders","summary":"Read an order","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Order"},
"guestLogout": {"method":"DELETE","path":"/auth/guest/session","contract":"identity","summary":"End a guest session","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":"allDevices","in":"query","required":null}],"requestBody":null,"responds":null},
"listDelegations": {"method":"GET","path":"/guests/{subjectId}/delegations","contract":"identity","summary":"Who may act for this guest, and for whom they may act","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listGuestDevices": {"method":"GET","path":"/guests/{subjectId}/devices","contract":"marketing-crm","summary":"A guest's registered devices","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"subject","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMfaMethods": {"method":"GET","path":"/auth/mfa/methods","contract":"identity","summary":"Enrolled MFA methods","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"MfaMethod"},
"listPaymentTokens": {"method":"GET","path":"/payment-tokens","contract":"orders","summary":"A guest's saved payment methods","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"redeemLoyaltyPoints": {"method":"POST","path":"/loyalty/redemptions","contract":"marketing-crm","summary":"Spend points","permission":"LOYALTY_REDEEM","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"LoyaltyPosition"},
"registerGuestDevice": {"method":"POST","path":"/guests/{subjectId}/devices","contract":"marketing-crm","summary":"Register a device for push","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"subject","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GuestDevice"},
"removeMfaMethod": {"method":"DELETE","path":"/auth/mfa/methods/{methodId}","contract":"identity","summary":"Remove an MFA method","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"revokeFacePass": {"method":"DELETE","path":"/face-pass/enrolments/{enrolmentId}","contract":"access","summary":"Remove a facial profile","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"revokeGuestDevice": {"method":"DELETE","path":"/guests/{subjectId}/devices/{deviceId}","contract":"marketing-crm","summary":"Revoke a device registration","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"subject","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"storePaymentToken": {"method":"POST","path":"/payment-tokens","contract":"orders","summary":"Save a payment method for future use","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PaymentToken"},
"transferWalletBalance": {"method":"POST","path":"/wallets/{walletId}/transfer","contract":"wallet","summary":"Send balance to another guest","permission":"WALLET_OPERATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WalletTransaction"},
"verifyGuestEmail": {"method":"POST","path":"/auth/guest/verify-email","contract":"identity","summary":"Send a verification link, or consume one","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"verifyMfaChallenge": {"method":"POST","path":"/auth/mfa/challenge/{challengeId}/verify","contract":"identity","summary":"Complete a sign-in or step-up challenge","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"verifyMfaEnrolment": {"method":"POST","path":"/auth/mfa/methods/{methodId}","contract":"identity","summary":"Complete enrolment","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MfaMethod"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"BiometricKind": {"type":"string","description":"BL-106, CF-35. **Two different legal postures, not two settings on one record.** 3.2.44 describes a temporary facial model taken at a counter or a gate and deleted when the ticket expires; 3.2.43 describes an enduring Face Pass enrolled deliberately on three surfaces. **Storing both as one record with a date makes the stricter rule depend on a field nobody enforces**, which is what BL-106 was raised to stop.\n`facePass` — enduring, explicit consent, revocable by the guest, anchored to the validity of the entitlement it belongs to.\n`faceTag` — same-visit, **consent still explicit and still recorded**, anchored to the ticket and purged at close of the operating day. **PDPL Article 4 is a closed list of exceptions with no legitimate-interests basis**, so a short life does not remove the need for consent — it only shortens what the consent is for.\n","enum":["facePass","faceTag"]},
"BiometricRetentionAnchor": {"type":"string","readOnly":true,"description":"BL-106, ADR-0047. **What the expiry is measured from, derived from the kind rather than chosen.** A retention period a person can type is a retention period somebody will type wrongly; the anchor follows the kind, and the kind follows how the biometric was taken.\n`entitlementValidity` — `facePass`. The face cannot outlive the pass it was enrolled for.\n`ticketValidity` — `faceTag` against a dated ticket.\n`operatingDayClose` — `faceTag` where the ticket has no end of its own, plus `VenueSettings.biometrics.faceTagPurgeMinutesAfterClose`.\n","enum":["entitlementValidity","ticketValidity","operatingDayClose"]},
"CreateResaleListingRequest": {"type":"object","x-ticvai-persistence":"none — request only","description":"Request only; persisted as `ResaleListing`. **What a seller decides**: which entitlement, and at what price. The id, the status, the fee snapshot and the partition key are the server's, which is why `createResaleListing` no longer takes the whole listing.\n","required":["entitlementId","askPrice"],"properties":{"entitlementId":{"type":"string","format":"uuid"},"askPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"sellerSubjectId":{"type":"string","format":"uuid","nullable":true,"description":"The holder listing it. A guest caller is always the seller and may name only themselves; a member of staff listing on a guest's behalf names the guest."}}},
"DelegatedAccess": {"x-ticvai-persistence":"identity.delegated_access","type":"object","required":["id","permission","scopePath","effect"],"properties":{"id":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid","nullable":true},"roleId":{"type":"string","format":"uuid","nullable":true},"permission":{"type":"string","description":"From the permission enum. `*` permitted on DENY only."},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"CF-132, CL-05. **A grant held by a guest rather than a staff principal.**\nSection 5.5 asks for portfolios — a primary holder assigning entitlements, transfer between linked accounts, shared wallets with individual tracking — and it appears ten times across ten sections. **Every one of those reduces to the same question: who may act on whose behalf, over what, and until when.**\n**That is a grant, not a household table.** A primary holder assigning an entitlement is a grant. A group leader holding tickets for twelve is a grant. A corporate account enrolling members is a grant with a quota. **A shared wallet with individual tracking is a grant over a balance, and the transaction log already records who spent.**\n**A household table would answer one of those four.**\n"},"overSubjectId":{"type":"string","format":"uuid","nullable":true,"description":"Whose behalf. **Null for a staff grant, which is the existing behaviour** — every grant written before 18 August means exactly what it meant before.\n"},"overObjectRef":{"type":"string","nullable":true,"description":"**Where the authority is over a thing rather than a scope** — a wallet, an entitlement, a booking. `scopePath` answers *where*; this answers *what*, and a guest's authority is almost always over a specific object rather than a branch of the tree.\n"},"delegationKind":{"type":"string","nullable":true,"enum":["primaryHolder","familyMember","groupLeader","attendee","corporateAdmin","corporateMember","carer"],"description":"**What kind of relationship this expresses**, for display and for reporting. The mechanism does not branch on it — a family member and a group attendee are the same grant with different words around them, which is the point.\n"},"quota":{"type":"integer","nullable":true,"description":"2.14.15 and 4.3.11. **How many the holder may assign.** A corporate account with fifty allocations and a family with four are the same structure with different numbers.\n"},"isRevocableBySubject":{"type":"boolean","default":true,"description":"**Whether the person it is over can end it.** A guest who linked a family member should be able to unlink them; a corporate member should not be able to revoke their employer's oversight — and **a delegation nobody can end is a delegation somebody will regret.**\n"},"scopePath":{"type":"string"},"effect":{"type":"string","enum":["ALLOW","DENY"]},"permissionId":{"type":"string","format":"uuid","nullable":true,"description":"**Taken from `identity.user_access`, 20 September, when that table was collapsed into this one.** `permission` above is free text; this names a row in `identity.permission`, the catalogue wired the same day. A grant that names a catalogue row can be checked against the keys the contracts actually enforce — which is the whole point of a catalogue that reported *154 on operations, 35 in roles.yaml, 0 shared*.\nNullable because a role grant carries no permission at all.\n"},"revokedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"Taken from `identity.user_access`. This table recorded `revokedBy` and not when, so it could say who revoked a grant and not whether it was before or after the thing somebody is asking about.\n"},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true},"createdByPrincipalId":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"}}},
"ExchangeRateDecimal": {"type":"string","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,6)","description":"**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one — a JavaScript client must not round a rate in transit. **Six decimal places**, the precision `finance.FxRate.rate` asks for, and stored at that precision.\n","pattern":"^\\d+(\\.\\d{1,6})?$"},
"FacePassEnrolment": {"type":"object","x-ticvai-persistence":"pii.subject_biometric","description":"3.2.43. **Metadata about a facial profile. Never the profile.**\n","required":["id","kind","subjectId","entitlementId","source","capturedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"subjectId":{"type":"string","format":"uuid"},"entitlementId":{"type":"string","format":"uuid","description":"The `Entitlement.id`, a UUIDv7 (`pii.subject_biometric.entitlement_id`)."},"kind":{"$ref":"#/components/schemas/BiometricKind"},"retentionAnchor":{"allOf":[{"$ref":"#/components/schemas/BiometricRetentionAnchor"}],"x-ticvai-derived":"onWrite","description":"BL-106. **Derived from `kind`, never sent.** `facePass` anchors to the entitlement, `faceTag` to the ticket or to the close of the operating day.\n"},"source":{"type":"string","enum":["guestApp","ticketCounter","annualPassCounter","entryGate"],"description":"**`entryGate` is valid for `faceTag` only**, and 3.2.43's omission of it from Face Pass is deliberate: an enduring enrolment is a considered act with consent attached, not something done in a queue. 3.2.44 puts a Face Tag at a gate precisely because it dies the same day.\n**A self-service kiosk enrolment reads `ticketCounter` here** (an on-site enrolment) so the r1 values stand; the precise channel is `enrolmentChannel` (DEC-236; CHG-CSP-021).\n"},"enrolmentChannel":{"type":"string","readOnly":true,"enum":["guestApp","ticketCounter","annualPassCounter","selfServiceKiosk","entryGate"],"description":"**Where the face was actually captured** (decided 2 October 2026, Chinmay, BO-186; DEC-236; CHG-CSP-021): `source` with `selfServiceKiosk` told apart. `entryGate` for a Face Tag only.\n"},"consentFormId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The venue's consent form the capture was consented on, and its version below (DEC-128; CHG-CSP-018)."},"consentFormVersion":{"type":"integer","nullable":true,"readOnly":true},"capturedAt":{"type":"string","format":"date-time"},"consentPurposeId":{"type":"string","format":"uuid"},"consentGivenAt":{"type":"string","format":"date-time"},"guardianSubjectId":{"type":"string","format":"uuid","nullable":true,"description":"Where the subject is a minor (3.2.12)."},"isActive":{"type":"boolean","readOnly":true},"expiresAt":{"type":"string","format":"date-time","nullable":true,"description":"**Bounded by whatever `retentionAnchor` names**, and a face outliving it is a biometric held for no stated purpose.\n**Settled 20 September by ADR-0047**, which CF-64 had been carrying since 6 August: a `facePass` cannot outlive its entitlement and a `faceTag` does not survive the close of the operating day. **These are ceilings rather than defaults** — they cannot be configured upward, because a retention that a tenant can extend without limit is the breach ADR-0047 gave the platform a ceiling to prevent.\n"}}},
"GiftCard": {"x-ticvai-persistence":"wallet.gift_card","type":"object","required":["cardCode","faceValue","balance","status","issuedAt"],"properties":{"cardCode":{"type":"string"},"kind":{"type":"string"},"faceValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"balance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["issued","active","partiallyRedeemed","redeemed","expired","blocked"]},"blockedReason":{"type":"string","nullable":true},"issuedAt":{"type":"string","format":"date-time"},"activatedAt":{"type":"string","format":"date-time","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true}}},
"GuestDevice": {"type":"object","x-ticvai-persistence":"marketing.guest_device","required":["id","subjectId","platform","status","registeredAt"],"properties":{"id":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid"},"platform":{"type":"string","enum":["ios","android","web"]},"tokenFingerprint":{"type":"string","description":"Hash of the token, not the token. The token itself is write-only — returning it would put a push credential in every response a support agent can read.\n"},"tokenRef":{"type":"string","writeOnly":true,"description":"**A vault reference to the push token**, written by the server from `registerGuestDevice.token` — the same pattern as `PaymentProvider.credentialRef`. Never the token and never returned; the sender resolves it at send time. Without it a registered device could not be sent to.\n"},"appVersion":{"type":"string","nullable":true},"osVersion":{"type":"string","nullable":true},"deviceModel":{"type":"string","nullable":true},"locale":{"type":"string","nullable":true},"status":{"type":"string","enum":["active","revoked","failed"]},"failureCount":{"type":"integer","description":"Consecutive delivery failures. Past the threshold the device is marked failed and stops being targeted — a dead token retried forever is wasted quota and a misleading delivery rate.\n"},"registeredAt":{"type":"string","format":"date-time"},"lastSeenAt":{"type":"string","format":"date-time","nullable":true},"revokedAt":{"type":"string","format":"date-time","nullable":true}}},
"GuestSession": {"x-ticvai-persistence":"none — Redis session registry","type":"object","required":["subjectId","tokens","isVerified","expiresAt"],"properties":{"subjectId":{"type":"string","format":"uuid"},"displayName":{"type":"string","nullable":true},"tokens":{"$ref":"#/components/schemas/TokenPair"},"isVerified":{"type":"boolean","description":"False until an OTP or a verified provider identity confirms ownership. An unverified account may browse and fill a cart but not transact: the gate is the checkout page (ADR-0045), where `checkoutCart` refuses it until the guest verifies or proves the contact by code. UAE Pass returns a verified identity, so it starts true. Rule on `verifyGuestEmail`, decided 17 September 2026.\n"},"identityProviders":{"type":"array","description":"Linked providers. Several may resolve to one account.","items":{"type":"string","enum":["password","otp","apple","google","uaePass"]}},"guestLinkId":{"type":"string","nullable":true,"description":"Present where the guest is linked across cells (ADR-0010)."},"requiresMfa":{"type":"boolean","default":false,"description":"True only where the sign-in venue enabled guest two-step verification (`VenueSettings.identity.guestTwoStep`, in tenancy) and this guest has an active method (decided 29 September, rev 3 GAP-B1, per venue). The session is then not usable until `verifyMfaChallenge` succeeds on a `signIn` challenge. Always false for a UAE Pass sign-in, which is already a verified two-factor identity (proposed, client to correct).\n"},"mfaMethods":{"type":"array","description":"The guest's active methods, so the client can offer the right one. Empty when `requiresMfa` is false.","items":{"$ref":"#/components/schemas/MfaMethod"}},"homeCellName":{"type":"string","nullable":true},"preferredLanguage":{"type":"string","nullable":true},"expiresAt":{"type":"string","format":"date-time","description":"**30 days, sliding** (decided 28 September, audit R126 (2)): each use of the session moves this to 30 days from now, and 30 days unused ends it. **One session per device**: a guest may be signed in on a phone and a laptop at once, and a new sign-in on the same `deviceId` ends that device's previous session.\n"}}},
"LoyaltyPosition": {"x-ticvai-persistence":"marketing.loyalty_position","type":"object","required":["subjectId","programmeId","pointsBalance","tierCode"],"properties":{"leaderboardNickname":{"type":"string","nullable":true,"maxLength":24,"description":"BL-173. **The name shown on a leaderboard, chosen by the guest.** Offered whenever they reach the board and changeable afterwards; `setLeaderboardNickname` is the only thing that writes it.\n**Null means the guest has not chosen one yet, and the board shows a generated `Player-4821` in its place** — never `pii.subject.display_name`, which would disclose silently on the day a guest first placed and is the case this field exists to prevent.\n**The generated name is computed at read time and not stored here.** Writing it would make *\"has this guest chosen a name\"* unanswerable, and that flag is what the prompt-on-reaching-the-board depends on.\n"},"subjectId":{"type":"string","format":"uuid"},"programmeId":{"type":"string","format":"uuid"},"pointsBalance":{"type":"integer"},"lifetimePoints":{"type":"integer"},"tierId":{"type":"string","format":"uuid","nullable":true,"description":"**The tier this row's `tierCode` and `tierName` are a copy of.** Added 20 September with `marketing.programme_tier`: the two strings were a cache of something that did not exist, and a cache with no source cannot be rebuilt or audited.\n"},"tierCode":{"type":"string"},"tierName":{"type":"string"},"pointsToNextTier":{"type":"integer","nullable":true},"nextExpiryPoints":{"type":"integer","nullable":true},"nextExpiryAt":{"type":"string","format":"date-time","nullable":true}}},
"MfaEnrolment": {"x-ticvai-persistence":"none — transient","type":"object","required":["methodId","kind"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The table had no key at all — no id, no parent and no natural key, so **no row could be addressed, updated or deleted.** The response schema returned everything a caller needs and not the row's own identity, which is the difference between an API response and a table.\n"},"methodId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/MfaKind"},"secret":{"type":"string","nullable":true,"description":"TOTP shared secret. Returned once, at enrolment, and never again."},"qrCodeUri":{"type":"string","nullable":true},"recoveryCodes":{"type":"array","description":"Returned once, in this enrolment response (`enrolMfaMethod` writes them, hashed, to `identity.mfa_recovery_code`). Not retrievable afterwards — `verifyMfaEnrolment` does not return them.\n","items":{"type":"string"}},"expiresAt":{"type":"string","format":"date-time"}}},
"MfaKind": {"type":"string","enum":["totp","smsOtp","emailOtp","biometric","hardwareToken"]},
"MfaMethod": {"x-ticvai-persistence":"identity.mfa_method","type":"object","required":["id","kind","isActive","enrolledAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/MfaKind"},"label":{"type":"string","nullable":true},"maskedTarget":{"type":"string","nullable":true,"description":"Partially masked destination, so a person can tell two methods apart."},"isActive":{"type":"boolean"},"isPrimary":{"type":"boolean"},"enrolledAt":{"type":"string","format":"date-time"},"lastUsedAt":{"type":"string","format":"date-time","nullable":true}}},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"Order": {"x-ticvai-persistence":"orders.sales_order + orders.order_line","type":"object","required":["id","venueId","scopePath","channel","status","currency","currencyScale","grossAmount","taxAmount","netAmount","lines","createdAt","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The client UUIDv7 from `CreateOrderRequest.id`."},"orderNumber":{"type":"string","readOnly":true,"description":"The number a guest reads and a cashier types. **Server-assigned: the venue prefix and a sequence per venue**, for example `DXB1-000123` (decided 28 September, audit R152). A till holds a reserved range of the venue sequence, so an order taken offline gets its number on the till and keeps it through `syncOrders`. **Not gapless**: an unused reserved range leaves a gap, and that is allowed. Only tax invoices are gapless, per legal entity. The receipt carries this number.\n"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for within a month of launch.\n"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"chargeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**The currency the guest selected and is charged in** (CHG-FIN-001, 2 October 2026). Null or equal to `currency` for a sale in the base currency. Everything else on the order, and every ledger posting, stays in the base currency `currency`."},"chargeFxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"readOnly":true,"description":"Units of `chargeCurrency` per one unit of the base currency, from the region's `tender` rate in force at checkout (`finance.FxRate`), stored on the order so the payment, the receipt, the tax invoice and any refund use the same rate (CHG-FIN-001)."},"chargeFxRateId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `finance.FxRate` row the rate was taken from, for audit."},"chargeTotal":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"`grossAmount` converted at `chargeFxRate` and rounded to the charge currency's scale: what the guest pays and what the payment request to the provider asks for (CHG-FIN-001)."},"chargeRateLockedUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"The quote holds until then (the cart lease). After it, the next payment attempt re-quotes at the rate then in force and the guest confirms the new amount (CHG-FIN-001)."},"droppedPromotions":{"type":"array","readOnly":true,"x-ticvai-persisted":false,"description":"**Promotions left off this order at checkout because their budget cap would have been exceeded** (decided 28 September, audit R101 (8)). Empty when none was dropped. Returned by `checkoutCart` and `createOrder`, not stored.\n","items":{"type":"object","required":["promotionId"],"properties":{"promotionId":{"type":"string","format":"uuid"},"name":{"type":"string"},"reason":{"type":"string","enum":["budgetCapReached"]}}}},"totalPriceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Sum across lines. Zero on a normal order."},"lines":{"type":"array","items":{"$ref":"#/components/schemas/OrderLine"}},"payments":{"type":"array","items":{"$ref":"#/components/schemas/Payment"}},"principalId":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid"},"shiftId":{"type":"string","format":"uuid","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"holdLabel":{"type":"string","maxLength":60,"nullable":true,"readOnly":true,"description":"The `label` a cashier gave when parking it with `holdOrder` — how they find it again. Null on an order never held."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When a held order expires and is voided (states/order.yaml), from `holdOrder`'s `holdUntil`. Null on an order not currently held."},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"OrderChannel": {"type":"string","description":"Where the order originated. Added when guest self-ordering was contracted — an order a guest placed on their own phone is commercially and operationally different from one a cashier typed, and reporting that cannot separate them cannot answer whether self-ordering is working.\n","enum":["pos","kiosk","guestApp","guestWeb","callCentre","partner","api","backOffice"]},
"OrderLine": {"x-ticvai-persistence":"orders.order_line + orders.order_line_eligibility + orders.order_line_discount","x-ticvai-retired-columns":["promotion_id","name","reason"],"allOf":[{"$ref":"#/components/schemas/CreateOrderLine"},{"type":"object","required":["serverUnitPrice","taxAmount","netAmount","grossAmount"],"properties":{"serverUnitPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the server computed on ingest."},"priceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Server minus quoted. Non-zero means the quoted price was honoured and the difference posted to the variance account.\n"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"entitlementIds":{"type":"array","description":"The entitlements this line issued. **These are the ticket ids** — `transferOrderTickets.ticketIds` and `reprintOrder.reissuedTicketIds` take and return them.","items":{"type":"string","format":"uuid"}},"crossRegionRightIds":{"type":"array","items":{"type":"string"},"description":"Redemption rights propagated to other cells for this line."},"reprintCount":{"type":"integer","minimum":0,"default":0,"readOnly":true,"description":"How many times this line's tickets were reprinted or resent. `reprintOrder` increments it; repeated reprints are the signal worth surfacing."},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"The order's venue, copied onto the line (ADR-0044's own example; system-design review SD-008, 29 September) so a line is scoped and partitionable without its order."},"discounts":{"type":"array","readOnly":true,"description":"**The discounts applied to this line, one row each** (system-design review SD-008, 29 September). Until then a discount object was flattened into the line as `promotion_id NOT NULL`, so a line with no promotion could not be inserted. A line with no discount has none.","items":{"$ref":"#/components/schemas/OrderLineDiscount"}}}}]},
"OrderStatus": {"type":"string","enum":["pending","held","paid","partiallyPaid","completed","voided","refunded","partiallyRefunded","failed"],"description":"`held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed.\n"},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Payment": {"x-ticvai-persistence":"orders.payment","type":"object","required":["id","orderId","tender","amount","status","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid"},"tender":{"$ref":"#/components/schemas/TenderKind"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","description":"4.6.11. **What the guest actually handed over**, which is not always what the venue books. A tourist paying USD cash at a till is a foreign tender; the sale is still recorded in base currency.\nEqual to the base currency for almost every payment. **Present on all of them so the foreign-tender report has a source** — `getForeignTenderReport` promised *what was taken in which currency* and nothing recorded it until 18 August.\n"},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"The amount in `tenderCurrency`, at that currency's own scale."},"fxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"description":"The rate applied, **stored on the payment rather than looked up later** (CF-37). A payment reconciled next month is reconciled at the rate of the day it was taken.\n"},"fxRateSource":{"type":"string","nullable":true,"enum":["manual","feed","cardScheme"],"description":"4.2.8. Manual or fed on a schedule. **`cardScheme` is where the terminal did the conversion and told us** — dynamic currency conversion, the scheme's rate rather than ours.\n"},"changeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"description":"4.6.11 is deliberately asymmetric: **accept foreign currency, refund in local.** A till giving change in five currencies needs five floats and five counts, and the variance becomes unattributable.\n**Cash at a till only** (CHG-FIN-001, 2 October 2026). A card or wallet payment the guest made in a currency they selected is refunded in that currency (`Refund.tenderCurrency`).\n"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"changeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["authorised","captured","pendingConfirmation","declined","failed","voided","refunded"]},"providerName":{"type":"string","nullable":true},"providerReference":{"type":"string","nullable":true,"description":"The provider's own id for the charge (Stripe PaymentIntent, NI order reference). What `payments.receivePaymentProviderWebhook` matches an incoming event on (SD-034)."},"providerIdempotencyKey":{"type":"string","nullable":true,"readOnly":true,"description":"The idempotency key sent to the provider, which is this payment's `id` (SD-034, 29 September). A retried provider call cannot charge twice."},"terminalId":{"type":"string","format":"uuid","nullable":true,"description":"The card terminal a till payment ran on (ECR flow, SD-034)."},"nextAction":{"type":"object","nullable":true,"x-ticvai-persisted":false,"description":"**What the caller does while the payment is `pendingConfirmation`** (SD-034, 29 September). `redirect`: send the browser to `url` (3-D Secure challenge or hosted page); the provider returns the guest to `returnUrl` and the result arrives by webhook. `terminal`: the card terminal has been instructed; wait for its result. Null once the payment has an outcome.","properties":{"kind":{"type":"string","enum":["redirect","terminal"]},"url":{"type":"string","format":"uri","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true}}},"lastInquiryAt":{"type":"string","format":"date-time","nullable":true},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"PaymentToken": {"type":"object","x-ticvai-persistence":"payments.token","description":"BL-116. **A stored credential, held by the provider and referenced here.** The platform never sees a card number, which is what keeps PCI scope where it belongs.\n**A token is provider-scoped.** A card tokenised with one gateway does not work with another, so a routing change does not silently move a guest's saved card — it means asking them again, and the model should make that visible rather than surprising.\n","required":["id","subjectId","providerId","token","isDefault"],"properties":{"id":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid"},"providerId":{"type":"string","format":"uuid"},"token":{"type":"string","format":"password","writeOnly":true,"description":"**Write-only, never returned.** The provider's reference to a credential it holds. Required on the stored row; absent from every response.\n"},"method":{"type":"string"},"maskedIdentifier":{"type":"string","description":"What a guest sees — the last four digits, the card brand. **Enough to choose between two saved cards and not enough to use one.**\n"},"expiresAt":{"type":"string","format":"date","nullable":true},"isDefault":{"type":"boolean"},"consentPurposeId":{"type":"string","format":"uuid","nullable":true,"description":"**Storing a card for future use is a purpose a guest consents to**, separate from the payment they are making now. A token taken without it is a card kept on a guest's behalf that they never agreed to.\n"}}},
"ResaleListing": {"type":"object","x-ticvai-persistence":"orders.resale_listing","description":"BL-060. **Smaller than it first looked** — most of the machinery exists. An entitlement can already be transferred, an order can already be created, and payment already routes. What was missing is the listing itself and a cart line that can point at one.\n**A resale is a transfer with money attached**, and the venue is in the middle: the buyer becomes the owner of the same entitlement (the virtual ticket ID is preserved, MoM 1 Sep 4.14), its media is re-issued and the transfer is logged, so **the media that admits is always one the venue issued.** That is what stops a screenshot at the gate.\n","required":["id","entitlementId","sellerSubjectId","askPrice","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"entitlementId":{"type":"string","format":"uuid"},"sellerSubjectId":{"type":"string","format":"uuid"},"askPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"priceCapPercent":{"type":"number","nullable":true,"readOnly":true,"description":"**A ceiling as a percentage of face value**, because uncapped resale is a venue watching its own tickets sold at four times the price with its name on them. Null means uncapped, which is a venue decision rather than a default. Snapshotted from `ResaleFeePolicy` at listing.\n"},"sellerFeePercent":{"type":"number","readOnly":true,"description":"Snapshotted from `ResaleFeePolicy` at listing."},"buyerFeePercent":{"type":"number","readOnly":true,"description":"Snapshotted from `ResaleFeePolicy` at listing."},"status":{"type":"string","readOnly":true,"enum":["pendingReview","listed","reserved","sold","withdrawn","expired","rejected"],"description":"`pendingReview` and `rejected` added 29 September (DM5): a listing the marketplace's `moderationMode` sends to review waits there until `approveListingModeration` lists or rejects it."},"listedAt":{"type":"string","format":"date-time","readOnly":true},"soldToSubjectId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"reviewReasons":{"type":"array","readOnly":true,"description":"Why the listing was sent to review (DM5, 29 September).","items":{"type":"string","enum":["highResalePrice","unusualDiscount","highValueTicket","vipTicket","sellerRisk","newSeller","multipleListings","identityIssue","paymentIssue","ticketOwnershipConcern","fraudIndicator"]}},"moderatedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"moderatedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"moderationReason":{"type":"string","maxLength":1000,"nullable":true,"readOnly":true},"payoutStatus":{"type":"string","readOnly":true,"enum":["pending","held","paid","failed"],"description":"**The seller is paid after the buyer is admitted, not after they pay.** A resale refunded at the gate for a void ticket cannot be clawed back from a seller who has already been paid.\n"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"Session": {"type":"object","required":["sessionId","principalId","roleId","scope","effectivePermissions"],"properties":{"sessionId":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid"},"roleId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"scope":{"type":"array","description":"Scope nodes this session may act within, resolved once at login from the ltree hierarchy with deny-overrides-allow. Clients filter navigation against this — they never compute it.\n","items":{"$ref":"../shared/common.yaml#/components/schemas/ScopeRef"}},"effectivePermissions":{"allOf":[{"$ref":"../shared/permissions.yaml#/components/schemas/PermissionSet"}],"description":"Flattened set across all granted scopes, after deny resolution. Convenience for coarse checks. Anything scope-sensitive must use `permissionsByScope`.\n"},"permissionsByScope":{"type":"array","description":"Permissions effective at each granted scope path. Clients filter navigation on this and never compute permissions themselves.\n","items":{"$ref":"../shared/permissions.yaml#/components/schemas/ScopedPermissions"}},"saleBoardId":{"type":"string","format":"uuid","description":"Landing surface, derived from the WORKSTATION, not the role (12 Aug 2026 §3). Ticketing, F&B or Retail board.\n\n**Optional since 2 October 2026: only a till session carries it** (Chinmay, door follow-ups; CHG-CSP-002; breaking change against r1 approved as BC-001 to BC-005 in `docs/active/breaking-changes.yaml`). A browser door (ADM-001, SUP-001, PTR-001) and a staff handheld (EMP-001) sign in with no workstation since CHG-DOOR-001, so they have no board to land on and the field is absent. On a till it is the workstation's effective board: the outlet's board unless the till overrides it (`tenancy.Workstation.saleBoardSource`; CHG-CSP-006). A client reads its landing from this field when present and from its own platform otherwise.\n"},"workstation":{"$ref":"#/components/schemas/WorkstationContext"},"openedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time"}}},
"TokenPair": {"x-ticvai-persistence":"none — transient","type":"object","required":["accessToken","refreshToken","expiresIn"],"properties":{"accessToken":{"type":"string","description":"JWT carrying `sid`, validated per request against the session registry."},"refreshToken":{"type":"string"},"expiresIn":{"type":"integer","description":"Seconds"}}},
"WalletTransaction": {"x-ticvai-persistence":"wallet.wallet_transaction","type":"object","required":["id","kind","amount","balanceAfter","recordedAt"],"properties":{"id":{"type":"string"},"walletId":{"type":"string","format":"uuid","x-ticvai-references":"wallet.wallet","description":"The wallet this movement is on (SD-027, 29 September). A shared wallet has many subjects, so the subject alone cannot say which balance moved."},"walletHoldId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"wallet.hold","description":"The hold a spend settled, where it came through `holdWalletFunds`."},"kind":{"$ref":"#/components/schemas/WalletTransactionKind"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"balanceAfter":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"orderId":{"type":"string","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"reason":{"type":"string","nullable":true},"principalId":{"type":"string","format":"uuid","nullable":true},"recordedAt":{"type":"string","format":"date-time"}}},
"WalletTransactionKind": {"type":"string","enum":["topUp","spend","refund","adjustment","bonus","expiry","transfer"]},
"WorkstationContext": {"type":"object","required":["id","code","venueId","regionId"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"regionId":{"type":"string","format":"uuid"},"accessPointId":{"type":"string","format":"uuid","description":"Inherited from the workstation, never selected by the operator."},"devices":{"type":"array","items":{"type":"object","required":["kind","driver"],"properties":{"kind":{"type":"string","enum":["receiptPrinter","ticketPrinter","cashDrawer","barcodeScanner","rfidReader","paymentTerminal","customerDisplay"]},"driver":{"type":"string"},"identifier":{"type":"string"}}}},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"currencyScale":{"type":"integer","minimum":0,"maximum":4},"timezone":{"type":"string"},"cellName":{"type":"string","description":"The cell serving this workstation's region. One cell per tenant per region (ADR-0014). A client uses this only for diagnostics and telemetry tagging — never for routing, which the Control Plane resolves.\n"},"deploymentProfile":{"type":"string","enum":["terminalLocal","venueEdge","thin"],"description":"Whether this surface reads catalogue locally (ADR-0013). Determines which flows the client enables offline.\n"}}}
}
```
