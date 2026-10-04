# P17-onboarding-assessment-01 — P17 · Onboarding & Assessment

**10 screens · 5 operations · 10 schemas · 2 permissions**

Platform P17 TICVAI Sign-up · ships as **ticvai-control** ·
public audience · web ·
online only

## Who this is for

**public on web.** Everything below is how you know what is
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
  `PLATFORM_PLAN_MANAGE, TENANT_CONFIGURE`. A control nobody can use must say so,
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
| `SGN-001` | Welcome & Start Your TICVAI Journey | B | 4 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `SGN-002` | Customer & Organization Registration | B | 35 | 0 | 6 | 14 | 1 | 0 | — | notStarted (—) |
| `SGN-003` | Venue Type & Business Profile | B | 1 | 12 | 6 | 2 | 1 | 0 | — | notStarted (—) |
| `SGN-004` | Visitor, Capacity & Operational Scale | B | 0 | 0 | 6 | 2 | 1 | 0 | — | notStarted (—) |
| `SGN-005` | Sales Channel Assessment | B | 11 | 0 | 6 | 2 | 1 | 0 | — | notStarted (—) |
| `SGN-006` | Ticketing & Product Requirements | B | 15 | 0 | 6 | 2 | 1 | 0 | — | notStarted (—) |
| `SGN-007` | Access, Queue & Visitor Experience Assessment | B | 0 | 0 | 6 | 2 | 1 | 6 | — | notStarted (—) |
| `SGN-008` | Additional Business Module Assessment | B | 0 | 0 | 6 | 2 | 1 | 0 | — | notStarted (—) |
| `SGN-009` | Integration, Payment & Technical Readiness | B | 0 | 0 | 6 | 2 | 1 | 0 | — | notStarted (—) |
| `SGN-010` | AI Assessment Summary & Handoff | B | 0 | 0 | 6 | 2 | 1 | 0 | — | notStarted (—) |

## Thin screens in this batch

**SGN-003, SGN-004, SGN-007, SGN-008, SGN-009, SGN-010 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `SGN-001` Welcome & Start Your TICVAI Journey

**Provide the entry point for a new customer starting self-service onboarding.**

| | |
|---|---|
| App · platform | TICVAI Control · P17 TICVAI Sign-up (web) |
| Module | Onboarding & Assessment · wave 3 · needs the `core` module |
| Block | Block B · ticket #29375 (APP-SIGNUP-SGN-001) |
| Who uses it | public |
| Device and orientation | This is a public marketing and sign-up web flow, 1440 desktop and 390 phone widths, in TICVAI's own brand. · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Starting Options) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/onboarding-assessment/welcome-start-your-ticvai-journey-sgn-001` |

**What the spec says about it.** The self-service form of `ADM-379`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-021): The welcome page scores nothing (scoreVsiAssessment is called on the assessment screens SGN-003 to SGN-010); the operator-led copy ADM-379 loses it too, so the …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The first page a prospect sees: start a new setup, continue a saved one, sign in, or ask for an enterprise consultation. A prospect has no tenant yet.

**Fixed on main** (the package already carries these; draw what it says): The screen calls scoreVsiAssessment. (CHG-WIR-021); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **What session does a prospect have between "Start new setup" and activation (to save and continue)?** → Drawn default stands (answer: "Email + one-time code"): A prospect sign-up session created by SGN-002 (email + one-time code); draw "Continue saved setup" as sign-in with that code. *(decided by Chinmay, 2026-10-02; DEC-167 / CHG-NOTE-005)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Start New Setup | select field | — | — | — | — | — | — |
| Continue Saved Setup | select field | — | — | — | — | — | — |
| Sign In | select field | — | — | — | — | — | — |
| Request Enterprise Consultation | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `SGN-002` Customer & Organization Registration: *Customer & Organization Registration*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The welcome start your configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the welcome start your untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No welcome start your configured yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
form example:
  Start New Setup: 11
  Continue Saved Setup: 233
  Sign In: 46
  Request Enterprise Consultation: 312
