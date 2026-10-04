# WS163 — Resource Management Configuration board 9

**10 screens · 14 operations · 28 schemas · 7 permissions**

Platform P08 Venue Management · ships as **venue-management** ·
staff audience · web ·
online only

## Who this is for

**staff on web.** Everything below is how you know what is
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
  `APPROVAL_DECIDE, APPROVAL_VIEW, ATTENDANCE_RECORD, INCIDENT_REPORT, RESOURCE_BOOK, RESOURCE_VIEW, WORKFORCE_VIEW`. A control nobody can use must say so,
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
| `BO-933` | My Resource Operations Home | D | 0 | 28 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-934` | My Schedule & Assignment Calendar | D | 0 | 26 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `BO-935` | Assignment Detail & Operational Brief | D | 9 | 18 | 6 | 12 | 0 | 0 | — | notStarted (—) |
| `BO-936` | Mobile Staff Check-In & Check-Out | D | 0 | 18 | 6 | 3 | 1 | 0 | — | notStarted (—) |
| `BO-937` | Resource Collection, Handover & Return | D | 5 | 0 | 6 | 25 | 0 | 0 | — | notStarted (—) |
| `BO-938` | Employee Requests & Resource Support | D | 6 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-939` | Shift Change, Swap, Pickup & Release | B–D | 0 | 0 | 6 | 1 | 1 | 6 | — | notStarted (—) |
| `BO-940` | Manager Mobile Approval Center | B | 0 | 0 | 6 | 13 | 0 | 3 | — | notStarted (—) |
| `BO-941` | Operational Notifications & Live Alerts | D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-942` | Mobile Operations Control & Offline Sync | B | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-933, BO-936, BO-939, BO-940, BO-942 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-933` My Resource Operations Home

**Provide each employee with a personalized operational landing screen showing what requires their attention now and next.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-933 |
| Who uses it | venue staff holding `RESOURCE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§The screen shall display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/my-resource-operations-home-bo-933` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The employee's home in the Staff App for resource work: one card that always answers "What am I supposed to do now?" (NOW - Private Ski Lesson 14:00-15:00, Ski School Zone A, booking BK-28491, 3 participants, starts in 12 min, View assignment, Check in), the NEXT card, then alerts, pending tasks, handovers, requests and messages. The one thing to get right: it is a phone screen in the Staff App, big targets and minimal typing, and it keeps working on the cached day when the signal drops.

**Known correction pending (do not draw the wrong version)**

