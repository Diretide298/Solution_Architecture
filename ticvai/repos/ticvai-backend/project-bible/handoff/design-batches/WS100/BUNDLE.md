# WS100 — Subscription Licensing AI Self Service board 3

**10 screens · 9 operations · 11 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `PLATFORM_BILLING_MANAGE, PLATFORM_PLAN_MANAGE, PLATFORM_TENANT_VIEW`. A control nobody can use must say so,
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
| `ADM-389` | Commercial Rules Engine Overview | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-390` | VSI Model Builder | B–D | 10 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-391` | VSI Scoring & Tier Threshold Configuration | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-392` | Subscription Tier Configuration | B–D | 0 | 0 | 6 | 2 | 1 | 0 | — | notStarted (—) |
| `ADM-393` | Tier Included Allowances | B–D | 9 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-394` | Commercial & Licensing Model Configuration | B–D | 23 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-395` | Billable Unit, Minimum Guarantee & Enforcement Rules | B–D | 17 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-396` | Overage Pricing & Capacity Packs | B–D | 11 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-397` | Commercial Model & Rule Simulation | B–D | 0 | 16 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-398` | Rule Versioning, Approval & Publication | B–D | 0 | 0 | 6 | 0 | 0 | 3 | — | notStarted (—) |

## Thin screens in this batch

**ADM-391, ADM-392, ADM-397, ADM-398 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-389` Commercial Rules Engine Overview

**Provide TICVAI administrators with the central configuration overview for all commercial and licensing rules.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PLATFORM_PLAN_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/commercial-rules-engine-overview-adm-389` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The commercial rules hub: models, tiers, the active VSI model, customers by model, near thresholds, pending rule changes.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Active Commercial Models** (metric tile)

**Active Tiers** (metric tile)

**Active VSI Model** (metric tile)

**Customers by Commercial Model** (metric tile)

**Average VSI** (metric tile)

**Customers Near Threshold** (metric tile)

**Customers Above Allowance** (metric tile)

**Per-Ticket Contracts** (metric tile)

**Minimum Guarantee Contracts** (metric tile)

**Pending Rule Changes** (metric tile)

**Data it reads**: `listLicensingModels` (onLoad, The rules engine)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Back to Platform Dashboard*
- → `ADM-390` VSI Model Builder: *VSI Model Builder*
- → `ADM-391` VSI Scoring & Tier Threshold Configuration: *VSI Scoring & Tier Threshold Configuration*
- → `ADM-392` Subscription Tier Configuration: *Subscription Tier Configuration*
- → `ADM-393` Tier Included Allowances: *Tier Included Allowances*
- → `ADM-394` Commercial & Licensing Model Configuration: *Commercial & Licensing Model Configuration*
- → `ADM-395` Billable Unit, Minimum Guarantee & Enforcement Rules: *Billable Unit, Minimum Guarantee & Enforcement Rules*
- → `ADM-396` Overage Pricing & Capacity Packs: *Overage Pricing & Capacity Packs*
- → `ADM-397` Commercial Model & Rule Simulation: *Commercial Model & Rule Simulation*
- → `ADM-398` Rule Versioning, Approval & Publication: *Rule Versioning, Approval & Publication*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The commercial rules overview list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the commercial rules overview untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing to show yet**: the figures fill as activity is recorded. Offers no create action — a monitor creates nothing — and says so rather than showing empty tiles. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the commercial rules overview are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
metric tiles:
  Active Commercial Models: 128
  Active Tiers: 46
  Active VSI Model: 312
  Customers by Commercial Model: 74
  Average VSI: 42 min
  Customers Near Threshold: 233
  Customers Above Allowance: 57
  Per-Ticket Contracts: 11
  Minimum Guarantee Contracts: AED 12,400.00
  Pending Rule Changes: 46
```

#### Permissions

- `listLicensingModels` → `PLATFORM_PLAN_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-389` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS155 Subscription Licensing AI Self Service Board 3.dc.html#adm-389`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 3
- Flow F209 *Subscription Licensing AI Self Service board 3: Commercial Rules Engine Overview*, step 1: Opens Commercial Rules Engine Overview → Provide TICVAI administrators with the central configuration overview for all commercial and licensing rules.
- Flow F209 *Subscription Licensing AI Self Service board 3: Commercial Rules Engine Overview*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F209 *Subscription Licensing AI Self Service board 3: Commercial Rules Engine Overview*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F209 *Subscription Licensing AI Self Service board 3: Commercial Rules Engine Overview*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F209 *Subscription Licensing AI Self Service board 3: Commercial Rules Engine Overview*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F209 *Subscription Licensing AI Self Service board 3: Commercial Rules Engine Overview*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F209 *Subscription Licensing AI Self Service board 3: Commercial Rules Engine Overview*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F209 *Subscription Licensing AI Self Service board 3: Commercial Rules Engine Overview*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F209 branch at step 1 (expected): when Nothing has been set up on Commercial Rules Engine Overview yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F209 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-389?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-002`, `ADM-390`, `ADM-391`, `ADM-392`, `ADM-393`, `ADM-394`, `ADM-395`, `ADM-396`, `ADM-397`, `ADM-398`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-390` VSI Model Builder

