# WS77 — Digital Asset Management DAM board 4

**10 screens · 5 operations · 6 schemas · 2 permissions**

Platform P13 Venue CMS · ships as **venue-management** ·
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

- **Every control that can be refused must be gated.** 2 permissions apply here:
  `ASSET_LIBRARY_MANAGE, ASSET_LIBRARY_VIEW`. A control nobody can use must say so,
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
| `CMS-091` | Asset Distribution & Delivery Command Center | B | 0 | 48 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `CMS-092` | Asset Usage & Distribution Map | B | 0 | 16 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `CMS-093` | Channel & Distribution Configuration | B | 13 | 0 | 6 | 1 | 1 | 0 | — | notStarted (—) |
| `CMS-094` | Secure Delivery URL, CDN & Rendition Delivery | B | 0 | 0 | 6 | 1 | 0 | 0 | — | notStarted (—) |
| `CMS-095` | Asset Replacement & Propagation Management | B | 0 | 0 | 6 | 1 | 1 | 0 | — | notStarted (—) |
| `CMS-096` | Fallback, Expiry & Distribution Continuity | B | 1 | 0 | 6 | 3 | 1 | 0 | — | notStarted (—) |
| `CMS-097` | DAM API & Integration Hub | B | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `CMS-098` | Delivery Monitoring & Integration Health | B | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `CMS-099` | Asset Usage & Performance Analytics | B | 0 | 6 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `CMS-100` | Distribution Intelligence, AI Insights & Optimization | B | 1 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**CMS-092, CMS-097, CMS-100 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `CMS-091` Asset Distribution & Delivery Command Center

**Provide a centralized operational overview of asset distribution across TICVAI and connected external channels.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | Block B · task APP-CMS-CMS-091 |
| Who uses it | venue staff holding `ASSET_LIBRARY_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/media-library/asset-distribution-delivery-command-center-cms-091` |

**Known gaps.** **The pack names 6 actions on this screen and the screen declares 0 operations.** Unserved: Distribution Map, Channel Management, Delivery Monitor, Replacement Center, API & Integration, Analytics. … **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Distribution of assets across channels: active references, delivery failures, assets needing replacement.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The table's columns are the workshop pack's labels with no bound response field (0 of 24 labels bound). (CHG-SGU-024)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SGU-023).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Asset | upload, or pick from the media library | — | — | `getMediaDistribution` ?assetId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every asset distribution delivery** (data table)

| Shows | Format | Notes |
|---|---|---|
| Assets in active use | text | not in the schema: `Assets in Active Use` |
| Active asset references | text | not in the schema: `Active Asset References` |
| Delivery requests | text | not in the schema: `Delivery Requests` |
| Active channels | text | not in the schema: `Active Channels` |
| Cdn/data delivery | text | not in the schema: `CDN/Data Delivery` |
| Failed deliveries | text | not in the schema: `Failed Deliveries` |
| Assets requiring replacement | text | not in the schema: `Assets Requiring Replacement` |
| Expiring assets in active use | text | not in the schema: `Expiring Assets in Active Use` |
| API requests | text | not in the schema: `API Requests` |
| Delivery availability % | text | not in the schema: `Delivery Availability %` |
| B2 c website | text | not in the schema: `B2C Website` |
| Mobile app | text | not in the schema: `Mobile App` |
| POS | text | not in the schema: `POS` |
| Kiosk | text | not in the schema: `Kiosk` |
| Ticket media | text | not in the schema: `Ticket Media` |
| Marketing | text | not in the schema: `Marketing` |
| Digital signage | text | not in the schema: `Digital Signage` |
| Partner/api | text | not in the schema: `Partner/API` |
| Delivery health | text | not in the schema: `Delivery Health` |
| 🟢 healthy | text | not in the schema: `🟢 Healthy` |
| 🟡 degraded | text | not in the schema: `🟡 Degraded` |
| 🔴 failed | text | not in the schema: `🔴 Failed` |
| ⚪ inactive | text | not in the schema: `⚪ Inactive` |
| Critical alerts | text | not in the schema: `Critical Alerts` |

**The selected asset distribution delivery** (detail panel): The pack groups this record's detail under its own headings: “Digital Asset Management”, “Active Channels 28”.

