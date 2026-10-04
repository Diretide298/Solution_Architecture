# WS22 — B2B, Reseller & OTA Partner Management board 2

**6 screens · 8 operations · 16 schemas · 2 permissions**

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

- **Every control that can be refused must be gated.** 2 permissions apply here:
  `PLATFORM_CELL_MANAGE, PLATFORM_TENANT_VIEW`. A control nobody can use must say so,
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
| `PTR-032` | Commercial Agreement Command Center | B | 2 | 30 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `PTR-033` | Agreement & Contract Terms Builder | B | 26 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `PTR-034` | Partner Rate & Net Pricing Configuration | B | 10 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `PTR-038` | Payment Terms, Billing & Account Configuration | B | 1 | 14 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `PTR-040` | Booking Limits, Commercial Exceptions & Approval | B | 22 | 0 | 5 | 0 | 1 | 6 | — | notStarted (generated) |
| `PTR-041` | Commercial Agreement 360°, Health & AI Review | B | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**PTR-038, PTR-041 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `PTR-032` Commercial Agreement Command Center

**Provide commercial and finance teams with a centralized view of all partner agreements and their current commercial health.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | Block B · ticket #29555 (APP-PARTNER-PTR-032) |
| Who uses it | partner staff holding `PLATFORM_TENANT_VIEW` (1 read); in the flows as partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each agreement should show) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/partners/commercial-agreement-command-center-ptr-032` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** All partner agreements and their commercial health: expiring, on credit hold, exposure, receivables.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SOT-015).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search commercial agreement | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by partner, partner type, brand, venue, country, agreement type and 5 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Partner type | text field | — | — | `listCommercialAgreement` ?partnerType |
| Brand | text field | — | — | `listCommercialAgreement` ?brand |
| Venue | text field | — | — | `listCommercialAgreement` ?venue |
| Country | text field | — | — | `listCommercialAgreement` ?country |
| Status | select | — | Pending approval · Active · Expiring soon · Expired · Suspended · Terminated | `listCommercialAgreement` ?status |
| Risk | radio group | — | Low · Medium · High · Critical | `listCommercialAgreement` ?risk |
| Credit status | select | — | Not enabled · Within limit · Warning · High risk · On hold · Blocked | `listCommercialAgreement` ?creditStatus |
| Expiring within days | number field (days) | — | — | `listCommercialAgreement` ?expiringWithinDays |
| Partner | picker: choose a partner | — | — | `listCommercialAgreement` ?partnerId |
| Agreement type | text field | — | — | `listCommercialAgreement` ?agreementType |
| Commercial owner | text field | — | — | `listCommercialAgreement` ?commercialOwner |
| Partner | picker: choose a partner | — | — | `listCommercialAgreementHealth` ?partnerId |
| Agreement | picker: choose an agreement | — | — | `listCommercialAgreementHealth` ?agreementId |
| Status | select | — | Pending approval · Active · Expiring soon · Expired · Suspended · Terminated | `listCommercialAgreementHealth` ?status |
| Risk | radio group | — | Low · Medium · High · Critical | `listCommercialAgreementHealth` ?risk |

#### Outputs: what the screen shows and produces

**Shown**

**Active Agreements** (metric tile)

**Draft Agreements** (metric tile)

**Pending Approval** (metric tile)

**Agreements Expiring Soon** (metric tile)

**Expired Agreements** (metric tile)

**Partners on Credit Hold** (metric tile)

**Total Approved Credit** (metric tile)

**Current Credit Exposure** (metric tile)

**Outstanding Receivables** (metric tile)

**Active Commercial Allocations** (metric tile)

**Agreements With Exceptions** (metric tile)

**Commercial Risk Alerts** (metric tile)

**Every commercial agreement** (data table, from `listCommercialAgreement`)

| Shows | Format | Notes |
|---|---|---|
| Agreement | the name it points at, never the id | Agreement ID |
| Partner | text | Partner trading name |
| Agreement type | text | Agreement Type code, seeded with reseller, ota, travelTrade, corporate, wholesale, affiliate, distribution, apiCommercial (pack p.26) |
| Brand venue | text | Brand/Venue summary of the agreement scope |
| Market | text | Market |
| Valid from | 1 Oct 2026 | Effective From |
| Valid to | 1 Oct 2026 | Effective To; empty for open-ended |
| Pricing model | chip: Retail price, Net rate, Discount from retail, Markup, Derived rate | Pricing Model (pack p.27) |
| Commission model | chip: Fixed percentage, Fixed amount, Product specific, Tiered, Volume based, Revenue … | Commission Model (pack p.29); none for a net-rate agreement |
| Credit term days | 1,234 | Payment Terms in days (0 = due immediately; Net 7/15/30/45 or custom) |
| Credit limit | AED 1,234.50 | Credit Limit; empty unless the payment model is creditAccount |
| Current exposure | AED 1,234.50 | Current Exposure |
| Allocation model | chip: Guaranteed, On request, Shared, Fixed quantity, Percentage, Rolling… | Allocation Model (pack p.35) |
| Agreement status | chip: Pending approval, Active, Expiring soon, Expired, Suspended, Terminated | Agreement Status |
| Commercial owner | text | Commercial Owner |

**The selected commercial agreement** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Agreement | the name it points at, never the id | Agreement ID |
| Partner | text | Partner trading name |
| Agreement type | text | Agreement Type code, seeded with reseller, ota, travelTrade, corporate, wholesale, affiliate, distribution, apiCommercial (pack p.26) |
| Brand venue | text | Brand/Venue summary of the agreement scope |
| Market | text | Market |
| Valid from | 1 Oct 2026 | Effective From |
| Valid to | 1 Oct 2026 | Effective To; empty for open-ended |
| Pricing model | chip: Retail price, Net rate, Discount from retail, Markup, Derived rate | Pricing Model (pack p.27) |
| Commission model | chip: Fixed percentage, Fixed amount, Product specific, Tiered, Volume based, Revenue … | Commission Model (pack p.29); none for a net-rate agreement |
| Credit term days | 1,234 | Payment Terms in days (0 = due immediately; Net 7/15/30/45 or custom) |
| Credit limit | AED 1,234.50 | Credit Limit; empty unless the payment model is creditAccount |
| Current exposure | AED 1,234.50 | Current Exposure |
| Allocation model | chip: Guaranteed, On request, Shared, Fixed quantity, Percentage, Rolling… | Allocation Model (pack p.35) |
| Agreement status | chip: Pending approval, Active, Expiring soon, Expired, Suspended, Terminated | Agreement Status |
| Commercial owner | text | Commercial Owner |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Money columns (creditLimit, currentExposure)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. Across tenants or regions figures in different currencies are never summed into one total; group by currency, or label the converted figure with its rate and time. *(source: ADR-0008; ADR-0011; DI-306)*

**Data it reads**: `listCommercialAgreement` (onLoad, Commercial Agreement Command Center); `listCommercialAgreementHealth` (onLoad, Commercial Agreement 360°, Health & AI Review)

**Where the user goes next**

- → `PTR-033` Agreement & Contract Terms Builder: *Works in Agreement & Contract Terms Builder*; calls `listCommercialAgreement`
- → `PTR-034` Partner Rate & Net Pricing Configuration: *Works in Partner Rate & Net Pricing Configuration*; calls `listCommercialAgreement`
- → `PTR-038` Payment Terms, Billing & Account Configuration: *Works in Payment Terms, Billing & Account Configuration*; calls `listCommercialAgreement`
- → `PTR-040` Booking Limits, Commercial Exceptions & Approval: *Works in Booking Limits, Commercial Exceptions & Approval*; calls `listCommercialAgreement`
- → `PTR-041` Commercial Agreement 360°, Health & AI Review: *Works in Commercial Agreement 360°, Health & AI Review*; calls `listCommercialAgreement`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The commercial agreement list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the commercial agreement untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No commercial agreements yet. Offers no create action here: agreements are drafted on the terms builder (PTR-033). |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the commercial agreement are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
metric tiles:
  Active Agreements: 128
  Draft Agreements: 46
  Pending Approval: 312
  Agreements Expiring Soon: 74
  Expired Agreements: 3
  Partners on Credit Hold: 233
  Total Approved Credit: 57
  Current Credit Exposure: AED 96,750.00
  Outstanding Receivables: AED 12,400.00
  Active Commercial Allocations: 46
Every commercial agreement:
- validFrom: 01/10/2026 09:14
  validTo: 31/12/2026 23:59
- validFrom: 30/09/2026 18:02
  validTo: 15/10/2026 00:00
- validFrom: 28/09/2026 11:45
  validTo: 01/11/2026 06:00
```

