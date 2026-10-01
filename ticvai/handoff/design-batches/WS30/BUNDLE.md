# WS30 — Membership   Annual Pass Management board 2

**10 screens · 9 operations · 15 schemas · 4 permissions**

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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `APPROVAL_REQUEST, GUEST_MANAGE, ORDER_MODIFY, PRODUCT_CONFIGURE`. A control nobody can use must say so,
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

## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `BO-294` | Member Operations Command Center | B–D | 2 | 24 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-295` | Member 360° Membership Account Workspace | B–D | 0 | 48 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `BO-296` | Membership Activation, Assignment & Credential Management | B–D | 5 | 12 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-297` | Visit, Admission & Entitlement Usage Monitor | B–D | 0 | 2 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `BO-298` | Membership Freeze, Suspension & Reactivation Management | B–D | 7 | 0 | 5 | 4 | 1 | 0 | — | notStarted (generated) |
| `BO-299` | Membership Upgrade, Downgrade & Product Migration Operations | B–D | 4 | 0 | 6 | 2 | 1 | 0 | — | notStarted (generated) |
| `BO-300` | Renewal Operations & Auto-Renewal Management | B–D | 0 | 20 | 6 | 1 | 0 | 0 | — | notStarted (generated) |
| `BO-301` | Member Exceptions, Overrides & Service Recovery | B–D | 6 | 0 | 6 | 7 | 0 | 0 | — | notStarted (generated) |
| `BO-302` | Member Lifecycle History, Audit & Case Timeline | B–D | 0 | 8 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-303` | Membership Analytics, Renewal Intelligence & AI Retention Center | B–D | 2 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**BO-300, BO-302 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-294` Member Operations Command Center

**Provide membership teams with a real-time operational dashboard for the complete active member population.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/sell/member-operations-command-center-bo-294` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search member operations | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by venue, product, tier, status, member type, activation and 5 more — which are present is a decision the pack already made. | — |

#### Outputs: what the screen shows and produces

**Shown**

**Active Members** (metric tile, from `listMember`)

**New Members Today** (metric tile, from `listMember`)

**Activated Today** (metric tile, from `listMember`)

**Pending Activation** (metric tile, from `listMember`)

**Expiring in 30 Days** (metric tile, from `listMember`)

**Renewal due** (metric tile, from `listMember`)

**Renewed This Month** (metric tile, from `listMember`)

**Renewal rate** (metric tile, from `listMember`)

**Suspended Memberships** (metric tile, from `listMember`)

**Frozen Memberships** (metric tile, from `listMember`)

**Membership Exceptions** (metric tile, from `listMember`)

**At risk members** (metric tile, from `listMember`)

**Every member operations** (data table, from `listMember`)

| Shows | Format | Notes |
|---|---|---|
| Membership ID | text | not in the schema: `MemberOperationsCommandCenterView.membershipId` |
| Member | text | not in the schema: `MemberOperationsCommandCenterView.member` |
| Membership product | text | not in the schema: `MemberOperationsCommandCenterView.membershipProduct` |
| Tier | text | not in the schema: `MemberOperationsCommandCenterView.tier` |
| Venue | text | not in the schema: `MemberOperationsCommandCenterView.venue` |
| Activation date | text | not in the schema: `MemberOperationsCommandCenterView.activationDate` |
| Expiry date | text | not in the schema: `MemberOperationsCommandCenterView.expiryDate` |
| Membership status | text | not in the schema: `MemberOperationsCommandCenterView.membershipStatus` |
| Usage level | text | not in the schema: `MemberOperationsCommandCenterView.usageLevel` |
| Renewal status | text | not in the schema: `MemberOperationsCommandCenterView.renewalStatus` |
| Outstanding issue | text | not in the schema: `MemberOperationsCommandCenterView.outstandingIssue` |
| Owner | text | not in the schema: `MemberOperationsCommandCenterView.owner` |

**The selected member operations** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Membership ID | text | not in the schema: `MemberOperationsCommandCenterView.membershipId` |
| Member | text | not in the schema: `MemberOperationsCommandCenterView.member` |
| Membership product | text | not in the schema: `MemberOperationsCommandCenterView.membershipProduct` |
| Tier | text | not in the schema: `MemberOperationsCommandCenterView.tier` |
| Venue | text | not in the schema: `MemberOperationsCommandCenterView.venue` |
| Activation date | text | not in the schema: `MemberOperationsCommandCenterView.activationDate` |
| Expiry date | text | not in the schema: `MemberOperationsCommandCenterView.expiryDate` |
| Membership status | text | not in the schema: `MemberOperationsCommandCenterView.membershipStatus` |
| Usage level | text | not in the schema: `MemberOperationsCommandCenterView.usageLevel` |
| Renewal status | text | not in the schema: `MemberOperationsCommandCenterView.renewalStatus` |
| Outstanding issue | text | not in the schema: `MemberOperationsCommandCenterView.outstandingIssue` |
| Owner | text | not in the schema: `MemberOperationsCommandCenterView.owner` |

**Data it reads**: `listMember` (onLoad, Member Operations Command Center)

**Where the user goes next**

- → `BO-100` Venue Home: *Venue Home*
- → `BO-297` Visit, Admission & Entitlement Usage Monitor: *Works in Visit, Admission & Entitlement Usage Monitor*; calls `listMember`
- → `BO-298` Membership Freeze, Suspension & Reactivation Management: *Works in Membership Freeze, Suspension & Reactivation Management*; calls `listMember`
- → `BO-302` Member Lifecycle History, Audit & Case Timeline: *Works in Member Lifecycle History, Audit & Case Timeline*; calls `listMember`
- → `BO-303` Membership Analytics, Renewal Intelligence & AI Retention Center: *Works in Membership Analytics, Renewal Intelligence & AI Retention Center*; calls `listMember`
- → `BO-295` Member 360° Membership Account Workspace: *Works in Member 360° Membership Account Workspace*; carries `membershipId`; calls `listMember`
- → `BO-296` Membership Activation, Assignment & Credential Management: *Works in Membership Activation, Assignment & Credential Management*; carries `membershipId`; calls `listMember`
- → `BO-299` Membership Upgrade, Downgrade & Product Migration Operations: *Works in Membership Upgrade, Downgrade & Product Migration Operations*; carries `membershipId`; calls `listMember`
- → `BO-300` Renewal Operations & Auto-Renewal Management: *Works in Renewal Operations & Auto-Renewal Management*; carries `membershipId`; calls `listMember`
- → `BO-301` Member Exceptions, Overrides & Service Recovery: *Works in Member Exceptions, Overrides & Service Recovery*; carries `membershipId`; calls `listMember`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The member operations list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the member operations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No member operations yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the member operations are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-294` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS83 Membership   Annual Pass Management Board 2.dc.html#bo-294`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 2
- Flow F139 *Membership Annual Pass Management board 2: Member Operations Command Center*, step 1: Opens Member Operations Command Center → Provide membership teams with a real-time operational dashboard for the complete active member population.
- Flow F139 *Membership Annual Pass Management board 2: Member Operations Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F139 *Membership Annual Pass Management board 2: Member Operations Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F139 *Membership Annual Pass Management board 2: Member Operations Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F139 *Membership Annual Pass Management board 2: Member Operations Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F139 *Membership Annual Pass Management board 2: Member Operations Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F139 *Membership Annual Pass Management board 2: Member Operations Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F139 *Membership Annual Pass Management board 2: Member Operations Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F139 branch at step 1 (expected): when Nothing has been set up on Member Operations Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F139 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-294?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-297`, `BO-298`, `BO-302`, `BO-303`, `BO-295`, `BO-296`, `BO-299`, `BO-300`, `BO-301`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-295` Member 360° Membership Account Workspace

**Provide a complete operational view of an individual member and their membership contract. This should be the primary screen an authorized membership-service agent opens when helping a member.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Show) and no metric row |
| Offline | online only |
| Opens with | `membershipId` (navigation) · cold entry: Opened from BO-294 with the membership picked there. Opened cold (a bookmark or a refresh), it shows the list to pick from rather than an empty record, and … |
| Route | `/sell/member-360-membership-account-workspace-bo-295` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every member 360° membership** (data table, from `setMemberMembershipAccount`)