| Shows | Format | Notes |
|---|---|---|
| Assets in active use | text | not in the schema: `Assets in Active Use` |
| Active asset references | text | not in the schema: `Active Asset References` |
| Delivery requests | text | not in the schema: `Delivery Requests` |
| Active channels | text | not in the schema: `Active Channels` |
| Cdn/data delivery | text | not in the schema: `CDN/Data Delivery` |
| Failed deliveries | text | not in the schema: `Failed Deliveries` |
| Assets requiring replacement | text | not in the schema: `Assets Requiring Replacement` |
| Expiring assets in active use | text | not in the schema: `Expiring Assets in Active Use` |
| API requests | text | not in the schema: `API Requests` |
| Delivery availability % | text | not in the schema: `Delivery Availability %` |
| B2 c website | text | not in the schema: `B2C Website` |
| Mobile app | text | not in the schema: `Mobile App` |
| POS | text | not in the schema: `POS` |
| Kiosk | text | not in the schema: `Kiosk` |
| Ticket media | text | not in the schema: `Ticket Media` |
| Marketing | text | not in the schema: `Marketing` |
| Digital signage | text | not in the schema: `Digital Signage` |
| Partner/api | text | not in the schema: `Partner/API` |
| Delivery health | text | not in the schema: `Delivery Health` |
| 🟢 healthy | text | not in the schema: `🟢 Healthy` |
| 🟡 degraded | text | not in the schema: `🟡 Degraded` |
| 🔴 failed | text | not in the schema: `🔴 Failed` |
| ⚪ inactive | text | not in the schema: `⚪ Inactive` |
| Critical alerts | text | not in the schema: `Critical Alerts` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Distribution Map (primary button) | navigation or local | — | — | — | — |
| Channel Management (secondary button) | navigation or local | — | — | — | — |
| Delivery Monitor (secondary button) | navigation or local | — | — | — | — |
| Replacement Center (secondary button) | navigation or local | — | — | — | — |
| API & Integration (secondary button) | navigation or local | — | — | — | — |
| Analytics (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getMediaDistribution` (onLoad, Delivery across channels)

**Where the user goes next**

- → `CMS-001` Tenant Workspace: *Back to Tenant Workspace*
- → `CMS-092` Asset Usage & Distribution Map: *Asset Usage & Distribution Map*
- → `CMS-093` Channel & Distribution Configuration: *Channel & Distribution Configuration*
- → `CMS-094` Secure Delivery URL, CDN & Rendition Delivery: *Secure Delivery URL, CDN & Rendition Delivery*; carries `assetId`
- → `CMS-095` Asset Replacement & Propagation Management: *Asset Replacement & Propagation Management*
- → `CMS-096` Fallback, Expiry & Distribution Continuity: *Fallback, Expiry & Distribution Continuity*
- → `CMS-097` DAM API & Integration Hub: *DAM API & Integration Hub*
- → `CMS-098` Delivery Monitoring & Integration Health: *Delivery Monitoring & Integration Health*
- → `CMS-099` Asset Usage & Performance Analytics: *Asset Usage & Performance Analytics*
- → `CMS-100` Distribution Intelligence, AI Insights & Optimization: *Distribution Intelligence, AI Insights & Optimization*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The asset distribution delivery list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the asset distribution delivery untouched. |
| Empty, first run (`?state=emptyFirstRun`) | Nothing here yet for Asset Distribution & Delivery Command Center. This screen only reads, so it offers no create action and says where the records come from. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the asset distribution delivery are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every asset distribution delivery:
- Assets in Active Use: 19
  Active Asset References: APR-2026-004812
  Delivery Requests: 128
  Active Channels: 11
  CDN/Data Delivery: 46
  Failed Deliveries: 5
  Assets Requiring Replacement: 19
  Expiring Assets in Active Use: 233
- Assets in Active Use: 233
  Active Asset References: APR-2026-004797
  Delivery Requests: 42
  Active Channels: 128
  CDN/Data Delivery: 312
  Failed Deliveries: 1
  Assets Requiring Replacement: 233
  Expiring Assets in Active Use: 57
- Assets in Active Use: 57
  Active Asset References: APR-2026-004755
  Delivery Requests: 7
  Active Channels: 46
  CDN/Data Delivery: 74
  Failed Deliveries: 3
  Assets Requiring Replacement: 57
  Expiring Assets in Active Use: 11
```

#### Permissions

- `getMediaDistribution` → `ASSET_LIBRARY_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Distribution board shows where and when each asset is used (e.g. a hero banner across every sales channel); channel configuration defines which rendition each channel consumes. *(client request · MoM 11 Sep 2026, 4.4 Asset Distribution, Delivery & Integration · DI-858)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-091` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS47 Digital Asset Management DAM Board 4.dc.html#cms-091`
- Workshop pack: Digital Asset Management DAM.pdf board 4
- Flow F186 *Digital Asset Management DAM board 4: Asset Distribution & Delivery Command …*, step 1: Opens Asset Distribution & Delivery Command Center → Provide a centralized operational overview of asset distribution across TICVAI and connected external channels.
- Flow F186 *Digital Asset Management DAM board 4: Asset Distribution & Delivery Command …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F186 *Digital Asset Management DAM board 4: Asset Distribution & Delivery Command …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F186 *Digital Asset Management DAM board 4: Asset Distribution & Delivery Command …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F186 *Digital Asset Management DAM board 4: Asset Distribution & Delivery Command …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F186 *Digital Asset Management DAM board 4: Asset Distribution & Delivery Command …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F186 *Digital Asset Management DAM board 4: Asset Distribution & Delivery Command …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F186 *Digital Asset Management DAM board 4: Asset Distribution & Delivery Command …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F186 branch at step 1 (expected): when Nothing has been set up on Asset Distribution & Delivery Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F186 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (48 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-091?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Distribution Map, Channel Management, Delivery Monitor, Replacement Center, API & Integration, Analytics.
- [ ] Every transition is wired: `CMS-001`, `CMS-092`, `CMS-093`, `CMS-094`, `CMS-095`, `CMS-096`, `CMS-097`, `CMS-098`, `CMS-099`, `CMS-100`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-092` Asset Usage & Distribution Map

**Show exactly where a digital asset is currently being used. This is one of the most important screens in the DAM.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | Block B · task APP-CMS-CMS-092 |
| Who uses it | venue staff holding `ASSET_LIBRARY_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/media-library/asset-usage-distribution-map-cms-092` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Where one asset is used now (web, app, kiosk, campaigns, signage), with counts per channel and links.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The table's columns are the workshop pack's labels with no bound response field (0 of 8 labels bound). (CHG-SGU-024)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SGU-023).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Asset | upload, or pick from the media library | — | — | `getMediaDistribution` ?assetId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every asset usage distribution** (data table)

| Shows | Format | Notes |
|---|---|---|
| TICVAI DAM asset | text | not in the schema: `TICVAI DAM Asset` |
| ↓ | text | not in the schema: `↓` |
| B2 c website — 5 | text | not in the schema: `B2C Website — 5` |
| Mobile app — 4 | text | not in the schema: `Mobile App — 4` |
| Kiosk — 3 | text | not in the schema: `Kiosk — 3` |
| Ticket media — 2 | text | not in the schema: `Ticket Media — 2` |
| Marketing campaign — 3 | text | not in the schema: `Marketing Campaign — 3` |
| Digital signage — 1 | text | not in the schema: `Digital Signage — 1` |

**The selected asset usage distribution** (detail panel): The pack groups this record's detail under its own headings: “Dubai Park Hero”, “Usage Table”, “Reference Type”, “Follow Current Version”, “Critical Requirement”.

| Shows | Format | Notes |
|---|---|---|
| TICVAI DAM asset | text | not in the schema: `TICVAI DAM Asset` |
| ↓ | text | not in the schema: `↓` |
| B2 c website — 5 | text | not in the schema: `B2C Website — 5` |
| Mobile app — 4 | text | not in the schema: `Mobile App — 4` |
| Kiosk — 3 | text | not in the schema: `Kiosk — 3` |
| Ticket media — 2 | text | not in the schema: `Ticket Media — 2` |
| Marketing campaign — 3 | text | not in the schema: `Marketing Campaign — 3` |
| Digital signage — 1 | text | not in the schema: `Digital Signage — 1` |

**Data it reads**: `getMediaDistribution` (onLoad, Where each asset appears)

**Where the user goes next**

- → `CMS-091` Asset Distribution & Delivery Command Center: *Back to Asset Distribution & Delivery Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The asset usage distribution list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the asset usage distribution untouched. |
| Empty, first run (`?state=emptyFirstRun`) | Nothing here yet for Asset Usage & Distribution Map. This screen only reads, so it offers no create action and says where the records come from. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the asset usage distribution are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every asset usage distribution:
- TICVAI DAM Asset: 128
  B2C Website — 5: 11
  Mobile App — 4: 57
  Kiosk — 3: 46
  Ticket Media — 2: 128
  Marketing Campaign — 3: 57
  Digital Signage — 1: 42 min
- TICVAI DAM Asset: 46
  B2C Website — 5: 128
  Mobile App — 4: 11
  Kiosk — 3: 312
  Ticket Media — 2: 46
  Marketing Campaign — 3: 11
  Digital Signage — 1: 1.8 s
- TICVAI DAM Asset: 312
  B2C Website — 5: 46
  Mobile App — 4: 128
  Kiosk — 3: 74
  Ticket Media — 2: 312
  Marketing Campaign — 3: 128
  Digital Signage — 1: 3 h 20 min
```

#### Permissions

- `getMediaDistribution` → `ASSET_LIBRARY_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Distribution board shows where and when each asset is used (e.g. a hero banner across every sales channel); channel configuration defines which rendition each channel consumes. *(client request · MoM 11 Sep 2026, 4.4 Asset Distribution, Delivery & Integration · DI-858)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-092` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS47 Digital Asset Management DAM Board 4.dc.html#cms-092`
- Workshop pack: Digital Asset Management DAM.pdf board 4
- Flow F186 *Digital Asset Management DAM board 4: Asset Distribution & Delivery Command …*, step 2: Works in Asset Usage & Distribution Map → Show exactly where a digital asset is currently being used. This is one of the most important screens in the DAM.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-092?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `CMS-091`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-093` Channel & Distribution Configuration

**Configure how DAM content can be consumed by different TICVAI modules and external channels.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | Block B · task APP-CMS-CMS-093 |
| Who uses it | venue staff holding `ASSET_LIBRARY_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/media-library/channel-distribution-configuration-cms-093` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** How each channel may consume assets: types, categories, approval and rights required, renditions, caching.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Channel name | select field | — | — | — | — | — | — |
| channel type | select field | — | — | — | — | — | — |
| tenant | select field | — | — | — | — | — | — |
| venue scope | select field | — | — | — | — | — | — |
| allowed asset types | select field | — | — | — | — | — | — |
| allowed categories | select field | — | — | — | — | — | — |
| required approval | select field | — | — | — | — | — | — |
| required rights | select field | — | — | — | — | — | — |
| preferred rendition | select field | — | — | — | — | — | — |
| fallback rendition | select field | — | — | — | — | — | — |
| delivery method | select field | — | — | — | — | — | — |
| caching policy | select field | — | — | — | — | — | — |
| authentication requirement | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `CMS-091` Asset Distribution & Delivery Command Center: *Back to Asset Distribution & Delivery Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The channel distribution configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the channel distribution untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No channel distribution configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
form example:
  Channel name: 19
  channel type: 233
  venue scope: AquaCove Abu Dhabi
  allowed asset types: 11
  allowed categories: 11
  required approval: 11
  required rights: 57
  preferred rendition: 74
  fallback rendition: 74
  delivery method: 46
  caching policy: 46
  authentication requirement: 57
```

#### Permissions

- `setMediaDistributionChannels` → `ASSET_LIBRARY_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 23.1.13 | System shall distribute approved assets to websites, mobile apps, kiosks, CRM campaigns, and digital channels. | Digital Asset Management | CONTRACTED | `setMediaDistributionChannels` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Distribution board shows where and when each asset is used (e.g. a hero banner across every sales channel); channel configuration defines which rendition each channel consumes. *(client request · MoM 11 Sep 2026, 4.4 Asset Distribution, Delivery & Integration · DI-858)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-093` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS47 Digital Asset Management DAM Board 4.dc.html#cms-093`
- Workshop pack: Digital Asset Management DAM.pdf board 4
- Flow F186 *Digital Asset Management DAM board 4: Asset Distribution & Delivery Command …*, step 4: Works in Channel & Distribution Configuration → Configure how DAM content can be consumed by different TICVAI modules and external channels.

#### Acceptance for the design

- [ ] Every input above is drawn (13), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-093?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `CMS-091`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-094` Secure Delivery URL, CDN & Rendition Delivery

**Provide optimized and controlled delivery of DAM assets without exposing private storage.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | Block B · task APP-CMS-CMS-094 |
| Who uses it | venue staff holding `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `assetId` (navigation) |
| Route | `/media-library/secure-delivery-url-cdn-rendition-delivery-cms-094` |

**Known gaps.** **The pack names 4 actions on this screen and the screen declares 0 operations.** Unserved: tokenized access, configurable expiry, cache policy, revocation where applicable. Each needs an operation … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Tokenised delivery URLs with expiry and cache policy; private storage never exposed.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** ↓. Each needs attaching to the control it gates, or the screen needs the control.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| tokenized access (primary button) | navigation or local | — | — | — | — |
| configurable expiry (secondary button) | navigation or local | — | — | — | — |
| cache policy (secondary button) | navigation or local | — | — | — | — |
| revocation where applicable (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `CMS-091` Asset Distribution & Delivery Command Center: *Back to Asset Distribution & Delivery Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The secure delivery url list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the secure delivery url untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No secure delivery url yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the secure delivery url are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds ASSET_LIBRARY_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: ASSET_LIBRARY_MANAGE for setMediaDistributionChannels. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/assets.yaml#setMediaDistributionChannels)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listMediaRenditions (MediaRendition):
- width: 12
  height: 12
  sizeBytes: 12
  status: active
- width: 3
  height: 3
  sizeBytes: 3
  status: pending
```

#### Permissions

- `setMediaDistributionChannels` → `ASSET_LIBRARY_MANAGE` (configure) · staff
- `listMediaRenditions` → `ASSET_LIBRARY_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 23.1.13 | System shall distribute approved assets to websites, mobile apps, kiosks, CRM campaigns, and digital channels. | Digital Asset Management | CONTRACTED | `setMediaDistributionChannels` |

#### Client meeting inputs

None names this screen.

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-094` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS47 Digital Asset Management DAM Board 4.dc.html#cms-094`
- Workshop pack: Digital Asset Management DAM.pdf board 4
- Flow F186 *Digital Asset Management DAM board 4: Asset Distribution & Delivery Command …*, step 6: Works in Secure Delivery URL, CDN & Rendition Delivery → Provide optimized and controlled delivery of DAM assets without exposing private storage.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-094?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: tokenized access, configurable expiry, cache policy, revocation where applicable.
- [ ] Every transition is wired: `CMS-091`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-095` Asset Replacement & Propagation Management

**Safely manage replacement of assets that are outdated, expired, incorrect, rebranded, or otherwise no longer suitable.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | Block B · task APP-CMS-CMS-095 |
| Who uses it | venue staff holding `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `mediaId` (navigation) |
| Route | `/media-library/asset-replacement-propagation-management-cms-095` |

**Known gaps.** **The pack names 5 actions on this screen and the screen declares 0 operations.** Unserved: Replace Everywhere Eligible, Replace Selected Uses, Schedule Replacement, Keep Existing Version, Create … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Replace an outdated asset everywhere eligible, in selected uses, or on a schedule, with fallback.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SGU-023).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Asset | upload, or pick from the media library | — | — | `getMediaDistribution` ?assetId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Replace Everywhere Eligible (primary button) | navigation or local | — | — | — | — |
| Replace Selected Uses (secondary button) | navigation or local | — | — | — | — |
| Schedule Replacement (secondary button) | navigation or local | — | — | — | — |
| Keep Existing Version (secondary button) | navigation or local | — | — | — | — |
| Create Fallback (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getMediaDistribution` (onLoad, Everywhere it would propagate to)

**Where the user goes next**

- → `CMS-091` Asset Distribution & Delivery Command Center: *Back to Asset Distribution & Delivery Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The asset replacement propagation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the asset replacement propagation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | Nothing here yet for Asset Replacement & Propagation Management. This screen only reads, so it offers no create action and says where the records come from. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the asset replacement propagation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The upload cannot be used: it is a different kind — an image cannot replace a document (`kindMismatch`) — or the transfer never finished … (UploadRefusedProblem) |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds ASSET_LIBRARY_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: ASSET_LIBRARY_MANAGE for replaceMediaAsset. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/assets.yaml#replaceMediaAsset)*
- **replaceMediaAsset answers 409**: Show it as something the person can act on, not a failure: The upload cannot be used: it is a different kind — an image cannot replace a document (`kindMismatch`) — or the transfer never finished (`transferIncomplete`), the upload ticket expired (`uploadExpired`), or the stored file is larger than the ticket allowed (`sizeExceeded`) *(source: contracts/satellite/assets.yaml#replaceMediaAsset)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
old: Summer 2025 hero.jpg
new: Summer 2026 hero.jpg
usages:
  web: 3
  app: 2
  kiosk: 1
mode: Replace everywhere eligible
```

#### Permissions

- `replaceMediaAsset` → `ASSET_LIBRARY_MANAGE` (configure) · staff
- `getMediaDistribution` → `ASSET_LIBRARY_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 23.1.8 | System shall maintain historical versions of assets and allow comparison, rollback, and restoration. | Digital Asset Management | CONTRACTED | `replaceMediaAsset` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Outdated/expired assets are replaced across all live locations at a scheduled time; if a primary asset is unavailable a backup image is substituted so channels never show a broken/missing image. *(client request · MoM 11 Sep 2026, 4.4 Asset Distribution, Delivery & Integration · DI-859)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-095` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS47 Digital Asset Management DAM Board 4.dc.html#cms-095`
- Workshop pack: Digital Asset Management DAM.pdf board 4
- Flow F186 *Digital Asset Management DAM board 4: Asset Distribution & Delivery Command …*, step 8: Works in Asset Replacement & Propagation Management → Safely manage replacement of assets that are outdated, expired, incorrect, rebranded, or otherwise no longer suitable.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-095?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Replace Everywhere Eligible, Replace Selected Uses, Schedule Replacement, Keep Existing Version, Create Fallback.
- [ ] Every transition is wired: `CMS-091`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-096` Fallback, Expiry & Distribution Continuity

**Ensure channels do not break when an asset becomes unavailable, expired, blocked, or fails delivery.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | Block B · task APP-CMS-CMS-096 |
| Who uses it | venue staff holding `ASSET_LIBRARY_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configured Fallback) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/media-library/fallback-expiry-distribution-continuity-cms-096` |

**Known gaps.** **The pack names 12 actions on this screen and the screen declares 0 operations.** Unserved: Usage-Level Fallback, Asset archived, rights expired, approval revoked, rendition unavailable, asset …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The fallback a channel shows when an asset becomes unavailable (archived, rights expired, approval revoked, rendition missing).

**Fixed on main** (the package already carries these; draw what it says): The field label is a sample asset ("DAM-IMG-009211 — Default Dubai Park Hero"). (CHG-SGU-023).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Default fallback asset | picker: choose an id (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Picked from the library (e.g. DAM-IMG-009211, "Default Dubai Park Hero"). | `MediaAsset.id` |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Usage-Level Fallback (primary button) | navigation or local | — | — | — | — |
| Asset archived (secondary button) | navigation or local | — | — | — | — |
| rights expired (secondary button) | navigation or local | — | — | — | — |
| approval revoked (secondary button) | navigation or local | — | — | — | — |
| rendition unavailable (secondary button) | navigation or local | — | — | — | — |
| asset restricted (secondary button) | navigation or local | — | — | — | — |
| delivery failure (secondary button) | navigation or local | — | — | — | — |
| version unavailable (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `CMS-091` Asset Distribution & Delivery Command Center: *Back to Asset Distribution & Delivery Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The fallback expiry distribution configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the fallback expiry distribution untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No fallback expiry distribution configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
channel: Guest app home banner
fallback: Default AquaCove hero.jpg
triggers:
- rights expired
- approval revoked
- rendition unavailable
```

#### Permissions

- `setMediaDistributionChannels` → `ASSET_LIBRARY_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 23.1.13 | System shall distribute approved assets to websites, mobile apps, kiosks, CRM campaigns, and digital channels. | Digital Asset Management | CONTRACTED | `setMediaDistributionChannels` |
| 23.1.3 | System shall support configurable metadata including asset type, owner, department, campaign, venue, event, creation date, expiry date, and usage rights. | Digital Asset Management | CONTRACTED | data `MediaAsset` |
| 23.1.10 | System shall support secure sharing of assets across departments, venues, tenants, and external partners. | Digital Asset Management | CONTRACTED | data `MediaAsset` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Outdated/expired assets are replaced across all live locations at a scheduled time; if a primary asset is unavailable a backup image is substituted so channels never show a broken/missing image. *(client request · MoM 11 Sep 2026, 4.4 Asset Distribution, Delivery & Integration · DI-859)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-096` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS47 Digital Asset Management DAM Board 4.dc.html#cms-096`
- Workshop pack: Digital Asset Management DAM.pdf board 4
- Flow F186 *Digital Asset Management DAM board 4: Asset Distribution & Delivery Command …*, step 10: Works in Fallback, Expiry & Distribution Continuity → Ensure channels do not break when an asset becomes unavailable, expired, blocked, or fails delivery.

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-096?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Usage-Level Fallback, Asset archived, rights expired, approval revoked, rendition unavailable, asset restricted, delivery failure, version unavailable.
- [ ] Every transition is wired: `CMS-091`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-097` DAM API & Integration Hub

**Provide controlled APIs and integration services for internal TICVAI modules and approved external systems.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | Block B · task APP-CMS-CMS-097 |
| Who uses it | venue staff holding `ASSET_LIBRARY_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/media-library/dam-api-integration-hub-cms-097` |

**Known gaps.** **The pack names 2 actions on this screen and the screen declares 0 operations.** Unserved: API credentials, service accounts. Each needs an operation, or needs removing from the screen; this is the … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** APIs and service accounts for modules and approved systems to consume DAM content.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SGU-023).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Asset | upload, or pick from the media library | — | — | `getMediaDistribution` ?assetId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| API credentials (primary button) | navigation or local | — | — | — | — |
| service accounts (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getMediaDistribution` (onLoad, What the API exposes)

**Where the user goes next**

- → `CMS-091` Asset Distribution & Delivery Command Center: *Back to Asset Distribution & Delivery Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The dam api integration list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the dam api integration untouched. |
| Empty, first run (`?state=emptyFirstRun`) | Nothing here yet for DAM API & Integration Hub. This screen only reads, so it offers no create action and says where the records come from. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the dam api integration are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
consumers:
- name: Guest app
  kind: internal
- name: Digital signage (Lagoon Zone)
  kind: external
  scope: read approved images
```

#### Permissions

- `getMediaDistribution` → `ASSET_LIBRARY_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-097` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS47 Digital Asset Management DAM Board 4.dc.html#cms-097`
- Workshop pack: Digital Asset Management DAM.pdf board 4
- Flow F186 *Digital Asset Management DAM board 4: Asset Distribution & Delivery Command …*, step 12: Works in DAM API & Integration Hub → Provide controlled APIs and integration services for internal TICVAI modules and approved external systems.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-097?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: API credentials, service accounts.
- [ ] Every transition is wired: `CMS-091`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-098` Delivery Monitoring & Integration Health

**Monitor the technical health of DAM delivery and connected integrations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | Block B · task APP-CMS-CMS-098 |
| Who uses it | venue staff holding `ASSET_LIBRARY_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Display; Detect) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/media-library/delivery-monitoring-integration-health-cms-098` |

**Known gaps.** **The pack names 11 actions on this screen and the screen declares 0 operations.** Unserved: View Consumer, Assign Replacement, Retry, View Logs, Notify Owner, Alerting, high error rate, delivery …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Delivery availability, response time, CDN cache hit and failures.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SGU-023).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getMediaUsageAnalytics` ?from |
| To | date and time picker | — | — | `getMediaUsageAnalytics` ?to |
| Group by | radio group | — | Asset type · Category · Venue · Owner · Channel | `getMediaUsageAnalytics` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Delivery Availability** (metric tile)

**Average Response Time** (metric tile)

**CDN Cache Hit %** (metric tile)

**API Success %** (metric tile)

**Failed Requests** (metric tile)

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| View Consumer (primary button) | navigation or local | — | — | — | — |
| Assign Replacement (secondary button) | navigation or local | — | — | — | — |
| Retry (secondary button) | navigation or local | — | — | — | — |
| View Logs (secondary button) | navigation or local | — | — | — | — |
| Notify Owner (secondary button) | navigation or local | — | — | — | — |
| Alerting (secondary button) | navigation or local | — | — | — | — |
| high error rate (secondary button) | navigation or local | — | — | — | — |
| delivery latency (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getMediaUsageAnalytics` (onLoad, Delivery health)

**Where the user goes next**

- → `CMS-091` Asset Distribution & Delivery Command Center: *Back to Asset Distribution & Delivery Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The delivery monitoring integration list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the delivery monitoring integration untouched. |
| Empty, first run (`?state=emptyFirstRun`) | Nothing here yet for Delivery Monitoring & Integration Health. This screen only reads, so it offers no create action and says where the records come from. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the delivery monitoring integration are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
metric tiles:
  Delivery Availability: 128
  Average Response Time: 42 min
  CDN Cache Hit %: 71%
  API Success %: 94%
  Failed Requests: 3
```

#### Permissions

- `getMediaUsageAnalytics` → `ASSET_LIBRARY_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Delivery monitoring tracks availability errors and broken references across the distribution network. *(client request · MoM 11 Sep 2026, 4.4 Asset Distribution, Delivery & Integration · DI-860)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-098` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS47 Digital Asset Management DAM Board 4.dc.html#cms-098`
- Workshop pack: Digital Asset Management DAM.pdf board 4
- Flow F186 *Digital Asset Management DAM board 4: Asset Distribution & Delivery Command …*, step 14: Works in Delivery Monitoring & Integration Health → Monitor the technical health of DAM delivery and connected integrations.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-098?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: View Consumer, Assign Replacement, Retry, View Logs, Notify Owner, Alerting, high error rate, delivery latency.
- [ ] Every transition is wired: `CMS-091`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-099` Asset Usage & Performance Analytics

**Show how digital assets are actually being consumed across TICVAI.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | Block B · task APP-CMS-CMS-099 |
| Who uses it | venue staff holding `ASSET_LIBRARY_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Performance Metrics) and a per-row directory (§Display; Identify) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/media-library/asset-usage-performance-analytics-cms-099` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** How assets are consumed: impressions, requests, downloads, reuse.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The table's columns are the workshop pack's labels with no bound response field (0 of 3 labels bound). (CHG-SGU-024)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SGU-023).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getMediaUsageAnalytics` ?from |
| To | date and time picker | — | — | `getMediaUsageAnalytics` ?to |
| Group by | radio group | — | Asset type · Category · Venue · Owner · Channel | `getMediaUsageAnalytics` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**impressions** (metric tile)

**requests** (metric tile)

**downloads** (metric tile)

**delivery volume** (metric tile)

**reuse count** (metric tile)

**Every asset usage performance** (data table)

| Shows | Format | Notes |
|---|---|---|
| Assets used | text | not in the schema: `Assets Used` |
| Asset requests | text | not in the schema: `Asset Requests` |
| Downloads | text | not in the schema: `Downloads` |

**The selected asset usage performance** (detail panel): The pack groups this record's detail under its own headings: “Digital Asset Management”, “Asset Channels Requests Downloads Status”, “No usage in”, “Storage”, “Important”.

| Shows | Format | Notes |
|---|---|---|
| Assets used | text | not in the schema: `Assets Used` |
| Asset requests | text | not in the schema: `Asset Requests` |
| Downloads | text | not in the schema: `Downloads` |

**Data it reads**: `getMediaUsageAnalytics` (onLoad, Usage and performance)

**Where the user goes next**

- → `CMS-091` Asset Distribution & Delivery Command Center: *Back to Asset Distribution & Delivery Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The asset usage performance list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the asset usage performance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | Nothing here yet for Asset Usage & Performance Analytics. This screen only reads, so it offers no create action and says where the records come from. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the asset usage performance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
metric tiles:
  impressions: 128
  requests: 46
  downloads: 312
  delivery volume: 74
  reuse count: 19
Every asset usage performance:
- Assets Used: 74
  Asset Requests: 128
  Downloads: 46
- Assets Used: 19
  Asset Requests: 42
  Downloads: 312
- Assets Used: 233
  Asset Requests: 7
  Downloads: 74
```

#### Permissions

- `getMediaUsageAnalytics` → `ASSET_LIBRARY_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-099` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS47 Digital Asset Management DAM Board 4.dc.html#cms-099`
- Workshop pack: Digital Asset Management DAM.pdf board 4
- Flow F186 *Digital Asset Management DAM board 4: Asset Distribution & Delivery Command …*, step 16: Works in Asset Usage & Performance Analytics → Show how digital assets are actually being consumed across TICVAI.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-099?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `CMS-091`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-100` Distribution Intelligence, AI Insights & Optimization

**Provide intelligent recommendations across DAM distribution, usage, delivery, replacements, and integrations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | Block B · task APP-CMS-CMS-100 |
| Who uses it | venue staff holding `ASSET_LIBRARY_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Select DAM Asset) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/media-library/distribution-intelligence-ai-insights-optimization-cms-100` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** AI recommendations across distribution, usage and replacement.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SGU-023).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| ↓ | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getMediaUsageAnalytics` ?from |
| To | date and time picker | — | — | `getMediaUsageAnalytics` ?to |
| Group by | radio group | — | Asset type · Category · Venue · Owner · Channel | `getMediaUsageAnalytics` ?groupBy |

