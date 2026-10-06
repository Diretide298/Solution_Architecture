# WS101 — Subscription Licensing AI Self Service board 4

**10 screens · 4 operations · 7 schemas · 3 permissions**

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
| `ADM-399` | Recommended Package Overview | B | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-400` | Commercial Model & Tier Selection | B | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-401` | Module Marketplace | B | 0 | 18 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-402` | AI Module & Package Recommendations | B | 0 | 14 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-403` | Module Detail & Commercial Treatment | B | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-404` | Module Dependency & Compatibility Manager | B | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-405` | Add-Ons, Capacity & Commercial Options | B | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-406` | Commercial Package Simulator | B | 0 | 20 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-407` | Package Review & Commercial Summary | B | 0 | 12 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-408` | Final Package Approval & Handoff | B–D | 0 | 0 | 6 | 0 | 0 | 3 | — | notStarted (—) |

## Thin screens in this batch

**ADM-399, ADM-400, ADM-401, ADM-402, ADM-403, ADM-404, ADM-405, ADM-406, ADM-407, ADM-408 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-399` Recommended Package Overview

**Present the AI-generated recommended package based on: Board 2 Customer Assessment VSI Operational requirements Commercial model Technical licensing profile Required modules Expected ticket/transaction volume Contract requirements**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · ticket #29316 (APP-CONSOLE-ADM-399) |
| Who uses it | ticvai staff holding `PLATFORM_PLAN_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/recommended-package-overview-adm-399` |

**What the spec says about it.** **Kept as TICVAI's operator-led view of the prospect journey (2 October 2026, CHG-SBO-015; BL-165):** ADM-399 to ADM-417 and SGN-011 to SGN-024 are one journey with two doors. A TICVAI sales operator runs it with or for a prospect on the Console; a prospect runs it alone on the sign-up (P17). The copies stay identical (`source.sameAs`), so the operator sees exactly what the prospect sees.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** TICVAI's view of the recommended package for a prospect (the Console twin of SGN-011).

**Fixed on main** (the package already carries these; draw what it says): ADM-399 to ADM-410 and ADM-414, ADM-415, ADM-417 repeat SGN-011 to SGN-024 by name and operation. (CHG-SBO-015); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `simulateCommercialPackage` (onLoad, The recommended package)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Back to Platform Dashboard*
- → `ADM-400` Commercial Model & Tier Selection: *Commercial Model & Tier Selection*
- → `ADM-401` Module Marketplace: *Module Marketplace*
- → `ADM-402` AI Module & Package Recommendations: *AI Module & Package Recommendations*
- → `ADM-403` Module Detail & Commercial Treatment: *Module Detail & Commercial Treatment*
- → `ADM-404` Module Dependency & Compatibility Manager: *Module Dependency & Compatibility Manager*
- → `ADM-405` Add-Ons, Capacity & Commercial Options: *Add-Ons, Capacity & Commercial Options*
- → `ADM-406` Commercial Package Simulator: *Commercial Package Simulator*
- → `ADM-407` Package Review & Commercial Summary: *Package Review & Commercial Summary*
- → `ADM-408` Final Package Approval & Handoff: *Final Package Approval & Handoff*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The recommended package overview list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the recommended package overview untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No recommended package overview yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the recommended package overview are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `SGN-011`: Same package object; the Console side may override with approval, the prospect side only accepts.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
package: Enterprise, per ticket + minimum guarantee
modules: 9
reason: 1.2 m visitors, 3 venues, F&B and access needed
```

#### Permissions

- `simulateCommercialPackage` → `PLATFORM_PLAN_MANAGE` (configure) · staff, guest, prospect

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- From onboarding data the system proposes a recommended commercial model and tier package (example: a museum recommended per-ticket plus minimum guarantee). *(client request · MoM 10 Sep 2026, 4.7 Package Builder & Module Marketplace · DI-823)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-399` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS156 Subscription Licensing AI Self Service Board 4.dc.html#adm-399`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 4
- Flow F210 *Subscription Licensing AI Self Service board 4: Recommended Package Overview*, step 1: Opens Recommended Package Overview → Present the AI-generated recommended package based on: Board 2 Customer Assessment VSI Operational requirements Commercial model Technical licensing profile Required modules Expected …
- Flow F210 *Subscription Licensing AI Self Service board 4: Recommended Package Overview*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F210 *Subscription Licensing AI Self Service board 4: Recommended Package Overview*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F210 *Subscription Licensing AI Self Service board 4: Recommended Package Overview*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F210 *Subscription Licensing AI Self Service board 4: Recommended Package Overview*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F210 *Subscription Licensing AI Self Service board 4: Recommended Package Overview*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F210 *Subscription Licensing AI Self Service board 4: Recommended Package Overview*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F210 *Subscription Licensing AI Self Service board 4: Recommended Package Overview*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F210 branch at step 1 (expected): when Nothing has been set up on Recommended Package Overview yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F210 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-399?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-002`, `ADM-400`, `ADM-401`, `ADM-402`, `ADM-403`, `ADM-404`, `ADM-405`, `ADM-406`, `ADM-407`, `ADM-408`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-400` Commercial Model & Tier Selection