| Shows | Format | Notes |
|---|---|---|
| Member name | text | not in the schema: `Member360MembershipAccountWorkspaceView.memberName` |
| Customer ID | text | not in the schema: `Member360MembershipAccountWorkspaceView.customerId` |
| Membership ID | text | not in the schema: `Member360MembershipAccountWorkspaceView.membershipId` |
| Membership product | text | not in the schema: `Member360MembershipAccountWorkspaceView.membershipProduct` |
| Tier | text | not in the schema: `Member360MembershipAccountWorkspaceView.tier` |
| Status | text | not in the schema: `Member360MembershipAccountWorkspaceView.status` |
| Activation date | text | not in the schema: `Member360MembershipAccountWorkspaceView.activationDate` |
| Expiry date | text | not in the schema: `Member360MembershipAccountWorkspaceView.expiryDate` |
| Renewal status | text | not in the schema: `Member360MembershipAccountWorkspaceView.renewalStatus` |
| Primary venue | text | not in the schema: `Member360MembershipAccountWorkspaceView.primaryVenue` |
| Credential status | text | not in the schema: `Member360MembershipAccountWorkspaceView.credentialStatus` |
| Primary member | text | not in the schema: `Member360MembershipAccountWorkspaceView.primaryMember` |
| Secondary adult | text | not in the schema: `Member360MembershipAccountWorkspaceView.secondaryAdult` |
| Dependents | text | not in the schema: `Member360MembershipAccountWorkspaceView.dependents` |
| Shared benefits | text | not in the schema: `Member360MembershipAccountWorkspaceView.sharedBenefits` |
| Individual benefits | text | not in the schema: `Member360MembershipAccountWorkspaceView.individualBenefits` |
| Membership version | text | not in the schema: `Member360MembershipAccountWorkspaceView.membershipVersion` |
| Purchase date | text | not in the schema: `Member360MembershipAccountWorkspaceView.purchaseDate` |
| Purchase channel | text | not in the schema: `Member360MembershipAccountWorkspaceView.purchaseChannel` |
| Original order | text | not in the schema: `Member360MembershipAccountWorkspaceView.originalOrder` |
| Validity | text | not in the schema: `Member360MembershipAccountWorkspaceView.validity` |
| Activation method | text | not in the schema: `Member360MembershipAccountWorkspaceView.activationMethod` |
| Renewal policy | text | not in the schema: `Member360MembershipAccountWorkspaceView.renewalPolicy` |
| Auto renew status | text | not in the schema: `Member360MembershipAccountWorkspaceView.autoRenewStatus` |

**The selected member 360° membership** (detail panel): The pack groups this record's detail under its own headings: “Guest Tickets”, “Free Parking”, “F&B Benefit”, “Retail Benefit”, “Link to”.