#### Outputs: what the screen shows and produces

**Data it reads**: `getMediaUsageAnalytics` (onLoad, Distribution intelligence)

**Where the user goes next**

- → `CMS-091` Asset Distribution & Delivery Command Center: *Back to Asset Distribution & Delivery Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The distribution intelligence insights configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the distribution intelligence insights untouched. |
| Empty, first run (`?state=emptyFirstRun`) | Nothing here yet for Distribution Intelligence, AI Insights & Optimization. This screen only reads, so it offers no create action and says where the records come from. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
getMediaUsageAnalytics (MediaUsageRow):
- label: AquaCove Abu Dhabi
  assetCount: 12
  storageBytes: 12
  downloads: 12
  views: 12
  shares: 12
  neverUsedCount: 12
- label: Main Gate Till 3
  assetCount: 3
  storageBytes: 3
  downloads: 3
  views: 3
  shares: 3
  neverUsedCount: 3
```

#### Permissions

- `getMediaUsageAnalytics` → `ASSET_LIBRARY_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-100` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS47 Digital Asset Management DAM Board 4.dc.html#cms-100`
- Workshop pack: Digital Asset Management DAM.pdf board 4
- Flow F186 *Digital Asset Management DAM board 4: Asset Distribution & Delivery Command …*, step 18: Works in Distribution Intelligence, AI Insights & Optimization → Provide intelligent recommendations across DAM distribution, usage, delivery, replacements, and integrations.

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-100?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `CMS-091`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P13 reference designs** (from `handoff/design-batches/apps/5-venue-management/README.md`)

