# WS76 — Digital Asset Management DAM board 3

**10 screens · 11 operations · 16 schemas · 7 permissions**

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

- **Every control that can be refused must be gated.** 7 permissions apply here:
  `ASSET_LIBRARY_APPROVE, ASSET_LIBRARY_MANAGE, ASSET_LIBRARY_SHARE, ASSET_LIBRARY_VIEW, PERMISSION_MANAGE, PERMISSION_VIEW, ROLE_MANAGE`. A control nobody can use must say so,
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
| `CMS-081` | DAM Governance & Rights Command Center | B | 0 | 16 | 6 | 1 | 1 | 0 | — | notStarted (—) |
| `CMS-082` | Asset Ownership & Responsibility Management | B | 0 | 0 | 6 | 1 | 1 | 0 | — | notStarted (—) |
| `CMS-083` | Rights, License & Usage Policy Management | B | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `CMS-084` | Asset Approval Workflow Management | B | 0 | 0 | 6 | 0 | 1 | 3 | — | notStarted (—) |
| `CMS-085` | Publication Eligibility & Governance Validation | B | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `CMS-086` | Role-Based Asset Access & Permission Management | B | 24 | 5 | 6 | 6 | 1 | 5 | — | notStarted (—) |
| `CMS-087` | Secure Internal & External Sharing | B | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `CMS-088` | Rights Expiry, Renewal & Usage Impact | B | 0 | 8 | 6 | 1 | 1 | 0 | — | notStarted (—) |
| `CMS-089` | Governance Audit Trail & Compliance Evidence | B | 1 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `CMS-090` | Governance Risk, Compliance & AI Recommendations | B | 0 | 20 | 6 | 1 | 1 | 0 | — | notStarted (—) |

## Thin screens in this batch

**CMS-082, CMS-083, CMS-085, CMS-089, CMS-090 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `CMS-081` DAM Governance & Rights Command Center

**Provide DAM administrators, brand managers, legal/compliance teams, and content managers with one overview of asset governance.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | Block B · task APP-CMS-CMS-081 |
| Who uses it | venue staff holding `ASSET_LIBRARY_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/media-library/dam-governance-rights-command-center-cms-081` |

**Known gaps.** **The pack names 5 actions on this screen and the screen declares 0 operations.** Unserved: Approval Queue, Rights Review, Expiring Assets, External Shares, Governance Issues. Each needs an … **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Asset governance overview: pending approval, restricted, expired, blocked, external shares, alerts.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The table's columns are the workshop pack's labels with no bound response field (0 of 8 labels bound). (CHG-SGU-024)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SGU-023).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Within days | number field (days) | 60 | — | `getExpiringRights` ?withinDays |
| From | date and time picker | — | — | `getMediaUsageAnalytics` ?from |
| To | date and time picker | — | — | `getMediaUsageAnalytics` ?to |
| Group by | radio group | — | Asset type · Category · Venue · Owner · Channel | `getMediaUsageAnalytics` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every dam governance rights** (data table)

| Shows | Format | Notes |
|---|---|---|
| Active assets | text | not in the schema: `Active Assets` |
| Pending approval | text | not in the schema: `Pending Approval` |
| Approved | text | not in the schema: `Approved` |
| Pending | text | not in the schema: `Pending` |
| Restricted | text | not in the schema: `Restricted` |
| Expired | text | not in the schema: `Expired` |
| Blocked | text | not in the schema: `Blocked` |
| Critical alerts | text | not in the schema: `Critical Alerts` |

**The selected dam governance rights** (detail panel): The pack groups this record's detail under its own headings: “Digital Asset Management”.

