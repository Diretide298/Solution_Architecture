# WS107 — Subscription Licensing AI Self Service board 10

**10 screens · 14 operations · 19 schemas · 5 permissions**

Platform P09 TICVAI Web · ships as **ticvai-control** ·
platformAdmin audience · web ·
online only

## Who this is for

**platformAdmin on web.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 5 permissions apply here:
  `PLATFORM_BILLING_MANAGE, PLATFORM_BILLING_VIEW, PLATFORM_PLAN_MANAGE, PLATFORM_TENANT_MANAGE, PLATFORM_TENANT_VIEW`. A control nobody can use must say so,
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
| `ADM-459` | Billing & Commercial Command Center | B | 0 | 18 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-460` | Billing Calculation & Charge Breakdown | B | 6 | 70 | 6 | 3 | 1 | 0 | — | notStarted (—) |
| `ADM-461` | Consumption Reconciliation & Billing Approval | B | 0 | 0 | 6 | 0 | 0 | 3 | — | notStarted (—) |
| `ADM-462` | Invoice & Payment Management | B | 0 | 0 | 6 | 1 | 1 | 0 | — | notStarted (—) |
| `ADM-463` | Subscription & Commercial Change Management | B | 0 | 12 | 6 | 4 | 0 | 0 | — | notStarted (—) |
| `ADM-464` | Renewal Management Center | B | 0 | 20 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-465` | AI Upgrade, Downgrade & Commercial Right-Sizing | B | 0 | 0 | 6 | 2 | 0 | 0 | — | notStarted (—) |
| `ADM-466` | Commercial Scenario Simulator | B | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-467` | Discount, Credit & Commercial Override Management | B | 10 | 0 | 6 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-468` | Renewal Approval, Activation & Commercial Handoff | B | 0 | 0 | 6 | 0 | 0 | 3 | — | notStarted (—) |

## Thin screens in this batch

**ADM-461, ADM-462, ADM-463, ADM-465, ADM-468 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-459` Billing & Commercial Command Center

**Provide finance, commercial and subscription teams with a consolidated view of the customer's financial position.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · ticket #29353 (APP-CONSOLE-ADM-459) |
| Who uses it | ticvai staff holding `PLATFORM_BILLING_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Financial KPIs) and a per-row directory (§Show) — counts over a population, then the population |
| Offline | online only |
| Opens with | `tenantId` (session) |
| Route | `/tenants-licensing/billing-commercial-command-center-adm-459` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** A customer's financial position with TICVAI: current charge, MRR, outstanding, next invoice, guarantee, consumption.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The table's columns are the workshop pack's labels with no bound response field (0 of 9 labels bound). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | select | — | Draft · Issued · Paid · Overdue · Disputed · Cancelled | `listSubscriptionInvoices` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Current Billing Period** (metric tile)

**Current Charge** (metric tile)

**MRR / Monthly Equivalent** (metric tile)

**ACV** (metric tile)

**YTD Revenue** (metric tile)

**Outstanding Balance** (metric tile)

**Next Invoice** (metric tile)

**Minimum Guarantee** (metric tile)

**Variable Consumption** (metric tile)

**Payment Status** (metric tile)

**Every billing commercial** (data table)

| Shows | Format | Notes |
|---|---|---|
| Platform fee | text | not in the schema: `Platform Fee` |
| Module fees | text | not in the schema: `Module Fees` |
| Ticket/transaction charges | text | not in the schema: `Ticket/Transaction Charges` |
| Minimum guarantee | text | not in the schema: `Minimum Guarantee` |
| Overage | text | not in the schema: `Overage` |
| Capacity | text | not in the schema: `Capacity` |
| Services | text | not in the schema: `Services` |
| Discounts/credits | text | not in the schema: `Discounts/Credits` |
| Tax | text | not in the schema: `Tax` |

**The selected billing commercial** (detail panel): The pack groups this record's detail under its own headings: “Dubai Discovery Museum”, “Billable Tickets”, “Rate”, “Commercial Health”.

| Shows | Format | Notes |
|---|---|---|
| Platform fee | text | not in the schema: `Platform Fee` |
| Module fees | text | not in the schema: `Module Fees` |
| Ticket/transaction charges | text | not in the schema: `Ticket/Transaction Charges` |
| Minimum guarantee | text | not in the schema: `Minimum Guarantee` |
| Overage | text | not in the schema: `Overage` |
| Capacity | text | not in the schema: `Capacity` |
| Services | text | not in the schema: `Services` |
| Discounts/credits | text | not in the schema: `Discounts/Credits` |
| Tax | text | not in the schema: `Tax` |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Money columns (Platform Fee)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. Across tenants or regions figures in different currencies are never summed into one total; group by currency, or label the converted figure with its rate and time. *(source: ADR-0008; ADR-0011; DI-306)*

**Data it reads**: `listSubscriptionInvoices` (onLoad, Billing at a glance)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Back to Platform Dashboard*
- → `ADM-460` Billing Calculation & Charge Breakdown: *Billing Calculation & Charge Breakdown*; carries `tenantId`
- → `ADM-461` Consumption Reconciliation & Billing Approval: *Consumption Reconciliation & Billing Approval*
- → `ADM-462` Invoice & Payment Management: *Invoice & Payment Management*; carries `invoiceId`
- → `ADM-463` Subscription & Commercial Change Management: *Subscription & Commercial Change Management*
- → `ADM-464` Renewal Management Center: *Renewal Management Center*
- → `ADM-465` AI Upgrade, Downgrade & Commercial Right-Sizing: *AI Upgrade, Downgrade & Commercial Right-Sizing*
- → `ADM-466` Commercial Scenario Simulator: *Commercial Scenario Simulator*
- → `ADM-467` Discount, Credit & Commercial Override Management: *Discount, Credit & Commercial Override Management*; carries `invoiceId`
- → `ADM-468` Renewal Approval, Activation & Commercial Handoff: *Renewal Approval, Activation & Commercial Handoff*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The billing commercial list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the billing commercial untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing to show yet**: the figures fill as activity is recorded. Offers no create action — a monitor creates nothing — and says so rather than showing empty tiles. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the billing commercial are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
metric tiles:
  Current Billing Period: AED 482,300.00
  Current Charge: 46
  MRR / Monthly Equivalent: AED 12,400.00
  ACV: 74
  YTD Revenue: AED 96,750.00
  Outstanding Balance: AED 12,400.00
  Next Invoice: AED 482,300.00
  Minimum Guarantee: AED 96,750.00
  Variable Consumption: 128
  Payment Status: 46
Every billing commercial:
- Platform Fee: AED 482,300.00
  Module Fees: AED 12,400.00
  Ticket/Transaction Charges: 312
  Minimum Guarantee: AED 12,400.00
  Overage: 42 min
  Capacity: 128
  Services: 128
  Discounts/Credits: 46
- Platform Fee: AED 96,750.00
  Module Fees: AED 482,300.00
  Ticket/Transaction Charges: 74
  Minimum Guarantee: AED 482,300.00
  Overage: 1.8 s
  Capacity: 46
  Services: 46
  Discounts/Credits: 312
- Platform Fee: AED 12,400.00
  Module Fees: AED 96,750.00
  Ticket/Transaction Charges: 19
  Minimum Guarantee: AED 96,750.00
  Overage: 3 h 20 min
  Capacity: 312
  Services: 312
  Discounts/Credits: 74
