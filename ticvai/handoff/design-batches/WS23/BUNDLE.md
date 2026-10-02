# WS23 — B2B, Reseller & OTA Partner Management board 3

**8 screens · 12 operations · 18 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `CASE_MANAGE, ORDER_MODIFY, PLATFORM_TENANT_VIEW`. A control nobody can use must say so,
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


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `PTR-042` | Partner Operations Command Center | B–D | 2 | 28 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `PTR-043` | Partner Orders & Booking Management | B–D | 2 | 32 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `PTR-044` | Reservations, Holds & Release Management | B–D | 0 | 160 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `PTR-045` | Partner Cancellations, Refunds & Amendments | B–D | 8 | 0 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `PTR-046` | Partner Statement & Account Activity | B–D | 0 | 18 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `PTR-049` | Partner Disputes, Cases & Service Management | B–D | 21 | 8 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `PTR-050` | Partner Performance Scorecard & Risk Monitoring | B–D | 0 | 2 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `PTR-051` | Partner AI Intelligence & Relationship Optimization | B–D | 0 | 2 | 6 | 0 | 1 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**PTR-045, PTR-050, PTR-051 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `PTR-042` Partner Operations Command Center

**Provide commercial, operations and finance teams with one real-time view of active B2B, reseller and OTA business.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner staff holding `PLATFORM_TENANT_VIEW` (1 read); in the flows as partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each partner should show) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/partners/partner-operations-command-center-ptr-042` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Partner business today: sales, orders, holds, cancellations, receivables, commission payable, exceptions.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SOT-015).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search partner operations | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by partner, partner type, venue, event, market, account manager and 4 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Venue | text field | — | — | `listPartner2` ?venue |
| Event | text field | — | — | `listPartner2` ?event |
| Market | text field | — | — | `listPartner2` ?market |
| Channel | select | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | `listPartner2` ?channel |
| From | date picker | — | — | `listPartner2` ?from |
| To | date picker | — | — | `listPartner2` ?to |
| Partner | picker: choose a partner | — | — | `listPartner2` ?partnerId |
| Partner type | text field | — | — | `listPartner2` ?partnerType |
| Account manager | text field | — | — | `listPartner2` ?accountManager |
| Operational status | radio group | — | Normal · Attention · Restricted · Suspended | `listPartner2` ?operationalStatus |
| Risk | radio group | — | Low · Medium · High · Critical | `listPartner2` ?risk |
| Brand | text field | — | — | `listPartner` ?brand |
| Venue | text field | — | — | `listPartner` ?venue |
| Account manager | text field | — | — | `listPartner` ?accountManager |
| Status | select | — | Lead · Applicant · Under review · Approved · Configuration · Active · Restricted · Suspended · Terminated · Archived | `listPartner` ?status |
| Risk | radio group | — | Low · Medium · High · Critical | `listPartner` ?risk |
| … 7 more | | | | `operations.json` |

#### Outputs: what the screen shows and produces

**Shown**

**Partner Sales Today** (metric tile)

**Partner Sales MTD** (metric tile)

**Active Partner Orders** (metric tile)

**Active Reservations/Holds** (metric tile)

**Tickets Sold** (metric tile)

**Cancellations** (metric tile)

**Refunds** (metric tile)

**Outstanding Receivables** (metric tile)

**Commission Payable** (metric tile)

**Pending Settlements** (metric tile)

**Operational Exceptions** (metric tile)

**Partners Requiring Attention** (metric tile)

**Every partner operations** (data table, from `listPartner2`)

| Shows | Format | Notes |
|---|---|---|
| Partner | text | Partner trading name |
| Partner type | text | Partner Type code |
| Account manager | text | Account Manager |
| Orders | 1,234 | Orders |
| Tickets | 1,234 | Tickets |
| Gross sales | AED 1,234.50 | Gross Sales |
| Net sales | AED 1,234.50 | Net Sales |
| Commission | AED 1,234.50 | Commission |
| Outstanding balance | AED 1,234.50 | Outstanding Balance |
| Credit utilization | 1,234.5 | Credit Utilization, percent |
| Allocation utilization | 1,234.5 | Allocation Utilization, percent |
| Cancellation rate | 12.5% | Cancellation Rate, percent |
| Operational status | text | Operational Status: normal, attention, restricted, suspended |
| Risk | chip: Low, Medium, High, Critical | Risk |

**The selected partner operations** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Partner | text | Partner trading name |
| Partner type | text | Partner Type code |
| Account manager | text | Account Manager |
| Orders | 1,234 | Orders |
| Tickets | 1,234 | Tickets |
| Gross sales | AED 1,234.50 | Gross Sales |
| Net sales | AED 1,234.50 | Net Sales |
| Commission | AED 1,234.50 | Commission |
| Outstanding balance | AED 1,234.50 | Outstanding Balance |
| Credit utilization | 1,234.5 | Credit Utilization, percent |
| Allocation utilization | 1,234.5 | Allocation Utilization, percent |
| Cancellation rate | 12.5% | Cancellation Rate, percent |
| Operational status | text | Operational Status: normal, attention, restricted, suspended |
| Risk | chip: Low, Medium, High, Critical | Risk |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Money columns (commission, outstandingBalance)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. Across tenants or regions figures in different currencies are never summed into one total; group by currency, or label the converted figure with its rate and time. *(source: ADR-0008; ADR-0011; DI-306)*

**Data it reads**: `listPartner2` (onLoad, Partner Operations Command Center); `listPartner` (onLoad, Partner Management Command Center)

**Where the user goes next**

- → `PTR-043` Partner Orders & Booking Management: *Works in Partner Orders & Booking Management*; calls `listPartner2`
- → `PTR-044` Reservations, Holds & Release Management: *Works in Reservations, Holds & Release Management*; calls `listPartner2`
- → `PTR-045` Partner Cancellations, Refunds & Amendments: *Works in Partner Cancellations, Refunds & Amendments*; calls `listPartner2`
- → `PTR-046` Partner Statement & Account Activity: *Works in Partner Statement & Account Activity*; calls `listPartner2`
- → `PTR-049` Partner Disputes, Cases & Service Management: *Works in Partner Disputes, Cases & Service Management*; calls `listPartner2`
- → `PTR-050` Partner Performance Scorecard & Risk Monitoring: *Works in Partner Performance Scorecard & Risk Monitoring*; calls `listPartner2`
- → `PTR-051` Partner AI Intelligence & Relationship Optimization: *Works in Partner AI Intelligence & Relationship Optimization*; calls `listPartner2`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The partner operations list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partner operations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No partner activity yet today. Offers no create action; the tiles show zero sales, not missing data. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the partner operations are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
metric tiles:
  Partner Sales Today: 128
  Partner Sales MTD: 46
  Active Partner Orders: 312
  Active Reservations/Holds: 74
  Tickets Sold: 19
  Cancellations: 233
  Refunds: 57
  Outstanding Receivables: AED 96,750.00
  Commission Payable: AED 12,400.00
  Pending Settlements: 46
```

#### Permissions

- `listPartner2` → `PLATFORM_TENANT_VIEW` (read) · partner
- `listPartner` → `PLATFORM_TENANT_VIEW` (read) · partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Operations dashboard per partner: order volume, revenue, reservations and tickets on hold (booked but not yet issued). Cancellations/refund requests, statement of account (opening/closing balance, activity), reconciliation exceptions and disputes are tracked from this view. *(client request · MoM 31 Aug 2026, 4.5 B2B Day-to-Day Operations & Settlement · DI-557)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-042` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS40 B2B, Reseller & OTA Partner Management Board 3.dc.html#ptr-042`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 3
- Flow F132 *B2B, Reseller & OTA Partner Management board 3: Partner Operations Command …*, step 1: Opens Partner Operations Command Center → Provide commercial, operations and finance teams with one real-time view of active B2B, reseller and OTA business.
- Flow F132 *B2B, Reseller & OTA Partner Management board 3: Partner Operations Command …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F132 *B2B, Reseller & OTA Partner Management board 3: Partner Operations Command …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F132 *B2B, Reseller & OTA Partner Management board 3: Partner Operations Command …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F132 *B2B, Reseller & OTA Partner Management board 3: Partner Operations Command …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F132 *B2B, Reseller & OTA Partner Management board 3: Partner Operations Command …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F132 *B2B, Reseller & OTA Partner Management board 3: Partner Operations Command …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F132 branch at step 1 (expected): when Nothing has been set up on Partner Operations Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F132 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (28 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-042?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `PTR-043`, `PTR-044`, `PTR-045`, `PTR-046`, `PTR-049`, `PTR-050`, `PTR-051`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-043` Partner Orders & Booking Management

**Provide a consolidated operational view of orders created by each partner.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner staff holding `PLATFORM_TENANT_VIEW` (1 read); in the flows as partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/partners/partner-orders-booking-management-ptr-043` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Orders created by partners with their references, agent user, customer, event and value.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SOT-015).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search partner orders booking | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by partner, partner order reference, ticvai order id, event, venue, product and 5 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Partner | text field | — | — | `listPartnerOrderBooking` ?partner |
| Partner order reference | text field | — | — | `listPartnerOrderBooking` ?partnerOrderReference |
| Ticvai order | text field | — | — | `listPartnerOrderBooking` ?ticvaiOrderId |
| Event | text field | — | — | `listPartnerOrderBooking` ?event |
| Venue | text field | — | — | `listPartnerOrderBooking` ?venue |
| Product | text field | — | — | `listPartnerOrderBooking` ?product |
| Booking date | date picker | — | — | `listPartnerOrderBooking` ?bookingDate |
| Visit event date | date picker | — | — | `listPartnerOrderBooking` ?visitEventDate |
| Status | select | — | Draft · Held · Confirmed · Partially fulfilled · Fulfilled · Cancelled · Refunded · Failed | `listPartnerOrderBooking` ?status |
| Agent | text field | — | — | `listPartnerOrderBooking` ?agent |
| Channel | select | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | `listPartnerOrderBooking` ?channel |

#### Outputs: what the screen shows and produces

**Shown**

**Every partner orders booking** (data table, from `listPartnerOrderBooking`)

| Shows | Format | Notes |
|---|---|---|
| TICVAI order ID | text | not in the schema: `TICVAI Order ID` |
| Partner reference | text | Partner Reference |
| Partner | text | not in the schema: `Partner` |
| Agent user | text | Agent/User |
| Customer name | text | Customer/Guest where applicable |
| Booking date | text | not in the schema: `Booking Date` |
| Event | text | not in the schema: `Event` |
| Products | list or chips (count when long) | Products |
| Quantity | 1,234 | Quantity |
| Gross value | AED 1,234.50 | Gross Value |
| Partner rate | AED 1,234.50 | Partner Rate applied |
| Commission | AED 1,234.50 | Commission |
| Net amount | AED 1,234.50 | Net Amount |
| Payment method | chip: Credit account, Prepaid, Card | Payment Method (the three payment models) |
| Billing status | text | Billing Status: unbilled, invoiced, paid, overdue or credited |
| Fulfillment status | text | Fulfillment Status: pending, partiallyIssued, issued or delivered |

