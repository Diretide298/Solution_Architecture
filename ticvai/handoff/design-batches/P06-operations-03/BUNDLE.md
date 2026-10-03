# P06-operations-03 — P06 · Operations (3 of 5)

**10 screens · 50 operations · 78 schemas · 23 permissions**

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

- **Every control that can be refused must be gated.** 23 permissions apply here:
  `AI_USE, ATTENDANCE_RECORD, CAPACITY_CONFIGURE, CASE_MANAGE, CASE_VIEW, GUEST_VIEW, INCIDENT_MANAGE, INCIDENT_REPORT, INCIDENT_VIEW, ORDER_CREATE, ORDER_DISCOUNT, ORDER_EXCHANGE`…. A control nobody can use must say so,
  not sit enabled and fail.
- **22 of these operations work offline**: addCaseMessage, addIncidentPerson, applyManualDiscount, createCase, createOrder, getOrder, getProduct, getQueue
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


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `EMP-031` | Queue monitor | D | 10 | 23 | 6 | 19 | 1 | 6 | — | notStarted (generated) |
| `EMP-032` | Manual wait entry | A | 3 | 10 | 6 | 4 | 1 | 0 | — | notStarted (generated) |
| `EMP-033` | Capacity view | B | 3 | 14 | 6 | 3 | 0 | 0 | — | notStarted (generated) |
| `EMP-034` | Walk-up sale | C | 127 | 34 | 6 | 93 | 1 | 0 | — | notStarted (generated) |
| `EMP-025` | Break management | D | 9 | 9 | 6 | 4 | 2 | 0 | — | notStarted (generated) |
| `EMP-026` | Incident report | A | 29 | 14 | 6 | 10 | 1 | 0 | — | notStarted (generated) |
| `EMP-027` | Incident detail | D | 20 | 14 | 7 | 1 | 0 | 0 | — | notStarted (generated) |
| `EMP-028` | Lost & found | D | 32 | 14 | 6 | 13 | 1 | 0 | — | notStarted (generated) |
| `EMP-029` | Guest assistance | D | 64 | 23 | 6 | 23 | 1 | 0 | — | notStarted (generated) |
| `EMP-030` | Venue map | C | 0 | 3 | 6 | 2 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**EMP-032, EMP-030 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `EMP-031` Queue monitor

**See the queue from the floor.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 2 · needs the `queue` module |
| Block | Block D · task APP-STAFF-EMP-031 |
| Who uses it | venue staff holding `AI_USE`, `QUEUE_MANAGE`, `QUEUE_VIEW` (1 operate, 1 configure, 1 read); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listQueues` reads the population and `getQueue` reads one of them — list, select, act |
| Offline | Last synced view with its age |
| Opens with | `queueId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/operations/queue-monitor` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Removed 24 August**: createQueue, updateQueue. **A handheld reads a queue and records a wait; it does not create one.** A queue is a venue configuration — bulk-attach residue, and `EMP-031` and `EMP-032` carried identical sets.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** A supervisor on the floor sees each ride's queue: current wait with source, general and virtual-queue waits separately, now serving, throughput, no-shows, and alerts (express queue growing, overall wait unusually long); can call the next parties, pause or close a queue, or enter a wait by hand. The one thing to get right: general and virtual waits side by side, with alerts first.

**Known correction pending (do not draw the wrong version)**

- **"Venue id" text field and AI requestSuggestion bound without a stated use** Why: Venue from session; an AI tip (DI-681 guest-flow tips) must be shown as a suggestion with its reason (VO-R11) or removed. *(source: screens/P06-staff-app.yaml#EMP-031 / DI-681; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listQueues`. | `listQueues` ?venueId |
| Open only | toggle | optional | off | — | — | Sends `?openOnly=` to `listQueues`. | `listQueues` ?openOnly |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category | picker: choose a category | — | — | `getWaitTimes` ?category |

**Form: Call next parties** (modal, opened by *Call next parties*; *Call next parties* calls `callNextParties`, *Cancel* sends nothing)

**Collects what `callNextParties` sends before it is called.** Nothing in the body is required. Optional: `partyCount`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Party count `partyCount` | number field | optional | — | min 1 | — | Defaults to the queue's capacity per cycle. | `callNextParties` body |

**Form: Save queue status** (modal, opened by *Save queue status*; *Save queue status* calls `setQueueStatus`, *Cancel* sends nothing)

**Collects what `setQueueStatus` sends before it is called.** Required: `status`, `reason`. Optional: `guestMessage`, `expectedReopenAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | radio group | required | — | Open · Paused · Closed · At capacity | — | — | `setQueueStatus` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `setQueueStatus` body |
| Guest message `guestMessage` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `setQueueStatus` body |
| Expected reopen at `expectedReopenAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setQueueStatus` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Form: Save wait time** (modal, opened by *Save wait time*; *Save wait time* calls `setWaitTime`, *Cancel* sends nothing)

**Collects what `setWaitTime` sends before it is called.** Required: `waitMinutes`. Optional: `expiresInMinutes`, `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Wait minutes `waitMinutes` | number field (minutes) | required | — | min 0 | — | — | `setWaitTime` body |
| Expires in minutes `expiresInMinutes` | number field (minutes) | optional | 30 | min 1 | — | How long this manual figure stands before the queue reverts. | `setWaitTime` body |
| Note `note` | text area | optional | — | max length 200 | — | — | `setWaitTime` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

#### Outputs: what the screen shows and produces

**Shown**