**Allow TICVAI commercial users — or authorized self-service customers where applicable — to select the appropriate commercial charging model. This replaces the previous assumption that this screen is only a tier comparison.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · ticket #29330 (APP-CONSOLE-ADM-400) |
| Who uses it | ticvai staff holding `PLATFORM_PLAN_MANAGE`, `PLATFORM_TENANT_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/commercial-model-tier-selection-adm-400` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The commercial model and tier chosen for a customer, by TICVAI's commercial team (twin of SGN-012).

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

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
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listPlans` (onLoad, Tiers to choose from)

**Where the user goes next**

- → `ADM-399` Recommended Package Overview: *Back to Recommended Package Overview*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The commercial model tier list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the commercial model tier untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No commercial model tier yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the commercial model tier are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Can read but not change (holds PLATFORM_TENANT_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: PLATFORM_PLAN_MANAGE for simulateCommercialPackage. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/subscription.yaml#simulateCommercialPackage)*

#### Consistency with other screens

- Match `SGN-012`: Twin.

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

- `listPlans` → `PLATFORM_TENANT_VIEW` (read) · staff, prospect
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-400` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS156 Subscription Licensing AI Self Service Board 4.dc.html#adm-400`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 4
- Flow F210 *Subscription Licensing AI Self Service board 4: Recommended Package Overview*, step 2: Works in Commercial Model & Tier Selection → Allow TICVAI commercial users — or authorized self-service customers where applicable — to select the appropriate commercial charging model. This replaces the previous assumption that this screen is …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-400?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-399`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-401` Module Marketplace

**Allow the customer or TICVAI commercial team to select optional TICVAI modules.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · ticket #29317 (APP-CONSOLE-ADM-401) |
| Who uses it | ticvai staff holding `PLATFORM_PLAN_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Each module displays) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/module-marketplace-adm-401` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Optional modules for a customer, by TICVAI's commercial team (twin of SGN-013).

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The table's columns are the workshop pack's labels with no bound response field (0 of 9 labels bound). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every module marketplace** (data table)

| Shows | Format | Notes |
|---|---|---|
| Module name | text | not in the schema: `Module Name` |
| Description | text | not in the schema: `Description` |
| Key features | text | not in the schema: `Key Features` |
| Commercial status | text | not in the schema: `Commercial Status` |
| Included / optional | text | not in the schema: `Included / Optional` |
| Price or contract treatment | text | not in the schema: `Price or Contract Treatment` |
| Dependencies | text | not in the schema: `Dependencies` |
| Recommended / required | text | not in the schema: `Recommended / Required` |
| Trial availability | text | not in the schema: `Trial Availability` |

**The selected module marketplace** (detail panel): The pack groups this record's detail under its own headings: “Sales”, “Venue Operations”, “Customer”, “Commercial”, “Important”.

| Shows | Format | Notes |
|---|---|---|
| Module name | text | not in the schema: `Module Name` |
| Description | text | not in the schema: `Description` |
| Key features | text | not in the schema: `Key Features` |
| Commercial status | text | not in the schema: `Commercial Status` |
| Included / optional | text | not in the schema: `Included / Optional` |
| Price or contract treatment | text | not in the schema: `Price or Contract Treatment` |
| Dependencies | text | not in the schema: `Dependencies` |
| Recommended / required | text | not in the schema: `Recommended / Required` |
| Trial availability | text | not in the schema: `Trial Availability` |