```

#### Permissions

- `listSubscriptionInvoices` → `PLATFORM_BILLING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Billing consolidates consumption per billing cycle into an invoice with tier plus usage/overage charges; renewal is automatic (monthly/annual) or a manual contract review, per agreed terms. *(client request · MoM 10 Sep 2026, 4.16 Billing, Reconciliation & Renewal · DI-837)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-459` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS162 Subscription Licensing AI Self Service Board 10.dc.html#adm-459`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 10
- Flow F216 *Subscription Licensing AI Self Service board 10: Billing & Commercial Command …*, step 1: Opens Billing & Commercial Command Center → Provide finance, commercial and subscription teams with a consolidated view of the customer's financial position.
- Flow F216 *Subscription Licensing AI Self Service board 10: Billing & Commercial Command …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F216 *Subscription Licensing AI Self Service board 10: Billing & Commercial Command …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F216 *Subscription Licensing AI Self Service board 10: Billing & Commercial Command …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F216 *Subscription Licensing AI Self Service board 10: Billing & Commercial Command …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F216 *Subscription Licensing AI Self Service board 10: Billing & Commercial Command …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F216 *Subscription Licensing AI Self Service board 10: Billing & Commercial Command …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F216 *Subscription Licensing AI Self Service board 10: Billing & Commercial Command …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F216 branch at step 1 (expected): when Nothing has been set up on Billing & Commercial Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F216 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-459?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-002`, `ADM-460`, `ADM-461`, `ADM-462`, `ADM-463`, `ADM-464`, `ADM-465`, `ADM-466`, `ADM-467`, `ADM-468`.
- [ ] Every gated control is gated: `PLATFORM_BILLING_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-460` Billing Calculation & Charge Breakdown

**Calculate exactly what TICVAI should charge for the billing period. This screen must dynamically change according to the commercial model.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · ticket #29354 (APP-CONSOLE-ADM-460) |
| Who uses it | ticvai staff holding `PLATFORM_BILLING_MANAGE`, `PLATFORM_BILLING_VIEW`, `PLATFORM_TENANT_VIEW` (1 configure, 2 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): Pick a tenant and a period, calculate the charge as a dry run, read the lines, then issue (defined 4 October 2026 from generateInvoice, CHG-FXS-001). |
| Offline | online only |
| Opens with | `tenantId` (navigation) |
| Route | `/tenants-licensing/billing-calculation-charge-breakdown-adm-460` |

**What the spec says about it.** **Defined 4 October 2026 from generateInvoice: the dry run (dryRun true) is the calculation and its lines are the charge breakdown; the same call without dryRun issues it** (CHG-FXS-001)

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** What TICVAI charges for a period, broken down by fee type for the customer's commercial model.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | — | `Tenant.id` |
| Period start | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `SubscriptionInvoice.periodStart` |
| Period end | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `SubscriptionInvoice.periodEnd` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |
| Status | select | — | Draft · Issued · Paid · Overdue · Disputed · Cancelled | `listSubscriptionInvoices` ?status |

**Sent by *Calculate*** (`generateInvoice`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Period start `periodStart` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `generateInvoice` body |
| Period end `periodEnd` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `generateInvoice` body |
| Dry run `dryRun` | toggle | optional | off | — | — | — | `generateInvoice` body |

#### Outputs: what the screen shows and produces

**Shown**

**Charge lines** (data table, from `generateInvoice`): One line per licensed module at its listed price, the package's base line, and metered usage lines; the commercial model decides which lines appear.

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Base plan, Module, Add on, Overage, Metered, One off… | `module`, one per licensed module at its platform price, and `metered`, usage such as AI tokens (decided 29 September). |
| Module code | text | The module a `module` or `metered` line charges for. |
| Description | text | — |
| Quantity | 1,234.5 | — |
| Unit price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Subtotal** (metric tile, from `generateInvoice`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Invoice number | text | A tax invoice number, so gapless, per legal entity (decided 28 September, audit R152): one unbroken sequence for the TICVAI legal entity … |
| Period start | 1 Oct 2026 | — |
| Period end | 1 Oct 2026 | — |
| Status | chip: Draft, Issued, Paid, Overdue, Disputed, Cancelled | — |
| Lines | list or chips (count when long) | — |
| Description | text | — |
| Kind | chip: Base plan, Module, Add on, Overage, Metered, One off… | `module`, one per licensed module at its platform price, and `metered`, usage such as AI tokens (decided 29 September). |
| Module code | text | The module a `module` or `metered` line charges for. |
| Audience | chip: Staff, Guest | For an AI `metered` line, whose usage it is. |
| Metric | chip: Venues, Workstations, Active users, Devices, Branded apps, AI tokens… | — |
| Quantity | 1,234.5 | — |
| Unit price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Subtotal | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Plan version used | text | Priced against the version the tenant is subscribed to, not the latest. |
| Credited total | AED 1,234.50 | The sum of the credit notes issued against this invoice (`issueCreditNote`); the invoice itself is never edited. |
| Issued at | 1 Oct 2026, 14:30 | — |

**Tax** (metric tile, from `generateInvoice`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Invoice number | text | A tax invoice number, so gapless, per legal entity (decided 28 September, audit R152): one unbroken sequence for the TICVAI legal entity … |
| Period start | 1 Oct 2026 | — |
| Period end | 1 Oct 2026 | — |
| Status | chip: Draft, Issued, Paid, Overdue, Disputed, Cancelled | — |
| Lines | list or chips (count when long) | — |
| Description | text | — |
| Kind | chip: Base plan, Module, Add on, Overage, Metered, One off… | `module`, one per licensed module at its platform price, and `metered`, usage such as AI tokens (decided 29 September). |
| Module code | text | The module a `module` or `metered` line charges for. |
| Audience | chip: Staff, Guest | For an AI `metered` line, whose usage it is. |
| Metric | chip: Venues, Workstations, Active users, Devices, Branded apps, AI tokens… | — |
| Quantity | 1,234.5 | — |
| Unit price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Subtotal | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Plan version used | text | Priced against the version the tenant is subscribed to, not the latest. |
| Credited total | AED 1,234.50 | The sum of the credit notes issued against this invoice (`issueCreditNote`); the invoice itself is never edited. |
| Issued at | 1 Oct 2026, 14:30 | — |

**Total** (metric tile, from `generateInvoice`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Invoice number | text | A tax invoice number, so gapless, per legal entity (decided 28 September, audit R152): one unbroken sequence for the TICVAI legal entity … |
| Period start | 1 Oct 2026 | — |
| Period end | 1 Oct 2026 | — |
| Status | chip: Draft, Issued, Paid, Overdue, Disputed, Cancelled | — |
| Lines | list or chips (count when long) | — |
| Description | text | — |
| Kind | chip: Base plan, Module, Add on, Overage, Metered, One off… | `module`, one per licensed module at its platform price, and `metered`, usage such as AI tokens (decided 29 September). |
| Module code | text | The module a `module` or `metered` line charges for. |
| Audience | chip: Staff, Guest | For an AI `metered` line, whose usage it is. |
| Metric | chip: Venues, Workstations, Active users, Devices, Branded apps, AI tokens… | — |
| Quantity | 1,234.5 | — |
| Unit price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Subtotal | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Plan version used | text | Priced against the version the tenant is subscribed to, not the latest. |
| Credited total | AED 1,234.50 | The sum of the credit notes issued against this invoice (`issueCreditNote`); the invoice itself is never edited. |
| Issued at | 1 Oct 2026, 14:30 | — |

**Invoices issued** (data table, from `listSubscriptionInvoices`)

| Shows | Format | Notes |
|---|---|---|
| Period start | 1 Oct 2026 | — |
| Period end | 1 Oct 2026 | — |
| Status | chip: Draft, Issued, Paid, Overdue, Disputed, Cancelled | — |
| Total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Calculate (primary button) | `generateInvoice` POST `/tenants/{tenantId}/invoices` | inline | SubscriptionInvoice | 409 An invoice already exists for this period | — |
| Issue invoice (secondary button) | `generateInvoice` POST `/tenants/{tenantId}/invoices` | inline | SubscriptionInvoice | 409 An invoice already exists for this period | — |

**Data it reads**: `listTenants` (onLoad, The tenant picker (audit R098)); `listSubscriptionInvoices` (onLoad, The tenant's invoices already issued, to show a period that …)

**Where the user goes next**

- → `ADM-459` Billing & Commercial Command Center: *Back to Billing & Commercial Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The list skeleton, with the filters already drawn. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves what is on screen untouched. |
| Empty, first run (`?state=emptyFirstRun`) | Nothing calculated yet: pick a tenant and a period. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the billing calculation charge are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `listTenants` requires to show this screen, and names that permission (the screen's other reads need `PLATFORM_BILLING_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_BILLING_MANAGE` for `generateInvoice`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 An invoice already exists for this period |

#### Edge cases to draw

- **generateInvoice answers 409**: Show it as something the person can act on, not a failure: An invoice already exists for this period *(source: contracts/satellite/subscription.yaml#generateInvoice)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
period: September 2026
platformFee: AED 25,000.00
ticketCharges: AED 32,850.00
minimumGuarantee: AED 30,000.00
total: AED 60,742.50 incl. VAT 5%
```