**Every queue** (data table, from `listQueues`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | in the reader's language | — |
| Kind | chip: Standby, Single rider, Fast pass, Virtual, Accessible, Group only… | 5.6.x. A ride has several queues and the model had one. |
| Notify before call minutes | 1,234 | BL-017, 19.2.61. A guest was not told their turn was approaching, which makes a virtual queue worse than a physical one — at least a line … |

**Every waiting guest** (data table, from `listQueueEntries`)

| Shows | Format | Notes |
|---|---|---|
| Queue name | in the reader's language | — |
| Party number | 1,234 | What the guest sees and what appears on signage. |
| Status | chip: Waiting, Called, Redeemed, Expired, No show, Cancelled… | — |
| Estimated call at | 1 Oct 2026, 14:30 | — |

**The selected queue** (detail panel, from `listQueues`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | in the reader's language | — |
| Notify before call minutes | 1,234 | BL-017, 19.2.61. A guest was not told their turn was approaching, which makes a virtual queue worse than a physical one — at least a line … |
| Capacity per cycle | 1,234 | — |
| Cycle minutes | 1,234.5 | — |

**The wait time** (detail panel, from `getWaitTimes`)

| Shows | Format | Notes |
|---|---|---|
| Queue name | in the reader's language | — |
| Status | chip: Open, Paused, Closed, At capacity | — |
| Wait minutes | 1,234 | Null where the queue is closed or no estimate is available. |
| Source | chip: Sensor, Throughput, Manual, Unavailable | Where the estimate came from. Surfaced so an operator knows whether a figure is measured or guessed. |
| Height requirement cm | 1,234 | — |

**The queue** (detail panel, from `getQueue`)

| Shows | Format | Notes |
|---|---|---|
| Now serving party number | 1,234 | — |
| Last called at | 1 Oct 2026, 14:30 | — |
| Throughput last hour | 1,234 | — |
| No show rate percent | 1,234.5 | — |
| Feed | grouped details | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Call next parties (primary button) | `callNextParties` POST `/queues/{queueId}/call-next` | inline | inline | — | opens modal first |
| Save queue status (secondary button) | `setQueueStatus` PUT `/queues/{queueId}/status` | inline | QueueStatusResult | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | works offline; opens modal first |
| Save wait time (secondary button) | `setWaitTime` PUT `/queues/{queueId}/wait-time` | inline | WaitTime | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | works offline; opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Queue cards**: Ride, standby wait and virtual wait separately with sources, now serving, throughput last hour, no-show %; alert badges. *(source: DI-681 / contracts/satellite/queue.yaml#getQueue / contracts/satellite/queue.yaml#getWaitTimes)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Call next parties / Pause / Close / Enter wait**: Close needs a reason and a guest message and notifies everyone waiting; Enter wait opens EMP-032. *(source: contracts/satellite/queue.yaml#callNextParties / contracts/satellite/queue.yaml#setQueueStatus / F67 step 2)*

**Data it reads**: `listQueues` (onLoad, List queues); `getWaitTimes` (onLoad, Wait times across a venue)

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*
- → `EMP-032` Manual wait entry: *The sensor is wrong, so a wait is entered by hand*; carries `queueId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The queue list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the queue untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No queue yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, openOnly and the queue are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `QUEUE_VIEW`, which `listQueues` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `AI_USE` for `requestSuggestion`; `QUEUE_MANAGE` for `callNextParties`, `setQueueStatus`, `setWaitTime`. |
| Offline (`?state=offline`) | Last synced view with its age |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 A setting the answer cannot do without is missing (29 September, AI functions review). (AiMissingSettingProblem) |

#### Edge cases to draw

- **Offline**: Last synced view with its age; status changes queue locally. *(source: screens/P06-staff-app.yaml#EMP-031 / contracts/satellite/queue.yaml#setQueueStatus)*

#### Consistency with other screens

- Match `BO-005`: Same labels as the back-office queue monitor.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
cards:
- ride: Falcon Coaster
  standby: 60 min Live
  virtual: 55 min
  serving: 198
  alert: Express queue growing
```

#### Permissions

- `listQueues` → `QUEUE_VIEW` (read) · staff, guest
- `getQueue` → `QUEUE_VIEW` (read) · staff
- `callNextParties` → `QUEUE_MANAGE` (configure) · staff
- `getWaitTimes` → no permission · guest, public
- `listQueueEntries` → `QUEUE_VIEW` (read) · staff
- `setQueueStatus` → `QUEUE_MANAGE` (configure) · staff
- `setWaitTime` → `QUEUE_MANAGE` (configure) · staff
- `requestSuggestion` → `AI_USE` (operate) · staff, guest

**A refused user sees:** Shown when the caller lacks `QUEUE_VIEW`, which `listQueues` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `AI_USE` for `requestSuggestion`; `QUEUE_MANAGE` for `callNextParties`, `setQueueStatus`, `setWaitTime`.

#### Requirements it meets

19 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.37 | Estimated Waiting Time - System shall provide estimated waiting times. | Guest Mobile App & Branding | CONTRACTED | `getWaitTimes` |
| 5.6.3 | Display queue lengths, wait times, throughput, capacity utilization, occupancy, and customer flow metrics. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.15 | Continuously calculate and display estimated waiting times. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.16 | Allow guests to view their live queue position and estimated service time. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.2 | Real-time Queue Dashboard: Staff view of queue lengths, wait times, and customer flow. | F&B & Guest Management | CONTRACTED | `listQueueEntries` |
| 5.6.29 | Maintain complete audit logs for reservations, transfers, modifications, cancellations, and check-ins. | F&B & Guest Management | CONTRACTED | `listQueueEntries` |
| 5.6.24 | Automatically recover queue reservations after operational disruptions. | F&B & Guest Management | CONTRACTED | `setQueueStatus` |
| 5.6.25 | Support automatic queue suspension and guest reallocation when attractions become unavailable. | F&B & Guest Management | CONTRACTED | `setQueueStatus` |
| 2.1.28 | Kiosks shall provide an AI assistant to guide guests through ticket selection, promotions, FAQs, recommendations, and checkout. | Ticketing Sales | CONTRACTED | `requestSuggestion` |
| 4.1.16 | Analyze menu performance and profitability. | Bundles and Promotions | CONTRACTED | `requestSuggestion` |
| 4.1.19 | Recommend actions to reduce waste and spoilage. | Bundles and Promotions | CONTRACTED | `requestSuggestion` |
| 4.1.20 | Recommend pricing and promotion strategies. | Bundles and Promotions | CONTRACTED | `requestSuggestion` |
| … 7 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Ops view shows current wait per ride with general and virtual-queue waits separately, and alerts for e.g. a growing express queue or unusually long overall queue. *(client request · MoM 7 Sep 2026, 4.17 Virtual Queue - Operations Dashboard & AI Guest Flow Optimization · DI-681)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'wait-time')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A244** Build virtual queue with 3 guest tiers (walk-in, VQ, VIP); keep VQ separate from VIP lane *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A245** Recalculate virtual queue return times live, not fixed at booking *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A246** Support virtual queue via app (theme parks) and kiosk/wristband scan (water parks) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A247** Build virtual queue ops dashboard, AI guest-flow tips and fast-lane upsell on long waits *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-031` · status **notStarted** · provenance generated
- Flow F67 *A queue is monitored and capacity is held*, step 1: The supervisor reads the queue. → **Adaptor-first** (ADR-0012): the reading comes from whatever queue system the venue runs, and the platform holds what it reports.
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)
- ADR-0012 *Queue Integration — Adaptor-First, Vendor Deferred* (`docs/adr/0012-queue-integration-adaptor-first.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state (403, 404, 422).
- [ ] Every output is drawn (23 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-031?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Call next parties, Save queue status, Save wait time.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`, `EMP-032`.
- [ ] Every gated control is gated: `AI_USE`, `QUEUE_MANAGE`, `QUEUE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-032` Manual wait entry

**Take over when the wait feed dies.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `queue` module |
| Block | Block A · task APP-STAFF-EMP-032 |
| Who uses it | venue staff holding `QUEUE_MANAGE`, `QUEUE_VIEW` (1 configure, 1 read); in the flows as guest, supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listQueueEntries` reads the population and `getWaitTimes` reads one of them — list, select, act |
| Offline | **Queues locally.** Manual entry exists because a feed died, so it must not need the network the feed lost |
| Opens with | `queueId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/operations/manual-wait-entry` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Cross-platform navigation removed 24 August**: BO-005. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link. **Removed 24 August**: callNextParties, createQueue, setQueueStatus, updateQueue. **A handheld reads a queue and records a wait; it does not create one.** A queue is a venue configuration — bulk-attach residue, and `EMP-031` and `EMP-032` carried identical sets.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): The waiting-guest table and queue list do not serve manual wait entry; only the chosen ride's wait and its source are needed (design-notes correction … Removed 2 October 2026 (CHG-WIR-001): The waiting-guest table and queue list do not serve manual wait entry; only the chosen ride's wait and its source are needed (design-notes correction …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Take over when the wait feed dies: a supervisor at the queue sets the wait by hand, valid for a stated time, recorded as a manual reading. It must work offline. The one thing to get right: one ride, one big stepper, a valid-for choice, Save.

**Fixed on main** (the package already carries these; draw what it says): Waiting-guest table and queue list on the manual entry screen (CHG-WIR-001).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category | picker: choose a category | — | — | `getWaitTimes` ?category |

**Form: Save wait time** (modal, opened by *Save wait time*; *Save wait time* calls `setWaitTime`, *Cancel* sends nothing)

**Collects what `setWaitTime` sends before it is called.** Required: `waitMinutes`. Optional: `expiresInMinutes`, `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Wait minutes `waitMinutes` | number field (minutes) | required | — | min 0 | — | — | `setWaitTime` body |
| Expires in minutes `expiresInMinutes` | number field (minutes) | optional | 30 | min 1 | — | How long this manual figure stands before the queue reverts. | `setWaitTime` body |
| Note `note` | text area | optional | — | max length 200 | — | — | `setWaitTime` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Wait and valid for**: As BO-004 (5-minute stepper, 15/30/60 minutes validity, note). *(source: contracts/satellite/queue.yaml#setWaitTime)*

#### Outputs: what the screen shows and produces

**Shown**

**The queue** (detail panel, from `getQueue`)

| Shows | Format | Notes |
|---|---|---|
| Now serving party number | 1,234 | — |
| Last called at | 1 Oct 2026, 14:30 | — |
| Throughput last hour | 1,234 | — |
| No show rate percent | 1,234.5 | — |
| Feed | grouped details | — |

**The wait time** (detail panel, from `getWaitTimes`)

| Shows | Format | Notes |
|---|---|---|
| Queue name | in the reader's language | — |
| Status | chip: Open, Paused, Closed, At capacity | — |
| Wait minutes | 1,234 | Null where the queue is closed or no estimate is available. |
| Source | chip: Sensor, Throughput, Manual, Unavailable | Where the estimate came from. Surfaced so an operator knows whether a figure is measured or guessed. |
| Height requirement cm | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save wait time (primary button) | `setWaitTime` PUT `/queues/{queueId}/wait-time` | inline | WaitTime | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | works offline; opens modal first |

**Data it reads**: `getWaitTimes` (onLoad, Wait times across a venue)

**Where the user goes next**

- → `EMP-033` Capacity view: *Capacity is checked against occupancy*
- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*
- → `BO-005` Queue Monitor: *Parties are called*; carries `queueId`; calls `setWaitTime`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The manual wait entry list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the manual wait entry untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No manual wait entry yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on status and the manual wait entry are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `QUEUE_VIEW`, which `getQueue` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Queues locally.** Manual entry exists because a feed died, so it must not need the network the feed lost |

#### Edge cases to draw

- **Offline**: Queued locally and applied with the device time. *(source: screens/P06-staff-app.yaml#EMP-032)*

#### Consistency with other screens

- Match `BO-004`: Same action and labels.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
entry:
  ride: Laser Arena
  wait: 25
  validFor: 30 min
```

#### Permissions

- `setWaitTime` → `QUEUE_MANAGE` (configure) · staff
- `getWaitTimes` → no permission · guest, public
- `getQueue` → `QUEUE_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `QUEUE_VIEW`, which `getQueue` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.37 | Estimated Waiting Time - System shall provide estimated waiting times. | Guest Mobile App & Branding | CONTRACTED | `getWaitTimes` |
| 5.6.3 | Display queue lengths, wait times, throughput, capacity utilization, occupancy, and customer flow metrics. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.15 | Continuously calculate and display estimated waiting times. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.16 | Allow guests to view their live queue position and estimated service time. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- **Open question.** Open: how per-ride occupancy is counted (entry sensors, manual security counts, CCTV/computer vision); Allam to check with Warner Bros. World, which has a visible wait-time display. Manual count entry stays a possible source. *(open · MoM 7 Sep 2026, 4.16 Wait-Time Calculation & People-Counting Technology · DI-680)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-032` · status **notStarted** · provenance generated
- Flow F21 *A ride queue fills and a guest is redirected*, step 4: The feed dies and a supervisor types the wait → **Manual entry is first-class** (ADR-0012), not a fallback bolted on
- Flow F67 *A queue is monitored and capacity is held*, step 2: The sensor is wrong, so a wait is entered by hand. → **A manual reading is a reading.** A supervisor standing at the queue is a better sensor than a broken beam, and the source is recorded so nobody trusts the two equally later.
- Flow F21 branch at step 4 (recoverable): when The feed dies mid-day, `getQueueFeedHealth` flags it. Manual entry takes over, and the guest app shows a wait typed by a person rather than nothing.
- ADR-0012 *Queue Integration — Adaptor-First, Vendor Deferred* (`docs/adr/0012-queue-integration-adaptor-first.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-032?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save wait time.
- [ ] Every transition is wired: `EMP-033`, `EMP-001`, `EMP-002`, `EMP-003`, `BO-005`.
- [ ] Every gated control is gated: `QUEUE_MANAGE`, `QUEUE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-033` Capacity view

**Know whether the next session can take a walk-up.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 2 · needs the `ticketing` module |
| Block | Block B · task APP-STAFF-EMP-033 |
| Who uses it | venue staff holding `CAPACITY_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listChannelCapacities` reads the population and `getChannelAllocations` reads one of them — list, select, act |
| Offline | Last synced, with age |
| Opens with | `channelCapacityId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/operations/capacity-view` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-018): Capacity authoring (create envelope, save allocations, save capacity) is a back-office job; the handheld's purpose is to read (design-notes correction … Removed 2 October 2026 (CHG-WIR-018): Capacity authoring (create envelope, save allocations, save capacity) is a back-office job; the handheld's purpose is to read (design-notes correction … Removed 2 October 2026 (CHG-WIR-018): Capacity authoring (create envelope, save allocations, save capacity) is a back-office job; the handheld's purpose is to read (design-notes correction …

**From the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process.** Capacity view: can the next session take a walk-up? After Block A. Read-mostly: remaining per channel for today's sessions.

**Fixed on main** (the package already carries these; draw what it says): Create channel capacity, Save channel allocations and Save channel capacity on a steward's handheld. (CHG-WIR-018).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Performance id | picker: choose a performance (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?performanceId=` to `listChannelCapacities`. | `listChannelCapacities` ?performanceId |

**Form: Release channel allocation** (modal, opened by *Release channel allocation*; *Release channel allocation* calls `relinquishChannelAllocation`, *Cancel* sends nothing)

**Collects what `relinquishChannelAllocation` sends before it is called.** Required: `channels`. Optional: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Channels `channels` | multi-select chips | required | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre; at least 1 | — | — | `relinquishChannelAllocation` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `relinquishChannelAllocation` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every channel capacity** (data table, from `listChannelCapacities`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Capacity | 1,234 | — |
| Sold | 1,234 | Units sold. Maintained on write (decided 29 September, SD-023): raised by `convertInventoryHold` in the order transaction and by … |
| Remaining | 1,234 | What can still be held. Decremented at the hold with a guarded statement (`remaining >= n`) under the row lock, never at the sale, so two … |

**The selected channel capacity** (detail panel, from `listChannelCapacities`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Oversell allowance | 1,234 | BL-046, 1.3.13. The guard existed in one direction — an envelope could be raised freely and refused reduction below what had sold. |
| Capacity | 1,234 | — |
| Sold | 1,234 | Units sold. Maintained on write (decided 29 September, SD-023): raised by `convertInventoryHold` in the order transaction and by … |
| Remaining | 1,234 | What can still be held. Decremented at the hold with a guarded statement (`remaining >= n`) under the row lock, never at the sale, so two … |

**The channel allocation set** (detail panel, from `getChannelAllocations`)

| Shows | Format | Notes |
|---|---|---|
| Capacity | 1,234 | — |
| Allocations | list or chips (count when long) | — |
| General pool units | 1,234 | Unallocated remainder. Any channel may draw from it once its own allocation is exhausted. |
| Total sold | 1,234 | — |
| Total remaining | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Release channel allocation (secondary button) | `relinquishChannelAllocation` POST `/channel-capacities/{channelCapacityId}/channel-allocations/release` | inline | ChannelAllocationSet | — | opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **session capacity**: Each session with remaining for walk-up (onsite allocation) and total; low and sold out marked. *(source: screens/P06-staff-app.yaml#EMP-033 purpose)*

**Data it reads**: `listChannelCapacities` (onLoad, List capacity envelopes)

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The capacity list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the capacity untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No capacity yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on performanceId and the capacity are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listChannelCapacities` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `CAPACITY_CONFIGURE` for `relinquishChannelAllocation`. |
| Offline (`?state=offline`) | Last synced, with age |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
sessions:
- 14:00 · onsite 12 left of 40
- 15:00 · onsite 0 (online 6)
```

#### Permissions

- `listChannelCapacities` → `PRODUCT_VIEW` (read) · staff, partner
- `getChannelAllocations` → `PRODUCT_VIEW` (read) · staff, partner
- `relinquishChannelAllocation` → `CAPACITY_CONFIGURE` (configure) · staff, partner

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listChannelCapacities` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `CAPACITY_CONFIGURE` for `relinquishChannelAllocation`.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.13.40 | Capacity Management Visibility | Ticketing Sales | CONTRACTED | `listChannelCapacities` |
| 8.9.2 | System shall display current attendance, occupancy levels, capacity utilization, and crowd distribution across parks, venues, facilities, and attractions. | Unified Operations Dashboard | CONTRACTED | `listChannelCapacities` |
| 1.3.13 | The system should have the option to allow over sales for free events. | Ticketing Catalogue | CONTRACTED | data `ChannelCapacity` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-033` · status **notStarted** · provenance generated
- Flow F67 *A queue is monitored and capacity is held*, step 3: Capacity is checked against occupancy. → **Capacity is an envelope, not a headcount.** allocates capacity across channels — holding admission means taking it off the channels, which is a venue-wide act rather than a lane one.
- Flow F67 branch at step 3 (high): when Occupancy reaches the safety limit., **Channel allocations are pulled back rather than a lane refusing.** A capacity limit enforced per lane is not a limit — releasing the allocation stops every channel at once, including the web.

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-033?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Release channel allocation.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-034` Walk-up sale

**Sell at the gate without a till.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 2 · needs the `ticketing` module |
| Block | Block C · task APP-STAFF-EMP-034 |
| Who uses it | venue staff holding `ORDER_CREATE`, `ORDER_DISCOUNT`, `ORDER_EXCHANGE`, `ORDER_MODIFY`, `ORDER_REFUND`, `ORDER_REPRINT`… (8 operate, 2 read); in the flows as cashier |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listProducts` reads the population and `getOrder` reads one of them — list, select, act |
| Offline | **Cash only offline.** Card completes nowhere the acquirer saw it |
| Opens with | `orderId` (deepLink), `productId` (deepLink) · cold entry: **A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the … |
| Route | `/operations/walk-up-sale` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Removed 24 August**: createProduct, updateProduct. **Bulk-attach residue, found by walking a journey.** A device-settings screen does not read guest loyalty, a venue map does not set a refund policy, a shift summary does not close the shift, and **a rota a steward can rewrite is not a rota.**

**Known gaps.** Removed 2 October 2026 (CHG-WIR-018): Product authoring (alternative codes, attributes, lifecycle) on a walk-up sale; a seller does not author the catalogue (design-notes correction ticketing-guest … Removed 2 October 2026 (CHG-WIR-018): Product authoring (alternative codes, attributes, lifecycle) on a walk-up sale; a seller does not author the catalogue (design-notes correction ticketing-guest … Removed 2 October 2026 (CHG-WIR-018): Product authoring (alternative codes, attributes, lifecycle) on a walk-up sale; a seller does not author the catalogue (design-notes correction ticketing-guest …

**From the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process.** Walk-up sale on the handheld at the gate, without a till. After Block A. A small catalogue, quantities, card on the device or cash; capacity products blocked offline.

**Fixed on main** (the package already carries these; draw what it says): Product authoring actions (Save alternative codes, Save product attributes, Transition product lifecycle) on a walk-up sale. (CHG-WIR-018).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listProducts`. | `listProducts` ?venueId |
| Kind | select | optional | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | — | Sends `?kind=` to `listProducts`. | `listProducts` ?kind |
| Is sellable | toggle | optional | — | — | — | Sends `?isSellable=` to `listProducts`. | `listProducts` ?isSellable |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category | picker: choose a category | — | — | `listProducts` ?categoryId |
| Segment tag | text field | — | max length 120 | `listProducts` ?segmentTag |
| Guided answers | multi-picker: choose guided answers | — | at most 10 | `listProducts` ?guidedAnswerIds |
| Principal | picker: choose a principal | — | — | `listOrders` ?principalId |
| Shift | picker: choose a shift | — | — | `listOrders` ?shiftId |
| Status | select | — | Pending · Held · Paid · Partially paid · Completed · Voided · Refunded · Partially refunded · Failed; It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed. | `listOrders` ?status |
| Created from | date and time picker | — | — | `listOrders` ?createdFrom |
| Created to | date and time picker | — | — | `listOrders` ?createdTo |
| Workstation | picker: choose a workstation | — | — | `listOrders` ?workstationId |
| Subject | picker: choose a subject | — | — | `listOrders` ?subjectId |
| Tender | select | — | Cash · Card · Wallet · Voucher · Bank transfer · Hotel charge · Installment · Gift card · Complimentary | `listOrders` ?tender |

**Form: Split order** (modal, opened by *Split order*; *Split order* calls `splitOrder`, *Cancel* sends nothing)

**Collects what `splitOrder` sends before it is called.** Required: `groups`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Groups `groups` | repeatable rows | required | — | at least 2 | — | — | `splitOrder` body |
| Lines `groups[].lineIds` | multi-picker: choose lines | optional | — | — | — | — | `splitOrder` body |
| Subject `groups[].subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | — | `splitOrder` body |

Errors to draw in the form: 409 The order is partly paid and the payment is not yet allocated to lines (`paymentNotAllocated`), which the description makes a precondition of splitting. (OrderRefusedProblem)

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

**Form: Apply manual discount** (modal, opened by *Apply manual discount*; *Apply manual discount* calls `applyManualDiscount`, *Cancel* sends nothing)

**Collects what `applyManualDiscount` sends before it is called.** Required: `id`, `reason`, `recordedAt`. Optional: `lineId`, `amount`, `percentage`, `reasonCode`, `approverPrincipalId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of this discount, and its idempotency key — it must equal the `Idempotency-Key` header. | `applyManualDiscount` body |
| Line `lineId` | picker: choose a line | optional | — | — | shows names, sends the id | Omit to discount the order rather than a line. | `applyManualDiscount` body |
| Amount `amount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `applyManualDiscount` body |
| Percentage `percentage` | stepper or slider (%) | optional | — | min 0; max 100 | — | — | `applyManualDiscount` body |
| Reason `reason` | text area | required | — | min length 3; max length 300 | — | Required, and free text rather than a code list. A cashier forced to pick the nearest reason picks the first one, and the register stops meaning anything. | `applyManualDiscount` body |
| Reason code `reasonCode` | text field | optional | — | — | — | Optional alongside the free text, where the venue maintains a list. | `applyManualDiscount` body |
| Approver principal `approverPrincipalId` | picker: choose an approver principal | optional | — | — | shows names, sends the id | Required above the venue threshold. May not be the requester. | `applyManualDiscount` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `applyManualDiscount` body |

Errors to draw in the form: 403 Above the cashier's limit and no approver supplied (`approverRequired`), or the approver is the requester (`approverIsRequester`). (OrderRefusedProblem)

**Form: Create refund** (modal, opened by *Create refund*; *Create refund* calls `createRefund`, *Cancel* sends nothing)

**Collects what `createRefund` sends before it is called.** Required: `id`, `amount`, `reason`, `recordedAt`. Optional: `lineIds`, `secondaryAuthorisation`, `refundToOriginalTender`, `alternateTender`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the refund, and its idempotency key — it must equal the `Idempotency-Key` header. | `createRefund` body |
| Lines `lineIds` | multi-picker: choose lines | optional | — | — | — | Omit to refund the whole order. | `createRefund` body |
| Amount `amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createRefund` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `createRefund` body |
| Secondary authorisation `secondaryAuthorisation` | group | optional | — | — | — | Required above the venue's `requiresSecondUserAbove`. A second user — cashier or supervisor — names themselves. | `createRefund` body |
| Principal `secondaryAuthorisation.principalId` | picker: choose a principal | required | — | — | shows names, sends the id | — | `createRefund` body |
| Credential `secondaryAuthorisation.credential` | text area | required | — | max length 512 | — | The second person's staff PIN, as they sign in at a till with it. A PIN, never a password (decided 28 September, audit R123 (7)). | `createRefund` body |
| Refund to original tender `refundToOriginalTender` | toggle | optional | on | — | — | — | `createRefund` body |
| Alternate tender `alternateTender` | select | optional | — | Cash · Card · Wallet · Voucher · Bank transfer · Hotel charge · Installment · Gift card · Complimentary | — | `wallet` is a digital wallet (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 … | `createRefund` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createRefund` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Second authorisation required and absent (`secondAuthorisationRequired`), refund window closed (`refundWindowClosed`), or the amount exceeds what remains … (RefundPolicyProblem)

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

**Sent by *Void order*** (`voidOrder`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of this void, and its idempotency key — it must equal the `Idempotency-Key` header. | `voidOrder` body |
| Reason `reason` | select | required | — | Guest changed mind · Entered in error · Item unavailable · Quality issue · Duplicate · Other | — | The void reason list (decided 28 September, audit R125 (4)): the one list `voidOrder` takes, and the list `fnb.amendFnbOrder` and `fnb.cancelFnbOrder` point to. | `voidOrder` body |
| Note `note` | text area | optional | — | min length 3; max length 500; Required when `reason` is `other` (audit R222); optional otherwise. | — | Required when `reason` is `other` (audit R222); optional otherwise. | `voidOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `voidOrder` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every product** (data table, from `listProducts`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Description | text | — |
| On sale from | 1 Oct 2026, 14:30 | 1.4.8. A seasonal product should not need somebody awake at midnight. |

**Every alternative code** (data table, from `listAlternativeCodes`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Partner name | text | — |
| Note | text | — |

**Every refund** (data table, from `listOrderRefunds`)

| Shows | Format | Notes |
|---|---|---|
| FX rate | text | The rate on the original payment, not today's (BL-087, CF-118). `Payment` records `tenderCurrency`, `fxRate` and `fxRateSource` at the … |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Applied percentage | 1,234.5 | From the venue's time bands, or an approver override. |
| Status | chip: Pending approval, Pending gateway, Completed, Declined, Failed | — |

**Every order** (data table, from `listOrders`)

| Shows | Format | Notes |
|---|---|---|
| Order number | text | — |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Line count | 1,234 | — |
| Hold label | text | As `Order.holdLabel`. |

**Every product variant** (data table, from `listProductVariants`)

| Shows | Format | Notes |
|---|---|---|
| SKU | text | — |
| Axis values | grouped details | — |
| Name | text | Taken from their variant tables, 20 September. `axisValues` gives `{size: L}` and no string a guest can read. |
| Barcode | text | Taken from their variant tables, 20 September. `catalogue.alternative_code` is a partner's own code for a variant and requires `partnerId` … |

**The selected product** (detail panel, from `getProduct`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Kind | chip: Admission, Timed admission, Dated admission, Open dated, Seated, Membership… | `openDated` added 24 August from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no … |
| Lifecycle state | chip: Draft, In review, Approved, Live, Withdrawn, Archived | — |

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
| Create order (primary button) | `createOrder` POST `/orders` | CreateOrderRequest | Order | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 A lease covering a line has expired (`leaseExpired`), capacity is exhausted (`capacityExhausted`), or the catalogue bundle the … | works offline; opens modal first |
| Apply manual discount (secondary button) | `applyManualDiscount` POST `/orders/{orderId}/discounts` | ManualDiscountRequest | Order | 403 Above the cashier's limit and no approver supplied (`approverRequired`), or the approver is the requester (`approverIsRequester`). (OrderRefusedProblem) | works offline; opens modal first |
| Create refund (secondary button) | `createRefund` POST `/orders/{orderId}/refunds` | CreateRefundRequest | Refund | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Second authorisation required and absent (`secondAuthorisationRequired`), refund window closed (`refundWindowClosed`), or the amount … | opens modal first |
| Exchange order lines (secondary button) | `exchangeOrderLines` POST `/orders/{orderId}/exchanges` | ExchangeOrderRequest | OrderExchangeResult | 409 Replacement unavailable (`replacementUnavailable`), outside the exchange window (`outsideExchangeWindow`), or the original is redeemed (`lineRedeemed`). (OrderRefusedProblem) | opens modal first |
| Hold order (secondary button) | `holdOrder` POST `/orders/{orderId}/hold` | inline | Order | 409 Order is already paid (`alreadyPaid`) or voided (`orderVoided`) — only a `pending` order is parked — or a seated line's lease ends before `holdUntil` … (OrderRefusedProblem) | works offline; opens modal first |
| Modify order (secondary button) | `modifyOrder` POST `/orders/{orderId}/modify` | ModifyOrderRequest | OrderModificationResult | 409 A targeted line's entitlement has been redeemed (`lineRedeemed`, naming it in `lineIds`), or the order is voided (`orderVoided`). (OrderRefusedProblem) | opens modal first |
| Reprint order (secondary button) | `reprintOrder` POST `/orders/{orderId}/reprints` | inline | inline | 400 Validation failed | works offline; opens modal first; produces a document or message: Reprint or resend tickets |
| Reschedule order (secondary button) | `rescheduleOrder` POST `/orders/{orderId}/reschedule` | inline | OrderExchangeResult | 409 Target performance is unavailable (`targetUnavailable`) or outside the reschedule window (`outsideRescheduleWindow`). (OrderRefusedProblem) | opens modal first |
| Resolve product by code (secondary button) | `resolveProductByCode` GET `/products/resolve` | — | ProductVariant | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Resume order (secondary button) | `resumeOrder` POST `/orders/{orderId}/resume` | — | OrderResumeResult | 409 Held order expired (`holdExpired`), or already resumed at another till (`alreadyResumed`). (OrderRefusedProblem) | — |
| Void order (destructive button) | `voidOrder` POST `/orders/{orderId}/voids` | inline | Order | 409 Settled — a payment on the order has been `captured`, so the money has moved (`alreadySettled`) — or taken in a shift that is now closed (`shiftClosed`). (OrderRefusedProblem) | works offline |
| Split order (secondary button) | `splitOrder` POST `/orders/{orderId}/split` | inline | inline | 409 The order is partly paid and the payment is not yet allocated to lines (`paymentNotAllocated`), which the description makes a precondition of splitting. (OrderRefusedProblem) | opens modal first |

**Data it reads**: `listProducts` (onLoad, List products); `listOrders` (onLoad, List orders)

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*
- → `EMP-036` Issue media: *Issue media*
- → `EMP-035` Payment on device: *The guest taps a card on the device*; carries `paymentId`

**What opens over it**

- confirmDialog *Void order*: **Names what `voidOrder` changes and what it leaves alone**, in the consequence rather than the verb. A walk-up sale this affects should be identified in the dialog, not just counted. **Collects what `voidOrder` sends before it is called.** Required: `id`, `reason`, `recordedAt`. `reason` is picked …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The walk-up sale list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the walk-up sale untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No walk-up sale yet. Offers Create order (`createOrder`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, kind, isSellable and the walk-up sale are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listProducts` requires to show this screen, and names that permission (the screen's other reads need `ORDER_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ORDER_CREATE` for `createOrder`; `ORDER_DISCOUNT` for … |
| Offline (`?state=offline`) | **Cash only offline.** Card completes nowhere the acquirer saw it |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A `categoryId` that names no category of the venue, or a `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 …; 400 Validation failed; 409 A lease covering a line has expired (`leaseExpired`), capacity is exhausted (`capacityExhausted`), or the catalogue bundle the client priced from is beyond its … (OrderRefusedProblem); 409 A targeted line's … |

#### Edge cases to draw

- **Offline**: Cash only; capacity-bound products blocked with a notice. *(source: screens/P06-staff-app.yaml#EMP-034 states.offline; DI-074)*

#### Consistency with other screens

- Match `POS-002`: Same cart lines and limits.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
sale: Day Pass · Adult × 2 · AED 490 · card
```

#### Permissions

- `createOrder` → `ORDER_CREATE` (operate) · staff, guest, partner
- `listProducts` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `applyManualDiscount` → `ORDER_DISCOUNT` (operate) · staff, partner
- `createRefund` → `ORDER_REFUND` (operate) · staff, partner
- `exchangeOrderLines` → `ORDER_EXCHANGE` (operate) · staff, partner
- `getOrder` → `ORDER_VIEW` (read) · staff, guest, partner
- `getOrderStatement` → `ORDER_VIEW` (read) · staff, partner
- `getProduct` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `holdOrder` → `ORDER_MODIFY` (operate) · staff, partner
- `listAlternativeCodes` → `PRODUCT_VIEW` (read) · staff, partner
- `listOrderRefunds` → `ORDER_VIEW` (read) · staff, partner
- `listOrders` → `ORDER_VIEW` (read) · staff, guest, partner
- `listProductVariants` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `modifyOrder` → `ORDER_MODIFY` (operate) · staff, partner
- `reprintOrder` → `ORDER_REPRINT` (operate) · staff, guest, partner, device
- `rescheduleOrder` → `ORDER_RESCHEDULE` (operate) · staff, partner
- `resolveProductByCode` → `PRODUCT_VIEW` (read) · staff, partner
- `resumeOrder` → `ORDER_MODIFY` (operate) · staff, partner
- `voidOrder` → `ORDER_VOID` (operate) · staff, partner
- `splitOrder` → `ORDER_MODIFY` (operate) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listProducts` requires to show this screen, and names that permission (the screen's other reads need `ORDER_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ORDER_CREATE` for `createOrder`; `ORDER_DISCOUNT` for …

#### Requirements it meets

93 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| 2.6.7 | For BtoC online sales, the following points shall be available online: | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.6.8 | - All PLUs | Ticketing Sales | CONTRACTED | `listProducts` |
| … 81 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Selling a capacity-based product (e.g. seat-assigned tickets) while offline is blocked with a clear notification, never allowed through or silently failing; non-capacity products stay sellable offline. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-074)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-034` · status **notStarted** · provenance generated
- Flow F66 *A walk-up sale is taken on a handheld*, step 1: The seller finds the product and takes the order. → **The same catalogue bundle the tills hold.** A roaming seller quoting a different price from the window ten metres away is a complaint.
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (127), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (34 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-034?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Create order, Apply manual discount, Create refund, Exchange order lines, Hold order, Modify order, Reprint order, Reschedule order, Resolve product by code, Resume order, Void order, Split order.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`, `EMP-036`, `EMP-035`.
- [ ] Every gated control is gated: `ORDER_CREATE`, `ORDER_DISCOUNT`, `ORDER_EXCHANGE`, `ORDER_MODIFY`, `ORDER_REFUND`, `ORDER_REPRINT`, `ORDER_RESCHEDULE`, `ORDER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-025` Break management

**Take a break without leaving a gate unstaffed.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 2 · needs the `core` module |
| Block | Block D · task APP-STAFF-EMP-025 |
| Who uses it | venue staff holding `ATTENDANCE_RECORD`, `WORKFORCE_VIEW` (1 operate, 1 read); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listAttendance` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | Queues locally |
| Opens with | `recordId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/operations/break-management` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Removed 24 August**: amendAttendance. **Bulk-attach residue, found by walking a journey.** A device-settings screen does not read guest loyalty, a venue map does not set a refund policy, a shift summary does not close the shift, and **a rota a steward can rewrite is not a rota.**

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Break management: a steward takes a break without leaving a gate or counter unstaffed. They see when their break is due under the shift's break policy, ask for cover, start the break, and end it. The one thing to get right: the break is tied to cover - the person sees who is covering (or that nobody is) before leaving the post - and the break timer is unmissable.

**Known correction pending (do not draw the wrong version)**

- **The contract records breaks only as they happen (breakStart, breakEnd); there is no planned break window and no cover request** Why: DI-237 asks staff to log break windows so a replacement can be scheduled, and DI-491 names swap requests for break cover; requestShiftSwap moves a whole shift, not a 30-minute window. *(source: DI-237 / DI-491 / contracts/satellite/workforce.yaml#recordAttendance / contracts/satellite/workforce.yaml#requestShiftSwap; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Generic attendance list with "Principal id" filter, latitude and longitude columns** Why: The screen is one person's break; a venue list is BO-056. *(source: screens/P06-staff-app.yaml#EMP-025; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **How is break cover arranged - a planned reliever on the rota, a request to the supervisor, or a swap of the window?** → Drawn default accepted: Show the planned reliever if the rota has one, otherwise "Ask for cover" as a message to the supervisor. *(decided by Chinmay, 2026-10-02; DEC-528 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

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

- **Start break**: One button, enabled from the earliest break time in the policy; before that it shows "Break from 11:00". The kind sent is breakStart with device time; no time entry. *(source: contracts/satellite/workforce.yaml#recordAttendance / contracts/satellite/workforce.yaml#/components/schemas/ShiftTemplate)*
- **Cover**: Who will cover the post: the planned reliever from the rota if any, otherwise "Ask for cover" (to the supervisor or the team). Shown as "Covered by Omar Haddad" or "No cover yet". *(source: DI-237 / DI-491 / contracts/satellite/workforce.yaml#sendStaffMessage)*

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
| Latitude | 1,234.5 | — |
| Original occurred at | 1 Oct 2026, 14:30 | The original is never overwritten. Attendance feeds pay, and a record that can be quietly rewritten is not evidence. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Record attendance (primary button) | `recordAttendance` POST `/attendance/clock` | inline | AttendanceRecord | 409 Out of sequence — a clock-out with no clock-in, or a second clock-in. Reported rather than silently corrected. | works offline; opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Break due**: From the shift's break policy: "30 min unpaid break due after 4 h (from 11:00)". Paid or unpaid in words. Number of breaks left this shift. *(source: screens/P08-venue-back-office.yaml#BO-880 / contracts/satellite/workforce.yaml#/components/schemas/ShiftTemplate)*
- **Break timer**: Large count-up "On break 12:40 of 30:00"; amber in the last 5 minutes, then "Over by 3 min" in words and colour. *(source: designer default)*
- **Today's breaks**: Each break with start, end and length; a break not taken by the latest break time shows "Break missed". *(source: contracts/satellite/workforce.yaml#/components/schemas/AttendanceRecord / contracts/satellite/workforce.yaml#/components/schemas/WorkforceComplianceFinding)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Start break**: Records breakStart; timer starts; offline it is saved with device time. *(source: contracts/satellite/workforce.yaml#recordAttendance)*
- **End break**: Records breakEnd and returns to EMP-024 or home with "Back on shift 11:31". *(source: contracts/satellite/workforce.yaml#recordAttendance)*
- **Ask for cover**: Sends a message to the supervisor ("Rahul needs break cover at Main Plaza Gate 2 from 11:00"). *(source: contracts/satellite/workforce.yaml#sendStaffMessage / DI-237)*

**Data it reads**: `listAttendance` (onLoad, Who was here)

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The break list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the break untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No break yet. Offers Record attendance (`recordAttendance`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on date, principalId, exceptionsOnly and the break are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `WORKFORCE_VIEW`, which `listAttendance` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ATTENDANCE_RECORD` for `recordAttendance`. |
| Offline (`?state=offline`) | Queues locally |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Out of sequence — a clock-out with no clock-in, or a second clock-in. Reported rather than silently corrected. |

#### Edge cases to draw

- **Starting a break with no cover at a post that must be staffed**: Warn "Main Plaza Gate 2 will be unstaffed" with Start anyway / Wait; the choice is recorded. *(source: DI-237 / contracts/satellite/workforce.yaml#/components/schemas/StaffingRules)*
- **Break end without a start (or the reverse)**: 409 message "No break started"; not silently fixed. *(source: contracts/satellite/workforce.yaml#recordAttendance)*
- **Offline**: Both buttons work and show "Saved on this phone"; Ask for cover queues. *(source: contracts/satellite/workforce.yaml#recordAttendance / contracts/satellite/workforce.yaml#sendStaffMessage)*

#### Consistency with other screens

- Match `EMP-024`: Breaks appear in the same today's record; same "Sent / Waiting to send" marks.
- Match `BO-880`: Break policy wording (duration, paid or unpaid, earliest and latest) comes from there.
- Match `BO-890`: A missed break here is the "Missed break" finding there.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
policy: 30 min unpaid break due after 4 h (from 11:00, latest 13:00)
cover: Covered by Omar Haddad
timer: On break 12:40 of 30:00
breaks:
- 11:02-11:31 (29 min)
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

- Staff can request a swap (e.g. break coverage) from another resource; attendance exceptions are marked manually (active, not active, absent, other). *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering; 4.9 AI Optimization, Mobile App & Analytics · DI-491)*
- Break management: staff log break windows so a replacement can be scheduled (e.g. so a ticket counter is not left unstaffed). *(client request · MoM 10 Aug 2026, 5.6 Roster, Leave & Break Management, Resources · DI-237)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-025` · status **notStarted** · provenance generated
- Flow F68 *A rota is published, worked and swapped*, step 5: They take a break and come back. → **Breaks are attendance events.** `amendAttendance` is a supervisor act and was on this screen — removed.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (9 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-025?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Record attendance.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`.
- [ ] Every gated control is gated: `ATTENDANCE_RECORD`, `WORKFORCE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-026` Incident report

**Record what happened while it is fresh.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `maintenance` module |
| Block | Block A · task APP-STAFF-EMP-026 |
| Who uses it | venue staff holding `GUEST_VIEW`, `INCIDENT_REPORT`, `INCIDENT_VIEW` (2 read, 1 operate); in the flows as supervisor, technician |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listIncidents` reads the population and `getIncident` reads one of them — list, select, act |
| Offline | Queues locally with the highest sync priority |
| Opens with | `incidentId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/operations/incident-report` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

**Known gaps.** Removed 2 October 2026 (CHG-SPO-018): a supervisor act (INCIDENT_MANAGE) on EMP-027 and BO-072; the reporter needs reportIncident only (F69 step 2; design-notes correction venue-operations EMP-026). Removed 2 October 2026 (CHG-SPO-018): a supervisor act (INCIDENT_MANAGE) on EMP-027 and BO-072; the reporter needs reportIncident only (F69 step 2; design-notes correction venue-operations EMP-026).

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Any member of staff records something that happened to a person or a place - an injury, a near miss, damage, a fire alarm, a security event - from where it happened, in under a minute, offline if need be. It reaches a supervisor immediately rather than sitting in a list. An incident is not a work order; it may lead to one. The one thing to get right: the minimum (kind, severity, where, when, one line, photo) is enough to send, and anything with a person hurt or at risk goes to the top of the sync queue and to a supervisor's phone.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Near miss is both a kind and a severity (CHG-SPO-019)
- No way to report a hazard (an unsafe condition before anything happened) (CHG-SPO-019)
- Nothing sets isReportable or notificationDueAt (CHG-SPO-019)

**Fixed on main** (the package already carries these; draw what it says): Record authority notification, Save incident and a table of every incident (with text filters) on the reporting screen (CHG-SPO-018).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should the incident kinds follow the pack's categories (Guest, Employee, Contractor, Ride/attraction, Electrical, Slip/trip/fall, Mechanical...) rather than the contract's ten?** → Drawn default accepted: Draw the contract's ten kinds. *(decided by Chinmay, 2026-10-02; DEC-134 / CHG-NOTE-008)*
- **How does a steward record a guest with nothing to scan (a companion with no ticket) while offline, if personal details live only in the protected store?** → Drawn default accepted: Draw "Name and phone" fields marked "Stored separately and protected"; offline they queue with the report. *(decided by Chinmay, 2026-10-02; DEC-135 / CHG-NOTE-008)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Severity | radio group | optional | — | Near miss · Minor · Moderate · Major · Critical | — | Sends `?severity=` to `listIncidents`. | `listIncidents` ?severity |
| Status | radio group | optional | — | Reported · Under investigation · Action required · Closed | — | Sends `?status=` to `listIncidents`. | `listIncidents` ?status |
| Is reportable | toggle | optional | — | — | — | Sends `?isReportable=` to `listIncidents`. | `listIncidents` ?isReportable |
| Photos | text area | optional | — | max length 256 | — | From the camera or the gallery, several at once; each uploads as it is added and can be removed before the report is sent. | `UploadIncidentMediaRequest.filename` |
| Find the guest involved | text field | optional | — | Requires `GUEST_VIEW_PII`: matching on personal data discloses it, so a caller without that permission who passes `search` is refused with 403 rather than having the parameter ignored. | — | Sends `?search=` to `searchGuests`. Optional, inside Add a person involved: a guest found here fills name and contact from the guest's record, so the person is linked rather than typed again. | `searchGuests` ?search |

**Form: Report incident** (modal, opened by *Report incident*; *Report incident* calls `reportIncident`, *Cancel* sends nothing)

**Collects what `reportIncident` sends before it is called.** Required: `id`, `kind`, `severity`, `venueId`, `description`, `occurredAt`, `recordedAt`. Optional: `assetId`, `locationDescription`, `involvedSubjectIds`, `involvedStaffPrincipalIds`, `witnessCount`, `firstAidGiven`, `emergencyServicesCalled`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `reportIncident` body |
| Kind `kind` | select | required | — | Guest injury · Staff injury · Near miss · Property damage · Equipment failure · Security incident · Fire or evacuation · Food safety · Environmental · Other | — | — | `reportIncident` body |
| Severity `severity` | radio group | required | — | Near miss · Minor · Moderate · Major · Critical | — | — | `reportIncident` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `reportIncident` body |
| Asset `assetId` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `reportIncident` body |
| Location description `locationDescription` | text area | optional | — | max length 500 | — | — | `reportIncident` body |
| Description `description` | text area | required | — | min length 3; max length 10000 | — | — | `reportIncident` body |
| Involved subjects `involvedSubjectIds` | multi-picker: choose involved subjects | optional | — | — | — | Opaque references. Personal details live in the erasable store, so the incident record survives an erasure request intact. | `reportIncident` body |
| Involved staff principals `involvedStaffPrincipalIds` | multi-picker: choose involved staff principals | optional | — | — | — | — | `reportIncident` body |
| Witness count `witnessCount` | number field | optional | — | — | — | — | `reportIncident` body |
| First aid given `firstAidGiven` | toggle | optional | off | — | — | — | `reportIncident` body |
| Emergency services called `emergencyServicesCalled` | toggle | optional | off | — | — | — | `reportIncident` body |
| Attachment refs `attachmentRefs` | list of values (chips) | optional | — | — | — | — | `reportIncident` body |
| Occurred at `occurredAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `reportIncident` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `reportIncident` body |

Errors to draw in the form: 400 Validation failed

**Form: Add a person involved** (modal, opened by *Add a person involved*; *Add person* calls `addIncidentPerson`, *Cancel* sends nothing)

**A person involved in the incident** (decided by Chinmay, 3 October 2026 (CHG-SPF-013)): name, role (guest, staff, contractor, other) and contact, with an optional guest lookup (`searchGuests`) that fills them from the guest's record. Stored as a PII subject; the consent rules apply, so contact details are asked only with the purpose shown. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Role `role` | radio group | required | — | Injured · Involved · Witness · Reporter | — | The person's part in the incident. | `addIncidentPerson` body |
| Party type `partyType` | radio group | optional | Guest | Guest · Public member · Staff · Contractor | — | — | `addIncidentPerson` body |
| Name `name` | text field | optional | — | max length 200 | — | Written to the erasable store (`pii.subject`), never to the incident (ADR-0023). | `addIncidentPerson` body |
| Phone `phone` | phone field | optional | — | max length 32 | +971 5X XXX XXXX (E.164) | Stored only with `contactConsent` true. | `addIncidentPerson` body |
| Email `email` | email field | optional | — | max length 254 | name@example.ae | Stored only with `contactConsent` true. | `addIncidentPerson` body |
| Contact consent `contactConsent` | toggle | optional | off | — | — | The person agreed to be contacted about this incident (consent rules apply; CHG-RUL-013). | `addIncidentPerson` body |
| Guest subject `guestSubjectId` | picker: choose a guest subject | optional | — | — | shows names, sends the id | A known guest, from the optional guest lookup; links their existing subject. | `addIncidentPerson` body |
| Principal `principalId` | picker: choose a principal | optional | — | — | shows names, sends the id | A member of staff; a principal, not a PII subject. | `addIncidentPerson` body |
| Note `note` | text area | optional | — | max length 2000 | — | — | `addIncidentPerson` body |

Errors to draw in the form: 400 Neither a name, a guest nor a member of staff given, or more than one of `guestSubjectId` and `principalId`.; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The incident is closed (`incident-closed`); reopen it first (CHG-RUL-011).

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Kind**: Large tiles with icons, in this order - Guest injured, Staff injured, Near miss, Property damage, Equipment failure, Security, Fire or evacuation, Food safety, Environmental, Other. Equipment failure offers "Also raise a fault for repair" after sending. *(source: contracts/satellite/maintenance.yaml#/components/schemas/IncidentKind / F69 step 1)*
- **Severity**: Four chips Minor, Moderate, Major, Critical with one-line meanings under each; when the kind is Near miss the severity is set to Near miss and hidden. Critical turns the Send button red and adds "Your supervisor will be called". *(source: contracts/satellite/maintenance.yaml#/components/schemas/IncidentSeverity / F08 step 6)*
- **When**: Defaults to now in venue time; "Earlier" opens a time picker limited to today and yesterday (occurredAt cannot be in the future). *(source: contracts/satellite/maintenance.yaml#reportIncident)*
- **Where**: Scan an asset tag, or pick the zone on a short list, or type a location (max 500). Never an id. *(source: screens/P06-staff-app.yaml#EMP-026 / contracts/satellite/maintenance.yaml#reportIncident)*
- **What happened**: Required, at least 3 characters, max 10,000; voice-to-text offered. This text is the original report and is never edited afterwards - say so under the field. *(source: contracts/satellite/maintenance.yaml#updateIncident / F69 step 2)*
- **People involved**: "Add a guest" (scan their ticket or wristband, or name and phone held in the protected store) and "Add a colleague" (staff picker); the incident keeps references only. Witness count as a stepper. First aid given and Emergency services called as two yes/no switches, off by default. *(source: contracts/satellite/maintenance.yaml#/components/schemas/IncidentInvolvedParty / contracts/satellite/maintenance.yaml#reportIncident)*
- **Photos**: At the top, camera first, as on Raise a task; optional but prompted. *(source: DI-232 / contracts/satellite/maintenance.yaml#reportIncident)*

#### Outputs: what the screen shows and produces

**Shown**

**Every incident** (data table, from `listIncidents`)

| Shows | Format | Notes |
|---|---|---|
| Incident number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Severity | chip: Near miss, Minor, Moderate, Major, Critical | — |
| Status | chip: Reported, Under investigation, Action required, Closed | — |
| Location description | text | — |

**The selected incident** (detail panel, from `listIncidents`)

| Shows | Format | Notes |
|---|---|---|
| Incident number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Kind | chip: Guest injury, Staff injury, Near miss, Property damage, Equipment failure, Security … | — |
| Severity | chip: Near miss, Minor, Moderate, Major, Critical | — |
| Status | chip: Reported, Under investigation, Action required, Closed | — |
| Location description | text | — |

**The incident** (detail panel, from `getIncident`)

| Shows | Format | Notes |
|---|---|---|
| Incident number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Kind | chip: Guest injury, Staff injury, Near miss, Property damage, Equipment failure, Security … | — |
| Severity | chip: Near miss, Minor, Moderate, Major, Critical | — |
| Status | chip: Reported, Under investigation, Action required, Closed | — |
| Location description | text | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Report incident (primary button) | `reportIncident` POST `/incidents` | ReportIncidentRequest | Incident | 400 Validation failed | works offline; opens modal first |
| Add a person involved (secondary button) | `addIncidentPerson` POST `/incidents/{incidentId}/people` | AddIncidentPersonRequest | IncidentInvolvedParty | 400 Neither a name, a guest nor a member of staff given, or more than one of `guestSubjectId` and `principalId`.; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. … | works offline; opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Sent**: "Reported - INC-2026-0213. Fatima Al Hashimi (duty supervisor) has been told." Offline "Saved - this will be sent first when you are back online" with a red count on the home screen. *(source: screens/P06-staff-app.yaml#EMP-026 / F08 step 6)*
- **Immediate actions prompt**: After sending, a short checklist the reporter can tick - Area blocked off, Supervisor called, First aider called - recorded by the supervisor later as an investigation note, not as fields here. *(source: screens/P06-staff-app.yaml#EMP-026 / contracts/satellite/maintenance.yaml#updateIncident)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Send report**: Records the incident (offline-capable, highest sync priority) and returns home; a Critical or injury report also alerts the duty supervisor, whose EMP-027 opens from the alert. *(source: contracts/satellite/maintenance.yaml#reportIncident / F69 step 2)*
- **Raise a fault for repair**: Offered after an Equipment failure or Property damage report; opens EMP-006 pre-filled with the asset, location and photos. *(source: contracts/satellite/maintenance.yaml#reportIncident / F12 step 1)*

**Data it reads**: `listIncidents` (onLoad, List incidents)

**Where the user goes next**

- → `EMP-004` Task list: *Technician picks up the work order*; calls `reportIncident`
- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*; carries `incidentId`
- → `EMP-027` Incident detail: *A supervisor reads it and adds detail*; carries `incidentId`; calls `reportIncident`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The incident report list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the incident report untouched. |
| Empty, first run (`?state=emptyFirstRun`) | Nothing reported yet by you today. Offers Report incident. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on severity, status, isReportable and the incident report are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `INCIDENT_VIEW`, which `listIncidents` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `INCIDENT_REPORT` for `reportIncident`. |
| Offline (`?state=offline`) | Queues locally with the highest sync priority |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Content type not permitted, or size beyond the media store's limit for that kind.; 400 Neither a name, a guest nor a member of staff given, or more than one of `guestSubjectId` and `principalId`.; 400 Validation failed; 409 The incident is closed (`incident-closed`); reopen it first (CHG-RUL-011). |

#### Edge cases to draw

- **Offline**: The report queues ahead of every other pending item; photos upload after the record so the incident exists even if a photo fails. *(source: screens/P06-staff-app.yaml#EMP-026 / contracts/satellite/maintenance.yaml#reportIncident)*
- **Reporter is not a supervisor**: The reporter sees only their own report afterwards; investigation and authority notification are not offered (INCIDENT_MANAGE). *(source: contracts/satellite/maintenance.yaml#updateIncident)*
- **Two stewards report the same event**: Both are kept; the supervisor links them on EMP-027. The second reporter is not blocked. *(source: designer default)*

#### Consistency with other screens

- Match `BO-072`: Same kinds, severities, colours and incident numbers as the back-office incident log.
- Match `EMP-006`: Shared photo-first layout and scan control; each screen offers a switch to the other.
- Match `EMP-029`: Guest assistance reports incidents with the same operation; draw one shared form component.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
report:
  number: INC-2026-0213
  kind: Guest injured
  severity: Moderate
  when: 1 Oct 2026 11:05
  where: Aqua Park, Wave Rider exit stairs
  what: Guest slipped on wet step, grazed knee, walked to first aid.
  people: Guest Sara Al Nuaimi (ticket VT0010); staff Maria Santos
  witnesses: 2
  firstAid: 'Yes'
  emergencyServices: 'No'
  reportedBy: Maria Santos
```

#### Permissions

- `reportIncident` → `INCIDENT_REPORT` (operate) · staff
- `getIncident` → `INCIDENT_VIEW` (read) · staff
- `listIncidents` → `INCIDENT_VIEW` (read) · staff
- `uploadIncidentMedia` → `INCIDENT_REPORT` (operate) · staff
- `addIncidentPerson` → `INCIDENT_REPORT` (operate) · staff
- `searchGuests` → `GUEST_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `INCIDENT_VIEW`, which `listIncidents` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `INCIDENT_REPORT` for `reportIncident`.

#### Requirements it meets

10 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 17.5.3 | Hazard Reporting - System shall support hazard reporting. | Maintenance & Safety Management | CONTRACTED | `reportIncident` |
| 17.5.4 | Incident Reporting - System shall support incident reporting. | Maintenance & Safety Management | CONTRACTED | `reportIncident` |
| 17.5.5 | Near-Miss Reporting - System shall support near-miss reporting. | Maintenance & Safety Management | CONTRACTED | `reportIncident` |
| 18.4.1 | Hazard Reporting - Users shall submit hazard reports. | Employee Mobile App & AI Assistant | CONTRACTED | `reportIncident` |
| 18.4.2 | Incident Reporting - Users shall submit incident reports. | Employee Mobile App & AI Assistant | CONTRACTED | `reportIncident` |
| 18.4.3 | Near-Miss Reporting - Users shall submit near-miss reports. | Employee Mobile App & AI Assistant | CONTRACTED | `reportIncident` |
| 18.4.4 | Safety Inspections - Users shall perform inspections. | Employee Mobile App & AI Assistant | CONTRACTED | `reportIncident` |
| 18.4.5 | Safety Checklists - Users shall complete safety checklists. | Employee Mobile App & AI Assistant | CONTRACTED | `reportIncident` |
| 18.4.6 | Corrective Actions - Users shall submit corrective actions. | Employee Mobile App & AI Assistant | CONTRACTED | `reportIncident` |
| 8.9.5 | System shall provide real-time visibility of incidents, hazards, complaints, emergencies, and operational disruptions. | Unified Operations Dashboard | CONTRACTED | `listIncidents` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Photo capture is the primary way to log faulty assets without barcodes (pipes, valves, lighting); barcode scan is secondary. *(agreed · MoM 10 Aug 2026, 5.3 Task, Work Order & Asset Management · DI-232)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-026` · status **notStarted** · provenance generated
- Flow F12 *Asset fails and closes a queue*, step 1: Reports the fault → The asset goes out of service. **The queue closes with it** — nobody has to remember
- Flow F69 *An incident is reported, escalated and closed*, step 1: A steward reports it from where it happened. → **Kind, location, people involved, time.** Typed in under a minute or it is typed later and wrongly.
- Flow F12 branch at step 1 (recoverable): when Asset is not safety-critical, Verification is still required but does not block return. The distinction is on the asset, not the judgement of whoever is on shift.
- Flow F12 branch at step 1 (requiresStaff): when Fault is reported during trading with a full queue, Waiting parties are released rather than silently dropped, and told. A guest holding a virtual queue place for a closed ride will come back to ask.
- ADR-0023 *— Personal data lives apart from the append-only ledger* (`docs/adr/0023-pii-separation.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (29), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-026?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Report incident, Add a person involved.
- [ ] Every transition is wired: `EMP-004`, `EMP-001`, `EMP-002`, `EMP-003`, `EMP-027`.
- [ ] Every gated control is gated: `GUEST_VIEW`, `INCIDENT_REPORT`, `INCIDENT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-027` Incident detail

**Follow up on something already reported.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 2 · needs the `maintenance` module |
| Block | Block D · task APP-STAFF-EMP-027 |
| Who uses it | venue staff holding `INCIDENT_MANAGE`, `INCIDENT_VIEW` (1 configure, 1 read); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listIncidents` reads the population and `getIncident` reads one of them — list, select, act |
| Offline | Cached; updates queue |
| Opens with | `incidentId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/operations/incident-detail` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Removed 24 August**: reportIncident. **Bulk-attach residue, found by walking a journey.** A device-settings screen does not read guest loyalty, a venue map does not set a refund policy, a shift summary does not close the shift, and **a rota a steward can rewrite is not a rota.** **Removed 24 August**: recordAuthorityNotification. **Bulk-attach residue.** A device-settings screen does not merge guest profiles, a rota view does not author the rota, a shift summary does not open a shift, and **authority notification belongs where the incident is raised, not where it is read.**

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The duty supervisor's follow-up of an incident on the Staff App: read the original report (never edited), add what was found as dated notes, adjust severity, assign an investigator, link a repair, and notify the authority where the incident is reportable. The one thing to get right: the record grows by appending - the original report stays at the top unchanged and every note is a new, signed entry - and a reportable incident shows its notification deadline as a countdown.

**Known correction pending (do not draw the wrong version)**

- **Offline state "Cached; updates queue"** Why: getIncident and updateIncident are not offline-capable, so updates cannot queue; make them offline-capable (append-only notes suit it) or change the state. *(source: screens/P06-staff-app.yaml#EMP-027 / contracts/satellite/maintenance.yaml#updateIncident; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Incident status has four values; the pack's lifecycle has seven** Why: Pack Reported > Assessed > Controlled > Investigated > Actions assigned > Verified > Closed; "Controlled" and "Verified" (closure checked by someone other than the actor) are lost. *(source: screens/P06-staff-app.yaml#EMP-027; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Authority notification is placed on EMP-050 (F69 step 3) instead of here (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Severity can be changed but only the current value is stored. Should a severity change be kept as history?** → Drawn default accepted: Draw the change with a required reason saved as an investigation note. *(decided by Chinmay, 2026-10-02; DEC-529 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.
- **For critical incidents, may the person who completed the corrective action also close the incident (the pack's segregation of duties)?** → Another supervisor must close a critical incident (the person who completed the corrective action cannot close it). *(decided by Chinmay, 2026-10-02; DEC-530 / CHG-NOTE-008)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Severity | radio group | optional | — | Near miss · Minor · Moderate · Major · Critical | — | Sends `?severity=` to `listIncidents`. | `listIncidents` ?severity |
| Status | radio group | optional | — | Reported · Under investigation · Action required · Closed | — | Sends `?status=` to `listIncidents`. | `listIncidents` ?status |
| Is reportable | toggle | optional | — | — | — | Sends `?isReportable=` to `listIncidents`. | `listIncidents` ?isReportable |

**Form: Save incident** (modal, opened by *Save incident*; *Save incident* calls `updateIncident`, *Cancel* sends nothing)

**Collects what `updateIncident` sends before it is called.** Nothing in the body is required. Optional: `status`, `severity`, `assignedToPrincipalId`, `investigationNote`, `rootCause`, `correctiveActions`, `correctiveWorkOrderId`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | radio group | optional | — | Reported · Under investigation · Action required · Closed | — | — | `updateIncident` body |
| Severity `severity` | radio group | optional | — | Near miss · Minor · Moderate · Major · Critical | — | — | `updateIncident` body |
| Assigned to principal `assignedToPrincipalId` | picker: choose an assigned to principal | optional | — | — | shows names, sends the id | — | `updateIncident` body |
| Investigation note `investigationNote` | text area | optional | — | max length 10000 | — | Appended as a new entry of `IncidentDetail.investigationNotes`, never overwriting the last (audit R106 (5)). | `updateIncident` body |
| Root cause `rootCause` | text area | optional | — | max length 2000 | — | — | `updateIncident` body |
| Corrective actions `correctiveActions` | text area | optional | — | max length 5000 | — | — | `updateIncident` body |
| Corrective work order `correctiveWorkOrderId` | picker: choose a corrective work order | optional | — | — | shows names, sends the id | — | `updateIncident` body |
| Attachment refs `attachmentRefs` | list of values (chips) | optional | — | — | — | — | `updateIncident` body |
| Escalate `escalate` | group | optional | — | — | — | Escalate an incident under investigation (the optional Escalated step; CHG-RUL-011). | `updateIncident` body |
| To principal `escalate.toPrincipalId` | picker: choose a to principal | required | — | — | shows names, sends the id | — | `updateIncident` body |
| Reason `escalate.reason` | text area | required | — | min length 3; max length 1000 | — | — | `updateIncident` body |
| Reason `reason` | text area | optional | — | min length 3; max length 1000 | — | Why the status changes. Required to reopen a closed incident (back to `underInvestigation`) and to close a `reported` one straight away (CHG-RUL-011). | `updateIncident` body |

Errors to draw in the form: 400 Closure attempted without findings or a corrective action; 403 A critical incident closed by the person who completed its corrective action (`closer-completed-action`; workbook Q530; CHG-CSA-033).; 422 A move outside the incident flow (`incident-transition-not-allowed`; CHG-RUL-011): to `actionRequired`, from `closed` to anything but `underInvestigation`, a …

**Form: Record authority notification** (modal, opened by *Record authority notification*; *Record authority notification* calls `recordAuthorityNotification`, *Cancel* sends nothing)

**Collects what `recordAuthorityNotification` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Authority `authority` | text field | required | — | max length 200 | — | — | `recordAuthorityNotification` body |
| Reference `reference` | text field | optional | — | max length 128 | — | — | `recordAuthorityNotification` body |
| Notified at `notifiedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `recordAuthorityNotification` body |
| Notified by principal `notifiedByPrincipalId` | picker: choose a notified by principal | optional | — | — | shows names, sends the id | — | `recordAuthorityNotification` body |
| Attachment refs `attachmentRefs` | list of values (chips) | optional | — | — | — | — | `recordAuthorityNotification` body |

Errors to draw in the form: 409 The incident is not reportable (`isReportable` false, audit R106 (6)).

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Add a note**: A single text box "Add to the investigation" (max 10,000) with photo attach; Save appends one entry with my name and time. There is no edit or delete on earlier notes. *(source: contracts/satellite/maintenance.yaml#updateIncident / F69 step 2)*
- **Status**: Reported > Under investigation > Action required > Closed as a stepper, forward only from the phone. Closing requires a root cause and corrective actions (or "No action needed" stated), and a linked work order where an action needs repair work. *(source: contracts/satellite/maintenance.yaml#updateIncident)*
- **Severity**: Same chips as the report; a change asks for a reason, which is saved as an investigation note ("Raised to Major - guest taken to hospital"). *(source: contracts/satellite/maintenance.yaml#updateIncident / designer default)*
- **Assign to**: Staff picker of people with incident-management rights at this venue; never an id. *(source: contracts/satellite/maintenance.yaml#updateIncident)*
- **Authority notification**: Shown only when the incident is reportable - authority (picker of the venue's usual authorities with free text fallback, max 200), reference (max 128), notified at (defaults now), attachments. Each notification is a new row; a second to the same authority is allowed. *(source: contracts/satellite/maintenance.yaml#recordAuthorityNotification / F69 step 3)*

#### Outputs: what the screen shows and produces

**Shown**

**Every incident** (data table, from `listIncidents`)

| Shows | Format | Notes |
|---|---|---|
| Incident number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Severity | chip: Near miss, Minor, Moderate, Major, Critical | — |
| Status | chip: Reported, Under investigation, Action required, Closed | — |
| Location description | text | — |

**The selected incident** (detail panel, from `listIncidents`)

| Shows | Format | Notes |
|---|---|---|
| Incident number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Kind | chip: Guest injury, Staff injury, Near miss, Property damage, Equipment failure, Security … | — |
| Severity | chip: Near miss, Minor, Moderate, Major, Critical | — |
| Status | chip: Reported, Under investigation, Action required, Closed | — |
| Location description | text | — |

**The incident** (detail panel, from `getIncident`)

| Shows | Format | Notes |
|---|---|---|
| Incident number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Kind | chip: Guest injury, Staff injury, Near miss, Property damage, Equipment failure, Security … | — |
| Severity | chip: Near miss, Minor, Moderate, Major, Critical | — |
| Status | chip: Reported, Under investigation, Action required, Closed | — |
| Location description | text | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save incident (primary button) | `updateIncident` PATCH `/incidents/{incidentId}` | inline | Incident | 400 Closure attempted without findings or a corrective action; 403 A critical incident closed by the person who completed its corrective action (`closer-completed-action`; workbook Q530; CHG-CSA-033).; 422 A move … | opens modal first |
| Record authority notification (secondary button) | `recordAuthorityNotification` POST `/incidents/{incidentId}/notify-authority` | inline | Incident | 409 The incident is not reportable (`isReportable` false, audit R106 (6)). | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Header**: Incident number, kind, severity badge, status, where, occurred at; for reportable incidents a red "Notify the authority by 14:05 (2 h 05 min left)" until a notification is recorded, then green "Notified 12:20 by Fatima Al Hashimi, ref AD-P-55812". *(source: contracts/satellite/maintenance.yaml#/components/schemas/Incident / screens/P08-venue-back-office.yaml#BO-072)*
- **Original report**: Read-only card with reporter, time, people involved (names only to those allowed), first aid, emergency services, witnesses, photos. *(source: contracts/satellite/maintenance.yaml#/components/schemas/IncidentDetail)*
- **Investigation timeline**: Every note oldest first, each with author and time; status and severity changes interleaved; notifications as their own entries. *(source: contracts/satellite/maintenance.yaml#/components/schemas/IncidentInvestigationNote / contracts/satellite/maintenance.yaml#/components/schemas/IncidentAuthorityNotification)*
- **Linked records**: The corrective work order with its live status, and any guest case. *(source: contracts/satellite/maintenance.yaml#/components/schemas/Incident / F69 step 2)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save**: Sends only what changed (PATCH); the new note appears at the bottom of the timeline. A closure without findings is refused 400 and the missing field is highlighted. *(source: contracts/satellite/maintenance.yaml#updateIncident)*
- **Record notification**: Appends a notification row; the button is not shown for a non-reportable incident (the server refuses 409). *(source: contracts/satellite/maintenance.yaml#recordAuthorityNotification)*
- **Raise a repair**: Opens EMP-006 with asset, location and photos; on return the new work order is linked as the corrective work order. *(source: contracts/satellite/maintenance.yaml#updateIncident / screens/P08-venue-back-office.yaml#BO-072)*
- **Open a guest case**: Where a guest is involved, creates a case linked to the incident; the conversation with the guest continues there. *(source: F69 step 2)*
- **Restore the area**: Opens EMP-050 for this incident once the cause is controlled. *(source: screens/P06-staff-app.yaml#EMP-027)*

**Data it reads**: `listIncidents` (onLoad, List incidents)

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*; carries `incidentId`
- → `EMP-050` Post-incident restore: *Where required, the authorities are notified*; carries `incidentId`
- → `EMP-038` Broadcast to team: *If it is a venue-wide event, an announcement goes out*; calls `recordAuthorityNotification`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The incident list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the incident untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No incident yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on severity, status, isReportable and the incident are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `INCIDENT_VIEW`, which `listIncidents` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `INCIDENT_MANAGE` for `updateIncident`, `recordAuthorityNotification`. |
| Offline (`?state=offline`) | Cached; updates queue |
| Denied (`?state=denied`) | Closing was refused: you completed the corrective action on this critical incident, so another supervisor closes it (403 closer-completed-action; DEC-530). |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Closure attempted without findings or a corrective action; 409 The incident is not reportable (`isReportable` false, audit R106 (6)).; 422 A move outside the incident flow (`incident-transition-not-allowed`; CHG-RUL-011): to `actionRequired`, from `closed` to anything but `underInvestigation`, a … |

#### Edge cases to draw

- **Offline**: The incident cannot be loaded or saved offline today (getIncident and updateIncident are online only); show the last opened copy read-only with "Offline - notes need the network". *(source: contracts/satellite/maintenance.yaml#getIncident / contracts/satellite/maintenance.yaml#updateIncident)*
- **Deadline passes without notification**: The countdown turns to "Overdue by 12 min" and stays red; recording a late notification is still allowed. *(source: contracts/satellite/maintenance.yaml#recordAuthorityNotification)*
- **Viewer without INCIDENT_MANAGE**: Read-only, with "Needs incident management rights" under the disabled Save (per VO-R08). *(source: contracts/satellite/maintenance.yaml#updateIncident)*

#### Consistency with other screens

- Match `BO-072`: The same incident record and timeline as the back-office incident log; notes added on either show on both.
- Match `EMP-050`: Restore is the step after control; it carries the incident id.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
incident:
  number: INC-2026-0213
  kind: Guest injured
  severity: Moderate
  status: Under investigation
  reportable: true
  notifyBy: 1 Oct 2026 14:05
  notes:
  - 11:22 Fatima Al Hashimi - Step 3 wet from slide splash-back; anti-slip mat missing since 09:00.
  - 11:40 Fatima Al Hashimi - Area coned off; WO-2026-01495 raised for the mat.
  correctiveWorkOrder: WO-2026-01495 (In progress)
```

#### Permissions

- `getIncident` → `INCIDENT_VIEW` (read) · staff
- `updateIncident` → `INCIDENT_MANAGE` (configure) · staff
- `listIncidents` → `INCIDENT_VIEW` (read) · staff
- `recordAuthorityNotification` → `INCIDENT_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `INCIDENT_VIEW`, which `listIncidents` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `INCIDENT_MANAGE` for `updateIncident`, `recordAuthorityNotification`.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.9.5 | System shall provide real-time visibility of incidents, hazards, complaints, emergencies, and operational disruptions. | Unified Operations Dashboard | CONTRACTED | `listIncidents` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-027` · status **notStarted** · provenance generated
- Flow F69 *An incident is reported, escalated and closed*, step 2: A supervisor reads it and adds detail. → **Appended, never overwritten.** An incident record edited after the fact is a record that cannot be relied on.
- Flow F69 *An incident is reported, escalated and closed*, step 3: Where required, the authorities are notified. → **The notification is itself a record.** *We told the police* with no time and no name is not evidence.
- Flow F69 branch at step 2 (high): when It involves a guest and becomes a case., `createCase` links the incident to the guest record. **An incident is what happened; a case is the conversation afterwards**, and conflating them puts operational detail in a guest-facing thread.

#### Acceptance for the design

- [ ] Every input above is drawn (20), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-027?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline, denied.
- [ ] Every action is wired with its success and its failure: Save incident, Record authority notification.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`, `EMP-050`, `EMP-038`.
- [ ] Every gated control is gated: `INCIDENT_MANAGE`, `INCIDENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-028` Lost & found

**Log something handed in.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 2 · needs the `marketing` module |
| Block | Block D · task APP-STAFF-EMP-028 |
| Who uses it | venue staff holding `CASE_MANAGE`, `CASE_VIEW` (1 configure, 1 read); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listCases` reads the population and `getCase` reads one of them — list, select, act |
| Offline | Queues locally and syncs on reconnect. The pending count is always current because it is local |
| Opens with | `caseId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/operations/lost-found` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** A steward logs something handed in, on the floor, so it can be matched to a guest's report and returned. The guest who lost it and the steward who found it end up in one conversation, and the case is closed with the guest told, not silently.

**Known correction pending (do not draw the wrong version)**

- **EMP-028 is wired to the case operations (createCase, listCases with staff filters), while LostItem and recordLostItem exist for exactly this.** Why: F70 step 3 says "lost and found is a case, not a separate register", contradicting LostItem ("one entity, two directions") and BO-073. Decide which model holds; the matching only works with LostItem. *(source: F70 step 3; contracts/satellite/marketing-crm.yaml#recordLostItem; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Status | select | optional | — | Open · In progress · Awaiting guest · Escalated · Resolved · Closed | — | Sends `?status=` to `listCases`. | `listCases` ?status |
| Assigned to principal id | picker: choose an assigned to principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?assignedToPrincipalId=` to `listCases`. | `listCases` ?assignedToPrincipalId |
| Breached sla | toggle | optional | — | — | — | Sends `?breachedSla=` to `listCases`. | `listCases` ?breachedSla |
| Priority | radio group | optional | — | Low · Normal · High · Urgent | — | Sends `?priority=` to `listCases`. | `listCases` ?priority |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Membership | picker: choose a membership | — | — | `listCases` ?membershipId |

**Form: Create case** (modal, opened by *Create case*; *Create case* calls `createCase`, *Cancel* sends nothing)

**Collects what `createCase` sends before it is called.** Required: `id`, `subject`, `description`, `channel`, `recordedAt`. Optional: `subjectId`, `categoryId`, `priority`, `kind`, `venueId`, `relatedOrderId`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createCase` body |
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | — | `createCase` body |
| Subject `subject` | text field | required | — | max length 200 | — | — | `createCase` body |
| Description `description` | text area | required | — | max length 10000 | — | — | `createCase` body |
| Category `categoryId` | picker: choose a category | optional | — | — | shows names, sends the id | — | `createCase` body |
| Membership `membershipId` | picker: choose a membership | optional | — | — | shows names, sends the id | The identity membership this case concerns (`identity.customer_membership`); member case notes are cases with this set. | `createCase` body |
| Priority `priority` | radio group | optional | Normal | Low · Normal · High · Urgent | — | — | `createCase` body |
| Kind `kind` | select | optional | — | Lost property · Complaint · Question · Accessibility · Refund request · Other; Stored on the case, because a lost-property report that forgets it was one cannot be routed to the lost and found desk.; A case raised as `other` must carry a non-empty `detail` … | — | What the guest says the case is about, in their words rather than the venue's taxonomy — `raiseMyCase` asks for it and `categoryId` is what staff file it under. | `createCase` body |
| Channel `channel` | select | required | — | Email · SMS · Whatsapp · Push · In app · Post | — | — | `createCase` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `createCase` body |
| Related order `relatedOrderId` | text field | optional | — | — | — | — | `createCase` body |
| Attachment refs `attachmentRefs` | list of values (chips) | optional | — | — | — | Stored on the opening `CaseMessage`, not on the case. | `createCase` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time the case was raised. The server stamps `Case.syncedAt` on arrival. | `createCase` body |

**Form: Add case message** (modal, opened by *Add case message*; *Add case message* calls `addCaseMessage`, *Cancel* sends nothing)

**Collects what `addCaseMessage` sends before it is called.** Required: `id`, `body`, `isInternal`, `recordedAt`. Optional: `channel`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `addCaseMessage` body |
| Body `body` | text area | required | — | min length 1; max length 10000 | — | — | `addCaseMessage` body |
| Is internal `isInternal` | toggle | required | — | — | — | — | `addCaseMessage` body |
| Channel `channel` | select | optional | — | Email · SMS · Whatsapp · Push · In app · Post | — | — | `addCaseMessage` body |
| Attachment refs `attachmentRefs` | list of values (chips) | optional | — | — | — | — | `addCaseMessage` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `addCaseMessage` body |

**Form: Escalate case** (modal, opened by *Escalate case*; *Escalate case* calls `escalateCase`, *Cancel* sends nothing)

**Collects what `escalateCase` sends before it is called.** Required: `reason`. Optional: `assignToPrincipalId`, `newPriority`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `escalateCase` body |
| Assign to principal `assignToPrincipalId` | picker: choose an assign to principal | optional | — | — | shows names, sends the id | — | `escalateCase` body |
| New priority `newPriority` | radio group | optional | — | Low · Normal · High · Urgent | — | — | `escalateCase` body |

**Form: Reopen case** (modal, opened by *Reopen case*; *Reopen case* calls `reopenCase`, *Cancel* sends nothing)

**Collects what `reopenCase` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | — | — | — | `reopenCase` body |

Errors to draw in the form: 409 The case is not `resolved` — a `closed` case is past its reopen window, and an open one has nothing to reopen. (StateTransitionProblem)

**Form: Save case** (modal, opened by *Save case*; *Save case* calls `updateCase`, *Cancel* sends nothing)

**Collects what `updateCase` sends before it is called.** Nothing in the body is required. Optional: `status`, `priority`, `assignedToPrincipalId`, `categoryId`, `resolutionNote`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | select | optional | — | Open · In progress · Awaiting guest · Escalated · Resolved · Closed | — | — | `updateCase` body |
| Priority `priority` | radio group | optional | — | Low · Normal · High · Urgent | — | — | `updateCase` body |
| Assigned to principal `assignedToPrincipalId` | picker: choose an assigned to principal | optional | — | — | shows names, sends the id | — | `updateCase` body |
| Category `categoryId` | picker: choose a category | optional | — | — | shows names, sends the id | — | `updateCase` body |
| Resolution note `resolutionNote` | text area | optional | — | max length 2000 | — | — | `updateCase` body |

Errors to draw in the form: 400 Resolving without a resolution note

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Found item**: Kind, colour, brand, where found, photo (camera), where it is stored. *(source: contracts/satellite/marketing-crm.yaml#recordLostItem)*

#### Outputs: what the screen shows and produces

**Shown**

**Every case** (data table, from `listCases`)

| Shows | Format | Notes |
|---|---|---|
| Case number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Guest name | text | Resolved from `pii.subject` when the case is read, never stored on the case. A name copied onto a case row is personal data outside the … |
| Subject | text | The case's one-line title, not a person. Stored as `title` so the table does not hold `subject` beside `subject_id`; the wire keeps … |
| Status | chip: Open, In progress, Awaiting guest, Escalated, Resolved, Closed | — |

**The selected case** (detail panel, from `listCases`)

| Shows | Format | Notes |
|---|---|---|
| Case number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Guest name | text | Resolved from `pii.subject` when the case is read, never stored on the case. A name copied onto a case row is personal data outside the … |
| Subject | text | The case's one-line title, not a person. Stored as `title` so the table does not hold `subject` beside `subject_id`; the wire keeps … |
| Status | chip: Open, In progress, Awaiting guest, Escalated, Resolved, Closed | — |
| Priority | chip: Low, Normal, High, Urgent | — |

**The case** (detail panel, from `getCase`)

| Shows | Format | Notes |
|---|---|---|
| Case number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Guest name | text | Resolved from `pii.subject` when the case is read, never stored on the case. A name copied onto a case row is personal data outside the … |
| Subject | text | The case's one-line title, not a person. Stored as `title` so the table does not hold `subject` beside `subject_id`; the wire keeps … |
| Status | chip: Open, In progress, Awaiting guest, Escalated, Resolved, Closed | — |
| Priority | chip: Low, Normal, High, Urgent | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create case (primary button) | `createCase` POST `/cases` | CreateCaseRequest | Case | — | works offline; opens modal first |
| Add case message (secondary button) | `addCaseMessage` POST `/cases/{caseId}/messages` | inline | CaseMessage | — | works offline; opens modal first |
| Escalate case (secondary button) | `escalateCase` POST `/cases/{caseId}/escalate` | inline | Case | — | opens modal first |
| Reopen case (secondary button) | `reopenCase` POST `/cases/{caseId}/reopen` | inline | Case | 409 The case is not `resolved` — a `closed` case is past its reopen window, and an open one has nothing to reopen. (StateTransitionProblem) | opens modal first |
| Save case (secondary button) | `updateCase` PATCH `/cases/{caseId}` | inline | Case | 400 Resolving without a resolution note | opens modal first |

**What each action does** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Hand in**: Works offline (the found record is offline-capable) and syncs; shows the reference to write on the tag. *(source: contracts/satellite/marketing-crm.yaml#recordLostItem)*

**Data it reads**: `listCases` (onLoad, List service cases)

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The lost found list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the lost found untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No lost found yet. Offers Create case (`createCase`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on status, assignedToPrincipalId, breachedSla, priority and the lost found are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `CASE_VIEW`, which `listCases` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `CASE_MANAGE` for `createCase`, `addCaseMessage`, `escalateCase`, `reopenCase` and 1 more. |
| Offline (`?state=offline`) | Queues locally and syncs on reconnect. The pending count is always current because it is local |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Resolving without a resolution note; 409 The case is not `resolved` — a `closed` case is past its reopen window, and an open one has nothing to reopen. (StateTransitionProblem) |

#### Consistency with other screens

- Match `BO-073`: Items logged here appear in the register as found.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
item:
  kind: Phone
  colour: Blue
  brand: Samsung
  where: Kids Club soft play
  stored: Guest Services drawer 2
  ref: F-2026-0612
```

#### Permissions

- `createCase` → `CASE_MANAGE` (configure) · staff, guest, partner
- `addCaseMessage` → `CASE_MANAGE` (configure) · staff, partner
- `escalateCase` → `CASE_MANAGE` (configure) · staff, partner
- `getCase` → `CASE_VIEW` (read) · staff, partner
- `listCases` → `CASE_VIEW` (read) · staff, guest, partner
- `reopenCase` → `CASE_MANAGE` (configure) · staff, partner
- `updateCase` → `CASE_MANAGE` (configure) · staff, partner

**A refused user sees:** Shown when the caller lacks `CASE_VIEW`, which `listCases` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `CASE_MANAGE` for `createCase`, `addCaseMessage`, `escalateCase`, `reopenCase` and 1 more.

#### Requirements it meets

13 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.66 | Guest Support - System shall provide guest support channels. | Guest Mobile App & Branding | CONTRACTED | `createCase` |
| 19.2.70 | Complaint Management - System shall support guest complaints. | Guest Mobile App & Branding | CONTRACTED | `createCase` |
| 2.8.12 | System shall allow agents to create, assign, escalate, track, and resolve guest cases including complaints, refund requests, service requests, incidents, and operational issues. Cases shall be linked … | Ticketing Sales | CONTRACTED | `createCase` |
| 5.3.34 | Link guest profiles with customer service cases, complaints, incidents, refunds, investigations, and follow-up activities. | F&B & Guest Management | CONTRACTED | `createCase` |
| 22.3.1 | Case Creation | Marketing & CRM | CONTRACTED | `createCase` |
| 22.3.2 | Case Classification | Marketing & CRM | CONTRACTED | `createCase` |
| 22.3.3 | Case Assignment | Marketing & CRM | CONTRACTED | `createCase` |
| 22.8.12 | Case Creation & Escalation | Marketing & CRM | CONTRACTED | `createCase` |
| 22.3.7 | Agent Notes & Attachments | Marketing & CRM | CONTRACTED | `addCaseMessage` |
| 22.3.6 | Case Escalation Management | Marketing & CRM | CONTRACTED | `escalateCase` |
| 22.3.10 | Case Audit Trail | Marketing & CRM | CONTRACTED | `getCase` |
| 22.2.17 | Case & Support History | Marketing & CRM | CONTRACTED | `listCases` |
| … 1 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Guest assistance: quick access to supervisors, announcements and venue information (e.g. opening hours), live ride/attraction status, and logging found items that surface for guest claim. *(client request · MoM 10 Aug 2026, 5.6 Roster, Leave & Break Management, Resources · DI-238)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-028` · status **notStarted** · provenance generated
- Flow F70 *A guest needs help and something is lost*, step 3: A lost item is logged. → **Lost and found is a case, not a separate register.** The guest who lost it and the guest who found it are both in a conversation.
- Flow F70 *A guest needs help and something is lost*, step 4: It is matched and returned. → **Closed with the guest told**, not closed silently. A case resolved without a message is a guest still waiting.
- Flow F70 branch at step 3 (high): when The item is high value or identity documents., Escalated immediately. **A passport in lost property is a different problem from an umbrella**, and the escalation path is the case one.
- Flow F70 branch at step 4 (medium): when The guest has left the venue., **The case stays open and reaches them by the channel they consented to.** A found item and no consent to contact is a real limit, and the case records that rather than hiding it.

#### Acceptance for the design

- [ ] Every input above is drawn (32), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-028?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create case, Add case message, Escalate case, Reopen case, Save case.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`.
- [ ] Every gated control is gated: `CASE_MANAGE`, `CASE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-029` Guest assistance

**Help a guest without leaving the floor.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 2 · needs the `marketing` module |
| Block | Block D · task APP-STAFF-EMP-029 |
| Who uses it | venue staff holding `CASE_MANAGE`, `CASE_VIEW`, `INCIDENT_MANAGE`, `INCIDENT_REPORT`, `INCIDENT_VIEW` (2 configure, 2 read, 1 operate); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listCases` reads the population and `getCase` reads one of them — list, select, act |
| Offline | Queues locally and syncs on reconnect. The pending count is always current because it is local |
| Opens with | `caseId` (deepLink), `incidentId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/operations/guest-assistance` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** A floor employee helps a guest without leaving the floor: checks for an existing case first, raises or updates one, or reports an incident when someone is hurt or something is unsafe. A guest asking twice about the same thing is not asked to explain it twice.

**Known correction pending (do not draw the wrong version)**

- **The case list exposes staff text filters (Assigned to principal id, Priority).** Why: On a phone the filters are Mine and Near me; ids are never typed. *(source: screens/P06-staff-app.yaml#EMP-029; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Status | select | optional | — | Open · In progress · Awaiting guest · Escalated · Resolved · Closed | — | Sends `?status=` to `listCases`. | `listCases` ?status |
| Assigned to principal id | picker: choose an assigned to principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?assignedToPrincipalId=` to `listCases`. | `listCases` ?assignedToPrincipalId |
| Breached sla | toggle | optional | — | — | — | Sends `?breachedSla=` to `listCases`. | `listCases` ?breachedSla |
| Priority | radio group | optional | — | Low · Normal · High · Urgent | — | Sends `?priority=` to `listCases`. | `listCases` ?priority |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Membership | picker: choose a membership | — | — | `listCases` ?membershipId |
| Severity | radio group | — | Near miss · Minor · Moderate · Major · Critical | `listIncidents` ?severity |
| Status | radio group | — | Reported · Under investigation · Action required · Closed | `listIncidents` ?status |
| Is reportable | toggle | — | — | `listIncidents` ?isReportable |

**Form: Report incident** (modal, opened by *Report incident*; *Report incident* calls `reportIncident`, *Cancel* sends nothing)

**Collects what `reportIncident` sends before it is called.** Required: `id`, `kind`, `severity`, `venueId`, `description`, `occurredAt`, `recordedAt`. Optional: `assetId`, `locationDescription`, `involvedSubjectIds`, `involvedStaffPrincipalIds`, `witnessCount`, `firstAidGiven`, `emergencyServicesCalled`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `reportIncident` body |
| Kind `kind` | select | required | — | Guest injury · Staff injury · Near miss · Property damage · Equipment failure · Security incident · Fire or evacuation · Food safety · Environmental · Other | — | — | `reportIncident` body |
| Severity `severity` | radio group | required | — | Near miss · Minor · Moderate · Major · Critical | — | — | `reportIncident` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `reportIncident` body |
| Asset `assetId` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `reportIncident` body |
| Location description `locationDescription` | text area | optional | — | max length 500 | — | — | `reportIncident` body |
| Description `description` | text area | required | — | min length 3; max length 10000 | — | — | `reportIncident` body |
| Involved subjects `involvedSubjectIds` | multi-picker: choose involved subjects | optional | — | — | — | Opaque references. Personal details live in the erasable store, so the incident record survives an erasure request intact. | `reportIncident` body |
| Involved staff principals `involvedStaffPrincipalIds` | multi-picker: choose involved staff principals | optional | — | — | — | — | `reportIncident` body |
| Witness count `witnessCount` | number field | optional | — | — | — | — | `reportIncident` body |
| First aid given `firstAidGiven` | toggle | optional | off | — | — | — | `reportIncident` body |
| Emergency services called `emergencyServicesCalled` | toggle | optional | off | — | — | — | `reportIncident` body |
| Attachment refs `attachmentRefs` | list of values (chips) | optional | — | — | — | — | `reportIncident` body |
| Occurred at `occurredAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `reportIncident` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `reportIncident` body |

Errors to draw in the form: 400 Validation failed

**Form: Create case** (modal, opened by *Create case*; *Create case* calls `createCase`, *Cancel* sends nothing)

**Collects what `createCase` sends before it is called.** Required: `id`, `subject`, `description`, `channel`, `recordedAt`. Optional: `subjectId`, `categoryId`, `priority`, `kind`, `venueId`, `relatedOrderId`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createCase` body |
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | — | `createCase` body |
| Subject `subject` | text field | required | — | max length 200 | — | — | `createCase` body |
| Description `description` | text area | required | — | max length 10000 | — | — | `createCase` body |
| Category `categoryId` | picker: choose a category | optional | — | — | shows names, sends the id | — | `createCase` body |
| Membership `membershipId` | picker: choose a membership | optional | — | — | shows names, sends the id | The identity membership this case concerns (`identity.customer_membership`); member case notes are cases with this set. | `createCase` body |
| Priority `priority` | radio group | optional | Normal | Low · Normal · High · Urgent | — | — | `createCase` body |
| Kind `kind` | select | optional | — | Lost property · Complaint · Question · Accessibility · Refund request · Other; Stored on the case, because a lost-property report that forgets it was one cannot be routed to the lost and found desk.; A case raised as `other` must carry a non-empty `detail` … | — | What the guest says the case is about, in their words rather than the venue's taxonomy — `raiseMyCase` asks for it and `categoryId` is what staff file it under. | `createCase` body |
| Channel `channel` | select | required | — | Email · SMS · Whatsapp · Push · In app · Post | — | — | `createCase` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `createCase` body |
| Related order `relatedOrderId` | text field | optional | — | — | — | — | `createCase` body |
| Attachment refs `attachmentRefs` | list of values (chips) | optional | — | — | — | Stored on the opening `CaseMessage`, not on the case. | `createCase` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time the case was raised. The server stamps `Case.syncedAt` on arrival. | `createCase` body |

**Form: Add case message** (modal, opened by *Add case message*; *Add case message* calls `addCaseMessage`, *Cancel* sends nothing)

**Collects what `addCaseMessage` sends before it is called.** Required: `id`, `body`, `isInternal`, `recordedAt`. Optional: `channel`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `addCaseMessage` body |
| Body `body` | text area | required | — | min length 1; max length 10000 | — | — | `addCaseMessage` body |
| Is internal `isInternal` | toggle | required | — | — | — | — | `addCaseMessage` body |
| Channel `channel` | select | optional | — | Email · SMS · Whatsapp · Push · In app · Post | — | — | `addCaseMessage` body |
| Attachment refs `attachmentRefs` | list of values (chips) | optional | — | — | — | — | `addCaseMessage` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `addCaseMessage` body |

**Form: Escalate case** (modal, opened by *Escalate case*; *Escalate case* calls `escalateCase`, *Cancel* sends nothing)

**Collects what `escalateCase` sends before it is called.** Required: `reason`. Optional: `assignToPrincipalId`, `newPriority`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `escalateCase` body |
| Assign to principal `assignToPrincipalId` | picker: choose an assign to principal | optional | — | — | shows names, sends the id | — | `escalateCase` body |
| New priority `newPriority` | radio group | optional | — | Low · Normal · High · Urgent | — | — | `escalateCase` body |

**Form: Record authority notification** (modal, opened by *Record authority notification*; *Record authority notification* calls `recordAuthorityNotification`, *Cancel* sends nothing)

**Collects what `recordAuthorityNotification` sends before it is called.** Required: `authority`, `notifiedAt`. Optional: `reference`, `notifiedByPrincipalId`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Authority `authority` | text field | required | — | max length 200 | — | — | `recordAuthorityNotification` body |
| Reference `reference` | text field | optional | — | max length 128 | — | — | `recordAuthorityNotification` body |
| Notified at `notifiedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `recordAuthorityNotification` body |
| Notified by principal `notifiedByPrincipalId` | picker: choose a notified by principal | optional | — | — | shows names, sends the id | — | `recordAuthorityNotification` body |
| Attachment refs `attachmentRefs` | list of values (chips) | optional | — | — | — | — | `recordAuthorityNotification` body |

Errors to draw in the form: 409 The incident is not reportable (`isReportable` false, audit R106 (6)).

**Form: Reopen case** (modal, opened by *Reopen case*; *Reopen case* calls `reopenCase`, *Cancel* sends nothing)

**Collects what `reopenCase` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | — | — | — | `reopenCase` body |

Errors to draw in the form: 409 The case is not `resolved` — a `closed` case is past its reopen window, and an open one has nothing to reopen. (StateTransitionProblem)

**Form: Save case** (modal, opened by *Save case*; *Save case* calls `updateCase`, *Cancel* sends nothing)

**Collects what `updateCase` sends before it is called.** Nothing in the body is required. Optional: `status`, `priority`, `assignedToPrincipalId`, `categoryId`, `resolutionNote`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | select | optional | — | Open · In progress · Awaiting guest · Escalated · Resolved · Closed | — | — | `updateCase` body |
| Priority `priority` | radio group | optional | — | Low · Normal · High · Urgent | — | — | `updateCase` body |
| Assigned to principal `assignedToPrincipalId` | picker: choose an assigned to principal | optional | — | — | shows names, sends the id | — | `updateCase` body |
| Category `categoryId` | picker: choose a category | optional | — | — | shows names, sends the id | — | `updateCase` body |
| Resolution note `resolutionNote` | text area | optional | — | max length 2000 | — | — | `updateCase` body |

Errors to draw in the form: 400 Resolving without a resolution note

**Form: Save incident** (modal, opened by *Save incident*; *Save incident* calls `updateIncident`, *Cancel* sends nothing)

**Collects what `updateIncident` sends before it is called.** Nothing in the body is required. Optional: `status`, `severity`, `assignedToPrincipalId`, `investigationNote`, `rootCause`, `correctiveActions`, `correctiveWorkOrderId`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | radio group | optional | — | Reported · Under investigation · Action required · Closed | — | — | `updateIncident` body |
| Severity `severity` | radio group | optional | — | Near miss · Minor · Moderate · Major · Critical | — | — | `updateIncident` body |
| Assigned to principal `assignedToPrincipalId` | picker: choose an assigned to principal | optional | — | — | shows names, sends the id | — | `updateIncident` body |
| Investigation note `investigationNote` | text area | optional | — | max length 10000 | — | Appended as a new entry of `IncidentDetail.investigationNotes`, never overwriting the last (audit R106 (5)). | `updateIncident` body |
| Root cause `rootCause` | text area | optional | — | max length 2000 | — | — | `updateIncident` body |
| Corrective actions `correctiveActions` | text area | optional | — | max length 5000 | — | — | `updateIncident` body |
| Corrective work order `correctiveWorkOrderId` | picker: choose a corrective work order | optional | — | — | shows names, sends the id | — | `updateIncident` body |
| Attachment refs `attachmentRefs` | list of values (chips) | optional | — | — | — | — | `updateIncident` body |
| Escalate `escalate` | group | optional | — | — | — | Escalate an incident under investigation (the optional Escalated step; CHG-RUL-011). | `updateIncident` body |
| To principal `escalate.toPrincipalId` | picker: choose a to principal | required | — | — | shows names, sends the id | — | `updateIncident` body |
| Reason `escalate.reason` | text area | required | — | min length 3; max length 1000 | — | — | `updateIncident` body |
| Reason `reason` | text area | optional | — | min length 3; max length 1000 | — | Why the status changes. Required to reopen a closed incident (back to `underInvestigation`) and to close a `reported` one straight away (CHG-RUL-011). | `updateIncident` body |

Errors to draw in the form: 400 Closure attempted without findings or a corrective action; 403 A critical incident closed by the person who completed its corrective action (`closer-completed-action`; workbook Q530; CHG-CSA-033).; 422 A move outside the incident flow (`incident-transition-not-allowed`; CHG-RUL-011): to `actionRequired`, from `closed` to anything but `underInvestigation`, a …

#### Outputs: what the screen shows and produces

**Shown**

**Every case** (data table, from `listCases`)

| Shows | Format | Notes |
|---|---|---|
| Case number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Guest name | text | Resolved from `pii.subject` when the case is read, never stored on the case. A name copied onto a case row is personal data outside the … |
| Subject | text | The case's one-line title, not a person. Stored as `title` so the table does not hold `subject` beside `subject_id`; the wire keeps … |
| Status | chip: Open, In progress, Awaiting guest, Escalated, Resolved, Closed | — |

**Every incident** (data table, from `listIncidents`)

| Shows | Format | Notes |
|---|---|---|
| Incident number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Severity | chip: Near miss, Minor, Moderate, Major, Critical | — |
| Status | chip: Reported, Under investigation, Action required, Closed | — |
| Location description | text | — |

**The selected case** (detail panel, from `listCases`)

| Shows | Format | Notes |
|---|---|---|
| Case number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Guest name | text | Resolved from `pii.subject` when the case is read, never stored on the case. A name copied onto a case row is personal data outside the … |
| Subject | text | The case's one-line title, not a person. Stored as `title` so the table does not hold `subject` beside `subject_id`; the wire keeps … |
| Status | chip: Open, In progress, Awaiting guest, Escalated, Resolved, Closed | — |
| Priority | chip: Low, Normal, High, Urgent | — |

**The incident** (detail panel, from `getIncident`)

| Shows | Format | Notes |
|---|---|---|
| Incident number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Kind | chip: Guest injury, Staff injury, Near miss, Property damage, Equipment failure, Security … | — |
| Severity | chip: Near miss, Minor, Moderate, Major, Critical | — |
| Status | chip: Reported, Under investigation, Action required, Closed | — |
| Location description | text | — |

**The case** (detail panel, from `getCase`)

| Shows | Format | Notes |
|---|---|---|
| Case number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Guest name | text | Resolved from `pii.subject` when the case is read, never stored on the case. A name copied onto a case row is personal data outside the … |
| Subject | text | The case's one-line title, not a person. Stored as `title` so the table does not hold `subject` beside `subject_id`; the wire keeps … |
| Status | chip: Open, In progress, Awaiting guest, Escalated, Resolved, Closed | — |
| Priority | chip: Low, Normal, High, Urgent | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Report incident (primary button) | `reportIncident` POST `/incidents` | ReportIncidentRequest | Incident | 400 Validation failed | works offline; opens modal first |
| Create case (secondary button) | `createCase` POST `/cases` | CreateCaseRequest | Case | — | works offline; opens modal first |
| Add case message (secondary button) | `addCaseMessage` POST `/cases/{caseId}/messages` | inline | CaseMessage | — | works offline; opens modal first |
| Escalate case (secondary button) | `escalateCase` POST `/cases/{caseId}/escalate` | inline | Case | — | opens modal first |
| Record authority notification (secondary button) | `recordAuthorityNotification` POST `/incidents/{incidentId}/notify-authority` | inline | Incident | 409 The incident is not reportable (`isReportable` false, audit R106 (6)). | opens modal first |
| Reopen case (secondary button) | `reopenCase` POST `/cases/{caseId}/reopen` | inline | Case | 409 The case is not `resolved` — a `closed` case is past its reopen window, and an open one has nothing to reopen. (StateTransitionProblem) | opens modal first |
| Save case (secondary button) | `updateCase` PATCH `/cases/{caseId}` | inline | Case | 400 Resolving without a resolution note | opens modal first |
| Save incident (secondary button) | `updateIncident` PATCH `/incidents/{incidentId}` | inline | Incident | 400 Closure attempted without findings or a corrective action; 403 A critical incident closed by the person who completed its corrective action (`closer-completed-action`; workbook Q530; CHG-CSA-033).; 422 A move … | opens modal first |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Existing cases**: The guest's open cases appear first when the guest is identified. *(source: F70 step 1)*

**What each action does** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Report incident**: For harm or safety (regulatory weight), separate from a service case. *(source: contracts/satellite/maintenance.yaml#reportIncident)*
- **Reply or note**: Explicit choice between reply to guest and internal note. *(source: contracts/satellite/marketing-crm.yaml#addCaseMessage; F05 step 2)*

**Data it reads**: `listCases` (onLoad, List service cases); `listIncidents` (onLoad, List incidents)

**Where the user goes next**

- → `EMP-030` Venue map: *They show the guest where to go*
- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*; carries `incidentId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The guest assistance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the guest assistance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No guest assistance yet. Offers Create case (`createCase`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on status, assignedToPrincipalId, breachedSla, priority and the guest assistance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `CASE_VIEW`, which `listCases` requires to show this screen, and names that permission (the screen's other reads need `INCIDENT_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `CASE_MANAGE` for `createCase`, `addCaseMessage`, `escalateCase` … |
| Offline (`?state=offline`) | Queues locally and syncs on reconnect. The pending count is always current because it is local |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Closure attempted without findings or a corrective action; 400 Resolving without a resolution note; 400 Validation failed; 409 The case is not `resolved` — a `closed` case is past its reopen window, and an open one has nothing to reopen. (StateTransitionProblem) |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
case: CA-1088 - Question - Is the wave pool open? - resolved on the spot
```

#### Permissions

- `reportIncident` → `INCIDENT_REPORT` (operate) · staff
- `createCase` → `CASE_MANAGE` (configure) · staff, guest, partner
- `addCaseMessage` → `CASE_MANAGE` (configure) · staff, partner
- `escalateCase` → `CASE_MANAGE` (configure) · staff, partner
- `getCase` → `CASE_VIEW` (read) · staff, partner
- `getIncident` → `INCIDENT_VIEW` (read) · staff
- `listCases` → `CASE_VIEW` (read) · staff, guest, partner
- `listIncidents` → `INCIDENT_VIEW` (read) · staff
- `recordAuthorityNotification` → `INCIDENT_MANAGE` (configure) · staff
- `reopenCase` → `CASE_MANAGE` (configure) · staff, partner
- `updateCase` → `CASE_MANAGE` (configure) · staff, partner
- `updateIncident` → `INCIDENT_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `CASE_VIEW`, which `listCases` requires to show this screen, and names that permission (the screen's other reads need `INCIDENT_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `CASE_MANAGE` for `createCase`, `addCaseMessage`, `escalateCase` …

#### Requirements it meets

23 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 17.5.3 | Hazard Reporting - System shall support hazard reporting. | Maintenance & Safety Management | CONTRACTED | `reportIncident` |
| 17.5.4 | Incident Reporting - System shall support incident reporting. | Maintenance & Safety Management | CONTRACTED | `reportIncident` |
| 17.5.5 | Near-Miss Reporting - System shall support near-miss reporting. | Maintenance & Safety Management | CONTRACTED | `reportIncident` |
| 18.4.1 | Hazard Reporting - Users shall submit hazard reports. | Employee Mobile App & AI Assistant | CONTRACTED | `reportIncident` |
| 18.4.2 | Incident Reporting - Users shall submit incident reports. | Employee Mobile App & AI Assistant | CONTRACTED | `reportIncident` |
| 18.4.3 | Near-Miss Reporting - Users shall submit near-miss reports. | Employee Mobile App & AI Assistant | CONTRACTED | `reportIncident` |
| 18.4.4 | Safety Inspections - Users shall perform inspections. | Employee Mobile App & AI Assistant | CONTRACTED | `reportIncident` |
| 18.4.5 | Safety Checklists - Users shall complete safety checklists. | Employee Mobile App & AI Assistant | CONTRACTED | `reportIncident` |
| 18.4.6 | Corrective Actions - Users shall submit corrective actions. | Employee Mobile App & AI Assistant | CONTRACTED | `reportIncident` |
| 19.2.66 | Guest Support - System shall provide guest support channels. | Guest Mobile App & Branding | CONTRACTED | `createCase` |
| 19.2.70 | Complaint Management - System shall support guest complaints. | Guest Mobile App & Branding | CONTRACTED | `createCase` |
| 2.8.12 | System shall allow agents to create, assign, escalate, track, and resolve guest cases including complaints, refund requests, service requests, incidents, and operational issues. Cases shall be linked … | Ticketing Sales | CONTRACTED | `createCase` |
| … 11 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Guest assistance: quick access to supervisors, announcements and venue information (e.g. opening hours), live ride/attraction status, and logging found items that surface for guest claim. *(client request · MoM 10 Aug 2026, 5.6 Roster, Leave & Break Management, Resources · DI-238)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-029` · status **notStarted** · provenance generated
- Flow F70 *A guest needs help and something is lost*, step 1: The steward opens guest assistance. → **Any existing case first.** A guest asking twice about the same thing should not be asked to explain it twice.
- ADR-0023 *— Personal data lives apart from the append-only ledger* (`docs/adr/0023-pii-separation.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (64), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (23 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-029?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Report incident, Create case, Add case message, Escalate case, Record authority notification, Reopen case, Save case, Save incident.
- [ ] Every transition is wired: `EMP-030`, `EMP-001`, `EMP-002`, `EMP-003`.
- [ ] Every gated control is gated: `CASE_MANAGE`, `CASE_VIEW`, `INCIDENT_MANAGE`, `INCIDENT_REPORT`, `INCIDENT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-030` Venue map

**Find a gate, an exit or a colleague.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 2 · needs the `ticketing` module |
| Block | Block C · task APP-STAFF-EMP-030 |
| Who uses it | venue staff holding `VENUE_MAP_VIEW` (1 read); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listDiningOutlets` reads the population and `getVenueMap` reads one of them — list, select, act |
| Offline | Cached map. **The zone list always works** because it is text |
| Opens with | `mapId` (deepLink), `venueId` (session) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/operations/venue-map` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Wired to the venue map 18 August (CF-123).** The published map with live state on it: 3.2.64 asks for access-control statistics drawn on a graphical map, and the same view carries wait times and closed rides. **The map changes monthly and the state changes every few seconds**, so they are separate calls. **Removed 24 August**: getRefundPolicy, setRefundPolicy. **Bulk-attach residue, found by walking a journey.** A device-settings screen does not read guest loyalty, a venue map does not set a refund policy, a shift summary does not close the shift, and **a rota a steward can rewrite is not a rota.** **Drawn 26 August** — `Seat Board 4.dc.html` frame `seat-4c`. **The frame names this screen on its own face**, which is the first pack to do that: the earlier F&B, POS and Retail boards had to be hand-assigned by purpose after three derivation attempts produced nonsense. **A board that says what it draws removes the guess entirely.**

**Known gaps.** **1 declared operation reach no component on this screen**: getVenueMapLive. Either the screen is missing what calls them, or the declaration is residue. Removed 2 October 2026 (CHG-WIR-008): listDiningOutlets and listDeliveryLocations are guest-audience operations with no permission; a staff screen calling them bypasses the staff permission model … Removed 2 October 2026 (CHG-WIR-008): listDiningOutlets and listDeliveryLocations are guest-audience operations with no permission; a staff screen calling them bypasses the staff permission model …

**From the Food, Beverage & Retail process.** Staff help a guest find a place: an outlet that is open now, a gate, toilets, the way to a lounger. From the F&B angle it answers "where can this guest eat right now, and how long is the wait", and, for a runner, "where is lounger B-14". The one thing to get right: an outlet that has closed must not be shown as open, because the map would send a guest to a locked door.

**Known correction pending (do not draw the wrong version)**

- **getVenueMapLive is declared and reaches no component (the screen's own gap).** Why: F70 step 2 depends on it for closures and queues, so the map otherwise shows an outlet that shut an hour ago. *(source: F70 step 2 / screens/P06-staff-app.yaml#EMP-030; Food, Beverage & Retail)*
- **requiresModule ticketing, and module placement under F&B.** Why: The venue map is a core wayfinding screen (venue-map contract). Gating it on ticketing hides it from an F&B-only tenant, and F&B only adds the dining layer. *(source: screens/P06-staff-app.yaml#EMP-030 / DI-228; Food, Beverage & Retail)*
- **The purpose "Find a gate, an exit or a colleague" has no operation for colleagues.** Why: Nothing on the screen reads staff locations. Drop "or a colleague", or add the source. *(source: screens/P06-staff-app.yaml#EMP-030; Food, Beverage & Retail)*

**Fixed on main** (the package already carries these; draw what it says): listDiningOutlets and listDeliveryLocations are guest-audience operations with no permission, and they are listed as unpermissioned on the … (CHG-WIR-008); "Ordering method" free-text filter and the "Every dining outlet" and "Every delivery location" data tables with outletId, menuId … (CHG-WIR-008).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Version | number field | — | — | `getVenueMap` ?version |
| Draft | toggle | off | Staff only, and it needs `VENUE_MAP_MANAGE`, because the draft is unfinished work that must never reach a guest. | `getVenueMap` ?draft |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**The venue map** (detail panel, from `getVenueMap`)

| Shows | Format | Notes |
|---|---|---|
| Map | grouped details | A park map, or a floor plan. Several per venue — a guest on the second floor should not be shown the ground floor's toilets. |
| Points | list or chips (count when long) | — |
| Paths | list or chips (count when long) | — |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Outlets on the map**: Only outlets open now by default, each with its name, kind (restaurant, counter, bar), wait in minutes and how it takes orders ("Table service", "Order at counter", "Order in app for collection"). Closed outlets are greyed with their opening time, never hidden while the "Show closed" filter is on. *(source: contracts/satellite/fnb.yaml#listDiningOutlets / F70 step 2 / contracts/satellite/venue-map.yaml#getVenueMapLive)*
- **Delivery locations (runner view)**: A search by location label (lounger, cabana, seat) giving the zone and the walk time. Unserviceable locations show their reason. These are delivery points, not bookable restaurant tables: dining tables never appear on the venue map. *(source: contracts/satellite/fnb.yaml#listDeliveryLocations / contracts/satellite/fnb.yaml#createTableReservation)*

**Data it reads**: `getVenueMap` (onLoad, A map with its points and paths); `getVenueMapLive` (onLoad, The map with live operational state on it)

**Where the user goes next**

- → `EMP-028` Lost & found: *A lost item is logged*
- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The venue map list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the venue map untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No venue map yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on openNow, orderingMethod and the venue map are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `VENUE_MAP_VIEW`, which `getVenueMap` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Cached map. **The zone list always works** because it is text |

#### Edge cases to draw

- **No signal in the middle of the park**: The cached map and the text list of zones still work; live waits and closures are greyed with "as of 14:05". *(source: screens/P06-staff-app.yaml#EMP-030 / contracts/satellite/venue-map.yaml#getVenueMap)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
outlets:
- name: Oasis Bistro
  kind: Restaurant
  zone: Main Plaza
  order: Table service
  wait: 15 min
  open: 12:00 to 23:00
- name: Bite & Go
  kind: Counter
  zone: Wave Pool
  order: Order at counter
  wait: 5 min
- name: Lagoon Bar
  kind: Bar
  zone: Lazy River
  state: Closed
  opens: '16:00'
deliveryLocation:
  label: Lounger B-14
  zone: Wave Pool beach
  walk: 4 min
  servedBy: Bite & Go
```

#### Permissions

- `getVenueMap` → `VENUE_MAP_VIEW` (read) · staff, guest
- `getVenueMapLive` → `VENUE_MAP_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `VENUE_MAP_VIEW`, which `getVenueMap` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.55 | Interactive Venue Map - System shall provide interactive venue maps. | Guest Mobile App & Branding | CONTRACTED | `getVenueMap` |
| 3.2.64 | It is possible to have an access control points graphical map presenting statistics in real time. | Admission and Access | CONTRACTED | `getVenueMapLive` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-030` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Seat Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/Seat Board 4.dc.html`
- Client design-board frames: `Seat Board 4.dc.html#seat-4c`
- Flow F70 *A guest needs help and something is lost*, step 2: They show the guest where to go. → **`getVenueMapLive` carries closures and queues.** A map showing an outlet that shut an hour ago sends the guest to a locked door.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (3 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-030?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `EMP-028`, `EMP-001`, `EMP-002`, `EMP-003`.
- [ ] Every gated control is gated: `VENUE_MAP_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
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

**8 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"addCaseMessage": {"method":"POST","path":"/cases/{caseId}/messages","contract":"marketing-crm","summary":"Add a message or internal note","permission":"CASE_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CaseMessage"},
"addIncidentPerson": {"method":"POST","path":"/incidents/{incidentId}/people","contract":"maintenance","summary":"Add a person involved in an incident","permission":"INCIDENT_REPORT","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AddIncidentPersonRequest","responds":"IncidentInvolvedParty"},
"applyManualDiscount": {"method":"POST","path":"/orders/{orderId}/discounts","contract":"orders","summary":"Apply a discount a cashier chose","permission":"ORDER_DISCOUNT","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ManualDiscountRequest","responds":"Order"},
"callNextParties": {"method":"POST","path":"/queues/{queueId}/call-next","contract":"queue","summary":"Call the next parties forward","permission":"QUEUE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"createCase": {"method":"POST","path":"/cases","contract":"marketing-crm","summary":"Raise a service case","permission":"CASE_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateCaseRequest","responds":"Case"},
"createOrder": {"method":"POST","path":"/orders","contract":"orders","summary":"Create an order","permission":"ORDER_CREATE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateOrderRequest","responds":"Order"},
"createRefund": {"method":"POST","path":"/orders/{orderId}/refunds","contract":"orders","summary":"Refund an order, wholly or in part","permission":"ORDER_REFUND","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateRefundRequest","responds":null},
"escalateCase": {"method":"POST","path":"/cases/{caseId}/escalate","contract":"marketing-crm","summary":"Escalate a case","permission":"CASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Case"},
"exchangeOrderLines": {"method":"POST","path":"/orders/{orderId}/exchanges","contract":"orders","summary":"Exchange lines for different products or dates","permission":"ORDER_EXCHANGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ExchangeOrderRequest","responds":"OrderExchangeResult"},
"getCase": {"method":"GET","path":"/cases/{caseId}","contract":"marketing-crm","summary":"Read a case with its thread","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"CaseDetail"},
"getChannelAllocations": {"method":"GET","path":"/channel-capacities/{channelCapacityId}/channel-allocations","contract":"catalogue","summary":"Capacity allocated to each channel","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ChannelAllocationSet"},
"getIncident": {"method":"GET","path":"/incidents/{incidentId}","contract":"maintenance","summary":"Read an incident","permission":"INCIDENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"IncidentDetail"},
"getOrder": {"method":"GET","path":"/orders/{orderId}","contract":"orders","summary":"Read an order","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Order"},
"getOrderStatement": {"method":"GET","path":"/orders/{orderId}/statement","contract":"orders","summary":"Full financial history of an order","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"OrderStatement"},
"getProduct": {"method":"GET","path":"/products/{productId}","contract":"catalogue","summary":"Read a product","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Product"},
"getQueue": {"method":"GET","path":"/queues/{queueId}","contract":"queue","summary":"Read a queue with live position","permission":"QUEUE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"QueueDetail"},
"getVenueMap": {"method":"GET","path":"/venue-maps/{mapId}","contract":"venue-map","summary":"A map with its points and paths","permission":"VENUE_MAP_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"version","in":"query","required":null},{"name":"draft","in":"query","required":null}],"requestBody":null,"responds":"VenueMapDetail"},
"getVenueMapLive": {"method":"GET","path":"/venue-maps/{mapId}/live","contract":"venue-map","summary":"The map with live operational state on it","permission":"VENUE_MAP_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":null},
"getWaitTimes": {"method":"GET","path":"/queues/wait-times","contract":"queue","summary":"Wait times across a venue","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":true},{"name":"category","in":"query","required":null}],"requestBody":null,"responds":"WaitTime"},
"holdOrder": {"method":"POST","path":"/orders/{orderId}/hold","contract":"orders","summary":"Park a sale and free the till","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Order"},
"listAlternativeCodes": {"method":"GET","path":"/products/{productId}/alternative-codes","contract":"catalogue","summary":"External identifiers for a product","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AlternativeCode"},
"listAttendance": {"method":"GET","path":"/attendance","contract":"workforce","summary":"Who was here","permission":"WORKFORCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"date","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"exceptionsOnly","in":"query","required":null}],"requestBody":null,"responds":"AttendanceRecord"},
"listCases": {"method":"GET","path":"/cases","contract":"marketing-crm","summary":"List service cases","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"assignedToPrincipalId","in":"query","required":null},{"name":"breachedSla","in":"query","required":null},{"name":"priority","in":"query","required":null},{"name":"membershipId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listChannelCapacities": {"method":"GET","path":"/channel-capacities","contract":"catalogue","summary":"List channel capacities","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"performanceId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listIncidents": {"method":"GET","path":"/incidents","contract":"maintenance","summary":"List incidents","permission":"INCIDENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"severity","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"isReportable","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOrderRefunds": {"method":"GET","path":"/orders/{orderId}/refunds","contract":"orders","summary":"List refunds against an order","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOrders": {"method":"GET","path":"/orders","contract":"orders","summary":"List orders","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"shiftId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"createdFrom","in":"query","required":null},{"name":"createdTo","in":"query","required":null},{"name":"workstationId","in":"query","required":null},{"name":"subjectId","in":"query","required":null},{"name":"tender","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProductVariants": {"method":"GET","path":"/products/{productId}/variants","contract":"catalogue","summary":"List generated variants","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProducts": {"method":"GET","path":"/products","contract":"catalogue","summary":"List products","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"isSellable","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"segmentTag","in":"query","required":null},{"name":"guidedAnswerIds","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listQueueEntries": {"method":"GET","path":"/queues/{queueId}/entries","contract":"queue","summary":"List entries in a queue","permission":"QUEUE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listQueues": {"method":"GET","path":"/queues","contract":"queue","summary":"List queues","permission":"QUEUE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"openOnly","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"modifyOrder": {"method":"POST","path":"/orders/{orderId}/modify","contract":"orders","summary":"Add or remove lines on an existing order","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ModifyOrderRequest","responds":"OrderModificationResult"},
"recordAttendance": {"method":"POST","path":"/attendance/clock","contract":"workforce","summary":"Clock in, clock out, or take a break","permission":"ATTENDANCE_RECORD","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AttendanceRecord"},
"recordAuthorityNotification": {"method":"POST","path":"/incidents/{incidentId}/notify-authority","contract":"maintenance","summary":"Record notification to an external authority","permission":"INCIDENT_MANAGE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Incident"},
"relinquishChannelAllocation": {"method":"POST","path":"/channel-capacities/{channelCapacityId}/channel-allocations/release","contract":"catalogue","summary":"Return unsold channel allocation to the general pool","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ChannelAllocationSet"},
"reopenCase": {"method":"POST","path":"/cases/{caseId}/reopen","contract":"marketing-crm","summary":"Reopen a resolved case","permission":"CASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Case"},
"reportIncident": {"method":"POST","path":"/incidents","contract":"maintenance","summary":"Report an incident","permission":"INCIDENT_REPORT","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ReportIncidentRequest","responds":"Incident"},
"reprintOrder": {"method":"POST","path":"/orders/{orderId}/reprints","contract":"orders","summary":"Reprint or resend tickets","permission":"ORDER_REPRINT","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"requestSuggestion": {"method":"POST","path":"/ai/suggestions","contract":"ai","summary":"Ask for an answer, however it is currently produced","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Suggestion"},
"rescheduleOrder": {"method":"POST","path":"/orders/{orderId}/reschedule","contract":"orders","summary":"Move an order to another performance","permission":"ORDER_RESCHEDULE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"OrderExchangeResult"},
"resolveProductByCode": {"method":"GET","path":"/products/resolve","contract":"catalogue","summary":"Resolve a partner code to a product","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"code","in":"query","required":true},{"name":"partnerId","in":"query","required":null}],"requestBody":null,"responds":"ProductVariant"},
"resumeOrder": {"method":"POST","path":"/orders/{orderId}/resume","contract":"orders","summary":"Bring a parked sale back to a till","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"OrderResumeResult"},
"searchGuests": {"method":"GET","path":"/guests","contract":"marketing-crm","summary":"Search guest profiles","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"search","in":"query","required":null},{"name":"segmentId","in":"query","required":null},{"name":"hasConsentFor","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"setQueueStatus": {"method":"PUT","path":"/queues/{queueId}/status","contract":"queue","summary":"Open, pause or close a queue","permission":"QUEUE_MANAGE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"QueueStatusResult"},
"setWaitTime": {"method":"PUT","path":"/queues/{queueId}/wait-time","contract":"queue","summary":"Manually set a wait time","permission":"QUEUE_MANAGE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WaitTime"},
"splitOrder": {"method":"POST","path":"/orders/{orderId}/split","contract":"orders","summary":"Break one order into independent orders","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"updateCase": {"method":"PATCH","path":"/cases/{caseId}","contract":"marketing-crm","summary":"Assign, reprioritise or resolve a case","permission":"CASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Case"},
"updateIncident": {"method":"PATCH","path":"/incidents/{incidentId}","contract":"maintenance","summary":"Investigate, escalate, close or reopen an incident","permission":"INCIDENT_MANAGE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Incident"},
"uploadIncidentMedia": {"method":"POST","path":"/incidents/{incidentId}/media","contract":"maintenance","summary":"Add a photo, video or document to an incident","permission":"INCIDENT_REPORT","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"UploadIncidentMediaRequest","responds":"IncidentMedia"},
"voidOrder": {"method":"POST","path":"/orders/{orderId}/voids","contract":"orders","summary":"Void an order","permission":"ORDER_VOID","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Order"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AddIncidentPersonRequest": {"x-ticvai-persistence":"none — request only; the person goes to pii.subject, the link to maintenance.incident_involved_party","type":"object","required":["role"],"properties":{"role":{"type":"string","enum":["injured","involved","witness","reporter"],"description":"The person's part in the incident."},"partyType":{"type":"string","enum":["guest","publicMember","staff","contractor"],"default":"guest"},"name":{"type":"string","maxLength":200,"writeOnly":true,"description":"Written to the erasable store (`pii.subject`), never to the incident (ADR-0023)."},"phone":{"type":"string","maxLength":32,"writeOnly":true,"description":"Stored only with `contactConsent` true."},"email":{"type":"string","format":"email","maxLength":254,"writeOnly":true,"description":"Stored only with `contactConsent` true."},"contactConsent":{"type":"boolean","default":false,"description":"The person agreed to be contacted about this incident (consent rules apply; CHG-RUL-013). Recorded as a consent with who took it and when.\n"},"guestSubjectId":{"type":"string","format":"uuid","nullable":true,"description":"A known guest, from the optional guest lookup; links their existing subject."},"principalId":{"type":"string","format":"uuid","nullable":true,"description":"A member of staff; a principal, not a PII subject."},"note":{"type":"string","maxLength":2000}}},
"AiMaturity": {"type":"object","x-ticvai-persistence":"none — embedded as jsonb on ai.suggestion and ai.forecast_version","description":"**Where an answer stands, on every answer** (29 September, AI functions review; baseline then learn). The customer sees a stage badge and a \"Based on\" chip, never a bare percentage (design 5.6), and \"Limited historical data\" while the starting pattern carries more than half the weight.","required":["stage","basedOn"],"properties":{"stage":{"type":"string","enum":["starting","learning","established","learned"],"description":"`starting`: the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, weather). `learning`: own data carries short-range patterns (about 4 weeks). `established`: own level and trend lead, the baseline fills gaps such as a holiday not yet seen (about 3 months, or at once with 12+ months imported). `learned`: a model trained on this tenant's data, promoted by an admin (AI-D16)."},"basedOn":{"type":"string","description":"The \"Based on\" line, in words, e.g. *Based on: your venue profile, UAE calendar, weather, 23 days of your sales*. Always present."},"sources":{"type":"array","items":{"type":"object","required":["source"],"properties":{"source":{"type":"string","enum":["venueSettings","startingPattern","calendar","weather","bookingsOnHand","ownHistory","importedHistory","configuration","trainedModel"]},"detail":{"type":"string","nullable":true,"description":"e.g. *23 days*, *water park pattern v3*, *Eid al-Adha 2027*."},"observations":{"type":"integer","nullable":true}}}},"ownDataShare":{"type":"number","minimum":0,"maximum":1,"description":"The weight own data carries, `n / (k + n)`. Below 0.5 the answer is marked \"Limited historical data\"."},"limitedHistory":{"type":"boolean"},"nextStage":{"type":"object","nullable":true,"description":"What the next stage needs, e.g. *8 more Saturdays of sales*, or *an admin promotion*.","properties":{"stage":{"type":"string","enum":["learning","established","learned"]},"needs":{"type":"string"},"expectedBy":{"type":"string","format":"date","nullable":true}}}}},
"AlternativeCode": {"x-ticvai-persistence":"catalogue.alternative_code","type":"object","required":["code","partnerId"],"properties":{"code":{"type":"string","maxLength":128},"partnerId":{"type":"string","format":"uuid"},"partnerName":{"type":"string"},"variantId":{"type":"string","format":"uuid"},"note":{"type":"string","maxLength":200}}},
"AttendanceAmendment": {"type":"object","x-ticvai-persistence":"workforce.attendance_amendment","description":"One correction to an attendance record, appended by `amendAttendance` and never updated (decided 28 September, audit R129 (7)).\n","required":["id","attendanceRecordId","amendedByPrincipalId","amendedAt","occurredAtBefore","occurredAtAfter","reason"],"properties":{"id":{"type":"string","format":"uuid"},"attendanceRecordId":{"type":"string","format":"uuid"},"amendedByPrincipalId":{"type":"string","format":"uuid"},"amendedAt":{"type":"string","format":"date-time"},"occurredAtBefore":{"type":"string","format":"date-time","description":"The record's time before this correction."},"occurredAtAfter":{"type":"string","format":"date-time","description":"The time this correction set (`correctedAt` on the request)."},"reason":{"type":"string","maxLength":300}}},
"AttendanceRecord": {"type":"object","x-ticvai-persistence":"workforce.attendance","required":["id","principalId","kind","occurredAt"],"properties":{"id":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid"},"assignmentId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["clockIn","clockOut","breakStart","breakEnd"]},"occurredAt":{"type":"string","format":"date-time","description":"Device time — when it happened."},"recordedAt":{"type":"string","format":"date-time","description":"When the server received it. **Both are kept**: a steward clocking in offline at a gate is not late because the sync was.\n"},"accessPointId":{"type":"string","format":"uuid","nullable":true},"latitude":{"type":"number","nullable":true},"longitude":{"type":"number","nullable":true},"isAmended":{"type":"boolean","readOnly":true},"amendedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Who made the latest amendment. The full history is `amendments` (audit R129 (7))."},"amendmentReason":{"type":"string","nullable":true,"readOnly":true,"description":"The latest amendment's reason. The full history is `amendments` (audit R129 (7))."},"originalOccurredAt":{"type":"string","format":"date-time","nullable":true,"description":"**The original is never overwritten.** Attendance feeds pay, and a record that can be quietly rewritten is not evidence.\n"},"amendments":{"type":"array","readOnly":true,"description":"**Every correction, oldest first, one row each** (decided 28 September, audit R129 (7)). A single set of amendment columns holds only the last one, and the second correction to a record would erase the evidence of the first.\n","items":{"$ref":"#/components/schemas/AttendanceAmendment"}},"exception":{"type":"string","nullable":true,"enum":["late","earlyLeave","missingClockOut","noShow","outOfGeofence","unscheduled"],"description":"Computed against the rota. Null where the record matches what was expected."}}},
"Case": {"x-ticvai-persistence":"marketing.case","x-ticvai-retired-columns":["guest_name","subject","is_sla_breached"],"type":"object","required":["id","caseNumber","subject","status","priority","createdAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Created on the device (`CreateCaseRequest.id`, `raiseMyCase`), so a UUIDv7."},"caseNumber":{"type":"string","readOnly":true,"description":"**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity. Assigned when the case reaches the server, so a retry with the same `id` keeps its number.\n"},"subjectId":{"type":"string","format":"uuid","nullable":true},"guestName":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"description":"**Resolved from `pii.subject` when the case is read, never stored on the case.** A name copied onto a case row is personal data outside the erasable store (ADR-0023), and it had no source anyway — no request carries it. Returned only to callers holding `GUEST_VIEW_PII`, as `searchGuests` does.\n"},"subject":{"type":"string","x-ticvai-column":"title","description":"**The case's one-line title**, not a person. Stored as `title` so the table does not hold `subject` beside `subject_id`; the wire keeps `subject` because screens bind it.\n"},"kind":{"allOf":[{"$ref":"#/components/schemas/CaseKind"}],"nullable":true,"description":"What the guest said it was about, where the guest raised it."},"channel":{"allOf":[{"$ref":"#/components/schemas/MessageChannel"}],"description":"How the guest reached the venue — `CreateCaseRequest.channel`, or `inApp` for a case raised through `raiseMyCase`."},"recordedAt":{"type":"string","format":"date-time","description":"Device time the case was raised — the start of the SLA clock."},"syncedAt":{"type":"string","format":"date-time","readOnly":true,"description":"Server time the case arrived. Equal to `recordedAt` for a case raised online."},"categoryId":{"type":"string","format":"uuid","nullable":true},"queueId":{"type":"string","format":"uuid","nullable":true,"description":"The `ServiceQueue` the case waits in, set by routing (`CaseRoutingRule.queueId`). Null once routed straight to an agent. (decided 29 September, data model for the agreed operations)"},"membershipId":{"type":"string","format":"uuid","nullable":true,"description":"The identity membership this case concerns (`identity.customer_membership`); member case notes are cases with this set. (decided 29 September, coordinator decision DM4, writers pass)"},"status":{"$ref":"#/components/schemas/CaseStatus"},"priority":{"$ref":"#/components/schemas/CasePriority"},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"relatedOrderId":{"type":"string","nullable":true},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"isSlaBreached":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"description":"**Computed when read, never stored.** True once the case has been open longer than its SLA allows — the time from `recordedAt` to `resolvedAt` (or to now, while unresolved), less `slaPausedSeconds`, is past the target that set `slaDueAt`. A stored flag would need a job to flip it at the moment of breach, and no such job is designed; `listCases?breachedSla` filters on the same computation.\n"},"slaPausedSeconds":{"type":"integer","description":"Accrued only while awaiting the guest. Waiting on an internal team does not pause the clock.\n"},"escalationCount":{"type":"integer"},"createdAt":{"type":"string","format":"date-time"},"resolvedAt":{"type":"string","format":"date-time","nullable":true}}},
"CaseDetail": {"x-ticvai-persistence":"marketing.case","allOf":[{"$ref":"#/components/schemas/Case"},{"type":"object","properties":{"description":{"type":"string"},"resolutionNote":{"type":"string","nullable":true},"messages":{"type":"array","items":{"$ref":"#/components/schemas/CaseMessage"}}}}]},
"CaseKind": {"type":"string","description":"**What the guest says the case is about**, in their words rather than the venue's taxonomy — `raiseMyCase` asks for it and `categoryId` is what staff file it under. Stored on the case, because a lost-property report that forgets it was one cannot be routed to the lost and found desk.\n**`other` only with a note (decided 28 September, audit R222).** A case raised as `other` must carry a non-empty `detail` (`raiseMyCase`), or it is refused with 400; the notes are reviewed quarterly to add the real kinds they reveal.\n","enum":["lostProperty","complaint","question","accessibility","refundRequest","other"]},
"CaseMessage": {"x-ticvai-persistence":"marketing.case_message","type":"object","required":["id","body","isInternal","authorKind","recordedAt"],"properties":{"resolution":{"type":"string","description":"**What was actually done about it.** Indexed for retrieval: an agent facing a complaint benefits more from how the last one was resolved than from a policy. Without this column `marketing.case` can only embed its subject line.\n"},"id":{"type":"string"},"body":{"type":"string"},"isInternal":{"type":"boolean"},"authorKind":{"type":"string","enum":["agent","guest","system","ai"]},"authorPrincipalId":{"type":"string","format":"uuid","nullable":true},"channel":{"$ref":"#/components/schemas/MessageChannel"},"attachmentRefs":{"type":"array","items":{"type":"string"}},"recordedAt":{"type":"string","format":"date-time","description":"Device time — `addCaseMessage` is offline-capable."},"syncedAt":{"type":"string","format":"date-time","readOnly":true,"description":"Server time the message arrived."}}},
"CasePriority": {"type":"string","enum":["low","normal","high","urgent"]},
"CaseStatus": {"type":"string","enum":["open","inProgress","awaitingGuest","escalated","resolved","closed"]},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"ChannelAllocation": {"x-ticvai-persistence":"catalogue.channel_allocation","type":"object","required":["channel","allocatedUnits"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"channel":{"$ref":"#/components/schemas/Channel"},"allocatedUnits":{"type":"integer","minimum":0},"soldUnits":{"type":"integer","readOnly":true},"leasedUnits":{"type":"integer","readOnly":true,"description":"Held by terminals on this channel but not yet sold."},"remainingUnits":{"type":"integer","readOnly":true},"releaseAt":{"type":"string","format":"date-time","nullable":true,"description":"Unsold units return to the general pool at this time. How distribution holds are freed close to a performance without someone remembering to do it.\n"},"salesChannelId":{"type":"string","format":"uuid","nullable":true,"description":"The channel profile (`catalogue.sales_channel`) this allocation serves (29 September, data model DM3)."},"allocationType":{"type":"string","enum":["sharedPool","dedicated","percentage","dynamic"],"default":"dedicated","description":"How the allocation is sized (29 September, data model DM3); the allocation rule of ADM-262 lives on this row."},"minimumUnits":{"type":"integer","nullable":true,"minimum":0},"maximumUnits":{"type":"integer","nullable":true,"minimum":0},"replenishmentRule":{"type":"object","additionalProperties":true,"nullable":true,"description":"`{sourceChannelId, trigger, thresholdUnits, sharePercent, units}`."},"waitlistBehavior":{"type":"string","enum":["none","joinWaitlist","notifyOnRelease"],"default":"none"},"releaseThresholdUnits":{"type":"integer","nullable":true,"minimum":0},"releaseHoursBeforeEvent":{"type":"integer","nullable":true,"minimum":0,"description":"Alternative to `releaseAt`, relative to the performance start."},"contractualUnits":{"type":"integer","nullable":true,"minimum":0,"description":"Units a partner agreement guarantees; rebalancing never goes below it."},"minimumGuaranteedUnits":{"type":"integer","nullable":true,"minimum":0},"isFrozen":{"type":"boolean","default":false,"description":"Excluded from rebalancing."}}},
"ChannelAllocationSet": {"x-ticvai-persistence":"none — projection","type":"object","required":["channelCapacityId","capacity","allocations","generalPoolUnits"],"properties":{"channelCapacityId":{"type":"string","format":"uuid"},"capacity":{"type":"integer"},"allocations":{"type":"array","items":{"$ref":"#/components/schemas/ChannelAllocation"}},"generalPoolUnits":{"type":"integer","description":"Unallocated remainder. Any channel may draw from it once its own allocation is exhausted.\n"},"totalSold":{"type":"integer"},"totalRemaining":{"type":"integer"}}},
"ChannelCapacity": {"x-ticvai-persistence":"catalogue.channel_capacity","type":"object","required":["id","performanceId","capacity","sold","leased","remaining","isSeated"],"properties":{"id":{"type":"string","format":"uuid"},"performanceId":{"type":"string","format":"uuid"},"name":{"type":"string"},"seatCategoryId":{"type":"string","format":"uuid","nullable":true},"oversellAllowance":{"type":"integer","default":0,"description":"BL-046, 1.3.13. **The guard existed in one direction** — an envelope could be raised freely and refused reduction below what had sold.\n**Free events oversell deliberately because no-show rates are known.** An allowance on the envelope rather than an admission policy, because **the gate must still refuse when actual capacity is reached** — overselling is a sales decision and admission is a safety one, and they must not share a number.\n"},"oversellBasis":{"type":"string","nullable":true,"enum":["fixedCount","historicNoShowRate","percentage"]},"capacity":{"type":"integer","minimum":0},"sold":{"type":"integer","readOnly":true,"x-ticvai-derived":"onWrite","description":"Units sold. **Maintained on write** (decided 29 September, SD-023): raised by `convertInventoryHold` in the order transaction and by consumption a workstation reports on `renewInventoryHold` or `relinquishInventoryHold`, lowered when a refund or cancellation returns the units. Always `capacity + oversellAllowance = sold + leased + remaining`.\n"},"leased":{"type":"integer","readOnly":true,"x-ticvai-derived":"onWrite","description":"Units in `active` holds, not yet sold. Raised at acquire, lowered at conversion, release, force-release and expiry (SD-023)."},"remaining":{"type":"integer","readOnly":true,"x-ticvai-derived":"onWrite","description":"What can still be held. **Decremented at the hold with a guarded statement** (`remaining >= n`) under the row lock, never at the sale, so two buyers cannot both take the last unit (SD-023, 29 September).\n"},"hasChannelAllocations":{"type":"boolean","description":"True where capacity is divided across channels. Leases then draw from a channel allocation rather than from raw capacity.\n"},"isSeated":{"type":"boolean","description":"Seated envelopes cannot be leased and are blocked offline. A seat map is not a count.\n"}}},
"CreateCaseRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","subject","description","channel","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid"},"subject":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":10000},"categoryId":{"type":"string","format":"uuid"},"membershipId":{"type":"string","format":"uuid","nullable":true,"description":"The identity membership this case concerns (`identity.customer_membership`); member case notes are cases with this set. Must belong to `subjectId` when both are given (422). (decided 29 September, coordinator decision DM4, writers pass)"},"priority":{"allOf":[{"$ref":"#/components/schemas/CasePriority"}],"default":"normal"},"kind":{"$ref":"#/components/schemas/CaseKind"},"channel":{"$ref":"#/components/schemas/MessageChannel"},"venueId":{"type":"string","format":"uuid"},"relatedOrderId":{"type":"string"},"attachmentRefs":{"type":"array","description":"Stored on the opening `CaseMessage`, not on the case.","items":{"type":"string"}},"recordedAt":{"type":"string","format":"date-time","description":"Device time the case was raised. The server stamps `Case.syncedAt` on arrival."}}},
"CreateOrderLine": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","variantId","quantity","quotedUnitPrice"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these."},"variantId":{"type":"string","format":"uuid"},"recommendationId":{"type":"string","format":"uuid","nullable":true,"description":"The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Carried from the cart line at checkout; stored on `orders.order_line` and sent in `order.completed` lines.\n"},"performanceId":{"type":"string","format":"uuid"},"bookedWindow":{"$ref":"#/components/schemas/BookedWindow"},"inventoryHoldId":{"type":"string","nullable":true,"description":"Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products."},"seatIds":{"type":"array","maxItems":50,"items":{"type":"string","format":"uuid"},"description":"Seated products only, as `seating.Seat.id`. Not available offline. **At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel** (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); **at most 10 per sale on staff and POS** (audit R080 (c)), across all the lines of one order for one performance. `createOrder` refuses more with 422 `seatLimitExceeded` (problem type `seat-limit-exceeded`)."},"resourceHoldId":{"type":"string","format":"uuid","nullable":true,"description":"A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. `createOrder` converts the hold into a `ResourceBooking` without releasing it. Not available offline."},"attributes":{"$ref":"#/components/schemas/OrderLineAttributes"},"quantity":{"type":"integer","minimum":1},"eligibilityDeclaration":{"type":"array","nullable":true,"x-ticvai-note":"One row per declared guest in `orders.order_line_eligibility` (named on `OrderLine`), because an array of objects is a child table's rows, not a column.\n","items":{"type":"object","properties":{"ageBand":{"type":"string","enum":["infant","child","junior","adult","senior"],"description":"Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+."},"ageYears":{"type":"integer","nullable":true},"heightBandIndex":{"type":"integer","nullable":true},"confidentSwimmer":{"type":"boolean","nullable":true,"description":"**Derived, kept for the gate check** (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this is filled from it (true for a `yes` covering this person, whether answered for them or once for the booking). A value sent that contradicts the record is ignored and the record wins. No longer the place a swim answer is captured.\n"},"guardianSigned":{"type":"boolean"}}},"description":"What was declared for each guest on this line, kept as the record staff check at the gate."},"quotedUnitPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the client charged, from its local bundle."},"holderName":{"type":"string","nullable":true},"dataMaskValues":{"type":"object","additionalProperties":true,"description":"**Deliberately open.** Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the venue's to define, as on `catalogue`'s own `dataMaskValues`.\n"}}},
"CreateOrderRequest": {"type":"object","required":["id","venueId","channel","lines","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7. Also the idempotency key: it must equal the `Idempotency-Key` header, and a replay or a mismatch follows `IdempotencyKey` in `shared/common.yaml`. Offline replay through `syncOrders` carries no header, and this id alone deduplicates there.\n"},"venueId":{"type":"string","format":"uuid"},"channel":{"$ref":"#/components/schemas/Channel"},"shiftId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"Null for an anonymous sale. Identity and entitlement are separate."},"guestLinkId":{"type":"string","nullable":true,"description":"Present where the guest is linked across cells."},"catalogueBundleVersion":{"type":"string","description":"The bundle the client priced from. Lets the server explain a variance rather than merely report one.\n"},"lines":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/CreateOrderLine"}},"recordedAt":{"type":"string","format":"date-time"}}},
"CreateQueueRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["code","name","venueId","capacityPerCycle","cycleMinutes"],"properties":{"code":{"type":"string","maxLength":64},"name":{"$ref":"#/components/schemas/LocalisedText"},"venueId":{"type":"string","format":"uuid"},"attractionProductId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true,"description":"The ride. Taking it out of service closes this queue rather than leaving guests holding positions for something that is not running.\n"},"accessPointId":{"type":"string","format":"uuid","nullable":true},"kind":{"type":"string","enum":["standby","singleRider","fastPass","virtual","accessible","groupOnly","staffOnly"],"default":"standby","description":"5.6.x. **A ride has several queues and the model had one.** A single-rider line and a standby line at the same attraction draw from one capacity and fill at different rates, and modelling them as one queue makes both wait estimates wrong.\n**`accessible` is not a courtesy lane.** It has its own capacity because a guest who cannot stand in a switchback needs a place to wait, not priority.\n"},"operatingWindows":{"type":"array","description":"**When the queue runs, which is not when the venue is open.** A ride closing an hour early for maintenance leaves a queue accepting guests for a cycle that will not happen.\nStored one row per window in `queue.queue_operating_window` (see `Queue`), not as a column on the queue.\n","items":{"type":"object","required":["day","from","to"],"properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"Venue local time, 24-hour `HH:MM`, when the queue starts running."},"to":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"Venue local time, 24-hour `HH:MM`, when the queue stops running."},"lastEntryMinutesBefore":{"type":"integer","default":0,"description":"**When the queue stops accepting, which is before it stops running.** A guest joining two minutes before close waits twenty and is turned away at the front.\n"}}}},"parentQueueId":{"type":"string","format":"uuid","nullable":true,"description":"Where several queues share one capacity. **The standby and single-rider lines at one ride draw from the same cycles**, and a parent is how that is expressed without either queue owning the other.\n"},"loadBalanceWithQueueIds":{"type":"array","description":"BL-137. **Two rides with the same theme and different waits**, and nothing directed a guest to the shorter one. Load balancing is an offer, not an assignment — **a guest sent to a ride they did not choose is a guest who feels managed.**\n","items":{"type":"string","format":"uuid"}},"inQueueOfferEnabled":{"type":"boolean","default":false,"description":"**A guest with twenty minutes to wait is a guest with twenty minutes to buy something.** Offers surface in the wait screen and are the only reason a virtual queue earns its infrastructure.\n"},"notifyBeforeCallMinutes":{"type":"integer","default":5,"description":"BL-017, 19.2.61. **A guest was not told their turn was approaching**, which makes a virtual queue worse than a physical one — at least a line is visible.\n"},"capacityPerCycle":{"type":"integer","minimum":1},"cycleMinutes":{"type":"number","minimum":0},"maxPartySize":{"type":"integer","default":6},"returnWindowMinutes":{"type":"integer","default":15,"description":"How long a called party has to arrive before the entry expires."},"heightRequirementCm":{"type":"integer","nullable":true},"fastPassAllocationPercent":{"type":"number","minimum":0,"maximum":100,"default":0,"description":"Share of each cycle reserved for Fast Pass holders."},"zone":{"type":"string","nullable":true},"fastPass":{"allOf":[{"$ref":"#/components/schemas/QueueFastPass"}],"nullable":true,"description":"The lane's Fast Pass block (decided 29 September, VM close-out). Null on a queue that takes no Fast Pass.\n"}}},
"CreateRefundRequest": {"type":"object","required":["id","amount","reason","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of the refund, and its idempotency key — it must equal the `Idempotency-Key` header."},"lineIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Omit to refund the whole order."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"reason":{"type":"string","minLength":3,"maxLength":500},"secondaryAuthorisation":{"type":"object","description":"Required above the venue's `requiresSecondUserAbove`. A second user — cashier or supervisor — names themselves. This is dual-authorisation, not escalation.\n","required":["principalId","credential"],"properties":{"principalId":{"type":"string","format":"uuid"},"credential":{"type":"string","maxLength":512,"description":"The second person's staff PIN, as they sign in at a till with it. **A PIN, never a password** (decided 28 September, audit R123 (7))."}}},"refundToOriginalTender":{"type":"boolean","default":true},"alternateTender":{"$ref":"#/components/schemas/TenderKind"},"recordedAt":{"type":"string","format":"date-time"}}},
"ExchangeOrderRequest": {"type":"object","required":["id","outgoingLineIds","incomingLines","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of this exchange, and its idempotency key — it must equal the `Idempotency-Key` header."},"outgoingLineIds":{"type":"array","minItems":1,"items":{"type":"string","format":"uuid"}},"incomingLines":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/CreateOrderLine"}},"waiveFee":{"type":"boolean","default":false},"reason":{"type":"string","maxLength":500},"recordedAt":{"type":"string","format":"date-time"}}},
"ExchangeRateDecimal": {"type":"string","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,6)","description":"**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one — a JavaScript client must not round a rate in transit. **Six decimal places**, the precision `finance.FxRate.rate` asks for, and stored at that precision.\n","pattern":"^\\d+(\\.\\d{1,6})?$"},
"GuestListing": {"type":"string","enum":["bookable","infoOnly","hidden"],"default":"bookable","description":"**How a product appears to a guest** (decided 29 September, rev 3 REV3-14). `bookable`: listed and searched while it is on sale, and added to the basket. `infoOnly`: listed and searched with its details, photo and `notBookableLabel` whether or not it is on sale, and **never added to a basket** (`addCartLine` refuses it with `409`); the screen opens its details instead. `hidden`: never listed or searched for a guest, and reachable only where a staff channel sells it. Independent of `isSellable`, which says whether a channel may sell it at all.\n"},
"GuestProfile": {"x-ticvai-persistence":"marketing.guest_profile","type":"object","required":["subjectId","isActive"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"subjectId":{"type":"string","format":"uuid","description":"Opaque reference. Personal data lives in the separately erasable store, which is what makes erasure possible against an append-only ledger.\n"},"displayName":{"type":"string","nullable":true},"email":{"type":"string","nullable":true},"phone":{"type":"string","nullable":true},"preferredLanguage":{"type":"string","nullable":true},"preferredChannel":{"$ref":"#/components/schemas/MessageChannel"},"guestLinkId":{"type":"string","nullable":true,"description":"Present where the guest is linked across cells. Marketing acts locally."},"tags":{"type":"array","items":{"type":"string"}},"engagementScore":{"type":"integer","nullable":true,"minimum":0,"maximum":100,"description":"22.2.20 and 22.2.21. **`lifetimeValue` and `visitCount` existed, so value was a stored figure and engagement was not.** They are different questions: a guest who spent a lot once and a guest who visits monthly have the same LTV and need opposite treatment.\n**Recency, frequency and breadth, not spend** — spend is already `lifetimeValue`, and folding it in here would make one number twice.\n"},"engagementTier":{"type":"string","nullable":true,"enum":["new","active","occasional","lapsing","lapsed","dormant"],"description":"5.3.19. **Automatic classification, computed rather than assigned.** `lapsing` is the tier the whole field exists for — **a guest who has not been for a while and still might is the only one marketing can change**, and lumping them with `lapsed` wastes the window.\n"},"lifetimeValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"visitCount":{"type":"integer"},"lastVisitAt":{"type":"string","format":"date-time","nullable":true},"isActive":{"type":"boolean"},"mergedIntoSubjectId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Set on the absorbed profile by `mergeGuestProfiles` and `mergeGuests`**, which retain it as a redirect rather than deleting it. A read that lands here follows it; a second merge of a profile that has one is refused as `alreadyMerged`.\n"},"mergedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"Incident": {"x-ticvai-persistence":"maintenance.incident","type":"object","required":["id","incidentNumber","kind","severity","status","venueId","occurredAt","reportedByPrincipalId"],"properties":{"id":{"type":"string","format":"uuid"},"incidentNumber":{"type":"string","readOnly":true,"description":"**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity.\n"},"kind":{"$ref":"#/components/schemas/IncidentKind"},"severity":{"$ref":"#/components/schemas/IncidentSeverity"},"status":{"$ref":"#/components/schemas/IncidentStatus"},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true},"locationDescription":{"type":"string","nullable":true},"isReportable":{"type":"boolean","description":"Requires notification to an external authority within a statutory window."},"notificationDueAt":{"type":"string","format":"date-time","nullable":true},"notifiedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"The earliest `notifiedAt` among this incident's authority notifications. **Maintained on write** by `recordAuthorityNotification`; each notification itself is a row of `maintenance.incident_authority_notification`.\n"},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true},"reportedByPrincipalId":{"type":"string","format":"uuid"},"correctiveWorkOrderId":{"type":"string","format":"uuid","nullable":true},"escalation":{"type":"object","nullable":true,"readOnly":true,"description":"**Set while the incident is escalated** (the optional Escalated step of the 3 October flow; CHG-RUL-011). Screens show \"Escalated\" when `status` is `underInvestigation` and this is set. Cleared when the incident closes.\n","properties":{"toPrincipalId":{"type":"string","format":"uuid"},"byPrincipalId":{"type":"string","format":"uuid"},"reason":{"type":"string"},"escalatedAt":{"type":"string","format":"date-time"}}},"reopenCount":{"type":"integer","minimum":0,"readOnly":true,"description":"How many times the incident was reopened (CHG-RUL-011). Each reopen is a logged row."},"occurredAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"closedAt":{"type":"string","format":"date-time","nullable":true},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"IncidentAuthorityNotification": {"x-ticvai-persistence":"maintenance.incident_authority_notification","type":"object","description":"**One notification to an external authority, appended by `recordAuthorityNotification`.** An incident may be reported to more than one authority, or to the same one twice, and each is the evidence that an obligation was met — so each is a row, not an overwrite of `maintenance.incident.notified_at`.\n","required":["id","incidentId","authority","notifiedAt"],"properties":{"id":{"type":"string","format":"uuid"},"incidentId":{"type":"string","format":"uuid"},"authority":{"type":"string","maxLength":200},"reference":{"type":"string","maxLength":128,"nullable":true},"notifiedAt":{"type":"string","format":"date-time"},"notifiedByPrincipalId":{"type":"string","format":"uuid"},"attachmentRefs":{"type":"array","items":{"type":"string"}},"recordedAt":{"type":"string","format":"date-time"}}},
"IncidentDetail": {"x-ticvai-persistence":"maintenance.incident","allOf":[{"$ref":"#/components/schemas/Incident"},{"type":"object","properties":{"description":{"type":"string","description":"The original report. Never edited — investigation adds to the record."},"investigationNote":{"type":"string","nullable":true,"readOnly":true,"description":"The latest entry of `investigationNotes`, kept for readers that show one line."},"investigationNotes":{"type":"array","readOnly":true,"description":"**Every investigation note, oldest first** (decided 28 September, audit R106 (5)). Read from `maintenance.incident_investigation_note`; appended by `updateIncident`.\n","items":{"$ref":"#/components/schemas/IncidentInvestigationNote"}},"rootCause":{"type":"string","nullable":true},"correctiveActions":{"type":"string","nullable":true},"firstAidGiven":{"type":"boolean"},"emergencyServicesCalled":{"type":"boolean"},"witnessCount":{"type":"integer"},"attachmentRefs":{"type":"array","items":{"type":"string"}},"involvedParties":{"type":"array","description":"Who was involved, as given in `ReportIncidentRequest.involvedSubjectIds` and `involvedStaffPrincipalIds`. Read from `maintenance.incident_involved_party`.\n","items":{"$ref":"#/components/schemas/IncidentInvolvedParty"}},"authorityNotifications":{"type":"array","description":"Read from `maintenance.incident_authority_notification`, oldest first.","items":{"$ref":"#/components/schemas/IncidentAuthorityNotification"}}}}]},
"IncidentInvestigationNote": {"x-ticvai-persistence":"maintenance.incident_investigation_note","type":"object","description":"**One investigation note, appended by `updateIncident`** (decided 28 September, audit R106 (5)). A history rather than a field, so what an investigator thought on Tuesday survives what they found on Thursday.\n","required":["id","incidentId","note","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"incidentId":{"type":"string","format":"uuid"},"note":{"type":"string","maxLength":10000},"kind":{"type":"string","enum":["note","statusChange","escalation","reopen"],"default":"note","description":"**Every change is logged here** (CHG-RUL-011): an investigator's note, or a row the server writes for a status change, an escalation or a reopen, with `note` as its reason.\n"},"fromStatus":{"allOf":[{"$ref":"#/components/schemas/IncidentStatus"}],"nullable":true},"toStatus":{"allOf":[{"$ref":"#/components/schemas/IncidentStatus"}],"nullable":true},"writtenByPrincipalId":{"type":"string","format":"uuid"},"recordedAt":{"type":"string","format":"date-time"}}},
"IncidentInvolvedParty": {"x-ticvai-persistence":"maintenance.incident_involved_party","type":"object","description":"**One person involved in an incident, by opaque reference.** A guest or member of the public is a `pii.subject` id — personal details live there, the erasable store of ADR-0023, so the incident record survives an erasure request intact. A member of staff is a principal id. Exactly one of the two is set, as `kind` says.\n","required":["id","incidentId","kind"],"properties":{"id":{"type":"string","format":"uuid"},"incidentId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["subject","staff"]},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"A `pii.subject` id where `kind` is `subject`."},"principalId":{"type":"string","format":"uuid","nullable":true,"description":"The staff principal where `kind` is `staff`."},"role":{"type":"string","nullable":true,"enum":["injured","involved","witness","reporter",null],"description":"The person's part in the incident, from `addIncidentPerson` (CHG-RUL-013)."},"contactStored":{"type":"boolean","readOnly":true,"description":"Whether a contact is held for the person: only with their consent to be contacted (`AddIncidentPersonRequest.contactConsent`; CHG-RUL-013).\n"}}},
"IncidentKind": {"type":"string","enum":["guestInjury","staffInjury","nearMiss","propertyDamage","equipmentFailure","securityIncident","fireOrEvacuation","foodSafety","environmental","other"]},
"IncidentMedia": {"x-ticvai-persistence":"maintenance.incident_media","type":"object","description":"**One photo, video or document on an incident** (`uploadIncidentMedia`; CHG-RUL-013). The file is in the media store; this row links it to the incident.\n","required":["id","incidentId","kind","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"incidentId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["photo","video","document"]},"status":{"type":"string","enum":["awaitingUpload","stored"],"readOnly":true,"description":"`stored` once the media store confirmed the transfer and `assetRef` is set."},"assetRef":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"assets.media_asset"},"caption":{"type":"string","nullable":true},"capturedAt":{"type":"string","format":"date-time","nullable":true},"uploadedByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"upload":{"type":"object","readOnly":true,"x-ticvai-persisted":false,"description":"The signed upload, as `assets.createUpload` returns it; only on the 201.","properties":{"uploadUrl":{"type":"string"},"method":{"type":"string","enum":["PUT","POST"]},"headers":{"type":"object","additionalProperties":{"type":"string"}},"expiresAt":{"type":"string","format":"date-time"}}}}},
"IncidentSeverity": {"type":"string","enum":["nearMiss","minor","moderate","major","critical"]},
"IncidentStatus": {"type":"string","enum":["reported","underInvestigation","actionRequired","closed"]},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"ManualDiscountRequest": {"type":"object","x-ticvai-persistence":"none — request only","required":["id","reason","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of this discount, and its idempotency key — it must equal the `Idempotency-Key` header."},"lineId":{"type":"string","format":"uuid","nullable":true,"description":"Omit to discount the order rather than a line."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"percentage":{"type":"number","minimum":0,"maximum":100},"reason":{"type":"string","minLength":3,"maxLength":300,"description":"Required, and free text rather than a code list. A cashier forced to pick the nearest reason picks the first one, and the register stops meaning anything.\n"},"reasonCode":{"type":"string","nullable":true,"description":"Optional alongside the free text, where the venue maintains a list."},"approverPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Required above the venue threshold. May not be the requester."},"recordedAt":{"type":"string","format":"date-time"}}},
"MessageChannel": {"type":"string","enum":["email","sms","whatsapp","push","inApp","post"]},
"ModifyOrderRequest": {"type":"object","required":["id","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 **of this modification, not of the order** — the order is the path's `orderId`. It is the modification's idempotency key and must equal the `Idempotency-Key` header.\n"},"addLines":{"type":"array","items":{"$ref":"#/components/schemas/CreateOrderLine"}},"removeLineIds":{"type":"array","items":{"type":"string","format":"uuid"}},"reason":{"type":"string","maxLength":500},"recordedAt":{"type":"string","format":"date-time"}}},
"Order": {"x-ticvai-persistence":"orders.sales_order + orders.order_line","type":"object","required":["id","venueId","scopePath","channel","status","currency","currencyScale","grossAmount","taxAmount","netAmount","lines","createdAt","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The client UUIDv7 from `CreateOrderRequest.id`."},"orderNumber":{"type":"string","readOnly":true,"description":"The number a guest reads and a cashier types. **Server-assigned: the venue prefix and a sequence per venue**, for example `DXB1-000123` (decided 28 September, audit R152). A till holds a reserved range of the venue sequence, so an order taken offline gets its number on the till and keeps it through `syncOrders`. **Not gapless**: an unused reserved range leaves a gap, and that is allowed. Only tax invoices are gapless, per legal entity. The receipt carries this number.\n"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for within a month of launch.\n"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"chargeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**The currency the guest selected and is charged in** (CHG-FIN-001, 2 October 2026). Null or equal to `currency` for a sale in the base currency. Everything else on the order, and every ledger posting, stays in the base currency `currency`."},"chargeFxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"readOnly":true,"description":"Units of `chargeCurrency` per one unit of the base currency, from the region's `tender` rate in force at checkout (`finance.FxRate`), stored on the order so the payment, the receipt, the tax invoice and any refund use the same rate (CHG-FIN-001)."},"chargeFxRateId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `finance.FxRate` row the rate was taken from, for audit."},"chargeTotal":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"`grossAmount` converted at `chargeFxRate` and rounded to the charge currency's scale: what the guest pays and what the payment request to the provider asks for (CHG-FIN-001)."},"chargeRateLockedUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"The quote holds until then (the cart lease). After it, the next payment attempt re-quotes at the rate then in force and the guest confirms the new amount (CHG-FIN-001)."},"droppedPromotions":{"type":"array","readOnly":true,"x-ticvai-persisted":false,"description":"**Promotions left off this order at checkout because their budget cap would have been exceeded** (decided 28 September, audit R101 (8)). Empty when none was dropped. Returned by `checkoutCart` and `createOrder`, not stored.\n","items":{"type":"object","required":["promotionId"],"properties":{"promotionId":{"type":"string","format":"uuid"},"name":{"type":"string"},"reason":{"type":"string","enum":["budgetCapReached"]}}}},"totalPriceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Sum across lines. Zero on a normal order."},"lines":{"type":"array","items":{"$ref":"#/components/schemas/OrderLine"}},"payments":{"type":"array","items":{"$ref":"#/components/schemas/Payment"}},"principalId":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid"},"shiftId":{"type":"string","format":"uuid","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"holdLabel":{"type":"string","maxLength":60,"nullable":true,"readOnly":true,"description":"The `label` a cashier gave when parking it with `holdOrder` — how they find it again. Null on an order never held."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When a held order expires and is voided (states/order.yaml), from `holdOrder`'s `holdUntil`. Null on an order not currently held."},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"OrderChannel": {"type":"string","description":"Where the order originated. Added when guest self-ordering was contracted — an order a guest placed on their own phone is commercially and operationally different from one a cashier typed, and reporting that cannot separate them cannot answer whether self-ordering is working.\n","enum":["pos","kiosk","guestApp","guestWeb","callCentre","partner","api","backOffice"]},
"OrderExchangeResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["orderId","outgoingValue","incomingValue","difference"],"properties":{"orderId":{"type":"string","format":"uuid"},"outgoingValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"incomingValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"exchangeFee":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"difference":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Only the difference settles. The replacement is held before the original is released, never the other way round.\n"},"newLineIds":{"type":"array","items":{"type":"string","format":"uuid"}},"revokedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}},"issuedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"OrderLine": {"x-ticvai-persistence":"orders.order_line + orders.order_line_eligibility + orders.order_line_discount","x-ticvai-retired-columns":["promotion_id","name","reason"],"allOf":[{"$ref":"#/components/schemas/CreateOrderLine"},{"type":"object","required":["serverUnitPrice","taxAmount","netAmount","grossAmount"],"properties":{"serverUnitPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the server computed on ingest."},"priceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Server minus quoted. Non-zero means the quoted price was honoured and the difference posted to the variance account.\n"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"entitlementIds":{"type":"array","description":"The entitlements this line issued. **These are the ticket ids** — `transferOrderTickets.ticketIds` and `reprintOrder.reissuedTicketIds` take and return them.","items":{"type":"string","format":"uuid"}},"crossRegionRightIds":{"type":"array","items":{"type":"string"},"description":"Redemption rights propagated to other cells for this line."},"reprintCount":{"type":"integer","minimum":0,"default":0,"readOnly":true,"description":"How many times this line's tickets were reprinted or resent. `reprintOrder` increments it; repeated reprints are the signal worth surfacing."},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"The order's venue, copied onto the line (ADR-0044's own example; system-design review SD-008, 29 September) so a line is scoped and partitionable without its order."},"discounts":{"type":"array","readOnly":true,"description":"**The discounts applied to this line, one row each** (system-design review SD-008, 29 September). Until then a discount object was flattened into the line as `promotion_id NOT NULL`, so a line with no promotion could not be inserted. A line with no discount has none.","items":{"$ref":"#/components/schemas/OrderLineDiscount"}}}}]},
"OrderModificationResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["order","balanceDue"],"properties":{"order":{"$ref":"#/components/schemas/Order"},"addedValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"removedValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"balanceDue":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Positive means the guest pays; negative means a refund is due."},"refundId":{"type":"string","format":"uuid","nullable":true},"revokedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}},"issuedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"OrderResumeResult": {"type":"object","x-ticvai-persistence":"none — computed","required":["order","hasChanged"],"properties":{"order":{"$ref":"#/components/schemas/Order"},"hasChanged":{"type":"boolean","description":"True where anything moved while the sale was parked. The cashier decides — silently charging the old price loses money, silently charging the new one loses the guest.\n"},"changes":{"type":"array","items":{"type":"object","properties":{"kind":{"type":"string","enum":["priceChanged","promotionExpired","promotionNowApplies","soldOut","seatHoldExpired","productWithdrawn"]},"lineId":{"type":"string","format":"uuid"},"detail":{"type":"string"},"wasAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"nowAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}}}},
"OrderStatement": {"x-ticvai-persistence":"none — computed from order, payment, refund and ledger","type":"object","required":["orderId","orderNumber","currency","entries","currentBalance"],"properties":{"orderId":{"type":"string","format":"uuid"},"orderNumber":{"type":"string"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"entries":{"type":"array","description":"Sequential. What an agent reads to a guest asking about a charge.","items":{"type":"object","required":["kind","amount","runningBalance","occurredAt"],"properties":{"kind":{"type":"string","enum":["sale","payment","refund","void","modification","exchange","fee","variance","chargeback"]},"description":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"runningBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"referenceId":{"type":"string","nullable":true},"principalId":{"type":"string","format":"uuid","nullable":true},"occurredAt":{"type":"string","format":"date-time"}}}},"totalPaid":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"totalRefunded":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"currentBalance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Positive means the guest owes; negative means a refund is outstanding."}}},
"OrderStatus": {"type":"string","enum":["pending","held","paid","partiallyPaid","completed","voided","refunded","partiallyRefunded","failed"],"description":"`held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed.\n"},
"OrderSummary": {"x-ticvai-persistence":"none — projection","type":"object","required":["id","orderNumber","status","grossAmount","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderNumber":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"The same vocabulary as `Order.channel`, which this projects."},"lineCount":{"type":"integer"},"principalId":{"type":"string","format":"uuid","description":"The cashier who raised it — what the held-orders list shows."},"holdLabel":{"type":"string","nullable":true,"description":"As `Order.holdLabel`."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"description":"As `Order.heldUntil`, so a held-orders list can warn about the ones about to lapse."},"createdAt":{"type":"string","format":"date-time"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Payment": {"x-ticvai-persistence":"orders.payment","type":"object","required":["id","orderId","tender","amount","status","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid"},"tender":{"$ref":"#/components/schemas/TenderKind"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","description":"4.6.11. **What the guest actually handed over**, which is not always what the venue books. A tourist paying USD cash at a till is a foreign tender; the sale is still recorded in base currency.\nEqual to the base currency for almost every payment. **Present on all of them so the foreign-tender report has a source** — `getForeignTenderReport` promised *what was taken in which currency* and nothing recorded it until 18 August.\n"},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"The amount in `tenderCurrency`, at that currency's own scale."},"fxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"description":"The rate applied, **stored on the payment rather than looked up later** (CF-37). A payment reconciled next month is reconciled at the rate of the day it was taken.\n"},"fxRateSource":{"type":"string","nullable":true,"enum":["manual","feed","cardScheme"],"description":"4.2.8. Manual or fed on a schedule. **`cardScheme` is where the terminal did the conversion and told us** — dynamic currency conversion, the scheme's rate rather than ours.\n"},"changeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"description":"4.6.11 is deliberately asymmetric: **accept foreign currency, refund in local.** A till giving change in five currencies needs five floats and five counts, and the variance becomes unattributable.\n**Cash at a till only** (CHG-FIN-001, 2 October 2026). A card or wallet payment the guest made in a currency they selected is refunded in that currency (`Refund.tenderCurrency`).\n"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"changeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["authorised","captured","pendingConfirmation","declined","failed","voided","refunded"]},"providerName":{"type":"string","nullable":true},"providerReference":{"type":"string","nullable":true,"description":"The provider's own id for the charge (Stripe PaymentIntent, NI order reference). What `payments.receivePaymentProviderWebhook` matches an incoming event on (SD-034)."},"providerIdempotencyKey":{"type":"string","nullable":true,"readOnly":true,"description":"The idempotency key sent to the provider, which is this payment's `id` (SD-034, 29 September). A retried provider call cannot charge twice."},"terminalId":{"type":"string","format":"uuid","nullable":true,"description":"The card terminal a till payment ran on (ECR flow, SD-034)."},"nextAction":{"type":"object","nullable":true,"x-ticvai-persisted":false,"description":"**What the caller does while the payment is `pendingConfirmation`** (SD-034, 29 September). `redirect`: send the browser to `url` (3-D Secure challenge or hosted page); the provider returns the guest to `returnUrl` and the result arrives by webhook. `terminal`: the card terminal has been instructed; wait for its result. Null once the payment has an outcome.","properties":{"kind":{"type":"string","enum":["redirect","terminal"]},"url":{"type":"string","format":"uri","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true}}},"lastInquiryAt":{"type":"string","format":"date-time","nullable":true},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"PlacedResource": {"type":"object","x-ticvai-persistence":"venuemap.placed_resource","description":"**A bookable resource where it stands on the map** (decided 29 September, rev 3 REV3-15 and GAP-C2): cabana B09 on the Beach, 15 guests, Large. The resource itself, its bookings and its holds live in `resources`; this row says where it is drawn and what the guest sees. Written into the working draft by `importVenueGeometry` or `setPlacedResource`, copied into the `VenueMapVersion` snapshot at publish. A guest picks one on the published map, holds it with `resources.createResourceHold` and buys it. **Supersedes audit R073 (c) and the 26 August minute for resources on an ingested map.**\n","required":["id","mapId","resourceId","label","kind","zone","capacity","priceBandCode","position"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"mapId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of the operation that writes it."},"resourceId":{"type":"string","format":"uuid","x-ticvai-references":"resources.Resource","description":"The `resources.Resource` this is. **Availability, holds and bookings are keyed by this**, so a republished map with the cabana moved keeps its bookings.\n"},"label":{"type":"string","maxLength":40,"x-ticvai-unique":"map","description":"What the guest sees and taps, e.g. `B09`. **Unique on the map**, compared without case after digit normalisation; normally the resource's `code`.\n"},"kind":{"type":"string","enum":["cabana","lounger","table","pitch","other"],"description":"A subset of `resources.ResourceKind`, the kinds a guest books from a map. A `table` here is a non-dining spot (a beach or event table) sold like a cabana; restaurant tables stay `fnb` table reservations (decided 29 September, rev 3 GAP-C2)."},"zone":{"type":"string","maxLength":80,"description":"The area the guest reads it by, e.g. `Beach`, `River`, `Terrace`."},"capacity":{"type":"integer","minimum":1,"maximum":500,"description":"Guests it takes, e.g. 15. Shown on the map and checked against the party at hold."},"priceBandCode":{"type":"string","maxLength":40,"description":"The band it sells in, e.g. `Large`, one of the `priceBands` given at import. The band's `variantId` prices it; the map holds no price.\n"},"variantId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"catalogue.ProductVariant","description":"Resolved from the price band. What a cart line for this resource names."},"position":{"type":"object","required":["x","y"],"description":"Drawing coordinates of its label anchor, as on `VenuePoint`.","properties":{"x":{"type":"number"},"y":{"type":"number"}}},"boundary":{"type":"array","nullable":true,"description":"The shape drawn, as a polygon in drawing coordinates. Null for a pin.","items":{"type":"object","properties":{"x":{"type":"number"},"y":{"type":"number"}}}},"isBookable":{"type":"boolean","default":true,"description":"False keeps it on the map and off sale, e.g. a cabana kept for staff use. Shown greyed.\n"}}},
"Product": {"x-ticvai-persistence":"catalogue.product","type":"object","required":["id","code","name","kind","venueId","scopePath","isSellable","hasVariants"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"familyKey":{"type":"string","maxLength":64,"pattern":"^[A-Za-z0-9_-]+$","nullable":true,"x-ticvai-unique":"venue","description":"**The same product at another location** (decided 29 September, rev 3 REV3-18). Optional. A tenant that sells one attraction at several venues gives each venue's product the same key, e.g. `aquarium-entry`; the key names the family across the tenant and each venue has at most one product in it, so a second product at the same venue with the key is refused with `409 duplicate-code`. **What it is for:** when a guest changes location on the booking screen (the 'Booking at' switcher, `BookingFlowConfig.locationSwitcher`), lines whose product shares a `familyKey` with a product at the new venue are carried over to that product, with times and prices refreshed; every other line is cleared. Null means the product belongs to no family and its lines always clear on a switch. Compared case-insensitively, like `code`.\n"},"name":{"type":"string","maxLength":200},"description":{"type":"string"},"kind":{"$ref":"#/components/schemas/ProductKind"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"createdByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"1.4.18. **The approval gate refuses an approver who is the author, and nothing recorded either.** `SeatBlock`, `DelegatedAccess` and `ManualDiscountRequest` all carry this and the product passing through approval did not.\n"},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"responsibleDepartmentId":{"type":"string","format":"uuid","nullable":true,"description":"Who owns this product commercially. A scope node at `department` level."},"onSaleFrom":{"type":"string","format":"date-time","nullable":true,"description":"1.4.8. **A seasonal product should not need somebody awake at midnight.** Archiving already runs on a timer in this contract, so the machinery exists; `effectiveFrom` appears on tax codes, FX rates and white-label policies and not here.\n"},"onSaleTo":{"type":"string","format":"date-time","nullable":true,"description":"Retires the product automatically. **Retirement is not deletion** — the product stops selling and every order that referenced it still resolves.\n"},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"**Taken from their `fnb.product` and `retail.product`, 20 September.** `catalogue.product_category` has existed since 20 August with two operations and nothing could be filed under it — a merchandise hierarchy with a tree and no leaves. Their per-domain product tables both carried this column and ours did not.\n"},"lifecycleState":{"$ref":"#/components/schemas/ProductLifecycleState"},"isSellable":{"type":"boolean","readOnly":true,"description":"True only when live **and** carried by a published bundle. Approval and publication are different acts.\n**Derived, never set.** It changes when `transitionProductLifecycle` moves the product and when `publishBundle` carries it, so `updateProduct` does not take it — `withdraw` is how a product stops selling.\n"},"isStockTracked":{"type":"boolean","default":false,"description":"**Taken from their `fnb.product`, 20 September.** Whether a sale decrements stock, which is not what `isSellable` asks. A ticket is sellable and tracks no stock; a bottle of water is both. Without it, an F&B sale cannot tell inventory whether to move.\n"},"hasVariants":{"type":"boolean"},"variantCount":{"type":"integer"},"segmentTags":{"type":"array","description":"7.3.5. **A channel and a segment tag are mandatory and nothing required either.** A catalogue that cannot be filtered by segment is a catalogue nobody can report on.\n**Hierarchical, not flat** — `family/with-toddlers` narrows `family` without duplicating it, which is how the promotions engine already treats scope.\n**A level is a tag under `level/`** (decided 29 September, rev 3 REV3-19): `level/beginner`, `level/intermediate`, `level/advanced`, `level/expert` (proposed codes, client to correct). A guest screen filters on it with `listProducts` `segmentTag`, and the words a guest reads beside each option come from `ProductCategory.description`, not from the tag.\n","items":{"type":"string"}},"codeSchema":{"type":"string","readOnly":true,"description":"7.3.4 specifies `[ParkCode]-[ProductType]-[Variant]`. **`Product.code` existed and nothing required a format**, so a venue with three thousand products had three thousand conventions.\nThe tenant sets the pattern and the platform generates against it. **Validation is the point, not the string** — a code typed by hand is a code that will not sort.\n"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/Channel"}},"entitlementTemplateId":{"type":"string","format":"uuid","nullable":true,"description":"What the buyer receives. Null for products that grant nothing — F&B and retail. Identity and entitlement are separate concerns.\n"},"blockedOffline":{"type":"boolean","description":"True for seated and retail. Seated because a seat map is not a count; retail because stock depletes in real time.\n"},"dataMaskValues":{"type":"object","additionalProperties":true,"description":"Custom fields. JSONB-backed, defined by the venue's data mask."},"guestListing":{"$ref":"#/components/schemas/GuestListing"},"notBookableLabel":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"The label a guest reads on an `infoOnly` product, e.g. *Info only* or *Not bookable online; ask at the desk* (decided 29 September, rev 3 REV3-14). Each value at most 60 characters. Null means the guest screen shows its default wording. Ignored unless `guestListing` is `infoOnly`.\n"},"salesContact":{"allOf":[{"$ref":"#/components/schemas/ProductSalesContact"}],"nullable":true,"description":"**Who a guest contacts to book a view-only product** (decided 29 September, W3), e.g. a training course listed with full details and no Book button. Shown as *Call sales* and *Email sales* on an `infoOnly` product. Null means the venue's own contact (white-label `getTenantAppStatus.contact`). Ignored unless `guestListing` is `infoOnly`.\n"},"bookingFlowId":{"type":"string","format":"uuid","nullable":true,"description":"**The booking flow this product is sold through** (decided 29 September, W8 and W12): a white-label `BookingFlow` of the venue, which orders the guest's steps (for a workshop, the product first and then the date and time). Null means the category's flow (`ProductCategory.bookingFlowId`), and failing that the venue's flow for the product's `kind`. Written by `createProduct` and `updateProduct`, which refuse an id that is not a flow of the venue with `422`.\n"},"displayTags":{"type":"array","maxItems":6,"items":{"$ref":"#/components/schemas/ProductDisplayTag"},"description":"**Short facts a guest reads on the ticket card and under *Read more***: *2 Hours*, *Min 1.10 m*, *Free adult entry*, *Valid 90 days*, *Emirates ID* (decided 29 September, 23SEP-3). Not `segmentTags`, which are for reporting and segmentation and which a guest never reads.\n**Derived on read when none are set.** When the venue has written no tags, a read returns tags derived from the product's duration (`clock`), entitlement validity (`calendar`) and the eligibility rule's `minHeightCm` (`height`), each marked `derived: true`; they are never stored. Once the venue writes any tag, only what it wrote is returned. Whether the guest screen shows them is `BookingFlowConfig.ticketTags` (white-label).\n"},"media":{"type":"array","maxItems":20,"items":{"$ref":"#/components/schemas/ProductMedia"},"description":"**The product's own photos and video** (decided 29 September, 23SEP-4). *Read more* opens on the `isPrimary` item, and a listing shows each product's primary image, so two tickets in one category no longer share the category's picture (`ProductCategory.imageAssetId`).\nEvery `assetId` names an asset of the asset library (`assets.yaml` `MediaAsset`) in status `ready` whose kind matches `kind`; anything else is a `422`. **Exactly one item is `isPrimary`** when the list is not empty, and an `assetId` appears once; otherwise `400`. Setting the list records each reference as asset usage (`MediaUsage` with `surface: product`, `referenceId` the product id, `isLive` true while the product is listed to guests), which is what stops a used asset being archived from under the product.\n"},"consentQuestionIds":{"type":"array","maxItems":10,"uniqueItems":true,"items":{"type":"string","format":"uuid"},"description":"**The consent questions a guest answers when booking this product**, in the order they are asked (decided 29 September, rev 3 REV3-26): *Are you able to swim?*, *Do you hold a scuba certification?*, *I accept the risk*. Each id names a consent question defined in marketing-crm (`ConsentQuestion`), which owns the text, its version and whether it is asked per person or once per booking; the answer is stored there as a consent record (question version, answer, who answered, when). **One question or several, as the venue chooses.** A flow can carry its own list too (`white-label.BookingFlow.settings.consentQuestionIds`, on the product's published booking flow as `getPublishedBookingFlow` resolves it: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig` 29 September, W12); a booking asks the union of the flow's questions and those of every product in the cart, each question once (`orders.Cart.consentQuestions`). An id that names no active consent question of the tenant is a `422`.\n"},"requiresTimeWindow":{"type":"boolean","default":false,"description":"**True for a space sold by the hour**, e.g. a meeting room type (decided 29 September, rev 3 REV3-13). The product is the room type (*focus pod*, *majlis*, *boardroom*, *auditorium*), never a named room; its lengths are a `length` axis (`setProductAttributes`) whose values carry `durationMinutes`, and each length is a variant priced on its own in the price list, so price is the room rate for that length. The cart line carries the booked start and end (orders), the end being the start plus the chosen variant's `durationMinutes`; `resources.listProductStartTimes` supplies the start times for a variant and a date and `allocateResources` picks the room from the product's resource requirements (`setExperienceResourceRequirements`) at checkout. True requires every active variant to have a `durationMinutes`; otherwise `422`.\n"},"productOwnerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The product owner (29 September, data model DM3), set with `setProductContextOwnership`. `responsibleDepartmentId` is the owning department."},"operationalContact":{"type":"string","maxLength":200,"nullable":true,"description":"A principal id or a name, as the context screen takes it."},"businessUnitId":{"type":"string","format":"uuid","nullable":true},"legalEntityId":{"type":"string","format":"uuid","nullable":true,"description":"A `ledger.legal_entity`, read through finance."},"attractionId":{"type":"string","format":"uuid","nullable":true},"siteId":{"type":"string","format":"uuid","nullable":true},"locationId":{"type":"string","format":"uuid","nullable":true},"brandId":{"type":"string","format":"uuid","nullable":true,"description":"The brand, as the context screen names it (a catalogue brand category)."},"marketCode":{"type":"string","maxLength":40,"nullable":true},"salesTerritory":{"type":"string","maxLength":100,"nullable":true}}},
"ProductDisplayTag": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","required":["kind","label"],"description":"One short fact on a ticket card (decided 29 September, 23SEP-3). `kind` picks the icon.","properties":{"kind":{"type":"string","enum":["clock","height","free","calendar","id"],"description":"`clock` a duration, `height` a height rule, `free` something included free, `calendar` a validity, `id` a document the guest must bring."},"label":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"What the guest reads, e.g. *2 Hours*. Each language value at most 40 characters."},"derived":{"type":"boolean","readOnly":true,"default":false,"description":"True on a tag the server derived on read because the venue set none. Never sent."}}},
"ProductKind": {"type":"string","description":"**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n","enum":["admission","timedAdmission","datedAdmission","openDated","seated","membership","bundle","fnb","retail","rental","addOn","giftCard"]},
"ProductLifecycleState": {"type":"string","enum":["draft","inReview","approved","live","withdrawn","archived"]},
"ProductMedia": {"x-ticvai-persistence":"catalogue.product_media","type":"object","required":["assetId","kind","isPrimary"],"description":"One photo or video of a product, referencing the asset library (decided 29 September, 23SEP-4). One row per product and asset, so the asset library can answer which products use an asset.\n","properties":{"assetId":{"type":"string","format":"uuid","description":"A `MediaAsset` of `assets.yaml`, in status `ready`."},"kind":{"type":"string","enum":["image","video"]},"isPrimary":{"type":"boolean","default":false,"description":"The item *Read more* opens on and a listing shows. Exactly one per product."},"displayOrder":{"type":"integer","default":100},"altText":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true}}},
"ProductSalesContact": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","description":"Who to contact to book a view-only product (decided 29 September, W3). At least one of `phone` or `email`.\n","minProperties":1,"properties":{"phone":{"type":"string","maxLength":32,"nullable":true},"email":{"type":"string","format":"email","maxLength":254,"nullable":true},"note":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"A line shown under the contact, e.g. *Group courses are booked by phone*. At most 200 characters per language."}}},
"ProductVariant": {"x-ticvai-persistence":"catalogue.variant","type":"object","required":["id","productId","sku","axisValues","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"productId":{"type":"string","format":"uuid"},"sku":{"type":"string"},"axisValues":{"type":"object","additionalProperties":{"type":"string"}},"name":{"type":"string","maxLength":150,"nullable":true,"description":"**Taken from their variant tables, 20 September.** `axisValues` gives `{size: L}` and no string a guest can read. A menu showing *Large* needs somewhere for the word to live.\n"},"barcode":{"type":"string","maxLength":64,"nullable":true,"description":"**Taken from their variant tables, 20 September.** `catalogue.alternative_code` is a partner's own code for a variant and **requires `partnerId`**, so a manufacturer's EAN had nowhere to go. One per variant against many per variant is a different cardinality and belongs in a different place — and a POS scan should be an indexed column lookup, not a join.\n"},"isDefault":{"type":"boolean","default":false,"description":"Taken from their variant tables. Which variant a product page opens on. Ours had no way to say, so a three-size drink opened on whichever row sorted first.\n"},"isActive":{"type":"boolean","description":"False when retired. Retired variants are never deleted — orders reference them."},"description":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"**Who this ticket type is for and what it includes**, shown behind the (i) on each Adult, Child, Senior or Infant row (decided 29 September, 23SEP-6). Each language value at most 300 characters; longer is a `400`. Set with `updateProductVariant`. Whether the guest screen shows it is `BookingFlowConfig.cardInfo` (white-label).\n"}}},
"Queue": {"x-ticvai-persistence":"queue.queue + queue.queue_operating_window","allOf":[{"$ref":"#/components/schemas/CreateQueueRequest"},{"type":"object","required":["id","status","waitingPartyCount"],"properties":{"id":{"type":"string","format":"uuid"},"status":{"$ref":"#/components/schemas/QueueStatus"},"statusReason":{"type":"string","nullable":true},"waitingPartyCount":{"type":"integer"},"waitingGuestCount":{"type":"integer"},"currentWaitMinutes":{"type":"integer","nullable":true},"waitTimeSource":{"$ref":"#/components/schemas/WaitTimeSource"},"waitTimeAsOf":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When `currentWaitMinutes` was last set, by whichever source set it. `WaitTime.asOf` reads this.\n"},"manualWaitExpiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"Set by `setWaitTime` as now plus `expiresInMinutes`. Past it, the manual figure is dropped and the queue reverts to its sensor or throughput estimate. Null when the current figure is not manual.\n"},"manualWaitNote":{"type":"string","maxLength":200,"nullable":true,"readOnly":true,"description":"The `note` given with the current manual figure. Cleared when it expires."},"expectedReopenAt":{"type":"string","format":"date-time","nullable":true}}}]},
"QueueDetail": {"x-ticvai-persistence":"queue.queue","allOf":[{"$ref":"#/components/schemas/Queue"},{"type":"object","properties":{"nowServingPartyNumber":{"type":"integer","nullable":true},"lastCalledAt":{"type":"string","format":"date-time","nullable":true},"throughputLastHour":{"type":"integer"},"noShowRatePercent":{"type":"number"},"feed":{"$ref":"#/components/schemas/QueueFeedHealth"}}}]},
"QueueEntryStatus": {"type":"string","enum":["waiting","called","redeemed","expired","noShow","cancelled","released"]},
"QueueFeedHealth": {"x-ticvai-persistence":"none — computed","type":"object","required":["feedId","isHealthy","isQuiet"],"properties":{"feedId":{"type":"string","format":"uuid"},"adaptor":{"$ref":"#/components/schemas/QueueFeedAdaptor"},"isHealthy":{"type":"boolean","description":"**Healthy means the last reading arrived within the feed's expected interval** (decided 28 September, audit R106 (1)): `lastReadingAt` is no older than `expectedIntervalSeconds`. It is the opposite of `isQuiet`, and nothing else (latency, discards) makes a reporting feed unhealthy.\n"},"isQuiet":{"type":"boolean","description":"No reading within the expected interval. The wait time falls back to throughput-derived and is marked stale rather than freezing at the last value.\n"},"lastReadingAt":{"type":"string","format":"date-time","nullable":true},"expectedIntervalSeconds":{"type":"integer","description":"The feed's `expectedIntervalSeconds` — the interval `isQuiet` is judged against, returned here so a health panel does not need the feed row as well.\n"},"readingsLastHour":{"type":"integer"},"discardedLastHour":{"type":"integer","description":"Out-of-order readings rejected in the last hour — rows of `queue.reading` for this feed with `disposition: discardedOutOfOrder`. Duplicates are not counted here: a duplicate has no row, and `submitQueueReading` reports it in its own `duplicates`.\n"}}},
"QueueStatus": {"type":"string","enum":["open","paused","closed","atCapacity"]},
"QueueStatusResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["queue","affectedEntries"],"properties":{"queue":{"$ref":"#/components/schemas/Queue"},"affectedEntries":{"type":"object","description":"What happened to guests already waiting. Closing releases and notifies them — a guest holding a position for a ride that will not run should be told.\n","properties":{"released":{"type":"integer"},"held":{"type":"integer"},"notified":{"type":"integer"}}}}},
"Refund": {"x-ticvai-persistence":"orders.refund","type":"object","required":["id","orderId","amount","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid"},"batchId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `RefundBatch` that raised this refund, where `createBulkRefund` did. Null for a refund raised on its own."},"fxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"readOnly":true,"description":"**The rate on the original payment, not today's** (BL-087, CF-118).\n`Payment` records `tenderCurrency`, `fxRate` and `fxRateSource` at the moment of sale, so the sale rate is always retrievable. **Refunding at today's rate repays a different amount of money than was taken** — a guest who paid 100 USD at 3.67 and is refunded at 3.72 gets back more AED than they gave, and the venue carries the difference on every refund.\nThe exposure runs both ways and neither direction is defensible: a guest short-changed by a moving rate has a complaint the venue cannot answer, because **the guest did nothing but wait.**\n"},"taxReversalEntryId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**A refund reverses the tax entry it created, and this is where that is stated rather than implied.** `reverseJournalEntry` and `calculateTax` both exist, so both halves were present and the obligation was assumed — **an implied obligation is one a developer can miss without failing anything.**\nNull only where the original sale carried no tax.\n"},"settleTo":{"type":"string","enum":["originalTender","advanceBalance","wireTransfer","storeCredit"],"default":"originalTender","description":"BL-086. **A refund could only go back the way it came.** A guest whose card has expired, a partner settling by wire, a guest who would rather have the credit — three real cases with one answer.\n**`originalTender` stays the default** because refunding elsewhere is how money laundering works, and anything else needs a reason.\n\n**`storeCredit` is a gift card issued for the refund amount** (decided 2 October 2026, Chinmay, batch 1, POS-011; DEC-061; CHG-CSP-037; DI-796), never a voucher or a wallet top-up.\n"},"fxVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Where the sale rate and the current rate differ, **the difference is booked as an FX variance rather than hidden in the refund**. `runFxRevaluation` already handles this class of movement and this is the same act at a smaller scale.\n"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**A refund goes back in the currency the guest paid** (decided 2 October 2026, Chinmay; CHG-FIN-001). For a card or wallet payment taken in a guest-selected currency, the refund request to the provider is in that currency, and `tenderAmount` is the refunded share of the original `Payment.tenderAmount` at the sale rate (`fxRate`), so a full refund returns exactly what was charged. `amount` stays in base currency for the ledger. Null for a refund in the base currency. Foreign cash refunded at a till is paid in base currency (DI-282)."},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"The refund in `tenderCurrency`, at that currency's own scale (CHG-FIN-001)."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"appliedPercentage":{"type":"number","description":"From the venue's time bands, or an approver override."},"status":{"type":"string","enum":["pendingApproval","pendingGateway","completed","declined","failed"]},"reason":{"type":"string"},"requestedByPrincipalId":{"type":"string","format":"uuid"},"secondaryPrincipalId":{"type":"string","format":"uuid","nullable":true},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"ledgerEntryId":{"type":"string","format":"uuid","nullable":true,"description":"Written before the gateway is called."},"gatewayReference":{"type":"string","nullable":true},"createdAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true}}},
"ReportIncidentRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","kind","severity","venueId","description","occurredAt","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/IncidentKind"},"severity":{"$ref":"#/components/schemas/IncidentSeverity"},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid"},"locationDescription":{"type":"string","maxLength":500},"description":{"type":"string","minLength":3,"maxLength":10000},"involvedSubjectIds":{"type":"array","description":"Opaque references. Personal details live in the erasable store, so the incident record survives an erasure request intact.\n","items":{"type":"string","format":"uuid"}},"involvedStaffPrincipalIds":{"type":"array","items":{"type":"string","format":"uuid"}},"witnessCount":{"type":"integer"},"firstAidGiven":{"type":"boolean","default":false},"emergencyServicesCalled":{"type":"boolean","default":false},"attachmentRefs":{"type":"array","items":{"type":"string"}},"occurredAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"}}},
"Suggestion": {"type":"object","x-ticvai-persistence":"ai.suggestion","description":"One answer to one question, with its reasoning and its confidence. **Built 24 August so that machine learning can be swapped in without touching a screen.**\n**A suggestion is never an action.** It proposes; `ProposedAction` and its approval path decide. A model that can order stock is a model that will order stock wrongly at three in the morning.\n**`inputs` is recorded, not just referenced.** A suggestion that cannot be reproduced cannot be defended to a finance controller asking why the system said to order four hundred.\n","required":["id","kind","basis","maturity","producedAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/SuggestionKind"},"basis":{"$ref":"#/components/schemas/SuggestionBasis"},"scopePath":{"type":"string"},"subjectRef":{"type":"string","nullable":true,"description":"What it is about — a product, an outlet, an item, a party."},"value":{"type":"object","additionalProperties":true,"description":"The suggestion itself. Shape depends on `kind`."},"confidence":{"type":"number","nullable":true,"minimum":0,"maximum":1,"description":"**Null for a heuristic and that is honest.** A rule has no confidence — dressing one up with 0.85 is the fastest way to make a manager trust a number that means nothing.\n"},"explanation":{"type":"string","description":"**Plain words, always present, whatever the basis.** *Because covers are up 12% on this day last year* — a suggestion a manager cannot explain to their own boss is a suggestion they will not action.\n"},"inputs":{"type":"object","additionalProperties":true,"description":"What went in. **Recorded so the answer can be reproduced** — and so that when a model replaces the rule, the two can be run against the same inputs and compared.\n"},"producerRef":{"type":"string","description":"The rule name or the model id and version. **A model version is part of the record**: *the model said so* is not an answer to *which model, when*.\n"},"maturity":{"$ref":"#/components/schemas/AiMaturity"},"producedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time","nullable":true,"description":"**A demand forecast for Saturday is worthless on Sunday.** An expired suggestion is hidden rather than shown stale.\n"}}},
"SuggestionBasis": {"type":"string","description":"**How the answer was reached, and this is the field the whole design exists for.**\nA venue must be able to see that today's price suggestion is a margin rule and next quarter's is a trained model — **the same operation, the same screen, a different basis** — and a screen that cannot say which is a screen that asks a manager to trust arithmetic it will not show.\n**Swapping a heuristic for a model is a provider change, not a contract change.** That is the point of the abstraction: the frontend, the audit record and the outcome capture all stay exactly as they are.\n","enum":["heuristic","statistical","model","hybrid","manual"]},
"SuggestionKind": {"type":"string","description":"What is being suggested. **A closed set, and the reason it is closed is the swap.** Every entry here is a question a venue asks that a model could answer better than a rule — and each one starts as a heuristic and becomes a model when there is data.\n**Six of these were drawn as their own endpoints on the client F&B boards** — `suggestPrice`, `simulateScenario`, `simulateSlaPolicy`, `suggestRequisition`, `suggestReplenishment`, `publishDemandPlan`. **Building six endpoints means six places to change when a model changes**, and the model will change more often than the venue's question does.\n**What each kind is based on, and when the venue's own data takes over. Proposed, client to correct (decided 28 September, audit R213; re-read 29 September, AI functions review).** The figure after each rule is **the point where own data takes over from the baseline, not a refusal**: below it the kind answers from the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, the weather) with `maturity.stage` `starting`, and between it and about three months it blends the two (`learning`). The day-one baseline per kind: `replenishment`, `requisition`, `prepPlan`, `staffing`, `demandForecast` and `scenario` from the baseline forecast (typical attendance from the venue AI settings x the venue-type month curve x the calendar x weather, bookings on hand as a floor); `menuEngineering` ranked by margin with popularity marked learning; `slaTarget` a standard default; `waitTime` people ahead / configured capacity; `upsell` the relationship map and business priority; `segmentation` known guest attributes; `anomaly` the venue's configured thresholds and actual against the forecast's low end; `sendTime` the channel's typical hour; `wasteRisk` shelf life and par against the forecast; `queueBalancing` configured capacity per queue. Only a missing setting refuses (422 `AiMissingSettingProblem`).\n- `price`: unit cost plus the category's target margin, held inside the price band. Minimum: a current cost, no history.\n- `replenishment`: par level minus on-hand plus expected use over the supplier lead time. Minimum: 14 days of stock movements.\n- `requisition`: the next service's prep-plan ingredient needs minus kitchen stock. Minimum: 14 days of sales.\n- `demandForecast`: the average of the same weekday over the last 8 weeks, adjusted by admissions already booked. Minimum: 8 weeks of sales.\n- `prepPlan`: forecast covers for the service times each item's share of the last 4 same weekdays. Minimum: 4 weeks of sales.\n- `menuEngineering`: each item placed by popularity against margin, over 90 days. Minimum: 90 days of sales.\n- `staffing`: forecast demand divided by the role's standard covers per staff hour. Minimum: 8 weeks of sales (the forecast it rests on).\n- `slaTarget`: the 80th percentile of actual times over the last 30 days. Minimum: 30 days of timed events.\n- `waitTime`: people ahead divided by the throughput of the last 30 minutes. Minimum: 30 minutes of throughput today.\n- `upsell`: the item most often bought with the basket's items over 90 days. Minimum: 90 days of orders.\n- `segmentation`: recency, frequency and spend scores over 12 months. Minimum: 90 days of orders.\n- `anomaly`: a value outside three standard deviations of the same weekday over 8 weeks. Minimum: 8 weeks of the measure.\n- `scenario`: the demand forecast re-run with the stated changes. Minimum: as `demandForecast`.\n- `sendTime` (added 29 September): per recipient, the hour inside `context.sendWindow` in which they have most often opened or clicked over the last 90 days (marketing-crm attribution touches), and where `context.channel` is `best`, the consented channel with the highest engagement. A recipient with fewer than three touches gets their segment's modal hour, and one with none the window's start. Asked with `subjectRef` a segment id or `context.subjectIds` (at most 10,000). `value` is `{recommendations: [{subjectId, sendAt, channel, basisTouches}]}`. Minimum: 90 days of message touches at the scope.\n- `wasteRisk` (added 29 September): per item at an outlet or store location, planned production and stock on hand minus forecast demand over the item's shelf life, plus batches expiring inside the horizon (`inventory.listExpiringBatches`). `value` is `{items: [{itemRef, quantityAtRisk, valueAtCost, expiresAt, recommendedAction (reducePrep, promote, transfer, useInRecipe), transferTo}]}`. Minimum: 14 days of recorded waste and of sales.\n- `queueBalancing` (added 29 September): per queue or attraction at `subjectRef` (a venue) over `horizon`, the forecast wait (the `queue` forecast definition) against throughput capacity, a recommended virtual-queue return-slot allocation by queue type, and guest redirection from over-used to under-used attractions. `value` is `{queues: [{queueId, forecastWaitMinutes, capacityPerHour, returnSlotsPerInterval, redirectTo}]}`. Minimum: 14 days of queue readings.\n- `itinerary` (added 29 September, MOB-6, guest-allowed): refines a `venue-map` visit plan the guest owns. `subjectRef` is the plan id; `value` is `{planId, baseVersion, changes, rationale}`, applied with `updateVisitPlan` as the guest. Minimum: none; the rules plan is the baseline. Every change names a point or performance of that day's venue only, rides, dining and retail alike (30 September client meeting, MoM 4.7).\n","enum":["price","replenishment","requisition","demandForecast","prepPlan","menuEngineering","staffing","slaTarget","waitTime","upsell","segmentation","anomaly","scenario","sendTime","wasteRisk","queueBalancing","itinerary"]},
"TenderKind": {"type":"string","description":"`wallet` is a **digital wallet** (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 (a)). **The stored-value TICVAI wallet is a separate tender**: it is spent through `authoriseStoredValue` and `captureStoredValue` (`StoredValueKind` `wallet`), never as this value, so the client can see which of the two the decision meant.\n","enum":["cash","card","wallet","voucher","bankTransfer","hotelCharge","installment","giftCard","complimentary"]},
"UploadIncidentMediaRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["kind","filename","contentType","sizeBytes"],"properties":{"kind":{"type":"string","enum":["photo","video","document"]},"filename":{"type":"string","maxLength":256},"contentType":{"type":"string"},"sizeBytes":{"type":"integer","minimum":1},"capturedAt":{"type":"string","format":"date-time","description":"Device time the photo or video was taken."},"caption":{"type":"string","maxLength":500}}},
"VenueMap": {"type":"object","x-ticvai-persistence":"venuemap.map","description":"A park map, or a floor plan. **Several per venue** — a guest on the second floor should not be shown the ground floor's toilets.\n","required":["id","name","venueId","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string","readOnly":true,"description":"Derived from `venueId`. Not sent by a client."},"kind":{"type":"string","enum":["park","floor","zone","parking"]},"floorLevel":{"type":"integer","nullable":true},"status":{"type":"string","enum":["draft","published","archived"],"readOnly":true,"description":"`draft` on create. Moves through `publishVenueMap` (`states/venue-map.yaml`), never by sending a value.\n"},"publishedVersion":{"type":"integer","nullable":true,"readOnly":true,"description":"The `VenueMapVersion.version` guests are served. Null until the first publish.\n"},"graphVersion":{"type":"integer","readOnly":true,"description":"**Bumped by a publish or a closure**, and returned as `VenueMapGraph.version`. Separate from `publishedVersion` because a closure changes the routes without creating a map version, and a closure that looked like a publish would lie about what changed.\n"},"isGeoreferenced":{"type":"boolean","readOnly":true,"description":"**Whether a guest can be located on it.** Without a georeference the map is a picture — useful, and not navigable.\n"},"baseAssetId":{"type":"string","format":"uuid","nullable":true,"description":"**The illustrated map a guest actually sees**, held in `assets` like any other media.\n**This is not the CAD drawing.** The drawing gives geometry — where things are, and how they connect. The base image is a designed illustration with the venue's own styling, and the two are different artefacts that happen to describe the same place. A park hands you an architect's plan and a beautiful painted map, and **the guest wants the second while the platform needs the first.**\nNull is valid. A map with geometry and no illustration renders as shapes — plain, and navigable.\n","x-ticvai-references":"assets.MediaAsset"},"baseImageAlignment":{"type":"object","nullable":true,"description":"**How the illustration lines up with the geometry.** They are drawn at different scales by different people, and a point placed on the plan lands in the wrong place on the painting unless something reconciles them.\nTwo known points is enough. **Without this the illustration is a picture behind the map rather than the map itself.**\n","properties":{"imageWidthPx":{"type":"integer"},"imageHeightPx":{"type":"integer"},"anchors":{"type":"array","minItems":2,"maxItems":4,"items":{"type":"object","properties":{"planX":{"type":"number"},"planY":{"type":"number"},"imageX":{"type":"number"},"imageY":{"type":"number"}}}}}},"tileSetRef":{"type":"string","nullable":true,"readOnly":true,"description":"Where a base image is large enough to need zoom levels. **A 12,000-pixel park map is not something a phone downloads on arrival**, and a guest opening the map on venue wifi at the gate is the worst moment to send twenty megabytes.\nGenerated from the base asset. Null means the image is small enough to serve whole.\n"},"boundsGeoJson":{"type":"string","nullable":true},"graphStatus":{"type":"string","readOnly":true,"enum":["notBuilt","connected","disconnected","partial"],"description":"**Whether every public point can actually be reached.** Computed at publish.\n`disconnected` means a point has no path to it at all — a toilet nobody can walk to is a toilet that does not exist. `partial` means every point is reachable and at least one only by steps, which is a different and quieter failure: **the map works until a wheelchair user opens it.**\n"},"modelAssetId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"assets.MediaAsset","description":"**The 3D layer of the working draft** (ADR-0069, contract item closed 3 October 2026): the GLB (`model3d` asset) the last `glbModel` import brought in. Set by `importVenueGeometry`, never by sending a value. Null for a 2D-only map, which is the default and needs nothing. The 3D model is a rendering of the map, never the source of its truth: routes come from the graph.\n"},"navigationFileAssetId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"assets.MediaAsset","description":"The navigation file imported with the model, kept so the import can be re-run and audited."},"modelTransform":{"readOnly":true,"description":"**How the model's local frame sits on the earth** (ADR-0069 section 3): the navigation file's anchor, stored once and used both ways. Null without a model. It maps onto the plan's georeference as the ADR says, so a map with a model is georeferenced.\n","allOf":[{"$ref":"#/components/schemas/VenueModelTransform"}]},"model3dStatus":{"type":"string","readOnly":true,"enum":["none","publishable","blocked"],"description":"**Whether the next publish carries the 3D layer.** `none`: no model. `publishable`: the last model import had no `error` finding. `blocked`: it had one (over 300,000 triangles at LOD0, uncompressed textures, a control point more than 10 m out, an invalid navigation file), named in that job's `model.findings`; the 2D map still publishes and guests see 2D until a corrected model is imported (ADR-0069 sections 3 and 6).\n"}}},
"VenueMapDetail": {"type":"object","description":"19.2.55. **The whole map in one call**, so a client caches it and filters locally.","properties":{"version":{"type":"integer","nullable":true,"readOnly":true,"description":"**The published version these points and paths belong to**, which is the number a client caches and sends back as `version`. It can differ from `map.publishedVersion` when an older version was asked for. Null when the draft was read.\n"},"map":{"$ref":"#/components/schemas/VenueMap"},"points":{"type":"array","items":{"$ref":"#/components/schemas/VenuePoint"}},"paths":{"type":"array","items":{"$ref":"#/components/schemas/VenuePath"}},"resources":{"type":"array","description":"The bookable resources placed on this version of the map (rev 3 REV3-15). Empty on a map that carries none.\n","items":{"$ref":"#/components/schemas/PlacedResource"}},"model3d":{"nullable":true,"description":"**The 3D layer of the version read** (ADR-0069; 3 October 2026, r1 additions). Null when that version has none, and then the guest app shows the 2D map with the same route, as it does on a phone that cannot hold 30 fps.\n","allOf":[{"$ref":"#/components/schemas/VenueModel3d"}]}}},
"VenueModel3d": {"type":"object","x-ticvai-persistence":"none — jsonb column","description":"**The 3D layer a guest app loads** (ADR-0069): the model and the transform of the version it read. The app downloads the GLB through the asset delivery rules (UAE-hosted for a UAE tenant, ADR-0069 section 7) and caches it with the graph.\n","required":["modelAssetId","transform"],"properties":{"modelAssetId":{"type":"string","format":"uuid","x-ticvai-references":"assets.MediaAsset"},"sizeBytes":{"type":"integer","nullable":true},"transform":{"$ref":"#/components/schemas/VenueModelTransform"}}},
"VenuePath": {"type":"object","x-ticvai-persistence":"venuemap.path","description":"19.2.56. **The navigation graph.** The map supplies it; routing over it is a client concern, because a phone with the map cached routes offline and a server round-trip per step does not.\n","required":["id","mapId","fromPointId","toPointId"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"mapId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of the operation that writes the path."},"fromPointId":{"type":"string","format":"uuid"},"toPointId":{"type":"string","format":"uuid"},"geometry":{"type":"string","nullable":true,"description":"The centreline this edge follows, as an encoded polyline. **A walkway in a drawing is a polygon and a route is a line down the middle of it**, so extraction thins the polygon to a centreline and splits it at every fork.\nNull where the path was drawn on screen as a straight connection, which is normal for a venue with no walkway layer.\n"},"distanceMetres":{"type":"number","nullable":true,"readOnly":true,"description":"Computed by the server from `geometry` and the georeference. **Along the centreline, not point to point.** A path that curves round a lake is longer than the distance between its ends, and a guest told 80 metres who walks 200 stops trusting the map.\nRequires a georeference for real units; without one, distances are in drawing units and routing still works because **only the ratios matter to a shortest path.**\n"},"isStepFree":{"type":"boolean","default":true,"description":"**The single most important attribute on this object.** A wheelchair user routed up a staircase has been failed by the map, not by the venue.\n"},"isIndoor":{"type":"boolean","default":false},"restrictedByPointId":{"type":"string","format":"uuid","nullable":true,"description":"**Where a path is one-way, it is because of a thing on it — not because of the path.** Removed `isOneWay` on 18 August: a pedestrian walkway has no direction, and the three cases that look one-way are all a gate or a queue.\nA turnstile is one-way and `access.AccessPoint.direction` already says so. A queue line is one-way and `queue` owns it. **Putting the restriction on the path duplicated both and would have drifted from them** — a gate reconfigured to bidirectional would leave a path still marked one-way, and nothing would have noticed.\nSet where a path passes through an access point. The router reads the direction from the point.\n"},"closedReason":{"type":"string","nullable":true,"readOnly":true,"description":"Set by `setPathClosure` during works or an incident, never by sending it here. **A closed path removes routes rather than hiding the path**, so a guest sees why rather than wondering where it went.\n"}}},
"VenuePoint": {"type":"object","x-ticvai-persistence":"venuemap.point","description":"19.2.57 to 19.2.60. **What a venue places on the map**, and what a guest taps.\n","required":["id","mapId","kind","name","position"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"mapId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of the operation that writes the point."},"kind":{"type":"string","enum":["ride","attraction","show","restaurant","cafe","shop","kiosk","toilet","babyCare","prayerRoom","firstAid","atm","lockers","entrance","exit","emergencyExit","assemblyPoint","parking","guestServices","smokingArea","waterFountain","chargingPoint","photoSpot","junction","other"],"description":"**A closed set, and `emergencyExit` is separate from `exit` on purpose.** An exit is where a guest leaves; an emergency exit is where they are sent, and a map that cannot tell them apart is a map that routes a normal departure through a fire door.\n**`junction` is the one that is not a point of interest.** A path connects two points, so a fork in a walkway with nothing at it still needs a node — otherwise every bend has to be named as a destination, and a guest browsing the map sees forty entries called *Path junction 12*.\n**Junctions are hidden from guests and present in the graph.** Generated by extraction where paths meet; a venue never places one by hand.\n"},"name":{"type":"string","x-ticvai-unique":"venue","description":"**Unique per venue** (decided 28 September, audit R108). Two points on a venue's maps never share a name, compared without case, so *Toilets North* names one place; `setVenuePoint` refuses a duplicate with `409` `duplicate-code`. Junctions are named by extraction and are exempt.\n"},"nameLocalised":{"type":"object","nullable":true,"additionalProperties":{"type":"string"}},"position":{"type":"object","required":["x","y"],"description":"Drawing coordinates. **Latitude and longitude are derived from the georeference**, not stored, so a map that is re-georeferenced does not need every point moved.\n","properties":{"x":{"type":"number"},"y":{"type":"number"}}},"outletId":{"type":"string","format":"uuid","nullable":true,"description":"For a restaurant, cafe, shop or kiosk. **Tapping it should open the menu**, and that only works if the map knows which outlet it is.\n"},"productId":{"type":"string","format":"uuid","nullable":true,"description":"For a ride or show — links to wait times and to booking. **What a guest is offered from any point, including a restaurant or a shop, is `featuredOffer`** (29 September, MOB-4); this link stays for wait times.\n"},"accessPointId":{"type":"string","format":"uuid","nullable":true,"description":"For an entrance or exit. **This is what makes 3.2.64 work** — live admission statistics drawn on the point they came from.\n"},"isStepFree":{"type":"boolean","default":true,"description":"Whether the point itself can be reached without steps. **The same name as `VenuePath.isStepFree`, because it is the same concept** (it was `isAccessible` until the 26 September audit). **Placed on the point rather than inferred from the path**, because a step-free route to a building with steps at the door is not a step-free route.\n"},"openingHours":{"type":"string","nullable":true},"iconRef":{"type":"string","nullable":true},"isActive":{"type":"boolean","default":true},"isNavigable":{"type":"boolean","default":true,"description":"Whether a route may pass through it. **False for a point that marks a place without being reachable** — a stage a guest cannot walk onto, a zone label.\n"},"isDestination":{"type":"boolean","default":true,"description":"**Whether a guest may be routed *to* it, and whether it appears in a list of places.** False for a `junction`, which exists in the graph and nowhere else.\nSeparate from `isNavigable` because the two differ: a junction is navigable and not a destination, and a fenced landmark is a destination you can be shown but not walked into.\n"},"description":{"type":"object","nullable":true,"additionalProperties":{"type":"string","maxLength":1000},"description":"**What the guest reads on Item Detail** (29 September, MOB-4). Keyed by locale, like `nameLocalised`. One screen now serves rides, shows, restaurants and shops (GST-004 and GST-006 merged), and it opens from the map pin, so the point carries the words rather than each kind borrowing them from a different module. Set on BO-094.\n"},"media":{"type":"array","maxItems":12,"description":"**The gallery on Item Detail** (29 September, MOB-4): images and short clips from the asset library, first `isPrimary` shown on the map card. Assets are referenced, never copied, so a replaced photo changes everywhere.\n","items":{"type":"object","required":["assetId","kind"],"properties":{"assetId":{"type":"string","format":"uuid","x-ticvai-references":"assets.media_asset"},"kind":{"type":"string","enum":["image","video"]},"isPrimary":{"type":"boolean","default":false},"altText":{"type":"string","nullable":true,"maxLength":200}}}},"featuredOffer":{"type":"object","nullable":true,"required":["kind","id"],"description":"**The product card on Item Detail, for every kind of point** (29 September, MOB-4). `productId` above links a ride or show to its wait times; this is what the guest is offered from the point, and it may be a bundle: a restaurant offers *meal combo with admission* (`promotions` bundle with an admission and a meal component), which checks out in about three steps (GST-004 → GST-056 → GST-041). A point with none shows no card. **Referenced, not priced here**: the card reads `catalogue.getProduct` or `promotions.getBundle` for the live price and availability.\n","properties":{"kind":{"type":"string","enum":["product","bundle"]},"id":{"type":"string","format":"uuid","description":"The `catalogue.product` id or the `promotions.bundle` id, by `kind`."},"label":{"type":"string","nullable":true,"maxLength":40,"description":"The button text, e.g. *Buy meal combo*. Null uses the product's own call to action."}}},"typicalDurationMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":600,"description":"**How long a visit to this point usually takes**, ride time and queue excluded (29 September, MOB-6). The visit planner lays out a day with it; the queue comes from `queue.getWaitTimes` on the day. Null for a point the planner never places (a toilet).\n"},"interestTags":{"type":"array","maxItems":12,"description":"**What a guest who says they like this would like here** (29 September, MOB-6): the planner matches the guest's interests against these. A closed list so that the Plan tab's interest chips and the venue's tags are the same words.\n","items":{"type":"string","enum":["thrill","family","kids","water","animals","shows","culture","shopping","dining","relaxing","photo","adventure","sport","nightlife","indoor"]}},"cuisineTags":{"type":"array","maxItems":8,"description":"**For dining points** (restaurant, cafe, kiosk; 29 September, MOB-6). The planner places meals at points whose cuisine the party chose, at meal times. Free text codes such as `arabic`, `indian`, `italian`, `fastFood`, `vegetarian`, `halal` — cuisines are too many to close, and a wrong enum is worse than an unmatched tag. **Read per venue**: the planner matches a guest's cuisine only against the points of the venue that day is at (30 September, MoM 4.7).\n","items":{"type":"string","maxLength":30}},"retailTags":{"type":"array","maxItems":8,"description":"**For retail points** (shop, and a kiosk that sells goods rather than food; 30 September client meeting, MoM 4.7: retail and kiosk shops join F&B as venue-linked planner options). The planner places a shop stop at points whose tags the party chose, on the day of this point's venue only. Free text codes such as `souvenirs`, `toys`, `apparel`, `photo`, `essentials`, for the same reason as `cuisineTags`. A kiosk may carry both lists.\n","items":{"type":"string","maxLength":30}}}},
"VoidReason": {"type":"string","description":"**The void reason list** (decided 28 September, audit R125 (4)): the one list `voidOrder` takes, and the list `fnb.amendFnbOrder` and `fnb.cancelFnbOrder` point to. `other` requires a note (audit R222), and the notes are reviewed quarterly to add real reasons. Proposed, client to correct.\n","enum":["guestChangedMind","enteredInError","itemUnavailable","qualityIssue","duplicate","other"]},
"WaitTime": {"x-ticvai-persistence":"none — computed from readings and throughput","type":"object","required":["queueId","waitMinutes","source","asOf","isStale"],"properties":{"queueId":{"type":"string","format":"uuid"},"queueName":{"$ref":"#/components/schemas/LocalisedText"},"attractionProductId":{"type":"string","format":"uuid","nullable":true},"attractionCategoryId":{"type":"string","format":"uuid","nullable":true,"description":"The catalogue `ProductCategory` the attraction product is filed under — the value the `category` filter on `getWaitTimes` matches. Read from catalogue, not stored here.\n"},"status":{"$ref":"#/components/schemas/QueueStatus"},"waitMinutes":{"type":"integer","nullable":true,"description":"Null where the queue is closed or no estimate is available."},"source":{"$ref":"#/components/schemas/WaitTimeSource"},"isStale":{"type":"boolean","description":"The underlying feed has gone quiet past its expected interval. The figure is shown with a caveat rather than frozen and presented as current, and it is not hidden (decided 28 September, audit R080 (b)): the screen shows `waitMinutes` with its `asOf` and a stale marker.\n"},"heightRequirementCm":{"type":"integer","nullable":true},"zone":{"type":"string","nullable":true},"asOf":{"type":"string","format":"date-time","description":"When the figure was produced — the queue's `waitTimeAsOf`."}}},
"WaitTimeSource": {"type":"string","description":"Where the estimate came from. Surfaced so an operator knows whether a figure is measured or guessed.\n","enum":["sensor","throughput","manual","unavailable"]},
"WaitingGuest": {"x-ticvai-persistence":"queue.entry","type":"object","required":["id","queueId","partyNumber","partySize","status","joinedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The client-generated UUIDv7 from `JoinQueueRequest.id`, and the `entryId` every entry path takes. `listMyWaitingGuests` gives it back to a guest who has lost it.\n"},"queueId":{"type":"string","format":"uuid"},"queueName":{"$ref":"#/components/schemas/LocalisedText"},"subjectId":{"type":"string","format":"uuid","nullable":true},"partyNumber":{"type":"integer","description":"What the guest sees and what appears on signage."},"partySize":{"type":"integer"},"status":{"$ref":"#/components/schemas/QueueEntryStatus"},"positionInQueue":{"type":"integer","nullable":true},"partiesAhead":{"type":"integer","nullable":true},"estimatedCallAt":{"type":"string","format":"date-time","nullable":true},"isFastPass":{"type":"boolean"},"priorityBasis":{"type":"string","enum":["none","entitlement","loyaltyTier","promotion","accessibility"],"default":"none","description":"Why this party is priority, when it is (decided 29 September, build pass; 5.6.7, 5.6.34): the first `QueueFastPass` criterion met at join, in the order entitlement, loyalty tier, promotion, accessibility. `isFastPass` is true whenever this is not `none`. Kept on the entry so a disputed priority can be explained afterwards.\n"},"priorityTierId":{"type":"string","format":"uuid","nullable":true,"description":"The loyalty tier that granted priority, where `priorityBasis` is `loyaltyTier`."},"priorityPromotionId":{"type":"string","format":"uuid","nullable":true,"description":"The promotion that granted priority, where `priorityBasis` is `promotion`."},"accessibilityNeedDeclared":{"type":"boolean","default":false,"description":"What the party declared at join, shown to the operator at the front."},"entitlementId":{"type":"string","nullable":true},"calledAt":{"type":"string","format":"date-time","nullable":true},"returnWindowEndsAt":{"type":"string","format":"date-time","nullable":true},"redeemedAt":{"type":"string","format":"date-time","nullable":true},"admittedCount":{"type":"integer","nullable":true},"joinedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}}
}
```