**Data it reads**: `listModuleCatalogue` (onLoad, The marketplace)

**Where the user goes next**

- → `ADM-399` Recommended Package Overview: *Back to Recommended Package Overview*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The module marketplace list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the module marketplace untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No module marketplace yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the module marketplace are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `SGN-013`: Twin.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every module marketplace:
- Module Name: 74
  Description: 74
  Key Features: 19
  Commercial Status: 46
  Included / Optional: 74
  Price or Contract Treatment: AED 482,300.00
  Dependencies: 19
  Recommended / Required: 57
- Module Name: 19
  Description: 19
  Key Features: 233
  Commercial Status: 312
  Included / Optional: 19
  Price or Contract Treatment: AED 96,750.00
  Dependencies: 233
  Recommended / Required: 11
- Module Name: 233
  Description: 233
  Key Features: 57
  Commercial Status: 74
  Included / Optional: 233
  Price or Contract Treatment: AED 12,400.00
  Dependencies: 57
  Recommended / Required: 128
```

#### Permissions

- `listModuleCatalogue` → `PLATFORM_PLAN_MANAGE` (configure) · staff, guest, prospect

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Module marketplace lists optional add-ons (B2C, B2B, mobile app, virtual queue, CRM, seat management, etc.) with AI recommendations from stated needs (e.g. virtual queue if queue management was flagged). *(client request · MoM 10 Sep 2026, 4.7 Package Builder & Module Marketplace · DI-824)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-401` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS156 Subscription Licensing AI Self Service Board 4.dc.html#adm-401`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 4
- Flow F210 *Subscription Licensing AI Self Service board 4: Recommended Package Overview*, step 4: Works in Module Marketplace → Allow the customer or TICVAI commercial team to select optional TICVAI modules.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-401?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-399`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-402` AI Module & Package Recommendations

**Use AI to recommend the appropriate modules and package configuration based on the customer's business.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · ticket #29318 (APP-CONSOLE-ADM-402) |
| Who uses it | ticvai staff holding `PLATFORM_PLAN_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Each recommendation shows) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/ai-module-package-recommendations-adm-402` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** AI module recommendations for a customer (twin of SGN-014).

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The table's columns are the workshop pack's labels with no bound response field (0 of 7 labels bound). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every module package recommendations** (data table)

| Shows | Format | Notes |
|---|---|---|
| Additional monthly cost | text | not in the schema: `Additional Monthly Cost` |
| Annual cost | text | not in the schema: `Annual Cost` |
| Per ticket impact | text | not in the schema: `Per-Ticket Impact` |
| Included in contract | text | not in the schema: `Included in Contract` |
| Revenue/operational benefit | text | not in the schema: `Revenue/Operational Benefit` |
| Confidence | text | not in the schema: `Confidence` |
| Reason | text | not in the schema: `Reason` |

**The selected module package recommendations** (detail panel): The pack groups this record's detail under its own headings: “Add Virtual Queue”, “Seat Management”.

| Shows | Format | Notes |
|---|---|---|
| Additional monthly cost | text | not in the schema: `Additional Monthly Cost` |
| Annual cost | text | not in the schema: `Annual Cost` |
| Per ticket impact | text | not in the schema: `Per-Ticket Impact` |
| Included in contract | text | not in the schema: `Included in Contract` |
| Revenue/operational benefit | text | not in the schema: `Revenue/Operational Benefit` |
| Confidence | text | not in the schema: `Confidence` |
| Reason | text | not in the schema: `Reason` |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Money columns (Additional Monthly Cost, Annual Cost)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. Across tenants or regions figures in different currencies are never summed into one total; group by currency, or label the converted figure with its rate and time. *(source: ADR-0008; ADR-0011; DI-306)*

**Data it reads**: `listModuleCatalogue` (onLoad, Recommended modules)

**Where the user goes next**