#### Permissions

- `listCommercialAgreement` → `PLATFORM_TENANT_VIEW` (read) · partner
- `listCommercialAgreementHealth` → `PLATFORM_TENANT_VIEW` (read) · partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Agreements overview shows active and pending agreements; partner pricing discounts configurable by quantity, amount, percentage or tiered volume bands (e.g. 10% up to 1,000 tickets, 15% from 1,000-5,000); commission rate per ticket sold. *(client request · MoM 31 Aug 2026, 4.4 B2B Commercial Agreements, Credit & Payment Models · DI-554)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-032` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS39 B2B, Reseller & OTA Partner Management Board 2.dc.html#ptr-032`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 2
- Flow F131 *B2B, Reseller & OTA Partner Management board 2: Commercial Agreement Command …*, step 1: Opens Commercial Agreement Command Center → Provide commercial and finance teams with a centralized view of all partner agreements and their current commercial health.
- Flow F131 *B2B, Reseller & OTA Partner Management board 2: Commercial Agreement Command …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F131 *B2B, Reseller & OTA Partner Management board 2: Commercial Agreement Command …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F131 *B2B, Reseller & OTA Partner Management board 2: Commercial Agreement Command …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F131 *B2B, Reseller & OTA Partner Management board 2: Commercial Agreement Command …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F131 branch at step 1 (expected): when Nothing has been set up on Commercial Agreement Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F131 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (30 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-032?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `PTR-033`, `PTR-034`, `PTR-038`, `PTR-040`, `PTR-041`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-033` Agreement & Contract Terms Builder

**Create the structured commercial agreement governing the partner relationship.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | Block B · ticket #29403 (APP-PARTNER-PTR-033) |
| Who uses it | partner staff holding `PLATFORM_CELL_MANAGE` (1 configure); in the flows as partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; Configure/reference) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/partners/agreement-contract-terms-builder-ptr-033` |

**Known gaps.** **The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: Manual Renewal, Renewal Notice Period, Renewal Approval. Each needs an operation, or needs removing from the …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** A partner's structured commercial agreement: type, entity, brand, venue, territory, currency, dates, renewal, payment and commission terms.

**Fixed on main** (the package already carries these; draw what it says): Fields drawn as drop-downs that cannot be choices: text field: Agreement Name, Partner, Contract Reference, Legal Entity, Territory, Credit … (CHG-SOT-015).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Agreement ID | select field | — | — | — | — | — | — |
| Agreement Name | text field | — | — | — | — | — | — |
| Partner | text field | — | — | — | — | — | — |
| Agreement Type | select field | — | — | — | — | — | — |
| Contract Reference | text field | — | — | — | — | — | — |
| Legal Entity | text field | — | — | — | — | — | — |
| Brand | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Territory | text field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Effective From | date picker | — | — | — | — | — | — |
| Effective To | select field | — | — | — | — | — | — |
| Renewal Type | select field | — | — | — | — | — | — |
| Commercial Owner | select field | — | — | — | — | — | — |
| Finance Owner | select field | — | — | — | — | — | — |
| Payment Terms | select field | — | — | — | — | — | — |
| Commission Terms | select field | — | — | — | — | — | — |
| Pricing Basis | select field | — | — | — | — | — | — |
| Credit Terms | text field | — | — | — | — | — | — |
| Allocation Terms | text field | — | — | — | — | — | — |
| Cancellation Conditions | text field | — | — | — | — | — | — |
| Refund Conditions | select field | — | — | — | — | — | — |
| Booking Restrictions | select field | — | — | — | — | — | — |
| Settlement Terms | select field | — | — | — | — | — | — |
| Minimum Commitment | select field | — | — | — | — | — | — |
| Sales Target | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Manual Renewal (primary button) | navigation or local | — | — | — | — |
| Renewal Notice Period (secondary button) | navigation or local | — | — | — | — |
| Renewal Approval (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `PTR-032` Commercial Agreement Command Center: *Returns to the board's landing screen*; calls `setAgreementContractTerm`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The agreement contract terms configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the agreement contract terms untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No agreement contract terms configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
form example:
  Agreement ID: 19
  Agreement Name: 11
  Partner: Arabian Trails
  Agreement Type: 46
  Contract Reference: APR-2026-004797
  Legal Entity: 46
  Brand: 74
  Venue: AquaCove Dubai
  Territory: 46
  Currency: 46
  Effective From: 01/11/2026
  Effective To: 01/11/2026 06:00
  Renewal Type: auto
  Commercial Owner: Fatima Al Mansoori
```

#### Permissions

- `setAgreementContractTerm` → `PLATFORM_CELL_MANAGE` (configure) · partner, prospect

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Agreements overview shows active and pending agreements; partner pricing discounts configurable by quantity, amount, percentage or tiered volume bands (e.g. 10% up to 1,000 tickets, 15% from 1,000-5,000); commission rate per ticket sold. *(client request · MoM 31 Aug 2026, 4.4 B2B Commercial Agreements, Credit & Payment Models · DI-554)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-033` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS39 B2B, Reseller & OTA Partner Management Board 2.dc.html#ptr-033`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 2
- Flow F131 *B2B, Reseller & OTA Partner Management board 2: Commercial Agreement Command …*, step 2: Works in Agreement & Contract Terms Builder → Create the structured commercial agreement governing the partner relationship.

#### Acceptance for the design

- [ ] Every input above is drawn (26), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-033?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Manual Renewal, Renewal Notice Period, Renewal Approval.
- [ ] Every transition is wired: `PTR-032`.
- [ ] Every gated control is gated: `PLATFORM_CELL_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-034` Partner Rate & Net Pricing Configuration

**Define the commercial pricing basis available to a partner without recreating TICVAI's Pricing Engine.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | Block B · ticket #29409 (APP-PARTNER-PTR-034) |
| Who uses it | partner staff holding `PLATFORM_CELL_MANAGE` (1 configure); in the flows as partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure by) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/partners/partner-rate-net-pricing-configuration-ptr-034` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The partner's net price basis per product, venue, event, ticket type, market and channel, without recreating the pricing engine.

**Fixed on main** (the package already carries these; draw what it says): Fields drawn as drop-downs that cannot be choices: text field: Partner, Agreement, Product Family, Ticket Type, Price Category, Market. (CHG-SOT-015).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Partner | text field | — | — | — | — | — | — |
| Agreement | text field | — | — | — | — | — | — |
| Product | select field | — | — | — | — | — | — |
| Product Family | text field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Event | select field | — | — | — | — | — | — |
| Ticket Type | text field | — | — | — | — | — | — |
| Price Category | text field | — | — | — | — | — | — |
| Market | text field | — | — | — | — | — | — |
| Channel | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `PTR-032` Commercial Agreement Command Center: *Returns to the board's landing screen*; calls `setPartnerRateNet`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The partner rate net configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partner rate net untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No partner rate net configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `PTR-011`: Quotes use these net prices.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
form example:
  Partner: Marina Leisure Group
  Agreement: 312
  Product: 46
  Product Family: 46
  Venue: AquaCove Dubai
  Event: 312
  Ticket Type: 46
  Price Category: AED 482,300.00
  Market: 57
  Channel: 128
```

#### Permissions

- `setPartnerRateNet` → `PLATFORM_CELL_MANAGE` (configure) · partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Agreements overview shows active and pending agreements; partner pricing discounts configurable by quantity, amount, percentage or tiered volume bands (e.g. 10% up to 1,000 tickets, 15% from 1,000-5,000); commission rate per ticket sold. *(client request · MoM 31 Aug 2026, 4.4 B2B Commercial Agreements, Credit & Payment Models · DI-554)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-034` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS39 B2B, Reseller & OTA Partner Management Board 2.dc.html#ptr-034`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 2
- Flow F131 *B2B, Reseller & OTA Partner Management board 2: Commercial Agreement Command …*, step 4: Works in Partner Rate & Net Pricing Configuration → Define the commercial pricing basis available to a partner without recreating TICVAI's Pricing Engine.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-034?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `PTR-032`.
- [ ] Every gated control is gated: `PLATFORM_CELL_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-038` Payment Terms, Billing & Account Configuration

**Define how the partner pays TICVAI and how transactions are financially grouped.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | Block B · ticket #29410 (APP-PARTNER-PTR-038) |
| Who uses it | partner staff holding `PLATFORM_CELL_MANAGE` (1 configure); in the flows as partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/partners/payment-terms-billing-account-configuration-ptr-038` |

**Known gaps.** **The pack names 8 actions on this screen and the screen declares 1 operation.** Unserved: Immediate Payment, Credit Account, Deposit Balance, Bank Transfer, Card, Prepaid Balance, Other approved …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** How a partner pays and how transactions are grouped for billing.

**Fixed on main** (the package already carries these; draw what it says): Payment methods drawn as buttons. (CHG-SOT-015).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Accepted payment methods | multi select | — | — | — | — | The payment methods this partner account may use. Options: Immediate Payment; Credit Account; Deposit Balance; Bank Transfer; Card; Payment Link; Prepaid Balance; Other approved method. | — |

#### Outputs: what the screen shows and produces

**Shown**

**Every payment terms billing** (data table, from `setPaymentTermBilling`)

| Shows | Format | Notes |
|---|---|---|
| Current balance | AED 1,234.50 | Current Balance |
| Outstanding | AED 1,234.50 | Outstanding |
| Overdue | AED 1,234.50 | Overdue |
| Available credit | AED 1,234.50 | Available Credit |
| Last payment | 1 Oct 2026 | Last Payment date |
| Next invoice | 1 Oct 2026 | Next Invoice date |
| Oldest outstanding invoice | 1 Oct 2026 | Due date of the Oldest Outstanding Invoice |

**The selected payment terms billing** (detail panel): The pack groups this record's detail under its own headings: “Important Boundary”.

| Shows | Format | Notes |
|---|---|---|
| Current balance | AED 1,234.50 | Current Balance |
| Outstanding | AED 1,234.50 | Outstanding |
| Overdue | AED 1,234.50 | Overdue |
| Available credit | AED 1,234.50 | Available Credit |
| Last payment | 1 Oct 2026 | Last Payment date |
| Next invoice | 1 Oct 2026 | Next Invoice date |
| Oldest outstanding invoice | 1 Oct 2026 | Due date of the Oldest Outstanding Invoice |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Money columns (currentBalance)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. Across tenants or regions figures in different currencies are never summed into one total; group by currency, or label the converted figure with its rate and time. *(source: ADR-0008; ADR-0011; DI-306)*

**Where the user goes next**

- → `PTR-032` Commercial Agreement Command Center: *Returns to the board's landing screen*; calls `setPaymentTermBilling`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The payment terms billing list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the payment terms billing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No payment terms billing yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the payment terms billing are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
partner: Desert Gate Tours LLC
paymentTerms: 30 days
methods:
- Credit account
- Bank transfer
outstanding: AED 64,200.00
```

#### Permissions

- `setPaymentTermBilling` → `PLATFORM_CELL_MANAGE` (configure) · partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Three partner payment models: (1) credit limit, invoiced monthly and settled by cheque/bank transfer; (2) prepayment wallet funded by bank transfer or online top-up and drawn down per sale; (3) pay-per-transaction by card. *(agreed · MoM 31 Aug 2026, 4.4 B2B Commercial Agreements, Credit & Payment Models · DI-555)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-038` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS39 B2B, Reseller & OTA Partner Management Board 2.dc.html#ptr-038`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 2
- Flow F131 *B2B, Reseller & OTA Partner Management board 2: Commercial Agreement Command …*, step 6: Works in Payment Terms, Billing & Account Configuration → Define how the partner pays TICVAI and how transactions are financially grouped.

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state.
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-038?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `PTR-032`.
- [ ] Every gated control is gated: `PLATFORM_CELL_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-040` Booking Limits, Commercial Exceptions & Approval

**Control transaction limits and provide a governed mechanism for commercial exceptions.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | Block B · ticket #29100 (APP-PARTNER-PTR-040) |
| Who uses it | partner staff holding `PLATFORM_CELL_MANAGE` (1 configure); in the flows as partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `challengeId` (navigation) |
| Route | `/partners/booking-limits-commercial-exceptions-approval-ptr-040` |

**Known gaps.** **The pack names 4 actions on this screen and the screen declares 1 operation.** Unserved: Price Exception, Credit Exception, Allocation Exception. Each needs an operation, or needs removing from the …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Partner booking limits and governed commercial exceptions (price, credit, allocation, limit); approving an exception requires a second factor.

**Fixed on main** (the package already carries these; draw what it says): Reaches approveBookingLimitCommercial (step-up mfa) and declares no way to raise the challenge. (CHG-SOT-015); Fields drawn as drop-downs that cannot be choices: text field: Agreement, Current Rule, Requested Exception, Reason. (CHG-SOT-015); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SOT-015).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Maximum Tickets Per Booking | text field | — | — | — | — | — | — |
| Maximum Booking Value | select field | — | — | — | — | — | — |
| Daily Booking Limit | select field | — | — | — | — | — | — |
| Monthly Booking Limit | select field | — | — | — | — | — | — |
| Event Limit | select field | — | — | — | — | — | — |
| Product Limit | select field | — | — | — | — | — | — |
| Hold Limit | select field | — | — | — | — | — | — |
| Reservation Duration | select field | — | — | — | — | — | — |
| Cancellation Limit | select field | — | — | — | — | — | — |
| Partner | select field | — | — | — | — | — | — |
| Agreement | text field | — | — | — | — | — | — |
| Request Type | select field | — | — | — | — | — | — |
| Current Rule | text field | — | — | — | — | — | — |
| Requested Exception | text field | — | — | — | — | — | — |
| Amount/Impact | select field | — | — | — | — | — | — |
| Reason | text field | — | — | — | — | — | — |
| Effective Period | select field | — | — | — | — | — | — |
| Requester | select field | — | — | — | — | — | — |
| Authentication code | text field | — | — | — | — | Asked in place inside the Approve the exception confirmation, because `approveBookingLimitCommercial` needs a fresh step-up token (`x-ticvai-step-up: mfa`); its result is the `stepUpToken`. Five … | — |

