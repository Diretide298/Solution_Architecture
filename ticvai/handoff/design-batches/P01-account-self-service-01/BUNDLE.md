# P01-account-self-service-01 — P01 · Account & Self-Service

**5 screens · 45 operations · 50 schemas · 8 permissions**

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

- **Every control that can be refused must be gated.** 8 permissions apply here:
  `GUEST_MANAGE, GUEST_VIEW, LEDGER_POST, LEDGER_VIEW, MARKETING_VIEW, ORDER_MODIFY, ORDER_VIEW, WALLET_VIEW`. A control nobody can use must say so,
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


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `WEB-016` | Login / Register | A | 35 | 6 | 6 | 15 | 11 | 0 | guest | review (client-verified) |
| `WEB-017` | My Account Dashboard | A | 3 | 74 | 6 | 56 | 1 | 0 | guest | review (client-verified) |
| `WEB-018` | My Tickets | A | 11 | 37 | 6 | 8 | 8 | 0 | guest | review (client-verified) |
| `WEB-019` | Order History | A | 15 | 74 | 6 | 16 | 2 | 0 | guest | review (client-verified) |
| `WEB-020` | Profile & Preferences | A | 16 | 47 | 6 | 15 | 0 | 0 | guest | review (client-verified) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `WEB-016` Login / Register

**Get a guest into the site, fast, on a device that may be shared: a one-time code to the email or mobile, a password, Apple or Google, or UAE Pass, or register a new account. **No enterprise SSO for guests** (decided 28 September, audit R167, first part). **A second factor only where the venue enabled guest two-step verification** (decided 29 September, rev 3 GAP-B1, per venue, superseding the second part of R167).**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Account & Self-Service · wave 1 · needs the `core` module |
| Block | Block A · task APP-WEB-WEB-016 |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025); in the flows as guest |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · the venue's theme |
| Pattern | form (compact density): **A sign-in form, not a list.** Four ways in (a one-time code, a password, Apple or Google, UAE Pass) and a way to register; `getGuestSession` is the one piece of context. Rebuilt 28 September: the … |
| Offline | **Not available, and the offline banner says why.** Signing in, registering and verifying a code need the server. |
| Opens with | `cartId` (session), `challengeId` (navigation), `subjectId` (navigation) · cold entry: **Needs nothing.** A guest arriving cold signs in and goes to My Account; one sent from the cart carries `cartId` and goes back to it. The SSO deep-link … |
| Route | `/account-and-self-service/login-register` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Corrected 24 August**: removed getCurrentSession, logout, selectRole. **A guest surface has no roles to select and its own logout** — `selectRole` is ADR-0002 staff authorisation and `getCurrentSession` is the staff session. `guestLogout` and `getGuestSession` are the equivalents and both already existed. **The screen was calling the staff identity surface because nothing checked that a guest platform only calls guest operations.** **Rebuilt 28 September as a guest sign-in form** (decided 28 September, audit R167, R073 (a)): removed `login`, `startSsoAuthorization`, `completeSsoAuthorization`, `listSsoProviders` and the six MFA operations — guests have no enterprise SSO. **The second factor came back on 29 September, per venue** (see below). Password sign-in is `guestPasswordLogin`. **Rev 3 (decided 29 September).** **Guest two-step verification is a per-venue setting, off by default** (GAP-B1, per venue, `VenueSettings.identity.guestTwoStep`; supersedes the second part of audit R167, *no guest MFA*; the first part, no enterprise SSO for guests, stands). The prompt appears only when the guest signs in at, or acts at, a venue that has it on; enrolment is on the guest's account (WEB-024). **Sign-in gate (REV3-3):** this screen is where WEB-008 (after add-ons) or WEB-012 (at payment) sends a guest who is not signed in, and it returns them to the cart with the basket kept; a guest code is offered instead when guest checkout is on (`FeatureToggle guestCheckout`, off by default; match …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The guest website's only door: one screen behind the header's profile icon with Sign in and Create account tabs, offering a six-digit code to email or mobile, a password, Apple or Google, and UAE Pass. It is reached from the header and from checkout (after Add-ons by default, or at payment), and must return the guest to exactly where they were with the basket intact. The one thing to get right: nothing on it may reveal whether an account exists, and nothing staff-side (SSO, roles, workstation) appears.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- verifyGuestOtp accepts a code of 4 to 10 characters while the agreed rule is exactly six digits. (CHG-SGU-024)

**Fixed on main** (the package already carries these; draw what it says): requiresModule is 'ticketing' on the guest website's sign-in, while GST-042 (the same door) is 'core'. (CHG-SGU-019); Overlays formGuestSocialLogin, formGuestUaePassLogin and formRefreshToken collect idToken, code/redirectUri and refreshToken as if typed. (CHG-DOOR-006); formRequestGuestOtp asks for `channel` as a field. (CHG-SGU-019).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **DI-974 names the tabs "Log in" and "Register"; every other door in the package says Sign in. Which wording?** → Drawn default accepted: Draw "Sign in" and "Create account" for consistency with every staff and guest door. *(decided by Chinmay, 2026-10-02; DEC-099 / CHG-NOTE-005)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Email or mobile number | text field | — | — | — | — | **Guest checkout asks only the configured fields** (W1): `BookingFlowSettings.guestContactFields` (email, mobile, name). | — |
| Code | text field | — | — | — | — | Shown once a code has been sent; `verifyGuestOtp` returns the `GuestSession`. | — |
| Password | text field | — | — | — | — | **Password sign-in** (decided 28 September, audit R073 (a)): sends `identifier`, `password` and the device's `deviceId` to `guestPasswordLogin`, which returns the same `GuestSession`. A wrong … | — |
| Verification code | text field | — | — | — | — | **Only when the returned `GuestSession` has `requiresMfa`**, which happens only at a venue whose `VenueSettings.identity.guestTwoStep.enabled` is on and only for a guest who enrolled a method (the … | — |

**Form: Create an account** (modal, opened by *Create an account*; *Register guest* calls `registerGuest`, *Cancel* sends nothing)

**Collects what `registerGuest` sends before it is called.** Required: `identifier`, `channel`. Optional: `displayName`, `password`, `preferredLanguage`, `consents`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Identifier `identifier` | text area | required | — | max length 256 | — | Email address or mobile number in E.164. | `registerGuest` body |
| Channel `channel` | segmented control | required | — | Email · SMS · Whatsapp | — | — | `registerGuest` body |
| Display name `displayName` | text field | optional | — | max length 200 | — | — | `registerGuest` body |
| Password `password` | text area | optional | — | min length 8; max length 256 | — | Optional. OTP-only accounts are supported and are the default. | `registerGuest` body |
| Preferred language `preferredLanguage` | language picker | optional | — | — | ISO 639-1 code, shown as the language name | — | `registerGuest` body |
| Consents `consents` | repeatable rows | optional | — | — | — | Consent captured at registration, recorded with the notice version. | `registerGuest` body |
| Purpose `consents[].purpose` | text field | optional | — | — | — | — | `registerGuest` body |
| Granted `consents[].granted` | toggle | optional | — | — | — | — | `registerGuest` body |
| Notice version `consents[].noticeVersion` | text field | optional | — | — | — | — | `registerGuest` body |

Errors to draw in the form: 409 Identifier already registered. Deliberately indistinguishable in timing from success — a registration endpoint that reveals which addresses exist is an account …

**Form: Sign in with password** (modal, opened by *Sign in with password*; *Sign in* calls `guestPasswordLogin`, *Cancel* sends nothing)

**Collects what `guestPasswordLogin` sends before it is called.** Required: `identifier`, `password`. Optional: `deviceId` (sent by the client, not typed). A 401 is one message whatever the cause; a 429 or a locked account says to try again later or use a one-time code instead (decided 28 September, audit R073 (a)). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Identifier `identifier` | text area | required | — | max length 256 | — | The email address or E.164 mobile number the account was registered with. | `guestPasswordLogin` body |
| Password `password` | text area | required | — | min length 8; max length 256 | — | — | `guestPasswordLogin` body |
| Device `deviceId` | text field | optional | — | — | — | Names the device; a new sign-in here ends the previous session on it. | `guestPasswordLogin` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | The venue the guest app or booking is in. Identity reads that venue's `VenueSettings.identity.guestTwoStep` to decide whether a second factor is asked (decided 29 September, rev 3 … | `guestPasswordLogin` body |

Errors to draw in the form: 400 Validation failed

**Form: Link an order I placed as a guest** (modal, opened by *Link an order I placed as a guest*; *Link guest checkout* calls `linkGuestCheckout`, *Cancel* sends nothing)

**Collects what `linkGuestCheckout` sends before it is called.** Required: `orderReference`. Optional: `verificationCode`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Order reference `orderReference` | text field | required | — | — | — | — | `linkGuestCheckout` body |
| Verification code `verificationCode` | text field | optional | — | — | — | From the booking confirmation. Proves possession of the booking. | `linkGuestCheckout` body |

Errors to draw in the form: 403 Contact detail on the order does not match the verified identifier

**Form: Send me a code** (modal, opened by *Send me a code*; *Request guest OTP* calls `requestGuestOtp`, *Cancel* sends nothing)

**Collects only the email or mobile number.** The channel follows from the identifier and the tenant's configured delivery (WhatsApp, SMS or email, DI-209); the guest is never asked to pick one. Dismissing sends nothing.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Identifier `identifier` | text area | required | — | max length 256 | — | — | `requestGuestOtp` body |
| Channel `channel` | segmented control | required | — | Whatsapp · SMS · Email | — | — | `requestGuestOtp` body |
| Purpose `purpose` | radio group | optional | Login | Login · Register · Verify · Password reset · Step up | — | — | `requestGuestOtp` body |

**Form: Sign in with the code** (modal, opened by *Sign in with the code*; *Verify guest OTP* calls `verifyGuestOtp`, *Cancel* sends nothing)

**Collects what `verifyGuestOtp` sends before it is called.** Required: `identifier`, `code`. Optional: `deviceId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Identifier `identifier` | text field | required | — | — | — | — | `verifyGuestOtp` body |
| Code `code` | text field | required | — | min length 4; max length 10 | — | — | `verifyGuestOtp` body |
| Device `deviceId` | text field | optional | — | — | — | — | `verifyGuestOtp` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | The venue the guest app or booking is in. Identity reads that venue's `VenueSettings.identity.guestTwoStep` to decide whether a second factor is asked (decided 29 September, rev 3 … | `verifyGuestOtp` body |

**Sent by *Continue with Apple or Google*** (`guestSocialLogin`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Provider `provider` | segmented control | required | — | Apple · Google | — | — | `guestSocialLogin` body |
| ID token `idToken` | text field | required | — | — | — | — | `guestSocialLogin` body |
| Device `deviceId` | text field | optional | — | — | — | — | `guestSocialLogin` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | The venue the guest app or booking is in. Identity reads that venue's `VenueSettings.identity.guestTwoStep` to decide whether a second factor is asked (decided 29 September, rev 3 … | `guestSocialLogin` body |

**Sent by *Continue with UAE Pass*** (`guestUaePassLogin`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | — | — | — | `guestUaePassLogin` body |
| Redirect URI `redirectUri` | text field | required | — | — | — | — | `guestUaePassLogin` body |
| State `state` | text field | optional | — | — | — | — | `guestUaePassLogin` body |
| Device `deviceId` | text field | optional | — | — | — | — | `guestUaePassLogin` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | The venue the guest app or booking is in. Identity reads that venue's `VenueSettings.identity.guestTwoStep` to decide whether a second factor is asked (decided 29 September, rev 3 … | `guestUaePassLogin` body |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Email or mobile number**: One field accepts either; a value starting with + or a digit is a mobile in E.164 (the UAE prefix +971 prefilled for a local number), anything with @ is an email. The channel is derived, not asked: email for an address; for a mobile, WhatsApp or SMS as the tenant configured, with a "Send by SMS instead" link when both are on. At least one of email or mobile is mandatory, never both. *(source: contracts/spine/identity.yaml#requestGuestOtp; DI-209; DI-372)*
- **Code**: Exactly six digits, numeric keypad, paste and SMS autofill accepted; the copy says six. The verify button enables at six digits. Wrong or expired code: one message, the attempts left, and Send a new code (the limit is VenueSettings.identity.guestOtpMaxAttempts). *(source: DI-1034; contracts/spine/identity.yaml#verifyGuestOtp)*
- **Password**: Minimum 8 characters with show/hide. Offered as an alternative to the code, never required: accounts are code-only by default and a password is optional at registration. *(source: contracts/spine/identity.yaml#guestPasswordLogin; contracts/spine/identity.yaml#registerGuest; R126)*
- **Create account**: Asks only the identifier (email or mobile), an optional display name and optional password, the language (Arabic or English, preselected from the site) and the consent purposes with their notice version. After the code no further profile fields are asked: the profile is completed later. *(source: contracts/spine/identity.yaml#registerGuest; DI-1002; DI-588)*
- **venueId (sent, not shown)**: The venue of the site or the booking in progress is sent with every sign-in call so identity can decide whether that venue's two-step verification applies. The guest never picks it here. *(source: contracts/spine/identity.yaml#verifyGuestOtp; R267; DI-1072)*

#### Outputs: what the screen shows and produces

**Shown**

**Who is signed in on this device** (detail panel, from `getGuestSession`): Shown only when a guest session already exists on this device, with a way to sign out so a shared device is handed over clean.

| Shows | Format | Notes |
|---|---|---|
| Subject | the name it points at, never the id | — |
| Display name | text | — |
| Is verified | yes / no (icon or chip) | False until an OTP or a verified provider identity confirms ownership. An unverified account may browse and fill a cart but not transact … |
| Identity providers | list or chips (count when long) | Linked providers. Several may resolve to one account. |
| Preferred language | text | — |
| Expires at | 1 Oct 2026, 14:30 | 30 days, sliding (decided 28 September, audit R126 (2)): each use of the session moves this to 30 days from now, and 30 days unused ends it. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Send me a code (primary button) | `requestGuestOtp` POST `/auth/guest/otp` | inline | inline | — | opens modal first |
| Sign in with the code (primary button) | `verifyGuestOtp` POST `/auth/guest/otp/verify` | inline | GuestSession | — | opens modal first |
| Sign in with password (secondary button) | `guestPasswordLogin` POST `/auth/guest/password` | inline | GuestSession | 400 Validation failed | opens modal first; produces a document or message: Sign in with an email or mobile and a password |
| Continue with Apple or Google (secondary button) | `guestSocialLogin` POST `/auth/guest/social` | inline | GuestSession | — | — |
| Continue with UAE Pass (secondary button) | `guestUaePassLogin` POST `/auth/guest/uae-pass` | inline | GuestSession | — | — |
| Create an account (secondary button) | `registerGuest` POST `/auth/guest/register` | RegisterGuestRequest | GuestSession | 409 Identifier already registered. Deliberately indistinguishable in timing from success — a registration endpoint that reveals which addresses exist is an account … | opens modal first |
| Sign out (secondary button) | `guestLogout` DELETE `/auth/guest/session` | — | — | — | — |
| Link an order I placed as a guest (secondary button) | `linkGuestCheckout` POST `/auth/guest/link-checkout` | inline | inline | 403 Contact detail on the order does not match the verified identifier | opens modal first |
| Keep my cart (secondary button) | `claimCart` POST `/carts/{cartId}/claim` | — | CartMergeResult | — | — |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Header entry point**: A single profile icon opens this screen on the Sign in tab; signed-in guests get their account menu from the same icon. Tabs read Sign in and Create account. *(source: DI-974)*
- **Checkout gate copy**: Arriving from checkout with guest checkout off, the screen opens with "This venue requires an account for checkout. Your basket is kept." and no guest button. With guest checkout on, "Continue as guest" sits under the code option. *(source: DI-1034; DI-1043; REV3-3)*
- **Who is signed in on this device**: Shown only when a guest session already exists on this browser: display name and masked contact, with Sign out so a shared device is handed over clean. Never shows the subject id or token expiry. *(source: screens/P01-guest-web-storefront.yaml#WEB-016)*

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Send me a code**: Always "We sent a code to f•••@gmail.com if an account can use it" style success, the same whether the identifier exists or not; resend is offered after 30 seconds; 429 says when to try again. *(source: contracts/spine/identity.yaml#requestGuestOtp)*
- **Sign in with the code / with password**: Success returns to the screen the guest came from with the cart claimed to the account (claimCart) and the browser's cookie decision attached (claimDeviceConsent). A password refusal is one message for wrong password, unknown account, no password and locked; locked or 429 adds "use a one-time code instead". *(source: contracts/spine/identity.yaml#guestPasswordLogin; contracts/spine/orders.yaml#claimCart; contracts/satellite/marketing-crm.yaml#claimDeviceConsent)*
- **Continue with Apple or Google / UAE Pass**: Hands off to the provider's own sheet or the UAE Pass redirect (mobile number, push approval, biometrics) and returns here to finish; UAE Pass arrives verified and pre-fills the guest's verified name. A provider email matching an existing account links to it rather than creating a duplicate. *(source: contracts/spine/identity.yaml#guestUaePassLogin; contracts/spine/identity.yaml#guestSocialLogin; DI-123)*
- **Verification code (two-step)**: Only when the returned session has requiresMfa: at a venue that switched guest two-step verification on, for a guest who enrolled. A guest who signed in with an emailed code is never offered email as the second factor. Never for UAE Pass. *(source: contracts/spine/identity.yaml#createMfaChallenge; DI-1072)*
- **Link an order I placed as a guest**: Asks the booking reference and the code from its confirmation; attaches it and every other guest-checkout order with the same verified contact, and says how many were attached. A contact mismatch is refused 403 and worded as "this booking was made with a different email or mobile". *(source: contracts/spine/identity.yaml#linkGuestCheckout; F56 step 3)*

**Data it reads**: `getGuestSession` (onLoad, Read the current guest session Only when signed in (decided …); `refreshToken` (background, Rotate the access token)

**Where the user goes next**

- → `WEB-017` My Account Dashboard: *My Account Dashboard*; carries `token`
- → `WEB-018` My Tickets: *My Tickets*
- → `WEB-019` Order History: *Order History*
- → `WEB-010` Shopping Cart: *Signed in and verified — back to the cart*; carries `cartId`; only when arrived from the cart
- → `WEB-011` Guest Details & Attendee Forms: *Guest Details & Attendee Forms*
- → `WEB-012` Checkout — Payment: *Checkout — Payment*
- → `GST-039` Profile: *They set a profile*; carries `subjectId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Checking whether this device already holds a guest session. The sign-in form stays visible. |
| Error (`?state=error`) | Identity could not be reached. **Says so rather than saying the password or code is wrong**, and keeps what was typed. |
| Empty, first run (`?state=emptyFirstRun`) | **Nobody signed in on this device** — the normal state. The form offers a code, a password, Apple or Google and UAE Pass, and Create an account (`registerGuest`). |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025), and this is the screen a guest who is not signed in is sent to, so it has no no-access case of its own. A session that has expired lands here with the screen it came from kept, and returns to it after sign-in. |
| Sign in refused (`?state=signInRefused`) | **One message for every refusal of a password sign-in**: `guestPasswordLogin` answers 401 alike for a wrong password, an unknown identifier, an account with no password and a locked account, and the screen never says which. Too many attempts (429, or the lockout after `PasswordPolicy.lockoutAfterAttempts`) says to try again later and offers **Send me a code** instead (decided 28 September, audit R073 (a)). |
| Offline (`?state=offline`) | **Not available, and the offline banner says why.** Signing in, registering and verifying a code need the server. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Identifier already registered. Deliberately indistinguishable in timing from success — a registration endpoint that reveals which addresses exist is an account …; 409 The key is already claimed by another subject (`already-claimed`); 422 A wrong code, attempts one to four (CHG-R1S-025; the r1 gate found only the fifth failure specified). |

#### Edge cases to draw