#### Permissions

- `generateInvoice` → `PLATFORM_BILLING_MANAGE` (configure) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listSubscriptionInvoices` → `PLATFORM_BILLING_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `listTenants` requires to show this screen, and names that permission (the screen's other reads need `PLATFORM_BILLING_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_BILLING_MANAGE` for `generateInvoice`.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.7.1 | Subscription Invoicing - System shall generate subscription invoices. | Subscription & Licensing Management | CONTRACTED | `generateInvoice` |
| 20.7.5 | Billing History - System shall maintain billing history. | Subscription & Licensing Management | CONTRACTED | `generateInvoice` |
| 2.6.6 | It is expected to have one webstore/application API for each venue. | Ticketing Sales | CONTRACTED | data `Tenant` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Billing consolidates consumption per billing cycle into an invoice with tier plus usage/overage charges; renewal is automatic (monthly/annual) or a manual contract review, per agreed terms. *(client request · MoM 10 Sep 2026, 4.16 Billing, Reconciliation & Renewal · DI-837)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-460` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS162 Subscription Licensing AI Self Service Board 10.dc.html#adm-460`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 10
- Flow F216 *Subscription Licensing AI Self Service board 10: Billing & Commercial Command …*, step 2: Works in Billing Calculation & Charge Breakdown → Calculate exactly what TICVAI should charge for the billing period. This screen must dynamically change according to the commercial model.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (403, 409).
- [ ] Every output is drawn (70 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-460?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Calculate, Issue invoice.
- [ ] Every transition is wired: `ADM-459`.
- [ ] Every gated control is gated: `PLATFORM_BILLING_MANAGE`, `PLATFORM_BILLING_VIEW`, `PLATFORM_TENANT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-461` Consumption Reconciliation & Billing Approval

**This is an important new screen following the introduction of transaction-based contracts. Finance must be able to reconcile the commercial consumption received from Board 9 before invoicing.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · ticket #29355 (APP-CONSOLE-ADM-461) |
| Who uses it | ticvai staff holding `PLATFORM_BILLING_MANAGE`, `PLATFORM_BILLING_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/consumption-reconciliation-billing-approval-adm-461` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Finance reconciles metered consumption before invoicing, and settles AI usage.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Period | text field | — | — | `getBillingReconciliation` ?period |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getBillingReconciliation` (onLoad, Consumption against invoice)

**Where the user goes next**

- → `ADM-459` Billing & Commercial Command Center: *Back to Billing & Commercial Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The consumption reconciliation billing list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the consumption reconciliation billing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No consumption reconciliation billing yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the consumption reconciliation billing are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Already settled for this period. Settling twice would invoice twice, and the idempotency key alone does not protect a re-run with a different key. |

#### Edge cases to draw

- **Can read but not change (holds PLATFORM_BILLING_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: PLATFORM_BILLING_MANAGE for settleAiUsage. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/subscription.yaml#settleAiUsage)*
- **settleAiUsage answers 409**: Show it as something the person can act on, not a failure: Already settled for this period. **Settling twice would invoice twice**, and the idempotency key alone does not protect a re-run with a different key. *(source: contracts/satellite/subscription.yaml#settleAiUsage)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
metered: 412,880 tickets
invoiced: 412,880
difference: 0
aiUsage: AED 1,240.00 to settle
```

#### Permissions

- `getBillingReconciliation` → `PLATFORM_BILLING_VIEW` (read) · staff
- `settleAiUsage` → `PLATFORM_BILLING_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-461` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS162 Subscription Licensing AI Self Service Board 10.dc.html#adm-461`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 10
- Flow F216 *Subscription Licensing AI Self Service board 10: Billing & Commercial Command …*, step 4: Works in Consumption Reconciliation & Billing Approval → This is an important new screen following the introduction of transaction-based contracts. Finance must be able to reconcile the commercial consumption received from Board 9 before invoicing.
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-461?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-459`.
- [ ] Every gated control is gated: `PLATFORM_BILLING_MANAGE`, `PLATFORM_BILLING_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-462` Invoice & Payment Management

**Generate, issue and track customer invoices and payments.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · ticket #29362 (APP-CONSOLE-ADM-462) |
| Who uses it | ticvai staff holding `PLATFORM_BILLING_MANAGE`, `PLATFORM_BILLING_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `invoiceId` (navigation), `tenantId` (session) |
| Route | `/tenants-licensing/invoice-payment-management-adm-462` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Issue invoices, record payments, issue credit notes.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | select | — | Draft · Issued · Paid · Overdue · Disputed · Cancelled | `listSubscriptionInvoices` ?status |
| Invoice | text field | — | — | `listCreditNotes` ?invoiceId |

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

- **Issue credit note**: Linked to the invoice, reason required, amount cannot exceed what remains creditable. *(source: contracts/satellite/subscription.yaml#issueCreditNote)*

**Data it reads**: `listSubscriptionInvoices` (onLoad, Invoices raised); `listCreditNotes` (onLoad, Credit notes issued)

**Where the user goes next**

- → `ADM-459` Billing & Commercial Command Center: *Back to Billing & Commercial Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The invoice payment list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the invoice payment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No invoice payment yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the invoice payment are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Not in a state that permits this; 409 The invoice is a draft or cancelled and cannot be credited; 422 The credit would take the invoice's credited total above its total, or a line names no line of the invoice |

#### Edge cases to draw

- **Can read but not change (holds PLATFORM_BILLING_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: PLATFORM_BILLING_MANAGE for recordInvoicePayment, issueCreditNote. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/subscription.yaml#recordInvoicePayment)*
- **recordInvoicePayment answers 409**: Show it as something the person can act on, not a failure: Not in a state that permits this *(source: contracts/satellite/subscription.yaml#recordInvoicePayment)*
- **issueCreditNote answers 409**: Show it as something the person can act on, not a failure: The invoice is a draft or cancelled and cannot be credited *(source: contracts/satellite/subscription.yaml#issueCreditNote)*
- **issueCreditNote answers 422**: Show it as something the person can act on, not a failure: The credit would take the invoice's credited total above its total, or a line names no line of the invoice *(source: contracts/satellite/subscription.yaml#issueCreditNote)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listSubscriptionInvoices (SubscriptionInvoice):
- periodStart: 01/10/2026 09:14
  periodEnd: 01/10/2026 09:14
  status: active
  subtotal: AED 1,250.00
  taxAmount: AED 1,250.00
  total: AED 1,250.00
  creditedTotal: AED 1,250.00
- periodStart: 30/09/2026 18:02
  periodEnd: 30/09/2026 18:02
  status: pending
  subtotal: AED 48,000.00
  taxAmount: AED 48,000.00
  total: AED 48,000.00
  creditedTotal: AED 48,000.00
```

#### Permissions

- `recordInvoicePayment` → `PLATFORM_BILLING_MANAGE` (configure) · staff
- `listSubscriptionInvoices` → `PLATFORM_BILLING_VIEW` (read) · staff
- `issueCreditNote` → `PLATFORM_BILLING_MANAGE` (configure) · staff
- `listCreditNotes` → `PLATFORM_BILLING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.7.7 | Credit Notes - System shall support credit note generation. | Subscription & Licensing Management | CONTRACTED | `issueCreditNote` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Billing consolidates consumption per billing cycle into an invoice with tier plus usage/overage charges; renewal is automatic (monthly/annual) or a manual contract review, per agreed terms. *(client request · MoM 10 Sep 2026, 4.16 Billing, Reconciliation & Renewal · DI-837)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-462` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS162 Subscription Licensing AI Self Service Board 10.dc.html#adm-462`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 10
- Flow F216 *Subscription Licensing AI Self Service board 10: Billing & Commercial Command …*, step 6: Works in Invoice & Payment Management → Generate, issue and track customer invoices and payments.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-462?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-459`.
- [ ] Every gated control is gated: `PLATFORM_BILLING_MANAGE`, `PLATFORM_BILLING_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 4 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-463` Subscription & Commercial Change Management

**Manage changes to an active commercial agreement without losing contractual history.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · ticket #29370 (APP-CONSOLE-ADM-463) |
| Who uses it | ticvai staff holding `PLATFORM_TENANT_MANAGE`, `PLATFORM_TENANT_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | `tenantId` (session) |
| Route | `/tenants-licensing/subscription-commercial-change-management-adm-463` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Change an active agreement without losing history: preview first (proration, impact), upgrades now, downgrades at renewal.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The table's columns are the workshop pack's labels with no bound response field (0 of 6 labels bound). (CHG-SBO-005)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Effective date**: Upgrade immediate with proration; downgrade fixed to the next renewal. *(source: R214)*

#### Outputs: what the screen shows and produces

**Shown**

**Every subscription commercial change** (data table)

| Shows | Format | Notes |
|---|---|---|
| Current monthly equivalent | text | not in the schema: `Current Monthly Equivalent` |
| Proposed monthly equivalent | text | not in the schema: `Proposed Monthly Equivalent` |
| Proration | text | not in the schema: `Proration` |
| Customer impact | text | not in the schema: `Customer Impact` |
| TICVAI revenue impact | text | not in the schema: `TICVAI Revenue Impact` |
| Contract value change | text | not in the schema: `Contract Value Change` |

**The selected subscription commercial change** (detail panel): The pack groups this record's detail under its own headings: “Change Types”, “Current”, “Proposed”, “Effective Timing”, “Draft Change”.

| Shows | Format | Notes |
|---|---|---|
| Current monthly equivalent | text | not in the schema: `Current Monthly Equivalent` |
| Proposed monthly equivalent | text | not in the schema: `Proposed Monthly Equivalent` |
| Proration | text | not in the schema: `Proration` |
| Customer impact | text | not in the schema: `Customer Impact` |
| TICVAI revenue impact | text | not in the schema: `TICVAI Revenue Impact` |
| Contract value change | text | not in the schema: `Contract Value Change` |

**Where the user goes next**

- → `ADM-459` Billing & Commercial Command Center: *Back to Billing & Commercial Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The subscription commercial change list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the subscription commercial change untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No subscription commercial change yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the subscription commercial change are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Downgrade conflicts with current usage. The response names every module and limit that would be violated. (DowngradeConflictProblem); 422 `effectiveFrom` was sent and is not the date the change must take effect: today for an upgrade, the next renewal for a downgrade (`effective-date-not-allowed` … |

#### Edge cases to draw

- **setSubscription answers 409**: Show it as something the person can act on, not a failure: Downgrade conflicts with current usage. The response names every module and limit that would be violated. Or the subscription is `expired` and cannot be reactivated (`subscription-expired`, audit STATE-SUBSCRIPTION); start a new one. *(source: contracts/satellite/subscription.yaml#setSubscription)*
- **setSubscription answers 422**: Show it as something the person can act on, not a failure: `effectiveFrom` was sent and is not the date the change must take effect: today for an upgrade, the next renewal for a downgrade (`effective-date-not-allowed`, audit R214 (1)). Or the plan is a custom package private to another tenant (`plan-not-offered`, decided 29 September). *(source: contracts/satellite/subscription.yaml#setSubscription)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every subscription commercial change:
- Current Monthly Equivalent: 312
  Proposed Monthly Equivalent: 74
  Proration: 46
  Customer Impact: Marina Leisure Group
  TICVAI Revenue Impact: AED 482,300.00
  Contract Value Change: AED 482,300.00
- Current Monthly Equivalent: 74
  Proposed Monthly Equivalent: 19
  Proration: 312
  Customer Impact: Desert Gate Tours LLC
  TICVAI Revenue Impact: AED 96,750.00
  Contract Value Change: AED 96,750.00
- Current Monthly Equivalent: 19
  Proposed Monthly Equivalent: 233
  Proration: 74
  Customer Impact: Arabian Trails
  TICVAI Revenue Impact: AED 12,400.00
  Contract Value Change: AED 12,400.00
```

#### Permissions

- `previewSubscriptionChange` → `PLATFORM_TENANT_VIEW` (read) · staff, prospect
- `setSubscription` → `PLATFORM_TENANT_MANAGE` (configure) · staff, prospect

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.2.5 | Subscription Upgrade - System shall support subscription upgrades. | Subscription & Licensing Management | CONTRACTED | `previewSubscriptionChange` |
| 20.2.6 | Subscription Downgrade - System shall support subscription downgrades. | Subscription & Licensing Management | CONTRACTED | `previewSubscriptionChange` |
| 20.2.2 | Monthly Billing - System shall support monthly subscriptions. | Subscription & Licensing Management | CONTRACTED | `setSubscription` |
| 20.2.3 | Annual Billing - System shall support annual subscriptions. | Subscription & Licensing Management | CONTRACTED | `setSubscription` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-463` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS162 Subscription Licensing AI Self Service Board 10.dc.html#adm-463`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 10
- Flow F216 *Subscription Licensing AI Self Service board 10: Billing & Commercial Command …*, step 8: Works in Subscription & Commercial Change Management → Manage changes to an active commercial agreement without losing contractual history.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-463?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-459`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_MANAGE`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-464` Renewal Management Center

**Manage the complete customer renewal pipeline.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · ticket #29228 (APP-CONSOLE-ADM-464) |
| Who uses it | ticvai; in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Renewal KPIs) and a per-row directory (§Analyze) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/renewal-management-center-adm-464` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape … Removed 2 October 2026 (CHG-WIR-021): listRenewalAuto and setRenewalAutoMembership are guest membership renewal operations; TICVAI customer renewal is a subscription matter (design-notes correction … Removed 2 October 2026 (CHG-WIR-021): listRenewalAuto and setRenewalAutoMembership are guest membership renewal operations; TICVAI customer renewal is a subscription matter (design-notes correction …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The customer renewal pipeline with growth, usage, overage and payment history per customer.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The table's columns are the workshop pack's labels with no bound response field (0 of 10 labels bound). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): Uses listRenewalAuto and setRenewalAutoMembership (guest membership operations). (CHG-WIR-021).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Renewals Due** (metric tile)

**Renewal ARR / Contract Value** (metric tile)

**Renewal Rate** (metric tile)

**At-Risk Revenue** (metric tile)

**Auto-Renew Value** (metric tile)

**Expansion Opportunity** (metric tile)

**Cost Optimization Opportunity** (metric tile)

**Every renewal** (data table)

| Shows | Format | Notes |
|---|---|---|
| Ticket growth | text | not in the schema: `Ticket Growth` |
| Transaction growth | text | not in the schema: `Transaction Growth` |
| Technical usage | text | not in the schema: `Technical Usage` |
| Overage | text | not in the schema: `Overage` |
| Minimum guarantee utilization | text | not in the schema: `Minimum Guarantee Utilization` |
| Module adoption | text | not in the schema: `Module Adoption` |
| Payment history | text | not in the schema: `Payment History` |
| Support activity | text | not in the schema: `Support Activity` |
| Contract exceptions | text | not in the schema: `Contract Exceptions` |
| Customer growth/decline | text | not in the schema: `Customer Growth/Decline` |

**The selected renewal** (detail panel): The pack groups this record's detail under its own headings: “Renewal Windows”, “Customer Renewal Table”.

| Shows | Format | Notes |
|---|---|---|
| Ticket growth | text | not in the schema: `Ticket Growth` |
| Transaction growth | text | not in the schema: `Transaction Growth` |
| Technical usage | text | not in the schema: `Technical Usage` |
| Overage | text | not in the schema: `Overage` |
| Minimum guarantee utilization | text | not in the schema: `Minimum Guarantee Utilization` |
| Module adoption | text | not in the schema: `Module Adoption` |
| Payment history | text | not in the schema: `Payment History` |
| Support activity | text | not in the schema: `Support Activity` |
| Contract exceptions | text | not in the schema: `Contract Exceptions` |
| Customer growth/decline | text | not in the schema: `Customer Growth/Decline` |

**Where the user goes next**

- → `ADM-459` Billing & Commercial Command Center: *Back to Billing & Commercial Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The renewal list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the renewal untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No renewal yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the renewal are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Can read but not change (holds PLATFORM_TENANT_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: PLATFORM_CELL_MANAGE for setRenewalAutoMembership. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/subscription.yaml#setRenewalAutoMembership)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
metric tiles:
  Renewals Due: 128
  Renewal ARR / Contract Value: AED 96,750.00
  Renewal Rate: 71%
  At-Risk Revenue: AED 482,300.00
  Auto-Renew Value: AED 96,750.00
  Expansion Opportunity: 233
  Cost Optimization Opportunity: AED 482,300.00
Every renewal:
- Ticket Growth: +6.2%
  Transaction Growth: +6.2%
  Technical Usage: 3 h 20 min
  Overage: 42 min
  Minimum Guarantee Utilization: 92%
  Module Adoption: 92%
  Payment History: 11
  Support Activity: 128
- Ticket Growth: -1.4%
  Transaction Growth: -1.4%
  Technical Usage: 42 min
  Overage: 1.8 s
  Minimum Guarantee Utilization: 78%
  Module Adoption: 78%
  Payment History: 128
  Support Activity: 46
- Ticket Growth: +12.0%
  Transaction Growth: +12.0%
  Technical Usage: 1.8 s
  Overage: 3 h 20 min
  Minimum Guarantee Utilization: 64%
  Module Adoption: 64%
  Payment History: 46
  Support Activity: 312
```

#### Permissions

**A refused user sees:** Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Billing consolidates consumption per billing cycle into an invoice with tier plus usage/overage charges; renewal is automatic (monthly/annual) or a manual contract review, per agreed terms. *(client request · MoM 10 Sep 2026, 4.16 Billing, Reconciliation & Renewal · DI-837)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-464` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS162 Subscription Licensing AI Self Service Board 10.dc.html#adm-464`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 10
- Flow F216 *Subscription Licensing AI Self Service board 10: Billing & Commercial Command …*, step 10: Works in Renewal Management Center → Manage the complete customer renewal pipeline.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-464?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-459`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-465` AI Upgrade, Downgrade & Commercial Right-Sizing

**Use AI to recommend the best future commercial structure, not simply the most expensive package. This remains a fundamental TICVAI AI principle.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · ticket #29371 (APP-CONSOLE-ADM-465) |
| Who uses it | ticvai staff holding `PLATFORM_BILLING_VIEW`, `PLATFORM_PLAN_MANAGE` (1 read, 1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/ai-upgrade-downgrade-commercial-right-sizing-adm-465` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** AI recommendation of the right commercial structure, not the most expensive one.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Horizon months | stepper or slider | 3 | min 1; max 12 | `getPlanRecommendations` ?horizonMonths |
| Kind | select | — | Upgrade · Downgrade · Add module · Remove module · Remove add on · Capacity pack | `getPlanRecommendations` ?kind |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getPlanRecommendations` (onLoad, Upgrade, downgrade and right-sizing recommendations for the …)

**Where the user goes next**

- → `ADM-459` Billing & Commercial Command Center: *Back to Billing & Commercial Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The upgrade downgrade commercial list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the upgrade downgrade commercial untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No upgrade downgrade commercial yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the upgrade downgrade commercial are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Can read but not change (holds PLATFORM_BILLING_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: PLATFORM_PLAN_MANAGE for simulateCommercialPackage. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/subscription.yaml#simulateCommercialPackage)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
customer: Gulf Fun Parks LLC
current: Enterprise
recommended: Growth + capacity pack
saving: AED 6,000.00 / month
```

#### Permissions

- `simulateCommercialPackage` → `PLATFORM_PLAN_MANAGE` (configure) · staff, guest, prospect
- `getPlanRecommendations` → `PLATFORM_BILLING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.8.4 | AI Upgrade Recommendations - System shall recommend subscription upgrades. | Subscription & Licensing Management | CONTRACTED | `getPlanRecommendations` |
| 20.8.5 | AI Cost Optimization - System shall recommend cost optimization opportunities. | Subscription & Licensing Management | CONTRACTED | `getPlanRecommendations` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-465` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS162 Subscription Licensing AI Self Service Board 10.dc.html#adm-465`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 10
- Flow F216 *Subscription Licensing AI Self Service board 10: Billing & Commercial Command …*, step 12: Works in AI Upgrade, Downgrade & Commercial Right-Sizing → Use AI to recommend the best future commercial structure, not simply the most expensive package. This remains a fundamental TICVAI AI principle.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403, 404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-465?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-459`.
- [ ] Every gated control is gated: `PLATFORM_BILLING_VIEW`, `PLATFORM_PLAN_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-466` Commercial Scenario Simulator

**Allow commercial and finance teams to model different renewal or contract scenarios before making an offer.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · ticket #29368 (APP-CONSOLE-ADM-466) |
| Who uses it | ticvai staff holding `PLATFORM_PLAN_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Comparison Metrics) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/commercial-scenario-simulator-adm-466` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Model renewal or contract scenarios before making an offer.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Customer Cost** (metric tile)

**TICVAI Revenue** (metric tile)

**Minimum Revenue Protection** (metric tile)

**Variable Revenue Exposure** (metric tile)

**Margin** (metric tile)

**Expected Overage** (metric tile)

**Customer Saving/Increase** (metric tile)

**Contract Predictability** (metric tile)

**Revenue Growth/Contraction** (metric tile)

**Where the user goes next**

- → `ADM-459` Billing & Commercial Command Center: *Back to Billing & Commercial Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The commercial scenario simulator list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the commercial scenario simulator untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing to show yet**: the figures fill as activity is recorded. Offers no create action — a monitor creates nothing — and says so rather than showing empty tiles. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the commercial scenario simulator are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
metric tiles:
  Customer Cost: AED 482,300.00
  TICVAI Revenue: AED 96,750.00
  Minimum Revenue Protection: AED 12,400.00
  Variable Revenue Exposure: AED 482,300.00
  Margin: 19
  Expected Overage: 1.8 s
  Customer Saving/Increase: 57
  Contract Predictability: 11
  Revenue Growth/Contraction: AED 12,400.00
```

#### Permissions

- `simulateCommercialPackage` → `PLATFORM_PLAN_MANAGE` (configure) · staff, guest, prospect

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-466` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS162 Subscription Licensing AI Self Service Board 10.dc.html#adm-466`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 10
- Flow F216 *Subscription Licensing AI Self Service board 10: Billing & Commercial Command …*, step 14: Works in Commercial Scenario Simulator → Allow commercial and finance teams to model different renewal or contract scenarios before making an offer.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-466?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-459`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-467` Discount, Credit & Commercial Override Management

**Govern non-standard commercial terms.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · ticket #29372 (APP-CONSOLE-ADM-467) |
| Who uses it | ticvai staff holding `PLATFORM_BILLING_MANAGE`, `PLATFORM_BILLING_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Required Fields) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `invoiceId` (navigation), `tenantId` (session) |
| Route | `/tenants-licensing/discount-credit-commercial-override-management-adm-467` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Non-standard commercial terms (discount, credit, override) with standard and proposed values, impact, expiry and the approval required; cancel or dispute an invoice.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Override Type | select field | — | — | — | — | — | — |
| Standard Value | select field | — | — | — | — | — | — |
| Proposed Value | select field | — | — | — | — | — | — |
| Financial Impact | select field | — | — | — | — | — | — |
| Reason | select field | — | — | — | — | — | — |
| Start Date | select field | — | — | — | — | — | — |
| Expiry | select field | — | — | — | — | — | — |
| Contract | select field | — | — | — | — | — | — |
| Requested By | select field | — | — | — | — | — | — |
| Required Approval | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Invoice | text field | — | — | `listCreditNotes` ?invoiceId |

#### Outputs: what the screen shows and produces

**Data it reads**: `listCreditNotes` (onLoad, Credits against the tenant's invoices)

**Where the user goes next**

- → `ADM-459` Billing & Commercial Command Center: *Back to Billing & Commercial Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The discount credit commercial configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the discount credit commercial untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No discount credit commercial configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Not in a state that permits this; 409 The invoice is a draft or cancelled and cannot be credited; 422 The credit would take the invoice's credited total above its total, or a line names no line of the invoice |

#### Edge cases to draw

- **Can read but not change (holds PLATFORM_BILLING_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: PLATFORM_BILLING_MANAGE for cancelInvoice, disputeInvoice, issueCreditNote. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/subscription.yaml#cancelInvoice)*
- **cancelInvoice answers 409**: Show it as something the person can act on, not a failure: Not in a state that permits this *(source: contracts/satellite/subscription.yaml#cancelInvoice)*
- **disputeInvoice answers 409**: Show it as something the person can act on, not a failure: Not in a state that permits this *(source: contracts/satellite/subscription.yaml#disputeInvoice)*
- **issueCreditNote answers 409**: Show it as something the person can act on, not a failure: The invoice is a draft or cancelled and cannot be credited *(source: contracts/satellite/subscription.yaml#issueCreditNote)*
- **issueCreditNote answers 422**: Show it as something the person can act on, not a failure: The credit would take the invoice's credited total above its total, or a line names no line of the invoice *(source: contracts/satellite/subscription.yaml#issueCreditNote)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
form example:
  Override Type: 233
  Standard Value: AED 482,300.00
  Proposed Value: AED 96,750.00
  Financial Impact: 74
  Reason: 312
  Start Date: 28/09/2026 11:45
  Expiry: 19
  Contract: 11
  Requested By: Omar Haddad
  Required Approval: 312
```

#### Permissions

- `cancelInvoice` → `PLATFORM_BILLING_MANAGE` (configure) · staff
- `disputeInvoice` → `PLATFORM_BILLING_MANAGE` (configure) · staff
- `issueCreditNote` → `PLATFORM_BILLING_MANAGE` (configure) · staff
- `listCreditNotes` → `PLATFORM_BILLING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.7.7 | Credit Notes - System shall support credit note generation. | Subscription & Licensing Management | CONTRACTED | `issueCreditNote` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-467` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS162 Subscription Licensing AI Self Service Board 10.dc.html#adm-467`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 10
- Flow F216 *Subscription Licensing AI Self Service board 10: Billing & Commercial Command …*, step 16: Works in Discount, Credit & Commercial Override Management → Govern non-standard commercial terms.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-467?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-459`.
- [ ] Every gated control is gated: `PLATFORM_BILLING_MANAGE`, `PLATFORM_BILLING_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 5 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-468` Renewal Approval, Activation & Commercial Handoff

**Finalize renewal and synchronize the approved future commercial agreement across TICVAI.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · ticket #29369 (APP-CONSOLE-ADM-468) |
| Who uses it | ticvai staff holding `PLATFORM_BILLING_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/renewal-approval-activation-commercial-handoff-adm-468` |

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: Revised Board 10 — Commercial Model Calculation. Each needs an operation, or needs removing from the … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Finalise a renewal and synchronise the new agreement across subscription, licence and billing.

**Fixed on main** (the package already carries these; draw what it says): Button labelled "Revised Board 10 — Commercial Model Calculation". (CHG-SBO-015); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Period | text field | — | — | `getBillingReconciliation` ?period |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Data it reads**: `getBillingReconciliation` (onLoad, Billing audit)

**Where the user goes next**

- → `ADM-459` Billing & Commercial Command Center: *Back to Billing & Commercial Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The renewal approval activation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the renewal approval activation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No renewal approval activation yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the renewal approval activation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
renewal: Marina Leisure Group 2027-2029
newAcv: AED 780,000.00
activation: 01/01/2027
```

#### Permissions

- `getBillingReconciliation` → `PLATFORM_BILLING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-468` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS162 Subscription Licensing AI Self Service Board 10.dc.html#adm-468`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 10
- Flow F216 *Subscription Licensing AI Self Service board 10: Billing & Commercial Command …*, step 18: Works in Renewal Approval, Activation & Commercial Handoff → Finalize renewal and synchronize the approved future commercial agreement across TICVAI.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-468?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-459`.
- [ ] Every gated control is gated: `PLATFORM_BILLING_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P09 reference designs** (from `handoff/design-batches/apps/6-ticvai-controller/README.md`)

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: the client-approved POS, for operator density and components.
- `sources/designs/TICVAI_Mobile.dc.html`: for finish and motion.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-028, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-039, DI-040, DI-041, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

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

### Across P09 TICVAI Web

- Portal access exposes TICVAI pricing, so prospects submit contact details and a trade license as proof of a real venue, reviewed and approved by TICVAI before access is granted. *(agreed · MoM 10 Sep 2026, 4.8 Customer Portal Access, Authentication & Verification · DI-827)*
- Simulation functionality stays embedded within each relevant configuration section rather than being consolidated, since it tests that section's own configuration. *(agreed · MoM 8 Sep 2026, 4.11 Dashboard & Reporting Module Consolidation Strategy · DI-722)*
- **Open question.** Proposed tenant hierarchy Tenant > Organization/Brand > Region > Branch > Venue > Department, under review against TICVAI's own organisational hierarchy before finalising. *(open · MoM 30 Jul 2026, 2. Proposed Multi-Tenant Hierarchy · DI-055)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Chart cards: title with period dropdown ("This Week"), headline metrics with deltas (Tickets Sold 12,840 +8.7%, Visitors, Conversion). Data visualisations must be easy to read. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Charts · DI-041)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Dynamic KPIs, forecasts and real-time insights; role-based dashboards, preferences and smart shortcuts for every user (e.g. greeting "Good morning, Ahmed" on the home screen, p2). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Smarter Data / Personalized Experience · DI-028)*

**4 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"cancelInvoice": {"method":"POST","path":"/invoices/{invoiceId}/cancel","contract":"subscription","summary":"Cancel or credit an invoice","permission":"PLATFORM_BILLING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"disputeInvoice": {"method":"POST","path":"/invoices/{invoiceId}/dispute","contract":"subscription","summary":"Raise a dispute","permission":"PLATFORM_BILLING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"generateInvoice": {"method":"POST","path":"/tenants/{tenantId}/invoices","contract":"subscription","summary":"Generate an invoice for a period","permission":"PLATFORM_BILLING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SubscriptionInvoice"},
"getBillingReconciliation": {"method":"GET","path":"/billing-reconciliation","contract":"subscription","summary":"Metered consumption against what was invoiced","permission":"PLATFORM_BILLING_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"platform","parameters":[{"name":"tenantId","in":"query","required":true},{"name":"period","in":"query","required":true}],"requestBody":null,"responds":"BillingReconciliation"},
"getPlanRecommendations": {"method":"GET","path":"/plan-recommendations","contract":"subscription","summary":"Which plan, module or pack would fit this tenant better, and what it would cost or save","permission":"PLATFORM_BILLING_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"platform","parameters":[{"name":"tenantId","in":"query","required":true},{"name":"horizonMonths","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"issueCreditNote": {"method":"POST","path":"/invoices/{invoiceId}/credit-notes","contract":"subscription","summary":"Issue a credit note against a tenant invoice, in full or in part","permission":"PLATFORM_BILLING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"IssueCreditNoteRequest","responds":"SubscriptionCreditNote"},
"listCreditNotes": {"method":"GET","path":"/tenants/{tenantId}/credit-notes","contract":"subscription","summary":"List a tenant's credit notes","permission":"PLATFORM_BILLING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"invoiceId","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSubscriptionInvoices": {"method":"GET","path":"/tenants/{tenantId}/invoices","contract":"subscription","summary":"List subscription invoices","permission":"PLATFORM_BILLING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTenants": {"method":"GET","path":"/tenants","contract":"subscription","summary":"List tenants","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"status","in":"query","required":null},{"name":"planId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"previewSubscriptionChange": {"method":"POST","path":"/tenants/{tenantId}/subscription/preview","contract":"subscription","summary":"Preview the effect of a plan change","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SetSubscriptionRequest","responds":"SubscriptionPreview"},
"recordInvoicePayment": {"method":"POST","path":"/invoices/{invoiceId}/payment","contract":"subscription","summary":"Record payment against an invoice","permission":"PLATFORM_BILLING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"setSubscription": {"method":"PUT","path":"/tenants/{tenantId}/subscription","contract":"subscription","summary":"Assign or change a subscription","permission":"PLATFORM_TENANT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SetSubscriptionRequest","responds":"Subscription"},
"settleAiUsage": {"method":"POST","path":"/ai-usage/settle","contract":"subscription","summary":"Turn metered AI interactions into a billable usage record","permission":"PLATFORM_BILLING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"simulateCommercialPackage": {"method":"POST","path":"/package-simulations","contract":"subscription","summary":"What this package would cost, and what it would provision","permission":"PLATFORM_PLAN_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"platform","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PackageSimulationRequest","responds":"PackageSimulation"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"BillingReconciliation": {"type":"object","description":"Boards 10.2 and 10.3. **The first invoice sets the tone for the relationship.**","properties":{"tenantId":{"type":"string","format":"uuid"},"period":{"type":"string"},"lines":{"type":"array","items":{"type":"object","properties":{"unit":{"type":"string"},"meteredQuantity":{"type":"integer"},"billedQuantity":{"type":"integer"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"variance":{"type":"integer"}}}},"meteredNotBilled":{"type":"integer"},"billedNotMetered":{"type":"integer"},"invoiceId":{"type":"string","format":"uuid","nullable":true},"approvedBy":{"type":"string","format":"uuid","nullable":true}}},
"CellTier": {"type":"string","enum":["shared","dedicated","isolated","clientHosted"]},
"DowngradeConflictProblem": {"x-ticvai-persistence":"none — error shape","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Problem"},{"type":"object","properties":{"modulesInUse":{"type":"array","description":"Enabled by the tenant but not licensed by the target plan.","items":{"type":"object","properties":{"moduleKey":{"type":"string"},"displayName":{"type":"string"},"isEnabled":{"type":"boolean"}}}},"limitsExceeded":{"type":"array","items":{"type":"object","properties":{"metric":{"$ref":"#/components/schemas/UsageMetric"},"currentUsage":{"type":"integer"},"targetLimit":{"type":"integer"}}}}}}]},
"InvoiceStatus": {"type":"string","enum":["draft","issued","paid","overdue","disputed","cancelled"]},
"IssueCreditNoteRequest": {"type":"object","x-ticvai-persistence":"none — request only","required":["reasonCode","settlement","lines"],"properties":{"reasonCode":{"type":"string","enum":["billingError","serviceCredit","disputeResolution","goodwill","other"]},"reason":{"type":"string","maxLength":500,"nullable":true},"settlement":{"type":"string","enum":["offsetNextInvoice","refund"]},"lines":{"type":"array","minItems":1,"items":{"type":"object","required":["invoiceLineIndex"],"properties":{"invoiceLineIndex":{"type":"integer","minimum":0,"description":"The line of the invoice being credited, by its position in `SubscriptionInvoice.lines`."},"quantity":{"type":"number","minimum":0,"nullable":true,"description":"Part of the line's quantity; null with `amount`, or for the whole line."},"amount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Part of the line's amount, net of tax; null with `quantity`, or for the whole line."}}}}}},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"PackageSimulation": {"type":"object","description":"Boards 3.9 and 4.8. **Refused at quote time rather than at go-live.**","properties":{"lines":{"type":"array","items":{"type":"object","properties":{"kind":{"type":"string","enum":["baseTier","module","addOn","capacityPack","overage","professionalServices","discount"]},"label":{"type":"string"},"quantity":{"type":"number","nullable":true},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"recurringTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"oneOffTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"contractTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"minimumGuarantee":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"findings":{"type":"array","items":{"type":"object","properties":{"severity":{"type":"string","enum":["blocking","warning","advisory"]},"code":{"type":"string"},"message":{"type":"string"}}}},"provisionable":{"type":"boolean"}}},
"PackageSimulationRequest": {"type":"object","required":["tierCode"],"properties":{"tierCode":{"type":"string"},"licensingModelId":{"type":"string","format":"uuid","nullable":true},"moduleCodes":{"type":"array","items":{"type":"string"}},"venueCount":{"type":"integer","default":1},"projectedVolumes":{"type":"object","additionalProperties":{"type":"integer"}},"contractMonths":{"type":"integer","default":12},"billingCycle":{"type":"string","nullable":true},"currency":{"type":"string","nullable":true}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"SetSubscriptionRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["planId"],"properties":{"planId":{"type":"string","format":"uuid"},"planVersion":{"type":"string","description":"Defaults to the current version."},"effectiveFrom":{"type":"string","format":"date","description":"Optional, and set by the server if omitted. Today for an upgrade, `renewsAt` for a downgrade; any other date is refused (audit R214 (1))."},"prorate":{"type":"boolean","default":true,"description":"An upgrade is always prorated and a downgrade, which starts at renewal, never is (audit R214 (1)). Kept so a preview can show the unprorated figure; `setSubscription` applies the rule whatever is sent."},"note":{"type":"string","maxLength":500}}},
"Subscription": {"x-ticvai-persistence":"subscription.contract","type":"object","required":["tenantId","planId","planVersion","status","startsAt"],"properties":{"tenantId":{"type":"string","format":"uuid"},"planId":{"type":"string","format":"uuid"},"planName":{"type":"string"},"planVersion":{"type":"string"},"status":{"type":"string","enum":["trial","active","pastDue","cancelled","expired"]},"startsAt":{"type":"string","format":"date"},"renewsAt":{"type":"string","format":"date","nullable":true},"cancelledAt":{"type":"string","format":"date","nullable":true},"scheduledChange":{"type":"object","nullable":true,"readOnly":true,"description":"A downgrade waiting for the next renewal (decided 28 September, audit R214 (1)). Null when none is scheduled.","properties":{"planId":{"type":"string","format":"uuid"},"planVersion":{"type":"string"},"effectiveFrom":{"type":"string","format":"date","description":"Always the `renewsAt` it was scheduled against."}}},"currentPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"billingPeriod":{"type":"string"}}},
"SubscriptionCreditNote": {"type":"object","x-ticvai-persistence":"control.credit_note + control.credit_note_line","description":"**A credit note against one tenant invoice** (20.7.7, 29 September build): its own number, lines, tax and total. The invoice it credits is never edited.","required":["id","creditNoteNumber","invoiceId","tenantId","reasonCode","settlement","total","issuedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"creditNoteNumber":{"type":"string","readOnly":true,"description":"**Gapless, per issuing legal entity, in its own sequence** (the R152 rule for invoices, decided 28 September, applied to credit notes): assigned at issue, never reused."},"invoiceId":{"type":"string","description":"The invoice credited."},"tenantId":{"type":"string","format":"uuid"},"reasonCode":{"type":"string","enum":["billingError","serviceCredit","disputeResolution","goodwill","other"]},"reason":{"type":"string","maxLength":500,"nullable":true},"settlement":{"type":"string","enum":["offsetNextInvoice","refund"]},"settlementStatus":{"type":"string","enum":["pending","offset","refunded"],"readOnly":true,"description":"`offset` once a later invoice has taken it; `refunded` once the refund is recorded."},"lines":{"type":"array","items":{"type":"object","properties":{"invoiceLineIndex":{"type":"integer"},"description":{"type":"string"},"quantity":{"type":"number","nullable":true},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"subtotal":{"x-ticvai-column":"net_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"total":{"x-ticvai-column":"gross_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"issuedAt":{"type":"string","format":"date-time","readOnly":true},"issuedByPrincipalId":{"type":"string","format":"uuid","readOnly":true}}},
"SubscriptionInvoice": {"x-ticvai-persistence":"control.invoice + control.invoice_line","type":"object","required":["id","invoiceNumber","tenantId","periodStart","periodEnd","status","total"],"properties":{"id":{"type":"string","format":"uuid"},"invoiceNumber":{"type":"string","readOnly":true,"description":"A tax invoice number, so **gapless, per legal entity** (decided 28 September, audit R152): one unbroken sequence for the TICVAI legal entity that issues it, assigned when the invoice is issued, never reused. A cancelled invoice keeps its number.\n"},"tenantId":{"type":"string","format":"uuid"},"periodStart":{"type":"string","format":"date"},"periodEnd":{"type":"string","format":"date"},"status":{"$ref":"#/components/schemas/InvoiceStatus"},"lines":{"type":"array","items":{"type":"object","properties":{"description":{"type":"string"},"kind":{"type":"string","enum":["basePlan","module","addOn","overage","metered","oneOff","credit"],"description":"`module`, one per licensed module at its platform price, and `metered`, usage such as AI tokens (decided 29 September)."},"moduleCode":{"type":"string","nullable":true,"description":"The module a `module` or `metered` line charges for."},"audience":{"type":"string","enum":["staff","guest"],"nullable":true,"description":"For an AI `metered` line, whose usage it is."},"metric":{"$ref":"#/components/schemas/UsageMetric"},"quantity":{"type":"number"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"subtotal":{"x-ticvai-column":"net_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"total":{"x-ticvai-column":"gross_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"planVersionUsed":{"type":"string","description":"Priced against the version the tenant is subscribed to, not the latest."},"creditedTotal":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"nullable":true,"description":"The sum of the credit notes issued against this invoice (`issueCreditNote`); the invoice itself is never edited. Null with none."},"issuedAt":{"type":"string","format":"date-time","nullable":true},"dueAt":{"type":"string","format":"date","nullable":true},"paidAt":{"type":"string","format":"date-time","nullable":true}}},
"SubscriptionPlanRecommendation": {"type":"object","x-ticvai-persistence":"none — computed from control.usage_record, the plan, tier and add-on limits and capacity packs, priced as simulateCommercialPackage prices","description":"One plan-fit move for a tenant, priced against staying as it is (20.8.4, 20.8.5; decided 29 September, build pass, group G2).","required":["kind","reason","projectedMonthlyCost"],"properties":{"kind":{"type":"string","enum":["upgrade","downgrade","addModule","removeModule","removeAddOn","capacityPack"]},"targetPlanId":{"type":"string","format":"uuid","nullable":true,"description":"The tier to move to, for `upgrade` and `downgrade`."},"moduleCode":{"type":"string","nullable":true,"description":"For `addModule` and `removeModule`."},"addOnCode":{"type":"string","nullable":true,"description":"For `removeAddOn`."},"billableUnit":{"type":"string","nullable":true,"description":"The unit that drives it (for `upgrade`, `downgrade` and `capacityPack`), as `getLicenceEnforcement` names it."},"capacityPackSize":{"type":"integer","nullable":true,"description":"For `capacityPack`, the pack size that covers the projected overage."},"projectedMonthlyCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"projectedSaving":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Against staying as it is over the horizon, monthly. Set where the move saves money."},"projectedAddedCost":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Where the move costs more than today but less than the alternative named in `comparedWith`."},"comparedWith":{"type":"string","enum":["currentPackage","projectedOverage","nextTier","capacityPack"],"description":"What the move is cheaper than. An `upgrade` is compared with paying the projected overage; a `capacityPack` with the next tier."},"reason":{"type":"string","maxLength":500,"description":"One sentence a person can repeat to the customer."},"basis":{"type":"object","description":"The numbers it rests on.","properties":{"usageWindowDays":{"type":"integer"},"usedAverage":{"type":"number","nullable":true},"usedPeak":{"type":"number","nullable":true},"projectedPeak":{"type":"number","nullable":true},"currentLimit":{"type":"number","nullable":true},"targetLimit":{"type":"number","nullable":true},"lastUsedAt":{"type":"string","format":"date-time","nullable":true,"description":"For `removeModule` and `removeAddOn`, the last metered use; null for never."}}},"applyWith":{"type":"string","enum":["setSubscription","addCapacityPack"],"description":"The operation a person uses to carry it out (after `previewSubscriptionChange` for `setSubscription`)."}}},
"SubscriptionPreview": {"x-ticvai-persistence":"none — computed","type":"object","required":["canApply","priceChange"],"properties":{"canApply":{"type":"boolean"},"priceChange":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"proratedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"modulesGained":{"type":"array","items":{"type":"string"}},"modulesLost":{"type":"array","items":{"type":"string"}},"conflicts":{"$ref":"#/components/schemas/DowngradeConflictProblem"},"cellTierChange":{"type":"object","nullable":true,"properties":{"from":{"$ref":"#/components/schemas/CellTier"},"to":{"$ref":"#/components/schemas/CellTier"},"requiresMigration":{"type":"boolean"}}}}},
"SuspensionMode": {"type":"string","description":"Access validation continues under every mode. A commercial dispute must not strand guests at a gate holding valid tickets.\n","enum":["readOnly","noNewSales","fullLockout"]},
"Tenant": {"x-ticvai-persistence":"control.tenant","type":"object","required":["id","code","name","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"status":{"$ref":"#/components/schemas/TenantStatus"},"suspensionMode":{"$ref":"#/components/schemas/SuspensionMode"},"suspensionReason":{"type":"string","nullable":true},"suspensionEffectiveAt":{"type":"string","format":"date-time","nullable":true,"description":"When the suspension takes, or took, effect — `suspendTenant.effectiveAt`. **A future value is a pending suspension**: the tenant stays `active` until then, and this row is the only place that says a suspension is coming."},"suspensionNoticeMessage":{"$ref":"#/components/schemas/subscription::LocalisedText","description":"The notice shown to the tenant's users about the suspension — `suspendTenant.noticeMessage`."},"terminationScheduledAt":{"type":"string","format":"date-time","nullable":true,"description":"When `terminateTenant` started the retention window. Null when no termination is under way."},"terminationRetentionUntil":{"type":"string","format":"date-time","nullable":true,"description":"`terminationScheduledAt` plus the request's `retentionDays`. **Stored, not recomputed** — the day count is client-supplied and exists nowhere else, and this is the date the cells are destroyed after."},"terminationReason":{"type":"string","maxLength":1000,"nullable":true},"terminationRequestedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"planId":{"type":"string","format":"uuid","nullable":true},"planName":{"type":"string","nullable":true},"cellCount":{"type":"integer"},"venueCount":{"type":"integer"},"regionId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The tenant's home region: the `tenancy` region node whose `RegionSettings` govern tenant-wide gates, today `allowedAiResidencies` (decided 28 September, audit R203). Written by the server when the tenant's first region is created; null until then. ADM-037 reads it to show the region's residency restriction, and `ai.setAiProvider` checks against the same region.\n"},"billingEmail":{"type":"string"},"billingAddress":{"type":"string","maxLength":500,"nullable":true,"description":"Accepted by `createTenant` and `updateTenant`; stored here so the response can return what was sent."},"accountManagerPrincipalId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"activatedAt":{"type":"string","format":"date-time","nullable":true}}},
"TenantStatus": {"type":"string","enum":["onboarding","active","suspended","terminating","terminated"]},
"UsageMetric": {"type":"string","enum":["venues","workstations","activeUsers","devices","brandedApps","aiTokens","apiCalls","storageGb","transactions","guestProfiles"]}
}
```