**Configure how TICVAI determines the operational size and complexity of a customer. VSI remains important even where VSI does not determine customer pricing.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PLATFORM_PLAN_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration Fields) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/vsi-model-builder-adm-390` |

**Known gaps.** **VSI Model Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** How TICVAI scores a customer's operational size (VSI): factors, weights, sources, bounds and applicability.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Factor Name | select field | — | — | — | — | — | — |
| Weight | select field | — | — | — | — | — | — |
| Data Source | select field | — | — | — | — | — | — |
| Minimum Value | select field | — | — | — | — | — | — |
| Maximum Value | select field | — | — | — | — | — | — |
| Scoring Method | select field | — | — | — | — | — | — |
| Mandatory/Optional | select field | — | — | — | — | — | — |
| Venue Type Applicability | select field | — | — | — | — | — | — |
| Market Applicability | select field | — | — | — | — | — | — |
| Effective Date | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Weights**: Weights total 100%; the screen shows the running total and refuses another sum. *(source: designer default)*

#### Outputs: what the screen shows and produces

**Data it reads**: `getVsiModel` (onLoad, The VSI model)

**Where the user goes next**

- → `ADM-389` Commercial Rules Engine Overview: *Back to Commercial Rules Engine Overview*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The vsi model configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the vsi model untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No vsi model configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
form example:
  Factor Name: 74
  Weight: 11
  Data Source: 233
  Minimum Value: AED 96,750.00
  Maximum Value: AED 12,400.00
  Scoring Method: 74
  Mandatory/Optional: 128
  Venue Type Applicability: AquaCove Dubai
  Market Applicability: 19
  Effective Date: 01/10/2026 09:14
```

#### Permissions

- `getVsiModel` → `PLATFORM_PLAN_MANAGE` (configure) · staff
- `setVsiModel` → `PLATFORM_PLAN_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- VSI is a weighted composite of onboarding factors - annual attendance (illustrated ~30% weight), POS terminals, access-control devices, venues, users, annual transaction volume - each configurable as mandatory or optional. *(agreed · MoM 10 Sep 2026, 4.2 Venue Size Index (VSI) Model & Tier Threshold Configuration · DI-817)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-390` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS155 Subscription Licensing AI Self Service Board 3.dc.html#adm-390`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 3
- Flow F209 *Subscription Licensing AI Self Service board 3: Commercial Rules Engine Overview*, step 2: Works in VSI Model Builder → Configure how TICVAI determines the operational size and complexity of a customer. VSI remains important even where VSI does not determine customer pricing.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-390?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-389`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-391` VSI Scoring & Tier Threshold Configuration