- → `ADM-399` Recommended Package Overview: *Back to Recommended Package Overview*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The module package recommendations list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the module package recommendations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No module package recommendations yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the module package recommendations are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `SGN-014`: Twin.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every module package recommendations:
- Additional Monthly Cost: AED 12,400.00
  Annual Cost: AED 12,400.00
  Per-Ticket Impact: 46
  Included in Contract: 19
  Revenue/Operational Benefit: AED 482,300.00
  Confidence: 92%
  Reason: 57
- Additional Monthly Cost: AED 482,300.00
  Annual Cost: AED 482,300.00
  Per-Ticket Impact: 312
  Included in Contract: 233
  Revenue/Operational Benefit: AED 96,750.00
  Confidence: 78%
  Reason: 11
- Additional Monthly Cost: AED 96,750.00
  Annual Cost: AED 96,750.00
  Per-Ticket Impact: 74
  Included in Contract: 57
  Revenue/Operational Benefit: AED 12,400.00
  Confidence: 64%
  Reason: 128
```

#### Permissions

- `listModuleCatalogue` → `PLATFORM_PLAN_MANAGE` (configure) · staff, guest, prospect

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Module marketplace lists optional add-ons (B2C, B2B, mobile app, virtual queue, CRM, seat management, etc.) with AI recommendations from stated needs (e.g. virtual queue if queue management was flagged). *(client request · MoM 10 Sep 2026, 4.7 Package Builder & Module Marketplace · DI-824)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-402` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS156 Subscription Licensing AI Self Service Board 4.dc.html#adm-402`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 4
- Flow F210 *Subscription Licensing AI Self Service board 4: Recommended Package Overview*, step 6: Works in AI Module & Package Recommendations → Use AI to recommend the appropriate modules and package configuration based on the customer's business.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-402?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-399`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-403` Module Detail & Commercial Treatment

**Provide detailed information about an individual module before adding it to the package.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · ticket #29319 (APP-CONSOLE-ADM-403) |
| Who uses it | ticvai staff holding `PLATFORM_PLAN_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/module-detail-commercial-treatment-adm-403` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** One module's commercial treatment (twin of SGN-015).

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listModuleCatalogue` (onLoad, One module in detail)

**Where the user goes next**

- → `ADM-399` Recommended Package Overview: *Back to Recommended Package Overview*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The module detail commercial list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the module detail commercial untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No module detail commercial yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the module detail commercial are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `SGN-015`: Twin.

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

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-403` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS156 Subscription Licensing AI Self Service Board 4.dc.html#adm-403`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 4
- Flow F210 *Subscription Licensing AI Self Service board 4: Recommended Package Overview*, step 8: Works in Module Detail & Commercial Treatment → Provide detailed information about an individual module before adding it to the package.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-403?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-399`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-404` Module Dependency & Compatibility Manager

**Ensure that the package is technically valid before commercial approval.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · ticket #29320 (APP-CONSOLE-ADM-404) |
| Who uses it | ticvai staff holding `PLATFORM_PLAN_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/module-dependency-compatibility-manager-adm-404` |

**Known gaps.** **Module Dependency & Compatibility Manager declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The module catalogue's dependencies and compatibility, maintained by TICVAI (this is where setModuleListing belongs, not on the prospect's SGN-016).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listModuleCatalogue` (onLoad, What depends on what)

**Where the user goes next**

- → `ADM-399` Recommended Package Overview: *Back to Recommended Package Overview*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The module dependency compatibility list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the module dependency compatibility untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No module dependency compatibility yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the module dependency compatibility are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `SGN-016`: The prospect sees the validation result only.

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

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Module dependency check before allowing combinations - e.g. flag that the online/B2C module must be included before enabling virtual queue. *(client request · MoM 10 Sep 2026, 4.7 Package Builder & Module Marketplace · DI-825)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-404` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS156 Subscription Licensing AI Self Service Board 4.dc.html#adm-404`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 4
- Flow F210 *Subscription Licensing AI Self Service board 4: Recommended Package Overview*, step 10: Works in Module Dependency & Compatibility Manager → Ensure that the package is technically valid before commercial approval.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-404?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-399`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-405` Add-Ons, Capacity & Commercial Options