```

#### Permissions

**A refused user sees:** TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Onboarding starts from a link on the TICVAI website and walks a structured question set; first section is organisation details: venue name, industry, attraction type, currency, region/country, contact details, business type (private, semi-government, non-profit). *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-809)*

Also apply: 10 for all of P17, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P17 TICVAI Sign-up.dc.html#sgn-001` · status **notStarted** · provenance —
- Workshop pack:  board 2

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SGN-001?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `SGN-002`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SGN-002` Customer & Organization Registration

**Create the initial customer account and organization profile.**

| | |
|---|---|
| App · platform | TICVAI Control · P17 TICVAI Sign-up (web) |
| Module | Onboarding & Assessment · wave 3 · needs the `core` module |
| Block | Block B · ticket #29091 (APP-SIGNUP-SGN-002) |
| Who uses it | public staff holding `TENANT_CONFIGURE` (1 configure) |
| Device and orientation | This is a public marketing and sign-up web flow, 1440 desktop and 390 phone widths, in TICVAI's own brand. · LTR and RTL · light theme |
| Pattern | wizard (compact density): Three steps on one form: prove the email, then the organisation, then submit (defined 4 October 2026 from OnboardingApplication, CHG-FXS-001). |
| Offline | online only |
| Opens with | `challengeId` (navigation) |
| Route | `/onboarding-assessment/customer-organization-registration-sgn-002` |

**What the spec says about it.** The self-service form of `ADM-380`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step. **Defined 4 October 2026 from StartProspectSignupRequest, VerifyProspectSignupCodeRequest and OnboardingApplication (companyName, contactEmail, contactPhone, countryCode, billingEntity)** (CHG-FXS-001)

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Create the prospect's customer account and organisation profile: legal name, country, contact, verified email.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- submitOnboardingApplication requires TENANT_CONFIGURE while the caller is a prospect with no tenant. (CHG-SOT-016)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Work email | email field | optional | — | max length 256 | name@example.ae | The prospect's work email; the one-time code goes here. | `StartProspectSignupRequest.email` |
| One-time code | text field | optional | — | pattern `^[0-9]{6}$` | — | Six digits; five attempts, then a new code is needed. | `VerifyProspectSignupCodeRequest.code` |
| Company name | text field | optional | — | — | — | — | `OnboardingApplication.companyName` |
| Contact email | email field | optional | — | — | name@example.ae | The verified email, read-only. | `OnboardingApplication.contactEmail` |
| Contact phone | phone field | optional | — | — | +971 5X XXX XXXX (E.164) | E.164, +971 by default. | `OnboardingApplication.contactPhone` |
| Country | text field | optional | — | — | — | ISO 3166-1 alpha-2; AE by default. | `OnboardingApplication.countryCode` |
| Legal name | text area | optional | — | max length 300 | — | Optional here; required before the first invoice. | `OnboardingApplication.billingEntity.legalName` |
| Trade licence number | text field | optional | — | max length 100 | — | Optional here. | `OnboardingApplication.billingEntity.tradeLicenceNumber` |
| Tax registration number (TRN) | text field | optional | — | max length 30 | — | Optional; 15 digits for a UAE VAT registrant. | `OnboardingApplication.billingEntity.trn` |

**Sent by *Send code*** (`startProspectSignup`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Email `email` | email field | required | — | max length 256 | name@example.ae | The prospect's work email; the one-time code goes here. | `startProspectSignup` body |
| Locale `locale` | text field | optional | — | max length 16 | — | The language the code message is written in (BCP 47), default English. | `startProspectSignup` body |

**Sent by *Verify code*** (`verifyProspectSignupCode`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | pattern `^[0-9]{6}$` | — | The six-digit one-time code sent to the email. | `verifyProspectSignupCode` body |

**Sent by *Submit*** (`submitOnboardingApplication`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `submitOnboardingApplication` body |
| Company name `companyName` | text field | required | — | — | — | — | `submitOnboardingApplication` body |
| Contact email `contactEmail` | email field | required | — | — | name@example.ae | — | `submitOnboardingApplication` body |
| Contact phone `contactPhone` | phone field | optional | — | — | +971 5X XXX XXXX (E.164) | — | `submitOnboardingApplication` body |
| Country code `countryCode` | text field | optional | — | — | — | — | `submitOnboardingApplication` body |
| Venue type template `venueTypeTemplateId` | picker: choose a venue type template | optional | — | — | shows names, sends the id | A water park and a theatre need different defaults, and asking a prospect to configure 300 settings from empty is asking them to leave. | `submitOnboardingApplication` body |
| Requested plan `requestedPlanId` | picker: choose a requested plan | optional | — | — | shows names, sends the id | — | `submitOnboardingApplication` body |
| Status `status` | select | required | — | Submitted · Verifying · Approved · Provisioning · Active · Rejected · Abandoned | — | — | `submitOnboardingApplication` body |
| Trial ends at `trialEndsAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Trial is a state, not a plan. A tenant on trial has the plan they will pay for and a date by which they must — modelling it as a separate plan means migrating them at conversion … | `submitOnboardingApplication` body |
| Rejection reason `rejectionReason` | text field | optional | — | — | — | — | `submitOnboardingApplication` body |
| Provisioned tenant `provisionedTenantId` | picker: choose a provisioned tenant | optional | — | — | shows names, sends the id | — | `submitOnboardingApplication` body |
| Billing entity `billingEntity` | group | optional | — | — | — | The company to be invoiced, saved on the application before verification (Chinmay, 2 October, workbook Q209 and Q223; CHG-CSA-030). | `submitOnboardingApplication` body |
| Legal name `billingEntity.legalName` | text area | optional | — | max length 300 | — | — | `submitOnboardingApplication` body |
| Trade licence number `billingEntity.tradeLicenceNumber` | text field | optional | — | max length 100 | — | — | `submitOnboardingApplication` body |
| Trn `billingEntity.trn` | text field | optional | — | max length 30 | — | The tax registration number; entering one makes the VAT certificate required. | `submitOnboardingApplication` body |
| Country code `billingEntity.countryCode` | text field | optional | — | min length 2; max length 2 | — | — | `submitOnboardingApplication` body |
| Address `billingEntity.address` | text area | optional | — | max length 1000 | — | — | `submitOnboardingApplication` body |
| Invoice email `billingEntity.invoiceEmail` | email field | optional | — | — | name@example.ae | — | `submitOnboardingApplication` body |
| Documents `billingEntity.documents` | repeatable rows | optional | — | — | — | The trade licence and, where a TRN is entered, the VAT certificate, each a stored file with its verification. | `submitOnboardingApplication` body |
| Document type `billingEntity.documents[].documentType` | segmented control | optional | — | Trade licence · VAT certificate | — | — | `submitOnboardingApplication` body |
| File ref `billingEntity.documents[].fileRef` | text field | optional | — | — | — | — | `submitOnboardingApplication` body |
| Expiry date `billingEntity.documents[].expiryDate` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `submitOnboardingApplication` body |
| Verification status `billingEntity.documents[].verificationStatus` | radio group | optional | — | Missing · Uploaded · Verified · Rejected · Expired | — | — | `submitOnboardingApplication` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Send code (secondary button) | `startProspectSignup` POST `/auth/prospect/signup` | StartProspectSignupRequest | ProspectSignupChallenge | 400 Validation failed | produces a document or message: Start (or resume) a TICVAI sign-up with an email and a one-time code |
| Verify code (secondary button) | `verifyProspectSignupCode` POST `/auth/prospect/signup/{challengeId}/verify` | VerifyProspectSignupCodeRequest | ProspectSignupSession | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The challenge is spent (`codeExpired`) because the code expired, five wrong codes were tried or it was already … | produces a document or message: Prove the email with the one-time code and receive the prospect sign-up session |
| Submit (primary button) | `submitOnboardingApplication` POST `/onboarding-applications` | OnboardingApplication | OnboardingApplication | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `SGN-001` Welcome & Start Your TICVAI Journey: *Back to Welcome & Start Your TICVAI Journey*
- → `SGN-003` Venue Type & Business Profile: *Venue Type & Business Profile*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Not used: the form renders at once. |
| Error (`?state=error`) | The call that failed is named beside its button (code, verify or submit); what was typed stays. |
| Empty, first run (`?state=emptyFirstRun`) | No customer organization registration yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the customer organization registration are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `submitOnboardingApplication` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The challenge is spent (`codeExpired`) because the code expired, five wrong codes were tried or it was already used; start a new one with startProspectSignup; 422 The code is wrong (`codeInvalid`); it counts against the challenge |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
organisation:
  legalName: Marina Leisure Group LLC
  country: AE
  contact: Aisha Al Nuaimi
  email: aisha@marinaleisure.ae
  phone: +971 2 555 0142