**Translate actual customer characteristics into a standardized VSI score and recommended operational tier.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PLATFORM_PLAN_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/vsi-scoring-tier-threshold-configuration-adm-391` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** VSI score thresholds that map to operational tiers.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save VSI model (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-389` Commercial Rules Engine Overview: *Back to Commercial Rules Engine Overview*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The vsi scoring tier list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the vsi scoring tier untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No vsi scoring tier yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the vsi scoring tier are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
thresholds:
- 0-30 Starter
- 31-60 Growth
- 61-100 Enterprise
```

#### Permissions

- `setVsiModel` → `PLATFORM_PLAN_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Tier thresholds map VSI ranges to tiers (0-30 Essential, 31-60 Professional, 61-80 Enterprise, 81-100 Enterprise Plus) with per-factor sub-thresholds (attendance 100-100,000 = 10 pts; 100,000-500,000 = 40); the system calculates the score and recommends the tier automatically. *(agreed · MoM 10 Sep 2026, 4.2 Venue Size Index (VSI) Model & Tier Threshold Configuration · DI-818)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-391` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS155 Subscription Licensing AI Self Service Board 3.dc.html#adm-391`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 3
- Flow F209 *Subscription Licensing AI Self Service board 3: Commercial Rules Engine Overview*, step 4: Works in VSI Scoring & Tier Threshold Configuration → Translate actual customer characteristics into a standardized VSI score and recommended operational tier.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-391?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save VSI model, Cancel.
- [ ] Every transition is wired: `ADM-389`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-392` Subscription Tier Configuration

**Configure TICVAI's standard subscription tiers for customers using tier-based commercial models.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PLATFORM_PLAN_MANAGE`, `PLATFORM_TENANT_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/subscription-tier-configuration-adm-392` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** TICVAI's standard subscription tiers (plans) for tier-based models.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Offered to tenant | picker: choose an offered to tenant | — | — | `listPlans` ?offeredToTenantId |
| Package kind | segmented control | — | Standard · Custom | `listPlans` ?packageKind |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create plan (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listPlans` (onLoad, Tiers defined)

**Where the user goes next**

- → `ADM-389` Commercial Rules Engine Overview: *Back to Commercial Rules Engine Overview*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The subscription tier list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the subscription tier untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No subscription tier yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the subscription tier are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 `offeredToTenantId` on a standard package, or a tenant that does not exist |

#### Edge cases to draw

- **Can read but not change (holds PLATFORM_TENANT_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: PLATFORM_PLAN_MANAGE for createPlan. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/subscription.yaml#createPlan)*
- **createPlan answers 422**: Show it as something the person can act on, not a failure: `offeredToTenantId` on a standard package, or a tenant that does not exist *(source: contracts/satellite/subscription.yaml#createPlan)*

#### Consistency with other screens

- Match `ADM-008`: Same plan objects.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listPlans (Plan):
- code: AQC-AUH
  name: Growth plan
  description: Guest charged twice at Main Gate Till 3
  basePrice: AED 1,250.00
  billingPeriod: monthly
- code: AQC-DXB
  name: AquaCove Annual Pass Gold
  description: Group of 40 from Desert Gate Tours
  basePrice: AED 48,000.00
  billingPeriod: quarterly
```

#### Permissions

- `createPlan` → `PLATFORM_PLAN_MANAGE` (configure) · staff
- `listPlans` → `PLATFORM_TENANT_VIEW` (read) · staff, prospect

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.2.1 | Subscription Plans - System shall support configurable subscription plans. | Subscription & Licensing Management | CONTRACTED | `createPlan` |
| 20.4.8 | Module Pricing - System shall support module-specific pricing. | Subscription & Licensing Management | CONTRACTED | `createPlan` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Each tier has its own price payable monthly, annually or in advance (cheque/bank transfer), with a configurable trial period; tier-included allowances (e.g. Professional up to 10 POS devices and 20 users) at the same price anywhere within the range. *(client request · MoM 10 Sep 2026, 4.3 Subscription Tiers, Allowances & Usage Thresholds · DI-819)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-392` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS155 Subscription Licensing AI Self Service Board 3.dc.html#adm-392`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 3
- Flow F209 *Subscription Licensing AI Self Service board 3: Commercial Rules Engine Overview*, step 6: Works in Subscription Tier Configuration → Configure TICVAI's standard subscription tiers for customers using tier-based commercial models.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-392?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create plan, Cancel.
- [ ] Every transition is wired: `ADM-389`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`, `PLATFORM_TENANT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-393` Tier Included Allowances

**Configure the resources included within each standard subscription tier.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PLATFORM_PLAN_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration per Allowance) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/tier-included-allowances-adm-393` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** What each tier includes: metric, quantity, period, warning threshold, enforcement, overage.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Metric | select field | — | — | — | — | — | — |
| Quantity | select field | — | — | — | — | — | — |
| Measurement Period | select field | — | — | — | — | — | — |
| Reset Period | select field | — | — | — | — | — | — |
| Warning Threshold | select field | — | — | — | — | — | — |
| Enforcement Type | select field | — | — | — | — | — | — |
| Overage Allowed | select field | — | — | — | — | — | — |
| Overage Rate | select field | — | — | — | — | — | — |
| Additional Pack Allowed | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setLicensingModel: tenant-wide only, no region or venue override is offered. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/satellite/subscription.yaml#setLicensingModel)*

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `ADM-389` Commercial Rules Engine Overview: *Back to Commercial Rules Engine Overview*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The tier included allowances configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the tier included allowances untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No tier included allowances configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
form example:
  Metric: 57
  Quantity: 46
  Measurement Period: 19
  Reset Period: 11
  Warning Threshold: 0
  Enforcement Type: 233
  Overage Allowed: 3 h 20 min
  Overage Rate: 87%
  Additional Pack Allowed: 11
```

#### Permissions

- `setLicensingModel` → `PLATFORM_PLAN_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Each tier has its own price payable monthly, annually or in advance (cheque/bank transfer), with a configurable trial period; tier-included allowances (e.g. Professional up to 10 POS devices and 20 users) at the same price anywhere within the range. *(client request · MoM 10 Sep 2026, 4.3 Subscription Tiers, Allowances & Usage Thresholds · DI-819)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-393` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS155 Subscription Licensing AI Self Service Board 3.dc.html#adm-393`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 3
- Flow F209 *Subscription Licensing AI Self Service board 3: Commercial Rules Engine Overview*, step 8: Works in Tier Included Allowances → Configure the resources included within each standard subscription tier.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-393?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-389`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-394` Commercial & Licensing Model Configuration

**This is the major revised screen. Configure how TICVAI charges a customer independently from how TICVAI technically licenses the customer. A. Commercial Charging Model**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PLATFORM_PLAN_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Commercial Configuration Fields; Separately configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/commercial-licensing-model-configuration-adm-394` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** How TICVAI charges a customer (commercial model) separately from how it licenses them technically: charging unit, rate, currency, guarantee, base fee, module charging, and the technical limits.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Commercial Model | select field | — | — | — | — | — | — |
| Charging Unit | select field | — | — | — | — | — | — |
| Rate | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Billing Period | select field | — | — | — | — | — | — |
| Included Volume | select field | — | — | — | — | — | — |
| Minimum Guarantee | select field | — | — | — | — | — | — |
| Guarantee Period | select field | — | — | — | — | — | — |
| Percentage Rate | select field | — | — | — | — | — | — |
| Fixed Base Fee | select field | — | — | — | — | — | — |
| Module Charging | select field | — | — | — | — | — | — |
| Effective Date | select field | — | — | — | — | — | — |
| Expiry | select field | — | — | — | — | — | — |
| Contract Applicability | select field | — | — | — | — | — | — |
| POS Limit | select field | — | — | — | — | — | — |
| Access Device Limit | select field | — | — | — | — | — | — |
| User Limit | select field | — | — | — | — | — | — |
| Venue Limit | select field | — | — | — | — | — | — |
| API Limit | select field | — | — | — | — | — | — |
| Storage Limit | select field | — | — | — | — | — | — |
| Module Entitlements | select field | — | — | — | — | — | — |
| Technical Capacity Profile | select field | — | — | — | — | — | — |
| Hard/Soft/Approval Enforcement | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setLicensingModel: tenant-wide only, no region or venue override is offered. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/satellite/subscription.yaml#setLicensingModel)*

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `ADM-389` Commercial Rules Engine Overview: *Back to Commercial Rules Engine Overview*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The commercial licensing model configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the commercial licensing model untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No commercial licensing model configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
form example:
  Commercial Model: 128
  Charging Unit: 57
  Rate: 94%
  Currency: 74
  Billing Period: AED 482,300.00
  Included Volume: 19
  Minimum Guarantee: AED 12,400.00
  Guarantee Period: AED 12,400.00
  Percentage Rate: 64%
  Fixed Base Fee: AED 12,400.00
  Module Charging: 46
  Effective Date: 28/09/2026 11:45
  Expiry: 312
  Contract Applicability: 74
```

#### Permissions

- `setLicensingModel` → `PLATFORM_PLAN_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Commercial models, combinable per client: tier-based, tier plus usage, per-ticket, per-transaction, percentage-based, minimum guarantee, hybrid, fixed multi-year contract. *(agreed · MoM 10 Sep 2026, 4.4 Commercial & Licensing Pricing Models · DI-821)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-394` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS155 Subscription Licensing AI Self Service Board 3.dc.html#adm-394`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 3
- Flow F209 *Subscription Licensing AI Self Service board 3: Commercial Rules Engine Overview*, step 10: Works in Commercial & Licensing Model Configuration → This is the major revised screen. Configure how TICVAI charges a customer independently from how TICVAI technically licenses the customer. A. Commercial Charging Model

#### Acceptance for the design

- [ ] Every input above is drawn (23), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-394?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-389`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-395` Billable Unit, Minimum Guarantee & Enforcement Rules

**Define exactly what TICVAI counts commercially and what happens when contractual or technical thresholds are reached.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PLATFORM_PLAN_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration should support; Commercial rule can specify; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/billable-unit-minimum-guarantee-enforcement-rules-adm-395` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** What counts as billable and what happens at contractual or technical thresholds (minimum guarantee, carry forward).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Ticket Sold | select field | — | — | — | — | — | — |
| Ticket Issued | select field | — | — | — | — | — | — |
| Paid Ticket | select field | — | — | — | — | — | — |
| Transaction | select field | — | — | — | — | — | — |
| Admission/Redemption | select field | — | — | — | — | — | — |
| Gross Transaction Value | select field | — | — | — | — | — | — |
| Net Transaction Value | select field | — | — | — | — | — | — |
| Custom Billable Event | select field | — | — | — | — | — | — |
| 50 billable tickets | select field | — | — | — | — | — | — |
| 1 billable transaction | select field | — | — | — | — | — | — |
| Guarantee Amount | select field | — | — | — | — | — | — |
| Monthly / Quarterly / Annual | text field | — | — | — | — | — | — |
| Carry Forward Allowed | select field | — | — | — | — | — | — |
| Carry Forward Period | select field | — | — | — | — | — | — |
| Reconciliation Method | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Effective Dates | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setLicensingModel: tenant-wide only, no region or venue override is offered. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/satellite/subscription.yaml#setLicensingModel)*

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `ADM-389` Commercial Rules Engine Overview: *Back to Commercial Rules Engine Overview*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The billable unit minimum configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the billable unit minimum untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No billable unit minimum configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
form example:
  Ticket Sold: 74
  Ticket Issued: 3
  Paid Ticket: 233
  Transaction: 57
  Admission/Redemption: 128
  Gross Transaction Value: AED 96,750.00
  Net Transaction Value: AED 482,300.00
  Custom Billable Event: 19
  50 billable tickets: 7
  1 billable transaction: 11
  Guarantee Amount: AED 48,000.00
  Monthly / Quarterly / Annual: 11
  Carry Forward Allowed: AED 482,300.00
  Carry Forward Period: AED 482,300.00
```

#### Permissions

- `setLicensingModel` → `PLATFORM_PLAN_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Billable/excludable ticket rules (e.g. complimentary, voided and refunded tickets excluded), minimum guarantee and overage rate are configured together; a commercial model simulator tests a model before it is assigned to a customer. *(client request · MoM 10 Sep 2026, 4.4 Commercial & Licensing Pricing Models · DI-822)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-395` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS155 Subscription Licensing AI Self Service Board 3.dc.html#adm-395`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 3
- Flow F209 *Subscription Licensing AI Self Service board 3: Commercial Rules Engine Overview*, step 12: Works in Billable Unit, Minimum Guarantee & Enforcement Rules → Define exactly what TICVAI counts commercially and what happens when contractual or technical thresholds are reached.

#### Acceptance for the design

- [ ] Every input above is drawn (17), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-395?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-389`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-396` Overage Pricing & Capacity Packs

**Configure additional consumption pricing and purchasable capacity.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PLATFORM_BILLING_MANAGE`, `PLATFORM_PLAN_MANAGE` (2 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Pack Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/overage-pricing-capacity-packs-adm-396` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Overage prices and purchasable capacity packs.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Pack Name | select field | — | — | — | — | — | — |
| Resource | select field | — | — | — | — | — | — |
| Quantity | select field | — | — | — | — | — | — |
| Price | select field | — | — | — | — | — | — |
| Recurring/One-Time | select field | — | — | — | — | — | — |
| Validity | select field | — | — | — | — | — | — |
| Applicable Tier | select field | — | — | — | — | — | — |
| Applicable Commercial Model | select field | — | — | — | — | — | — |
| Auto-Renew | select field | — | — | — | — | — | — |
| Proration | select field | — | — | — | — | — | — |
| Effective Dates | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setLicensingModel: tenant-wide only, no region or venue override is offered. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/satellite/subscription.yaml#setLicensingModel)*

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `ADM-389` Commercial Rules Engine Overview: *Back to Commercial Rules Engine Overview*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The overage pricing capacity configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the overage pricing capacity untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No overage pricing capacity configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
form example:
  Pack Name: 46
  Resource: 46
  Quantity: 312
  Price: AED 1,250.00
  Recurring/One-Time: 42 min
  Validity: 233
  Applicable Tier: 233
  Applicable Commercial Model: 312
  Auto-Renew: 312
  Proration: 312
  Effective Dates: 46
```

#### Permissions

- `setLicensingModel` → `PLATFORM_PLAN_MANAGE` (configure) · staff
- `addCapacityPack` → `PLATFORM_BILLING_MANAGE` (configure) · staff, prospect

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Billable/excludable ticket rules (e.g. complimentary, voided and refunded tickets excluded), minimum guarantee and overage rate are configured together; a commercial model simulator tests a model before it is assigned to a customer. *(client request · MoM 10 Sep 2026, 4.4 Commercial & Licensing Pricing Models · DI-822)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-396` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS155 Subscription Licensing AI Self Service Board 3.dc.html#adm-396`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 3
- Flow F209 *Subscription Licensing AI Self Service board 3: Commercial Rules Engine Overview*, step 14: Works in Overage Pricing & Capacity Packs → Configure additional consumption pricing and purchasable capacity.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-396?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-389`.
- [ ] Every gated control is gated: `PLATFORM_BILLING_MANAGE`, `PLATFORM_PLAN_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-397` Commercial Model & Rule Simulation

**Allow TICVAI to test commercial models before applying them. This screen now becomes more powerful than the original Board 3 simulator.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PLATFORM_PLAN_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/commercial-model-rule-simulation-adm-397` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Test a commercial model against a customer profile before applying it: annual cost, revenue, guarantee, overage, risk.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The table's columns are the workshop pack's labels with no bound response field (0 of 8 labels bound). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every commercial model rule** (data table)

| Shows | Format | Notes |
|---|---|---|
| Customer annual cost | text | not in the schema: `Customer Annual Cost` |
| TICVAI revenue | text | not in the schema: `TICVAI Revenue` |
| Variable revenue | text | not in the schema: `Variable Revenue` |
| Minimum guarantee | text | not in the schema: `Minimum Guarantee` |
| Capacity | text | not in the schema: `Capacity` |
| Projected overage | text | not in the schema: `Projected Overage` |
| Contract value | text | not in the schema: `Contract Value` |
| Commercial risk | text | not in the schema: `Commercial Risk` |

**The selected commercial model rule** (detail panel): The pack groups this record's detail under its own headings: “Customer Inputs”, “AED 145K/year”, “AED 150K/year”, “AED 120K/year”.

| Shows | Format | Notes |
|---|---|---|
| Customer annual cost | text | not in the schema: `Customer Annual Cost` |
| TICVAI revenue | text | not in the schema: `TICVAI Revenue` |
| Variable revenue | text | not in the schema: `Variable Revenue` |
| Minimum guarantee | text | not in the schema: `Minimum Guarantee` |
| Capacity | text | not in the schema: `Capacity` |
| Projected overage | text | not in the schema: `Projected Overage` |
| Contract value | text | not in the schema: `Contract Value` |
| Commercial risk | text | not in the schema: `Commercial Risk` |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Money columns (Contract Value, Customer Annual Cost, TICVAI Revenue, Variable Revenue)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. Across tenants or regions figures in different currencies are never summed into one total; group by currency, or label the converted figure with its rate and time. *(source: ADR-0008; ADR-0011; DI-306)*

**Where the user goes next**

- → `ADM-389` Commercial Rules Engine Overview: *Back to Commercial Rules Engine Overview*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The commercial model rule list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the commercial model rule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No commercial model rule yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the commercial model rule are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every commercial model rule:
- Customer Annual Cost: Marina Leisure Group
  TICVAI Revenue: AED 12,400.00
  Variable Revenue: AED 96,750.00
  Minimum Guarantee: AED 12,400.00
  Capacity: 128
  Projected Overage: 1.8 s
  Contract Value: AED 12,400.00
  Commercial Risk: 2
- Customer Annual Cost: Desert Gate Tours LLC
  TICVAI Revenue: AED 482,300.00
  Variable Revenue: AED 12,400.00
  Minimum Guarantee: AED 482,300.00
  Capacity: 46
  Projected Overage: 3 h 20 min
  Contract Value: AED 482,300.00
  Commercial Risk: 0
- Customer Annual Cost: Arabian Trails
  TICVAI Revenue: AED 96,750.00
  Variable Revenue: AED 482,300.00
  Minimum Guarantee: AED 96,750.00
  Capacity: 312
  Projected Overage: 42 min
  Contract Value: AED 96,750.00
  Commercial Risk: 5
```

#### Permissions

- `simulateCommercialPackage` → `PLATFORM_PLAN_MANAGE` (configure) · staff, guest, prospect

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Billable/excludable ticket rules (e.g. complimentary, voided and refunded tickets excluded), minimum guarantee and overage rate are configured together; a commercial model simulator tests a model before it is assigned to a customer. *(client request · MoM 10 Sep 2026, 4.4 Commercial & Licensing Pricing Models · DI-822)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-397` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS155 Subscription Licensing AI Self Service Board 3.dc.html#adm-397`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 3
- Flow F209 *Subscription Licensing AI Self Service board 3: Commercial Rules Engine Overview*, step 16: Works in Commercial Model & Rule Simulation → Allow TICVAI to test commercial models before applying them. This screen now becomes more powerful than the original Board 3 simulator.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-397?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-389`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-398` Rule Versioning, Approval & Publication

**Govern changes to all commercial, VSI, licensing, billable-unit and pricing rules.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PLATFORM_PLAN_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `planId` (navigation) |
| Route | `/tenants-licensing/rule-versioning-approval-publication-adm-398` |

**Known gaps.** **The pack names 2 actions on this screen and the screen declares 0 operations.** Unserved: Revised Board 3 — Critical Architecture, 1. Operational Classification. Each needs an operation, or needs … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Versioning, approval and publication of commercial, VSI and licensing rules.

**Fixed on main** (the package already carries these; draw what it says): Buttons labelled "Revised Board 3 — Critical Architecture" and "1. Operational Classification". (CHG-SBO-015).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create plan version (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-389` Commercial Rules Engine Overview: *Back to Commercial Rules Engine Overview*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rule versioning approval list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rule versioning approval untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rule versioning approval yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rule versioning approval are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 `offeredToTenantId` on a standard package, or a tenant that does not exist |

#### Edge cases to draw

- **createPlanVersion answers 422**: Show it as something the person can act on, not a failure: `offeredToTenantId` on a standard package, or a tenant that does not exist *(source: contracts/satellite/subscription.yaml#createPlanVersion)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
change: VSI model v4
status: awaiting approval
effectiveFrom: 01/11/2026
```

#### Permissions

- `createPlanVersion` → `PLATFORM_PLAN_MANAGE` (configure) · staff

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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-398` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS155 Subscription Licensing AI Self Service Board 3.dc.html#adm-398`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 3
- Flow F209 *Subscription Licensing AI Self Service board 3: Commercial Rules Engine Overview*, step 18: Works in Rule Versioning, Approval & Publication → Govern changes to all commercial, VSI, licensing, billable-unit and pricing rules.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-398?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create plan version, Cancel.
- [ ] Every transition is wired: `ADM-389`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
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

**8 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"addCapacityPack": {"method":"POST","path":"/capacity-packs","contract":"subscription","summary":"Buy headroom without changing tier","permission":"PLATFORM_BILLING_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"platform","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CapacityPack","responds":"CapacityPack"},
"createPlan": {"method":"POST","path":"/plans","contract":"subscription","summary":"Create a subscription plan","permission":"PLATFORM_PLAN_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreatePlanRequest","responds":"Plan"},
"createPlanVersion": {"method":"POST","path":"/plans/{planId}","contract":"subscription","summary":"Publish a new version of a plan","permission":"PLATFORM_PLAN_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreatePlanRequest","responds":"Plan"},
"getVsiModel": {"method":"GET","path":"/vsi-models","contract":"subscription","summary":"How a customer's scale is scored into a tier","permission":"PLATFORM_PLAN_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"platform","parameters":[],"requestBody":null,"responds":"VsiModel"},
"listLicensingModels": {"method":"GET","path":"/licensing-models","contract":"subscription","summary":"Billable units, minimum guarantees and overage","permission":"PLATFORM_PLAN_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"platform","parameters":[],"requestBody":null,"responds":"LicensingModel"},
"listPlans": {"method":"GET","path":"/plans","contract":"subscription","summary":"List subscription plans","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"offeredToTenantId","in":"query","required":false},{"name":"packageKind","in":"query","required":false}],"requestBody":null,"responds":"Plan"},
"setLicensingModel": {"method":"PUT","path":"/licensing-models","contract":"subscription","summary":"Define the billable unit and what happens at the edges","permission":"PLATFORM_PLAN_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"platform","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"LicensingModel","responds":"LicensingModel"},
"setVsiModel": {"method":"PUT","path":"/vsi-models","contract":"subscription","summary":"Weights, thresholds and the tiers they map to","permission":"PLATFORM_PLAN_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"platform","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VsiModel","responds":"VsiModel"},
"simulateCommercialPackage": {"method":"POST","path":"/package-simulations","contract":"subscription","summary":"What this package would cost, and what it would provision","permission":"PLATFORM_PLAN_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"platform","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PackageSimulationRequest","responds":"PackageSimulation"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"CapacityPack": {"type":"object","x-ticvai-persistence":"subscription.capacity_pack","description":"Board 3.8. **A good season should not require renegotiating a contract in August.**\n","required":["tenantId","unit","quantity"],"properties":{"id":{"type":"string","format":"uuid"},"tenantId":{"type":"string","format":"uuid"},"unit":{"type":"string"},"quantity":{"type":"integer"},"price":{"x-ticvai-column":"list_price","$ref":"../shared/common.yaml#/components/schemas/Money"},"validFrom":{"type":"string","format":"date"},"validTo":{"type":"string","format":"date","nullable":true},"temporary":{"type":"boolean","default":true},"approvedBy":{"type":"string","format":"uuid","nullable":true},"invoiceId":{"type":"string","format":"uuid","nullable":true}}},
"CellTier": {"type":"string","enum":["shared","dedicated","isolated","clientHosted"]},
"CreatePlanRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["code","name","cellTier","licensedModules","limits","basePrice"],"properties":{"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":1000},"cellTier":{"$ref":"#/components/schemas/CellTier"},"licensedModules":{"type":"array","minItems":1,"description":"**A closed set as of 24 August.** `moduleKey` was a free string, so nothing could join a licence to a screen — **a tenant without an F&B licence was still served every F&B screen**, because no screen said which module it belonged to in a form the licence could match.\n**The key is the join.** `screen.requiresModule` names one of these, and navigation is built from the intersection of what a tenant licensed and what their role permits.\n","items":{"$ref":"#/components/schemas/ModuleKey"}},"limits":{"type":"array","items":{"$ref":"#/components/schemas/EntitlementLimit"}},"basePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"billingPeriod":{"type":"string","enum":["monthly","quarterly","annual"]},"includesBrandedApp":{"type":"boolean","description":"Branded native publishing carries per-tenant operational cost and is priced, not absorbed.\n"},"includedAiTokens":{"type":"integer","nullable":true,"description":"AI tokens the package includes per billing period. Usage beyond it is a `metered` invoice line at the AI module's price (decided 29 September)."},"requestLimits":{"$ref":"#/components/schemas/PlanRequestLimits"},"packageKind":{"type":"string","enum":["standard","custom"],"default":"standard","description":"**Three standard packages, and custom ones allowed** (decided 29 September, Chinmay)."},"offeredToTenantId":{"type":"string","format":"uuid","nullable":true,"description":"**Private to one tenant** (decided 29 September, Chinmay): a custom package offered only to this tenant; `listPlans` shows it to no other tenant and `setSubscription` refuses it for any other (422 `plan-not-offered`). Null for a package any tenant may buy. Custom packages only."}}},
"EntitlementLimit": {"type":"object","required":["metric","limit"],"properties":{"metric":{"$ref":"#/components/schemas/UsageMetric"},"limit":{"type":"integer","nullable":true,"x-ticvai-column":"limit_value","description":"Null means unlimited. Stored as `limit_value` — `limit` is a reserved word, and `subscription.tier_allowance` already names the same figure `limit_value`."},"overageAllowed":{"type":"boolean","default":false},"overageUnitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},
"LicensingModel": {"type":"object","x-ticvai-persistence":"subscription.licensing_model","description":"Boards 3.6 and 3.7. **The single most consequential commercial decision in the product.**\n","required":["code","billableUnit"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"billableUnit":{"type":"string","enum":["perVenue","perAdmission","perTransaction","perActiveUser","perDevice","perModule","flatFee","revenueShare"]},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"revenueSharePercent":{"type":"number","nullable":true},"minimumGuarantee":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"minimumGuaranteePeriod":{"type":"string","enum":["monthly","quarterly","annual"],"nullable":true},"onBelowMinimum":{"type":"string","enum":["chargeMinimum","carryForward","waive"],"default":"chargeMinimum","description":"**A minimum guarantee with no enforcement rule is a number in a contract.**"},"includedAllowances":{"type":"object","additionalProperties":{"type":"integer"}},"overagePricing":{"type":"array","items":{"type":"object","properties":{"unit":{"type":"string"},"fromQuantity":{"type":"integer"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"tierCode":{"type":"string","nullable":true},"effectiveFrom":{"type":"string","format":"date","nullable":true}}},
"ModuleKey": {"$ref":"../shared/common.yaml#/components/schemas/ModuleKey"},
"PackageSimulation": {"type":"object","description":"Boards 3.9 and 4.8. **Refused at quote time rather than at go-live.**","properties":{"lines":{"type":"array","items":{"type":"object","properties":{"kind":{"type":"string","enum":["baseTier","module","addOn","capacityPack","overage","professionalServices","discount"]},"label":{"type":"string"},"quantity":{"type":"number","nullable":true},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"recurringTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"oneOffTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"contractTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"minimumGuarantee":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"findings":{"type":"array","items":{"type":"object","properties":{"severity":{"type":"string","enum":["blocking","warning","advisory"]},"code":{"type":"string"},"message":{"type":"string"}}}},"provisionable":{"type":"boolean"}}},
"PackageSimulationRequest": {"type":"object","required":["tierCode"],"properties":{"tierCode":{"type":"string"},"licensingModelId":{"type":"string","format":"uuid","nullable":true},"moduleCodes":{"type":"array","items":{"type":"string"}},"venueCount":{"type":"integer","default":1},"projectedVolumes":{"type":"object","additionalProperties":{"type":"integer"}},"contractMonths":{"type":"integer","default":12},"billingCycle":{"type":"string","nullable":true},"currency":{"type":"string","nullable":true}}},
"Plan": {"x-ticvai-persistence":"subscription.plan + subscription.plan_module + subscription.plan_limit","description":"**A plan's modules and limits are rows, keyed on `plan_id`.** `licensedModules` and `limits` are required on every plan, and `subscription.plan` alone had no column for either — so the licence position, the downgrade check and every module gate had nothing to read. `plan_module` holds one row per licensed `ModuleKey`; `plan_limit` one row per `EntitlementLimit`. Both belong to the plan version the row is, so a subscriber on an earlier version keeps the modules and limits they were sold.","allOf":[{"$ref":"#/components/schemas/CreatePlanRequest"},{"type":"object","required":["id","version","isActive","subscriberCount"],"properties":{"id":{"type":"string","format":"uuid"},"version":{"type":"string","description":"Existing subscribers stay on the version they were sold. A price change never applies retroactively.\n"},"isActive":{"type":"boolean"},"subscriberCount":{"type":"integer"},"publishedAt":{"type":"string","format":"date-time"}}}]},
"PlanRequestLimits": {"type":"object","nullable":true,"x-ticvai-persistence":"none — embedded in subscription.plan as its request_limits jsonb column","description":"**The limits section of a plan: every tenant has a request budget** (ADR-0064, accepted 1 October; it decides the per-tenant limit ADR-0032 deferred). A token bucket per tenant and audience in the kernel middleware of `commerce`, `access` and `operations`, counted in Azure Managed Redis so every replica agrees; a guest browse never spends a till's budget. Over budget, the call is refused `429` with `Retry-After` and the `RateLimit-*` headers (every operation declares it).\n\n**Null takes the platform default**, which starts at twice the tenant's expected peak from its sizing tier (`handoff/sizing.json` venue tiers) and is recalibrated after the benchmark and after four weeks of production. **A tenant may use the whole platform when others are quiet**: the per-replica share (`replicaSharePercent`) is enforced only above `shareEnforcedAbovePercent` of the replica's limit. If Redis is unavailable each replica falls back to its own buckets (the limit divided by the replica count); the request path never fails because the limiter's store did.","properties":{"guest":{"$ref":"#/components/schemas/RequestBudget"},"staff":{"$ref":"#/components/schemas/RequestBudget"},"service":{"$ref":"#/components/schemas/RequestBudget"},"partner":{"$ref":"#/components/schemas/RequestBudget"},"replicaSharePercent":{"type":"integer","minimum":1,"maximum":100,"default":25,"description":"The most of one replica's request slots one tenant may hold while the share is enforced."},"shareEnforcedAbovePercent":{"type":"integer","minimum":1,"maximum":100,"default":70,"description":"The replica load, as a percent of its limit, above which the share is enforced."}}},
"VsiModel": {"type":"object","x-ticvai-persistence":"subscription.vsi_model","description":"Board 3.2. **The number the whole commercial model hangs on**, and configurable so a prospect reaches a package without a sales call.\n","properties":{"version":{"type":"integer"},"factors":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string","enum":["annualVisitors","peakDailyCapacity","venueCount","salesChannels","moduleCount","integrationComplexity","seasonality","operatingHours","staffCount"]},"label":{"type":"string"},"weight":{"type":"number"},"bands":{"type":"array","items":{"type":"object","properties":{"upTo":{"type":"number","nullable":true},"points":{"type":"number"}}}}}}},"tiers":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string"},"name":{"type":"string"},"minimumScore":{"type":"number"},"maximumScore":{"type":"number","nullable":true}}}},"publishedAt":{"type":"string","format":"date-time","nullable":true}}}
}
```
