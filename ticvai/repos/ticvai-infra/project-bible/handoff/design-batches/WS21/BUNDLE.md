# WS21 — B2B, Reseller & OTA Partner Management board 1

**8 screens · 14 operations · 23 schemas · 3 permissions**

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
  `PARTNER_MANAGE, PLATFORM_CELL_MANAGE, PLATFORM_TENANT_VIEW`. A control nobody can use must say so,
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
| `PTR-022` | Partner Management Command Center | B–D | 2 | 30 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `PTR-023` | Partner Profile & Organization Setup | B–D | 16 | 0 | 5 | 0 | 2 | 0 | — | notStarted (generated) |
| `PTR-024` | Partner Onboarding & Application Workflow | B–D | 15 | 0 | 5 | 0 | 3 | 0 | — | notStarted (generated) |
| `PTR-025` | Partner Contacts & User Administration | B–D | 40 | 0 | 5 | 5 | 1 | 0 | — | notStarted (generated) |
| `PTR-027` | Partner Brand, Venue & Business Scope Assignment | B–D | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `PTR-028` | Partner Documentation & Compliance Repository | B–D | 15 | 0 | 5 | 0 | 2 | 0 | — | notStarted (generated) |
| `PTR-030` | Partner Approval, Status & Lifecycle Management | B–D | 12 | 0 | 5 | 0 | 2 | 3 | — | notStarted (generated) |
| `PTR-031` | Partner 360° Profile, Readiness & AI Review | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**PTR-027, PTR-031 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `PTR-022` Partner Management Command Center

**Provide a centralized management dashboard for all B2B, reseller, OTA and distribution partners across the TICVAI ecosystem.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner staff holding `PLATFORM_TENANT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each partner record should display) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/partners/partner-management-command-center-ptr-022` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The partner-management hub for the tenant's (or TICVAI's) partner team, not for partner users: partners by status, onboarding, approvals, credit holds, expiring agreements, sales.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SOT-015).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search partner | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by partner type, country, territory, brand, venue, account manager and 5 more — which are present is a decision the pack already made. | — |

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

**Total Partners** (metric tile)

**Active Partners** (metric tile)

**Pending Onboarding** (metric tile)

**Pending Approval** (metric tile)

**Suspended Partners** (metric tile)

**Expiring Agreements** (metric tile)

**Documentation Issues** (metric tile)

**Partners With Credit Holds** (metric tile)

**Connected OTA/API Partners** (metric tile)

**Partner Sales YTD** (metric tile)

**Partner Revenue YTD** (metric tile)

**High-Risk Partners** (metric tile)

**Every partner** (data table, from `listPartner`)