**Sent by *Email me a code instead*** (`createMfaChallenge`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Action `action` | text field | required | — | — | — | What the step-up is for. Recorded in the audit trail. | `createMfaChallenge` body |
| Method `methodId` | picker: choose a method | optional | — | — | shows names, sends the id | — | `createMfaChallenge` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | For a guest, the venue whose `VenueSettings.identity.guestTwoStep` applies (sign-in venue, or the venue of the booking being acted on). | `createMfaChallenge` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Price Exception (primary button) | navigation or local | — | — | — | — |
| Credit Exception (secondary button) | navigation or local | — | — | — | — |
| Allocation Exception (secondary button) | navigation or local | — | — | — | — |
| Booking Limit Exception (secondary button) | navigation or local | — | — | — | — |
| Email me a code instead (secondary button) | `createMfaChallenge` POST `/auth/mfa/challenge` | inline | inline | — | — |

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **approveBookingLimitCommercial**: Confirmation names the consequence first, then asks for the authentication code (authenticator app, or an emailed code as fallback); only a verified challenge sends approveBookingLimitCommercial with its single-use stepUpToken. Wrong code: the action is not sent and nothing changes; five wrong codes lock step-up for the policy's lockout minutes and the screen says when it lifts. Why the control exists: Sets what a partner may commit the venue to. *(source: contracts/satellite/subscription.yaml#approveBookingLimitCommercial; R126; contracts/spine/identity.yaml#createMfaChallenge)*

**Where the user goes next**

- → `PTR-032` Commercial Agreement Command Center: *Returns to the board's landing screen*; calls `approveBookingLimitCommercial`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The booking limits commercial configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the booking limits commercial untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No booking-limit exception waiting: nothing to approve, which is good news. Offers no create action. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 A wrong code, attempts one to four (CHG-R1S-025; the r1 gate found only the fifth failure specified). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
form example:
  Maximum Tickets Per Booking: 30
  Maximum Booking Value: AED 96,750.00
  Daily Booking Limit: OMR 48.500
  Monthly Booking Limit: AED 1,250.00
  Event Limit: AED 48,000.00
  Product Limit: OMR 48.500
  Hold Limit: AED 1,250.00
  Reservation Duration: 3 h 20 min
  Cancellation Limit: OMR 48.500
  Partner: Marina Leisure Group
  Agreement: 74
  Request Type: Discount override
  Current Rule: 128
  Requested Exception: 5
```

#### Permissions

- `approveBookingLimitCommercial` → `PLATFORM_CELL_MANAGE` (configure) · partner · step-up mfa
- `createMfaChallenge` → no permission · staff, partner, guest
- `verifyMfaChallenge` → no permission · staff, partner, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Inventory can be reserved for a specific partner; booking limits cap tickets per transaction or transactions per day, per partner or overall. *(client request · MoM 31 Aug 2026, 4.4 B2B Commercial Agreements, Credit & Payment Models · DI-556)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker · keyword 'ticket-booking ux')*
- **A46** Evaluate a dynamic bundle/package builder that auto-applies a discount when a guest adds multiple product types (ticket + F&B + retail) to cart, in addition to pre-defined packages *(Reshma Bandiwdekar · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'cart')*
- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A96** Build the journey library (abandoned cart with min-value/product filters, birthday, anniversary, cross-sell, survey — all consent-gated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'cart')*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'b2c checkout')*
- **A157** Keep F&B and retail online sale entirely within the platform (browse, cart, checkout, pickup or ship) with no redirect to a separate app *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 26 Aug 2026 · workshop tracker · keyword 'cart')*

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-040` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS39 B2B, Reseller & OTA Partner Management Board 2.dc.html#ptr-040`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 2
- Flow F131 *B2B, Reseller & OTA Partner Management board 2: Commercial Agreement Command …*, step 8: Works in Booking Limits, Commercial Exceptions & Approval → Control transaction limits and provide a governed mechanism for commercial exceptions.

#### Acceptance for the design

- [ ] Every input above is drawn (22), with its required mark, default, format and its error state (410, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-040?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Price Exception, Credit Exception, Allocation Exception, Booking Limit Exception, Email me a code instead.
- [ ] Every transition is wired: `PTR-032`.
- [ ] Every gated control is gated: `PLATFORM_CELL_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-041` Commercial Agreement 360°, Health & AI Review

**Give management a single consolidated view of the complete commercial relationship with a partner. Board 3 manages the day-to-day operational and financial relationship with active B2B, reseller and OTA partners. The three boards now form a clean lifecycle: Board 1 — Who is the partner? Onboarding → Organization → Users → Territory → Compliance → Permissions → Activation Board 2 — Under what commercial terms can they transact? Agreement → Rates → Commission → Credit → Security → Billing → Allocation → Limits Board 3 — What happens once the partner starts doing business? Orders → Reservations → Cancellations → Statements → Reconciliation → Commission Settlement → Disputes → Performance → Risk → AI Optimization A key principle for Board 3 is that it should provide a Partner Operations 360° without rebuilding functionality already owned by Orders, Finance, Ticketing, Payment or Channel Management.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | Block B · ticket #29556 (APP-PARTNER-PTR-041) |
| Who uses it | partner staff holding `PLATFORM_TENANT_VIEW` (1 read); in the flows as partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/partners/commercial-agreement-360-health-ai-review-ptr-041` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The complete commercial relationship with one partner, its health and AI review.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SOT-015).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Partner | picker: choose a partner | — | — | `listCommercialAgreementHealth` ?partnerId |
| Agreement | picker: choose an agreement | — | — | `listCommercialAgreementHealth` ?agreementId |
| Status | select | — | Pending approval · Active · Expiring soon · Expired · Suspended · Terminated | `listCommercialAgreementHealth` ?status |
| Risk | radio group | — | Low · Medium · High · Critical | `listCommercialAgreementHealth` ?risk |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Start Renewal, Request Commercial Review, Change Terms, Request Credit Review, Create Exception, Suspend Commercial Access. Each needs attaching to the control it gates, or the screen needs the control.

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listCommercialAgreementHealth` (onLoad, Commercial Agreement 360°, Health & AI Review)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The commercial agreement 360° list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the commercial agreement 360° untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No agreement to review yet: health appears once an agreement is active. Offers no create action. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the commercial agreement 360° are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listCommercialAgreementHealth (CommercialAgreement360HealthAiReviewView):
- rateModel: retailPrice
  averageDiscount: 12
  currentCommissionPercent: 12.5
  creditLimit: AED 1,250.00
- rateModel: netRate
  averageDiscount: 3
  currentCommissionPercent: 8.0
  creditLimit: AED 48,000.00
```

#### Permissions

- `listCommercialAgreementHealth` → `PLATFORM_TENANT_VIEW` (read) · partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Partner documents (e.g. trade licence, VAT certificate) follow a review/accept/reject/resubmit flow; approval status runs lead > submitted > active > suspended; a partner 360 view consolidates profile, agreement and payment information in one view. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-550)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-041` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS39 B2B, Reseller & OTA Partner Management Board 2.dc.html#ptr-041`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 2
- Flow F131 *B2B, Reseller & OTA Partner Management board 2: Commercial Agreement Command …*, step 10: Works in Commercial Agreement 360°, Health & AI Review → Give management a single consolidated view of the complete commercial relationship with a partner. Board 3 manages the day-to-day operational and financial relationship with active B2B, reseller and …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-041?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
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

**7 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"approveBookingLimitCommercial": {"method":"PUT","path":"/booking-limit-commercial","contract":"subscription","summary":"Booking Limits, Commercial Exceptions & Approval","permission":"PLATFORM_CELL_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"BookingLimitsCommercialExceptionsApprovalInput","responds":"BookingLimitsCommercialExceptionsApprovalView"},
"createMfaChallenge": {"method":"POST","path":"/auth/mfa/challenge","contract":"identity","summary":"Second factor at staff sign-in, and step-up for a sensitive action","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"listCommercialAgreement": {"method":"GET","path":"/commercial-agreement","contract":"subscription","summary":"Commercial Agreement Command Center","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"partnerType","in":"query","required":false},{"name":"brand","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"country","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"risk","in":"query","required":false},{"name":"creditStatus","in":"query","required":false},{"name":"expiringWithinDays","in":"query","required":false},{"name":"partnerId","in":"query","required":false},{"name":"agreementType","in":"query","required":false},{"name":"commercialOwner","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCommercialAgreementHealth": {"method":"GET","path":"/commercial-agreement-health","contract":"subscription","summary":"Commercial Agreement 360°, Health & AI Review","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"partnerId","in":"query","required":false},{"name":"agreementId","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"risk","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"setAgreementContractTerm": {"method":"PUT","path":"/agreement-contract-term","contract":"subscription","summary":"Agreement & Contract Terms Builder","permission":"PLATFORM_CELL_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AgreementContractTermsBuilderInput","responds":"AgreementContractTermsBuilderView"},
"setPartnerRateNet": {"method":"PUT","path":"/partner-rate-net","contract":"subscription","summary":"Partner Rate & Net Pricing Configuration","permission":"PLATFORM_CELL_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PartnerRateNetPricingConfigurationInput","responds":"PartnerRateNetPricingConfigurationView"},
"setPaymentTermBilling": {"method":"PUT","path":"/payment-term-billing","contract":"subscription","summary":"Payment Terms, Billing & Account Configuration","permission":"PLATFORM_CELL_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PaymentTermsBillingAccountConfigurationInput","responds":"PaymentTermsBillingAccountConfigurationView"},
"verifyMfaChallenge": {"method":"POST","path":"/auth/mfa/challenge/{challengeId}/verify","contract":"identity","summary":"Complete a sign-in or step-up challenge","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AgreementContractTermsBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; stored as control.partner_agreement (PartnerAgreement), a new version per amendment; documents are control.partner_document rows with agreementId; legalEntity, commercialOwner and financeOwner land in legalEntityId, commercialOwnerPrincipalId and financeOwnerPrincipalId (data model DM4)","description":"**What Agreement & Contract Terms Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"agreementId":{"type":"string","format":"uuid","description":"Agreement ID; omit to create"},"agreementName":{"type":"string","description":"Agreement Name"},"partnerId":{"type":"string","format":"uuid","description":"Partner"},"agreementType":{"type":"string","description":"Agreement Type code, seeded with reseller, ota, travelTrade, corporate, wholesale, affiliate, distribution, apiCommercial (pack p.26)"},"contractReference":{"type":"string","description":"Contract Reference"},"legalEntity":{"type":"string","description":"Legal Entity"},"brandId":{"type":"string","description":"Brand id","nullable":true},"allowedVenueIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Venues the agreement covers"},"territory":{"type":"string","description":"Territory"},"settlementCurrency":{"type":"string","pattern":"^[A-Z]{3}$","description":"Settlement currency, ISO 4217"},"validFrom":{"type":"string","format":"date","description":"Effective From"},"validTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true},"renewalType":{"type":"string","enum":["manual","auto"],"description":"Renewal Type"},"commercialOwner":{"type":"string","description":"Commercial Owner: staff principal id"},"financeOwner":{"type":"string","description":"Finance Owner: staff principal id"},"creditTermDays":{"type":"integer","description":"Payment Terms in days (0 = due immediately; Net 7/15/30/45 or custom)"},"commissionTerms":{"type":"string","description":"Commission Terms: summary or reference to the commission rules (listCommissionMarginIncentive)","nullable":true},"pricingBasis":{"type":"string","enum":["retailPrice","netRate","discountFromRetail","markup","derivedRate"],"description":"Pricing Basis (pack p.27 pricing models)"},"creditTerms":{"type":"string","description":"Credit Terms","nullable":true},"allocationTerms":{"type":"string","description":"Allocation Terms","nullable":true},"cancellationConditions":{"type":"string","description":"Cancellation Conditions","nullable":true},"bookingRestrictions":{"type":"string","description":"Booking Restrictions","nullable":true},"settlementTerms":{"type":"string","description":"Settlement Terms","nullable":true},"minimumCommitment":{"type":"integer","description":"Minimum Commitment: tickets over the agreement term","nullable":true},"salesTarget":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Sales Target over the agreement term"},"renewalNoticeDays":{"type":"integer","description":"Renewal Notice Period in days","nullable":true},"renegotiationRequired":{"type":"boolean","description":"Renegotiation Required"},"renewalRequiresApproval":{"type":"boolean","description":"Renewal Approval: renewal needs approval"},"rateMode":{"$ref":"#/components/schemas/PartnerRateMode","description":"Net rate or commission, as on PartnerAgreement"},"paymentModel":{"type":"string","enum":["creditAccount","prepaid","payPerTransaction"],"description":"Payment model, the three confirmed at MoM 5 Aug and MoM 31 Aug 4.4: creditAccount (sells to an approved credit ceiling, invoiced periodically), prepaid (pre-funded wallet drawn down per sale) or payPerTransaction (card at each sale)"},"refundConditions":{"type":"string","description":"Refund Conditions (pack p.26)","nullable":true},"agreementValue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Agreement value (MoM 31 Aug 4.4: each agreement captures term/value)"},"documents":{"type":"array","description":"Document Association","items":{"type":"object","properties":{"documentType":{"type":"string","enum":["signedContract","addendum","rateSheet","sla","nda","commercialAnnex"]},"documentId":{"type":"string","format":"uuid"}}}}}},
"AgreementContractTermsBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over control.partner_agreement and control.partner_document and the existing subscription state, assembled at read time (data model DM4)","description":"**What Agreement & Contract Terms Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"agreementId":{"type":"string","format":"uuid","description":"Agreement ID; omit to create"},"agreementName":{"type":"string","description":"Agreement Name"},"partnerId":{"type":"string","format":"uuid","description":"Partner"},"agreementType":{"type":"string","description":"Agreement Type code, seeded with reseller, ota, travelTrade, corporate, wholesale, affiliate, distribution, apiCommercial (pack p.26)"},"contractReference":{"type":"string","description":"Contract Reference"},"legalEntity":{"type":"string","description":"Legal Entity"},"brandId":{"type":"string","description":"Brand id","nullable":true},"allowedVenueIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Venues the agreement covers"},"territory":{"type":"string","description":"Territory"},"settlementCurrency":{"type":"string","pattern":"^[A-Z]{3}$","description":"Settlement currency, ISO 4217"},"validFrom":{"type":"string","format":"date","description":"Effective From"},"validTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true},"renewalType":{"type":"string","enum":["manual","auto"],"description":"Renewal Type"},"commercialOwner":{"type":"string","description":"Commercial Owner: staff principal id"},"financeOwner":{"type":"string","description":"Finance Owner: staff principal id"},"creditTermDays":{"type":"integer","description":"Payment Terms in days (0 = due immediately; Net 7/15/30/45 or custom)"},"commissionTerms":{"type":"string","description":"Commission Terms: summary or reference to the commission rules (listCommissionMarginIncentive)","nullable":true},"pricingBasis":{"type":"string","enum":["retailPrice","netRate","discountFromRetail","markup","derivedRate"],"description":"Pricing Basis (pack p.27 pricing models)"},"creditTerms":{"type":"string","description":"Credit Terms","nullable":true},"allocationTerms":{"type":"string","description":"Allocation Terms","nullable":true},"cancellationConditions":{"type":"string","description":"Cancellation Conditions","nullable":true},"bookingRestrictions":{"type":"string","description":"Booking Restrictions","nullable":true},"settlementTerms":{"type":"string","description":"Settlement Terms","nullable":true},"minimumCommitment":{"type":"integer","description":"Minimum Commitment: tickets over the agreement term","nullable":true},"salesTarget":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Sales Target over the agreement term"},"renewalNoticeDays":{"type":"integer","description":"Renewal Notice Period in days","nullable":true},"renegotiationRequired":{"type":"boolean","description":"Renegotiation Required"},"renewalRequiresApproval":{"type":"boolean","description":"Renewal Approval: renewal needs approval"},"rateMode":{"$ref":"#/components/schemas/PartnerRateMode","description":"Net rate or commission, as on PartnerAgreement"},"paymentModel":{"type":"string","enum":["creditAccount","prepaid","payPerTransaction"],"description":"Payment model, the three confirmed at MoM 5 Aug and MoM 31 Aug 4.4: creditAccount (sells to an approved credit ceiling, invoiced periodically), prepaid (pre-funded wallet drawn down per sale) or payPerTransaction (card at each sale)"},"refundConditions":{"type":"string","description":"Refund Conditions (pack p.26)","nullable":true},"agreementValue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Agreement value (MoM 31 Aug 4.4: each agreement captures term/value)"},"documents":{"type":"array","description":"Document Association","items":{"type":"object","properties":{"documentType":{"type":"string","enum":["signedContract","addendum","rateSheet","sla","nda","commercialAnnex"]},"documentId":{"type":"string","format":"uuid"}}}},"version":{"type":"integer","description":"Agreement version; amendments create a new one"},"status":{"$ref":"#/components/schemas/PartnerAgreementStatus","description":"Agreement status"}}},
"BookingLimitsCommercialExceptionsApprovalInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; stored as control.partner_booking_limit (PartnerBookingLimit) for the limits and control.partner_commercial_exception (PartnerCommercialException) for a request or decision; the decision itself goes to approvals (data model DM4)","description":"**What Booking Limits, Commercial Exceptions & Approval submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"maximumTicketsPerBooking":{"type":"integer","description":"Maximum Tickets Per Booking","nullable":true},"maximumBookingValue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Maximum Booking Value"},"dailyBookingLimit":{"type":"integer","description":"Daily Booking Limit: bookings per day (MoM 31 Aug 4.4: transactions per day)","nullable":true},"monthlyBookingLimit":{"type":"integer","description":"Monthly Booking Limit: bookings per month","nullable":true},"eventLimit":{"type":"integer","description":"Event Limit: tickets per event","nullable":true},"productLimit":{"type":"integer","description":"Product Limit: tickets per product per day","nullable":true},"holdLimit":{"type":"integer","description":"Hold Limit: tickets on hold at once","nullable":true},"holdDurationMinutes":{"type":"integer","description":"Reservation Duration: hold duration in minutes","nullable":true},"cancellationLimitPercent":{"type":"number","description":"Cancellation Limit: percent of a booking that may be cancelled without approval (decided 29 September, readiness close-out)","nullable":true},"partnerId":{"type":"string","format":"uuid","description":"Partner; empty for the overall limit that applies to every partner","nullable":true},"agreementId":{"type":"string","format":"uuid","description":"Agreement","nullable":true},"requestType":{"type":"string","enum":["priceException","creditException","allocationException","commissionException","bookingLimitException","paymentTermException","cancellationException"],"description":"Exception Request type","nullable":true},"currentRule":{"type":"string","description":"Current Rule","nullable":true},"requestedException":{"type":"string","description":"Requested Exception","nullable":true},"amountImpact":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Amount/Impact"},"reason":{"type":"string","description":"Reason","nullable":true},"exceptionId":{"type":"string","format":"uuid","description":"Exception request id; omit to raise a new request","nullable":true},"effectiveFrom":{"type":"string","format":"date","description":"Effective Period start","nullable":true},"effectiveTo":{"type":"string","format":"date","description":"Effective Period end","nullable":true},"decision":{"type":"string","enum":["approve","reject","returnForChanges"],"description":"Approver's decision on exceptionId; empty when setting limits or raising a request","nullable":true}}},
"BookingLimitsCommercialExceptionsApprovalView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over control.partner_booking_limit and control.partner_commercial_exception and the existing subscription state, assembled at read time (data model DM4)","description":"**What Booking Limits, Commercial Exceptions & Approval displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"maximumTicketsPerBooking":{"type":"integer","description":"Maximum Tickets Per Booking","nullable":true},"maximumBookingValue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Maximum Booking Value"},"dailyBookingLimit":{"type":"integer","description":"Daily Booking Limit: bookings per day (MoM 31 Aug 4.4: transactions per day)","nullable":true},"monthlyBookingLimit":{"type":"integer","description":"Monthly Booking Limit: bookings per month","nullable":true},"eventLimit":{"type":"integer","description":"Event Limit: tickets per event","nullable":true},"productLimit":{"type":"integer","description":"Product Limit: tickets per product per day","nullable":true},"holdLimit":{"type":"integer","description":"Hold Limit: tickets on hold at once","nullable":true},"holdDurationMinutes":{"type":"integer","description":"Reservation Duration: hold duration in minutes","nullable":true},"cancellationLimitPercent":{"type":"number","description":"Cancellation Limit: percent of a booking that may be cancelled without approval (decided 29 September, readiness close-out)","nullable":true},"partnerId":{"type":"string","format":"uuid","description":"Partner; empty for the overall limit that applies to every partner","nullable":true},"agreementId":{"type":"string","format":"uuid","description":"Agreement","nullable":true},"requestType":{"type":"string","enum":["priceException","creditException","allocationException","commissionException","bookingLimitException","paymentTermException","cancellationException"],"description":"Exception Request type","nullable":true},"currentRule":{"type":"string","description":"Current Rule","nullable":true},"requestedException":{"type":"string","description":"Requested Exception","nullable":true},"amountImpact":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Amount/Impact"},"reason":{"type":"string","description":"Reason","nullable":true},"requester":{"type":"string","description":"Requester","nullable":true},"exceptionId":{"type":"string","format":"uuid","description":"Exception request id; omit to raise a new request","nullable":true},"effectiveFrom":{"type":"string","format":"date","description":"Effective Period start","nullable":true},"effectiveTo":{"type":"string","format":"date","description":"Effective Period end","nullable":true},"decision":{"type":"string","enum":["approve","reject","returnForChanges"],"description":"Approver's decision on exceptionId; empty when setting limits or raising a request","nullable":true},"approvalStatus":{"type":"string","description":"Approval status of the exception: pendingApproval, approved, rejected, returned or expired","nullable":true},"approvalRequestId":{"type":"string","description":"Approval request","nullable":true},"aiImpactSummary":{"type":"string","description":"Advisory AI impact summary","nullable":true}}},
"CommercialAgreement360HealthAiReviewView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over control.partner_agreement with control.partner_security, control.partner_allocation, control.partner_commission_rule, control.partner_rate and control.partner_commercial_exception and the existing subscription state, assembled at read time (data model DM4)","description":"**What Commercial Agreement 360°, Health & AI Review displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"contractStatus":{"$ref":"#/components/schemas/PartnerAgreementStatus","description":"Contract status"},"renewal":{"type":"string","description":"Renewal: manual or auto, and whether a renewal workflow is open"},"rateModel":{"type":"string","enum":["retailPrice","netRate","discountFromRetail","markup","derivedRate"],"description":"Rate model"},"averageDiscount":{"type":"number","description":"Average discount from retail, percent"},"currentCommissionPercent":{"type":"number","description":"Current commission, percent","nullable":true},"incentives":{"type":"array","items":{"type":"string"},"description":"Active incentives"},"creditLimit":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Credit limit"},"creditExposure":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Credit exposure"},"availableCredit":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Available credit"},"depositGuarantee":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Deposit/guarantee held"},"securityExpiry":{"type":"string","format":"date","description":"Security expiry","nullable":true},"creditTermDays":{"type":"integer","description":"Payment terms in days","nullable":true},"outstandingBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Outstanding balance"},"overdueAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Overdue amount"},"contractualAllocation":{"type":"integer","description":"Contractual allocation, units"},"utilization":{"type":"number","description":"Allocation utilisation, percent"},"minimumSales":{"type":"integer","description":"Minimum sales commitment, units","nullable":true},"achievement":{"type":"number","description":"Commitment achievement, percent"},"activeApprovedExceptions":{"type":"integer","description":"Active approved exceptions"},"partnerId":{"type":"string","format":"uuid","description":"Partner"},"partnerName":{"type":"string","description":"Partner"},"agreementId":{"type":"string","format":"uuid","description":"Agreement"},"commercialOwner":{"type":"string","description":"Commercial Owner"},"validFrom":{"type":"string","format":"date","description":"Effective period start"},"validTo":{"type":"string","format":"date","description":"Effective period end","nullable":true},"riskRating":{"type":"string","enum":["low","medium","high","critical"],"description":"Risk"},"healthScore":{"type":"integer","description":"Commercial Health score, 0-100"},"healthBreakdown":{"type":"object","description":"Commercial Health by component, each 0-100","properties":{"agreement":{"type":"integer"},"margin":{"type":"integer"},"credit":{"type":"integer"},"payment":{"type":"integer"},"security":{"type":"integer"},"allocation":{"type":"integer"},"commitment":{"type":"integer"}}},"recommendations":{"type":"array","items":{"type":"string","enum":["reviewRate","adjustCredit","rebalanceAllocation","renewAgreement","reviewCommission","requestUpdatedGuarantee","reduceUnusedCommitment","placePartnerUnderReview"]},"description":"Advisory AI Recommendations"},"aiInsights":{"type":"array","items":{"type":"string"},"description":"Advisory AI Executive Review"}}},
"CommercialAgreementCommandCenterSummary": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection; the headline tiles over the list, computed at read time for the filters in force","description":"**The headline figures on Commercial Agreement Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.","properties":{"activeAgreements":{"type":"integer","description":"Active Agreements"},"draftAgreements":{"type":"integer","description":"Draft Agreements: pendingApproval agreements not yet submitted to the approvals engine (decided 29 September, readiness close-out)"},"pendingApproval":{"type":"integer","description":"Pending Approval: pendingApproval agreements with an open approval request"},"agreementsExpiringSoon":{"type":"integer","description":"Agreements Expiring Soon: status expiringSoon"},"expiredAgreements":{"type":"integer","description":"Expired Agreements"},"partnersOnCreditHold":{"type":"integer","description":"Partners on Credit Hold"},"totalApprovedCredit":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Total Approved Credit"},"currentCreditExposure":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Current Credit Exposure"},"outstandingReceivables":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Outstanding Receivables"},"activeCommercialAllocations":{"type":"integer","description":"Active Commercial Allocations"},"agreementsWithExceptions":{"type":"integer","description":"Agreements With Exceptions"},"commercialRiskAlerts":{"type":"integer","description":"Commercial Risk Alerts"}}},
"CommercialAgreementCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over control.partner_agreement with control.partner, control.partner_credit_profile, control.partner_allocation and control.partner_commission_rule and the existing subscription state, assembled at read time (data model DM4)","description":"**What Commercial Agreement Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"agreementId":{"type":"string","format":"uuid","description":"Agreement ID"},"partner":{"type":"string","description":"Partner trading name"},"agreementType":{"type":"string","description":"Agreement Type code, seeded with reseller, ota, travelTrade, corporate, wholesale, affiliate, distribution, apiCommercial (pack p.26)"},"brandVenue":{"type":"string","description":"Brand/Venue summary of the agreement scope"},"market":{"type":"string","description":"Market"},"validFrom":{"type":"string","format":"date","description":"Effective From"},"validTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true},"pricingModel":{"type":"string","enum":["retailPrice","netRate","discountFromRetail","markup","derivedRate"],"description":"Pricing Model (pack p.27)"},"commissionModel":{"type":"string","enum":["fixedPercentage","fixedAmount","productSpecific","tiered","volumeBased","revenueBased","performanceIncentive","campaignIncentive","none"],"description":"Commission Model (pack p.29); none for a net-rate agreement"},"creditTermDays":{"type":"integer","description":"Payment Terms in days (0 = due immediately; Net 7/15/30/45 or custom)","nullable":true},"creditLimit":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Credit Limit; empty unless the payment model is creditAccount"},"currentExposure":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Current Exposure"},"allocationModel":{"type":"string","enum":["guaranteed","onRequest","shared","fixedQuantity","percentage","rolling","seasonal","none"],"description":"Allocation Model (pack p.35)"},"agreementStatus":{"$ref":"#/components/schemas/PartnerAgreementStatus","description":"Agreement Status"},"commercialOwner":{"type":"string","description":"Commercial Owner"},"partnerId":{"type":"string","format":"uuid","description":"Partner"},"rateMode":{"$ref":"#/components/schemas/PartnerRateMode","description":"Net rate or commission, as on PartnerAgreement"},"paymentModel":{"type":"string","enum":["creditAccount","prepaid","payPerTransaction"],"description":"Payment model, the three confirmed at MoM 5 Aug and MoM 31 Aug 4.4: creditAccount (sells to an approved credit ceiling, invoiced periodically), prepaid (pre-funded wallet drawn down per sale) or payPerTransaction (card at each sale)"},"riskRating":{"type":"string","enum":["low","medium","high","critical"],"description":"Commercial risk"},"aiInsights":{"type":"array","items":{"type":"string"},"description":"Advisory AI commercial-risk flags, e.g. expiry against forward bookings"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PartnerAgreementStatus": {"type":"string","enum":["pendingApproval","active","expiringSoon","expired","suspended","terminated"]},
"PartnerRateMode": {"type":"string","description":"**Alternatives, not both.** A partner buys at a net rate and keeps the margin, or sells at face value and is paid commission. Both is being paid twice for the same sale.\n","enum":["netRate","commission"]},
"PartnerRateNetPricingConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; stored as control.partner_rate + control.partner_rate_volume_band (PartnerRate); rateId is its id (data model DM4)","description":"**What Partner Rate & Net Pricing Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"partnerId":{"type":"string","format":"uuid","description":"Partner"},"agreementId":{"type":"string","format":"uuid","description":"Agreement"},"product":{"type":"string","description":"Product id; blank = all in the family/venue","nullable":true},"productFamily":{"type":"string","description":"Product Family","nullable":true},"venue":{"type":"string","description":"Venue id; rates may differ per venue (MoM 31 Aug 4.3)","nullable":true},"event":{"type":"string","description":"Event id","nullable":true},"ticketType":{"type":"string","description":"Ticket Type","nullable":true},"priceCategory":{"type":"string","description":"Price Category","nullable":true},"market":{"type":"string","description":"Market","nullable":true},"channel":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"}],"nullable":true,"description":"Channel"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From"},"effectiveTo":{"type":"string","format":"date","description":"Effective To","nullable":true},"blackoutDates":{"type":"array","items":{"type":"string","format":"date"},"description":"Blackout Dates"},"eventExceptions":{"type":"array","items":{"type":"string"},"description":"Event Exceptions: event ids this rate does not apply to"},"seasonalRate":{"type":"boolean","description":"Seasonal Rate: this row overrides the base rate within its dates"},"minimumPermittedRate":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Guardrail: minimum permitted rate"},"maxDiscountPercent":{"type":"number","description":"Guardrail: maximum discount from retail, percent","nullable":true},"marginFloor":{"type":"number","description":"Guardrail: margin floor, percent","nullable":true},"manualOverrideAllowed":{"type":"boolean","description":"Guardrail: manual override permitted"},"approvalThreshold":{"type":"number","description":"Guardrail: discount percent above which the rate needs approval (pack p.37: discount > 15% requires approval)","nullable":true},"rateId":{"type":"string","format":"uuid","description":"Rate id; omit to create"},"pricingModel":{"type":"string","enum":["retailPrice","netRate","discountFromRetail","markup","derivedRate"],"description":"Pricing Model: retail price, net rate, discount from retail, markup or derived from a pricing profile"},"netRate":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Partner net rate, for netRate"},"discountPercent":{"type":"number","description":"Discount from retail, percent, for discountFromRetail","nullable":true},"maxMarkupPercent":{"type":"number","description":"Permitted markup, percent, for markup","nullable":true},"pricingProfileId":{"type":"string","description":"Approved pricing profile, for derivedRate","nullable":true},"volumeBands":{"type":"array","description":"Tiered volume bands (MoM 31 Aug 4.4, MoM 1 Sep 4.3: e.g. 10% up to 1,000 tickets, 15% from 1,000-5,000); fromUnits as on PartnerAgreement.volumeTiers","items":{"type":"object","properties":{"fromUnits":{"type":"integer"},"discountPercent":{"type":"number"}}}}}},
"PartnerRateNetPricingConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over control.partner_rate (PartnerRate) and the existing subscription state, assembled at read time (data model DM4)","description":"**What Partner Rate & Net Pricing Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"partnerId":{"type":"string","format":"uuid","description":"Partner"},"agreementId":{"type":"string","format":"uuid","description":"Agreement"},"product":{"type":"string","description":"Product id; blank = all in the family/venue","nullable":true},"productFamily":{"type":"string","description":"Product Family","nullable":true},"venue":{"type":"string","description":"Venue id; rates may differ per venue (MoM 31 Aug 4.3)","nullable":true},"event":{"type":"string","description":"Event id","nullable":true},"ticketType":{"type":"string","description":"Ticket Type","nullable":true},"priceCategory":{"type":"string","description":"Price Category","nullable":true},"market":{"type":"string","description":"Market","nullable":true},"channel":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"}],"nullable":true,"description":"Channel"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From"},"effectiveTo":{"type":"string","format":"date","description":"Effective To","nullable":true},"blackoutDates":{"type":"array","items":{"type":"string","format":"date"},"description":"Blackout Dates"},"eventExceptions":{"type":"array","items":{"type":"string"},"description":"Event Exceptions: event ids this rate does not apply to"},"seasonalRate":{"type":"boolean","description":"Seasonal Rate: this row overrides the base rate within its dates"},"minimumPermittedRate":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Guardrail: minimum permitted rate"},"maxDiscountPercent":{"type":"number","description":"Guardrail: maximum discount from retail, percent","nullable":true},"marginFloor":{"type":"number","description":"Guardrail: margin floor, percent","nullable":true},"manualOverrideAllowed":{"type":"boolean","description":"Guardrail: manual override permitted"},"approvalThreshold":{"type":"number","description":"Guardrail: discount percent above which the rate needs approval (pack p.37: discount > 15% requires approval)","nullable":true},"rateId":{"type":"string","format":"uuid","description":"Rate id; omit to create"},"pricingModel":{"type":"string","enum":["retailPrice","netRate","discountFromRetail","markup","derivedRate"],"description":"Pricing Model: retail price, net rate, discount from retail, markup or derived from a pricing profile"},"netRate":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Partner net rate, for netRate"},"discountPercent":{"type":"number","description":"Discount from retail, percent, for discountFromRetail","nullable":true},"maxMarkupPercent":{"type":"number","description":"Permitted markup, percent, for markup","nullable":true},"pricingProfileId":{"type":"string","description":"Approved pricing profile, for derivedRate","nullable":true},"volumeBands":{"type":"array","description":"Tiered volume bands (MoM 31 Aug 4.4, MoM 1 Sep 4.3: e.g. 10% up to 1,000 tickets, 15% from 1,000-5,000); fromUnits as on PartnerAgreement.volumeTiers","items":{"type":"object","properties":{"fromUnits":{"type":"integer"},"discountPercent":{"type":"number"}}}},"publicRate":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Public rate from the price list, read-only, for comparison"},"rateHierarchyLevel":{"type":"string","enum":["standardPrice","partnerTypeRate","partnerAgreementRate","productEventException"],"description":"Rate Hierarchy level of this row"},"validationIssues":{"type":"array","description":"Guardrail breaches and overlaps","items":{"type":"object","properties":{"code":{"type":"string","enum":["belowMinimumRate","discountAboveMaximum","marginBelowFloor","overlappingRate"]},"message":{"type":"string"}}}},"aiInsights":{"type":"array","items":{"type":"string"},"description":"Advisory AI margin-erosion or inconsistent-rate flags"}}},
"PaymentTermsBillingAccountConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; stored as control.partner_billing_profile (PartnerBillingProfile); paymentModel and creditTermDays are control.partner_agreement columns, billingCurrency is its settlementCurrency, billingEntity lands in billingEntityName, the partner's own billing entity as text, not a ledger.legal_entity reference (decided 29 September, writers pass; DM4)","description":"**What Payment Terms, Billing & Account Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"consolidatedBilling":{"type":"boolean","description":"Consolidated Billing: one invoice across the partner's branches"},"billingEntity":{"type":"string","description":"Billing Entity: the partner's own legal entity invoiced, as text; stored as PartnerBillingProfile.billingEntityName, not a ledger.legal_entity reference (decided 29 September, writers pass; DM4)"},"billingCurrency":{"type":"string","pattern":"^[A-Z]{3}$","description":"Billing Currency; equals the agreement settlementCurrency"},"invoiceFrequency":{"type":"string","enum":["perTransaction","weekly","monthly"],"description":"Invoice Frequency"},"invoiceGrouping":{"type":"string","enum":["perPartner","perBranch","perVenue","perEvent","perPurchaseOrder"],"description":"Invoice Grouping (decided 29 September, readiness close-out)"},"taxProfile":{"type":"string","description":"Tax Profile id"},"purchaseOrderRequired":{"type":"boolean","description":"Purchase Order Required"},"statementFrequency":{"type":"string","enum":["weekly","monthly"],"description":"Statement Frequency"},"billingContact":{"type":"string","description":"Billing Contact (partner contact id)"},"financeEmail":{"type":"string","description":"Finance Email","format":"email"},"partnerId":{"type":"string","format":"uuid","description":"Partner"},"agreementId":{"type":"string","format":"uuid","description":"Agreement"},"paymentModel":{"type":"string","enum":["creditAccount","prepaid","payPerTransaction"],"description":"Payment model, the three confirmed at MoM 5 Aug and MoM 31 Aug 4.4: creditAccount (sells to an approved credit ceiling, invoiced periodically), prepaid (pre-funded wallet drawn down per sale) or payPerTransaction (card at each sale)"},"creditTermDays":{"type":"integer","description":"Payment Terms in days: 0 due immediately, 7, 15, 30, 45 or custom (as on PartnerAgreement)"},"allowedPaymentMethods":{"type":"array","items":{"type":"string","enum":["creditAccount","bankTransfer","cheque","card","paymentLink","prepaidBalance","other"]},"description":"Payment Methods (cheque from MoM 31 Aug 4.4)"}}},
"PaymentTermsBillingAccountConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over control.partner_billing_profile (PartnerBillingProfile) and the existing subscription state, assembled at read time (data model DM4)","description":"**What Payment Terms, Billing & Account Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"consolidatedBilling":{"type":"boolean","description":"Consolidated Billing: one invoice across the partner's branches"},"billingEntity":{"type":"string","description":"Billing Entity: the partner's own legal entity invoiced, as text; stored as PartnerBillingProfile.billingEntityName, not a ledger.legal_entity reference (decided 29 September, writers pass; DM4)"},"billingCurrency":{"type":"string","pattern":"^[A-Z]{3}$","description":"Billing Currency; equals the agreement settlementCurrency"},"invoiceFrequency":{"type":"string","enum":["perTransaction","weekly","monthly"],"description":"Invoice Frequency"},"invoiceGrouping":{"type":"string","enum":["perPartner","perBranch","perVenue","perEvent","perPurchaseOrder"],"description":"Invoice Grouping (decided 29 September, readiness close-out)"},"taxProfile":{"type":"string","description":"Tax Profile id"},"purchaseOrderRequired":{"type":"boolean","description":"Purchase Order Required"},"statementFrequency":{"type":"string","enum":["weekly","monthly"],"description":"Statement Frequency"},"billingContact":{"type":"string","description":"Billing Contact (partner contact id)"},"financeEmail":{"type":"string","description":"Finance Email","format":"email"},"prepaidBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Prepaid wallet balance (payment model prepaid)"},"currentBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Current Balance"},"outstanding":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Outstanding"},"overdue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Overdue"},"availableCredit":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Available Credit"},"lastPayment":{"type":"string","format":"date","description":"Last Payment date","nullable":true},"nextInvoice":{"type":"string","format":"date","description":"Next Invoice date","nullable":true},"oldestOutstandingInvoice":{"type":"string","format":"date","description":"Due date of the Oldest Outstanding Invoice","nullable":true},"partnerId":{"type":"string","format":"uuid","description":"Partner"},"agreementId":{"type":"string","format":"uuid","description":"Agreement"},"paymentModel":{"type":"string","enum":["creditAccount","prepaid","payPerTransaction"],"description":"Payment model, the three confirmed at MoM 5 Aug and MoM 31 Aug 4.4: creditAccount (sells to an approved credit ceiling, invoiced periodically), prepaid (pre-funded wallet drawn down per sale) or payPerTransaction (card at each sale)"},"creditTermDays":{"type":"integer","description":"Payment Terms in days: 0 due immediately, 7, 15, 30, 45 or custom (as on PartnerAgreement)"},"allowedPaymentMethods":{"type":"array","items":{"type":"string","enum":["creditAccount","bankTransfer","cheque","card","paymentLink","prepaidBalance","other"]},"description":"Payment Methods (cheque from MoM 31 Aug 4.4)"},"applied":{"type":"boolean","description":"False when the save changed `paymentModel` or `creditTermDays` and the agreement amendment awaits approval; the billing-profile fields are applied either way (decided 29 September, writers pass; DM4)"},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"description":"The approvals.request raised for the agreement amendment; empty when none was needed (decided 29 September, writers pass; DM4)"}}},
"Session": {"type":"object","required":["sessionId","principalId","roleId","scope","effectivePermissions"],"properties":{"sessionId":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid"},"roleId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"scope":{"type":"array","description":"Scope nodes this session may act within, resolved once at login from the ltree hierarchy with deny-overrides-allow. Clients filter navigation against this — they never compute it.\n","items":{"$ref":"../shared/common.yaml#/components/schemas/ScopeRef"}},"effectivePermissions":{"allOf":[{"$ref":"../shared/permissions.yaml#/components/schemas/PermissionSet"}],"description":"Flattened set across all granted scopes, after deny resolution. Convenience for coarse checks. Anything scope-sensitive must use `permissionsByScope`.\n"},"permissionsByScope":{"type":"array","description":"Permissions effective at each granted scope path. Clients filter navigation on this and never compute permissions themselves.\n","items":{"$ref":"../shared/permissions.yaml#/components/schemas/ScopedPermissions"}},"saleBoardId":{"type":"string","format":"uuid","description":"Landing surface, derived from the WORKSTATION, not the role (12 Aug 2026 §3). Ticketing, F&B or Retail board.\n\n**Optional since 2 October 2026: only a till session carries it** (Chinmay, door follow-ups; CHG-CSP-002; breaking change against r1 approved as BC-001 to BC-005 in `docs/active/breaking-changes.yaml`). A browser door (ADM-001, SUP-001, PTR-001) and a staff handheld (EMP-001) sign in with no workstation since CHG-DOOR-001, so they have no board to land on and the field is absent. On a till it is the workstation's effective board: the outlet's board unless the till overrides it (`tenancy.Workstation.saleBoardSource`; CHG-CSP-006). A client reads its landing from this field when present and from its own platform otherwise.\n"},"workstation":{"$ref":"#/components/schemas/WorkstationContext"},"openedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time"}}},
"WorkstationContext": {"type":"object","required":["id","code","venueId","regionId"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"regionId":{"type":"string","format":"uuid"},"accessPointId":{"type":"string","format":"uuid","description":"Inherited from the workstation, never selected by the operator."},"devices":{"type":"array","items":{"type":"object","required":["kind","driver"],"properties":{"kind":{"type":"string","enum":["receiptPrinter","ticketPrinter","cashDrawer","barcodeScanner","rfidReader","paymentTerminal","customerDisplay"]},"driver":{"type":"string"},"identifier":{"type":"string"}}}},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"currencyScale":{"type":"integer","minimum":0,"maximum":4},"timezone":{"type":"string"},"cellName":{"type":"string","description":"The cell serving this workstation's region. One cell per tenant per region (ADR-0014). A client uses this only for diagnostics and telemetry tagging — never for routing, which the Control Plane resolves.\n"},"deploymentProfile":{"type":"string","enum":["terminalLocal","venueEdge","thin"],"description":"Whether this surface reads catalogue locally (ADR-0013). Determines which flows the client enables offline.\n"}}}
}
```