**The selected partner orders booking** (detail panel): The pack groups this record's detail under its own headings: “Important Architecture”.

| Shows | Format | Notes |
|---|---|---|
| TICVAI order ID | text | not in the schema: `TICVAI Order ID` |
| Partner reference | text | Partner Reference |
| Partner | text | not in the schema: `Partner` |
| Agent user | text | Agent/User |
| Customer name | text | Customer/Guest where applicable |
| Booking date | text | not in the schema: `Booking Date` |
| Event | text | not in the schema: `Event` |
| Products | list or chips (count when long) | Products |
| Quantity | 1,234 | Quantity |
| Gross value | AED 1,234.50 | Gross Value |
| Partner rate | AED 1,234.50 | Partner Rate applied |
| Commission | AED 1,234.50 | Commission |
| Net amount | AED 1,234.50 | Net Amount |
| Payment method | chip: Credit account, Prepaid, Card | Payment Method (the three payment models) |
| Billing status | text | Billing Status: unbilled, invoiced, paid, overdue or credited |
| Fulfillment status | text | Fulfillment Status: pending, partiallyIssued, issued or delivered |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** View, Modify, Cancel, Rebook, Resend Tickets, Reissue, Add Internal Note, Escalate, Open Financial Record. Each needs attaching to the control it gates, or the screen needs the control.

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Money columns (commission, grossValue, netAmount)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. Across tenants or regions figures in different currencies are never summed into one total; group by currency, or label the converted figure with its rate and time. *(source: ADR-0008; ADR-0011; DI-306)*

**Data it reads**: `listPartnerOrderBooking` (onLoad, Partner Orders & Booking Management)

**Where the user goes next**

- → `PTR-042` Partner Operations Command Center: *Returns to the board's landing screen*; calls `listPartnerOrderBooking`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The partner orders booking list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partner orders booking untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No partner bookings yet. Offers no create action: partners book on their own booking screens. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the partner orders booking are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every partner orders booking:
- TICVAI Order ID: 11
  Partner: Marina Leisure Group
  Booking Date: 01/10/2026 09:14
  Event: 233
- TICVAI Order ID: 128
  Partner: Desert Gate Tours LLC
  Booking Date: 30/09/2026 18:02
  Event: 57
- TICVAI Order ID: 46
  Partner: Arabian Trails
  Booking Date: 28/09/2026 11:45
  Event: 11