**Allow additional resources to be added without unnecessarily moving the customer to another tier. This remains a very important TICVAI commercial principle.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · ticket #29321 (APP-CONSOLE-ADM-405) |
| Who uses it | ticvai staff holding `PLATFORM_BILLING_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/add-ons-capacity-commercial-options-adm-405` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Add capacity packs to a customer's package without a tier change.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Add capacity pack (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-399` Recommended Package Overview: *Back to Recommended Package Overview*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The add-ons capacity commercial list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the add-ons capacity commercial untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No add-ons capacity commercial yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the add-ons capacity commercial are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `SGN-017`: Twin.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
pack: Extra 5 POS terminals
price: AED 1,500.00 / month
tierUnchanged: true
```

#### Permissions

- `addCapacityPack` → `PLATFORM_BILLING_MANAGE` (configure) · staff, prospect

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-405` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS156 Subscription Licensing AI Self Service Board 4.dc.html#adm-405`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 4
- Flow F210 *Subscription Licensing AI Self Service board 4: Recommended Package Overview*, step 12: Works in Add-Ons, Capacity & Commercial Options → Allow additional resources to be added without unnecessarily moving the customer to another tier. This remains a very important TICVAI commercial principle.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-405?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Add capacity pack, Cancel.
- [ ] Every transition is wired: `ADM-399`.
- [ ] Every gated control is gated: `PLATFORM_BILLING_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-406` Commercial Package Simulator

**Compare different ways of commercially packaging the same customer. This screen must consume the commercial models configured in Board 3.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · ticket #29322 (APP-CONSOLE-ADM-406) |
| Who uses it | ticvai staff holding `PLATFORM_PLAN_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/commercial-package-simulator-adm-406` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Compare ways of packaging the same customer: monthly equivalent, guarantee, variable exposure, overage, TICVAI revenue.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The table's columns are the workshop pack's labels with no bound response field (0 of 10 labels bound). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every commercial package simulator** (data table)

| Shows | Format | Notes |
|---|---|---|
| Monthly equivalent | text | not in the schema: `Monthly Equivalent` |
| Annual cost | text | not in the schema: `Annual Cost` |
| Minimum guarantee | text | not in the schema: `Minimum Guarantee` |
| Variable exposure | text | not in the schema: `Variable Exposure` |
| Included modules | text | not in the schema: `Included Modules` |
| Technical capacity | text | not in the schema: `Technical Capacity` |
| Expected overage | text | not in the schema: `Expected Overage` |
| Customer saving | text | not in the schema: `Customer Saving` |
| TICVAI revenue | text | not in the schema: `TICVAI Revenue` |
| Contract predictability | text | not in the schema: `Contract Predictability` |

**The selected commercial package simulator** (detail panel): The pack groups this record's detail under its own headings: “Expected”, “AED 240,000”, “AED 15,000/month”, “Variable”, “AED 220,500”.

| Shows | Format | Notes |
|---|---|---|
| Monthly equivalent | text | not in the schema: `Monthly Equivalent` |
| Annual cost | text | not in the schema: `Annual Cost` |
| Minimum guarantee | text | not in the schema: `Minimum Guarantee` |
| Variable exposure | text | not in the schema: `Variable Exposure` |
| Included modules | text | not in the schema: `Included Modules` |
| Technical capacity | text | not in the schema: `Technical Capacity` |
| Expected overage | text | not in the schema: `Expected Overage` |
| Customer saving | text | not in the schema: `Customer Saving` |
| TICVAI revenue | text | not in the schema: `TICVAI Revenue` |
| Contract predictability | text | not in the schema: `Contract Predictability` |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Money columns (Annual Cost, TICVAI Revenue, Variable Exposure)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. Across tenants or regions figures in different currencies are never summed into one total; group by currency, or label the converted figure with its rate and time. *(source: ADR-0008; ADR-0011; DI-306)*

**Where the user goes next**

- → `ADM-399` Recommended Package Overview: *Back to Recommended Package Overview*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The commercial package simulator list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the commercial package simulator untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No commercial package simulator yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the commercial package simulator are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
scenarios:
- name: Growth tier
  monthlyEquivalent: AED 18,000.00
  minimumGuarantee: AED 0.00
  expectedOverage: AED 1,200.00