- **Session expired mid-booking**: The guest lands here with the screen they came from kept and returns to it after signing in, basket intact. *(source: screens/P01-guest-web-storefront.yaml#WEB-016; ADR-0030)*
- **Registering an identifier that already has an account**: The same "check your email/phone for a code" outcome as a new registration; the code then signs the guest into the existing account. Never "this email is already registered". *(source: contracts/spine/identity.yaml#registerGuest)*
- **Identity service unreachable**: Says the service could not be reached and keeps what was typed; never says the code or password is wrong. *(source: screens/P01-guest-web-storefront.yaml#WEB-016)*
- **Offline**: Not available; the offline banner says signing in needs a connection. *(source: screens/P01-guest-web-storefront.yaml#WEB-016)*

#### Consistency with other screens

- Match `GST-042`: Same methods, same order, same wording and the same six-digit rule; the app is the same door in a different shell.
- Match `WEB-012`: The checkout gate and the guest-checkout code use this screen's code step, not a second implementation.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
identifier: fatima.mansoori@gmail.com
mobile: +971 50 412 7789
maskedTarget: f•••@gmail.com
code: '482913'
displayName: Fatima Al Mansoori / فاطمة المنصوري
linkOrder:
  orderReference: AQC-AUH-260930-0412
  verificationCode: 7Q4K2M
  attachedOrderCount: 3
```

#### Permissions

- `registerGuest` → no permission · anonymous
- `getGuestSession` → no permission · guest
- `guestLogout` → no permission · guest
- `guestPasswordLogin` → no permission · anonymous
- `guestSocialLogin` → no permission · anonymous
- `guestUaePassLogin` → no permission · anonymous
- `linkGuestCheckout` → no permission · guest
- `refreshToken` → no permission · staff, partner, guest
- `requestGuestOtp` → no permission · anonymous
- `verifyGuestOtp` → no permission · anonymous
- `claimCart` → no permission · guest
- `createMfaChallenge` → no permission · staff, partner, guest
- `verifyMfaChallenge` → no permission · staff, partner, guest
- `claimDeviceConsent` → no permission · guest

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025), and this is the screen a guest who is not signed in is sent to, so it has no no-access case of its own. A session that has expired lands here with the screen it came from kept, and returns to it after sign-in.

#### Requirements it meets

15 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.1 | User Registration - System shall support user registration. | Guest Mobile App & Branding | CONTRACTED | `registerGuest` |
| 2.6.20 | - Single Sign On Registration | Ticketing Sales | CONTRACTED | `registerGuest` |
| 2.6.28 | A online sale can be done using Guest Checkout or Registration on the website or Login to SSO. This should be configurable per site based on the client requirements. | Ticketing Sales | CONTRACTED | `registerGuest` |
| 19.2.2 | User Login - System shall support user login. | Guest Mobile App & Branding | CONTRACTED | `getGuestSession` |
| 2.6.29 | If the customers require to have access to this account, this account shall have a login and password in order to recall previous transactions. | Ticketing Sales | CONTRACTED | `getGuestSession` |
| 19.2.3 | Social Login - System shall support social login. | Guest Mobile App & Branding | CONTRACTED | `guestSocialLogin` |
| 19.2.4 | Apple Login - System shall support Apple Sign-In. | Guest Mobile App & Branding | CONTRACTED | `guestSocialLogin` |
| 19.2.5 | Google Login - System shall support Google Sign-In. | Guest Mobile App & Branding | CONTRACTED | `guestSocialLogin` |
| 5.3.6 | The system should allow linking of guest accounts with social media logins. | F&B & Guest Management | CONTRACTED | `guestSocialLogin` |
| 2.6.66 | Customer should be able to login through UAE Pass and all the customer details should be captured and saved as profile information | Ticketing Sales | CONTRACTED | `guestUaePassLogin` |
| 2.6.67 | B2C Ticketing website should support the following: - Guest Checkout - Loing through Apple ID - Login through Google ID - Login through UAE Pass - Login through SSO - Login through Registered Account | Ticketing Sales | CONTRACTED | `guestUaePassLogin` |
| 5.3.3 | The system should be able to accept checkout for guests that do not wish to create an account in order to complete an order. Minimum required information as configured (e.g. email address) will still … | F&B & Guest Management | CONTRACTED | `linkGuestCheckout` |
| … 3 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Web screens carry: cart promo code (valid/invalid/expired) and empty basket with confirm; interrupted-payment recovery ("we are checking with your bank" → success/failed/unknown); reprint/resend tickets; UAE Pass sign-in, link guest checkout, sign out; support cases and Sahli handoff; FX rates with timestamp; remaining entitlements. *(agreed · design review 29 Sep 2026, GAP-B3 · B. Web — missing functions on existing screens · DI-1074)*
- Guest two-step verification is a per-venue setting, off by default. Enrolment lives on the guest's tenant-wide account; the second factor is asked only when signing in or acting at a venue that enables it. Guests never see enterprise SSO. *(agreed · design review 29 Sep 2026, GAP-B1 · B. Login: set up two-step verification; C. Security & Sign-in (step-up auth) · DI-1072)*
- Sign-in (or the guest code when guest checkout is on) is asked when the guest leaves the Add-ons step; the basket is kept. Setting "Ask to sign in": After add-ons (default) or At payment. *(agreed · rev 3 design review 29 Sep 2026, REV3-3 · 3. The sign-in screen should appear after Add-ons · DI-1043)*
- After the code, a match prompt shows what matched (e.g. 4 past orders, first order 12 Mar 2024, profile type), never the other profile's name or details, with "Use this profile" / "Not me – keep separate". Expired state: "This match has expired – continue as a new guest." *(agreed · design review 29 Sep 2026, 1. Guest checkout, code proof, profile matching (WEB-012) · DI-1035)*
- Guest checkout is a venue toggle, off by default: off = sign-in screen at payment ("This venue requires an account for checkout. Your basket is kept."), guest button hidden. On = "Continue as guest" with email or mobile (per "Match returning guests by") and a code; only exactly six digits accepted, copy says six. *(agreed · design review 29 Sep 2026, 1. Guest checkout, code proof, profile matching (WEB-012) · DI-1034)*
- The guest-checkout email pop-up collects only the fields configured in the back end (email, phone and/or name). After the code is verified, do not ask for name/email/phone again: go straight to T&Cs and complete the booking; profile is created and can be completed later (Platinumlist pattern). *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W1 Guest checkout · DI-1002)*
- At checkout guests can sign in, register (with a visible loyalty-points incentive) or continue as guest; terms acceptance is implied by proceeding to payment, with no separate checkbox. *(client request · MoM 31 Aug 2026, 4.13 UX Reference Walkthrough (Little Explorer) · DI-588)*
- Decision: at least one of e-mail or mobile number is mandatory at profile creation (not both — some customers decline e-mail); the system supports conditional "either/or" mandatory-field rules. *(agreed · MoM 20 Aug 2026, 4.1 CRM; 5. Key Decisions · DI-372)*
- Sign-up by phone number or email, verified by OTP (WhatsApp or SMS/email as configured), then minimal profile (first/last name). *(client request · MoM 10 Aug 2026, 4.7 Account Creation, Localisation & Multi-Currency · DI-209)*
- UAE Pass login: customer enters mobile number, approves a push notification, confirms with biometrics; verified personal details are pulled into the booking automatically and a linked account is created. *(agreed · MoM 3 Aug 2026, 9. Website Structure, Localization & Authentication · DI-123)*
- Checkout supports guest checkout, registered-account checkout, and single sign-on (e.g. Okta, Azure AD, a ticketing-specific SSO). *(agreed · MoM 3 Aug 2026, 9. Website Structure, Localization & Authentication · DI-121)*

Also apply: 1 for P01 · Account & Self-Service, 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

**Specific to this screen** (the tenant's setting is the input; the right column is what it changes here). Draw each with its default, and the alternate where the alternate theme sets one.

*Booking settings (tenant, with per-venue overrides)*, set in `CMS-016` Site Settings:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Guest contact fields (`bookingFlow.guestContactFields`) | Email · Mobile · Name; at least 1; at most 3; no duplicates; Must include the contact the guest's code is sent to and matched on (identity `GuestMatchPolicy.; matchBy`), or 400. | Email | What the guest-checkout pop-up asks, and nothing else (decided 29 September, W1). |
| Settings: guest contact fields (`bookingFlow.venueOverrides[].settings.guestContactFields`) | Email · Mobile · Name; at least 1; at most 3; no duplicates; Must include the contact the guest's code is sent to and matched on (identity `GuestMatchPolicy.; matchBy`), or 400. | Email | What the guest-checkout pop-up asks, and nothing else (decided 29 September, W1). |

*Cookie banner*, set in `CMS-026` Cookie Banner & Preference Center Designer:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Buttons: action (`cookieBanner.buttons[].action`) | Accept all · Reject non essential · Manage preferences · Save preferences · Do not sell or share | — | — |

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-016` · status **review** · provenance client-verified
- Prototype (rev 3 (pointer moved to the 30 September build, CHG-R1S-015), verified 2026-09-28, match partial): `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`, view *Header profile icon (signed out), or automatically when leaving Add-ons / at payment*. Differences: No password sign-in and no mobile-number OTP (YAML has guestPasswordLogin and 'Email or mobile number'); it is a modal, not a page. Account → Security still shows 'Two-step verification' and passkeys, which the YAML ruled out for guests (R167). Guest checkout route belongs to WEB-012 in the prototype.
- Flow F56 *A guest registers, verifies and sets preferences*, step 3: A guest who checked out anonymously links their order. → **This is the operation that stops duplicates.** A guest who bought without an account and registers afterwards is one person — and without this they are two, which is what `mergeGuests` then has to …
- Flow F01 branch at step 4 (recoverable): when The guest is not signed in and leaves the ticket step (or Add-ons, where the booking has one), With the published flow's `settings.signInAt` `afterAddOns` (the default; read with `getPublishedBookingFlow`, W12) the guest is asked to sign in, or for a guest code when guest checkout is on …
- Flow F01 branch at step 4 (recoverable): when The guest checks out as a guest (guest checkout on for the venue), The pop-up asks only `BookingFlowSettings.guestContactFields` (email, and name or mobile where configured), then the six-digit code. After the code nothing is asked again: the cart goes to WEB-012 …
- Flow F56 branch at step 3 (high): when The anonymous order cannot be matched., **Left unlinked rather than guessed.** Linking the wrong order gives a stranger somebody else’s ticket.
- ADR-0002 *Authorisation is user-driven, not workstation-driven* (`docs/adr/0002-authorisation-is-user-driven-not-workstation-driven.md`)
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0045 *Every order carries a proven contact, and the gate is the checkout page* (`docs/adr/0045-every-order-carries-a-proven-contact.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (35), with its required mark, default, format and its error state (400, 403, 404, 409, 410, 422).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-016?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, signInRefused, offline.
- [ ] Every action is wired with its success and its failure: Send me a code, Sign in with the code, Sign in with password, Continue with Apple or Google, Continue with UAE Pass, Create an account, Sign out, Link an order I placed as a guest, Keep my cart.
- [ ] Every transition is wired: `WEB-017`, `WEB-018`, `WEB-019`, `WEB-010`, `WEB-011`, `WEB-012`, `GST-039`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 11 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 4 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `WEB-017` My Account Dashboard

**Everything I have with this venue at a glance: bookings, wallet, loyalty, challenges and invitations, each opening its own pane.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Account & Self-Service · wave 1 · needs the `marketing` module |
| Block | Block A · task APP-WEB-WEB-017 |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · the venue's theme |
| Pattern | listDetail (compact density): `listGuestDevices` reads the population and `getWishlist` reads one of them — list, select, act |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | `subjectId` (session), `token` (deepLink) · cold entry: **A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared ticket, a forwarded confirmation … |
| Route | `/account-and-self-service/my-account-dashboard` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Drawn 26 August** — `Dashboards Board` frame `web-017`. **One board draws five dashboards across five platforms** — platform admin, partner, support, guest web and cross-tenant health. A dashboard is a shape rather than a domain, and the pack recognised that before the package did. **The loyalty tile's programmeId comes from listLoyaltyProgrammes (4 October 2026)** (CHG-FXS-003) **The loyalty programme is picked from listLoyaltyProgrammes when there are several** (CHG-FXS-003)

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The signed-in guest's account home on the web. Tiles show upcoming bookings, wallet, loyalty position, active challenges, invitations, and shortcuts to profile, privacy, newsletters, cases and wishlist. Each tile loads and fails on its own. The prototype makes the account one page with section panes, and the other account screens are panes of it.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- getMyChallenges has no response schema. (CHG-SGU-024)

**Fixed on main** (the package already carries these; draw what it says): WEB-017 declares the wishlist and device operations and recordConsent as action-bar buttons (Add to wishlist, Register guest device, Revoke … (CHG-SGU-017); Upcoming bookings, wallet and orders tiles have no operation on this screen. (CHG-SGU-017).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Programme | picker: choose an id | optional | — | — | shows names, sends the id | Shown only when the venue runs more than one; the first active one otherwise. | `LoyaltyProgramme.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| State | radio group | Usable now | Usable now · Upcoming · Expired · All | `listMyEntitlements` ?state |
| Include shared | toggle | on | — | `listMyEntitlements` ?includeShared |
| Since | date picker | — | — | `listMyOrders` ?since |
| Programme | picker: choose a programme | — | — | `getLoyaltyPosition` ?programmeId |

**Form: Respond to invitation** (modal, opened by *Respond to invitation*; *Respond to invitation* calls `respondToInvitation`, *Cancel* sends nothing)

**Collects what `respondToInvitation` sends before it is called.** Required: `response`. Optional: `plusOnes`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Response `response` | segmented control | required | — | Accept · Decline | — | — | `respondToInvitation` body |
| Plus ones `plusOnes` | number field | optional | 0 | — | — | — | `respondToInvitation` body |

Errors to draw in the form: 409 Already answered, expired or revoked — the token is single-use — or an acceptance when the campaign's `quota` of places is taken. (InvitationResponseProblem)

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Invitation response**: Accept or decline, with plus-ones only if the invitation allows them. The link token is single-use, so a second click shows the response already given. Accepting issues the entitlement, which then appears under bookings. *(source: contracts/satellite/marketing-crm.yaml#respondToInvitation)*

#### Outputs: what the screen shows and produces

**Shown**

**Upcoming bookings** (metric tile, from `listMyEntitlements`): Next visits; opens WEB-018.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | A UUIDv7, matching `TicketStatus.ticketId` — stable for the life of the ticket and independent of the media carrying it. |
| Template | the name it points at, never the id | The definition it was issued against. Pinned at issue — a template edited next month must not change what this guest bought. |
| Product | the name it points at, never the id | — |
| Order | the name it points at, never the id | The order's id, a UUIDv7 as in `/orders/{orderId}` (`orders.sales_order.id`). Null for an entitlement an invitation issued (`invitationId` … |
| Order line | the name it points at, never the id | — |
| Subject | the name it points at, never the id | Who holds it. Null is legitimate — a ticket bought as a gift or sold at a till to somebody who gave no details has no subject until it is … |
| Venue | the name it points at, never the id | — |
| Media code | text | What is scanned — a QR payload, a wristband serial, a card number. Rotatable without reissuing, because a guest whose wristband broke … |
| Status | chip: Issued, Partially consumed, Fully consumed, Expired, Cancelled, Surrendered | What the storage layer holds, and what a guest is shown. `MediaEntitlements` carried only `isValid` and a reason string — a boolean cannot … |
| Status note | text | Not `TicketStatus` — that is a validation result with a misleading name, computed at scan time and carrying `isValid` and `isInsideVenue`. |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | Resolved at issue from the template, then owned here. A freeze extends it, a reissue replaces it, and neither reaches back to the template. |
| Entries used | 1,234 | The number `validateAccess` decrements and nothing was decrementing. A ten-entry pass with no counter is a ten-entry pass that admits … |
| Entries allowed | 1,234 | — |
| Last entry at | 1 Oct 2026, 14:30 | `recordedAt` of the latest admission counted in `entriesUsed`, written by the same writes. |
| First entry at | 1 Oct 2026, 14:30 | `recordedAt` of the first admission, written by the same writes as `lastEntryAt`; it starts a time-bound entitlement's window (DEC-232 … |
| Time bound until | 1 Oct 2026, 14:30 | Where the template is time-bound, when its window closes: `firstEntryAt` plus the validity rule's `minutesAfterFirstScan` (decided 2 … |
| Lifecycle label | chip: Created, Pending fulfillment, Active, Partially used, Used, Expired… | The Virtual Ticket status in the client's 13 names, mapped onto the entitlement model (decided 2 October 2026, Chinmay, critical set 2 … |
| Cancellation kind | chip: Voided, Refunded, Performance cancelled, Superseded | Which act cancelled the entitlement, so the pack's Voided, Refunded and Reissued / superseded are told apart while `status` keeps the one … |

**Orders** (metric tile, from `listMyOrders`): Recent orders; opens WEB-019.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | The client UUIDv7 from `CreateOrderRequest.id`. |
| Order number | text | The number a guest reads and a cashier types. Server-assigned: the venue prefix and a sequence per venue, for example `DXB1-000123` … |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for … |
| Venue | the name it points at, never the id | — |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Net amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunded amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Charge currency | text | The currency the guest selected and is charged in (CHG-FIN-001, 2 October 2026). |
| Charge FX rate | text | Units of `chargeCurrency` per one unit of the base currency, from the region's `tender` rate in force at checkout (`finance.FxRate`) … |
| Charge FX rate | the name it points at, never the id | The `finance.FxRate` row the rate was taken from, for audit. |
| Charge total | AED 1,234.50 | `grossAmount` converted at `chargeFxRate` and rounded to the charge currency's scale: what the guest pays and what the payment request to … |
| Charge rate locked until | 1 Oct 2026, 14:30 | The quote holds until then (the cart lease). After it, the next payment attempt re-quotes at the rate then in force and the guest confirms … |
| Dropped promotions | list or chips (count when long) | Promotions left off this order at checkout because their budget cap would have been exceeded (decided 28 September, audit R101 (8)). |
| Promotion | the name it points at, never the id | — |
| Name | text | — |

**Wallet** (metric tile, from `getWallet`): Balance; opens WEB-021.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Subject | the name it points at, never the id | — |
| Balance | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Credits | list or chips (count when long) | 4.3.5 and 4.3.19. One balance and one bonus balance with one expiry could not express what the requirement asks for — cash, bonus and … |
| Kind | chip: Cash, Bonus, Redemption, Refund, Goodwill | `cash` is money the guest paid and the others are not. That distinction decides what is refundable, what expires, and what shows as a … |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Expires at | 1 Oct 2026, 14:30 | — |
| Source ref | text | — |
| Is refundable | yes / no (icon or chip) | True only for `cash`. A guest cannot cash out a promotional credit, and a wallet that lets them has given away the promotion twice. |
| Bonus balance | AED 1,234.50 | Promotional value. Typically non-refundable and spent first. |
| Currency | text | — |
| Status | chip: Active, Suspended, Closed | — |
| Home cell name | text | Where the authoritative balance lives. Present when the guest is linked across cells. |
| Expires at | 1 Oct 2026, 14:30 | — |
| Last activity at | 1 Oct 2026, 14:30 | — |

**Loyalty** (metric tile, from `getLoyaltyPosition`): The guest's position in the programme from listLoyaltyProgrammes (the first active one).

| Shows | Format | Notes |
|---|---|---|
| Subject | the name it points at, never the id | — |
| Programme | the name it points at, never the id | — |
| Points balance | 1,234 | — |
| Points pending | 1,234 | Earned and not yet cleared — a purchase inside the refund window. Summed at read from the guest's `marketing.loyalty_points` accruals whose … |
| Tier | text | — |
| Next tier | text | The name of the next `MarketingProgrammeTier` by `rank` above the guest's current tier, resolved at read. |
| Points to next tier | 1,234 | — |
| Expiring points | 1,234 | — |
| Expiring at | 1 Oct 2026, 14:30 | Points that lapse unannounced are a complaint. The date is returned so the interface can warn before it happens. |

**The challenge** (detail panel, from `getMyChallenges`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Kind | chip: Visit, Spend, Ride, Collection, Streak, Referral… | What an entrant does to progress. `scan`, `activity` and `purchase` were added from the BO-825 pack (decided 28 September, audit R275 (c)) … |
| Reward kind | chip: Badge, Loyalty points, Wallet credit, Voucher, Entitlement, None | 22.6.13. A reward that issues wallet credit is money, and it goes through the same stored-value mechanism as everything else rather than a … |
| Reward value | 1,234 | Points, for `rewardKind: loyaltyPoints` only. A count, not an amount — a money reward is `rewardAmount`, never this. |
| Reward amount | AED 1,234.50 | The credit, for `rewardKind: walletCredit` only. The shared `Money`, stored as `numeric(18,4)` with currency and scale resolved from the … |
| Starts at | 1 Oct 2026, 14:30 | — |
| Ends at | 1 Oct 2026, 14:30 | — |
| Status | chip: Draft, Active, Paused, Ended, Archived | — |

**The wishlist** (detail panel, from `getWishlist`): A shortcut tile with the count; opens WEB-009.

| Shows | Format | Notes |
|---|---|---|
| Subject | the name it points at, never the id | — |
| Items | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Respond to invitation (secondary button) | `respondToInvitation` POST `/invitations/{token}/respond` | inline | Invitation | 409 Already answered, expired or revoked — the token is single-use — or an acceptance when the campaign's `quota` of places is taken. (InvitationResponseProblem) | opens modal first |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Loyalty tile**: Tier, points, and points to the next tier as a progress bar; expiring points with their date if any expire within 30 days. Links to WEB-043. *(source: F53 step 1; contracts/satellite/marketing-crm.yaml#getLoyaltyPosition)*
- **Challenges tile**: Each active challenge with its progress (2 of 3 visits), not just the outcome, because progress is what changes behaviour. *(source: contracts/satellite/marketing-crm.yaml#getMyChallenges)*
- **Complete your details banner**: For a profile created by guest checkout, a dismissible prompt to add what the checkout pop-up did not ask. It never blocks anything. *(source: DI-1002; screens/P01-guest-web-storefront.yaml#WEB-020)*
- **Consent reminder**: If getGuestConsents reports a consent given against a superseded notice, show "Our privacy notice changed - review your choices" linking to the profile's consent section. *(source: contracts/satellite/marketing-crm.yaml#getGuestConsents)*

**What each action does** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Open a tile**: Goes to the owning screen (WEB-018 bookings, WEB-019 orders, WEB-043 loyalty, WEB-020 profile, WEB-024 devices and privacy). *(source: screens/P01-guest-web-storefront.yaml#WEB-017)*

**Data it reads**: `getWishlist` (onLoad, Read a guest's saved items); `getMyChallenges` (onLoad, Outstanding security challenges); `listMyEntitlements` (onLoad, Upcoming bookings tile); `listMyOrders` (onLoad, Orders tile); `getWallet` (onLoad, Wallet tile); `getLoyaltyPosition` (onLoad, Loyalty tile); `listLoyaltyProgrammes` (onLoad, The venue's loyalty programme, whose id getLoyaltyPosition …)

**Where the user goes next**

- → `WEB-016` Login / Register: *Login / Register*; carries `challengeId`, `subjectId`
- → `WEB-018` My Tickets: *My Tickets*; carries `entitlementId`, `orderId`
- → `WEB-019` Order History: *Order History*; carries `orderId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Tiles skeleton |
| Error (`?state=error`) | Partial. Each tile fails independently |
| Empty, first run (`?state=emptyFirstRun`) | A new account with no orders — offers what to do next |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listGuestDevices` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `MARKETING_VIEW`, which `getMyChallenges` requires to show this screen, and names that permission (the screen's other reads need `ORDER_VIEW`, `WALLET_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `GUEST_VIEW` for `respondToInvitation`. |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Already answered, expired or revoked — the token is single-use — or an acceptance when the campaign's `quota` of places is taken. (InvitationResponseProblem) |

#### Edge cases to draw

- **One tile's read fails**: That tile shows "Could not load - retry"; the rest of the page works. *(source: screens/P01-guest-web-storefront.yaml#WEB-017)*
- **Brand-new account with no orders**: Offers what to do next (Browse tickets, Complete your details), not empty tiles. *(source: screens/P01-guest-web-storefront.yaml#WEB-017)*

#### Consistency with other screens

- Match `GST-039`: The app's account home holds the same tiles in the same order and with the same labels.
- Match `WEB-043`: The loyalty tile and the loyalty page use the same tier badge and progress bar.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
guest: Rahul Menon
loyalty:
  tier: Silver
  points: 2340
  toNext: 660 to Gold
  expiring: 150 points on 31 Oct 2026
challenge: Visit 3 times this autumn - 2 of 3
invitation: Coastal Aqua Members' Night, Thu 5 Nov 2026 19:00, plus one allowed
```

#### Permissions

- `getWishlist` → no permission · guest
- `getMyChallenges` → `MARKETING_VIEW` (read) · staff, guest
- `respondToInvitation` → `GUEST_VIEW` (read) · guest, public
- `listMyEntitlements` → `ORDER_VIEW` (read) · staff, guest
- `listMyOrders` → no permission · guest
- `getWallet` → `WALLET_VIEW` (read) · staff, guest
- `getLoyaltyPosition` → no permission · guest
- `listLoyaltyProgrammes` → `MARKETING_VIEW` (read) · staff, guest

**A refused user sees:** Shown when the caller lacks `MARKETING_VIEW`, which `getMyChallenges` requires to show this screen, and names that permission (the screen's other reads need `ORDER_VIEW`, `WALLET_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `GUEST_VIEW` for `respondToInvitation`.

#### Requirements it meets

56 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.9 | Digital Wallet - System shall provide a digital wallet. | Guest Mobile App & Branding | CONTRACTED | `getWallet` |
| 1.1.105 | Stored value card management | Ticketing Catalogue | CONTRACTED | `getWallet` |
| 1.1.108 | Balance enquiry | Ticketing Catalogue | CONTRACTED | `getWallet` |
| 1.1.111 | Expiry management | Ticketing Catalogue | CONTRACTED | `getWallet` |
| 2.6.48 | System shall provide one unified wallet experience across website, mobile app, POS, kiosk, and membership channels. The wallet shall show stored value, vouchers, loyalty points, membership benefits … | Ticketing Sales | CONTRACTED | `getWallet` |
| 2.13.34 | Digital Wallet Integration | Ticketing Sales | CONTRACTED | `getWallet` |
| 4.3.7 | The system should allow guests to use their digital wallet to make online and in-app purchases (through API integrations), buy tickets of all type or purchase any service within venue such as retail … | Bundles and Promotions | CONTRACTED | `getWallet` |
| 4.3.8 | The system should provide a digital wallet that allows: - multiple channels for payments, including but not limited to the Mobile app and wearable (which is linked to the digital wallet). - multiple … | Bundles and Promotions | CONTRACTED | `getWallet` |
| 4.3.13 | The system should allow guests to make in-store and attraction payments using digital wallets via contactless methods as RFID, NFC and QR-code. | Bundles and Promotions | CONTRACTED | `getWallet` |
| 4.3.20 | The system should enable usage of wallet by other systems through integration. All functionalities of the wallet such as credit redemption, balance check and wallet funding should be available … | Bundles and Promotions | CONTRACTED | `getWallet` |
| 4.3.22 | Support cashless stored-value balances. | Bundles and Promotions | CONTRACTED | `getWallet` |
| 4.3.23 | Support gift card balances. | Bundles and Promotions | CONTRACTED | `getWallet` |
| … 44 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Web account gets device management and "sign out a lost device" (WEB-024). Face Pass stays mobile-only until the facial-reader vendor SDK supports web capture. *(agreed · design review 29 Sep 2026, GAP-D1 · D. Mobile-only features get web equivalents · DI-1077)*

Also apply: 1 for P01 · Account & Self-Service, 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-017` · status **review** · provenance client-verified · **Drawn by Claude Design on `Dashboards Board.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Prototype (rev 3 (pointer moved to the 30 September build, CHG-R1S-015), verified 2026-09-28, match exact): `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`, view *Sign in → avatar menu → 'Account overview'*. Differences: Prototype makes the account a single page with section panes; most YAML account screens (019–024, 026, 027, 030, 031, 034) are panes of it. Groups & invitations (respondToInvitation, getMyChallenges, referral code) sits here. Signed-out state 'Sign in to see your account' is drawn.
- Derived from `wireframes/reference/Dashboards Board.dc.html`
- Client design-board frames: `Dashboards Board.dc.html#web-017`
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (74 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-017?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Respond to invitation.
- [ ] Every transition is wired: `WEB-016`, `WEB-018`, `WEB-019`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `WEB-018` My Tickets

**Find my tickets for this venue.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Account & Self-Service · wave 1 · needs the `access` module |
| Block | Block A · task APP-WEB-WEB-018 |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · the venue's theme |
| Pattern | listDetail (compact density): `listMyEntitlements` reads the population and `getEntitlement` reads one of them — list, select, act |
| Offline | **The offline banner shows.** Tickets already loaded stay visible with their age, and a ticket's rotating code is derived on the device from its seed, so it changes with no signal (decided 28 September, audit R230). Sharing, transferring and adding to a phone wallet need the connection. |
| Opens with | `subjectId` (session), `entitlementId` (deepLink), `orderId` (deepLink) · cold entry: **A ticket link opened after the event.** Shows the entitlement with its status — expired, used, transferred — because *not found* to somebody holding a ticket … |
| Route | `/account-and-self-service/my-tickets` |

**What the spec says about it.** Dynamic QR with a visible countdown: a rotating code derived in the page from the `rotation` seed that `getEntitlementCredential` returns, with the seconds to the next step shown (audit R230). **No screenshot blocking on the web** — a browser cannot enforce it, so the page promises none (decided 28 September, audit R077 (c)). Purpose derived from the screen name and its operations on 17 August, not from a requirement. The read surface Deep asked for. **All four were missing and the table itself did not exist until 18 August.** **Rewired on the 20 August review.** **`listEntitlements` wired 24 August, raised in review.** The staff-scoped list was on this guest screen — **a guest-facing list must be scoped to the caller, not filtered by a subject parameter**, or a guest is one parameter away from somebody else’s. **Cross-surface parity, 31 August**: added transferOrderTickets. **The same screen on web and app was calling different operations** — one side could do something the other could not, and nothing recorded the difference as deliberate.

**Known gaps.** **`getEntitlementCredential` declares its response inline**, so the component that shows it names fields but binds to no schema. The contract should name the shape. **`getEntitlementHistory` declares its response inline**, so the component that shows it names fields but binds to no schema. The contract should name the shape.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The guest's tickets on the website, seen from the gate's side: what will work today is at the top, each ticket shows its scan code and how many entries are left, and the full history answers "it says I already used it". The one thing to get right: for a dynamic-QR event the website does not show a working code; it sends the guest into the app to activate it, and says why.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- getEntitlementCredential and getEntitlementHistory responses are inline (no named schema) (CHG-SGU-024)

**Fixed on main** (the package already carries these; draw what it says): Table columns bind raw Entitlement fields (id, templateId, subjectId, scopePath, orderLineId) (CHG-SGU-021).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should the web show any code at all for a dynamic-QR event once it is activated in the app (e.g. for printing), or always redirect?** → Drawn default accepted: Always redirect to the app for dynamic-QR events (DI-635). *(decided by Chinmay, 2026-10-02; DEC-141 / CHG-NOTE-008)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| State | radio group | optional | Usable now | Usable now · Upcoming · Expired · All | — | Sends `?state=` to `listMyEntitlements`. | `listMyEntitlements` ?state |
| Include shared | toggle | optional | on | — | — | Sends `?includeShared=` to `listMyEntitlements`. | `listMyEntitlements` ?includeShared |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Rotate | toggle | off | — | `getEntitlementCredential` ?rotate |
| Include expired | toggle | on | — | `listEntitlements` ?includeExpired |

**Form: Issue wallet pass** (modal, opened by *Issue wallet pass*; *Issue wallet pass* calls `issueWalletPass`, *Cancel* sends nothing)

**Collects what `issueWalletPass` sends before it is called.** Required: `entitlementId`, `platform`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Entitlement `entitlementId` | picker: choose an entitlement | required | — | — | shows names, sends the id | — | `issueWalletPass` body |
| Platform `platform` | segmented control | required | — | Apple · Google | — | — | `issueWalletPass` body |

**Form: Share entitlement** (modal, opened by *Share entitlement*; *Share entitlement* calls `shareEntitlement`, *Cancel* sends nothing)

**Collects what `shareEntitlement` sends before it is called.** Required: `toSubjectId`. Optional: `validUntil`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| To subject `toSubjectId` | picker: choose a to subject | required | — | — | shows names, sends the id | — | `shareEntitlement` body |
| Valid until `validUntil` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `shareEntitlement` body |

Errors to draw in the form: 409 Not shareable, and the reason says which: the entitlement's template does not allow sharing (`sharingNotAllowed`, `EntitlementTemplate.canShareMedia` false) … (EntitlementRefusedProblem)

**Form: Transfer order tickets** (modal, opened by *Transfer order tickets*; *Transfer order tickets* calls `transferOrderTickets`, *Cancel* sends nothing)

**Collects what `transferOrderTickets` sends before it is called.** Required: `ticketIds`, `recipient`. Optional: `message`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Tickets `ticketIds` | multi-picker: choose tickets | required | — | at least 1 | — | The entitlements to hand over. A ticket is an entitlement, so each value is an `Entitlement.id` on this order — the ids in `OrderLine.entitlementIds`. | `transferOrderTickets` body |
| Recipient `recipient` | group | required | — | — | — | — | `transferOrderTickets` body |
| Channel `recipient.channel` | segmented control | required | — | Email · SMS · Whatsapp | — | — | `transferOrderTickets` body |
| Address `recipient.address` | text field | required | — | — | — | — | `transferOrderTickets` body |
| Message `message` | text area | optional | — | max length 500 | — | — | `transferOrderTickets` body |

Errors to draw in the form: 409 Ticket already redeemed (`alreadyRedeemed`), already offered (`alreadyOffered`), or the product forbids transfer (`transferNotAllowed`). (TicketTransferProblem)

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **State filter**: Tabs, not a dropdown: Usable now (default), Upcoming, Past. "Past" reads the separate history list (used, expired, transferred away); the other two read the current list. Include shared is a toggle "Show tickets shared with me", default on. *(source: contracts/spine/access.yaml#listMyEntitlements / contracts/spine/access.yaml#listEntitlements)*
- **Transfer (recipient, tickets, message)**: Per ticket, never whole order: tick the tickets to hand over, recipient by email or mobile (+971 format hint), optional message (max 500). Only tickets whose product allows transfer are tickable; the others show "Not transferable" beside them. *(source: contracts/spine/orders.yaml#transferOrderTickets / MATRIX 1.1.27)*

#### Outputs: what the screen shows and produces

**Shown**

**My tickets** (card list, from `listMyEntitlements`): One list with tabs, Upcoming and Past: the product, the date, the status in plain words, entries left and the code on opening. No ids, scope, template or order line.

| Shows | Format | Notes |
|---|---|---|
| Product | the name it points at, never the id | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | Resolved at issue from the template, then owned here. A freeze extends it, a reissue replaces it, and neither reaches back to the template. |
| Lifecycle label | chip: Created, Pending fulfillment, Active, Partially used, Used, Expired… | The Virtual Ticket status in the client's 13 names, mapped onto the entitlement model (decided 2 October 2026, Chinmay, critical set 2 … |
| Entries used | 1,234 | The number `validateAccess` decrements and nothing was decrementing. A ten-entry pass with no counter is a ten-entry pass that admits … |
| Entries allowed | 1,234 | — |
| Holder name | text | — |

**Entitlement history** (data table, from `getEntitlementHistory`): Shows `at`, `kind`, `accessPointName`, `denyReason`, `byPrincipalName` from `getEntitlementHistory`'s inline response. **The response has no named schema**, so this cannot bind until the contract names one.

| Shows | Format | Notes |
|---|---|---|
| At | 1 Oct 2026, 14:30 | — |
| Kind | chip: Issued, Scanned, Denied, Frozen, Unfrozen, Shared… | — |
| Access point name | text | — |
| Deny reason | text | — |
| By principal name | text | — |

**Past** (card list, from `listEntitlements`): The Past tab of the same list.

| Shows | Format | Notes |
|---|---|---|
| Product | the name it points at, never the id | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | Resolved at issue from the template, then owned here. A freeze extends it, a reissue replaces it, and neither reaches back to the template. |
| Lifecycle label | chip: Created, Pending fulfillment, Active, Partially used, Used, Expired… | The Virtual Ticket status in the client's 13 names, mapped onto the entitlement model (decided 2 October 2026, Chinmay, critical set 2 … |
| Entries used | 1,234 | The number `validateAccess` decrements and nothing was decrementing. A ten-entry pass with no counter is a ten-entry pass that admits … |
| Entries allowed | 1,234 | — |
| Holder name | text | — |

**The selected entitlement** (detail panel, from `getEntitlement`)

| Shows | Format | Notes |
|---|---|---|
| Media code | text | What is scanned — a QR payload, a wristband serial, a card number. Rotatable without reissuing, because a guest whose wristband broke … |
| Status | chip: Issued, Partially consumed, Fully consumed, Expired, Cancelled, Surrendered | What the storage layer holds, and what a guest is shown. `MediaEntitlements` carried only `isValid` and a reason string — a boolean cannot … |
| Status note | text | Not `TicketStatus` — that is a validation result with a misleading name, computed at scan time and carrying `isValid` and `isInsideVenue`. |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | Resolved at issue from the template, then owned here. A freeze extends it, a reissue replaces it, and neither reaches back to the template. |
| Entries used | 1,234 | The number `validateAccess` decrements and nothing was decrementing. A ten-entry pass with no counter is a ten-entry pass that admits … |
| Entries allowed | 1,234 | — |
| Last entry at | 1 Oct 2026, 14:30 | `recordedAt` of the latest admission counted in `entriesUsed`, written by the same writes. |

**Entitlement credential** (detail panel, from `getEntitlementCredential`): Shows `mediaCode`, `payload`, `expiresAt` from `getEntitlementCredential`'s inline response. **The response has no named schema**, so this cannot bind until the contract names one. **A rotating code derived on the device** (decided 28 September, audit R230): while online the screen fetches `rotation` (secret, `timeStepSeconds`, `digits`, `algorithm`, valid `validFrom` to `validTo`) and computes …

| Shows | Format | Notes |
|---|---|---|
| Media code | text | — |
| Payload | text | — |
| Expires at | 1 Oct 2026, 14:30 | — |
| Rotation | grouped details | The time-based seed the rotating code is derived from (audit R230). Null for a credential that does not rotate (a wristband serial, a … |
| Secret | text | Base32 shared secret. Held on the device and in the gates' offline package; replaced by `rotate=true`. |
| Time step seconds | 1,234 | 30 seconds for an admission QR (Chinmay, 3 October 2026, Block A business rules: GST-055's admission QR rotates every 30 seconds … |
| Digits | 1,234 | — |
| Algorithm | chip: SHA1, SHA256, SHA512 | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | The seed stops verifying after this. The app fetches a fresh one whenever it is online before then. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Transfer order tickets (primary button) | `transferOrderTickets` POST `/orders/{orderId}/transfer` | inline | TicketTransfer | 409 Ticket already redeemed (`alreadyRedeemed`), already offered (`alreadyOffered`), or the product forbids transfer (`transferNotAllowed`). (TicketTransferProblem) | opens modal first; produces a document or message: Transfer tickets to another guest |
| Issue wallet pass (secondary button) | `issueWalletPass` POST `/wallet-passes` | inline | WalletPass | — | opens modal first; produces a document or message: Generate an Apple or Google wallet pass |
| Share entitlement (secondary button) | `shareEntitlement` POST `/entitlements/{entitlementId}/share` | inline | EntitlementShare | 409 Not shareable, and the reason says which: the entitlement's template does not allow sharing (`sharingNotAllowed`, `EntitlementTemplate.canShareMedia` false) … (EntitlementRefusedProblem) | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Ticket card**: Product name, visit date or validity window, venue, holder name when name-bound, and an entries meter "2 of 10 entries left" (entriesAllowed empty = "Unlimited entries"). Status in guest words: Ready to use, Partly used, Used, Expired, Cancelled, Transferred away; frozen passes show "Paused until <date>". Tags per DI-1025 (max 6) under the name. *(source: contracts/spine/orders.yaml#/components/schemas/EntitlementStatus / contracts/spine/access.yaml#getEntitlement / DI-670 / DI-1025)*
- **Scan code panel**: Static QR (or rotating code with a visible seconds countdown when the credential rotates) plus the ticket number printed under it. One ticket shows its linked media together (QR, wristband, Face Pass) rather than separate cards. No screenshot-blocking promise on the web. *(source: contracts/spine/access.yaml#getEntitlementCredential / DI-652 / R230 / R077)*
- **Dynamic-QR event ticket**: Instead of a code: "This event uses a live code in the app. Open the app to activate your ticket", with app-store links and a QR that deep-links to the ticket in the app. *(source: DI-635)*
- **History**: Newest first: date and time (venue time), what happened (Entered at Main Plaza Gate 2, Refused: already used, Shared with Khalid, Transferred), never staff principal ids; a denial shows its reason in the same words the scanner uses (per VO-R06). *(source: contracts/spine/access.yaml#getEntitlementHistory)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Transfer tickets**: Sends a claim link; the ticket shows "Transfer pending until claimed" and stays usable by the sender until the recipient claims it; an unclaimed transfer expires back to the sender. *(source: contracts/spine/orders.yaml#transferOrderTickets)*
- **Share**: Lets one person present the same ticket while the owner keeps it; the owner can revoke, the recipient cannot pass it on. *(source: contracts/spine/orders.yaml#shareEntitlement)*
- **Add to Apple Wallet / Google Wallet**: Generates a live pass for the chosen platform; hidden for dynamic-QR events until activated in the app. *(source: contracts/spine/orders.yaml#issueWalletPass / DI-609 / DI-635)*

**Data it reads**: `listMyEntitlements` (onLoad, Every ticket, pass and membership this guest holds); `getEntitlement` (onLoad, One entitlement, with what remains on it); `getEntitlementCredential` (onLoad, The thing that gets scanned — with the `rotation` seed the …); `getEntitlementHistory` (onLoad, Every scan, freeze, share and reissue against it); `listEntitlements` (onLoad, Every entitlement this guest holds, including expired)

**Where the user goes next**

- → `WEB-016` Login / Register: *Login / Register*; carries `subjectId`
- → `WEB-017` My Account Dashboard: *My Account Dashboard*
- → `WEB-019` Order History: *Order History*; carries `orderId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Tickets load |
| Error (`?state=error`) | Could not load |
| Empty, first run (`?state=emptyFirstRun`) | No tickets — distinguishes never bought from all past |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the current filters. **The filters are named and clearable from here** — an empty list with the filter state hidden elsewhere is a person who thinks the data is gone. **Added 25 August with the derived list component**: a screen that lists has to say what it shows when the list is empty, and this screen gained the list before it gained the sentence. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the … |
| Offline (`?state=offline`) | **The offline banner shows.** Tickets already loaded stay visible with their age, and a ticket's rotating code is derived on the device from its seed, so it changes with no signal (decided 28 September, audit R230). Sharing, transferring and adding to a phone wallet need the connection. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Not shareable, and the reason says which: the entitlement's template does not allow sharing (`sharingNotAllowed`, `EntitlementTemplate.canShareMedia` false) … (EntitlementRefusedProblem); 409 Ticket already redeemed (`alreadyRedeemed`), already offered (`alreadyOffered`), or the product forbids transfer (`transferNotAllowed`). (TicketTransferProblem) |

#### Edge cases to draw

- **Waiver required and not completed**: Card shows "Complete your waiver before entry" with the action, and the code is withheld or marked not yet valid. *(source: DI-574)*
- **Deferred seat assignment**: Card shows section and quantity with "Seats and codes will be emailed before the event"; no code yet. *(source: DI-423)*
- **Entitlement shared with the guest**: Labelled "Shared by <owner first name>"; no transfer or share actions on it. *(source: contracts/spine/access.yaml#getEntitlement)*

#### Consistency with other screens

- Match `GST-012`: Same card, statuses, entries meter and history wording as the app's Tickets tab.
- Match `SCN-003`: Denial wording in the history must equal the scanner's deny labels (VO-R06).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tickets:
- product: Aqua Park Day Pass - Adult
  date: Sat 10 Oct 2026
  status: Ready to use
  entries: 1 of 1
  ticketNumber: VT0010
  media: QR-7F3K-92LD
- product: Summit Peaks Annual Pass
  valid: 1 Oct 2026 - 30 Sep 2027
  status: Partly used
  entries: Unlimited, last entry 28 Sep 18:42
  holder: Sara Al Nuaimi
  media: QR + Face Pass
- product: Falcon Coaster Fast Pass x2
  date: Sat 10 Oct 2026
  status: Ready to use
  entries: 2 of 2
history:
- 28 Sep 2026 18:42 - Entered at Main Plaza Gate 2
- '28 Sep 2026 18:40 - Refused at North Entry: wrong gate, use Main Plaza'
```

#### Permissions

- `listMyEntitlements` → `ORDER_VIEW` (read) · staff, guest
- `getEntitlement` → `ORDER_VIEW` (read) · staff, guest
- `getEntitlementCredential` → `ORDER_VIEW` (read) · staff, guest
- `getEntitlementHistory` → `ORDER_VIEW` (read) · staff, guest
- `listEntitlements` → no permission · guest
- `transferOrderTickets` → no permission · guest
- `issueWalletPass` → `ORDER_VIEW` (read) · staff, guest
- `shareEntitlement` → `ORDER_MODIFY` (operate) · staff, guest

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the …

#### Requirements it meets

8 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.13 | Ticket Transfer - System shall support ticket transfers. | Guest Mobile App & Branding | CONTRACTED | `transferOrderTickets` |
| 1.1.27 | System shall support ticket ownership transfer between guests according to configurable policies, fees and approval workflows. | Ticketing Catalogue | CONTRACTED | `transferOrderTickets` |
| 1.6.17 | System shall expose marketplace functionality through APIs for websites, mobile applications, partner platforms, and third-party integrations. | Ticketing Catalogue | CONTRACTED | `transferOrderTickets` |
| 2.6.39 | Customer should have the ability to view the order transactions with all the details for the logged in users and should be able to resend the tickets / Transfer Tickets to Friend / Download tickets | Ticketing Sales | CONTRACTED | `transferOrderTickets` |
| 2.13.37 | Ticket Transfer & Reassignment | Ticketing Sales | CONTRACTED | `transferOrderTickets` |
| 19.2.14 | Ticket Sharing - System shall support ticket sharing. | Guest Mobile App & Branding | CONTRACTED | `shareEntitlement` |
| 2.14.10 | Manage entitlement balances and usage limits. | Ticketing Sales | CONTRACTED | data `Entitlement` |
| 2.16.15 | The system shall support replacement of lost, damaged, or stolen media while automatically disabling previous media and preserving entitlement history. | Ticketing Sales | CONTRACTED | data `Entitlement` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Web screens carry: cart promo code (valid/invalid/expired) and empty basket with confirm; interrupted-payment recovery ("we are checking with your bank" → success/failed/unknown); reprint/resend tickets; UAE Pass sign-in, link guest checkout, sign out; support cases and Sahli handoff; FX rates with timestamp; remaining entitlements. *(agreed · design review 29 Sep 2026, GAP-B3 · B. Web — missing functions on existing screens · DI-1074)*
- Entitlements portfolio is used both by the guest (mobile app) and by customer service: one view of restrictions, wallet balance and all entitlements; a unified list across a visit (e.g. four admissions, two fast passes, a meal package, a parking entitlement). *(client request · MoM 7 Sep 2026, 4.9 Entitlements Portfolio - Structure, Family/Group & Assignment · DI-667)*
- Any online purchase for a dynamic-QR event must be linked to the mobile app to show the working code; web/desktop purchases are redirected into the app for activation, not exempted. *(agreed · MoM 2 Sep 2026, 4.7 Confirmed (Pradnya's question) · DI-635)*
- Upgrades must be available in the guest mobile/web app: guests view eligible upgrade options and complete the upgrade online without visiting on-site. *(agreed · MoM 1 Sep 2026, 4.9 / 5. Key Decisions · DI-606)*
- Staff can upgrade multiple tickets in one action. "Quick upgrade" is a direct single-path upgrade (gold > platinum); "flexible upgrade" lets the guest choose among several eligible targets. *(client request · MoM 1 Sep 2026, 4.9 Ticket Upgrade & Downgrade Configuration · DI-605)*
- Qossai: where a waiver is required before entry, an incomplete waiver can block ticket download, activation, check-in or access; ticket and scan screens need a waiver-incomplete state. *(agreed · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-574)*
- Decision (raised by Chinmay): date-change/reschedule is a product-level on/off setting with its own policy rules (e.g. allowed up to 24 hours before the visit, denied within 24 hours), not a separate screen. Typically off for special-day tickets (e.g. New Year, 1 January only), on for standard GA. *(agreed · MoM 25 Aug 2026, 4.3 Ticket Type Deep-Dive; 5. Key Decisions · DI-446)*
- Decision: deferred seat assignment — sale confirmed at purchase as section + quantity; seats allocated internally; closer to the event ops/admin trigger a bulk e-mail issuing QR tickets with final seats. Immediate seat assignment remains for venues that need it. *(agreed · MoM 21 Aug 2026, 4.7 Deferred Seat Assignment Model; 5. Key Decisions · DI-423)*

Also apply: 1 for P01 · Account & Self-Service, 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

**Specific to this screen** (the tenant's setting is the input; the right column is what it changes here). Draw each with its default, and the alternate where the alternate theme sets one.

*Footer*, set in `CMS-009` Navigation & Menus:

Also set there, as content the tenant writes: social links: platform.

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-018` · status **review** · provenance client-verified
- Prototype (rev 3 (pointer moved to the 30 September build, CHG-R1S-015), verified 2026-09-28, match partial): `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`, view *Header 'My tickets' → a ticket → 'Manage' (ticket sheet)*. Differences: QR is static — no rotating code with a visible countdown (YAML R230). Prototype adds reschedule, add guests, refund, resale and cancel on the ticket sheet (YAML routes refunds to WEB-019 and transfers to WEB-030).
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (37 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-018?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Transfer order tickets, Issue wallet pass, Share entitlement.
- [ ] Every transition is wired: `WEB-016`, `WEB-017`, `WEB-019`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 8 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `WEB-019` Order History

**Find order history for this venue.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Account & Self-Service · wave 1 · needs the `ticketing` module |
| Block | Block A · task APP-WEB-WEB-019 |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · the venue's theme |
| Pattern | listDetail (compact density): `listMyOrders` reads the population and `getOrder` reads one of them — list, select, act |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | `subjectId` (session), `orderId` (deepLink), `documentId` (navigation), `invoiceId` (navigation) · cold entry: **A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the … |
| Route | `/account-and-self-service/order-history` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **`listMyOrders` wired 24 August, raised in review.** The staff-scoped list was on this guest screen — **a guest-facing list must be scoped to the caller, not filtered by a subject parameter**, or a guest is one parameter away from somebody else’s. **Cross-surface parity, 31 August**: added getOrder, listOrders. **A guest does not know which surface they are on** — the same named screen on web and app now calls the same guest-callable operations. **Tax documents, as the UAE requires them** (research 2 October 2026, CHG-FIN-011; Executive Regulation Art. 59-60): the document a paid order gets is titled "Tax Invoice" (a simplified tax invoice for a guest, a full one with the buyer's name, address and TRN on request), never "Receipt" or "VAT receipt" as the title, and a correction is a "Tax Credit Note" (the contract calls it a credit memo). A simplified tax invoice is issued automatically when the order is paid; a full one is offered for a VAT-registered buyer and is the only kind above AED 10,000 for them. Amounts and VAT are in AED; a guest who paid in another currency sees the amount paid, the currency and the rate as payment information (CHG-FIN-001). A refund shows where the money went and in which currency: "USD 81.72 back to your Visa ending 4417" (CHG-FIN-001).

**Known gaps.** The staff-scoped order list; a guest screen lists the caller's own orders with `listMyOrders` (removed from guest screens on 24 August, back with the 31 August parity pass). Transfer is WEB-030's; order history views, downloads and refunds.

**From the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process.** The signed-in guest's orders at this venue, newest first, with each order's tickets, tax invoice and the two after-sales actions a guest may start (send tickets to someone, ask for a refund). Block A. Get right that it lists only the caller's own orders and that a refund is a request, not a refund.

**Fixed on main** (the package already carries these; draw what it says): The layout carries both "Every order" from listMyOrders and "Every order" from listOrders (the staff-scoped list). (CHG-GST-003).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Since | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?since=` to `listMyOrders`. | `listMyOrders` ?since |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Order | picker: choose an order | — | — | `listTaxInvoices` ?orderId |
| Legal entity | picker: choose a legal entity | — | — | `listTaxInvoices` ?legalEntityId |
| Invoice type | segmented control | — | Simplified · Full · Consolidated | `listTaxInvoices` ?invoiceType |
| Status | radio group | — | Issued · Partially credited · Fully credited · Superseded | `listTaxInvoices` ?status |
| Issued from | date picker | — | — | `listTaxInvoices` ?issuedFrom |
| Issued to | date picker | — | — | `listTaxInvoices` ?issuedTo |
| Tax invoice | picker: choose a tax invoice | — | — | `listCreditMemos` ?taxInvoiceId |
| Refund | picker: choose a refund | — | — | `listCreditMemos` ?refundId |
| Legal entity | picker: choose a legal entity | — | — | `listCreditMemos` ?legalEntityId |
| Issued from | date picker | — | — | `listCreditMemos` ?issuedFrom |
| Issued to | date picker | — | — | `listCreditMemos` ?issuedTo |

**Form: Ask for a refund** (modal, opened by *Ask for a refund*; *Create refund request* calls `createRefundRequest`, *Cancel* sends nothing)

**Collects what `createRefundRequest` sends before it is called.** Required: `orderId`, `reason`. Optional: `lineIds`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Order `orderId` | picker: choose an order | required | — | — | shows names, sends the id | — | `createRefundRequest` body |
| Lines `lineIds` | multi-picker: choose lines | optional | — | — | — | — | `createRefundRequest` body |
| Reason `reason` | text area | required | — | min length 3; max length 1000 | — | — | `createRefundRequest` body |

Errors to draw in the form: 403 Authenticated but not permitted at the requested scope

**Form: Get a tax invoice** (modal, opened by *Get a tax invoice*; *Get a tax invoice* calls `issueTaxInvoice`, *Cancel* sends nothing)

The company name and TRN to put on the invoice, and where to email it; the order is the one selected and the invoice type is full.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Invoice type `invoiceType` | segmented control | required | — | Simplified · Full · Consolidated | — | 5.7.93. `simplified` for one order with no recipient details, `full` for one order with them, `consolidated` for several paid orders of one buyer on one invoice. | `issueTaxInvoice` body |
| Orders `orderIds` | multi-picker: choose orders | required | — | at least 1 | — | One order for `simplified` and `full`; one or more for `consolidated`. Every order must be paid, of one buyer, one legal entity and one currency. | `issueTaxInvoice` body |
| Recipient `recipient` | group | optional | — | — | — | Who the invoice is addressed to. Required for `full` and `consolidated`. | `issueTaxInvoice` body |
| Name `recipient.name` | text area | required | — | max length 300 | — | — | `issueTaxInvoice` body |
| Address `recipient.address` | text area | optional | — | max length 1000 | — | — | `issueTaxInvoice` body |
| Country code `recipient.countryCode` | text field | optional | — | pattern `^[A-Z]{2}$` | — | — | `issueTaxInvoice` body |
| Tax registration number `recipient.taxRegistrationNumber` | text field | optional | — | max length 30 | — | The recipient's TRN where they are VAT-registered. | `issueTaxInvoice` body |
| Customer account `recipient.customerAccountId` | picker: choose a customer account | optional | — | — | shows names, sends the id | The B2B credit account (payments `B2bCreditAccount`) where a company is invoiced. | `issueTaxInvoice` body |
| Languages `languages` | list of values (chips) | optional | — | — | — | Overrides the template's languages for this document, within those the template offers. | `issueTaxInvoice` body |
| Supersedes invoice `supersedesInvoiceId` | picker: choose a supersedes invoice | optional | — | — | shows names, sends the id | A simplified invoice this full invoice replaces for the same supply. Refused unless the law allows it (make-or-break on issueTaxInvoice). | `issueTaxInvoice` body |
| Deliver to email `deliverToEmail` | email field | optional | — | — | name@example.ae | Sends the PDF on issue as well as returning it. | `issueTaxInvoice` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 An order is not paid, is already on a tax invoice of the same or a wider kind (`order-already-invoiced`), or the legal entity has no active template for the …; 422 A `full` or `consolidated` invoice without a recipient name and address, a `consolidated` invoice whose orders span buyers, legal entities or currencies, more …

**Rules for these inputs** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **since**: A simple period filter (Last 30 days, This year, All), not a raw date field; default All. *(source: contracts/spine/orders.yaml#listMyOrders)*
- **refund request**: Choose the lines (all by default), a reason of at least 3 characters (a short list plus "Other"), and send. Copy says "We'll review your request" and when the venue usually answers; it never says "refunded". *(source: contracts/spine/orders.yaml#createRefundRequest; DI-254)*

#### Outputs: what the screen shows and produces

**Shown**

**Your orders** (card list, from `listMyOrders`): Was the generated table 'Every order'; staff and plumbing columns removed (decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-3)).

| Shows | Format | Notes |
|---|---|---|
| Order number | text | The number a guest reads and a cashier types. Server-assigned: the venue prefix and a sequence per venue, for example `DXB1-000123` … |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Lines | list or chips (count when long) | — |
| Created at | 1 Oct 2026, 14:30 | — |

**Tax invoices** (card list, from `listTaxInvoices`): The VAT receipt (simplified tax invoice) and any full tax invoice for the order, with its number.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Invoice number | text | Server-assigned from the legal entity's series for the document kind, in sequence and without gaps, e.g. |
| Invoice type | chip: Simplified, Full, Consolidated | 5.7.93. `simplified` for one order with no recipient details, `full` for one order with them, `consolidated` for several paid orders of one … |
| Status | chip: Issued, Partially credited, Fully credited, Superseded | `issued` until a credit memo is issued against it; `superseded` where a full invoice replaced a simplified one for the same supply (only if … |
| Legal entity | the name it points at, never the id | — |
| Template | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Orders | list or chips (count when long) | — |
| Supplier name | text | — |
| Supplier address | text | — |
| Supplier tax registration number | text | — |
| Buyer subject | the name it points at, never the id | The guest the orders belong to; the key a guest's own reads filter on. |
| Buyer name | text | — |
| Buyer address | text | — |
| Buyer country code | text | — |
| Buyer tax registration number | text | — |
| Customer account | the name it points at, never the id | — |
| Issued at | 1 Oct 2026, 14:30 | — |
| Supply date | 1 Oct 2026 | The date of supply where it differs from the issue date (the latest order's payment date on a consolidated invoice). |

**Tax credit notes** (card list, from `listCreditMemos`): Any tax credit note issued after a refund (DEC-086).

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Credit memo number | text | Server-assigned from the legal entity's credit memo series, in sequence without gaps. |
| Tax invoice | the name it points at, never the id | — |
| Tax invoice number | text | — |
| Kind | chip: Full, Partial | — |
| Reason | chip: Refund, Cancellation, Price adjustment, Return of goods, Billing error, Other | — |
| Refund | the name it points at, never the id | — |
| Cancelled order | the name it points at, never the id | — |
| Legal entity | the name it points at, never the id | — |
| Buyer subject | the name it points at, never the id | — |
| Issued at | 1 Oct 2026, 14:30 | — |
| Currency | text | — |
| Net amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax amount in legal currency | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Legal FX rate | text | The invoice's own `legalFxRate`, never today's (CHG-FIN-011). |
| Invoice supply value | AED 1,234.50 | The value of the supply shown on the tax invoice (Executive Regulation Art. 60(1)(e)), adjusted by any earlier credit note on the same … |
| Corrected supply value | AED 1,234.50 | The correct value of the supply after this credit note (Art. 60(1)(e)). |

**The tax invoice** (detail panel, from `getTaxInvoice`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Invoice number | text | Server-assigned from the legal entity's series for the document kind, in sequence and without gaps, e.g. |
| Invoice type | chip: Simplified, Full, Consolidated | 5.7.93. `simplified` for one order with no recipient details, `full` for one order with them, `consolidated` for several paid orders of one … |
| Status | chip: Issued, Partially credited, Fully credited, Superseded | `issued` until a credit memo is issued against it; `superseded` where a full invoice replaced a simplified one for the same supply (only if … |
| Legal entity | the name it points at, never the id | — |
| Template | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Orders | list or chips (count when long) | — |
| Supplier name | text | — |
| Supplier address | text | — |
| Supplier tax registration number | text | — |
| Buyer subject | the name it points at, never the id | The guest the orders belong to; the key a guest's own reads filter on. |
| Buyer name | text | — |
| Buyer address | text | — |
| Buyer country code | text | — |
| Buyer tax registration number | text | — |
| Customer account | the name it points at, never the id | — |
| Issued at | 1 Oct 2026, 14:30 | — |
| Supply date | 1 Oct 2026 | The date of supply where it differs from the issue date (the latest order's payment date on a consolidated invoice). |
| Currency | text | — |

**The selected order** (detail panel, from `getOrder`)

| Shows | Format | Notes |
|---|---|---|
| Order number | text | The number a guest reads and a cashier types. Server-assigned: the venue prefix and a sequence per venue, for example `DXB1-000123` … |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Net amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunded amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Charge total | AED 1,234.50 | `grossAmount` converted at `chargeFxRate` and rounded to the charge currency's scale: what the guest pays and what the payment request to … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Download or email the PDF (secondary button) | `getTaxDocumentRendition` GET `/tax-documents/{documentId}/rendition` | — | FinTaxDocumentRendition | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | produces a document or message: The PDF of a tax invoice or credit memo, in a language |
| Ask for a refund (secondary button) | `createRefundRequest` POST `/refund-requests` | inline | inline | 403 Authenticated but not permitted at the requested scope | opens modal first |
| Get a tax invoice (secondary button) | `issueTaxInvoice` POST `/tax-invoices` | FinIssueTaxInvoiceRequest | FinTaxInvoice | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 An order is not paid, is already on a tax invoice of the same or a wider kind (`order-already-invoiced`), or … | opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **order row**: Order number, visit date, what was bought in one line ("3 × 2 park ticket"), total in AED and status in guest words (Paid, Partly refunded, Refunded, Cancelled, Used). *(source: contracts/spine/orders.yaml#/components/schemas/Order)*
- **tax invoice**: View or download the tax invoice PDF, and credit memos for refunds, per order. *(source: screens/P01-guest-web-storefront.yaml#WEB-019 apis (listTaxInvoices, getTaxDocumentRendition))*

**What each action does** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **View tickets**: Opens My Tickets (WEB-018) on that order. *(source: screens/P01-guest-web-storefront.yaml#WEB-019 transitions)*
- **Request a refund**: Enters the venue's approval queue; the row shows "Refund requested" until operations approve, reject or ask for more information. *(source: DI-254; contracts/spine/orders.yaml#createRefundRequest)*

**Data it reads**: `listMyOrders` (onLoad, The orders this guest placed); `listTaxInvoices` (onLoad, List tax invoices); `getTaxInvoice` (onLoad, Show a tax invoice); `listCreditMemos` (onLoad, List credit memos)

**Where the user goes next**

- → `WEB-016` Login / Register: *Login / Register*; carries `subjectId`
- → `WEB-017` My Account Dashboard: *My Account Dashboard*
- → `WEB-018` My Tickets: *My Tickets*; carries `orderId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The order history list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the order history untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No order history yet. Offers Create refund request (`createRefundRequest`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on since and the order history are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the … |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 An order is not paid, is already on a tax invoice of the same or a wider kind (`order-already-invoiced`), or the legal entity has no active template for the …; 422 A `full` or `consolidated` invoice without a recipient name and address, a `consolidated` invoice whose orders span buyers, legal entities or currencies, more … |

#### Edge cases to draw

- **An order bought as a guest checkout before the account existed**: Appears once the contact was verified (matches attach automatically); an unverified one does not appear and the page offers "Can't find an order? Link a booking" (GAP-B3 link guest checkout). *(source: DI-1074; screens/P01-guest-web-storefront.yaml#WEB-012 notes (R120 b))*

#### Consistency with other screens

- Match `GST-016`: Same order wording and status words on the app.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- order: YAS1-000123
  date: Fri 2 Oct
  items: 3 × 2 park ticket
  total: AED 1,660
  status: Paid
- order: YAS1-000098
  date: Sat 12 Sep
  items: Cabana B09
  total: AED 1,855
  status: Refunded
```

#### Permissions

- `listMyOrders` → no permission · guest
- `getOrder` → `ORDER_VIEW` (read) · staff, guest, partner
- `createRefundRequest` → no permission · guest
- `listTaxInvoices` → `LEDGER_VIEW` (read) · staff, guest
- `getTaxInvoice` → `LEDGER_VIEW` (read) · staff, guest
- `listCreditMemos` → `LEDGER_VIEW` (read) · staff, guest
- `getTaxDocumentRendition` → `LEDGER_VIEW` (read) · staff, guest
- `issueTaxInvoice` → `LEDGER_POST` (operate) · staff, guest, service

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the …

#### Requirements it meets

16 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.12 | Ticket Viewing - System shall display ticket details. | Guest Mobile App & Branding | CONTRACTED | `getOrder` |
| 2.6.2 | Post-order service 1) On the order details page, users can view the order number, amount, time, payment method, user information, refund/change policies, and the QR code of the e-ticket 2) During the … | Ticketing Sales | CONTRACTED | `getOrder` |
| 2.12.27 | All orders can be finalized for payment registration or modified or even cancelled at the Guest Service or any reservation PC. | Ticketing Sales | CONTRACTED | `getOrder` |
| 5.7.8 | The system should be able to use of a unique Order or Reference number (PNR) for each transaction, which can be communicated to the Payment Gateway, Acquiring Bank and the ERP system for … | F&B & Guest Management | CONTRACTED | `getOrder` |
| 19.2.15 | Ticket Cancellation - System shall support ticket cancellation. | Guest Mobile App & Branding | CONTRACTED | `createRefundRequest` |
| 19.2.82 | Self-Service Refund Requests - System shall support self-service refund requests. | Guest Mobile App & Branding | CONTRACTED | `createRefundRequest` |
| 2.6.42 | Customer should be able to intiate refund tickets from the online portal | Ticketing Sales | CONTRACTED | `createRefundRequest` |
| 2.12.12 | The system should allow amendment and refunds (full or partial) based on ticket status (available, expired, etc.). This should be configurable. | Ticketing Sales | CONTRACTED | `createRefundRequest` |
| 2.12.15 | The system should be able to refund in different and multiple payment methods (example: System to allow refunds in cash for the tickets/bookings purchased through credit card). | Ticketing Sales | CONTRACTED | `createRefundRequest` |
| 2.12.18 | The system should provide the option to issue refund in the original mode of payment used by the guest or a different method of payment with supervisor override. Refund can also be offered as credits … | Ticketing Sales | CONTRACTED | `createRefundRequest` |
| 4.2.2 | The system should be able to refund transactions that contain promotions and ensure discounted amount is not refunded | Bundles and Promotions | CONTRACTED | `createRefundRequest` |
| 4.6.10 | The system to be able to refund in different and multiple payment methods. For example, system to allow refunds in cash or original payment methods. | Bundles and Promotions | CONTRACTED | `createRefundRequest` |
| … 4 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Online/app returns: customer submits a return request with a reason (and photo if applicable) → approval team → courier pickup → refund after verified receipt. Confirmed: an item bought at the POS can also be returned via the web portal, subject to approval. *(agreed · MoM 19 Aug 2026, 4.7 Returns, Refunds & Exchanges — In-Store and Online; 5. Key Decisions · DI-367)*
- Guests can request a refund from their account/profile; operations are notified and can approve, reject or ask for more information. *(agreed · MoM 12 Aug 2026, 9. Refund Ledger Sequencing and Refund Policy · DI-254)*

Also apply: 1 for P01 · Account & Self-Service, 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-019` · status **review** · provenance client-verified
- Prototype (rev 3 (pointer moved to the 30 September build, CHG-R1S-015), verified 2026-09-28, match partial): `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`, view *Account → 'Order history'*. Differences: A list pane with toast-only actions; no order detail view. Refund request and transfer are rows, not flows.
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state (403, 404, 409, 422).
- [ ] Every output is drawn (74 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-019?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Download or email the PDF, Ask for a refund, Get a tax invoice.
- [ ] Every transition is wired: `WEB-016`, `WEB-017`, `WEB-018`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `WEB-020` Profile & Preferences

**Correct your details, choose what we may send you, and record your needs.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Account & Self-Service · wave 1 · needs the `marketing` module |
| Block | Block A · task APP-WEB-WEB-020 |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · the venue's theme |
| Pattern | listDetail (compact density): `listConsentPurposes` reads the population and `getGuestProfile` reads one of them — list, select, act |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | `subjectId` (session) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/account-and-self-service/profile-and-preferences` |

**What the spec says about it.** Consent withdrawal must be as easy as granting it. Same screen, same number of clicks. Purpose derived from the screen name and its operations on 17 August, not from a requirement. Profile and Preferences. **Wishlist and device operations removed; profile, consent and email verification added.** Deep listed exactly these. **Rewired on the 20 August review.** **29 September (W1).** *Complete your details* for a profile created by guest checkout.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The web page where a guest corrects their own details, sets preferences, and gives or withdraws consent. Withdrawing must be exactly as easy as giving: same screen, same number of clicks. A profile created by guest checkout shows "Complete your details" and is never blocked. Preferences (what they like) and consent (what they permit) are visibly separate sections, because a preference update must never quietly grant marketing permission.

**Fixed on main** (the package already carries these; draw what it says): The profile is read with getGuestProfile (staff-and-guest, by subjectId) while getMyProfile, the guest's own read, is consumed by no screen. (CHG-SGU-017); The screen writes consent but has no getGuestConsents, so it cannot show the current position it is changing. (CHG-SGU-017); Purpose text reads "Change how profile behaves here, and see which level the current value came from". (CHG-SGU-017).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| What we may send you | repeatable rows | optional | — | — | — | One row per configured purpose (`listConsentPurposes`), its channels as toggles, its plain-language description and the notice version in force; the current position from `getGuestConsents` (Given … | `ConsentState.purposes` |
| Consent toggle | repeatable rows | optional | — | — | — | Per purpose and channel; recorded at once on change, append-only. | `ConsentState.purposes` |

**Form: Save guest preferences** (modal, opened by *Save guest preferences*; *Save guest preferences* calls `updateGuestPreferences`, *Cancel* sends nothing)

**Collects what `updateGuestPreferences` sends before it is called.** Nothing in the body is required. Optional: `seatingPreference`, `drinkPreferences`, `dietary`, `accessibility`, `preferredChannel`. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets them (readOnly in the contract): `id`, `subjectId` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Seating preference `seatingPreference` | text field | optional | — | max length 200 | — | — | `updateGuestPreferences` body |
| Drink preferences `drinkPreferences` | list of values (chips) | optional | — | — | — | — | `updateGuestPreferences` body |
| Dietary `dietary` | list of values (chips) | optional | — | — | — | Also written by `updateMyProfile`. | `updateGuestPreferences` body |
| Accessibility `accessibility` | list of values (chips) | optional | — | — | — | Also written by `updateMyProfile`. | `updateGuestPreferences` body |
| Preferred channel `preferredChannel` | select | optional | — | Email · SMS · Whatsapp · Push · In app · Post | — | Stored on the profile (`GuestProfile.preferredChannel`) — carried here because the preference screen edits it beside the rest. | `updateGuestPreferences` body |

**Form: Save my profile** (modal, opened by *Save my profile*; *Save my profile* calls `updateMyProfile`, *Cancel* sends nothing)

**Collects what `updateMyProfile` sends before it is called.** Nothing in the body is required. Optional: `displayName`, `email`, `phone`, `preferredLanguage`, `preferredChannel`, `dietary`, `accessibility`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Display name `displayName` | text field | optional | — | — | — | — | `updateMyProfile` body |
| Email `email` | email field | optional | — | — | name@example.ae | — | `updateMyProfile` body |
| Phone `phone` | phone field | optional | — | — | +971 5X XXX XXXX (E.164) | — | `updateMyProfile` body |
| Preferred language `preferredLanguage` | text field | optional | — | — | — | — | `updateMyProfile` body |
| Preferred channel `preferredChannel` | radio group | optional | — | Email · SMS · Whatsapp · Push · None | — | — | `updateMyProfile` body |
| Dietary `dietary` | list of values (chips) | optional | — | — | — | Health-adjacent personal data, kept structured rather than as a tag (BL-134). `GuestProfile.tags` carries VIP-style markers adequately and is the wrong home for a nut allergy — … | `updateMyProfile` body |
| Accessibility `accessibility` | list of values (chips) | optional | — | — | — | Same treatment, same reason. Stored as `GuestPreferences.accessibility`. | `updateMyProfile` body |

**Form: Verify guest email** (modal, opened by *Verify guest email*; *Verify guest email* calls `verifyGuestEmail`, *Cancel* sends nothing)

**Collects what `verifyGuestEmail` sends before it is called.** Required: `mode`. Optional: `token`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Mode `mode` | segmented control | required | — | Send · Confirm | — | — | `verifyGuestEmail` body |
| Token `token` | text field | optional | — | — | — | For `confirm`. Single use and short-lived — a verification link that works forever is a verification link in an old inbox. | `verifyGuestEmail` body |

Errors to draw in the form: 410 The token expired or was already used. Distinct from an invalid one — a guest who clicked an old link should be offered a new one rather than told they are …

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Name, email, phone, language, preferred channel**: A guest may correct only these (plus dietary and accessibility), never their tags, lifetime value or tier. At least one of email or mobile must remain. A changed email is unverified until the link is confirmed, and an unverified account cannot buy, so show "Verify your new email" immediately. Preferred channel is email, SMS, WhatsApp, push or none; "none" stops marketing channels only, and transactional messages still arrive. *(source: contracts/satellite/marketing-crm.yaml#updateMyProfile; DI-372; contracts/spine/identity.yaml#verifyGuestEmail)*
- **Dietary and accessibility needs**: Structured choices, not free tags. They are health-adjacent personal data, so explain they are used to serve the guest and are not marketing. Saved by updateMyProfile or updateGuestPreferences; both write the same fields. *(source: contracts/satellite/marketing-crm.yaml#updateMyProfile; contracts/satellite/marketing-crm.yaml#updateGuestPreferences)*
- **Consent toggles**: One row per configured purpose (from the venue's consent purposes), each with the channels it covers as toggles, the purpose's plain-language description, and a link to the notice version in force. Each change is recorded at once as a new, append-only consent record with source "website" and the notice version. No Save button is needed for consent, and a failed write reverts the toggle with an error. *(source: contracts/satellite/marketing-crm.yaml#recordConsent; contracts/satellite/marketing-crm.yaml#listConsentPurposes; screens/P01-guest-web-storefront.yaml#WEB-020)*
- **Identity verification (only where the venue's policy asks)**: Document kind (passport, Emirates ID, national ID, driving licence, residence permit), number, expiry, and a photo of the document. The number is hashed and only the last four characters are ever shown back. *(source: contracts/spine/identity.yaml#submitGuestIdentityDocument)*

#### Outputs: what the screen shows and produces

**Shown**

**Complete your details** (banner, from `updateMyProfile`): For a profile created by guest checkout (W1): asks for what the pop-up did not; never blocks.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Subject | the name it points at, never the id | Opaque reference. Personal data lives in the separately erasable store, which is what makes erasure possible against an append-only ledger. |
| Display name | text | — |
| Email | text | — |
| Phone | +971 50 123 4567 | — |
| Preferred language | text | — |
| Preferred channel | chip: Email, SMS, Whatsapp, Push, In app, Post | — |
| Guest link | text | Present where the guest is linked across cells. Marketing acts locally. |
| Tags | list or chips (count when long) | — |
| Engagement score | 1,234 | 22.2.20 and 22.2.21. `lifetimeValue` and `visitCount` existed, so value was a stored figure and engagement was not. |
| Engagement tier | chip: New, Active, Occasional, Lapsing, Lapsed, Dormant | 5.3.19. Automatic classification, computed rather than assigned. |
| Lifetime value | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Visit count | 1,234 | — |
| Last visit at | 1 Oct 2026, 14:30 | — |
| Is active | yes / no (icon or chip) | — |
| Merged into subject | the name it points at, never the id | Set on the absorbed profile by `mergeGuestProfiles` and `mergeGuests`, which retain it as a redirect rather than deleting it. |
| Merged at | 1 Oct 2026, 14:30 | — |

**Purposes and notices** (card list, from `listConsentPurposes`): The configured purposes with their plain-language description, channels and the notice version in force.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Purpose | chip: Marketing, Personalisation, Profiling, Third party sharing, AI processing … | — |
| Display name | text | — |
| Description | text | — |
| Channels | list or chips (count when long) | — |
| Notice version | text | Current version of the notice. A consent against a superseded version is reported as requiring renewal rather than silently honoured. |
| Is required for service | yes / no (icon or chip) | True for transactional. Withdrawing it means the service cannot be delivered, so it is presented differently. |
| Expires after months | 1,234 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**My details** (detail panel, from `getMyProfile`): Read by session (`getMyProfile`), matching `updateMyProfile`; it cannot be pointed at another guest.

| Shows | Format | Notes |
|---|---|---|
| Profile | grouped details | — |
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Subject | the name it points at, never the id | Opaque reference. Personal data lives in the separately erasable store, which is what makes erasure possible against an append-only ledger. |
| Display name | text | — |
| Email | text | — |
| Phone | +971 50 123 4567 | — |
| Preferred language | text | — |
| Preferred channel | chip: Email, SMS, Whatsapp, Push, In app, Post | — |
| Guest link | text | Present where the guest is linked across cells. Marketing acts locally. |
| Tags | list or chips (count when long) | — |
| Engagement score | 1,234 | 22.2.20 and 22.2.21. `lifetimeValue` and `visitCount` existed, so value was a stored figure and engagement was not. |
| Engagement tier | chip: New, Active, Occasional, Lapsing, Lapsed, Dormant | 5.3.19. Automatic classification, computed rather than assigned. |
| Lifetime value | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Visit count | 1,234 | — |
| Last visit at | 1 Oct 2026, 14:30 | — |
| Is active | yes / no (icon or chip) | — |
| Merged into subject | the name it points at, never the id | Set on the absorbed profile by `mergeGuestProfiles` and `mergeGuests`, which retain it as a redirect rather than deleting it. |
| Merged at | 1 Oct 2026, 14:30 | — |
| Preferences | grouped details | What the guest likes, kept apart from what they permit (consent) and from who they are (the profile). |
| ID | the name it points at, never the id | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save my profile (primary button) | `updateMyProfile` PATCH `/guests/me/profile` | inline | GuestProfile | — | opens modal first |
| Verify guest email (secondary button) | `verifyGuestEmail` POST `/auth/guest/verify-email` | inline | inline | 410 The token expired or was already used. Distinct from an invalid one — a guest who clicked an old link should be offered a new one rather than told they are … | opens modal first; produces a document or message: Send a verification link, or consume one |
| Save guest preferences (secondary button) | `updateGuestPreferences` PUT `/guests/{subjectId}/preferences` | GuestPreferences | GuestPreferences | — | opens modal first |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Consent state per purpose**: Given (with date), Withdrawn (with date) or Not asked. A consent given against a superseded notice shows "Needs renewing" with the new notice to read. *(source: contracts/satellite/marketing-crm.yaml#getGuestConsents; contracts/satellite/marketing-crm.yaml#/components/schemas/ConsentDecision)*
- **Verification status**: Pending, verified, rejected or resubmit; for a rejection, the reason the guest is shown. *(source: contracts/spine/identity.yaml#getMyIdentityVerification)*

**What each action does** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Save my details**: Saves the profile fields; on failure the form keeps what was typed and says what failed. *(source: screens/P01-guest-web-storefront.yaml#WEB-020)*
- **Withdraw all marketing**: One action that records "withdrawn" for the marketing purpose on every channel (channels omitted applies to all). Confirmation names what stops (offers and news) and what continues (tickets, receipts). *(source: contracts/satellite/marketing-crm.yaml#recordConsent)*

**Data it reads**: `listConsentPurposes` (onLoad, The purposes the consent rows show); `getMyIdentityVerification` (onLoad, Show the guest's ID verification status); `getMyProfile` (onLoad, The guest's own details, read by session); `getGuestConsents` (onLoad, The current consent position the toggles change)

**Where the user goes next**

- → `WEB-016` Login / Register: *Login / Register*; carries `subjectId`
- → `WEB-017` My Account Dashboard: *My Account Dashboard*
- → `WEB-018` My Tickets: *My Tickets*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Profile and consents |
| Error (`?state=error`) | **Save failed and the form keeps what was typed.** A consent change that silently did not save is a compliance failure, so the screen states it rather than showing success |
| Empty, first run (`?state=emptyFirstRun`) | — |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the current filters. **The filters are named and clearable from here** — an empty list with the filter state hidden elsewhere is a person who thinks the data is gone. **Added 25 August with the derived list component**: a screen that lists has to say what it shows when the list is empty, and this screen gained the list before it gained the sentence. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the … |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Notice version unknown, or the purpose is not configured; 409 A verification is already pending for this guest; 422 The document has expired, or its kind is not accepted by the tenant's policy |

#### Edge cases to draw

- **The guest removes their email and has no mobile**: Refused inline - "Keep at least an email or a mobile so we can send your tickets". *(source: DI-372)*
- **A consent change fails to save**: The toggle returns to its previous position and the page says the change did not save. Never show success for an unsaved consent. *(source: screens/P01-guest-web-storefront.yaml#WEB-020)*

#### Consistency with other screens

- Match `GST-039`: Same fields, same consent rows, same "Withdraw all marketing" wording.
- Match `WEB-027`: Newsletters (subscriptions) live on WEB-027; this page links to it and does not duplicate the list toggles.
- Match `WEB-024`: The data request and delete-account actions live on WEB-024; this page links there.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
profile:
  name: Sarah Thompson
  email: sarah.t@example.ae
  mobile: +971 55 987 2210
  language: English
  channel: WhatsApp
consents:
- Offers and news - Email Given 12 Sep 2026, WhatsApp Not asked, SMS Withdrawn 2 Oct 2026
- Personalised recommendations - Given 12 Sep 2026
- Sharing with partner venues - Not asked
dietary:
- Vegetarian
- Nut allergy
accessibility:
- Step-free access
```

#### Permissions

- `updateMyProfile` → `GUEST_VIEW` (read) · guest
- `recordConsent` → no permission · guest, staff
- `listConsentPurposes` → `GUEST_VIEW` (read) · staff, guest
- `verifyGuestEmail` → `GUEST_VIEW` (read) · guest, anonymous
- `updateGuestPreferences` → `GUEST_MANAGE` (configure) · staff, guest
- `getMyIdentityVerification` → no permission · guest
- `submitGuestIdentityDocument` → no permission · guest
- `getMyProfile` → `GUEST_VIEW` (read) · guest
- `getGuestConsents` → `GUEST_VIEW` (read) · staff, guest

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the …

#### Requirements it meets

15 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.7 | Profile Management - System shall support profile management. | Guest Mobile App & Branding | CONTRACTED | `updateMyProfile` |
| 2.6.40 | Customer should be able to view and amend user profile | Ticketing Sales | CONTRACTED | `updateMyProfile` |
| 5.3.5 | The system should allow user to amend account contact details (postal address, email address, telephone number, newsletter opt-in, SMS opt-in, etc.) | F&B & Guest Management | CONTRACTED | `updateMyProfile` |
| 22.13.13 | Right to Rectification | Marketing & CRM | CONTRACTED | `updateMyProfile` |
| 5.3.9 | The system should allow the guest to explicitly opt in to receive any information from venue or its partners. | F&B & Guest Management | CONTRACTED | `recordConsent` |
| 5.3.18 | Maintain auditable consent records for Email, SMS, WhatsApp, Push Notifications, Marketing Communications, Privacy Policies, Terms & Conditions, and GDPR compliance. | F&B & Guest Management | CONTRACTED | `recordConsent` |
| 7.3.9 | Store and manage customer consent preferences for email, SMS, WhatsApp, push notifications and third-party marketing. Record consent status, source, timestamp, IP address and revocation history. … | F&B POS | CONTRACTED | `recordConsent` |
| 22.2.18 | Consent Management | Marketing & CRM | CONTRACTED | `recordConsent` |
| 22.4.5 | Subscription Management | Marketing & CRM | CONTRACTED | `recordConsent` |
| 22.13.1 | Consent Management Framework | Marketing & CRM | CONTRACTED | `recordConsent` |
| 22.13.2 | Marketing Consent Management | Marketing & CRM | CONTRACTED | `recordConsent` |
| 22.13.3 | Channel-Specific Consent | Marketing & CRM | CONTRACTED | `recordConsent` |
| … 3 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P01 · Account & Self-Service, 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-020` · status **review** · provenance client-verified
- Prototype (rev 3 (pointer moved to the 30 September build, CHG-R1S-015), verified 2026-09-28, match partial): `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`, view *Account → 'Personal details', 'Notifications', 'Accessibility'*. Differences: Split over three panes; fields are read-only with a 'Save changes' toast. No 'which level the current value came from' (YAML purpose). Consent purposes appear as two marketing toggles rather than the configured purpose list.
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0045 *Every order carries a proven contact, and the gate is the checkout page* (`docs/adr/0045-every-order-carries-a-proven-contact.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (16), with its required mark, default, format and its error state (400, 404, 409, 410, 422).
- [ ] Every output is drawn (47 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-020?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save my profile, Verify guest email, Save guest preferences.
- [ ] Every transition is wired: `WEB-016`, `WEB-017`, `WEB-018`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 2 edge case(s) from the process notes are drawn.
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

### In P01 · Account & Self-Service

- Decision: profiles are never merged automatically. Likely duplicates are notified to the customer (push or e-mail) and merge only on the customer's confirmation; an admin review queue tracks flagged duplicates independently of the customer's response. *(agreed · MoM 20 Aug 2026, 4.2 Duplicate Detection; 5. Key Decisions · DI-377)*

**22 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"claimCart": {"method":"POST","path":"/carts/{cartId}/claim","contract":"orders","summary":"Attach an anonymous cart to a guest","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CartMergeResult"},
"claimDeviceConsent": {"method":"POST","path":"/guests/{subjectId}/consents/claim-device","contract":"marketing-crm","summary":"Attach a browser's cookie decision to the guest who turned out to own it","permission":null,"offlineCapable":false,"conflictPolicy":"append","scopeLevel":"subject","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ClaimDeviceConsentRequest","responds":"ConsentState"},
"createMfaChallenge": {"method":"POST","path":"/auth/mfa/challenge","contract":"identity","summary":"Second factor at staff sign-in, and step-up for a sensitive action","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"createRefundRequest": {"method":"POST","path":"/refund-requests","contract":"orders","summary":"Guest-initiated refund request","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"getEntitlement": {"method":"GET","path":"/entitlements/{entitlementId}","contract":"access","summary":"One entitlement, with what remains on it","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Entitlement"},
"getEntitlementCredential": {"method":"GET","path":"/entitlements/{entitlementId}/credential","contract":"access","summary":"The thing that gets scanned","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"rotate","in":"query","required":null}],"requestBody":null,"responds":null},
"getEntitlementHistory": {"method":"GET","path":"/entitlements/{entitlementId}/history","contract":"access","summary":"Every scan, freeze, share and reissue against it","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":null},
"getGuestConsents": {"method":"GET","path":"/guests/{subjectId}/consents","contract":"marketing-crm","summary":"Read a guest's consent state","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ConsentState"},
"getGuestSession": {"method":"GET","path":"/auth/guest/session","contract":"identity","summary":"Read the current guest session","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"GuestSession"},
"getLoyaltyPosition": {"method":"GET","path":"/loyalty/position","contract":"marketing-crm","summary":"A guest's points, tier and what is within reach","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"programmeId","in":"query","required":true}],"requestBody":null,"responds":null},
"getMyChallenges": {"method":"GET","path":"/guests/me/challenges","contract":"marketing-crm","summary":"Active challenges and how far along I am","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":null},
"getMyIdentityVerification": {"method":"GET","path":"/auth/guest/identity-verifications/current","contract":"identity","summary":"The guest's own latest identity verification","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"IdentityGuestVerification"},
"getMyProfile": {"method":"GET","path":"/guests/me/profile","contract":"marketing-crm","summary":"A guest reading their own details","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"subject","parameters":[],"requestBody":null,"responds":null},
"getOrder": {"method":"GET","path":"/orders/{orderId}","contract":"orders","summary":"Read an order","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Order"},
"getTaxDocumentRendition": {"method":"GET","path":"/tax-documents/{documentId}/rendition","contract":"finance","summary":"The PDF of a tax invoice or credit memo, in a language","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"language","in":"query","required":null}],"requestBody":null,"responds":"FinTaxDocumentRendition"},
"getTaxInvoice": {"method":"GET","path":"/tax-invoices/{invoiceId}","contract":"finance","summary":"One tax invoice, with its lines, VAT per rate and credit memos","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[],"requestBody":null,"responds":"FinTaxInvoice"},
"getWallet": {"method":"GET","path":"/wallets/{subjectId}","contract":"wallet","summary":"Read a guest wallet","permission":"WALLET_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Wallet"},
"getWishlist": {"method":"GET","path":"/guests/{subjectId}/wishlist","contract":"marketing-crm","summary":"Read a guest's saved items","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"subject","parameters":[],"requestBody":null,"responds":"Wishlist"},
"guestLogout": {"method":"DELETE","path":"/auth/guest/session","contract":"identity","summary":"End a guest session","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":"allDevices","in":"query","required":null}],"requestBody":null,"responds":null},
"guestPasswordLogin": {"method":"POST","path":"/auth/guest/password","contract":"identity","summary":"Sign in with an email or mobile and a password","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GuestSession"},
"guestSocialLogin": {"method":"POST","path":"/auth/guest/social","contract":"identity","summary":"Sign in with Apple or Google","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GuestSession"},
"guestUaePassLogin": {"method":"POST","path":"/auth/guest/uae-pass","contract":"identity","summary":"Sign in with a national identity provider","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GuestSession"},
"issueTaxInvoice": {"method":"POST","path":"/tax-invoices","contract":"finance","summary":"Issue a tax invoice for one or more paid orders","permission":"LEDGER_POST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"FinIssueTaxInvoiceRequest","responds":"FinTaxInvoice"},
"issueWalletPass": {"method":"POST","path":"/wallet-passes","contract":"orders","summary":"Generate an Apple or Google wallet pass","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WalletPass"},
"linkGuestCheckout": {"method":"POST","path":"/auth/guest/link-checkout","contract":"identity","summary":"Attach a guest checkout to an account","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"listConsentPurposes": {"method":"GET","path":"/consent-purposes","contract":"marketing-crm","summary":"Configured consent purposes","permission":"GUEST_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCreditMemos": {"method":"GET","path":"/credit-memos","contract":"finance","summary":"Credit memos issued, newest first","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"taxInvoiceId","in":"query","required":null},{"name":"refundId","in":"query","required":null},{"name":"legalEntityId","in":"query","required":null},{"name":"issuedFrom","in":"query","required":null},{"name":"issuedTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listEntitlements": {"method":"GET","path":"/my/entitlements/all","contract":"access","summary":"Every entitlement this guest holds, including expired","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":"includeExpired","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listLoyaltyProgrammes": {"method":"GET","path":"/loyalty/programmes","contract":"marketing-crm","summary":"List loyalty programmes","permission":"MARKETING_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMyEntitlements": {"method":"GET","path":"/guests/me/entitlements","contract":"access","summary":"Every ticket, pass and membership this guest holds","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"state","in":"query","required":null},{"name":"includeShared","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMyOrders": {"method":"GET","path":"/my/orders","contract":"orders","summary":"The orders this guest placed","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":"since","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTaxInvoices": {"method":"GET","path":"/tax-invoices","contract":"finance","summary":"Tax invoices issued, newest first","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"orderId","in":"query","required":null},{"name":"legalEntityId","in":"query","required":null},{"name":"invoiceType","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"issuedFrom","in":"query","required":null},{"name":"issuedTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"recordConsent": {"method":"POST","path":"/guests/{subjectId}/consents","contract":"marketing-crm","summary":"Record a consent decision","permission":null,"offlineCapable":false,"conflictPolicy":"append","scopeLevel":"subject","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RecordConsentRequest","responds":"ConsentState"},
"refreshToken": {"method":"POST","path":"/auth/refresh","contract":"identity","summary":"Rotate the access token","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TokenPair"},
"registerGuest": {"method":"POST","path":"/auth/guest/register","contract":"identity","summary":"Create a guest account","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RegisterGuestRequest","responds":"GuestSession"},
"requestGuestOtp": {"method":"POST","path":"/auth/guest/otp","contract":"identity","summary":"Request a one-time code","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"respondToInvitation": {"method":"POST","path":"/invitations/{token}/respond","contract":"marketing-crm","summary":"Accept or decline","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Invitation"},
"shareEntitlement": {"method":"POST","path":"/entitlements/{entitlementId}/share","contract":"orders","summary":"Let somebody else use this, without giving it away","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"EntitlementShare"},
"submitGuestIdentityDocument": {"method":"POST","path":"/auth/guest/identity-verifications","contract":"identity","summary":"Submit an identity document for verification","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"IdentityGuestDocumentSubmission","responds":"IdentityGuestVerification"},
"transferOrderTickets": {"method":"POST","path":"/orders/{orderId}/transfer","contract":"orders","summary":"Transfer tickets to another guest","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"updateGuestPreferences": {"method":"PUT","path":"/guests/{subjectId}/preferences","contract":"marketing-crm","summary":"The things a regular should not have to say twice","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"lastWriterWins","scopeLevel":"subject","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GuestPreferences","responds":"GuestPreferences"},
"updateMyProfile": {"method":"PATCH","path":"/guests/me/profile","contract":"marketing-crm","summary":"A guest correcting their own details","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"lastWriterWins","scopeLevel":"subject","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GuestProfile"},
"verifyGuestEmail": {"method":"POST","path":"/auth/guest/verify-email","contract":"identity","summary":"Send a verification link, or consume one","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"verifyGuestOtp": {"method":"POST","path":"/auth/guest/otp/verify","contract":"identity","summary":"Verify a one-time code and issue a session","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GuestSession"},
"verifyMfaChallenge": {"method":"POST","path":"/auth/mfa/challenge/{challengeId}/verify","contract":"identity","summary":"Complete a sign-in or step-up challenge","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"Cart": {"type":"object","x-ticvai-persistence":"orders.cart","required":["id","venueId","channel","status","lines"],"properties":{"id":{"type":"string","format":"uuid"},"token":{"type":"string","readOnly":true,"description":"**How an anonymous guest returns to their cart**, including from a recovery email. Rotated on claim, so a link shared before signing in does not reach the account after.\n"},"venueId":{"type":"string","format":"uuid"},"channel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"Null while anonymous. Set by `claimCart`."},"status":{"$ref":"#/components/schemas/CartStatus"},"lines":{"type":"array","items":{"$ref":"#/components/schemas/CartLine"}},"conflicts":{"type":"array","items":{"$ref":"#/components/schemas/CartConflict"}},"consentQuestions":{"type":"array","readOnly":true,"description":"**The consent questions this cart's products and flow ask** (decided 29 September, rev 3 REV3-26), computed on read at their current version as **the union of each line's published booking flow's `white-label.BookingFlow.settings.consentQuestionIds`** (the flow `getPublishedBookingFlow` resolves for the line's product: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig`, 29 September W12) **and every line's `catalogue.Product.consentQuestionIds`, each question once**: the flow's first, in its order, then each product's in cart-line order, a question already listed not repeated (its `lineIds` gain the line). The client asks them, in the order given, and sends the answers to `marketing.recordConsentAnswers`; `answered` then turns true. One or several, as the venue chose. `checkoutCart` refuses while a required one is unanswered.\n","items":{"allOf":[{"$ref":"../satellite/marketing-crm.yaml#/components/schemas/ConsentQuestion"},{"type":"object","properties":{"lineIds":{"type":"array","description":"The cart lines that ask it. Empty for a question the flow asks.","items":{"type":"string","format":"uuid"}},"answered":{"type":"boolean","description":"Every person (for `perPerson`) or the booking (for `perBooking`) has an answer."}}}]}},"subtotal":{"x-ticvai-column":"net_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"discountTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"total":{"x-ticvai-column":"gross_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"appliedPromotionIds":{"type":"array","description":"**Re-evaluated on every read.** A promotion that expired while the cart sat must not still be applied at checkout, and a promotion that became applicable should be.\n","items":{"type":"string","format":"uuid"}},"couponCodes":{"type":"array","readOnly":true,"description":"The promo codes the guest entered through `applyCartPromoCode` (decided 28 September, audit R073 (e)). **Sent as `couponCodes` on every promotions evaluation of this cart**, so a code is re-checked on each read like any promotion; a code that stops qualifying stays listed here and its promotion drops out of `appliedPromotionIds`.\n","items":{"type":"string","maxLength":100}},"expiresAt":{"type":"string","format":"date-time","description":"The earliest lease expiry in the cart, or the cart's own window where it holds none."},"extensionsUsed":{"type":"integer","readOnly":true},"maxExtensions":{"type":"integer","readOnly":true},"locale":{"type":"string"},"createdAt":{"type":"string","format":"date-time"},"updatedAt":{"type":"string","format":"date-time"}}},
"CartMergeResult": {"type":"object","x-ticvai-persistence":"none — computed","required":["cart"],"properties":{"cart":{"$ref":"#/components/schemas/Cart"},"mergedLineCount":{"type":"integer"},"droppedLines":{"type":"array","description":"**Reported, never silent.** Lines that could not be re-leased on merge are named, so a guest signing in is told what they lost rather than discovering it at checkout.\n","items":{"type":"object","properties":{"productName":{"type":"string"},"reason":{"type":"string","enum":["noCapacity","expired","notSellableOnChannel","duplicate"]}}}}}},
"Challenge": {"type":"object","x-ticvai-persistence":"marketing.challenge","description":"BL-022, CF-137. **Section 22.6 is twenty requirements and 19.2.73–75 three more** — checked against the matrix on 18 August rather than assumed. It is asked for explicitly.\n**Gamification is not loyalty.** Loyalty pays for spend; a challenge pays for behaviour the venue wants and spend does not produce — a second visit, a quiet Tuesday, a ride nobody rides. **A challenge that only rewards spending is a loyalty programme with worse arithmetic.**\n","required":["id","name","kind","goal","status"],"properties":{"id":{"readOnly":true,"type":"string","format":"uuid"},"name":{"type":"string"},"kind":{"type":"string","description":"What an entrant does to progress. `scan`, `activity` and `purchase` were added from the BO-825 pack (decided 28 September, audit R275 (c)): `scan` counts scans of a named code or point (a trail marker, a stand), `activity` counts completions of a named attraction or activity that is not a ride, and `purchase` counts purchases of named products or categories. **`purchase` is not `spend`**: `spend` counts money, whatever was bought; `purchase` counts items bought.\n","enum":["visit","spend","ride","collection","streak","referral","survey","social","milestone","scan","activity","purchase"]},"scope":{"type":"string","enum":["individual","family","group","team"],"default":"individual","description":"22.6.7 and 22.6.8. **A family challenge is not a per-person challenge counted twice** — members contribute toward one shared goal, and a school competing against another school is a group scoring against a group.\n**This is the field that needs the portfolio work** (CF-132): a family challenge without a family is an individual challenge with a label.\n"},"goal":{"type":"object","description":"What completes it.","properties":{"metric":{"type":"string"},"target":{"type":"number"},"withinDays":{"type":"integer","nullable":true}}},"eventId":{"type":"string","format":"uuid","nullable":true},"rewardKind":{"type":"string","enum":["badge","loyaltyPoints","walletCredit","voucher","entitlement","none"],"description":"22.6.13. **A reward that issues wallet credit is money**, and it goes through the same stored-value mechanism as everything else rather than a parallel one.\n"},"rewardValue":{"type":"integer","nullable":true,"minimum":1,"description":"**Points, for `rewardKind: loyaltyPoints` only.** A count, not an amount — a money reward is `rewardAmount`, never this.\n"},"rewardAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"**The credit, for `rewardKind: walletCredit` only.** The shared `Money`, stored as `numeric(18,4)` with currency and scale resolved from the region, because a wallet credit is money and naming-and-style 5.1 forbids money as a bare number.\n"},"badgeAssetId":{"type":"string","format":"uuid","nullable":true},"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time","nullable":true},"status":{"readOnly":true,"type":"string","enum":["draft","active","paused","ended","archived"]},"scopePath":{"readOnly":true,"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"ChallengeProgress": {"type":"object","x-ticvai-persistence":"marketing.challenge_progress","description":"22.6.15. **Progress is shown, not just the outcome.** A guest two visits from a reward behaves differently from one who does not know how close they are, which is the entire mechanism.\n","required":["id","challengeId","subjectId","current","target"],"properties":{"id":{"type":"string","format":"uuid"},"challengeId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid"},"portfolioId":{"type":"string","format":"uuid","nullable":true,"description":"For a family or group challenge — where the shared progress accrues."},"current":{"type":"number"},"target":{"type":"number"},"streakCount":{"type":"integer","nullable":true},"completedAt":{"type":"string","format":"date-time","nullable":true},"rewardIssuedAt":{"type":"string","format":"date-time","nullable":true}}},
"ClaimDeviceConsentRequest": {"type":"object","x-ticvai-persistence":"none — request only","required":["consentKey"],"properties":{"consentKey":{"type":"string","maxLength":64}}},
"ConsentDecision": {"type":"string","enum":["granted","withdrawn","notAsked"]},
"ConsentPurpose": {"type":"string","enum":["marketing","personalisation","profiling","thirdPartySharing","aiProcessing","transactional"]},
"ConsentPurposeConfig": {"x-ticvai-persistence":"marketing.consent_purpose + marketing.consent_purpose_channel","type":"object","required":["purpose","channels","noticeVersion","isRequiredForService"],"properties":{"purpose":{"$ref":"#/components/schemas/ConsentPurpose"},"displayName":{"type":"string"},"description":{"type":"string"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/MessageChannel"}},"noticeVersion":{"type":"string","description":"Current version of the notice. A consent against a superseded version is reported as requiring renewal rather than silently honoured.\n"},"isRequiredForService":{"type":"boolean","description":"True for transactional. Withdrawing it means the service cannot be delivered, so it is presented differently.\n"},"expiresAfterMonths":{"type":"integer","nullable":true}}},
"ConsentSource": {"type":"string","enum":["guestApp","website","kiosk","pos","callCentre","import","agentRecorded","cookieBanner","checkout"],"description":"`checkout` (30 September, M18-15): an opt-in ticked beside the terms at checkout, carried on orders `checkoutCart` `marketingConsents[]` and recorded by `recordCheckoutConsents`, bound to the order and the verified contact. `cookieBanner` (29 September, build; BL-073 §4b): a decision made on the cookie banner or preference centre and moved onto the guest by `claimDeviceConsent`. Kept apart from `website`, a form submission, because the audit trail (2.6.56) has to tell the two apart."},
"ConsentState": {"x-ticvai-persistence":"none — projection over consent_record","type":"object","required":["subjectId","purposes"],"properties":{"subjectId":{"type":"string","format":"uuid"},"purposes":{"type":"array","items":{"type":"object","required":["purpose","decision","requiresRenewal"],"properties":{"purpose":{"$ref":"#/components/schemas/ConsentPurpose"},"decision":{"$ref":"#/components/schemas/ConsentDecision"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/MessageChannel"}},"noticeVersion":{"type":"string","nullable":true},"requiresRenewal":{"type":"boolean","description":"True where the notice has been superseded since consent was given."},"decidedAt":{"type":"string","format":"date-time","nullable":true}}}}}},
"Entitlement": {"type":"object","x-ticvai-persistence":"access.entitlement","description":"**What a guest actually holds.** Found missing on 18 August by the schema audit — 33 tables in `orders`, seven in `access`, and none of them stored an issued ticket.\nThe package sold products, defined `EntitlementTemplate`, recorded `ScanEvent.ticketId`, transferred `ticket_transfer.ticketIds` and issued `wallet_pass.entitlementId` — **five artefacts referring to a thing that did not exist.** `validateAccess` read the *template* and never the instance, and `suspendEntitlement` suspended the template, **which would have suspended it for every guest who held one.**\n**The template is the definition and this is the instance.** A template says *an annual pass admits once a day for a year*; this says *this guest's annual pass, bought on 3 March, used eleven times, frozen for two weeks in July, valid until 2 March.*\n","required":["id","templateId","productId","orderId","subjectId","status","validFrom","validTo"],"properties":{"id":{"type":"string","format":"uuid","description":"A UUIDv7, matching `TicketStatus.ticketId` — **stable for the life of the ticket and independent of the media carrying it.** A guest whose wristband broke keeps the same entitlement with a new `mediaCode`.\n**This is the ticket id.** Wherever an operation takes a `ticketId` or `ticketIds` — `lookupTicket`, `listScans`, `ScanEvent`, the offline package and `transferOrderTickets` — it is this value. An order line's `entitlementIds` are the ticket ids of that line.\n"},"templateId":{"type":"string","format":"uuid","description":"The definition it was issued against. **Pinned at issue** — a template edited next month must not change what this guest bought.\n"},"productId":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid","nullable":true,"description":"The order's id, a UUIDv7 as in `/orders/{orderId}` (`orders.sales_order.id`). **Null for an entitlement an invitation issued** (`invitationId`; 4 October 2026, CHG-FXC-007)."},"orderLineId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"Who holds it. **Null is legitimate** — a ticket bought as a gift or sold at a till to somebody who gave no details has no subject until it is claimed.\n"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"mediaCode":{"type":"string","description":"What is scanned — a QR payload, a wristband serial, a card number. **Rotatable without reissuing**, because a guest whose wristband broke should not need a new ticket.\n"},"status":{"$ref":"../spine/orders.yaml#/components/schemas/EntitlementStatus"},"statusNote":{"type":"string","nullable":true,"description":"**Not `TicketStatus` — that is a validation result with a misleading name**, computed at scan time and carrying `isValid` and `isInsideVenue`. The lifecycle is `orders.EntitlementStatus`, and `states/entitlement-status.yaml` has modelled it since before this table existed.\n**Which is the finding in one line: the package had the lifecycle, the state model and the validation result, and no row to hang them on.**\n"},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time","description":"**Resolved at issue from the template, then owned here.** A freeze extends it, a reissue replaces it, and neither reaches back to the template.\n**What the pre-expiry notice is measured from** (29 September, build pass, group G2; 5.5.30). A daily run in access publishes `entitlement.expiringSoon` once per entitlement and `validTo` when an entitlement in `issued` or `partiallyConsumed` comes within its template's `expiryNoticeDays` (`catalogue.EntitlementTemplate`), and not for one bought inside that window. Marketing turns it into the reminder (a `MessageTrigger` on the event, or a triggered campaign on `entitlementExpiring`); access only says the date is near. A freeze or renewal that moves `validTo` raises the next notice once.\n"},"entriesUsed":{"type":"integer","default":0,"readOnly":true,"x-ticvai-derived":"onWrite","description":"**The number `validateAccess` decrements and nothing was decrementing.** A ten-entry pass with no counter is a ten-entry pass that admits forever.\n**Maintained on write**, in the same transaction as the admitting `access.scan_event` row: by `validateAccess`, `validateGroupAccess` (by the count admitted) and `syncScans` for each replayed admission the server accepts. A replayed scan the server downgrades to `denied` does not count.\n"},"entriesAllowed":{"type":"integer","nullable":true},"lastEntryAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"`recordedAt` of the latest admission counted in `entriesUsed`, written by the same writes. A scan replayed late with an earlier `recordedAt` does not move it back.\n"},"firstEntryAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"`recordedAt` of the first admission, written by the same writes as `lastEntryAt`; it starts a time-bound entitlement's window (DEC-232; CHG-CSP-030). A replayed earlier scan moves it back."},"timeBoundUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"**Where the template is time-bound, when its window closes**: `firstEntryAt` plus the validity rule's `minutesAfterFirstScan` (decided 2 October 2026, Chinmay, BO-159; DEC-232; CHG-CSP-030). Null until the first scan and on an entitlement with no time bound. A scan after it is denied (`timeBoundWindowElapsed`); it never extends `validTo`, and the earlier of the two wins."},"lifecycleLabel":{"type":"string","readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","enum":["created","pendingFulfillment","active","partiallyUsed","used","expired","suspended","cancelled","voided","reissuedSuperseded","refunded","transferred","blocked"],"description":"**The Virtual Ticket status in the client's 13 names, mapped onto the entitlement model** (decided 2 October 2026, Chinmay, critical set 2, BO-336: \"Map the pack's 13 names onto the model; add any missing states\", and BO-336/DI-670: \"Reserved maps to Pending fulfilment\"; DEC-266; CHG-CSP-033). Computed on read from `status` (orders `EntitlementStatus`), `suspendedReason`, `cancellationKind`, `issuedVia` and an active identity lock; the mapping is in `states/entitlement-status.yaml`. It is what BO-334, BO-336 and the ticket status transition matrix (`AccessTicketStatusTransition`) show; logic still reads `status`."},"cancellationKind":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","enum":["voided","refunded","performanceCancelled","superseded"],"description":"**Which act cancelled the entitlement**, so the pack's Voided, Refunded and Reissued / superseded are told apart while `status` keeps the one r1 value `cancelled` (DEC-266; CHG-CSP-033). Written with the cancelling transition: `voidEntitlement`, `createRefund`, `cancelPerformance`, or a reissue that supersedes it (`supersedesEntitlementId` on the new one). Null unless `cancelled`."},"frozenDays":{"type":"integer","default":0,"readOnly":true,"x-ticvai-derived":"onWrite","description":"Days added by a freeze. **Maintained on write** by the freeze operation (`freezeEntitlement`), in the same write that extends `validTo` by those days. **Held here rather than computed from a freeze log**, because a gate has to answer in under 300ms and cannot replay a history to decide validity.\n"},"suspendedReason":{"type":"string","nullable":true},"freezeReason":{"type":"string","nullable":true,"enum":["travelling","injury","personal","seasonal","other"],"description":"The `reason` of the latest `freezeEntitlement` (audit R222). Null when never frozen."},"freezeNote":{"type":"string","nullable":true,"maxLength":500,"description":"The `note` the latest `freezeEntitlement` took, required there when `reason` is `other` (decided 28 September, audit R222). Kept so the quarterly review of `other` notes has something to read."},"isNameBound":{"type":"boolean","default":false},"holderName":{"type":"string","nullable":true},"sharedWithSubjectIds":{"type":"array","description":"`shareEntitlement`. **The owner keeps it and a second person may present it** — the asymmetry that stops a shared family pass becoming a resale chain.\n","items":{"type":"string","format":"uuid"}},"issuedVia":{"type":"string","enum":["sale","invitation","reissue","transfer","resale","membership","groupBooking"],"description":"**How it came to exist, and it matters to finance.** A sold entitlement carries deferred revenue; an invitation carries a marketing cost; a reissue carries neither.\n"},"supersedesEntitlementId":{"type":"string","format":"uuid","nullable":true,"description":"For a reissue or a resale. **The chain is traceable** — a ticket appearing from nowhere is indistinguishable from a fraudulent one.\n"},"walletValueId":{"type":"string","format":"uuid","nullable":true,"description":"Where the template carries stored value. **A `retail.Wallet` bound to the entitlement, not a balance on it** (CF-126).\n"},"facePassEnrolmentId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"The active `facePass` enrolment on this entitlement (`FacePassEnrolment.id`), or null when none is. **Computed on read from `pii.subject_biometric` and not stored here** — the PII split keeps the biometric on its own side, and this carries only its id. It is how a screen holding a pass finds the enrolment `getFacePassEnrolment` and `revokeFacePass` take.\n"},"invitationId":{"type":"string","format":"uuid","nullable":true,"description":"**The invitation that issued it** (4 October 2026, CHG-FXC-007): `orders.issueInvitation` issues the entitlement without an order, because an invitation never enters the order path. Exactly one of `orderId` and `invitationId` is set."}}},
"EntitlementShare": {"type":"object","x-ticvai-persistence":"none — a view of the identity.delegated_access row shareEntitlement writes","description":"**A second person's right to present an entitlement the owner still holds.** Returned by `shareEntitlement` and `revokeEntitlementShare`; its `id` is the delegated-access row the share is.\n","required":["id","entitlementId","toSubjectId","status"],"properties":{"id":{"type":"string","format":"uuid"},"entitlementId":{"type":"string","format":"uuid"},"toSubjectId":{"type":"string","format":"uuid","description":"The guest it is shared with. They may present it; they may not share or transfer it on."},"validFrom":{"type":"string","format":"date-time"},"validUntil":{"type":"string","format":"date-time","nullable":true,"description":"Null means until revoked or until the entitlement itself ends."},"revokedAt":{"type":"string","format":"date-time","nullable":true},"status":{"type":"string","enum":["active","revoked","expired"]}}},
"ExchangeRateDecimal": {"type":"string","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,6)","description":"**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one — a JavaScript client must not round a rate in transit. **Six decimal places**, the precision `finance.FxRate.rate` asks for, and stored at that precision.\n","pattern":"^\\d+(\\.\\d{1,6})?$"},
"FinCreditMemo": {"x-ticvai-persistence":"ledger.credit_memo + ledger.credit_memo_line","type":"object","description":"5.7.94. **A tax credit note against one tax invoice**, with its own series. Never edited.","required":["id","creditMemoNumber","taxInvoiceId","kind","reason","legalEntityId","issuedAt","currency","netAmount","taxAmount","grossAmount","lines"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"creditMemoNumber":{"type":"string","readOnly":true,"description":"Server-assigned from the legal entity's credit memo series, in sequence without gaps."},"taxInvoiceId":{"type":"string","format":"uuid"},"taxInvoiceNumber":{"type":"string","readOnly":true},"kind":{"type":"string","enum":["full","partial"]},"reason":{"type":"string","enum":["refund","cancellation","priceAdjustment","returnOfGoods","billingError","other"]},"refundId":{"type":"string","format":"uuid","nullable":true},"cancelledOrderId":{"type":"string","format":"uuid","nullable":true},"legalEntityId":{"type":"string","format":"uuid"},"buyerSubjectId":{"type":"string","format":"uuid","nullable":true},"issuedAt":{"type":"string","format":"date-time"},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmountInLegalCurrency":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"legalFxRate":{"allOf":[{"$ref":"#/components/schemas/FxRateValue"}],"nullable":true,"readOnly":true,"description":"The invoice's own `legalFxRate`, never today's (CHG-FIN-011)."},"invoiceSupplyValue":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"**The value of the supply shown on the tax invoice** (Executive Regulation Art. 60(1)(e)), adjusted by any earlier credit note on the same invoice. With `correctedSupplyValue` and `netAmount` (the difference) and `taxAmountInLegalCurrency` (the tax on the difference in AED), the four figures the law requires (CHG-FIN-011)."},"correctedSupplyValue":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"The correct value of the supply after this credit note (Art. 60(1)(e))."},"supplierName":{"type":"string","readOnly":true,"description":"Snapshot of the legal entity at issue, as on the invoice (Art. 60(1)(b))."},"supplierAddress":{"type":"string","nullable":true,"readOnly":true},"supplierTaxRegistrationNumber":{"type":"string","nullable":true,"readOnly":true},"buyerName":{"type":"string","nullable":true,"readOnly":true,"description":"The recipient as on the invoice; name, address and TRN where they are registered (Art. 60(1)(c))."},"buyerAddress":{"type":"string","nullable":true,"readOnly":true},"buyerTaxRegistrationNumber":{"type":"string","nullable":true,"readOnly":true},"note":{"type":"string","nullable":true,"description":"The brief explanation of why the credit note was issued, printed on it (Art. 60(1)(f)); the reason's own wording when no note is given (CHG-FIN-011)."},"renditionAssetId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"eInvoiceStatus":{"$ref":"#/components/schemas/FinEInvoiceTransmissionStatus"},"issuedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"lines":{"type":"array","items":{"$ref":"#/components/schemas/FinCreditMemoLine"}},"scopePath":{"type":"string","readOnly":true}}},
"FinCreditMemoLine": {"type":"object","required":["invoiceLineNumber","netAmount","taxAmount","grossAmount"],"properties":{"invoiceLineNumber":{"type":"integer","minimum":1},"description":{"type":"string","maxLength":500},"quantity":{"type":"number","nullable":true},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxRate":{"type":"number"},"taxCategory":{"$ref":"#/components/schemas/FinTaxCategory"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},
"FinEInvoiceTransmissionStatus": {"type":"string","description":"6.1.1. `notRequired` where the legal entity's provider is `disabled` or absent.","enum":["notRequired","queued","sent","accepted","rejected","failed"]},
"FinIssueTaxInvoiceRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["invoiceType","orderIds"],"properties":{"invoiceType":{"$ref":"#/components/schemas/FinTaxInvoiceType"},"orderIds":{"type":"array","minItems":1,"description":"One order for `simplified` and `full`; one or more for `consolidated`. Every order must be paid, of one buyer, one legal entity and one currency.","items":{"type":"string","format":"uuid"}},"recipient":{"$ref":"#/components/schemas/FinTaxInvoiceRecipient"},"languages":{"type":"array","description":"Overrides the template's languages for this document, within those the template offers.","items":{"type":"string","pattern":"^[a-z]{2}(-[A-Z]{2})?$"}},"supersedesInvoiceId":{"type":"string","format":"uuid","nullable":true,"description":"A simplified invoice this full invoice replaces for the same supply. Refused unless the law allows it (make-or-break on issueTaxInvoice)."},"deliverToEmail":{"type":"string","format":"email","nullable":true,"description":"Sends the PDF on issue as well as returning it."}}},
"FinTaxCategory": {"type":"string","description":"How a line is treated for VAT. Taken from the tax code the line was posted with.","enum":["standardRated","zeroRated","exempt","outOfScope","reverseCharge"]},
"FinTaxDocumentRendition": {"x-ticvai-persistence":"none — a signed link to the stored PDF","type":"object","required":["documentId","documentKind","url","expiresAt"],"properties":{"documentId":{"type":"string","format":"uuid"},"documentKind":{"type":"string","enum":["taxInvoice","creditMemo"]},"documentNumber":{"type":"string"},"language":{"type":"string","nullable":true},"contentType":{"type":"string","default":"application/pdf"},"url":{"type":"string","format":"uri"},"expiresAt":{"type":"string","format":"date-time"}}},
"FinTaxInvoice": {"x-ticvai-persistence":"ledger.tax_invoice + ledger.tax_invoice_line","type":"object","description":"5.7.93, 5.10.3. **A guest tax invoice, as issued, never edited.** Corrections are credit memos. The supplier block is a snapshot of the legal entity at issue, so a later change of address does not change a document already given to a guest.","required":["id","invoiceNumber","invoiceType","status","legalEntityId","issuedAt","supplyDate","currency","netAmount","taxAmount","grossAmount","lines"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"invoiceNumber":{"type":"string","readOnly":true,"description":"Server-assigned from the legal entity's series for the document kind, in sequence and without gaps, e.g. `INV-2026-000123`. Never reused."},"invoiceType":{"$ref":"#/components/schemas/FinTaxInvoiceType"},"status":{"$ref":"#/components/schemas/FinTaxInvoiceStatus"},"legalEntityId":{"type":"string","format":"uuid"},"templateId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"orderIds":{"type":"array","items":{"type":"string","format":"uuid"}},"supplierName":{"type":"string"},"supplierAddress":{"type":"string","nullable":true},"supplierTaxRegistrationNumber":{"type":"string","nullable":true},"buyerSubjectId":{"type":"string","format":"uuid","nullable":true,"description":"The guest the orders belong to; the key a guest's own reads filter on."},"buyerName":{"type":"string","nullable":true},"buyerAddress":{"type":"string","nullable":true},"buyerCountryCode":{"type":"string","pattern":"^[A-Z]{2}$","nullable":true},"buyerTaxRegistrationNumber":{"type":"string","nullable":true},"customerAccountId":{"type":"string","format":"uuid","nullable":true},"issuedAt":{"type":"string","format":"date-time"},"supplyDate":{"type":"string","format":"date","description":"The date of supply where it differs from the issue date (the latest order's payment date on a consolidated invoice). A day in the region's time zone."},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"discountAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmountInLegalCurrency":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"The tax in the legal entity's currency (AED in the UAE) where the invoice currency differs. **In the UAE the converted amounts use the UAE Central Bank rate at the date of supply** (Decree-Law Art. 69) and the rate is printed (`legalFxRate`, Executive Regulation Art. 59(1)(k)); CHG-FIN-011."},"legalCurrency":{"type":"string","pattern":"^[A-Z]{3}$","readOnly":true,"description":"The legal entity's currency (AED in the UAE), in which the law requires the tax and the gross amount (CHG-FIN-011)."},"grossAmountInLegalCurrency":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"The gross amount payable in the legal currency (Executive Regulation Art. 59(1)(j); for a simplified invoice the total consideration, Art. 59(2)(e)). Equal to `grossAmount` when the invoice is in the legal currency (CHG-FIN-011)."},"legalFxRate":{"allOf":[{"$ref":"#/components/schemas/FxRateValue"}],"nullable":true,"readOnly":true,"description":"Units of the legal currency per one unit of `currency`, printed with the tax where the invoice is not in the legal currency (Art. 59(1)(k)). Null when it is (CHG-FIN-011)."},"legalFxRateSource":{"allOf":[{"$ref":"#/components/schemas/FxRateSource"}],"nullable":true,"readOnly":true,"description":"`uaeCentralBank` for a UAE legal entity (Decree-Law Art. 69)."},"paidCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"Where the guest paid in a currency they selected (`orders.Order.chargeCurrency`, CHG-FIN-001), printed as payment information with `paidAmount` and the charge rate. The invoice itself is in the base currency, so the AED amounts the law requires are the invoice's own figures (CHG-FIN-011)."},"paidAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"What the guest paid in `paidCurrency` (`orders.Order.chargeTotal`)."},"reverseChargeStatement":{"type":"string","nullable":true,"readOnly":true,"description":"Where the recipient must account for the tax, the statement saying so and the Decree-Law provision (Art. 59(1)(l), Art. 48). Null otherwise (CHG-FIN-011)."},"creditedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"languages":{"type":"array","items":{"type":"string"}},"supersedesInvoiceId":{"type":"string","format":"uuid","nullable":true},"renditionAssetId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The PDF rendered at issue; read through getTaxDocumentRendition."},"eInvoiceStatus":{"$ref":"#/components/schemas/FinEInvoiceTransmissionStatus"},"issuedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Null where the platform issued it."},"lines":{"type":"array","items":{"$ref":"#/components/schemas/FinTaxInvoiceLine"}},"taxSummary":{"type":"array","x-ticvai-persisted":false,"description":"VAT per rate and category, summed from the lines for the response.","items":{"type":"object","properties":{"taxCategory":{"$ref":"#/components/schemas/FinTaxCategory"},"taxRate":{"type":"number"},"taxableAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Written at the scope of the venue the orders were sold at, or the region for a consolidated invoice across venues."}}},
"FinTaxInvoiceLine": {"type":"object","description":"One line as it was sold and taxed. Amounts are in the invoice currency.","required":["lineNumber","description","quantity","netAmount","taxAmount","grossAmount","taxCategory"],"properties":{"lineNumber":{"type":"integer","minimum":1},"orderId":{"type":"string","format":"uuid"},"orderLineId":{"type":"string","format":"uuid","nullable":true},"description":{"type":"string","maxLength":500},"quantity":{"type":"number"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"discountAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxCodeId":{"type":"string","format":"uuid","nullable":true},"taxRate":{"type":"number","minimum":0,"maximum":100},"taxCategory":{"$ref":"#/components/schemas/FinTaxCategory"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"creditedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmountInLegalCurrency":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"The amount payable for the line in the legal currency (AED), Executive Regulation Art. 59(1)(h); equal to `grossAmount` on an invoice in the legal currency (CHG-FIN-011)."}}},
"FinTaxInvoiceRecipient": {"x-ticvai-persistence":"none — copied onto the invoice as buyer columns","type":"object","description":"Who the invoice is addressed to. Required for `full` and `consolidated`.","required":["name"],"properties":{"name":{"type":"string","maxLength":300},"address":{"type":"string","maxLength":1000,"nullable":true},"countryCode":{"type":"string","pattern":"^[A-Z]{2}$","nullable":true},"taxRegistrationNumber":{"type":"string","maxLength":30,"nullable":true,"description":"The recipient's TRN where they are VAT-registered."},"customerAccountId":{"type":"string","format":"uuid","nullable":true,"description":"The B2B credit account (payments `B2bCreditAccount`) where a company is invoiced."}}},
"FinTaxInvoiceStatus": {"type":"string","description":"`issued` until a credit memo is issued against it; `superseded` where a full invoice replaced a simplified one for the same supply (only if the law allows it; see issueTaxInvoice).","enum":["issued","partiallyCredited","fullyCredited","superseded"]},
"FinTaxInvoiceType": {"type":"string","description":"5.7.93. `simplified` for one order with no recipient details, `full` for one order with them, `consolidated` for several paid orders of one buyer on one invoice.\n**When a simplified tax invoice is allowed in the UAE** (research 2 October 2026, CHG-FIN-011; Executive Regulation, Cabinet Decision 52 of 2017 as amended, Art. 59(5)): the recipient is not VAT-registered, or is registered and the consideration does not exceed AED 10,000, and the reverse charge does not apply. Otherwise the invoice is `full`. Both kinds carry the title \"Tax Invoice\" (Art. 59(1)(a), 59(2)(a)); a simplified one is issued on the date of supply (Art. 59(13)(1)), a full one within 14 days (Decree-Law Art. 67(1)).","enum":["simplified","full","consolidated"]},
"FxRateSource": {"type":"string","description":"**Where the rate came from, and which provider specifically.** `source: provider` said a feed set it and not which one — two tenants on different feeds were indistinguishable in the ledger, and a rate cannot be defended in an audit without naming its origin.\n\n**`uaeCentralBank` is the default for AED pairs.** The UAE Central Bank publishes an official daily rate and it is what a UAE auditor expects to see — a commercial feed is defensible for tender and awkward for statutory reporting.\n\n**`openExchangeRates` and `ecb` are the commercial and reference options.** ECB publishes daily reference rates free and is the usual fallback for non-AED pairs; Open Exchange Rates is the common commercial feed with intraday granularity. **The choice is per purpose, not per platform** — a tender rate wants intraday, a reporting rate wants the official daily close.","enum":["manual","uaeCentralBank","ecb","openExchangeRates","cardScheme","provider"]},
"FxRateValue": {"x-ticvai-persistence-column":"numeric(18,6)","type":"string","pattern":"^\\d+(\\.\\d{1,6})?$","description":"**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one (naming-and-style 5.1). Up to six decimal places — a two-place rate on a three-place currency loses money on every transaction, quietly — and stored as `numeric(18,6)` so the six places the wire carries survive the database.\n"},
"GuestPreferences": {"type":"object","x-ticvai-persistence":"marketing.guest_preference","description":"**What the guest likes, kept apart from what they permit** (consent) and from who they are (the profile). One row per subject. `dietary` and `accessibility` are here rather than as tags because BL-134 gives them their own consent purpose and retention.\n","properties":{"id":{"type":"string","format":"uuid","readOnly":true},"subjectId":{"type":"string","format":"uuid","readOnly":true},"seatingPreference":{"type":"string","nullable":true,"maxLength":200},"drinkPreferences":{"type":"array","items":{"type":"string"}},"dietary":{"type":"array","description":"Also written by `updateMyProfile`.","items":{"type":"string"}},"accessibility":{"type":"array","description":"Also written by `updateMyProfile`.","items":{"type":"string"}},"preferredChannel":{"allOf":[{"$ref":"#/components/schemas/MessageChannel"}],"x-ticvai-persisted":false,"description":"**Stored on the profile** (`GuestProfile.preferredChannel`) — carried here because the preference screen edits it beside the rest.\n"},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"GuestProfile": {"x-ticvai-persistence":"marketing.guest_profile","type":"object","required":["subjectId","isActive"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"subjectId":{"type":"string","format":"uuid","description":"Opaque reference. Personal data lives in the separately erasable store, which is what makes erasure possible against an append-only ledger.\n"},"displayName":{"type":"string","nullable":true},"email":{"type":"string","nullable":true},"phone":{"type":"string","nullable":true},"preferredLanguage":{"type":"string","nullable":true},"preferredChannel":{"$ref":"#/components/schemas/MessageChannel"},"guestLinkId":{"type":"string","nullable":true,"description":"Present where the guest is linked across cells. Marketing acts locally."},"tags":{"type":"array","items":{"type":"string"}},"engagementScore":{"type":"integer","nullable":true,"minimum":0,"maximum":100,"description":"22.2.20 and 22.2.21. **`lifetimeValue` and `visitCount` existed, so value was a stored figure and engagement was not.** They are different questions: a guest who spent a lot once and a guest who visits monthly have the same LTV and need opposite treatment.\n**Recency, frequency and breadth, not spend** — spend is already `lifetimeValue`, and folding it in here would make one number twice.\n"},"engagementTier":{"type":"string","nullable":true,"enum":["new","active","occasional","lapsing","lapsed","dormant"],"description":"5.3.19. **Automatic classification, computed rather than assigned.** `lapsing` is the tier the whole field exists for — **a guest who has not been for a while and still might is the only one marketing can change**, and lumping them with `lapsed` wastes the window.\n"},"lifetimeValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"visitCount":{"type":"integer"},"lastVisitAt":{"type":"string","format":"date-time","nullable":true},"isActive":{"type":"boolean"},"mergedIntoSubjectId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Set on the absorbed profile by `mergeGuestProfiles` and `mergeGuests`**, which retain it as a redirect rather than deleting it. A read that lands here follows it; a second merge of a profile that has one is refused as `alreadyMerged`.\n"},"mergedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"GuestSession": {"x-ticvai-persistence":"none — Redis session registry","type":"object","required":["subjectId","tokens","isVerified","expiresAt"],"properties":{"subjectId":{"type":"string","format":"uuid"},"displayName":{"type":"string","nullable":true},"tokens":{"$ref":"#/components/schemas/TokenPair"},"isVerified":{"type":"boolean","description":"False until an OTP or a verified provider identity confirms ownership. An unverified account may browse and fill a cart but not transact: the gate is the checkout page (ADR-0045), where `checkoutCart` refuses it until the guest verifies or proves the contact by code. UAE Pass returns a verified identity, so it starts true. Rule on `verifyGuestEmail`, decided 17 September 2026.\n"},"identityProviders":{"type":"array","description":"Linked providers. Several may resolve to one account.","items":{"type":"string","enum":["password","otp","apple","google","uaePass"]}},"guestLinkId":{"type":"string","nullable":true,"description":"Present where the guest is linked across cells (ADR-0010)."},"requiresMfa":{"type":"boolean","default":false,"description":"True only where the sign-in venue enabled guest two-step verification (`VenueSettings.identity.guestTwoStep`, in tenancy) and this guest has an active method (decided 29 September, rev 3 GAP-B1, per venue). The session is then not usable until `verifyMfaChallenge` succeeds on a `signIn` challenge. Always false for a UAE Pass sign-in, which is already a verified two-factor identity (proposed, client to correct).\n"},"mfaMethods":{"type":"array","description":"The guest's active methods, so the client can offer the right one. Empty when `requiresMfa` is false.","items":{"$ref":"#/components/schemas/MfaMethod"}},"homeCellName":{"type":"string","nullable":true},"preferredLanguage":{"type":"string","nullable":true},"expiresAt":{"type":"string","format":"date-time","description":"**30 days, sliding** (decided 28 September, audit R126 (2)): each use of the session moves this to 30 days from now, and 30 days unused ends it. **One session per device**: a guest may be signed in on a phone and a laptop at once, and a new sign-in on the same `deviceId` ends that device's previous session.\n"}}},
"IdentityGuestDocumentSubmission": {"type":"object","x-ticvai-persistence":"none — request only; the document goes to pii.subject_document and the verification to identity.guest_identity_verification","required":["documentKind","documentNumber","documentAssetId"],"properties":{"documentKind":{"type":"string","enum":["passport","emiratesId","nationalId","drivingLicence","residencePermit","other"],"description":"The vocabulary of `pii.subject_document.kind`."},"documentNumber":{"type":"string","format":"password","writeOnly":true,"maxLength":64,"description":"**Write-only, never returned.** Hashed on arrival; only the last four are kept in clear."},"issuingCountry":{"type":"string","pattern":"^[A-Z]{2}$","nullable":true},"expiresOn":{"type":"string","format":"date","nullable":true},"documentAssetId":{"type":"string","format":"uuid","description":"The uploaded scan or photo of the document."},"selfieAssetId":{"type":"string","format":"uuid","nullable":true,"description":"A live photo for the reviewer to compare, where the policy asks for one. Deleted with the scan."},"reason":{"type":"string","enum":["policyRequired","ageRestrictedPurchase","residentPricing","accountRecovery"],"default":"policyRequired","description":"What the guest is verifying for; the review queue shows it."}}},
"IdentityGuestVerification": {"type":"object","x-ticvai-persistence":"identity.guest_identity_verification","description":"**One guest identity-document verification** (5.3.21; decided 29 September, build pass): the document it checks, its status, the method and who decided. The document itself is `pii.subject_document`; this row holds no document number.","required":["id","subjectId","status","submittedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"subjectId":{"type":"string","format":"uuid"},"subjectDocumentId":{"type":"string","format":"uuid","description":"The `pii.subject_document` row submitted."},"documentKind":{"type":"string","enum":["passport","emiratesId","nationalId","drivingLicence","residencePermit","other"]},"documentNumberLast4":{"type":"string","maxLength":4,"nullable":true,"readOnly":true},"reason":{"type":"string","enum":["policyRequired","ageRestrictedPurchase","residentPricing","accountRecovery"]},"status":{"type":"string","enum":["pending","verified","rejected","resubmissionRequested"],"readOnly":true},"method":{"type":"string","enum":["manualReview","documentScanner","provider"],"nullable":true,"readOnly":true},"decisionReason":{"type":"string","maxLength":300,"nullable":true,"readOnly":true},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"submittedAt":{"type":"string","format":"date-time","readOnly":true},"decidedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"documentImageDeletedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When the scan (and any selfie) was deleted under the policy's retention."}}},
"Invitation": {"type":"object","x-ticvai-persistence":"marketing.invitation","description":"**Addressed and tokenised.** A guest accepting an invitation is claiming a specific place, not buying one.\n","required":["id","campaignId","token","status"],"properties":{"id":{"type":"string","format":"uuid"},"campaignId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true},"recipientEmail":{"type":"string","format":"email","nullable":true},"token":{"type":"string","description":"**Single-use and unguessable.** An invitation link forwarded to a group chat is the failure mode, and a token that survives its first use is one that ends up there.\n"},"plusOnes":{"type":"integer","default":0},"status":{"type":"string","enum":["issued","viewed","accepted","declined","expired","revoked"]},"entitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}},"respondedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"LoyaltyProgramme": {"x-ticvai-persistence":"marketing.loyalty_programme + marketing.points_earning_rule + marketing.programme_tier","type":"object","required":["id","code","name","earnRules","tiers"],"properties":{"tiers":{"type":"array","description":"**Rows of `marketing.programme_tier`**, the same shape `MarketingProgrammeTier` has — one definition of a tier, not a second copy that cannot round-trip. `loyaltyProgrammeId` and `id` are the server's on create.\n","items":{"$ref":"#/components/schemas/MarketingProgrammeTier"}},"id":{"readOnly":true,"type":"string","format":"uuid"},"code":{"type":"string","x-ticvai-unique":"tenant","description":"**Unique per tenant** (decided 28 September, audit R108). A code already used by any loyalty programme in the tenant, at any venue, is refused with `409 duplicate-code`.\n"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid","nullable":true},"pointsLiabilityAccountId":{"type":"string","format":"uuid","description":"Points post here on accrual. They are a liability from the moment they are earned, not from the moment they are spent.\n"},"earnRules":{"type":"array","items":{"type":"object","required":["trigger","points"],"properties":{"trigger":{"type":"string","enum":["perCurrencyUnit","perVisit","perProduct","onSignup","onBirthday","onReview"]},"points":{"type":"number"},"productKinds":{"type":"array","description":"Limits a `perProduct` or `perCurrencyUnit` rule to these kinds. Empty means every kind.","items":{"$ref":"../spine/catalogue.yaml#/components/schemas/ProductKind"}},"multiplier":{"type":"number"}}}},"pointsExpireAfterMonths":{"type":"integer","nullable":true},"isActive":{"type":"boolean"}}},
"MarketingProgrammeTier": {"type":"object","x-ticvai-persistence":"marketing.programme_tier","description":"**The tier definition decision 8 promised and nobody built.** `marketing.loyalty_position` carried `tierCode`, `tierName` and `pointsToNextTier` as denormalised strings and a number, with no table saying what tiers exist or what each one requires — so `pointsToNextTier` was computed from a threshold that lived nowhere.\n**Not named `marketing.loyalty_tier`**: that name is recorded in `schema-history.json` as renamed to `marketing.points_earning_rule` on 20 September, and a rename record that contradicts the schema is worse than a longer name. Not named `marketing.tier` either, because `subscription.tier_allowance` is a SaaS plan's tier and one bare `tier` in a package with two tier concepts is how `plan_id` came to point at `subscription.plan`.\n**The denormalised copy on the position stays.** A till rendering *Gold* beside a balance must not join, and must certainly not cross a cell boundary to print a word. This table is the source of truth and those columns are its cache.\n","required":["loyaltyProgrammeId","code","name","rank"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"loyaltyProgrammeId":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string","maxLength":40},"name":{"type":"string","maxLength":120},"rank":{"type":"integer","description":"**Order, not threshold.** Two tiers can share a qualifying rule and still have an order, and sorting by points breaks the moment a tier is granted rather than earned.\n"},"minLifetimePoints":{"type":"integer","nullable":true,"description":"What reaching this tier requires. **`pointsToNextTier` on the position is this minus the guest's lifetime points**, and until now it was this minus nothing.\n"},"retainLifetimePoints":{"type":"integer","nullable":true,"description":"What keeping it requires, per review period. **Usually lower than reaching it**, and a scheme that cannot express the difference either never demotes or demotes on the day a guest stops earning.\n"},"validityMonths":{"type":"integer","nullable":true,"description":"Null means the tier does not lapse on its own."},"benefits":{"type":"array","description":"What the tier gives, as the guest reads it. Text shown, not rules enforced.","items":{"type":"string"}},"earnMultiplier":{"type":"number","nullable":true,"description":"Applied to every earn rule while the guest holds this tier. Null means 1."},"isActive":{"type":"boolean","default":true}}},
"MessageChannel": {"type":"string","enum":["email","sms","whatsapp","push","inApp","post"]},
"MfaMethod": {"x-ticvai-persistence":"identity.mfa_method","type":"object","required":["id","kind","isActive","enrolledAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/MfaKind"},"label":{"type":"string","nullable":true},"maskedTarget":{"type":"string","nullable":true,"description":"Partially masked destination, so a person can tell two methods apart."},"isActive":{"type":"boolean"},"isPrimary":{"type":"boolean"},"enrolledAt":{"type":"string","format":"date-time"},"lastUsedAt":{"type":"string","format":"date-time","nullable":true}}},
"Order": {"x-ticvai-persistence":"orders.sales_order + orders.order_line","type":"object","required":["id","venueId","scopePath","channel","status","currency","currencyScale","grossAmount","taxAmount","netAmount","lines","createdAt","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The client UUIDv7 from `CreateOrderRequest.id`."},"orderNumber":{"type":"string","readOnly":true,"description":"The number a guest reads and a cashier types. **Server-assigned: the venue prefix and a sequence per venue**, for example `DXB1-000123` (decided 28 September, audit R152). A till holds a reserved range of the venue sequence, so an order taken offline gets its number on the till and keeps it through `syncOrders`. **Not gapless**: an unused reserved range leaves a gap, and that is allowed. Only tax invoices are gapless, per legal entity. The receipt carries this number.\n"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for within a month of launch.\n"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"chargeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**The currency the guest selected and is charged in** (CHG-FIN-001, 2 October 2026). Null or equal to `currency` for a sale in the base currency. Everything else on the order, and every ledger posting, stays in the base currency `currency`."},"chargeFxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"readOnly":true,"description":"Units of `chargeCurrency` per one unit of the base currency, from the region's `tender` rate in force at checkout (`finance.FxRate`), stored on the order so the payment, the receipt, the tax invoice and any refund use the same rate (CHG-FIN-001)."},"chargeFxRateId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `finance.FxRate` row the rate was taken from, for audit."},"chargeTotal":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"`grossAmount` converted at `chargeFxRate` and rounded to the charge currency's scale: what the guest pays and what the payment request to the provider asks for (CHG-FIN-001)."},"chargeRateLockedUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"The quote holds until then (the cart lease). After it, the next payment attempt re-quotes at the rate then in force and the guest confirms the new amount (CHG-FIN-001)."},"droppedPromotions":{"type":"array","readOnly":true,"x-ticvai-persisted":false,"description":"**Promotions left off this order at checkout because their budget cap would have been exceeded** (decided 28 September, audit R101 (8)). Empty when none was dropped. Returned by `checkoutCart` and `createOrder`, not stored.\n","items":{"type":"object","required":["promotionId"],"properties":{"promotionId":{"type":"string","format":"uuid"},"name":{"type":"string"},"reason":{"type":"string","enum":["budgetCapReached"]}}}},"totalPriceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Sum across lines. Zero on a normal order."},"lines":{"type":"array","items":{"$ref":"#/components/schemas/OrderLine"}},"payments":{"type":"array","items":{"$ref":"#/components/schemas/Payment"}},"principalId":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid"},"shiftId":{"type":"string","format":"uuid","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"holdLabel":{"type":"string","maxLength":60,"nullable":true,"readOnly":true,"description":"The `label` a cashier gave when parking it with `holdOrder` — how they find it again. Null on an order never held."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When a held order expires and is voided (states/order.yaml), from `holdOrder`'s `holdUntil`. Null on an order not currently held."},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"OrderChannel": {"type":"string","description":"Where the order originated. Added when guest self-ordering was contracted — an order a guest placed on their own phone is commercially and operationally different from one a cashier typed, and reporting that cannot separate them cannot answer whether self-ordering is working.\n","enum":["pos","kiosk","guestApp","guestWeb","callCentre","partner","api","backOffice"]},
"OrderLine": {"x-ticvai-persistence":"orders.order_line + orders.order_line_eligibility + orders.order_line_discount","x-ticvai-retired-columns":["promotion_id","name","reason"],"allOf":[{"$ref":"#/components/schemas/CreateOrderLine"},{"type":"object","required":["serverUnitPrice","taxAmount","netAmount","grossAmount"],"properties":{"serverUnitPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the server computed on ingest."},"priceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Server minus quoted. Non-zero means the quoted price was honoured and the difference posted to the variance account.\n"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"entitlementIds":{"type":"array","description":"The entitlements this line issued. **These are the ticket ids** — `transferOrderTickets.ticketIds` and `reprintOrder.reissuedTicketIds` take and return them.","items":{"type":"string","format":"uuid"}},"crossRegionRightIds":{"type":"array","items":{"type":"string"},"description":"Redemption rights propagated to other cells for this line."},"reprintCount":{"type":"integer","minimum":0,"default":0,"readOnly":true,"description":"How many times this line's tickets were reprinted or resent. `reprintOrder` increments it; repeated reprints are the signal worth surfacing."},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"The order's venue, copied onto the line (ADR-0044's own example; system-design review SD-008, 29 September) so a line is scoped and partitionable without its order."},"discounts":{"type":"array","readOnly":true,"description":"**The discounts applied to this line, one row each** (system-design review SD-008, 29 September). Until then a discount object was flattened into the line as `promotion_id NOT NULL`, so a line with no promotion could not be inserted. A line with no discount has none.","items":{"$ref":"#/components/schemas/OrderLineDiscount"}}}}]},
"OrderStatus": {"type":"string","enum":["pending","held","paid","partiallyPaid","completed","voided","refunded","partiallyRefunded","failed"],"description":"`held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed.\n"},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Payment": {"x-ticvai-persistence":"orders.payment","type":"object","required":["id","orderId","tender","amount","status","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid"},"tender":{"$ref":"#/components/schemas/TenderKind"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","description":"4.6.11. **What the guest actually handed over**, which is not always what the venue books. A tourist paying USD cash at a till is a foreign tender; the sale is still recorded in base currency.\nEqual to the base currency for almost every payment. **Present on all of them so the foreign-tender report has a source** — `getForeignTenderReport` promised *what was taken in which currency* and nothing recorded it until 18 August.\n"},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"The amount in `tenderCurrency`, at that currency's own scale."},"fxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"description":"The rate applied, **stored on the payment rather than looked up later** (CF-37). A payment reconciled next month is reconciled at the rate of the day it was taken.\n"},"fxRateSource":{"type":"string","nullable":true,"enum":["manual","feed","cardScheme"],"description":"4.2.8. Manual or fed on a schedule. **`cardScheme` is where the terminal did the conversion and told us** — dynamic currency conversion, the scheme's rate rather than ours.\n"},"changeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"description":"4.6.11 is deliberately asymmetric: **accept foreign currency, refund in local.** A till giving change in five currencies needs five floats and five counts, and the variance becomes unattributable.\n**Cash at a till only** (CHG-FIN-001, 2 October 2026). A card or wallet payment the guest made in a currency they selected is refunded in that currency (`Refund.tenderCurrency`).\n"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"changeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["authorised","captured","pendingConfirmation","declined","failed","voided","refunded"]},"providerName":{"type":"string","nullable":true},"providerReference":{"type":"string","nullable":true,"description":"The provider's own id for the charge (Stripe PaymentIntent, NI order reference). What `payments.receivePaymentProviderWebhook` matches an incoming event on (SD-034)."},"providerIdempotencyKey":{"type":"string","nullable":true,"readOnly":true,"description":"The idempotency key sent to the provider, which is this payment's `id` (SD-034, 29 September). A retried provider call cannot charge twice."},"terminalId":{"type":"string","format":"uuid","nullable":true,"description":"The card terminal a till payment ran on (ECR flow, SD-034)."},"nextAction":{"type":"object","nullable":true,"x-ticvai-persisted":false,"description":"**What the caller does while the payment is `pendingConfirmation`** (SD-034, 29 September). `redirect`: send the browser to `url` (3-D Secure challenge or hosted page); the provider returns the guest to `returnUrl` and the result arrives by webhook. `terminal`: the card terminal has been instructed; wait for its result. Null once the payment has an outcome.","properties":{"kind":{"type":"string","enum":["redirect","terminal"]},"url":{"type":"string","format":"uri","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true}}},"lastInquiryAt":{"type":"string","format":"date-time","nullable":true},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"RecordConsentRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["purpose","decision","noticeVersion","source","recordedAt"],"properties":{"purpose":{"$ref":"#/components/schemas/ConsentPurpose"},"decision":{"$ref":"#/components/schemas/ConsentDecision"},"channels":{"type":"array","description":"Omit to apply to every channel the purpose covers.","items":{"$ref":"#/components/schemas/MessageChannel"}},"noticeVersion":{"type":"string"},"source":{"$ref":"#/components/schemas/ConsentSource"},"recordedAt":{"type":"string","format":"date-time"}}},
"RegisterGuestRequest": {"type":"object","required":["identifier","channel"],"properties":{"identifier":{"type":"string","maxLength":256,"description":"Email address or mobile number in E.164."},"channel":{"type":"string","enum":["email","sms","whatsapp"]},"displayName":{"type":"string","maxLength":200},"password":{"type":"string","minLength":8,"maxLength":256,"writeOnly":true,"description":"Optional. OTP-only accounts are supported and are the default."},"preferredLanguage":{"type":"string","pattern":"^[a-z]{2}$"},"consents":{"type":"array","description":"Consent captured at registration, recorded with the notice version.","items":{"type":"object","properties":{"purpose":{"type":"string"},"granted":{"type":"boolean"},"noticeVersion":{"type":"string"}}}}}},
"Session": {"type":"object","required":["sessionId","principalId","roleId","scope","effectivePermissions"],"properties":{"sessionId":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid"},"roleId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"scope":{"type":"array","description":"Scope nodes this session may act within, resolved once at login from the ltree hierarchy with deny-overrides-allow. Clients filter navigation against this — they never compute it.\n","items":{"$ref":"../shared/common.yaml#/components/schemas/ScopeRef"}},"effectivePermissions":{"allOf":[{"$ref":"../shared/permissions.yaml#/components/schemas/PermissionSet"}],"description":"Flattened set across all granted scopes, after deny resolution. Convenience for coarse checks. Anything scope-sensitive must use `permissionsByScope`.\n"},"permissionsByScope":{"type":"array","description":"Permissions effective at each granted scope path. Clients filter navigation on this and never compute permissions themselves.\n","items":{"$ref":"../shared/permissions.yaml#/components/schemas/ScopedPermissions"}},"saleBoardId":{"type":"string","format":"uuid","description":"Landing surface, derived from the WORKSTATION, not the role (12 Aug 2026 §3). Ticketing, F&B or Retail board.\n\n**Optional since 2 October 2026: only a till session carries it** (Chinmay, door follow-ups; CHG-CSP-002; breaking change against r1 approved as BC-001 to BC-005 in `docs/active/breaking-changes.yaml`). A browser door (ADM-001, SUP-001, PTR-001) and a staff handheld (EMP-001) sign in with no workstation since CHG-DOOR-001, so they have no board to land on and the field is absent. On a till it is the workstation's effective board: the outlet's board unless the till overrides it (`tenancy.Workstation.saleBoardSource`; CHG-CSP-006). A client reads its landing from this field when present and from its own platform otherwise.\n"},"workstation":{"$ref":"#/components/schemas/WorkstationContext"},"openedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time"}}},
"TokenPair": {"x-ticvai-persistence":"none — transient","type":"object","required":["accessToken","refreshToken","expiresIn"],"properties":{"accessToken":{"type":"string","description":"JWT carrying `sid`, validated per request against the session registry."},"refreshToken":{"type":"string"},"expiresIn":{"type":"integer","description":"Seconds"}}},
"Wallet": {"x-ticvai-persistence":"wallet.wallet + wallet.credit_lot","type":"object","required":["subjectId","balance","currency","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"subjectId":{"type":"string","format":"uuid"},"balance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"credits":{"type":"array","description":"4.3.5 and 4.3.19. **One balance and one bonus balance with one expiry could not express what the requirement asks for** — cash, bonus and redemption credit, each with its own expiry.\n**The expiries are the reason this is a list.** Cash a guest paid for should outlive a promotional credit they were given, and a single `expiresAt` either expires the money they paid or never expires the promotion.\n**Consumed first-expiry-first-out across all three** (4.3.19), which is also the order that is fairest to the guest — spend what is about to die before what is not.\n**One entry per `active` lot in `wallet.credit_lot`** for this wallet: `amount` is the lot's `remaining_amount`, `expiresAt` its `expires_at`, `sourceRef` its `source_reference`. `kind` and `isRefundable` are not stored on the lot; they come from the lot's credit type (`listCreditLots` returns the lots themselves).\n","items":{"type":"object","required":["kind","amount"],"properties":{"kind":{"type":"string","enum":["cash","bonus","redemption","refund","goodwill"],"description":"**`cash` is money the guest paid and the others are not.** That distinction decides what is refundable, what expires, and what shows as a liability.\n","x-ticvai-persisted":false},"amount":{"x-ticvai-column":"remaining_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"sourceRef":{"type":"string","nullable":true,"x-ticvai-column":"source_reference"},"isRefundable":{"type":"boolean","default":false,"x-ticvai-persisted":false,"description":"**True only for `cash`.** A guest cannot cash out a promotional credit, and a wallet that lets them has given away the promotion twice.\n"}}}},"bonusBalance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Promotional value. Typically non-refundable and spent first."},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"status":{"type":"string","enum":["active","suspended","closed"]},"homeCellName":{"type":"string","nullable":true,"description":"Where the authoritative balance lives. Present when the guest is linked across cells.\n"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"lastActivityAt":{"type":"string","format":"date-time","nullable":true}}},
"WalletPass": {"type":"object","x-ticvai-persistence":"orders.wallet_pass","description":"BL-029. **`appleWallet` and `googlePay` are feature toggles on the native apps** — there is no pass generation, no update push, no serial and no authentication token.\n**A wallet pass is a live object, not a download.** The value over a PDF is that it updates: a changed gate, a cancelled performance, a time that moved. **A pass that cannot be pushed to is a screenshot with better rounding.**\n","required":["id","entitlementId","platform","serialNumber","status"],"properties":{"id":{"type":"string","format":"uuid"},"entitlementId":{"type":"string","format":"uuid"},"platform":{"type":"string","enum":["apple","google"]},"serialNumber":{"type":"string"},"authenticationToken":{"type":"string","format":"password","writeOnly":true,"description":"**Write-only.** How the device proves it may fetch an update, and the reason a leaked serial alone is not enough to read somebody's ticket.\n"},"status":{"type":"string","enum":["issued","updated","voided","expired"]},"lastPushedAt":{"type":"string","format":"date-time","nullable":true},"deviceRegistrations":{"type":"integer","description":"How many devices hold it. **A guest with the pass on a phone and a watch is one entitlement and two registrations**, and both need the update.\n"},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"Wishlist": {"type":"object","required":["subjectId","items"],"x-ticvai-persistence":"none — wrapper. The items are the table, keyed by subject","properties":{"subjectId":{"type":"string","format":"uuid"},"items":{"type":"array","x-ticvai-persistence":"marketing.wishlist_item","items":{"type":"object","required":["id","variantId","addedAt","isAvailable"],"properties":{"id":{"type":"string","format":"uuid"},"variantId":{"type":"string","format":"uuid"},"productName":{"type":"string"},"performanceId":{"type":"string","format":"uuid","nullable":true},"performanceStartsAt":{"type":"string","format":"date-time","nullable":true},"price":{"x-ticvai-column":"list_price","$ref":"../shared/common.yaml#/components/schemas/Money","description":"The variant's current list price when the wishlist is read. Stored as `list_price` (naming-and-style 5.1 bans a bare `price` column); the wire keeps `price`."},"imageAssetRef":{"type":"string","nullable":true},"isAvailable":{"type":"boolean","description":"False where the product has been withdrawn or the performance has passed. Returned rather than dropped — a guest who saved something and finds it silently gone assumes the feature is broken.\n"},"unavailableReason":{"type":"string","nullable":true},"note":{"type":"string","nullable":true},"addedAt":{"type":"string","format":"date-time"}}}}}},
"WorkstationContext": {"type":"object","required":["id","code","venueId","regionId"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"regionId":{"type":"string","format":"uuid"},"accessPointId":{"type":"string","format":"uuid","description":"Inherited from the workstation, never selected by the operator."},"devices":{"type":"array","items":{"type":"object","required":["kind","driver"],"properties":{"kind":{"type":"string","enum":["receiptPrinter","ticketPrinter","cashDrawer","barcodeScanner","rfidReader","paymentTerminal","customerDisplay"]},"driver":{"type":"string"},"identifier":{"type":"string"}}}},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"currencyScale":{"type":"integer","minimum":0,"maximum":4},"timezone":{"type":"string"},"cellName":{"type":"string","description":"The cell serving this workstation's region. One cell per tenant per region (ADR-0014). A client uses this only for diagnostics and telemetry tagging — never for routing, which the Control Plane resolves.\n"},"deploymentProfile":{"type":"string","enum":["terminalLocal","venueEdge","thin"],"description":"Whether this surface reads catalogue locally (ADR-0013). Determines which flows the client enables offline.\n"}}}
}
```