| Shows | Format | Notes |
|---|---|---|
| Active assets | text | not in the schema: `Active Assets` |
| Pending approval | text | not in the schema: `Pending Approval` |
| Approved | text | not in the schema: `Approved` |
| Pending | text | not in the schema: `Pending` |
| Restricted | text | not in the schema: `Restricted` |
| Expired | text | not in the schema: `Expired` |
| Blocked | text | not in the schema: `Blocked` |
| Critical alerts | text | not in the schema: `Critical Alerts` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Approval Queue (primary button) | navigation or local | — | — | — | — |
| Rights Review (secondary button) | navigation or local | — | — | — | — |
| Expiring Assets (secondary button) | navigation or local | — | — | — | — |
| External Shares (secondary button) | navigation or local | — | — | — | — |
| Governance Issues (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getExpiringRights` (onLoad, Rights about to lapse); `getMediaUsageAnalytics` (onLoad, Governance coverage)

**Where the user goes next**

- → `CMS-001` Tenant Workspace: *Back to Tenant Workspace*
- → `CMS-082` Asset Ownership & Responsibility Management: *Asset Ownership & Responsibility Management*
- → `CMS-083` Rights, License & Usage Policy Management: *Rights, License & Usage Policy Management*; carries `assetId`
- → `CMS-084` Asset Approval Workflow Management: *Asset Approval Workflow Management*; carries `assetId`
- → `CMS-085` Publication Eligibility & Governance Validation: *Publication Eligibility & Governance Validation*; carries `assetId`
- → `CMS-086` Role-Based Asset Access & Permission Management: *Role-Based Asset Access & Permission Management*
- → `CMS-087` Secure Internal & External Sharing: *Secure Internal & External Sharing*
- → `CMS-088` Rights Expiry, Renewal & Usage Impact: *Rights Expiry, Renewal & Usage Impact*; carries `assetId`
- → `CMS-089` Governance Audit Trail & Compliance Evidence: *Governance Audit Trail & Compliance Evidence*; carries `assetId`
- → `CMS-090` Governance Risk, Compliance & AI Recommendations: *Governance Risk, Compliance & AI Recommendations*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The dam governance rights list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the dam governance rights untouched. |
| Empty, first run (`?state=emptyFirstRun`) | Nothing here yet for DAM Governance & Rights Command Center. This screen only reads, so it offers no create action and says where the records come from. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the dam governance rights are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every dam governance rights:
- Active Assets: 128
  Pending Approval: 128
  Approved: 128
  Pending: 11
  Restricted: 312
  Expired: 5
  Blocked: 11
  Critical Alerts: 128
- Active Assets: 42
  Pending Approval: 46
  Approved: 46
  Pending: 128
  Restricted: 74
  Expired: 1
  Blocked: 128
  Critical Alerts: 42
- Active Assets: 7
  Pending Approval: 312
  Approved: 312
  Pending: 46
  Restricted: 19
  Expired: 3
  Blocked: 46
  Critical Alerts: 7
```

#### Permissions

- `getExpiringRights` → `ASSET_LIBRARY_VIEW` (read) · staff
- `getMediaUsageAnalytics` → `ASSET_LIBRARY_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 23.1.11 | System shall track asset ownership, copyright information, licensing terms, and expiration dates. | Digital Asset Management | CONTRACTED | `getExpiringRights` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Governance overview shows assets pending approval vs approved; each asset names business owner, content owner, rights owner and approver; usage rights state where it may be used (e.g. social media yes, third-party distribution no). *(client request · MoM 11 Sep 2026, 4.3 Asset Governance, Rights, Approvals & Secure Sharing · DI-853)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-081` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS46 Digital Asset Management DAM Board 3.dc.html#cms-081`
- Workshop pack: Digital Asset Management DAM.pdf board 3
- Flow F185 *Digital Asset Management DAM board 3: DAM Governance & Rights Command Center*, step 1: Opens DAM Governance & Rights Command Center → Provide DAM administrators, brand managers, legal/compliance teams, and content managers with one overview of asset governance.
- Flow F185 *Digital Asset Management DAM board 3: DAM Governance & Rights Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F185 *Digital Asset Management DAM board 3: DAM Governance & Rights Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F185 *Digital Asset Management DAM board 3: DAM Governance & Rights Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F185 *Digital Asset Management DAM board 3: DAM Governance & Rights Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F185 *Digital Asset Management DAM board 3: DAM Governance & Rights Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F185 *Digital Asset Management DAM board 3: DAM Governance & Rights Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F185 *Digital Asset Management DAM board 3: DAM Governance & Rights Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F185 branch at step 1 (expected): when Nothing has been set up on DAM Governance & Rights Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F185 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-081?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Approval Queue, Rights Review, Expiring Assets, External Shares, Governance Issues.
- [ ] Every transition is wired: `CMS-001`, `CMS-082`, `CMS-083`, `CMS-084`, `CMS-085`, `CMS-086`, `CMS-087`, `CMS-088`, `CMS-089`, `CMS-090`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-082` Asset Ownership & Responsibility Management

**Define who owns and is responsible for each digital asset from a business and operational perspective. This should be separate from the person who simply uploaded the file.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | Block B · task APP-CMS-CMS-082 |
| Who uses it | venue staff holding `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `mediaId` (navigation) |
| Route | `/media-library/asset-ownership-responsibility-management-cms-082` |

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: Partner. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Business owner of each asset, separate from the uploader.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SGU-023).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Partner (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `CMS-081` DAM Governance & Rights Command Center: *Back to DAM Governance & Rights Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The asset ownership responsibility list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the asset ownership responsibility untouched. |
| Empty, first run (`?state=emptyFirstRun`) | Nothing here yet for Asset Ownership & Responsibility Management. This screen only reads, so it offers no create action and says where the records come from. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the asset ownership responsibility are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Status change refused: archiving an asset that is still referenced (`inUse`, with every reference listed), or a transition `states/media.yaml` does not allow … (MediaStatusRefusedProblem) |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds ASSET_LIBRARY_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: ASSET_LIBRARY_MANAGE for updateMediaAsset. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/assets.yaml#updateMediaAsset)*
- **updateMediaAsset answers 409**: Show it as something the person can act on, not a failure: Status change refused: archiving an asset that is still referenced (`inUse`, with every reference listed), or a transition `states/media.yaml` does not allow from the asset's current status (`transitionNotAllowed`) *(source: contracts/satellite/assets.yaml#updateMediaAsset)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
getMediaAsset (MediaAssetDetail):
- kind: standard
  status: active
  sizeBytes: 12
  title: Lazy river at sunset.jpg
  description: Guest charged twice at Main Gate Till 3
- kind: standard
  status: pending
  sizeBytes: 3
  title: Wave pool promo (Arabic).mp4
  description: Group of 40 from Desert Gate Tours
```

#### Permissions

- `updateMediaAsset` → `ASSET_LIBRARY_MANAGE` (configure) · staff
- `getMediaAsset` → `ASSET_LIBRARY_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 23.1.12 | System shall track where assets are used across websites, mobile applications, campaigns, kiosks, emails, and digital channels. | Digital Asset Management | CONTRACTED | `getMediaAsset` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Governance overview shows assets pending approval vs approved; each asset names business owner, content owner, rights owner and approver; usage rights state where it may be used (e.g. social media yes, third-party distribution no). *(client request · MoM 11 Sep 2026, 4.3 Asset Governance, Rights, Approvals & Secure Sharing · DI-853)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-082` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS46 Digital Asset Management DAM Board 3.dc.html#cms-082`
- Workshop pack: Digital Asset Management DAM.pdf board 3
- Flow F185 *Digital Asset Management DAM board 3: DAM Governance & Rights Command Center*, step 2: Works in Asset Ownership & Responsibility Management → Define who owns and is responsible for each digital asset from a business and operational perspective. This should be separate from the person who simply uploaded the file.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-082?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Partner, Cancel.
- [ ] Every transition is wired: `CMS-081`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-083` Rights, License & Usage Policy Management

**Define exactly how an asset is legally and commercially allowed to be used.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | Block B · task APP-CMS-CMS-083 |
| Who uses it | venue staff holding `ASSET_LIBRARY_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `assetId` (navigation) |
| Route | `/media-library/rights-license-usage-policy-management-cms-083` |

**Known gaps.** **The pack names 2 actions on this screen and the screen declares 0 operations.** Unserved: Commercial use permitted, Non-commercial only. Each needs an operation, or needs removing from the screen … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** How an asset may be used legally and commercially: licensor, territory, channels, dates, commercial or not.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Commercial use permitted (primary button) | navigation or local | — | — | — | — |
| Non-commercial only (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `CMS-081` DAM Governance & Rights Command Center: *Back to DAM Governance & Rights Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rights license usage list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rights license usage untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rights license usage yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rights license usage are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rights:
  licensor: Marina Leisure Group (own)
  territory: GCC
  channels:
  - web
  - app
  - signage
  validTo: 31/12/2027
  commercialUse: true
```

#### Permissions

- `setMediaAssetRights` → `ASSET_LIBRARY_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Governance overview shows assets pending approval vs approved; each asset names business owner, content owner, rights owner and approver; usage rights state where it may be used (e.g. social media yes, third-party distribution no). *(client request · MoM 11 Sep 2026, 4.3 Asset Governance, Rights, Approvals & Secure Sharing · DI-853)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-083` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS46 Digital Asset Management DAM Board 3.dc.html#cms-083`
- Workshop pack: Digital Asset Management DAM.pdf board 3
- Flow F185 *Digital Asset Management DAM board 3: DAM Governance & Rights Command Center*, step 4: Works in Rights, License & Usage Policy Management → Define exactly how an asset is legally and commercially allowed to be used.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-083?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Commercial use permitted, Non-commercial only.
- [ ] Every transition is wired: `CMS-081`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-084` Asset Approval Workflow Management

**Provide configurable governance before an asset becomes approved for operational or public use.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | Block B · task APP-CMS-CMS-084 |
| Who uses it | venue staff holding `ASSET_LIBRARY_APPROVE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | approvalInbox (compact density): the pack lists Approve and Reject among this screen's own actions — every row is waiting for a decision, so the empty state is success rather than a prompt to create something |
| Offline | online only |
| Opens with | `assetId` (navigation) |
| Route | `/media-library/asset-approval-workflow-management-cms-084` |

**What the spec says about it.** **No Delegate button (CHG-SGU-023).** Delegation is configured ahead of time (`createApprovalDelegation` on the approvals screens), not chosen per decision.

**Known gaps.** **The pack names 6 actions on this screen and the screen declares 0 operations.** Unserved: Approve, Reject, Request Changes, Delegate, Add Comment, Rejection. Each needs an operation, or needs … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Approval of assets before public use: approve, reject with reason, request changes, comment.

**Fixed on main** (the package already carries these; draw what it says): "Delegate" is a decision button. (CHG-SGU-023).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Approve (primary button) | navigation or local | — | — | — | — |
| Reject (destructive button) | navigation or local | — | — | — | — |
| Request Changes (secondary button) | navigation or local | — | — | — | — |
| Add Comment (secondary button) | navigation or local | — | — | — | — |
| Rejection (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `CMS-081` DAM Governance & Rights Command Center: *Back to DAM Governance & Rights Command Center*

**What opens over it**

- confirmDialog *Reject*: **Reject on a asset approval workflow is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The asset approval workflow list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the asset approval workflow untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing is waiting, which is the good outcome.** An empty queue means every request has been decided — this state offers no create action, because creating work is not what an empty inbox needs. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the asset approval workflow are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Not eligible to publish; the unmet conditions are listed in `unmet` (MediaNotPublishableProblem) |

#### Edge cases to draw

- **setMediaAssetApproval answers 409**: Show it as something the person can act on, not a failure: Not eligible to publish; the unmet conditions are listed in `unmet` *(source: contracts/satellite/assets.yaml#setMediaAssetApproval)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
asset: Wave pool promo (Arabic).mp4
requestedBy: Noura Al Hammadi
approver: Aisha Al Nuaimi
sla: 1 day
```

#### Permissions

- `setMediaAssetApproval` → `ASSET_LIBRARY_APPROVE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Publishing needs combined validation of approval status, usage rights and channel permissions before an asset can go live on a given channel. *(agreed · MoM 11 Sep 2026, 4.3 Asset Governance, Rights, Approvals & Secure Sharing · DI-854)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-084` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS46 Digital Asset Management DAM Board 3.dc.html#cms-084`
- Workshop pack: Digital Asset Management DAM.pdf board 3
- Flow F185 *Digital Asset Management DAM board 3: DAM Governance & Rights Command Center*, step 6: Works in Asset Approval Workflow Management → Provide configurable governance before an asset becomes approved for operational or public use.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-084?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Approve, Reject, Request Changes, Add Comment, Rejection.
- [ ] Every transition is wired: `CMS-081`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_APPROVE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-085` Publication Eligibility & Governance Validation

**Determine whether an asset is actually eligible to be used or distributed. This screen is particularly important. An asset being technically available in DAM does not mean it should be publishable.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | Block B · task APP-CMS-CMS-085 |
| Who uses it | venue staff holding `ASSET_LIBRARY_APPROVE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `assetId` (navigation) |
| Route | `/media-library/publication-eligibility-governance-validation-cms-085` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Whether an asset may be published: approved, rights valid for the channel, rendition ready, not restricted. Available in the library does not mean publishable.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** 🟢 B2C Allowed. Each needs attaching to the control it gates, or the screen needs the control.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save media asset approval (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `CMS-081` DAM Governance & Rights Command Center: *Back to DAM Governance & Rights Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The publication eligibility governance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the publication eligibility governance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No publication eligibility governance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the publication eligibility governance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Not eligible to publish; the unmet conditions are listed in `unmet` (MediaNotPublishableProblem) |

#### Edge cases to draw

- **setMediaAssetApproval answers 409**: Show it as something the person can act on, not a failure: Not eligible to publish; the unmet conditions are listed in `unmet` *(source: contracts/satellite/assets.yaml#setMediaAssetApproval)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
asset: Lazy river at sunset.jpg
approved: true
rightsValidFor:
- web
- app
renditionReady: true
eligible: web and app only (signage not licensed)
```

#### Permissions

- `setMediaAssetApproval` → `ASSET_LIBRARY_APPROVE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Publishing needs combined validation of approval status, usage rights and channel permissions before an asset can go live on a given channel. *(agreed · MoM 11 Sep 2026, 4.3 Asset Governance, Rights, Approvals & Secure Sharing · DI-854)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-085` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS46 Digital Asset Management DAM Board 3.dc.html#cms-085`
- Workshop pack: Digital Asset Management DAM.pdf board 3
- Flow F185 *Digital Asset Management DAM board 3: DAM Governance & Rights Command Center*, step 8: Works in Publication Eligibility & Governance Validation → Determine whether an asset is actually eligible to be used or distributed. This screen is particularly important. An asset being technically available in DAM does not mean it should be publishable.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-085?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save media asset approval, Cancel.
- [ ] Every transition is wired: `CMS-081`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_APPROVE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-086` Role-Based Asset Access & Permission Management

**Control who can discover, view, edit, download, share, approve, or manage assets.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | Block B · task APP-CMS-CMS-086 |
| Who uses it | venue staff holding `PERMISSION_MANAGE`, `PERMISSION_VIEW`, `ROLE_MANAGE` (2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/media-library/role-based-asset-access-permission-management-cms-086` |

**What the spec says about it.** **The generator's 'needs a person' gaps removed 4 October 2026 (the screen is filled); the roles come from listRoles so a policy's appliesToRoleIds can be picked by name** (CHG-FXS-005)

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Who may discover, view, edit, download, share, approve or manage assets.

**Fixed on main** (the package already carries these; draw what it says): Empty table and a generic policy create. (CHG-SGU-023).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Roles | multi-picker: choose applies to roles | optional | — | — | — | Options from listRoles, by name. | `AuthorisationPolicy.appliesToRoleIds` |
| Asset actions | list of values (chips) | optional | — | — | — | ASSET_LIBRARY_VIEW, ASSET_LIBRARY_SHARE, ASSET_LIBRARY_APPROVE, ASSET_LIBRARY_MANAGE, ASSET_VIEW and ASSET_MANAGE (the permission vocabulary). | `AuthorisationPolicy.permissions` |
| Policy name | text field | optional | — | — | — | — | `AuthorisationPolicy.name` |
| Policy code | text field | optional | — | — | — | — | `AuthorisationPolicy.code` |
| Effect | segmented control | optional | — | Permit · Deny | — | Deny wins over permit when two policies disagree. 3.3.32 asks for least-privilege, and a permit that can override a deny is not least-privilege by any reading — it is the union of every mistake … | `AuthorisationPolicy.effect` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Draft · Pending approval · Active · Suspended · Retired | `listAuthorisationPolicies` ?status |
| Scope path | text field | — | — | `listAuthorisationPolicies` ?scopePath |

**Form: Grant an asset action to a role** (modal, opened by *Grant an asset action to a role*; *Grant an asset action to a role* calls `createAuthorisationPolicy`, *Cancel* sends nothing)

The role, the asset actions it may take (discover, view, edit, download, share, approve, manage) and the scope it applies at. Dismissing sends nothing.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | — | — | — | `createAuthorisationPolicy` body |
| Name `name` | text field | required | — | — | — | — | `createAuthorisationPolicy` body |
| Description `description` | text area | optional | — | — | — | — | `createAuthorisationPolicy` body |
| Is template `isTemplate` | toggle | optional | off | — | — | — | `createAuthorisationPolicy` body |
| Permissions `permissions` | list of values (chips) | optional | — | — | — | Which permissions this policy speaks to. A policy with an empty list speaks to all of them, which is powerful enough that it is worth being explicit about. | `createAuthorisationPolicy` body |
| Conditions `conditions` | repeatable rows | optional | — | — | — | — | `createAuthorisationPolicy` body |
| Attribute `conditions[].attribute` | select | required | — | User.attribute · Employee.attribute · Employee.on shift · Membership.tier · Membership.status · Accreditation.type · Accreditation.status · Customer.segment · Resource.classification · Venue.attribute · Venue.id · Attraction.attribute … | — | — | `createAuthorisationPolicy` body |
| Key `conditions[].key` | text field | optional | — | — | — | For the `*.attribute` forms — which attribute, by code. | `createAuthorisationPolicy` body |
| Operator `conditions[].operator` | select | required | — | Equals · Not equals · In · Not in · Greater than · Less than · Between · Contains · Starts with · Exists | — | — | `createAuthorisationPolicy` body |
| Value `conditions[].value` | field | optional | — | — | — | The single comparand for `equals`, `notEquals`, `greaterThan`, `lessThan`, `contains` and `startsWith` — a string, number or boolean, by the attribute. | `createAuthorisationPolicy` body |
| Values `conditions[].values` | list of values (chips) | optional | — | — | — | — | `createAuthorisationPolicy` body |
| Combining `combining` | segmented control | optional | All must match | All must match · Any may match | — | — | `createAuthorisationPolicy` body |
| Effect `effect` | segmented control | required | — | Permit · Deny | — | Deny wins over permit when two policies disagree. 3.3.32 asks for least-privilege, and a permit that can override a deny is not least-privilege by any reading — it is the union of … | `createAuthorisationPolicy` body |
| Priority `priority` | number field | optional | 0 | — | — | — | `createAuthorisationPolicy` body |
| Scope path `scopePath` | text field | optional | — | — | — | 3.3.40 to 3.3.43. Tenant, venue and cross-venue policies are one mechanism, because `scope_path` is prefix-comparable — `uae.dubai` contains `uae.dubai.marina` — and inheritance … | `createAuthorisationPolicy` body |
| Applies to roles `appliesToRoleIds` | multi-picker: choose applies to roles | optional | — | — | — | — | `createAuthorisationPolicy` body |
| Effective from `effectiveFrom` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createAuthorisationPolicy` body |
| Effective to `effectiveTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createAuthorisationPolicy` body |
| Delegated admin roles `delegatedAdminRoleIds` | multi-picker: choose delegated admin roles | optional | — | — | — | 3.3.35. Who may edit this policy without being a platform administrator. | `createAuthorisationPolicy` body |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: createAuthorisationPolicy: tenant-wide only, no region or venue override is offered. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/spine/identity.yaml#createAuthorisationPolicy)*

#### Outputs: what the screen shows and produces

**Shown**

**Roles and asset actions** (data table, from `listAuthorisationPolicies`): One row per policy; role ids shown by the role's name from listRoles.

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Effect | chip: Permit, Deny | Deny wins over permit when two policies disagree. 3.3.32 asks for least-privilege, and a permit that can override a deny is not … |
| Permissions | list or chips (count when long) | Which permissions this policy speaks to. A policy with an empty list speaks to all of them, which is powerful enough that it is worth being … |
| Applies to roles | list or chips (count when long) | — |
| Effective to | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Grant an asset action to a role (primary button) | `createAuthorisationPolicy` POST `/authorisation-policies` | AuthorisationPolicy | AuthorisationPolicy | — | opens modal first |

**Data it reads**: `listAuthorisationPolicies` (onLoad, Who may see which assets); `listRoles` (onLoad, The roles a policy applies to (appliesToRoleIds), by name)

**Where the user goes next**

- → `CMS-081` DAM Governance & Rights Command Center: *Back to DAM Governance & Rights Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The role-based asset access list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the role-based asset access untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No role-based asset access yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the role-based asset access are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PERMISSION_VIEW`, which `listAuthorisationPolicies` requires to show this screen, and names that permission (the screen's other reads need `ROLE_MANAGE` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PERMISSION_MANAGE` for `createAuthorisationPolicy`. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds PERMISSION_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: PERMISSION_MANAGE for createAuthorisationPolicy. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/identity.yaml#createAuthorisationPolicy)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listAuthorisationPolicies (AuthorisationPolicy):
- code: AQC-AUH
  name: AquaCove Abu Dhabi
  description: Guest charged twice at Main Gate Till 3
  isTemplate: true
  combining: allMustMatch
  effect: permit
- code: AQC-DXB
  name: Main Gate Till 3
  description: Group of 40 from Desert Gate Tours
  isTemplate: false
  combining: anyMayMatch
  effect: deny
```

#### Permissions

- `listAuthorisationPolicies` → `PERMISSION_VIEW` (read) · staff
- `createAuthorisationPolicy` → `PERMISSION_MANAGE` (configure) · staff
- `listRoles` → `ROLE_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PERMISSION_VIEW`, which `listAuthorisationPolicies` requires to show this screen, and names that permission (the screen's other reads need `ROLE_MANAGE` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PERMISSION_MANAGE` for `createAuthorisationPolicy`.

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.3.1 | Allows permissions to be granted dynamically based on attributes and context rather than fixed roles only. | Admission and Access | CONTRACTED | `createAuthorisationPolicy` |
| 3.3.5 | Dynamic Rule Engine Administrators shall configure access policies without software development. | Admission and Access | CONTRACTED | `createAuthorisationPolicy` |
| 7.1.44 | Provide a no-code visual interface for building access policies using conditions, rules, logic operators, approval requirements and reusable components. | F&B POS | CONTRACTED | `createAuthorisationPolicy` |
| 3.3.35 | Delegated Access Management - System shall support delegated administration of access policies. | Admission and Access | CONTRACTED | data `AuthorisationPolicy` |
| 3.3.40 | Tenant-Specific Policies - System shall support tenant-specific access policies. | Admission and Access | CONTRACTED | data `AuthorisationPolicy` |
| 3.3.42 | Cross-Venue Access Policies - System shall support policies spanning multiple venues. | Admission and Access | CONTRACTED | data `AuthorisationPolicy` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Role-based access controls who can discover, preview, download, edit, approve, share or manage assets. *(client request · MoM 11 Sep 2026, 4.3 Asset Governance, Rights, Approvals & Secure Sharing · DI-855)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S2** Role-based access control: role and permission matrix *(Chinmay Parab · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'permission matrix')*
- **A48** Update Employee App wireframe: remove the manual role-selection screen — role and home dashboard should be determined automatically from backend RBAC configuration immediately after login *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'rbac')*
- **A63** Design RBAC enhancements: a roles-comparison view for side-by-side permission auditing, and the POS session model (one user per workstation session, fully role-driven access with automatic front-end/"sales board" … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 12 Aug 2026 · workshop tracker · keyword 'rbac')*
- **A97** Document the RBAC role-permission matrix (edit/view · view-only · hidden, per role per module, sub-permissions, default templates) *(Chinmay Parab · High · Ongoing → 30 Sep: Closed, Rolled into S2 · 20 Aug 2026 · workshop tracker · keyword 'rbac')*
- **A130** Enforce venue-level admission capacity as superseding event capacity, with a blocking validation and an RBAC-gated override *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 25 Aug 2026 · workshop tracker · keyword 'rbac')*

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-086` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS46 Digital Asset Management DAM Board 3.dc.html#cms-086`
- Workshop pack: Digital Asset Management DAM.pdf board 3
- Flow F185 *Digital Asset Management DAM board 3: DAM Governance & Rights Command Center*, step 10: Works in Role-Based Asset Access & Permission Management → Control who can discover, view, edit, download, share, approve, or manage assets.
- ADR-0068 *Guest admission policy lives in Access only, and the offline package carries it* (`docs/adr/0068-guest-admission-policy-lives-in-access-only.md`)
- ADR-0051 *Every AI function ships on a baseline and learns per tenant; a model goes live only on evidence* (`docs/adr/0051-ai-ships-on-a-baseline-and-learns-per-tenant.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (24), with its required mark, default, format and its error state.
- [ ] Every output is drawn (5 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-086?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Grant an asset action to a role.
- [ ] Every transition is wired: `CMS-081`.
- [ ] Every gated control is gated: `PERMISSION_MANAGE`, `PERMISSION_VIEW`, `ROLE_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-087` Secure Internal & External Sharing

**Allow controlled sharing without users manually downloading assets and sending uncontrolled copies.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | Block B · task APP-CMS-CMS-087 |
| Who uses it | venue staff holding `ASSET_LIBRARY_SHARE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/media-library/secure-internal-external-sharing-cms-087` |

**Known gaps.** **The pack names 5 actions on this screen and the screen declares 0 operations.** Unserved: Copy Secure Link, Extend, Change Permission, Revoke, View Activity. Each needs an operation, or needs … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Secure share links with expiry and permission instead of downloads; extend, change or revoke, with activity.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** View + Download Approved Renditions. Each needs attaching to the control it gates, or the screen needs the control.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Copy Secure Link (primary button) | navigation or local | — | — | — | — |
| Extend (secondary button) | navigation or local | — | — | — | — |
| Change Permission (secondary button) | navigation or local | — | — | — | — |
| Revoke (destructive button) | navigation or local | — | — | — | — |
| View Activity (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `CMS-081` DAM Governance & Rights Command Center: *Back to DAM Governance & Rights Command Center*

**What opens over it**

- confirmDialog *Revoke*: **Revoke on a secure internal external is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The secure internal external list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the secure internal external untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No secure internal external yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the secure internal external are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
share: Summer 2026 press kit
recipient: press@gulfnews.example
permission: view and download
expires: 15/10/2026
views: 6
```

#### Permissions

- `createMediaShare` → `ASSET_LIBRARY_SHARE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Secure sharing: password-protected links, watermarking and download restrictions - e.g. an external agency can preview/download an approved rendition but not the original source file. *(client request · MoM 11 Sep 2026, 4.3 Asset Governance, Rights, Approvals & Secure Sharing · DI-856)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-087` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS46 Digital Asset Management DAM Board 3.dc.html#cms-087`
- Workshop pack: Digital Asset Management DAM.pdf board 3
- Flow F185 *Digital Asset Management DAM board 3: DAM Governance & Rights Command Center*, step 12: Works in Secure Internal & External Sharing → Allow controlled sharing without users manually downloading assets and sending uncontrolled copies.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-087?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Copy Secure Link, Extend, Change Permission, Revoke, View Activity.
- [ ] Every transition is wired: `CMS-081`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_SHARE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-088` Rights Expiry, Renewal & Usage Impact

**Prevent expired assets from continuing to be used across TICVAI channels.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | Block B · task APP-CMS-CMS-088 |
| Who uses it | venue staff holding `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | `assetId` (navigation) |
| Route | `/media-library/rights-expiry-renewal-usage-impact-cms-088` |

**Known gaps.** **The pack names 6 actions on this screen and the screen declares 0 operations.** Unserved: Renew Rights, Upload Renewal Document, Change Expiry, Find Replacement, Notify Owner, Expiry Workflow. Each … **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Assets whose rights expire in 7, 30 or 60 days or have expired, with live usages and renewal or replacement.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The table's columns are the workshop pack's labels with no bound response field (0 of 6 labels bound). (CHG-SGU-024)

**Fixed on main** (the package already carries these; draw what it says): "Example" and "DAM-IMG-008421" are table columns. (CHG-SGU-023).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Within days | number field (days) | 60 | — | `getExpiringRights` ?withinDays |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every rights expiry renewal** (data table)

| Shows | Format | Notes |
|---|---|---|
| Expires in 7 days | text | not in the schema: `Expires in 7 Days` |
| Expires in 30 days | text | not in the schema: `Expires in 30 Days` |
| Expires in 60 days | text | not in the schema: `Expires in 60 Days` |
| Expired | text | not in the schema: `Expired` |

**The selected rights expiry renewal** (detail panel): The pack groups this record's detail under its own headings: “Rights expire”, “Impact”, “Owner notification”, “Digital Asset Management”, “Escalation”, “Expired”.

| Shows | Format | Notes |
|---|---|---|
| Expires in 7 days | text | not in the schema: `Expires in 7 Days` |
| Expires in 30 days | text | not in the schema: `Expires in 30 Days` |
| Expires in 60 days | text | not in the schema: `Expires in 60 Days` |
| Expired | text | not in the schema: `Expired` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Renew Rights (primary button) | navigation or local | — | — | — | — |
| Upload Renewal Document (secondary button) | navigation or local | — | — | — | — |
| Change Expiry (secondary button) | navigation or local | — | — | — | — |
| Find Replacement (secondary button) | navigation or local | — | — | — | — |
| Notify Owner (secondary button) | navigation or local | — | — | — | — |
| Expiry Workflow (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getExpiringRights` (onLoad, What lapses, and what it would break)

**Where the user goes next**

- → `CMS-081` DAM Governance & Rights Command Center: *Back to DAM Governance & Rights Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rights expiry renewal list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rights expiry renewal untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rights expiry renewal yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rights expiry renewal are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds ASSET_LIBRARY_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: ASSET_LIBRARY_MANAGE for setMediaAssetRights. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/assets.yaml#setMediaAssetRights)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every rights expiry renewal:
- Expires in 7 Days: 46
  Expires in 30 Days: 312
  Expires in 60 Days: 312
  Expired: 5
  Example: 11
  DAM-IMG-008421: 57
- Expires in 7 Days: 312
  Expires in 30 Days: 74
  Expires in 60 Days: 74
  Expired: 1
  Example: 128
  DAM-IMG-008421: 11
- Expires in 7 Days: 74
  Expires in 30 Days: 19
  Expires in 60 Days: 19
  Expired: 3
  Example: 46
  DAM-IMG-008421: 128
```

#### Permissions

- `getExpiringRights` → `ASSET_LIBRARY_VIEW` (read) · staff
- `setMediaAssetRights` → `ASSET_LIBRARY_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 23.1.11 | System shall track asset ownership, copyright information, licensing terms, and expiration dates. | Digital Asset Management | CONTRACTED | `getExpiringRights` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Rights-expiry tracking flags expiring assets and shows where they are in use; audit trail records who extended an expiry and when; AI risk view highlights e.g. an asset expiring while active in several campaigns. *(client request · MoM 11 Sep 2026, 4.3 Asset Governance, Rights, Approvals & Secure Sharing · DI-857)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-088` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS46 Digital Asset Management DAM Board 3.dc.html#cms-088`
- Workshop pack: Digital Asset Management DAM.pdf board 3
- Flow F185 *Digital Asset Management DAM board 3: DAM Governance & Rights Command Center*, step 14: Works in Rights Expiry, Renewal & Usage Impact → Prevent expired assets from continuing to be used across TICVAI channels.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (8 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-088?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Renew Rights, Upload Renewal Document, Change Expiry, Find Replacement, Notify Owner, Expiry Workflow.
- [ ] Every transition is wired: `CMS-081`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-089` Governance Audit Trail & Compliance Evidence

**Provide complete traceability for asset governance.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | Block B · task APP-CMS-CMS-089 |
| Who uses it | venue staff holding `ASSET_LIBRARY_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Asset Uploaded) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `assetId` (navigation) |
| Route | `/media-library/governance-audit-trail-compliance-evidence-cms-089` |

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: Action. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Every governance action on assets (approval, rights change, share, delete) with who and when.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SGU-023).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| ↓ | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Action (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `CMS-081` DAM Governance & Rights Command Center: *Back to DAM Governance & Rights Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The governance audit trail configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the governance audit trail untouched. |
| Empty, first run (`?state=emptyFirstRun`) | Nothing here yet for Governance Audit Trail & Compliance Evidence. This screen only reads, so it offers no create action and says where the records come from. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
entries:
- 01/10/2026 10:02 Aisha Al Nuaimi approved Wave pool promo (Arabic).mp4
- 30/09/2026 16:44 Noura Al Hammadi changed rights expiry on Lazy river at sunset.jpg
```

#### Permissions

- `listMediaAssetAudit` → `ASSET_LIBRARY_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Rights-expiry tracking flags expiring assets and shows where they are in use; audit trail records who extended an expiry and when; AI risk view highlights e.g. an asset expiring while active in several campaigns. *(client request · MoM 11 Sep 2026, 4.3 Asset Governance, Rights, Approvals & Secure Sharing · DI-857)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-089` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS46 Digital Asset Management DAM Board 3.dc.html#cms-089`
- Workshop pack: Digital Asset Management DAM.pdf board 3
- Flow F185 *Digital Asset Management DAM board 3: DAM Governance & Rights Command Center*, step 16: Works in Governance Audit Trail & Compliance Evidence → Provide complete traceability for asset governance.

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-089?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Action.
- [ ] Every transition is wired: `CMS-081`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-090` Governance Risk, Compliance & AI Recommendations

**Provide a consolidated view of governance risks and use AI to help identify problems requiring human attention.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | Block B · task APP-CMS-CMS-090 |
| Who uses it | venue staff holding `ASSET_LIBRARY_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/media-library/governance-risk-compliance-ai-recommendations-cms-090` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Governance risks (no rights, expired in use, long-lived shares, missing evidence) with AI help.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The table's columns are the workshop pack's labels with no bound response field (0 of 10 labels bound). (CHG-SGU-024)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SGU-023).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Within days | number field (days) | 60 | — | `getExpiringRights` ?withinDays |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every governance risk compliance** (data table)

| Shows | Format | Notes |
|---|---|---|
| Assets without rights | text | not in the schema: `Assets Without Rights` |
| Expired assets | text | not in the schema: `Expired Assets` |
| Rights expiring | text | not in the schema: `Rights Expiring` |
| Unapproved assets | text | not in the schema: `Unapproved Assets` |
| Restricted assets in active usage | text | not in the schema: `Restricted Assets in Active Usage` |
| External shares | text | not in the schema: `External Shares` |
| Long lived shares | text | not in the schema: `Long-Lived Shares` |
| Missing evidence | text | not in the schema: `Missing Evidence` |
| Approval SLA breaches | text | not in the schema: `Approval SLA Breaches` |
| Risk queue | text | not in the schema: `Risk Queue` |

**The selected governance risk compliance** (detail panel): The pack groups this record's detail under its own headings: “Asset Risk Usage Severity Action”, “Digital Asset Management”, “Human Governance”, “Approved”, “However”, “Therefore”.

| Shows | Format | Notes |
|---|---|---|
| Assets without rights | text | not in the schema: `Assets Without Rights` |
| Expired assets | text | not in the schema: `Expired Assets` |
| Rights expiring | text | not in the schema: `Rights Expiring` |
| Unapproved assets | text | not in the schema: `Unapproved Assets` |
| Restricted assets in active usage | text | not in the schema: `Restricted Assets in Active Usage` |
| External shares | text | not in the schema: `External Shares` |
| Long lived shares | text | not in the schema: `Long-Lived Shares` |
| Missing evidence | text | not in the schema: `Missing Evidence` |
| Approval SLA breaches | text | not in the schema: `Approval SLA Breaches` |
| Risk queue | text | not in the schema: `Risk Queue` |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** ↓. Each needs attaching to the control it gates, or the screen needs the control.

**Data it reads**: `getExpiringRights` (onLoad, Risk from lapsing rights)

**Where the user goes next**

- → `CMS-081` DAM Governance & Rights Command Center: *Back to DAM Governance & Rights Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The governance risk compliance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the governance risk compliance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | Nothing here yet for Governance Risk, Compliance & AI Recommendations. This screen only reads, so it offers no create action and says where the records come from. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the governance risk compliance are still there. The pack's own statuses are 🟢 Valid — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every governance risk compliance:
- Assets Without Rights: 233
  Expired Assets: 128
  Rights Expiring: 11
  Unapproved Assets: 128
  Restricted Assets in Active Usage: 3 h 20 min
  External Shares: 11
  Long-Lived Shares: 46
  Missing Evidence: 0
- Assets Without Rights: 57
  Expired Assets: 42
  Rights Expiring: 128
  Unapproved Assets: 42
  Restricted Assets in Active Usage: 42 min
  External Shares: 128
  Long-Lived Shares: 312
  Missing Evidence: 5
- Assets Without Rights: 11
  Expired Assets: 7
  Rights Expiring: 46
  Unapproved Assets: 7
  Restricted Assets in Active Usage: 1.8 s
  External Shares: 46
  Long-Lived Shares: 74
  Missing Evidence: 1
```

#### Permissions

- `getExpiringRights` → `ASSET_LIBRARY_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 23.1.11 | System shall track asset ownership, copyright information, licensing terms, and expiration dates. | Digital Asset Management | CONTRACTED | `getExpiringRights` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Rights-expiry tracking flags expiring assets and shows where they are in use; audit trail records who extended an expiry and when; AI risk view highlights e.g. an asset expiring while active in several campaigns. *(client request · MoM 11 Sep 2026, 4.3 Asset Governance, Rights, Approvals & Secure Sharing · DI-857)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-090` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS46 Digital Asset Management DAM Board 3.dc.html#cms-090`
- Workshop pack: Digital Asset Management DAM.pdf board 3
- Flow F185 *Digital Asset Management DAM board 3: DAM Governance & Rights Command Center*, step 18: Works in Governance Risk, Compliance & AI Recommendations → Provide a consolidated view of governance risks and use AI to help identify problems requiring human attention.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-090?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `CMS-081`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
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

**10 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createAuthorisationPolicy": {"method":"POST","path":"/authorisation-policies","contract":"identity","summary":"Write a policy without writing code","permission":"PERMISSION_MANAGE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AuthorisationPolicy","responds":"AuthorisationPolicy"},
"createMediaShare": {"method":"POST","path":"/media-shares","contract":"assets","summary":"Share assets with somebody outside the platform, on terms","permission":"ASSET_LIBRARY_SHARE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MediaShare","responds":"MediaShare"},
"getExpiringRights": {"method":"GET","path":"/media/rights-expiring","contract":"assets","summary":"Assets whose licence is expiring or expired","permission":"ASSET_LIBRARY_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"withinDays","in":"query","required":null}],"requestBody":null,"responds":"ExpiringMedia"},
"getMediaAsset": {"method":"GET","path":"/media/{mediaId}","contract":"assets","summary":"Read an asset with derivatives and usage","permission":"ASSET_LIBRARY_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"MediaAssetDetail"},
"getMediaUsageAnalytics": {"method":"GET","path":"/media-usage","contract":"assets","summary":"Downloads, views, shares and library health","permission":"ASSET_LIBRARY_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"MediaUsageRow"},
"listAuthorisationPolicies": {"method":"GET","path":"/authorisation-policies","contract":"identity","summary":"Attribute-based authorisation policies","permission":"PERMISSION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"scopePath","in":"query","required":null}],"requestBody":null,"responds":"AuthorisationPolicy"},
"listMediaAssetAudit": {"method":"GET","path":"/media-assets/{assetId}/audit","contract":"assets","summary":"Who did what to this asset, and who received it","permission":"ASSET_LIBRARY_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"MediaAuditRecord"},
"listRoles": {"method":"GET","path":"/roles","contract":"identity","summary":"List roles","permission":"ROLE_MANAGE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"setMediaAssetApproval": {"method":"POST","path":"/media-assets/{assetId}/approval","contract":"assets","summary":"Submit, approve, reject or publish an asset","permission":"ASSET_LIBRARY_APPROVE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MediaAssetApproval"},
"setMediaAssetRights": {"method":"PUT","path":"/media-assets/{assetId}/rights","contract":"assets","summary":"Licence, permitted use and expiry","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MediaRights","responds":"MediaRights"},
"updateMediaAsset": {"method":"PATCH","path":"/media/{mediaId}","contract":"assets","summary":"Amend metadata, tags or rights","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MediaAsset"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessCondition": {"type":"object","description":"**One attribute, one operator, one value** — and the attribute names are an enum rather than free text, because a policy that reads `venu.type` silently never matches.\nThe enum is the matrix, row by row: user (3.3.7), employee (3.3.8), membership (3.3.9), accreditation (3.3.10), customer segment (3.3.11), resource classification (3.3.12), venue (3.3.13), attraction (3.3.14), device (3.3.15), day of week (3.3.16), season (3.3.17), event (3.3.18), capacity (3.3.19), occupancy (3.3.20), risk score (3.3.21), location (3.3.2) and time (3.3.3).\n","required":["attribute","operator"],"properties":{"attribute":{"type":"string","enum":["user.attribute","employee.attribute","employee.onShift","membership.tier","membership.status","accreditation.type","accreditation.status","customer.segment","resource.classification","venue.attribute","venue.id","attraction.attribute","device.kind","device.id","device.trusted","time.ofDay","time.dayOfWeek","time.season","time.withinOperatingHours","event.id","event.status","capacity.utilisationPercent","occupancy.level","risk.score","ticket.status","location.scopePath"]},"key":{"type":"string","nullable":true,"description":"For the `*.attribute` forms — which attribute, by code."},"operator":{"type":"string","enum":["equals","notEquals","in","notIn","greaterThan","lessThan","between","contains","startsWith","exists"]},"value":{"nullable":true,"description":"The single comparand for `equals`, `notEquals`, `greaterThan`, `lessThan`, `contains` and `startsWith` — a string, number or boolean, by the attribute. Null for `exists`; `in`, `notIn` and `between` use `values`.\n"},"values":{"type":"array","items":{"type":"string"}}}},
"AuthorisationPolicy": {"type":"object","x-ticvai-persistence":"identity.authorisation_policy","description":"3.3. **Conditions and an effect, evaluated by one engine.** A role says who you are; a policy says under what circumstances that is enough.\n\n**Which of the two policy engines this is** (stated 29 September, build pass). The package has two: this one, and the access contract's `AccessDynamicPolicy` (`access.dynamic_policy`). **This one governs who may do what in the software**: a principal's permissions on operations and screens (`permissions` names them), narrowed or extended by who, where, when and on what device, and decided by `evaluateAccess`. **`AccessDynamicPolicy` governs who may pass which gate**: a guest's, holder's or employee's admission at an access point, decided in the gate's validation with results such as `requireId` or `requireSupervisor` that mean nothing to a permission check. A staff member's badge opening a staff door is a gate decision (access); the same staff member approving a refund is a permission decision (here).\n**Settled by ADR-0068 (accepted 1 October): guest admission lives in Access only.** This engine keeps staff authorisation and was renamed to say so: `identity.access_policy` became `identity.authorisation_policy`, its versions `identity.authorisation_policy_version`, and its operations `*AuthorisationPolicy*`. \"Access policy\" now means `AccessDynamicPolicy` and nothing else.\n","required":["code","name","effect"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"Assigned by the server on `createAuthorisationPolicy`; the path names the policy on update."},"code":{"type":"string"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"isTemplate":{"type":"boolean","default":false},"permissions":{"type":"array","items":{"type":"string"},"description":"**Which permissions this policy speaks to.** A policy with an empty list speaks to all of them, which is powerful enough that it is worth being explicit about.\n"},"conditions":{"type":"array","x-ticvai-persistence-column":"jsonb","items":{"$ref":"#/components/schemas/AccessCondition"}},"combining":{"type":"string","enum":["allMustMatch","anyMayMatch"],"default":"allMustMatch"},"effect":{"type":"string","enum":["permit","deny"],"description":"**Deny wins over permit when two policies disagree.** 3.3.32 asks for least-privilege, and a permit that can override a deny is not least-privilege by any reading — it is the union of every mistake anybody has made.\n"},"priority":{"type":"integer","default":0},"scopePath":{"type":"string","description":"3.3.40 to 3.3.43. **Tenant, venue and cross-venue policies are one mechanism**, because `scope_path` is prefix-comparable — `uae.dubai` contains `uae.dubai.marina` — and inheritance is the prefix walk rather than a second table.\n"},"appliesToRoleIds":{"type":"array","items":{"type":"string","format":"uuid"}},"status":{"type":"string","readOnly":true,"description":"**Moved only by `setAuthorisationPolicyState`.** A policy is created as a `draft`, and a status sent in a create or update body is ignored — otherwise a write could skip the approval 3.3.26 requires.\n","enum":["draft","pendingApproval","active","suspended","retired"]},"version":{"type":"integer","default":1,"readOnly":true,"description":"Set by the server; every `updateAuthorisationPolicy` writes a new version."},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"effectiveTo":{"type":"string","format":"date-time","nullable":true},"delegatedAdminRoleIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"3.3.35. **Who may edit this policy without being a platform administrator.** A venue manager tuning their own opening-hours rule should not need someone who can edit every tenant's.\n"}}},
"ExpiringMedia": {"x-ticvai-persistence":"none — computed","type":"object","required":["assetId","filename","validTo","isExpired","isInUse"],"properties":{"assetId":{"type":"string","format":"uuid"},"filename":{"type":"string"},"thumbnailUrl":{"type":"string","nullable":true},"licensor":{"type":"string","nullable":true},"validTo":{"type":"string","format":"date"},"daysRemaining":{"type":"integer"},"isExpired":{"type":"boolean"},"isInUse":{"type":"boolean","description":"True while `liveUsageCount` is above zero, that is, while live (published) content references the asset (audit R106 (10)). Drafts and collections do not count."},"liveUsageCount":{"type":"integer","description":"References from live (published) content only (audit R106 (10)). Expired and live is the combination that matters."}}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"MediaAsset": {"x-ticvai-persistence":"assets.media_asset","type":"object","required":["id","kind","status","filename","contentType","sizeBytes","referenceCount","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/MediaKind"},"status":{"$ref":"#/components/schemas/MediaStatus"},"filename":{"type":"string"},"contentType":{"type":"string"},"sizeBytes":{"type":"integer"},"title":{"$ref":"#/components/schemas/LocalisedText"},"description":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"Set by `updateMediaAsset` and matched by `searchMedia`'s `search`. It was accepted and searched on before it had anywhere to be stored.\n"},"altText":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"Required before use in a guest-facing surface. WCAG 2.2 AA."},"width":{"type":"integer","nullable":true},"height":{"type":"integer","nullable":true},"durationSeconds":{"type":"number","nullable":true},"customMetadata":{"type":"object","nullable":true,"additionalProperties":true,"description":"BL-178. **`assets` is a strong contract and its metadata was fixed** — kind, title, alt text, dimensions, rights. A venue photographing four thousand products wants its own fields: shoot date, photographer, model release, season.\n**Free-form and searchable, not a schema.** Every venue would want a different one, and a fixed set would be wrong for all of them.\n"},"sharedWithTenantIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"BL-178. **Cross-tenant sharing, and it is refused by default for a reason.** A brand operating three venues wants one logo library; two unrelated tenants sharing an asset store is the isolation breach ADR-0011 exists to prevent.\n**Only within one tenant's own scope tree.** A share naming a tenant outside it is refused rather than warned about — this is the one place where a permissive default would be a cross-tenant data leak.\n"},"tags":{"type":"array","items":{"type":"string"}},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"The asset's category, one of `MediaTaxonomy.categories[].id`; null while unclassified. Set by `bulkUpdateMediaAssets` (`setCategoryId`) (decided 29 September, data model DM4).\n"},"venueId":{"type":"string","format":"uuid","nullable":true},"url":{"type":"string","description":"Signed and expiring for private assets; stable CDN URL for public ones."},"thumbnailUrl":{"type":"string","nullable":true},"referenceCount":{"type":"integer","description":"How many surfaces reference this asset. Non-zero refuses deletion.\n"},"rights":{"$ref":"#/components/schemas/MediaRights"},"isRightsExpired":{"type":"boolean"},"version":{"type":"integer"},"uploadedByPrincipalId":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"}}},
"MediaAssetApproval": {"type":"object","x-ticvai-persistence":"assets.approval","description":"Boards 3.4 and 3.5. **Publication eligibility is computed from four facts.**","properties":{"assetId":{"type":"string","format":"uuid"},"state":{"type":"string","enum":["draft","pendingApproval","approved","rejected","published","archived"]},"eligibility":{"type":"array","readOnly":true,"items":{"type":"object","properties":{"check":{"type":"string","enum":["approved","rightsCurrent","renditionsReady","classificationComplete"]},"satisfied":{"type":"boolean"},"detail":{"type":"string","nullable":true}}}},"approvedBy":{"type":"string","format":"uuid","nullable":true},"comment":{"type":"string","nullable":true},"at":{"type":"string","format":"date-time"},"scopePath":{"type":"string"}}},
"MediaAssetDetail": {"x-ticvai-persistence":"assets.media_asset","allOf":[{"$ref":"#/components/schemas/MediaAsset"},{"type":"object","properties":{"derivatives":{"type":"array","description":"Generated from the original, never uploaded separately. A new breakpoint is a re-render rather than a re-upload of everything.\n","items":{"type":"object","properties":{"label":{"type":"string"},"width":{"type":"integer"},"height":{"type":"integer"},"sizeBytes":{"type":"integer"},"url":{"type":"string"}}}},"usage":{"type":"array","description":"Every place this asset is referenced.","items":{"$ref":"#/components/schemas/MediaUsage"}},"collections":{"type":"array","items":{"type":"object","properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"}}}},"previousVersions":{"type":"array","items":{"type":"object","properties":{"version":{"type":"integer"},"replacedAt":{"type":"string","format":"date-time"},"replacedByPrincipalId":{"type":"string","format":"uuid"}}}}}}]},
"MediaAuditRecord": {"type":"object","x-ticvai-persistence":"assets.audit","description":"Board 3.9. **Distribution as well as edits** — the question asked afterwards is who had it.\n","properties":{"id":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"},"action":{"type":"string","enum":["uploaded","updated","retagged","versioned","approved","published","shared","downloaded","delivered","archived","deleted"]},"actorId":{"type":"string","format":"uuid","nullable":true},"recipient":{"type":"string","nullable":true},"detail":{"type":"string","nullable":true},"scopePath":{"type":"string"}}},
"MediaKind": {"type":"string","enum":["image","video","audio","document","vector","font","archive","model3d"],"description":"`model3d` added 3 October 2026 (r1 additions; ADR-0069 action item 4): a glTF binary (`model/gltf-binary`, `.glb`) venue model, at most 40 MB. No rendition or derivative is generated for it; the guest app downloads the file as uploaded.\n"},
"MediaRights": {"x-ticvai-persistence":"none — embedded in asset","type":"object","description":"Licensing terms. Tracked because an expired licence on a live surface is a legal exposure, not a housekeeping item.\n","properties":{"licenceKind":{"type":"string","enum":["owned","royaltyFree","rightsManaged","creativeCommons","editorialOnly","unknown"]},"licensor":{"type":"string","nullable":true},"licenceReference":{"type":"string","nullable":true},"validFrom":{"type":"string","format":"date","nullable":true},"validTo":{"type":"string","format":"date","nullable":true},"permittedUses":{"type":"array","items":{"type":"string","enum":["web","print","socialMedia","inVenue","advertising","internal"]}},"attributionRequired":{"type":"boolean","default":false},"attributionText":{"type":"string","nullable":true},"permittedTerritories":{"type":"array","items":{"type":"string"},"description":"ISO country or region codes. **Empty means unrestricted, which is a claim rather than an absence** — an unknown territory and a worldwide licence are not the same thing, and `licenceKind: unknown` is how the second is said.\n"},"permittedChannels":{"type":"array","items":{"type":"string"},"description":"Distribution channel codes, checked by `setMediaDistributionChannels`. Narrower than `permittedUses`, which describes the medium rather than the route.\n"},"modelReleaseHeld":{"type":"boolean","default":false},"renewalOwner":{"type":"string","format":"uuid","nullable":true}}},
"MediaShare": {"type":"object","x-ticvai-persistence":"assets.share","description":"Board 3.7. **A licence grant with a link attached** — revocable, expiring and logged.","required":["assetIds","expiresAt"],"properties":{"id":{"type":"string","format":"uuid"},"assetIds":{"type":"array","items":{"type":"string","format":"uuid"}},"recipientEmail":{"type":"string","nullable":true},"recipientOrganisation":{"type":"string","nullable":true},"allowDownload":{"type":"boolean","default":false},"allowedRenditions":{"type":"array","items":{"type":"string"}},"passwordProtected":{"type":"boolean","default":false},"expiresAt":{"type":"string","format":"date-time"},"revokedAt":{"type":"string","format":"date-time","nullable":true},"url":{"type":"string","readOnly":true},"openedCount":{"type":"integer","readOnly":true},"scopePath":{"type":"string"}}},
"MediaStatus": {"type":"string","enum":["processing","ready","quarantined","failed","archived"]},
"MediaUsage": {"x-ticvai-persistence":"assets.media_usage","type":"object","description":"One place an asset is used. **`surface: product` is written by catalogue** for each item of `Product.media` (decided 29 September, rev 3 23SEP-4): `referenceId` is the product id and `isLive` is true while the product is listed to guests, which is what stops an asset in use on a ticket card being archived from under it.\n","required":["surface","referenceId"],"properties":{"extractedText":{"type":"string","description":"**Text pulled out of an uploaded document**, after extraction. The generic retrieval path for anything a tenant uploads — a PDF nobody can search is a PDF nobody reads.\n"},"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"surface":{"type":"string","enum":["tenantBranding","homepageBanner","promoBlock","contentPage","product","event","menuItem","merchandise","workOrder","incident","inspection","campaign"]},"referenceId":{"type":"string"},"label":{"type":"string"},"isLive":{"type":"boolean","description":"True where the referencing surface is published to guests."}}},
"MediaUsageRow": {"type":"object","description":"Boards 1.10 and 4.9. **Assets never used is the number that justifies the library.**","properties":{"key":{"type":"string"},"label":{"type":"string"},"assetCount":{"type":"integer"},"storageBytes":{"type":"integer"},"downloads":{"type":"integer"},"views":{"type":"integer"},"shares":{"type":"integer"},"neverUsedCount":{"type":"integer"},"unclassifiedCount":{"type":"integer"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Role": {"x-ticvai-persistence":"identity.role","type":"object","required":["id","code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","x-ticvai-unique":"tenant","description":"**Unique within the tenant** (decided 28 September, audit R108). A seeded role's code is reserved in every tenant. Unique per tenant, not per venue, because a grant names a role anywhere in the tree; `createRole` refuses a duplicate with `409 duplicate-code`.\n"},"name":{"type":"string"},"description":{"type":"string"},"permissions":{"type":"array","description":"**A role that grants no permissions is not a role.** `Role` carried a code, a name and two counts until 18 August, and `identity.role_permission` derived from it with exactly one column — `role_id`. **A join table that joins to nothing**, found by Hrushikant in review and missed by the schema audit that ran the same day.\n**The audit asked whether every table had columns, a relationship and an owner, and this table had all three.** What it did not ask is whether a table with one column can do the job its name claims.\n","items":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission"}},"inheritsFromRoleId":{"type":"string","format":"uuid","nullable":true,"description":"**Role composition, one level deep and no deeper.** A supervisor role that is a cashier plus three permissions is how venues actually describe them.\n**Cycles are refused and depth is capped at one**, because a permission set nobody can read off the screen is a permission set nobody audits.\n"},"isSystem":{"type":"boolean","default":false,"description":"**Seeded roles ship and are editable; deleting one is refused.** A venue that removes `cashier` and rebuilds it has two roles with one name in the audit log.\n**The seeded system roles are Cashier, Supervisor, Venue Manager, Finance and Tenant Admin** (proposed in `docs/active/seed-data-proposal.md` section 2, client to correct; audit R229).\n\n**Superseded 2 October 2026: no fixed default roles** (Chinmay; DEC-007; CHG-CSP-003). The five are presets (`CapabilityTemplate`, `isPreset`) a role starts from, not roles a tenant is given. The field stays for clients built at r1 and is false on every role created from 2 October.\n"},"presetCode":{"type":"string","nullable":true,"readOnly":true,"maxLength":64,"description":"**The preset this role was started from, for the record only** (decided 2 October 2026, Chinmay; DEC-007; CHG-CSP-003): the first of `createRole.presetCodes`, or null for a role ticked by hand. It binds nothing; a later edit of the preset never changes this role.\n"},"principalCount":{"type":"integer"},"grantCount":{"type":"integer"}}}
}
```