| Shows | Format | Notes |
|---|---|---|
| Member name | text | not in the schema: `Member360MembershipAccountWorkspaceView.memberName` |
| Customer ID | text | not in the schema: `Member360MembershipAccountWorkspaceView.customerId` |
| Membership ID | text | not in the schema: `Member360MembershipAccountWorkspaceView.membershipId` |
| Membership product | text | not in the schema: `Member360MembershipAccountWorkspaceView.membershipProduct` |
| Tier | text | not in the schema: `Member360MembershipAccountWorkspaceView.tier` |
| Status | text | not in the schema: `Member360MembershipAccountWorkspaceView.status` |
| Activation date | text | not in the schema: `Member360MembershipAccountWorkspaceView.activationDate` |
| Expiry date | text | not in the schema: `Member360MembershipAccountWorkspaceView.expiryDate` |
| Renewal status | text | not in the schema: `Member360MembershipAccountWorkspaceView.renewalStatus` |
| Primary venue | text | not in the schema: `Member360MembershipAccountWorkspaceView.primaryVenue` |
| Credential status | text | not in the schema: `Member360MembershipAccountWorkspaceView.credentialStatus` |
| Primary member | text | not in the schema: `Member360MembershipAccountWorkspaceView.primaryMember` |
| Secondary adult | text | not in the schema: `Member360MembershipAccountWorkspaceView.secondaryAdult` |
| Dependents | text | not in the schema: `Member360MembershipAccountWorkspaceView.dependents` |
| Shared benefits | text | not in the schema: `Member360MembershipAccountWorkspaceView.sharedBenefits` |
| Individual benefits | text | not in the schema: `Member360MembershipAccountWorkspaceView.individualBenefits` |
| Membership version | text | not in the schema: `Member360MembershipAccountWorkspaceView.membershipVersion` |
| Purchase date | text | not in the schema: `Member360MembershipAccountWorkspaceView.purchaseDate` |
| Purchase channel | text | not in the schema: `Member360MembershipAccountWorkspaceView.purchaseChannel` |
| Original order | text | not in the schema: `Member360MembershipAccountWorkspaceView.originalOrder` |
| Validity | text | not in the schema: `Member360MembershipAccountWorkspaceView.validity` |
| Activation method | text | not in the schema: `Member360MembershipAccountWorkspaceView.activationMethod` |
| Renewal policy | text | not in the schema: `Member360MembershipAccountWorkspaceView.renewalPolicy` |
| Auto renew status | text | not in the schema: `Member360MembershipAccountWorkspaceView.autoRenewStatus` |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Activate, Freeze, Suspend, Resume, Renew, Replace Credential, Add Note, Review Eligibility, Manage Dependents. Each needs attaching to the control it gates, or the screen needs the control.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-294` Member Operations Command Center: *Returns to the board's landing screen*; calls `setMemberMembershipAccount`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The member 360° membership list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the member 360° membership untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No member 360° membership yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the member 360° membership are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The benefit is exhausted for this period, or the membership is not active |

#### Permissions

- `recordBenefitUsage` → `GUEST_MANAGE` (configure) · staff, service

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- B2B account financial tab shows credit limit, credit days and a linked account-specific price list; accounts can be a main account with child (agent) accounts; every account shows its full sales/transaction history, as does a B2C customer profile. *(client request · MoM 7 Aug 2026, 11. Accounts Management (B2B and B2C) · DI-162)*
- Membership / season pass is defined by start/end date rather than quantity, requires customer profile capture at purchase, and supports renew, upgrade, cancel and extend workflows. *(agreed · MoM 5 Aug 2026, 4. Ticket Catalogue & Product Types · DI-138)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-295` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS83 Membership   Annual Pass Management Board 2.dc.html#bo-295`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 2
- Flow F139 *Membership Annual Pass Management board 2: Member Operations Command Center*, step 2: Works in Member 360° Membership Account Workspace → Provide a complete operational view of an individual member and their membership contract. This should be the primary screen an authorized membership-service agent opens when helping a member.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (48 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-295?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `BO-294`.
- [ ] Every gated control is gated: `GUEST_MANAGE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-296` Membership Activation, Assignment & Credential Management

**Manage the operational process that turns a purchased membership product into an active membership assigned to a specific individual.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_MODIFY` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `membershipId` (navigation) |
| Route | `/sell/membership-activation-assignment-credential-management-bo-296` |

#### Inputs: what the user enters or picks

**Sent by *Block*** (`resolveMembershipActivation`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Action `action` | select | required | — | Activate · Block · Review · Replace · Link · Escalate | — | The activation-queue action (decided 29 September, readiness close-out). | `resolveMembershipActivation` body |
| Credential `credentialId` | picker: choose a credential | optional | — | — | shows names, sends the id | The credential being replaced. Required for `replace`. | `resolveMembershipActivation` body |
| Media code `mediaCode` | text field | optional | — | max length 100 | — | The new media's code. Required for `replace`. | `resolveMembershipActivation` body |
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | The guest the membership is linked to. Required for `link`. | `resolveMembershipActivation` body |
| Reason `reason` | text area | optional | — | min length 3; max length 500 | — | Required for `block` and `escalate`. | `resolveMembershipActivation` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every membership activation credential** (data table, from `listMembershipActivationCredential`)

| Shows | Format | Notes |
|---|---|---|
| Purchase date | text | not in the schema: `MembershipActivationAssignmentCredentialManagementView.purchaseDate` |
| Eligible activation date | text | not in the schema: `MembershipActivationAssignmentCredentialManagementView.eligibleActivationDate` |
| Activation deadline | text | not in the schema: `MembershipActivationAssignmentCredentialManagementView.activationDeadline` |
| Selected start date | text | not in the schema: `MembershipActivationAssignmentCredentialManagementView.selectedStartDate` |
| Calculated expiry | text | not in the schema: `MembershipActivationAssignmentCredentialManagementView.calculatedExpiry` |
| Activation method | text | not in the schema: `MembershipActivationAssignmentCredentialManagementView.activationMethod` |

**The selected membership activation credential** (detail panel): The pack groups this record's detail under its own headings: “Show memberships”, “Purchased Membership”, “Associate membership with”, “Record reason”.

| Shows | Format | Notes |
|---|---|---|
| Purchase date | text | not in the schema: `MembershipActivationAssignmentCredentialManagementView.purchaseDate` |
| Eligible activation date | text | not in the schema: `MembershipActivationAssignmentCredentialManagementView.eligibleActivationDate` |
| Activation deadline | text | not in the schema: `MembershipActivationAssignmentCredentialManagementView.activationDeadline` |
| Selected start date | text | not in the schema: `MembershipActivationAssignmentCredentialManagementView.selectedStartDate` |
| Calculated expiry | text | not in the schema: `MembershipActivationAssignmentCredentialManagementView.calculatedExpiry` |
| Activation method | text | not in the schema: `MembershipActivationAssignmentCredentialManagementView.activationMethod` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Block (primary button) | `resolveMembershipActivation` POST `/memberships/{membershipId}/activation/resolve` | MembershipActivationActionInput | MembershipActivationView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 `replace` without `credentialId` and `mediaCode`, `link` without `subjectId`, or `block` or `escalate` without … | — |
| Review (secondary button) | `resolveMembershipActivation` POST `/memberships/{membershipId}/activation/resolve` | MembershipActivationActionInput | MembershipActivationView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 `replace` without `credentialId` and `mediaCode`, `link` without `subjectId`, or `block` or `escalate` without … | — |
| Replace (secondary button) | `resolveMembershipActivation` POST `/memberships/{membershipId}/activation/resolve` | MembershipActivationActionInput | MembershipActivationView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 `replace` without `credentialId` and `mediaCode`, `link` without `subjectId`, or `block` or `escalate` without … | — |
| Link (secondary button) | `resolveMembershipActivation` POST `/memberships/{membershipId}/activation/resolve` | MembershipActivationActionInput | MembershipActivationView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 `replace` without `credentialId` and `mediaCode`, `link` without `subjectId`, or `block` or `escalate` without … | — |
| Escalate (secondary button) | `resolveMembershipActivation` POST `/memberships/{membershipId}/activation/resolve` | MembershipActivationActionInput | MembershipActivationView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 `replace` without `credentialId` and `mediaCode`, `link` without `subjectId`, or `block` or `escalate` without … | — |

**Data it reads**: `listMembershipActivationCredential` (onLoad, Membership Activation, Assignment & Credential Management)

**Where the user goes next**

- → `BO-294` Member Operations Command Center: *Returns to the board's landing screen*; calls `listMembershipActivationCredential`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The membership activation credential list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the membership activation credential untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No membership activation credential yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the membership activation credential are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 `replace` without `credentialId` and `mediaCode`, `link` without `subjectId`, or `block` or `escalate` without a `reason` (`activation-action-incomplete`). |

#### Permissions

- `resolveMembershipActivation` → `ORDER_MODIFY` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-296` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS83 Membership   Annual Pass Management Board 2.dc.html#bo-296`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 2
- Flow F139 *Membership Annual Pass Management board 2: Member Operations Command Center*, step 4: Works in Membership Activation, Assignment & Credential Management → Manage the operational process that turns a purchased membership product into an active membership assigned to a specific individual.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-296?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Block, Review, Replace, Link, Escalate.
- [ ] Every transition is wired: `BO-294`.
- [ ] Every gated control is gated: `ORDER_MODIFY`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-297` Visit, Admission & Entitlement Usage Monitor

**Provide membership teams with complete visibility of how a member uses admission and other membership entitlements.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Detect) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/sell/visit-admission-entitlement-usage-monitor-bo-297` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Total Visits** (metric tile, from `listVisitAdmissionEntitlement`)

**Visits This Month** (metric tile, from `listVisitAdmissionEntitlement`)

**Last Visit** (metric tile, from `listVisitAdmissionEntitlement`)

**Upcoming Reservation start** (metric tile, from `listVisitAdmissionEntitlement`)

**Guest Tickets Used** (metric tile, from `listVisitAdmissionEntitlement`)

**Guest Tickets Remaining** (metric tile, from `listVisitAdmissionEntitlement`)

**Parking Uses** (metric tile, from `listVisitAdmissionEntitlement`)

**Benefit usage** (metric tile, from `listVisitAdmissionEntitlement`)

**No-Shows** (metric tile, from `listVisitAdmissionEntitlement`)

**Every visit admission entitlement** (data table, from `listVisitAdmissionEntitlement`)

| Shows | Format | Notes |
|---|---|---|
| Validation result | text | not in the schema: `VisitAdmissionEntitlementUsageMonitorView.validationResult` |

**The selected visit admission entitlement** (detail panel): The pack groups this record's detail under its own headings: “Benefit”, “Guest”, “Parking 18 Unlimited”, “Manual Adjustment”, “Require”.

| Shows | Format | Notes |
|---|---|---|
| Validation result | text | not in the schema: `VisitAdmissionEntitlementUsageMonitorView.validationResult` |

**Data it reads**: `listVisitAdmissionEntitlement` (onLoad, Visit, Admission & Entitlement Usage Monitor)

**Where the user goes next**

- → `BO-294` Member Operations Command Center: *Returns to the board's landing screen*; calls `listVisitAdmissionEntitlement`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The visit admission entitlement list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the visit admission entitlement untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No visit admission entitlement yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the visit admission entitlement are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Accreditation-holder monitoring is a filtered view inside the general entitlement monitoring, not a separate platform, so staff can quickly distinguish and support large accredited groups. *(agreed · MoM 7 Sep 2026, 4.10 Entitlements Lifecycle, Consumption Monitoring & Screen Consolidation · DI-672)*
- Entitlement statuses: active, reserved, consumed, transferred, expired, refunded/cancelled; views show entitlements nearing expiry, real-time consumption per customer, and whether a ticket has been upgraded. *(client request · MoM 7 Sep 2026, 4.10 / 4.11 Entitlements Lifecycle & Usage · DI-670)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-297` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS83 Membership   Annual Pass Management Board 2.dc.html#bo-297`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 2
- Flow F139 *Membership Annual Pass Management board 2: Member Operations Command Center*, step 6: Works in Visit, Admission & Entitlement Usage Monitor → Provide membership teams with complete visibility of how a member uses admission and other membership entitlements.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-297?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-294`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-298` Membership Freeze, Suspension & Reactivation Management

**Manage temporary interruption of membership rights without necessarily terminating the membership contract.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_MODIFY`, `PRODUCT_CONFIGURE` (1 operate, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Freeze Configuration Consumption; Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `entitlementId` (navigation) · cold entry: Opened from BO-294 with the membership entitlement picked there. Opened cold (a bookmark or a refresh), it shows the list to pick from rather than an empty … |
| Route | `/sell/membership-freeze-suspension-reactivation-management-bo-298` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Start Date | select field | — | — | — | — | — | — |
| End Date | select field | — | — | — | — | — | — |
| Duration | select field | — | — | — | — | — | — |
| Reason | select field | — | — | — | — | The freeze reasons of `freezeEntitlement`: travelling, injury, personal, seasonal, other. **Choosing Other makes Note required** (decided 28 September, audit R222). | — |
| Note | text field | — | — | — | — | **Required, at least 3 characters, when the reason is Other** — the form will not submit without it, and `freezeEntitlement` refuses 400 (decided 28 September, audit R222). Optional for every other … | — |
| Requested By | select field | — | — | — | — | — | — |
| Approved By | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Freeze (primary button) | navigation or local | — | — | — | — |
| Suspend (destructive button) | navigation or local | — | — | — | — |
| Resume (secondary button) | navigation or local | — | — | — | — |
| Reactivate (secondary button) | navigation or local | — | — | — | — |
| Administrative Hold (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listMembershipFreezeSuspension` (onLoad, Membership Freeze, Suspension & Reactivation Management)

**Where the user goes next**

- → `BO-294` Member Operations Command Center: *Returns to the board's landing screen*; calls `listMembershipFreezeSuspension`

**What opens over it**

- confirmDialog *Suspend*: **Suspend on a membership freeze suspension is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The membership freeze suspension configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the membership freeze suspension untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No membership freeze suspension configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 `reason` is `other` with no `note` (audit R222). |

#### Permissions

- `freezeEntitlement` → `PRODUCT_CONFIGURE` (configure) · staff, guest
- `reinstateEntitlement` → `PRODUCT_CONFIGURE` (configure) · staff
- `suspendEntitlement` → `ORDER_MODIFY` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.14.13 | Allow temporary suspension of memberships. | Ticketing Sales | CONTRACTED | `freezeEntitlement` |
| 1.1.100 | Membership reactivation | Ticketing Catalogue | CONTRACTED | `reinstateEntitlement` |
| 1.1.99 | Membership suspension | Ticketing Catalogue | CONTRACTED | `suspendEntitlement` |
| 3.2.22 | The system should allow manual disabling of access for an individual guest ticket. | Admission and Access | CONTRACTED | `suspendEntitlement` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Membership lifecycle: upgrade, downgrade, suspend (freezes validity until re-enabled), deactivate and cancel, with configurable timing windows (e.g. upgrade allowed only in the final two months before expiry). *(client request · MoM 25 Aug 2026, 4.8 Eligibility Rules, Special Products & Memberships · DI-467)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-298` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS83 Membership   Annual Pass Management Board 2.dc.html#bo-298`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 2
- Flow F139 *Membership Annual Pass Management board 2: Member Operations Command Center*, step 8: Works in Membership Freeze, Suspension & Reactivation Management → Manage temporary interruption of membership rights without necessarily terminating the membership contract.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-298?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Freeze, Suspend, Resume, Reactivate, Administrative Hold.
- [ ] Every transition is wired: `BO-294`.
- [ ] Every gated control is gated: `ORDER_MODIFY`, `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-299` Membership Upgrade, Downgrade & Product Migration Operations

**Manage operational movement of an active member between membership products or tiers.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_MODIFY` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `membershipId` (navigation) |
| Route | `/sell/membership-upgrade-downgrade-product-migration-operation-bo-299` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Sent by *Migrate membership*** (`migrateMembership`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Target product `targetProductId` | picker: choose a target product | required | — | — | shows names, sends the id | The membership product it moves to. | `migrateMembership` body |
| Direction `direction` | segmented control | required | — | Upgrade · Downgrade · Migration | — | Which way it moves (decided 29 September, readiness close-out). | `migrateMembership` body |
| Effective timing `effectiveTiming` | radio group | required | — | Immediate · Next visit · Next renewal · End of current term | — | When the move takes effect (decided 29 September, readiness close-out). | `migrateMembership` body |
| Pro rata `proRata` | toggle | optional | off | — | — | Charge or credit the difference for the remaining term. | `migrateMembership` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Next Visit (primary button) | navigation or local | — | — | — | — |
| Next Renewal (secondary button) | navigation or local | — | — | — | — |
| End of Current Term (destructive button) | navigation or local | — | — | — | — |
| Migrate membership (primary button) | `migrateMembership` POST `/memberships/{membershipId}/migrations` | MembershipMigrationInput | MembershipMigrationView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The membership is not active (`membershipNotActive`), the target is the product it already holds … | — |

**Data it reads**: `listMembershipUpgradeDowngrade` (onLoad, Membership Upgrade, Downgrade & Product Migration Operations)

**Where the user goes next**

- → `BO-294` Member Operations Command Center: *Returns to the board's landing screen*; calls `listMembershipUpgradeDowngrade`

**What opens over it**

- confirmDialog *End of Current Term*: **End of Current Term on a membership upgrade downgrade is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The membership upgrade downgrade list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the membership upgrade downgrade untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No membership upgrade downgrade yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the membership upgrade downgrade are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The membership is not active (`membershipNotActive`), the target is the product it already holds (`sameProduct`), or a migration is already scheduled … (MembershipMigrationProblem) |

#### Permissions

- `migrateMembership` → `ORDER_MODIFY` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.14.21 | System shall allow members to downgrade from one membership tier to another according to configurable business rules, effective dates, and entitlement adjustment policies. | Ticketing Sales | CONTRACTED | `migrateMembership` |
| 13.3.3 | APIs shall support membership creation, renewal, upgrade, downgrade, freeze, entitlement validation and membership status retrieval. | Developer & API Management | CONTRACTED | `migrateMembership` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Membership lifecycle: upgrade, downgrade, suspend (freezes validity until re-enabled), deactivate and cancel, with configurable timing windows (e.g. upgrade allowed only in the final two months before expiry). *(client request · MoM 25 Aug 2026, 4.8 Eligibility Rules, Special Products & Memberships · DI-467)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-299` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS83 Membership   Annual Pass Management Board 2.dc.html#bo-299`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 2
- Flow F139 *Membership Annual Pass Management board 2: Member Operations Command Center*, step 10: Works in Membership Upgrade, Downgrade & Product Migration Operations → Manage operational movement of an active member between membership products or tiers.

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-299?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Next Visit, Next Renewal, End of Current Term, Migrate membership.
- [ ] Every transition is wired: `BO-294`.
- [ ] Every gated control is gated: `ORDER_MODIFY`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-300` Renewal Operations & Auto-Renewal Management

**Operationally manage memberships approaching expiry and execute the renewal policies configured in Board 1.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_MODIFY` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Track) and no metric row |
| Offline | online only |
| Opens with | `membershipId` (navigation) · cold entry: Opened from BO-294 with the membership picked there. Opened cold (a bookmark or a refresh), it shows the list to pick from rather than an empty record, and … |
| Route | `/sell/renewal-operations-auto-renewal-management-bo-300` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every renewal operations auto-renewal** (data table, from `listRenewalAuto`)