```

#### Permissions

- `submitOnboardingApplication` → `TENANT_CONFIGURE` (configure) · public, prospect
- `startProspectSignup` → no permission · public, prospect
- `verifyProspectSignupCode` → no permission · public, prospect

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `submitOnboardingApplication` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

14 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.1.1 | Customer Registration - System shall support self-service customer registration. | Subscription & Licensing Management | CONTRACTED | data `OnboardingApplication` |
| 20.1.3 | AI Setup Wizard - System shall provide AI-assisted onboarding. | Subscription & Licensing Management | CONTRACTED | data `OnboardingApplication` |
| 20.1.4 | Venue Type Templates - System shall provide venue-specific setup templates. | Subscription & Licensing Management | CONTRACTED | data `OnboardingApplication` |
| 20.1.5 | Automatic Configuration - System shall automatically configure the platform based on onboarding selections. | Subscription & Licensing Management | CONTRACTED | data `OnboardingApplication` |
| 20.1.6 | Trial-to-Paid Conversion - System shall support conversion from trial to paid subscriptions. | Subscription & Licensing Management | CONTRACTED | data `OnboardingApplication` |
| 20.3.1 | Venue Size Index - System shall support licensing based on Venue Size Index. | Subscription & Licensing Management | CONTRACTED | data `OnboardingApplication` |
| 20.3.2 | POS-Based Licensing - System shall support licensing based on POS quantities. | Subscription & Licensing Management | CONTRACTED | data `OnboardingApplication` |
| 20.3.3 | User-Based Licensing - System shall support licensing based on active users. | Subscription & Licensing Management | CONTRACTED | data `OnboardingApplication` |
| 20.3.4 | Venue-Based Licensing - System shall support licensing based on number of venues. | Subscription & Licensing Management | CONTRACTED | data `OnboardingApplication` |
| 20.3.5 | Transaction-Based Licensing - System shall support licensing based on transaction volumes. | Subscription & Licensing Management | CONTRACTED | data `OnboardingApplication` |
| 20.3.6 | Attendance-Based Licensing - System shall support licensing based on attendance volumes. | Subscription & Licensing Management | CONTRACTED | data `OnboardingApplication` |
| 20.3.7 | Hybrid Licensing Models - System shall support hybrid licensing calculations. | Subscription & Licensing Management | CONTRACTED | data `OnboardingApplication` |
| … 2 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Onboarding starts from a link on the TICVAI website and walks a structured question set; first section is organisation details: venue name, industry, attraction type, currency, region/country, contact details, business type (private, semi-government, non-profit). *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-809)*

Also apply: 10 for all of P17, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P17 TICVAI Sign-up.dc.html#sgn-002` · status **notStarted** · provenance —
- Workshop pack:  board 2

#### Acceptance for the design