- **Board 9 screens are placed in the venue back office (venue-management-web) as P08 screens** Why: The pack says board 9 is exposed through the TICVAI Employee App, not a separate app; these belong to P06. *(source: screens/P08-venue-back-office.yaml#BO-933; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The home is drawn as a 14-column data table titled "Every resource operations home"** Why: It is a card layout; the pack's fourteen items are cards and chips. *(source: screens/P08-venue-back-office.yaml#BO-933; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **listResourceBookings has no "my assignments" filter** Why: The employee is a principal; the read filters by resourceId only, so the app must first resolve the person's resource. *(source: contracts/satellite/resources.yaml#listResourceBookings / contracts/satellite/resources.yaml#/components/schemas/Resource; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Resource | picker: choose a resource | — | — | `listResourceBookings` ?resourceId |
| From | date and time picker | — | — | `listResourceBookings` ?from |
| To | date and time picker | — | — | `listResourceBookings` ?to |
| Status | select | — | Reserved · Checked out · Returned · Overdue · Cancelled · No show | `listResourceBookings` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every resource operations home** (data table)

| Shows | Format | Notes |
|---|---|---|
| Current shift | text | not in the schema: `Current shift` |
| Current assignment | text | not in the schema: `Current assignment` |
| Next assignment | text | not in the schema: `Next assignment` |
| Today's schedule | text | not in the schema: `Today's schedule` |
| Assigned venue | text | not in the schema: `Assigned venue` |
| Check in status | text | not in the schema: `Check-in status` |
| Break status | text | not in the schema: `Break status` |
| Pending tasks | text | not in the schema: `Pending tasks` |
| Resource handovers | text | not in the schema: `Resource handovers` |
| Employee requests | text | not in the schema: `Employee requests` |
| Notifications | text | not in the schema: `Notifications` |
| Manager messages | text | not in the schema: `Manager messages` |
| Smart operational card | text | not in the schema: `Smart Operational Card` |
| “what am i supposed to do now?” | text | not in the schema: `“What am I supposed to do now?”` |

**The selected resource operations home** (detail panel): The pack groups this record's detail under its own headings: “Private Ski Lesson”, “Group Ski Lesson”, “Zone B”, “The employee may ask”.

| Shows | Format | Notes |
|---|---|---|
| Current shift | text | not in the schema: `Current shift` |
| Current assignment | text | not in the schema: `Current assignment` |
| Next assignment | text | not in the schema: `Next assignment` |
| Today's schedule | text | not in the schema: `Today's schedule` |
| Assigned venue | text | not in the schema: `Assigned venue` |
| Check in status | text | not in the schema: `Check-in status` |
| Break status | text | not in the schema: `Break status` |
| Pending tasks | text | not in the schema: `Pending tasks` |
| Resource handovers | text | not in the schema: `Resource handovers` |
| Employee requests | text | not in the schema: `Employee requests` |
| Notifications | text | not in the schema: `Notifications` |
| Manager messages | text | not in the schema: `Manager messages` |
| Smart operational card | text | not in the schema: `Smart Operational Card` |
| “what am i supposed to do now?” | text | not in the schema: `“What am I supposed to do now?”` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **NOW card**: Assignment title, time, location (zone), booking reference, participant count, a countdown ("Starts in 12 min") or "In progress", and the two primary buttons View assignment and Check in. *(source: screens/P08-venue-back-office.yaml#BO-933)*
- **NEXT card and day strip**: Next assignment with time and zone; a short strip of today's schedule linking to BO-934. *(source: screens/P08-venue-back-office.yaml#BO-934)*
- **Status row**: Current shift, check-in status, break status, assigned venue as chips at the top. *(source: screens/P08-venue-back-office.yaml#BO-933)*
- **Alerts**: "Your 15:30 assignment has moved to Zone C"; "Equipment package ready for collection"; "Your certification expires in 14 days" - newest first, each opening its screen. *(source: screens/P08-venue-back-office.yaml#BO-934)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Tiles**: My schedule (BO-934), Resources (handover BO-937), Requests; Check in opens attendance; AI assistant answers "What is my next assignment?". *(source: screens/P08-venue-back-office.yaml#BO-934 / screens/P08-venue-back-office.yaml#BO-933)*

**Data it reads**: `listResourceBookings` (onLoad, Today's assignments)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-934` My Schedule & Assignment Calendar: *My Schedule & Assignment Calendar*
- → `BO-935` Assignment Detail & Operational Brief: *Assignment Detail & Operational Brief*; carries `resourceId`
- → `BO-936` Mobile Staff Check-In & Check-Out: *Mobile Staff Check-In & Check-Out*
- → `BO-937` Resource Collection, Handover & Return: *Resource Collection, Handover & Return*; carries `bookingId`
- → `BO-938` Employee Requests & Resource Support: *Employee Requests & Resource Support*
- → `BO-939` Shift Change, Swap, Pickup & Release: *Shift Change, Swap, Pickup & Release*
- → `BO-940` Manager Mobile Approval Center: *Manager Mobile Approval Center*
- → `BO-941` Operational Notifications & Live Alerts: *Operational Notifications & Live Alerts*
- → `BO-942` Mobile Operations Control & Offline Sync: *Mobile Operations Control & Offline Sync*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource operations home list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource operations home untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource operations home yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the resource operations home are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Offline**: The cached day with "Updated 13:42" and the offline indicator (VO-R07); check-in still records with device time. *(source: contracts/satellite/workforce.yaml#recordAttendance)*
- **No assignment now**: NOW card says "No assignment until 15:30 - Group Ski Lesson" or "You are off today". *(source: designer default)*

#### Consistency with other screens

- Match `EMP-003`: The Staff App home (on duty) is the same screen (VO-R14); add the NOW/NEXT assignment cards to EMP-003 rather than build a second home.
- Match `BO-934`: Same assignment titles and statuses.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
user: Maria Santos - Ski instructor - Summit Peaks Ski School
now:
  title: Private Ski Lesson
  time: 14:00-15:00
  where: Ski School - Zone A
  booking: BK-28491
  participants: 3
  status: Starts in 12 min
next:
  title: Group Ski Lesson
  time: 15:30-16:30
  where: Zone B
  participants: 8
alerts:
- Your 15:30 assignment has moved to Zone C
- Equipment package ready for collection
- Your first aid certificate expires in 14 days
```

#### Permissions

- `listResourceBookings` → `RESOURCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Employee mobile app: staff see their assigned bookings and tasks for the day, perform check-in/check-out and shift closing, and request swaps directly from the app — mirroring the booking info on their back-office profile. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel; 4.9 AI Optimization, Mobile App & Analytics · DI-492)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-933` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS134 Resource Management Configuration Board 9.dc.html#bo-933`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 9
- Flow F272 *Resource Management Configuration board 9: My Resource Operations Home*, step 1: Opens My Resource Operations Home → Provide each employee with a personalized operational landing screen showing what requires their attention now and next.
- Flow F272 *Resource Management Configuration board 9: My Resource Operations Home*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F272 *Resource Management Configuration board 9: My Resource Operations Home*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F272 *Resource Management Configuration board 9: My Resource Operations Home*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F272 *Resource Management Configuration board 9: My Resource Operations Home*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F272 *Resource Management Configuration board 9: My Resource Operations Home*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F272 *Resource Management Configuration board 9: My Resource Operations Home*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F272 *Resource Management Configuration board 9: My Resource Operations Home*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F272 branch at step 1 (expected): when Nothing has been set up on My Resource Operations Home yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F272 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (28 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-933?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-934`, `BO-935`, `BO-936`, `BO-937`, `BO-938`, `BO-939`, `BO-940`, `BO-941`, `BO-942`.
- [ ] Every gated control is gated: `RESOURCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-934` My Schedule & Assignment Calendar

**Provide employees with a mobile view of their working schedule and operational assignments.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-934 |
| Who uses it | venue staff holding `RESOURCE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/my-schedule-assignment-calendar-bo-934` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The employee's own schedule on the phone: assignments, breaks and free time as a day timeline (08:00-10:00 Group lesson Zone A, 10:00-10:30 Break, 10:30-12:00 Private lesson Zone B), with status per assignment and live changes ("Zone A -> Zone C") pushed as they happen. The one thing to get right: a changed assignment shows old and new side by side and stays marked until the employee has seen it.

**Known correction pending (do not draw the wrong version)**

- **getResourceCalendar returns every resource's grid with no filter for the signed-in person** Why: An employee must see only their own schedule; the read has no principal or "me" parameter. *(source: contracts/satellite/resources.yaml#getResourceCalendar; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The seven assignment statuses are drawn as table columns, and "Schedule Timeline" as a button** Why: Statuses are chips on blocks; the timeline is the Day view. *(source: screens/P08-venue-back-office.yaml#BO-934; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Changed, Requires attention and Confirmed have no source in the booking status** Why: ResourceBookingStatus is reserved, checkedOut, returned, overdue, cancelled, noShow. *(source: contracts/satellite/resources.yaml#/components/schemas/ResourceBooking; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getResourceCalendar` ?from |
| To | date and time picker | — | — | `getResourceCalendar` ?to |
| Resource type | picker: choose a resource type | — | — | `getResourceCalendar` ?resourceTypeId |
| Category | picker: choose a category | — | — | `getResourceCalendar` ?categoryId |
| Granularity | radio group | — | Day · Week · Month · Agenda | `getResourceCalendar` ?granularity |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **View**: Day / Week / Month with Agenda (VO-R01); Day is the default, opening on today with Today and Tomorrow shortcuts as the pack asks. *(source: screens/P08-venue-back-office.yaml#BO-934)*

#### Outputs: what the screen shows and produces

**Shown**

**Calendar** (calendar view, from `getResourceCalendar`): The signed-in person's schedule and assignments. Day, week, month and agenda views; the day starts at the venue's `calendarDayStartHour`. Filters the category on what it read.

| Shows | Format | Notes |
|---|---|---|
| Resource | the name it points at, never the id | — |
| Resource name | text | — |
| Resource type | the name it points at, never the id | — |
| Utilisation percent | 1,234.5 | — |
| Segments | list or chips (count when long) | — |
| From | 1 Oct 2026, 14:30 | — |
| To | 1 Oct 2026, 14:30 | — |
| State | chip: Available, Reserved, Assigned, Partially utilised, Fully utilised, Unavailable… | — |
| Booking | the name it points at, never the id | — |
| Conflicts with | list or chips (count when long) | — |

**Every schedule calendar** (data table)

| Shows | Format | Notes |
|---|---|---|
| Upcoming | text | not in the schema: `Upcoming` |
| Confirmed | text | not in the schema: `Confirmed` |
| In progress | text | not in the schema: `In Progress` |
| Completed | text | not in the schema: `Completed` |
| Changed | text | not in the schema: `Changed` |
| Cancelled | text | not in the schema: `Cancelled` |
| Requires attention | text | not in the schema: `Requires Attention` |
| Live updates | text | not in the schema: `Live Updates` |

**The selected schedule calendar** (detail panel): The pack groups this record's detail under its own headings: “Zone A”, “Zone C”.

| Shows | Format | Notes |
|---|---|---|
| Upcoming | text | not in the schema: `Upcoming` |
| Confirmed | text | not in the schema: `Confirmed` |
| In progress | text | not in the schema: `In Progress` |
| Completed | text | not in the schema: `Completed` |
| Changed | text | not in the schema: `Changed` |
| Cancelled | text | not in the schema: `Cancelled` |
| Requires attention | text | not in the schema: `Requires Attention` |
| Live updates | text | not in the schema: `Live Updates` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Schedule Timeline (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Timeline**: Blocks for assignments (title, zone, participants), breaks and lunch from the rota, and Available gaps; times in the venue's 12/24-hour setting (VO-R10). *(source: screens/P08-venue-back-office.yaml#BO-934)*
- **Status chips**: Upcoming, Confirmed, In progress, Completed, Changed, Cancelled, Requires attention - Changed and Requires attention in amber with the change described. *(source: screens/P08-venue-back-office.yaml#BO-935)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Tap an assignment**: Opens the assignment detail (BO-935). *(source: designer default)*
- **Request shift change**: Opens the swap request (EMP-023). *(source: screens/P08-venue-back-office.yaml#BO-934)*

**Data it reads**: `getResourceCalendar` (onLoad, My schedule)

**Where the user goes next**

- → `BO-933` My Resource Operations Home: *Back to My Resource Operations Home*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The schedule calendar list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the schedule calendar untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No schedule calendar yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the schedule calendar are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Assignment changed while offline**: On reconnect the change appears with a notification; until then the cached version shows its age (VO-R07). *(source: screens/P08-venue-back-office.yaml#BO-935)*

#### Consistency with other screens

- Match `EMP-022`: My rota in the Staff App is the same screen (VO-R14); extend it with resource assignments rather than add a second schedule.
- Match `BO-864`: Same state colours as the operations calendar.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
day: Sun 11 Oct 2026 - Maria Santos
blocks:
- time: 08:00-10:00
  what: Group Ski Lesson
  where: Zone A
  participants: 12
  status: Completed
- time: 10:00-10:30
  what: Break
- time: 10:30-12:00
  what: Private Ski Lesson
  where: Zone B
  participants: 4
  status: In progress
- time: 15:00-17:00
  what: Corporate Event Support
  where: Grand Hall
  status: Changed - was Zone A
```

#### Permissions

- `getResourceCalendar` → `RESOURCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Every calendar has day, week and month (and agenda) views, and the day view is broken into hours from the venue's day start hour (calendarDayStartHour). *(agreed · MoM 17 Sep 2026, M17-03 · DI-919)*
- Employee mobile app: staff see their assigned bookings and tasks for the day, perform check-in/check-out and shift closing, and request swaps directly from the app — mirroring the booking info on their back-office profile. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel; 4.9 AI Optimization, Mobile App & Analytics · DI-492)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-934` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS134 Resource Management Configuration Board 9.dc.html#bo-934`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 9
- Flow F272 *Resource Management Configuration board 9: My Resource Operations Home*, step 2: Works in My Schedule & Assignment Calendar → Provide employees with a mobile view of their working schedule and operational assignments.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-934?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Schedule Timeline.
- [ ] Every transition is wired: `BO-933`.
- [ ] Every gated control is gated: `RESOURCE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-935` Assignment Detail & Operational Brief

**Give the employee all information required to execute a specific assignment.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-935 |
| Who uses it | venue staff holding `ATTENDANCE_RECORD`, `INCIDENT_REPORT`, `RESOURCE_BOOK`, `RESOURCE_VIEW` (3 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `resourceId` (navigation), `bookingId` (navigation) |
| Route | `/rentals/assignment-detail-operational-brief-bo-935` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Everything an employee needs to carry out one assignment on the phone: what, when, where (zone, meeting point, map link), who (participants, only the guest notes that matter operationally), what to collect (radio, helmet set, cones, tablet - Ready or Collect), the checklist and the supervisor, with Start, Check in, Report issue, Request replacement and Complete. The one thing to get right: every action works offline with the device time recorded, and customer data stays minimal.

**Known correction pending (do not draw the wrong version)**

- **The brief is drawn as a nine-column table titled "Every detail operational brief"** Why: It is a mobile detail screen (header, sections, actions). *(source: screens/P08-venue-back-office.yaml#BO-935; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Check in, Contact supervisor and View checklist have no operation bound although recordAttendance is listed** Why: Check in should bind recordAttendance with the assignment; the other two need a supervisor contact and a checklist source. *(source: screens/P08-venue-back-office.yaml#BO-935 / contracts/satellite/workforce.yaml#recordAttendance; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Placed in P08 (venue back office)** Why: Board 9 is the Employee App (P06). *(source: screens/P08-venue-back-office.yaml#BO-933; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Resource | picker: choose a resource | — | — | `listResourceBookings` ?resourceId |
| From | date and time picker | — | — | `listResourceBookings` ?from |
| To | date and time picker | — | — | `listResourceBookings` ?to |
| Status | select | — | Reserved · Checked out · Returned · Overdue · Cancelled · No show | `listResourceBookings` ?status |

**Sent by *Start assignment*** (`setResourceBookingProgress`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| State `state` | segmented control | required | — | Started · Completed | — | `started` is recorded as `checkedOut`, `completed` as `returned`. | `setResourceBookingProgress` body |
| Note `note` | text area | optional | — | max length 1000 | — | — | `setResourceBookingProgress` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | When the employee pressed the button on the device, not when the write reached the server. | `setResourceBookingProgress` body |

**Sent by *Report issue*** (`raiseResourceRequest`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7, so a request raised offline is not duplicated on sync. | `raiseResourceRequest` body |
| Kind `kind` | select | required | — | Replacement resource · Additional equipment · Resource issue · Maintenance request · Assignment change · Venue change · Schedule clarification · Other | — | The request kinds on BO-935 / BO-938 (decided 29 September, readiness close-out). | `raiseResourceRequest` body |
| Booking `bookingId` | picker: choose a booking | optional | — | — | shows names, sends the id | — | `raiseResourceRequest` body |
| Resource `resourceId` | picker: choose a resource | optional | — | — | shows names, sends the id | — | `raiseResourceRequest` body |
| Detail `detail` | text area | required | — | min length 3; max length 2000 | — | — | `raiseResourceRequest` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `raiseResourceRequest` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every detail operational brief** (data table)

| Shows | Format | Notes |
|---|---|---|
| Assignment | text | not in the schema: `Assignment` |
| Date | text | not in the schema: `Date` |
| Start/end | text | not in the schema: `Start/end` |
| Venue | text | not in the schema: `Venue` |
| Zone/location | text | not in the schema: `Zone/location` |
| Role | text | not in the schema: `Role` |
| Status | text | not in the schema: `Status` |
| Priority | text | not in the schema: `Priority` |
| Operational information | text | not in the schema: `Operational Information` |

**The selected detail operational brief** (detail panel): The pack groups this record's detail under its own headings: “Depending on assignment type”, “Where appropriate, provide”, “Equipment Required”, “Customer Information”.

| Shows | Format | Notes |
|---|---|---|
| Assignment | text | not in the schema: `Assignment` |
| Date | text | not in the schema: `Date` |
| Start/end | text | not in the schema: `Start/end` |
| Venue | text | not in the schema: `Venue` |
| Zone/location | text | not in the schema: `Zone/location` |
| Role | text | not in the schema: `Role` |
| Status | text | not in the schema: `Status` |
| Priority | text | not in the schema: `Priority` |
| Operational information | text | not in the schema: `Operational Information` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Start assignment (primary button) | `setResourceBookingProgress` POST `/resource-bookings/{bookingId}/progress` | ResourceBookingProgressInput | ResourceBooking | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `invalidProgressStep`: `started` on a booking that is not `reserved`, or `completed` on one that is not … | — |
| Check in (secondary button) | navigation or local | — | — | — | — |
| Contact supervisor (secondary button) | navigation or local | — | — | — | — |
| Report issue (secondary button) | `raiseResourceRequest` POST `/resource-requests` | ResourceRequestInput | ResourceRequest | 422 `subjectRequired`: no `bookingId` or `resourceId` on a kind that needs one; or a `bookingId` / `resourceId` that does not exist at this venue … | — |
| Request replacement (secondary button) | `raiseResourceRequest` POST `/resource-requests` | ResourceRequestInput | ResourceRequest | 422 `subjectRequired`: no `bookingId` or `resourceId` on a kind that needs one; or a `bookingId` / `resourceId` that does not exist at this venue … | — |
| View checklist (secondary button) | navigation or local | — | — | — | — |
| Complete assignment (secondary button) | `setResourceBookingProgress` POST `/resource-bookings/{bookingId}/progress` | ResourceBookingProgressInput | ResourceBooking | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `invalidProgressStep`: `started` on a booking that is not `reserved`, or `completed` on one that is not … | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Header**: Assignment title, status chip (Upcoming, In progress, Completed), date, start-end, venue and zone, role (Lead instructor), priority. *(source: screens/P08-venue-back-office.yaml#BO-935)*
- **Operational information**: By assignment type - event, experience or booking; participant count (2 adults, 2 kids); required resources with Ready / Collect state; instructions; checklist; contact person and supervisor; guest notes limited to what the job needs ("First time on slope, kids aged 8 and 10, prefer Arabic"), no phone numbers or payment data. *(source: screens/P08-venue-back-office.yaml#BO-935 / screens/P08-venue-back-office.yaml#BO-936)*
- **Location**: Zone, meeting point and a venue map link within the configured venue map. *(source: screens/P08-venue-back-office.yaml#BO-936)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Start assignment / Complete assignment**: Records started or completed with the device time; offline it queues and syncs; the booking moves to in progress, then completed. *(source: contracts/satellite/resources.yaml#setResourceBookingProgress)*
- **Check in**: Clocks in against this assignment (with access point or location where the venue requires it). *(source: contracts/satellite/workforce.yaml#recordAttendance)*
- **Report issue / Request replacement**: Raises a resource request of kind Resource issue or Replacement resource about this booking or item, with detail and photo; a guest or staff injury goes to incident report instead. Offline requests keep their own id so they are not duplicated on sync. *(source: contracts/satellite/resources.yaml#raiseResourceRequest / contracts/satellite/maintenance.yaml#reportIncident)*
- **Contact supervisor / View checklist**: Call or message the named supervisor; open the assignment checklist. *(source: screens/P08-venue-back-office.yaml#BO-936)*

**Data it reads**: `listResourceBookings` (onLoad, The assignment itself)

**Where the user goes next**

- → `BO-933` My Resource Operations Home: *Back to My Resource Operations Home*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The detail operational brief list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the detail operational brief untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No detail operational brief yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the detail operational brief are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Out of sequence — a clock-out with no clock-in, or a second clock-in. Reported rather than silently corrected.; 409 `invalidProgressStep`: `started` on a booking that is not `reserved`, or `completed` on one that is not `checkedOut` or `overdue`.; 422 `subjectRequired`: no `bookingId` or `resourceId` on a kind that needs one; or a `bookingId` / `resourceId` that does … |

#### Edge cases to draw

- **Complete pressed without Start (forgot)**: Ask "Start and complete now?" recording both with the device time and a note. *(source: contracts/satellite/resources.yaml#setResourceBookingProgress)*
- **Assignment changed by the manager while open**: Banner "This assignment moved to Zone C at 13:20" with old and new. *(source: screens/P08-venue-back-office.yaml#BO-935)*

#### Consistency with other screens

- Match `BO-099`: The participant list is the performance manifest (waivers, levels) from the Block A screen; link to it rather than repeat it.
- Match `EMP-005`: Same detail layout as a task detail in the Staff App.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
assignment:
  title: Private Ski Lesson
  booking: BK-28491
  date: Sun 11 Oct 2026
  time: 10:30-12:00
  where: Ski School - Zone B, Slope 2
  role: Lead instructor
  guests: 4 (2 adults, 2 kids)
resources:
- Instructor radio - Ready
- Helmet set (4) - Ready
- Training cones - Ready
- Training tablet T-044 - Collect
notes: First time on slope. Kids aged 8 and 10. Prefer Arabic.
```

#### Permissions

- `getResource` → `RESOURCE_VIEW` (read) · staff
- `listResourceBookings` → `RESOURCE_VIEW` (read) · staff
- `recordAttendance` → `ATTENDANCE_RECORD` (operate) · staff
- `reportIncident` → `INCIDENT_REPORT` (operate) · staff
- `setResourceBookingProgress` → `RESOURCE_BOOK` (operate) · staff
- `raiseResourceRequest` → `RESOURCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

12 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.81 | System shall record planned shifts, actual check-in times, actual check-out times, attendance status, lateness, early departures, no-shows, overtime hours, attendance exceptions, and workforce … | Ticketing Catalogue | CONTRACTED | `recordAttendance` |
| 18.9.1 | Attendance Management - Users shall clock in and clock out. | Employee Mobile App & AI Assistant | CONTRACTED | `recordAttendance` |
| 18.9.2 | Shift Management - Users shall view assigned shifts. | Employee Mobile App & AI Assistant | CONTRACTED | `recordAttendance` |
| 17.5.3 | Hazard Reporting - System shall support hazard reporting. | Maintenance & Safety Management | CONTRACTED | `reportIncident` |
| 17.5.4 | Incident Reporting - System shall support incident reporting. | Maintenance & Safety Management | CONTRACTED | `reportIncident` |
| 17.5.5 | Near-Miss Reporting - System shall support near-miss reporting. | Maintenance & Safety Management | CONTRACTED | `reportIncident` |
| 18.4.1 | Hazard Reporting - Users shall submit hazard reports. | Employee Mobile App & AI Assistant | CONTRACTED | `reportIncident` |
| 18.4.2 | Incident Reporting - Users shall submit incident reports. | Employee Mobile App & AI Assistant | CONTRACTED | `reportIncident` |
| 18.4.3 | Near-Miss Reporting - Users shall submit near-miss reports. | Employee Mobile App & AI Assistant | CONTRACTED | `reportIncident` |
| 18.4.4 | Safety Inspections - Users shall perform inspections. | Employee Mobile App & AI Assistant | CONTRACTED | `reportIncident` |
| 18.4.5 | Safety Checklists - Users shall complete safety checklists. | Employee Mobile App & AI Assistant | CONTRACTED | `reportIncident` |
| 18.4.6 | Corrective Actions - Users shall submit corrective actions. | Employee Mobile App & AI Assistant | CONTRACTED | `reportIncident` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-935` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS134 Resource Management Configuration Board 9.dc.html#bo-935`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 9
- Flow F272 *Resource Management Configuration board 9: My Resource Operations Home*, step 4: Works in Assignment Detail & Operational Brief → Give the employee all information required to execute a specific assignment.
- ADR-0023 *— Personal data lives apart from the append-only ledger* (`docs/adr/0023-pii-separation.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (400, 404, 409, 422).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-935?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Start assignment, Check in, Contact supervisor, Report issue, Request replacement, View checklist, Complete assignment.
- [ ] Every transition is wired: `BO-933`.
- [ ] Every gated control is gated: `ATTENDANCE_RECORD`, `INCIDENT_REPORT`, `RESOURCE_BOOK`, `RESOURCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-936` Mobile Staff Check-In & Check-Out

**Allow employees to record attendance and assignment presence from the Employee App.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-936 |
| Who uses it | venue staff holding `ATTENDANCE_RECORD` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/mobile-staff-check-in-check-out-bo-936` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The resource pack's mobile check-in and check-out screen (board 9, screen 4). Board 9 is delivered inside the Employee App, not as a separate app, so this is the Staff App's clock screen (EMP-024): shift, venue, current time, "Ready to check in", and one button, with configurable verification and offline capture. The one thing to get right: draw it once, as EMP-024, adding the pack's verification methods, assignment-level check-in and the check-out summary.

**Known correction pending (do not draw the wrong version)**

- **A mobile Employee App screen is placed on P08 (Venue back office) under module Rentals** Why: Board 9 is exposed through the Employee App, not a separate app; it duplicates EMP-024 on P06. *(source: screens/P08-venue-back-office.yaml#BO-933 / screens/P08-venue-back-office.yaml#BO-936; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Table columns are the pack's sample values ("08:00–16:00", "Ski School", "07:56", "Ready to Check In", "[CHECK IN]")** Why: Sample data used as labels; the screen is one card. *(source: screens/P08-venue-back-office.yaml#BO-936; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is an allowed check-in window (e.g. from 30 minutes before start) enforced, and where is it configured?** → Drawn default accepted: Show the button from 30 minutes before start with the window stated; enforcement pending. *(decided by Chinmay, 2026-10-02; DEC-516 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Verification**: Mobile confirmation, venue QR, resource QR, NFC, manager validation or integrated attendance system, as the venue configures; the primary method is a large scan target, the rest secondary. *(source: screens/P08-venue-back-office.yaml#BO-936)*
- **Assignment check-in**: Optional second check-in to a specific activity ("Check into Private ski lesson - Zone A"). *(source: screens/P08-venue-back-office.yaml#BO-936)*

#### Outputs: what the screen shows and produces

**Shown**

**Every mobile staff check-in** (data table)

| Shows | Format | Notes |
|---|---|---|
| Shift | text | not in the schema: `Shift` |
| 08:00–16:00 | text | not in the schema: `08:00–16:00` |
| Venue | text | not in the schema: `Venue` |
| Ski school | text | not in the schema: `Ski School` |
| Current time | text | not in the schema: `Current Time` |
| 07:56 | text | not in the schema: `07:56` |
| Status | text | not in the schema: `Status` |
| Ready to check in | text | not in the schema: `Ready to Check In` |
| [CHECK IN] | text | not in the schema: `[CHECK IN]` |

**The selected mobile staff check-in** (detail panel): The pack groups this record's detail under its own headings: “Check-In”, “Assignment Check-In”, “On checkout, display”.

| Shows | Format | Notes |
|---|---|---|
| Shift | text | not in the schema: `Shift` |
| 08:00–16:00 | text | not in the schema: `08:00–16:00` |
| Venue | text | not in the schema: `Venue` |
| Ski school | text | not in the schema: `Ski School` |
| Current time | text | not in the schema: `Current Time` |
| 07:56 | text | not in the schema: `07:56` |
| Status | text | not in the schema: `Status` |
| Ready to check in | text | not in the schema: `Ready to Check In` |
| [CHECK IN] | text | not in the schema: `[CHECK IN]` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Check-in card**: Shift "07:00-15:00", venue, current time, status "Ready to check in", button; last check-out shown below ("Fri 9 Oct, 15:02"). *(source: screens/P08-venue-back-office.yaml#BO-936)*
- **Check-out summary**: Actual working time, breaks, overtime, exceptions, outstanding assignments. *(source: screens/P08-venue-back-office.yaml#BO-936)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Check in / Check out**: As EMP-024; validation of date and time, venue, scheduled shift, assignment, device session and check-in window where configured. *(source: screens/P08-venue-back-office.yaml#BO-936 / contracts/satellite/workforce.yaml#recordAttendance)*

**Where the user goes next**

- → `BO-933` My Resource Operations Home: *Back to My Resource Operations Home*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The mobile staff check-in list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the mobile staff check-in untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No mobile staff check-in yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the mobile staff check-in are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Out of sequence — a clock-out with no clock-in, or a second clock-in. Reported rather than silently corrected. |

#### Edge cases to draw

- **Offline**: Device timestamp, offline indicator, later synchronisation; conflicts flagged on sync, never silently overwritten. *(source: screens/P08-venue-back-office.yaml#BO-936 / screens/P08-venue-back-office.yaml#BO-942)*

#### Consistency with other screens

- Match `EMP-024`: Same screen; EMP-024 survives on P06 and this entry becomes an anchor to it (per VO-R14).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
card:
  person: Rahul Menon
  shift: Sat 10 Oct 2026, 07:00-15:00
  venue: Aqua Park - Main Plaza Gate 2
  now: 06:56
  status: Ready to check in
  last: Fri 9 Oct, 15:02
```

#### Permissions

- `recordAttendance` → `ATTENDANCE_RECORD` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.81 | System shall record planned shifts, actual check-in times, actual check-out times, attendance status, lateness, early departures, no-shows, overtime hours, attendance exceptions, and workforce … | Ticketing Catalogue | CONTRACTED | `recordAttendance` |
| 18.9.1 | Attendance Management - Users shall clock in and clock out. | Employee Mobile App & AI Assistant | CONTRACTED | `recordAttendance` |
| 18.9.2 | Shift Management - Users shall view assigned shifts. | Employee Mobile App & AI Assistant | CONTRACTED | `recordAttendance` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Employee mobile app: staff see their assigned bookings and tasks for the day, perform check-in/check-out and shift closing, and request swaps directly from the app — mirroring the booking info on their back-office profile. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel; 4.9 AI Optimization, Mobile App & Analytics · DI-492)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-936` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS134 Resource Management Configuration Board 9.dc.html#bo-936`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 9
- Flow F272 *Resource Management Configuration board 9: My Resource Operations Home*, step 6: Works in Mobile Staff Check-In & Check-Out → Allow employees to record attendance and assignment presence from the Employee App.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-936?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-933`.
- [ ] Every gated control is gated: `ATTENDANCE_RECORD`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-937` Resource Collection, Handover & Return

**Digitally manage physical resources transferred between employees, departments, or operational locations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-937 |
| Who uses it | venue staff holding `RESOURCE_BOOK` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `bookingId` (navigation) |
| Route | `/rentals/resource-collection-handover-return-bo-937` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Scan-first custody of operational equipment between storage, employees and events: Collect (scan Radio R-184, Tablet T-044, AV toolkit K-12), Handover from one employee to another with both confirming, and Return with condition and location - building a chain of custody (Storage > Ahmed > Sarah > Corporate Gala > Returned). The one thing to get right: scan, confirm, done - and a damaged return takes the item out of use until inspected.

**Known correction pending (do not draw the wrong version)**

- **The four condition values and "Return" are drawn as selectFields** Why: Condition is one choice of four buttons; Return is a tab/action. *(source: screens/P08-venue-back-office.yaml#BO-937; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Condition enum (good, minorDamage, majorDamage, notReturned) differs from the pack's Good, Minor damage, Damaged, Missing component** Why: Missing component has no value and notReturned has no pack label. *(source: screens/P08-venue-back-office.yaml#BO-937 / contracts/satellite/resources.yaml#checkInResource; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No operation records an employee-to-employee handover or a return location** Why: Check-out and check-in move an item between store and one subject with a deposit; a two-party handover confirmed by both has no write. *(source: screens/P08-venue-back-office.yaml#BO-937 / contracts/satellite/resources.yaml#checkOutResource; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Placed in P08** Why: Board 9 belongs to the Employee App (P06). *(source: screens/P08-venue-back-office.yaml#BO-933; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Good | select field | — | — | — | — | — | — |
| Minor damage | select field | — | — | — | — | — | — |
| Damaged | select field | — | — | — | — | — | — |
| Missing component | select field | — | — | — | — | — | — |
| Return | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Scan**: Camera scan of the item's QR or barcode (manual code entry as fallback with reason); shows item, status and what it is assigned to before accepting. *(source: screens/P08-venue-back-office.yaml#BO-937 / MATRIX 7.4.51)*
- **Condition**: Four large buttons Good / Minor damage / Damaged / Missing component; photo required for anything but Good where configured. *(source: screens/P08-venue-back-office.yaml#BO-937 / contracts/satellite/resources.yaml#checkInResource)*
- **Handover recipient**: Pick or scan the receiving employee's badge; the receiver confirms on their own device. *(source: screens/P08-venue-back-office.yaml#BO-937)*
- **Return location**: Store or station picked from a short list (default the item's home station). *(source: screens/P08-venue-back-office.yaml#BO-938)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Collected items**: List with item, category, quantity (Helmet set x4) and Collected tick; tabs Collect / Handover / Return. *(source: screens/P08-venue-back-office.yaml#BO-937)*
- **Chain of custody**: Timeline of holders and places with times on the item's page. *(source: screens/P08-venue-back-office.yaml#BO-938)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Confirm collection**: Hands the items over to the employee for the assignment; recorded with device time, offline-capable. *(source: contracts/satellite/resources.yaml#checkOutResource)*
- **Submit return**: Takes the items back with condition; Damaged or Missing component blocks the item until inspected, whatever the user chooses. *(source: contracts/satellite/resources.yaml#checkInResource)*

**Where the user goes next**

- → `BO-933` My Resource Operations Home: *Back to My Resource Operations Home*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource collection handover configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource collection handover untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource collection handover configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Scanned item is assigned to someone else**: "Radio R-184 is with Sarah Al Mansoori for Corporate Gala - request handover?" *(source: screens/P08-venue-back-office.yaml#BO-937)*
- **Offline**: Scans and confirmations queue with device time and an offline indicator; status updates on sync (VO-R07). *(source: contracts/satellite/resources.yaml#checkOutResource)*

#### Consistency with other screens

- Match `BO-097`: Guest check-out and check-in use the same condition words where they overlap.
- Match `EMP-074`: Rental equipment scan in the Staff App uses the same scan component.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
employee: Ahmed Al Mansoori - Technical crew - Corporate Gala
items:
- item: Radio R-184
  status: Collected
- item: Helmet set H-221
  qty: 4
  status: Collected
- item: Training tablet T-044
  status: Collected
custody: Storage 09:02 > Ahmed Al Mansoori 09:05 > Fatima Al Hashimi 13:40 > Returned to AV store 18:22 (Good)
```

#### Permissions

- `checkOutResource` → `RESOURCE_BOOK` (operate) · staff
- `checkInResource` → `RESOURCE_BOOK` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

25 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.8 | The system should allow check out & check in feature for rental resources. For example, towels in the water park. Inventory management of these resources should be handled in the system. | Ticketing Catalogue | CONTRACTED | `checkOutResource` |
| 1.2.9 | The system should allow configuration of deposit requirement for rental resources. The collection and return of the deposit at the time of check-in and check-out should be handled within the system. | Ticketing Catalogue | CONTRACTED | `checkOutResource` |
| 1.2.10 | The system should allow linking of a checked-out resource object to a guest profile. Specification of a rental time period for a checked-out resource object should be supported. | Ticketing Catalogue | CONTRACTED | `checkOutResource` |
| 7.4.10 | The system can manage Cabins rental | F&B POS | CONTRACTED | `checkOutResource` |
| 7.4.36 | Lockers can be managed by the system (sales and inventory) | F&B POS | CONTRACTED | `checkOutResource` |
| 7.4.37 | Wheelchairs can be managed by the system (sales and inventory) | F&B POS | CONTRACTED | `checkOutResource` |
| 7.4.38 | Strollers can be managed by the system (sales and inventory) | F&B POS | CONTRACTED | `checkOutResource` |
| 7.4.51 | Track serial numbers for RFID wristbands, devices, lockers, tablets and rental assets. Record assignment, location, status and movement history. | F&B POS | CONTRACTED | `checkOutResource` |
| 7.4.52 | Manage deposits for rented assets such as lockers, strollers, wheelchairs and equipment. Support collection, refund, partial refund and forfeiture workflows. | F&B POS | CONTRACTED | `checkOutResource` |
| 7.6.1 | Functional Requirements Ability to create and manage rental products (Bike, Kayak, Watercraft, Stroller, Cabana, Locker, Wheelchair, etc.). Configure: - Product Code - Product Name - Description - … | F&B POS | CONTRACTED | `checkOutResource` |
| 7.6.2 | Serial Number Management Support unique serial number assignment for each rental item. Ability to: - Create serial numbers - Activate/Deactivate serial numbers Mark item as: - Available - Rented - … | F&B POS | CONTRACTED | `checkOutResource` |
| 7.6.3 | Functional Requirements Real-time inventory tracking. Maintain available inventory by: - Product - Date - Time Slot - Location Automatically reduce inventory upon reservation. Automatically restore … | F&B POS | CONTRACTED | `checkOutResource` |
| … 13 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-937` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS134 Resource Management Configuration Board 9.dc.html#bo-937`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 9
- Flow F272 *Resource Management Configuration board 9: My Resource Operations Home*, step 8: Works in Resource Collection, Handover & Return → Digitally manage physical resources transferred between employees, departments, or operational locations.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-937?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-933`.
- [ ] Every gated control is gated: `RESOURCE_BOOK`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-938` Employee Requests & Resource Support

**Allow frontline employees to submit operational resource-related requests directly from the Employee App.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-938 |
| Who uses it | venue staff holding `RESOURCE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/employee-requests-resource-support-bo-938` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-005): raiseMyCase is a guest-only operation for guest cases; an employee request is raiseResourceRequest (design-notes correction customer-marketing BO-938).

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Frontline employees request resource help from the employee app (replacement, extra equipment, issue, maintenance, assignment or venue change, schedule clarification). It is an internal request, not a guest case.

**Fixed on main** (the package already carries these; draw what it says): raiseMyCase (a guest-only operation for guest cases) is declared beside raiseResourceRequest. (CHG-WIR-005).

#### Inputs: what the user enters or picks

**Sent by *Replacement resource*** (`raiseResourceRequest`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7, so a request raised offline is not duplicated on sync. | `raiseResourceRequest` body |
| Kind `kind` | select | required | — | Replacement resource · Additional equipment · Resource issue · Maintenance request · Assignment change · Venue change · Schedule clarification · Other | — | The request kinds on BO-935 / BO-938 (decided 29 September, readiness close-out). | `raiseResourceRequest` body |
| Booking `bookingId` | picker: choose a booking | optional | — | — | shows names, sends the id | — | `raiseResourceRequest` body |
| Resource `resourceId` | picker: choose a resource | optional | — | — | shows names, sends the id | — | `raiseResourceRequest` body |
| Detail `detail` | text area | required | — | min length 3; max length 2000 | — | — | `raiseResourceRequest` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `raiseResourceRequest` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Replacement resource (primary button) | `raiseResourceRequest` POST `/resource-requests` | ResourceRequestInput | ResourceRequest | 422 `subjectRequired`: no `bookingId` or `resourceId` on a kind that needs one; or a `bookingId` / `resourceId` that does not exist at this venue … | — |
| Additional equipment (secondary button) | `raiseResourceRequest` POST `/resource-requests` | ResourceRequestInput | ResourceRequest | 422 `subjectRequired`: no `bookingId` or `resourceId` on a kind that needs one; or a `bookingId` / `resourceId` that does not exist at this venue … | — |
| Resource issue (secondary button) | `raiseResourceRequest` POST `/resource-requests` | ResourceRequestInput | ResourceRequest | 422 `subjectRequired`: no `bookingId` or `resourceId` on a kind that needs one; or a `bookingId` / `resourceId` that does not exist at this venue … | — |
| Maintenance request (secondary button) | `raiseResourceRequest` POST `/resource-requests` | ResourceRequestInput | ResourceRequest | 422 `subjectRequired`: no `bookingId` or `resourceId` on a kind that needs one; or a `bookingId` / `resourceId` that does not exist at this venue … | — |
| Assignment change (secondary button) | `raiseResourceRequest` POST `/resource-requests` | ResourceRequestInput | ResourceRequest | 422 `subjectRequired`: no `bookingId` or `resourceId` on a kind that needs one; or a `bookingId` / `resourceId` that does not exist at this venue … | — |
| Venue change request (secondary button) | `raiseResourceRequest` POST `/resource-requests` | ResourceRequestInput | ResourceRequest | 422 `subjectRequired`: no `bookingId` or `resourceId` on a kind that needs one; or a `bookingId` / `resourceId` that does not exist at this venue … | — |
| Schedule clarification (secondary button) | `raiseResourceRequest` POST `/resource-requests` | ResourceRequestInput | ResourceRequest | 422 `subjectRequired`: no `bookingId` or `resourceId` on a kind that needs one; or a `bookingId` / `resourceId` that does not exist at this venue … | — |
| Custom operational request (secondary button) | `raiseResourceRequest` POST `/resource-requests` | ResourceRequestInput | ResourceRequest | 422 `subjectRequired`: no `bookingId` or `resourceId` on a kind that needs one; or a `bookingId` / `resourceId` that does not exist at this venue … | — |

**Where the user goes next**

- → `BO-933` My Resource Operations Home: *Back to My Resource Operations Home*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The employee requests resource list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the employee requests resource untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No employee requests resource yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the employee requests resource are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 `subjectRequired`: no `bookingId` or `resourceId` on a kind that needs one; or a `bookingId` / `resourceId` that does not exist at this venue … |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
request: Replacement resource - Life jackets x10 for Station B - urgent
```

#### Permissions

- `raiseResourceRequest` → `RESOURCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-938` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS134 Resource Management Configuration Board 9.dc.html#bo-938`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 9
- Flow F272 *Resource Management Configuration board 9: My Resource Operations Home*, step 10: Works in Employee Requests & Resource Support → Allow frontline employees to submit operational resource-related requests directly from the Employee App.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-938?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Replacement resource, Additional equipment, Resource issue, Maintenance request, Assignment change, Venue change request, Schedule clarification, Custom operational request.
- [ ] Every transition is wired: `BO-933`.
- [ ] Every gated control is gated: `RESOURCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-939` Shift Change, Swap, Pickup & Release

**Expose the Board 4 Shift Marketplace capabilities through the Employee App. This screen does not recreate shift rules; it consumes the workforce rules already configured in Board 4.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WORKFORCE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `assignmentId` (navigation) |
| Route | `/rentals/shift-change-swap-pickup-release-bo-939` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The resource pack's mobile shift change screen (board 9, screen 7): the employee's side of the shift marketplace - request a swap, transfer or release of my shift, and see and request open shifts I am eligible for - consuming the rules configured centrally. It belongs in the Employee App and is EMP-023 plus an Open shifts tab. The one thing to get right: only shifts the person is eligible for are shown ("You are eligible"), and request status says who it waits for.

**Known correction pending (do not draw the wrong version)**

- **A mobile Employee App screen is placed on P08 under module Rentals, with empty components** Why: Board 9 is delivered in the Employee App; this duplicates EMP-023. *(source: screens/P08-venue-back-office.yaml#BO-933 / screens/P08-venue-back-office.yaml#BO-939; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **listOpenShifts and claimOpenShift are not bound, though the screen's first tab is Open shifts** Why: The open-shift half of the screen has no data. *(source: screens/P08-venue-back-office.yaml#BO-939 / contracts/satellite/workforce.yaml#listOpenShifts; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Transfer and release have no operation** Why: requestShiftSwap only hands a shift to a named colleague. *(source: MATRIX 1.2.80 / contracts/satellite/workforce.yaml#requestShiftSwap; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Does "open exchange" (offer my shift to anyone eligible) mean releasing it to the marketplace?** → Drawn default accepted: Treat it as Release to the marketplace; drawn greyed until a release operation exists. *(decided by Chinmay, 2026-10-02; DEC-517 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Tabs**: Open shifts / My requests (as in the client render), plus "Change my shift" from a shift. *(source: screens/P08-venue-back-office.yaml#BO-939)*
- **My shift action**: Swap (with a named colleague or open exchange), Transfer, Release; validated both sides before submission. *(source: screens/P08-venue-back-office.yaml#BO-939 / screens/P08-venue-back-office.yaml#BO-940)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Open shift card**: Day and time, venue, role, "You are eligible", estimated hours ("8 h"), incentive if any, and Request shift. *(source: screens/P08-venue-back-office.yaml#BO-939 / contracts/satellite/workforce.yaml#listOpenShifts)*
- **My requests**: Each request with status Awaiting employee, Awaiting manager, Approved, Rejected. *(source: screens/P08-venue-back-office.yaml#BO-940 / contracts/satellite/workforce.yaml#listShiftSwapRequests)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Request shift**: Claims the open shift; a refusal names the rule ("Would exceed 60 h this week"). *(source: contracts/satellite/workforce.yaml#claimOpenShift)*
- **Create swap request**: As EMP-023. *(source: contracts/satellite/workforce.yaml#requestShiftSwap)*

**Data it reads**: `listShiftSwapRequests` (onLoad, Requests outstanding)

**Where the user goes next**

- → `BO-933` My Resource Operations Home: *Back to My Resource Operations Home*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The shift change swap list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the shift change swap untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No shift change swap yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the shift change swap are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The swap is not like for like (audit R129 (6)): the other person does not hold the assignment's role (`swap-role-mismatch`), or is not staff at the … |

#### Edge cases to draw

- **Shift taken by someone else first**: "Already taken" and the card disappears; nothing else changes. *(source: contracts/satellite/workforce.yaml#claimOpenShift)*
- **Offline**: Cached open shifts with age; Request shift disabled with "Needs a connection". *(source: contracts/satellite/workforce.yaml#listOpenShifts)*

#### Consistency with other screens

- Match `EMP-023`: Same screen on P06; EMP-023 survives with an Open shifts tab, this entry becomes an anchor (per VO-R14).
- Match `BO-887`: Manager side of the same requests and open shifts.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
openShifts:
- day: Sat 17 Oct
  time: 14:00-22:00
  venue: Aqua Park
  role: Customer Service
  eligible: You are eligible
  hours: 8 h
- day: Sun 18 Oct
  time: 10:00-18:00
  venue: Summit Peaks - Grand Hall
  role: Event Support
  eligible: You are eligible
  hours: 8 h
myRequests:
- type: Swap
  shift: Thu 15 Oct 08:00-16:00
  with: Omar Haddad
  status: Approved
```

#### Permissions

- `requestShiftSwap` → `WORKFORCE_VIEW` (read) · staff
- `listShiftSwapRequests` → `WORKFORCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.80 | System shall allow employees to request shift swaps, shift transfers, shift pickups, and shift releases. Approval workflows, qualification validation, staffing rules, and manager approvals shall be … | Ticketing Catalogue | CONTRACTED | `requestShiftSwap` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Staff can request a swap (e.g. break coverage) from another resource; attendance exceptions are marked manually (active, not active, absent, other). *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering; 4.9 AI Optimization, Mobile App & Analytics · DI-491)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A59** Cross-check the workstation/POS/till wireframes shared by Allam against the functionality matrix and consolidate/redesign dashboards where overlapping (e.g., shift-closing vs. till-closing screens) *(Chinmay Parab / Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'till')*
- **A77** Design cash/shift (till) management and the workstation/POS admin dashboard suite: blind cash-out reconciliation, supervisor shift-closure authorization, a configurable cash-drawer limit with mid-shift unload, automatic … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 14 Aug 2026 · workshop tracker · keyword 'shift')*
- **A150** Manage personnel as a resource type (duty/leave status, skills and certification levels, certification expiry, shift templates, leave quotas, optional external HR integration) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A155** Build AI resource forecasting, the employee mobile app (bookings, check-in/out, shift close, swaps) and cost/revenue analytics by resource and event *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A269** POS: auto hardware check at shift start; cashier report visibility as a role toggle *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 9 Sep 2026 · workshop tracker · keyword 'shift')*
- **A272** Agree shift-close cash-variance approach (expected-sales visibility, no-supervisor fallback) *(Qossai / Allam · Medium · With client → 30 Sep: Closed, Moved to T10 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'shift')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-939` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS134 Resource Management Configuration Board 9.dc.html#bo-939`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 9
- Flow F272 *Resource Management Configuration board 9: My Resource Operations Home*, step 12: Works in Shift Change, Swap, Pickup & Release → Expose the Board 4 Shift Marketplace capabilities through the Employee App. This screen does not recreate shift rules; it consumes the workforce rules already configured in Board 4.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-939?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-933`.
- [ ] Every gated control is gated: `WORKFORCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-940` Manager Mobile Approval Center

**Allow authorized supervisors and managers to approve operational requests without requiring access to the desktop backend.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block B · task VM-BO-940 |
| Who uses it | venue staff holding `APPROVAL_DECIDE`, `APPROVAL_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `requestId` (navigation) |
| Route | `/rentals/manager-mobile-approval-center-bo-940` |

**Known gaps.** **Manager Mobile Approval Center declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Approve operational requests from a phone: the same decisions as the inbox, in a mobile layout, with the second factor where required.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Assigned to me | toggle | — | — | `listApprovalRequests` ?assignedToMe |
| Raised by me | toggle | — | — | `listApprovalRequests` ?raisedByMe |
| Status | select | — | Draft · Pending · Escalated · Returned · Information requested · Approved · Rejected · Withdrawn · Expired · Cancelled | `listApprovalRequests` ?status |
| Kind | select | — | Refund · Price override · Discount override · Complimentary ticket · Membership cancellation · Access permission change · Configuration change · AI recommendation · Release promotion · Requisition · Stock write off · Journal entry …; - Publishing white-label … | `listApprovalRequests` ?kind |
| Breaching within minutes | number field (minutes) | — | — | `listApprovalRequests` ?breachingWithinMinutes |
| Sort | segmented control | Sla proximity | Sla proximity · AI priority | `listApprovalRequests` ?sort |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Decide (Approve / Reject / Return / Request information)**: Four outcomes, not two: reject needs a reason the requester reads; return sends it back to amend; request information pauses the SLA clock. Approving records an authorisation and does not perform the action; on a multi-level chain the request moves to the next level. Where the rule demands MFA the decision carries a stepUpToken from the in-place challenge; where it demands a signature, the signature step comes first. *(source: contracts/spine/approvals.yaml#decideApprovalRequest; F14 step 4)*

**Data it reads**: `listApprovalRequests` (onLoad, Approvals on mobile)

**Where the user goes next**

- → `BO-933` My Resource Operations Home: *Back to My Resource Operations Home*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The mobile approval list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the mobile approval untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No mobile approval yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the mobile approval are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The request is no longer open for a decision. `refusedReason` says which: `alreadyDecided` (approved or rejected), `withdrawn`, `expired` or `cancelled`, and … (ApprovalStateProblem) |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds APPROVAL_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: APPROVAL_DECIDE for decideApprovalRequest. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/approvals.yaml#decideApprovalRequest)*
- **decideApprovalRequest answers 403**: Show it as something the person can act on, not a failure: The approver may not decide this request. **Always carries `refusedReason`**, one value per cause — the approver is the requester (`approverIsRequester`), is not in the resolved chain (`notInApproverChain`), lacks the permission the rule demands (`insufficientPermission`), gave no step-up token where the rule requires MFA (`mfaR... *(source: contracts/spine/approvals.yaml#decideApprovalRequest)*
- **decideApprovalRequest answers 409**: Show it as something the person can act on, not a failure: The request is no longer open for a decision. `refusedReason` says which: `alreadyDecided` (approved or rejected), `withdrawn`, `expired` or `cancelled`, and `currentStatus` carries the status it is in. *(source: contracts/spine/approvals.yaml#decideApprovalRequest)*
- **The approver raised the request, or sits outside the resolved chain**: Decide is refused 403 with refusedReason (approverIsRequester, notInApproverChain, missing permission or step-up); show the reason in words and who can decide instead. Segregation of duties survives delegation. *(source: contracts/spine/approvals.yaml#decideApprovalRequest; contracts/spine/approvals.yaml#createApprovalDelegation)*

#### Consistency with other screens

- Match `BO-084`: Same queue and dialog.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listApprovalRequests (ApprovalRequest):
- kind: standard
  rerouteOnNoApprover: true
  allowEmailApproval: true
  status: active
  summary: Guest charged twice at Main Gate Till 3
  amount: AED 1,250.00
  justification: Guest charged twice at Main Gate Till 3
- kind: standard
  rerouteOnNoApprover: false
  allowEmailApproval: false
  status: pending
  summary: Group of 40 from Desert Gate Tours
  amount: AED 48,000.00
  justification: Group of 40 from Desert Gate Tours
```

#### Permissions

- `listApprovalRequests` → `APPROVAL_VIEW` (read) · staff, public
- `decideApprovalRequest` → `APPROVAL_DECIDE` (operate) · staff, public

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

13 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 11.1.55 | Regulatory Audit Support - System shall provide approval records suitable for regulatory audits. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.56 | Immutable Approval Records - System shall prevent modification of completed approval records. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.62 | Approval Tamper Detection - System shall detect unauthorized modification attempts on approval records. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.74 | AI Priority Scoring - System shall prioritize approval requests using AI scoring. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 18.6.1 | Approval Inbox - Users shall view pending approvals. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |
| 18.6.2 | Approval Actions - Authorized users shall approve or reject requests. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |
| 18.6.3 | Approval Comments - Users shall submit approval comments. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |
| 11.1.20 | Approval Comments - System shall allow approvers to add comments to approval decisions. | Approval Workflows & Governance | CONTRACTED | `decideApprovalRequest` |
| 11.1.21 | Approval Rejection Reasons - System shall require rejection reasons when approvals are denied. | Approval Workflows & Governance | CONTRACTED | `decideApprovalRequest` |
| 11.1.57 | Digital Signature Support - System shall support digital signatures for sensitive approvals. | Approval Workflows & Governance | CONTRACTED | `decideApprovalRequest` |
| 11.1.59 | Approval Authentication - System shall require authentication before approval actions are executed. | Approval Workflows & Governance | CONTRACTED | `decideApprovalRequest` |
| 11.1.60 | MFA-Protected Approvals - System shall support MFA requirements for sensitive approval actions. | Approval Workflows & Governance | CONTRACTED | `decideApprovalRequest` |
| … 1 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-940` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS134 Resource Management Configuration Board 9.dc.html#bo-940`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 9
- Flow F272 *Resource Management Configuration board 9: My Resource Operations Home*, step 14: Works in Manager Mobile Approval Center → Allow authorized supervisors and managers to approve operational requests without requiring access to the desktop backend.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-940?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-933`.
- [ ] Every gated control is gated: `APPROVAL_DECIDE`, `APPROVAL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 5 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-941` Operational Notifications & Live Alerts

**Provide employees and managers with timely, prioritized operational notifications.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-941 |
| Who uses it | venue staff holding `WORKFORCE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/operational-notifications-live-alerts-bo-941` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The resource pack's mobile notifications screen (board 9, screen 9): prioritised operational notifications for employees and managers - assignment changed, schedule, shift, resource replacement, maintenance, event, attendance, approval, emergency, AI recommendation - with acknowledgement and escalation. It belongs in the Employee App and is EMP-037. The one thing to get right: priority (Critical, High, Standard, Informational) drives order and treatment, and a critical alert not acknowledged in time escalates.

**Known correction pending (do not draw the wrong version)**

- **A mobile Employee App screen placed on P08 under module Rentals, with the notification categories drawn as action buttons** Why: Board 9 is the Employee App; categories are filter values. Duplicates EMP-037. *(source: screens/P08-venue-back-office.yaml#BO-933 / screens/P08-venue-back-office.yaml#BO-941; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Only listAnnouncements is bound** Why: Announcements are broadcasts; personal operational notifications (assignment changed, resource replaced, shift approved) have no feed, no priority field and no escalation setting. *(source: screens/P08-venue-back-office.yaml#BO-942 / contracts/satellite/workforce.yaml#listAnnouncements; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which operation feeds personal operational notifications, and where are escalation periods and recipients configured?** → Drawn default accepted: Draw them in the same inbox list with priority pills; escalation shown as a status line only. *(decided by Chinmay, 2026-10-02; DEC-518 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Unacknowledged only | toggle | — | — | `listAnnouncements` ?unacknowledgedOnly |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Category filter**: All / Assignments / Resources / System chips as in the client render; categories are filter values, not buttons. *(source: screens/P08-venue-back-office.yaml#BO-941)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Assignment (primary button) | navigation or local | — | — | — | — |
| Schedule (secondary button) | navigation or local | — | — | — | — |
| Resource (secondary button) | navigation or local | — | — | — | — |
| Event (secondary button) | navigation or local | — | — | — | — |
| Attendance (secondary button) | navigation or local | — | — | — | — |
| Approval (secondary button) | navigation or local | — | — | — | — |
| Emergency/critical operations (secondary button) | navigation or local | — | — | — | — |
| AI recommendation (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Notification row**: Priority pill in words (Critical, High, Info), title ("Assignment changed"), one-line body ("Your 15:30 lesson moved to Zone C"), time ago. Critical rows pinned and red-bordered, with Acknowledge. *(source: screens/P08-venue-back-office.yaml#BO-942 / screens/P08-venue-back-office.yaml#BO-941)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Open / Acknowledge / Accept / Decline where permitted / Go to assignment**: As EMP-037; acknowledgement queues offline. *(source: screens/P08-venue-back-office.yaml#BO-942 / contracts/satellite/workforce.yaml#acknowledgeAnnouncement)*

**Data it reads**: `listAnnouncements` (onLoad, Live alerts and notices)

**Where the user goes next**

- → `BO-933` My Resource Operations Home: *Back to My Resource Operations Home*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The operational notifications live list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the operational notifications live untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No operational notifications live yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the operational notifications live are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Critical alert not acknowledged within the configured period**: Escalates to the supervisor, then the operations manager; the row shows "Escalated to Fatima Al Hashimi 14:42". *(source: screens/P08-venue-back-office.yaml#BO-942)*

#### Consistency with other screens

- Match `EMP-037`: Same screen; EMP-037 survives on P06 and this entry becomes an anchor (per VO-R14).
- Match `BO-066`: Announcement kinds published there arrive here among the notifications.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
notifications:
- priority: Critical
  title: Assignment changed
  body: Winter Lights AV moved to Grand Hall. Start time unchanged.
  age: 2 min
- priority: High
  title: Resource replacement
  body: Projector P-17 unavailable. P-24 assigned.
  age: 12 min
- priority: Info
  title: Shift approved
  body: Your Saturday shift pickup has been approved.
  age: 1 h
```

#### Permissions

- `listAnnouncements` → `WORKFORCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-941` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS134 Resource Management Configuration Board 9.dc.html#bo-941`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 9
- Flow F272 *Resource Management Configuration board 9: My Resource Operations Home*, step 16: Works in Operational Notifications & Live Alerts → Provide employees and managers with timely, prioritized operational notifications.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-941?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Assignment, Schedule, Resource, Event, Attendance, Approval, Emergency/critical operations, AI recommendation.
- [ ] Every transition is wired: `BO-933`.
- [ ] Every gated control is gated: `WORKFORCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-942` Mobile Operations Control & Offline Sync

**Configure and monitor how Resource Management operates on mobile devices, particularly where connectivity is unreliable.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block B · task VM-BO-942 |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/mobile-operations-control-offline-sync-bo-942` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-001): getGameplaySyncStatus reports game readers' offline plays; the Employee App's handsets and pending resource actions are not game readers. No read of mobile …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Configures and monitors how the Employee App runs resource-management work (check-in, scanning, handover, checklists) when connectivity drops, and shows which handsets are offline or holding unsynced actions. It belongs to the resource-management board; it has nothing to do with game readers. The one thing to get right: per-function offline switches with the limits, and a device monitor where sync conflicts are flagged and kept, never silently overwritten.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No record for the mobile offline settings (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): getGameplaySyncStatus is bound (CHG-WIR-001); Filed under the Games & Rides process module while the screen is Rentals / resource management (CHG-SBO-003); A primary button labelled "Board 9 — Smart Mobile Home Principle" (CHG-SBO-016).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Offline capability**: Master switch, then per-function switches - Assignment cache, Schedule cache, Check-in, Resource scanning, Handover, Checklist. Maximum offline period (hours), Synchronisation frequency (minutes). *(source: screens/P08-venue-back-office.yaml#BO-942)*
- **Data retention on the device**: Read-only reference to the tenant's retention setting for cached data, linking to where it is set. *(source: screens/P08-venue-back-office.yaml#BO-942 / contracts/spine/tenancy.yaml#listDataRetentionSettings)*
- **Conflict policy**: Closed choice - Ask a supervisor (default), or Apply configured policy; the pack's rule that a conflict is never silently overwritten is fixed text. *(source: screens/P08-venue-back-office.yaml#BO-942)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Device and sync monitor**: Tiles Active mobile sessions, Offline devices, Pending actions, Sync failures; table Device, Staff, Last sync, Pending actions, App version (current or behind), Status. *(source: screens/P08-venue-back-office.yaml#BO-942)*
- **Offline workspace preview**: Phone-size frame of the Staff App offline state - "OFFLINE MODE, last synchronised 14:32", cached items (Today's assignments, Resource details, Operational checklist, Venue information), "Pending synchronisation 4 actions" listing them. *(source: screens/P08-venue-back-office.yaml#BO-942)*
- **Conflicts**: List of flagged conflicts with the original offline action preserved, the server state, the operational impact and Resolve. *(source: screens/P08-venue-back-office.yaml#BO-942)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save mobile configuration**: Greyed until a record holds these settings (VO-R13). *(source: DI-653)*
- **Resolve conflict**: Supervisor chooses keep server state or apply the offline action, with a reason; audited. *(source: screens/P08-venue-back-office.yaml#BO-942)*

**Where the user goes next**

- → `BO-933` My Resource Operations Home: *Back to My Resource Operations Home*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The mobile operations offline list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the mobile operations offline untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No mobile operations offline yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the mobile operations offline are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A resource assigned offline became unavailable centrally**: Sync flags the conflict, keeps the offline transaction, shows the impact, and asks for resolution. *(source: screens/P08-venue-back-office.yaml#BO-942)*
- **Actions synced out of order**: Applied in the order they happened, with original and sync times shown. *(source: DI-065)*

#### Consistency with other screens

- Match `BO-471`: Same monitor pattern (pending, oldest, last sync) as the games offline monitor, different data.
- Match `BO-933`: Returns to My Resource Operations Home; the role-based mobile home (pack p148) is that board's subject.
- Match `EMP-043`: The Staff App's offline indicator and pending count (VO-R07) are what the preview shows.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
config:
  offline: 'On'
  functions: Assignment cache, Schedule cache, Check-in, Scanning, Handover, Checklist
  maxOffline: 8 hours
  syncEvery: 5 min
devices:
- device: EMP-HS-014
  staff: Maria Santos
  lastSync: '14:32'
  pending: 4
  appVersion: 2.6.1
  status: Offline
- device: EMP-HS-022
  staff: Omar Haddad
  lastSync: '14:58'
  pending: 0
  appVersion: 2.6.1
  status: Online
```

#### Permissions

**A refused user sees:** Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-942` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS134 Resource Management Configuration Board 9.dc.html#bo-942`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 9
- Flow F272 *Resource Management Configuration board 9: My Resource Operations Home*, step 18: Works in Mobile Operations Control & Offline Sync → Configure and monitor how Resource Management operates on mobile devices, particularly where connectivity is unreliable.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-942?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-933`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P08 reference designs** (from `handoff/design-batches/apps/5-venue-management/README.md`)

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: the client-approved POS, for operator density and components.
- `sources/designs/TICVAI_Mobile.dc.html`: for finish and motion.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-028, DI-029, DI-030, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-039, DI-040, DI-041, DI-042, DI-043, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051, DI-052 (each is in the design inputs below).

**Workshop tracker rows about P08 as a whole** (1: 1 open, 0 closed). Open first; a closed row says where it went on 30 September.

- **S8** Venue Management back-end configuration wireframes *(Chinmay Parab · In progress · due Fri 2 Oct · 30 Sep 2026 · 30 Sep tracker)*

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

### Across P08 Venue Management

- Qossai: configuration screens should consolidate related functionality, potentially merging 3-4 previously separate screens into one, rather than the repetitive one-screen-per-concept pattern of the AI-built reference system. *(agreed · MoM 24 Sep 2026, 4.5 Screen Consolidation Philosophy · DI-987)*
- **Open question.** Open: should AI monitoring live in one centralised AI command dashboard or be distributed as widgets in each functional module's own dashboard? Allam: Softlabs' call; the current proposal is illustrative and Softlabs may propose a better structure. *(open · MoM 18 Sep 2026, 4.4 AI Governance — Risk, Compliance & Continuous Monitoring · DI-936)*
- Simulation functionality stays embedded within each relevant configuration section rather than being consolidated, since it tests that section's own configuration. *(agreed · MoM 8 Sep 2026, 4.11 Dashboard & Reporting Module Consolidation Strategy · DI-722)*
- Client boards (POS Frontline, F&B, Retail, Inventory & Procurement) share one architecture: six boards of ten screens per domain, a command centre first and an AI/analytics board last, under the hierarchy Company > Venue > Department > Workstation > Operator/Shift > Transaction > Exception > Reconciliation > Analytics. *(agreed · client-design-boards-audit 20 Aug 2026, Opening / What the boards give us · DI-400)*
- Decision: RBAC per role, per module, three levels — edit/view, view-only, hidden (e.g. a marketing officer does not see Finance at all) — plus sub-permissions within a module (a CRM role may get Campaigns and Communications but not Journeys). Default role templates, admin-customisable. *(agreed · MoM 20 Aug 2026, 4.7 Role-Based Access Control (RBAC); 5. Key Decisions · DI-387)*
- **Open question.** Allam: a user's visibility must be restrictable to specific outlets (an F&B manager of one outlet should not see other outlets' items); also relevant for ticketing/event-specific access. Implementation approach still open. *(open · MoM 18 Aug 2026, 4.6 Role-Based & Outlet-Level Access Control — Open Item · DI-331)*
- Access loads automatically at login on POS and web/admin. A user with one role logs straight in; a user with several roles (e.g. admin, cashier, supervisor, manager) is prompted to choose which role to use. *(agreed · MoM 12 Aug 2026, 4. Multiple Roles per User and Role Switching · DI-249)*
- Back office is role-driven from any device: a finance user signing in from a workstation, laptop or home sees only finance reports and related information. *(agreed · MoM 12 Aug 2026, 3. Role-Based Access and Workstation-Linked Front-End · DI-248)*
- Built-in help menu with step-by-step tutorials with screenshots for common tasks (e.g. how to sell a ticket at the POS). *(client request · MoM 7 Aug 2026, 8. Legacy POS Layout Designer & System Logging · DI-160)*
- Custom data-capture fields ("data mask") at account, event, extended-ticket and product level: field types text, dropdown, radio, true/false; multi-language labels; validation (min/max length, required/optional); reusable value lists (e.g. country list). Standard fields come out of the box. *(agreed · MoM 7 Aug 2026, 6. Data Mask: Flexible Custom Data Capture · DI-155)*
- Load/traffic dashboards respect the tenancy model: a venue manager sees traffic for their own venue only. *(agreed · MoM 31 Jul 2026, 4. Non-Functional Requirements: Scalability & Availability · DI-061)*
- Allam: queue management is built into the system (not third-party) so traffic entering the site can be throttled from the back office itself. *(agreed · MoM 31 Jul 2026, 4. Non-Functional Requirements: Scalability & Availability · DI-060)*
- **Open question.** Proposed tenant hierarchy Tenant > Organization/Brand > Region > Branch > Venue > Department, under review against TICVAI's own organisational hierarchy before finalising. *(open · MoM 30 Jul 2026, 2. Proposed Multi-Tenant Hierarchy · DI-055)*
- Documentation deliverable includes user guides and help content; the preview shows a TICVAI Help Center with categories (Getting Started, Events, Tickets, Orders, Payments, Memberships, Access Control, Reports, Integrations), a "Welcome to TICVAI" getting-started article and Quick Links (Create an Event, Set Pricing, Manage Access, View Reports). *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - What We Deliver / Key Deliverables Preview · DI-052)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- AI Assistant panel: a short framing ("Based on last 30 days, here are 3 actions that can improve your revenue") then actionable recommendations, each with its potential impact (e.g. "Increase pricing for VIP seats, +12%") and a chevron, plus "View all recommendations". *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - AI Panels · DI-043)*
- Chart cards: title with period dropdown ("This Week"), headline metrics with deltas (Tickets Sold 12,840 +8.7%, Visitors, Conversion). Data visualisations must be easy to read. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Charts · DI-041)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Back-office shell: collapsible left sidebar with Overview, Events, Tickets, Orders, Customers, Memberships, Access Control, POS, Reports, Analytics, AI Assistant, Settings, and the signed-in user (name, role) at the bottom; top bar with global search (Cmd+K), current time and date, Notifications with unread dot, and user menu. *(agreed · Design Vision Book 29 Jul 2026, 04 Dashboard Vision (p4) - navigation shell · DI-030)*
- Dynamic KPIs, forecasts and real-time insights; role-based dashboards, preferences and smart shortcuts for every user (e.g. greeting "Good morning, Ahmed" on the home screen, p2). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Smarter Data / Personalized Experience · DI-028)*
- Reports and historical searches must still retrieve archived transactions when required; the retention period (e.g. keep 3 of 5+ years live) is configurable per customer, archival manual or automated. *(agreed · MoM 28 Jul 2026, 23. Database Optimisation and Archiving · DI-018)*
- Back-office controls for the waiting room: configurable maximum active users and admission intervals, set per customer and venue. *(agreed · MoM 28 Jul 2026, 19. Auto-scaling and Virtual Waiting Room · DI-017)*

**5 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"checkInResource": {"method":"POST","path":"/resource-bookings/{bookingId}/check-in","contract":"resources","summary":"Take it back, and settle the deposit","permission":"RESOURCE_BOOK","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ResourceBooking"},
"checkOutResource": {"method":"POST","path":"/resource-bookings/{bookingId}/check-out","contract":"resources","summary":"Hand it over, with a deposit against it","permission":"RESOURCE_BOOK","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ResourceBooking"},
"decideApprovalRequest": {"method":"POST","path":"/approval-requests/{requestId}/decide","contract":"approvals","summary":"Approve, reject, return or ask for information","permission":"APPROVAL_DECIDE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ApprovalRequest"},
"getResource": {"method":"GET","path":"/resources/{resourceId}","contract":"resources","summary":"One resource, with every configured section","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Resource"},
"getResourceCalendar": {"method":"GET","path":"/resource-calendar","contract":"resources","summary":"Every resource against time, with conflicts already marked","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true},{"name":"resourceTypeId","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"granularity","in":"query","required":null}],"requestBody":null,"responds":"ResourceCalendarRow"},
"listAnnouncements": {"method":"GET","path":"/announcements","contract":"workforce","summary":"What staff have been told","permission":"WORKFORCE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"unacknowledgedOnly","in":"query","required":null}],"requestBody":null,"responds":"Announcement"},
"listApprovalRequests": {"method":"GET","path":"/approval-requests","contract":"approvals","summary":"Requests awaiting a decision, or already decided","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"assignedToMe","in":"query","required":null},{"name":"raisedByMe","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"breachingWithinMinutes","in":"query","required":null},{"name":"sort","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listResourceBookings": {"method":"GET","path":"/resource-bookings","contract":"resources","summary":"Bookings, filtered","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"resourceId","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"status","in":"query","required":null}],"requestBody":null,"responds":"ResourceBooking"},
"listShiftSwapRequests": {"method":"GET","path":"/shift-swaps","contract":"workforce","summary":"Swap requests and their state","permission":"WORKFORCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ShiftSwap"},
"raiseResourceRequest": {"method":"POST","path":"/resource-requests","contract":"resources","summary":"Ask for a replacement, extra equipment or a change to an assignment","permission":"RESOURCE_VIEW","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResourceRequestInput","responds":"ResourceRequest"},
"recordAttendance": {"method":"POST","path":"/attendance/clock","contract":"workforce","summary":"Clock in, clock out, or take a break","permission":"ATTENDANCE_RECORD","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AttendanceRecord"},
"reportIncident": {"method":"POST","path":"/incidents","contract":"maintenance","summary":"Report an incident","permission":"INCIDENT_REPORT","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ReportIncidentRequest","responds":"Incident"},
"requestShiftSwap": {"method":"POST","path":"/rota-assignments/{assignmentId}/swap","contract":"workforce","summary":"Ask someone to take your shift","permission":"WORKFORCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"setResourceBookingProgress": {"method":"POST","path":"/resource-bookings/{bookingId}/progress","contract":"resources","summary":"Start or complete a staff or instructor assignment","permission":"RESOURCE_BOOK","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResourceBookingProgressInput","responds":"ResourceBooking"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"Announcement": {"type":"object","x-ticvai-persistence":"workforce.announcement","required":["title","body","kind","publishedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"title":{"type":"string","maxLength":140},"body":{"type":"string","maxLength":4000},"kind":{"$ref":"#/components/schemas/AnnouncementKind"},"venueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"departmentIds":{"type":"array","items":{"type":"string","format":"uuid"}},"roleIds":{"type":"array","items":{"type":"string","format":"uuid"}},"requiresAcknowledgement":{"type":"boolean"},"deliveryChannels":{"type":"array","description":"How it reaches people (29 September, build, 18.1.5). `inApp` always; `push` to the targeted people's registered staff phones (tenancy `RegisteredDevice`, kind `mobileHandset`). `emergency` is sent by both whatever is set here.\n","items":{"type":"string","enum":["inApp","push"]},"default":["inApp","push"]},"expiresAt":{"type":"string","format":"date-time","nullable":true},"publishedByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"publishedAt":{"type":"string","format":"date-time"},"locale":{"type":"string","nullable":true}}},
"AnnouncementKind": {"type":"string","description":"`emergency` is not a louder `operational`. It overrides the home screen, bypasses quiet hours, requires acknowledgement, and carries a separate permission.\n","enum":["operational","safety","emergency","hr","celebration"]},
"ApprovalDecision": {"type":"object","x-ticvai-persistence":"approvals.decision","required":["level","principalId","decision","decidedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"level":{"type":"integer"},"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"},"delegatedFrom":{"type":"string","format":"uuid","nullable":true},"decision":{"type":"string","enum":["approve","reject"]},"comment":{"type":"string","nullable":true},"reason":{"type":"string","nullable":true},"usedMfa":{"type":"boolean"},"signatureRef":{"type":"string","nullable":true},"decidedAt":{"type":"string","format":"date-time"}}},
"ApprovalKind": {"type":"string","description":"11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n\n**Optional review steps a venue switches on, decided 2 October 2026** (Chinmay; CHG-CSP-036, CHG-CSP-028, CHG-CSP-031). Each is an existing kind narrowed by the rule's `subjectTypes`, so no kind is added (a new value here would be a breaking change against r1) and each is off until the venue saves an active matrix for it:\n- **A purchase order** (`requisition`, subject `purchaseOrder`; Chinmay, 3 October 2026, Block A business rules; CHG-RUL-004): the PO approval matrix. Blanket and RFQ-award orders are raised without a requisition and are approved here instead; `inventory.createPurchaseOrder` asks for every order, by kind and value. - **Publishing white-label content** (`configurationChange`, subject `whiteLabelPublication`): simulate, then a single publish by a holder of the permission; a review step only where the venue sets one up (batch 1, CMS-014; DEC-156). - **Recording F&B waste above a value** (`stockWriteOff`, subject `fnbWaste`): the venue's waste-approval policy, value bands as `minAmount` and `maxAmount`, photo evidence above a value held by fnb (batch 6 #192, BO-139; DEC-192; R144). - **Publishing an access topology** (`configurationChange`, subject `topologyPublication`): second-person approval when the venue switches it on (batch 6 #230, BO-153; DEC-230). - **A permanent identity lock, a whitelist entry, or releasing a full-identity or permanent lock** (`accessPermissionChange`, subjects `identityLock`, `whitelistEntry`, `identityLockRelease`): always a second approver, never for an until-end-of-day lock (critical set 1, BO-229 and BO-247; DEC-254, DEC-260); the tenant default matrix names the security approver role and a venue may tighten it, never remove it.\n\n**A rota shift swap** (4 October 2026, CHG-FXC-008; Sprint 1-2 judging: `workforce.requestShiftSwap` raised a request\nwith no kind that fits). `configurationChange`, subject `shiftSwap`, `subjectContract` `workforce`, `subjectId` the\nShiftSwap id: an existing kind narrowed by `subjectTypes`, as the optional review steps above, so no kind is added.","enum":["refund","priceOverride","discountOverride","complimentaryTicket","membershipCancellation","accessPermissionChange","configurationChange","aiRecommendation","releasePromotion","requisition","stockWriteOff","journalEntry","periodClose","periodReopen","purchaseOrderCancel","purchaseOrderShortClose","tenantMigration","productChange","pricingChange"]},
"ApprovalMode": {"type":"string","description":"11.1.43–11.1.46. **Sequential** asks one at a time, **parallel** asks everyone at once, **consensus** needs all of them, **majority** needs more than half.\nParallel and consensus differ in when it completes: parallel completes on the first approval, consensus waits for all. Conflating them is how a four-eyes rule turns into a one-eye rule.\n","enum":["sequential","parallel","consensus","majority"]},
"ApprovalRequest": {"type":"object","x-ticvai-persistence":"approvals.request","required":["id","kind","status","requestedByPrincipalId","requestedAt"],"properties":{"id":{"type":"string"},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"rerouteOnNoApprover":{"type":"boolean","default":true,"description":"BL-154. **An approver on leave is an approval that waits for them to come back.** Reroutes to the next in the chain rather than stalling — `workforce` already knows who is on leave, and an approval queue nobody is watching is the thing that stops a venue.\n"},"outOfOfficeDelegateId":{"type":"string","format":"uuid","nullable":true},"allowEmailApproval":{"type":"boolean","default":false,"description":"**Approving from an email link with no second factor is the weakest path in the system**, so it is off by default and available only below a configured value.\n"},"reopenedFrom":{"type":"string","format":"uuid","nullable":true,"description":"**Reopening a decided approval creates a new one that points back.** Editing a decision in place destroys the record of what was originally approved, which is the only thing an audit wants.\n"},"status":{"$ref":"#/components/schemas/ApprovalStatus"},"subjectContract":{"type":"string"},"subjectType":{"type":"string"},"subjectId":{"type":"string"},"scopePath":{"type":"string"},"summary":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"justification":{"type":"string","nullable":true},"requestedByPrincipalId":{"type":"string","format":"uuid"},"matrixVersion":{"type":"integer"},"mode":{"$ref":"#/components/schemas/ApprovalMode"},"currentLevel":{"type":"integer"},"totalLevels":{"type":"integer"},"pendingApprovers":{"type":"array","items":{"type":"object","properties":{"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"}}}},"decisions":{"type":"array","description":"Every decision at every level, in order. **Immutable once the request completes** (11.1.56) — an approval is evidence, and amending one is a different fact.\n","items":{"$ref":"#/components/schemas/ApprovalDecision"}},"escalations":{"type":"array","description":"11.1.48. Who was asked, when, and why it moved up. **Escalation adds an approver rather than replacing one**, so the original stays in the record.\n","items":{"type":"object","properties":{"at":{"type":"string","format":"date-time"},"reason":{"type":"string"},"fromLevel":{"type":"integer"},"toLevel":{"type":"integer"},"wasAutomatic":{"type":"boolean"}}}},"resubmittedFromId":{"type":"string","nullable":true},"reopenedFromId":{"type":"string","nullable":true},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"slaBreached":{"type":"boolean"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Who claimed or was assigned the request in a shared queue (`assignApprovalRequest`; DI-723; CHG-CSP-042). Null while it sits in the queue."},"assignedToDepartmentId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The department queue it was assigned to, where it went to a department rather than a person (CHG-CSP-042)."},"assignedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"requestedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"aiAssessment":{"type":"object","nullable":true,"readOnly":true,"description":"**AI context for the reviewer, never an input to the decision** (11.1.73 to 11.1.75; MoM 8 September; 29 September, build pass, group G2). Written by approvals from `ai.scoreApprovalRequest` on submit and on each SLA tick; null where AI is off or has not answered. Shown on the request labelled as AI; orders the inbox only when `sort=aiPriority` is asked for.","properties":{"riskScore":{"type":"integer","minimum":0,"maximum":100},"riskBand":{"type":"string","enum":["low","medium","high","critical"]},"priorityScore":{"type":"integer","minimum":0,"maximum":100},"escalationSuggestion":{"type":"object","description":"A suggestion a person may act on through `escalateApprovalRequest`, or the tenant's own SLA policy may; nothing escalates because of it.","properties":{"action":{"type":"string","enum":["escalate","addBackupApprover","none"]},"reason":{"type":"string","nullable":true}}},"signals":{"type":"array","maxItems":10,"description":"The signals behind the scores, largest first, as `ai.AiApprovalRequestScore.signals`.","items":{"type":"object","properties":{"code":{"type":"string"},"contribution":{"type":"number"},"detail":{"type":"string","nullable":true}}}},"scoreId":{"type":"string","format":"uuid","description":"The `ai.approval_request_score` row it was copied from; `ai.getApprovalRequestScore` gives the full context. Not a foreign key (the score lives in the AI service)."},"decisionRecordId":{"type":"string","description":"The ai decision record, for the audit of what the AI said and why."},"assessedAt":{"type":"string","format":"date-time"}}}}},
"ApprovalStatus": {"type":"string","enum":["draft","pending","escalated","returned","informationRequested","approved","rejected","withdrawn","expired","cancelled"]},
"AttendanceAmendment": {"type":"object","x-ticvai-persistence":"workforce.attendance_amendment","description":"One correction to an attendance record, appended by `amendAttendance` and never updated (decided 28 September, audit R129 (7)).\n","required":["id","attendanceRecordId","amendedByPrincipalId","amendedAt","occurredAtBefore","occurredAtAfter","reason"],"properties":{"id":{"type":"string","format":"uuid"},"attendanceRecordId":{"type":"string","format":"uuid"},"amendedByPrincipalId":{"type":"string","format":"uuid"},"amendedAt":{"type":"string","format":"date-time"},"occurredAtBefore":{"type":"string","format":"date-time","description":"The record's time before this correction."},"occurredAtAfter":{"type":"string","format":"date-time","description":"The time this correction set (`correctedAt` on the request)."},"reason":{"type":"string","maxLength":300}}},
"AttendanceRecord": {"type":"object","x-ticvai-persistence":"workforce.attendance","required":["id","principalId","kind","occurredAt"],"properties":{"id":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid"},"assignmentId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["clockIn","clockOut","breakStart","breakEnd"]},"occurredAt":{"type":"string","format":"date-time","description":"Device time — when it happened."},"recordedAt":{"type":"string","format":"date-time","description":"When the server received it. **Both are kept**: a steward clocking in offline at a gate is not late because the sync was.\n"},"accessPointId":{"type":"string","format":"uuid","nullable":true},"latitude":{"type":"number","nullable":true},"longitude":{"type":"number","nullable":true},"isAmended":{"type":"boolean","readOnly":true},"amendedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Who made the latest amendment. The full history is `amendments` (audit R129 (7))."},"amendmentReason":{"type":"string","nullable":true,"readOnly":true,"description":"The latest amendment's reason. The full history is `amendments` (audit R129 (7))."},"originalOccurredAt":{"type":"string","format":"date-time","nullable":true,"description":"**The original is never overwritten.** Attendance feeds pay, and a record that can be quietly rewritten is not evidence.\n"},"amendments":{"type":"array","readOnly":true,"description":"**Every correction, oldest first, one row each** (decided 28 September, audit R129 (7)). A single set of amendment columns holds only the last one, and the second correction to a record would erase the evidence of the first.\n","items":{"$ref":"#/components/schemas/AttendanceAmendment"}},"exception":{"type":"string","nullable":true,"enum":["late","earlyLeave","missingClockOut","noShow","outOfGeofence","unscheduled"],"description":"Computed against the rota. Null where the record matches what was expected."}}},
"Incident": {"x-ticvai-persistence":"maintenance.incident","type":"object","required":["id","incidentNumber","kind","severity","status","venueId","occurredAt","reportedByPrincipalId"],"properties":{"id":{"type":"string","format":"uuid"},"incidentNumber":{"type":"string","readOnly":true,"description":"**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity.\n"},"kind":{"$ref":"#/components/schemas/IncidentKind"},"severity":{"$ref":"#/components/schemas/IncidentSeverity"},"status":{"$ref":"#/components/schemas/IncidentStatus"},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true},"locationDescription":{"type":"string","nullable":true},"isReportable":{"type":"boolean","description":"Requires notification to an external authority within a statutory window."},"notificationDueAt":{"type":"string","format":"date-time","nullable":true},"notifiedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"The earliest `notifiedAt` among this incident's authority notifications. **Maintained on write** by `recordAuthorityNotification`; each notification itself is a row of `maintenance.incident_authority_notification`.\n"},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true},"reportedByPrincipalId":{"type":"string","format":"uuid"},"correctiveWorkOrderId":{"type":"string","format":"uuid","nullable":true},"escalation":{"type":"object","nullable":true,"readOnly":true,"description":"**Set while the incident is escalated** (the optional Escalated step of the 3 October flow; CHG-RUL-011). Screens show \"Escalated\" when `status` is `underInvestigation` and this is set. Cleared when the incident closes.\n","properties":{"toPrincipalId":{"type":"string","format":"uuid"},"byPrincipalId":{"type":"string","format":"uuid"},"reason":{"type":"string"},"escalatedAt":{"type":"string","format":"date-time"}}},"reopenCount":{"type":"integer","minimum":0,"readOnly":true,"description":"How many times the incident was reopened (CHG-RUL-011). Each reopen is a logged row."},"occurredAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"closedAt":{"type":"string","format":"date-time","nullable":true},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"IncidentKind": {"type":"string","enum":["guestInjury","staffInjury","nearMiss","propertyDamage","equipmentFailure","securityIncident","fireOrEvacuation","foodSafety","environmental","other"]},
"IncidentSeverity": {"type":"string","enum":["nearMiss","minor","moderate","major","critical"]},
"IncidentStatus": {"type":"string","enum":["reported","underInvestigation","actionRequired","closed"]},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ReportIncidentRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","kind","severity","venueId","description","occurredAt","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/IncidentKind"},"severity":{"$ref":"#/components/schemas/IncidentSeverity"},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid"},"locationDescription":{"type":"string","maxLength":500},"description":{"type":"string","minLength":3,"maxLength":10000},"involvedSubjectIds":{"type":"array","description":"Opaque references. Personal details live in the erasable store, so the incident record survives an erasure request intact.\n","items":{"type":"string","format":"uuid"}},"involvedStaffPrincipalIds":{"type":"array","items":{"type":"string","format":"uuid"}},"witnessCount":{"type":"integer"},"firstAidGiven":{"type":"boolean","default":false},"emergencyServicesCalled":{"type":"boolean","default":false},"attachmentRefs":{"type":"array","items":{"type":"string"}},"occurredAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"}}},
"Resource": {"type":"object","x-ticvai-persistence":"resources.resource","description":"**A specific object, not a quantity of interchangeable ones.** A venue with forty identical strollers has forty resources, because guest number twelve returned stroller number twelve.\n","required":["id","code","name","kind","venueId"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"kind":{"$ref":"#/components/schemas/ResourceKind"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"parentResourceId":{"type":"string","format":"uuid","nullable":true,"description":"**A pool cabana belongs to the pool area; a seat belongs to an auditorium.** Booking a parent takes its children with it, which is the behaviour a venue expects and would otherwise have to enforce by hand.\n"},"principalId":{"type":"string","format":"uuid","nullable":true,"description":"For a resource of kind `instructor` or `staff`. **`workforce` still owns their rota** — this says whether they are qualified and whether they are already committed.\n"},"attributes":{"type":"object","additionalProperties":true,"description":"Configurable per kind — capacity, size, shade, power, poolside."},"setupMinutes":{"type":"integer","default":0,"description":"**Before the booking, not inside it.** An auditorium booked 14:00–16:00 is unavailable from 13:30 with a 30-minute setup, and a calendar that cannot express that double-books every time.\n"},"teardownMinutes":{"type":"integer","default":0,"description":"After the booking. **Kept as it is** (decided 29 September, W10): with a `cleaningPolicy` of `afterEveryBooking` the cleaning buffer is added after the teardown, so a room with no teardown and a 15-minute clean is free 15 minutes after each booking ends.\n"},"cleaningPolicy":{"allOf":[{"$ref":"#/components/schemas/ResourceCleaningPolicy"}],"nullable":true,"description":"How the resource is cleaned between uses (decided 29 September, W10). Null means no cleaning is scheduled beyond `teardownMinutes`."},"requiresQualification":{"type":"array","items":{"type":"string"},"description":"Qualification codes a person must hold to be assigned to this."},"depositAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["available","booked","checkedOut","maintenance","retired"]},"isActive":{"type":"boolean","default":true},"resourceTypeId":{"type":"string","format":"uuid","nullable":true,"description":"**The configurable resource type** (`resources.resource_type`, 4 October 2026, CHG-FXC-003). `kind` is the fixed family a type belongs to; this is the tenant's own type within it, and the `resourceTypeId` filter of `suggestResources` and `ResourceRequirement.resourceTypeId` match on it."}}},
"ResourceBooking": {"type":"object","x-ticvai-persistence":"resources.booking","required":["id","resourceId","from","to","status"],"properties":{"id":{"type":"string","format":"uuid"},"resourceId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true},"orderId":{"type":"string","format":"uuid","nullable":true},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"status":{"$ref":"#/components/schemas/ResourceBookingStatus"},"holdId":{"type":"string","format":"uuid","nullable":true,"description":"The `ResourceHold` this booking was converted from, where a guest picked the resource on a venue map (rev 3 REV3-15). Null for a staff booking or an allocation.\n"},"recurrenceGroupId":{"type":"string","format":"uuid","nullable":true,"description":"Ties the occurrences of a recurring booking. **Cancelling one week does not cancel the series**, and cancelling the series is a separate act with a separate confirmation.\n"},"depositAuthorisationId":{"type":"string","format":"uuid","nullable":true,"description":"The hold, through `orders.authoriseStoredValue` (CF-126). **A deposit taken and refunded is two transactions and a fee; held and released is neither.**\n"},"checkedOutAt":{"type":"string","format":"date-time","nullable":true},"dueBackAt":{"type":"string","format":"date-time","nullable":true},"returnedAt":{"type":"string","format":"date-time","nullable":true},"conditionOut":{"type":"string","nullable":true},"conditionIn":{"type":"string","nullable":true},"syncedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When the latest offline check-out or check-in write reached the server. **The device times are `checkedOutAt` and `returnedAt`**, taken from each write's `recordedAt`; this is the server's half of the pair naming-and-style 5.2 requires. Null while pending.\n"}}},
"ResourceBookingProgressInput": {"type":"object","x-ticvai-persistence":"none — request only; the step is recorded on resources.booking","description":"What `setResourceBookingProgress` takes (decided 29 September, readiness close-out).","required":["state","recordedAt"],"properties":{"state":{"type":"string","enum":["started","completed"],"description":"`started` is recorded as `checkedOut`, `completed` as `returned`."},"note":{"type":"string","maxLength":1000,"nullable":true},"recordedAt":{"type":"string","format":"date-time","description":"When the employee pressed the button on the device, not when the write reached the server."}}},
"ResourceBookingStatus": {"type":"string","enum":["reserved","checkedOut","returned","overdue","cancelled","noShow"]},
"ResourceCalendarRow": {"type":"object","description":"Board 2.01. **One resource across the window, with its states already computed** — including conflict, which a client cannot derive from a booking list.\n","properties":{"resourceId":{"type":"string","format":"uuid"},"resourceName":{"type":"string"},"resourceTypeId":{"type":"string","format":"uuid"},"utilisationPercent":{"type":"number"},"segments":{"type":"array","items":{"type":"object","properties":{"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"state":{"type":"string","enum":["available","reserved","assigned","partiallyUtilised","fullyUtilised","unavailable","onBreak","onLeave","underMaintenance","operationallyBlocked","pendingApproval","conflict"]},"bookingId":{"type":"string","format":"uuid","nullable":true},"conflictsWith":{"type":"array","items":{"type":"string","format":"uuid"}}}}}}},
"ResourceCleaningPolicy": {"x-ticvai-persistence":"none — columns on resources.resource","type":"object","description":"**When the resource is cleaned, and what that takes out of availability** (decided 29 September, W10; the meeting-room case from the 29 September website review).\n- `afterEveryBooking` (option A): `bufferMinutes` blocked after every booking, after its teardown. - `timesPerDay` (option B): `cleaningsPerDay` cleanings of `bufferMinutes` each, between `windowStart` and `windowEnd`, **placed by the system**. The targets are spread evenly across the window; each is put in the free gap nearest its target that is long enough, and never on a booking, a hold or a block. **A confirmed booking is never moved for a cleaning.** Placement is computed on read from the day's bookings, so it moves when bookings change, and a start time is offered only if every cleaning of that day can still be placed after it is booked.\n`createResource` and `updateResource` refuse a policy with `timesPerDay` and no `cleaningsPerDay`, or a window that ends before it starts, with `422`.\n","required":["mode","bufferMinutes"],"properties":{"mode":{"type":"string","enum":["afterEveryBooking","timesPerDay"]},"bufferMinutes":{"type":"integer","minimum":5,"maximum":240,"description":"Minutes one cleaning takes. The prototype uses 15 (proposed default, client to correct)."},"cleaningsPerDay":{"type":"integer","minimum":1,"maximum":24,"nullable":true,"description":"Required for `timesPerDay`; ignored for `afterEveryBooking`."},"windowStart":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","nullable":true,"description":"Venue-local time the cleaning window opens. Null means the resource's opening time."},"windowEnd":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","nullable":true,"description":"Venue-local time the cleaning window closes. Null means the resource's closing time."}}},
"ResourceKind": {"type":"string","description":"BL-135. **`locker` was an entitlement kind in `orders` and nothing issued, assigned or released one.** A locker is a specific object checked out to a named guest and returned — which is this context exactly, and modelling it as an entitlement would have needed a second check-out mechanism.\nA seed for `ResourceType` rather than the law (board 1.02): a customer adding a class does it with `createResourceType`, not by waiting for this list to grow.\n**`table` is a non-dining spot** (decided 29 September, rev 3 GAP-C2, confirmed by Chinmay): a beach or event table placed on a venue map, picked and sold like a cabana (`createResourceHold`, then the order). **A dining table is not this**: restaurant tables stay `fnb` tables, booked with `fnb.createTableReservation` and the waitlist (audit R073 (d)).\n","enum":["cabana","lounger","locker","wheelchair","stroller","equipment","room","auditorium","vehicle","instructor","staff","table","pitch","studio","other"],"x-ticvai-refuses":{"mealPlan":"**Listed by 5.5.8b and deliberately not a kind.** 5.5.8b groups meal plans with lockers and parking, but a meal plan is a balance rather than an object. It resolves to `retail.Wallet` with a `mealPlan` credit kind (CF-126), not to a resource — so it is not offered here, and a form built from this enum cannot offer it either."}},
"ResourceRequest": {"type":"object","x-ticvai-persistence":"resources.resource_request","description":"**An employee's request about the resources on an assignment** (decided 29 September, readiness close-out; BO-935, BO-938). New table. Raised `open`, then `acknowledged`, `resolved` or `declined` by the resource manager.\n","required":["id","kind","detail","status","raisedByPrincipalId","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/ResourceRequestKind"},"bookingId":{"type":"string","format":"uuid","nullable":true},"resourceId":{"type":"string","format":"uuid","nullable":true},"detail":{"type":"string"},"status":{"type":"string","enum":["open","acknowledged","resolved","declined"],"readOnly":true,"description":"`open` on raise."},"raisedByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","readOnly":true},"resolutionNote":{"type":"string","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true}}},
"ResourceRequestInput": {"type":"object","x-ticvai-persistence":"none — request only","description":"What `raiseResourceRequest` takes.","required":["id","kind","detail","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7, so a request raised offline is not duplicated on sync."},"kind":{"$ref":"#/components/schemas/ResourceRequestKind"},"bookingId":{"type":"string","format":"uuid","nullable":true},"resourceId":{"type":"string","format":"uuid","nullable":true},"detail":{"type":"string","minLength":3,"maxLength":2000},"recordedAt":{"type":"string","format":"date-time"}}},
"ResourceRequestKind": {"type":"string","enum":["replacementResource","additionalEquipment","resourceIssue","maintenanceRequest","assignmentChange","venueChange","scheduleClarification","other"],"description":"The request kinds on BO-935 / BO-938 (decided 29 September, readiness close-out). `other` is the pack's custom operational request."},
"ShiftSwap": {"type":"object","x-ticvai-persistence":"workforce.shift_swap","required":["id","assignmentId","fromPrincipalId","toPrincipalId","status"],"properties":{"id":{"type":"string","format":"uuid"},"assignmentId":{"type":"string","format":"uuid"},"fromPrincipalId":{"type":"string","format":"uuid"},"toPrincipalId":{"type":"string","format":"uuid"},"status":{"type":"string","enum":["awaitingPeer","awaitingApproval","approved","rejected","withdrawn"],"description":"**Both parties before the supervisor.** A swap approved against someone who never agreed is a gap in the rota nobody notices until the shift starts.\n"},"approvalRequestId":{"type":"string","nullable":true,"description":"Routed through `approvals` rather than a second mechanism here."},"reason":{"type":"string","nullable":true},"requestedAt":{"type":"string","format":"date-time"}}},
"StoredValueKind": {"type":"string","description":"**Six things in this package hold a balance and behave the same way** — a wallet, a gift card, a game card, a voucher, a loyalty position and a prepaid entitlement. They were built separately across three sessions and each grew its own balance, bonus balance, status, blocked reason and expiry (CF-126).\n**The concern is not tidiness. Only one of the six could hold an authorisation.** `authoriseWalletSpend` / `captureWalletAuthorisation` / `relinquishWalletAuthorisation` gave two-phase spend to the retail wallet alone, so **a guest with 200 game credits starting a play the machine then failed had no held balance** — the credits were either taken or not, with no third state.\nThe entities stay distinct because their lifecycles genuinely differ — a gift card activates at a till, a loyalty position never expires the same way. **What is shared is the spend mechanism**, and this enum is what lets it be shared.\n","enum":["wallet","giftCard","gameCard","voucher","loyalty","prepaidEntitlement"]}
}
```