| Shows | Format | Notes |
|---|---|---|
| Member | text | not in the schema: `RenewalOperationsAutoRenewalManagementView.member` |
| Membership | text | not in the schema: `RenewalOperationsAutoRenewalManagementView.membership` |
| Tier | text | not in the schema: `RenewalOperationsAutoRenewalManagementView.tier` |
| Expiry | text | not in the schema: `RenewalOperationsAutoRenewalManagementView.expiry` |
| Renewal window | text | not in the schema: `RenewalOperationsAutoRenewalManagementView.renewalWindow` |
| Renewal price | text | not in the schema: `RenewalOperationsAutoRenewalManagementView.renewalPrice` |
| Auto renew | text | not in the schema: `RenewalOperationsAutoRenewalManagementView.autoRenew` |
| Payment method status | text | not in the schema: `RenewalOperationsAutoRenewalManagementView.paymentMethodStatus` |
| Eligibility | text | not in the schema: `RenewalOperationsAutoRenewalManagementView.eligibility` |
| Renewal status | text | not in the schema: `RenewalOperationsAutoRenewalManagementView.renewalStatus` |

**The selected renewal operations auto-renewal** (detail panel): The pack groups this record's detail under its own headings: “Segment members into”, “Validate”, “Final failure”, “Renewal Grace”, “Renewal Continuity”, “Current expiry”.

| Shows | Format | Notes |
|---|---|---|
| Member | text | not in the schema: `RenewalOperationsAutoRenewalManagementView.member` |
| Membership | text | not in the schema: `RenewalOperationsAutoRenewalManagementView.membership` |
| Tier | text | not in the schema: `RenewalOperationsAutoRenewalManagementView.tier` |
| Expiry | text | not in the schema: `RenewalOperationsAutoRenewalManagementView.expiry` |
| Renewal window | text | not in the schema: `RenewalOperationsAutoRenewalManagementView.renewalWindow` |
| Renewal price | text | not in the schema: `RenewalOperationsAutoRenewalManagementView.renewalPrice` |
| Auto renew | text | not in the schema: `RenewalOperationsAutoRenewalManagementView.autoRenew` |
| Payment method status | text | not in the schema: `RenewalOperationsAutoRenewalManagementView.paymentMethodStatus` |
| Eligibility | text | not in the schema: `RenewalOperationsAutoRenewalManagementView.eligibility` |
| Renewal status | text | not in the schema: `RenewalOperationsAutoRenewalManagementView.renewalStatus` |

**Data it reads**: `listRenewalAuto` (onLoad, Renewal Operations & Auto-Renewal Management)

**Where the user goes next**

- → `BO-294` Member Operations Command Center: *Returns to the board's landing screen*; calls `listRenewalAuto`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The renewal operations auto-renewal list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the renewal operations auto-renewal untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No renewal operations auto-renewal yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the renewal operations auto-renewal are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Outside the grace period (`outsideGracePeriod`), or already renewed for this term (`alreadyRenewedForTerm`). (MembershipRenewalProblem) |

#### Permissions