- [ ] Every input above is drawn (35), with its required mark, default, format and its error state (400, 404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SGN-002?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Send code, Verify code, Submit, Cancel.
- [ ] Every transition is wired: `SGN-001`, `SGN-003`.
- [ ] Every gated control is gated: `TENANT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SGN-003` Venue Type & Business Profile

**Understand what type of operation the customer runs.**

| | |
|---|---|
| App · platform | TICVAI Control · P17 TICVAI Sign-up (web) |
| Module | Onboarding & Assessment · wave 3 · needs the `core` module |
| Block | Block B · ticket #29377 (APP-SIGNUP-SGN-003) |
| Who uses it | public staff holding `PLATFORM_PLAN_MANAGE` (1 configure) |
| Device and orientation | This is a public marketing and sign-up web flow, 1440 desktop and 390 phone widths, in TICVAI's own brand. · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Visual cards) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/onboarding-assessment/venue-type-business-profile-sgn-003` |

**What the spec says about it.** The self-service form of `ADM-381`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step.

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The prospect's venue type and business profile (waterpark, museum, stadium...), multi-select.

**Known correction pending (do not draw the wrong version)**

- **The table's columns are the workshop pack's labels with no bound response field (0 of 12 labels bound).** Why: The operation returns no schema with described properties, so a developer cannot fill these columns and a designer cannot know their formats. The response schema needs the fields (or the columns go). *(source: screens/P17-ticvai-signup.yaml#SGN-003; Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management))*

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- A sign-up screen calls operations a prospect cannot call: scoreVsiAssessment (staff/guest). (CHG-SOT-016)

**Fixed on main** (the package already carries these; draw what it says): Venue types are drawn as table columns. (CHG-SBO-023); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue type | multi select | — | — | — | — | The venue types the prospect chooses from (Museum, Attraction, Theme Park, Waterpark, Stadium, Theatre, Exhibition / Event Venue, Zoo / Aquarium, Tour Operator, Entertainment Center, Multi-Venue … | — |

#### Outputs: what the screen shows and produces

**Shown**

**The selected venue type business** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Museum | text | not in the schema: `Museum` |
| Attraction | text | not in the schema: `Attraction` |
| Theme park | text | not in the schema: `Theme Park` |
| Waterpark | text | not in the schema: `Waterpark` |
| Stadium | text | not in the schema: `Stadium` |
| Theatre | text | not in the schema: `Theatre` |
| Exhibition / event venue | text | not in the schema: `Exhibition / Event Venue` |
| Zoo / aquarium | text | not in the schema: `Zoo / Aquarium` |
| Tour operator | text | not in the schema: `Tour Operator` |
| Entertainment center | text | not in the schema: `Entertainment Center` |
| Multi venue operator | text | not in the schema: `Multi-Venue Operator` |
| Other | text | not in the schema: `Other` |

**Where the user goes next**

- → `SGN-002` Customer & Organization Registration: *Back to Customer & Organization Registration*
- → `SGN-004` Visitor, Capacity & Operational Scale: *Visitor, Capacity & Operational Scale*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The venue type business list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the venue type business untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No venue type business yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the venue type business are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every venue type business:
- Museum: 57
  Attraction: 312
  Theme Park: 312
  Waterpark: 46
  Stadium: 11
  Theatre: 11
  Exhibition / Event Venue: 128
  Zoo / Aquarium: 57
- Museum: 11
  Attraction: 74
  Theme Park: 74
  Waterpark: 312
  Stadium: 128
  Theatre: 128
  Exhibition / Event Venue: 46
  Zoo / Aquarium: 11
- Museum: 128
  Attraction: 19
  Theme Park: 19
  Waterpark: 74
  Stadium: 46
  Theatre: 46
  Exhibition / Event Venue: 312
  Zoo / Aquarium: 128
```

#### Permissions

- `scoreVsiAssessment` → `PLATFORM_PLAN_MANAGE` (configure) · staff, guest, prospect

**A refused user sees:** TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.8.1 | AI Subscription Recommendations - System shall recommend optimal subscription plans. | Subscription & Licensing Management | CONTRACTED | `scoreVsiAssessment` |
| 20.8.2 | AI Module Recommendations - System shall recommend marketplace modules. | Subscription & Licensing Management | CONTRACTED | `scoreVsiAssessment` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Operating model question: attraction, museum, park, event, etc. *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-810)*

Also apply: 10 for all of P17, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P17 TICVAI Sign-up.dc.html#sgn-003` · status **notStarted** · provenance —
- Workshop pack:  board 2

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SGN-003?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `SGN-002`, `SGN-004`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SGN-004` Visitor, Capacity & Operational Scale

**Collect the information required to understand venue size and eventually calculate the VSI.**

| | |
|---|---|
| App · platform | TICVAI Control · P17 TICVAI Sign-up (web) |
| Module | Onboarding & Assessment · wave 3 · needs the `core` module |
| Block | Block B · ticket #29378 (APP-SIGNUP-SGN-004) |
| Who uses it | public staff holding `PLATFORM_PLAN_MANAGE` (1 configure) |
| Device and orientation | This is a public marketing and sign-up web flow, 1440 desktop and 390 phone widths, in TICVAI's own brand. · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/onboarding-assessment/visitor-capacity-operational-scale-sgn-004` |

**What the spec says about it.** The self-service form of `ADM-382`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Visitor numbers, capacity and operating scale, used to compute the venue size index.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- A sign-up screen calls operations a prospect cannot call: scoreVsiAssessment (staff/guest). (CHG-SOT-016)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `SGN-003` Venue Type & Business Profile: *Back to Venue Type & Business Profile*
- → `SGN-005` Sales Channel Assessment: *Sales Channel Assessment*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The visitor capacity operational list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the visitor capacity operational untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No visitor capacity operational yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the visitor capacity operational are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
annualVisitors: 1,200,000
peakDay: 18,000
venues: 3
operatingDays: 340
```

#### Permissions

- `scoreVsiAssessment` → `PLATFORM_PLAN_MANAGE` (configure) · staff, guest, prospect

**A refused user sees:** TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.8.1 | AI Subscription Recommendations - System shall recommend optimal subscription plans. | Subscription & Licensing Management | CONTRACTED | `scoreVsiAssessment` |
| 20.8.2 | AI Module Recommendations - System shall recommend marketplace modules. | Subscription & Licensing Management | CONTRACTED | `scoreVsiAssessment` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Visitor capacity and scale: expected annual/monthly visitors, venue capacity, entrances/exits, number of POS and access-control points, user count, estimated transaction volume, growth forecast. *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-811)*

Also apply: 10 for all of P17, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P17 TICVAI Sign-up.dc.html#sgn-004` · status **notStarted** · provenance —
- Workshop pack:  board 2

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SGN-004?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `SGN-003`, `SGN-005`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SGN-005` Sales Channel Assessment

**Understand how the customer intends to sell tickets and products.**

| | |
|---|---|
| App · platform | TICVAI Control · P17 TICVAI Sign-up (web) |
| Module | Onboarding & Assessment · wave 3 · needs the `core` module |
| Block | Block B · ticket #29379 (APP-SIGNUP-SGN-005) |
| Who uses it | public staff holding `PLATFORM_PLAN_MANAGE` (1 configure) |
| Device and orientation | This is a public marketing and sign-up web flow, 1440 desktop and 390 phone widths, in TICVAI's own brand. · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Selectable options) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/onboarding-assessment/sales-channel-assessment-sgn-005` |

**What the spec says about it.** The self-service form of `ADM-383`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-025): listSaleChannel reads a live tenant's configured channels, and a prospect has no cell and no channels; the assessment uses the answers only (scoreVsiAssessment) …

**From the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process.** The prospect's sales channels during self-service sign-up, each with a volume estimate. After Block A.

**Known correction pending (do not draw the wrong version)**

- **The channels are drawn as a mix of select and text fields labelled with checkbox characters.** Why: They are checkboxes with a number each. *(source: screens/P17-ticvai-signup.yaml#SGN-005 layout; Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| ☐ On-site POS | select field | — | — | — | — | — | — |
| ☐ Own Website / B2C | text field | — | — | — | — | — | — |
| ☐ Mobile App | select field | — | — | — | — | — | — |
| ☐ Tour Operators | select field | — | — | — | — | — | — |
| ☐ Hotels | select field | — | — | — | — | — | — |
| ☐ Resellers | select field | — | — | — | — | — | — |
| ☐ Corporate Customers | select field | — | — | — | — | — | — |
| ☐ Call Center | select field | — | — | — | — | — | — |
| ☐ Kiosk | select field | — | — | — | — | — | — |
| ☐ Flying / Mobile POS | text field | — | — | — | — | — | — |
| ☐ OTA / Third-Party Channels | text field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **channels**: Checkboxes (On-site POS, Own website, Mobile app, Tour operators, Hotels, Resellers, Corporate, Call centre, Kiosk, Flying POS, OTA) each with an annual volume estimate. *(source: DI-812)*

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `SGN-004` Visitor, Capacity & Operational Scale: *Back to Visitor, Capacity & Operational Scale*
- → `SGN-006` Ticketing & Product Requirements: *Ticketing & Product Requirements*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The sales channel assessment configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the sales channel assessment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No sales channel assessment configured yet. Offers no create action — this screen declares no operation that makes one and says what the platform does in the meantime. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Permission denied (`?state=emptyNoAccess`) | TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
channels:
- On-site POS · 300,000 tickets/yr
- Own website · 450,000
- Kiosk · 60,000
```

#### Permissions

- `scoreVsiAssessment` → `PLATFORM_PLAN_MANAGE` (configure) · staff, guest, prospect

**A refused user sees:** TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.8.1 | AI Subscription Recommendations - System shall recommend optimal subscription plans. | Subscription & Licensing Management | CONTRACTED | `scoreVsiAssessment` |
| 20.8.2 | AI Module Recommendations - System shall recommend marketplace modules. | Subscription & Licensing Management | CONTRACTED | `scoreVsiAssessment` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Sales channels of interest (online, on-site, B2C, B2B/OTA) each with volume estimates. *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-812)*

Also apply: 10 for all of P17, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P17 TICVAI Sign-up.dc.html#sgn-005` · status **notStarted** · provenance —
- Workshop pack:  board 2

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SGN-005?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `SGN-004`, `SGN-006`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SGN-006` Ticketing & Product Requirements

**Understand what the venue intends to sell.**

| | |
|---|---|
| App · platform | TICVAI Control · P17 TICVAI Sign-up (web) |
| Module | Onboarding & Assessment · wave 3 · needs the `core` module |
| Block | Block B · ticket #29380 (APP-SIGNUP-SGN-006) |
| Who uses it | public staff holding `PLATFORM_PLAN_MANAGE` (1 configure) |
| Device and orientation | This is a public marketing and sign-up web flow, 1440 desktop and 390 phone widths, in TICVAI's own brand. · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Selectable options) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/onboarding-assessment/ticketing-product-requirements-sgn-006` |

**What the spec says about it.** The self-service form of `ADM-384`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** What the venue intends to sell (admission types, passes, vouchers, bundles, events).

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- A sign-up screen calls operations a prospect cannot call: scoreVsiAssessment (staff/guest). (CHG-SOT-016)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| General Admission | select field | — | — | — | — | — | — |
| Dated Admission | select field | — | — | — | — | — | — |
| Timeslot Admission | select field | — | — | — | — | — | — |
| Open-Dated Ticket | select field | — | — | — | — | — | — |
| Multi-Day Ticket | select field | — | — | — | — | — | — |
| Family Ticket | select field | — | — | — | — | — | — |
| Group Ticket | select field | — | — | — | — | — | — |
| Membership | select field | — | — | — | — | — | — |
| Annual Pass | select field | — | — | — | — | — | — |
| Season Pass | select field | — | — | — | — | — | — |
| Voucher | select field | — | — | — | — | — | — |
| Bundle | select field | — | — | — | — | — | — |
| Add-On | select field | — | — | — | — | — | — |
| Camp / Course | select field | — | — | — | — | — | — |
| Special Event | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `SGN-005` Sales Channel Assessment: *Back to Sales Channel Assessment*
- → `SGN-007` Access, Queue & Visitor Experience Assessment: *Access, Queue & Visitor Experience Assessment*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The ticketing product requirements configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the ticketing product requirements untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No ticketing product requirements configured yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
form example:
  General Admission: 46
  Dated Admission: 128
  Timeslot Admission: 1.8 s
  Open-Dated Ticket: 19
  Multi-Day Ticket: 19
  Family Ticket: 312
  Group Ticket: 312
  Membership: 46
  Annual Pass: 74
  Season Pass: 19
  Voucher: 46
  Bundle: 46
  Add-On: 312
  Camp / Course: 312
```

#### Permissions

- `scoreVsiAssessment` → `PLATFORM_PLAN_MANAGE` (configure) · staff, guest, prospect

**A refused user sees:** TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.8.1 | AI Subscription Recommendations - System shall recommend optimal subscription plans. | Subscription & Licensing Management | CONTRACTED | `scoreVsiAssessment` |
| 20.8.2 | AI Module Recommendations - System shall recommend marketplace modules. | Subscription & Licensing Management | CONTRACTED | `scoreVsiAssessment` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Product/module types they plan to sell: general admission, seat-based, resource management, events, memberships, wallet, etc.; plus guest access/validation methods. *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-813)*

Also apply: 10 for all of P17, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P17 TICVAI Sign-up.dc.html#sgn-006` · status **notStarted** · provenance —
- Workshop pack:  board 2

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SGN-006?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `SGN-005`, `SGN-007`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SGN-007` Access, Queue & Visitor Experience Assessment

**Determine admission and visitor-flow requirements.**

| | |
|---|---|
| App · platform | TICVAI Control · P17 TICVAI Sign-up (web) |
| Module | Onboarding & Assessment · wave 3 · needs the `core` module |
| Block | Block B · ticket #29381 (APP-SIGNUP-SGN-007) |
| Who uses it | public staff holding `PLATFORM_PLAN_MANAGE` (1 configure) |
| Device and orientation | This is a public marketing and sign-up web flow, 1440 desktop and 390 phone widths, in TICVAI's own brand. · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/onboarding-assessment/access-queue-visitor-experience-assessment-sgn-007` |

**What the spec says about it.** The self-service form of `ADM-385`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Admission, queue and visitor-flow needs.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- A sign-up screen calls operations a prospect cannot call: scoreVsiAssessment (staff/guest). (CHG-SOT-016)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `SGN-006` Ticketing & Product Requirements: *Back to Ticketing & Product Requirements*
- → `SGN-008` Additional Business Module Assessment: *Additional Business Module Assessment*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The access queue visitor list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the access queue visitor untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No access queue visitor yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the access queue visitor are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
gates: 14
admissionMedia:
- QR
- RFID wristband
virtualQueue: true
```

#### Permissions

- `scoreVsiAssessment` → `PLATFORM_PLAN_MANAGE` (configure) · staff, guest, prospect

**A refused user sees:** TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.8.1 | AI Subscription Recommendations - System shall recommend optimal subscription plans. | Subscription & Licensing Management | CONTRACTED | `scoreVsiAssessment` |
| 20.8.2 | AI Module Recommendations - System shall recommend marketplace modules. | Subscription & Licensing Management | CONTRACTED | `scoreVsiAssessment` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Product/module types they plan to sell: general admission, seat-based, resource management, events, memberships, wallet, etc.; plus guest access/validation methods. *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-813)*

Also apply: 10 for all of P17, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'wait-time')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A244** Build virtual queue with 3 guest tiers (walk-in, VQ, VIP); keep VQ separate from VIP lane *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A245** Recalculate virtual queue return times live, not fixed at booking *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A246** Support virtual queue via app (theme parks) and kiosk/wristband scan (water parks) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A247** Build virtual queue ops dashboard, AI guest-flow tips and fast-lane upsell on long waits *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*

#### References

- Wireframe frame: `wireframes/P17 TICVAI Sign-up.dc.html#sgn-007` · status **notStarted** · provenance —
- Workshop pack:  board 2

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SGN-007?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `SGN-006`, `SGN-008`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SGN-008` Additional Business Module Assessment

**Identify additional TICVAI operational modules based on the customer's business.**

| | |
|---|---|
| App · platform | TICVAI Control · P17 TICVAI Sign-up (web) |
| Module | Onboarding & Assessment · wave 3 · needs the `core` module |
| Block | Block B · ticket #29382 (APP-SIGNUP-SGN-008) |
| Who uses it | public staff holding `PLATFORM_PLAN_MANAGE` (1 configure) |
| Device and orientation | This is a public marketing and sign-up web flow, 1440 desktop and 390 phone widths, in TICVAI's own brand. · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/onboarding-assessment/additional-business-module-assessment-sgn-008` |

**What the spec says about it.** The self-service form of `ADM-386`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Additional modules the business needs, suggested from earlier answers.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- A sign-up screen calls operations a prospect cannot call: listModuleCatalogue (staff/guest), scoreVsiAssessment (staff/guest). (CHG-SOT-016)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listModuleCatalogue` (onLoad, Additional modules)

**Where the user goes next**

- → `SGN-007` Access, Queue & Visitor Experience Assessment: *Back to Access, Queue & Visitor Experience Assessment*
- → `SGN-009` Integration, Payment & Technical Readiness: *Integration, Payment & Technical Readiness*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The additional business module list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the additional business module untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No additional business module yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the additional business module are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listModuleCatalogue (ModuleListing):
- name: Growth plan
  description: Guest charged twice at Main Gate Till 3
  price: AED 1,250.00
- name: AquaCove Annual Pass Gold
  description: Group of 40 from Desert Gate Tours
  price: AED 48,000.00
```

#### Permissions

- `listModuleCatalogue` → `PLATFORM_PLAN_MANAGE` (configure) · staff, guest, prospect
- `scoreVsiAssessment` → `PLATFORM_PLAN_MANAGE` (configure) · staff, guest, prospect

**A refused user sees:** TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.8.1 | AI Subscription Recommendations - System shall recommend optimal subscription plans. | Subscription & Licensing Management | CONTRACTED | `scoreVsiAssessment` |
| 20.8.2 | AI Module Recommendations - System shall recommend marketplace modules. | Subscription & Licensing Management | CONTRACTED | `scoreVsiAssessment` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Additional modules needed (F&B, retail, membership/CRM, etc.). *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-814)*

Also apply: 10 for all of P17, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P17 TICVAI Sign-up.dc.html#sgn-008` · status **notStarted** · provenance —
- Workshop pack:  board 2

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SGN-008?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `SGN-007`, `SGN-009`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SGN-009` Integration, Payment & Technical Readiness

**Understand external systems and technical requirements that could affect complexity, implementation approach and commercial scope.**

| | |
|---|---|
| App · platform | TICVAI Control · P17 TICVAI Sign-up (web) |
| Module | Onboarding & Assessment · wave 3 · needs the `core` module |
| Block | Block B · ticket #29383 (APP-SIGNUP-SGN-009) |
| Who uses it | public staff holding `PLATFORM_PLAN_MANAGE` (1 configure) |
| Device and orientation | This is a public marketing and sign-up web flow, 1440 desktop and 390 phone widths, in TICVAI's own brand. · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/onboarding-assessment/integration-payment-technical-readiness-sgn-009` |

**What the spec says about it.** The self-service form of `ADM-387`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** External systems, payment providers and technical constraints affecting scope.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- A sign-up screen calls operations a prospect cannot call: scoreVsiAssessment (staff/guest). (CHG-SOT-016)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `SGN-008` Additional Business Module Assessment: *Back to Additional Business Module Assessment*
- → `SGN-010` AI Assessment Summary & Handoff: *AI Assessment Summary & Handoff*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The integration payment technical list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the integration payment technical untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No integration payment technical yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the integration payment technical are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
paymentProvider: Network International
erp: SAP S/4HANA
existingTicketing: replace
```

#### Permissions

- `scoreVsiAssessment` → `PLATFORM_PLAN_MANAGE` (configure) · staff, guest, prospect

**A refused user sees:** TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.8.1 | AI Subscription Recommendations - System shall recommend optimal subscription plans. | Subscription & Licensing Management | CONTRACTED | `scoreVsiAssessment` |
| 20.8.2 | AI Module Recommendations - System shall recommend marketplace modules. | Subscription & Licensing Management | CONTRACTED | `scoreVsiAssessment` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Payment gateway/device integration needs: select from a supported list or specify an unlisted provider. *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-815)*

Also apply: 10 for all of P17, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P17 TICVAI Sign-up.dc.html#sgn-009` · status **notStarted** · provenance —
- Workshop pack:  board 2

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SGN-009?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `SGN-008`, `SGN-010`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SGN-010` AI Assessment Summary & Handoff

**Consolidate everything learned during onboarding and prepare the customer for Board 3/4 commercial recommendation.**

| | |
|---|---|
| App · platform | TICVAI Control · P17 TICVAI Sign-up (web) |
| Module | Onboarding & Assessment · wave 3 · needs the `core` module |
| Block | Block B · ticket #29384 (APP-SIGNUP-SGN-010) |
| Who uses it | public staff holding `PLATFORM_PLAN_MANAGE` (1 configure) |
| Device and orientation | This is a public marketing and sign-up web flow, 1440 desktop and 390 phone widths, in TICVAI's own brand. · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/onboarding-assessment/ai-assessment-summary-handoff-sgn-010` |

**What the spec says about it.** The self-service form of `ADM-388`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The assessment summarised for the prospect before the recommendation; editable answers.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- A sign-up screen calls operations a prospect cannot call: scoreVsiAssessment (staff/guest). (CHG-SOT-016)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `SGN-009` Integration, Payment & Technical Readiness: *Back to Integration, Payment & Technical Readiness*
- → `SGN-011` Recommended Package Overview: *Recommended Package Overview*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The assessment summary handoff list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the assessment summary handoff untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No assessment summary handoff yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the assessment summary handoff are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
venueType: Waterpark
vsi: 68
modulesNeeded:
- ticketing
- pos
- fnb
- access
- membership
```

#### Permissions

- `scoreVsiAssessment` → `PLATFORM_PLAN_MANAGE` (configure) · staff, guest, prospect

**A refused user sees:** TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.8.1 | AI Subscription Recommendations - System shall recommend optimal subscription plans. | Subscription & Licensing Management | CONTRACTED | `scoreVsiAssessment` |
| 20.8.2 | AI Module Recommendations - System shall recommend marketplace modules. | Subscription & Licensing Management | CONTRACTED | `scoreVsiAssessment` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The prospect reviews then submits the assessment, which becomes the basis for the system's proposed commercial/licensing model. *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-816)*

Also apply: 10 for all of P17, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P17 TICVAI Sign-up.dc.html#sgn-010` · status **notStarted** · provenance —
- Workshop pack:  board 2

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SGN-010?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `SGN-009`, `SGN-011`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P17 reference designs** (from `handoff/design-batches/apps/6-ticvai-controller/README.md`)

- `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html`: the newest client-approved public look, for finish.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-040, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

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

### Across P17 TICVAI Sign-up

- The TICVAI marketing site should showcase demo versions of each platform (POS, kiosk, mobile app, menu management). *(client request · MoM 29 Sep 2026, 3. B2B / reseller portal · DI-1024)*
- Small/medium venues (e.g. 2 POS, 2 access points, basic B2C site) see pricing, subscribe and start configuring within a few days with no sales involvement; large/enterprise prospects stay sales-assisted (demo, consultative scoping) and enterprise-tier pricing is not exposed through self-service. *(agreed · MoM 10 Sep 2026, 4.9 Sales-Assisted vs. Self-Service Segmentation Philosophy · DI-829)*
- On top of the trade-license review, the applicant confirms access to the submitted domain email (link or OTP, 2FA-style) before portal access. *(agreed · MoM 10 Sep 2026, 4.8 Customer Portal Access, Authentication & Verification · DI-828)*
- Portal access exposes TICVAI pricing, so prospects submit contact details and a trade license as proof of a real venue, reviewed and approved by TICVAI before access is granted. *(agreed · MoM 10 Sep 2026, 4.8 Customer Portal Access, Authentication & Verification · DI-827)*
- Gap (Allam): screens don't show how a prospect logs into a secure portal to view their proposed package; account credentials (user ID and password) are created once onboarding is submitted so the prospect can access and track the proposal. *(client request · MoM 10 Sep 2026, 4.7 Package Builder & Module Marketplace · DI-826)*
- Prospect onboarding: a short questionnaire (venue type, user count, expected annual visitors, modules such as B2C, B2B, seat assignment) via a website/AI-assisted flow; small/medium venues auto-classified and self-configure via AI-assisted setup; enterprise routed to a sales-assisted demo. *(client request · MoM 9 Sep 2026, 4.19 Licensing & Subscription Model - Preliminary Concept · DI-807)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Small-customer self-service subscription flow: select required modules, pay online, enter venue and business details, environment is provisioned automatically, then the customer configures products, tickets, users and venue information and starts using the system. *(client request · MoM 28 Jul 2026, 6. Two Deployment and Commercial Models · DI-011)*

**10 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"listModuleCatalogue": {"method":"GET","path":"/module-catalogue","contract":"subscription","summary":"Modules, their dependencies and their commercial treatment","permission":"PLATFORM_PLAN_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"platform","parameters":[],"requestBody":null,"responds":"ModuleListing"},
"scoreVsiAssessment": {"method":"POST","path":"/vsi-assessments","contract":"subscription","summary":"Score a prospect's answers into a tier and a package","permission":"PLATFORM_PLAN_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"platform","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VsiAssessment","responds":"VsiResult"},
"startProspectSignup": {"method":"POST","path":"/auth/prospect/signup","contract":"identity","summary":"Start (or resume) a TICVAI sign-up with an email and a one-time code","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"platform","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"StartProspectSignupRequest","responds":"ProspectSignupChallenge"},
"submitOnboardingApplication": {"method":"POST","path":"/onboarding-applications","contract":"subscription","summary":"A prospect signs themselves up","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"OnboardingApplication","responds":"OnboardingApplication"},
"verifyProspectSignupCode": {"method":"POST","path":"/auth/prospect/signup/{challengeId}/verify","contract":"identity","summary":"Prove the email with the one-time code and receive the prospect sign-up session","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"platform","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VerifyProspectSignupCodeRequest","responds":"ProspectSignupSession"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"BillingEntity": {"type":"object","x-ticvai-persistence":"control.billing_entity","description":"**The company TICVAI invoices for a tenant, with its trade licence and VAT certificate** (Chinmay, 2 October, workbook Q209: \"a new billing-entity record in the subscription contract\"; DI-830; CHG-CSA-030). One per tenant, mastered in the control plane. `legalName` and `countryCode` are required on save (400 otherwise); they are not marked required here so the record can ride, optional, on an onboarding application. **Documents** (workbook Q210, the default): a trade licence always; a VAT certificate when a `trn` is entered. Which documents a country requires is configurable per country (tenancy `RegionSettings`); the default is that rule.","properties":{"id":{"type":"string","format":"uuid","readOnly":true},"tenantId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Null while it rides on an onboarding application."},"legalName":{"type":"string","maxLength":300},"tradeLicenceNumber":{"type":"string","maxLength":100,"nullable":true},"trn":{"type":"string","maxLength":30,"nullable":true,"description":"The tax registration number; entering one makes the VAT certificate required."},"countryCode":{"type":"string","minLength":2,"maxLength":2},"address":{"type":"string","maxLength":1000,"nullable":true},"invoiceEmail":{"type":"string","format":"email","nullable":true},"documents":{"x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","type":"array","description":"The trade licence and, where a TRN is entered, the VAT certificate, each a stored file with its verification.","items":{"type":"object","properties":{"documentType":{"type":"string","enum":["tradeLicence","vatCertificate"]},"fileRef":{"type":"string","nullable":true},"expiryDate":{"type":"string","format":"date","nullable":true},"verificationStatus":{"type":"string","enum":["missing","uploaded","verified","rejected","expired"]}}}},"missingDocuments":{"type":"array","readOnly":true,"description":"The documents the country's rule requires that are not yet uploaded and verified.","items":{"type":"string"}},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"ModuleListing": {"type":"object","x-ticvai-persistence":"subscription.module_listing","description":"Board 4.6. **A marketplace without a dependency graph sells combinations that cannot be provisioned.**\n**TICVAI configures each module's price here, and tenants are billed per module (decided 29 September, Chinmay).** A usage-priced module (the AI module's tokens) has `pricingBasis` `metered`: `price` is then per `meteredUnitSize` units of `meteredMetric`, and the invoice carries it as a `metered` line.\n","required":["moduleCode"],"properties":{"moduleCode":{"type":"string","description":"**Values are `ModuleKey`s** (4 October 2026, CHG-FXC-010; ADM-424): the vocabulary of\n`white-label.ModuleEnablement.moduleKey`, so a dependency is checked against what `setModuleEnablement` switches."},"name":{"type":"string"},"description":{"type":"string","nullable":true},"category":{"type":"string","nullable":true},"requiresModules":{"type":"array","description":"**Values are `ModuleKey`s** (4 October 2026, CHG-FXC-010; ADM-424): the vocabulary of\n`white-label.ModuleEnablement.moduleKey`, so a dependency is checked against what `setModuleEnablement` switches.","items":{"type":"string"}},"incompatibleWithModules":{"type":"array","description":"**Values are `ModuleKey`s** (4 October 2026, CHG-FXC-010; ADM-424): the vocabulary of\n`white-label.ModuleEnablement.moduleKey`, so a dependency is checked against what `setModuleEnablement` switches.","items":{"type":"string"}},"includedInTiers":{"type":"array","items":{"type":"string"}},"price":{"x-ticvai-column":"list_price","$ref":"../shared/common.yaml#/components/schemas/Money"},"pricingBasis":{"type":"string","enum":["included","flatFee","perVenue","perUnit","revenueShare","metered"]},"meteredMetric":{"allOf":[{"$ref":"#/components/schemas/UsageMetric"}],"nullable":true,"description":"For `metered`, what is counted (`aiTokens` for the AI module). Null otherwise."},"meteredUnitSize":{"type":"integer","minimum":1,"nullable":true,"description":"For `metered`, how many units `price` buys (e.g. 1000 tokens). Null otherwise."},"provisioningMinutes":{"type":"integer","nullable":true},"requiresProfessionalServices":{"type":"boolean","default":false},"status":{"type":"string","enum":["available","beta","deprecated","withdrawn"]}}},
"OnboardingApplication": {"type":"object","x-ticvai-persistence":"control.onboarding_application","description":"BL-165. **`subscription` handles the operator-led path well and has no prospect-led one.** `createTenant` and `provisionCell` assume somebody at Softlabs decided this tenant exists.\nA prospect signing themselves up is a different shape: **nothing is provisioned until they are verified**, because an unverified application that provisions a cell is a cell somebody has to clean up.\n","required":["id","companyName","contactEmail","status"],"properties":{"id":{"type":"string","format":"uuid"},"companyName":{"type":"string"},"contactEmail":{"type":"string","format":"email"},"contactPhone":{"type":"string","nullable":true},"countryCode":{"type":"string"},"venueTypeTemplateId":{"type":"string","format":"uuid","nullable":true,"description":"**A water park and a theatre need different defaults**, and asking a prospect to configure 300 settings from empty is asking them to leave.\n"},"requestedPlanId":{"type":"string","format":"uuid"},"status":{"type":"string","enum":["submitted","verifying","approved","provisioning","active","rejected","abandoned"]},"trialEndsAt":{"type":"string","format":"date-time","nullable":true,"description":"**Trial is a state, not a plan.** A tenant on trial has the plan they will pay for and a date by which they must — modelling it as a separate plan means migrating them at conversion, which is the moment least worth adding risk to.\n"},"rejectionReason":{"type":"string","nullable":true},"provisionedTenantId":{"type":"string","format":"uuid","nullable":true},"billingEntity":{"$ref":"#/components/schemas/BillingEntity","description":"**The company to be invoiced, saved on the application before verification** (Chinmay, 2 October, workbook Q209 and Q223; CHG-CSA-030). Nothing is provisioned until the application is verified; on provisioning it becomes the tenant's billing entity (`getBillingEntity`)."}}},
"ProspectSignupChallenge": {"type":"object","x-ticvai-persistence":"none — the challenge is held by identity for its lifetime (CHG-CLN-019)","required":["challengeId","expiresInSeconds"],"properties":{"challengeId":{"type":"string","format":"uuid"},"expiresInSeconds":{"type":"integer"},"resendAfterSeconds":{"type":"integer"}}},
"ProspectSignupSession": {"type":"object","x-ticvai-persistence":"none — a session token, not a table the package reads (CHG-CLN-019)","required":["token","expiresAt","resumed"],"properties":{"token":{"type":"string","description":"The `prospectAuth` bearer token, scoped to one onboarding application."},"expiresAt":{"type":"string","format":"date-time"},"onboardingApplicationId":{"type":"string","format":"uuid","nullable":true,"description":"The application in progress for this email, or null until the first `submitOnboardingApplication`."},"resumed":{"type":"boolean","description":"True when the email already had an application in progress (\"Continue saved setup\")."}}},
"StartProspectSignupRequest": {"type":"object","x-ticvai-persistence":"none — request only (DEC-167; CHG-CLN-019)","required":["email"],"properties":{"email":{"type":"string","format":"email","maxLength":256,"description":"The prospect's work email; the one-time code goes here."},"locale":{"type":"string","maxLength":16,"nullable":true,"description":"The language the code message is written in (BCP 47), default English."}}},
"UsageMetric": {"type":"string","enum":["venues","workstations","activeUsers","devices","brandedApps","aiTokens","apiCalls","storageGb","transactions","guestProfiles"]},
"VerifyProspectSignupCodeRequest": {"type":"object","x-ticvai-persistence":"none — request only (CHG-CLN-019)","required":["code"],"properties":{"code":{"type":"string","pattern":"^[0-9]{6}$","description":"The six-digit one-time code sent to the email."}}},
"VsiAssessment": {"type":"object","x-ticvai-persistence":"subscription.vsi_assessment","description":"Board 2 — the ten-screen questionnaire, as data.","properties":{"id":{"type":"string","format":"uuid"},"organisationName":{"type":"string","nullable":true},"contactEmail":{"type":"string","nullable":true},"venueType":{"type":"string","nullable":true},"answers":{"type":"object","additionalProperties":true},"requestedModules":{"type":"array","items":{"type":"string"}},"submittedAt":{"type":"string","format":"date-time","nullable":true}}},
"VsiResult": {"type":"object","description":"Board 2.10. **A prospect told only their price has been told nothing they can argue with.**\n","properties":{"assessmentId":{"type":"string","format":"uuid"},"score":{"type":"number"},"tierCode":{"type":"string"},"tierName":{"type":"string"},"factors":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string"},"label":{"type":"string"},"answer":{"type":"string"},"points":{"type":"number"}}}},"recommendedModules":{"type":"array","items":{"type":"string"}},"recommendedPlanId":{"type":"string","format":"uuid","nullable":true},"indicativePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}
}
```