- `sources/designs/guest-rev3-29-september/TICVAI Engine Controls Manual.dc.html`: the look of the controls: every configuration control, laid out and explained.
- `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html`: the configuration side panel, for the controls, and the guest booking the live preview shows.
- `sources/designs/TICVAI_White_Label_Guest_App_UI_Reference_1.pdf`: the client's White Label Builder boards.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-039, DI-040, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

**Workshop tracker rows about P13 as a whole** (5: 0 open, 5 closed). Open first; a closed row says where it went on 30 September.

- **A47** Advise Qossai/Allam on the Apple/Google Developer account ownership model and a simplified, low-effort app-publishing workflow for white-labelled tenant apps (incl. how to reflect "Powered by TICVAI" branding) *(Pradnya Yeram · Low · Done → 30 Sep: Closed, Done (as recorded earlier) · 24 Sep 2026 · workshop tracker)*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker)*
- **A338** Build the real white-label CMS builder (client builds a site in ~30 min) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 24 Sep 2026 · workshop tracker)*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker)*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker)*

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

### Across P13 Venue CMS

- The config side panel is a reference tool only, not the CMS. The CMS will be step-based and include header/footer, logos and banners. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W12 Config side panel · DI-1014)*
- Decision: RBAC per role, per module, three levels — edit/view, view-only, hidden (e.g. a marketing officer does not see Finance at all) — plus sub-permissions within a module (a CRM role may get Campaigns and Communications but not Journeys). Default role templates, admin-customisable. *(agreed · MoM 20 Aug 2026, 4.7 Role-Based Access Control (RBAC); 5. Key Decisions · DI-387)*
- Qossai: build AI-assisted site design/generation into the website builder, keeping site design (header, footer, color, font, layout) separate from content (tickets), with tickets flowing into the site's structure once published. To be explored. *(client request · MoM 3 Aug 2026, 7. AI-Assisted Website Generation · DI-115)*
- Qossai: give clients as much design flexibility as possible within the configurable structure. *(client request · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-114)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*