- `renewMembership` → `ORDER_MODIFY` (operate) · staff, service

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.7.96 | The system shall support subscription creation, renewal, upgrade, downgrade, suspension, cancellation, expiry, and reactivation. Applicable to memberships, annual passes, recurring services, and … | F&B & Guest Management | CONTRACTED | `renewMembership` |

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-300` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS83 Membership   Annual Pass Management Board 2.dc.html#bo-300`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 2
- Flow F139 *Membership Annual Pass Management board 2: Member Operations Command Center*, step 12: Works in Renewal Operations & Auto-Renewal Management → Operationally manage memberships approaching expiry and execute the renewal policies configured in Board 1.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-300?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-294`.
- [ ] Every gated control is gated: `ORDER_MODIFY`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-301` Member Exceptions, Overrides & Service Recovery

**Provide controlled handling of member-specific situations that fall outside normal membership policy.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `APPROVAL_REQUEST`, `ORDER_MODIFY`, `PRODUCT_CONFIGURE` (2 operate, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `membershipId` (navigation), `entitlementId` (navigation) · cold entry: Opened from BO-294 with the membership entitlement picked there. Opened cold (a bookmark or a refresh), it shows the list to pick from rather than an empty … |
| Route | `/sell/member-exceptions-overrides-service-recovery-bo-301` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Sent by *Eligibility Override*** (`createMemberException`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | select | required | — | Eligibility override · Expiry extension · Complimentary renewal · Complimentary benefit · Entitlement adjustment · Freeze exception · Suspension override · Replacement credential | — | The exception kind (decided 29 September, readiness close-out). `complimentaryRenewal` and `complimentaryBenefit` move money and need an approved `approvalRequestId`. | `createMemberException` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `createMemberException` body |
| Approval request `approvalRequestId` | picker: choose an approval request | optional | — | — | shows names, sends the id | The approved request in `approvals`. Required for `complimentaryRenewal` and `complimentaryBenefit`. | `createMemberException` body |
| Extend days `extendDays` | number field (days) | optional | — | min 1; max 366 | — | Required for `expiryExtension`. | `createMemberException` body |
| Benefit `benefitId` | picker: choose a benefit | optional | — | — | shows names, sends the id | The plan benefit (`catalogue.membership_benefit`). Required for `complimentaryBenefit` and `entitlementAdjustment`. | `createMemberException` body |
| Quantity `quantity` | number field | optional | — | min 1 | — | How many of the benefit. Required with `benefitId`. | `createMemberException` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Eligibility Override (primary button) | `createMemberException` POST `/memberships/{membershipId}/exceptions` | MemberExceptionInput | MemberExceptionView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The approval request named is not approved - pending, rejected or expired (`approvalNotApproved`). … | — |
| Expiry Extension (secondary button) | `createMemberException` POST `/memberships/{membershipId}/exceptions` | MemberExceptionInput | MemberExceptionView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The approval request named is not approved - pending, rejected or expired (`approvalNotApproved`). … | — |
| Complimentary Renewal (secondary button) | `createMemberException` POST `/memberships/{membershipId}/exceptions` | MemberExceptionInput | MemberExceptionView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The approval request named is not approved - pending, rejected or expired (`approvalNotApproved`). … | — |
| Complimentary Benefit (secondary button) | `createMemberException` POST `/memberships/{membershipId}/exceptions` | MemberExceptionInput | MemberExceptionView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The approval request named is not approved - pending, rejected or expired (`approvalNotApproved`). … | — |
| Entitlement Adjustment (secondary button) | `createMemberException` POST `/memberships/{membershipId}/exceptions` | MemberExceptionInput | MemberExceptionView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The approval request named is not approved - pending, rejected or expired (`approvalNotApproved`). … | — |
| Freeze Exception (secondary button) | `createMemberException` POST `/memberships/{membershipId}/exceptions` | MemberExceptionInput | MemberExceptionView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The approval request named is not approved - pending, rejected or expired (`approvalNotApproved`). … | — |
| Suspension Override (secondary button) | `createMemberException` POST `/memberships/{membershipId}/exceptions` | MemberExceptionInput | MemberExceptionView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The approval request named is not approved - pending, rejected or expired (`approvalNotApproved`). … | — |
| Replacement Credential (secondary button) | `createMemberException` POST `/memberships/{membershipId}/exceptions` | MemberExceptionInput | MemberExceptionView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The approval request named is not approved - pending, rejected or expired (`approvalNotApproved`). … | — |

**Data it reads**: `listMemberExceptionOverride` (onLoad, Member Exceptions, Overrides & Service Recovery)

**Where the user goes next**

- → `BO-294` Member Operations Command Center: *Returns to the board's landing screen*; calls `listMemberExceptionOverride`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The member exceptions overrides list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the member exceptions overrides untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No member exceptions overrides yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the member exceptions overrides are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 `reason` is `other` with no `note` (audit R222).; 409 An open request already exists for this subject. Two approvals for one refund is how a refund gets paid twice. (ApprovalStateProblem); 409 The approval request named is not approved - pending, rejected or expired (`approvalNotApproved`). (MemberExceptionProblem); 422 A money-moving kind (`complimentaryRenewal`, `complimentaryBenefit`) with … |

#### Permissions

- `createApprovalRequest` → `APPROVAL_REQUEST` (operate) · staff
- `freezeEntitlement` → `PRODUCT_CONFIGURE` (configure) · staff, guest
- `reinstateEntitlement` → `PRODUCT_CONFIGURE` (configure) · staff
- `createMemberException` → `ORDER_MODIFY` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.59 | Complimentary entitlement redemption | Ticketing Catalogue | CONTRACTED | `createApprovalRequest` |
| 1.2.64 | Employees shall submit requests from mobile app. | Ticketing Catalogue | CONTRACTED | `createApprovalRequest` |
| 1.2.65 | Managers shall approve requests from mobile app. | Ticketing Catalogue | CONTRACTED | `createApprovalRequest` |
| 11.1.51 | Draft Approval Requests - System shall support saving approval requests in draft status. | Approval Workflows & Governance | CONTRACTED | `createApprovalRequest` |
| 11.1.63 | API-Based Approval Processing - System shall expose approval workflows through APIs. | Approval Workflows & Governance | CONTRACTED | `createApprovalRequest` |
| 2.14.13 | Allow temporary suspension of memberships. | Ticketing Sales | CONTRACTED | `freezeEntitlement` |
| 1.1.100 | Membership reactivation | Ticketing Catalogue | CONTRACTED | `reinstateEntitlement` |

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-301` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS83 Membership   Annual Pass Management Board 2.dc.html#bo-301`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 2
- Flow F139 *Membership Annual Pass Management board 2: Member Operations Command Center*, step 14: Works in Member Exceptions, Overrides & Service Recovery → Provide controlled handling of member-specific situations that fall outside normal membership policy.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-301?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Eligibility Override, Expiry Extension, Complimentary Renewal, Complimentary Benefit, Entitlement Adjustment, Freeze Exception, Suspension Override, Replacement Credential.
- [ ] Every transition is wired: `BO-294`.
- [ ] Every gated control is gated: `APPROVAL_REQUEST`, `ORDER_MODIFY`, `PRODUCT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-302` Member Lifecycle History, Audit & Case Timeline

**Maintain a complete historical record of everything that has happened to the membership from purchase to final expiry.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Track) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/sell/member-lifecycle-history-audit-case-timeline-bo-302` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every member lifecycle history** (data table, from `listMemberLifecycleCase`)

| Shows | Format | Notes |
|---|---|---|
| Event type | text | not in the schema: `MemberLifecycleHistoryAuditCaseTimelineView.eventType` |
| Freeze | text | not in the schema: `Freeze` |
| Upgrade | text | not in the schema: `Upgrade` |
| Downgrade | text | not in the schema: `Downgrade` |

**The selected member lifecycle history** (detail panel): The pack groups this record's detail under its own headings: “Before/After Audit”, “Expiry”, “Reason”, “Record”, “Link to”, “Case Notes”.

| Shows | Format | Notes |
|---|---|---|
| Event type | text | not in the schema: `MemberLifecycleHistoryAuditCaseTimelineView.eventType` |
| Freeze | text | not in the schema: `Freeze` |
| Upgrade | text | not in the schema: `Upgrade` |
| Downgrade | text | not in the schema: `Downgrade` |

**Data it reads**: `listMemberLifecycleCase` (onLoad, Member Lifecycle History, Audit & Case Timeline)

**Where the user goes next**

- → `BO-294` Member Operations Command Center: *Returns to the board's landing screen*; calls `listMemberLifecycleCase`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The member lifecycle history list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the member lifecycle history untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No member lifecycle history yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the member lifecycle history are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-302` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS83 Membership   Annual Pass Management Board 2.dc.html#bo-302`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 2
- Flow F139 *Membership Annual Pass Management board 2: Member Operations Command Center*, step 16: Works in Member Lifecycle History, Audit & Case Timeline → Maintain a complete historical record of everything that has happened to the membership from purchase to final expiry.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (8 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-302?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-294`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-303` Membership Analytics, Renewal Intelligence & AI Retention Center

**Turn membership operational data into actionable intelligence for retention, renewal, product optimization and member engagement.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Display; Forecast) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/sell/membership-analytics-renewal-intelligence-ai-retention-c-bo-303` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search membership analytics renewal | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by membership product, tier, purchase month, venue, acquisition channel, customer segment and 2 more — which are present is a decision the pack already made. | — |

#### Outputs: what the screen shows and produces

**Shown**

**Active Members** (metric tile)

**New Memberships** (metric tile)

**Renewal Rate** (metric tile)

**Churn Rate** (metric tile)

**Auto-Renew Success** (metric tile)

**Average Membership Tenure** (metric tile)

**Average Visits per Member** (metric tile)

**Revenue per Member** (metric tile)

**Membership Utilization** (metric tile)

**Benefit Utilization** (metric tile)

**Upgrade Rate** (metric tile)

**Freeze/Suspension Rate** (metric tile)

**Expected Renewals** (metric tile)

**Expected Churn** (metric tile)

**Renewal Revenue** (metric tile)

**Upgrade Revenue** (metric tile)

**Membership Base Growth** (metric tile)

**Data it reads**: `listMembershipRenewalRetention` (onLoad, Membership Analytics, Renewal Intelligence & AI Retention …)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The membership analytics renewal list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the membership analytics renewal untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No membership analytics renewal yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the membership analytics renewal are still there. The pack's own statuses are 5 Management — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-303` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS83 Membership   Annual Pass Management Board 2.dc.html#bo-303`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 2
- Flow F139 *Membership Annual Pass Management board 2: Member Operations Command Center*, step 18: Works in Membership Analytics, Renewal Intelligence & AI Retention Center → Turn membership operational data into actionable intelligence for retention, renewal, product optimization and member engagement.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-303?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
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

### In P08 · Sell

- Allam: back-end configuration is the most critical part; the screens must make visually clear how administrators configure products, pricing per channel, attributes/components, entitlements, validity and access permissions, comparable to the structured product/metric-sheet approach of an earlier reference system. *(agreed · MoM 24 Sep 2026, 4.3 Back-End Configuration Detail — Requested Format (Screens, Not Just Functional Lists) · DI-985)*
- Chinmay: reduce the number of configuration screens/pages and consolidate related settings/toggles to avoid a long, click-heavy admin flow; Allam agreed, citing the previous system's demo as a starting reference. *(agreed · MoM 25 Aug 2026, 4.11 UX Simplification & Distributed Inventory · DI-474)*
- Retail dashboard gives a consolidated real-time view across outlets — total retail sales, total and average transactions, store performance snapshot, system alerts and out-of-stock indicators — viewable by day, week or month. *(client request · MoM 19 Aug 2026, 4.1 Retail Command Center — Dashboard & Store Setup · DI-349)*
- Allam/Qossai: the workstation/till/POS wireframes are reference only (partly ChatGPT-generated, with errors) and not to be replicated; Softlabs may consolidate dashboards freely and must cross-check the functionality matrix for missing items. *(agreed · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-312)*

**7 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createApprovalRequest": {"method":"POST","path":"/approval-requests","contract":"approvals","summary":"Raise a request","permission":"APPROVAL_REQUEST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateApprovalRequest","responds":"ApprovalRequest"},
"createMemberException": {"method":"POST","path":"/memberships/{membershipId}/exceptions","contract":"orders","summary":"Record a member exception, override or service-recovery act","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MemberExceptionInput","responds":"MemberExceptionView"},
"freezeEntitlement": {"method":"POST","path":"/entitlements/{entitlementId}/freeze","contract":"catalogue","summary":"Pause a membership at the guest's request","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Entitlement"},
"migrateMembership": {"method":"POST","path":"/memberships/{membershipId}/migrations","contract":"orders","summary":"Upgrade, downgrade or migrate an active membership to another product","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MembershipMigrationInput","responds":"MembershipMigrationView"},
"recordBenefitUsage": {"method":"POST","path":"/memberships/{membershipId}/benefit-usage","contract":"identity","summary":"Consume a benefit","permission":"GUEST_MANAGE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"membershipId","in":"path","required":true},{"name":null,"in":null,"required":null}],"requestBody":"IdentityBenefitUsage","responds":"IdentityBenefitUsage"},
"reinstateEntitlement": {"method":"POST","path":"/entitlements/{entitlementId}/reinstate","contract":"catalogue","summary":"Lift a suspension","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Entitlement"},
"renewMembership": {"method":"POST","path":"/memberships/{membershipId}/renewals","contract":"orders","summary":"Renew a membership","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"membershipId","in":"path","required":true},{"name":null,"in":null,"required":null}],"requestBody":"OrdersMembershipRenewal","responds":"OrdersMembershipRenewal"},
"resolveMembershipActivation": {"method":"POST","path":"/memberships/{membershipId}/activation/resolve","contract":"orders","summary":"Act on a membership in the activation queue","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MembershipActivationActionInput","responds":"MembershipActivationView"},
"suspendEntitlement": {"method":"POST","path":"/entitlements/{entitlementId}/suspend","contract":"catalogue","summary":"Suspend or reinstate an entitlement","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"ApprovalDecision": {"type":"object","x-ticvai-persistence":"approvals.decision","required":["level","principalId","decision","decidedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"level":{"type":"integer"},"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"},"delegatedFrom":{"type":"string","format":"uuid","nullable":true},"decision":{"type":"string","enum":["approve","reject"]},"comment":{"type":"string","nullable":true},"reason":{"type":"string","nullable":true},"usedMfa":{"type":"boolean"},"signatureRef":{"type":"string","nullable":true},"decidedAt":{"type":"string","format":"date-time"}}},
"ApprovalKind": {"type":"string","description":"11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n","enum":["refund","priceOverride","discountOverride","complimentaryTicket","membershipCancellation","accessPermissionChange","configurationChange","aiRecommendation","releasePromotion","requisition","stockWriteOff","journalEntry","periodClose","periodReopen","purchaseOrderCancel","purchaseOrderShortClose","tenantMigration","productChange","pricingChange"]},
"ApprovalMode": {"type":"string","description":"11.1.43–11.1.46. **Sequential** asks one at a time, **parallel** asks everyone at once, **consensus** needs all of them, **majority** needs more than half.\nParallel and consensus differ in when it completes: parallel completes on the first approval, consensus waits for all. Conflating them is how a four-eyes rule turns into a one-eye rule.\n","enum":["sequential","parallel","consensus","majority"]},
"ApprovalRequest": {"type":"object","x-ticvai-persistence":"approvals.request","required":["id","kind","status","requestedByPrincipalId","requestedAt"],"properties":{"id":{"type":"string"},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"rerouteOnNoApprover":{"type":"boolean","default":true,"description":"BL-154. **An approver on leave is an approval that waits for them to come back.** Reroutes to the next in the chain rather than stalling — `workforce` already knows who is on leave, and an approval queue nobody is watching is the thing that stops a venue.\n"},"outOfOfficeDelegateId":{"type":"string","format":"uuid","nullable":true},"allowEmailApproval":{"type":"boolean","default":false,"description":"**Approving from an email link with no second factor is the weakest path in the system**, so it is off by default and available only below a configured value.\n"},"reopenedFrom":{"type":"string","format":"uuid","nullable":true,"description":"**Reopening a decided approval creates a new one that points back.** Editing a decision in place destroys the record of what was originally approved, which is the only thing an audit wants.\n"},"status":{"$ref":"#/components/schemas/ApprovalStatus"},"subjectContract":{"type":"string"},"subjectType":{"type":"string"},"subjectId":{"type":"string"},"scopePath":{"type":"string"},"summary":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"justification":{"type":"string","nullable":true},"requestedByPrincipalId":{"type":"string","format":"uuid"},"matrixVersion":{"type":"integer"},"mode":{"$ref":"#/components/schemas/ApprovalMode"},"currentLevel":{"type":"integer"},"totalLevels":{"type":"integer"},"pendingApprovers":{"type":"array","items":{"type":"object","properties":{"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"}}}},"decisions":{"type":"array","description":"Every decision at every level, in order. **Immutable once the request completes** (11.1.56) — an approval is evidence, and amending one is a different fact.\n","items":{"$ref":"#/components/schemas/ApprovalDecision"}},"escalations":{"type":"array","description":"11.1.48. Who was asked, when, and why it moved up. **Escalation adds an approver rather than replacing one**, so the original stays in the record.\n","items":{"type":"object","properties":{"at":{"type":"string","format":"date-time"},"reason":{"type":"string"},"fromLevel":{"type":"integer"},"toLevel":{"type":"integer"},"wasAutomatic":{"type":"boolean"}}}},"resubmittedFromId":{"type":"string","nullable":true},"reopenedFromId":{"type":"string","nullable":true},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"slaBreached":{"type":"boolean"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"requestedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"aiAssessment":{"type":"object","nullable":true,"readOnly":true,"description":"**AI context for the reviewer, never an input to the decision** (11.1.73 to 11.1.75; MoM 8 September; 29 September, build pass, group G2). Written by approvals from `ai.scoreApprovalRequest` on submit and on each SLA tick; null where AI is off or has not answered. Shown on the request labelled as AI; orders the inbox only when `sort=aiPriority` is asked for.","properties":{"riskScore":{"type":"integer","minimum":0,"maximum":100},"riskBand":{"type":"string","enum":["low","medium","high","critical"]},"priorityScore":{"type":"integer","minimum":0,"maximum":100},"escalationSuggestion":{"type":"object","description":"A suggestion a person may act on through `escalateApprovalRequest`, or the tenant's own SLA policy may; nothing escalates because of it.","properties":{"action":{"type":"string","enum":["escalate","addBackupApprover","none"]},"reason":{"type":"string","nullable":true}}},"signals":{"type":"array","maxItems":10,"description":"The signals behind the scores, largest first, as `ai.AiApprovalRequestScore.signals`.","items":{"type":"object","properties":{"code":{"type":"string"},"contribution":{"type":"number"},"detail":{"type":"string","nullable":true}}}},"scoreId":{"type":"string","format":"uuid","description":"The `ai.approval_request_score` row it was copied from; `ai.getApprovalRequestScore` gives the full context. Not a foreign key (the score lives in the AI service)."},"decisionRecordId":{"type":"string","description":"The ai decision record, for the audit of what the AI said and why."},"assessedAt":{"type":"string","format":"date-time"}}}}},
"ApprovalStatus": {"type":"string","enum":["draft","pending","escalated","returned","informationRequested","approved","rejected","withdrawn","expired","cancelled"]},
"CreateApprovalRequest": {"type":"object","x-ticvai-persistence":"none — request only","required":["id","kind","subjectContract","subjectType","subjectId","scopePath","summary"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"subjectContract":{"type":"string","description":"Which contract owns the thing being approved."},"subjectType":{"type":"string"},"subjectId":{"type":"string","description":"**A reference, never a copy.** A copy goes stale between raising and deciding, and an approver reading a stale copy approves something that no longer exists.\n"},"scopePath":{"type":"string"},"summary":{"type":"string","maxLength":300,"description":"What the approver sees in their queue before opening it."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"attributes":{"type":"object","additionalProperties":true},"justification":{"type":"string","maxLength":1000},"isDraft":{"type":"boolean","default":false,"description":"True saves the request at `draft` without routing it; `submitApprovalRequest` sends it later (decided 28 September, audit R129).\n"}}},
"Entitlement": {"type":"object","x-ticvai-persistence":"access.entitlement","description":"**What a guest actually holds.** Found missing on 18 August by the schema audit — 33 tables in `orders`, seven in `access`, and none of them stored an issued ticket.\nThe package sold products, defined `EntitlementTemplate`, recorded `ScanEvent.ticketId`, transferred `ticket_transfer.ticketIds` and issued `wallet_pass.entitlementId` — **five artefacts referring to a thing that did not exist.** `validateAccess` read the *template* and never the instance, and `suspendEntitlement` suspended the template, **which would have suspended it for every guest who held one.**\n**The template is the definition and this is the instance.** A template says *an annual pass admits once a day for a year*; this says *this guest's annual pass, bought on 3 March, used eleven times, frozen for two weeks in July, valid until 2 March.*\n","required":["id","templateId","productId","orderId","subjectId","status","validFrom","validTo"],"properties":{"id":{"type":"string","format":"uuid","description":"A UUIDv7, matching `TicketStatus.ticketId` — **stable for the life of the ticket and independent of the media carrying it.** A guest whose wristband broke keeps the same entitlement with a new `mediaCode`.\n**This is the ticket id.** Wherever an operation takes a `ticketId` or `ticketIds` — `lookupTicket`, `listScans`, `ScanEvent`, the offline package and `transferOrderTickets` — it is this value. An order line's `entitlementIds` are the ticket ids of that line.\n"},"templateId":{"type":"string","format":"uuid","description":"The definition it was issued against. **Pinned at issue** — a template edited next month must not change what this guest bought.\n"},"productId":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid","description":"The order's id, a UUIDv7 as in `/orders/{orderId}` (`orders.sales_order.id`)."},"orderLineId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"Who holds it. **Null is legitimate** — a ticket bought as a gift or sold at a till to somebody who gave no details has no subject until it is claimed.\n"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"mediaCode":{"type":"string","description":"What is scanned — a QR payload, a wristband serial, a card number. **Rotatable without reissuing**, because a guest whose wristband broke should not need a new ticket.\n"},"status":{"$ref":"../spine/orders.yaml#/components/schemas/EntitlementStatus"},"statusNote":{"type":"string","nullable":true,"description":"**Not `TicketStatus` — that is a validation result with a misleading name**, computed at scan time and carrying `isValid` and `isInsideVenue`. The lifecycle is `orders.EntitlementStatus`, and `states/entitlement-status.yaml` has modelled it since before this table existed.\n**Which is the finding in one line: the package had the lifecycle, the state model and the validation result, and no row to hang them on.**\n"},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time","description":"**Resolved at issue from the template, then owned here.** A freeze extends it, a reissue replaces it, and neither reaches back to the template.\n**What the pre-expiry notice is measured from** (29 September, build pass, group G2; 5.5.30). A daily run in access publishes `entitlement.expiringSoon` once per entitlement and `validTo` when an entitlement in `issued` or `partiallyConsumed` comes within its template's `expiryNoticeDays` (`catalogue.EntitlementTemplate`), and not for one bought inside that window. Marketing turns it into the reminder (a `MessageTrigger` on the event, or a triggered campaign on `entitlementExpiring`); access only says the date is near. A freeze or renewal that moves `validTo` raises the next notice once.\n"},"entriesUsed":{"type":"integer","default":0,"readOnly":true,"x-ticvai-derived":"onWrite","description":"**The number `validateAccess` decrements and nothing was decrementing.** A ten-entry pass with no counter is a ten-entry pass that admits forever.\n**Maintained on write**, in the same transaction as the admitting `access.scan_event` row: by `validateAccess`, `validateGroupAccess` (by the count admitted) and `syncScans` for each replayed admission the server accepts. A replayed scan the server downgrades to `denied` does not count.\n"},"entriesAllowed":{"type":"integer","nullable":true},"lastEntryAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"`recordedAt` of the latest admission counted in `entriesUsed`, written by the same writes. A scan replayed late with an earlier `recordedAt` does not move it back.\n"},"frozenDays":{"type":"integer","default":0,"readOnly":true,"x-ticvai-derived":"onWrite","description":"Days added by a freeze. **Maintained on write** by the freeze operation (`freezeEntitlement`), in the same write that extends `validTo` by those days. **Held here rather than computed from a freeze log**, because a gate has to answer in under 300ms and cannot replay a history to decide validity.\n"},"suspendedReason":{"type":"string","nullable":true},"freezeReason":{"type":"string","nullable":true,"enum":["travelling","injury","personal","seasonal","other"],"description":"The `reason` of the latest `freezeEntitlement` (audit R222). Null when never frozen."},"freezeNote":{"type":"string","nullable":true,"maxLength":500,"description":"The `note` the latest `freezeEntitlement` took, required there when `reason` is `other` (decided 28 September, audit R222). Kept so the quarterly review of `other` notes has something to read."},"isNameBound":{"type":"boolean","default":false},"holderName":{"type":"string","nullable":true},"sharedWithSubjectIds":{"type":"array","description":"`shareEntitlement`. **The owner keeps it and a second person may present it** — the asymmetry that stops a shared family pass becoming a resale chain.\n","items":{"type":"string","format":"uuid"}},"issuedVia":{"type":"string","enum":["sale","invitation","reissue","transfer","resale","membership","groupBooking"],"description":"**How it came to exist, and it matters to finance.** A sold entitlement carries deferred revenue; an invitation carries a marketing cost; a reissue carries neither.\n"},"supersedesEntitlementId":{"type":"string","format":"uuid","nullable":true,"description":"For a reissue or a resale. **The chain is traceable** — a ticket appearing from nowhere is indistinguishable from a fraudulent one.\n"},"walletValueId":{"type":"string","format":"uuid","nullable":true,"description":"Where the template carries stored value. **A `retail.Wallet` bound to the entitlement, not a balance on it** (CF-126).\n"},"facePassEnrolmentId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"The active `facePass` enrolment on this entitlement (`FacePassEnrolment.id`), or null when none is. **Computed on read from `pii.subject_biometric` and not stored here** — the PII split keeps the biometric on its own side, and this carries only its id. It is how a screen holding a pass finds the enrolment `getFacePassEnrolment` and `revokeFacePass` take.\n"}}},
"IdentityBenefitUsage": {"type":"object","x-ticvai-persistence":"identity.benefit_usage","description":"**Taken from the backend workbook, 20 September.** Tracks each use of a customer's membership benefit and the remaining allowance.","required":["customerMembershipId","membershipBenefitId","quantity","usedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"customerMembershipId":{"type":"string","format":"uuid"},"membershipBenefitId":{"type":"string","format":"uuid"},"quantity":{"type":"number"},"sourceType":{"type":"string","maxLength":30,"nullable":true},"sourceOrderId":{"type":"string","format":"uuid","nullable":true},"usedAt":{"type":"string","format":"date-time"},"remainingQuantity":{"type":"number","nullable":true,"readOnly":true,"description":"Written on the row by the server when the usage is recorded; ignored in a request."},"notes":{"type":"string","maxLength":500,"nullable":true}}},
"MemberExceptionInput": {"type":"object","x-ticvai-persistence":"none — request only","description":"What `createMemberException` takes. The eight kinds are the pack's own labels on BO-301 (decided 29 September, readiness close-out).\n","required":["kind","reason"],"properties":{"kind":{"type":"string","description":"The exception kind (decided 29 September, readiness close-out). `complimentaryRenewal` and `complimentaryBenefit` move money and need an approved `approvalRequestId`.","enum":["eligibilityOverride","expiryExtension","complimentaryRenewal","complimentaryBenefit","entitlementAdjustment","freezeException","suspensionOverride","replacementCredential"]},"reason":{"type":"string","minLength":3,"maxLength":500},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"description":"The approved request in `approvals`. Required for `complimentaryRenewal` and `complimentaryBenefit`."},"extendDays":{"type":"integer","minimum":1,"maximum":366,"nullable":true,"description":"Required for `expiryExtension`."},"benefitId":{"type":"string","format":"uuid","nullable":true,"description":"The plan benefit (`catalogue.membership_benefit`). Required for `complimentaryBenefit` and `entitlementAdjustment`."},"quantity":{"type":"integer","minimum":1,"nullable":true,"description":"How many of the benefit. Required with `benefitId`."}}},
"MemberExceptionView": {"type":"object","x-ticvai-persistence":"orders.member_exception","description":"**One exception made to a membership, and who made it.** Written by `createMemberException` (decided 29 September, readiness close-out); the audit trail a membership that behaves outside its plan is explained from.\n","required":["id","membershipId","kind","reason","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"membershipId":{"type":"string","format":"uuid","readOnly":true,"description":"The membership in the path."},"kind":{"type":"string","enum":["eligibilityOverride","expiryExtension","complimentaryRenewal","complimentaryBenefit","entitlementAdjustment","freezeException","suspensionOverride","replacementCredential"]},"reason":{"type":"string","maxLength":500},"approvalRequestId":{"type":"string","format":"uuid","nullable":true},"extendDays":{"type":"integer","nullable":true},"benefitId":{"type":"string","format":"uuid","nullable":true},"quantity":{"type":"integer","nullable":true},"newExpiryAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"With `expiryExtension` or `complimentaryRenewal`, the membership's expiry after the exception."},"recordedBy":{"type":"string","format":"uuid","readOnly":true,"description":"The principal who made the exception."},"recordedAt":{"type":"string","format":"date-time","readOnly":true}}},
"MembershipActivationActionInput": {"type":"object","x-ticvai-persistence":"none — request only","description":"What `resolveMembershipActivation` takes (decided 29 September, readiness close-out).","required":["action"],"properties":{"action":{"type":"string","description":"The activation-queue action (decided 29 September, readiness close-out).","enum":["activate","block","review","replace","link","escalate"]},"credentialId":{"type":"string","format":"uuid","nullable":true,"description":"The credential being replaced. Required for `replace`."},"mediaCode":{"type":"string","maxLength":100,"nullable":true,"description":"The new media's code. Required for `replace`."},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"The guest the membership is linked to. Required for `link`."},"reason":{"type":"string","minLength":3,"maxLength":500,"nullable":true,"description":"Required for `block` and `escalate`."}}},
"MembershipActivationView": {"type":"object","x-ticvai-persistence":"orders.membership_activation_action","description":"**One action taken on a membership in the activation queue.** Written by `resolveMembershipActivation` (decided 29 September, readiness close-out).\n","required":["id","membershipId","action","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"membershipId":{"type":"string","format":"uuid","readOnly":true},"action":{"type":"string","enum":["activate","block","review","replace","link","escalate"]},"credentialId":{"type":"string","format":"uuid","nullable":true},"mediaCode":{"type":"string","maxLength":100,"nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"reason":{"type":"string","maxLength":500,"nullable":true},"membershipStatus":{"type":"string","maxLength":30,"readOnly":true,"description":"The membership's status after the action."},"recordedBy":{"type":"string","format":"uuid","readOnly":true},"recordedAt":{"type":"string","format":"date-time","readOnly":true}}},
"MembershipMigrationInput": {"type":"object","x-ticvai-persistence":"none — request only","description":"What `migrateMembership` takes (decided 29 September, readiness close-out).","required":["targetProductId","direction","effectiveTiming"],"properties":{"targetProductId":{"type":"string","format":"uuid","description":"The membership product it moves to."},"direction":{"type":"string","description":"Which way it moves (decided 29 September, readiness close-out).","enum":["upgrade","downgrade","migration"]},"effectiveTiming":{"type":"string","description":"When the move takes effect (decided 29 September, readiness close-out).","enum":["immediate","nextVisit","nextRenewal","endOfCurrentTerm"]},"proRata":{"type":"boolean","default":false,"description":"Charge or credit the difference for the remaining term."}}},
"MembershipMigrationView": {"type":"object","x-ticvai-persistence":"orders.membership_migration","description":"**One move of a membership to another product.** Written by `migrateMembership` (decided 29 September, readiness close-out).\n","required":["id","membershipId","fromProductId","targetProductId","direction","effectiveTiming","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"membershipId":{"type":"string","format":"uuid","readOnly":true},"fromProductId":{"type":"string","format":"uuid","readOnly":true},"targetProductId":{"type":"string","format":"uuid"},"direction":{"type":"string","enum":["upgrade","downgrade","migration"]},"effectiveTiming":{"type":"string","enum":["immediate","nextVisit","nextRenewal","endOfCurrentTerm"]},"proRata":{"type":"boolean"},"proRataAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"readOnly":true,"description":"With `proRata`, the difference charged (positive) or credited (negative)."},"orderId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The order the pro-rata difference went through."},"effectiveAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When it took, or will take, effect. Null for `nextVisit` until the visit."},"status":{"type":"string","readOnly":true,"enum":["scheduled","applied"]},"createdAt":{"type":"string","format":"date-time","readOnly":true}}},
"OrdersMembershipRenewal": {"type":"object","x-ticvai-persistence":"orders.membership_renewal","description":"**Taken from the backend workbook, 20 September.** Stores membership renewal transactions and the result of each renewal attempt.","required":["customerMembershipId","entitlementTemplateId","type","status","attemptedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"customerMembershipId":{"type":"string","format":"uuid","description":"The membership in the path. Taken from the path on `renewMembership`."},"entitlementTemplateId":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The order the renewal charged through. Set by the server."},"type":{"type":"string","maxLength":30},"status":{"type":"string","maxLength":30,"readOnly":true},"previousExpiryAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"newExpiryAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"Computed from the entitlement template's term and grace period."},"attemptedAt":{"type":"string","format":"date-time","readOnly":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"failureReason":{"type":"string","maxLength":500,"nullable":true,"readOnly":true}}}
}
```