- name: Per ticket + guarantee
  monthlyEquivalent: AED 16,400.00
  minimumGuarantee: AED 12,000.00
  variableExposure: AED 6,500.00
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-406` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS156 Subscription Licensing AI Self Service Board 4.dc.html#adm-406`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 4
- Flow F210 *Subscription Licensing AI Self Service board 4: Recommended Package Overview*, step 14: Works in Commercial Package Simulator → Compare different ways of commercially packaging the same customer. This screen must consume the commercial models configured in Board 3.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-406?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-399`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-407` Package Review & Commercial Summary

**Provide the complete package before customer acceptance or internal approval.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · ticket #29323 (APP-CONSOLE-ADM-407) |
| Who uses it | ticvai staff holding `PLATFORM_PLAN_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/package-review-commercial-summary-adm-407` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The complete package with every exception (discount, special rate, free period, capacity override) before approval.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The table's columns are the workshop pack's labels with no bound response field (0 of 6 labels bound). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every package review commercial** (data table)

| Shows | Format | Notes |
|---|---|---|
| Discount | text | not in the schema: `Discount` |
| Special rate | text | not in the schema: `Special Rate` |
| Included module | text | not in the schema: `Included Module` |
| Free period | text | not in the schema: `Free Period` |
| Capacity override | text | not in the schema: `Capacity Override` |
| Contract exception | text | not in the schema: `Contract Exception` |

**The selected package review commercial** (detail panel): The pack groups this record's detail under its own headings: “VSI”, “Rate”, “Contract”, “Included Technical Capacity”, “Modules”, “Expected Tickets”.

| Shows | Format | Notes |
|---|---|---|
| Discount | text | not in the schema: `Discount` |
| Special rate | text | not in the schema: `Special Rate` |
| Included module | text | not in the schema: `Included Module` |
| Free period | text | not in the schema: `Free Period` |
| Capacity override | text | not in the schema: `Capacity Override` |
| Contract exception | text | not in the schema: `Contract Exception` |

**Data it reads**: `simulateCommercialPackage` (onLoad, Review the summary)

**Where the user goes next**

- → `ADM-399` Recommended Package Overview: *Back to Recommended Package Overview*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The package review commercial list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the package review commercial untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No package review commercial yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the package review commercial are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every package review commercial:
- Discount: 12
  Special Rate: 94%
  Included Module: 11
  Free Period: 74
  Capacity Override: 46
  Contract Exception: 1
- Discount: 3
  Special Rate: 87%
  Included Module: 128
  Free Period: 19
  Capacity Override: 312
  Contract Exception: 3
- Discount: 0
  Special Rate: 71%
  Included Module: 46
  Free Period: 233
  Capacity Override: 74
  Contract Exception: 2
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-407` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS156 Subscription Licensing AI Self Service Board 4.dc.html#adm-407`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 4
- Flow F210 *Subscription Licensing AI Self Service board 4: Recommended Package Overview*, step 16: Works in Package Review & Commercial Summary → Provide the complete package before customer acceptance or internal approval.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-407?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-399`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-408` Final Package Approval & Handoff

**Govern final approval of the commercial package and send the approved configuration into purchase/contract activation.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai; in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/final-package-approval-handoff-adm-408` |

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: Board 4 — Required Package Data Model. Each needs an operation, or needs removing from the screen; this is … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Final internal approval of a package and handoff to activation.

**Fixed on main** (the package already carries these; draw what it says): The only operation is createPartnerQuote (PARTNER_MANAGE, a tenant's B2B quote). (CHG-WIR-021); A button labelled "Board 4 — Required Package Data Model". (CHG-SBO-015).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `ADM-399` Recommended Package Overview: *Back to Recommended Package Overview*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The final package approval list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the final package approval untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No final package approval yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the final package approval are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
package: Marina Leisure Group 2027
approvals:
  commercial: approved
  finance: pending
```

#### Permissions