**6 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"getMediaDistribution": {"method":"GET","path":"/media-distribution","contract":"assets","summary":"Where an asset is used and how it is delivered","permission":"ASSET_LIBRARY_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"assetId","in":"query","required":true}],"requestBody":null,"responds":"MediaDistribution"},
"getMediaUsageAnalytics": {"method":"GET","path":"/media-usage","contract":"assets","summary":"Downloads, views, shares and library health","permission":"ASSET_LIBRARY_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"MediaUsageRow"},
"listMediaRenditions": {"method":"GET","path":"/media-assets/{assetId}/renditions","contract":"assets","summary":"The derived sizes and formats, and whether they are ready","permission":"ASSET_LIBRARY_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"MediaRendition"},
"replaceMediaAsset": {"method":"POST","path":"/media/{mediaId}/replace","contract":"assets","summary":"Replace the file behind an asset","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MediaReplaceResult"},
"setMediaDistributionChannels": {"method":"PUT","path":"/media-distribution/channels","contract":"assets","summary":"CDN, delivery URLs, fallbacks and expiry behaviour","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MediaDistributionChannel","responds":"MediaDistributionChannel"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"MediaAsset": {"x-ticvai-persistence":"assets.media_asset","type":"object","required":["id","kind","status","filename","contentType","sizeBytes","referenceCount","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/MediaKind"},"status":{"$ref":"#/components/schemas/MediaStatus"},"filename":{"type":"string"},"contentType":{"type":"string"},"sizeBytes":{"type":"integer"},"title":{"$ref":"#/components/schemas/LocalisedText"},"description":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"Set by `updateMediaAsset` and matched by `searchMedia`'s `search`. It was accepted and searched on before it had anywhere to be stored.\n"},"altText":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"Required before use in a guest-facing surface. WCAG 2.2 AA."},"width":{"type":"integer","nullable":true},"height":{"type":"integer","nullable":true},"durationSeconds":{"type":"number","nullable":true},"customMetadata":{"type":"object","nullable":true,"additionalProperties":true,"description":"BL-178. **`assets` is a strong contract and its metadata was fixed** — kind, title, alt text, dimensions, rights. A venue photographing four thousand products wants its own fields: shoot date, photographer, model release, season.\n**Free-form and searchable, not a schema.** Every venue would want a different one, and a fixed set would be wrong for all of them.\n"},"sharedWithTenantIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"BL-178. **Cross-tenant sharing, and it is refused by default for a reason.** A brand operating three venues wants one logo library; two unrelated tenants sharing an asset store is the isolation breach ADR-0011 exists to prevent.\n**Only within one tenant's own scope tree.** A share naming a tenant outside it is refused rather than warned about — this is the one place where a permissive default would be a cross-tenant data leak.\n"},"tags":{"type":"array","items":{"type":"string"}},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"The asset's category, one of `MediaTaxonomy.categories[].id`; null while unclassified. Set by `bulkUpdateMediaAssets` (`setCategoryId`) (decided 29 September, data model DM4).\n"},"venueId":{"type":"string","format":"uuid","nullable":true},"url":{"type":"string","description":"Signed and expiring for private assets; stable CDN URL for public ones."},"thumbnailUrl":{"type":"string","nullable":true},"referenceCount":{"type":"integer","description":"How many surfaces reference this asset. Non-zero refuses deletion.\n"},"rights":{"$ref":"#/components/schemas/MediaRights"},"isRightsExpired":{"type":"boolean"},"version":{"type":"integer"},"uploadedByPrincipalId":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"}}},
"MediaDistribution": {"type":"object","description":"Boards 4.2 and 4.5. **The usage map that makes replacement safe.**","properties":{"assetId":{"type":"string","format":"uuid"},"deliveryUrls":{"type":"array","items":{"type":"object","properties":{"channel":{"type":"string"},"rendition":{"type":"string"},"url":{"type":"string"},"cdn":{"type":"string","nullable":true}}}},"usedBy":{"type":"array","items":{"type":"object","properties":{"surface":{"type":"string"},"referenceId":{"type":"string","format":"uuid"},"label":{"type":"string"},"live":{"type":"boolean"}}}},"lastDeliveredAt":{"type":"string","format":"date-time","nullable":true}}},
"MediaDistributionChannel": {"type":"object","x-ticvai-persistence":"assets.distribution_channel","description":"Boards 4.3, 4.4 and 4.6. **The fallback keeps a page from breaking.**","required":["code"],"properties":{"code":{"type":"string"},"name":{"type":"string"},"cdnBaseUrl":{"type":"string","nullable":true},"signedUrls":{"type":"boolean","default":false},"signedUrlTtlSeconds":{"type":"integer","nullable":true},"defaultRendition":{"type":"string","nullable":true},"fallbackAssetId":{"type":"string","format":"uuid","nullable":true,"description":"**What renders when the real one cannot.** Rights expired, rendition failed, CDN unreachable — three causes, one visible outcome, and one place to decide it.\n"},"onRightsExpiry":{"type":"string","enum":["serveFallback","serveNothing","continueServing"],"default":"serveFallback"},"scopePath":{"type":"string"}}},
"MediaRendition": {"type":"object","x-ticvai-persistence":"assets.rendition","description":"Boards 2.8 and 2.9. **Readiness is the fact that matters**, not existence.","required":["preset"],"properties":{"id":{"type":"string","format":"uuid"},"preset":{"type":"string","description":"e.g. `thumbnail`, `web1600`, `printCmyk`, `hls720`."},"format":{"type":"string","nullable":true},"width":{"type":"integer","nullable":true},"height":{"type":"integer","nullable":true},"sizeBytes":{"type":"integer","nullable":true},"status":{"type":"string","enum":["queued","processing","ready","failed"]},"failureReason":{"type":"string","nullable":true},"url":{"type":"string","nullable":true},"scopePath":{"type":"string"}}},
"MediaReplaceResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["asset","affectedSurfaces"],"properties":{"asset":{"$ref":"#/components/schemas/MediaAsset"},"affectedSurfaces":{"type":"integer","description":"How many surfaces now show the new file."},"liveSurfaces":{"type":"integer","description":"Of those, how many are published to guests right now."},"derivativesRegenerating":{"type":"boolean"}}},
"MediaUsageRow": {"type":"object","description":"Boards 1.10 and 4.9. **Assets never used is the number that justifies the library.**","properties":{"key":{"type":"string"},"label":{"type":"string"},"assetCount":{"type":"integer"},"storageBytes":{"type":"integer"},"downloads":{"type":"integer"},"views":{"type":"integer"},"shares":{"type":"integer"},"neverUsedCount":{"type":"integer"},"unclassifiedCount":{"type":"integer"}}}
}
```