```

#### Permissions

- `listPartnerOrderBooking` → `PLATFORM_TENANT_VIEW` (read) · partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- For partners not integrating by API, TICVAI can issue a bulk batch of pre-generated tickets (QR codes, agreed rates, defined validity) as a CSV export for the partner to import and resell. *(agreed · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-553)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker · keyword 'ticket-booking ux')*
- **A46** Evaluate a dynamic bundle/package builder that auto-applies a discount when a guest adds multiple product types (ticket + F&B + retail) to cart, in addition to pre-defined packages *(Reshma Bandiwdekar · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'cart')*
- **A96** Build the journey library (abandoned cart with min-value/product filters, birthday, anniversary, cross-sell, survey — all consent-gated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'cart')*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'b2c checkout')*
- **A157** Keep F&B and retail online sale entirely within the platform (browse, cart, checkout, pickup or ship) with no redirect to a separate app *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 26 Aug 2026 · workshop tracker · keyword 'cart')*
- **A158** Obtain the resource-management reference documentation, review the hardware/ticketing docs, route follow-up questions to Qossai, and review the House of Wisdom booking flow as a UX reference *(Allam / Chinmay Parab / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 26 Aug 2026 · workshop tracker · keyword 'booking flow')*

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-043` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS40 B2B, Reseller & OTA Partner Management Board 3.dc.html#ptr-043`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 3
- Flow F132 *B2B, Reseller & OTA Partner Management board 3: Partner Operations Command …*, step 2: Works in Partner Orders & Booking Management → Provide a consolidated operational view of orders created by each partner.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (32 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-043?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `PTR-042`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-044` Reservations, Holds & Release Management

**Manage inventory temporarily reserved by B2B partners before final confirmation. This is particularly important for tour operators, corporate groups and travel-trade partners.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner staff holding `PLATFORM_TENANT_VIEW` (1 read); in the flows as partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/partners/reservations-holds-release-management-ptr-044` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Inventory held by partners before confirmation: expiring today, expired, converted, released.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SOT-015).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Partner | picker: choose a partner | — | — | `listReservationHoldRelease` ?partnerId |
| Event | text field | — | — | `listReservationHoldRelease` ?event |
| Status | radio group | — | Active · Extended · Converted · Released · Expired | `listReservationHoldRelease` ?status |
| Expiring before | date and time picker | — | — | `listReservationHoldRelease` ?expiringBefore |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Active Holds** (metric tile, from `listReservationHoldRelease`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Hold | the name it points at, never the id | Hold ID |
| Partner | text | Partner trading name |
| Event | text | Event |
| Product | text | Product |
| Quantity | 1,234 | Quantity |
| Seat zone | text | Seat/Zone where applicable |
| Hold created at | 1 Oct 2026, 14:30 | Hold Created |
| Hold expires at | 1 Oct 2026, 14:30 | Hold Expiry |
| Created by | 1 Oct 2026, 14:30 | Created By |
| Commercial value | AED 1,234.50 | Commercial Value |
| Allocation source | chip: Partner allocation, Channel allocation, General capacity | Allocation Source |
| Status | text | Status: active, extended, converted, released, expired |
| Extensions used | 1,234 | Extensions used so far |
| Partner | the name it points at, never the id | Partner |
| AI insights | list or chips (count when long) | Advisory AI conversion-probability and release suggestions |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Reservations, Holds & Release Management. The pack's KPI cards, split out of the row (decided 29 September … |
| Active holds | 1,234 | Active Holds |

**Held Tickets** (metric tile, from `listReservationHoldRelease`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Hold | the name it points at, never the id | Hold ID |
| Partner | text | Partner trading name |
| Event | text | Event |
| Product | text | Product |
| Quantity | 1,234 | Quantity |
| Seat zone | text | Seat/Zone where applicable |
| Hold created at | 1 Oct 2026, 14:30 | Hold Created |
| Hold expires at | 1 Oct 2026, 14:30 | Hold Expiry |
| Created by | 1 Oct 2026, 14:30 | Created By |
| Commercial value | AED 1,234.50 | Commercial Value |
| Allocation source | chip: Partner allocation, Channel allocation, General capacity | Allocation Source |
| Status | text | Status: active, extended, converted, released, expired |
| Extensions used | 1,234 | Extensions used so far |
| Partner | the name it points at, never the id | Partner |
| AI insights | list or chips (count when long) | Advisory AI conversion-probability and release suggestions |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Reservations, Holds & Release Management. The pack's KPI cards, split out of the row (decided 29 September … |
| Active holds | 1,234 | Active Holds |

**Held Value** (metric tile, from `listReservationHoldRelease`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Hold | the name it points at, never the id | Hold ID |
| Partner | text | Partner trading name |
| Event | text | Event |
| Product | text | Product |
| Quantity | 1,234 | Quantity |
| Seat zone | text | Seat/Zone where applicable |
| Hold created at | 1 Oct 2026, 14:30 | Hold Created |
| Hold expires at | 1 Oct 2026, 14:30 | Hold Expiry |
| Created by | 1 Oct 2026, 14:30 | Created By |
| Commercial value | AED 1,234.50 | Commercial Value |
| Allocation source | chip: Partner allocation, Channel allocation, General capacity | Allocation Source |
| Status | text | Status: active, extended, converted, released, expired |
| Extensions used | 1,234 | Extensions used so far |
| Partner | the name it points at, never the id | Partner |
| AI insights | list or chips (count when long) | Advisory AI conversion-probability and release suggestions |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Reservations, Holds & Release Management. The pack's KPI cards, split out of the row (decided 29 September … |
| Active holds | 1,234 | Active Holds |

**Expiring Today** (metric tile, from `listReservationHoldRelease`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Hold | the name it points at, never the id | Hold ID |
| Partner | text | Partner trading name |
| Event | text | Event |
| Product | text | Product |
| Quantity | 1,234 | Quantity |
| Seat zone | text | Seat/Zone where applicable |
| Hold created at | 1 Oct 2026, 14:30 | Hold Created |
| Hold expires at | 1 Oct 2026, 14:30 | Hold Expiry |
| Created by | 1 Oct 2026, 14:30 | Created By |
| Commercial value | AED 1,234.50 | Commercial Value |
| Allocation source | chip: Partner allocation, Channel allocation, General capacity | Allocation Source |
| Status | text | Status: active, extended, converted, released, expired |
| Extensions used | 1,234 | Extensions used so far |
| Partner | the name it points at, never the id | Partner |
| AI insights | list or chips (count when long) | Advisory AI conversion-probability and release suggestions |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Reservations, Holds & Release Management. The pack's KPI cards, split out of the row (decided 29 September … |
| Active holds | 1,234 | Active Holds |

**Expired Holds** (metric tile, from `listReservationHoldRelease`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Hold | the name it points at, never the id | Hold ID |
| Partner | text | Partner trading name |
| Event | text | Event |
| Product | text | Product |
| Quantity | 1,234 | Quantity |
| Seat zone | text | Seat/Zone where applicable |
| Hold created at | 1 Oct 2026, 14:30 | Hold Created |
| Hold expires at | 1 Oct 2026, 14:30 | Hold Expiry |
| Created by | 1 Oct 2026, 14:30 | Created By |
| Commercial value | AED 1,234.50 | Commercial Value |
| Allocation source | chip: Partner allocation, Channel allocation, General capacity | Allocation Source |
| Status | text | Status: active, extended, converted, released, expired |
| Extensions used | 1,234 | Extensions used so far |
| Partner | the name it points at, never the id | Partner |
| AI insights | list or chips (count when long) | Advisory AI conversion-probability and release suggestions |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Reservations, Holds & Release Management. The pack's KPI cards, split out of the row (decided 29 September … |
| Active holds | 1,234 | Active Holds |

**Converted Holds** (metric tile, from `listReservationHoldRelease`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Hold | the name it points at, never the id | Hold ID |
| Partner | text | Partner trading name |
| Event | text | Event |
| Product | text | Product |
| Quantity | 1,234 | Quantity |
| Seat zone | text | Seat/Zone where applicable |
| Hold created at | 1 Oct 2026, 14:30 | Hold Created |
| Hold expires at | 1 Oct 2026, 14:30 | Hold Expiry |
| Created by | 1 Oct 2026, 14:30 | Created By |
| Commercial value | AED 1,234.50 | Commercial Value |
| Allocation source | chip: Partner allocation, Channel allocation, General capacity | Allocation Source |
| Status | text | Status: active, extended, converted, released, expired |
| Extensions used | 1,234 | Extensions used so far |
| Partner | the name it points at, never the id | Partner |
| AI insights | list or chips (count when long) | Advisory AI conversion-probability and release suggestions |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Reservations, Holds & Release Management. The pack's KPI cards, split out of the row (decided 29 September … |
| Active holds | 1,234 | Active Holds |

**Released Inventory, tickets** (metric tile, from `listReservationHoldRelease`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Hold | the name it points at, never the id | Hold ID |
| Partner | text | Partner trading name |
| Event | text | Event |
| Product | text | Product |
| Quantity | 1,234 | Quantity |
| Seat zone | text | Seat/Zone where applicable |
| Hold created at | 1 Oct 2026, 14:30 | Hold Created |
| Hold expires at | 1 Oct 2026, 14:30 | Hold Expiry |
| Created by | 1 Oct 2026, 14:30 | Created By |
| Commercial value | AED 1,234.50 | Commercial Value |
| Allocation source | chip: Partner allocation, Channel allocation, General capacity | Allocation Source |
| Status | text | Status: active, extended, converted, released, expired |
| Extensions used | 1,234 | Extensions used so far |
| Partner | the name it points at, never the id | Partner |
| AI insights | list or chips (count when long) | Advisory AI conversion-probability and release suggestions |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Reservations, Holds & Release Management. The pack's KPI cards, split out of the row (decided 29 September … |
| Active holds | 1,234 | Active Holds |

**Every reservations holds release** (data table, from `listReservationHoldRelease`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Hold | the name it points at, never the id | Hold ID |
| Partner | text | Partner trading name |
| Event | text | Event |
| Product | text | Product |
| Quantity | 1,234 | Quantity |
| Seat zone | text | Seat/Zone where applicable |
| Hold created at | 1 Oct 2026, 14:30 | Hold Created |
| Hold expires at | 1 Oct 2026, 14:30 | Hold Expiry |
| Created by | 1 Oct 2026, 14:30 | Created By |
| Commercial value | AED 1,234.50 | Commercial Value |
| Allocation source | chip: Partner allocation, Channel allocation, General capacity | Allocation Source |
| Status | text | Status: active, extended, converted, released, expired |
| Extensions used | 1,234 | Extensions used so far |
| Partner | the name it points at, never the id | Partner |
| AI insights | list or chips (count when long) | Advisory AI conversion-probability and release suggestions |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Reservations, Holds & Release Management. The pack's KPI cards, split out of the row (decided 29 September … |
| Active holds | 1,234 | Active Holds |

**The selected reservations holds release** (detail panel): The pack groups this record's detail under its own headings: “When a hold expires”.

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Extend Hold, Reduce Hold, Release Hold, Convert to Booking, Reassign where permitted, Escalate. Each needs attaching to the control it gates, or the screen needs the control.

**Data it reads**: `listReservationHoldRelease` (onLoad, Reservations, Holds & Release Management)

**Where the user goes next**

- → `PTR-042` Partner Operations Command Center: *Returns to the board's landing screen*; calls `listReservationHoldRelease`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reservations holds release list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reservations holds release untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No holds open: no partner inventory is reserved right now. Offers no create action. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the reservations holds release are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
metric tiles:
  Active Holds: 128
  Held Tickets: 46
  Held Value: AED 12,400.00
  Expiring Today: 74
  Expired Holds: 3
  Converted Holds: 233
  Released Inventory, tickets: 57
```

#### Permissions

- `listReservationHoldRelease` → `PLATFORM_TENANT_VIEW` (read) · partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-044` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS40 B2B, Reseller & OTA Partner Management Board 3.dc.html#ptr-044`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 3
- Flow F132 *B2B, Reseller & OTA Partner Management board 3: Partner Operations Command …*, step 4: Works in Reservations, Holds & Release Management → Manage inventory temporarily reserved by B2B partners before final confirmation. This is particularly important for tour operators, corporate groups and travel-trade partners.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (160 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-044?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `PTR-042`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-045` Partner Cancellations, Refunds & Amendments

**Manage post-booking changes according to the partner's commercial agreement and product policies.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner staff holding `ORDER_MODIFY`, `PLATFORM_TENANT_VIEW` (1 operate, 1 read); in the flows as partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/partners/partner-cancellations-refunds-amendments-ptr-045` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Partner cancellations, refunds and amendments under the agreement's policies.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Partner | picker: choose a partner | — | — | `listPartnerCancellationRefund` ?partnerId |
| Request type | select | — | Full cancellation · Partial cancellation · Date change · Performance change · Quantity reduction · Product change · Ticket reissue · Customer name change · Refund request | `listPartnerCancellationRefund` ?requestType |
| Status | radio group | — | Requested · Pending approval · Approved · Rejected · Processed | `listPartnerCancellationRefund` ?status |
| From | date picker | — | — | `listPartnerCancellationRefund` ?from |
| To | date picker | — | — | `listPartnerCancellationRefund` ?to |

**Form: Create partner change request** (modal, opened by *Create partner change request*; *Create partner change request* calls `createPartnerChangeRequest`, *Cancel* sends nothing)

**Collects what `createPartnerChangeRequest` sends before it is called.** Required: `orderId`, `requestType`. Optional: `quantity`, `targetPerformanceId`, `targetProductId`, `newCustomerName`, `feeWaiverRequested`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Order `orderId` | picker: choose an order | required | — | — | shows names, sends the id | The partner's order (orders.sales_order) | `createPartnerChangeRequest` body |
| Request type `requestType` | select | required | — | Full cancellation · Partial cancellation · Date change · Performance change · Quantity reduction · Product change · Ticket reissue · Customer name change · Refund request | — | — | `createPartnerChangeRequest` body |
| Quantity `quantity` | number field | optional | — | min 1 | — | Tickets affected; required for partialCancellation and quantityReduction | `createPartnerChangeRequest` body |
| Target performance `targetPerformanceId` | picker: choose a target performance | optional | — | — | shows names, sends the id | Required for dateChange and performanceChange | `createPartnerChangeRequest` body |
| Target product `targetProductId` | picker: choose a target product | optional | — | — | shows names, sends the id | Required for productChange | `createPartnerChangeRequest` body |
| New customer name `newCustomerName` | text field | optional | — | — | — | Required for customerNameChange | `createPartnerChangeRequest` body |
| Fee waiver requested `feeWaiverRequested` | toggle | optional | off | — | — | — | `createPartnerChangeRequest` body |
| Reason `reason` | text area | optional | — | — | — | — | `createPartnerChangeRequest` body |

Errors to draw in the form: 404 No such order for this partner; 422 A field the request type needs is missing

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create partner change request (primary button) | `createPartnerChangeRequest` POST `/partner-change-requests` | PartnerChangeRequestInput | PartnerChangeRequest | 404 No such order for this partner; 422 A field the request type needs is missing | gated `ORDER_MODIFY`; opens modal first |

**Data it reads**: `listPartnerCancellationRefund` (onLoad, Partner Cancellations, Refunds & Amendments)

**Where the user goes next**

- → `PTR-042` Partner Operations Command Center: *Returns to the board's landing screen*; calls `listPartnerCancellationRefund`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The partner cancellations refunds list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partner cancellations refunds untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No partner cancellations refunds yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the partner cancellations refunds are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 A field the request type needs is missing |

#### Edge cases to draw

- **Can read but not change (holds PLATFORM_TENANT_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: ORDER_MODIFY for Create partner change request. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/subscription.yaml#createPartnerChangeRequest)*
- **createPartnerChangeRequest answers 404**: Show it as something the person can act on, not a failure: No such order for this partner *(source: contracts/satellite/subscription.yaml#createPartnerChangeRequest)*
- **createPartnerChangeRequest answers 422**: Show it as something the person can act on, not a failure: A field the request type needs is missing *(source: contracts/satellite/subscription.yaml#createPartnerChangeRequest)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
booking: DGT-AUH-88412
change: Cancel 6 of 40 tickets
policy: free until 48 h before visit
refund: AED 1,050.00
```

#### Permissions

- `listPartnerCancellationRefund` → `PLATFORM_TENANT_VIEW` (read) · partner
- `createPartnerChangeRequest` → `ORDER_MODIFY` (operate) · partner, staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Operations dashboard per partner: order volume, revenue, reservations and tickets on hold (booked but not yet issued). Cancellations/refund requests, statement of account (opening/closing balance, activity), reconciliation exceptions and disputes are tracked from this view. *(client request · MoM 31 Aug 2026, 4.5 B2B Day-to-Day Operations & Settlement · DI-557)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A75** Design the refund engine: a six-step ledger-to-gateway refund flow with configurable time-banded percentages, an authorized-approver override, partial refunds, both operations- and customer-initiated requests, plus bulk … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 12 Aug 2026 · workshop tracker · keyword 'refund')*
- **A80** Implement a currency-locking rule for refunds/change: always issue in the local/base currency, locked at the value recorded at time of purchase; track foreign-currency activity only via a separate report *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 14 Aug 2026 · workshop tracker · keyword 'refund')*
- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'refund')*
- **A140** Centralise policy management (reschedule, exchange, refund, cancellation, upgrade, downgrade, ownership transfer, membership conversion) with each product mapped to pricing, GL code, promotions and channels *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'refund')*
- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'refund')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'refund')*

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-045` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS40 B2B, Reseller & OTA Partner Management Board 3.dc.html#ptr-045`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 3
- Flow F132 *B2B, Reseller & OTA Partner Management board 3: Partner Operations Command …*, step 6: Works in Partner Cancellations, Refunds & Amendments → Manage post-booking changes according to the partner's commercial agreement and product policies.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-045?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create partner change request.
- [ ] Every transition is wired: `PTR-042`.
- [ ] Every gated control is gated: `ORDER_MODIFY`, `PLATFORM_TENANT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-046` Partner Statement & Account Activity

**Give finance and commercial teams a complete financial statement for each partner account.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner staff holding `PLATFORM_TENANT_VIEW` (1 read); in the flows as partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each line should show) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/partners/partner-statement-account-activity-ptr-046` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** A partner account statement: opening balance, sales, payments, credits, commission, closing balance and ageing.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SOT-015).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Partner | picker: choose a partner | — | — | `listPartnerStatementAccount` ?partnerId |
| Period | radio group | — | Daily · Weekly · Monthly · Custom | `listPartnerStatementAccount` ?period |
| From | date picker | — | — | `listPartnerStatementAccount` ?from |
| To | date picker | — | — | `listPartnerStatementAccount` ?to |
| Transaction type | select | — | Booking · Invoice · Payment · Refund · Credit note · Commission · Manual adjustment · Deposit · Settlement | `listPartnerStatementAccount` ?transactionType |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Opening Balance** (metric tile)

**Sales** (metric tile)

**Payments** (metric tile)

**Credits** (metric tile)

**Refunds** (metric tile)

**Commission** (metric tile)

**Adjustments** (metric tile)

**Closing Balance** (metric tile)

**Overdue Balance** (metric tile)

**Available Credit** (metric tile)

**Current** (metric tile)

**1–30 Days** (metric tile)

**31–60 Days** (metric tile)

**61–90 Days** (metric tile)

**90+ Days** (metric tile)

**Every partner statement account** (data table, from `listPartnerStatementAccount`)

| Shows | Format | Notes |
|---|---|---|
| Date | 1 Oct 2026 | Date |
| Transaction type | chip: Booking, Invoice, Payment, Refund, Credit note, Commission… | Transaction Type |
| Reference | text | Reference |
| Order invoice | text | Order/Invoice number |
| Debit | AED 1,234.50 | Debit |
| Credit | AED 1,234.50 | Credit |
| Running balance | AED 1,234.50 | Running Balance |
| Due date | 1 Oct 2026 | Due Date |
| Status | text | Status: open, partiallyPaid, paid, overdue or void |

**The selected partner statement account** (detail panel): The pack groups this record's detail under its own headings: “Generate by”, “Partner Access”, “Architecture”.

| Shows | Format | Notes |
|---|---|---|
| Date | 1 Oct 2026 | Date |
| Transaction type | chip: Booking, Invoice, Payment, Refund, Credit note, Commission… | Transaction Type |
| Reference | text | Reference |
| Order invoice | text | Order/Invoice number |
| Debit | AED 1,234.50 | Debit |
| Credit | AED 1,234.50 | Credit |
| Running balance | AED 1,234.50 | Running Balance |
| Due date | 1 Oct 2026 | Due Date |
| Status | text | Status: open, partiallyPaid, paid, overdue or void |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Ageing**: Current, 1–30, 31–60, 61–90, 90+ days in the account currency; overdue highlighted. *(source: contracts/satellite/subscription.yaml#listPartnerStatementAccount)*
- **Money columns (runningBalance)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. Across tenants or regions figures in different currencies are never summed into one total; group by currency, or label the converted figure with its rate and time. *(source: ADR-0008; ADR-0011; DI-306)*

**Data it reads**: `listPartnerStatementAccount` (onLoad, Partner Statement & Account Activity)

**Where the user goes next**

- → `PTR-042` Partner Operations Command Center: *Returns to the board's landing screen*; calls `listPartnerStatementAccount`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The partner statement account list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partner statement account untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No account activity in this period: the opening balance is the closing balance. Offers no create action. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the partner statement account are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
metric tiles:
  Opening Balance: 128
  Sales: 46
  Payments: 312
  Credits: 74
  Refunds: 19
  Commission: AED 12,400.00
  Adjustments: 57
  Closing Balance: 11
  Overdue Balance: 1
  Available Credit: 46
```

#### Permissions

- `listPartnerStatementAccount` → `PLATFORM_TENANT_VIEW` (read) · partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Operations dashboard per partner: order volume, revenue, reservations and tickets on hold (booked but not yet issued). Cancellations/refund requests, statement of account (opening/closing balance, activity), reconciliation exceptions and disputes are tracked from this view. *(client request · MoM 31 Aug 2026, 4.5 B2B Day-to-Day Operations & Settlement · DI-557)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-046` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS40 B2B, Reseller & OTA Partner Management Board 3.dc.html#ptr-046`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 3
- Flow F132 *B2B, Reseller & OTA Partner Management board 3: Partner Operations Command …*, step 8: Works in Partner Statement & Account Activity → Give finance and commercial teams a complete financial statement for each partner account.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-046?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `PTR-042`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-049` Partner Disputes, Cases & Service Management

**Provide a structured case-management environment for partner operational and commercial disputes.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner staff holding `CASE_MANAGE`, `PLATFORM_TENANT_VIEW` (1 configure, 1 read); in the flows as partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Monitor) and no metric row |
| Offline | online only |
| Opens with | `caseId` (navigation) |
| Route | `/partners/partner-disputes-cases-service-management-ptr-049` |

**Known gaps.** **The pack names 8 actions on this screen; 6 are served since the writers pass (29 September): Booking Dispute, Pricing Dispute, Credit Dispute, Ticket Issue, Allocation Issue, API Issue by …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Partner disputes and cases by type with SLA.

**Fixed on main** (the package already carries these; draw what it says): Case types drawn as buttons. (CHG-SOT-015); formCreatePartnerCase asks the person for status, id. (CHG-SOT-015).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Case type | select field | — | — | — | — | Chosen when creating a case (`createPartnerCase.category`). Options: Booking Dispute; Pricing Dispute; Credit Dispute; Ticket Issue; Allocation Issue; API Issue; Finance review; Technical review. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Partner | picker: choose a partner | — | — | `listPartnerDisputeCase` ?partnerId |
| Category | select | — | Booking dispute · Pricing dispute · Commission dispute · Credit dispute · Invoice dispute · Cancellation dispute · Ticket issue · Allocation issue · API issue · Settlement dispute | `listPartnerDisputeCase` ?category |
| Status | select | — | Open · Assigned · Investigating · Waiting partner · Waiting internal · Resolution proposed · Resolved · Closed | `listPartnerDisputeCase` ?status |
| Priority | radio group | — | Low · Medium · High · Urgent | `listPartnerDisputeCase` ?priority |
| Owner | text field | — | — | `listPartnerDisputeCase` ?owner |
| Sla breach | toggle | — | — | `listPartnerDisputeCase` ?slaBreach |

**Form: Create partner case** (modal, opened by *Create partner case*; *Create partner case* calls `createPartnerCase`, *Cancel* sends nothing)

**Collects what `createPartnerCase` sends before it is called.** The person picks the **case type** (booking dispute, pricing dispute, credit dispute, ticket issue, allocation issue, API issue) and the priority, describes it and links the order, invoice or settlement batch; `partnerId` comes from the session; the owner, SLA policy, resolution target and response times are the server's. Never `id` or `status`: an id is a client UUIDv7 generated silently and the status and timestamps are the server's (design-notes correction, CHG-SOT-015). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Partner `partnerId` | picker: choose a partner | required | — | — | shows names, sends the id | The partner (control.partner). | `createPartnerCase` body |
| Contact `contactId` | picker: choose a contact | optional | — | — | shows names, sends the id | Partner contact (control.partner_contact). | `createPartnerCase` body |
| Category `category` | select | required | — | Booking dispute · Pricing dispute · Commission dispute · Credit dispute · Invoice dispute · Cancellation dispute · Ticket issue · Allocation issue · API issue · Settlement dispute | — | Category. | `createPartnerCase` body |
| Priority `priority` | radio group | required | — | Low · Medium · High · Urgent | — | Priority (decided 29 September, readiness close-out). | `createPartnerCase` body |
| Order `orderId` | picker: choose an order | optional | — | — | shows names, sends the id | Related order (orders.sales_order). | `createPartnerCase` body |
| Invoice reference `invoiceReference` | text field | optional | — | — | — | Related invoice number. | `createPartnerCase` body |
| Settlement batch `settlementBatchId` | picker: choose a settlement batch | optional | — | — | shows names, sends the id | Related settlement (control.partner_settlement_batch). | `createPartnerCase` body |
| Amount in dispute `amountInDispute` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Amount in dispute. | `createPartnerCase` body |
| Description `description` | text area | required | — | — | — | Description. | `createPartnerCase` body |
| Evidence `evidence` | list of values (chips) | optional | — | — | — | Evidence: attachment references. | `createPartnerCase` body |
| Owner principal `ownerPrincipalId` | picker: choose an owner principal | optional | — | — | shows names, sends the id | Owner, a staff principal. | `createPartnerCase` body |
| Sla policy `slaPolicyId` | picker: choose a sla policy | optional | — | — | shows names, sends the id | The SLA policy applied (approvals.sla_policy, the approvals engine's ApprovalSlaPolicy), which sets the first-response and resolution targets and the reminder/breach behaviour … | `createPartnerCase` body |
| First response at `firstResponseAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | First response at. | `createPartnerCase` body |
| Resolved at `resolvedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Resolved at. | `createPartnerCase` body |
| Scope path `scopePath` | text field | optional | — | — | — | The partition key (ADR-0005), written at `tenant` scope. | `createPartnerCase` body |

Errors to draw in the form: 422 A money category with nothing named, or an unknown SLA policy

**Form: Act on partner case** (modal, opened by *Act on partner case*; *Act on partner case* calls `actOnPartnerCase`, *Cancel* sends nothing)

**Collects what `actOnPartnerCase` sends before it is called.** Required: `action`. Optional: `ownerPrincipalId`, `resolution`, `reason`, `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Action `action` | select | required | — | Assign · Start investigation · Wait for partner · Partner responded · Wait for internal · Internal responded · Propose resolution · Accept resolution · Reject resolution · Reopen · Close without investigation | — | — | `actOnPartnerCase` body |
| Owner principal `ownerPrincipalId` | picker: choose an owner principal | optional | — | — | shows names, sends the id | For assign | `actOnPartnerCase` body |
| Resolution `resolution` | text field | optional | — | — | — | For proposeResolution, the adjustment, credit, correction or no-change reason proposed | `actOnPartnerCase` body |
| Reason `reason` | text area | optional | — | — | — | For rejectResolution, reopen and closeWithoutInvestigation | `actOnPartnerCase` body |
| Note `note` | text area | optional | — | — | — | Message kept on the case trail | `actOnPartnerCase` body |

Errors to draw in the form: 404 No such case; 409 The action does not fit the case's status, or the reopening window has passed; 422 A field the action needs is missing

#### Outputs: what the screen shows and produces

**Shown**

**Every partner disputes cases** (data table, from `listPartnerDisputeCase`)

| Shows | Format | Notes |
|---|---|---|
| First response | 1 Oct 2026, 14:30 | First Response at |
| Resolution target | 1 Oct 2026, 14:30 | Resolution Target |
| Time open | 1,234 | Time Open, hours |
| Sla breach | yes / no (icon or chip) | SLA Breach |

**The selected partner disputes cases** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| First response | 1 Oct 2026, 14:30 | First Response at |
| Resolution target | 1 Oct 2026, 14:30 | Resolution Target |
| Time open | 1,234 | Time Open, hours |
| Sla breach | yes / no (icon or chip) | SLA Breach |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create partner case (secondary button) | `createPartnerCase` POST `/partner-cases` | PartnerCase | PartnerCase | 422 A money category with nothing named, or an unknown SLA policy | gated `CASE_MANAGE`; opens modal first |
| Act on partner case (secondary button) | `actOnPartnerCase` POST `/partner-cases/{caseId}/actions` | inline | PartnerCase | 404 No such case; 409 The action does not fit the case's status, or the reopening window has passed; 422 A field the action needs is missing | gated `CASE_MANAGE`; opens modal first |

**Data it reads**: `listPartnerDisputeCase` (onLoad, Partner Disputes, Cases & Service Management)

**Where the user goes next**

- → `PTR-042` Partner Operations Command Center: *Returns to the board's landing screen*; calls `listPartnerDisputeCase`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The partner disputes cases list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partner disputes cases untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No partner disputes cases yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the partner disputes cases are still there. The pack's own statuses are Proposed → Resolved → Closed — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The action does not fit the case's status, or the reopening window has passed; 422 A field the action needs is missing; 422 A money category with nothing named, or an unknown SLA policy |

#### Edge cases to draw

- **Can read but not change (holds PLATFORM_TENANT_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: CASE_MANAGE for Create partner case, Act on partner case. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/subscription.yaml#createPartnerCase)*
- **createPartnerCase answers 422**: Show it as something the person can act on, not a failure: A money category with nothing named, or an unknown SLA policy *(source: contracts/satellite/subscription.yaml#createPartnerCase)*
- **actOnPartnerCase answers 409**: Show it as something the person can act on, not a failure: The action does not fit the case's status, or the reopening window has passed *(source: contracts/satellite/subscription.yaml#actOnPartnerCase)*
- **actOnPartnerCase answers 422**: Show it as something the person can act on, not a failure: A field the action needs is missing *(source: contracts/satellite/subscription.yaml#actOnPartnerCase)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
case: PC-2026-0091
type: Pricing dispute
partner: Arabian Trails
firstResponse: 2 h
status: open
```

#### Permissions

- `listPartnerDisputeCase` → `PLATFORM_TENANT_VIEW` (read) · partner
- `createPartnerCase` → `CASE_MANAGE` (configure) · staff, partner
- `actOnPartnerCase` → `CASE_MANAGE` (configure) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Operations dashboard per partner: order volume, revenue, reservations and tickets on hold (booked but not yet issued). Cancellations/refund requests, statement of account (opening/closing balance, activity), reconciliation exceptions and disputes are tracked from this view. *(client request · MoM 31 Aug 2026, 4.5 B2B Day-to-Day Operations & Settlement · DI-557)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-049` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS40 B2B, Reseller & OTA Partner Management Board 3.dc.html#ptr-049`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 3
- Flow F132 *B2B, Reseller & OTA Partner Management board 3: Partner Operations Command …*, step 10: Works in Partner Disputes, Cases & Service Management → Provide a structured case-management environment for partner operational and commercial disputes.

#### Acceptance for the design

- [ ] Every input above is drawn (21), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (8 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-049?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create partner case, Act on partner case.
- [ ] Every transition is wired: `PTR-042`.
- [ ] Every gated control is gated: `CASE_MANAGE`, `PLATFORM_TENANT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 4 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-050` Partner Performance Scorecard & Risk Monitoring

**Create a consistent scorecard for evaluating the quality and commercial value of every partner relationship.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner staff holding `PLATFORM_TENANT_VIEW` (1 read); in the flows as partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/partners/partner-performance-scorecard-risk-monitoring-ptr-050` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** A consistent partner scorecard (sales, cancellations, payment behaviour, compliance) with risk.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SOT-015).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Partner | picker: choose a partner | — | — | `listPartnerPerformanceScorecard` ?partnerId |
| Partner type | text field | — | — | `listPartnerPerformanceScorecard` ?partnerType |
| Market | text field | — | — | `listPartnerPerformanceScorecard` ?market |
| Risk rating | radio group | — | Low · Medium · High · Critical | `listPartnerPerformanceScorecard` ?riskRating |
| Trend | segmented control | — | Improving · Stable · Declining | `listPartnerPerformanceScorecard` ?trend |
| Period | text field | — | — | `listPartnerPerformanceScorecard` ?period |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every partner performance scorecard** (data table, from `listPartnerPerformanceScorecard`)

| Shows | Format | Notes |
|---|---|---|
| Trend | chip: Improving, Stable, Declining | Trend |

**The selected partner performance scorecard** (detail panel): The pack groups this record's detail under its own headings: “Commercial”, “Allocation”, “Financial”, “Operational”, “Technical”, “Compliance”.

| Shows | Format | Notes |
|---|---|---|
| Trend | chip: Improving, Stable, Declining | Trend |

**Data it reads**: `listPartnerPerformanceScorecard` (onLoad, Partner Performance Scorecard & Risk Monitoring)

**Where the user goes next**

- → `PTR-042` Partner Operations Command Center: *Returns to the board's landing screen*; calls `listPartnerPerformanceScorecard`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The partner performance scorecard list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partner performance scorecard untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No scorecard yet: a partner is scored after its first full period of trading. Offers no create action. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the partner performance scorecard are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listPartnerPerformanceScorecard (PartnerPerformanceScorecardRiskMonitoringView):
- growth: 12
  margin: 12
  utilization: 12
  sellThrough: 12
  returnedInventory: 12
- growth: 3
  margin: 3
  utilization: 3
  sellThrough: 3
  returnedInventory: 3
```

#### Permissions

- `listPartnerPerformanceScorecard` → `PLATFORM_TENANT_VIEW` (read) · partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- AI partner performance view surfaces trends, risks and opportunities across the partner base for account-management decisions. *(client request · MoM 31 Aug 2026, 4.5 B2B Day-to-Day Operations & Settlement · DI-558)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-050` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS40 B2B, Reseller & OTA Partner Management Board 3.dc.html#ptr-050`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 3
- Flow F132 *B2B, Reseller & OTA Partner Management board 3: Partner Operations Command …*, step 12: Works in Partner Performance Scorecard & Risk Monitoring → Create a consistent scorecard for evaluating the quality and commercial value of every partner relationship.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-050?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `PTR-042`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-051` Partner AI Intelligence & Relationship Optimization

**Provide TICVAI's AI decision-support layer across the complete partner lifecycle. This screen should combine information from Boards 1, 2 and 3.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner staff holding `PLATFORM_TENANT_VIEW` (1 read); in the flows as partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Analyze) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/partners/partner-ai-intelligence-relationship-optimization-ptr-051` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** AI insights across the partner lifecycle with the inputs considered.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SOT-015).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Partner | picker: choose a partner | — | — | `listPartnerRelationship` ?partnerId |
| Category | radio group | — | Commercial · Allocation · Credit · Risk · Growth | `listPartnerRelationship` ?category |
| Opportunity class | radio group | — | Grow · Maintain · Review · Restrict | `listPartnerRelationship` ?opportunityClass |
| Status | radio group | — | Open · Accepted · Modified · Rejected · Assigned | `listPartnerRelationship` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every partner intelligence relationship** (data table, from `listPartnerRelationship`)

| Shows | Format | Notes |
|---|---|---|
| Inputs considered | list or chips (count when long) | AI Inputs the recommendation drew on |

**The selected partner intelligence relationship** (detail panel): The pack groups this record's detail under its own headings: “Commercial”, “Allocation”, “Credit”, “Risk”, “Growth”, “Natural-Language Analysis”.

| Shows | Format | Notes |
|---|---|---|
| Inputs considered | list or chips (count when long) | AI Inputs the recommendation drew on |

**Data it reads**: `listPartnerRelationship` (onLoad, Partner AI Intelligence & Relationship Optimization)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The partner intelligence relationship list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partner intelligence relationship untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No recommendations yet: there is not enough partner history to learn from. Offers no create action. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the partner intelligence relationship are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listPartnerRelationship (PartnerAiIntelligenceRelationshipOptimizationView):
- reason: Guest charged twice at Main Gate Till 3
  confidence: 12
  category: commercial
- reason: Group of 40 from Desert Gate Tours
  confidence: 3
  category: allocation
```

#### Permissions

- `listPartnerRelationship` → `PLATFORM_TENANT_VIEW` (read) · partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- AI partner performance view surfaces trends, risks and opportunities across the partner base for account-management decisions. *(client request · MoM 31 Aug 2026, 4.5 B2B Day-to-Day Operations & Settlement · DI-558)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-051` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS40 B2B, Reseller & OTA Partner Management Board 3.dc.html#ptr-051`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 3
- Flow F132 *B2B, Reseller & OTA Partner Management board 3: Partner Operations Command …*, step 14: Works in Partner AI Intelligence & Relationship Optimization → Provide TICVAI's AI decision-support layer across the complete partner lifecycle. This screen should combine information from Boards 1, 2 and 3.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-051?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `PLATFORM_TENANT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
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

**8 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"actOnPartnerCase": {"method":"POST","path":"/partner-cases/{caseId}/actions","contract":"subscription","summary":"Work a partner case","permission":"CASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PartnerCase"},
"createPartnerCase": {"method":"POST","path":"/partner-cases","contract":"subscription","summary":"Open a partner dispute or service case","permission":"CASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PartnerCase","responds":"PartnerCase"},
"createPartnerChangeRequest": {"method":"POST","path":"/partner-change-requests","contract":"subscription","summary":"A partner asks to cancel or amend a booking","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":"dryRun","in":"query","required":false}],"requestBody":"PartnerChangeRequestInput","responds":"PartnerChangeRequest"},
"listPartner": {"method":"GET","path":"/partner","contract":"subscription","summary":"Partner Management Command Center","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"brand","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"accountManager","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"risk","in":"query","required":false},{"name":"integrationType","in":"query","required":false},{"name":"partnerType","in":"query","required":false},{"name":"country","in":"query","required":false},{"name":"territory","in":"query","required":false},{"name":"agreementStatus","in":"query","required":false},{"name":"creditStatus","in":"query","required":false},{"name":"search","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPartner2": {"method":"GET","path":"/partner-2","contract":"subscription","summary":"Partner Operations Command Center","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"venue","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"market","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false},{"name":"partnerId","in":"query","required":false},{"name":"partnerType","in":"query","required":false},{"name":"accountManager","in":"query","required":false},{"name":"operationalStatus","in":"query","required":false},{"name":"risk","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPartnerCancellationRefund": {"method":"GET","path":"/partner-cancellation-refund","contract":"subscription","summary":"Partner Cancellations, Refunds & Amendments","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"partnerId","in":"query","required":false},{"name":"requestType","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPartnerDisputeCase": {"method":"GET","path":"/partner-dispute-case","contract":"subscription","summary":"Partner Disputes, Cases & Service Management","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"partnerId","in":"query","required":false},{"name":"category","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"priority","in":"query","required":false},{"name":"owner","in":"query","required":false},{"name":"slaBreach","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPartnerOrderBooking": {"method":"GET","path":"/partner-order-booking","contract":"subscription","summary":"Partner Orders & Booking Management","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"partner","in":"query","required":false},{"name":"partnerOrderReference","in":"query","required":false},{"name":"ticvaiOrderId","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"bookingDate","in":"query","required":false},{"name":"visitEventDate","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"agent","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPartnerPerformanceScorecard": {"method":"GET","path":"/partner-performance-scorecard","contract":"subscription","summary":"Partner Performance Scorecard & Risk Monitoring","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"partnerId","in":"query","required":false},{"name":"partnerType","in":"query","required":false},{"name":"market","in":"query","required":false},{"name":"riskRating","in":"query","required":false},{"name":"trend","in":"query","required":false},{"name":"period","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPartnerRelationship": {"method":"GET","path":"/partner-relationship","contract":"subscription","summary":"Partner AI Intelligence & Relationship Optimization","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"partnerId","in":"query","required":false},{"name":"category","in":"query","required":false},{"name":"opportunityClass","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPartnerStatementAccount": {"method":"GET","path":"/partner-statement-account","contract":"subscription","summary":"Partner Statement & Account Activity","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"partnerId","in":"query","required":false},{"name":"period","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false},{"name":"transactionType","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listReservationHoldRelease": {"method":"GET","path":"/reservation-hold-release","contract":"subscription","summary":"Reservations, Holds & Release Management","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"partnerId","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"expiringBefore","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PartnerAgreementStatus": {"type":"string","enum":["pendingApproval","active","expiringSoon","expired","suspended","terminated"]},
"PartnerAiIntelligenceRelationshipOptimizationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over subscription state, assembled at read time from tables that already exist","description":"**What Partner AI Intelligence & Relationship Optimization displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"recommendation":{"type":"string","description":"Recommendation"},"reason":{"type":"string","description":"Reason"},"expectedImpact":{"type":"string","description":"Expected Impact"},"confidence":{"type":"number","description":"Confidence, 0-1"},"risks":{"type":"array","items":{"type":"string"},"description":"Risks"},"supportingMetrics":{"type":"array","description":"Supporting Metrics","items":{"type":"object","properties":{"name":{"type":"string"},"value":{"type":"string"}}}},"recommendationId":{"type":"string","format":"uuid","description":"Recommendation id"},"partnerId":{"type":"string","format":"uuid","description":"Partner"},"partner":{"type":"string","description":"Partner trading name"},"category":{"type":"string","enum":["commercial","allocation","credit","risk","growth"],"description":"Recommendation category"},"opportunityClass":{"type":"string","enum":["grow","maintain","review","restrict"],"description":"Partner Opportunity Matrix class, from configurable business criteria"},"inputsConsidered":{"type":"array","items":{"type":"string","enum":["partnerProfile","territory","agreements","rates","commission","credit","paymentBehavior","allocation","orders","cancellations","settlement","cases","channelPerformance","historicalTrends"]},"description":"AI Inputs the recommendation drew on"},"scenarioEstimate":{"type":"object","nullable":true,"description":"Scenario Simulation estimate, where the recommendation carries one","properties":{"additionalSales":{"type":"integer"},"revenue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"margin":{"type":"number"},"creditExposure":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"inventoryRisk":{"type":"string"}}},"status":{"type":"string","description":"Recommendation status: open, accepted, modified, rejected, assigned"},"createdAt":{"type":"string","format":"date-time","description":"Generated at"}}},
"PartnerCancellationsRefundsAmendmentsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over control.partner_change_request (PartnerChangeRequest) and the existing subscription state, assembled at read time (data model DM4)","description":"**What Partner Cancellations, Refunds & Amendments displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"originalState":{"type":"string","description":"Audit: original state of the booking (summary)"},"newState":{"type":"string","description":"Audit: new state of the booking (summary)","nullable":true},"requestedBy":{"type":"string","description":"Audit: requesting user"},"reason":{"type":"string","description":"Reason"},"financialImpact":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Financial impact (net change to the partner account)"},"approvedBy":{"type":"string","description":"Approved by","nullable":true},"requestId":{"type":"string","format":"uuid","description":"Amendment request id"},"partnerId":{"type":"string","format":"uuid","description":"Partner"},"partner":{"type":"string","description":"Partner trading name"},"orderId":{"type":"string","format":"uuid","description":"Order"},"orderNumber":{"type":"string","description":"Order number"},"requestType":{"type":"string","enum":["fullCancellation","partialCancellation","dateChange","performanceChange","quantityReduction","productChange","ticketReissue","customerNameChange","refundRequest"],"description":"Request type"},"quantity":{"type":"integer","description":"Tickets affected","nullable":true},"originalValue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Original Value"},"cancellationAllowed":{"type":"boolean","description":"Cancellation/change allowed under the evaluated policy"},"cancellationFee":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Cancellation Fee"},"refundOrCredit":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Refund/Credit to the partner"},"allocationImpact":{"type":"integer","description":"Allocation impact, units returned (+) or taken (-)"},"commissionAdjustment":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Commission Adjustment"},"approvalReasons":{"type":"array","items":{"type":"string","enum":["transactionValue","eventProximity","cancellationPercentage","partnerStatus","exceptionRequest"]},"description":"Why approval is required; empty when none"},"status":{"type":"string","description":"Status: requested, pendingApproval, approved, rejected, processed"},"requestedAt":{"type":"string","format":"date-time","description":"Requested at"},"aiInsights":{"type":"array","items":{"type":"string"},"description":"Advisory AI unusual-cancellation-pattern flags"}}},
"PartnerCase": {"type":"object","x-ticvai-persistence":"control.partner_case","description":"A partner dispute or service case: category, priority, what it relates to, the amount in dispute, the evidence, the owner and the SLA. Partner cases stay apart from `marketing.case`, which is a guest's service case with a guest lifecycle (decided 29 September, data model DM4)\n\n**Written by** createPartnerCase and actOnPartnerCase (assign, investigate, wait on the partner or a team, propose, accept or reject a resolution, reopen, close) (decided 29 September, writers pass; DM4).","required":["id","partnerId","category","priority","description","status","resolutionTargetAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"partnerId":{"type":"string","format":"uuid","description":"The partner (control.partner)."},"contactId":{"type":"string","format":"uuid","nullable":true,"description":"Partner contact (control.partner_contact)."},"category":{"type":"string","enum":["bookingDispute","pricingDispute","commissionDispute","creditDispute","invoiceDispute","cancellationDispute","ticketIssue","allocationIssue","apiIssue","settlementDispute"],"description":"Category."},"priority":{"type":"string","enum":["low","medium","high","urgent"],"description":"Priority (decided 29 September, readiness close-out)."},"orderId":{"type":"string","format":"uuid","nullable":true,"description":"Related order (orders.sales_order)."},"invoiceReference":{"type":"string","nullable":true,"description":"Related invoice number."},"settlementBatchId":{"type":"string","format":"uuid","nullable":true,"description":"Related settlement (control.partner_settlement_batch)."},"amountInDispute":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Amount in dispute."},"description":{"type":"string","description":"Description."},"evidence":{"type":"array","items":{"type":"string"},"description":"Evidence: attachment references."},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Owner, a staff principal."},"slaPolicyId":{"x-ticvai-references":"approvals.sla_policy","type":"string","format":"uuid","nullable":true,"description":"The SLA policy applied (approvals.sla_policy, the approvals engine's ApprovalSlaPolicy), which sets the first-response and resolution targets and the reminder/breach behaviour; `resolutionTargetAt` is computed from it when the case is opened. Replaces the free-text `slaPolicy` (decided 29 September, writers pass; DM4)"},"status":{"type":"string","enum":["open","assigned","investigating","waitingPartner","waitingInternal","resolutionProposed","resolved","closed"],"default":"open","readOnly":true,"description":"Status (states/partner-case.yaml). Created `open` by createPartnerCase and moved only by actOnPartnerCase (decided 29 September, writers pass; DM4)"},"firstResponseAt":{"type":"string","format":"date-time","nullable":true,"description":"First response at."},"resolutionTargetAt":{"type":"string","format":"date-time","readOnly":true,"description":"Resolution target, computed from the SLA policy (`slaPolicyId`) when the case is opened; time in `waitingPartner` extends it (decided 29 September, writers pass; DM4)"},"resolvedAt":{"type":"string","format":"date-time","nullable":true,"description":"Resolved at."},"scopePath":{"type":"string","description":"The partition key (ADR-0005), written at `tenant` scope."},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"PartnerChangeRequest": {"type":"object","x-ticvai-persistence":"control.partner_change_request","description":"A partner's request to cancel or amend a booking, with the outcome the policy evaluated: whether it is allowed, the fee, the refund or credit, and the allocation and commission impact. A refund it produces is an `orders.refund`; this row is the request and its evaluation (decided 29 September, data model DM4)\n\n**Written by** createPartnerChangeRequest, which creates the row and evaluates it against policy in the same call; approval, where needed, is decided in approvals and the order change is carried out in orders (decided 29 September, writers pass; DM4).","required":["id","partnerId","orderId","requestType","status","requestedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"partnerId":{"type":"string","format":"uuid","description":"The partner (control.partner)."},"orderId":{"type":"string","format":"uuid","description":"Order (orders.sales_order)."},"requestType":{"type":"string","enum":["fullCancellation","partialCancellation","dateChange","performanceChange","quantityReduction","productChange","ticketReissue","customerNameChange","refundRequest"],"description":"Request type."},"quantity":{"type":"integer","minimum":0,"nullable":true,"description":"Tickets affected."},"reason":{"type":"string","nullable":true,"description":"Reason."},"originalState":{"type":"string","description":"Audit: original state of the booking (summary)."},"newState":{"type":"string","nullable":true,"description":"Audit: new state of the booking (summary)."},"originalValue":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Original value."},"cancellationAllowed":{"type":"boolean","description":"Cancellation/change allowed under the evaluated policy."},"cancellationFee":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Cancellation fee."},"refundOrCredit":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Refund/credit to the partner."},"financialImpact":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Net change to the partner account."},"allocationImpact":{"type":"integer","nullable":true,"description":"Allocation impact, units returned (+) or taken (-)."},"commissionAdjustment":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Commission adjustment."},"approvalReasons":{"type":"array","items":{"type":"string","enum":["transactionValue","eventProximity","cancellationPercentage","partnerStatus","exceptionRequest"]},"description":"Why approval is required; empty when none."},"status":{"type":"string","enum":["requested","pendingApproval","approved","rejected","processed"],"default":"requested","description":"Status."},"requestedByPrincipalId":{"type":"string","format":"uuid","description":"Requesting user."},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Approver."},"approvalRequestId":{"type":"string","nullable":true,"readOnly":true,"description":"Approval request, when one was needed."},"refundId":{"type":"string","format":"uuid","nullable":true,"description":"The refund it produced (orders.refund), once processed."},"requestedAt":{"type":"string","format":"date-time","description":"Requested at."},"targetPerformanceId":{"type":"string","format":"uuid","nullable":true,"description":"The performance (catalogue.performance) asked for, for dateChange and performanceChange (decided 29 September, writers pass; DM4)"},"targetProductId":{"type":"string","format":"uuid","nullable":true,"description":"The product (catalogue.product) asked for, for productChange (decided 29 September, writers pass; DM4)"},"newCustomerName":{"type":"string","nullable":true,"description":"The name asked for, for customerNameChange (decided 29 September, writers pass; DM4)"},"feeWaiverRequested":{"type":"boolean","default":false,"description":"The partner asks for the cancellation fee to be waived; a waiver always needs approval (`approvalReasons` gains exceptionRequest) (decided 29 September, writers pass; DM4)"},"scopePath":{"type":"string","description":"The partition key (ADR-0005), written at `tenant` scope."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"PartnerChangeRequestInput": {"type":"object","x-ticvai-persistence":"none — request only; stored as control.partner_change_request (PartnerChangeRequest) with its evaluation (decided 29 September, writers pass; DM4)","description":"What a partner sends to cancel or amend a booking (createPartnerChangeRequest). The evaluation (allowed, fee, refund, impacts, status) is computed, never sent (decided 29 September, writers pass; DM4)","required":["orderId","requestType"],"properties":{"orderId":{"type":"string","format":"uuid","description":"The partner's order (orders.sales_order)"},"requestType":{"type":"string","enum":["fullCancellation","partialCancellation","dateChange","performanceChange","quantityReduction","productChange","ticketReissue","customerNameChange","refundRequest"]},"quantity":{"type":"integer","minimum":1,"nullable":true,"description":"Tickets affected; required for partialCancellation and quantityReduction"},"targetPerformanceId":{"type":"string","format":"uuid","nullable":true,"description":"Required for dateChange and performanceChange"},"targetProductId":{"type":"string","format":"uuid","nullable":true,"description":"Required for productChange"},"newCustomerName":{"type":"string","nullable":true,"description":"Required for customerNameChange"},"feeWaiverRequested":{"type":"boolean","default":false},"reason":{"type":"string","nullable":true}}},
"PartnerDisputesCasesServiceManagementView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over control.partner_case (PartnerCase) and the existing subscription state, assembled at read time (data model DM4)","description":"**What Partner Disputes, Cases & Service Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"caseId":{"type":"string","description":"Case ID"},"partner":{"type":"string","description":"Partner trading name"},"contact":{"type":"string","description":"Partner contact","nullable":true},"category":{"type":"string","enum":["bookingDispute","pricingDispute","commissionDispute","creditDispute","invoiceDispute","cancellationDispute","ticketIssue","allocationIssue","apiIssue","settlementDispute"],"description":"Category (Case Types)"},"priority":{"type":"string","enum":["low","medium","high","urgent"],"description":"Priority (decided 29 September, readiness close-out)"},"relatedOrder":{"type":"string","description":"Related Order","nullable":true},"relatedInvoice":{"type":"string","description":"Related Invoice","nullable":true},"relatedSettlement":{"type":"string","description":"Related Settlement","nullable":true},"amountInDispute":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Amount in Dispute"},"description":{"type":"string","description":"Description"},"evidence":{"type":"array","items":{"type":"string"},"description":"Evidence: attachment references"},"owner":{"type":"string","description":"Owner","nullable":true},"sla":{"type":"string","description":"SLA policy applied"},"status":{"type":"string","description":"Status: open, assigned, investigating, waitingPartner, waitingInternal, resolutionProposed, resolved, closed"},"firstResponse":{"type":"string","format":"date-time","description":"First Response at","nullable":true},"resolutionTarget":{"type":"string","format":"date-time","description":"Resolution Target"},"timeOpen":{"type":"integer","description":"Time Open, hours"},"slaBreach":{"type":"boolean","description":"SLA Breach"},"partnerId":{"type":"string","format":"uuid","description":"Partner"},"aiSummary":{"type":"string","description":"Advisory AI case summary","nullable":true}}},
"PartnerManagementCommandCenterSummary": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection; the headline tiles over the list, computed at read time for the filters in force","description":"**The headline figures on Partner Management Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.","properties":{"totalPartners":{"type":"integer","description":"Total Partners"},"activePartners":{"type":"integer","description":"Active Partners"},"pendingOnboarding":{"type":"integer","description":"Pending Onboarding"},"pendingApproval":{"type":"integer","description":"Pending Approval"},"suspendedPartners":{"type":"integer","description":"Suspended Partners"},"expiringAgreements":{"type":"integer","description":"Expiring Agreements: partners whose active agreement ends within its expiryAlertDays (default 30) (decided 29 September, readiness close-out)"},"documentationIssues":{"type":"integer","description":"Documentation Issues: partners with a mandatory document missing, rejected, expiring or expired"},"partnersWithCreditHolds":{"type":"integer","description":"Partners With Credit Holds: partners whose credit status is onHold or blocked"},"connectedOtaApiPartners":{"type":"integer","description":"Connected OTA/API Partners"},"partnerSalesYtd":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Partner Sales YTD: gross value of partner orders this calendar year (decided 29 September, readiness close-out)"},"partnerRevenueYtd":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Partner Revenue YTD: partner sales net of commission this calendar year (decided 29 September, readiness close-out)"},"highRiskPartners":{"type":"integer","description":"High-Risk Partners"}}},
"PartnerManagementCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over control.partner (Partner), control.partner_credit_profile, control.partner_application, control.partner_scope_assignment and control.partner_distribution_right and the existing subscription state, assembled at read time (data model DM4)","description":"**What Partner Management Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"partnerId":{"type":"string","format":"uuid","description":"Partner ID"},"tradingName":{"type":"string","description":"Trading Name"},"legalEntity":{"type":"string","description":"Legal Entity"},"partnerType":{"type":"string","description":"Partner type code from the tenant's configurable partner-type list (MoM 31 Aug 4.3: configurable category/type), seeded with the pack's p.7 list: b2bReseller, travelAgent, tourOperator, ota, corporateCustomer, hotelConcierge, destinationManagementCompany, affiliate, wholesaler, distributor, governmentPartner, schoolInstitution, apiPartner, internalGroupCompany"},"country":{"type":"string","description":"Country, ISO 3166-1 alpha-2"},"territory":{"type":"string","description":"Territory: summary of the authorised markets (listTerritoryMarketDistribution)"},"assignedBrands":{"type":"array","items":{"type":"string"},"description":"Assigned Brand/Venue: brand names in the partner's business scope (setPartnerBrandVenue)"},"assignedVenues":{"type":"array","items":{"type":"string"},"description":"Assigned Brand/Venue: venue names in the partner's business scope (setPartnerBrandVenue)"},"commercialOwner":{"type":"string","description":"Commercial Owner: staff display name of the account manager"},"distributionChannel":{"type":"array","items":{"type":"string","enum":["b2bPortal","api","otaConnection","agentPortal","affiliateLink","voucherDistribution","bulkTicketExport","other"]},"description":"Distribution Channel: Distribution methods: b2bPortal (the TICVAI B2B portal), api (partner consumes the TICVAI API), otaConnection (TICVAI integrates into the OTA, either direction per MoM 31 Aug 4.3), agentPortal, affiliateLink, voucherDistribution, bulkTicketExport (pre-generated QR tickets as CSV, MoM 5 Aug option 3), other"},"accountStatus":{"type":"string","description":"Account Status: lead, applicant, underReview, approved, configuration, active, restricted, suspended, terminated or archived (pack p.6 and p.18 merged with MoM 31 Aug 4.3 lead -> submitted -> active -> suspended; \"submitted\" is applicant)"},"onboardingStatus":{"type":"string","description":"Onboarding Status: the application stage (application, businessVerification, documentation, commercialReview, financeReview, technicalReview, approval, configuration, activation) or complete"},"agreementStatus":{"allOf":[{"$ref":"#/components/schemas/PartnerAgreementStatus"}],"nullable":true,"description":"Agreement Status of the partner's current agreement; empty when none"},"creditStatus":{"type":"string","description":"Credit Status: notEnabled, withinLimit, warning (at the warning threshold), highRisk, onHold or blocked (decided 29 September, readiness close-out)"},"integrationStatus":{"type":"string","enum":["none","testing","connected","degraded","disconnected"],"x-ticvai-persisted":false,"description":"Integration Status: none, testing, connected, degraded or disconnected (decided 29 September, readiness close-out). **Derived at read time, not a column** (decided 29 September, writers pass; DM4), from the partner's OTA/API channel listings (control.channel_listing) and the health of its API clients (control.api_client, with webhook deliveries in control.webhook_delivery), first match wins: `none` when the partner has no channel listing and no API client; `disconnected` when every listing is `paused` or `delisted` or every production API client is `suspended` or `revoked`; `degraded` when a `live` listing's `lastPushedAt` is older than twice its `pushIntervalMinutes`, or webhook deliveries to the partner failed in the last hour; `connected` when a `live` listing or an `active` production client exists and none of the above holds; otherwise `testing` (only `draft` listings or only sandbox clients). The thresholds are proposed, the venue may correct them."},"lastActivity":{"type":"string","format":"date-time","description":"Last Activity"},"riskRating":{"type":"string","enum":["low","medium","high","critical"],"description":"Risk rating, Low / Medium / High / Critical (pack p.58); drives the Risk filter and the High-Risk Partners KPI"},"aiInsights":{"type":"array","items":{"type":"string"},"description":"Partner Attention Required: advisory AI flags such as an agreement expiring against forward bookings (pack p.6)"}}},
"PartnerOperationsCommandCenterSummary": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection; the headline tiles over the list, computed at read time for the filters in force","description":"**The headline figures on Partner Operations Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.","properties":{"partnerSalesToday":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Partner Sales Today"},"partnerSalesMtd":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Partner Sales MTD"},"activePartnerOrders":{"type":"integer","description":"Active Partner Orders"},"activeReservations":{"type":"integer","description":"Active Reservations"},"activeHolds":{"type":"integer","description":"Active Holds"},"ticketsSold":{"type":"integer","description":"Tickets Sold"},"cancellations":{"type":"integer","description":"Cancellations"},"refunds":{"type":"integer","description":"Refunds"},"outstandingReceivables":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Outstanding Receivables"},"commissionPayable":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Commission Payable"},"pendingSettlements":{"type":"integer","description":"Pending Settlements"},"operationalExceptions":{"type":"integer","description":"Operational Exceptions"},"partnersRequiringAttention":{"type":"integer","description":"Partners Requiring Attention"},"activityFeed":{"type":"array","description":"Activity Feed: recent partner events, newest first","items":{"type":"object","properties":{"at":{"type":"string","format":"date-time"},"partnerId":{"type":"string","format":"uuid"},"message":{"type":"string"}}}}}},
"PartnerOperationsCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over subscription state, assembled at read time from tables that already exist","description":"**What Partner Operations Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"partner":{"type":"string","description":"Partner trading name"},"partnerType":{"type":"string","description":"Partner Type code"},"accountManager":{"type":"string","description":"Account Manager"},"orders":{"type":"integer","description":"Orders"},"tickets":{"type":"integer","description":"Tickets"},"grossSales":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Gross Sales"},"netSales":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Net Sales"},"commission":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Commission"},"outstandingBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Outstanding Balance"},"creditUtilization":{"type":"number","description":"Credit Utilization, percent"},"allocationUtilization":{"type":"number","description":"Allocation Utilization, percent"},"cancellationRate":{"type":"number","description":"Cancellation Rate, percent"},"operationalStatus":{"type":"string","description":"Operational Status: normal, attention, restricted, suspended"},"risk":{"type":"string","enum":["low","medium","high","critical"],"description":"Risk"},"partnerId":{"type":"string","format":"uuid","description":"Partner"},"aiInsights":{"type":"array","items":{"type":"string"},"description":"Advisory AI attention flags for this partner"}}},
"PartnerOrdersBookingManagementView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over subscription state, assembled at read time from tables that already exist","description":"**What Partner Orders & Booking Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"partnerReference":{"type":"string","description":"Partner Reference"},"agentUser":{"type":"string","description":"Agent/User"},"customerName":{"type":"string","description":"Customer/Guest where applicable","nullable":true},"products":{"type":"array","items":{"type":"string"},"description":"Products"},"quantity":{"type":"integer","description":"Quantity"},"grossValue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Gross Value"},"partnerRate":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Partner Rate applied"},"commission":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Commission"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Net Amount"},"paymentMethod":{"type":"string","enum":["creditAccount","prepaid","card"],"description":"Payment Method (the three payment models)"},"billingStatus":{"type":"string","description":"Billing Status: unbilled, invoiced, paid, overdue or credited"},"fulfillmentStatus":{"type":"string","description":"Fulfillment Status: pending, partiallyIssued, issued or delivered"},"orderId":{"type":"string","format":"uuid","description":"TICVAI Order ID"},"orderNumber":{"type":"string","description":"TICVAI order number"},"partnerId":{"type":"string","format":"uuid","description":"Partner"},"partnerName":{"type":"string","description":"Partner"},"bookingDate":{"type":"string","format":"date-time","description":"Booking Date"},"event":{"type":"string","description":"Event","nullable":true},"visitDate":{"type":"string","format":"date","description":"Visit/Event Date","nullable":true},"orderStatus":{"type":"string","description":"Order status: draft, held, confirmed, partiallyFulfilled, fulfilled, cancelled, refunded, failed"},"salesChannel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel","description":"Channel"}}},
"PartnerPerformanceScorecardRiskMonitoringView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over control.partner, control.partner_document, control.partner_security, control.partner_allocation and control.partner_case and the existing subscription state, assembled at read time (data model DM4)","description":"**What Partner Performance Scorecard & Risk Monitoring displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"sales":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Commercial: gross sales"},"revenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Commercial: revenue net of commission"},"growth":{"type":"number","description":"Commercial: growth against the previous period, percent"},"margin":{"type":"number","description":"Commercial: margin, percent"},"averageOrderValue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Commercial: average order value"},"utilization":{"type":"number","description":"Allocation: utilisation, percent"},"sellThrough":{"type":"number","description":"Allocation: sell-through, percent"},"returnedInventory":{"type":"integer","description":"Allocation: returned inventory, units"},"averagePaymentDelayDays":{"type":"number","description":"Financial: average payment delay, days"},"creditUtilization":{"type":"number","description":"Financial: credit utilisation, percent"},"overdueBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Financial: overdue balance"},"cancellationRate":{"type":"number","description":"Operational: cancellation rate, percent"},"errorRate":{"type":"number","description":"Operational: error rate, percent"},"supportCases":{"type":"integer","description":"Operational: support cases"},"apiSuccessRate":{"type":"number","description":"Technical: API success rate, percent","nullable":true},"transactionFailureRate":{"type":"number","description":"Technical: transaction failure rate, percent","nullable":true},"documentation":{"type":"string","description":"Compliance: documentation state, compliant, expiring, incomplete or nonCompliant"},"agreementStatus":{"allOf":[{"$ref":"#/components/schemas/PartnerAgreementStatus"}],"nullable":true,"description":"Compliance: agreement status"},"securityGuaranteeStatus":{"type":"string","description":"Compliance: security/guarantee state, covered, partiallyCovered, expired or notRequired"},"partnerId":{"type":"string","format":"uuid","description":"Partner"},"partner":{"type":"string","description":"Partner trading name"},"partnerType":{"type":"string","description":"Partner Type code"},"period":{"type":"string","description":"Scorecard period, e.g. 2026-09"},"refundRate":{"type":"number","description":"Operational: refund rate, percent"},"syncReliability":{"type":"number","description":"Technical: sync reliability, percent","nullable":true},"overallScore":{"type":"integer","description":"Partner Score, 0-100"},"dimensionScores":{"type":"object","description":"Score by dimension, each 0-100","properties":{"commercial":{"type":"integer"},"financial":{"type":"integer"},"allocation":{"type":"integer"},"operational":{"type":"integer"},"technical":{"type":"integer"},"compliance":{"type":"integer"}}},"riskRating":{"type":"string","enum":["low","medium","high","critical"],"description":"Risk Rating"},"trend":{"type":"string","enum":["improving","stable","declining"],"description":"Trend"},"benchmark":{"type":"object","description":"Benchmarking: average overall score of the comparison groups","properties":{"samePartnerType":{"type":"number"},"sameMarket":{"type":"number"},"sameChannel":{"type":"number"},"portfolioAverage":{"type":"number"}}},"aiInsights":{"type":"array","items":{"type":"string"},"description":"Advisory AI risk detection"}}},
"PartnerStatementAccountActivitySummary": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection; the headline tiles over the list, computed at read time for the filters in force","description":"**The headline figures on Partner Statement & Account Activity.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.","properties":{"openingBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Opening Balance"},"sales":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Sales"},"payments":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Payments"},"credits":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Credits"},"refunds":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Refunds"},"commission":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Commission"},"adjustments":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Adjustments"},"closingBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Closing Balance"},"overdueBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Overdue Balance"},"availableCredit":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Available Credit"},"current":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Aging: current (not yet due)"},"aged1To30":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Aging: 1-30 days"},"aged31To60":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Aging: 31-60 days"},"aged61To90":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Aging: 61-90 days"},"aged90Plus":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Aging: 90+ days"}}},
"PartnerStatementAccountActivityView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over subscription state, assembled at read time from tables that already exist","description":"**What Partner Statement & Account Activity displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"date":{"type":"string","format":"date","description":"Date"},"transactionType":{"type":"string","enum":["booking","invoice","payment","refund","creditNote","commission","manualAdjustment","deposit","settlement"],"description":"Transaction Type"},"reference":{"type":"string","description":"Reference"},"orderInvoice":{"type":"string","description":"Order/Invoice number","nullable":true},"debit":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Debit"},"credit":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Credit"},"runningBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Running Balance"},"dueDate":{"type":"string","format":"date","description":"Due Date","nullable":true},"status":{"type":"string","description":"Status: open, partiallyPaid, paid, overdue or void"}}},
"ReservationsHoldsReleaseManagementSummary": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection; the headline tiles over the list, computed at read time for the filters in force","description":"**The headline figures on Reservations, Holds & Release Management.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.","properties":{"activeHolds":{"type":"integer","description":"Active Holds"},"heldTickets":{"type":"integer","description":"Held Tickets"},"heldValue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Held Value"},"expiringToday":{"type":"integer","description":"Expiring Today"},"expiredHolds":{"type":"integer","description":"Expired Holds"},"convertedHolds":{"type":"integer","description":"Converted Holds"},"releasedInventory":{"type":"integer","description":"Released Inventory, tickets"}}},
"ReservationsHoldsReleaseManagementView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over subscription state, assembled at read time from tables that already exist","description":"**What Reservations, Holds & Release Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"holdId":{"type":"string","format":"uuid","description":"Hold ID"},"partner":{"type":"string","description":"Partner trading name"},"event":{"type":"string","description":"Event"},"product":{"type":"string","description":"Product"},"quantity":{"type":"integer","description":"Quantity"},"seatZone":{"type":"string","description":"Seat/Zone where applicable","nullable":true},"holdCreatedAt":{"type":"string","format":"date-time","description":"Hold Created"},"holdExpiresAt":{"type":"string","format":"date-time","description":"Hold Expiry"},"createdBy":{"type":"string","format":"date-time","description":"Created By"},"commercialValue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Commercial Value"},"allocationSource":{"type":"string","enum":["partnerAllocation","channelAllocation","generalCapacity"],"description":"Allocation Source"},"status":{"type":"string","description":"Status: active, extended, converted, released, expired"},"extensionsUsed":{"type":"integer","description":"Extensions used so far"},"partnerId":{"type":"string","format":"uuid","description":"Partner"},"aiInsights":{"type":"array","items":{"type":"string"},"description":"Advisory AI conversion-probability and release suggestions"}}}
}
```