| Shows | Format | Notes |
|---|---|---|
| Partner | the name it points at, never the id | Partner ID |
| Trading name | text | Trading Name |
| Legal entity | text | Legal Entity |
| Partner type | text | Partner type code from the tenant's configurable partner-type list (MoM 31 Aug 4.3: configurable category/type), seeded with the pack's p.7 … |
| Country | text | Country, ISO 3166-1 alpha-2 |
| Territory | text | Territory: summary of the authorised markets (listTerritoryMarketDistribution) |
| Assigned brand/venue | text | not in the schema: `Assigned Brand/Venue` |
| Commercial owner | text | Commercial Owner: staff display name of the account manager |
| Distribution channel | list or chips (count when long) | Distribution Channel: Distribution methods: b2bPortal (the TICVAI B2B portal), api (partner consumes the TICVAI API), otaConnection (TICVAI … |
| Account status | text | Account Status: lead, applicant, underReview, approved, configuration, active, restricted, suspended, terminated or archived (pack p.6 and … |
| Onboarding status | text | Onboarding Status: the application stage (application, businessVerification, documentation, commercialReview, financeReview … |
| Agreement status | chip: Pending approval, Active, Expiring soon, Expired, Suspended, Terminated | Agreement Status of the partner's current agreement; empty when none |
| Credit status | text | Credit Status: notEnabled, withinLimit, warning (at the warning threshold), highRisk, onHold or blocked (decided 29 September, readiness … |
| Integration status | chip: None, Testing, Connected, Degraded, Disconnected | Integration Status: none, testing, connected, degraded or disconnected (decided 29 September, readiness close-out). |
| Last activity | 1 Oct 2026, 14:30 | Last Activity |

**The selected partner** (detail panel): The pack groups this record's detail under its own headings: “Partner Attention Required”.

| Shows | Format | Notes |
|---|---|---|
| Partner | the name it points at, never the id | Partner ID |
| Trading name | text | Trading Name |
| Legal entity | text | Legal Entity |
| Partner type | text | Partner type code from the tenant's configurable partner-type list (MoM 31 Aug 4.3: configurable category/type), seeded with the pack's p.7 … |
| Country | text | Country, ISO 3166-1 alpha-2 |
| Territory | text | Territory: summary of the authorised markets (listTerritoryMarketDistribution) |
| Assigned brand/venue | text | not in the schema: `Assigned Brand/Venue` |
| Commercial owner | text | Commercial Owner: staff display name of the account manager |
| Distribution channel | list or chips (count when long) | Distribution Channel: Distribution methods: b2bPortal (the TICVAI B2B portal), api (partner consumes the TICVAI API), otaConnection (TICVAI … |
| Account status | text | Account Status: lead, applicant, underReview, approved, configuration, active, restricted, suspended, terminated or archived (pack p.6 and … |
| Onboarding status | text | Onboarding Status: the application stage (application, businessVerification, documentation, commercialReview, financeReview … |
| Agreement status | chip: Pending approval, Active, Expiring soon, Expired, Suspended, Terminated | Agreement Status of the partner's current agreement; empty when none |
| Credit status | text | Credit Status: notEnabled, withinLimit, warning (at the warning threshold), highRisk, onHold or blocked (decided 29 September, readiness … |
| Integration status | chip: None, Testing, Connected, Degraded, Disconnected | Integration Status: none, testing, connected, degraded or disconnected (decided 29 September, readiness close-out). |
| Last activity | 1 Oct 2026, 14:30 | Last Activity |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Create Partner, Review Application, Approve, Assign Account Manager, Suspend, Open Commercial Profile, View Users, View Documents, View Performance. Each needs attaching to the control it gates, or the screen needs the control.

**Data it reads**: `listPartner2` (onLoad, Partner Operations Command Center); `listPartner` (onLoad, Partner Management Command Center)

**Where the user goes next**

- → `PTR-023` Partner Profile & Organization Setup: *Sets up the organisation record*; calls `listPartner`
- → `PTR-024` Partner Onboarding & Application Workflow: *Reads the application the applicant submitted*; calls `listPartner`
- → `PTR-027` Partner Brand, Venue & Business Scope Assignment: *Assigns the brands, venues and business scope the partner may sell*; calls `listPartner`
- → `PTR-028` Partner Documentation & Compliance Repository: *Checks the compliance and documentation file*; calls `listPartner`
- → `PTR-025` Partner Contacts & User Administration: *Creates the partner's first user*; calls `listPartner`
- → `PTR-030` Partner Approval, Status & Lifecycle Management: *Approves the partner and moves it to active*; calls `listPartner`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The partner list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partner untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No partners yet. Offers no create action here: a partner arrives through onboarding (PTR-024), and this screen says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the partner are still there. The pack's own statuses are Suspended → Terminated → Archived — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
metric tiles:
  Total Partners: 128
  Active Partners: 46
  Pending Onboarding: 312
  Pending Approval: 74
  Suspended Partners: AED 96,750.00
  Expiring Agreements: 233
  Documentation Issues: 0
  Partners With Credit Holds: 11
  Connected OTA/API Partners: 128
  Partner Sales YTD: 46
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
- Partner overview lists all B2B partners with status, pending approvals and documentation state. Partner profile captures company info and a configurable partner category/type; profile fields are fully customisable. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-547)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-022` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS38 B2B, Reseller & OTA Partner Management Board 1.dc.html#ptr-022`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 1
- Flow F110 *A partner is onboarded onto the B2B portal*, step 2: Opens the partner command centre → Every partner and every pending application in one place
- Flow F110 *A partner is onboarded onto the B2B portal*, step 4: Returns to the command centre → Application read, nothing yet granted
- Flow F110 *A partner is onboarded onto the B2B portal*, step 6: Returns to the command centre → Organisation known, scope still unbounded
- Flow F110 *A partner is onboarded onto the B2B portal*, step 8: Returns to the command centre → Scope set, compliance unverified
- Flow F110 *A partner is onboarded onto the B2B portal*, step 10: Returns to the command centre → Compliance checked
- Flow F110 *A partner is onboarded onto the B2B portal*, step 12: Returns to the command centre → Everything configured, nothing yet live
- Flow F110 branch at step 10 (requiresStaff): when No permission profile exists to choose, The permission profile the partner's users inherit is chosen on PTR-029, which is a Venue Management staff screen since 2 October 2026 (CHG-CLN-004) and is reached from Venue Home, not from this hub. …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (30 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-022?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `PTR-023`, `PTR-024`, `PTR-027`, `PTR-028`, `PTR-025`, `PTR-030`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-023` Partner Profile & Organization Setup

**Create the master business record for each external distribution partner.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner staff holding `PLATFORM_CELL_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/partners/partner-profile-organization-setup-ptr-023` |

**Known gaps.** **The pack names 2 actions on this screen and the screen declares 1 operation.** Unserved: Key Account, New Partner. Each needs an operation, or needs removing from the screen; this is the Phase 3 …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The master record of a distribution partner: legal entity, trading name, type, registration, tax number, addresses, currency, time zone.

**Fixed on main** (the package already carries these; draw what it says): Fields drawn as drop-downs that cannot be choices: text field: Legal Entity Name, Trading Name, Registration Number, Tax/VAT Number, City … (CHG-SOT-015).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Partner ID | select field | — | — | — | — | — | — |
| Legal Entity Name | text field | — | — | — | — | — | — |
| Trading Name | text field | — | — | — | — | — | — |
| Partner Type | select field | — | — | — | — | — | — |
| Registration Number | text field | — | — | — | — | — | — |
| Tax/VAT Number | text field | — | — | — | — | — | — |
| Country | select field | — | — | — | — | — | — |
| City | text field | — | — | — | — | — | — |
| Registered Address | text field | — | — | — | — | — | — |
| Business Address | text field | — | — | — | — | — | — |
| Website | text field | — | — | — | — | — | — |
| Main Telephone | select field | — | — | — | — | — | — |
| General Email | select field | — | — | — | — | — | — |
| Preferred Language | select field | — | — | — | — | — | — |
| Default Currency | select field | — | — | — | — | — | — |
| Time Zone | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Registration and tax numbers**: Format checked per country; partner code unique per tenant. *(source: R108)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Key Account (primary button) | navigation or local | — | — | — | — |
| New Partner (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `PTR-022` Partner Management Command Center: *Returns to the command centre*; calls `setPartnerProfileOrganization`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The partner profile organization configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partner profile organization untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No partner profile organization configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
form example:
  Partner ID: Marina Leisure Group
  Legal Entity Name: 312
  Trading Name: 57
  Partner Type: Marina Leisure Group
  Registration Number: 11
  Tax/VAT Number: 74
  Country: 233
  City: 74
  Registered Address: 312
  Business Address: 46
  Website: 46
  Main Telephone: 46
  General Email: 46
  Preferred Language: 42 min
```

#### Permissions

- `setPartnerProfileOrganization` → `PLATFORM_CELL_MANAGE` (configure) · partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Partner overview lists all B2B partners with status, pending approvals and documentation state. Partner profile captures company info and a configurable partner category/type; profile fields are fully customisable. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-547)*
- B2B account financial tab shows credit limit, credit days and a linked account-specific price list; accounts can be a main account with child (agent) accounts; every account shows its full sales/transaction history, as does a B2C customer profile. *(client request · MoM 7 Aug 2026, 11. Accounts Management (B2B and B2C) · DI-162)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-023` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS38 B2B, Reseller & OTA Partner Management Board 1.dc.html#ptr-023`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 1
- Flow F110 *A partner is onboarded onto the B2B portal*, step 5: Sets up the organisation record → Legal entity, trading name, tax identity and billing address

#### Acceptance for the design

- [ ] Every input above is drawn (16), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-023?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Key Account, New Partner.
- [ ] Every transition is wired: `PTR-022`.
- [ ] Every gated control is gated: `PLATFORM_CELL_MANAGE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-024` Partner Onboarding & Application Workflow

**Manage the complete journey from a new partner application through internal review and activation.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner staff holding `PARTNER_MANAGE`, `PLATFORM_TENANT_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `applicationId` (navigation) |
| Route | `/partners/partner-onboarding-application-workflow-ptr-024` |

**Known gaps.** **The pack names 5 actions on this screen; 1 are served since the writers pass (29 September): Request More Information by `actOnPartnerApplicationReview`.** Still unserved: Product requirements …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** A partner application from submission through review to activation: documents validated, reject with a message that prompts resubmission, approve to send credentials with a temporary password.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SOT-015).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Company information | select field | — | — | — | — | — | — |
| Requested partner type | select field | — | — | — | — | — | — |
| Markets | select field | — | — | — | — | — | — |
| Expected sales volume | select field | — | — | — | — | — | — |
| Requested products | select field | — | — | — | — | — | — |
| Requested venues | select field | — | — | — | — | — | — |
| Preferred distribution method | select field | — | — | — | — | — | — |
| Estimated annual business | select field | — | — | — | — | — | — |
| Contact information | select field | — | — | — | — | — | — |
| Billing requirements | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Stage | select | — | Application · Business verification · Documentation · Commercial review · Finance review · Technical review · Approval · Configuration · Activation | `listPartnerOnboardingApplication` ?stage |
| Status | select | — | Submitted · In review · More information requested · Approved · Rejected · Withdrawn | `listPartnerOnboardingApplication` ?status |
| Requested partner type | text field | — | — | `listPartnerOnboardingApplication` ?requestedPartnerType |
| Search | text field | — | — | `listPartnerOnboardingApplication` ?search |

**Form: Act on partner application review** (modal, opened by *Act on partner application review*; *Act on partner application review* calls `actOnPartnerApplicationReview`, *Cancel* sends nothing)

**Collects what `actOnPartnerApplicationReview` sends before it is called.** Required: `action`. Optional: `department`, `assigneePrincipalId`, `note`, `documentIds`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Action `action` | radio group | required | — | Start review · Complete task · Request information · Supply information · Withdraw | — | The action (states/partner-application.yaml) | `actOnPartnerApplicationReview` body |
| Department `department` | radio group | optional | — | Commercial · Finance · Operations · Technical | — | For completeTask, the department whose review task is done | `actOnPartnerApplicationReview` body |
| Assignee principal `assigneePrincipalId` | picker: choose an assignee principal | optional | — | — | shows names, sends the id | For startReview, who each opened task is assigned to when one person reviews all; empty leaves them to each department's queue | `actOnPartnerApplicationReview` body |
| Note `note` | text area | optional | — | — | — | The reviewer's finding (completeTask), what is missing (requestInformation, required) or the applicant's answer (supplyInformation) | `actOnPartnerApplicationReview` body |
| Documents `documentIds` | multi-picker: choose documents | optional | — | — | — | For supplyInformation, documents uploaded in answer (control.partner_document) | `actOnPartnerApplicationReview` body |

Errors to draw in the form: 404 No such application; 409 The action does not fit the application's status (states/partner-application.yaml); 422 No open review task for that department, or a requestInformation without a note

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Product requirements (primary button) | navigation or local | — | — | — | — |
| Sequential approval (secondary button) | navigation or local | — | — | — | — |
| Parallel approval (secondary button) | navigation or local | — | — | — | — |
| Rejection (secondary button) | navigation or local | — | — | — | — |
| Request More Information (secondary button) | navigation or local | — | — | — | — |
| Act on partner application review (secondary button) | `actOnPartnerApplicationReview` POST `/partner-applications/{applicationId}/review-actions` | PartnerApplicationReviewAction | PartnerApplication | 404 No such application; 409 The action does not fit the application's status (states/partner-application.yaml); 422 No open review task for that department, or a requestInformation without a note | gated `PARTNER_MANAGE`; opens modal first |

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Approve application**: Creates the partner and its first user; the welcome email carries a temporary password that must be changed at first sign-in. *(source: DI-166; DI-548; F110 step 1)*

**Data it reads**: `listPartnerOnboardingApplication` (onLoad, Partner Onboarding & Application Workflow)

**Where the user goes next**

- → `PTR-022` Partner Management Command Center: *Returns to the command centre*; calls `listPartnerOnboardingApplication`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The partner onboarding application configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partner onboarding application untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No applications waiting: nothing to review, which is good news. Offers no create action; applications arrive from the partner sign-up. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The action does not fit the application's status (states/partner-application.yaml); 422 No open review task for that department, or a requestInformation without a note |

#### Edge cases to draw

- **Can read but not change (holds PLATFORM_TENANT_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: PARTNER_MANAGE for Act on partner application review. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/subscription.yaml#actOnPartnerApplicationReview)*
- **actOnPartnerApplicationReview answers 409**: Show it as something the person can act on, not a failure: The action does not fit the application's status (states/partner-application.yaml) *(source: contracts/satellite/subscription.yaml#actOnPartnerApplicationReview)*
- **actOnPartnerApplicationReview answers 422**: Show it as something the person can act on, not a failure: No open review task for that department, or a requestInformation without a note *(source: contracts/satellite/subscription.yaml#actOnPartnerApplicationReview)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
form example:
  Company information: 74
  Requested partner type: Desert Gate Tours LLC
  Markets: 46
  Expected sales volume: 128
  Requested products: 57
  Requested venues: 7
  Preferred distribution method: 74
  Estimated annual business: 128
  Contact information: 74
  Billing requirements: AED 12,400.00
```

#### Permissions

- `listPartnerOnboardingApplication` → `PLATFORM_TENANT_VIEW` (read) · partner
- `actOnPartnerApplicationReview` → `PARTNER_MANAGE` (configure) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Partner onboarding: partner signs up via a registration link/form on the B2B platform, then review and approval, with confirmation emails and back-office visibility of required next steps. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-548)*
- Partner review: operations validate documents and can reject (e.g. expired trade licence) with a message prompting resubmission; approval emails credentials with a temporary password, and the partner must set their own password at first login. *(client request · MoM 7 Aug 2026, 13. Tenant/B2B Onboarding & Self-Registration Flow · DI-166)*
- "Become a partner" link on the tenant website opens a registration form capturing company type, name, address, Emirate/state and documents (trade licence, VAT/TRN certificate); submitting creates a pending account and emails the tenant's operations team. *(client request · MoM 7 Aug 2026, 13. Tenant/B2B Onboarding & Self-Registration Flow · DI-165)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-024` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS38 B2B, Reseller & OTA Partner Management Board 1.dc.html#ptr-024`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 1
- Flow F110 *A partner is onboarded onto the B2B portal*, step 3: Reads the application the applicant submitted → The application, its documents and its declared trading intent
- Flow F110 branch at step 3 (abandonsFlow): when The applicant could not submit an application at all, `submitOnboardingApplication` is `public` and requires `TENANT_CONFIGURE`. Until that is reconciled the only working front door is `registerPartner`, and any journey that depends on the application …

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-024?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Product requirements, Sequential approval, Parallel approval, Rejection, Request More Information, Act on partner application review.
- [ ] Every transition is wired: `PTR-022`.
- [ ] Every gated control is gated: `PARTNER_MANAGE`, `PLATFORM_TENANT_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-025` Partner Contacts & User Administration

**Manage the individuals authorized to interact with TICVAI on behalf of each partner.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner staff holding `PARTNER_MANAGE`, `PLATFORM_TENANT_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `partnerId` (session) |
| Route | `/partners/partner-contacts-user-administration-ptr-025` |

**Known gaps.** **The pack names 9 actions on this screen; 6 are served since the writers pass (29 September): Primary Contact, Commercial, Finance, Operations, Management, Emergency Contact by …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The people who act for a partner: contacts by type and users with role, branch, sales location and currency.

**Fixed on main** (the package already carries these; draw what it says): formCreatePartnerUser asks the person for id. (CHG-SOT-015).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Name | select field | — | — | — | — | — | — |
| Position | select field | — | — | — | — | — | — |
| Department | select field | — | — | — | — | — | — |
| Email | select field | — | — | — | — | — | — |
| Mobile | select field | — | — | — | — | — | — |
| Telephone | select field | — | — | — | — | — | — |
| Language | select field | — | — | — | — | — | — |
| Time Zone | select field | — | — | — | — | — | — |
| Contact Type | select field | — | — | — | — | — | — |
| Status | select field | — | — | — | — | — | — |
| Username | select field | — | — | — | — | — | — |
| Partner | select field | — | — | — | — | — | — |
| Branch | select field | — | — | — | — | — | — |
| Role | select field | — | — | — | — | — | — |
| Permissions | select field | — | — | — | — | — | — |
| Sales Location | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Partner | picker: choose a partner | — | — | `listPartnerContactUser` ?partnerId |
| Contact type | select | — | Primary · Commercial · Reservations · Finance · Technical · Operations · Management · Emergency | `listPartnerContactUser` ?contactType |
| Status | radio group | — | Invited · Active · Disabled · Revoked · Expired | `listPartnerContactUser` ?status |
| Has user account | toggle | — | — | `listPartnerContactUser` ?hasUserAccount |
| Search | text field | — | — | `listPartnerContactUser` ?search |

**Form: Save partner contact** (modal, opened by *Save partner contact*; *Save partner contact* calls `setPartnerContact`, *Cancel* sends nothing)

**Collects what `setPartnerContact` sends before it is called.** Required: `partnerId`. Optional: `contactId`, `action`, `name`, `position`, `department`, `email`, `mobile`, `telephone`, `language`, `timeZone`, `contactType`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Contact `contactId` | picker: choose a contact | optional | — | — | shows names, sends the id | The contact to change; omit to create | `setPartnerContact` body |
| Partner `partnerId` | picker: choose a partner | required | — | — | shows names, sends the id | The partner (control.partner) | `setPartnerContact` body |
| Action `action` | radio group | optional | Save | Save · Disable · Enable · Revoke | — | save creates or edits; disable, enable and revoke change access (states/partner-contact.yaml) | `setPartnerContact` body |
| Name `name` | text field | optional | — | — | — | Name; required to create | `setPartnerContact` body |
| Position `position` | text field | optional | — | — | — | — | `setPartnerContact` body |
| Department `department` | text field | optional | — | — | — | — | `setPartnerContact` body |
| Email `email` | email field | optional | — | — | name@example.ae | — | `setPartnerContact` body |
| Mobile `mobile` | phone field | optional | — | — | +971 5X XXX XXXX (E.164) | — | `setPartnerContact` body |
| Telephone `telephone` | phone field | optional | — | — | +971 5X XXX XXXX (E.164) | — | `setPartnerContact` body |
| Language `language` | text field | optional | — | — | — | BCP 47 tag | `setPartnerContact` body |
| Time zone `timeZone` | text field | optional | — | — | — | IANA name | `setPartnerContact` body |
| Contact type `contactType` | select | optional | — | Primary · Commercial · Reservations · Finance · Technical · Operations · Management · Emergency | — | Contact type; required to create | `setPartnerContact` body |

Errors to draw in the form: 404 No such contact or partner; 409 The action does not fit the contact's status (states/partner-contact.yaml), or it would leave the partner with no active primary contact

**Form: Create partner user** (modal, opened by *Create partner user*; *Create partner user* calls `createPartnerUser`, *Cancel* sends nothing)

**Collects what `createPartnerUser` sends before it is called.** The person picks the user (by name) and their branch, then the role, sales location, currency, expiry and limits; `partnerId` comes from the session. Never `id` or `status`: an id is a client UUIDv7 generated silently and the status and timestamps are the server's (design-notes correction, CHG-SOT-015). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createPartnerUser` body |
| Partner `partnerId` | picker: choose a partner | required | — | — | shows names, sends the id | The partner (control.partner) the user belongs to. | `createPartnerUser` body |
| Principal `principalId` | picker: choose a principal | required | — | — | shows names, sends the id | — | `createPartnerUser` body |
| Role `role` | text field | optional | — | — | — | The partner role shown for the user: Partner Administrator, Booking Agent, Supervisor, Finance User, Reporting User or API Administrator (pack p.12). | `createPartnerUser` body |
| Sales location `salesLocation` | text field | optional | — | — | — | The sales location (branch office or desk) the user sells from, shown on listPartnerContactUser (decided 29 September, writers pass; DM4) | `createPartnerUser` body |
| Currency `currency` | text field | optional | — | pattern `^[A-Z]{3}$` | — | Currency the user sells in, ISO 4217; empty means the agreement's settlementCurrency (decided 29 September, writers pass; DM4) | `createPartnerUser` body |
| Account expires at `accountExpiresAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | When the user's account expires; empty for no expiry. | `createPartnerUser` body |
| Branch scope path `branchScopePath` | text field | required | — | — | — | The branch this user sits on. An ltree, like every other scope path, so a report at agency level rolls up its branches without anybody writing a join. | `createPartnerUser` body |
| Allocation quota `allocationQuota` | number field | optional | — | — | — | Units this branch may sell. Null inherits the parent's, and a quota set at branch level below the agency's is a deliberate restriction rather than an error. | `createPartnerUser` body |
| Credit limit override `creditLimitOverride` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createPartnerUser` body |
| Can manage users `canManageUsers` | toggle | optional | off | — | — | Partner-managed access control — 2.7.51 asks for it, and a venue administering every travel agent's staff list is a venue doing the agency's HR. | `createPartnerUser` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Primary Contact (primary button) | navigation or local | — | — | — | — |
| Commercial (secondary button) | navigation or local | — | — | — | — |
| Finance (secondary button) | navigation or local | — | — | — | — |
| Operations (secondary button) | navigation or local | — | — | — | — |
| Management (secondary button) | navigation or local | — | — | — | — |
| Emergency Contact (secondary button) | navigation or local | — | — | — | — |
| Password policy (secondary button) | navigation or local | — | — | — | — |
| SSO where available (secondary button) | navigation or local | — | — | — | — |
| Save partner contact (secondary button) | `setPartnerContact` PUT `/partner-contacts` | PartnerContactInput | PartnerContact | 404 No such contact or partner; 409 The action does not fit the contact's status (states/partner-contact.yaml), or it would leave the partner with no active primary contact | gated `PARTNER_MANAGE`; opens modal first |
| Create partner user (secondary button) | `createPartnerUser` POST `/partners/{partnerId}/users` | PartnerUser | PartnerUser | — | gated `PARTNER_MANAGE`; opens modal first |

**Data it reads**: `listPartnerContactUser` (onLoad, Partner Contacts & User Administration)

**Where the user goes next**

- → `PTR-022` Partner Management Command Center: *Returns to the command centre*; calls `listPartnerContactUser`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The partner contacts user configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partner contacts user untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No partner contacts user configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The action does not fit the contact's status (states/partner-contact.yaml), or it would leave the partner with no active primary contact |

#### Edge cases to draw

- **Can read but not change (holds PLATFORM_TENANT_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: PARTNER_MANAGE for Save partner contact, Create partner user. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/subscription.yaml#setPartnerContact)*
- **setPartnerContact answers 404**: Show it as something the person can act on, not a failure: No such contact or partner *(source: contracts/satellite/subscription.yaml#setPartnerContact)*
- **setPartnerContact answers 409**: Show it as something the person can act on, not a failure: The action does not fit the contact's status (states/partner-contact.yaml), or it would leave the partner with no active primary contact *(source: contracts/satellite/subscription.yaml#setPartnerContact)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
form example:
  Name: 19
  Position: 46
  Department: Retail
  Email: 128
  Mobile: 312
  Telephone: 57
  Language: 1.8 s
  Time Zone: 42 min
  Contact Type: 19
  Status: 11
  Username: 312
  Partner: Arabian Trails
  Branch: 312
  Role: 46
```

#### Permissions

- `listPartnerContactUser` → `PLATFORM_TENANT_VIEW` (read) · partner
- `setPartnerContact` → `PARTNER_MANAGE` (configure) · staff, partner
- `createPartnerUser` → `PARTNER_MANAGE` (configure) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.7.7 | Master accounts must be able to create sub-users with limited permissions to avoid sharing login credentials and security risks. | Ticketing Sales | CONTRACTED | data `PartnerUser` |
| 2.7.18 | Each BtoB Customer can ask for an account. It is expected to have the possibility to create a login and password for the BtoB Customers. | Ticketing Sales | CONTRACTED | data `PartnerUser` |
| 2.7.34 | The system should support, at minimum, the following security controls for the B2B portal: - Password protected access to the B2B portal. B2B set-up of own users/passwords. - Forgot password … | Ticketing Sales | CONTRACTED | data `PartnerUser` |
| 2.7.51 | System shall support hierarchical B2B account structures such as Master Agency, Branch, Department, and User. Permissions, quotas, credit limits, pricing, and reporting access shall be configurable … | Ticketing Sales | CONTRACTED | data `PartnerUser` |
| 3.5.7 | Support tiered B2B2C or B2B2B2C approach, White-label B2B portal with master / sub-agent user hierarchy and role controls | Admission and Access | CONTRACTED | data `PartnerUser` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A partner has multiple agents/sub-agents who can each sell on its behalf; territory/market rights set the regions it may sell into; brand/venue association sets which venues and products it can sell, with distinct pricing per venue. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-549)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-025` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS38 B2B, Reseller & OTA Partner Management Board 1.dc.html#ptr-025`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 1
- Flow F110 *A partner is onboarded onto the B2B portal*, step 11: Creates the partner's first user → One identity inside the partner organisation

#### Acceptance for the design

- [ ] Every input above is drawn (40), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-025?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Primary Contact, Commercial, Finance, Operations, Management, Emergency Contact, Password policy, SSO where available, Save partner contact, Create partner user.
- [ ] Every transition is wired: `PTR-022`.
- [ ] Every gated control is gated: `PARTNER_MANAGE`, `PLATFORM_TENANT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-027` Partner Brand, Venue & Business Scope Assignment

**Determine which TICVAI business entities the partner relationship covers. This is deliberately separate from product assignment, which is governed through the Sales Channel and commercial configuration layers.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner staff holding `PLATFORM_CELL_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/partners/partner-brand-venue-business-scope-assignment-ptr-027` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Which brands and venues the partner relationship covers (separate from product assignment).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `PTR-022` Partner Management Command Center: *Returns to the command centre*; calls `setPartnerBrandVenue`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The partner brand venue list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partner brand venue untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No partner brand venue yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the partner brand venue are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
partner: Desert Gate Tours LLC
brands:
- AquaCove Waterparks
venues:
- AquaCove Abu Dhabi
- AquaCove Dubai
```

#### Permissions

- `setPartnerBrandVenue` → `PLATFORM_CELL_MANAGE` (configure) · partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A partner has multiple agents/sub-agents who can each sell on its behalf; territory/market rights set the regions it may sell into; brand/venue association sets which venues and products it can sell, with distinct pricing per venue. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-549)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'cms')*
- **A56** Confirm and implement branding rules across surfaces: TICVAI branding (with "Powered by TICVAI") on staff-facing POS/tablet devices, and white-labeled, client-branded UI on guest-facing kiosks *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'white-label')*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'white-label')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'cms')*

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-027` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS38 B2B, Reseller & OTA Partner Management Board 1.dc.html#ptr-027`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 1
- Flow F110 *A partner is onboarded onto the B2B portal*, step 7: Assigns the brands, venues and business scope the partner may sell → **The commercial boundary**, and the one that becomes `Session.scope` for every user the partner later creates

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-027?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes, Cancel.
- [ ] Every transition is wired: `PTR-022`.
- [ ] Every gated control is gated: `PLATFORM_CELL_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-028` Partner Documentation & Compliance Repository

**Maintain required partner documentation and ensure that commercial accounts remain compliant.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner staff holding `PLATFORM_TENANT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture; Configure whether expiration should) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/partners/partner-documentation-compliance-repository-ptr-028` |

**Known gaps.** **The pack names 4 actions on this screen and the screen declares 1 operation.** Unserved: Commercial Registration, Bank Details, Signed Agreement, API Agreement. Each needs an operation, or needs …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Required partner documents with expiry and verification, and what an expired document does (warn, block bookings, block credit, suspend, manual review).

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SOT-015).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Document Type | select field | — | — | — | — | — | — |
| Document Number | select field | — | — | — | — | — | — |
| Issue Date | select field | — | — | — | — | — | — |
| Expiry Date | select field | — | — | — | — | — | — |
| Issuing Authority | select field | — | — | — | — | — | — |
| File | select field | — | — | — | — | — | — |
| Verification Status | select field | — | — | — | — | — | — |
| Verified By | select field | — | — | — | — | — | — |
| Verification Date | select field | — | — | — | — | — | — |
| Notes | select field | — | — | — | — | — | — |
| Warn only | select field | — | — | — | — | — | — |
| Block new bookings | select field | — | — | — | — | — | — |
| Block credit transactions | select field | — | — | — | — | — | — |
| Suspend partner | select field | — | — | — | — | — | — |
| Require manual review | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Partner | picker: choose a partner | — | — | `listPartnerDocumentationCompliance` ?partnerId |
| Document type | text field | — | — | `listPartnerDocumentationCompliance` ?documentType |
| Verification status | select | — | Missing · Uploaded · Under review · Verified · Rejected · Expiring · Expired | `listPartnerDocumentationCompliance` ?verificationStatus |
| Expiring within days | number field (days) | — | — | `listPartnerDocumentationCompliance` ?expiringWithinDays |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Commercial Registration (primary button) | navigation or local | — | — | — | — |
| Bank Details (secondary button) | navigation or local | — | — | — | — |
| Signed Agreement (secondary button) | navigation or local | — | — | — | — |
| API Agreement (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listPartnerDocumentationCompliance` (onLoad, Partner Documentation & Compliance Repository)

**Where the user goes next**

- → `PTR-022` Partner Management Command Center: *Returns to the command centre*; calls `listPartnerDocumentationCompliance`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The partner documentation compliance configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partner documentation compliance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No documents on file for this partner yet. Offers no action on this screen: documents arrive with the onboarding application; it names which documents the partner type requires. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
form example:
  Document Type: 233
  Document Number: 128
  Issue Date: 28/09/2026 11:45
  Expiry Date: 01/10/2026 09:14
  Issuing Authority: 233
  File: 46
  Verification Status: 46
  Verified By: 312
  Verification Date: 28/09/2026 11:45
  Notes: 57
  Warn only: 74
  Block new bookings: 7
  Block credit transactions: 233
  Suspend partner: Desert Gate Tours LLC
```

#### Permissions

- `listPartnerDocumentationCompliance` → `PLATFORM_TENANT_VIEW` (read) · partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Partner documents (e.g. trade licence, VAT certificate) follow a review/accept/reject/resubmit flow; approval status runs lead > submitted > active > suspended; a partner 360 view consolidates profile, agreement and payment information in one view. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-550)*
- "Become a partner" link on the tenant website opens a registration form capturing company type, name, address, Emirate/state and documents (trade licence, VAT/TRN certificate); submitting creates a pending account and emails the tenant's operations team. *(client request · MoM 7 Aug 2026, 13. Tenant/B2B Onboarding & Self-Registration Flow · DI-165)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-028` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS38 B2B, Reseller & OTA Partner Management Board 1.dc.html#ptr-028`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 1
- Flow F110 *A partner is onboarded onto the B2B portal*, step 9: Checks the compliance and documentation file → Licences, insurance and signed agreement present or missing
- Flow F110 branch at step 9 (recoverable): when Compliance documents are missing or expired, **Onboarding pauses rather than fails.** Scope and profile stay configured and the partner sits unapproved, which is why step 13 is separated from step 11 — a partly-onboarded partner must be a …

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-028?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Commercial Registration, Bank Details, Signed Agreement, API Agreement.
- [ ] Every transition is wired: `PTR-022`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-030` Partner Approval, Status & Lifecycle Management

**Govern the complete business lifecycle of a partner after onboarding.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner staff holding `PLATFORM_CELL_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `challengeId` (navigation) |
| Route | `/partners/partner-approval-status-lifecycle-management-ptr-030` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** A partner's lifecycle status after onboarding (active, restricted, suspended, terminated) and the reason category; changes need a second factor.

**Fixed on main** (the package already carries these; draw what it says): Reaches approvePartnerStatuLifecycle (step-up mfa) and declares no way to raise the challenge. (CHG-SOT-015); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SOT-015).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Commercial | select field | — | — | — | — | — | — |
| Compliance | select field | — | — | — | — | — | — |
| Credit | select field | — | — | — | — | — | — |
| Fraud | select field | — | — | — | — | — | — |
| Contract Expiry | select field | — | — | — | — | — | — |
| Performance | select field | — | — | — | — | — | — |
| Technical | select field | — | — | — | — | — | — |
| Management Decision | select field | — | — | — | — | — | — |
| Authentication code | text field | — | — | — | — | Asked in place inside the Approve confirmation, because `approvePartnerStatuLifecycle` needs a fresh step-up token (`x-ticvai-step-up: mfa`); its result is the `stepUpToken`. Five wrong codes lock … | — |

**Sent by *Email me a code instead*** (`createMfaChallenge`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Action `action` | text field | required | — | — | — | What the step-up is for. Recorded in the audit trail. | `createMfaChallenge` body |
| Method `methodId` | picker: choose a method | optional | — | — | shows names, sends the id | — | `createMfaChallenge` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | For a guest, the venue whose `VenueSettings.identity.guestTwoStep` applies (sign-in venue, or the venue of the booking being acted on). | `createMfaChallenge` body |

#### Outputs: what the screen shows and produces

**Shown**

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Activate, Restrict, Suspend, Reactivate, Terminate, Archive. Each needs attaching to the control it gates, or the screen needs the control.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Approve (primary button) | navigation or local | — | — | — | — |
| Email me a code instead (secondary button) | `createMfaChallenge` POST `/auth/mfa/challenge` | inline | inline | — | — |

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **approvePartnerStatuLifecycle**: Confirmation names the consequence first, then asks for the authentication code (authenticator app, or an emailed code as fallback); only a verified challenge sends approvePartnerStatuLifecycle with its single-use stepUpToken. Wrong code: the action is not sent and nothing changes; five wrong codes lock step-up for the policy's lockout minutes and the screen says when it lifts. Why the control exists: Makes a partner able to trade, or stops them. *(source: contracts/satellite/subscription.yaml#approvePartnerStatuLifecycle; R126; contracts/spine/identity.yaml#createMfaChallenge)*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The partner approval status configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partner approval status untouched. |
| Empty, first run (`?state=emptyFirstRun`) | Nothing waiting for approval: every partner is in a settled state. Offers no create action. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
form example:
  Commercial: 312
  Compliance: 78%
  Credit: 128
  Fraud: 128
  Contract Expiry: 74
  Performance: 128
  Technical: 11
  Management Decision: 1.8 s
```

#### Permissions

- `approvePartnerStatuLifecycle` → `PLATFORM_CELL_MANAGE` (configure) · partner · step-up mfa
- `createMfaChallenge` → no permission · staff, partner, guest
- `verifyMfaChallenge` → no permission · staff, partner, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Partner documents (e.g. trade licence, VAT certificate) follow a review/accept/reject/resubmit flow; approval status runs lead > submitted > active > suspended; a partner 360 view consolidates profile, agreement and payment information in one view. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-550)*
- Partner review: operations validate documents and can reject (e.g. expired trade licence) with a message prompting resubmission; approval emails credentials with a temporary password, and the partner must set their own password at first login. *(client request · MoM 7 Aug 2026, 13. Tenant/B2B Onboarding & Self-Registration Flow · DI-166)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-030` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS38 B2B, Reseller & OTA Partner Management Board 1.dc.html#ptr-030`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 1
- Flow F110 *A partner is onboarded onto the B2B portal*, step 13: Approves the partner and moves it to active → **The partner can trade.** Approval is last on purpose: scope, compliance and permissions are all in place before the account can raise an order
- Flow F110 branch at step 13 (requiresStaff): when The partner is approved before scope or compliance is set, Nothing in the screens enforces the order of steps 5 to 11 — they are all spokes off one hub and reachable in any sequence. **An approved partner with unbounded scope can sell inventory it was never …

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-030?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Approve, Email me a code instead.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `PLATFORM_CELL_MANAGE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-031` Partner 360° Profile, Readiness & AI Review

**Provide one consolidated Partner 360 screen before activation and throughout the relationship. This should become one of the most useful screens for TICVAI commercial management. Board 1 established who the partner is and what they are authorized to access. Board 2 establishes the commercial rules under which that partner can transact with TICVAI.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner staff holding `PLATFORM_TENANT_VIEW` (1 read) |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/partners/partner-360-profile-readiness-ai-review-ptr-031` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** One partner's profile, readiness and AI review before activation and throughout.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SOT-015).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Partner | picker: choose a partner | — | — | `listPartnerProfileReadiness` ?partnerId |
| Status | select | — | Lead · Applicant · Under review · Approved · Configuration · Active · Restricted · Suspended · Terminated · Archived | `listPartnerProfileReadiness` ?status |
| Search | text field | — | — | `listPartnerProfileReadiness` ?search |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listPartnerProfileReadiness` (onLoad, Partner 360° Profile, Readiness & AI Review)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The partner 360° profile list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partner 360° profile untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No partner profile to review yet: readiness appears once a partner has an application. Offers no create action. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the partner 360° profile are still there. The pack's own statuses are 8.1.9 Partner lifecycle governance — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
partner: Arabian Trails
readiness: documents 4 of 5, agreement signed, credit not set
aiNote: Trade licence expires in 20 days
```

#### Permissions

- `listPartnerProfileReadiness` → `PLATFORM_TENANT_VIEW` (read) · partner

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

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-031` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS38 B2B, Reseller & OTA Partner Management Board 1.dc.html#ptr-031`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 1

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-031?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
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

**14 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"actOnPartnerApplicationReview": {"method":"POST","path":"/partner-applications/{applicationId}/review-actions","contract":"subscription","summary":"Move a partner application through its departmental review","permission":"PARTNER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PartnerApplicationReviewAction","responds":"PartnerApplication"},
"approvePartnerStatuLifecycle": {"method":"PUT","path":"/partner-statu-lifecycle","contract":"subscription","summary":"Partner Approval, Status & Lifecycle Management","permission":"PLATFORM_CELL_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PartnerApprovalStatusLifecycleManagementInput","responds":"PartnerApprovalStatusLifecycleManagementView"},
"createMfaChallenge": {"method":"POST","path":"/auth/mfa/challenge","contract":"identity","summary":"Second factor at staff sign-in, and step-up for a sensitive action","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"createPartnerUser": {"method":"POST","path":"/partners/{partnerId}/users","contract":"subscription","summary":"Add a user to a partner branch","permission":"PARTNER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PartnerUser","responds":"PartnerUser"},
"listPartner": {"method":"GET","path":"/partner","contract":"subscription","summary":"Partner Management Command Center","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"brand","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"accountManager","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"risk","in":"query","required":false},{"name":"integrationType","in":"query","required":false},{"name":"partnerType","in":"query","required":false},{"name":"country","in":"query","required":false},{"name":"territory","in":"query","required":false},{"name":"agreementStatus","in":"query","required":false},{"name":"creditStatus","in":"query","required":false},{"name":"search","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPartner2": {"method":"GET","path":"/partner-2","contract":"subscription","summary":"Partner Operations Command Center","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"venue","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"market","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false},{"name":"partnerId","in":"query","required":false},{"name":"partnerType","in":"query","required":false},{"name":"accountManager","in":"query","required":false},{"name":"operationalStatus","in":"query","required":false},{"name":"risk","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPartnerContactUser": {"method":"GET","path":"/partner-contact-user","contract":"subscription","summary":"Partner Contacts & User Administration","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"partnerId","in":"query","required":false},{"name":"contactType","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"hasUserAccount","in":"query","required":false},{"name":"search","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPartnerDocumentationCompliance": {"method":"GET","path":"/partner-documentation-compliance","contract":"subscription","summary":"Partner Documentation & Compliance Repository","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"partnerId","in":"query","required":false},{"name":"documentType","in":"query","required":false},{"name":"verificationStatus","in":"query","required":false},{"name":"expiringWithinDays","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPartnerOnboardingApplication": {"method":"GET","path":"/partner-onboarding-application","contract":"subscription","summary":"Partner Onboarding & Application Workflow","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"stage","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"requestedPartnerType","in":"query","required":false},{"name":"search","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPartnerProfileReadiness": {"method":"GET","path":"/partner-profile-readiness","contract":"subscription","summary":"Partner 360° Profile, Readiness & AI Review","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"partnerId","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"search","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"setPartnerBrandVenue": {"method":"PUT","path":"/partner-brand-venue","contract":"subscription","summary":"Partner Brand, Venue & Business Scope Assignment","permission":"PLATFORM_CELL_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PartnerBrandVenueBusinessScopeAssignmentInput","responds":"PartnerBrandVenueBusinessScopeAssignmentView"},
"setPartnerContact": {"method":"PUT","path":"/partner-contacts","contract":"subscription","summary":"Create, edit, disable, enable or revoke a partner contact","permission":"PARTNER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PartnerContactInput","responds":"PartnerContact"},
"setPartnerProfileOrganization": {"method":"PUT","path":"/partner-profile-organization","contract":"subscription","summary":"Partner Profile & Organization Setup","permission":"PLATFORM_CELL_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PartnerProfileOrganizationSetupInput","responds":"PartnerProfileOrganizationSetupView"},
"verifyMfaChallenge": {"method":"POST","path":"/auth/mfa/challenge/{challengeId}/verify","contract":"identity","summary":"Complete a sign-in or step-up challenge","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Partner360ProfileReadinessAiReviewView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over control.partner and its control.partner_* rows and the existing subscription state, assembled at read time (data model DM4)","description":"**What Partner 360° Profile, Readiness & AI Review displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"companyInformationAndHierarchy":{"type":"string","description":"Organization: legal entity and parent chain, e.g. \"Gulf Travel LLC > Gulf Travel Group\""},"keyPartnerContacts":{"type":"array","items":{"type":"string"},"description":"Contacts: key partner contacts (name and contact type)"},"activeB2bUsers":{"type":"integer","description":"Users: active B2B users"},"authorizedMarkets":{"type":"array","items":{"type":"string"},"description":"Territories: authorized markets"},"brandsAndVenues":{"type":"array","items":{"type":"string"},"description":"Business Scope: brands and venues"},"complianceStatus":{"type":"string","description":"Documentation: compliant, expiring, incomplete or nonCompliant"},"authorizedCapabilities":{"type":"array","items":{"type":"string"},"description":"Permissions: authorized capabilities"},"commercialSummary":{"type":"string","description":"Commercial: agreement and credit summary"},"connectedChannels":{"type":"array","items":{"type":"string","enum":["b2bPortal","api","otaConnection","agentPortal","affiliateLink","voucherDistribution","bulkTicketExport","other"]},"description":"Distribution: connected channels"},"performanceSummary":{"type":"string","description":"Performance: scorecard summary"},"partnerId":{"type":"string","format":"uuid","description":"Partner"},"partnerName":{"type":"string","description":"Partner Name"},"partnerType":{"type":"string","description":"Partner Type code"},"accountManager":{"type":"string","description":"Account Manager"},"country":{"type":"string","description":"Country, ISO 3166-1 alpha-2"},"status":{"type":"string","description":"Status: lead, applicant, underReview, approved, configuration, active, restricted, suspended, terminated or archived (pack p.6 and p.18 merged with MoM 31 Aug 4.3 lead -> submitted -> active -> suspended; \"submitted\" is applicant)"},"riskRating":{"type":"string","enum":["low","medium","high","critical"],"description":"Risk"},"salesYtd":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Sales YTD"},"outstandingBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Outstanding Balance"},"readinessScore":{"type":"integer","description":"Readiness Score, 0-100"},"readinessBreakdown":{"type":"object","description":"Readiness by section, each 0-100","properties":{"organization":{"type":"integer"},"contacts":{"type":"integer"},"documentation":{"type":"integer"},"territory":{"type":"integer"},"permissions":{"type":"integer"},"commercialAgreement":{"type":"integer"},"credit":{"type":"integer"},"integration":{"type":"integer"}}},"blockers":{"type":"array","items":{"type":"string"},"description":"Critical blockers to activation"},"aiRecommendation":{"type":"string","enum":["recommendedForActivation","activationNotRecommended"],"description":"Advisory AI Partner Review verdict","nullable":true},"aiInsights":{"type":"array","items":{"type":"string"},"description":"Advisory AI Partner Review narrative"}}},
"PartnerAgreementStatus": {"type":"string","enum":["pendingApproval","active","expiringSoon","expired","suspended","terminated"]},
"PartnerApplication": {"type":"object","x-ticvai-persistence":"control.partner_application + control.partner_application_review_task","description":"A partner onboarding application and where it stands in the review. `registerPartner` creates one with the partner record it opens (lifecycle `applicant`); the stage moves through the departmental reviews and the decision itself goes through `approvals` (decided 29 September, data model DM4)\n\n**Written by** registerPartner (creates the application `submitted` with the partner `applicant`) and actOnPartnerApplicationReview (starts the review, completes a departmental task, asks for and receives more information, withdraws); the approval itself is decided in approvals (decided 29 September, writers pass; DM4).","required":["id","companyName","stage","status","submittedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"partnerId":{"type":"string","format":"uuid","nullable":true,"description":"Partner record created on submission (lifecycle applicant)."},"companyName":{"type":"string","description":"Company legal name as applied."},"tradingName":{"type":"string","nullable":true,"description":"Trading name as applied."},"country":{"type":"string","nullable":true,"description":"Country, ISO 3166-1 alpha-2."},"requestedPartnerType":{"type":"string","nullable":true,"description":"Requested partner type code (see `Partner.partnerType`)."},"markets":{"type":"array","items":{"type":"string"},"description":"Markets the applicant wants to sell into."},"expectedSalesVolume":{"type":"integer","nullable":true,"description":"Expected sales volume, tickets per year."},"requestedProducts":{"type":"array","items":{"type":"string"},"description":"Requested products."},"requestedVenues":{"type":"array","items":{"type":"string"},"description":"Requested venues."},"preferredDistributionMethod":{"type":"string","enum":["b2bPortal","api","otaConnection","agentPortal","affiliateLink","voucherDistribution","bulkTicketExport","other"],"nullable":true,"description":"Preferred distribution method."},"estimatedAnnualBusiness":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Estimated annual business value."},"contactName":{"type":"string","nullable":true,"description":"Applicant contact name."},"contactEmail":{"type":"string","format":"email","description":"Applicant contact email."},"billingRequirements":{"type":"string","nullable":true,"description":"Billing requirements as stated by the applicant."},"businessCase":{"type":"string","nullable":true,"description":"Commercial review: business case."},"territory":{"type":"string","nullable":true,"description":"Commercial review: territory."},"creditRequest":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Finance review: requested credit limit."},"paymentTerms":{"type":"string","nullable":true,"description":"Finance review: requested payment terms."},"taxRegistrationNumber":{"type":"string","nullable":true,"description":"Finance review: tax/VAT registration number."},"productRequirements":{"type":"string","nullable":true,"description":"Operations review: product requirements."},"fulfillmentRequirements":{"type":"string","nullable":true,"description":"Operations review: fulfilment requirements."},"apiIntegrationRequirements":{"type":"string","nullable":true,"description":"Technical review: API/integration requirements."},"stage":{"type":"string","enum":["application","businessVerification","documentation","commercialReview","financeReview","technicalReview","approval","configuration","activation"],"default":"application","description":"Current onboarding stage (pack p.9 Onboarding Workflow)."},"status":{"type":"string","enum":["submitted","inReview","moreInformationRequested","approved","rejected","withdrawn"],"default":"submitted","description":"Application status."},"reviewTasks":{"type":"array","items":{"type":"object","required":["department","completed"],"properties":{"department":{"type":"string","enum":["commercial","finance","operations","technical"]},"assigneePrincipalId":{"type":"string","format":"uuid","nullable":true},"dueAt":{"type":"string","format":"date-time","nullable":true},"completed":{"type":"boolean"}}},"description":"Internal Review: the task each department receives; the rows of control.partner_application_review_task."},"submittedAt":{"type":"string","format":"date-time","description":"Submitted at."},"slaDueAt":{"type":"string","format":"date-time","nullable":true,"description":"When the current stage breaches its SLA."},"approvalRequestId":{"type":"string","nullable":true,"readOnly":true,"description":"The approvals request carrying the decision, as on `PartnerAgreement`."},"scopePath":{"type":"string","description":"The partition key (ADR-0005), written at `tenant` scope."},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"PartnerApplicationReviewAction": {"type":"object","x-ticvai-persistence":"none — request only; applied to control.partner_application and control.partner_application_review_task, and to control.partner on startReview and withdraw (decided 29 September, writers pass; DM4)","description":"One review action on a partner application (actOnPartnerApplicationReview) (decided 29 September, writers pass; DM4)","required":["action"],"properties":{"action":{"type":"string","enum":["startReview","completeTask","requestInformation","supplyInformation","withdraw"],"description":"The action (states/partner-application.yaml)"},"department":{"type":"string","enum":["commercial","finance","operations","technical"],"nullable":true,"description":"For completeTask, the department whose review task is done"},"assigneePrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"For startReview, who each opened task is assigned to when one person reviews all; empty leaves them to each department's queue"},"note":{"type":"string","nullable":true,"description":"The reviewer's finding (completeTask), what is missing (requestInformation, required) or the applicant's answer (supplyInformation)"},"documentIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"For supplyInformation, documents uploaded in answer (control.partner_document)"}}},
"PartnerApprovalStatusLifecycleManagementInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; stored as control.partner_status_history (PartnerStatusHistory), with the resulting status on control.partner (data model DM4)","description":"**What Partner Approval, Status & Lifecycle Management submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"partnerId":{"type":"string","format":"uuid","description":"Partner"},"action":{"type":"string","enum":["approve","activate","restrict","suspend","reactivate","terminate","archive"],"description":"Status Actions"},"reasonCategory":{"type":"string","enum":["commercial","compliance","credit","fraud","contractExpiry","performance","technical","managementDecision"],"description":"Status Reasons"},"reasonNote":{"type":"string","description":"Free-text reason","nullable":true},"suspensionScope":{"type":"string","enum":["full","selected"],"description":"Suspension Scope: full suspension or selected restrictions","nullable":true},"restrictions":{"type":"array","items":{"type":"string","enum":["stopNewBookings","stopCreditSales","stopApi","stopSpecificVenue","stopSpecificMarket"]},"description":"Selected restrictions when suspensionScope is selected, or for restrict"},"restrictedVenueIds":{"type":"array","items":{"type":"string"},"description":"Venues for stopSpecificVenue"},"restrictedMarkets":{"type":"array","items":{"type":"string"},"description":"Markets for stopSpecificMarket"},"effectiveFrom":{"type":"string","format":"date-time","description":"When the change takes effect; lifecycle changes are effective-dated"},"dryRun":{"type":"boolean","description":"When true, return the impact analysis without changing anything, so the screen can show it before the administrator confirms (decided 29 September, readiness close-out)"}}},
"PartnerApprovalStatusLifecycleManagementView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over control.partner and control.partner_status_history and the existing subscription state, assembled at read time (data model DM4)","description":"**What Partner Approval, Status & Lifecycle Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"futureBookings":{"type":"integer","description":"Impact: future bookings"},"activeHolds":{"type":"integer","description":"Impact: active holds"},"outstandingBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Impact: outstanding balance"},"pendingSettlement":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Impact: pending settlement"},"activeUsers":{"type":"integer","description":"Impact: active users"},"activeIntegrations":{"type":"integer","description":"Impact: active integrations"},"existingCustomers":{"type":"integer","description":"Impact: existing customers holding tickets"},"existingTickets":{"type":"integer","description":"Impact: existing tickets; never invalidated by a suspension"},"currentAllocations":{"type":"integer","description":"Impact: current contractual allocations"},"partnerId":{"type":"string","format":"uuid","description":"Partner"},"action":{"type":"string","enum":["approve","activate","restrict","suspend","reactivate","terminate","archive"],"description":"Status Actions"},"reasonCategory":{"type":"string","enum":["commercial","compliance","credit","fraud","contractExpiry","performance","technical","managementDecision"],"description":"Status Reasons"},"reasonNote":{"type":"string","description":"Free-text reason","nullable":true},"suspensionScope":{"type":"string","enum":["full","selected"],"description":"Suspension Scope: full suspension or selected restrictions","nullable":true},"restrictions":{"type":"array","items":{"type":"string","enum":["stopNewBookings","stopCreditSales","stopApi","stopSpecificVenue","stopSpecificMarket"]},"description":"Selected restrictions when suspensionScope is selected, or for restrict"},"restrictedVenueIds":{"type":"array","items":{"type":"string"},"description":"Venues for stopSpecificVenue"},"restrictedMarkets":{"type":"array","items":{"type":"string"},"description":"Markets for stopSpecificMarket"},"effectiveFrom":{"type":"string","format":"date-time","description":"When the change takes effect; lifecycle changes are effective-dated"},"status":{"type":"string","description":"Resulting account status: lead, applicant, underReview, approved, configuration, active, restricted, suspended, terminated or archived (pack p.6 and p.18 merged with MoM 31 Aug 4.3 lead -> submitted -> active -> suspended; \"submitted\" is applicant)"},"applied":{"type":"boolean","description":"False when dryRun was set or the change awaits approval"},"approvalRequestId":{"type":"string","description":"Approval request raised for the change","nullable":true},"aiImpactSummary":{"type":"string","description":"Advisory AI summary of the business impact","nullable":true}}},
"PartnerBrandVenueBusinessScopeAssignmentInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; stored as control.partner_scope_assignment (PartnerScopeAssignment); brand, venue and attraction land in brandId, venueId and attractionId, assignmentId is its id (data model DM4)","description":"**What Partner Brand, Venue & Business Scope Assignment submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"tenant":{"type":"string","description":"Tenant id"},"brand":{"type":"string","description":"Brand id; blank = every brand of the tenant","nullable":true},"venue":{"type":"string","description":"Venue id; blank = every venue of the brand","nullable":true},"attraction":{"type":"string","description":"Attraction id; blank = every attraction of the venue","nullable":true},"businessUnit":{"type":"string","description":"Business Unit","nullable":true},"eventPortfolio":{"type":"string","description":"Event Portfolio","nullable":true},"market":{"type":"string","description":"Market","nullable":true},"startDate":{"type":"string","format":"date","description":"Start Date"},"endDate":{"type":"string","format":"date","description":"End Date; a set end date makes the assignment temporary","nullable":true},"seasonalScope":{"type":"boolean","description":"Seasonal Scope: when true the start and end month-day recur every year (decided 29 September, readiness close-out)"},"assignmentId":{"type":"string","format":"uuid","description":"Assignment id; omit to create"},"partnerId":{"type":"string","format":"uuid","description":"Partner"},"authorized":{"type":"boolean","description":"Authorized (true) or explicitly not authorized (false), the pack's Not Authorized example"},"scopeExclusions":{"type":"array","items":{"type":"string"},"description":"Scope Overrides: product or product-category ids excluded inside this scope (e.g. all Dubai Arena events except VIP Hospitality); consumed by the commercial/channel rules"}}},
"PartnerBrandVenueBusinessScopeAssignmentView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over control.partner_scope_assignment (PartnerScopeAssignment) and the existing subscription state, assembled at read time (data model DM4)","description":"**What Partner Brand, Venue & Business Scope Assignment displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"tenant":{"type":"string","description":"Tenant id"},"brand":{"type":"string","description":"Brand id; blank = every brand of the tenant","nullable":true},"venue":{"type":"string","description":"Venue id; blank = every venue of the brand","nullable":true},"attraction":{"type":"string","description":"Attraction id; blank = every attraction of the venue","nullable":true},"businessUnit":{"type":"string","description":"Business Unit","nullable":true},"eventPortfolio":{"type":"string","description":"Event Portfolio","nullable":true},"market":{"type":"string","description":"Market","nullable":true},"startDate":{"type":"string","format":"date","description":"Start Date"},"endDate":{"type":"string","format":"date","description":"End Date; a set end date makes the assignment temporary","nullable":true},"seasonalScope":{"type":"boolean","description":"Seasonal Scope: when true the start and end month-day recur every year (decided 29 September, readiness close-out)"},"assignmentId":{"type":"string","format":"uuid","description":"Assignment id; omit to create"},"partnerId":{"type":"string","format":"uuid","description":"Partner"},"authorized":{"type":"boolean","description":"Authorized (true) or explicitly not authorized (false), the pack's Not Authorized example"},"scopeExclusions":{"type":"array","items":{"type":"string"},"description":"Scope Overrides: product or product-category ids excluded inside this scope (e.g. all Dubai Arena events except VIP Hospitality); consumed by the commercial/channel rules"}}},
"PartnerContact": {"type":"object","x-ticvai-persistence":"control.partner_contact","description":"A person at the partner, with or without a B2B user account. A contact with an account links to its principal (`control.partner_user` carries the branch, quota and credit); one without an account is still somebody finance or operations must be able to reach (decided 29 September, data model DM4)\n\n**Written by** setPartnerContact (create, edit, disable, enable, revoke) and by createPartnerUser, which creates the contact `invited` for a user with an account (decided 29 September, writers pass; DM4).","required":["id","partnerId","name","contactType","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"partnerId":{"type":"string","format":"uuid","description":"The partner (control.partner)."},"name":{"type":"string","description":"Name."},"position":{"type":"string","nullable":true,"description":"Position."},"department":{"type":"string","nullable":true,"description":"Department."},"email":{"type":"string","format":"email","nullable":true,"description":"Email."},"mobile":{"type":"string","nullable":true,"description":"Mobile."},"telephone":{"type":"string","nullable":true,"description":"Telephone."},"language":{"type":"string","nullable":true,"description":"Language, BCP 47 tag."},"timeZone":{"type":"string","nullable":true,"description":"Time zone, IANA name."},"contactType":{"type":"string","enum":["primary","commercial","reservations","finance","technical","operations","management","emergency"],"description":"Contact type."},"principalId":{"type":"string","format":"uuid","nullable":true,"description":"Identity principal of the B2B user account (identity.principal); empty for a contact with no account."},"status":{"type":"string","enum":["invited","active","disabled","revoked","expired"],"default":"active","description":"Status; a contact with no user account is active or disabled."},"scopePath":{"type":"string","description":"The partition key (ADR-0005), written at `tenant` scope."},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"PartnerContactInput": {"type":"object","x-ticvai-persistence":"none — request only; stored as control.partner_contact (PartnerContact) (decided 29 September, writers pass; DM4)","description":"What setPartnerContact submits. Without `contactId` it creates a contact with no user account; a contact who signs in is created through createPartnerUser (decided 29 September, writers pass; DM4)","required":["partnerId"],"properties":{"contactId":{"type":"string","format":"uuid","nullable":true,"description":"The contact to change; omit to create"},"partnerId":{"type":"string","format":"uuid","description":"The partner (control.partner)"},"action":{"type":"string","enum":["save","disable","enable","revoke"],"default":"save","description":"save creates or edits; disable, enable and revoke change access (states/partner-contact.yaml)"},"name":{"type":"string","description":"Name; required to create"},"position":{"type":"string","nullable":true},"department":{"type":"string","nullable":true},"email":{"type":"string","format":"email","nullable":true},"mobile":{"type":"string","nullable":true},"telephone":{"type":"string","nullable":true},"language":{"type":"string","nullable":true,"description":"BCP 47 tag"},"timeZone":{"type":"string","nullable":true,"description":"IANA name"},"contactType":{"type":"string","enum":["primary","commercial","reservations","finance","technical","operations","management","emergency"],"description":"Contact type; required to create"}}},
"PartnerContactsUserAdministrationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over control.partner_contact (PartnerContact) with control.partner_user and the existing subscription state, assembled at read time (data model DM4)","description":"**What Partner Contacts & User Administration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"name":{"type":"string","description":"Name"},"position":{"type":"string","description":"Position"},"department":{"type":"string","description":"Department"},"email":{"type":"string","description":"Email","format":"email"},"mobile":{"type":"string","description":"Mobile"},"telephone":{"type":"string","description":"Telephone"},"language":{"type":"string","description":"Language, BCP 47 tag"},"timeZone":{"type":"string","description":"Time Zone, IANA name"},"contactType":{"type":"string","enum":["primary","commercial","reservations","finance","technical","operations","management","emergency"],"description":"Contact Type"},"status":{"type":"string","description":"Status: invited, active, disabled, revoked or expired (a contact with no user account is active or disabled)"},"username":{"type":"string","description":"Username of the B2B user account; empty for a contact with no account","nullable":true},"partnerId":{"type":"string","format":"uuid","description":"Partner"},"branchScopePath":{"type":"string","description":"Branch the user sits on, as the PartnerUser scope path","nullable":true},"role":{"type":"string","description":"Partner role, e.g. Partner Administrator, Booking Agent, Supervisor, Finance User, Reporting User, API Administrator; PartnerUser.role (control.partner_user), the grants themselves are RBAC data (decided 29 September, writers pass; DM4)","nullable":true},"permissions":{"type":"array","items":{"type":"string"},"description":"Effective permissions of the user, within the partner ceiling"},"salesLocation":{"type":"string","description":"Sales Location; PartnerUser.salesLocation (control.partner_user), empty for a contact with no account (decided 29 September, writers pass; DM4)","nullable":true},"currency":{"type":"string","pattern":"^[A-Z]{3}$","description":"Currency the user sells in; PartnerUser.currency (control.partner_user) (decided 29 September, writers pass; DM4)"},"mfaEnrolled":{"type":"boolean","description":"MFA enrolled"},"accountExpiresAt":{"type":"string","format":"date-time","description":"Account expiry; PartnerUser.accountExpiresAt (control.partner_user) (decided 29 September, writers pass; DM4)","nullable":true},"contactId":{"type":"string","format":"uuid","description":"Contact id"},"principalId":{"type":"string","format":"uuid","description":"Identity principal of the B2B user account; empty for a contact with no account","nullable":true}}},
"PartnerDocumentationComplianceRepositoryView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over control.partner_document (PartnerDocument) and the existing subscription state, assembled at read time (data model DM4)","description":"**What Partner Documentation & Compliance Repository displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"documentType":{"type":"string","description":"Document Type code from the configurable list, seeded with tradeLicence, taxVatCertificate, commercialRegistration, bankDetails, insurance, signedAgreement, nda, apiAgreement, complianceDocument, authorizedSignatoryId, other"},"documentNumber":{"type":"string","description":"Document Number"},"expiryDate":{"type":"string","format":"date","description":"Expiry Date","nullable":true},"issuingAuthority":{"type":"string","description":"Issuing Authority"},"fileRef":{"type":"string","description":"Stored file reference","nullable":true},"verificationStatus":{"type":"string","description":"Verification Status: missing, uploaded, underReview, verified, rejected, expiring or expired"},"verifiedBy":{"type":"string","description":"Verified By: staff display name","nullable":true},"verificationDate":{"type":"string","format":"date-time","description":"Verification Date","nullable":true},"notes":{"type":"string","description":"Notes"},"documentId":{"type":"string","format":"uuid","description":"Document id"},"partnerId":{"type":"string","format":"uuid","description":"Partner"},"issueDate":{"type":"string","format":"date","description":"Issue Date","nullable":true},"mandatory":{"type":"boolean","description":"Whether this document type is mandatory for the partner type"},"daysToExpiry":{"type":"integer","description":"Days until expiry; negative once expired","nullable":true},"expiryAction":{"type":"string","enum":["warnOnly","blockNewBookings","blockCreditTransactions","suspendPartner","requireManualReview"],"description":"Compliance Rules: what expiry or absence of this document does"},"aiInsights":{"type":"array","items":{"type":"string"},"description":"Advisory AI findings from the uploaded file (extracted fields, missing or inconsistent information)"}}},
"PartnerManagementCommandCenterSummary": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection; the headline tiles over the list, computed at read time for the filters in force","description":"**The headline figures on Partner Management Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.","properties":{"totalPartners":{"type":"integer","description":"Total Partners"},"activePartners":{"type":"integer","description":"Active Partners"},"pendingOnboarding":{"type":"integer","description":"Pending Onboarding"},"pendingApproval":{"type":"integer","description":"Pending Approval"},"suspendedPartners":{"type":"integer","description":"Suspended Partners"},"expiringAgreements":{"type":"integer","description":"Expiring Agreements: partners whose active agreement ends within its expiryAlertDays (default 30) (decided 29 September, readiness close-out)"},"documentationIssues":{"type":"integer","description":"Documentation Issues: partners with a mandatory document missing, rejected, expiring or expired"},"partnersWithCreditHolds":{"type":"integer","description":"Partners With Credit Holds: partners whose credit status is onHold or blocked"},"connectedOtaApiPartners":{"type":"integer","description":"Connected OTA/API Partners"},"partnerSalesYtd":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Partner Sales YTD: gross value of partner orders this calendar year (decided 29 September, readiness close-out)"},"partnerRevenueYtd":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Partner Revenue YTD: partner sales net of commission this calendar year (decided 29 September, readiness close-out)"},"highRiskPartners":{"type":"integer","description":"High-Risk Partners"}}},
"PartnerManagementCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over control.partner (Partner), control.partner_credit_profile, control.partner_application, control.partner_scope_assignment and control.partner_distribution_right and the existing subscription state, assembled at read time (data model DM4)","description":"**What Partner Management Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"partnerId":{"type":"string","format":"uuid","description":"Partner ID"},"tradingName":{"type":"string","description":"Trading Name"},"legalEntity":{"type":"string","description":"Legal Entity"},"partnerType":{"type":"string","description":"Partner type code from the tenant's configurable partner-type list (MoM 31 Aug 4.3: configurable category/type), seeded with the pack's p.7 list: b2bReseller, travelAgent, tourOperator, ota, corporateCustomer, hotelConcierge, destinationManagementCompany, affiliate, wholesaler, distributor, governmentPartner, schoolInstitution, apiPartner, internalGroupCompany"},"country":{"type":"string","description":"Country, ISO 3166-1 alpha-2"},"territory":{"type":"string","description":"Territory: summary of the authorised markets (listTerritoryMarketDistribution)"},"assignedBrands":{"type":"array","items":{"type":"string"},"description":"Assigned Brand/Venue: brand names in the partner's business scope (setPartnerBrandVenue)"},"assignedVenues":{"type":"array","items":{"type":"string"},"description":"Assigned Brand/Venue: venue names in the partner's business scope (setPartnerBrandVenue)"},"commercialOwner":{"type":"string","description":"Commercial Owner: staff display name of the account manager"},"distributionChannel":{"type":"array","items":{"type":"string","enum":["b2bPortal","api","otaConnection","agentPortal","affiliateLink","voucherDistribution","bulkTicketExport","other"]},"description":"Distribution Channel: Distribution methods: b2bPortal (the TICVAI B2B portal), api (partner consumes the TICVAI API), otaConnection (TICVAI integrates into the OTA, either direction per MoM 31 Aug 4.3), agentPortal, affiliateLink, voucherDistribution, bulkTicketExport (pre-generated QR tickets as CSV, MoM 5 Aug option 3), other"},"accountStatus":{"type":"string","description":"Account Status: lead, applicant, underReview, approved, configuration, active, restricted, suspended, terminated or archived (pack p.6 and p.18 merged with MoM 31 Aug 4.3 lead -> submitted -> active -> suspended; \"submitted\" is applicant)"},"onboardingStatus":{"type":"string","description":"Onboarding Status: the application stage (application, businessVerification, documentation, commercialReview, financeReview, technicalReview, approval, configuration, activation) or complete"},"agreementStatus":{"allOf":[{"$ref":"#/components/schemas/PartnerAgreementStatus"}],"nullable":true,"description":"Agreement Status of the partner's current agreement; empty when none"},"creditStatus":{"type":"string","description":"Credit Status: notEnabled, withinLimit, warning (at the warning threshold), highRisk, onHold or blocked (decided 29 September, readiness close-out)"},"integrationStatus":{"type":"string","enum":["none","testing","connected","degraded","disconnected"],"x-ticvai-persisted":false,"description":"Integration Status: none, testing, connected, degraded or disconnected (decided 29 September, readiness close-out). **Derived at read time, not a column** (decided 29 September, writers pass; DM4), from the partner's OTA/API channel listings (control.channel_listing) and the health of its API clients (control.api_client, with webhook deliveries in control.webhook_delivery), first match wins: `none` when the partner has no channel listing and no API client; `disconnected` when every listing is `paused` or `delisted` or every production API client is `suspended` or `revoked`; `degraded` when a `live` listing's `lastPushedAt` is older than twice its `pushIntervalMinutes`, or webhook deliveries to the partner failed in the last hour; `connected` when a `live` listing or an `active` production client exists and none of the above holds; otherwise `testing` (only `draft` listings or only sandbox clients). The thresholds are proposed, the venue may correct them."},"lastActivity":{"type":"string","format":"date-time","description":"Last Activity"},"riskRating":{"type":"string","enum":["low","medium","high","critical"],"description":"Risk rating, Low / Medium / High / Critical (pack p.58); drives the Risk filter and the High-Risk Partners KPI"},"aiInsights":{"type":"array","items":{"type":"string"},"description":"Partner Attention Required: advisory AI flags such as an agreement expiring against forward bookings (pack p.6)"}}},
"PartnerOnboardingApplicationWorkflowView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over control.partner_application + control.partner_application_review_task (PartnerApplication) and the existing subscription state, assembled at read time (data model DM4)","description":"**What Partner Onboarding & Application Workflow displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"companyName":{"type":"string","description":"Company legal name as applied"},"requestedPartnerType":{"type":"string","description":"Requested partner type code (see partnerType)"},"markets":{"type":"array","items":{"type":"string"},"description":"Markets the applicant wants to sell into"},"expectedSalesVolume":{"type":"integer","description":"Expected sales volume, tickets per year"},"requestedProducts":{"type":"array","items":{"type":"string"},"description":"Requested products"},"requestedVenues":{"type":"array","items":{"type":"string"},"description":"Requested venues"},"preferredDistributionMethod":{"type":"string","enum":["b2bPortal","api","otaConnection","agentPortal","affiliateLink","voucherDistribution","bulkTicketExport","other"],"description":"Preferred distribution method. Distribution methods: b2bPortal (the TICVAI B2B portal), api (partner consumes the TICVAI API), otaConnection (TICVAI integrates into the OTA, either direction per MoM 31 Aug 4.3), agentPortal, affiliateLink, voucherDistribution, bulkTicketExport (pre-generated QR tickets as CSV, MoM 5 Aug option 3), other"},"estimatedAnnualBusiness":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Estimated annual business value"},"contactName":{"type":"string","description":"Applicant contact name"},"billingRequirements":{"type":"string","description":"Billing requirements as stated by the applicant"},"businessCase":{"type":"string","description":"Commercial review: business case"},"territory":{"type":"string","description":"Commercial review: territory"},"creditRequest":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Finance review: requested credit limit"},"paymentTerms":{"type":"string","description":"Finance review: requested payment terms"},"taxRegistrationNumber":{"type":"string","description":"Finance review: tax/VAT registration number"},"productRequirements":{"type":"string","description":"Operations review: product requirements"},"fulfillmentRequirements":{"type":"string","description":"Operations review: fulfilment requirements"},"apiIntegrationRequirements":{"type":"string","description":"Technical review: API/integration requirements"},"applicationId":{"type":"string","format":"uuid","description":"Application id"},"partnerId":{"type":"string","format":"uuid","description":"Partner record created on submission (lifecycle applicant)","nullable":true},"contactEmail":{"type":"string","description":"Applicant contact email","format":"email"},"stage":{"type":"string","enum":["application","businessVerification","documentation","commercialReview","financeReview","technicalReview","approval","configuration","activation"],"description":"Current onboarding stage (pack p.9 Onboarding Workflow)"},"status":{"type":"string","description":"Application status: submitted, inReview, moreInformationRequested, approved, rejected or withdrawn"},"submittedAt":{"type":"string","format":"date-time","description":"Submitted at"},"slaDueAt":{"type":"string","format":"date-time","description":"When the current stage breaches its SLA","nullable":true},"reviewTasks":{"type":"array","description":"Internal Review: the task each department receives","items":{"type":"object","properties":{"department":{"type":"string","enum":["commercial","finance","operations","technical"]},"assignee":{"type":"string"},"dueAt":{"type":"string","format":"date-time"},"completed":{"type":"boolean"}}}},"aiSummary":{"type":"string","description":"Advisory AI summary of the application (pack p.10)","nullable":true}}},
"PartnerOperationsCommandCenterSummary": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection; the headline tiles over the list, computed at read time for the filters in force","description":"**The headline figures on Partner Operations Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.","properties":{"partnerSalesToday":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Partner Sales Today"},"partnerSalesMtd":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Partner Sales MTD"},"activePartnerOrders":{"type":"integer","description":"Active Partner Orders"},"activeReservations":{"type":"integer","description":"Active Reservations"},"activeHolds":{"type":"integer","description":"Active Holds"},"ticketsSold":{"type":"integer","description":"Tickets Sold"},"cancellations":{"type":"integer","description":"Cancellations"},"refunds":{"type":"integer","description":"Refunds"},"outstandingReceivables":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Outstanding Receivables"},"commissionPayable":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Commission Payable"},"pendingSettlements":{"type":"integer","description":"Pending Settlements"},"operationalExceptions":{"type":"integer","description":"Operational Exceptions"},"partnersRequiringAttention":{"type":"integer","description":"Partners Requiring Attention"},"activityFeed":{"type":"array","description":"Activity Feed: recent partner events, newest first","items":{"type":"object","properties":{"at":{"type":"string","format":"date-time"},"partnerId":{"type":"string","format":"uuid"},"message":{"type":"string"}}}}}},
"PartnerOperationsCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over subscription state, assembled at read time from tables that already exist","description":"**What Partner Operations Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"partner":{"type":"string","description":"Partner trading name"},"partnerType":{"type":"string","description":"Partner Type code"},"accountManager":{"type":"string","description":"Account Manager"},"orders":{"type":"integer","description":"Orders"},"tickets":{"type":"integer","description":"Tickets"},"grossSales":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Gross Sales"},"netSales":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Net Sales"},"commission":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Commission"},"outstandingBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Outstanding Balance"},"creditUtilization":{"type":"number","description":"Credit Utilization, percent"},"allocationUtilization":{"type":"number","description":"Allocation Utilization, percent"},"cancellationRate":{"type":"number","description":"Cancellation Rate, percent"},"operationalStatus":{"type":"string","description":"Operational Status: normal, attention, restricted, suspended"},"risk":{"type":"string","enum":["low","medium","high","critical"],"description":"Risk"},"partnerId":{"type":"string","format":"uuid","description":"Partner"},"aiInsights":{"type":"array","items":{"type":"string"},"description":"Advisory AI attention flags for this partner"}}},
"PartnerProfileOrganizationSetupInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; stored as control.partner (Partner); accountManager and the other owners land in the *PrincipalId columns (data model DM4)","description":"**What Partner Profile & Organization Setup submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"partnerId":{"type":"string","format":"uuid","description":"Partner ID; omit to create a new partner"},"legalEntityName":{"type":"string","description":"Legal Entity Name"},"tradingName":{"type":"string","description":"Trading Name"},"partnerType":{"type":"string","description":"Partner type code from the tenant's configurable partner-type list (MoM 31 Aug 4.3: configurable category/type), seeded with the pack's p.7 list: b2bReseller, travelAgent, tourOperator, ota, corporateCustomer, hotelConcierge, destinationManagementCompany, affiliate, wholesaler, distributor, governmentPartner, schoolInstitution, apiPartner, internalGroupCompany"},"registrationNumber":{"type":"string","description":"Registration Number"},"taxVatNumber":{"type":"string","description":"Tax/VAT Number"},"country":{"type":"string","description":"Country, ISO 3166-1 alpha-2"},"city":{"type":"string","description":"City"},"registeredAddress":{"type":"string","description":"Registered Address"},"businessAddress":{"type":"string","description":"Business Address"},"website":{"type":"string","description":"Website","format":"uri"},"mainTelephone":{"type":"string","description":"Main Telephone"},"generalEmail":{"type":"string","description":"General Email","format":"email"},"preferredLanguage":{"type":"string","description":"Preferred Language, BCP 47 tag"},"defaultCurrency":{"type":"string","pattern":"^[A-Z]{3}$","description":"Default Currency, ISO 4217"},"timeZone":{"type":"string","description":"Time Zone, IANA name"},"accountManager":{"type":"string","format":"uuid","description":"Account Manager: staff principal id"},"commercialManager":{"type":"string","format":"uuid","description":"Commercial Manager: staff principal id"},"financeOwner":{"type":"string","format":"uuid","description":"Finance Owner: staff principal id"},"operationalOwner":{"type":"string","format":"uuid","description":"Operational Owner: staff principal id"},"technicalOwner":{"type":"string","format":"uuid","description":"Technical Owner: staff principal id"},"parentPartnerId":{"type":"string","format":"uuid","description":"Parent partner in the hierarchy; empty for a top-level partner","nullable":true},"classificationTags":{"type":"array","items":{"type":"string","enum":["strategic","keyAccount","standard","newPartner","highVolume","vip","restricted"]},"description":"Account Classification: internal tags"}}},
"PartnerProfileOrganizationSetupView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over control.partner (Partner) and the existing subscription state, assembled at read time (data model DM4)","description":"**What Partner Profile & Organization Setup displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"partnerId":{"type":"string","format":"uuid","description":"Partner ID; server-assigned"},"legalEntityName":{"type":"string","description":"Legal Entity Name"},"tradingName":{"type":"string","description":"Trading Name"},"partnerType":{"type":"string","description":"Partner type code from the tenant's configurable partner-type list (MoM 31 Aug 4.3: configurable category/type), seeded with the pack's p.7 list: b2bReseller, travelAgent, tourOperator, ota, corporateCustomer, hotelConcierge, destinationManagementCompany, affiliate, wholesaler, distributor, governmentPartner, schoolInstitution, apiPartner, internalGroupCompany"},"registrationNumber":{"type":"string","description":"Registration Number"},"taxVatNumber":{"type":"string","description":"Tax/VAT Number"},"country":{"type":"string","description":"Country, ISO 3166-1 alpha-2"},"city":{"type":"string","description":"City"},"registeredAddress":{"type":"string","description":"Registered Address"},"businessAddress":{"type":"string","description":"Business Address"},"website":{"type":"string","description":"Website","format":"uri"},"mainTelephone":{"type":"string","description":"Main Telephone"},"generalEmail":{"type":"string","description":"General Email","format":"email"},"preferredLanguage":{"type":"string","description":"Preferred Language, BCP 47 tag"},"defaultCurrency":{"type":"string","pattern":"^[A-Z]{3}$","description":"Default Currency, ISO 4217"},"timeZone":{"type":"string","description":"Time Zone, IANA name"},"accountManager":{"type":"string","format":"uuid","description":"Account Manager: staff principal id"},"commercialManager":{"type":"string","format":"uuid","description":"Commercial Manager: staff principal id"},"financeOwner":{"type":"string","format":"uuid","description":"Finance Owner: staff principal id"},"operationalOwner":{"type":"string","format":"uuid","description":"Operational Owner: staff principal id"},"technicalOwner":{"type":"string","format":"uuid","description":"Technical Owner: staff principal id"},"parentPartnerId":{"type":"string","format":"uuid","description":"Parent partner in the hierarchy (Global Partner -> UAE Entity); empty for a top-level partner","nullable":true},"classificationTags":{"type":"array","items":{"type":"string","enum":["strategic","keyAccount","standard","newPartner","highVolume","vip","restricted"]},"description":"Account Classification: internal tags"},"possibleDuplicates":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Advisory: partner ids the AI duplicate check matched on company details; a human decides"}}},
"PartnerUser": {"type":"object","x-ticvai-persistence":"control.partner_user","description":"2.7.51, BL-075. **A partner was a flat account** — `registerPartner` created one and nothing created a user beneath it.\nThe requirement asks for Master Agency, Branch, Department and User with permissions, quotas and credit cascading down. **That is a scope tree, and `tenancy` already has one** — so this is a principal on a partner branch rather than a new hierarchy.\n**Quota and credit resolve the way configuration does: nearest ancestor wins.** A branch with no credit limit inherits the agency's, which is the behaviour a partner expects and would otherwise have to be enforced by hand.\n","required":["id","partnerId","principalId","branchScopePath"],"properties":{"id":{"type":"string","format":"uuid"},"partnerId":{"x-ticvai-references":"control.partner","type":"string","format":"uuid","description":"The partner (control.partner) the user belongs to. **Resolves to control.partner**, not to control.partner_agreement as the naming convention guessed before the partner master existed (decided 29 September, writers pass; DM4)"},"principalId":{"type":"string","format":"uuid"},"role":{"type":"string","nullable":true,"description":"The partner role shown for the user: Partner Administrator, Booking Agent, Supervisor, Finance User, Reporting User or API Administrator (pack p.12). The permissions the role grants stay RBAC data in identity; this is the label listPartnerContactUser shows (decided 29 September, writers pass; DM4)"},"salesLocation":{"type":"string","nullable":true,"description":"The sales location (branch office or desk) the user sells from, shown on listPartnerContactUser (decided 29 September, writers pass; DM4)"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"description":"Currency the user sells in, ISO 4217; empty means the agreement's settlementCurrency (decided 29 September, writers pass; DM4)"},"accountExpiresAt":{"type":"string","format":"date-time","nullable":true,"description":"When the user's account expires; empty for no expiry. An expired account cannot sign in and shows as `expired` on listPartnerContactUser (decided 29 September, writers pass; DM4)"},"branchScopePath":{"type":"string","description":"The branch this user sits on. **An ltree, like every other scope path**, so a report at agency level rolls up its branches without anybody writing a join.\n"},"allocationQuota":{"type":"integer","nullable":true,"description":"Units this branch may sell. **Null inherits the parent's**, and a quota set at branch level below the agency's is a deliberate restriction rather than an error.\n"},"creditLimitOverride":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"canManageUsers":{"type":"boolean","default":false,"description":"**Partner-managed access control** — 2.7.51 asks for it, and a venue administering every travel agent's staff list is a venue doing the agency's HR.\n"}}},
"Session": {"type":"object","required":["sessionId","principalId","roleId","scope","effectivePermissions"],"properties":{"sessionId":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid"},"roleId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"scope":{"type":"array","description":"Scope nodes this session may act within, resolved once at login from the ltree hierarchy with deny-overrides-allow. Clients filter navigation against this — they never compute it.\n","items":{"$ref":"../shared/common.yaml#/components/schemas/ScopeRef"}},"effectivePermissions":{"allOf":[{"$ref":"../shared/permissions.yaml#/components/schemas/PermissionSet"}],"description":"Flattened set across all granted scopes, after deny resolution. Convenience for coarse checks. Anything scope-sensitive must use `permissionsByScope`.\n"},"permissionsByScope":{"type":"array","description":"Permissions effective at each granted scope path. Clients filter navigation on this and never compute permissions themselves.\n","items":{"$ref":"../shared/permissions.yaml#/components/schemas/ScopedPermissions"}},"saleBoardId":{"type":"string","format":"uuid","description":"Landing surface, derived from the WORKSTATION, not the role (12 Aug 2026 §3). Ticketing, F&B or Retail board.\n\n**Optional since 2 October 2026: only a till session carries it** (Chinmay, door follow-ups; CHG-CSP-002; breaking change against r1 approved as BC-001 to BC-005 in `docs/active/breaking-changes.yaml`). A browser door (ADM-001, SUP-001, PTR-001) and a staff handheld (EMP-001) sign in with no workstation since CHG-DOOR-001, so they have no board to land on and the field is absent. On a till it is the workstation's effective board: the outlet's board unless the till overrides it (`tenancy.Workstation.saleBoardSource`; CHG-CSP-006). A client reads its landing from this field when present and from its own platform otherwise.\n"},"workstation":{"$ref":"#/components/schemas/WorkstationContext"},"openedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time"}}},
"WorkstationContext": {"type":"object","required":["id","code","venueId","regionId"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"regionId":{"type":"string","format":"uuid"},"accessPointId":{"type":"string","format":"uuid","description":"Inherited from the workstation, never selected by the operator."},"devices":{"type":"array","items":{"type":"object","required":["kind","driver"],"properties":{"kind":{"type":"string","enum":["receiptPrinter","ticketPrinter","cashDrawer","barcodeScanner","rfidReader","paymentTerminal","customerDisplay"]},"driver":{"type":"string"},"identifier":{"type":"string"}}}},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"currencyScale":{"type":"integer","minimum":0,"maximum":4},"timezone":{"type":"string"},"cellName":{"type":"string","description":"The cell serving this workstation's region. One cell per tenant per region (ADR-0014). A client uses this only for diagnostics and telemetry tagging — never for routing, which the Control Plane resolves.\n"},"deploymentProfile":{"type":"string","enum":["terminalLocal","venueEdge","thin"],"description":"Whether this surface reads catalogue locally (ADR-0013). Determines which flows the client enables offline.\n"}}}
}
```