**A refused user sees:** Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access.

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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-408` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS156 Subscription Licensing AI Self Service Board 4.dc.html#adm-408`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 4
- Flow F210 *Subscription Licensing AI Self Service board 4: Recommended Package Overview*, step 18: Works in Final Package Approval & Handoff → Govern final approval of the commercial package and send the approved configuration into purchase/contract activation.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-408?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-399`.
- [ ] Sign-in is asked only where the spec asks for it.
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
"addCapacityPack": {"method":"POST","path":"/capacity-packs","contract":"subscription","summary":"Buy headroom without changing tier","permission":"PLATFORM_BILLING_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"platform","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CapacityPack","responds":"CapacityPack"},
"listModuleCatalogue": {"method":"GET","path":"/module-catalogue","contract":"subscription","summary":"Modules, their dependencies and their commercial treatment","permission":"PLATFORM_PLAN_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"platform","parameters":[],"requestBody":null,"responds":"ModuleListing"},
"listPlans": {"method":"GET","path":"/plans","contract":"subscription","summary":"List subscription plans","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"offeredToTenantId","in":"query","required":false},{"name":"packageKind","in":"query","required":false}],"requestBody":null,"responds":"Plan"},
"simulateCommercialPackage": {"method":"POST","path":"/package-simulations","contract":"subscription","summary":"What this package would cost, and what it would provision","permission":"PLATFORM_PLAN_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"platform","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PackageSimulationRequest","responds":"PackageSimulation"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"CapacityPack": {"type":"object","x-ticvai-persistence":"subscription.capacity_pack","description":"Board 3.8. **A good season should not require renegotiating a contract in August.**\n","required":["tenantId","unit","quantity"],"properties":{"id":{"type":"string","format":"uuid"},"tenantId":{"type":"string","format":"uuid"},"unit":{"type":"string"},"quantity":{"type":"integer"},"price":{"x-ticvai-column":"list_price","$ref":"../shared/common.yaml#/components/schemas/Money"},"validFrom":{"type":"string","format":"date"},"validTo":{"type":"string","format":"date","nullable":true},"temporary":{"type":"boolean","default":true},"approvedBy":{"type":"string","format":"uuid","nullable":true},"invoiceId":{"type":"string","format":"uuid","nullable":true}}},
"CreatePlanRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["code","name","cellTier","licensedModules","limits","basePrice"],"properties":{"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":1000},"cellTier":{"$ref":"#/components/schemas/CellTier"},"licensedModules":{"type":"array","minItems":1,"description":"**A closed set as of 24 August.** `moduleKey` was a free string, so nothing could join a licence to a screen — **a tenant without an F&B licence was still served every F&B screen**, because no screen said which module it belonged to in a form the licence could match.\n**The key is the join.** `screen.requiresModule` names one of these, and navigation is built from the intersection of what a tenant licensed and what their role permits.\n","items":{"$ref":"#/components/schemas/subscription::ModuleKey"}},"limits":{"type":"array","items":{"$ref":"#/components/schemas/EntitlementLimit"}},"basePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"billingPeriod":{"type":"string","enum":["monthly","quarterly","annual"]},"includesBrandedApp":{"type":"boolean","description":"Branded native publishing carries per-tenant operational cost and is priced, not absorbed.\n"},"includedAiTokens":{"type":"integer","nullable":true,"description":"AI tokens the package includes per billing period. Usage beyond it is a `metered` invoice line at the AI module's price (decided 29 September)."},"requestLimits":{"$ref":"#/components/schemas/PlanRequestLimits"},"packageKind":{"type":"string","enum":["standard","custom"],"default":"standard","description":"**Three standard packages, and custom ones allowed** (decided 29 September, Chinmay)."},"offeredToTenantId":{"type":"string","format":"uuid","nullable":true,"description":"**Private to one tenant** (decided 29 September, Chinmay): a custom package offered only to this tenant; `listPlans` shows it to no other tenant and `setSubscription` refuses it for any other (422 `plan-not-offered`). Null for a package any tenant may buy. Custom packages only."}}},
"ModuleListing": {"type":"object","x-ticvai-persistence":"subscription.module_listing","description":"Board 4.6. **A marketplace without a dependency graph sells combinations that cannot be provisioned.**\n**TICVAI configures each module's price here, and tenants are billed per module (decided 29 September, Chinmay).** A usage-priced module (the AI module's tokens) has `pricingBasis` `metered`: `price` is then per `meteredUnitSize` units of `meteredMetric`, and the invoice carries it as a `metered` line.\n","required":["moduleCode"],"properties":{"moduleCode":{"type":"string","description":"**Values are `ModuleKey`s** (4 October 2026, CHG-FXC-010; ADM-424): the vocabulary of\n`white-label.ModuleEnablement.moduleKey`, so a dependency is checked against what `setModuleEnablement` switches."},"name":{"type":"string"},"description":{"type":"string","nullable":true},"category":{"type":"string","nullable":true},"requiresModules":{"type":"array","description":"**Values are `ModuleKey`s** (4 October 2026, CHG-FXC-010; ADM-424): the vocabulary of\n`white-label.ModuleEnablement.moduleKey`, so a dependency is checked against what `setModuleEnablement` switches.","items":{"type":"string"}},"incompatibleWithModules":{"type":"array","description":"**Values are `ModuleKey`s** (4 October 2026, CHG-FXC-010; ADM-424): the vocabulary of\n`white-label.ModuleEnablement.moduleKey`, so a dependency is checked against what `setModuleEnablement` switches.","items":{"type":"string"}},"includedInTiers":{"type":"array","items":{"type":"string"}},"price":{"x-ticvai-column":"list_price","$ref":"../shared/common.yaml#/components/schemas/Money"},"pricingBasis":{"type":"string","enum":["included","flatFee","perVenue","perUnit","revenueShare","metered"]},"meteredMetric":{"allOf":[{"$ref":"#/components/schemas/UsageMetric"}],"nullable":true,"description":"For `metered`, what is counted (`aiTokens` for the AI module). Null otherwise."},"meteredUnitSize":{"type":"integer","minimum":1,"nullable":true,"description":"For `metered`, how many units `price` buys (e.g. 1000 tokens). Null otherwise."},"provisioningMinutes":{"type":"integer","nullable":true},"requiresProfessionalServices":{"type":"boolean","default":false},"status":{"type":"string","enum":["available","beta","deprecated","withdrawn"]}}},
"PackageSimulation": {"type":"object","description":"Boards 3.9 and 4.8. **Refused at quote time rather than at go-live.**","properties":{"lines":{"type":"array","items":{"type":"object","properties":{"kind":{"type":"string","enum":["baseTier","module","addOn","capacityPack","overage","professionalServices","discount"]},"label":{"type":"string"},"quantity":{"type":"number","nullable":true},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"recurringTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"oneOffTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"contractTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"minimumGuarantee":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"findings":{"type":"array","items":{"type":"object","properties":{"severity":{"type":"string","enum":["blocking","warning","advisory"]},"code":{"type":"string"},"message":{"type":"string"}}}},"provisionable":{"type":"boolean"}}},
"PackageSimulationRequest": {"type":"object","required":["tierCode"],"properties":{"tierCode":{"type":"string"},"licensingModelId":{"type":"string","format":"uuid","nullable":true},"moduleCodes":{"type":"array","items":{"type":"string"}},"venueCount":{"type":"integer","default":1},"projectedVolumes":{"type":"object","additionalProperties":{"type":"integer"}},"contractMonths":{"type":"integer","default":12},"billingCycle":{"type":"string","nullable":true},"currency":{"type":"string","nullable":true}}},
"Plan": {"x-ticvai-persistence":"subscription.plan + subscription.plan_module + subscription.plan_limit","description":"**A plan's modules and limits are rows, keyed on `plan_id`.** `licensedModules` and `limits` are required on every plan, and `subscription.plan` alone had no column for either — so the licence position, the downgrade check and every module gate had nothing to read. `plan_module` holds one row per licensed `ModuleKey`; `plan_limit` one row per `EntitlementLimit`. Both belong to the plan version the row is, so a subscriber on an earlier version keeps the modules and limits they were sold.","allOf":[{"$ref":"#/components/schemas/CreatePlanRequest"},{"type":"object","required":["id","version","isActive","subscriberCount"],"properties":{"id":{"type":"string","format":"uuid"},"version":{"type":"string","description":"Existing subscribers stay on the version they were sold. A price change never applies retroactively.\n"},"isActive":{"type":"boolean"},"subscriberCount":{"type":"integer"},"publishedAt":{"type":"string","format":"date-time"}}}]},
"UsageMetric": {"type":"string","enum":["venues","workstations","activeUsers","devices","brandedApps","aiTokens","apiCalls","storageGb","transactions","guestProfiles"]}
}
```
